"""bydevil.com'a gömülü GameBanana verisinden maps/ ve skies/ klasörlerini günceller.

Kullanım:
  python .github/scripts/update_works.py               # https://bydevil.com/ adresinden indirir
  python .github/scripts/update_works.py kayit.html    # kaydedilmiş bir sayfadan okur
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
    """marker'ı içeren en dıştaki JSON nesnesini döndürür."""
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
    """Kapak resmini <folder>/img/<id>.jpg olarak saklar; başarısız olursa uzak adresi döndürür."""
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
        except Exception as e:  # ağ hatası: uzak adres kullanılır, bir sonraki çalışmada yeniden denenir
            print(f"Resim alınamadı ({item['id']}): {e}")
            return url
    return f"/{folder}/img/{item['id']}.jpg"


def card(item):
    return {k: item.get(k) for k in ("name", "category", "downloads", "likes", "image", "url")}


def entry(item):
    """Liste sayfaları için kısa kayıt."""
    return card(item) | {"date": item.get("date"), "updated": item.get("updated")}


def fmt(n):
    return f"{n:,}".replace(",", ".")


def day(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%d.%m.%Y") if ts else "—"


def md_name(name):
    return name.replace("|", "\\|")


def rel(src):
    """README içinde yerel resimleri klasöre göre göreli yap."""
    return src.split("/", 2)[2] if src and src.startswith(("/maps/", "/skies/")) else src


def gallery(items):
    cells = [
        f'<td width="33%" valign="top"><a href="{m["url"]}"><img src="{rel(m["image"])}" alt=""></a><br>'
        f'<b>{m["name"]}</b><br><sub>⬇ {fmt(m.get("downloads", 0))}</sub></td>'
        for m in items
    ]
    rows = ["<tr>" + "".join(cells[i:i + 3]) + "</tr>" for i in range(0, len(cells), 3)]
    return "<table>\n" + "\n".join(rows) + "\n</table>"


def table(items):
    lines = ["| Ad | İndirme | Beğeni | Tarih |", "| --- | ---: | ---: | --- |"]
    lines += [
        f'| [{md_name(m["name"])}]({m["url"]}) | {fmt(m.get("downloads", 0))} | {m.get("likes", 0)} | {day(m.get("date"))} |'
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
    cats = Counter(m.get("category") or "Diğer" for m in maps)
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
        groups[m.get("category") or "Diğer"].append(m)
    sections = "\n\n".join(
        f"### {name} ({cats[name]})\n\n{table(groups[name])}" for name, _ in cats.most_common()
    )
    readme = f"""# Haritalar

Counter-Strike 1.6 için **{len(maps)} harita** · toplam **{fmt(total)}** indirme.
Tüm haritalar ücretsizdir ve GameBanana üzerinden indirilir. → [bydevil.com/maps](https://bydevil.com/maps/)

## En çok indirilenler

{gallery(data["featured"])}

## Oyun modları

{" · ".join(f"[{n}](#{n.lower().replace('/', '').replace(' ', '-')}-{c}) **{c}**" for n, c in cats.most_common())}

{sections}

---

<sub>Bu sayfa her gün GameBanana verileriyle otomatik güncellenir.</sub>
"""
    a = write(ROOT / "maps" / "maps.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    b = write(ROOT / "maps" / "README.md", readme)
    return a or b


def skies_files(skies):
    total = sum(s.get("downloads", 0) for s in skies)
    data = {
        "count": len(skies),
        "downloads": total,
        "featured": [card(s) | {"category": None} for s in by_downloads(skies)[:4]],
        "items": [entry(s) | {"category": None} for s in by_downloads(skies)],
    }
    readme = f"""# Skyboxlar

Counter-Strike 1.6 ve GoldSrc için **{len(skies)} skybox** · toplam **{fmt(total)}** indirme.
Tüm skyboxlar ücretsizdir ve GameBanana üzerinden indirilir. → [bydevil.com/skies](https://bydevil.com/skies/)

## En çok indirilenler

{gallery([card(s) for s in by_downloads(skies)[:6]])}

## Tüm skyboxlar

{table(skies)}

---

<sub>Bu sayfa her gün GameBanana verileriyle otomatik güncellenir.</sub>
"""
    a = write(ROOT / "skies" / "skies.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    b = write(ROOT / "skies" / "README.md", readme)
    return a or b


def main():
    page = load_page(sys.argv[1] if len(sys.argv) > 1 else None)
    maps = embedded_object(page, '"mapCount":')["maps"]
    skies = embedded_object(page, '"skies":[')["skies"]
    for m in maps:
        m["image"] = local_image(m, "maps")
    for s in skies:
        s["image"] = local_image(s, "skies")
    if len(maps) < 10 or len(skies) < 10:
        raise SystemExit(f"Beklenmeyen veri: {len(maps)} harita, {len(skies)} skybox")
    changed = maps_files(maps) | skies_files(skies)
    print(f"{'Güncellendi' if changed else 'Değişiklik yok'}: {len(maps)} harita, {len(skies)} skybox")


if __name__ == "__main__":
    main()
