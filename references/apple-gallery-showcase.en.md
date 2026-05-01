# Apple Gallery Showcase · Gallery Display Wall Animation Style

> Inspiration source: Claude Design official website hero video + Apple product page "work wall" style display
> Practical origin: huashu-design release hero v5
> Applicable scenarios: **product launch hero animation, skill capability demo, portfolio showcase** — any scenario needing to display "multiple high-quality outputs" simultaneously while guiding audience attention

---

## Trigger Decision: When to Use This Style

**Suitable**:
- Have 10+ real outputs to display on same screen (PPT, App, infographic)
- Audience is professional (developers, designers, product managers), sensitive to "texture"
- Convey vibe: "restrained, exhibition-style, premium, spatial"
- Need focus and global to exist simultaneously (see details but don't lose overall)

**Not suitable**:
- Single product focus (use frontend-design product hero template)
- Emotion-driven/story-heavy animation (use timeline narrative template)
- Small screen / vertical (tilted perspective will be blurry on small screens)

---

## Core Visual Tokens

```css
:root {
  /* Light gallery palette */
  --bg:         #F5F5F7;   /* Main canvas background — Apple official gray */
  --bg-warm:    #FAF9F5;   /* Warm off-white variant */
  --ink:        #1D1D1F;   /* Main text color */
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
1. **Never use pure black background**. Black makes work look like movie, not "work results that can be adopted"
2. **Terracotta orange is the only hue accent**, rest all grayscale + white
3. **Three font stacks** (serif-en + serif-cn + sans + mono) create "publication" not "internet product" vibe

---

## Core Layout Patterns

### 1. Floating Cards (Basic Unit of Entire Style)

```css
.gallery-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 6px;                          /* Padding is "mounting paper" */
  border: 1px solid var(--hairline);
  box-shadow:
    0 20px 60px -20px rgba(29, 29, 31, 0.12),   /* Main shadow, soft and long */
    0 6px 18px -6px rgba(29, 29, 31, 0.06);     /* Second layer near light, creates floating feel */
  aspect-ratio: 16 / 9;                  /* Unified slide ratio */
  overflow: hidden;
}
.gallery-card img {
  width: 100%; height: 100%;
  object-fit: cover;
  border-radius: 9px;                    /* Slightly smaller than card radius, visual nesting */
}
```

**Counter-example**: Don't do edge-to-edge tiles (no padding no border no shadow) — that's infographic density expression, not exhibition.

### 2. 3D Tilted Work Wall

```css
.gallery-viewport {
  position: absolute; inset: 0;
  overflow: hidden;
  perspective: 2400px;                   /* Deeper perspective, tilt not exaggerated */
  perspective-origin: 50% 45%;
}
.gallery-canvas {
  width: 4320px;                         /* Canvas = 2.25× viewport */
  height: 2520px;                        /* Leave pan space */
  transform-origin: center center;
  transform: perspective(2400px)
             rotateX(14deg)              /* Tilt back */
             rotateY(-10deg)             /* Turn left */
             rotateZ(-2deg);             /* Slight tilt, remove too regular feel */
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 40px;
  padding: 60px;
}
```

**Parameter sweet spot**:
- rotateX: 10-15deg (more becomes like VIP backdrop at wine party)
- rotateY: ±8-12deg (symmetric left-right)
- rotateZ: ±2-3deg ("not arranged by machine" human touch)
- perspective: 2000-2800px (less than 2000 fisheye, greater than 3000 approaches orthographic projection)

### 3. 2×2 Four-Corner Convergence (Selection Scene)

```css
.grid22 {
  display: grid;
  grid-template-columns: repeat(2, 800px);
  gap: 56px 64px;
  align-items: start;
}
```

Each card slides in from corresponding corner (tl/tr/bl/br) to center + fade in. Corresponding `cornerEntry` vectors:

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

### Pattern A · Four-Corner Convergence (0.8-1.2s)

4 elements slide in from viewport four corners, simultaneously scale 0.85→1.0, corresponding ease-out. Suitable for "show multiple direction choices" opening.

```js
const inP = easeOut(clampLerp(t, start, end));
card.style.transform = `translate3d(${(1-inP)*ce.dx}px, ${(1-inP)*ce.dy}px, 0) scale(${0.85 + 0.15*inP})`;
card.style.opacity = inP;
```

### Pattern B · Selected Enlarge + Others Slide Out (0.8s)

Selected card enlarges 1.0→1.28, other cards fade out + blur + drift to four corners:

```js
// Selected
card.style.transform = `translate3d(${cellDx*outP}px, ${cellDy*outP}px, 0) scale(${1 + 0.28*easeOut(zoomP)})`;
// Unselected
card.style.opacity = 1 - outP;
card.style.filter = `blur(${outP * 1.5}px)`;
```

**Key**: Unselected need blur, not pure fade. Blur simulates depth of field, visually "pushes" selected out.

### Pattern C · Ripple Expansion (1.7s)

From center outward, by distance delay, each card fades in sequentially + scales from 1.25x to 0.94x ("camera pulls back"):

```js
const col = i % COLS, row = Math.floor(i / COLS);
const dc = col - (COLS-1)/2, dr = row - (ROWS-1)/2;
const dist = Math.sqrt(dc*dc + dr*dr);
const delay = (dist / maxDist) * 0.8;
const localT = Math.max(0, (t - rippleStart - delay) / 0.7);
card.style.opacity = easeOut(Math.min(1, localT));

