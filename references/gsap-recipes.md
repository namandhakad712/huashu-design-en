# GSAP Recipes · Translation layer from design language to GSAP timelines

> This file does exactly one thing: translate the animation design language that
> huashu-design has already settled on (the five-segment narrative, easing system,
> 8 rules of motion language, and scene recipes in `animation-best-practices.md`,
> plus the 22-second 5-scene template in `cinematic-patterns.md`) into
> copy-paste-ready GSAP timeline implementation recipes that run on the
> HyperFrames rendering backend.
>
> **Design judgment follows this skill's own references; GSAP is only the implementation tool.**
> When to hold, which narrative arc to use, what counts as beautiful — read
> `animation-best-practices.md` §0; this file only answers "how do I write this rule in GSAP."
> HyperFrames' composition contract (composition root attributes, `.clip` markers, render
> commands, check audit) is in `references/hyperframes-backend.md`; this file only cites, not restates.

---

## 0 · Base boilerplate (every composition starts here)

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {};

  const tl = gsap.timeline({
    paused: true,                                   // required. HyperFrames is responsible for seeking
    defaults: { ease: "expo.out", duration: 0.6 },  // this skill's primary easing (see §1)
  });

  // ... all tweens attach to this timeline ...

  window.__timelines["main"] = tl;  // key must equal the composition root's data-composition-id
</script>
```

Hard constraints (violate any one and the render result is undefined):

- the timeline must be `paused: true`; **never call `tl.play()`** for render-critical animation
- the timeline must be built in synchronous code, not inside async / timers / event callbacks
- render duration comes from the composition root's `data-duration`, not timeline length. Don't pad length with empty tweens
- no `repeat: -1`. For looping motion, compute a finite repeat count from the visible duration
- note: `defaults: { ease: "expo.out" }` differs from the `power3.out` house default in the hyperframes-animation docs. That is its own taste; this skill's established rule is "expoOut is the default primary easing," and the translation layer follows its own design language

---

## 1 · Easing mapping table · Custom Easing → GSAP

The custom Easing functions in `assets/animations.jsx`, mapped one-to-one to GSAP syntax.
The first three are mathematically **the exact same curve**, not approximations.

| Custom Easing | Math definition | GSAP syntax | Relationship | Usage (established rules) |
|---|---|---|---|---|
| `expoOut` | `1 - 2^(-10t)` | `"expo.out"` | identical | **Default primary easing**. Card rise-in, panel entrances, Terminal fade, focus overlay |
| `overshoot` | easeOutBack, c1=1.70158 | `"back.out"` (default 1.70158) or `"back.out(1.7)"` | identical | Toggle switches, button pops, emphasis interactions |
| `spring` | easeOutElastic, period 2π/3 | `"elastic.out(1, 0.3)"` (i.e. the default `"elastic.out"`) | identical | Geometry settling, physical landing, UI jiggle |
| `easeIn` | `t²` | `"power1.in"` | identical | Exits, Anticipation prep segments |
| `easeOut` | `1-(1-t)²` | `"power1.out"` | identical | Light motion on secondary elements (caption fades, etc.) |
| `easeInOut` | quad inOut | `"power1.inOut"` | identical | Sustained motion (mouse-trajectory interpolation and other symmetric motion) |
| `linear` | `t` | `"none"` | identical | Only for proxy-driven / constant-velocity camera motion. **Forbidden on element effects** |
| `anticipation` | piecewise curve, dips to -0.3 then recovers | no built-in equivalent; use a function ease (see below) |  | Entrance with anticipation |

### 1.1 anticipation · function ease

GSAP accepts any `(p) => number` as an ease, so just port the custom definition verbatim:

```js
// Point-for-point identical to Easing.anticipation in animations.jsx
const anticipation = (t) => {
  if (t < 0.2) return -0.3 * (t / 0.2) * (t / 0.2);   // first 20%: dip opposite direction
  const a = (t - 0.2) / 0.8;
  return -0.012 + 1.012 * a * a * (3 - 2 * a);         // last 80%: smoothstep recovery
};

tl.fromTo("#card", { y: 40 }, { y: 0, duration: 0.7, ease: anticipation }, "s2");
```

Note: this curve overshoots 0 (into negative values), so **it may only be used on transforms** (y / scale / rotation),
never on opacity or colors (it would push them out of legal range).

### 1.2 Alternative for spring · baked spring (seek-safe true physics)

`"elastic.out(1, 0.3)"` is the exact equivalent of the custom spring; using it directly is fine.
When you want a true spring feel with **adjustable damping** (e.g. "settles with almost no overshoot, just a long tail"),
use the `springEase` closed-form solution provided by hyperframes-animation (`adapters/gsap-easing-and-stagger.md`
has the full 40-line implementation; the closed form is a pure function of time, so it's seek-safe):

```js
// dampingFraction 1.0 = calm settling with no overshoot; 0.6-0.7 ≈ the bounce of the custom spring
const settle = springEase({ response: 0.4, dampingFraction: 0.65 });
tl.fromTo("#hero", { scale: 0 }, { scale: 1,
  duration: settle.duration, ease: settle.ease }, "s4");   // duration must be used together; it's part of the physics
