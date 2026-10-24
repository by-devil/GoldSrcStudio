"""bydevil.com'a gömülü GameBanana verisinden data/works.json dosyasını üretir.

Kullanım:
  python scripts/update_works.py                 # https://bydevil.com/ adresinden indirir
  python scripts/update_works.py kayit.html      # kaydedilmiş bir sayfadan okur
"""
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

SOURCE_URL = "https://bydevil.com/"
OUT = Path(__file__).resolve().parent.parent / "data" / "works.json"

PLUGINS = [
    "Pro Public TOP15", "Royal Pass", "Team System", "GunGame TOP15",
    "Zombie Plague TOP15", "Public Battle Pass", "Zombie Plague Battle Pass",
]


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


def card(item, category=None):
    return {
        "name": item["name"],
        "category": category or item.get("category"),
        "downloads": item.get("downloads", 0),
        "likes": item.get("likes", 0),
        "image": item.get("image"),
        "url": item["url"],
    }


def build(page):
    maps = embedded_object(page, '"mapCount":')["maps"]
    skies = embedded_object(page, '"skies":[')["skies"]
    if len(maps) < 10 or len(skies) < 10:
        raise SystemExit(f"Beklenmeyen veri: {len(maps)} harita, {len(skies)} skybox")

    by_dl = lambda xs: sorted(xs, key=lambda x: x.get("downloads", 0), reverse=True)
    cats = Counter(m.get("category") or "Diğer" for m in maps)
    return {
        "maps": {
            "count": len(maps),
            "downloads": sum(m.get("downloads", 0) for m in maps),
            "categories": [{"name": n, "count": c} for n, c in cats.most_common()],
            "featured": [card(m) for m in by_dl(maps)[:6]],
        },
        "skies": {
            "count": len(skies),
            "downloads": sum(s.get("downloads", 0) for s in skies),
            "featured": [card(s, "Skybox") for s in by_dl(skies)[:4]],
        },
        "plugins": {"status": "Yakında", "items": PLUGINS},
    }


def main():
    data = build(load_page(sys.argv[1] if len(sys.argv) > 1 else None))
    new = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if OUT.exists() and OUT.read_text(encoding="utf-8") == new:
        print("Değişiklik yok.")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(new, encoding="utf-8")
    print(f"Güncellendi: {data['maps']['count']} harita, {data['skies']['count']} skybox")


if __name__ == "__main__":
    main()
