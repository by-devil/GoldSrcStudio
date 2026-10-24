"""Updates maps/ and skies/ from the GameBanana data embedded in bydevil.com.

Writes maps.json / skies.json for the site and README.md (English) +
README.tr.md (Turkish) for GitHub.

Usage:
  python .github/scripts/update_works.py               # downloads https://bydevil.com/
  python .github/scripts/update_works.py saved.html    # reads a saved copy of the page
"""
import json
import sys
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

SOURCE_URL = "https://bydevil.com/"
ROOT = Path(__file__).resolve().parents[2]


def load_page(arg):
    if arg:
        return Path(arg).read_text(encoding="utf-8")
    req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "GoldSrcStudio-works-updater"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def embedded_object(page, marker):
    """Returns the outermost JSON object that contains marker."""
    i = page.index(marker)
    start = i
    while True:
        start = page.rindex("{", 0, start)
        try:
            obj, end = json.JSONDecoder().raw_decode(page[start:])
        except ValueError:
            continue
        if start + end > i:
            return obj


def by_downloads(items):
    return sorted(items, key=lambda x: x.get("downloads", 0), reverse=True)


IMG_TIMEOUT = 30


def local_image(item, folder):
    """Stores the cover as <folder>/img/<id>.jpg; falls back to the remote URL on failure."""
    url = item.get("image")
    if not url or not item.get("id"):
        return url
    path = ROOT / folder / "img" / f"{item['id']}.jpg"
    if not path.exists():
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GoldSrcStudio-works-updater", "Referer": "https://bydevil.com/"})
            with urllib.request.urlopen(req, timeout=IMG_TIMEOUT) as r:
                body = r.read()
            if len(body) < 500:
                return url
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        except Exception as e:  # network error: keep the remote URL, retried on the next run
            print(f"Could not fetch image ({item['id']}): {e}")
            return url
    return f"/{folder}/img/{item['id']}.jpg"


def card(item):
    return {k: item.get(k) for k in ("name", "category", "downloads", "likes", "image", "url")}


def entry(item):
    """Short record for the list pages."""
    return card(item) | {"date": item.get("date"), "updated": item.get("updated")}


def fmt(n, lang="tr"):
    return f"{n:,}" if lang == "en" else f"{n:,}".replace(",", ".")


def day(ts, lang="tr"):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d" if lang == "en" else "%d.%m.%Y") if ts else "—"


LANGS = {"en": "README.md", "tr": "README.tr.md"}


def switch(lang):
    return "**English** · [Türkçe](README.tr.md)" if lang == "en" else "[English](README.md) · **Türkçe**"


def md_name(name):
    return name.replace("|", "\\|")


def rel(src):
    """Makes local images relative to the folder inside the README."""
    return src.split("/", 2)[2] if src and src.startswith(("/maps/", "/skies/")) else src