```

**Forbidden** to bring in any real-time spring library (react-spring and other integrators): state accumulates frame by frame and cannot be deterministically seeked.

---

## 2 · Five-segment narrative skeleton · Slow-Fast-Boom-Stop (15/15/40/20/10%)

Why: uniformly paced animation is a tech demo; rhythm makes it narrative (best-practices §1).

A labeled timeline skeleton template — change `D` to fit any total duration:

```js
const D = 15;   // total duration (seconds), matches the composition root's data-duration
const at = (p) => D * p;

const tl = gsap.timeline({
  paused: true,
  defaults: { ease: "expo.out", duration: 0.6 },
});

// ── five-segment labels, ratio 15 / 15 / 40 / 20 / 10 ──────────────────
tl.addLabel("s1_trigger",  at(0));     // slow · trigger: give humans reaction time, establish realism
tl.addLabel("s2_generate", at(0.15));  // medium · generate: the visual wow point appears
tl.addLabel("s3_process",  at(0.30));  // fast · process: show control/density/detail
tl.addLabel("s4_boom",     at(0.70));  // Boom · explosion: pull back / 3D pop-out / panels emerge
tl.addLabel("s5_hold",     at(0.90));  // quiet · landing: Logo morph + abrupt stop

// ── S1 trigger (slow rhythm: single action + lots of whitespace) ──────
tl.fromTo("#terminal", { y: 48, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.8 }, "s1_trigger+=0.1");

// ── S2 generate (one clear wow point, no action stacking) ─────────────
tl.fromTo("#result-panel", { scale: 0.92, autoAlpha: 0 },
  { scale: 1, autoAlpha: 1, duration: 0.7 }, "s2_generate");

// ── S3 process (highest density: stagger, typewriter, focus switches all go here) ──
tl.fromTo(".row", { y: 10, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.4, stagger: 0.03 }, "s3_process");

// ── S4 boom (camera-level action: pull back / rotationX / elements emerge) ───────
tl.to("#stage", { scale: 0.82, rotationX: 8, duration: 1.2,
  ease: "expo.inOut" }, "s4_boom");

// ── S5 landing (Logo morph contraction, see §3.6; then nothing happens) ────────
// the final ~0.5s is a deliberate still hold: no tweens added, never fade to black

window.__timelines["main"] = tl;
```

Key points:

- **Whitespace after S5**: `data-duration` extends to the end, but there are no tweens on the timeline,
  so the frame holds on the final state. This is how the "abrupt stop" is implemented (no fade-out ending)
- The 22-second 5-scene template (cinematic-patterns Pattern B) is isomorphic: swap the ratios for
  Invoke 3-4s / Process 5-6s / Insight 4-5s / Output 3-4s / Hero 4-5s, using the same labeling method
- Full-screen transitions between scenes use autoAlpha cross-fade + displacement, not display toggling
  (`display` / bare `visibility` are renderer no-go zones; show/hide always via `autoAlpha`)

---

## 3 · The 8 rules of motion language · rule-by-rule translation

### 3.1 No pure black or pure white backgrounds

Non-timeline rule: the background is static CSS, a neutral with color temperature; the exact values come from the brand spec.
The only GSAP tie-in: when the background needs to change between scenes, tween `backgroundColor` (it's on the allowlist),
and the two scenes' backgrounds should be in the same hue family (cinematic-patterns §2's color-consistency constraint):

```js
tl.to("#stage", { backgroundColor: "#F4EFE6", duration: 0.8, ease: "sine.inOut" }, "s4_boom");
```

### 3.2 Easing is never linear

Why: `linear` makes digital elements feel mechanical; `expoOut` gives physical weight (best-practices §2).

Implementation: write `ease: "expo.out"` in the timeline `defaults` (see §0 boilerplate),
and override per-tween per the §1 mapping table. `ease: "none"` is only allowed in two places:
proxy-driven tweens (§7) and deliberate mechanical motion (constant-velocity camera pans).

### 3.3 Slow-Fast-Boom-Stop

See §2 skeleton; not repeated.

### 3.4 Show "process," not "magic results"

Why: the product is a collaborator, not a magician; showing tweaks / error fixes / redline strikes against the "one-click magic"
of AI slop (best-practices §3.4).

The two most-used "process feel" recipes:

**Chunk Reveal (simulating token streaming)**. The original recipe used `setTimeout + Math.random`,
both illegal under seek rendering. Translated to "precomputed schedule + proxy driver," safe for bidirectional seek:

```js
// Why not tl.call(): callbacks are irreversible; dragging backward in preview leaves stale state
const rand = mulberry32(42);                              // seeded random, see §7.4
const text = "为你生成了三个候选方案，第一个最激进。";
const chunks = text.split(/(?=[，。、；])|(?<=[，。、；])/); // split Chinese into chunks at punctuation
const times = []; let acc = 0;
chunks.forEach(() => { acc += 0.04 + rand() * 0.08; times.push(acc); }); // irregular 40-120ms

