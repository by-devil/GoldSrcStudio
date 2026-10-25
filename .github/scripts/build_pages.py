"""Builds the site's HTML pages and the repository READMEs (Turkish + English).

Usage: python .github/scripts/build_pages.py
Run it again whenever site.css / site.js, tools/tools.json or plugins/plugins.json
change: asset URLs get a content hash so browsers never use a stale copy.

Pages: every text is written in both languages. T('tr', 'en') emits two
<span data-l> elements and site.css shows the selected one (html[data-lang]).
The choice is kept in localStorage as "gs-lang"; ?lang=en / ?lang=tr also works.

READMEs: README.md (English) and README.tr.md (Turkish) in every folder.

Tool installers live in GitHub Releases, not in the repository. For a new
version: create a release on GitHub with the installer attached, then set
"download", "size" (bytes) and "sha256" for the tool in tools/tools.json.
"""
import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
tools = json.load(open('tools/tools.json', encoding='utf-8'))
_js = open('assets/site.js', encoding='utf-8').read()
STEAM = re.search(r"const STEAM = '(<svg.*?</svg>)';", _js).group(1)
DISCORD = re.search(r"const DISCORD = '(<svg.*?</svg>)';", _js).group(1)
VER = hashlib.sha1(open('assets/site.css', 'rb').read() + _js.encode()).hexdigest()[:8]

# Theme and language are set before first paint to avoid a flash.
HEAD_JS = ('(function(d){var t="original",l="";try{var q=/[?&]lang=(tr|en)/.exec(location.search);'
           'if(q)localStorage.setItem("gs-lang",q[1]);t=localStorage.getItem("gs-theme")||t;l=localStorage.getItem("gs-lang")||""}catch(e){}'
           'if(!l)l=/^tr/i.test(navigator.language||"tr")?"tr":"en";d.dataset.theme=t;d.dataset.lang=l;d.lang=l})(document.documentElement)')

def T(tr, en):
    return f'<span data-l="tr">{tr}</span><span data-l="en">{en}</span>'

def IC(paths):
    return f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">{paths}</svg>'

ICON = {
    'tool': IC('<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
    'map': IC('<path d="m9 4-5 2v14l5-2 6 2 5-2V4l-5 2-6-2zM9 4v14M15 6v14"/>'),
    'cloud': IC('<path d="M7 18a4 4 0 0 1-.6-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z"/>'),
    'plug': IC('<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0V8zM12 17v4"/>'),
}

SITE = 'https://tools.bydevil.com'

def page_url(path):
    return '/' + path[:-len('index.html')] if path.endswith('index.html') else '/' + path

def shell(path, page, title, desc, body, slug=None, image='/assets/map-optimization.jpg'):
    """title and desc are (tr, en) pairs."""
    url = SITE + page_url(path)
    alt = '' if page == 'notfound' else f'''
  <link rel="alternate" hreflang="tr" href="{url}?lang=tr">
  <link rel="alternate" hreflang="en" href="{url}?lang=en">
  <link rel="alternate" hreflang="x-default" href="{url}">'''
    html = f'''<!doctype html>
<!-- © GoldSrc Studio · by Devil. Tasarım ve içerik izinsiz kopyalanamaz / Design and content may not be copied without permission. -->
<html lang="tr" data-theme="original" data-lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title[0]}</title>
  <meta name="description" content="{desc[0]}">
  <meta name="theme-color" content="#0d141c">
  <meta name="author" content="GoldSrc Studio · by Devil">
  <meta name="copyright" content="© GoldSrc Studio · by Devil. Tüm hakları saklıdır / All rights reserved.">
  <script>{HEAD_JS}</script>
  <meta property="og:title" content="{title[0]}">
  <meta property="og:description" content="{desc[0]}">
  <meta property="og:image" content="https://tools.bydevil.com{image}">
  <link rel="icon" type="image/png" href="/assets/goldsrc-mark.png">{alt}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css?v={VER}">
  <script src="/assets/site.js?v={VER}" defer></script>
</head>
<body data-page="{page}"{f' data-slug="{slug}"' if slug else ''} data-title-en="{title[1]}" data-desc-en="{desc[1]}">
  <header id="hdr"></header>
  <main>
{body}
  </main>
  <footer id="ftr"></footer>
</body>
</html>
'''
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)

