# Cinematic Patterns · Best Practice for Workflow Demos

> The 5 key patterns for upgrading from "PPT animation" to "launch-level cinematic."
> Distilled from the two cinematic demos in the 2026-04 "talking about skills" deck (Nuwa workflow + Darwin workflow); tested and reproducible.

---

## 0 · What this document solves

When you need to make a "demo animation showing a workflow" (typical scenarios: skill workflow, product onboarding, API call flows, agent task execution), there are two common approaches:

| Paradigm | What it looks like | Consequence |
|---|---|---|
| **PPT animation** (bad) | step 1 fade in → step 2 fade in → step 3 fade in, 4 boxes side by side on screen | The viewer feels "it's just a PPT with fades," no wow moment |
| **Cinematic** (good) | scene-based, only one thing focused at a time, scenes linked by dissolve / focus pull / morph | The viewer feels "this is a product-launch segment" and wants to screenshot and share |

The root of the difference **is not animation technique** — it's **narrative paradigm**. This document explains how to upgrade from the former to the latter.

---

## 1 · The five core patterns

### Pattern A · Dashboard + Cinematic Overlay two-layer structure

**Problem**: a pure cinematic defaults to a black screen + a ▶ button; if the user lands on this page and doesn't click, there's nothing to see.

**Solution**:
```
DEFAULT state (always shown): complete static workflow dashboard
  └── viewers see at a glance how this skill / workflow runs

POINT ▶ trigger (overlay floats up): 22-second cinematic
  └── when finished, auto-fades back to DEFAULT

```

**Implementation essentials**:
- `.dash` visible by default, `.cinema` default `opacity: 0; pointer-events: none`
- `.play-cta` is a small gold button in the bottom-right corner (not a big central overlay)
- Click → `cinema.classList.add('show')` + `dash.classList.add('hide')`
- Run once with `requestAnimationFrame` (not a loop); when done, `endCinematic()` reverses the state

**Anti-pattern**: default = a big central ▶ overlay covering everything; the page is blank until clicked.

---

### Pattern B · Scene-based, NOT Step-based

**Problem**: splitting the animation into "step 1 shows → step 2 shows → ..." is PPT thinking.

**Solution**: split into 5 scenes, each scene an **independent shot**, full-screen focus on one thing at a time:

| Scene type | Responsibility | Duration |
|---|---|---|
| 1 · Invoke | user input trigger (terminal typewriter) | 3-4s |
| 2 · Process | visualization of the core workflow (distinct visual language) | 5-6s |
| 3 · Result/Insight | the distilled key artifacts (visualized) | 4-5s |
| 4 · Output | showing the actual output (files / diff / numbers) | 3-4s |
| 5 · Hero Reveal | closing hero moment (big text + value proposition) | 4-5s |

**Total ≈ 22 seconds** — the tested golden length:
- Under 18 seconds: PMs aren't in the zone yet when it ends
- Over 25 seconds: patience runs out
- 22 seconds is just enough for "hook → unfold → tie off → leave an impression"

**Implementation essentials**:
- `T = { DURATION: 22.0, s1_in: [0, 0.7], s2_in: [3.8, 4.6], ... }` global timeline
- a single `requestAnimationFrame(render)` computes the opacity / transform for all scenes
- don't chain `setTimeout`s (fragile, hard to debug)
- easing must use `expoOut` / `easeOut` / cubic-bezier; **linear is forbidden**

---

### Pattern C · Each demo's visual language must be independent

**Problem**: after finishing the first cinematic, lazily reusing the same template for the second (same orbit + pentagon + typewriter + hero big text), only swapping the copy.

**Consequence**: viewers find the two skills "look identical," which is equivalent to saying "these two skills are no different."

**Solution**: each workflow's core metaphor is different, so the visual language must be different.

**Comparison case**:

