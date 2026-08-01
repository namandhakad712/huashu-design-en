# Animation Best Practices · Positive Animation Design Syntax

> Based on a deep breakdown of Anthropic's three official product animations (Claude Design / Claude Code Desktop / Claude for Word),
> these are the "Anthropic-level" animation design rules distilled from them.
>
> Use alongside `animation-pitfalls.md` (the pitfall checklist) — this file is about "**how you should do it**",
> the pitfalls are about "**how you should not do it**". The two are orthogonal, and both should be read.
>
> **Scope statement**: this file only covers **motion logic and expressive style**; it does **not introduce any concrete brand color values**.
> Color decisions go through the §1.a core asset protocol (extracted from the brand spec) or the "Design Direction Advisor"
> (each of the 20 philosophies' own color schemes). This reference discusses "**how it moves**", not "**what color**".

---

## §0 · Who You Are · Identity and Taste

> Before reading any technical rules below, read this section first. Rules **emerge from identity** —
> not the other way around.

### §0.1 Identity Anchor

**You are a motion designer who has studied the motion portfolios of Anthropic / Apple / Pentagram / Field.io.**

When making animations, you are not tweaking CSS transitions — you are using digital elements to **simulate a physical world**,
letting the viewer's subconscious believe "this is an object with weight, inertia, and overflow."

You do not make PowerPoint-style animations. You do not make "fade in fade out" animations. Your animations make people believe the screen
**is a space you can reach into**.

### §0.2 Core Beliefs (3)

1. **Animation is physics, not easing curves**
   `linear` is a number, `expoOut` is an object. You believe the pixels on screen deserve to be treated as "objects."
   Every easing choice is answering the physics question "how heavy is this element? how much friction does it have?"

2. **Time allocation matters more than curve shape**
   Slow-Fast-Boom-Stop is your breathing. **An animation with uniform rhythm is a tech demo; an animation with rhythm is a narrative.**
   Slowing down at the right moment — matters more than using the right easing at the wrong moment.

3. **Yielding to the audience is harder than showing off**
   Pausing 0.5 seconds before a key result is **craft**, not compromise. **Giving the human brain time to react is the animator's highest virtue.**
   By default, AI produces a pause-free, max-information-density animation — that is amateur work. What you do is restraint.

### §0.3 Taste Standard · What Is Beautiful

Your criteria for distinguishing "good" from "great" are below. Each has a **recognition method** — when you see a candidate animation,
use these questions to judge whether it passes, rather than mechanically checking against the 14 rules.

| Dimension of beauty | Recognition method (audience reaction) |
|---|---|
| **Physical weight** | When the animation ends, the element "**lands**" steadily — not merely "**stops**" there. The audience subconsciously feels "this has weight" |
| **Yielding to the audience** | A perceivable pause (≥300ms) before key information appears — the audience has time to "**see**" before continuing |
| **Whitespace** | The ending is an abrupt cut + hold, not a fade to black. The final frame is crisp, affirmative, decisive |
| **Restraint** | Only one place in the whole film is "120% polished"; the other 80% is just right — **showing off everywhere is a cheap signal** |
| **Hand-feel** | Curves (not straight lines), irregularity (not the mechanical rhythm of `setInterval`), a sense of breathing |
| **Respect** | Show the process of tweaking, show the fixing of bugs — **don't hide the work, don't hand over "magic."** AI is a collaborator, not a magician |

### §0.4 Self-Check · First-Impression Method

After you finish an animation, **what is the audience's first reaction?** — this is the only metric you need to optimize.

| Audience reaction | Rating | Diagnosis |
|---|---|---|
| "Looks fairly smooth" | good | Passable but characterless; you're making PowerPoint |
| "That animation is really smooth" | good+ | The technique is right, but nothing is stunning |
| "This thing really looks like it **floated up from the desktop**" | great | You've hit physical weight |
| "This doesn't look AI-made" | great+ | You've reached the Anthropic bar |
| "I want to **screenshot** this and post it" | great++ | You've made the audience spread it voluntarily |

**The difference between great and good is not technical correctness, it's taste.** Correct technique + right taste = great.
Correct technique + empty taste = good. Wrong technique = not even in the door.

### §0.5 The Relationship Between Identity and Rules

The technical rules in §1-§8 below are **execution vehicles** for this identity in concrete scenarios — not an independent list of rules.

- When you hit a scenario the rules don't cover → return to §0 and judge with **identity**, don't guess
- When rules conflict → return to §0 and judge with the **taste standard** which one matters more
- To break a rule → first answer: "Which beauty in §0.3 does this serve?" If you can answer, break it; if you can't, don't

Good. Keep reading.

---

## Overview · Animation as Physics, Unfolded in Three Layers

The root cause of cheap-feeling AI-generated animation is — **they behave like "numbers", not "objects."**
Real-world objects have mass, inertia, elasticity, and overflow. The "premium feel" of Anthropic's three films
comes precisely from giving digital elements **a set of physical-world motion rules**.

This rule set has 3 layers:

1. **Narrative rhythm layer**: the time allocation of Slow-Fast-Boom-Stop
2. **Motion curve layer**: Expo Out / Overshoot / Spring, rejecting linear
3. **Expressive language layer**: showing process, mouse arcs, Logo morph-and-collapse

---

## 1. Narrative Rhythm · The Slow-Fast-Boom-Stop 5-Segment Structure

All three Anthropic films follow this structure without exception:

| Segment | Share | Rhythm | Function |
|---|---|---|---|
| **S1 Trigger** | ~15% | Slow | Gives humans reaction time, establishes a sense of reality |
| **S2 Generate** | ~15% | Medium | The visual wow moment appears |
| **S3 Process** | ~40% | Fast | Shows controllability / density / detail |
| **S4 Boom** | ~20% | Boom | Camera pulls back / 3D pop-out / multi-panel emergence |
| **S5 Landing** | ~10% | Still | Brand Logo + abrupt cut |

**Concrete duration mapping** (using a 15-second animation as an example):
S1 Trigger 2s · S2 Generate 2s · S3 Process 6s · S4 Boom 3s · S5 Landing 2s

**What is forbidden**:
- ❌ Uniform rhythm (same information density every second) — audience fatigue
- ❌ Sustained high density — no peaks, no memory points
- ❌ Fading out at the end (fade out to transparent) — should be an **abrupt cut**

**Self-check**: draw 5 thumbnails on paper, each representing the climactic frame of one segment. If the 5 drawings look too similar,
your rhythm wasn't built.

---

## 2. Easing Philosophy · Reject linear, Embrace Physics

Every motion in Anthropic's three films uses bezier curves with a "damped" feel. The default cubic easeOut
(`1-(1-t)³`) is **not sharp enough** — the start isn't fast enough, the stop isn't steady enough.

### The Three Core Easings (built into animations.jsx)

```js
// 1. Expo Out · fast start, gradual braking (most used, default main easing)
// CSS equivalent: cubic-bezier(0.16, 1, 0.3, 1)
Easing.expoOut(t) // = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)

// 2. Overshoot · springy toggle/button pop
// CSS equivalent: cubic-bezier(0.34, 1.56, 0.64, 1)
Easing.overshoot(t)

// 3. Spring physics · geometry reset, natural settling
Easing.spring(t)
```

### Usage Mapping

| Scenario | Which Easing to Use |
|---|---|
| Card rise-in / panel entry / Terminal fade / focus overlay | **`expoOut`** (main easing, most used) |
| Toggle switch / button pop / emphasized interaction | `overshoot` |
| Preview geometry reset / physical settling / UI element wobble | `spring` |
| Continuous motion (e.g. mouse trajectory interpolation) | `easeInOut` (preserve symmetry) |

### Counter-Intuitive Insight

Most product promos animate **too fast and too stiff**. `linear` makes digital elements feel like machines, `easeOut` is the passing grade,
and `expoOut` is the technical root of the "premium feel" — it gives digital elements a **physical-world sense of weight**.

---

## 3. Motion Language · 8 Common Principles

### 3.1 Don't Use Pure Black or Pure White as a Base Color

None of Anthropic's three films uses `#FFFFFF` or `#000000` as the base color. **Neutral colors with a color temperature**
(warm or cool) carry the materiality of "paper / canvas / desktop" and weaken the machine feel.

**Concrete color decisions** go through the §1.a core asset protocol (extracted from the brand spec) or the "Design Direction Advisor"
(each of the 20 philosophies' own base-color schemes). This reference gives no concrete color values — that is a **brand decision**, not a motion rule.

### 3.2 Easing Is Never linear

See §2.

### 3.3 Slow-Fast-Boom-Stop Narrative

See §1.

### 3.4 Show "Process" Instead of "Magic Results"

- Claude Design shows parameter tweaks and slider dragging (not one-click perfect results)
- Claude Code shows code errors + AI fixing them (not one-shot success)
- Claude for Word shows the redline editing process of deletions in red and additions in green (not dropping the final draft)

**Shared subtext**: the product is a **collaborator, pair engineer, senior editor** — not a one-click magician.
This precisely hits professional users' pain points around "controllability" and "authenticity."

**Anti-AI slop**: AI by default makes "one-click magic success" animations (one-click generate → perfect result),
which is the common denominator. **Doing the opposite** — showing the process, showing tweaks, showing bugs and fixes —
is the source of brand distinctiveness.

### 3.5 Mouse Trajectories Drawn by Hand (Arcs + Perlin Noise)

Real human mouse movement isn't a straight line; it's "initial acceleration → arc → deceleration with correction → click."
AI mouse trajectories interpolated in straight lines **trigger a subconscious aversion**.

```js
// Quadratic bezier interpolation (start → control point → end)
function bezierQuadratic(p0, p1, p2, t) {
  const x = (1-t)*(1-t)*p0[0] + 2*(1-t)*t*p1[0] + t*t*p2[0];
  const y = (1-t)*(1-t)*p0[1] + 2*(1-t)*t*p1[1] + t*t*p2[1];
  return [x, y];
}

// Path: start → offset midpoint → end (to create an arc)
const path = [[100, 100], [targetX - 200, targetY + 80], [targetX, targetY]];

// Then layer on a tiny amount of Perlin Noise (±2px) to create "hand tremor"
const jitterX = (simpleNoise(t * 10) - 0.5) * 4;
const jitterY = (simpleNoise(t * 10 + 100) - 0.5) * 4;
```

### 3.6 Logo "Morph-and-Collapse" (Morph)

In Anthropic's three films, the Logo entrance is **never a simple fade-in**; it is **morphed from the previous visual element**.

**Shared pattern**: in the final 1-2 seconds, do a Morph / Rotate / Converge that makes the whole narrative "collapse" onto the brand mark.

**Low-cost implementation** (no real morph needed):
Collapse the previous visual element into a color block (scale → 0.1, translate toward center),
then the color block "expands" out into the wordmark. Use a 150ms fast cut + motion blur for the transition
(`filter: blur(6px)` → `0`).

```js
<Sprite start={13} end={14}>
  {/* Collapse: previous element scale 0.1, opacity stays, filter blur increases */}
  const scale = interpolate(t, [0, 0.5], [1, 0.1], Easing.expoOut);
  const blur = interpolate(t, [0, 0.5], [0, 6]);
</Sprite>
<Sprite start={13.5} end={15}>
  {/* Expand: Logo from color block center scale 0.1 → 1, blur 6 → 0 */}
  const scale = interpolate(t, [0, 0.6], [0.1, 1], Easing.overshoot);
  const blur = interpolate(t, [0, 0.6], [6, 0]);
</Sprite>
```

### 3.7 Serif + Sans-Serif Dual Typography

- **Brand / narration**: serif (carries "scholarly / published / tasteful" qualities)
- **UI / code / data**: sans-serif + monospace

**A single font family is always wrong**. Serif gives "taste," sans-serif gives "function."

Specific font choices go through the brand spec (the Display / Body / Mono stacks in brand-spec.md) or the Design Direction
Advisor's 20 philosophies. This reference gives no specific fonts — that is a **brand decision**.

### 3.8 Focus Switch = Dim Background + Sharpen Foreground + Flash Guide

A focus switch is **not just lowering opacity**. The complete recipe is:

```js
// Filter combination for non-focused elements
tile.style.filter = `
  brightness(${1 - 0.5 * focusIntensity})
  saturate(${1 - 0.3 * focusIntensity})
  blur(${focusIntensity * 4}px)        // ← key: only adding blur truly makes it "recede"
`;
tile.style.opacity = 0.4 + 0.6 * (1 - focusIntensity);

// After focus completes, do a 150ms Flash highlight at the focus position to guide the eye back
focusOverlay.animate([
  { background: 'rgba(255,255,255,0.3)' },
  { background: 'rgba(255,255,255,0)' }
], { duration: 150, easing: 'ease-out' });
```

**Why blur is mandatory**: with opacity + brightness alone, the non-focused elements are still "sharp" —
visually there's no "receding into the background" effect. blur(4-8px) genuinely pushes the non-focused elements back a depth layer.

---

## 4. Concrete Motion Techniques (Copy-Paste-Ready Code Snippets)

### 4.1 FLIP / Shared Element Transition

The button "expands" into an input field; this is **not** button disappears + new panel appears. The core is **the same DOM element**
transitioning between two states, not two elements cross-fading.

```jsx
// Use Framer Motion layoutId
<motion.div layoutId="design-button">Design</motion.div>
// ↓ after click, the same layoutId
<motion.div layoutId="design-button">
  <input placeholder="Describe your design..." />
</motion.div>
```

Native implementation reference: https://aerotwist.com/blog/flip-your-animations/

### 4.2 "Breathing" Expansion (width→height)

Panel expansion is **not** stretching width and height at the same time, but:
- First 40% of the time: only stretch width (keep height small)
- Last 60% of the time: width holds steady, height expands

This mimics the physical-world feeling of "unfolding first, then filling with water."

```js
const widthT = interpolate(t, [0, 0.4], [0, 1], Easing.expoOut);
const heightT = interpolate(t, [0.3, 1], [0, 1], Easing.expoOut);
style.width = `${widthT * targetW}px`;
style.height = `${heightT * targetH}px`;
```

### 4.3 Staggered Fade-up (30ms stagger)

When table rows, card columns, or list items enter, **delay each element by 30ms** and bring `translateY` back from 10px to 0.

```js
rows.forEach((row, i) => {
  const localT = Math.max(0, t - i * 0.03);  // 30ms stagger
  row.style.opacity = interpolate(localT, [0, 0.3], [0, 1], Easing.expoOut);
  row.style.transform = `translateY(${
    interpolate(localT, [0, 0.3], [10, 0], Easing.expoOut)
  }px)`;
});
```

### 4.4 Non-Linear Breathing · Hover 0.5s Before Key Results

Machines execute fast and seamlessly, but **hover 0.5 seconds before key results appear** to give the viewer's brain reaction time.

```jsx
// Typical scenario: AI finishes generating → hover 0.5s → the result emerges
<Sprite start={8} end={8.5}>
  {/* 0.5s pause — nothing moves, let the viewer stare at the loading state */}
  <LoadingState />
</Sprite>
<Sprite start={8.5} end={10}>
  <ResultAppear />
</Sprite>
```

**Counter-example**: cutting seamlessly from AI generation to the result — the viewer has no reaction time and the information is lost.

### 4.5 Chunk Reveal · Simulating Token Streaming

AI-generated text should **not** pop out character by character via `setInterval` (like old movie subtitles); use **chunk reveal**
— 2-5 characters appear at a time, with irregular intervals, simulating real token streaming output.

```js
// Split by chunks rather than by characters
const chunks = text.split(/(\s+|,\s*|\.\s*|;\s*)/);  // split by words + punctuation
let i = 0;
function reveal() {
  if (i >= chunks.length) return;
  element.textContent += chunks[i++];
  const delay = 40 + Math.random() * 80;  // irregular 40-120ms
  setTimeout(reveal, delay);
}
reveal();
```

### 4.6 Anticipation → Action → Follow-through

Three of the Disney 12 principles. Anthropic uses them very explicitly:

- **Anticipation** (preparation): a small opposite motion before the action begins (button slightly shrinks then pops)
- **Action**: the main action itself
- **Follow-through**: residual motion after the action ends (card bounces slightly after settling)

```js
// The complete three-phase card entrance
const anticip = interpolate(t, [0, 0.2], [1, 0.95], Easing.easeIn);     // anticipation
const action  = interpolate(t, [0.2, 0.7], [0.95, 1.05], Easing.expoOut); // action
const settle  = interpolate(t, [0.7, 1], [1.05, 1], Easing.spring);       // follow-through
// final scale = product of the three phases or applied piecewise
```

**Counter-example**: an animation with only Action and no Anticipation + Follow-through looks like a "PowerPoint animation."

### 4.7 3D Perspective + translateZ Layering

To get a "tilted 3D + floating card" feel, add `perspective` to the container and give individual elements different translateZ values:

```css
.stage-wrap {
  perspective: 2400px;
  perspective-origin: 50% 30%;  /* line of sight slightly looking down */
}
.card-grid {
  transform-style: preserve-3d;
  transform: rotateX(8deg) rotateY(-4deg);  /* golden ratio */
}
.card:nth-child(3n) { transform: translateZ(30px); }
.card:nth-child(5n) { transform: translateZ(-20px); }
.card:nth-child(7n) { transform: translateZ(60px); }
```

**Why rotateX 8° / rotateY -4° is the golden ratio**:
- Greater than 10° → elements distort too much, they look "fallen over"
- Less than 5° → looks like "shear" rather than "perspective"
- The asymmetric 8° × -4° ratio simulates the natural angle of a "camera looking down from the top-left of the desktop"

### 4.8 Diagonal Pan · Moving XY Together

Camera movement is not purely vertical or purely horizontal, but **moves XY together** to simulate diagonal motion:

```js
const panX = Math.sin(flowT * 0.22) * 40;
const panY = Math.sin(flowT * 0.35) * 30;
stage.style.transform = `
  translate(-50%, -50%)
  rotateX(8deg) rotateY(-4deg)
  translate3d(${panX}px, ${panY}px, 0)
`;
```

**Key**: X and Y use different frequencies (0.22 vs 0.35) to avoid regular Lissajous loops.

---

## 5. Scene Recipes (Three Narrative Templates)

Of the reference materials, the three videos correspond to three product personalities. **Choose the one that best fits your product**; don't mix them.

### Recipe A · Apple Keynote Drama (Claude Design type)

**Best for**: major releases, hero animations, visual-wow priority
**Rhythm**: Slow-Fast-Boom-Stop with a strong arc
**Easing**: `expoOut` throughout + a little `overshoot`
**SFX density**: high (~0.4/s), SFX pitch tuned to the BGM scale
**BGM**: IDM / minimal tech-electronics, cool and precise
**Collapse**: camera pulls back sharply → drop → Logo morph → ethereal single note → abrupt cut

### Recipe B · One-Take Tool Film (Claude Code type)

**Best for**: developer tools, productivity apps, flow-state scenarios
**Rhythm**: sustained steady flow, no obvious peaks
**Easing**: `spring` physics + `expoOut`
**SFX density**: **0** (purely BGM-driven editing rhythm)
**BGM**: Lo-fi Hip-hop / Boom-bap, 85-90 BPM
**Core technique**: land key UI actions on the BGM kick/snare transients — "**the music's rhythm IS the interaction sound**"

### Recipe C · Office Efficiency Narrative (Claude for Word type)

**Best for**: enterprise software, documents/spreadsheets/calendars, professional-feel priority
**Rhythm**: hard cuts between scenes + Dolly In/Out
**Easing**: `overshoot` (toggle) + `expoOut` (panels)
**SFX density**: medium (~0.3/s), UI clicks dominant
**BGM**: Jazzy Instrumental, minor key, BPM 90-95
**Core highlight**: one scene must have "the whole film's high point" — a 3D pop-out / floating off the plane

---

## 6. Counter-Examples · This Is What AI Slop Looks Like

| Anti-pattern | Why it's wrong | Correct approach |
|---|---|---|
| `transition: all 0.3s ease` | `ease` is linear's cousin; all elements move at the same speed | Use `expoOut` + per-element stagger |
| All entrances as `opacity 0→1` | No sense of motion direction | Pair with `translateY 10→0` + Anticipation |
| Logo fade-in | No narrative collapse | Morph / Converge / collapse-expand |
| Mouse moving in a straight line | subconscious machine feel | Bezier arcs + Perlin Noise |
| Text popping out character by character (setInterval) | Like old movie subtitles | Chunk Reveal with random intervals |
| No hover before key results | Viewer has no reaction time | Hover 0.5s before the result |
| Focus switch only changes opacity | Non-focused elements stay sharp | opacity + brightness + **blur** |
| Pure black / pure white background | cyberpunk feel / reflection fatigue | Neutral colors with temperature (go through the brand spec) |
| All animations equally fast | No rhythm | Slow-Fast-Boom-Stop |
| Fade out ending | No decisiveness | Abrupt cut (hold the final frame) |

---

## 6.5 · Visual Density Clauses for Director's Notes (Practical lesson from the B00 phase, 2026-07-17)

**A director's notes that only writes narrative + camera movement will come back as wireframes.** In the B00 step-jump b-roll test: the v1 director's notes fully covered all six scenes' narrative, timeline, and camera moves; the animation and motion delivered by the implementing agent all passed, all checks green — but the visuals were schematic-level "three plain dark blocks + big text," rejected in one vote by the director ("too simple, too boring"). With no density standard, an agent will always deliver with the minimal geometry required to get by.

**The director's notes (or any animation brief) must explicitly include three things**:

1. **Visual density standard**: the required magnitude of detail elements per screen (skeleton-UI content rows, legends, textures, secondary elements), plus one executable acceptance statement, such as "pause at any frame and it doesn't look embarrassing next to the reference benchmark"
2. **Reference benchmark**: point at a specific finished work (an older animation in the same project / the A-series / some demo), and borrow the build craft directly — don't let the agent invent things from nothing
3. **Global atmosphere layer checklist**: ground-line anchoring, soft shadows on elements, paper/surface background texture, hero element's companion or similar personified small elements, idle micro-motion for static elements (breathing / cursor / micro-advance) — the main remedy for "empty and boring" is this layer, not the primary elements themselves

**The fix path also has a standard pattern**: the motion skeleton (timeline / camera moves / morph path / text-card timing) and the visual craft (elements / density / atmosphere) are two layers. When acceptance is rejected, first ask which layer the problem is in — if the motion passes, just do a re-skin, don't re-choreograph.

---

## 7. Self-Check Checklist (60 Seconds Before Delivering an Animation)

- [ ] Is the narrative structure Slow-Fast-Boom-Stop, not uniform rhythm?
- [ ] Is the default easing `expoOut`, not `easeOut` or `linear`?
- [ ] Do toggles / button pops use `overshoot`?
- [ ] Do card / list entrances have a 30ms stagger?
- [ ] Is there a 0.5s hover before key results?
- [ ] Does text use Chunk Reveal, not setInterval character-by-character?
- [ ] Does the focus switch add blur (not just opacity)?
- [ ] Is the Logo a morph-and-collapse (Morph), not a fade-in?
- [ ] Is the base color not pure black / pure white (has temperature)?
- [ ] Does the text have serif + sans-serif hierarchy?
- [ ] Does the ending cut abruptly, not fade out?
- [ ] (If there's a mouse) is the mouse trajectory an arc, not a straight line?
- [ ] Does the SFX density match the product personality (see recipes A/B/C)?
- [ ] Is there a 6-8dB loudness gap between BGM and SFX? (see `audio-design-rules.md`)

---

## 8. Relationship to Other References

| reference | Positioning | Relationship |
|---|---|---|
| `animation-pitfalls.md` | Technical pitfalls (16) | "**How you should not do it**" · the inverse of this file |
| `animations.md` | Stage/Sprite engine usage | The basics of **how to write** animation |
| `audio-design-rules.md` | Dual-track audio rules | Rules for **scoring** animation with audio |
| `sfx-library.md` | Catalog of 37 SFX | The sound-effect **asset library** |
| `apple-gallery-showcase.md` | Apple gallery showcase style | A monograph on one specific motion style |
| **This file** | Positive motion design syntax | "**How you should do it**" |

**Call order**:
1. First look at Step 3 form-derivation's five questions in the SKILL.md workflow (decides the narrative role and visual temperature)
2. After choosing a direction, read this file to lock the **motion language** (recipe A/B/C)
3. When writing code, consult `animations.md` and `animation-pitfalls.md`
4. When exporting video, go through `audio-design-rules.md` + `sfx-library.md`

---

## Appendix · Source Material for This File

- Anthropic official animation breakdown: `参考动画/BEST-PRACTICES.md` in the Huashu-Design project directory
- Anthropic audio breakdown: `AUDIO-BEST-PRACTICES.md` in the same directory
- The 3 reference videos: `ref-{1,2,3}.mp4` + the corresponding `gemini-ref-*.md` / `audio-ref-*.md`
- **Strict filter**: this reference does not include any concrete brand color values, font names, or product names.
  Color/typography decisions go through the §1.a core asset protocol or the 20 design philosophies.
