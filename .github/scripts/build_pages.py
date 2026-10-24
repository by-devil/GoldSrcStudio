"""Sitenin HTML sayfalarını tek şablondan üretir (Türkçe + İngilizce).

Kullanım: python .github/scripts/build_pages.py
site.css / site.js değişince de çalıştırılmalı: dosya adreslerine içerik
özetinden bir sürüm eklenir, böylece tarayıcılar eski kopyayı kullanmaz.

Dil: her metin iki dilde yazılır. T('tr', 'en') iki <span data-l> üretir,
site.css seçili dili (html[data-lang]) gösterir. Seçim localStorage'da
"gs-lang" olarak saklanır; ?lang=en / ?lang=tr adresle de seçilebilir.
"""
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
tools = json.load(open('tools/tools.json', encoding='utf-8'))
_js = open('assets/site.js', encoding='utf-8').read()
STEAM = re.search(r"const STEAM = '(<svg.*?</svg>)';", _js).group(1)
DISCORD = re.search(r"const DISCORD = '(<svg.*?</svg>)';", _js).group(1)
VER = hashlib.sha1(open('assets/site.css', 'rb').read() + _js.encode()).hexdigest()[:8]

# Tema ve dil, ilk boyamadan önce ayarlanır (yanıp sönme olmasın diye).
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

def shell(path, page, title, desc, body, slug=None, image='/assets/map-optimization.jpg'):
    """title ve desc: (tr, en) çiftleri."""
    html = f'''<!doctype html>
<html lang="tr" data-theme="original" data-lang="tr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title[0]}</title>
  <meta name="description" content="{desc[0]}">
  <meta name="theme-color" content="#0d141c">
  <script>{HEAD_JS}</script>
  <meta property="og:title" content="{title[0]}">
  <meta property="og:description" content="{desc[0]}">
  <meta property="og:image" content="https://tools.bydevil.com{image}">
  <link rel="icon" type="image/png" href="/assets/goldsrc-mark.png">
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

# Ana sayfa
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
    </div></section>''')

# Araçlar
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

shell('404.html', 'notfound', ('Sayfa bulunamadı — GoldSrc Studio', 'Page not found — GoldSrc Studio'),
  ('Aradığın sayfa bulunamadı.', 'The page you are looking for could not be found.'), f'''    <section class="section"><div class="wrap" style="text-align:center;padding:60px 0">
      <span class="eyebrow"><i></i>404</span>
      <h1 style="margin:18px 0 10px;font-size:40px;font-weight:800;letter-spacing:-.03em">{T('Bu sayfa bulunamadı.', 'This page could not be found.')}</h1>
      <p style="color:var(--text-2)">{T('Aradığın şey taşınmış olabilir. Hızlı arama için <span class="kbd">/</span> tuşuna bas.', 'It may have moved. Press <span class="kbd">/</span> for quick search.')}</p>
      <div class="actions" style="justify-content:center;margin-top:24px"><a class="btn primary" href="/">{T('Ana sayfa', 'Home')}</a><a class="btn" href="/tools/">{T('Araçlar', 'Tools')}</a></div>
    </div></section>''')
print('ok')
