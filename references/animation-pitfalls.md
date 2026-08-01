# Animation Pitfalls: Bugs and Rules from HTML Animation

The most common bugs hit when doing animation, and how to avoid them. Every rule comes from a real failure case.

Read this before writing any animation, and you'll save yourself a round of iteration.

## 1. Stacked Layouts — `position: relative` Is the Default Obligation

**The bug**: A sentence-wrap element wrapped 3 bracket-layers (`position: absolute`). No `position: relative` was set on sentence-wrap, so the absolute brackets used `.canvas` as their coordinate system and floated 200px off the bottom of the screen.

**Rule**:
- Any container that holds `position: absolute` children **must** explicitly set `position: relative`
- Even if no "offset" is needed visually, write `position: relative` as the coordinate-system anchor
- If you're writing `.parent { ... }` and its children contain `.child { position: absolute }`, add relative to the parent out of reflex

**Quick check**: For every `position: absolute`, walk up the ancestors and make sure the nearest positioned ancestor is the coordinate system you *want*.

## 2. Character Traps — Don't Rely on Rare Unicode

**The bug**: Wanted to use `␣` (U+2423 OPEN BOX) to visualize "space tokens". Neither Noto Serif SC nor Cormorant Garamond has this glyph, so it rendered as blank/tofu and the audience couldn't see it at all.

**Rule**:
- **Every character that appears in the animation must exist in the fonts you've chosen**
- Blacklist of common rare characters: `␣ ␀ ␐ ␋ ␨ ↩ ⏎ ⌘ ⌥ ⌃ ⇧ ␦ ␖ ␛`
- For metacharacters like "space / enter / tab", use a **semantic box built with CSS**:
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
- Verify emoji too: some emoji fall back to a gray box in fonts other than Noto Emoji. Prefer the `emoji` font-family or SVG

## 3. Data-Driven Grid/Flex Templates

**The bug**: The code had `const N = 6` tokens, but the CSS hard-coded `grid-template-columns: 80px repeat(5, 1fr)`. As a result the 6th token had no column and the whole matrix was misaligned.

**Rule**:
- When the count comes from a JS array (`TOKENS.length`), the CSS template should be data-driven too
- Option A: inject with CSS variables from JS
  ```js
  el.style.setProperty('--cols', N);
  ```
  ```css
  .grid { grid-template-columns: 80px repeat(var(--cols), 1fr); }
  ```
- Option B: use `grid-auto-flow: column` and let the browser expand automatically
- **Forbid the "fixed number + JS constant" combination** — if N changes, the CSS won't sync

## 4. Transition Gaps — Scene Changes Must Be Continuous

**The bug**: Between zoom1 (13-19s) → zoom2 (19.2-23s), the main sentence was already hidden, and zoom1 fade out (0.6s) + zoom2 fade in (0.6s) + stagger delay (0.2s+) added up to roughly 1 second of pure blank screen. The audience thought the animation was stuck.

**Rule**:
- When switching scenes continuously, fade out and fade in should **overlap**, not have one fully disappear before the next starts
  ```js
  // Bad:
  if (t >= 19) hideZoom('zoom1');      // 19.0s out
  if (t >= 19.4) showZoom('zoom2');    // 19.4s in → 0.4s of blank in between

  // Good:
  if (t >= 18.6) hideZoom('zoom1');    // start fade out 0.4s early
  if (t >= 18.6) showZoom('zoom2');    // fade in at the same time (cross-fade)
  ```
- Or use an "anchor element" (like the main sentence) as the visual connection between scenes, briefly re-showing it during the zoom switch
- Calculate the duration of your CSS transitions carefully so the next one isn't triggered before the transition finishes

## 5. Pure Render Principle — Animation State Should Be Seekable

**The bug**: Used `setTimeout` + `fireOnce(key, fn)` to chain-trigger animation states. Playing normally worked fine, but when doing frame-by-frame recording / seeking to an arbitrary time, previously fired setTimeout callbacks had already executed and couldn't "go back in time".

