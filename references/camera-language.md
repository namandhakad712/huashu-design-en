# Camera Language · Camera Moves Direction System

> **When to read this file**: before any "camera-level" motion appears on screen — zoom / pan / orbit / parallax /
> transitions / establishing shots and closing credits. As long as what moves is the "camera" and not the "elements", read this first before writing the timeline.
> How elements move (entrance / stagger / physical feel) belongs in `animation-best-practices.md`;
> this file answers **when the camera moves, how much it moves, how long it moves, and how camera shots connect**.
> The runnable GSAP-side implementations (rig containers, PageCam translation, logarithmic-duration helper) are in
> the "Camera Rig Recipes" section of `gsap-recipes.md`; this file only provides design judgment and formulas.
>
> Parameter source annotation convention: **(HuaRec)** = parameter values actually measured in the Huashu-Design Studio camera-moves directing system;
> **(shotcraft)** = the 106-card camera system of video-shotcraft; **(measured)** = real-world practice in this skill's own projects;
> **(inferred)** = borrowed from general cinematic vocabulary, parameters pending calibration.

---

## §0 · Thesis · Camera moves are budget-driven, not effects-driven

Most AI-generated animation treats camera moves as "effects-driven": add a zoom wherever a zoom can be added, the more the camera moves, the more "premium" it looks.
That is the shared source of both motion sickness and cheapness. The correct mental model comes from two axioms (HuaRec):

- **A1 Visibility invariant**: at any moment, what the audience should be looking at must be inside the visible area (including an 8% safety margin).
  Any shot that violates this should instead reduce its zoom, merge shots, or not be shot at all.
- **A2 Comfort budget**: every camera change is an attention expense and must be managed like a budget.
  Once the budget is spent, even a great shot does not get made.

| Budget item | Typical value | Tuning feel |
|---|---|---|
| Interval between adjacent camera changes | ≥2.6-3.0s (restrained tier 5.0s) | Below 2.6s viewers start to feel dizzy; MTV-style fast cutting does not suit product demos (HuaRec) |
| Camera changes within any 15s window | ≤4-5 times (restrained tier 3 times) | If exceeded, cut the shot with the weakest motivation — don't compress the intervals (HuaRec) |
| Push-in zoom floor | 1.25x | Below 1.25x the visual change of a zoom is imperceptible, pure shaking — don't shoot it (establishing 1.06x is the sole exception) (HuaRec) |
| Push-in zoom ceiling | 2.3x (restrained tier 1.8x) | Any higher and pixel density can't hold up; swap the source asset first, then talk about zoom ratio (HuaRec) |
| Shots per minute | Restrained ≤4 shots/min, normal ≤6 shots/min | "Leave room to breathe, not MTV" (HuaRec) |

Two more style axioms on top (shotcraft):

1. **Cinematic feel = camera moves × light and shadow × rhythm × sound, not flashy animation**. Passing on each of the four dimensions beats maxing out a single one.
2. **Pacing preference is one-directional: prefer slow over fast**. All historical user feedback points to "slow down / linger", none points to "speed up".
   When unsure of a duration, pick the longer one; when unsure whether to move the camera, don't move it.

These two are the same root as "yield to the audience" in best-practices §0.2: the camera makes decisions on behalf of the audience's eyes,
and the fewer and more accurate the decisions, the more the audience trusts you.

---

## §1 · Camera Language Glossary · Camera-Move Motivation Decision Table

Ask motivation first for every camera move: **which question does this shot answer for the audience?** If you can't answer, don't move.