def head(crumb, h1, lead, right=''):
    c = f'<nav class="crumbs"><a href="/">{T("Ana sayfa", "Home")}</a><span class="sep">/</span><span>{crumb}</span></nav>' if crumb else ''
    return f'''    <div class="page-head"><div class="wrap">
      {c}
      <div class="page-head-row">
        <div><h1>{h1}</h1><p class="lead">{lead}</p></div>
        {right}
      </div>
    </div></div>'''

CTA_CONTACT = T('İletişime geç', 'Get in touch')

# Home
shell('index.html', 'home',
  ('GoldSrc Studio — CS 1.6 araçları, haritaları, skyboxları ve eklentileri', 'GoldSrc Studio — CS 1.6 tools, maps, skyboxes and plugins'),
  ('Counter-Strike 1.6 ve GoldSrc için modlama araçları, haritalar, skyboxlar ve AMXX eklentileri tek çatı altında.',
   'Modding tools, maps, skyboxes and AMXX plugins for Counter-Strike 1.6 and GoldSrc, all under one roof.'), f'''    <section class="hero">
      <div class="hero-media"><img src="/assets/map-optimization.jpg" alt=""></div>
      <div class="wrap hero-inner">
        <span class="eyebrow"><i></i>{T('Araçlar · Haritalar · Skyboxlar · AMXX eklentileri', 'Tools · Maps · Skyboxes · AMXX plugins')}</span>
        <h1>{T('<span lang="en">Counter-Strike 1.6</span> için <span class="accent">her şey</span>, tek çatı altında.',
               '<span class="accent">Everything</span> for Counter-Strike 1.6, under one roof.')}</h1>
        <p class="lead">{T('Modlama araçları, ücretsiz haritalar ve skyboxlar, sunucular için AMXX eklentileri. Haritanı analiz et, modelini boya, sunucunu güçlendir.',
                           'Modding tools, free maps and skyboxes, and AMXX plugins for servers. Analyse your map, paint your model, power up your server.')}</p>
        <div class="actions hero-actions">
          <a class="btn primary" href="/tools/">{ICON['tool']}{T('Araçlar', 'Tools')}</a>
          <a class="btn" href="/maps/">{ICON['map']}{T('Haritalar', 'Maps')}</a>
          <a class="btn" href="/skies/">{ICON['cloud']}{T('Skyboxlar', 'Skyboxes')}</a>
          <a class="btn" href="/plugins/">{ICON['plug']}{T('Eklentiler', 'Plugins')}</a>
        </div>
        <div class="hero-stats" id="stats"></div>
      </div>
    </section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>{T('Araçlar', 'Tools')}</h2></div><a class="more" href="/tools/">{T('Tüm araçlar →', 'All tools →')}</a></div>
      <div class="grid cols-3" id="home-tools"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>{T('En çok indirilen haritalar', 'Most downloaded maps')}</h2></div><a class="more" href="/maps/">{T('Tüm haritalar →', 'All maps →')}</a></div>
      <div class="grid cols-4" id="home-maps"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>{T('Popüler skyboxlar', 'Popular skyboxes')}</h2></div><a class="more" href="/skies/">{T('Tüm skyboxlar →', 'All skyboxes →')}</a></div>
      <div class="grid cols-4" id="home-skies"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>{T('AMXX eklentileri', 'AMXX plugins')}</h2></div><a class="more" href="/plugins/">{T('Tüm eklentiler →', 'All plugins →')}</a></div>
      <div class="grid cols-3" id="home-plugins"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="cta-band"><div><h2>{T('Bir fikrin ya da hata bildirimin mi var?', 'Got an idea or a bug report?')}</h2><p>{T('Steam, Discord veya GameBanana üzerinden ulaş.', 'Reach out on Steam, Discord or GameBanana.')}</p></div>
        <div class="actions"><a class="btn primary" href="/contact/">{CTA_CONTACT}</a><a class="btn" href="https://github.com/by-devil/GoldSrcStudio/issues" target="_blank" rel="noopener">{T('Hata bildir ↗', 'Report a bug ↗')}</a></div></div>
    </div></section>''', image='/assets/social-preview.png')