**Rule**:
- The `render(t)` function should ideally be a **pure function**: given t, it outputs a single unique DOM state
- If you must use side effects (like class toggling), use a `fired` set with explicit reset:
  ```js
  const fired = new Set();
  function fireOnce(key, fn) { if (!fired.has(key)) { fired.add(key); fn(); } }
  function reset() { fired.clear(); /* clear all .show classes */ }
  ```
- Expose `window.__seek(t)` for Playwright / debugging:
  ```js
  window.__seek = (t) => { reset(); render(t); };
  ```
- Animation-related setTimeout should never span more than 1s, otherwise seeking backward gets scrambled

## 6. Measuring Before Fonts Load = Wrong Measurements

**The bug**: Called `charRect(idx)` to measure bracket positions right at DOMContentLoaded, before fonts loaded, so every character width was the fallback font's width and all positions were wrong. When fonts finally loaded (~500ms later), the brackets' `left: Xpx` still held the old values, permanently offset.

**Rule**:
- Any layout code that depends on DOM measurement (`getBoundingClientRect`, `offsetWidth`) **must** be wrapped in `document.fonts.ready.then()`
  ```js
  document.fonts.ready.then(() => {
    requestAnimationFrame(() => {
      buildBrackets(...);  // fonts are ready now, measurements are accurate
      tick();              // start the animation
    });
  });
  ```
- The extra `requestAnimationFrame` gives the browser one frame to commit the layout
- If using Google Fonts CDN, `<link rel="preconnect">` speeds up first load

## 7. Recording Prep — Reserve Handles for Video Export

**The bug**: Playwright's `recordVideo` defaults to 25fps and starts recording from context creation. The first 2 seconds of page load and font loading all got recorded. On delivery, the video had 2 blank/white-flashing seconds at the front.

**Rule**:
- Provide a `render-video.js` tool to handle: warmup navigate → reload to restart the animation → wait for the duration → ffmpeg trim the head + transcode to H.264 MP4
- **Frame 0** of the animation should be a complete initial state with the final layout in place (not blank or loading)
- Want 60fps? Use ffmpeg `minterpolate` post-processing; don't rely on the browser's source framerate
- Want a GIF? Two-stage palette (`palettegen` + `paletteuse`) can compress a 30s 1080p animation to 3MB

See `video-export.md` for the full invocation.

## 8. Batch Export — tmp Directories Must Include PID to Avoid Concurrency Conflicts

**The bug**: Used `render-video.js` with 3 processes to record 3 HTML files in parallel. Because TMP_DIR was named only with `Date.now()`, all 3 processes starting in the same millisecond shared the same tmp directory. The first process to finish cleaned up tmp, and the other two hit `ENOENT` reading the directory and all crashed.

**Rule**:
- Any temp directory that multiple processes might share must be named with a **PID or random suffix**:
  ```js
  const TMP_DIR = path.join(DIR, '.video-tmp-' + Date.now() + '-' + process.pid);
  ```
- If you really want to process multiple files in parallel, use the shell's `&` + `wait` rather than forking inside a single node script
- When batch-recording multiple HTML files, the conservative approach: run **serially** (parallel is fine for 2 or fewer, but for 3+ just queue up)

## 9. Progress Bars / Replay Buttons in the Recording — Chrome Elements Pollute the Video

**The bug**: The animation HTML added a `.progress` bar, a `.replay` button, and a `.counter` timestamp for convenient human debugging. When recorded to MP4 for delivery, these elements showed up at the bottom of the video, like the developer tools had been screen-captured.

**Rule**:
- In the HTML, keep the human-facing "chrome elements" (progress bar / replay button / footer / masthead / counter / phase labels) managed separately from the actual video content
- **Convention class name** `.no-record`: any element with this class is automatically hidden by the recording script
- On the script side (`render-video.js`), inject CSS by default to hide common chrome class names:
  ```
  .progress .counter .phases .replay .masthead .footer .no-record [data-role="chrome"]
  ```
- Inject via Playwright's `addInitScript` (it takes effect before every navigate, so reload is stable too)
- Add a `--keep-chrome` flag when you want to view the raw HTML (with chrome)

## 10. Animation Repeats in the First Few Seconds of the Recording — Warmup Frame Leak

