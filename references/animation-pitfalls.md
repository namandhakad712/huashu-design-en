# Animation Pitfalls: HTML Animation Bugs and Rules

Bugs most commonly encountered when making animations and how to avoid them. Every rule comes from real failure cases.

Read this before writing animation, can save one round of iteration.

## 1. Stacked Layout — `position: relative` is Default Obligation

**Pitfall**: A sentence-wrap element wraps 3 bracket-layers (`position: absolute`). Didn't set sentence-wrap to `position: relative`, so absolute brackets use `.canvas` as coordinate system, floating 200px below screen.

**Rules**:
- Any container containing `position: absolute` children **must** explicitly have `position: relative`
- Even if visually no "offset" needed, write `position: relative` as coordinate system anchor
- If you're writing `.parent { ... }` and its children have `.child { position: absolute }`, instinctively add relative to parent

**Quick check**: Every time `position: absolute` appears, count up ancestors, ensure the nearest positioned ancestor is the coordinate system you *want*.

## 2. Character Trap — Don't Rely on Rare Unicode

**Pitfall**: Want to use `␣` (U+2423 OPEN BOX) to visualize "space token". Noto Serif SC / Cormorant Garamond don't have this glyph, renders as blank/tofu, audience can't see at all.

**Rules**:
- **Every character appearing in animation must exist in your chosen font**
- Common rare character blacklist: `␣ ␀ ␐ ␋ ␨ ↩ ⏎ ⌘ ⌥ ⌃ ⇧ ␦ ␖ ␛`
- To express "space / return / tab" meta-characters, use **CSS-constructed semantic boxes**:
  ```html
  <span class="space-key">Space</span>
  ```
  ```css
  .space-key {
    display: inline-flex;
    padding: 4px 14px;
    border: 1.5px solid var(--accent);
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.3em;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  ```
- Emoji also verify: certain emoji in fonts other than Noto Emoji fallback to gray square, better use `emoji` font-family or SVG

## 3. Data-Driven Grid/Flex Template

**Pitfall**: Code has `const N = 6` tokens, but CSS hardcoded `grid-template-columns: 80px repeat(5, 1fr)`. Result: 6th token has no column, entire matrix misaligned.

**Rules**:
- When count comes from JS array (`TOKENS.length`), CSS template should also be data-driven
- Option A: Inject CSS variables from JS
  ```js
  el.style.setProperty('--cols', N);
  ```
  ```css
  .grid { grid-template-columns: 80px repeat(var(--cols), 1fr); }
  ```
- Option B: Use `grid-auto-flow: column` for browser auto-expansion
- **Disable "fixed number + JS constant" combination**, when N changes CSS won't sync

## 4. Transition Gap — Scene Switches Must Be Continuous

**Pitfall**: Between zoom1 (13-19s) and zoom2 (19.2-23s), main sentence already hidden, zoom1 fade out (0.6s) + zoom2 fade in (0.6s) + stagger delay (0.2s+) = about 1 second pure blank screen. Audience thinks animation froze.

**Rules**:
- When continuously switching scenes, fade out and fade in should **cross-over**, not wait for previous to fully disappear before starting next
  ```js
  // Bad:
  if (t >= 19) hideZoom('zoom1');      // 19.0s out
  if (t >= 19.4) showZoom('zoom2');    // 19.4s in → 0.4s blank in between

  // Good:
  if (t >= 18.6) hideZoom('zoom1');    // Start fade out 0.4s early
  if (t >= 18.6) showZoom('zoom2');    // Same time fade in (cross-fade)
  ```
- Or use an "anchor element" (like main sentence) as visual connection between scenes, it briefly reappears during zoom switch
- Calculate CSS transition duration clearly, avoid triggering next before transition ends

## 5. Pure Render Principle — Animation State Should Be Seekable

**Pitfall**: Use `setTimeout` + `fireOnce(key, fn)` chain to trigger animation states. Normal playback fine, but when frame-by-frame recording/seeking to any time point, previous setTimeout already executed can't "go back in time".

**Rules**:
- `render(t)` function ideally is **pure function**: given t outputs unique DOM state
- If must use side effects (like class switching), use `fired` set with explicit reset:
  ```js
  const fired = new Set();
  function fireOnce(key, fn) { if (!fired.has(key)) { fired.add(key); fn(); } }
  function reset() { fired.clear(); /* clear all .show classes */ }
  ```
- Expose `window.__seek(t)` for Playwright/debugging:
  ```js
  window.__seek = (t) => { reset(); render(t); };
  ```
