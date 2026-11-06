#!/usr/bin/env python3
"""Slice Xiaohongshu image-text HTML into 3:4 images, and check the spots that would bite on a phone.

HTML conventions (write them like the templates in assets/style-specimens/xhs/):
  <section class="xhs-page">         one page, 1242×1660
  <section class="xhs-strip" style="--n:3">   one long scroll, 1242×N wide, cut into N images
Pages are numbered and emitted in document order: 01.png 02.png …, plus one sheet.jpg to take it all in at a glance.

Checks four things (reports facts only; whether to fix them is your call):
  ✗ font size under the floor: any text < --min-label; paragraphs that wrap onto two or more lines < --min-body
  ✗ text outside the page: clipped glyphs
  ✗ text across a seam: in a long scroll a line of text crosses the joint between two images and gets cut while swiping
  ✗ text overlapping text: the boxes of two text runs overlap
  ! text covered: another element (sticker, color block) sits on top of the text's left/middle/right points
  ! text crowded against a graphic: the text box touches a small color block that holds no text (grid cells, dots), no matter which is on top
Add data-overlap-ok to elements you stack on purpose. No ✗ does not mean shippable — still go through sheet.jpg image by image.

Usage (from the skill root or anywhere):
  python3 scripts/xhs_render.py note.html [more.html] --out images/ [--jpg] [--min-body 42 --min-label 32]
Exit code: 1 when there is a ✗.
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

W, H = 1242, 1660

PROBE = r'''([minBody, minLabel]) => {
  const secs = [...document.querySelectorAll('.xhs-page, .xhs-strip')];
  const out = [];
  secs.forEach((sec, si) => {
    window.scrollTo(0, 0);   // taken without scrolling, sr is in page coordinates
    const sr = sec.getBoundingClientRect();
    const n = sec.classList.contains('xhs-strip') ? Math.round(sr.width / 1242) : 1;
    const items = [];
    const walk = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walk.nextNode())) {
      const t = node.textContent.replace(/\s+/g, ' ').trim();
      if (!t) continue;
      const el = node.parentElement, cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) === 0) continue;
      const range = document.createRange(); range.selectNodeContents(node);
      const rects = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1);
      if (!rects.length) continue;
      // font size as actually displayed: count any scale on ancestors too
      let k = 1, p = el; while (p && p !== sec) { const tf = getComputedStyle(p).transform; if (tf && tf !== 'none') { const d = new DOMMatrix(tf); k *= Math.hypot(d.a, d.b); } p = p.parentElement; }
      const px = parseFloat(cs.fontSize) * k;
      const lines = new Set(rects.map(r => Math.round(r.top / (px * 0.6)))).size;
      items.push({ el, t: t.slice(0, 24), len: t.length, lines, px: Math.round(px * 10) / 10, ok: !!el.closest('[data-overlap-ok]'),
                   rects: rects.map(r => [r.left - sr.left, r.top - sr.top, r.right - sr.left, r.bottom - sr.top]) });
    }
    const issues = [];
    for (const it of items) {
      if (it.px < minLabel) issues.push(['✗', `font size ${it.px}px < label floor ${minLabel}px`, it.t]);
      else if (it.lines >= 2 && it.len >= 16 && it.px < minBody) issues.push(['✗', `body font size ${it.px}px < body floor ${minBody}px`, it.t]);
      for (const [l, t, r, b] of it.rects) {
        if (l < -2 || t < -2 || r > sr.width + 2 || b > sr.height + 2) { issues.push(['✗', 'text outside the page', it.t]); break; }
      }
      if (n > 1) for (const [l, t, r, b] of it.rects) {
        const seam = [...Array(n - 1)].map((_, j) => (j + 1) * 1242).find(x => l < x - 4 && r > x + 4);
        if (seam) { issues.push(['✗', `text across seam ${seam / 1242}`, it.t]); break; }
      }
    }
    // a text box is taller than the glyphs (it carries the leading above and below); trim 20% off top and bottom before comparing, so adjacent lines of the same paragraph don't count as overlap
    const core = ([l, t, r, b]) => { const d = (b - t) * 0.2; return [l + 2, t + d, r - 2, b - d]; };
    const hit = (a, b) => { a = core(a); b = core(b); return a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3]; };
    for (let i = 0; i < items.length; i++) for (let j = i + 1; j < items.length; j++) {
      const a = items[i], b = items[j];
      if (a.ok || b.ok || a.el.contains(b.el) || b.el.contains(a.el)) continue;  // inline fragments within the same run don't count
      if (a.rects.some(x => b.rects.some(y => hit(x, y)))) issues.push(['✗', 'text overlapping text', `${a.t} / ${b.t}`]);
    }
    // text covered: scroll to the left/middle/right points of each line and see whether the topmost element is this text itself
    for (const it of items) {
      if (it.ok) continue;
      let found = null;
      for (const [l, t, r, b] of it.rects) {
        const w = r - l, h = b - t, vert = h > w * 1.5;   // vertical text: sample points along the long edge
        const pts = vert ? [t + w * 0.3, (t + b) / 2, b - w * 0.3].map(y => [sr.left + (l + r) / 2, sr.top + y])
                         : [l + h * 0.3, (l + r) / 2, r - h * 0.3].map(x => [sr.left + x, sr.top + (t + b) / 2]);
        for (const [cx, cy] of pts) {
          window.scrollTo(cx - innerWidth / 2, cy - innerHeight / 2);
          const px = cx - window.scrollX, py = cy - window.scrollY, hitEl = document.elementFromPoint(px, py);
          if (!hitEl || hitEl === it.el || it.el.contains(hitEl) || hitEl.contains(it.el) || hitEl.closest('[data-overlap-ok]')) continue;
          // at big sizes with line-height:1 glyphs stick out of their box; the hit test still counts them. If the point isn't inside the other box, skip it (text overlapping text has its own check)
          const hb = hitEl.getBoundingClientRect();
          if (px < hb.left || px > hb.right || py < hb.top || py > hb.bottom) continue;
          found = hitEl; break;
        }
        if (found) break;
      }
      if (found) issues.push(['!', found.tagName === 'IMG' ? 'text over an image box (transparent padding counts — take a look)' : 'text covered by another element', it.t]);
    }
    // text crowded against graphics: regardless of stacking, a text box touches a small color block holding no text (grid cells, dots, markers; long edge < 120px).
    // Most common when a grid collapses into one column or a chart overflows. Big backdrops usually sit as siblings of the text, so they don't count.
    const shapes = [...sec.querySelectorAll('*')].filter(e => {
      if (e.closest('[data-overlap-ok]') || e.textContent.trim() || e.children.length || e.closest('svg')) return false;
      const q = e.getBoundingClientRect();
      if (Math.max(q.width, q.height) >= 120) return false;
      const bg = getComputedStyle(e).backgroundColor;
      return bg && !/rgba\(.*,\s*0\)$/.test(bg) && bg !== 'transparent';
    });
    window.scrollTo(0, 0);
    for (const it of items) {
      if (it.ok) continue;
      const hitShape = shapes.find(e => {
        const q = e.getBoundingClientRect(), g = [q.left - sr.left, q.top - sr.top, q.right - sr.left, q.bottom - sr.top];
        return q.width > 0 && q.height > 0 && it.rects.some(x => hit(x, g));
      });
      if (hitShape) issues.push(['!', 'text crowded against a graphic', it.t]);
    }
    out.push({ index: si, n, w: Math.round(sr.width), h: Math.round(sr.height), issues });
  });
  return out;
}'''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--out', default='xhs-out', help='output directory')
    ap.add_argument('--jpg', action='store_true', help='also save a jpg copy (quality 92, faster to upload)')
    ap.add_argument('--min-body', type=float, default=42, help='body floor, on a 1242-wide canvas (= 36 at 1080 wide)')
    ap.add_argument('--min-label', type=float, default=32, help='label floor, on a 1242-wide canvas (= 28 at 1080 wide)')
    ap.add_argument('--no-check', action='store_true')
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
        from PIL import Image
    except ImportError:
        sys.exit('Playwright and Pillow required: pip install playwright pillow && python3 -m playwright install chromium')

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    made, bad = [], 0
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            sys.exit(f'Chromium failed to launch: {str(e).splitlines()[0]}\nInstall it: python3 -m playwright install chromium')
        page = browser.new_page(viewport={'width': W, 'height': H})
        for f in a.files:
            src = Path(f).resolve()
            try:
                page.goto(src.as_uri(), wait_until='networkidle', timeout=30000)
            except Exception:   # usually a webfont link that didn't come back on a slow or dead network; keep going with whatever has loaded
                print(f'  ! {src.name}: network resources not fully loaded within 30 s (most likely a webfont link); falling back to system fonts and rendering anyway')
            page.evaluate('document.fonts.ready')
            page.wait_for_timeout(400)
            secs = page.locator('.xhs-page, .xhs-strip')
            if secs.count() == 0:
                print(f'✗ {src.name}: no .xhs-page / .xhs-strip'); bad += 1; continue
            report = [] if a.no_check else page.evaluate(PROBE, [a.min_body, a.min_label])
            for i in range(secs.count()):
                fd, tmp = tempfile.mkstemp(suffix='.png', prefix='xhs-strip-')   # intermediate images go to the system temp dir, one per process
                os.close(fd); tmp = Path(tmp)
                secs.nth(i).screenshot(path=str(tmp))
                im = Image.open(tmp).convert('RGB')
                n = max(1, round(im.width / W))
                first = len(made) + 1
                for k in range(n):
                    piece = im.crop((k * W, 0, (k + 1) * W, H))
                    name = out / f'{len(made) + 1:02d}.png'
                    piece.save(name)
                    if a.jpg:
                        piece.save(name.with_suffix('.jpg'), quality=92)
                    made.append(name)
                tmp.unlink()
                label = f'{first:02d}' if n == 1 else f'{first:02d}–{len(made):02d}'
                for lvl, what, txt in (report[i]['issues'] if report else []):
                    print(f'  {lvl} page {label}  {what}: {txt}')
                    bad += lvl == '✗'
        browser.close()

    if made:
        cols, tw = 6, 300
        th = tw * H // W
        rows = (len(made) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * (tw + 12) + 12, rows * (th + 12) + 12), (217, 217, 214))
        for k, f in enumerate(made):
            sheet.paste(Image.open(f).convert('RGB').resize((tw, th)), (12 + (k % cols) * (tw + 12), 12 + (k // cols) * (th + 12)))
        sheet.save(out / 'sheet.jpg', quality=85)
    print(f'{"✓" if not bad else "✗"} {len(made)} images → {out}/ (overview in sheet.jpg)' + (f', {bad} to fix' if bad else ''))
    if len(made) > 18:
        print('  ! Xiaohongshu allows at most 18 images per post')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