# Tools
shell('tools/index.html', 'tools', ('Araçlar — GoldSrc Studio', 'Tools — GoldSrc Studio'),
  ('GoldSrc ve CS 1.6 için ücretsiz Windows araçları.', 'Free Windows tools for GoldSrc and CS 1.6.'),
  head(T('Araçlar', 'Tools'), T('Araçlar', 'Tools'),
       T('<span class="tool-count">5</span> bağımsız uygulama. Hepsi Windows için, ücretsiz; indirme dosyaları doğrudan bu siteden ve GameBanana\'dan.',
         '<span class="tool-count">5</span> standalone apps. All free and for Windows; downloads straight from this site and from GameBanana.')) + '''
    <section class="section"><div class="wrap"><div class="grid cols-3" id="tool-grid"></div></div></section>''')

for t in tools:
    en = t.get('en', {})
    shell(f'tools/{t["slug"]}/index.html', 'tool', (f'{t["name"]} — GoldSrc Studio',) * 2,
          (t['summary'], en.get('summary', t['summary'])), '', slug=t['slug'], image=t['image'])

def list_page(path, page, title, desc, h1, lead, chips, placeholder):
    right = f'''<div class="stats" style="grid-template-columns:repeat(2,minmax(150px,1fr));min-width:min(100%,340px)">
          <div class="stat"><b id="list-count">—</b><span>{T('Toplam', 'Total')}</span></div><div class="stat"><b id="list-dl">—</b><span>{T('İndirme', 'Downloads')}</span></div></div>'''
    shell(path, page, title, desc, head(h1, h1, lead, right) + f'''
    <section class="section"><div class="wrap">
      {'<div class="chips" id="chips"></div>' if chips else ''}
      <div class="toolbar">
        <label class="field"><svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="{placeholder[0]}" data-en-placeholder="{placeholder[1]}" autocomplete="off"></label>
        <select class="select" id="sort" aria-label="Sırala" data-en-aria-label="Sort">
          <option value="downloads" data-en="Most downloaded">En çok indirilen</option><option value="likes" data-en="Most liked">En çok beğenilen</option><option value="new" data-en="Newest">En yeni</option><option value="az">A → Z</option>
        </select>
        <span class="count-note" id="result-note"></span>
      </div>
      <div class="grid cols-4" id="list-grid"></div>
      <div class="load-more"><button class="btn" id="more" type="button">{T('Daha fazla göster', 'Show more')}</button></div>
    </div></section>''')

list_page('maps/index.html', 'maps', ('Haritalar — GoldSrc Studio', 'Maps — GoldSrc Studio'),
  ('Counter-Strike 1.6 için ücretsiz haritalar.', 'Free maps for Counter-Strike 1.6.'), T('Haritalar', 'Maps'),
  T('Base Builder, Gun Game, Zombie Mod ve daha fazlası. Tüm haritalar ücretsiz ve GameBanana üzerinden indirilir.',
    'Base Builder, Gun Game, Zombie Mod and more. All maps are free and download from GameBanana.'),
  True, ('Harita ara… (ör. dust2)', 'Search maps… (e.g. dust2)'))
list_page('skies/index.html', 'skies', ('Skyboxlar — GoldSrc Studio', 'Skyboxes — GoldSrc Studio'),
  ('GoldSrc ve CS 1.6 için skybox paketleri.', 'Skybox packs for GoldSrc and CS 1.6.'), T('Skyboxlar', 'Skyboxes'),
  T('Counter-Strike 1.6 ve GoldSrc için gökyüzü paketleri. Tümü ücretsiz ve GameBanana üzerinden indirilir.',
    'Sky packs for Counter-Strike 1.6 and GoldSrc. All free and downloaded from GameBanana.'),
  False, ('Skybox ara…', 'Search skyboxes…'))

shell('plugins/index.html', 'plugins', ('AMXX eklentileri — GoldSrc Studio', 'AMXX plugins — GoldSrc Studio'),
  ('Counter-Strike 1.6 sunucuları için AMX Mod X eklentileri.', 'AMX Mod X plugins for Counter-Strike 1.6 servers.'),
  head(T('Eklentiler', 'Plugins'), T('AMXX eklentileri', 'AMXX plugins'),
       T('Counter-Strike 1.6 sunucuları için sıralama, sezon ve ekonomi sistemleri. Ekran görüntüleri ve ayrıntılar için bir eklenti seç.',
         'Ranking, season and economy systems for Counter-Strike 1.6 servers. Pick a plugin for screenshots and details.')) + f'''
    <section class="section"><div class="wrap">
      <div class="grid cols-3" id="plugin-grid"></div>
      <div class="cta-band" style="margin-top:28px"><div><h2>{T('Sunucun için eklenti mi lazım?', 'Need a plugin for your server?')}</h2><p>{T('Fiyat ve kurulum için yaz.', 'Write for pricing and installation.')}</p></div>
        <div class="actions"><a class="btn primary" href="/contact/">{CTA_CONTACT}</a><a class="btn" href="https://bydevil.com/plugins/" target="_blank" rel="noopener">bydevil.com/plugins ↗</a></div></div>
    </div></section>''')

