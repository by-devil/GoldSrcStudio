"""AMXX eklentilerinin ekran görüntülerini bydevil.com'dan assets/plugins/ altına indirir.

Kullanım: python .github/scripts/fetch_plugin_images.py
Var olan dosyalar yeniden indirilmez.
"""
import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://bydevil.com/assets/'

def seq(folder, prefix, n, ext='jpg'):
    return [f'{folder}/{prefix}-{i:02d}.{ext}' for i in range(1, n + 1)]

FILES = [
    *[f'propublic/pp-{n}.jpg' for n in ['1-top15', '2-toptime', '3-profil', '4-steam-profil', '5-steam-bilgi', '6-fungun', '7-avatar', '8-arayuz']],
    *seq('royalpass', 'rp', 17),
    *seq('takim', 'tk', 9),
    *seq('zp-top15', 'zp', 12),
    *seq('battlepass-public', 'bpp', 10),
    *seq('battlepass-zp', 'bpz', 9),
    'gungame-top15/el-sonu.webp',
    'gungame-top15/mac-sonu-bireysel.jpg',
]

ok = fail = 0
for f in FILES:
    out = ROOT / 'assets' / 'plugins' / f
    if out.exists():
        continue
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(BASE + f, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=30).read()
        out.write_bytes(data)
        ok += 1
    except Exception as e:
        print(f'İndirilemedi: {f} ({e})')
        fail += 1
print(f'{ok} indirildi, {fail} hata')