| Shot | Motivation (when to give it) | Parameter range | Taboos |
|---|---|---|---|
| **push in** | "Look here next": focus on one specific UI element / data / keyword; rising tension | Zoom ratios 1.3 / 1.45 / 1.8 / 2.3 tiers (see §4); duration follows the logarithmic formula; enter the shot 0.15s early (HuaRec) | Don't push below 1.25x; don't push during full-screen-level changes like scrolling / page switching / video playback ("push-in during scroll causes dizziness"); no camera moves mid-narration (see §6 move on pause) (HuaRec) |
| **pull out** | Revealing the full picture and context: "so it belongs to a larger system"; closing finale | Duration follows the same logarithmic formula; finale pull-out 0.55s + ≥0.8s full-frame pause (HuaRec) | No "out-in-out" pumping: when the gap between shots is smaller than the transition duration, cut straight to the next shot without returning to 1x (see §5) (HuaRec) |
| **pan** | Transfer between two mid-distance focal points (normalized distance 0.22-0.45); sweeping across multiple side-by-side elements in one shot | Only worth panning at combined zoom ≥1.25; diagonal pan uses dual-frequency sine (X/Y frequency ratio 0.22:0.35, amplitude 30-40px) (HuaRec / existing in this skill) | Don't pan between focal points farther than 0.45 (diagonal jump) — drop the shot; pure single-axis pan feels mechanical, prefer diagonal |
| **orbit** | Single-protagonist texture close-up, the shot with the strongest "physicality"; building the hero element's legend | rotY dominant + persp 1100-1200px; measured camera positions rotX46/rotY−30/rotZ9 → rotX42/rotY26/rotZ−7 (shotcraft) | A single technique gets to be the protagonist only once per film (shotcraft); forbidden on information-dense frames (the camera position serves readability — face it head-on when there's lots of text) |
| **dolly zoom** | The reveal moment of "worldview inversion": subject unchanged, context drastically changes | Fake recipe in §8: subject pinned, background scale 1→2.0-2.5 + opacity ≤0.6 (shotcraft) | At most once per film; using it without a narrative drop = pure showing off |
| **static** | Text reading, real-human-speed interaction demos, information-dense shots; the default answer when budget runs low | Brand lockup settles and holds ≥1s; 0.5s of stillness after mass motion finishes; opening subject action arc ≥3s (shotcraft) | None. Staying still is always a legitimate choice — "not giving a shot" is itself a director's decision |

Two horizontal rules:

- **Speed is felt through acceleration, not uniform speed** (shotcraft). Uniform motion reads as a cheap PPT;
  to get a "fast" feel, use a short accelerating segment + a long ease-out, not by halving the whole duration.
- **The camera position serves readability** (shotcraft): information-dense shots face head-on; text close-ups use a lateral horizontal camera position
  (rotY dominant, very small rotX); no global one-size-fits-all tilt; product promo films default to no handheld shake.

---

## §2 · zoom vs dolly Selection · Real 3D Verdict

"Push in" has two implementations with completely different looks — pick first, then write code:

| Dimension | zoom (scale scaling) | dolly (perspective + translateZ forward motion) |
|---|---|---|
| Parallax | None. All layers scale proportionally, the frame reads as "a single image being enlarged" | Present. Near layers move fast, far layers move slow, the frame reads as "the camera advancing through space" |
| Feel | Clean, informational, suits UI close-ups / data focus | Spatial, cinematic, suits hero display / atmosphere segments |
| Cost | Low: a single transform | High: requires layered structure + preserve-3d, plus the rasterization-blur problem (§3.4) |
| Selection rule | Content is flat information (interfaces, documents, charts) → zoom | Content has a clear "foreground / subject / background" hierarchy, and that hierarchy is worth seeing → dolly |

**Real 3D verdict** (resolves the boundary line where two older docs in this skill contradicted each other):

- Elements participating in 3D **≤8** → use real translateZ layering (the golden-angle recipe in best-practices §4.7 applies as-is)
- Elements **≥20** → give up real 3D, fake depth with shadow / blur / brightness differences (the stance of hero-case-study)
- Between 8-20 → ask one question: does this shot need parallax? If yes, go real 3D; if not, fake depth.
  The cost of real 3D isn't in the writing, it's in the tuning: every added layer adds another set of "perspective distortion + text blur + layer interleaving" to debug.

---

## §3 · Camera Rig Implementation Conventions