const tw = { t: 0 };
tl.to(tw, {
  t: acc, duration: acc, ease: "none",
  onUpdate: () => {   // recompute full visible text from t each frame: pure function, correct when scrubbing back
    let n = 0;
    while (n < times.length && times[n] <= tw.t) n++;
    document.querySelector("#stream").textContent = chunks.slice(0, n).join("");
  },
}, "s2_generate+=0.3");
```

**Number counter (showing real data climbing)**:

```js
// snap guarantees integers; innerText is the counter approach HyperFrames endorses
tl.fromTo("#metric", { innerText: 0 },
  { innerText: 237, snap: { innerText: 1 }, duration: 1.2, ease: "expo.out" }, "s3_process");
```

For thousands separators / suffixes, switch to proxy + onUpdate (derive `toLocaleString` from `tw.v`); same pattern as above.

### 3.5 Mouse trajectory · arc + hand tremor

Why: a straight-line-interpolated mouse has a subconscious mechanical feel; a real hand does "accelerate, arc, decelerate-and-correct"
(best-practices §3.5).

Bezier arcs can't be expressed with ordinary property tweens, so use a proxy driver. For the tremor, skip Perlin
(the original relied on runtime noise); use two sine waves with incommensurable frequencies — a deterministic equivalent:

```js
const mouse = { p: 0 };
const P0 = [100, 100];                       // start point
const P2 = [tx, ty];                          // end point (click target)
const P1 = [tx - 200, ty + 80];               // control point: offset from midpoint to create the arc

tl.to(mouse, {
  p: 1, duration: 1.1, ease: "power1.inOut",  // symmetric easing: accelerate out, decelerate in
  onUpdate: () => {
    const t = mouse.p;
    let x = (1-t)*(1-t)*P0[0] + 2*(1-t)*t*P1[0] + t*t*P2[0];
    let y = (1-t)*(1-t)*P0[1] + 2*(1-t)*t*P1[1] + t*t*P2[1];
    x += Math.sin(t * 47.13) * 2 * (1 - t);   // ±2px tremor, converges near the target
    y += Math.sin(t * 33.7 + 1.3) * 2 * (1 - t);
    gsap.set("#cursor", { x, y });            // everything derived from p, seek-safe
  },
}, "s1_trigger+=0.5");

// click feedback: anticipation shrink, then rebound
tl.to("#cursor", { scale: 0.85, duration: 0.08, ease: "power1.in" }, ">");
tl.to("#cursor", { scale: 1, duration: 0.25, ease: "back.out" }, ">");
```

### 3.6 Logo morph contraction

Why: a simple Logo fade-in has no narrative closure; the previous visual element should "collapse" and then "expand" into the Logo,
so the story collapses onto the brand point (best-practices §3.6).

Blur goes through CSS variables (`filter` is paint-only and seek-safe — the approach endorsed by the official depth-of-field-blur rule):

```css
#lastVisual, #logo { --blur: 0px; filter: blur(var(--blur)); will-change: filter; }
```

```js
tl.addLabel("morph", "s5_hold-=0.3");

// collapse: previous visual shrinks into a color block, motion blur rises
tl.to("#lastVisual", { scale: 0.1, "--blur": "6px",
  duration: 0.5, ease: "expo.out" }, "morph");

// expand: Logo pops out from the center of the color block, blur resolves to sharp
tl.fromTo("#logo",
  { scale: 0.1, "--blur": "6px", autoAlpha: 0 },
  { scale: 1, "--blur": "0px", autoAlpha: 1, duration: 0.6, ease: "back.out" },
  "morph+=0.35");                              // ~150ms overlap = quick cut

tl.to("#lastVisual", { autoAlpha: 0, duration: 0.15 }, "morph+=0.5");
// then: hold, no tweens, abrupt stop
```

### 3.7 Serif + sans-serif dual typefaces

Non-timeline rule: static CSS; font choices come from the brand spec.
The HyperFrames compiler automatically fetches Google Fonts and injects deterministic `@font-face`
(verified in Phase 0; the self-built pipeline's font-timing pitfalls don't exist in the new backend), so just reference Google Fonts normally in CSS.

### 3.8 Focus switch = background dim + foreground sharpen + Flash guide

Why: dropping opacity alone leaves non-focused elements still sharp; only adding blur truly pushes them into the background
(best-practices §3.8).

All three filters go through CSS variables; GSAP tweens the variables themselves:

```css
.tile {
  --f: 0;   /* focusIntensity 0→1 */
  filter: brightness(calc(1 - 0.5 * var(--f)))
          saturate(calc(1 - 0.3 * var(--f)))
          blur(calc(var(--f) * 4px));          /* ← key: blur really pushes non-focused back */
  will-change: filter;
}
```

```js
tl.addLabel("focus", "s3_process+=1.5");