# MOTD kits: each kit's files live in kits/<slug>/<folder>/; a zip with fixed timestamps is
# built from them (same bytes every run) and its name, size, hash and contents go to kits.json.
kits = json.load(open('kits/kits.json', encoding='utf-8'))
for k in kits:
    base = f'kits/{k["slug"]}'
    files = sorted(os.path.relpath(os.path.join(d, f), base).replace(os.sep, '/')
                   for d, _, fs in os.walk(f'{base}/{k["folder"]}') for f in fs)
    zpath = f'{base}/{k["file"]["name"]}'
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for f in files:
            info = zipfile.ZipInfo(f, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, open(f'{base}/{f}', 'rb').read())
    data = open(zpath, 'rb').read()
    k['file'] = {'name': k['file']['name'], 'size': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                 'contents': [f.split('/', 1)[1] for f in files]}
with open('kits/kits.json', 'w', encoding='utf-8') as fp:
    json.dump(kits, fp, ensure_ascii=False, indent=2)
    fp.write('\n')

shell('kits/index.html', 'kits', ('MOTD kitleri — GoldSrc Studio', 'MOTD kits — GoldSrc Studio'),
  ('CS 1.6 web MOTD panellerini her çözünürlükte ve CSDurağı istemcisinde düzgün gösteren ücretsiz kitler.',
   'Free kits that make CS 1.6 web MOTD panels work at every resolution and in the CSDurağı client.'),
  head(T('Kitler', 'Kits'), T('MOTD kitleri', 'MOTD kits'),
       T('Web MOTD panellerini her çözünürlükte ve CSDurağı istemcisinde düzgün gösteren küçük, ücretsiz kitler. Dosyalar şifresiz; GitHub\'da da açık.',
         'Small, free kits that make web MOTD panels work at every resolution and in the CSDurağı client. No passwords; the files are also open on GitHub.')) + f'''
    <section class="section"><div class="wrap">
      <div class="kit-list" id="kit-list"></div>
      <div class="cta-band" style="margin-top:28px"><div><h2>{T('MOTD paneliniz mi bozuk?', 'Is your MOTD panel broken?')}</h2><p>{T('Sunucuna özel düzenleme için yaz.', 'Write for a custom fix for your server.')}</p></div>
        <div class="actions"><a class="btn primary" href="/contact/">{CTA_CONTACT}</a></div></div>
    </div></section>''', image=f'/kits/{kits[0]["slug"]}/{kits[0]["shots"][0]["file"]}')

