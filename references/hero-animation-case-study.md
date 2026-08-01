# Gallery Ripple + Multi-Focus · Scene Orchestration Philosophy

> A **reusable visual orchestration structure** distilled from the huashu-design hero animation v9 (25 seconds, 8 scenes).
> Not an animation production pipeline, but **under what circumstances this orchestration is "right"**.
> Live reference: [demos/hero-animation-v9.mp4](../demos/hero-animation-v9.mp4) · [https://www.huasheng.ai/huashu-design-hero/](https://www.huasheng.ai/huashu-design-hero/)

## In One Sentence

> **When you have 20+ homogeneous visual assets and the scene needs to "express scale and depth", prefer the Gallery Ripple + Multi-Focus orchestration over piling up layouts.**

Generic SaaS feature animations, product launches, skill promotion, and series portfolio showcases — as long as there are enough assets with consistent style, this structure almost always works.

---

## What This Technique Actually Expresses

It's not "showing off assets" — it tells a narrative through **two changes in rhythm**:

**First beat · Ripple expansion (~1.5s)**: 48 cards radiate outward from the center, and the audience is struck by the "quantity" — "oh, this thing has this many outputs."

**Second beat · Multi-Focus (~8s, 4 cycles)**: while the camera slowly pans, 4 times the background is dimmed + desaturated and a single card is enlarged to the center of the screen — the audience shifts from the "impact of quantity" to the "gaze at quality", with a steady 1.7s rhythm each time.

**Core narrative structure**: **Scale (Ripple) → Gaze (Focus × 4) → Fade out (Walloff)**. Combined, these three beats express "Breadth × Depth" — it's not just that you can do a lot, but that each one is worth stopping to look at.

Compare with counter-examples:

| Approach | Audience Perception |
|------|---------|
| 48 cards laid out statically (no Ripple) | Pretty but has no narrative, like a grid screenshot |
| Quick-cutting one by one (no Gallery context) | Like a slideshow, loses the "sense of scale" |
| Only Ripple, no Focus | Strikes you but doesn't make you remember any specific card |
| **Ripple + Focus × 4 (this recipe)** | **First struck by quantity, then gazing at quality, finally fading out calmly — a complete emotional arc** |

---

## Prerequisites (All Must Be Met)

This orchestration is **not a silver bullet** — all 4 conditions below are required:

1. **Asset count ≥ 20, ideally 30+**
   Fewer than 20 assets and the Ripple looks "empty" — only when every one of the 48 slots is moving do you get the sense of density. v9 used 48 slots × 32 images (looping fill).

2. **Visually consistent assets**
   All 16:9 slide previews / all app screenshots / all cover designs — the aspect ratio, tone, and layout should feel like "one set". Mixing styles makes the Gallery look like a clipboard.

3. **Assets still carry readable information when enlarged on their own**
   Focus enlarges a card to 960px wide; if the source image gets blurry or becomes information-poor when scaled up, this Focus beat is wasted. Reverse validation: can you pick 4 of the 48 as the "most representative"? If not, the asset quality is uneven.

4. **The scene itself is landscape or square, not portrait**
   The Gallery's 3D tilt (`rotateX(14deg) rotateY(-10deg)`) needs horizontal extension; a portrait screen makes the tilt look narrow and awkward.

**Fallback paths when a condition is missing**:

| What's Missing | Degrades to |
|-------|-----------|
| Assets < 20 | Switch to "3-5 cards in a static row + focus one at a time" |
| Inconsistent styles | Switch to a keynote-style "cover + 3 chapter hero images" |
| Information-poor | Switch to a "data-driven dashboard" or "quote + big type" |
| Portrait scene | Switch to "vertical scroll + sticky cards" |

---

## Technical Recipe (v9 Production Parameters)

### 4-Layer Structure

```
viewport (1920×1080, perspective: 2400px)
  └─ canvas (4320×2520, extra-large overflow) → 3D tilt + pan
      └─ 8×6 grid = 48 cards (gap 40px, padding 60px)
          └─ img (16:9, border-radius 9px)
      └─ focus-overlay (absolute center, z-index 40)
          └─ img (matches selected slide)
```

**Key**: The canvas is 2.25x larger than the viewport, so the pan has a "peeking at a bigger world" feel.

### Ripple Expansion (Distance-Delay Algorithm)

```js
// Each card's entry time = distance from center × 0.8s delay
const col = i % 8, row = Math.floor(i / 8);
const dc = col - 3.5, dr = row - 2.5;       // offset from center
const dist = Math.hypot(dc, dr);
const maxDist = Math.hypot(3.5, 2.5);
const delay = (dist / maxDist) * 0.8;       // 0 → 0.8s
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
const opacity = expoOut(Math.min(1, localT));
```

**Core parameters**:
- Total duration 1.7s (`T.s3_ripple: [8.3, 10.0]`)
- Max delay 0.8s (center appears first, corners last)
- Each card's entry duration 0.7s
- Easing: `expoOut` (a burst feel, not smooth)

**Done in parallel**: canvas scale goes from 1.25 → 0.94 (zoom out to reveal) — a synchronized push-back feel that accompanies the appearance.

### Multi-Focus (4-Beat Rhythm)

```js
T.focuses = [
  { start: 11.0, end: 12.7, idx: 2  },  // 1.7s
  { start: 13.3, end: 15.0, idx: 3  },  // 1.7s
  { start: 15.6, end: 17.3, idx: 10 },  // 1.7s
  { start: 17.9, end: 19.6, idx: 16 },  // 1.7s
];
```

**Rhythm rule**: each focus is 1.7s, with a 0.6s breather between. Total 8s (11.0–19.6s).

**Inside each focus**:
- In ramp: 0.4s (`expoOut`)
- Hold: middle 0.9s (`focusIntensity = 1`)
- Out ramp: 0.4s (`easeOut`)

**Background changes (this is the key)**:

```js
if (focusIntensity > 0) {
  const dimOp = entryOp * (1 - 0.6 * focusIntensity);  // dim to 40%
  const brt = 1 - 0.32 * focusIntensity;                // brightness 68%
  const sat = 1 - 0.35 * focusIntensity;                // saturate 65%
  card.style.filter = `brightness(${brt}) saturate(${sat})`;
}
```

**Not just opacity — desaturate + darken at the same time**. This makes the foreground overlay's colors "pop" rather than just "get a bit brighter".

**Focus overlay size animation**:
- From 400×225 (entry) → 960×540 (hold state)
- Surrounded by a 3-layer shadow + a 3px accent-colored outline ring, giving a "framed" feel

### Pan (Continuous Motion Keeps Stillness from Being Boring)

```js
const panT = Math.max(0, t - 8.6);
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;
```

- A two-layer motion of sine wave + linear drift — not a pure loop; the position is different at every moment
- Different X/Y frequencies (0.12 vs 0.09) to avoid visually detecting a "regular loop"
- Clamped to ±900/500px to prevent drifting out

**Why not pure linear pan**: with pure linear motion the audience can "predict" where the next second will be; sine + drift keeps every second new, and under the 3D tilt it produces a subtle "boat-sway feel" (the good kind), holding the viewer's attention.

---

## 5 Reusable Patterns (Distilled from the v6→v9 Iterations)

### 1. **expoOut as the primary easing, not cubicOut**

`easeOut = 1 - (1-t)³` (smooth) vs `expoOut = 1 - 2^(-10t)` (explosive then rapidly converging).

**Why**: the first 30% of expoOut quickly reaches 90%, more like physical damping, matching the intuition of "something heavy landing". Particularly good for:
- Card entry (weight)
- Ripple expansion (shockwave)
- Brand floating up (settling feel)

**When to still use cubicOut**: focus out ramps, symmetrical micro-animations.

### 2. **Paper-toned background + terracotta orange accent (Anthropic heritage)**

```css
--bg: #F7F4EE;        /* warm paper */
--ink: #1D1D1F;       /* near black */
--accent: #D97757;    /* terracotta orange */
--hairline: #E4DED2;  /* warm hairlines */
```

**Why**: the warm background keeps a "breathing" quality even after GIF compression, unlike pure white which feels "screen-like". Terracotta orange, as the only accent, runs through the terminal prompt, selected dir-card, cursor, brand hyphen, and focus ring — every visual anchor is threaded together by this single color.

**v5 lesson**: adding a noise overlay to simulate "paper grain" ruined GIF frame compression entirely (every frame differed). v6 switched to "just the base color + warm shadows", keeping 90% of the paper feel while cutting GIF size by 60%.

### 3. **Two-Tier Shadows Simulate Depth Without Real 3D**

```css
.gallery-card.depth-near { box-shadow: 0 32px 80px -22px rgba(60,40,20,0.22), ... }
.gallery-card.depth-far  { box-shadow: 0 14px 40px -16px rgba(60,40,20,0.10), ... }
```

A deterministic `sin(i × 1.7) + cos(i × 0.73)` algorithm assigns each card one of three shadow tiers (near/mid/far) — **it visually reads as "3D stacking", yet the transform never changes between frames, with zero GPU cost**.

**The cost of real 3D**: each card gets its own `translateZ`, and the GPU computes 48 transforms + shadow blur every frame. v4 tried it, and even Playwright recording struggled at 25fps. v6's two-tier shadows are <5% apart to the naked eye, but cost 10x less.

### 4. **Weight Variation (font-variation-settings) Feels More Cinematic Than Size Change**

```js
const wght = 100 + (700 - 100) * morphP;  // 100 → 700 over 0.9s
wordmark.style.fontVariationSettings = `"wght" ${wght.toFixed(0)}`;
```

The brand wordmark morphs from Thin → Bold over 0.9s, paired with a subtle letter-spacing adjustment (-0.045 → -0.048em).

**Why it's better than scaling**:
- Scaling has been seen too many times; expectations are set in stone
- Weight variation is an "inner fullness" — like a balloon being inflated, not "pushed closer"
- Variable fonts only became common in 2020+, so audiences subconsciously read it as "modern"

**Limitation**: the font must support variable fonts (Inter / Roboto Flex / Recursive, etc.). Ordinary static fonts can only approximate it (switching between a few fixed weights causes jumps).

### 5. **Corner Brand as a Low-Intensity Persistent Signature**

During the Gallery stage, a small `HUASHU · DESIGN` mark sits in the top-left corner at 16% opacity, 12px, with wide letter-spacing.

**Why include this**:
- After the Ripple burst, the audience can easily "lose focus" and forget what they're watching; the light mark in the top-left helps anchor them
- More sophisticated than a full-screen big logo — people who do branding know a brand signature doesn't need to shout
- Leaves an attribution signal when the GIF is screenshotted and shared

**Rules**: it appears only in the middle section (when the frame is busy); off at the opening (so it doesn't cover the terminal), and off at the end (the brand reveal is the star).

---

## Counter-Examples: When Not to Use This Orchestration

**❌ Product demos (that need to show features)**: the Gallery flashes every card past in an instant, and the audience can't remember any single feature. Instead use "single-screen focus + tooltip callouts".

**❌ Data-driven content**: the audience needs to read numbers, and the Gallery's fast rhythm doesn't leave time to read. Instead use "data charts + item-by-item reveal".

**❌ Narrative storytelling**: the Gallery is a "parallel" structure, while stories need "cause and effect". Instead use keynote chapter transitions.

**❌ Only 3-5 assets**: the Ripple lacks density and looks like "patching". Instead use "static arrangement + highlight one at a time".

**❌ Portrait (9:16)**: the 3D tilt needs horizontal extension; on a portrait screen the tilt feels "crooked" rather than "unfolding".

---

## How to Tell If Your Task Fits This Orchestration

A three-step quick check:

**Step 1 · Asset count**: count how many similar visual assets you have. < 15 → stop; 15-25 → make do; 25+ → use it directly.

**Step 2 · Consistency test**: place 4 random assets side by side — do they look like "one set"? If not → unify the style first, or change your approach.

**Step 3 · Narrative match**: are you expressing "Breadth × Depth" (quantity × quality)? Or "process", "feature", or "story"? If it's not the former, don't force it.

If all three steps are yes, just fork the v6 HTML, change the `SLIDE_FILES` array and the timeline, and it's reusable. Change the palette via `--bg / --accent / --ink` — a full reskin without changing the bones.

---

## Related References

- Full technical workflow: [references/animations.md](animations.md) · [references/animation-best-practices.md](animation-best-practices.md)
- Animation export pipeline: [references/video-export.md](video-export.md)
- Audio configuration (BGM + SFX dual-track): [references/audio-design-rules.md](audio-design-rules.md)
- Apple gallery-style horizontal reference: [references/apple-gallery-showcase.md](apple-gallery-showcase.md)
- Source HTML (v6 + audio integration): `www.huasheng.ai/huashu-design-hero/index.html`
