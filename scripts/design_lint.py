#!/usr/bin/env python3
"""
design_lint.py — a facts-only design check, plus a "look fingerprint": did the three directions collide with each
other, and did they collide with recent projects.

It does not judge whether a design looks good (taste is the user's call); it only answers checkable questions:
  red light      broken images, text too small to read, insufficient contrast, console errors — must be fixed before delivery
  yellow light   template chrome: all-caps eyebrow labels, "A · B · C", trailing arrows, one word recolored… reflex
                 moves that appear by themselves and cost almost nothing to remove
  info           look families: warm-paper serif, dark single-accent, hairline newspaper, card kit. A family is not a
                 problem in itself — good designs often live inside one; change only when all three directions land in
                 the same family, or collide with a recent project in the look ledger
  fingerprint    background, accent palette, fonts, layout skeleton — feeds compare and ledger

Usage:
  python3 scripts/design_lint.py check a.html [b.html …] [--min-body 14] [--viewport 1440x900] [--json]
  python3 scripts/design_lint.py compare dir-1.html dir-2.html dir-3.html     are the three directions reskins of each other
  python3 scripts/design_lint.py ledger [--last 8]                           what recent deliveries looked like
  python3 scripts/design_lint.py ledger add final.html --project <name> [--note "…"]
  python3 scripts/design_lint.py ledger check dir-1.html dir-2.html …        do the new directions collide with recent projects

The look ledger lives at ~/.huashu-design/ledger.jsonl (override with HUASHU_DESIGN_HOME); it stays on this machine
and is never distributed with the skill.
Dependencies: pip install playwright pillow && playwright install chromium
"""

import argparse
import glob
import io
import json
import math
import os
import sys
from datetime import date
from pathlib import Path

# Clustering traits of AI-generated pages in 2026. Source: Anthropic's official frontend-design skill (2026)
# https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md
CREAM = (0xF4, 0xF1, 0xEA)
CLAY = (0xD9, 0x77, 0x57)