// non-focused elements: three filters + dim in a single tween
tl.to(".tile:not(.focus-target)", {
  "--f": 1, opacity: 0.4, duration: 0.5, ease: "expo.out",
}, "focus");

// Flash highlight guides the eye back.
// Note: the original recipe used element.animate() (WAAPI), which runs on wall-clock time and is
// non-deterministic under seek; it must be translated to a tween
tl.fromTo("#focusFlash",
  { backgroundColor: "rgba(255,255,255,0.3)" },
  { backgroundColor: "rgba(255,255,255,0)", duration: 0.15, ease: "power1.out" },
  "focus+=0.5");

// focus release: settle sharp. Before handing off to the next scene, blur must be pulled back to 0;
// stopping mid-blur reads to the audience as "the render glitched"
tl.to(".tile", { "--f": 0, opacity: 1, duration: 0.5, ease: "power2.inOut" }, "focus+=2.5");
```

Performance constraints (from the official DoF rule): blur radius on large elements ≤24px; prefer "dim + moderate blur"
over maxing out the blur; only add `will-change: filter` to elements whose blur actually animates.

---

## 4 · Specific motion techniques · GSAP versions of the §4 snippets

### 4.1 FLIP / Shared Element (button expanding into an input box)

Why: one element transitions between two states — not a cross-fade between two elements (best-practices §4.1).

The original recipe used Framer Motion's layoutId. On the GSAP side we don't bring in the Flip plugin
(unverified under HyperFrames); compute it by hand instead: the composition viewport is fixed (data-width/height),
so both states' geometry are design constants — hardcode them with fromTo. All displacement/scaling runs on transform
while the element stays in its final layout position:

```css
/* element lays out at the "final" state; the start state is expressed via transform */
#search-box { width: 560px; height: 56px; }   /* static final state, no size tweening */
```

```js
// start geometry: button 120x44 at (400, 300); final state: input 560x56 at (200, 300)
tl.fromTo("#search-box",
  { x: 200, y: 0, scaleX: 120/560, scaleY: 44/56, transformOrigin: "left top" },
  { x: 0,   y: 0, scaleX: 1, scaleY: 1, duration: 0.6, ease: "expo.out" },
  "s2_generate");
// inner text counter-compensates or delays entrance to avoid scaleX stretching (same handling as §4.2)
tl.fromTo("#search-box .placeholder", { autoAlpha: 0 },
  { autoAlpha: 1, duration: 0.3 }, "s2_generate+=0.4");
```

### 4.2 Breathing expansion (expand first, then fill)

Why: panels shouldn't stretch width and height at the same time; expanding horizontally first, then vertically, feels like the physical world
(best-practices §4.2).

The original tweens width/height directly — a reflow no-go under HyperFrames (integer-pixel snapping,
visible jitter on slow segments, §7.2). Translated to scaleX/scaleY, keeping the time offset unchanged:

```js
// L = total expansion duration; first 40% stretches horizontal, vertical starts at 30%, the two overlap
const L = 0.9;
tl.fromTo("#panel",
  { scaleX: 0, scaleY: 0.12, transformOrigin: "left top" },
  { scaleX: 1, duration: 0.4 * L, ease: "expo.out" }, "open");
tl.to("#panel", { scaleY: 1, duration: 0.7 * L, ease: "expo.out" }, "open+=" + 0.3 * L);

// content surfaces only after the shell finishes expanding: both fits the "expand, then fill" imagery
// and hides the stretch-deformation of content during the scale
tl.fromTo("#panel .content", { autoAlpha: 0, y: 8 },
  { autoAlpha: 1, y: 0, duration: 0.35 }, "open+=" + 0.75 * L);
```

Note the scale version isn't pixel-faithful (corners and borders deform with the scale). That's imperceptible
when the expanding shell is a solid-color / large-radius panel; if the panel's border detail matters,
switch to "fixed shell + clip-path reveal of content" and verify with captured frames.

### 4.3 Staggered Fade-up (30ms stagger)

Why: list items entering one-by-one feel more like objects than a block appearing; 30ms is the established interval (best-practices §4.3).

```js
tl.fromTo(".row",
  { y: 10, autoAlpha: 0 },
  { y: 0, autoAlpha: 1, duration: 0.4, ease: "expo.out", stagger: 0.03 },
  "s3_process");

// variant: emerge from center outward (common for the multi-panel emergence in S4's explosion)
tl.fromTo(".panel",
  { y: 24, autoAlpha: 0, scale: 0.96 },
  { y: 0, autoAlpha: 1, scale: 1, duration: 0.5, ease: "expo.out",
    stagger: { each: 0.03, from: "center" } },
  "s4_boom");
```

Use `fromTo`, not `from`: sub-compositions get re-seeked repeatedly, and `from` snapshots the start state
at registration time, which can misalign after scrubbing; `fromTo` declares both ends explicitly and is always consistent.

### 4.4 0.5s hold before key results

Why: machines execute fast and continuously, but the human brain needs reaction time — a 0.5s pause before key results is a courtesy to the audience
(best-practices §4.4, core belief #3 in §0.2).

In GSAP a "hold" is just an empty gap in position parameters; use labels to write the pause in as an explicit design decision:

```js
// the moment generation completes
tl.addLabel("generated", "s2_generate+=1.2");
// loading state holds 0.5s: no tweens during these 0.5s, the audience watches the loading state
tl.addLabel("reveal", "generated+=0.5");