| Dimension | Nuwa (distillation) | Darwin (optimization skill) |
|---|---|---|
| Core metaphor | collect → distill → write | loop → evaluate → ratchet |
| Visual motion | floating / radiating / pentagon | looping / ascending / comparing |
| Scene 2 | 3D Orbit · 8 archives floating in a perspective ellipse | Spin Loop · tokens run 5 laps around a 6-node ring |
| Scene 3 | Pentagon · 5 tokens radiating from the center | v1 vs v5 · side-by-side diff (red version vs gold version) |
| Scene 4 | SKILL.md typewriter | Hill-Climb · full-screen curve drawing |
| Scene 5 hero | "21 minutes" serif italic big text | spinning gear ⚙ + "KEPT +1.1" gold tag |

**Judgment standard**: cover the copy and look at visuals only — can you tell which demo this is? If not, it's laziness.

---

### Pattern D · Use real AI-generated assets, not emoji or hand-drawn SVG

**Problem**: 3D orbit / gallery needs asset fragments floating; emoji (📚🎤) is ugly and unbranded, and hand-drawn SVG book spines never look like real books.

**Solution**: run `huashu-gpt-image` to generate one 4×2 grid image (8 theme-related objects · white background · 60px breathing space · unified style), then use `extract_grid.py --mode bbox` to cut out 8 separate transparent PNGs.

**Prompt essentials** (detailed prompt patterns in the `huashu-gpt-image` skill):
- IP anchoring ("1960s Caltech archive aesthetic" / "Hearthstone-style consistent treatment")
- White background (easy to cut out; gray backgrounds feel nicer but make transparent cutouts hard)
- 4×2, not 5×5 (avoids the last-row compression bug)
- Persona finishing ("You are a Wired magazine curator preparing an exhibition photo")

**Anti-pattern**: using emoji as icons, using CSS silhouettes instead of product images.

---

### Pattern E · BGM + SFX dual-track system

**Problem**: animation with no sound at all — viewers subconsciously feel "this thing looks like a cheap demo."

**Solution**: BGM drone + 11 SFX cues.

**Generic SFX cue recipe** (for workflow demos):