shell('contact/index.html', 'contact', ('İletişim — GoldSrc Studio', 'Contact — GoldSrc Studio'),
  ('Steam, Discord ve GameBanana üzerinden iletişim.', 'Get in touch on Steam, Discord and GameBanana.'),
  head(T('İletişim', 'Contact'), T('Bir fikrin mi var? <span class="accent">Konuşalım.</span>', 'Got an idea? <span class="accent">Let\'s talk.</span>'),
       T('Araç geri bildirimi, harita önerisi, AMXX fikirleri ya da sadece selam vermek için. Doğrudan mesaj için en hızlı yol Steam.',
         'Tool feedback, map suggestions, AMXX ideas or just to say hi. Steam is the fastest way to send a direct message.')) + f'''
    <section class="section"><div class="wrap">
      <div class="contact-grid">
        <a class="contact-card steam" href="https://steamcommunity.com/id/SODEJ/" target="_blank" rel="noopener">
          <span class="ci">{STEAM}</span><span><b>Steam</b><small>{T('Doğrudan mesaj için en hızlı yol', 'Fastest way to send a direct message')}</small></span><span class="go">↗</span></a>
        <button class="contact-card discord" type="button" id="discord-copy">
          <span class="ci">{DISCORD}</span><span><b>Discord</b><small id="discord-note">{T('serhatondes · kopyalamak için tıkla', 'serhatondes · click to copy')}</small></span><span class="go">⧉</span></button>
        <a class="contact-card" href="https://gamebanana.com/members/1419476" target="_blank" rel="noopener">
          <span class="ci"><img src="/assets/gamebanana.png" alt=""></span><span><b>GameBanana</b><small>{T('Tüm haritalar, skyboxlar ve araçlar', 'All maps, skyboxes and tools')}</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://github.com/by-devil/GoldSrcStudio/issues" target="_blank" rel="noopener">
          <span class="ci"><svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></span><span><b>GitHub</b><small>{T('Hata bildirimi ve öneriler', 'Bug reports and suggestions')}</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://fpslist.com/" target="_blank" rel="noopener">
          <span class="ci"><img class="full" src="/assets/fpslist.svg" alt=""></span><span><b>FPSList</b><small>{T('Oyun sunucu listesi', 'Game server list')}</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://bydevil.com/" target="_blank" rel="noopener">
          <span class="ci"><img class="full" src="/assets/bydevil-mark.png" alt="" style="padding:6px"></span><span><b>bydevil.com</b><small>{T('Haritalar, skyboxlar ve kitler', 'Maps, skyboxes and kits')}</small></span><span class="go">↗</span></a>
      </div>
    </div></section>''')

LEGACY = json.dumps({t['legacyDownload']: t['download'] for t in tools if t.get('legacyDownload')})
shell('404.html', 'notfound', ('Sayfa bulunamadı — GoldSrc Studio', 'Page not found — GoldSrc Studio'),
  ('Aradığın sayfa bulunamadı.', 'The page you are looking for could not be found.'), f'''    <script>(function(m){{var u=m[location.pathname];if(u)location.replace(u)}})({LEGACY})</script>
    <section class="section"><div class="wrap" style="text-align:center;padding:60px 0">
      <span class="eyebrow"><i></i>404</span>
      <h1 style="margin:18px 0 10px;font-size:40px;font-weight:800;letter-spacing:-.03em">{T('Bu sayfa bulunamadı.', 'This page could not be found.')}</h1>
      <p style="color:var(--text-2)">{T('Aradığın şey taşınmış olabilir. Hızlı arama için <span class="kbd">/</span> tuşuna bas.', 'It may have moved. Press <span class="kbd">/</span> for quick search.')}</p>
      <div class="actions" style="justify-content:center;margin-top:24px"><a class="btn primary" href="/">{T('Ana sayfa', 'Home')}</a><a class="btn" href="/tools/">{T('Araçlar', 'Tools')}</a></div>
    </div></section>''')
# ---------- READMEs ----------
plugins = json.load(open('plugins/plugins.json', encoding='utf-8'))
maps = json.load(open('maps/maps.json', encoding='utf-8'))
skies = json.load(open('skies/skies.json', encoding='utf-8'))
LANGS = {'en': 'README.md', 'tr': 'README.tr.md'}

def loc(item, lang):
    """Item with its English fields applied for lang == 'en'."""
    return {**item, **item.get('en', {})} if lang == 'en' else item

def num(n, lang):
    return f'{n:,}'.replace(',', ',' if lang == 'en' else '.')

def switch(lang):
    return '**English** · [Türkçe](README.tr.md)' if lang == 'en' else '[English](README.md) · **Türkçe**'

def readme(folder, make):
    for lang, name in LANGS.items():
        open(os.path.join(folder, name), 'w', encoding='utf-8').write(make(lang, lambda tr, en: en if lang == 'en' else tr))

def rows(cells, per):
    return '\n'.join('<tr>' + ''.join(cells[i:i + per]) + '</tr>' for i in range(0, len(cells), per))

def plugin_cell(p, lang, L, base=''):
    p = loc(p, lang)
    cover = p['shots'][p['cover']]['file']
    return (f'<td width="33%" valign="top"><a href="{base}{p["slug"]}"><img src="{base}{p["slug"]}/{cover}" alt="{p["name"]}"></a><br>'
            f'<b><a href="{base}{p["slug"]}">{p["name"]}</a></b> · <sub>{len(p["shots"])} {L("ekran görüntüsü", "screenshots")}</sub><br>{p["text"]}</td>')