tl.fromTo("#result", { scale: 0.94, autoAlpha: 0 },
  { scale: 1, autoAlpha: 1, duration: 0.7, ease: "expo.out" }, "reveal");
```

### 4.5 Anticipation → Action → Follow-through

Why: an Action-only animation is a PowerPoint animation; Disney's three beats give motion life
(best-practices §4.6).

Three sequential tweens, easing per the §1 mapping (prep power1.in, action expo.out, rebound elastic):

```js
tl.addLabel("pop", "s2_generate+=0.2");
tl.to("#card", { scale: 0.95, duration: 0.12, ease: "power1.in"  }, "pop");        // prep
tl.to("#card", { scale: 1.05, duration: 0.30, ease: "expo.out"   }, ">");          // action
tl.to("#card", { scale: 1.00, duration: 0.35, ease: "elastic.out(1, 0.3)" }, ">"); // rebound
```

Single-tween version: `ease: anticipation` (§1.1) does "prep + action" in one step, plus a rebound segment.

### 4.6 3D Perspective + translateZ layering

Why: rotateX 8° / rotateY -4° simulate a camera looking down from the desk's top-left at a natural angle
(best-practices §4.7).

Perspective and layering are static CSS (copy the original recipe; perspective / translateZ don't need to move);
the moving parts (standing up on entry, pulling back in S4) use GSAP's 3D transform aliases:

```css
.stage-wrap { perspective: 2400px; perspective-origin: 50% 30%; }
.card-grid  { transform-style: preserve-3d; }
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

```js
// entry: slowly stand from head-on to the golden angle
tl.fromTo("#card-grid", { rotationX: 0, rotationY: 0 },
  { rotationX: 8, rotationY: -4, duration: 1.4, ease: "expo.out" }, "s2_generate");
```

### 4.7 Diagonal pan · moving X and Y together, with different frequencies

Why: using different frequencies for X and Y avoids the regularity of a closed Lissajous loop, simulating a hand-held camera's diagonal drift
(best-practices §4.8).

