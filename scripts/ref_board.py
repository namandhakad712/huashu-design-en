#!/usr/bin/env python3
"""Screenshot reference works into a reference board, so the agent has actually "seen" them before starting.

Write the words "reference Stripe Press" and the model produces its average impression of Stripe Press;
put a screenshot in front of its eyes and it will go measure the grid, compare font sizes, pick the colors.

Usage:
  python3 scripts/ref_board.py <url-or-image> [<url-or-image> …] --out refs/board.jpg [--full]

  URLs: opened in a headless browser; the first screen is captured (--full captures the whole page, up to 4000px tall)
  Images: local paths or image URLs (.jpg/.png/.webp/.gif), placed on the board as-is
  Each source is saved as its own shot (board-1.jpg …, the board's name plus an index, so it never overwrites screenshots you put into refs/ yourself), then one combined board is assembled.
  Sources that won't open, and shots that come back almost a solid color (common with WebGL sites), are listed — the run never aborts.

Once you have the image, open the board with your image-viewing ability and write "what exactly is being borrowed" as concrete rules
(how many grid columns, the heading-to-body font-size ratio, the dominant color's share, the text-image relationship), not "referenced its style".
"""

import argparse
import html
import sys
from pathlib import Path

IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif')


def shoot(page, src, out, full):
    if Path(src).exists():
        src = Path(src).resolve().as_uri()
    if src.lower().split('?')[0].endswith(IMG_EXT):
        page.set_viewport_size({'width': 1440, 'height': 900})
        r = page.goto(src, wait_until='load', timeout=30000)   # the browser opens the image directly and wraps it in an <img> itself
        if (r and not r.ok) or not page.evaluate('document.images[0] && document.images[0].naturalWidth'):
            raise RuntimeError(f'Image failed to load (HTTP {r.status if r else "?"})')
        page.locator('img').first.screenshot(path=str(out), type='jpeg', quality=82)
        return
    page.set_viewport_size({'width': 1440, 'height': 900})
    page.goto(src, wait_until='domcontentloaded', timeout=30000)
    try:
        page.wait_for_load_state('networkidle', timeout=8000)
    except Exception:
        pass  # sites with long-lived connections never reach networkidle; the first screen is usually enough
    page.wait_for_timeout(800)
    if full:
        h = min(page.evaluate('document.documentElement.scrollHeight'), 4000)
        page.set_viewport_size({'width': 1440, 'height': h})
        page.wait_for_timeout(400)
    page.screenshot(path=str(out), type='jpeg', quality=82)


def mostly_blank(path):
    """A screenshot that is almost a single color: WebGL sites often come out black in a headless browser, lazy-loading pages white.

    Criterion: pixels clearly different from the most common color (brightness gap > 24) are under 0.8%. Measured: a WebGL black screen
    is about 0.4%, the emptiest minimal design (one number and a row of hairlines) about 1.5%. Without Pillow installed, returns None — cannot tell.
    """
    try:
        from PIL import Image
    except ImportError:
        return None
    from collections import Counter
    px = Image.open(path).convert('L').resize((360, 225)).tobytes()
    mode = Counter(px).most_common(1)[0][0]
    return sum(1 for v in px if abs(v - mode) > 24) / len(px) < 0.008


def board(page, shots, out):
    cells = ''.join(
        f'<figure><img src="{p.resolve().as_uri()}"><figcaption>{html.escape(s)}</figcaption></figure>'
        for p, s in shots)
    page.set_viewport_size({'width': 1500, 'height': 600})
    tmp = out.parent / '.board.html'
    tmp.write_text(f'''<!doctype html><meta charset="utf-8"><style>
body{{margin:0;padding:20px;background:#ddd;font:13px/1.3 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}}
.g{{display:grid;grid-template-columns:repeat(2,720px);gap:16px;align-items:start}}
figure{{margin:0}} img{{width:720px;display:block;max-height:1100px;object-fit:cover;object-position:top}}
figcaption{{margin-top:4px;word-break:break-all;color:#333}}</style><div class="g">{cells}</div>''', encoding='utf-8')
    page.goto(tmp.resolve().as_uri(), wait_until='load', timeout=30000)   # local images can only be referenced from a file:// page
    page.screenshot(path=str(out), full_page=True, type='jpeg', quality=80)
    tmp.unlink()


def main(argv):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description='Screenshot reference works into a reference board')
    ap.add_argument('sources', nargs='+')
    ap.add_argument('--out', default='refs/board.jpg')
    ap.add_argument('--full', action='store_true', help='capture the full page (up to 4000px)')
    a = ap.parse_args(argv)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('Playwright required: pip install playwright && python3 -m playwright install chromium')
        print('Without it: use WebSearch image results, or ask the user to send screenshots, save them into refs/, and open them directly with your image-viewing ability.')
        return 2
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    shots, failed, unchecked = [], [], False
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as e:
            print('Chromium failed to launch:', str(e).splitlines()[0])
            print('Install it: python3 -m playwright install chromium')
            return 2
        page = browser.new_page()
        for i, src in enumerate(a.sources, 1):
            one = out.with_name(f'{out.stem}-{i}.jpg')
            if Path(src).exists() and Path(src).resolve() == one.resolve():
                one = out.with_name(f'{out.stem}-{i}-shot.jpg')
            try:
                shoot(page, src, one, a.full)
                blank = mostly_blank(one)
                unchecked = unchecked or blank is None
                if blank:
                    failed.append(src)
                    print('✗', src, ': shot is almost a solid color (WebGL/3D site or lazy loading) — as good as not seen')
                    continue
                shots.append((one, src))
                print('✓', one, '←', src)
            except Exception as e:
                failed.append(src)
                print('✗', src, ':', str(e).splitlines()[0])
        if shots:
            board(page, shots, out)
            print('Reference board →', out)
        elif out.exists():
            out.unlink()   # the previous run's old board would be mistaken for this run's
        browser.close()
    if unchecked:
        print('\nPillow not installed (pip install pillow): cannot auto-check whether shots are a solid color — open each one and look before using it.')
    if failed:
        print('\nSources that would not open (common causes: anti-bot, login required, region locks). Switch to a report page or an image URL of the same work, '
              'or ask the user for screenshots. Do not pretend to have seen it from memory.')
    return 0 if shots else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