COLLECT_JS = r"""
() => {
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true });
  const cache = {};
  // any CSS color (incl. oklch/color-mix) → [r,g,b,a]: draw one pixel and read it back, rather than parsing it ourselves
  const rgba = (s) => {
    if (!s || s === 'transparent') return [0, 0, 0, 0];
    if (cache[s]) return cache[s];
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = s; cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    // alpha only ever appears as "the fourth component" or "after the /": the last number of rgb(187,187,187) is not alpha
    let a = 1; const inner = (/\(([^)]*)\)/.exec(s) || [])[1] || '';
    const parts = inner.split(/[\s,/]+/).filter(Boolean);
    const raw = inner.includes('/') ? parts[parts.length - 1] : (/^(rgba|hsla)\(/.test(s) && parts.length === 4 ? parts[3] : null);
    if (raw) a = raw.endsWith('%') ? parseFloat(raw) / 100 : parseFloat(raw);
    return (cache[s] = [d[0], d[1], d[2], a]);
  };
  const lum = ([r, g, b]) => { const f = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const opaqueBg = (e) => {   // returns [r,g,b,1], null (image/gradient/canvas — cannot compute) or undefined (transparent, keep looking)
    if (/^(IMG|VIDEO|CANVAS|PICTURE|IFRAME)$/.test(e.tagName) || e instanceof SVGElement) return null;
    const cs = getComputedStyle(e);
    if (cs.backgroundImage && cs.backgroundImage !== 'none') return null;
    const c = rgba(cs.backgroundColor); return c[3] > 0.9 ? c : undefined;
  };
  const bgOf = (el) => {
    const own = opaqueBg(el); if (own !== undefined) return own;   // a button/label's own background counts first
    const r = el.getBoundingClientRect(); const x = r.left + r.width / 2, y = r.top + r.height / 2;
    if (x >= 0 && y >= 0 && x < innerWidth && y < innerHeight) {
      for (const e of document.elementsFromPoint(x, y)) {
        if (e === el || el.contains(e)) continue;
        const b = opaqueBg(e); if (b !== undefined) return b;
      }
      return [255, 255, 255, 1];
    }
    for (let e = el.parentElement; e && e.nodeType === 1; e = e.parentElement) { const b = opaqueBg(e); if (b !== undefined) return b; }
    return [255, 255, 255, 1];
  };
  const opacityOf = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) o *= parseFloat(getComputedStyle(e).opacity); return o; };
  // text inside SVG counts at its rendered size (a viewBox may scale it up or down)
  const scaleOf = (el) => { if (!(el instanceof SVGElement) || !el.getScreenCTM) return 1; const m = el.getScreenCTM(); return m ? Math.hypot(m.a, m.b) || 1 : 1; };
  const CAPTION = 'figcaption, footer, small, caption, aside, sup, sub, [class*=caption], [class*=credit], [class*=footnote], [class*=meta]';
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.05; };
  const ownText = (el) => Array.from(el.childNodes).filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
  const fam = (s) => (s || '').split(',')[0].replace(/["']/g, '').trim();

  const out = { small: [], lowContrast: [], eyebrows: [], dots: 0, emDashLabels: 0, arrows: 0, numbered: [],
                accentWord: [], cardKit: 0, hairlines: 0, radiusZero: 0, radiusTotal: 0, monoSmall: 0,
                broken: [], fonts: {}, display: null, body: null, headlineSerif: false, textColors: {}, bg: null,
                bodySmall: [], relImgs: [], textTotal: 0 };

  const all = Array.from(document.body ? document.body.querySelectorAll('*') : []);
  const cardSig = {};
  let displayEl = null, maxFs = 0;   // display font = the font used by the largest text on the page
  for (const el of all) {
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    const t = ownText(el);
    const fs = parseFloat(cs.fontSize) * scaleOf(el);
    if (t.length > 1) {
      out.textTotal += t.length;
      if (fs > maxFs) { maxFs = fs; displayEl = el; }
      const f = fam(cs.fontFamily); out.fonts[f] = (out.fonts[f] || 0) + t.length;
      const col = rgba(cs.color); const key = col.slice(0, 3).join(',');
      out.textColors[key] = (out.textColors[key] || 0) + t.length * fs;
      if (fs < (window.__MIN_LABEL || 12)) out.small.push({ text: t.slice(0, 30), px: Math.round(fs) });
      // body-like text: a passage of 28+ characters that is not a caption/footer gets the body floor (p, li or div alike)
      if (t.length >= 28 && !el.closest(CAPTION) && fs < (window.__MIN_BODY || 14)) out.bodySmall.push({ text: t.slice(0, 30), px: Math.round(fs) });
      const bg = bgOf(el);
      if (bg) { const a = col[3] * opacityOf(el);   // semi-transparent text is blended with the background before contrast is computed
        const fg = [0, 1, 2].map((i) => col[i] * a + bg[i] * (1 - a));
        const c = contrast(fg, bg); const large = fs >= 24 || (fs >= 18.66 && parseInt(cs.fontWeight) >= 700);
        if (c < (large ? 3 : 4.5)) out.lowContrast.push({ text: t.slice(0, 30), ratio: Math.round(c * 100) / 100, px: fs }); }
      const latin = t.replace(/[^A-Za-z]/g, '');
      const caps = cs.textTransform === 'uppercase' || (latin.length >= 3 && latin === latin.toUpperCase());
      const ls = cs.letterSpacing === 'normal' ? 0 : parseFloat(cs.letterSpacing) / fs;
      if (caps && latin.length >= 2 && ls >= 0.06 && fs <= 15) out.eyebrows.push(t.slice(0, 30));
      if (/\s·\s/.test(t)) out.dots += (t.match(/\s·\s/g) || []).length;
      if (/^[A-Z][A-Z\s]{1,20}\s—\s\S/.test(t)) out.emDashLabels++;
      if (/→\s*$/.test(t) && (el.closest('a,button') || cs.cursor === 'pointer')) out.arrows++;
      if (/^0\d([\s./—-]|$)/.test(t) && t.length <= 6) out.numbered.push(t);
      if (/mono/i.test(cs.fontFamily) && fs <= 14) out.monoSmall++;
    }
    // card kit: the same border-radius + the same box-shadow recurring
    if (cs.boxShadow !== 'none' && parseFloat(cs.borderRadius) > 0) {
      const sig = cs.borderRadius + '|' + cs.boxShadow; cardSig[sig] = (cardSig[sig] || 0) + 1;
    }
    const r = el.getBoundingClientRect();
    if (r.width > 200 && ['Top', 'Bottom', 'Left', 'Right'].some((s) => cs['border' + s + 'Style'] !== 'none' && parseFloat(cs['border' + s + 'Width']) > 0 && parseFloat(cs['border' + s + 'Width']) <= 1)) out.hairlines++;
    if (r.width > 120 && r.height > 60 && (cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || cs.borderStyle !== 'none')) {
      out.radiusTotal++; if (parseFloat(cs.borderRadius) === 0) out.radiusZero++;
    }
  }
  out.cardKit = Math.max(0, ...Object.values(cardSig));

  // one word recolored/italicized inside a headline
  for (const h of document.querySelectorAll('h1, h2')) {
    if (!visible(h)) continue;
    const hs = getComputedStyle(h); const total = h.textContent.trim().length;
    for (const c of h.querySelectorAll('em, i, span, strong, b, mark')) {
      const cs = getComputedStyle(c); const n = c.textContent.trim().length;
      if (n > 0 && n <= total * 0.4 && (cs.color !== hs.color || cs.fontStyle !== hs.fontStyle || cs.fontFamily !== hs.fontFamily)) { out.accentWord.push(h.textContent.trim().slice(0, 40)); break; }
    }
  }
  const h = displayEl;
  if (h) { const cs = getComputedStyle(h); out.display = fam(cs.fontFamily);
    // only the first font actually in use counts: the sans-serif in "Inter, sans-serif" must not be read as a serif
    const first = cs.fontFamily.split(',').map((x) => x.replace(/["']/g, '').trim()).find((x) => document.fonts.check(`16px "${x}"`) || /^(serif|sans-serif|monospace)$/.test(x)) || out.display;
    out.headlineSerif = !/sans/i.test(first) && /(^serif$|garamond|newsreader|serif|caslon|playfair|fraunces|cormorant|tiempos|lora|baskerville|didot|bodoni|georgia|times|songti|宋|明朝|mincho)/i.test(first); }
  const p = Array.from(document.querySelectorAll('p, li')).find((e) => visible(e) && e.textContent.trim().length > 20);
  if (p) { const cs = getComputedStyle(p); out.body = fam(cs.fontFamily); out.bodyPx = parseFloat(cs.fontSize); }
  for (const img of document.images) {
    const src = img.getAttribute('src') || '';
    if (img.complete && img.naturalWidth === 0 && visible(img)) out.broken.push(src.slice(0, 80) || '(no src)');
    else if (src && !/^(data:|https?:|blob:)/.test(src)) out.relImgs.push(src.slice(0, 60));
  }
  out.bg = rgba(getComputedStyle(document.body).backgroundColor)[3] > 0.5 ? rgba(getComputedStyle(document.body).backgroundColor) : rgba(getComputedStyle(document.documentElement).backgroundColor);
  return out;
}
"""