- Animation-related setTimeout shouldn't span >1 second, otherwise seek jumping back gets chaotic

## 6. Pre-Font-Load Measurement = Wrong Measurement

**Pitfall**: Call `charRect(idx)` to measure bracket position immediately on DOMContentLoaded, fonts not loaded yet, each character width is fallback font width, all positions wrong. When fonts load (~500ms later), bracket `left: Xpx` still old value, permanently offset.

**Rules**:
- Any layout code depending on DOM measurement (`getBoundingClientRect`, `offsetWidth`) **must** be wrapped in `document.fonts.ready.then()`:
  ```js
  document.fonts.ready.then(() => {
    requestAnimationFrame(() => {
      buildBrackets(...);  // Fonts ready now, measurement accurate
      tick();              // Animation starts
    });
  });
  ```
- Additional `requestAnimationFrame` gives browser one frame to commit layout
- If using Google Fonts CDN, `<link rel="preconnect">` speeds first load

## 7. Recording Prep — Reserve Hooks for Video Export

**Pitfall**: Playwright `recordVideo` defaults to 25fps, starts recording from context creation. Page load, font load first 2 seconds all recorded. Delivered video first 2 seconds blank/flash white.

**Rules**:
- Provide `render-video.js` tool handles: warmup navigate → reload restart animation → wait duration → ffmpeg trim head + convert H.264 MP4
- Animation **frame 0** must be complete initial state with layout ready (not blank or loading)
- Want 60fps? Use ffmpeg `minterpolate` post-processing, don't rely on browser source frame rate
- Want GIF? Two-stage palette (`palettegen` + `paletteuse`), can compress 30s 1080p to 3MB

See `video-export.md` for complete script usage.

## 8. Batch Export — tmp Directory Must Have PID to Prevent Concurrent Conflicts

**Pitfall**: Using `render-video.js` 3 processes in parallel record 3 HTMLs. Because TMP_DIR only uses `Date.now()` naming, 3 processes starting same millisecond share same tmp directory. First completed process cleans tmp, other two read directory get `ENOENT`, all crash.

**Rules**:
- Any temporary directory that might be shared by multiple processes must be named with **PID or random suffix**:
  ```js
  const TMP_DIR = path.join(DIR, '.video-tmp-' + Date.now() + '-' + process.pid);
  ```
- If truly want parallel multiple files, use shell's `&` + `wait` not fork within one node script
- When batch recording multiple HTMLs, conservative approach: **serial** (2 or less can parallel, 3+ should queue)

## 9. Progress Bar/Replay Button in Recording — Chrome Elements Pollute Video

**Pitfall**: Animation HTML added `.progress` progress bar, `.replay` replay button, `.counter` timestamp for human debug convenience. When recording MP4 for delivery, these elements appear at video bottom, like capturing developer tools.

**Rules**:
- HTML "chrome elements" for human use (progress bar / replay button / footer / masthead / counter / phase labels) separate from video content body
- **Convention**: class name `.no-record`: any element with this class, recording script auto-hides
- Script side (`render-video.js`) injects CSS to hide common chrome class names by default:
  ```
  .progress .counter .phases .replay .masthead .footer .no-record [data-role="chrome"]
  ```
- Use Playwright's `addInitScript` to inject (applies before every navigate, stable through reload)
- Want to see original HTML (with chrome) add `--keep-chrome` flag

## 10. Recording First Seconds Animation Repeat — Warmup Frame Leak

**Pitfall**: `render-video.js` old flow `goto → wait fonts 1.5s → reload → wait duration`. Recording starts from context creation, warmup phase animation already played some, after reload restarts from 0. Result video first seconds are "animation mid + switch + animation from 0", strong repeat feel.

**Rules**:
- **Warmup and Record must use independent contexts**:
  - Warmup context (no `recordVideo` option): only responsible for load url, wait fonts, then close
  - Record context (has `recordVideo`): fresh state start, animation starts from t=0
- ffmpeg `-ss trim` can only trim Playwright's slight startup latency (~0.3s), **cannot** cover warmup frames; source must be clean
- Recording context close = webm file written to disk, this is Playwright's constraint
- Related code pattern:
  ```js
  // Phase 1: warmup (throwaway)
  const warmupCtx = await browser.newContext({ viewport });
  const warmupPage = await warmupCtx.newPage();
  await warmupPage.goto(url, { waitUntil: 'networkidle' });
  await warmupPage.waitForTimeout(1200);
  await warmupCtx.close();

  // Phase 2: record (fresh)
  const recordCtx = await browser.newContext({ viewport, recordVideo });
  const page = await recordCtx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(DURATION * 1000);
  await page.close();
  await recordCtx.close();
  ```

