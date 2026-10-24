"""Sitenin HTML sayfalarını tek şablondan üretir.

Kullanım: python .github/scripts/build_pages.py
site.css / site.js değişince de çalıştırılmalı: dosya adreslerine içerik
özetinden bir sürüm eklenir, böylece tarayıcılar eski kopyayı kullanmaz.
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

def shell(path, page, title, desc, body, slug=None, image='/assets/map-optimization.jpg'):
    html = f'''<!doctype html>
<html lang="tr" data-theme="original">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0d141c">
  <script>try{{document.documentElement.dataset.theme=localStorage.getItem("gs-theme")||"original"}}catch(e){{document.documentElement.dataset.theme="original"}}</script>
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://tools.bydevil.com{image}">
  <link rel="icon" type="image/png" href="/assets/goldsrc-mark.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/site.css?v={VER}">
  <script src="/assets/site.js?v={VER}" defer></script>
</head>
<body data-page="{page}"{f' data-slug="{slug}"' if slug else ''}>
  <header id="hdr"></header>
  <main>
{body}
  </main>
  <footer id="ftr"></footer>
</body>
</html>
'''
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w').write(html)

def head(crumb, h1, lead, right=''):
    c = f'<nav class="crumbs"><a href="/">Ana sayfa</a><span class="sep">/</span><span>{crumb}</span></nav>' if crumb else ''
    return f'''    <div class="page-head"><div class="wrap">
      {c}
      <div class="page-head-row">
        <div><h1>{h1}</h1><p class="lead">{lead}</p></div>
        {right}
      </div>
    </div></div>'''

# Ana sayfa
shell('index.html', 'home', 'GoldSrc Studio — CS 1.6 araçları, haritaları ve skyboxları',
  'Counter-Strike 1.6 ve GoldSrc için bağımsız modlama araçları, haritalar ve skyboxlar.', '''    <section class="hero">
      <div class="hero-media"><img src="/assets/map-optimization.jpg" alt=""></div>
      <div class="wrap hero-inner">
        <span class="eyebrow"><i></i>GoldSrc ekosistemi için bağımsız stüdyo</span>
        <h1><span lang="en">Counter-Strike 1.6</span> için <span class="accent">özenle yapılmış</span> araçlar.</h1>
        <p class="lead">Haritaları analiz et, modelleri boya, skinleri düzenle, botların yolunu çiz.</p>
        <div class="actions">
          <a class="btn primary" href="/tools/">Araçları keşfet</a>
          <a class="btn" href="/maps/">Haritalara göz at</a>
        </div>
      </div>
    </section>
    <section class="section"><div class="wrap"><div class="stats" id="stats"></div></div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>Araçlar</h2></div><a class="more" href="/tools/">Tüm araçlar →</a></div>
      <div class="grid cols-3" id="home-tools"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>En çok indirilen haritalar</h2></div><a class="more" href="/maps/">Tüm haritalar →</a></div>
      <div class="grid cols-4" id="home-maps"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="sec-head"><div><h2>Popüler skyboxlar</h2></div><a class="more" href="/skies/">Tüm skyboxlar →</a></div>
      <div class="grid cols-4" id="home-skies"></div>
    </div></section>
    <section class="section"><div class="wrap">
      <div class="cta-band"><div><h2>Bir fikrin ya da hata bildirimin mi var?</h2><p>Steam, Discord veya GameBanana üzerinden ulaş.</p></div>
        <div class="actions"><a class="btn primary" href="/contact/">İletişime geç</a><a class="btn" href="https://github.com/by-devil/GoldSrcStudio/issues" target="_blank" rel="noopener">Hata bildir ↗</a></div></div>
    </div></section>''')

# Araçlar
shell('tools/index.html', 'tools', 'Araçlar — GoldSrc Studio', 'GoldSrc ve CS 1.6 için ücretsiz Windows araçları.',
  head('Araçlar', 'Araçlar', '<span id="tool-count">5</span> bağımsız uygulama. Hepsi Windows için, ücretsiz; indirme dosyaları doğrudan bu siteden ve GameBanana\'dan.') + '''
    <section class="section"><div class="wrap"><div class="grid cols-3" id="tool-grid"></div></div></section>''')

for t in tools:
    shell(f'tools/{t["slug"]}/index.html', 'tool', f'{t["name"]} — GoldSrc Studio', t['summary'], '', slug=t['slug'], image=t['image'])

def list_page(path, page, title, desc, h1, lead, chips, placeholder):
    shell(path, page, title, desc, head(h1, h1, lead, '''<div class="stats" style="grid-template-columns:repeat(2,minmax(150px,1fr));min-width:min(100%,340px)">
          <div class="stat"><b id="list-count">—</b><span>Toplam</span></div><div class="stat"><b id="list-dl">—</b><span>İndirme</span></div></div>''') + f'''
    <section class="section"><div class="wrap">
      {'<div class="chips" id="chips"></div>' if chips else ''}
      <div class="toolbar">
        <label class="field"><svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="{placeholder}" autocomplete="off"></label>
        <select class="select" id="sort" aria-label="Sırala">
          <option value="downloads">En çok indirilen</option><option value="likes">En çok beğenilen</option><option value="new">En yeni</option><option value="az">A → Z</option>
        </select>
        <span class="count-note" id="result-note"></span>
      </div>
      <div class="grid cols-4" id="list-grid"></div>
      <div class="load-more"><button class="btn" id="more" type="button">Daha fazla göster</button></div>
    </div></section>''')

list_page('maps/index.html', 'maps', 'Haritalar — GoldSrc Studio', 'Counter-Strike 1.6 için ücretsiz haritalar.', 'Haritalar',
  'Base Builder, Gun Game, Zombie Mod ve daha fazlası. Tüm haritalar ücretsiz ve GameBanana üzerinden indirilir.', True, 'Harita ara… (ör. dust2)')
list_page('skies/index.html', 'skies', 'Skyboxlar — GoldSrc Studio', 'GoldSrc ve CS 1.6 için skybox paketleri.', 'Skyboxlar',
  'Counter-Strike 1.6 ve GoldSrc için gökyüzü paketleri. Tümü ücretsiz ve GameBanana üzerinden indirilir.', False, 'Skybox ara…')

shell('plugins/index.html', 'plugins', 'AMXX eklentileri — GoldSrc Studio', 'Counter-Strike 1.6 sunucuları için AMX Mod X eklentileri.',
  head('Eklentiler', 'AMXX eklentileri', 'Sunucular için sıralama, sezon ve ekonomi sistemleri. Derlenmiş <b>.amxx</b> olarak satışa sunulacak; fiyatlar ve ödeme sistemi yakında.',
       '<span class="eyebrow"><i></i>Yakında</span>') + '''
    <section class="section"><div class="wrap">
      <div class="grid cols-3" id="plugin-grid"></div>
      <div class="cta-band" style="margin-top:28px"><div><h2>Çıkınca haber almak ister misin?</h2><p>Sunucun için hangisini beklediğini yaz, öncelik verelim.</p></div>
        <a class="btn primary" href="/contact/">İletişime geç</a></div>
    </div></section>''')

shell('contact/index.html', 'contact', 'İletişim — GoldSrc Studio', 'Steam, Discord ve GameBanana üzerinden iletişim.',
  head('İletişim', 'Bir fikrin mi var? <span class="accent">Konuşalım.</span>',
       'Araç geri bildirimi, harita önerisi, AMXX fikirleri ya da sadece selam vermek için. Doğrudan mesaj için en hızlı yol Steam.') + f'''
    <section class="section"><div class="wrap">
      <div class="contact-grid">
        <a class="contact-card steam" href="https://steamcommunity.com/id/SODEJ/" target="_blank" rel="noopener">
          <span class="ci">{STEAM}</span><span><b>Steam</b><small>Doğrudan mesaj için en hızlı yol</small></span><span class="go">↗</span></a>
        <button class="contact-card discord" type="button" id="discord-copy">
          <span class="ci">{DISCORD}</span><span><b>Discord</b><small id="discord-note">serhatondes · kopyalamak için tıkla</small></span><span class="go">⧉</span></button>
        <a class="contact-card" href="https://gamebanana.com/members/1419476" target="_blank" rel="noopener">
          <span class="ci"><img src="/assets/gamebanana.png" alt=""></span><span><b>GameBanana</b><small>Tüm haritalar, skyboxlar ve araçlar</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://github.com/by-devil/GoldSrcStudio/issues" target="_blank" rel="noopener">
          <span class="ci"><svg viewBox="0 0 16 16"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></span><span><b>GitHub</b><small>Hata bildirimi ve öneriler</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://fpslist.com/" target="_blank" rel="noopener">
          <span class="ci"><img class="full" src="/assets/fpslist.svg" alt=""></span><span><b>FPSList</b><small>Oyun sunucu listesi</small></span><span class="go">↗</span></a>
        <a class="contact-card" href="https://bydevil.com/" target="_blank" rel="noopener">
          <span class="ci"><img class="full" src="/assets/bydevil-mark.png" alt="" style="padding:6px"></span><span><b>bydevil.com</b><small>Haritalar, skyboxlar ve kitler</small></span><span class="go">↗</span></a>
      </div>
    </div></section>''')

shell('404.html', 'notfound', 'Sayfa bulunamadı — GoldSrc Studio', 'Aradığın sayfa bulunamadı.', '''    <section class="section"><div class="wrap" style="text-align:center;padding:60px 0">
      <span class="eyebrow"><i></i>404</span>
      <h1 style="margin:18px 0 10px;font-size:40px;font-weight:800;letter-spacing:-.03em">Bu sayfa bulunamadı.</h1>
      <p style="color:var(--text-2)">Aradığın şey taşınmış olabilir. Hızlı arama için <span class="kbd">/</span> tuşuna bas.</p>
      <div class="actions" style="justify-content:center;margin-top:24px"><a class="btn primary" href="/">Ana sayfa</a><a class="btn" href="/tools/">Araçlar</a></div>
    </div></section>''')
print('ok')