# ---------- color ----------

def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def oklab(rgb):
    r, g, b = (_lin(x) for x in rgb[:3])
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def dist(a, b):
    return math.dist(oklab(a), oklab(b))


def lch(rgb):
    L, a, b = oklab(rgb)
    return L, math.hypot(a, b), (math.degrees(math.atan2(b, a)) + 360) % 360


def hexs(rgb):
    return '#%02X%02X%02X' % tuple(int(x) for x in rgb[:3])


def bg_class(rgb):
    L, C, H = lch(rgb)
    if L > 0.9:
        if C < 0.003:
            return 'light·neutral white'
        return 'light·warm paper' if 40 <= H <= 110 else 'light·tinted'
    if L < 0.28:
        return 'dark·near-black' if C < 0.03 else 'dark·tinted'
    return 'mid·tinted' if C > 0.04 else 'mid·grey'


def palette(png_bytes, n=6):
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes)).convert('RGB')
    im.thumbnail((240, 240))
    q = im.quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    return [{'hex': hexs(pal[i * 3:i * 3 + 3]), 'rgb': pal[i * 3:i * 3 + 3], 'share': round(c / total, 3)} for c, i in counts]


def layout_vector(png_bytes, w=32, h=20):
    """Layout skeleton: strip color, keep only the light/dark structure, then normalize — two versions that are
    reskins without a skeleton change will correlate strongly."""
    from PIL import Image, ImageFilter
    im = Image.open(io.BytesIO(png_bytes)).convert('L').filter(ImageFilter.FIND_EDGES).resize((w, h), Image.BILINEAR)
    v = list(im.tobytes())
    mu = sum(v) / len(v)
    sd = math.sqrt(sum((x - mu) ** 2 for x in v) / len(v)) or 1
    return [round((x - mu) / sd, 3) for x in v]