def gallery(items, lang):
    cells = [
        f'<td width="33%" valign="top"><a href="{m["url"]}"><img src="{rel(m["image"])}" alt=""></a><br>'
        f'<b>{m["name"]}</b><br><sub>⬇ {fmt(m.get("downloads", 0), lang)}</sub></td>'
        for m in items
    ]
    rows = ["<tr>" + "".join(cells[i:i + 3]) + "</tr>" for i in range(0, len(cells), 3)]
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def table(items, lang):
    head = "| Name | Downloads | Likes | Date |" if lang == "en" else "| Ad | İndirme | Beğeni | Tarih |"
    lines = [head, "| --- | ---: | ---: | --- |"]
    lines += [
        f'| [{md_name(m["name"])}]({m["url"]}) | {fmt(m.get("downloads", 0), lang)} | {m.get("likes", 0)} | {day(m.get("date"), lang)} |'
        for m in by_downloads(items)
    ]
    return "\n".join(lines)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def maps_files(maps):
    cats = Counter(m.get("category") or "Other" for m in maps)
    total = sum(m.get("downloads", 0) for m in maps)
    data = {
        "count": len(maps),
        "downloads": total,
        "categories": [{"name": n, "count": c} for n, c in cats.most_common()],
        "featured": [card(m) for m in by_downloads(maps)[:6]],
        "items": [entry(m) for m in by_downloads(maps)],
    }
    groups = defaultdict(list)
    for m in maps:
        groups[m.get("category") or "Other"].append(m)
    def readme(lang):
        L = lambda tr, en: en if lang == "en" else tr
        sections = "\n\n".join(f"### {name} ({cats[name]})\n\n{table(groups[name], lang)}" for name, _ in cats.most_common())
        return f"""{switch(lang)}

# {L("Haritalar", "Maps")}

{L(f"Counter-Strike 1.6 için **{len(maps)} harita** · toplam **{fmt(total)}** indirme.", f"**{len(maps)} maps** for Counter-Strike 1.6 · **{fmt(total, lang)}** downloads in total.")}
{L("Tüm haritalar ücretsizdir ve GameBanana üzerinden indirilir.", "All maps are free and download from GameBanana.")} → [bydevil.com/maps](https://bydevil.com/maps/)

## {L("En çok indirilenler", "Most downloaded")}

{gallery(data["featured"], lang)}

## {L("Oyun modları", "Game modes")}

{" · ".join(f"[{n}](#{n.lower().replace('/', '').replace(' ', '-')}-{c}) **{c}**" for n, c in cats.most_common())}

{sections}

---

<sub>{L("Bu sayfa her gün GameBanana verileriyle otomatik güncellenir.", "This page is updated automatically every day from GameBanana data.")}</sub>
"""
    changed = write(ROOT / "maps" / "maps.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    for lang, name in LANGS.items():
        changed |= write(ROOT / "maps" / name, readme(lang))
    return changed


def skies_files(skies):
    total = sum(s.get("downloads", 0) for s in skies)
    data = {
        "count": len(skies),
        "downloads": total,
        "featured": [card(s) | {"category": None} for s in by_downloads(skies)[:4]],
        "items": [entry(s) | {"category": None} for s in by_downloads(skies)],
    }
    def readme(lang):
        L = lambda tr, en: en if lang == "en" else tr
        return f"""{switch(lang)}

# {L("Skyboxlar", "Skyboxes")}

{L(f"Counter-Strike 1.6 ve GoldSrc için **{len(skies)} skybox** · toplam **{fmt(total)}** indirme.", f"**{len(skies)} skyboxes** for Counter-Strike 1.6 and GoldSrc · **{fmt(total, lang)}** downloads in total.")}
{L("Tüm skyboxlar ücretsizdir ve GameBanana üzerinden indirilir.", "All skyboxes are free and download from GameBanana.")} → [bydevil.com/skies](https://bydevil.com/skies/)

## {L("En çok indirilenler", "Most downloaded")}

{gallery([card(s) for s in by_downloads(skies)[:6]], lang)}

## {L("Tüm skyboxlar", "All skyboxes")}

{table(skies, lang)}

---

<sub>{L("Bu sayfa her gün GameBanana verileriyle otomatik güncellenir.", "This page is updated automatically every day from GameBanana data.")}</sub>
"""
    changed = write(ROOT / "skies" / "skies.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    for lang, name in LANGS.items():
        changed |= write(ROOT / "skies" / name, readme(lang))
    return changed


def main():
    page = load_page(sys.argv[1] if len(sys.argv) > 1 else None)
    maps = embedded_object(page, '"mapCount":')["maps"]
    skies = embedded_object(page, '"skies":[')["skies"]
    for m in maps:
        m["image"] = local_image(m, "maps")
    for s in skies:
        s["image"] = local_image(s, "skies")
    if len(maps) < 10 or len(skies) < 10:
        raise SystemExit(f"Unexpected data: {len(maps)} maps, {len(skies)} skyboxes")
    changed = maps_files(maps) | skies_files(skies)
    print(f"{'Updated' if changed else 'No changes'}: {len(maps)} maps, {len(skies)} skyboxes")


if __name__ == "__main__":
    main()