Camera motion and element animation **must not fight over the same transform**. All camera-level motion is funneled into a dedicated container.

### 3.1 Layered Container Structure

```html
<div id="viewport">          <!-- fixed viewport, overflow: hidden, holds the perspective -->
  <div id="camera">          <!-- camera layer: only carries camera transforms, nothing else -->
    <div id="world">         <!-- world layer: all on-screen content lives here, element animations only move things inside world -->
      ...scene content...
    </div>
  </div>
  <div id="hud">             <!-- captions / corner badges / chrome: sibling of #camera, naturally doesn't follow the camera -->
  </div>
</div>
```

Division-of-labor iron rules:

- Only camera tweens (translate / scale / rotate / zoom properties) appear on `#camera`; element entrances, stagger,
  and hover states are always written on the elements inside `#world`. The two layers know nothing about each other, and the camera can be entirely re-framed at any time without touching element animations
- Captions and chrome **preferably live in `#hud`**, staying still at zero cost; only for annotations that "must follow an element inside world
  but keep constant font size" (like a follow tooltip) do you apply a counter-transform on that element:
  `scale(1/zoom)` cancels out the camera zoom in reverse, updated in sync with the camera every frame
- **transform-origin is the push-in target point**: for a flat zoom, set origin to the target element's center then scale —
  equivalent to "aim the camera at it and push in". In PageCam mode cx/cy take on the same responsibility

### 3.2 PageCam Keyframe Model (shotcraft, 2.5D camera math)

Define the camera state as a keyframe object; camera motion = interpolation between keyframes:

```
{ frame, cx, cy, zoom, rotX, rotY, rotZ, persp }
```

cx/cy is the **point in world coordinates that the camera is aimed at**, zoom is the zoom ratio. Using a 1920×1080 canvas as the example
(swap 960/540 for W/2, H/2 at other sizes):

**Flat mode** (no rotation, pure zoom + pan):

```
transform: translate(960 − cx·zoom, 540 − cy·zoom) scale(zoom)
transform-origin: 0 0
```

**3D mode** (with rotX/rotY/rotZ):

```
outer layer (#camera): perspective: persp·zoom;  perspective-origin: 960px 540px
inner layer (#world):  zoom: {zoom};                        /* note: this is the CSS zoom property, see §3.4 */
                       Tx = 960/zoom − cx;  Ty = 540/zoom − cy
                       transform: translate(Tx, Ty) rotateY() rotateX() rotateZ()
                       transform-origin: cx cy
                       transform-style: preserve-3d
```

Typical camera parameters (shotcraft measured): full-page zoom 0.78 → close-up 2.6;
side shot rotY34 / rotX8 / persp1200 (side shots beat top-down; rotY dominant + just a little rotX);
orbit start/end positions see the table in §1.

### 3.3 Rig Construction Gotchas (camera-specific pitfalls)

- **Pan revealing edges**: `#world` must be larger than the viewport (bleed outward on all sides ≥ max pan amplitude + 8% margin),
  otherwise panning exposes blank space beyond the canvas. This is the mirror side of the A1 visibility axiom: what shouldn't be seen must also be invisible
- **Broken perspective**: any intermediate layer between `#camera` and `#world` with
  `overflow: hidden`, `filter`, or `opacity <1` creates a new stacking context,
  kills preserve-3d, and the 3D layering instantly flattens. In 3D mode, apply filter effects only on the innermost layer
- **Per-frame out-of-bounds fallback** (HuaRec): when the camera focus follows a moving point, check every frame whether the target exits the visible area;
  if it does, hold the zoom ratio and only pull it back to the edge along the out-of-bounds axis with minimal correction. Better the camera "gives way" than the target leaving the frame

### 3.4 CSS zoom Rasterization Technique · Permanently Fix Blurry 3D Text (the most valuable knowledge in the library, shotcraft)

**Problem**: in 3D mode, enlarging with `transform: scale()` makes Chromium rasterize at the element's layout size,
then scales the bitmap up — text inevitably blurs. The higher the zoom, the worse the blur; anything over 2x is undeliverable.