## 11. Don't Draw "Pseudo Chrome" in Frame — Decorative Player UI Collides with Real Chrome

**Pitfall**: Animation uses `Stage` component, already has scrubber + timestamp + pause button (belongs to `.no-record` chrome, auto-hidden during export). I also drew a "magazine page number feel decorative progress bar" at bottom "`00:60 ──── CLAUDE-DESIGN / ANATOMY`", self-feeling good. **Result**: User sees two progress bars — one Stage controller, one my decoration. Visually completely colliding, judged as bug. "What's that progress bar in the video?"

**Rules**:
- Stage already provides: scrubber + timestamp + pause/replay buttons. **Don't draw** progress indicator, current timestamp, copyright signature, chapter counter in frame — either collide with chrome or are filler slop (violate "earn its place" principle)
- "Page number feel", "magazine feel", "bottom signature strip" these **decorative demands** are high-frequency filler AI automatically adds. Every appearance should be alert — does it really convey irreplaceable information? Or just fill blank?
- If you believe certain bottom strip must exist (e.g., animation theme is about player UI), it must be **narratively necessary** AND **visually significantly distinguished** from Stage scrubber (different position, form, tone)

**Element ownership test** (every element drawn in canvas must answer):

| What it belongs to | Handle |
|------------|------|
| Narrative content of one scene | OK, keep |
| Global chrome (control/debug) | Add `.no-record` class, hidden during export |
| **Belongs to neither any scene nor chrome** | **Delete**. This is orphaned, definitely filler slop |

**Self-check (3 seconds before delivery)**: Take a static screenshot, ask yourself:
- Is there "things looking like video player UI" (horizontal progress bar, timestamp, control button look)?
- If yes, does removing it damage narrative? If no, delete.
- Does same type of information (progress/time/signature) appear twice? Merge to chrome in one place.

**Counter-examples**: Bottom `00:42 ──── PROJECT NAME`, bottom right corner "CH 03 / 06" chapter counter, edge version number "v0.3.1" — all pseudo chrome filler.

## 12. Recording Pre-blank + Recording Start Offset — `__ready` × tick × lastTick Triple Trap

**Pitfall (A · pre-blank)**: Export 60-second animation MP4, first 2-3 seconds blank page. `ffmpeg --trim=0.3` can't cut.

**Pitfall (B · start offset, 2026-04-20 real incident)**: Export 24-second video, user feel "video starts playing at 19 seconds". Actually animation recorded from t=5 to t=24 then loop back to t=0, recorded 5 seconds to end — so video last 5 seconds are animation's real beginning.

**Root cause** (both pitfalls share one root cause):

Playwright `recordVideo` starts writing WebM from moment `newContext()` is created, at this point Babel/React/font loading takes L seconds (2-6s). Recording script waits `window.__ready = true` as "animation starts from here" anchor — it and animation `time = 0` must strictly pair. Two common wrong ways:

| Wrong way | Symptom |
|------|------|
| `__ready` set in `useEffect` or sync setup phase (before tick first frame) | Recording script thinks animation started, but WebM still recording blank page → **pre-blank** |
| `lastTick = performance.now()` initialized at **script top level** | L seconds of font loading counted into first frame `dt`, `time` instantly jumps to L → entire recording offset by L seconds → **start offset** |

**✅ Correct complete starter tick template** (hand-written animations must use this skeleton):

```js
// ━━━━━━ state ━━━━━━
let time = 0;
let playing = false;   // ❗ Default don't play, wait for fonts ready then start
let lastTick = null;   // ❗ sentinel—first frame of tick forces dt to 0 (don't use performance.now())
const fired = new Set();

// ━━━━━━ tick ━━━━━━
function tick(now) {
  if (lastTick === null) {
    lastTick = now;
    window.__ready = true;   // ✅ Pair: "recording start" and "animation t=0" same frame
    render(0);               // Re-render once more to ensure DOM ready (fonts already ready)
    requestAnimationFrame(tick);
    return;
  }
  const dt = (now - lastTick) / 1000;   // After first frame dt starts advancing
  lastTick = now;

  if (playing) {
    let t = time + dt;
    if (t >= DURATION) {
      t = window.__recording ? DURATION - 0.001 : 0;  // When recording don't loop, leave 0.001s to keep last frame
      if (!window.__recording) fired.clear();
    }
    time = t;
    render(time);
  }
  requestAnimationFrame(tick);
}

// ━━━━━━ boot ━━━━━━
// Don't immediately rAF at top level—wait for fonts loaded before starting
document.fonts.ready.then(() => {
  render(0);                 // First render initial frame (fonts ready)
  playing = true;
  requestAnimationFrame(tick);  // First tick will pair __ready + t=0
});

// ━━━━━━ seek interface (for render-video defensive correction) ━━━━━━
window.__seek = (t) => { fired.clear(); time = t; lastTick = null; render(t); };
```