**The bug**: The old `render-video.js` flow was `goto → wait fonts 1.5s → reload → wait duration`. Recording started at context creation, so the animation had already played some of its timeline during warmup, then restarted from 0 after reload. The result: the first few seconds of the video were "mid-animation + a cutover + animation starting from 0", a strong sense of repetition.

**Rule**:
- **Warmup and Record must use separate contexts**:
  - Warmup context (no `recordVideo` option): only loads the url, waits for fonts, then closes
  - Record context (with `recordVideo`): starts from a fresh state, animation recorded from t=0
- ffmpeg `-ss trim` can only cut Playwright's small startup latency (~0.3s); it **cannot** mask warmup frames — the source must be clean
- Closing the recording context = webm file written to disk; this is a Playwright constraint
- Relevant code pattern:
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

## 11. Don't Draw "Fake Chrome" in the Frame — Decorative Player UI Collides with Real Chrome

**The bug**: The animation used the `Stage` component, which already ships with a scrubber + timecode + pause button (all `.no-record` chrome, auto-hidden on export). I then drew a "`00:60 ──── CLAUDE-DESIGN / ANATOMY`" magazine-page-number-style decorative progress bar at the bottom of the frame, feeling quite pleased with myself. **Result**: the user saw two progress bars — one is the Stage controller, one is the decoration I drew. Visually they collided completely and it was flagged as a bug. "Why is there a progress bar inside the video?"

**Rule**:

