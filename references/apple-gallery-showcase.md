# Apple Gallery Showcase · Gallery Display Wall Animation Style

> Inspiration: the Claude Design site's hero video + the "gallery wall" style display on Apple product pages
> From practice: the huashu-design v5 release hero
> Use cases: **product launch hero animation, skill capability demos, portfolio showcases** — any scenario that needs to present "multiple high-quality outputs" at once while guiding the audience's attention

---

## Trigger Check: When to Use This Style

**Good fit**:
- 10+ real outputs to display on screen at once (PPT, app, web pages, infographics)
- Audience is professional (developers, designers, product managers), sensitive to "polish"
- You want to convey a feel of "restrained, exhibition-like, premium, spacious"
- You need both focus and the big picture at once (see the details without losing the whole)

**Poor fit**:
- Single-product focus (use a dedicated single-product hero template instead)
- Emotion-driven / story-heavy animation (use the timeline narrative template)
- Small / portrait screens (the tilted perspective gets blurry on small screens)

---

## Core Visual Tokens

```css
:root {
  /* Light gallery palette */
  --bg:         #F5F5F7;   /* Main canvas background — Apple's site gray */
  --bg-warm:    #FAF9F5;   /* Warm off-white variant */
  --ink:        #1D1D1F;   /* Primary text color */
  --ink-80:     #3A3A3D;
  --ink-60:     #545458;
  --muted:      #86868B;   /* Secondary text */
  --dim:        #C7C7CC;
  --hairline:   #E5E5EA;   /* Card 1px border */
  --accent:     #D97757;   /* Terracotta orange — Claude brand */
  --accent-deep:#B85D3D;

  --serif-cn: "Noto Serif SC", "Songti SC", Georgia, serif;
  --serif-en: "Source Serif 4", "Tiempos Headline", Georgia, serif;
  --sans:     "Inter", -apple-system, "PingFang SC", system-ui;
  --mono:     "JetBrains Mono", "SF Mono", ui-monospace;
}
```

**Key principles**:
1. **Never use a pure black background**. Black makes the work look like a movie, not like "work results that can be adopted"
2. **Terracotta orange is the only hue accent**; everything else is grayscale + white
3. **Three font stacks** (serif EN + serif CN + sans + mono) create a "publication" feel rather than an "internet product" one

---

## Core Layout Patterns

### 1. Floating Cards (the Basic Unit of the Entire Style)

```css
.gallery-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 6px;                          /* Padding is the "mounting mat" */
  border: 1px solid var(--hairline);
  box-shadow:
    0 20px 60px -20px rgba(29, 29, 31, 0.12),   /* Main shadow, soft and long */
    0 6px 18px -6px rgba(29, 29, 31, 0.06);     /* Second-layer near light, creates the floating feel */
  aspect-ratio: 16 / 9;                  /* Unified slide ratio */
  overflow: hidden;
}
.gallery-card img {
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 9px;                    /* Slightly smaller than the card's radius, visual nesting */
}
```

**Anti-example**: don't use edge-to-edge tiles (no padding, no border, no shadow) — that's infographic density, not an exhibition.

### 2. 3D Tilted Work Wall

```css
.gallery-viewport {
  position: absolute; inset: 0;
  overflow: hidden;
  perspective: 2400px;                   /* Deeper perspective, so the tilt isn't exaggerated */
  perspective-origin: 50% 45%;
}
.gallery-canvas {
  width: 4320px;                         /* Canvas = 2.25× viewport */
  height: 2520px;                        /* Leaves room to pan */
  transform-origin: center center;
  transform: perspective(2400px)
             rotateX(14deg)              /* Tilts back */
             rotateY(-10deg)             /* Turns left */
             rotateZ(-2deg);             /* Slight tilt to lose the overly tidy look */
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 40px;
  padding: 60px;
}
```

**Parameter sweet spot**:
- rotateX: 10–15deg (beyond that it starts to look like a VIP backdrop at a party)
- rotateY: ±8–12deg (left–right symmetry)
- rotateZ: ±2–3deg (the human touch of "this wasn't arranged by a machine")
- perspective: 2000–2800px (below 2000 you get fisheye; above 3000 it approaches orthographic projection)