| Time point | SFX | Trigger scene |
|---|---|---|
| 0.10s | whoosh | terminal rising from the bottom |
| 3.0s | enter | typewriter done, press enter |
| 4.0s | slide-in | scene 2 elements enter |
| 5-9s × 5 times | sparkle | key process nodes (per generation / per token / per data point) |
| 14s | click | switch to output scene |
| 17.8s | logo-reveal | hero reveal moment |
| typewriter | type | fires every 2 characters (don't make the density too high) |

**Band isolation**: BGM volume 0.32 (low-frequency bed), SFX volume 0.55 (mid-high-frequency punch), sparkle 0.7 (should stand out), logo-reveal 0.85 (the strongest hero moment).

**User control**:
- must have a ▶ start overlay (browser autoplay restriction)
- small mute button in the top-right corner (user can mute anytime)
- don't make it "forced sound as soon as this page is reached"

---

## 2 · Static Dashboard design essentials

The dashboard is Layer 1 of the two-layer structure; a PM can understand the skill without clicking ▶.

**Layout**: 3-column grid (or 1 big + 2 small), each panel solves one problem:

| Panel type | What problem it solves | Example |
|---|---|---|
| **Pipeline / Flow Diagram** | "What is this skill's workflow?" | Nuwa 4-phase pipeline · Darwin autoresearch loop |
| **Snapshot / State** | "What does the real output data look like?" | Darwin 8-dimension rubric snapshot |
| **Trajectory / Evolution** | "How does it change over multiple runs?" | Darwin 5-generation hill-climb curve |
| **Examples / Gallery** | "What has already been produced?" | Nuwa 21-personas gallery |
| **Strip · Example I/O** | "input what → output what" | Nuwa example strip: `› nuwa distill feynman → feynman.skill (21 min)` |

**Key constraints**:
- information density must be sufficient (every panel must carry differentiated information)
- but no data slop (every number must mean something)
- colors consistent with the cinematic (same color family, so switching isn't jarring)

---

## 3 · Debugging and development tools

Any long animation must ship with three dev tools, or debugging explodes.

### Tool 1 · `?seek=N` freeze to the Nth second

```js
const seek = parseFloat(params.get('seek'));
if (!isNaN(seek)) {
  started = true; muted = true;
  frozenT = seek;  // render() uses this t instead of elapsed
  cinema.classList.add('show'); dash.classList.add('hide');
}

// in render():
let t = frozenT !== null ? frozenT : (elapsed % T.DURATION);
```

Usage: `http://.../slide.html?seek=12` jumps straight to the frame at second 12 without waiting to play.

### Tool 2 · `?autoplay=1` skip the ▶ overlay

Convenient for playwright automated screenshot testing, and for forcing startup when embedded in an iframe.

### Tool 3 · Manual REPLAY button

A small button in the top-right corner; users/debuggers can replay as many times as they want. CSS:

```css
.replay{position:absolute;top:18px;right:18px;background:rgba(212,165,116,0.1);
  border:1px solid rgba(212,165,116,0.3);color:#D4A574;
  font-family:monospace;font-size:10px;letter-spacing:.28em;text-transform:uppercase;
  padding:6px 12px;border-radius:1px;cursor:pointer;backdrop-filter:blur(6px);z-index:6}
```

---

## 4 · iframe embedding pitfalls (if the cinematic is embedded in a deck)

### Pitfall 1 · the parent window's click zone intercepts buttons inside the iframe

If the deck index.html adds "left/right 22vw transparent click zones for paging," they will **cover the ▶ play button inside the iframe** — clicking the button gets swallowed into "next page."

**Fix**: give the click zones `top: 12vh; bottom: 25vh` — leave the top and bottom 25% non-intercepting so both the central ▶ and bottom-right ▶ inside the iframe are clickable.

### Pitfall 2 · after the iframe steals focus, keyboard events are lost

After the user clicks inside the iframe, focus is in the iframe and the parent window no longer receives ←/→ keyboard events.

**Fix**:
```js
iframe.addEventListener('load', () => {
  // inject a keyboard forwarder
  const doc = iframe.contentDocument;
  doc.addEventListener('keydown', (e) => {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: e.key, ... }));
  });
  // drag focus back to the parent window after clicking
  doc.addEventListener('click', () => setTimeout(() => window.focus(), 0));
});
```

### Pitfall 3 · file:// vs https:// behavior differences

A cinematic tested locally under file:// may break after deployment, because:
- under file:// the iframe contentDocument is same-origin
- under https:// it's also same-origin (if the same host), but audio autoplay restrictions are stricter

**Fixes**:
- before deploying, run `python3 -m http.server` and test against local HTTP once
- BGM must wait for the user to click ▶ before `bgm.play()`; don't play on page-load immediately

---

## 5 · Anti-pattern quick reference

| ❌ Anti-pattern | ✅ Correct pattern |
|---|---|
| Default = black screen ▶ overlay | Default = static dashboard, ▶ is auxiliary |
| 4 steps in a row on one screen, fade in | 5 full-screen scenes, each focusing on one thing |
| Reusing a template with swapped copy for different demos | Each demo has an independent visual language (distinguishable with copy covered) |
| emoji / hand-drawn SVG as assets | gpt-image-2 big image + extract_grid cutouts |
| No BGM no SFX | BGM + 11 SFX cues dual-track system |
| Scheduling with setTimeout chains | requestAnimationFrame + global timeline T object |
| linear animation | Expo / cubic-bezier easing |
| No dev tools | `?seek=N` + `?autoplay=1` + REPLAY button |
| Buttons inside the iframe swallowed by the parent click zone | click zone gets top/bottom margins to make room for the buttons |

---

## 6 · Time budget

Following this set of patterns, a complete cinematic demo (including dashboard):

| Task | Time |
|---|---|
| Design the 5-scene narrative + visual language | 30 minutes (be deliberate; it determines independence) |
| Dashboard static layout + content | 1 hour |
| Implement the 5 cinematic scenes | 1.5 hours |
| Audio cue timing + replay button | 30 minutes |
| Playwright screenshot validation of 5 key moments | 15 minutes |
| **Single demo total** | **3-4 hours** |

The second demo reuses the framework but **the visual language must be independent**; roughly 2-3 hours.