def tool_file(t):
    return t['download'].split('/')[-1], f'{t["size"] / 1048576:.1f} MB', t['sha256']

def low(text):
    """Lower-cases the first letter of a list item joined mid-sentence (keeps acronyms like NAV)."""
    return text if text[1:2].isupper() else ('i' if text[0] == 'İ' else text[0].lower()) + text[1:]

def tool_cell(t, lang, L):
    t = loc(t, lang)
    file = tool_file(t)[0]
    links = [f'<a href="{t["download"]}"><b>⬇ {L("İndir", "Download")}</b></a>', f'<a href="{t["gamebanana"]}">GameBanana →</a>']
    if t.get('repo'):
        links.append(f'<a href="{t["repo"]}">GitHub →</a>')
    return (f'<td width="50%" valign="top"><img src="{t["image"][1:]}" alt="{t["name"]}"><br>'
            f'<b><a href="tools/{t["slug"]}">{t["name"]}</a></b> · <sub>{t["version"]} · {t["platform"]}</sub><br>'
            f'{t["summary"]} {", ".join(low(f) if i else f for i, f in enumerate(t["features"][:3]))}.<br>{" · ".join(links)}</td>')

for t in tools:
    def tool_readme(lang, L, t=t):
        t = loc(t, lang)
        file, size, sha = tool_file(t)
        links = [f'[GameBanana]({t["gamebanana"]})'] + ([f'[GitHub]({t["repo"]})'] if t.get('repo') else [])
        manual = (f'\n<details>\n<summary><b>{L("Kullanım kılavuzu", "User manual")}</b></summary>\n\n```\n{t["manual"]}\n```\n\n</details>\n'
                  if t.get('manual') else '')
        return f"""{switch(lang)}

# {t['name']}

**{t['summary']}**

![{t['name']}](../../{t['image'][1:]})

{t['description']}

## {L('Öne çıkan özellikler', 'Key features')}

{chr(10).join('- ' + f for f in t['features'])}

## {L('Bilgiler', 'Details')}

| | |
| --- | --- |
| {L('Kategori', 'Category')} | {t['category']} |
| {L('Sürüm', 'Version')} | {t['version']} |
| Platform | {t['platform']} |
| {L('Dosya türleri', 'File types')} | `{t['fileTypes']}` |
| {L('Son güncelleme', 'Last updated')} | {t['updated']} |

## {L('İndir', 'Download')}

**[⬇ {file}]({t['download']})** · {size}

<sub>SHA-256: `{sha}`</sub>
{f'{chr(10)}> ℹ️ {t["note"]}{chr(10)}' if t.get('note') else ''}
{L('Diğer bağlantılar', 'Other links')}: {' · '.join(links)}
{manual}
> {L('Araçlar beta aşamasındadır. Dosyalarını düzenlemeden önce yedeklemeni öneririz.', 'The tools are in beta. We recommend backing up your files before editing them.')}

[← {L('Tüm araçlar', 'All tools')}](../../{LANGS[lang]})
"""
    readme(f'tools/{t["slug"]}', tool_readme)

for p in plugins:
    def plugin_readme(lang, L, p=p):
        p = loc(p, lang)
        shots = '\n'.join(f'### {i}. {L(x["label"], x["en"])}\n\n![{L(x["label"], x["en"])}]({x["file"]})\n' for i, x in enumerate(p['shots'], 1))
        return f"""{switch(lang)}

# {p['name']}

**{L('AMX Mod X eklentisi', 'AMX Mod X plugin')} · Counter-Strike 1.6**

![{p['name']}]({p['shots'][p['cover']]['file']})

{p['text']}

{' · '.join(f'`{t}`' for t in p['tags'])}

{L('Fiyat, kurulum ve canlı ayrıntılar', 'Pricing, installation and live details')}: **[bydevil.com]({p['link']})** · [{L('İletişim', 'Contact')}](https://tools.bydevil.com/contact/)

## {L('Ekran görüntüleri', 'Screenshots')}

{shots}
[← {L('Tüm eklentiler', 'All plugins')}](../{LANGS[lang]})
"""
    readme(f'plugins/{p["slug"]}', plugin_readme)