### 3. 2×2 Four-Corner Convergence (Selection Scene)

```css
.grid22 {
  display: grid;
  grid-template-columns: repeat(2, 800px);
  gap: 56px 64px;
  align-items: start;
}
```

Each card slides in from its corresponding corner (tl/tr/bl/br) toward the center + fade in. The matching `cornerEntry` vectors:

```js
const cornerEntry = {
  tl: { dx: -700, dy: -500 },
  tr: { dx:  700, dy: -500 },
  bl: { dx: -700, dy:  500 },
  br: { dx:  700, dy:  500 },
};
```

---

## Five Core Animation Patterns

### Pattern A · Four-Corner Convergence (0.8–1.2s)

Four elements slide in from the viewport's four corners while scaling 0.85→1.0, with ease-out. Good for an opening that "presents a choice of directions".

```js
const inP = easeOut(clampLerp(t, start, end));
card.style.transform = `translate3d(${(1-inP)*ce.dx}px, ${(1-inP)*ce.dy}px, 0) scale(${0.85 + 0.15*inP})`;
card.style.opacity = inP;
```

### Pattern B · Selected Card Enlarges + Others Slide Out (0.8s)

The selected card enlarges 1.0→1.28 while the others fade out + blur + drift back toward the four corners:

```js
// Selected
card.style.transform = `translate3d(${cellDx*outP}px, ${cellDy*outP}px, 0) scale(${1 + 0.28*easeOut(zoomP)})`;
// Unselected
card.style.opacity = 1 - outP;
card.style.filter = `blur(${outP * 1.5}px)`;
```

**Key point**: the unselected cards need blur, not a plain fade. Blur simulates depth of field and visually "pushes" the selected card forward.

### Pattern C · Ripple Expansion (1.7s)

From the center outward, with delay based on distance, each card fades in in sequence while scaling from 1.25x down to 0.94x (a "camera pull-back"):

```js
const col = i % COLS, row = Math.floor(i / COLS);
const dc = col - (COLS-1)/2, dr = row - (ROWS-1)/2;
const dist = Math.sqrt(dc*dc + dr*dr);
const delay = (dist / maxDist) * 0.8;
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
card.style.opacity = easeOut(Math.min(1, localT));

// At the same time, the whole gallery scales 1.25→0.94
const galleryScale = 1.25 - 0.31 * easeOut(rippleProgress);
```

### Pattern D · Sinusoidal Pan (Continuous Drift)

Combines a sine wave + linear drift to avoid the "has a start and an end" looping feel of a marquee:

```js
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;    // Drifts left horizontally
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;    // Drifts up vertically
const clampedX = Math.max(-900, Math.min(900, panX));   // Prevents exposing the edges
```