def corr(a, b):
    return sum(x * y for x, y in zip(a, b)) / len(a)


def palette_distance(p, q):
    """Mean nearest distance between two palettes (area-weighted, symmetric). Below 0.06 is essentially the same set
    of colors."""
    def one(x, y):
        return sum(c['share'] * min(dist(c['rgb'], d['rgb']) for d in y) for c in x) / (sum(c['share'] for c in x) or 1)
    return round((one(p, q) + one(q, p)) / 2, 3)


# ---------- collection ----------

def expand(paths):
    """Expand globs ourselves: PowerShell and quoted arguments won't do it for you."""
    out = []
    for p in paths:
        hits = sorted(glob.glob(p)) if any(c in p for c in '*?[') else [p]
        out += hits or [p]
    return out


def collect(paths, viewport=(1440, 900), min_body=14, min_label=12):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Check skipped: the Python playwright package is not installed. Install it and rerun: '
              'pip install playwright pillow && playwright install chromium',
              file=sys.stderr)
        sys.exit(0)
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for path in expand(paths):
            page = browser.new_page(viewport={'width': viewport[0], 'height': viewport[1]})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)[:160]))
            page.on('console', lambda m: errors.append(m.text[:160]) if m.type == 'error' else None)
            page.add_init_script(f'window.__MIN_BODY = {min_body}; window.__MIN_LABEL = {min_label};')
            try:
                page.goto(Path(path).resolve().as_uri(), wait_until='domcontentloaded', timeout=20000)
                try:   # don't let unreachable web fonts/CDNs stall the whole batch; wait at most 8 more seconds
                    page.wait_for_load_state('load', timeout=8000)
                except Exception:
                    errors.append('page load timed out (most likely web fonts or a CDN unreachable) — checking the content that did load')
                try:
                    page.evaluate('document.fonts.ready')
                except Exception:
                    pass
                page.wait_for_timeout(800)
                facts = page.evaluate(COLLECT_JS)
                shot = page.screenshot()
                facts['palette'] = palette(shot)
                facts['layout'] = layout_vector(shot)
            except Exception as e:
                facts = {'fatal': str(e).split('\n')[0][:200]}
            facts['errors'] = errors
            facts['path'] = str(Path(path).resolve())
            results.append(facts)
            page.close()
        browser.close()
    return results


def fingerprint(f):
    """A one-sentence plain-language description of this version's look, plus the numbers that can be compared."""
    bg = f['bg'] if f['bg'] and f['bg'][3] > 0.5 else f['palette'][0]['rgb']
    accents = [c for c in f['palette'] if lch(c['rgb'])[1] > 0.06 and c['share'] > 0.004][:2]
    serif = 'serif headline' if f['headlineSerif'] else 'sans-serif headline'
    desc = f'{bg_class(bg)} base {hexs(bg)}, {serif} ({f["display"] or "?"}), body {f["body"] or "?"}'
    if accents:
        desc += ', accents ' + '/'.join(c['hex'] for c in accents)
    return {'bg': hexs(bg), 'bg_class': bg_class(bg), 'display': f['display'], 'body': f['body'],
            'serif': f['headlineSerif'], 'palette': f['palette'], 'layout': f['layout'], 'desc': desc}


