#!/usr/bin/env node
/**
 * gen_deck_thumbs.mjs — generate one thumbnail per page of a multi-file deck (for deck_index.html's "infinite gallery" overview).
 *
 * Background: deck_index.html has two overview modes —
 *   · Grid (default, 60%): renders the real sub-pages in iframes — sharp, WYSIWYG, no thumbnails needed.
 *   · Infinite gallery (40%): tiles all pages seamlessly with a slow drift; dozens to hundreds of tiles would
 *     stutter as iframes, so the gallery uses <img> thumbnails instead — the same image reused many times is
 *     decoded once by the browser, keeping it smooth.
 *   This script prepares that batch of thumbnails for the gallery. Grid mode doesn't need it.
 *
 * Usage (copy to the deck project root, install dependencies, then run):
 *   npm install playwright sharp     (sharp optional: without it the browser screenshots JPEGs directly at thumbnail size)
 *   node gen_deck_thumbs.mjs --slides slides --out thumbs [--width 1600] [--quality 86]
 *
 * Then add thumb to each MANIFEST item in index.html (same name as file, .jpg):
 *   { file: "slides/01-cover.html", thumb: "thumbs/01-cover.jpg", label: "Cover" }
 * deck_index.html only uses thumb in gallery mode; grid mode always uses file (iframe). Without thumb the gallery falls back to iframe.
 *
 * Tip: don't make the thumbnail resolution too low (default 1600px), or gallery cards blur when hovered to zoom.
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > -1 && process.argv[i + 1] ? process.argv[i + 1] : d; };
const slidesDir = arg('slides', 'slides');
const outDir = arg('out', 'thumbs');
const width = parseInt(arg('width', '1600'), 10);
const quality = parseInt(arg('quality', '86'), 10);
const W = parseInt(arg('canvas-w', '1920'), 10);
const H = parseInt(arg('canvas-h', '1080'), 10);

if (!fs.existsSync(slidesDir)) { console.error('slides directory not found: ' + slidesDir); process.exit(1); }
fs.mkdirSync(outDir, { recursive: true });
const files = fs.readdirSync(slidesDir).filter(f => f.endsWith('.html')).sort();
if (!files.length) { console.error('no .html files in the slides directory'); process.exit(1); }

const browser = await chromium.launch().catch(() => chromium.launch({ channel: 'chrome' })).catch(() => chromium.launch({ channel: 'msedge' }));  // when the Playwright browser isn't downloaded, borrow the user's installed Chrome / Edge
const sharp = await import('sharp').then(m => m.default).catch(() => null);
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: sharp ? 1 : width / W });
let ok = 0;
for (const f of files) {
  const base = f.replace(/\.html$/, '');
  const out = path.join(outDir, base + '.jpg');
  try {
    await page.goto('file://' + path.resolve(slidesDir, f), { waitUntil: 'load' });
    await page.waitForTimeout(2800);                 // wait for webfonts / images to paint
    if (sharp) {
      const buf = await page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: W, height: H } });
      await sharp(buf).resize(width).jpeg({ quality }).toFile(out);
    } else {
      await page.screenshot({ path: out, type: 'jpeg', quality, clip: { x: 0, y: 0, width: W, height: H } });
    }
    ok++; console.log('[ok] ' + out);
  } catch (e) { console.error('[FAIL] ' + f + ': ' + e.message); }
}
await browser.close();
console.log(`\n=== ${ok}/${files.length} thumbnails → ${outDir}/ ===`);
console.log('Add thumb to each MANIFEST item in index.html: "' + outDir + '/<same-name>.jpg" (gallery mode only)');