**Parameters**:
- Sine period `0.09–0.15 rad/s` (slow, roughly one oscillation every 30–50 seconds)
- Linear drift `5–8 px/s` (slower than a viewer's blink)
- Amplitude `120–220 px` (large enough to be felt, small enough not to cause dizziness)

### Pattern E · Focus Overlay (Focus Switch)

**Key design**: the focus overlay is a **flat element** (not tilted) that floats above the tilted canvas. The selected slide scales from its tile position (~400×225) to the screen center (960×540); the background canvas keeps its tilt but **dims to 45%**:

```js
// Focus overlay (flat, centered)
focusOverlay.style.width = (startW + (endW - startW) * focusIntensity) + 'px';
focusOverlay.style.height = (startH + (endH - startH) * focusIntensity) + 'px';
focusOverlay.style.opacity = focusIntensity;

// Background cards dim but stay visible (key: don't mask them 100%)
card.style.opacity = entryOp * (1 - 0.55 * focusIntensity);   // 1 → 0.45
card.style.filter = `brightness(${1 - 0.3 * focusIntensity})`;
```

**The iron law of clarity**:
- The focus overlay's `<img>` must point its `src` directly at the original image — **don't reuse the compressed thumbnail from the gallery**
- Preload all original images into a `new Image()[]` array up front
- The overlay's own `width`/`height` are computed per frame; the browser resamples the original image every frame

---

## Timeline Architecture (Reusable Skeleton)

```js
const T = {
  DURATION: 25.0,
  s1_in: [0.0, 0.8],    s1_type: [1.0, 3.2],  s1_out: [3.5, 4.0],
  s2_in: [3.9, 5.1],    s2_hold: [5.1, 7.0],  s2_out: [7.0, 7.8],
  s3_hold: [7.8, 8.3],  s3_ripple: [8.3, 10.0],
  panStart: 8.6,
  focuses: [
    { start: 11.0, end: 12.7, idx: 2  },
    { start: 13.3, end: 15.0, idx: 3  },
    { start: 15.6, end: 17.3, idx: 10 },
    { start: 17.9, end: 19.6, idx: 16 },
  ],
  s4_walloff: [21.1, 21.8], s4_in: [21.8, 22.7], s4_hold: [23.7, 25.0],
};

// Core easing (v9's historical implementation used cubic; new projects default
// the main easing to expoOut — see the correction in best-practices §2 / hero-case-study Pattern 1)
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeInOut = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
function lerp(time, start, end, fromV, toV, easing) {
  if (time <= start) return fromV;
  if (time >= end) return toV;
  let p = (time - start) / (end - start);
  if (easing) p = easing(p);
  return fromV + (toV - fromV) * p;
}

// A single render(t) function reads the timestamp and writes to all elements
function render(t) { /* ... */ }
requestAnimationFrame(function tick(now) {
  const t = ((now - startMs) / 1000) % T.DURATION;
  render(t);
  requestAnimationFrame(tick);
});
```

**Architecture essence**: **all state is derived from the timestamp t** — no state machine, no setTimeout. The payoff:
- You can jump to any moment instantly via `window.__setTime(12.3)` (handy for playwright frame-by-frame captures)
- Looping is naturally seamless (`t mod DURATION`)
- You can freeze any frame while debugging

---

## Texture Details (Easy to Overlook but Critical)

### 1. SVG Noise Texture

Light backgrounds are most at risk of looking "too flat". Overlay a very faint layer of fractalNoise:

```html
<style>
.stage::before {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.078  0 0 0 0 0.078  0 0 0 0 0.074  0 0 0 0 0.035 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: 0.5;
  pointer-events: none;
  z-index: 30;
}
</style>
```

It looks the same either way — until you remove it.

### 2. Corner Brand Mark

```html
<div class="corner-brand">
  <div class="mark"></div>
  <div>HUASHU · DESIGN</div>
</div>
```

```css
.corner-brand {
  position: absolute; top: 48px; left: 72px;
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--muted);
}
```

Shown only in the work-wall scene, with a fade in/out. Like a museum label.

### 3. Brand Closure Wordmark

```css
.brand-wordmark {
  font-family: var(--sans);
  font-size: 148px;
  font-weight: 700;
  letter-spacing: -0.045em;   /* Negative letter-spacing is the key — it compacts the type into a mark */
}
.brand-wordmark .accent {
  color: var(--accent);
  font-weight: 500;           /* The accent character is actually lighter, for visual contrast */
}
```

`letter-spacing: -0.045em` is standard practice for the large type on Apple product pages.

---

## Common Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Looks like a PPT template | Cards have no shadow / hairline | Add two-layer box-shadow + 1px border |
| Tilt looks cheap | Only rotateY, no rotateZ | Add ±2–3deg rotateZ to break up the tidiness |
| Pan feels "stuttery" | Used setTimeout or a CSS keyframes loop | Use rAF + continuous sin/cos functions |
| Text is unreadable during focus | Reused the gallery tile's low-res image | Dedicated overlay + direct original-image src |
| Background too empty | Flat `#F5F5F7` | Overlay SVG fractalNoise at 0.5 opacity |
| Type looks too "internet" | Only Inter | Add Serif (one CN, one EN) + mono for a three-stack system |

---

## References

- Full implementation sample: hero-animation-v5.html (the original author's local sample, not distributed with the repository)
- Original inspiration: the claude.ai/design hero video
- Reference aesthetics: Apple product pages, Dribbble shot collection pages

When you need an animation that "displays multiple high-quality outputs", just copy the skeleton from this file, swap in your content, and tune the timing.