**Solution**: don't enlarge via `transform: scale`, use the **CSS `zoom` property** instead. `zoom` is a layout-level scale —
Chromium re-lays-out and re-rasterizes at the enlarged size, so text stays vector-sharp at any zoom ratio.
The 3D mode formula in §3.2 writes `zoom: {zoom}` on the inner layer instead of `scale({zoom})` precisely for this reason.

Supporting points:

| Point | Approach | Source |
|---|---|---|
| Coordinate compensation | `zoom` changes the layout coordinate system, so translate amounts must be divided by zoom: `Tx = 960/zoom − cx` (already included in the §3.2 formula) | (shotcraft) |
| Relation to the reflow ban | gsap-recipes §6.2 bans tweening layout properties because of integer snap jitter; `zoom` is whole-page scaling, the snap is imperceptible, and the text-sharpness gain far outweighs it. **This technique is the only legal exception to §6.2, used only for the `#world` camera layer** | (measured) |
| Rendering environment | Fully applicable in HyperFrames / Playwright offline per-frame seek rendering: the per-frame re-layout cost doesn't affect the output, only the render time. The live browser preview may drop frames, which is normal — the rendered output is what counts | (shotcraft) |
| Bitmap asset enhancement | Full-page screenshots at 2x sampling; prepare separate 4x single-element screenshots for close-ups, crossfaded over the low-zoom texture for 6f during the push-in | (shotcraft) |
| Depth-of-field atmosphere | DoF is atmosphere only: a top gradient band with blur + mask, no true per-layer depth of field | (shotcraft) |

---

## §4 · Camera Easing and Duration

### 4.1 Easing Vocabulary

| Scenario | easing | Tuning feel |
|---|---|---|
| Active camera move (push in / pull out, with clear start and end points) | `cubic-bezier(0.65,0,0.35,1)` = GSAP `power3.inOut` | Steady at both ends, the feel of "the director gives the shot"; **never linear, never spring overshoot** (HuaRec) |
| Follow camera move (camera chasing an already-started action) | `cubic-bezier(0.33,0,0.15,1)` | Light departure, very long brake, the camera reads as "following along" rather than "cutting over"; the shotcraft camera default |
| Sustained drift (idle drift, uniform cruising) | `sine.inOut` yoyo or `none` | The only scenario where uniform camera speed is allowed (existing rule in gsap-recipes §1); banned for actions with start and end points |
| Cursor / focus follow smoothing | `quickTo` + ~0.15s smoothing; Catmull-Rom path interpolation | The zero-phase idea of forward+backward EMA: follows tightly but without jitter (HuaRec) |

Verdict when the two defaults conflict: single push/pull trusts HuaRec (power3.inOut), compound moves
and multi-segment continuous shots trust shotcraft (0.33,0,0.15,1).

### 4.2 Logarithmic zoom-duration formula (fixed durations are the source of the amateur feel)

All push/pull durations are determined by the zoom-ratio change, so any magnitude of zoom has consistent "visual speed":

```
duration = 0.55 × |ln(zoom₂ / zoom₁)| / ln 2      clamp to [0.30, 0.94] seconds
```

A 1→2x push is exactly 0.55s; 1→1.3x is about 0.30s (hits the floor); 0.78→2.6x hits the ceiling at 0.94s. (HuaRec)
Larger shot-size transitions take longer, smaller ones shorter — guarding against both "one lurch to position" and "dragging".

### 4.3 Zoom Tier Table

| Tier | Zoom ratio | Use case | Tuning feel |
|---|---|---|---|
| Establishing micro-push | 1.06x | Establishing shots only (opening, §6); the audience can't perceive the zoom, only that "the frame feels alive" | The only tier allowed below 1.25x (HuaRec) |
| Light push | 1.3x | Suggestive focus: doesn't interrupt global reading, just "notice this area" | |
| Medium push | 1.45x | Standard UI close-up: one panel / one block of code | |
| Heavy push | 1.8x | Single-element close-up: one button / one number | The ceiling of the restrained tier (HuaRec) |
| Ceiling | 2.3x | Extreme close-up; the source must hold up (2x screenshots / 4x slices, §3.4) | Beyond this, swap the asset, don't force the push (HuaRec) |

