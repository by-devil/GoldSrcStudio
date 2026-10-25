#!/usr/bin/env python3
"""motd-fit: CS 1.6 MOTD sayfalarini her oyun cozunurlugune sigdiran CSS ureticisi.

MOTD penceresi yuksekligi ~ ekran yuksekliginin 0.6 kati (1024x768 -> ~460px,
800x600 -> ~360px, 640x480 -> ~288px). Bu arac, CSS dosyanizdaki px degerlerini
(font-size, padding, margin, line-height) okuyup 13 adet
@media screen and (max-height:Npx) basamagi uretir. transform/zoom kullanmaz:
eski MOTD tarayicilarinda (Chromium 535) tiklama noktasi kaymaz.

Kullanim:
  python3 motd_fit.py style.css                      # tum kurallar
  python3 motd_fit.py style.css --only ".nav a,.card" # sadece bu seciciler (| ile ayir)
  python3 motd_fit.py style.css --skip ".logo|.icon"
Cikti dosyanin sonuna /* motd-fit:start */ ... /* motd-fit:end */ arasina yazilir;
tekrar calistirmak eski blogu degistirir. --stdout ile sadece ekrana basar.
"""
import argparse, re, sys

# (max-height px, yazi carpani, bosluk carpani) - top15 (Rank System Ultimate) basamaklari
STEPS = [(525, .97, .93), (515, .95, .90), (500, .93, .86), (455, .90, .78), (450, .89, .76),
         (432, .87, .72), (400, .84, .66), (385, .82, .62), (360, .79, .56), (335, .76, .50),
         (330, .75, .48), (288, .70, .40), (265, .66, .36)]
MIN_FONT = 9
PROPS = re.compile(r'^(font-size|line-height|padding(-\w+)?|margin(-\w+)?)$')
START, END = '/* motd-fit:start */', '/* motd-fit:end */'

def top_level_rules(css):
    """@media/@keyframes disindaki (selector, govde) ciftleri."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    flat, depth, at = [], 0, False
    for i, ch in enumerate(css):
        if depth == 0 and ch == '@': at = True
        if ch == '{': depth += 1
        if not at: flat.append(ch)
        if ch == '}':
            depth -= 1
            if depth == 0: at = False
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', ''.join(flat))]

KEEP = 30   # bu ve ustu bosluklar genelde ikon/avatar yeri: dokunulmaz

def scale(prop, val, f_font, f_space):
    def fs(n):
        if n < 14: f = 1 - (1 - f_font) * .7            # kucuk yazi okunur kalsin
        elif n < 20: f = f_font
        else: f = (f_font + f_space) / 2                 # buyuk basliklar daha cok kuculur
        return max(MIN_FONT, round(n * f))
    if prop == 'font-size':
        return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: '%dpx' % fs(float(m.group(1))), val)
    if prop == 'line-height':
        return re.sub(r'(\d+(?:\.\d+)?)px', lambda m: '%dpx' % round(float(m.group(1)) * f_font), val)
    # padding/margin: ust-alt daha cok, sag-sol az kuculur
    toks = val.split()
    if prop.endswith(('-left', '-right')): axes = ['h']
    elif prop.endswith(('-top', '-bottom')) or len(toks) == 1: axes = ['v'] * len(toks)
    else: axes = {2: ['v', 'h'], 3: ['v', 'h', 'v'], 4: ['v', 'h', 'v', 'h']}.get(len(toks), ['v'] * len(toks))
    out = []
    for t, ax in zip(toks, axes):
        m = re.match(r'^(-?\d+(?:\.\d+)?)px$', t)
        if not m or abs(float(m.group(1))) >= KEEP: out.append(t); continue
        n = float(m.group(1)); f = f_space if ax == 'v' else 1 - (1 - f_font) * 1.5
        out.append('%dpx' % round(n * f))
    return ' '.join(out)

def build(css, only=None, skip=None):
    # ayni secici birden cok kez yazildiysa birlestir (sonraki kazanir; !important olan olcekten cikar)
    rules = {}
    for sel, body in top_level_rules(css):
        if only and sel not in only: continue
        if skip and any(s in sel for s in skip): continue
        d = rules.setdefault(sel, {})
        for decl in body.split(';'):
            if ':' not in decl: continue
            p, v = (x.strip() for x in decl.split(':', 1))
            if p == 'height' and 'px' in v: d['__h'] = 1
            if not PROPS.match(p): continue
            if p == 'line-height' and d.get('__h'): continue
            if 'px' in v and '!important' not in v: d.pop(p, None); d[p] = v
            else: d.pop(p, None)
    rules = [(k, [(p, x) for p, x in v.items() if p != '__h']) for k, v in rules.items()]
    rules = [r for r in rules if r[1]]
    out = [START, '/* motd-fit (MIT): MOTD yuksekligine gore otomatik kucultme */']
    prev = {}
    for h, ff, fs in STEPS:
        body = []
        for sel, decls in rules:
            ch = []
            for p, v in decls:
                nv = scale(p, v, ff, fs)
                if prev.get((sel, p), v) != nv: ch.append('%s:%s' % (p, nv))   # degismeyeni onceki basamak zaten veriyor
                prev[(sel, p)] = nv
            if ch: body.append('%s{%s}' % (sel, ';'.join(ch)))
        if body: out.append('@media screen and (max-height:%dpx){\n%s\n}' % (h, '\n'.join(body)))
    out.append(END)
    return '\n'.join(out)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('css'); ap.add_argument('--only'); ap.add_argument('--skip'); ap.add_argument('--stdout', action='store_true')
    a = ap.parse_args()
    src = open(a.css, encoding='utf-8').read()
    for m in re.finditer(r'@media[^{]*max-width[^{]*\{', src):
        if 'height' not in m.group(0) and re.search(r'width:\s*100%', src[m.end():m.end() + 3000].split('\n}')[0]):
            print('UYARI: "%s" tek sutun yapiyor olabilir. 800x600 MOTD 720px\'ten dar; kartlar alt alta '
                  'dizilip sayfa uzar. "and (min-height:471px)" ekleyin (README > Tuzaklar).' % m.group(0).strip(' {'), file=sys.stderr)
    base = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', src, flags=re.S).rstrip()
    block = build(base, a.only and [s.strip() for s in a.only.split('|')], a.skip and [s.strip() for s in a.skip.split('|')])
    if a.stdout: print(block); return
    open(a.css, 'w', encoding='utf-8').write(base + '\n\n' + block + '\n')
    print('%s: %d basamak yazildi' % (a.css, len(STEPS)), file=sys.stderr)

if __name__ == '__main__':
    main()