**Why this template is correct**:

| Link | Why must do this |
|------|-------------|
| `lastTick = null` + first frame `return` | Avoid "script load to tick first execution" L seconds counted into animation time |
| `playing = false` default | During font loading, even if `tick` runs it doesn't advance time, avoids render offset |
| `__ready` set in tick first frame | Recording script starts timing at this moment, corresponding frame is animation's true t=0 |
| Start tick only inside `document.fonts.ready.then(...)` | Avoid font fallback width measurement, avoid first frame font jump |
| `window.__seek` exists | Lets `render-video.js` actively correct — second defense line |

**Recording script corresponding defense**:
1. `addInitScript` injects `window.__recording = true` (before page goto)
2. `waitForFunction(() => window.__ready === true)`, record this moment offset as ffmpeg trim
3. **Additional**: after `__ready`, actively `page.evaluate(() => window.__seek && window.__seek(0))`, force HTML possible time deviation to zero — second defense line for HTML not strictly following starter template

**Verification method**: After exporting MP4
```bash
ffmpeg -i video.mp4 -ss 0 -vframes 1 frame-0.png
ffmpeg -i video.mp4 -ss $DURATION-0.1 -vframes 1 frame-end.png
```
First frame must be animation t=0 initial state (not mid, not black), last frame must be animation final state (not second loop moment).

**Reference implementation**: `assets/animations.jsx` Stage component, `scripts/render-video.js` both implement this protocol. Hand-written HTML must use starter tick template — every line defends against specific bugs.

## 13. Recording Forbids Loop — `window.__recording` Signal

**Pitfall**: Animation Stage defaults `loop=true` (convenient for browser viewing). `render-video.js` records duration seconds then waits 300ms buffer, this 300ms lets Stage enter next loop. ffmpeg `-t DURATION` captures, last 0.5-1s falls into next loop — video ending suddenly returns to first frame (Scene 1), audience thinks video has bug.

**Root cause**: No handshake protocol between recording script and HTML. HTML doesn't know it's being recorded, still loops as if browser interaction scenario.

**Rules**:

1. **Recording script**: inject `window.__recording = true` in `addInitScript` (before page goto):
   ```js
   await recordCtx.addInitScript(() => { window.__recording = true; });
   ```

2. **Stage component**: recognize this signal, force loop=false:
   ```js
   const effectiveLoop = (typeof window !== 'undefined' && window.__recording) ? false : loop;
   // ...
   if (next >= duration) return effectiveLoop ? 0 : duration - 0.001;
   //                                                       ↑ Leave 0.001 prevent Sprite end=duration being closed
   ```

3. **Ending Sprite's fadeOut**: In recording scenario should set `fadeOut={0}`, otherwise video end fades to transparent/dark — user expects clear last frame, not fade out. When hand-writing HTML, recommend all ending Sprites use `fadeOut={0}`.

**Reference implementation**: `assets/animations.jsx` Stage / `scripts/render-video.js` both have built-in handshake. Hand-written Stage must implement `__recording` detection — otherwise recording will definitely hit this pitfall.

**Verify**: After exporting MP4, `ffmpeg -ss 19.8 -i video.mp4 -frames:v 1 end.png`, check if last 0.2 seconds is still expected last frame, no sudden switch to another scene.

## 14. 60fps Video Default Use Frame Copy — minterpolate Compatibility Poor

**Pitfall**: `convert-formats.sh` using `minterpolate=fps=60:mi_mode=mci...` generated 60fps MP4 can't open in some macOS QuickTime/Safari versions (black or directly refuse). VLC / Chrome can open.

**Root cause**: minterpolate outputs H.264 elementary stream containing some SEI/SPS fields certain players have trouble parsing.

**Rules**:
- Default 60fps use simple `fps=60` filter (frame copy), wide compatibility (QuickTime/Safari/Chrome/VLC all open)
- High-quality interpolation use `--minterpolate` flag explicitly enable — but **must test** target player locally before delivery
- 60fps tag value is **platform algorithm recognition** (Bilibili / YouTube 60fps tag prioritized streaming), actual perceived smoothness for CSS animation minimal improvement
- Add `-profile:v high -level 4.0` to improve H.264 general compatibility