Framing formula (HuaRec): `scale = 0.8 / max(target bounding box normalized width, height)`, then clamp into the tier range.
Content occupies 80% of the visible area, leaving 20% breathing room — don't fill the frame.

### 4.4 Pacing Budget (ties into the §0 budget table)

- Interval between adjacent camera changes ≥2.6-3.0s; ≤4-5 per 15s window (HuaRec)
- Enter the shot 0.15s before the action (camera arrives first, action happens after), linger 1.2s after the action finishes before moving on (HuaRec)
- Isolated small actions shorter than 1.2s aren't worth their own shot — guard against "a pump for every click" (HuaRec)

---

## §5 · Inter-Shot Grammar · The Core of Anti-Dizziness

**Dizziness isn't caused by a single shot, it's caused by how shots connect.** The "out-in-out" pump and far-focal-point diagonal jumping
contribute the overwhelming majority of motion-sickness feeling (HuaRec). For two adjacent shots (gap <1.5s), split by focal-point distance into thirds:

| Normalized focal distance | Connection | Notes |
|---|---|---|
| <0.22 (near) | **Merge shots** | Merge into one shot: take the combined bounding box of both targets, recompute the zoom, view it all in one shot |
| 0.22-0.45 (medium) | **Change to a pan** | Prefer a wider zoom (combined zoom ≥1.25), pan across in one shot instead of "out and back in" |
| >0.45 (far / diagonal) | **Drop the shot** | Cut the shot with weaker motivation. **Never film two far focal points back to back** — the diagonal jump is the most dizzying connection |

Two more timing rules (HuaRec):

- **Tight gaps cut straight across**: when the gap between adjacent shots is smaller than the transition duration, don't return to 1.0x — transition directly from the current zoom
  to the next shot's zoom and focal point. Returning to 1x and pushing again is the direct source of the "pump" feel
- **A "pull out and push in again" is only allowed when the gap is ≥1.5s**: the audience has enough time to re-orient in the full frame, only then does out-in not feel dizzy

---

## §6 · Cinematic Opening and Closing · Establishing Shots, Finale, Move on Pause

Three grammar items with minimal cost and noticeably stronger production quality (HuaRec):

1. **Establishing shot**: when the film is >14s long and the first formal shot comes after 7s,
   insert a **1.06x center micro-push** over [0, 3.0s] at the opening: start already in a slight push-in state, ease out and settle back to the full frame within 3 seconds.
   The audience's first feeling is "the camera is alive", not "the PPT started playing"
2. **Full-frame finale iron rule**: pull the final shot's framing in early, leaving 0.55s of pull-out transition + **≥0.8s full-frame pause**.
   The finished film always ends on a still full frame, **never stopping abruptly in a push-in state**. Fully compatible with best-practices' "stop abruptly + hold"
   ending: the held frame must be the full frame
3. **Move on pause**: cut on action, move on pause. In animated films with narration, if a camera move would collide with
   the middle of speech, snap it earlier to the nearest voice-silence point (move at most 0.8s earlier, **only earlier, never later**).
   The audience's cognitive cost of moving their eyes during an auditory gap is lowest. When the voiceover pipeline (voiceover-pipeline.md) schedules shots,
   it takes the narration's sentence-break gaps directly as snap points

---

## §7 · Transition Grammar Table · A Three-Layer Vocabulary

Transitions are an independent layer: pick the seam by **energy drop**, use exactly one style per seam, and transition frames are drawn from the adjacent shots' budgets.
"Universally praised release films have no bare cuts from start to finish" (shotcraft).