readme('plugins', lambda lang, L: f"""{switch(lang)}

# {L('AMXX eklentileri', 'AMXX plugins')}

{L('Counter-Strike 1.6 sunucuları için sıralama, sezon ve ekonomi sistemleri', 'Ranking, season and economy systems for Counter-Strike 1.6 servers')} · **{len(plugins)} {L('eklenti', 'plugins')}**.
{L('Sitede', 'On the site')}: [tools.bydevil.com/plugins](https://tools.bydevil.com/plugins/) · {L('Satış ve kurulum', 'Sales and installation')}: [bydevil.com/plugins](https://bydevil.com/plugins/)

<table>
{rows([plugin_cell(p, lang, L) for p in plugins], 3)}
</table>

[← {L('Ana sayfa', 'Home')}](../{LANGS[lang]})
""")

def kit_cell(k, lang, L, base=''):
    k = loc(k, lang)
    return (f'<td width="33%" valign="top"><a href="{base}{k["slug"]}"><img src="{base}{k["slug"]}/{k["shots"][0]["file"]}" alt="{k["name"]}"></a><br>'
            f'<b><a href="{base}{k["slug"]}">{k["name"]}</a></b><br>{k["intro"]}</td>')

for k in kits:
    def kit_readme(lang, L, k=k):
        k = loc(k, lang)
        shots = '\n'.join(f'### {L(x["label"], x["en"])}\n\n![{L(x["label"], x["en"])}]({x["file"]})\n' for x in k['shots'])
        feats = '\n\n'.join(f'**{a}**  \n{b}' for a, b in k['features'])
        extra = [f'[{L("Forum konusu", "Forum topic")} (webailesi.com)]({k["topic"]})'] + ([f'[{L("Video", "Video")} (YouTube)]({k["video"]})'] if k.get('video') else [])
        credits = f'\n## {L("Kredi", "Credits")}\n\n{k["credits"]}\n' if k.get('credits') else ''
        return f"""{switch(lang)}

# {k['name']}

**{L('CS 1.6 MOTD kiti · ücretsiz', 'CS 1.6 MOTD kit · free')}**

![{k['name']}]({k['shots'][0]['file']})

{k['intro']}

{' · '.join(f'`{t}`' for t in k['tags'])}

## {L('Özellikler', 'Features')}

{feats}

## {L('İndir', 'Download')}

**[⬇ {k['file']['name']}]({SITE}/kits/{k['slug']}/{k['file']['name']})** · {k['file']['size'] / 1024:.0f} KB · {L('şifresiz', 'no password')}

<sub>SHA-256: `{k['file']['sha256']}`</sub>

{L('Dosyalara tek tek bakmak için', 'Browse the files')}: [`{k['folder']}/`]({k['folder']})

{' · '.join(extra)}
{credits}
## {L('Ekran görüntüleri', 'Screenshots')}

{shots}
[← {L('Tüm kitler', 'All kits')}](../{LANGS[lang]})
"""
    readme(f'kits/{k["slug"]}', kit_readme)

readme('kits', lambda lang, L: f"""{switch(lang)}

# {L('MOTD kitleri', 'MOTD kits')}

{L('CS 1.6 web MOTD panellerini her çözünürlükte ve CSDurağı istemcisinde düzgün gösteren küçük, ücretsiz kitler.', 'Small, free kits that make CS 1.6 web MOTD panels work at every resolution and in the CSDurağı client.')}
{L('Sitede', 'On the site')}: [tools.bydevil.com/kits](https://tools.bydevil.com/kits/)

<table>
{rows([kit_cell(k, lang, L) for k in kits], 3)}
</table>

[← {L('Ana sayfa', 'Home')}](../{LANGS[lang]})
""")

