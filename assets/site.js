/* GoldSrc Studio — ortak menü, altbilgi, hızlı arama ve sayfa içerikleri */
(() => {
  'use strict';

  const LINKS = {
    github: 'https://github.com/by-devil/GoldSrcStudio',
    issues: 'https://github.com/by-devil/GoldSrcStudio/issues',
    steam: 'https://steamcommunity.com/id/SODEJ/',
    gamebanana: 'https://gamebanana.com/members/1419476',
    fpslist: 'https://fpslist.com/',
    goldsrc: 'https://www.goldsrcstudio.com/',
    bydevil: 'https://bydevil.com/',
    discord: 'serhatondes',
  };
  /* ---------- dil ---------- */
  const LANG = document.documentElement.dataset.lang === 'en' ? 'en' : 'tr';
  const L = (tr, en) => LANG === 'en' ? en : tr;
  const LOCALE = L('tr-TR', 'en-US');

  const PLUGIN_BASE = 'https://bydevil.com/plugins/#';
  const BD = 'https://bydevil.com/assets/'; // eklenti ekran görüntüleri bydevil.com'da duruyor
  const PLUGINS = [
    { id: 'propublic', name: 'Pro Public TOP15', img: BD + 'propublic/pp-1-top15.jpg', tags: L(['Top15', 'Toptime', 'Profil', 'FunGun'], ['Top15', 'Toptime', 'Profile', 'FunGun']),
      text: L('Pro Public sunucuları için eksiksiz istatistik sistemi: Top15 ve süre sıralamaları, detaylı oyuncu profilleri, Steam bilgileri ve FunGun tarama geçmişi.',
        'Complete stats system for Pro Public servers: Top15 and playtime rankings, detailed player profiles, Steam info and FunGun scan history.') },
    { id: 'royalpass', name: 'Royal Pass', img: BD + 'royalpass/rp-04.jpg', tags: L(['Görevler', 'Mağaza', 'Kutular', 'Pazar'], ['Missions', 'Shop', 'Cases', 'Market']),
      text: L('Puan ekonomisi: görevlerden puan kazan, kozmetik mağazasında harca, kutu aç, oyuncu pazarında alım satım yap.',
        'Points economy: earn points from missions, spend them in the cosmetics shop, open cases and trade on the player market.') },
    { id: 'takim', name: 'Team System', img: BD + 'takim/tk-01.jpg', tags: L(['Yönetim', 'Görevler', 'FreeVIP', 'Sezon'], ['Management', 'Missions', 'FreeVIP', 'Season']),
      text: L('Takım (klan) sistemi: takım kur, üye davet et, banner ve renklerle özelleştir, sezon sıralamasında birlikte yüksel.',
        'Team (clan) system: create a team, invite members, customise it with banners and colours, and climb the season ranking together.') },
    { id: 'gungame', name: 'GunGame TOP15', img: '/assets/plugins/gungame-top15/gg-01.webp', tags: L(['Bireysel', 'Takım', 'FFA', 'Sezon'], ['Solo', 'Team', 'FFA', 'Season']),
      text: L('Bireysel, takım ve FFA sıralamaları; puan, XP, K/D, bıçak ve seri istatistikleri, oyuncu profilleri ve sezon görünümleri.',
        'Solo, team and FFA rankings; points, XP, K/D, knife and streak stats, player profiles and season views.') },
    { id: 'zombieplague', name: 'Zombie Plague TOP15', img: BD + 'zp-top15/zp-01.jpg', tags: L(['Genel', 'Süre', 'Profil', 'Haftalık ödül'], ['Overall', 'Playtime', 'Profile', 'Weekly reward']),
      text: L('Zombie Plague için sıralama: liderle kıyaslayan profiller, rütbe yolu, özelleştirilebilir kart, sezon arşivi ve haftalık VIP ödülleri.',
        'Rankings for Zombie Plague: profiles compared with the leader, a rank path, a customisable card, season archive and weekly VIP rewards.') },
    { id: 'battlepass', name: 'Public Battle Pass', img: BD + 'battlepass-public/bpp-01.jpg', tags: L(['Seviyeler', 'Kasalar', 'Çark', 'Envanter'], ['Tiers', 'Cases', 'Wheel', 'Inventory']),
      text: L('Public sunucular için sezonluk battle pass: ücretsiz ve premium seviye ödülleri, kasalar, çark ve efekt envanteri.',
        'Seasonal battle pass for public servers: free and premium tier rewards, cases, a prize wheel and an effects inventory.') },
    { id: 'battlepass', name: 'Zombie Plague Battle Pass', img: BD + 'battlepass-zp/bpz-01.jpg', tags: L(['Ödüller', 'Görevler', 'Çark', 'Mağaza'], ['Rewards', 'Missions', 'Wheel', 'Shop']),
      text: L('Haftalık sezon sistemi: her gün ücretsiz ve premium ödül, günlük görevler, coin çarkı ve mağaza.',
        'Weekly season system: free and premium rewards every day, daily missions, a coin wheel and a shop.') },
  ];

  /* ---------- yardımcılar ---------- */
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmt = n => Number(n || 0).toLocaleString(LOCALE);
  const day = ts => ts ? new Date(ts * 1000).toLocaleDateString(LOCALE, { day: 'numeric', month: 'short', year: 'numeric' }) : '';
  const ext = 'target="_blank" rel="noopener"';
  const cache = {};
  const getJSON = url => (cache[url] ||= fetch(url, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error(url); return r.json(); }));
  const data = {
    tools: () => getJSON('/tools/tools.json').then(list => list.map(t => LANG === 'en' && t.en ? { ...t, ...t.en } : t)),
    maps: () => getJSON('/maps/maps.json'),
    skies: () => getJSON('/skies/skies.json'),
  };

  const P = {
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    chev: '<path d="m6 9 6 6 6-6"/>',
    menu: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    dl: '<path d="M12 4v11m0 0-4-4m4 4 4-4M5 20h14"/>',
    out: '<path d="M14 5h5v5M19 5l-8 8M18 14v4a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h4"/>',
    right: '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    left: '<path d="M19 12H5m5-5-5 5 5 5"/>',
    tool: '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    map: '<path d="m9 4-5 2v14l5-2 6 2 5-2V4l-5 2-6-2zM9 4v14M15 6v14"/>',
    cloud: '<path d="M7 18a4 4 0 0 1-.6-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-.5 9H7z"/>',
    plug: '<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0V8zM12 17v4"/>',
    chat: '<path d="M4 5h16v11H9l-5 4V5z"/>',
    heart: '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    cal: '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>',
    box: '<path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3zM4 7.5l8 4.5 8-4.5M12 12v9"/>',
    alert: '<path d="M12 3 2 20h20L12 3zM12 10v4M12 17v.5"/>',
    copy: '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
    file: '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8l-5-5zM14 3v5h5"/>',
    theme: '<path d="M12 3a9 9 0 1 0 0 18c1 0 1.5-.8 1.5-1.6 0-.9-.7-1.3-.7-2.1 0-.9.7-1.5 1.6-1.5H16a5 5 0 0 0 5-5c0-4.3-4-7.8-9-7.8z"/><circle cx="7.5" cy="11" r="1.2"/><circle cx="10.5" cy="7" r="1.2"/><circle cx="15.5" cy="7.5" r="1.2"/>',
  };
  const icon = (n, cls = '') => `<svg class="ico ${cls}" viewBox="0 0 24 24" aria-hidden="true">${P[n]}</svg>`;
  const GH = '<svg class="ico fill" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>';
  const STEAM = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11.979 0C5.678 0 .511 4.86.022 11.037l6.432 2.658c.545-.371 1.203-.59 1.912-.59.063 0 .125.004.188.006l2.861-4.142V8.91c0-2.495 2.028-4.524 4.524-4.524 2.494 0 4.524 2.031 4.524 4.527s-2.03 4.525-4.524 4.525h-.105l-4.076 2.911c0 .052.004.105.004.159 0 1.875-1.515 3.396-3.39 3.396-1.635 0-3.016-1.173-3.331-2.727L.436 15.27C1.862 20.307 6.486 24 11.979 24c6.627 0 11.999-5.373 11.999-12S18.605 0 11.979 0zM7.54 18.21l-1.473-.61c.262.543.714.999 1.314 1.25 1.297.539 2.793-.076 3.332-1.375.263-.63.264-1.319.005-1.949s-.75-1.121-1.377-1.383c-.624-.26-1.29-.249-1.878-.03l1.523.63c.956.4 1.409 1.5 1.009 2.455-.397.957-1.497 1.41-2.454 1.012H7.54zm11.415-9.303c0-1.662-1.353-3.015-3.015-3.015-1.665 0-3.015 1.353-3.015 3.015 0 1.665 1.35 3.015 3.015 3.015 1.663 0 3.015-1.35 3.015-3.015zm-5.273-.005c0-1.252 1.013-2.266 2.265-2.266 1.249 0 2.266 1.014 2.266 2.266 0 1.251-1.017 2.265-2.266 2.265-1.253 0-2.265-1.014-2.265-2.265z"/></svg>';
  const DISCORD = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z"/></svg>';

  const page = document.body.dataset.page;
  const imgFallback = 'onerror="this.remove()"';

  /* ---------- menü ---------- */
  function header(tools) {
    const groups = { tools: ['tools', 'tool'], maps: ['maps', 'skies'] };
    const cur = p => (groups[p] || [p]).includes(page) ? ' aria-current="page"' : '';
    const toolLinks = tools.map(t => `
      <a class="mlink" href="/tools/${t.slug}/">
        <span class="mlink-ic"><img src="${esc(t.image)}" alt=""></span>
        <span><span class="mlink-t">${esc(t.name)}</span><span class="mlink-d">${esc(t.summary)}</span></span>
      </a>`).join('');
    const item = (key, href, label, mega) => `
      <div class="hdr-item"${mega ? ' data-menu' : ''}>
        <a class="hdr-link" href="${href}"${cur(key)}>${label}${mega ? icon('chev', 'chev') : ''}</a>
        ${mega ? `<div class="mega" role="menu">${mega}</div>` : ''}
      </div>`;
    const works = `
      <div class="mega-grid">
        <p class="mega-label">${L('Topluluk için', 'For the community')}</p>
        <a class="mlink" href="/maps/"><span class="mlink-ic">${icon('map')}</span><span><span class="mlink-t">${L('Haritalar', 'Maps')}</span><span class="mlink-d">${L('Base Builder, Gun Game, Zombie ve daha fazlası', 'Base Builder, Gun Game, Zombie and more')}</span></span></a>
        <a class="mlink" href="/skies/"><span class="mlink-ic">${icon('cloud')}</span><span><span class="mlink-t">${L('Skyboxlar', 'Skyboxes')}</span><span class="mlink-d">${L('GoldSrc için gökyüzü paketleri', 'Sky packs for GoldSrc')}</span></span></a>
        <a class="mlink" href="/plugins/"><span class="mlink-ic">${icon('plug')}</span><span><span class="mlink-t">${L('AMXX eklentileri', 'AMXX plugins')}</span><span class="mlink-d">${L('Sıralama, sezon ve ekonomi sistemleri', 'Ranking, season and economy systems')}</span></span></a>
        <a class="mlink" href="${LINKS.gamebanana}" ${ext}><span class="mlink-ic"><img src="/assets/gamebanana.png" alt="" style="width:22px;height:22px;image-rendering:pixelated"></span><span><span class="mlink-t">${L('GameBanana profili', 'GameBanana profile')}</span><span class="mlink-d">${L('Tüm yüklemeler tek yerde', 'All uploads in one place')}</span></span></a>
      </div>`;
    return `
      <div class="wrap hdr-bar">
        <a class="hdr-brand" href="/" aria-label="${L('GoldSrc Studio ana sayfa', 'GoldSrc Studio home')}">
          <img src="/assets/goldsrc-mark.png" alt="" width="34" height="34">
          <span class="hdr-wm"><b>GoldSrc Studio</b></span>
        </a>
        <nav class="hdr-nav" aria-label="${L('Ana menü', 'Main menu')}">
          ${item('tools', '/tools/', L('Araçlar', 'Tools'), `<div class="mega-grid"><p class="mega-label">${L('Uygulamalar', 'Apps')}</p>${toolLinks}<div class="mega-foot"><a href="/tools/">${L('Tüm araçlar →', 'All tools →')}</a></div></div>`)}
          ${item('maps', '/maps/', L('Çalışmalar', 'Works'), works)}
          ${item('plugins', '/plugins/', L('Eklentiler', 'Plugins'))}
          ${item('contact', '/contact/', L('İletişim', 'Contact'))}
        </nav>
        <div class="hdr-right">
          <button class="hdr-search" type="button" data-palette><span class="hs-ic">${icon('search')}</span><span class="hs-txt">${L('Ara', 'Search')}<em>${L('Araçlar, haritalar, skyboxlar', 'Tools, maps, skyboxes')}</em></span><span class="hs-keys"><span class="kbd">Ctrl</span><span class="kbd">K</span></span></button>
          <a class="pill-link" href="${LINKS.goldsrc}" ${ext}><img src="/assets/goldsrc-mark.png" alt=""><span>GoldSrc Studio</span></a>
          <a class="pill-link" href="${LINKS.bydevil}" ${ext}><img src="/assets/bydevil-mark.png" alt=""><span>By Devil</span></a>
          <button class="lang-btn" type="button" data-lang-btn aria-label="${L('Dili değiştir: English', 'Switch language: Türkçe')}" title="${L('Dil / Language', 'Language / Dil')}">
            <span${LANG === 'tr' ? ' class="on"' : ''}>TR</span><span${LANG === 'en' ? ' class="on"' : ''}>EN</span></button>
          <div style="position:relative"><button class="icon-btn" type="button" data-theme-btn aria-label="${L('Tema', 'Theme')}" aria-expanded="false">${icon('theme')}</button></div>
          <a class="icon-btn hdr-gh" href="${LINKS.github}" ${ext} aria-label="GitHub">${GH}</a>
          <button class="icon-btn hdr-burger" type="button" aria-label="${L('Menü', 'Menu')}" aria-expanded="false">${icon('menu')}</button>
        </div>
      </div>`;
  }

  function footer(tools) {
    return `
      <div class="wrap">
        <div class="ftr-top">
          <div class="ftr-about">
            <a class="hdr-brand" href="/"><img src="/assets/goldsrc-mark.png" alt="" width="34" height="34"><span class="hdr-wm"><b>GoldSrc Studio</b></span></a>
            <p>${L('Counter-Strike 1.6 ve GoldSrc topluluğu için bağımsız araçlar, haritalar, skyboxlar ve AMXX eklentileri.', 'Independent tools, maps, skyboxes and AMXX plugins for the Counter-Strike 1.6 and GoldSrc community.')}</p>
            <div class="ftr-social">
              <a href="${LINKS.steam}" ${ext} aria-label="Steam">${STEAM}</a>
              <a href="/contact/" aria-label="Discord">${DISCORD}</a>
              <a href="${LINKS.gamebanana}" ${ext} aria-label="GameBanana"><img src="/assets/gamebanana.png" alt=""></a>
              <a href="${LINKS.github}" ${ext} aria-label="GitHub">${GH}</a>
              </div>
            <a class="site-pill" href="${LINKS.fpslist}" ${ext}><img src="/assets/fpslist.svg" alt=""><span>FPSList<small>${L('Oyun sunucu listesi', 'Game server list')}</small></span></a>
            <div hidden>
            </div>
          </div>
          <div><h4>${L('Araçlar', 'Tools')}</h4><ul>${tools.map(t => `<li><a href="/tools/${t.slug}/">${esc(t.name)}</a></li>`).join('')}</ul></div>
          <div><h4>${L('Çalışmalar', 'Works')}</h4><ul>
            <li><a href="/maps/">${L('Haritalar', 'Maps')}</a></li><li><a href="/skies/">${L('Skyboxlar', 'Skyboxes')}</a></li><li><a href="/plugins/">${L('AMXX eklentileri', 'AMXX plugins')}</a></li>
            <li><a href="${LINKS.gamebanana}" ${ext}>GameBanana</a></li></ul></div>
          <div><h4>${L('Bağlantılar', 'Links')}</h4><ul>
            <li><a href="/contact/">${L('İletişim', 'Contact')}</a></li><li><a href="${LINKS.issues}" ${ext}>${L('Hata bildir', 'Report a bug')}</a></li>
            <li><a href="${LINKS.goldsrc}" ${ext}>goldsrcstudio.com</a></li><li><a href="${LINKS.bydevil}" ${ext}>bydevil.com</a></li>
            <li><a href="${LINKS.fpslist}" ${ext}>fpslist.com</a></li></ul></div>
        </div>
        <div class="ftr-bottom">
          <span>© ${new Date().getFullYear()} GoldSrc Studio · by Devil · ${L('Tüm hakları saklıdır.', 'All rights reserved.')}</span>
          <span>${L('Valve Corporation veya Steam ile bağlantılı değildir.', 'Not affiliated with Valve Corporation or Steam.')}</span>
        </div>
      </div>`;
  }

  function wireHeader(hdr) {
    const items = $$('[data-menu]', hdr);
    const close = except => items.forEach(i => i !== except && i.classList.remove('open'));
    const desktop = () => matchMedia('(min-width: 981px)').matches;
    items.forEach(it => {
      let t;
      it.addEventListener('mouseenter', () => { if (!desktop()) return; clearTimeout(t); close(it); it.classList.add('open'); });
      it.addEventListener('mouseleave', () => { if (!desktop()) return; t = setTimeout(() => it.classList.remove('open'), 140); });
      $('.hdr-link', it).addEventListener('click', e => {
        if (desktop()) return;
        if (!it.classList.contains('open')) { e.preventDefault(); close(it); it.classList.add('open'); }
      });
    });
    document.addEventListener('click', e => { if (!hdr.contains(e.target)) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
    const burger = $('.hdr-burger', hdr);
    burger.addEventListener('click', () => {
      const open = hdr.classList.toggle('menu-open');
      burger.setAttribute('aria-expanded', open);
      burger.innerHTML = icon(open ? 'close' : 'menu');
    });
  }

  /* ---------- tema ---------- */
  const THEMES = [
    ['original', 'Original', L('Katmanlı maviler', 'Layered blues'), '#1a2634', '#5ab0ec'],
    ['dust', 'Dust', L('Sıcak kum', 'Warm sand'), '#15130f', '#e9a23b'],
    ['carbon', 'Carbon', L('Nötr grafit', 'Neutral graphite'), '#0f1012', '#e9ebee'],
    ['radar', 'Radar', L('Mini harita yeşili', 'Minimap green'), '#0c1411', '#3fd99a'],
    ['ember', 'Ember', L('T tarafı turuncusu', 'T-side orange'), '#141010', '#ff7043'],
  ];
  function wireTheme(hdr) {
    const btn = $('[data-theme-btn]', hdr);
    let menu;
    const current = () => document.documentElement.dataset.theme || 'original';
    const set = t => {
      document.documentElement.dataset.theme = t;
      try { localStorage.setItem('gs-theme', t); } catch { /* gizli pencere vb. */ }
      $$('.swatch', menu).forEach(b => b.setAttribute('aria-checked', b.dataset.t === t));
    };
    btn.addEventListener('click', e => {
      e.stopPropagation();
      if (!menu) {
        menu = document.createElement('div');
        menu.className = 'theme-menu';
        menu.setAttribute('role', 'radiogroup');
        menu.innerHTML = `<p>${L('Tema', 'Theme')}</p>` + THEMES.map(([id, name, desc, a, b]) =>
          `<button class="swatch" type="button" role="radio" data-t="${id}" aria-checked="${current() === id}">
            <span class="swatch-chip"><span style="background:${a}"></span><span style="background:${b}"></span></span>${name}<small>${desc}</small></button>`).join('');
        menu.addEventListener('click', ev => { const b = ev.target.closest('.swatch'); if (b) set(b.dataset.t); });
        btn.parentElement.append(menu);
        document.addEventListener('click', ev => { if (!menu.contains(ev.target) && ev.target !== btn) { menu.hidden = true; btn.setAttribute('aria-expanded', false); } });
        return btn.setAttribute('aria-expanded', true);
      }
      menu.hidden = !menu.hidden;
      btn.setAttribute('aria-expanded', !menu.hidden);
    });
  }

  /* ---------- hızlı arama ---------- */
  function palette() {
    let el, list, input, results = [], sel = 0;
    const norm = s => s.toLocaleLowerCase(LOCALE).normalize('NFD').replace(/[̀-ͯ]/g, '');
    async function build() {
      const [tools, maps, skies] = await Promise.all([data.tools(), data.maps().catch(() => ({ items: [] })), data.skies().catch(() => ({ items: [] }))]);
      const G = { pages: L('Sayfalar', 'Pages'), tools: L('Araçlar', 'Tools'), plugins: L('Eklentiler', 'Plugins'), maps: L('Haritalar', 'Maps'), skies: L('Skyboxlar', 'Skyboxes') };
      const pages = [
        { group: G.pages, name: L('Araçlar', 'Tools'), sub: L('Tüm uygulamalar', 'All apps'), href: '/tools/', ic: icon('tool') },
        { group: G.pages, name: L('Haritalar', 'Maps'), sub: `${maps.count || ''} ${L('harita', 'maps')}`, href: '/maps/', ic: icon('map') },
        { group: G.pages, name: L('Skyboxlar', 'Skyboxes'), sub: `${skies.count || ''} ${L('skybox', 'skyboxes')}`, href: '/skies/', ic: icon('cloud') },
        { group: G.pages, name: L('AMXX eklentileri', 'AMXX plugins'), sub: L('Sunucu sistemleri', 'Server systems'), href: '/plugins/', ic: icon('plug') },
        ...PLUGINS.map(p => ({ group: G.plugins, name: p.name, sub: 'AMX Mod X · bydevil.com', href: PLUGIN_BASE + p.id, ext: true, site: 'bydevil.com', ic: icon('plug') })),
        { group: G.pages, name: L('İletişim', 'Contact'), sub: 'Steam, Discord, GameBanana', href: '/contact/', ic: icon('chat') },
      ];
      return [
        ...tools.map(t => ({ group: G.tools, home: true, name: t.name, sub: t.summary, href: `/tools/${t.slug}/`, ic: `<img src="${esc(t.image)}" alt="">` })),
        ...pages.map(r => ({ ...r, home: r.group === G.pages })),
        ...(maps.items || []).map(m => ({ group: G.maps, name: m.name, sub: `${m.category} · ⬇ ${fmt(m.downloads)}`, href: m.url, ext: true, ic: m.image ? `<img src="${esc(m.image)}" alt="" ${imgFallback}>` : icon('map') })),
        ...(skies.items || []).map(m => ({ group: G.skies, name: m.name, sub: `Skybox · ⬇ ${fmt(m.downloads)}`, href: m.url, ext: true, ic: m.image ? `<img src="${esc(m.image)}" alt="" ${imgFallback}>` : icon('cloud') })),
      ];
    }
    let all;
    function render() {
      const q = norm(input.value.trim());
      results = (q ? all.filter(r => norm(r.name + ' ' + r.sub).includes(q)) : all.filter(r => r.home)).slice(0, 40);
      sel = Math.min(sel, Math.max(results.length - 1, 0));
      let g = '';
      list.innerHTML = results.length ? results.map((r, i) => {
        const head = r.group !== g ? `<div class="palette-group">${(g = r.group)}</div>` : '';
        return `${head}<a class="palette-item${i === sel ? ' on' : ''}" href="${esc(r.href)}" ${r.ext ? ext : ''} data-i="${i}">
          <span class="pi">${r.ic}</span><span><b>${esc(r.name)}</b><small>${esc(r.sub)}</small></span>${r.ext ? `<span class="ext">${r.site || 'GameBanana'} ↗</span>` : ''}</a>`;
      }).join('') : `<div class="palette-empty">${L('Sonuç bulunamadı.', 'No results found.')}</div>`;
    }
    async function open() {
      if (!el) {
        el = document.createElement('div');
        el.className = 'palette';
        el.innerHTML = `<div class="palette-box" role="dialog" aria-label="${L('Hızlı arama', 'Quick search')}">
          <label class="palette-in">${icon('search')}<input type="search" placeholder="${L('Araç, harita veya skybox ara…', 'Search tools, maps or skyboxes…')}" autocomplete="off"><span class="kbd">Esc</span></label>
          <div class="palette-list"></div>
          <div class="palette-foot"><span><span class="kbd">↑</span> <span class="kbd">↓</span> ${L('gez', 'navigate')}</span><span><span class="kbd">Enter</span> ${L('aç', 'open')}</span></div></div>`;
        document.body.append(el);
        list = $('.palette-list', el); input = $('input', el);
        el.addEventListener('click', e => { if (e.target === el) hide(); });
        input.addEventListener('input', () => { sel = 0; render(); });
        input.addEventListener('keydown', e => {
          if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault(); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + results.length) % Math.max(results.length, 1); render();
            $('.palette-item.on', list)?.scrollIntoView({ block: 'nearest' });
          } else if (e.key === 'Enter' && results[sel]) {
            e.preventDefault(); const r = results[sel];
            r.ext ? window.open(r.href, '_blank', 'noopener') : (location.href = r.href); hide();
          }
        });
        list.addEventListener('mousemove', e => { const a = e.target.closest('[data-i]'); if (a && +a.dataset.i !== sel) { sel = +a.dataset.i; render(); } });
        all = await build();
      }
      el.hidden = false; input.value = ''; sel = 0; render(); input.focus();
    }
    const hide = () => { if (el) el.hidden = true; };
    document.addEventListener('keydown', e => {
      const typing = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName);
      if ((e.key === '/' && !typing) || ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k')) { e.preventDefault(); open(); }
      else if (e.key === 'Escape') hide();
    });
    $$('[data-palette]').forEach(b => b.addEventListener('click', open));
  }

  /* ---------- parçalar ---------- */
  const toolCard = t => `
    <article class="card tool-card hover fade">
      <a class="card-media contain" href="/tools/${t.slug}/"><span class="badge">${esc(t.version)}</span><img src="${esc(t.image)}" alt="${esc(t.name)} ${L('ekran görüntüsü', 'screenshot')}" loading="lazy"></a>
      <div class="card-body">
        <div class="tags"><span class="tag accent">${esc(t.category)}</span><span class="tag">${esc(t.platform)}</span></div>
        <a class="card-title" href="/tools/${t.slug}/">${esc(t.name)}</a>
        <p class="card-text">${esc(t.summary)}</p>
        <div class="card-meta"><span>${icon('cal')}${esc(t.updated)}</span><span>${icon('file')}${esc(t.fileTypes)}</span></div>
      </div>
      <div class="card-actions">
        <a class="btn sm primary" href="${esc(t.download)}" download>${icon('dl')}${L('İndir', 'Download')}</a>
        <a class="btn sm" href="/tools/${t.slug}/">${L('Ayrıntılar', 'Details')}</a>
        <a class="btn sm" href="${esc(t.github)}" ${ext} aria-label="GitHub">${GH}</a>
        <a class="btn sm" href="${esc(t.gamebanana)}" ${ext}>GameBanana ${icon('out')}</a>
      </div>
    </article>`;
  const workCard = (m, kind) => `
    <a class="card fade" href="${esc(m.url)}" ${ext}>
      <div class="card-media">${m.image ? `<img src="${esc(m.image)}" alt="" loading="lazy" ${imgFallback}>` : ''}${kind === 'map' && m.category ? `<span class="badge">${esc(m.category)}</span>` : ''}</div>
      <div class="card-body">
        <span class="card-title">${esc(m.name)}</span>
        <div class="card-meta"><span>${icon('dl')}${fmt(m.downloads)}</span><span>${icon('heart')}${fmt(m.likes)}</span>${m.date ? `<span>${icon('cal')}${day(m.date)}</span>` : ''}</div>
      </div>
    </a>`;
  const pluginCard = p => `
    <a class="card plugin-card fade" href="${PLUGIN_BASE}${p.id}" ${ext}>
      <div class="card-media"><span class="plugin-ph">${icon('plug')}<b lang="en">${esc(p.name)}</b></span>${p.img ? `<img src="${esc(p.img)}" alt="${esc(p.name)}" loading="lazy" ${imgFallback}>` : ''}<span class="badge">AMX Mod X</span></div>
      <div class="card-body">
        <span class="card-title" lang="en">${esc(p.name)}</span>
        <p class="card-text">${esc(p.text)}</p>
        <div class="tags">${p.tags.map(t => `<span class="tag">${esc(t)}</span>`).join('')}</div>
        <span class="plugin-go">${L('Ekran görüntüleri ve ayrıntılar', 'Screenshots and details')} ${icon('out')}</span>
      </div>
    </a>`;
  const statTile = (ic, value, label) => `<div class="hstat"><b>${value}</b><span>${icon(ic)}${label}</span></div>`;

  /* ---------- sayfalar ---------- */
  const pages = {
    async home(main) {
      const [tools, maps, skies] = await Promise.all([data.tools(), data.maps(), data.skies()]);
      $('#stats', main).innerHTML =
        statTile('tool', tools.length, L('GoldSrc aracı', 'GoldSrc tools')) +
        statTile('map', fmt(maps.count), L('Harita', 'Maps')) +
        statTile('cloud', fmt(skies.count), L('Skybox', 'Skyboxes')) +
        statTile('plug', PLUGINS.length, L('AMXX eklentisi', 'AMXX plugins')) +
        statTile('dl', fmt(maps.downloads + skies.downloads), L('Toplam indirme', 'Total downloads'));
      $('#home-tools', main).innerHTML = tools.map(toolCard).join('');
      $('#home-maps', main).innerHTML = maps.featured.slice(0, 4).map(m => workCard(m, 'map')).join('');
      $('#home-skies', main).innerHTML = skies.featured.slice(0, 4).map(m => workCard(m, 'sky')).join('');
      $('#home-plugins', main).innerHTML = PLUGINS.slice(0, 3).map(pluginCard).join('');
    },

    async tools(main) {
      const tools = await data.tools();
      $$('.tool-count', main).forEach(el => { el.textContent = tools.length; });
      $('#tool-grid', main).innerHTML = tools.map(toolCard).join('');
    },

    async tool(main) {
      const tools = await data.tools();
      const i = tools.findIndex(t => t.slug === document.body.dataset.slug);
      const t = tools[i];
      if (!t) { main.innerHTML = `<div class="wrap section"><div class="empty">${L('Araç bulunamadı.', 'Tool not found.')}</div></div>`; return; }
      document.title = `${t.name} — GoldSrc Studio`;
      const prev = tools[(i - 1 + tools.length) % tools.length], next = tools[(i + 1) % tools.length];
      const file = t.download.split('/').pop();
      main.innerHTML = `
        <div class="page-head"><div class="wrap">
          <nav class="crumbs"><a href="/">${L('Ana sayfa', 'Home')}</a><span class="sep">/</span><a href="/tools/">${L('Araçlar', 'Tools')}</a><span class="sep">/</span><span>${esc(t.name)}</span></nav>
          <div class="page-head-row">
            <div><div class="tags" style="margin-bottom:12px"><span class="tag accent">${esc(t.category)}</span><span class="tag">${esc(t.version)}</span><span class="tag">${esc(t.platform)}</span></div>
              <h1 lang="en">${esc(t.name)}</h1><p class="lead">${esc(t.summary)}</p></div>
            <div class="actions"><a class="btn primary" href="${esc(t.download)}" download>${icon('dl')}${L('İndir', 'Download')}</a><a class="btn" href="${esc(t.github)}" ${ext}>${GH} GitHub</a><a class="btn" href="${esc(t.gamebanana)}" ${ext}>GameBanana ${icon('out')}</a></div>
          </div>
        </div></div>
        <div class="wrap section">
          <div class="detail">
            <div>
              <div class="shot fade"><img src="${esc(t.image)}" alt="${esc(t.name)} ${L('ekran görüntüsü', 'screenshot')}"></div>
              <div class="prose" style="margin-top:26px"><p>${esc(t.description)}</p></div>
              <h2 style="margin:30px 0 14px;font-size:19px">${L('Öne çıkan özellikler', 'Key features')}</h2>
              <ul class="feature-list">${(t.features || []).map(f => `<li>${esc(f)}</li>`).join('')}</ul>
              <div class="notice" style="margin-top:28px">${icon('alert')}<span>${L('Araçlar beta aşamasındadır. Dosyalarını düzenlemeden önce yedeklemeni öneririz.', 'The tools are in beta. We recommend backing up your files before editing them.')}</span></div>
            </div>
            <aside class="side">
              <div class="panel download-box">
                <h3>${L('İndir', 'Download')}</h3>
                <a class="btn primary" href="${esc(t.download)}" download>${icon('dl')}${esc(file)}</a>
                <div class="actions" style="margin-top:10px">
                  <a class="btn sm" style="flex:1" href="${esc(t.gamebanana)}" ${ext}>GameBanana ${icon('out')}</a>
                  <a class="btn sm" style="flex:1" href="${esc(t.github)}" ${ext}>${GH} GitHub</a>
                </div>
                ${t.repo ? `<a class="btn sm" style="margin-top:8px" href="${esc(t.repo)}" ${ext}>${GH} ${L('Ayrı repo', 'Separate repo')}: ${esc(t.repo.split('/').pop())}</a>` : ''}
                <div hidden>
                </div>
              </div>
              <div class="panel"><h3>${L('Bilgiler', 'Details')}</h3>
                <dl class="facts">
                  <dt>${L('Sürüm', 'Version')}</dt><dd>${esc(t.version)}</dd><dt>Platform</dt><dd>${esc(t.platform)}</dd>
                  <dt>${L('Dosya türleri', 'File types')}</dt><dd>${esc(t.fileTypes)}</dd><dt>${L('Son güncelleme', 'Last updated')}</dt><dd>${esc(t.updated)}</dd><dt>${L('Kategori', 'Category')}</dt><dd>${esc(t.category)}</dd>
                </dl>
              </div>
              <div class="panel"><h3>${L('Destek', 'Support')}</h3>
                <p class="card-text" style="margin-bottom:12px">${L('Bir hata mı buldun ya da fikrin mi var?', 'Found a bug or have an idea?')}</p>
                <div class="actions"><a class="btn sm" href="/contact/">${L('İletişim', 'Contact')}</a><a class="btn sm" href="${LINKS.issues}" ${ext}>${L('Hata bildir', 'Report a bug')} ${icon('out')}</a></div>
              </div>
            </aside>
          </div>
          <div class="tool-nav" style="margin-top:44px">
            <a href="/tools/${prev.slug}/"><small>← ${L('Önceki araç', 'Previous tool')}</small><b>${esc(prev.name)}</b></a>
            <a href="/tools/${next.slug}/"><small>${L('Sonraki araç', 'Next tool')} →</small><b>${esc(next.name)}</b></a>
          </div>
        </div>`;
    },

    maps: main => listPage(main, 'map'),
    skies: main => listPage(main, 'sky'),

    plugins(main) {
      $('#plugin-grid', main).innerHTML = PLUGINS.map(pluginCard).join('');
    },

    contact(main) {
      const b = $('#discord-copy', main), note = $('#discord-note', main);
      b?.addEventListener('click', async () => {
        const label = note.innerHTML;
        try { await navigator.clipboard.writeText(LINKS.discord); note.textContent = L('Kopyalandı: serhatondes', 'Copied: serhatondes'); note.classList.add('copied'); }
        catch { note.textContent = L('Kullanıcı adı: serhatondes', 'Username: serhatondes'); }
        setTimeout(() => { note.innerHTML = label; note.classList.remove('copied'); }, 2200);
      });
    },
  };

  async function listPage(main, kind) {
    const d = await (kind === 'map' ? data.maps() : data.skies());
    const items = d.items || [];
    const state = { q: '', cat: '', sort: 'downloads', limit: 24 };
    $('#list-count', main).textContent = fmt(d.count);
    $('#list-dl', main).textContent = fmt(d.downloads);
    const chips = $('#chips', main);
    if (chips && d.categories) {
      chips.innerHTML = `<button class="chip on" data-cat="">${L('Tümü', 'All')} <small>${d.count}</small></button>` +
        d.categories.map(c => `<button class="chip" data-cat="${esc(c.name)}">${esc(c.name)} <small>${c.count}</small></button>`).join('');
      chips.addEventListener('click', e => {
        const c = e.target.closest('[data-cat]'); if (!c) return;
        $$('.chip', chips).forEach(x => x.classList.toggle('on', x === c));
        state.cat = c.dataset.cat; state.limit = 24; draw();
      });
    }
    const norm = s => s.toLocaleLowerCase(LOCALE);
    $('#q', main).addEventListener('input', e => { state.q = norm(e.target.value.trim()); state.limit = 24; draw(); });
    $('#sort', main).addEventListener('change', e => { state.sort = e.target.value; draw(); });
    $('#more', main).addEventListener('click', () => { state.limit += 24; draw(); });
    const sorters = {
      downloads: (a, b) => b.downloads - a.downloads,
      likes: (a, b) => b.likes - a.likes || b.downloads - a.downloads,
      new: (a, b) => (b.date || 0) - (a.date || 0),
      az: (a, b) => a.name.localeCompare(b.name, LANG),
    };
    function draw() {
      const list = items.filter(m => (!state.cat || m.category === state.cat) && (!state.q || norm(m.name).includes(state.q))).sort(sorters[state.sort]);
      $('#result-note', main).textContent = `${fmt(list.length)} ${L('sonuç', list.length === 1 ? 'result' : 'results')}`;
      $('#list-grid', main).innerHTML = list.length ? list.slice(0, state.limit).map(m => workCard(m, kind)).join('') : `<div class="empty" style="grid-column:1/-1">${L('Sonuç bulunamadı.', 'No results found.')}</div>`;
      $('#more', main).hidden = list.length <= state.limit;
    }
    draw();
  }

  /* ---------- dil seçimi ---------- */
  // Sabit metinler sayfada iki dilde durur (data-l, site.css gösterir); öznitelikler ve başlık burada çevrilir.
  function applyLang() {
    if (LANG !== 'en') return;
    const b = document.body;
    if (b.dataset.titleEn) document.title = b.dataset.titleEn;
    if (b.dataset.descEn) $('meta[name="description"]')?.setAttribute('content', b.dataset.descEn);
    $$('[data-en]').forEach(el => { el.textContent = el.dataset.en; });
    $$('[data-en-placeholder]').forEach(el => { el.placeholder = el.dataset.enPlaceholder; });
    $$('[data-en-aria-label]').forEach(el => el.setAttribute('aria-label', el.dataset.enAriaLabel));
  }
  function wireLang(hdr) {
    $('[data-lang-btn]', hdr).addEventListener('click', () => {
      try { localStorage.setItem('gs-lang', LANG === 'en' ? 'tr' : 'en'); } catch { /* gizli pencere vb. */ }
      const u = new URL(location.href);
      u.searchParams.set('lang', LANG === 'en' ? 'tr' : 'en');
      location.replace(u);
    });
  }

  /* ---------- kopyalamaya karşı caydırıcılar ---------- */
  // Tarayıcıya gelen her şey görülebilir; bunlar yalnızca hızlı kopyalamayı zorlaştırır.
  function guard() {
    if (window.top !== window.self) { try { window.top.location = window.self.location; } catch { document.documentElement.hidden = true; } }
    const field = el => el.closest?.('input, textarea, select, [contenteditable]');
    document.addEventListener('contextmenu', e => { if (!field(e.target)) e.preventDefault(); });
    document.addEventListener('dragstart', e => { if (e.target.tagName === 'IMG' || e.target.tagName === 'CANVAS') e.preventDefault(); });
    document.addEventListener('keydown', e => {
      const k = e.key.toLowerCase(), mod = e.ctrlKey || e.metaKey;
      if (e.key === 'F12' || (mod && (k === 'u' || k === 's' || k === 'p')) || (mod && e.shiftKey && 'ijc'.includes(k))) e.preventDefault();
    });
    document.addEventListener('copy', e => {
      const sel = String(window.getSelection() || '');
      if (field(e.target) || sel.length < 40) return;
      e.preventDefault();
      e.clipboardData.setData('text/plain', `${sel}\n\n${L('Kaynak', 'Source')}: ${location.href} · © GoldSrc Studio`);
    });
    // Resimler sayfada <img> olarak kalmaz: hemen <canvas> ile değiştirilir, dosya sayfa dışında yüklenip
    // canvas'a çizilir. "Resim indirici" eklentileri sayfadaki <img> etiketlerini tarar, canvas'ı bulamaz.
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { io.unobserve(e.target); e.target._load(); } }), { rootMargin: '400px' });
    const shield = img => {
      const src = img.getAttribute('src');
      if (!src || /\.svg(\?|$)/i.test(src)) return;
      const c = document.createElement('canvas');
      c.className = img.className; c.classList.add('pimg');
      if (img.style.cssText) c.style.cssText = img.style.cssText;
      c.setAttribute('role', 'img'); c.setAttribute('aria-label', img.alt || '');
      const pix = getComputedStyle(img).imageRendering === 'pixelated';
      img.removeAttribute('src'); img.onerror = img.onload = null;
      img.replaceWith(c);
      c._load = () => {
        const im = new Image();
        im.onerror = () => c.remove();
        im.onload = () => {
          const r = c.getBoundingClientRect(), nw = im.naturalWidth, nh = im.naturalHeight;
          const fit = r.width ? Math.max(r.width / nw, r.height / nh) : 160 / nw;
          const k = nw * nh <= 65536 ? 1 : Math.min(1, fit * Math.min(window.devicePixelRatio || 1, 2));
          c.width = Math.max(1, Math.round(nw * k)); c.height = Math.max(1, Math.round(nh * k));
          const g = c.getContext('2d'); g.imageSmoothingQuality = 'high'; g.imageSmoothingEnabled = !pix;
          g.drawImage(im, 0, 0, c.width, c.height);
        };
        im.src = src;
      };
      io.observe(c);
    };
    const scan = root => { if (root.tagName === 'IMG') shield(root); else root.querySelectorAll?.('img').forEach(shield); };
    scan(document.body);
    new MutationObserver(ms => ms.forEach(m => m.addedNodes.forEach(scan))).observe(document.body, { childList: true, subtree: true });

    console.log('%cGoldSrc Studio', 'font:700 22px sans-serif;color:#5ab0ec');
    console.log(L('Bu sitenin tasarımı ve içeriği GoldSrc Studio / by Devil\'e aittir. İzinsiz kopyalanamaz.',
      'The design and content of this site belong to GoldSrc Studio / by Devil. Do not copy without permission.'));
  }

  /* ---------- başlat ---------- */
  async function init() {
    guard();
    applyLang();
    const hdr = $('#hdr'), ftr = $('#ftr'), main = $('main');
    let tools = [];
    try { tools = await data.tools(); } catch { /* menü araçsız da çalışır */ }
    hdr.className = 'hdr'; hdr.innerHTML = header(tools); wireHeader(hdr); wireTheme(hdr); wireLang(hdr);
    ftr.className = 'ftr'; ftr.innerHTML = footer(tools);
    palette();
    try { await pages[page]?.(main); }
    catch (err) { console.error(err); }
  }
  init();
})();