### 7.1 The six shot-transition styles (transitions with presence, for seams with large energy drops)

| Style | Suitable energy drop | Parameters | Pitfalls |
|---|---|---|---|
| flash-wash | high→high, strong paragraph shift | White field peaks 2-4f, with 5f of gradient on each side | White flash only covers the cut point, don't reuse it as decoration |
| dip-to-dark | high→low, emotional downtempo | Dim to the rgba(20,20,20,0.9) order, total length ≤0.6s | Don't linger in the dark field, the audience thinks the film is over |
| defocus-handoff | mid→mid, same-level topic switch | Outgoing blur 0→8px overlaps incoming blur 8px→0 for ≥8f | Keep large blur areas ≤24px (DoF performance constraint) |
| title-card | chapter-level separation | Card holds ≥1s, 0.3s transition before and after | ≤2 cards per film; more reads like a slideshow |
| whip-pan | low→high, energy spikes up | Hold ≥20f at both ends → whip 1.5 screens in 8f, peak ≥300px/f to blur convincingly (shotcraft) | Too slow and it's just a pan; if it doesn't blur enough, the shortcoming shows |
| mask-wipe | spatial transfer, "pass through one interface into another" | Mask edge easing `(0.4,0,0.6,1)` (shotcraft) | The mask shape must come from an element already in the frame (window/card rounded corners); a shape out of nowhere is slop |

### 7.2 The three hidden-cut styles (transitions the audience can't tell happened)

| Style | Approach | Source |
|---|---|---|
| flash-cut | A white flash straddles the hard cut point, 5f each side, only covering the cut | (shotcraft, empirically validated parameters) |
| Foreground-occlusion cut | The moment a foreground element (card / panel / cursor hand) sweeps across the full screen, switch scene | (inferred: general cinematic vocabulary, parameters pending measurement) |
| Motion-blur cut | Hard cut on the peak frame of high-speed motion, matching motion direction on both sides, motion blur swallows the cut point | (inferred: general cinematic vocabulary, parameters pending measurement) |

### 7.3 The two travel styles (spatially continuous transitions, no energy drop, the scene is moving)

| Style | Approach | Pitfalls |
|---|---|---|
| Shared-element settle | An element from the previous shot (logo/card) moves continuously to its new position in the next shot, the camera version of the FLIP idea | The element must be the same identity in both shots; too much shape change breaks the "it's the same thing" perception |
| Letterform counter traversal | Push the camera through a large letterform's counter (the void in O/口/0) into the next scene | The counter must be large enough (≥1/3 of screen height); the traversal zoom uses the logarithmic-duration ceiling of 0.94s |

Quick selection: large energy drop → pick one of the six; don't want to be noticed → hidden-cut; two scenes spatially continuous → travel.
Hard cuts aren't forbidden — they just "must be wrapped by one of the layers above".

---

## §8 · Multi-Layer Parallax Recipe · Fake Dolly-Zoom

### 8.1 Parallax Layer Speed Coefficients (shotcraft)

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Layer speed coefficient | Far 0.35 / mid 0.7 / near 1.4 (multiples of camera displacement) | Adjacent layer speed ratios must be **≥2×** to be discernible; a 1.2× difference the audience can't read |
| Layer count | ≤4 layers | Nobody can see parallax beyond 4 layers, pure budget waste |
| Implementation | Each layer multiplies the same camera x/y by its own coefficient and translates | Everything derived from the camera state, seek-safe; don't give each layer its own tween |

### 8.2 Fake dolly-zoom (pure CSS, no real 3D needed)

```
Subject: pinned still (or only a ≤1.02x breath)
Background: scale 1 → 2.0-2.5, while opacity drops to ≤0.6
```

The subject stays, the background surges toward the audience, producing the inversion of "the world approaches while the protagonist is frozen" (shotcraft).
Give it enough duration (≥1.2s); use per §1: at most once per film, saved for the true reveal moment.

---

## §9 · Motion-Derived Signals · blur / Follow / Residual Vibration