def judge(f):
    red, yellow = [], []
    if f.get('fatal'):
        return [f'Cannot open: {f["fatal"]}'], []
    if not f['textTotal']:
        yellow.append('No detectable text on the page (all images/canvas?) — the findings below rest on the screenshot palette alone')
    if f['broken']:
        red.append(f'{len(f["broken"])} broken images: {f["broken"][:3]}')
    if f['errors']:
        red.append(f'{len(f["errors"])} console errors: {f["errors"][:2]}')
    if f['bodySmall']:
        red.append(f'body font size below the floor in {len(f["bodySmall"])} places, e.g. {f["bodySmall"][:2]}')
    if len(f['small']) >= 3:
        red.append(f'text below the label floor in {len(f["small"])} places, e.g. {[(s["text"], s["px"]) for s in f["small"][:3]]}')
    if f['relImgs']:
        yellow.append(f'{len(f["relImgs"])} relative-path images ({f["relImgs"][:2]}): in a single-file delivery opened by '
                      f'double-click, moving one directory breaks them all — inline them as base64')
    if f['lowContrast']:
        red.append(f'insufficient contrast in {len(f["lowContrast"])} places, e.g. {f["lowContrast"][:3]}')

    chrome = []
    if len(f['eyebrows']) >= 3:
        chrome.append(f'{len(f["eyebrows"])} all-caps letter-spaced eyebrow labels ({f["eyebrows"][:3]})')
    if f['dots'] >= 2:
        chrome.append(f'"A · B · C" middot chains: {f["dots"]}')
    if f['emDashLabels']:
        chrome.append(f'"WORD — snippet" labels: {f["emDashLabels"]}')
    if f['arrows'] >= 2:
        chrome.append(f'trailing "→" arrows on links/buttons: {f["arrows"]}')
    if f['monoSmall'] >= 4:
        chrome.append(f'small monospace labels: {f["monoSmall"]}')
    if chrome:
        yellow.append('Template chrome: ' + '; '.join(chrome))
    if f['accentWord']:
        yellow.append(f'one recolored/italicized word inside a headline: {len(f["accentWord"])} places ({f["accentWord"][:2]})')
    if len(f['numbered']) >= 3:
        yellow.append(f'01/02/03 numbering: {len(f["numbered"])} — is the content really a sequence?')
    if f['display'] and f['display'].lower() in ('inter', 'roboto', 'arial', 'helvetica', 'system-ui', '-apple-system'):
        yellow.append(f'headline font is {f["display"]} (a UI text face used as display)')
    return red, yellow


def families(f):
    """Which common look family this version falls into. Description only, not a fault: used to compare the three
    directions and the ledger."""
    if f.get('fatal') or not f.get('palette'):
        return []
    out = []
    bg = f['bg'] if f['bg'] and f['bg'][3] > 0.5 else f['palette'][0]['rgb']
    cream = bg_class(bg) == 'light·warm paper'   # must be a warm hue: a light cool grey (e.g. #DFEBE5) is numerically close to cream too, but it is not this family
    clay = any(dist(c['rgb'], CLAY) < 0.07 for c in f['palette']) or \
        any(dist([int(x) for x in k.split(',')], CLAY) < 0.07 for k in f['textColors'])
    if cream and (clay or f['headlineSerif']):
        parts = ['warm cream base'] + (['terracotta accent'] if clay else []) + (['serif display headline'] if f['headlineSerif'] else [])
        out.append('warm-paper serif·' + ' + '.join(parts) + " (also Claude's own palette)")
    L, C, _ = lch(bg)
    vivid = [c for c in f['palette'] if lch(c['rgb'])[1] > 0.15]
    if L < 0.2 and len(vivid) == 1:
        out.append(f'dark single-accent·near-black base + one bright accent ({vivid[0]["hex"]})')
    if f['hairlines'] >= 8 and f['radiusTotal'] and f['radiusZero'] / f['radiusTotal'] > 0.9:
        out.append(f'hairline newspaper·{f["hairlines"]} 1px hairlines, zero corner radius')
    if f['cardKit'] >= 4:
        out.append(f'card kit·same radius + same shadow repeated {f["cardKit"]} times')
    return out


# ---------- look ledger ----------

def ledger_file():
    return Path(os.environ.get('HUASHU_DESIGN_HOME') or Path.home() / '.huashu-design') / 'ledger.jsonl'


def ledger_read(last=None):
    f = ledger_file()
    rows = [json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip()] if f.exists() else []
    return rows[-last:] if last else rows