readme('.', lambda lang, L: f"""<p align="center">
  <img src="assets/goldsrc-mark.png" width="88" alt="GoldSrc Studio">
</p>

<h1 align="center">GoldSrc Studio</h1>

<p align="center">
  {L('Counter-Strike 1.6 ve GoldSrc topluluğu için araçlar, haritalar, skyboxlar ve AMXX eklentileri.', 'Tools, maps, skyboxes and AMXX plugins for the Counter-Strike 1.6 and GoldSrc community.')}<br>
  <a href="https://tools.bydevil.com"><b>tools.bydevil.com</b></a> ·
  <a href="https://www.goldsrcstudio.com">goldsrcstudio.com</a> ·
  <a href="https://bydevil.com">bydevil.com</a>
</p>

<p align="center">{'<b>English</b> · <a href="README.tr.md">Türkçe</a>' if lang == 'en' else '<a href="README.md">English</a> · <b>Türkçe</b>'}</p>

<p align="center">
  <img src="assets/map-optimization.jpg" width="820" alt="Map Optimization">
</p>

---

## {L('Araçlar', 'Tools')}

<table>
{rows([tool_cell(t, lang, L) for t in tools], 2)}
</table>

## {L('Haritalar ve skyboxlar', 'Maps and skyboxes')}

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="maps"><img src="{maps['featured'][0]['image'].lstrip('/')}" alt=""></a><br>
      <b><a href="maps">{maps['count']} {L('Harita', 'Maps')} →</a></b><br>
      {L('Base Builder, Gun Game, Zombie Mod ve daha fazlası', 'Base Builder, Gun Game, Zombie Mod and more')} · {num(maps['downloads'], lang)} {L('indirme', 'downloads')}
    </td>
    <td width="50%" valign="top">
      <a href="skies"><img src="{skies['featured'][0]['image'].lstrip('/')}" alt=""></a><br>
      <b><a href="skies">{skies['count']} {L('Skybox', 'Skyboxes')} →</a></b><br>
      {L('Counter-Strike 1.6 ve GoldSrc için gökyüzleri', 'Skies for Counter-Strike 1.6 and GoldSrc')} · {num(skies['downloads'], lang)} {L('indirme', 'downloads')}
    </td>
  </tr>
</table>

## {L('AMXX eklentileri', 'AMXX plugins')}

<table>
{rows([plugin_cell(p, lang, L, 'plugins/') for p in plugins], 3)}
</table>

[{L('Tüm eklentiler', 'All plugins')} →](plugins)

## {L('MOTD kitleri', 'MOTD kits')}

<table>
{rows([kit_cell(k, lang, L, 'kits/') for k in kits], 3)}
</table>

[{L('Tüm kitler', 'All kits')} →](kits)

## {L('Hata bildirimi ve öneriler', 'Bug reports and suggestions')}

{L('Bir sorun bulduysan ya da yeni bir araç fikrin varsa [issue aç](../../issues).', 'Found a problem or have an idea for a new tool? [Open an issue](../../issues).')}

---

<sub>{L('GoldSrc Studio bağımsız bir projedir; Valve Corporation veya Steam ile bağlantılı değildir.', 'GoldSrc Studio is an independent project and is not affiliated with Valve Corporation or Steam.')}</sub>
""")
# ---------- sitemap.xml + robots.txt ----------
# Images are drawn into <canvas> on the site, so they are listed here for Google Images.
def absu(u):
    return u if u.startswith('http') else SITE + u

def entry(path, images):
    url = SITE + path
    imgs = ''.join(f'<image:image><image:loc>{absu(i)}</image:loc></image:image>' for i in dict.fromkeys(i for i in images if i))
    langs = ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url}?lang={l}"/>' for l in ('tr', 'en'))
    return f'<url><loc>{url}</loc>{langs}<xhtml:link rel="alternate" hreflang="x-default" href="{url}"/>{imgs}</url>'

plugin_imgs = [f'/plugins/{p["slug"]}/{x["file"]}' for p in plugins for x in p['shots']]
urls = [
    entry('/', ['/assets/map-optimization.jpg'] + [t['image'] for t in tools] + [m['image'] for m in maps['featured'] + skies['featured']]
          + [f'/plugins/{p["slug"]}/{p["shots"][p["cover"]]["file"]}' for p in plugins]),
    entry('/tools/', [t['image'] for t in tools]),
    *[entry(f'/tools/{t["slug"]}/', [t['image']]) for t in tools],
    entry('/maps/', [m['image'] for m in maps['items']]),
    entry('/skies/', [m['image'] for m in skies['items']]),
    entry('/plugins/', plugin_imgs),
    entry('/kits/', [f'/kits/{k["slug"]}/{x["file"]}' for k in kits for x in k['shots']]),
    entry('/contact/', []),
]
open('sitemap.xml', 'w', encoding='utf-8').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + '\n'.join(urls) + '\n</urlset>\n')
open('robots.txt', 'w', encoding='utf-8').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('ok')
