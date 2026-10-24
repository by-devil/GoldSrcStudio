"""Writes the GitHub release notes of every tool from tools/tools.json (English + Turkish).

Usage:
  python .github/scripts/release_notes.py           # prints the notes
  python .github/scripts/release_notes.py --apply   # updates the releases (needs the gh CLI and GH_TOKEN)

Beta / test versions are marked as pre-releases; the newest stable one becomes "Latest".
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = 'https://tools.bydevil.com'
ISSUES = 'https://github.com/by-devil/GoldSrcStudio/issues/new/choose'

TEXT = {
    'en': {
        'features': 'Key features', 'download': 'Download', 'file': 'File', 'size': 'Size', 'platform': 'Platform',
        'install': 'Installation', 'verify': 'Verify the download', 'links': 'Links', 'website': 'Website',
        'bug': 'Report a bug', 'beta': 'This is a beta build. Back up your files before editing them.',
        'exe': ['Download **{file}** from the assets below.', 'Run the installer and follow the steps.',
                'If Windows SmartScreen appears, click **More info → Run anyway** (the installer is not code-signed).'],
        'zip': ['Download **{file}** from the assets below.', 'Extract the ZIP to a folder.',
                'Run the `.exe` inside. If Windows SmartScreen appears, click **More info → Run anyway**.'],
        'certutil': 'In PowerShell or Command Prompt:',
    },
    'tr': {
        'features': 'Öne çıkan özellikler', 'download': 'İndir', 'file': 'Dosya', 'size': 'Boyut', 'platform': 'Platform',
        'install': 'Kurulum', 'verify': 'İndirmeyi doğrula', 'links': 'Bağlantılar', 'website': 'Web sitesi',
        'bug': 'Hata bildir', 'beta': 'Bu bir beta sürümüdür. Dosyalarını düzenlemeden önce yedekle.',
        'exe': ['Aşağıdaki dosyalardan **{file}** dosyasını indir.', 'Kurulumu çalıştır ve adımları izle.',
                'Windows SmartScreen uyarısı çıkarsa **Ek bilgi → Yine de çalıştır**\'a tıkla (kurulum dosyası imzalı değildir).'],
        'zip': ['Aşağıdaki dosyalardan **{file}** dosyasını indir.', 'ZIP dosyasını bir klasöre çıkar.',
                'İçindeki `.exe` dosyasını çalıştır. Windows SmartScreen uyarısı çıkarsa **Ek bilgi → Yine de çalıştır**\'a tıkla.'],
        'certutil': 'PowerShell veya Komut İstemi\'nde:',
    },
}


def is_beta(t):
    return any(w in t['version'].lower() for w in ('beta', 'test'))


def body(t, lang):
    x = TEXT[lang]
    t = {**t, **t['en']} if lang == 'en' else t
    file = t['download'].split('/')[-1]
    steps = '\n'.join(f'{i}. {s.format(file=file)}' for i, s in enumerate(x['zip' if file.endswith('.zip') else 'exe'], 1))
    note = f'\n> [!NOTE]\n> {t["note"]}\n' if t.get('note') else ''
    beta = f'\n> [!WARNING]\n> {x["beta"]}\n' if is_beta(t) else ''
    return f"""**{t['summary']}**

{t['description']}

### {x['features']}

{chr(10).join('- ' + f for f in t['features'])}

### {x['download']}

| {x['file']} | {x['size']} | {x['platform']} |
| --- | --- | --- |
| [{file}]({t['download']}) | {t['size'] / 1048576:.1f} MB | {t['platform']} |
{note}{beta}
### {x['install']}

{steps}

### {x['verify']}

{x['certutil']}

```
certutil -hashfile {file} SHA256
```

SHA-256: `{t['sha256']}`

### {x['links']}

[{x['website']}]({SITE}/tools/{t['slug']}/) · [GameBanana]({t['gamebanana']}) · [{x['bug']}]({ISSUES})"""


def notes(t):
    return f"""<p align="center"><img src="{SITE}{t['image']}" alt="{t['name']}" width="820"></p>

{body(t, 'en')}

<details>
<summary><b>🇹🇷 Türkçe</b></summary>

{body(t, 'tr')}

</details>
"""


def main():
    tools = json.load(open(ROOT / 'tools' / 'tools.json', encoding='utf-8'))
    stable = [t for t in tools if not is_beta(t)]
    latest = stable[0]['slug'] if stable else None
    for t in tools:
        tag = t['download'].split('/download/', 1)[1].split('/')[0]
        text = notes(t)
        if '--apply' not in sys.argv:
            print(f'===== {tag}\n{text}')
            continue
        path = ROOT / f'.release-{tag}.md'
        path.write_text(text, encoding='utf-8')
        cmd = ['gh', 'release', 'edit', tag, '--title', f"{t['name']} {t['version']}", '--notes-file', str(path),
               f'--prerelease={str(is_beta(t)).lower()}']
        if t['slug'] == latest:
            cmd.append('--latest')
        subprocess.run(cmd, check=True)
        path.unlink()
        print('updated', tag)


if __name__ == '__main__':
    main()