The camera's "sense of speed" doesn't come from a faster duration, but from secondary signals **derived** from velocity (shotcraft / HuaRec):

| Signal | Formula | Parameters |
|---|---|---|
| Velocity-driven blur | `v = velocityAt(f)` (central difference: `(pos(f+1)−pos(f−1))/2`), blur intensity ∝ v | Triggers only when zoom speed >0.6/s, intensity `min(10, v×5)`px. **Blur only at the moment of motion; still frames are always sharp** (HuaRec) |
| Lagged follow layer | Follow layer = subject sampled at `f − delay` | Shadow lags 2f, afterimage lags 4f (shotcraft). Afterimage substitutes for motion blur: 5% path lag + blur(6px) + opacity 0.25·(1−t) |
| dampedSettle residual vibration | `e^(−d·t) · sin(2π·f·t)`, f≈0.1, damping≈0.15 | 1-2 tiny residual sways after a camera stops abruptly, amplitude ≤3px; not applied to active camera moves (the §4.1 inOut family), only to whip-pan / hard-brake types |

All three are pure functions of time (difference, delayed sampling, closed-form decay), naturally seek-safe,
satisfying the determinism requirement of gsap-recipes §6.

---

## §10 · Camera-Move Self-Checklist (60 seconds after writing the timeline)

- [ ] Does every camera move answer "which question did it answer for the audience"? Were the unanswerable ones deleted?
- [ ] No zoom below 1.25x (except the establishing 1.06x)?
- [ ] Adjacent shot interval ≥2.6s, ≤4-5 per 15s window?
- [ ] All push/pull durations follow the logarithmic formula, no pulled-from-thin-air fixed durations?
- [ ] Push/pull easing is power3.inOut, no linear / spring overshoot?
- [ ] Were adjacent shots run through the three-way verdict by focal distance (merge / pan / drop)? No two consecutive far-focal-point diagonal jumps?
- [ ] Tight-gap shots cut straight across, no pump from returning to 1x?
- [ ] Film >14s and first shot later than 7s: added the 1.06x establishing micro-push?
- [ ] Ending is a still full frame ≥0.8s, not ending in a push-in state?
- [ ] Has narration: camera moves snapped to speech gaps (only earlier ≤0.8s)?
- [ ] All camera motion funneled into the `#camera` layer, not fighting element animations for the transform?
- [ ] 3D text close-ups went through CSS zoom rasterization, no blurry scale-up?
- [ ] Every transition seam uses exactly one style, no bare cuts in the film?
- [ ] parallax adjacent layer speed ratio ≥2×, ≤4 layers?
- [ ] blur only in motion transients, all still frames sharp?

---

## §11 · Relation to Other References

| reference | Division of labor | Boundary |
|---|---|---|
| `animation-best-practices.md` | How elements move, narrative pacing, taste standards | It governs the "actors", this file governs the "camera"; the "camera pulls out" in the S4 burst segment uses §4 of this file for parameters |
| `gsap-recipes.md` | Runnable GSAP implementations of all rules in this file | "Camera Rig Recipes" section: rig containers, PageCam translation, logarithmic-duration helper, counter-transform |
| `animation-pitfalls.md` | Pitfall checklist | Camera-specific pitfalls (scale blur / broken perspective / pan revealing edges) §3.3-3.4 cover the design side; pitfalls collects the technical-side reproductions |
| `hyperframes-backend.md` | Rendering backend contract | Applicability of the CSS zoom technique under offline per-frame rendering see §3.4 |
| `voiceover-pipeline.md` | Voiceover-driven long videos | The silence-point data for move on pause (§6.3) comes from narration sentence-break gaps |
| `ai-video-review.md` | Finished-film review | The review checklist's transition classification extends per the §7 three-layer vocabulary |

**Call order**: during the director's-notes / storyboard stage read §0-§2 to set the budget and vocabulary → before writing the timeline read §3-§7 to set implementation conventions
and seams → before delivery, run the §10 checklist.

