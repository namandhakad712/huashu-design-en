#!/usr/bin/env python3
"""Render the style specimens to images, and assemble one overview sheet per section.

Specimens are assets/style-specimens/<section>/<number-name>.html, 1200×750, with the style name in <title>.
Renders go to the same-named .jpg; each section also gets a sheet-<section>.jpg to take in every style of that section at a glance.

Usage (from the skill root):
  python3 scripts/build_specimens.py              # re-render everything
  python3 scripts/build_specimens.py web app      # render only these sections
  python3 scripts/build_specimens.py --sheets     # only re-assemble the overview sheets
  python3 scripts/build_specimens.py assets/style-specimens/web/03-x.html   # render only these files, no sheets
"""

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'assets' / 'style-specimens'
W, H = 1200, 750
COLS = 4


def groups(names):
    found = sorted(p for p in ROOT.iterdir() if p.is_dir())
    return [g for g in found if not names or g.name in names]


def render(page, src):
    page.goto(src.resolve().as_uri(), wait_until='networkidle', timeout=45000)
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(300)
    page.screenshot(path=str(src.with_suffix('.jpg')), type='jpeg', quality=82)


def sheet(page, group):
    items = []
    for src in sorted(group.glob('*.html')):
        jpg = src.with_suffix('.jpg')
        if not jpg.exists():
            continue
        title = src.stem
        text = src.read_text(encoding='utf-8')
        if '<title>' in text:
            title = text.split('<title>', 1)[1].split('</title>', 1)[0].strip()
        items.append((jpg, title))
    if not items:
        return None
    cells = ''.join(
        f'<figure><img src="{jpg.resolve().as_uri()}"><figcaption>{html.escape(t)}</figcaption></figure>'
        for jpg, t in items)
    doc = f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;padding:24px;background:#d9d9d6;font:600 15px/1.35 -apple-system,"PingFang SC","Noto Sans SC",sans-serif;color:#1a1a1a}}
.g{{display:grid;grid-template-columns:repeat({COLS},300px);gap:18px 14px}}
figure{{margin:0}} img{{width:300px;height:{300 * H // W}px;display:block;box-shadow:0 0 0 1px rgba(0,0,0,.15)}}
figcaption{{margin-top:6px}}</style><div class="g">{cells}</div>'''
    tmp = group / '.sheet.html'
    tmp.write_text(doc, encoding='utf-8')
    page.set_viewport_size({'width': COLS * 314 + 34, 'height': 600})
    page.goto(tmp.resolve().as_uri(), wait_until='load')
    out = ROOT / f'sheet-{group.name}.jpg'
    page.screenshot(path=str(out), full_page=True, type='jpeg', quality=80)
    tmp.unlink()
    return out


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    only_sheets = '--sheets' in argv
    files = [Path(a) for a in argv if a.endswith('.html')]
    names = [a for a in argv if not a.startswith('--') and not a.endswith('.html')]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Playwright required: pip install playwright && python3 -m playwright install chromium')
        return 2
    failed = []
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print('Chromium failed to launch:', str(e).splitlines()[0], '\nInstall it: python3 -m playwright install chromium')
            return 2
        page = browser.new_page(viewport={'width': W, 'height': H})
        for src in files:
            try:
                render(page, src)
                print('✓', src)
            except Exception as e:
                failed.append(src.name)
                print('✗', src, e)
        for g in ([] if files else groups(names)):
            if not only_sheets:
                for src in sorted(g.glob('*.html')):
                    try:
                        render(page, src)
                        print('✓', src.relative_to(ROOT))
                    except Exception as e:  # one failed render doesn't sink the whole batch
                        failed.append(src.name)
                        print('✗', src.relative_to(ROOT), e)
            out = sheet(page, g)
            if out:
                print('Overview', out.relative_to(ROOT.parent.parent))
        browser.close()
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
