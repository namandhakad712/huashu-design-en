#!/usr/bin/env node
/**
 * HTML animation → MP4 via deterministic frame-by-frame SEEK (Playwright + ffmpeg).
 *
 * This is the frame-by-frame alternative renderer to render-video.js (Playwright
 * recordVideo). The core technique borrows the "frozen clock + seek to a timestamp
 * and screenshot" approach from HeyGen HyperFrames (Apache 2.0), but without pulling
 * in any third-party packages — it only uses the playwright + ffmpeg already present
 * in this skill, so it stays runtime-neutral.
 *
 * Three stubborn blockers it solves versus render-video.js (see references/video-export.md § "seek rendering"):
 *   1. Frame rate is no longer locked to 25fps by the Chromium headless compositor — --fps gives any native frame rate
 *   2. No more post-hoc minterpolate interpolation from convert-formats.sh (ghosting
 *      + macOS QuickTime compatibility bug, see animation-pitfalls §14) — every frame is a real seek capture
 *   3. No screen recording → no black frames at the start → none of the --trim / --fontwait / __ready offset machinery needed
 *   Bonus: screenshots taken after seeking to a timestamp are deterministic — same
 *   input, same output (recordVideo captures in real time and is non-deterministic)
 *
 * Prerequisite: the animation must run on the Stage clock (the <Stage> from
 * assets/animations.jsx or the <NarrationStage> from narration_stage.jsx) — these
 * respond to window.__seekRender by freezing their self-running clock and expose
 * window.__seek(t). Pure CSS @keyframes / Lottie / hand-written non-Stage animations
 * don't respond to __seek; keep using render-video.js for those.
 *
 * Requires: global playwright (`npm install -g playwright`), ffmpeg on PATH.
 *
 * Usage:
 *   NODE_PATH=$(npm root -g) node render-video-seek.js <html-file> \
 *     [--duration=30] [--fps=60] [--width=1920] [--height=1080] \
 *     [--concurrency=4] [--settle=2] [--keep-chrome]
 *
 * Output: next to the HTML file, same basename with .mp4 suffix.
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

function arg(name, def) {
  const p = process.argv.find(a => a.startsWith('--' + name + '='));
  return p ? p.slice(name.length + 3) : def;
}
function hasFlag(name) {
  return process.argv.includes('--' + name);
}

const HTML_FILE = process.argv[2];
if (!HTML_FILE || HTML_FILE.startsWith('--')) {
  console.error('Usage: node render-video-seek.js <html-file>');
  console.error('Example: NODE_PATH=$(npm root -g) node render-video-seek.js my-animation.html --fps=60');
  process.exit(1);
}

const DURATION    = parseFloat(arg('duration', '30'));
const FPS         = parseFloat(arg('fps', '60'));      // any native frame rate; true 60fps by default
const WIDTH       = parseInt(arg('width', '1920'));
const HEIGHT      = parseInt(arg('height', '1080'));
const CONCURRENCY = Math.max(1, parseInt(arg('concurrency', '4')));  // number of parallel workers (one page each)
const SETTLE      = Math.max(1, parseInt(arg('settle', '2')));        // how many rAFs to wait after each seek before screenshotting
const READY_TIMEOUT = parseFloat(arg('readytimeout', '8'));
const KEEP_CHROME = hasFlag('keep-chrome');

const HTML_ABS = path.resolve(HTML_FILE);
const BASENAME = path.basename(HTML_FILE, path.extname(HTML_FILE));
const DIR      = path.dirname(HTML_ABS);
const TMP_DIR  = path.join(DIR, '.seek-tmp-' + Date.now() + '-' + process.pid);
const MP4_OUT  = path.join(DIR, BASENAME + '.mp4');

// Chrome-hiding rules exactly matching render-video.js (so both pipelines produce the same look)
const HIDE_CHROME_CSS = `
  .no-record,
  .progress, .progress-bar,
  .counter, .tCur,
  .phases, .phase-label, .phase,
  .replay, button.replay,
  .masthead, .kicker, .title,
  .footer,
  [data-role="chrome"], [data-record="hidden"] {
    display: none !important;
  }
`;

const TOTAL_FRAMES = Math.round(FPS * DURATION);

console.log(`▸ Seek-rendering: ${HTML_FILE}`);
console.log(`  size: ${WIDTH}x${HEIGHT} · ${FPS}fps · duration: ${DURATION}s · frames: ${TOTAL_FRAMES} · workers: ${CONCURRENCY}`);
console.log(`  output: ${MP4_OUT}`);

// Runs inside the page context: waits n rAFs (lets React/Babel commit + layout settle before the screenshot)
async function waitRaf(page, n) {
  await page.evaluate((count) => new Promise(resolve => {
    let i = 0;
    const step = () => { i++; (i >= count) ? resolve() : requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }), n);
}

// One worker: opens a page, navigates to the URL, waits for __seek to be ready, renders its assigned frames
async function renderFrames(context, url, frames) {
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });

  // In __seekRender mode, Stage / NarrationStage expose window.__seek and freeze the self-running clock
  await page.waitForFunction(
    () => window.__ready === true && typeof window.__seek === 'function',
    { timeout: READY_TIMEOUT * 1000 },
  );

  for (const f of frames) {
    const t = f / FPS;
    await page.evaluate((tt) => window.__seek(tt), t);
    await waitRaf(page, SETTLE);
    await page.screenshot({
      path: path.join(TMP_DIR, 'frame-' + String(f).padStart(6, '0') + '.png'),
      clip: { x: 0, y: 0, width: WIDTH, height: HEIGHT },
    });
  }
  await page.close();
}

(async () => {
  fs.mkdirSync(TMP_DIR, { recursive: true });

  const browser = await chromium.launch();
  const url = 'file://' + HTML_ABS;

  const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    deviceScaleFactor: 1,
  });

  // Key signal: __seekRender makes Stage / NarrationStage freeze the wall-clock rAF; frames
  // are instead advanced by the external __seek
  // __recording is reused as-is so Stage forces loop=false (existing convention)
  await context.addInitScript(() => {
    window.__recording = true;
    window.__seekRender = true;
  });

  if (!KEEP_CHROME) {
    // Same chrome hiding as render-video.js (CSS + fixed-bar heuristic)
    await context.addInitScript(css => {
      const HIDE_MARK = 'data-video-hidden';
      function injectStyle() {
        const style = document.createElement('style');
        style.setAttribute('data-inject', 'render-video-chrome-hide');
        style.textContent = css;
        (document.head || document.documentElement).appendChild(style);
      }
      function hideChromeBars() {
        const vh = window.innerHeight;
        document.querySelectorAll('div, nav, header, footer, section, aside')
          .forEach(el => {
            if (el.hasAttribute(HIDE_MARK)) return;
            if (el.dataset.recordKeep === 'true') return;
            const s = getComputedStyle(el);
            if (s.position !== 'fixed' && s.position !== 'sticky') return;
            const r = el.getBoundingClientRect();
            if (r.height > vh * 0.25) return;
            const atBottom = r.bottom >= vh - 30;
            const atTop = r.top <= 30 && r.height < 80;
            if (!atBottom && !atTop) return;
            const txt = el.textContent || '';
            const hasBtn = !!el.querySelector('button, [role="button"]');
            const hasCtrls = /[⏸▶⏮⏭↻↺↩↪]|\d+\.\d+\s*s/.test(txt);
            if (hasBtn || hasCtrls) {
              el.style.setProperty('display', 'none', 'important');
              el.setAttribute(HIDE_MARK, '1');
            }
          });
      }
      const start = () => {
        injectStyle();
        hideChromeBars();
        const obs = new MutationObserver(hideChromeBars);
        obs.observe(document.body, { childList: true, subtree: true });
        setTimeout(() => obs.disconnect(), 6000);
      };
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', start, { once: true });
      } else {
        start();
      }
    }, HIDE_CHROME_CSS);
  }

  // Round-robin the frames across CONCURRENCY workers (each page has its own window, so seeks don't interfere)
  const buckets = Array.from({ length: CONCURRENCY }, () => []);
  for (let f = 0; f < TOTAL_FRAMES; f++) buckets[f % CONCURRENCY].push(f);

  console.log(`▸ Capturing ${TOTAL_FRAMES} frames across ${CONCURRENCY} workers…`);
  try {
    await Promise.all(buckets.map(b => b.length ? renderFrames(context, url, b) : Promise.resolve()));
  } catch (e) {
    const msg = String(e && e.message || e);
    if (/__seek|__ready/.test(msg)) {
      console.error('');
      console.error('✗ The animation does not expose window.__seek (or it never became ready).');
      console.error('  Seek rendering only supports animations driven by the Stage clock (assets/animations.jsx <Stage>');
      console.error('  or narration_stage.jsx <NarrationStage>). For pure CSS @keyframes / Lottie /');
      console.error('  hand-written non-Stage animations, use render-video.js instead.');
      console.error('');
    }
    await browser.close();
    fs.rmSync(TMP_DIR, { recursive: true, force: true });
    console.error(msg.slice(0, 500));
    process.exit(1);
  }

  await browser.close();

  const pngCount = fs.readdirSync(TMP_DIR).filter(f => f.endsWith('.png')).length;
  if (pngCount === 0) {
    console.error('✗ No frames captured');
    process.exit(1);
  }
  console.log(`▸ Captured ${pngCount}/${TOTAL_FRAMES} frames. Encoding H.264…`);

  // PNG sequence → MP4. No trimming (there were no black frames to begin with); both
  // input and output frame rates are set to FPS.
  const ffmpeg = spawnSync('ffmpeg', [
    '-y',
    '-framerate', String(FPS),
    '-i', path.join(TMP_DIR, 'frame-%06d.png'),
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-crf', '18',
    '-preset', 'medium',
    '-r', String(FPS),
    '-movflags', '+faststart',
    MP4_OUT,
  ], { stdio: ['ignore', 'ignore', 'pipe'] });

  if (ffmpeg.status !== 0) {
    console.error('✗ ffmpeg failed:\n' + ffmpeg.stderr.toString().slice(-2000));
    process.exit(1);
  }

  fs.rmSync(TMP_DIR, { recursive: true, force: true });

  const mp4Size = (fs.statSync(MP4_OUT).size / 1024 / 1024).toFixed(1);
  console.log(`✓ Done: ${MP4_OUT} (${mp4Size} MB · ${FPS}fps native)`);
})();