**`convert-formats.sh` already defaults to compatible mode**. If need interpolation high quality, add `--minterpolate` flag:
```bash
bash convert-formats.sh input.mp4 --minterpolate
```

## 15. `file://` + External `.jsx` CORS Trap — Single File Delivery Must Inline Engine

**Pitfall**: Animation HTML uses `<script type="text/babel" src="animations.jsx"></script>` to externally load engine. Open locally by double-click (`file://` protocol) → Babel Standalone uses XHR to fetch `.jsx` → Chrome reports `Cross origin requests are only supported for protocol schemes: http, https, chrome, chrome-extension...` → entire page black screen, doesn't report `pageerror` only console error, easily misdiagnosed as "animation didn't trigger".

Starting HTTP server may not save — when machine has global proxy, `localhost` also goes through proxy, returns 502 / connection failed.

**Rules**:
- **Single file delivery (double-click to open HTML)** → `animations.jsx` must be **inlined** into `<script type="text/babel">...</script>` tag, don't use `src="animations.jsx"`
- **Multi-file project (HTTP server for demo)** → can external load, but delivery must explicitly state `python3 -m http.server 8000` command
- Judgment: deliver "HTML file" or "project directory with server"? Former use inline
- Stage component / animations.jsx often 200+ lines — paste into HTML `<script>` block fully acceptable, don't fear size

**Minimum verification**: Double-click your generated HTML, **don't** open through any server. If Stage shows animation first frame normally, then passed.

## 16. Cross-Scene Invert Context — Don't Hardcode Colors for In-Frame Elements

**Pitfall**: When making multi-scene animation, `ChapterLabel` / `SceneNumber` / `Watermark` etc **elements appearing across scenes** hardcoded `color: '#1A1A1A'` (dark text). First 4 scenes light background OK, at 5th dark background scene "05" and watermark disappear directly — no error, no trigger any check, key information invisible.

**Rules**:
- **In-frame elements reused across multiple scenes** (chapter labels / scene numbers / timestamps / watermarks / copyright bars) **forbidden to hardcode color values**
- Change to one of three ways:
  1. **`currentColor` inheritance**: element only writes `color: currentColor`, parent scene container sets `color: computed value`
  2. **invert prop**: component accepts `<ChapterLabel invert />` manual switch light/dark
  3. **Auto-compute based on background**: `color: contrast-color(var(--scene-bg))` (CSS 4 new API, or JS judgment)
- Deliver use Playwright to screenshot **representative frame of each scene**, human eye check "cross-scene elements" all visible

This pitfall's concealment — **no bug alerts**. Only human eye or OCR can discover.

---

## Quick Self-Check List (5 Seconds Before Starting)

- [ ] Every `position: absolute` parent has `position: relative`?
- [ ] Special characters in animation (`␣` `⌘` `emoji`) all exist in font?
- [ ] Grid/Flex template count matches JS data length?
- [ ] Scene transitions have cross-fade, no >0.3s pure blank?
- [ ] DOM measurement code wrapped in `document.fonts.ready.then()`?
- [ ] `render(t)` is pure, or has explicit reset mechanism?
- [ ] Frame 0 is complete initial state, not blank?
- [ ] No "pseudo chrome" decoration in frame (progress bar/timestamp/bottom signature collides with Stage scrubber)?
- [ ] Animation tick first frame syncs `window.__ready = true`? (Use animations.jsx built-in; add yourself for hand-written HTML)
- [ ] Stage detects `window.__recording` forces loop=false? (Must add for hand-written HTML)
- [ ] Ending Sprite's `fadeOut` set to 0 (video ends at clear frame)?
- [ ] 60fps MP4 default uses frame copy mode (compatibility), high-quality interpolation only add `--minterpolate`?
- [ ] After export, sample frame 0 + end frame verify is animation initial/final state?
- [ ] Specific brand involved (Stripe/Anthropic/Lovart/...): finished "Brand Asset Protocol" (SKILL.md §1.a five steps)? Have `brand-spec.md` written?
- [ ] Single file delivered HTML: `animations.jsx` is inlined, not `src="..."`? (file:// under external .jsx causes CORS black screen)
- [ ] Elements appearing across scenes (chapter labels/watermark/scene numbers) not hardcoded color? Visible under each scene background?