- Stage already provides: scrubber + timecode + pause/replay buttons. **Do not draw** progress indicators, current timecodes, copyright credit bars, or chapter counters inside the frame — they either collide with the chrome or they're filler slop (violating the "earn its place" principle).
- These "page-number feel", "magazine feel", "bottom credit bar" **decorative impulses** are high-frequency fillers that AI adds automatically. Be wary of every single one — does it genuinely convey irreplaceable information, or is it just filling whitespace?
- If you firmly believe some bottom bar must exist (e.g., the animation's theme is literally about player UI), then it must be **narratively necessary** and **visually distinct from the Stage scrubber** (different position, different form, different palette).

**Element ownership test** (every element drawn into the canvas must be able to answer):

| What does it belong to | Handling |
|------------|------|
| Narrative content of some scene | OK, keep it |
| Global chrome (for control/debugging) | Add `.no-record` class, hidden on export |
| **Belongs to no scene, and isn't chrome** | **Delete it**. This is an ownerless thing, guaranteed filler slop |

**Self-check (3 seconds before delivery)**: capture a static frame and ask yourself —

- Is there anything that "looks like video player UI" in the frame (a horizontal progress bar, timecode, control-button shapes)?
- If so, does deleting it damage the narrative? If not, delete it.
- Does the same class of info (progress/time/credit) appear twice? Consolidate it into the chrome in one place.

**Counter-examples**: drawing `00:42 ──── PROJECT NAME` at the bottom, a "CH 03 / 06" chapter counter in the bottom-right, or a version number "v0.3.1" at the edge of the frame — all of these are fake chrome filler.

## 12. Pre-Recording Blank + Recording Start Offset — the `__ready` × tick × lastTick Triple Trap

**The bug (A · leading blank)**: A 60-second animation exported to MP4 had the first 2-3 seconds as a blank page. `ffmpeg --trim=0.3` couldn't cut it off.

**The bug (B · start offset, real incident 2026-04-20)**: Exported a 24-second video, and the user perceived "the first frame of the video only plays at 19 seconds". In reality the animation was recorded from t=5, recorded to t=24 then looped back to t=0, and recorded 5 more seconds to the end — so the last 5 seconds of the video were the animation's actual beginning.

**Root cause** (both bugs share one root cause):

Playwright `recordVideo` starts writing the WebM the moment `newContext()` runs, at which point Babel/React/font loading have consumed L seconds (2-6s). The recording script waits for `window.__ready = true` as the "animation starts here" anchor — it must strictly pair with the animation's `time = 0`. There are two common failure modes:

| Failure mode | Symptom |
|------|------|
| `__ready` is set in `useEffect` or during synchronous setup (before tick's first frame) | The recording script thinks the animation started, but the WebM is still recording a blank page → **leading blank** |
| tick's `lastTick = performance.now()` is initialized at **script top level** | The L seconds of font loading get counted into the first frame's `dt`, so `time` jumps instantly to L → the whole recording lags by L seconds → **start offset** |

**✅ The correct complete starter tick template** (hand-written animations must use this skeleton):

```js
// ━━━━━━ state ━━━━━━
let time = 0;
let playing = false;   // ❗ default not playing, start only when fonts are ready
let lastTick = null;   // ❗ sentinel — forces dt to 0 on tick's first frame (don't use performance.now())
const fired = new Set();

// ━━━━━━ tick ━━━━━━
function tick(now) {
  if (lastTick === null) {
    lastTick = now;
    window.__ready = true;   // ✅ pair: "recording start" and "animation t=0" on the same frame
    render(0);               // re-render once to make sure the DOM is ready (fonts are ready now)
    requestAnimationFrame(tick);
    return;
  }
  const dt = (now - lastTick) / 1000;   // dt only starts advancing after the first frame
  lastTick = now;

  if (playing) {
    let t = time + dt;
    if (t >= DURATION) {
      t = window.__recording ? DURATION - 0.001 : 0;  // don't loop while recording; keep 0.001s so the last frame is preserved
      if (!window.__recording) fired.clear();
    }
    time = t;
    render(time);
  }
  requestAnimationFrame(tick);
}

// ━━━━━━ boot ━━━━━━
// don't rAF at top level immediately — start only after fonts finish loading
document.fonts.ready.then(() => {
  render(0);                 // draw the initial frame first (fonts ready)
  playing = true;
  requestAnimationFrame(tick);  // the first tick pairs __ready + t=0
});

// ━━━━━━ seek interface (for defensive correction by render-video) ━━━━━━
window.__seek = (t) => { fired.clear(); time = t; lastTick = null; render(t); };
```

**Why this template is right**:

| Aspect | Why it must be this way |
|------|-------------|
| `lastTick = null` + first-frame `return` | Prevents the L seconds between "script loaded" and "tick's first execution" from being counted into animation time |
| `playing = false` default | Even if `tick` runs during font loading, it doesn't advance `time`, avoiding mis-renders |
| `__ready` set on tick's first frame | The recording script starts timing at this moment; the frame shown is the animation's true t=0 |
| Start tick only inside `document.fonts.ready.then(...)` | Avoids fallback-font width measurements and first-frame font jumps |
| `window.__seek` exists | Lets `render-video.js` actively correct — a second line of defense |

**Matching defense on the recording-script side**:
1. `addInitScript` injects `window.__recording = true` (before the page goto)
2. `waitForFunction(() => window.__ready === true)`, recording the offset at that moment as the ffmpeg trim
3. **Extra**: after `__ready`, actively `page.evaluate(() => window.__seek && window.__seek(0))`, force any time deviation in the HTML back to zero — this is the second line of defense, for HTML that doesn't strictly follow the starter template

**Verification**: after exporting the MP4
```bash
ffmpeg -i video.mp4 -ss 0 -vframes 1 frame-0.png
ffmpeg -i video.mp4 -ss $DURATION-0.1 -vframes 1 frame-end.png
```
The first frame must be the animation's t=0 initial state (not mid-animation, not black), and the last frame must be the animation's final state (not some moment in the second loop).

**Reference implementation**: the `Stage` component in `assets/animations.jsx` and `scripts/render-video.js` already implement this protocol. Hand-written HTML must use the starter tick template — every line is there to guard against a specific bug.

## 13. No Looping While Recording — the `window.__recording` Signal

**The bug**: The animation Stage defaults to `loop=true` (convenient for previewing in the browser). `render-video.js` waits an extra 300ms of buffer after recording the duration before stopping, and that 300ms lets the Stage enter its next loop. When ffmpeg cuts with `-t DURATION`, the last 0.5-1s falls into the next loop — the video suddenly jumps back to the first frame (Scene 1) at the end, and the audience thinks the video is bugged.

**Root cause**: There was no "I am recording" handshake between the recording script and the HTML. The HTML didn't know it was being recorded and kept looping as it would in an interactive browser session.

**Rule**:

1. **Recording script**: inject `window.__recording = true` in `addInitScript` (before the page goto):
   ```js
   await recordCtx.addInitScript(() => { window.__recording = true; });
   ```

2. **Stage component**: recognize this signal and force loop=false:
   ```js
   const effectiveLoop = (typeof window !== 'undefined' && window.__recording) ? false : loop;
   // ...
   if (next >= duration) return effectiveLoop ? 0 : duration - 0.001;
   //                                                       ↑ keep 0.001 to prevent Sprite end=duration from being shut off
   ```

3. **Ending Sprite's fadeOut**: in the recording scenario it should be set to `fadeOut={0}`, otherwise the video tail fades to transparent/dark — the user expects to stop on a crisp last frame, not a fade-out. When writing HTML by hand, set `fadeOut={0}` on the ending Sprites.

**Reference implementation**: the `Stage` in `assets/animations.jsx` / `scripts/render-video.js` already have the handshake built in. Hand-written Stage must implement the `__recording` check — otherwise recording is guaranteed to hit this bug.

**Verification**: after exporting the MP4, `ffmpeg -ss 19.8 -i video.mp4 -frames:v 1 end.png` and check whether the last 0.2s is still the expected final frame, not a sudden switch to another scene.

## 14. 60fps Video Defaults to Frame Duplication — minterpolate Has Poor Compatibility

**The bug**: The 60fps MP4 generated by `convert-formats.sh` using `minterpolate=fps=60:mi_mode=mci...` failed to open in some versions of macOS QuickTime / Safari (a black screen or outright refusal to play). VLC / Chrome could open it.

**Root cause**: The H.264 elementary stream produced by minterpolate contains SEI / SPS fields that some players choke on.

**Rule**:

- For default 60fps, use the simple `fps=60` filter (frame duplication); compatibility is broad (QuickTime/Safari/Chrome/VLC all open it)
- For high-quality interpolation, enable it explicitly with the `--minterpolate` flag — but you **must test it locally in the target players** before delivery
- The value of the 60fps label is **algorithm recognition by upload platforms** (Bilibili / YouTube prioritize streaming for 60fps markers); the actual perceived smoothness gain is minimal for CSS animations
- Add `-profile:v high -level 4.0` to improve general H.264 compatibility

**`convert-formats.sh` already defaults to compatibility mode**. If you need interpolated high quality, add the `--minterpolate` flag:
```bash
bash convert-formats.sh input.mp4 --minterpolate
```

## 15. `file://` + External `.jsx` CORS Trap — Single-File Delivery Must Inline the Engine

**The bug**: The animation HTML used `<script type="text/babel" src="animations.jsx"></script>` to load the engine externally. Double-clicking the file locally (`file://` protocol) → Babel Standalone fetches the `.jsx` via XHR → Chrome reports `Cross origin requests are only supported for protocol schemes: http, https, chrome, chrome-extension...` → the whole page goes black, and it only reports a console error, not a `pageerror`, making it easy to misdiagnose as "the animation didn't trigger".

Starting an HTTP server may not save you either — when the machine has a global proxy, `localhost` also goes through the proxy and returns 502 / connection failure.

**Rule**:

- **Single-file delivery (an HTML that works by double-clicking)** → `animations.jsx` must be **inlined** inside a `<script type="text/babel">...</script>` tag; don't use `src="animations.jsx"`
- **Multi-file projects (HTTP server for demos)** → external loading is fine, but the delivery docs must clearly state the `python3 -m http.server 8000` command
- The deciding question: is what you deliver to the user "an HTML file" or "a project directory with a server"? The former gets inlining
- The `Stage` component / `animations.jsx` is often 200+ lines — pasting it into the HTML `<script>` block is perfectly acceptable; don't fear the size

**Minimal verification**: double-click the HTML you generated, and **do not** open it through any server. Only pass if the Stage correctly shows the animation's first frame.

## 16. Inverted Context Across Scenes — Don't Hard-Code Colors on In-Frame Elements

**The bug**: In a multi-scene animation, elements that **appear across scenes** like `ChapterLabel` / `SceneNumber` / `Watermark` had `color: '#1A1A1A'` (dark text) hard-coded in the component. The first 4 scenes had light backgrounds so it was fine; when scene 5 had a black background, "05" and the watermark simply disappeared — no error, no check triggered, key info invisibly gone.

**Rule**:

- **In-frame elements reused across multiple scenes** (chapter labels / scene numbers / timecodes / watermarks / credit bars) **must not hard-code color values**
- Use one of three approaches instead:
  1. **`currentColor` inheritance**: the element only writes `color: currentColor`; the parent scene container sets `color: computed value`
  2. **invert prop**: the component accepts `<ChapterLabel invert />` to manually switch light/dark
  3. **Auto-compute from background**: `color: contrast-color(var(--scene-bg))` (a CSS 4 new API, or decide in JS)
- Before delivery, use Playwright to extract a **representative frame from each scene** and eyeball whether the "cross-scene elements" are all visible

The sneakiness of this bug is that — **there's no error alert**. Only a human eye or OCR can find it.

## 17. Truly Self-Contained Offline / No-CDN — Inline All of React/Babel, and Transpile the Engine Too

**The bug (May 2026 觅游 promo animation)**: The animation HTML used `<script src="https://unpkg.com/react...">` + `<script src=".../@babel/standalone">` from the CDN. The machine had a global proxy, and when Playwright recorded, chromium hit `net::ERR_CONNECTION_CLOSED` on unpkg and Google Fonts alike:

1. React/ReactDOM didn't load → `window.React undefined`
2. Babel didn't load → the JSX in `<script type="text/babel">` ran as plain JS → `Unexpected token '<'`

After fixing React/Babel, a second bug surfaced: **inlining the `animations.jsx` engine as a plain `<script>` still reported `Unexpected token '<'` → `window.Animations is undefined`**. Root cause: **the `animations.jsx` engine itself contains JSX** (the `Stage`/`Sprite` components do `return (<div>...)`), and it was originally designed to be loaded via `<script type="text/babel">` and transpiled by Babel. Only the app code was transpiled, and the engine was forgotten → the engine's JSX was never compiled.

**Rule** (when you need a truly self-contained single file that "double-click to open / works offline / can be recorded by Playwright"):

- **Inline React + ReactDOM locally**: `curl`-download `react.production.min.js` (~10KB) + `react-dom.production.min.js` (~131KB) locally, inline them into `<script>`, don't go through the CDN
- **Build-time Babel precompilation, no Babel at runtime**: use `@babel/standalone` (downloaded once, build-only) in node to run `Babel.transform(src,{presets:['react']}).code`, converting JSX → `React.createElement`. **Both the app and the `animations.jsx` engine must pass through transform** — the engine contains JSX, and if you miss it you're guaranteed to get `Unexpected token '<'`
- **Switch fonts to system fonts**: the Google Fonts CDN gets cut off by the proxy too. Chinese animations use `'PingFang SC'` (sans) / `'Songti SC'` (serif) system fonts that don't depend on the network. `document.fonts.ready` resolves immediately for system fonts, so recording doesn't stall
- **Base64-inline image assets**: `<img src="png/x.png">` relative paths render under `file://`, but for true portability (moving files without losing images) inline them as base64 data URLs; for large background images, convert to JPEG and compress first, then base64
- **Build templating**: the HTML template keeps `__REACT__/__REACTDOM__/__ASSETS__/__ENGINE__` tokens plus a `type="text/jsx-source"` block of app source; the node build script reads the tokens and injects (vendors verbatim, engine + app through Babel) → writes the final single file. Change the animation, re-run the build on the same template

**Verification**: Playwright `page.evaluate(()=>({React:typeof window.React, Animations:typeof window.Animations}))` — both should be `object`. If either is `undefined`, the corresponding `<script>` threw (most likely un-transpiled JSX).

**Relationship to bug #15**: #15 is about "single files shouldn't use `src=` to link `.jsx` externally (file:// CORS)"; this bug goes further — even **remote CDNs for React/Babel/fonts break on restricted networks**, so for true self-containment you must inline everything + transpile at build time.

## 18. 【HyperFrames】CSS transition + class toggling Is Non-Deterministic Under Seek Rendering

CSS `transition` runs on wall-clock time, not the timeline. Under frame-by-frame seek rendering, every frame is an independent screenshot, and the transition's intermediate state depends on "how much wall-clock time passed when we sought to this frame" — completely non-deterministic; it might sit forever at the starting value or randomly stop mid-way. Measured during the c3 migration (2026-07-17): `.watermark-br` with `transition: opacity 0.6s` + class toggling made the opacity misbehave under seek rendering.

**Fix**: express every state change on the render path as a tween or a pure function of t. When migrating old demos, search the whole file for `transition:` and change each one to a lerp inside `render(t)`; for newly written compositions, don't write transitions at all. Transitions for interactive states like hover are fine (they're not triggered during rendering).

## 19. 【HyperFrames】Proxy Tween's First Frame Doesn't Fire — Manually Add `render(0)`

When mounting `render(t)` into a GSAP timeline with a proxy tween (the old-demo adapter route), the timeline sitting at t=0 doesn't necessarily call `onUpdate` — the first frame may be the HTML's static, uninitialized state rather than the picture from `render(0)`.

**Fix**: after registering the timeline, manually synchronously call `render(0)` once. Full recipe in `references/hyperframes-backend.md`.

## 20. 【HyperFrames】The contrast Gate Conflicts with Dark Cinematic Style — Use `--no-contrast`; the Other Four Gates Must Be 0 Errors

The `npm run check` contrast gate checks all text against WCAG AA 4.5:1. In dark cinematic designs, 16-40% opacity watermarks, mono labels, and decorative text are **deliberately** low-contrast (part of the cinematic feel); they'd report errors on delivery, and the framework has no per-element exemption mechanism. In the c3 measurements, all 42 contrast errors were by design.

**Fix**: for dark cinematic output use `npx hyperframes check --no-contrast`; the lint/runtime/layout/motion four gates must still be 0 errors. **For light-background informational output, don't skip contrast** — errors in that context are usually real readability problems (the readability hard floor is in the SKILL.md Fallback section).

## 21. 【HyperFrames/GSAP】the fromTo immediateRender Phantom — Elements Appear Seconds Early

GSAP's `fromTo()` defaults to `immediateRender: true`: when the timeline is built, the from state is rendered onto the elements. If the from state itself is visible (`autoAlpha > 0`), the element appears on screen before its tween starts — short-lived effects like sparks, click circles, ripples, and dust are the most prone (B00 measured a case that hit 4 of these: effects hung on the frame several seconds before their alignment moment).

**Fix**: add explicit `immediateRender: false` to every `fromTo()` whose from state is visible; or switch to "set initially hidden + to". Self-check: after rendering, extract the opening frame of each scene and look for "effect elements that shouldn't be present".

## 22. 【Camera】Blurry Text in 3D / Zoom Modes — Use CSS `zoom`, Not `transform scale`

**Symptom**: when zooming into the page with `transform: scale()` (especially in 3D perspective mode), text goes blurry; the higher the multiplier, the blurrier; above 2x it's undeliverable.

**Root cause**: Chromium rasterizes at the element's **layout size**, then scales up the bitmap. scale only enlarges the bitmap.

**Solution** (shotcraft precedent, the most expensive knowledge in the library): the camera layer's zoom goes through the CSS **`zoom` property** (layout-level scaling — re-layouts and re-rasterizes at the enlarged size, so text stays sharp at any multiplier). Coordinate math and the full formulas in `camera-language.md` §3.4 and `gsap-recipes.md` §9.2. Note: `zoom` triggers a re-layout every frame, making it the single legal exception to "never tween layout properties"; use it only on the `#world` camera layer; under offline frame-by-frame rendering the render time slowing down is normal — output quality wins. Supporting detail: full-page screenshots start at 2x, close-ups get an extra 4x slice cross-fading in over 6f during the push-in phase.

## 23. 【Camera】Perspective Broken by an Intermediate Layer — 3D Instantly Goes Flat

**Symptom**: `perspective` + `preserve-3d` are set, but the render has no 3D feel at all; every layer sits flat.

**Root cause**: **any intermediate layer** between `#camera` and the 3D children that has one of `overflow: hidden`, `filter`, `opacity < 1`, `clip-path` creates a new stacking context and flattens the preserve-3d.

**Solution**: in 3D mode, only put filter/opacity effects on the **innermost elements**; check the container chain layer by layer for the four properties above. Troubleshooting mantra: from `#camera` to the offending element, run `getComputedStyle` on every layer in between and check those four properties.

## 24. 【Camera】pan Exposes Edges — Blank Outside the Canvas Shows While Panning

**Symptom**: white or black edges show at the frame border when the camera pans/tilts.

**Root cause**: `#world` is sized exactly to the viewport, so the moment the camera moves it goes out of bounds.

**Solution**: expand `#world` with a bleed margin around all four sides ≥ the maximum pan amplitude + 8% safety margin (camera-language §3.3). Background/atmosphere layers must cover the full bleed area, not just the viewport. Self-check: seek the timeline to both endpoints of each pan and screenshot, checking all four edges.

## Quick Self-Check Checklist (5 seconds before starting work)

- [ ] Every `position: absolute`'s parent has `position: relative`?
- [ ] All special characters in the animation (`␣` `⌘` `emoji`) exist in the fonts?
- [ ] The Grid/Flex template's count matches the length of the JS data?
- [ ] Scene switches cross-fade, with no pure-blank gap longer than 0.3s?
- [ ] DOM measurement code is wrapped in `document.fonts.ready.then()`?
- [ ] `render(t)` is pure, or has an explicit reset mechanism?
- [ ] Frame 0 is a complete initial state, not blank?
- [ ] No "fake chrome" decoration in the frame (progress bar/timecode/bottom credit bar colliding with the Stage scrubber)?
- [ ] The animation tick sets `window.__ready = true` synchronously on the first frame? (built into animations.jsx; add it yourself for hand-written HTML)
- [ ] The Stage detects `window.__recording` and forces loop=false? (mandatory for hand-written HTML)
- [ ] The ending Sprite's `fadeOut` is set to 0 (stop on a crisp frame at the video tail)?
- [ ] 60fps MP4 defaults to frame-duplication mode (compatibility), with `--minterpolate` only for high-quality interpolation?
- [ ] After export, extract frame 0 + last frame to verify they're the animation's initial/final states?
- [ ] Involves a specific brand (Stripe/Anthropic/Lovart/...): did you run the full "brand asset protocol" (SKILL.md §1.a, five steps)? Did you write `brand-spec.md`?
- [ ] Single-file delivery HTML: `animations.jsx` is inlined, not `src="..."`? (external .jsx goes black from CORS under file://)
- [ ] Cross-scene elements (chapter labels/watermarks/scene numbers) have no hard-coded colors? Visible against every scene's background?
- [ ] For offline / truly self-contained: React+ReactDOM inlined locally, **both the app and the `animations.jsx` engine pass through Babel transpile**, fonts use system fonts? (see bug #17; the engine contains JSX, missing the transpile guarantees `Unexpected token '<'`)
- [ ] 【HyperFrames】No CSS `transition` on the render path? All state changes are tweens or pure functions of t? (bug #18)
- [ ] 【HyperFrames】`render(0)` was called after registering proxy-tween scenes? (bug #19)
- [ ] 【HyperFrames】Did check pass? `--no-contrast` for dark cinematic style, the other four gates 0 errors? (bug #20)
- [ ] 【HyperFrames/GSAP】Every `fromTo()` with a visible from state has `immediateRender:false`? (bug #21, B00 measured 4 phantoms)
- [ ] 【Camera】3D/zoom close-ups go through CSS `zoom`, no blurry scale blow-up? (bug #22)
- [ ] 【Camera】No overflow/filter/opacity/clip-path on the intermediate layers between `#camera` and the 3D elements? (bug #23)
- [ ] 【Camera】`#world` has expanded bleed, and the four edges of pan-endpoint screenshots show no blank? (bug #24)