def ledger_summary(rows):
    if not rows:
        return (f'The look ledger is empty ({ledger_file()}). Record an entry with ledger add after each delivery; '
                f'only then can the next project actively steer away.')
    lines = [f'Looks of the last {len(rows)} deliveries (new projects: actively avoid the few that keep recurring):']
    for r in rows:
        lines.append(f'  {r["date"]} {r["project"]}: {r["desc"]}' + (f'  // {r["note"]}' if r.get('note') else ''))
    n = len(rows)
    tally = {}
    for r in rows:
        for k in (r['bg_class'] + ' base', 'serif headline' if r['serif'] else 'sans-serif headline', 'font ' + (r['display'] or '?')):
            tally[k] = tally.get(k, 0) + 1
    rep = [f'{k} {v}/{n}' for k, v in sorted(tally.items(), key=lambda x: -x[1]) if v >= max(2, n * 0.5)]
    if rep:
        lines.append('Recurring: ' + ', '.join(rep) + ' — this time, at least one direction must not land here again')
    return '\n'.join(lines)


def similar(a, b, brand=False, ignore_layout=False):
    """Returns where two versions collide (empty = no collision). brand=colors and fonts are brand-constrained,
    compare skeletons only; ignore_layout=for forms whose skeletons are naturally identical, e.g. an app on several
    devices side by side."""
    hits = []
    pd = palette_distance(a['palette'], b['palette'])
    lc = corr(a['layout'], b['layout'])
    if pd < 0.06 and not brand:
        hits.append(f'palettes nearly identical (distance {pd})')
    if lc > 0.55 and not ignore_layout:
        hits.append(f'layout skeletons highly similar (correlation {lc:.2f})')
    if not brand and a['bg_class'] == b['bg_class'] and a['serif'] == b['serif'] and (a['display'] or '').lower() == (b['display'] or '').lower():
        hits.append(f'same background class + same headline font ({a["bg_class"]}, {a["display"]})')
    return hits, pd, lc


# ---------- commands ----------

def cmd_check(a):
    res = collect(a.files, a.viewport, a.min_body, a.min_label)
    worst = 0
    out = []
    for f in res:
        red, yellow = judge(f)
        fp = fingerprint(f) if not f.get('fatal') else {'desc': '(cannot open)'}
        worst = max(worst, 1 if red else 0)
        out.append({'path': f['path'], 'red': red, 'yellow': yellow, 'families': families(f), 'look': fp['desc']})
        if not a.json:
            print(f'\n■ {f["path"]}\n  Look: {fp["desc"]}')
            for r in red:
                print(f'  🔴 {r}')
            for y in yellow:
                print(f'  🟡 {y}')
            for i in families(f):
                print(f'  ℹ️  Look family {i}')
            if not red and not yellow:
                print('  ✓ No red lights, no template chrome')
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif any(o['yellow'] for o in out):
        print('\n🟡 Template chrome is a reflex move: if the brief asks for it, keep it; otherwise delete the structure '
              '(e.g. the whole eyebrow line) — swapping in a different symbol to dodge the check does not count as a fix.'
              '\nℹ️  Look families need no fixing; they only matter in compare / ledger check.')
    return worst


def cmd_compare(a):
    res = collect(a.files, a.viewport, a.min_body, a.min_label)
    failed = [f for f in res if f.get('fatal')]
    if failed:
        for f in failed:
            print(f'Cannot open, comparison aborted: {f["path"]}: {f["fatal"]}')
        return 2
    fps = [fingerprint(f) for f in res]
    names = [Path(f['path']).name for f in res]
    print('Looks of the three directions:')
    for n, fp in zip(names, fps):
        print(f'  {n}: {fp["desc"]}')
    bad = 0
    for i in range(len(fps)):
        for j in range(i + 1, len(fps)):
            hits, pd, lc = similar(fps[i], fps[j], a.brand, a.ignore_layout)
            print(f'  {names[i]} ↔ {names[j]}: palette distance {pd}, skeleton correlation {lc:.2f}' + (f' → collision: {"; ".join(hits)}' if hits else ''))
            bad += bool(hits)
    if len(fps) >= 3 and len({fp['bg_class'] for fp in fps}) == 1 and not a.brand:
        print(f'  🟡 All three directions share one background class ({fps[0]["bg_class"]}) — the user is seeing three variants of a single temperament')
        bad += 1
    fams = [{x.split('·')[0] for x in families(f)} for f in res]
    shared = set.intersection(*fams) if len(fams) >= 3 else set()
    if shared and not a.brand:
        print(f'  🟡 All three directions land in the same look family ({", ".join(sorted(shared))}) — keeping one or two in it is fine; all three in it is three variants of a single temperament')
        bad += 1
    print('  ✓ The three directions are distinct' if not bad else '  → Redo the colliding direction from its direction card: change the skeleton or the sources, not the colors')
    return 1 if bad else 0