// Simultaneously overall scale 1.25→0.94
const galleryScale = 1.25 - 0.31 * easeOut(rippleProgress);
```

### Pattern D · Sinusoidal Pan (Continuous Drift)

Use sine wave + linear drift combination, avoid marquee "has start has end" looping feel:

```js
const panX = Math.sin(panT * 0.12) * 220 - panT * 8;    // Horizontal left drift
const panY = Math.cos(panT * 0.09) * 120 - panT * 5;    // Vertical up drift
const clampedX = Math.max(-900, Math.min(900, panX));   // Prevent edge exposure
```

**Parameters**:
- Sine period `0.09-0.15 rad/s` (slow, ~30-50 seconds one oscillation)
- Linear drift `5-8 px/s` (slower than viewer blink)
- Amplitude `120-220 px` (big enough to feel, small enough not to dizzy)

### Pattern E · Focus Overlay (Focus Switch)

**Key design**: Focus overlay is a **flat element** (not tilted), floating above tilted canvas. Selected slide scales from tile position (~400×225) to screen center (960×540), background canvas doesn't change tilt but **dims to 45%**:

```js
// Focus overlay (flat, centered)
focusOverlay.style.width = (startW + (endW - startW) * focusIntensity) + 'px';
focusOverlay.style.height = (startH + (endH - startH) * focusIntensity) + 'px';
focusOverlay.style.opacity = focusIntensity;

// Background cards dim, but still visible (key! don't 100% mask)
card.style.opacity = entryOp * (1 - 0.55 * focusIntensity);   // 1 → 0.45
card.style.filter = `brightness(${1 - 0.3 * focusIntensity})`;
```

**Clarity iron law**:
- Focus overlay's `<img>` must `src` directly connect to original image, **don't reuse gallery compressed thumbnail**
- Preload all original images to `new Image()[]` array in advance
- Overlay own `width/height` calculated per frame, browser resamples original every frame

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

// Core easing
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeInOut = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2, 3)/2;
function lerp(time, start, end, fromV, toV, easing) {
  if (time <= start) return fromV;
  if (time >= end) return toV;
  let p = (time - start) / (end - start);
  if (easing) p = easing(p);
  return fromV + (toV - fromV) * p;
}

// Single render(t) function reads timestamp, writes all elements
function render(t) { /* ... */ }
requestAnimationFrame(function tick(now) {
  const t = ((now - startMs) / 1000) % T.DURATION;
  render(t);
  requestAnimationFrame(tick);
});
```

**Architecture essence**: **All states derived from timestamp t**, no state machine, no setTimeout. This:
- Play to any moment `window.__setTime(12.3)` immediately jumps (convenient for playwright frame-by-frame capture)
- Loop naturally seamless (t mod DURATION)
- Debug can freeze any frame

---

## Texture Details (Easily Overlooked But Critical)

### 1. SVG noise texture

Light background most fears "too flat". Overlay one layer very weak fractalNoise:

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

Looks no difference, removing reveals presence.

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

Only shows in work wall scene, fade in/out. Like museum exhibition label.

### 3. Brand Closure Wordmark

```css
.brand-wordmark {
  font-family: var(--sans);
  font-size: 148px;
  font-weight: 700;
  letter-spacing: -0.045em;   /* Negative letter-spacing key, makes characters compact into mark */
}
.brand-wordmark .accent {
  color: var(--accent);
  font-weight: 500;           /* Accent character反而细一点，视觉差 */
}
```

`letter-spacing: -0.045em` is standard approach for Apple product page large text.

---

## Common Failure Modes

| Symptom | Cause | Solution |
|---|---|---|
| Looks like PPT template | Cards no shadow/hairline | Add two-layer box-shadow + 1px border |
| Tilt feels cheap | Only rotateY without rotateZ | Add ±2-3deg rotateZ to break regularity |
| Pan feels "stuck" | Used setTimeout or CSS keyframes loop | Use rAF + sin/cos continuous function |
| Text unclear during focus | Reused gallery tile low-res image | Independent overlay + original image src direct |
| Background too empty | Solid `#F5F5F7` | Overlay SVG fractalNoise 0.5 opacity |
| Fonts too "internet" | Only Inter | Add Serif (cn+en) + mono three stacks |

---

## References

- Complete implementation sample: `/Users/alchain/Documents/写作/01-公众号写作/项目/2026.04-huashu-design发布/配图/hero-animation-v5.html`
- Original inspiration: claude.ai/design hero video
- Reference aesthetics: Apple product page, Dribbble shot collection pages

When encountering animation needs for "multiple high-quality outputs to display", directly copy skeleton from this file, change content + adjust timing.