The original computed `Math.sin(flowT * ...)` per frame; the GSAP version layers two yoyo tweens with different
durations (GSAP tracks x / y independently, so the two tweens don't conflict). Repeat must be finite:

```js
// different periods (4.6s vs 2.9s) = different frequencies, path doesn't close
// repeat count derived from visible duration: Math.ceil(D / dur) guarantees full coverage
tl.to("#stage", { x: 40, duration: 4.6, ease: "sine.inOut",
  yoyo: true, repeat: Math.ceil(D / 4.6) }, 0);
tl.to("#stage", { y: 30, duration: 2.9, ease: "sine.inOut",
  yoyo: true, repeat: Math.ceil(D / 2.9) }, 0);
```

### 4.8 Abrupt-stop ending

Why: a fade-out has no decisiveness; the final frame should be crisp and affirmative (best-practices §0.3 whitespace).

Implementation-wise it's "writing no code": after S5's Logo settles, there are no more tweens on the timeline;
`data-duration` extends 0.5-1s past the last tween's end, and the frame holds on the final state.
If there's BGM, use a volume tween to trim the tail (volume is on the allowlist):

```js
tl.to("#bgm", { volume: 0, duration: 0.4 }, "s5_hold+=0.8");  // audio cut off, visuals don't move
```

---

## 5 · Scene recipes A/B/C · timeline structure notes

Design judgment (which one to pick, SFX density, BGM style) lives in best-practices §5; here are only the timeline-side differences.

### Recipe A · Apple Keynote theatrical

- Skeleton: §2 five-segment structure verbatim, with S4's Boom fully played up
- defaults: `ease: "expo.out"`, with `"back.out"` overridden at emphasis interactions
- S4 signature move: rapid camera pull-back + drop. `tl.to("#stage", { scale: 0.78, y: -40, duration: 1.1, ease: "expo.inOut" }, "s4_boom")`
- S5: Logo Morph (§3.6) + a single ethereal tone + hold

### Recipe B · one-continuous-shot tool feel

- Skeleton: **skip** the five-segment peak structure; one continuous flow. Labels placed on BGM bars:
  `tl.addLabel("bar1", 0); tl.addLabel("bar2", 60/88*4);` (88 BPM, one bar ≈ 2.73s)
- Key UI actions' position parameters are written directly on the kick/snare moments — musical groove as interaction SFX
- easing: `springEase` (§1.2) + `"expo.out"` — more settling feel than explosion
- no S4-style Boom; the ending is equally abrupt

### Recipe C · office-productivity narrative

- Skeleton: multiple scenes with hard cuts. One label per scene, fast autoAlpha cuts (0.15s) between scenes
  rather than long cross-fades; paired with Dolly In/Out:
  `tl.fromTo("#scene2", { scale: 1.06 }, { scale: 1, duration: 1.2, ease: "expo.out" }, "sc2")`
- toggle-type interactions all use `"back.out"`; panels all use `"expo.out"`
- the piece must contain exactly one highlight: a 3D pop-out (§4.6's rotationX + translateZ elements floating up),
  done once — showing off everywhere is a cheap signal (§0.3 restraint)

---

## 6 · Seek-safety rules (Phase 0 verified; all of these were hit)

HyperFrames rendering is per-frame seek + screenshot. Any state that isn't a "pure function of time" produces
non-deterministic results in the render — and it **often looks fine in preview**; only the rendered output exposes it.

### 6.1 No CSS transition + class toggling · express everything as tweens

CSS transitions run on the browser's wall clock, not the timeline. Under per-frame seek, every frame is a "state mutation";
the transition either never fires or starts from a wrong state — Phase 0 hit this during the c3 migration.

```css
/* ✗ old way: classList.add('lit') in JS, relying on a transition */
.capsule { transition: transform 0.3s ease; }
.capsule.lit { transform: scale(1.06); }
```

```js
// ✓ new way: the state change itself is a tween on the timeline
tl.to("#capsule", { scale: 1.06, duration: 0.3, ease: "expo.out" }, "lit_at");
tl.to("#capsule", { scale: 1.0,  duration: 0.3, ease: "expo.out" }, "lit_at+=1.2");
```

Same-class no-go zones: `element.animate()` (WAAPI, also wall-clock — §3.8's Flash already has a translation),
and CSS `@keyframes` animation used for render-critical animation.
Before shipping, sweep once: `grep -n "transition:\|animation:\|\.animate(" index.html` —
every hit is either deleted or translated into a tween.

### 6.2 No tweening reflow-triggering properties · use transform instead

Layout properties snap to integer device pixels in the browser's layout phase. Fast tweens hide it;
on a slow ease-out tail, per-frame movement under 1px becomes "bunch up for a few frames, jump 1px" — visible jitter.
Phase 0's lint caught letterSpacing jittering frame-by-frame, exactly this kind of silent visual bug.

| ✗ forbidden to tween | ✓ faithful replacement |
|---|---|
| `width` / `height` | `scaleX` / `scaleY` + `transformOrigin` (content handling in §4.2) |
| `top` / `left` / `right` / `bottom` | element sits at its CSS final position; tween `x` / `y` offsets |
| `fontSize` | `scale` (visually equivalent, sub-pixel smooth) |
| `letterSpacing` / `wordSpacing` | split per character and tween each character's `x` (uniform scale isn't the same effect — it scales glyphs, not tracking) |
| `margin*` / `padding*` | layout hardcoded; move `x` / `y` |

Fix principle: **reproduce the same visual, only removing the jitter**. Passing lint isn't the bar; frame-by-frame comparison with the original animation is.

### 6.3 onUpdate doesn't fire at t=0 · proxy tweens must paint the first frame manually

When the timeline is seeked to 0, a proxy tween's `onUpdate` may not fire, leaving the first frame as blank / initial DOM.
For every proxy-driven scene (§3.4 chunk reveal, §3.5 mouse, §7 legacy-demo adapters),
call it once manually after registering the timeline:

```js
window.__timelines["main"] = tl;
render(0);   // first-frame insurance: explicitly paint the t=0 frame
```

### 6.4 No Math.random / Date.now · use a seeded random function

The same frame must render identically on every seek. Runtime randomness = different every render = can't render frame by frame.
When you need a "random feel" (particles, tremor, irregular intervals), use mulberry32, generating **all random values up front**
before building the timeline (the Phase 0 3D-particle demo's verified approach):

```js
function mulberry32(seed) {
  return function () {
    seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = mulberry32(20260717);   // seed hardcoded; changing the seed = a new random version

// usage: pre-generate, don't draw fresh values inside onUpdate
const offsets = Array.from({ length: 40 }, () => (rand() - 0.5) * 24);
```

Equally forbidden: `Date.now()`, `performance.now()`, and any event-driven state (the render mode has no input events).

---

## 7 · Legacy demo adapter recipe · hanging render(t) on GSAP

The animation core of all 21 self-built-engine legacy demos is a `render(t)` pure function. Migration doesn't rewrite animation logic:
use a proxy tween to hang render(t) on a GSAP timeline (Phase 0 verified: 20-30 minutes per demo,
zero lines of animation code changed, c3 cinematic demo's 1134 lines passed).

### 7.1 Proxy tween template (12 lines, the verified c3 original)

```js
// =============== HyperFrames adapter ===============
// proxy tween drives the original render(t). Every frame is a pure function of timeline time:
// no rAF, no clock, no input state.
window.__timelines = window.__timelines || {};
const proxy = { t: 0 };
const tl = gsap.timeline({ paused: true });
tl.to(proxy, {
  t: T.DURATION,            // the legacy demo's total duration constant
  duration: T.DURATION,
  ease: "none",             // time must map linearly; easing lives inside render(t)
  onUpdate: () => render(proxy.t),
}, 0);
window.__timelines["main"] = tl;

// first-frame insurance (onUpdate doesn't fire when the timeline sits at t=0, §6.3)
render(0);
```

### 7.2 Four migration steps

1. **Wrap root / clip**: add composition-root attributes to the outermost container
   (`data-composition-id="main"` + `data-duration` + dimensions),
   and give the stage element `.clip` plus `data-start` / `data-duration` / `data-track-index`.
   Full contract in `hyperframes-backend.md`
2. **Remove self-driving**: delete the rAF loop, `setInterval`, auto-play logic, and the
   `performance.now()` origin. `render(t)` only takes parameter t and no longer finds time itself
3. **Attach the proxy**: paste the §7.1 template, align `T.DURATION` with `data-duration`, end with `render(0)`
4. **Sweep transitions**: `grep -n "transition:\|animation:\|\.animate(\|Math.random\|Date.now\|performance.now"`
   — clear every hit. Class-toggle effects become pure functions of t per §6.1 (the most common residue in
   legacy demos is the "classList.add + transition" combo)

After migrating, run `npx hyperframes check` once (use `--no-contrast` for dark cinematic pieces;
the other four disciplines must be 0 errors), then capture frames at 3-4 key moments and compare against the old version.

### 7.3 When not to use the adapter

The adapter is a **brownfield migration** solution. Newly written animation uses this file's native timeline
style from §0-§5 directly: readable labels, declarative stagger, and the GSAP inspector can inspect tween-by-tween —
animation hidden inside a proxy black box is opaque to auditing tools.

---

## 8 · Pre-ship self-check (GSAP side; supplements the best-practices §7 checklist)

- [ ] Is the timeline `paused: true` with a registration key equal to `data-composition-id`?
- [ ] Are the defaults `expo.out`, with no bare `linear` / `ease` on element effects?
- [ ] Are all five-segment labels present, with a hold gap after S5 (no fade out)?
- [ ] Does `grep "transition:\|\.animate(\|Math.random\|Date.now"` return 0?
- [ ] No tweening of width / height / top / left / letterSpacing / fontSize?
- [ ] Are all `repeat` values finite?
- [ ] Do proxy scenes append `render(0)` at the end?
- [ ] Do blur / filter all go through CSS variables, and do blurred elements have `will-change: filter`?
- [ ] Do sub-composition entrances all use `fromTo` rather than `from`?
- [ ] Does `npx hyperframes check` pass (`--no-contrast` for dark pieces, 0 errors otherwise)?

---

## 9 · Camera Rig recipes · the implementation layer for camera motion

Why: camera motion and element animation fighting over the same transform is the technical root of messy camera work
(camera-language.md §3). All camera-level tweens funnel into a dedicated rig container;
the camera state rides on a proxy object, and every frame derives the full camera DOM state from it — seek-safe.

### 9.1 Rig container structure (static skeleton)

```html
<div id="viewport">                <!-- fixed viewport -->
  <div id="camera">                <!-- camera layer: only camera transforms -->
    <div id="world">...</div>      <!-- world layer: element animation happens only in here -->
  </div>
  <div id="hud">...</div>          <!-- captions/corner badges: sibling of #camera, naturally static -->
</div>
```

```css
#viewport { position: relative; width: 1920px; height: 1080px; overflow: hidden; }
#camera   { position: absolute; inset: 0; perspective-origin: 960px 540px; }
#world    { position: absolute; transform-origin: 0 0; will-change: transform; }
/* pan edge insurance: #world size ≥ viewport + max pan amplitude + 8% margin (camera-language §3.3) */
```

### 9.2 Camera proxy + PageCam keyframe translation

The camera is a plain object; GSAP tweens its fields and `onUpdate` writes the state into the DOM.
Everything derives from cam, so scrubbing backward is also correct (same proxy idea as §3.4's chunk reveal):

```js
const cam = { cx: 960, cy: 540, zoom: 1, rotX: 0, rotY: 0, rotZ: 0, persp: 1200 };
const camEl = document.querySelector("#camera");
const world = document.querySelector("#world");

// ── planar mode (pure zoom + pan, no rotation) ──────────────────────────
function applyCam() {
  world.style.transform =
    `translate(${960 - cam.cx * cam.zoom}px, ${540 - cam.cy * cam.zoom}px) scale(${cam.zoom})`;
  applyCounter();
}

// ── 3D mode (has rotX/rotY/rotZ) · scaling via the CSS zoom property, not scale ──
// layout-level scaling lets Chromium rasterize at the scaled size, curing blurry text in 3D
// (camera-language §3.4, the most expensive knowledge in the library). zoom changes the coordinate
// system, so translate must be divided by zoom.
function applyCam3d() {
  camEl.style.perspective = `${cam.persp * cam.zoom}px`;
  world.style.zoom = cam.zoom;
  world.style.transformOrigin = `${cam.cx}px ${cam.cy}px`;
  world.style.transform =
    `translate(${960 / cam.zoom - cam.cx}px, ${540 / cam.zoom - cam.cy}px)` +
    ` rotateY(${cam.rotY}deg) rotateX(${cam.rotX}deg) rotateZ(${cam.rotZ}deg)`;
  applyCounter();
}
```

Note: CSS `zoom` triggers re-layout every frame — the **only legal exception** to the §6.2 reflow ban,
allowed solely on the `#world` camera layer. Under HyperFrames / Playwright's offline per-frame rendering,
single-frame time doesn't affect the output; dropped frames in live preview are normal — trust the rendered output.

### 9.3 Logarithmic duration helper (fixed durations are the source of the amateur feel)

```js
// camera-language §4.2: 1→2x is exactly 0.55s; any zoom amplitude has consistent visual speed
function zoomDur(z1, z2) {
  return gsap.utils.clamp(0.30, 0.94,
    0.55 * Math.abs(Math.log(z2 / z1)) / Math.LN2);
}
```

### 9.4 Camera shot syntax (push in → hold → pan → closing pull-out)

All camera tweens drive cam; easing follows camera-language §4.1:
active pushes/pulls use `power3.inOut`, follow shots use `cubic-bezier(0.33,0,0.15,1)` (custom ease below).

```js
const followEase = gsap.parseEase("0.33,0,0.15,1");   // shotcraft's default camera ease

// establishing micro-push: starts at 1.06x on boot, eases back to full over 3s
// (only when the piece is >14s AND the first shot is >7s)
tl.fromTo(cam, { zoom: 1.06 },
  { zoom: 1, duration: 3.0, ease: "power2.out", onUpdate: applyCam }, 0);

// push-in close-up: target point (1240, 430), 1 → 1.8x, duration from the formula
tl.to(cam, { cx: 1240, cy: 430, zoom: 1.8,
  duration: zoomDur(1, 1.8), ease: "power3.inOut", onUpdate: applyCam },
  "s2_generate");
// hold ≥1.2s after the camera lands before moving on (no tween = hold)

// mid-distance focus shift: doesn't return to 1x, pans straight across (inter-shot syntax: 0.22-0.45 → pan)
tl.to(cam, { cx: 880, cy: 620,
  duration: 0.7, ease: followEase, onUpdate: applyCam }, "s3_process+=1.5");

// closing: 0.55s pull-out + ≥0.8s full-frame pause, data-duration extends to the end of the pause
tl.to(cam, { cx: 960, cy: 540, zoom: 1,
  duration: 0.55, ease: "power3.inOut", onUpdate: applyCam }, "s5_hold");

window.__timelines["main"] = tl;
applyCam();   // first-frame insurance: onUpdate doesn't fire when the timeline sits at t=0 (§6.3)
```

The camera budget isn't written into the code; it's decided at shot planning: adjacent camera-tween starts ≥2.6s apart,
≤4-5 in a 15s window, and no zooms under 1.25x (camera-language §0/§4.4).

### 9.5 counter-transform · captions/annotations that follow while keeping constant font size

Captions and chrome belong in `#hud` by preference (they don't follow the camera — zero cost). For annotations that
must live inside world and follow elements while keeping a constant font size, counter the camera zoom in reverse:

```js
const counters = gsap.utils.toArray(".cam-counter");   // annotations needing constant font size
function applyCounter() {
  const inv = 1 / cam.zoom;
  counters.forEach((el) => { el.style.transform = `scale(${inv})`; });
}
```

`.cam-counter`'s own entrance animation goes on its **child elements**, to avoid fighting over the counter's transform.

### 9.6 Multi-layer parallax · everything derived from cam

No independent tweens per layer; each layer's speed factor multiplies the same camera displacement
(inter-layer factor ratio ≥2x, ≤4 layers, camera-language §8.1) — naturally synced, naturally seek-safe:

```js
const LAYERS = [
  { el: document.querySelector("#bg"),  k: 0.35 },
  { el: document.querySelector("#mid"), k: 0.7  },
  { el: document.querySelector("#fg"),  k: 1.4  },
];
function applyParallax() {
  const dx = 960 - cam.cx, dy = 540 - cam.cy;    // camera displacement
  LAYERS.forEach(({ el, k }) => {
    el.style.transform = `translate(${dx * k}px, ${dy * k}px)`;
  });
}
// append applyParallax() to the end of applyCam() and you're done
```

### 9.7 Camera Rig self-check (appended to the §8 checklist)

- [ ] Do camera tweens only touch the cam proxy, with nothing inside `#world` touched by camera tweens?
- [ ] Is `applyCam()` first-frame appended after registering the timeline?
- [ ] Do 3D text close-ups use CSS `zoom`, without blurry `scale()` blow-ups?
- [ ] Does `zoom` appear only on `#world` (the reflow exception doesn't spread)?
- [ ] Do all push/pull durations come from `zoomDur()`, with no hand-written constants?
- [ ] Is there a ≥0.8s no-tween full-frame hold after the closing pull-out?