def cmd_ledger(a):
    if a.action == 'add':
        if not a.files or not a.project:
            print('Usage: design_lint.py ledger add final.html --project <name> [--note "…"]', file=sys.stderr)
            return 2
        f = collect(a.files[:1], a.viewport, a.min_body, a.min_label)[0]
        if f.get('fatal'):
            print(f'Cannot open, nothing recorded: {f["fatal"]}', file=sys.stderr)
            return 2
        fp = fingerprint(f)
        p = Path(a.files[0]).resolve().parent
        if p.name == 'design-demos':
            p = p.parent
        row = {'date': date.today().isoformat(), 'project': a.project, 'project_dir': str(p), 'file': f['path'],
               'note': a.note or '', **{k: fp[k] for k in ('desc', 'bg', 'bg_class', 'display', 'body', 'serif', 'palette', 'layout')}}
        ledger_file().parent.mkdir(parents=True, exist_ok=True)
        with ledger_file().open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
        print(f'Recorded → {ledger_file()}\n  {a.project}: {fp["desc"]}')
        return 0
    rows = ledger_read(a.last)
    if a.action == 'check':
        if not rows:
            print(ledger_summary(rows))
            return 0
        res = [f for f in collect(a.files, a.viewport, a.min_body, a.min_label) if not f.get('fatal')]
        bad = 0
        for f in res:
            fp = fingerprint(f)
            clash = [(r, similar(fp, r)[0]) for r in rows]
            clash = [(r, h) for r, h in clash if h]
            print(f'■ {Path(f["path"]).name}: {fp["desc"]}')
            for r, h in clash:
                print(f'  🟡 Collides with {r["date"]} {r["project"]}: {"; ".join(h)}')
            bad += bool(clash)
        if bad == len(res):
            print('→ Every direction collides with recent projects: let at least one direction leave the recently recurring look behind entirely')
        return 1 if bad == len(res) else 0
    print(ledger_summary(rows))
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):   # Windows consoles are not UTF-8 by default; don't let one emoji crash the check
        try:
            stream.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass
    p = argparse.ArgumentParser(description='A facts-only design check + look fingerprint')
    sub = p.add_subparsers(dest='cmd', required=True)

    def common(sp):
        sp.add_argument('--viewport', default='1440x900', type=lambda s: tuple(int(x) for x in s.lower().split('x')))
        sp.add_argument('--min-body', type=float, default=14, help='minimum body font size; 24 for decks; 36 for 1080-wide long-form images meant for phones')
        sp.add_argument('--min-label', type=float, default=12, help='minimum label/caption font size; 16 for decks; 28 for 1080-wide long-form images meant for phones')
        sp.add_argument('--brand', action='store_true', help='compare: colors and fonts are brand-constrained, compare skeletons only')
        sp.add_argument('--ignore-layout', action='store_true', help='compare: forms whose skeletons are naturally identical, e.g. an app on several devices side by side')
        sp.add_argument('--json', action='store_true')
    c = sub.add_parser('check')
    c.add_argument('files', nargs='+')
    common(c)
    c = sub.add_parser('compare')
    c.add_argument('files', nargs='+')
    common(c)
    c = sub.add_parser('ledger')
    c.add_argument('action', nargs='?', choices=['list', 'add', 'check'], default='list')
    c.add_argument('files', nargs='*')
    c.add_argument('--project')
    c.add_argument('--note')
    c.add_argument('--last', type=int, default=8)
    common(c)
    a = p.parse_args(argv)
    return {'check': cmd_check, 'compare': cmd_compare, 'ledger': cmd_ledger}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
