# Product UI Showcase Animation Playbook

> **This is the single entry point when "the product being promoted has a UI."** Client work, release films, feature demos — as long as the protagonist of the frame is an interface, read this file before starting.
>
> Core claim in one sentence: **the biggest source of quality in product animation is "real UI + cinematic camera moves", not effects.** Tech feel comes from making the audience recognize "this is that product", from how the camera looks at it — not from particles, glow, or cyber gradients. One real screenshot with one restrained push-in beats ten layers of hand-built fake UI.
>
> Parameter source annotation convention: (shotcraft·card name) = measured values from video-shotcraft shot cards; (huarec) = the Huashu-Design Studio camera-moves directing system; (best-practices §x) (gsap-recipes §x) = this skill's existing references. 30fps context, 1f ≈ 33ms.
>
> Division of labor: this file governs "how the UI as protagonist performs"; camera vocabulary and camera-move motivation live in `camera-language.md`; element-level motion grammar (easing, stagger, FLIP, Chunk Reveal) lives in `animation-best-practices.md` — this file only references, never rewrites.

---

## §0 Two Axioms (override all parameters in the eight forms)

| Axiom | Content | Source |
|---|---|---|
| **Visibility invariant** | At any moment, the cursor and the UI operation in progress must be inside the visible area (including an 8% safety margin). Violating shots should instead reduce their zoom, merge shots, or not be shot | huarec A1 |
| **Visual language grows from the product** | First extract the product's own design tokens (typeface/corner radius/color palette/grid), and the whole film may only reuse or restrain-edly extend them. Shot cards only inherit motion grammar and pacing; the skin is re-skinned per the target product | shotcraft axiom 1 |

---

## §1 Decision Tree: Real UI Screenshot Camera Moves vs HTML-Rebuilt UI

This is the decision in this file that **most affects the workload**; the two paths differ by an order of magnitude. Default to judging from the cheapest path:

```
Product UI needs to appear
 │
 ├─ Does the interface only need to "be looked at" (push-in / tour / hover / compare)?
 │   └─ Yes → [Path One] screenshot in frame + 2.5D camera moves. Stop there, don't rebuild
 │
 ├─ Do only a handful of elements need to move individually (one card floating up, one row of data scrolling)?
 │   └─ Yes → [Path Three] hybrid: screenshot as the base + key elements rebuilt as slices
 │
 └─ Is the interface itself the narrative subject, with elements entering one by one / responding to operations / changing state?
     └─ Yes → [Path Two] HTML rebuild. Use the build-up eight-form ②
```

| Path | Approach | Workload | Applicability criteria |
|---|---|---|---|
| One · Screenshot camera moves | Real screenshot inside a `browser_window.jsx` / `macos_window.jsx` device frame, zoom/rotate/pan on the container | Hours | The interface is "the object being watched"; the audience doesn't need to see changes happen inside the interface |
| Two · HTML rebuild | Pixel-by-pixel rebuild of a movable DOM structure from the screenshot | Days | Elements need independent timelines: progressive generation, typing, state switching, hover responses |
| Three · Hybrid | Full-page screenshot as the base texture; elements that need to move are cut out as transparent slices and animated at their original coordinates | Half a day | 90% of the frame is static, 10% of elements need to be alive. **The right answer for most client work** |

**The key to the hybrid strategy**: after an element finishes animating, it must return to its real slot on the screenshot. If the target card floats above the grid without settling back into the layout, the audience instantly reads "fake" (shotcraft·type-and-filter; the Q9 judgment case nearly caused a full file rewrite over this).

The five steps of the hybrid path:

1. Lay a full-page 2x screenshot as the base, fit it into a device frame (web products use `browser_window.jsx`, desktop apps use `macos_window.jsx`)
2. Cut the elements that need to move out as transparent slices using layout.json coordinates
3. Lay a "page background patch" on the screenshot base at the slice's original position to cover the baked-in original element (the spotlight-hero-card's in-place patch technique: after the card lifts off, lay a background patch in place + an accent-color breathing outline, which brightens and disappears at the moment of landing)
4. Stack the slice on the patch and animate it, ending back at the layout.json slot
5. During the close-up push-in segment, use 4x high-res slices crossfaded for 6f to cover the low-zoom texture (shotcraft·PageCam companion technique)

**Device frame selection**: the frame is the contextual signal of "this is real software"; a bare screenshot floating on the canvas reads like a sticker. But the frame also eats frame area — once a close-up pushes past zoom 2x the frame is out of frame, and you can use a frameless slice directly.

### The asset trio (collect all three before taking Path One/Three)

The standard collection items of shotcraft pipeline stage 1 (shotcraft·six-stage pipeline):

| Asset | Spec | Use |
|---|---|---|
| Full-page 2x screenshot | Device pixel ratio 2 minimum, full-length page captured whole | Base texture; the floor below which pushed-in shots don't blur |
| Element transparent slices | Cut out each element that needs to move individually, 4x is better | The "actors" of the hybrid path; crossfaded for 6f during close-up pushes to cover the low-zoom texture |
| layout.json coordinate table | Each slice's `{x,y,w,h}` in the full-page coordinate system | The "real slot" basis for settling back after animation; the positioning anchor for annotations/highlight frames |

Screenshot sourcing goes through the UI screenshot collection protocol in `brand-asset-protocol.md` (App Store screenshots, official website screenshots, demo video frames, real captures from user accounts), with the same "5-10-2-8" quality bar applying. The cure for blurry text under pushed-in close-ups (CSS `zoom` layout-level scaling replacing transform scale) is in `camera-language.md`.

---

## §2 The Eight UI Showcase Forms · Overview

| # | Form | One-liner | Path | Source card |
|---|---|---|---|---|
| ① | 3D showcase / hero close-up | One card becomes the film's protagonist: spotlight → push-in → hover → settle back | One/Three | spotlight-hero-card |
| ② | Interface build-up | The interface from nothing: skeleton → content → data; appearing is the narrative | Two | skeleton-reveal / row-embed / document-typewriter-reveal |
| ③ | User typing simulation | Human-speed typing, cursor solid-then-blinks | Two/Three | type-and-filter |
| ④ | Cursor operation narrative | Cursor as actor: arcing movement, click ripples, hover linkage | All | type-and-filter / collab-cursor-moves |
| ⑤ | UI state transitions on a timeline | Tab/modal/route switches written as a scene on the timeline | Two | command-palette-summon |
| ⑥ | 3D interface tour | Long interface tilted and gliding past, or the camera touring face-on | One | steep-tilt-glide / graze-face-tour |
| ⑦ | Long-page scroll narrative | Long page fast-scroll hard-brake, stopping at the target row | One/Three | scroll-brake-moves |
| ⑧ | feature callout annotations | Annotation lines growing, highlight frames, explanation cards, before/after comparison | All | before-after-slider-scrub etc. |

Selection discipline: **one shot tells one form, and one form is the protagonist only once per film** (shotcraft axiom 5). The eight forms may appear multiple times in one film, but each occupies its own shots.

---

## §3 The Eight Forms in Detail

### ① 3D showcase / hero close-up

Stand one core object (card/panel/module) up as the product's atomic unit. The shot with the highest texture and the slowest pacing, suited for the "single-protagonist legend" segment right after the opening.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Camera position | rotY 34° dominant + rotX only 8°, perspective 1200px | Side shots beat top-down, "shoot from the left, not from below"; a large rotX turns it into looking at a desktop |
| Push-in | Full-page zoom 0.78 holds one beat, then 16f push to zoom 2.6 | The stillness before the push is "let the audience see the whole first"; pushing straight in has no sense of space |
| Action arc | rise 10f (`cubic-bezier(0.2,1.25,0.3,1)` overshoot) → hover 54f (sin bob amplitude 4px period 40f, translateZ 110px) → reseat 18f landing at press scale 0.997 | Lockdown to landing is about 3.3s; a texture shot must be this slow — the first draft is almost always too fast |
| Contour beam | SVG rounded-rect stroke runs two loops: first loop 14f fast and bright, second loop 20f slow and weak (opacity 0.62) | The two loops must differ in speed to read as "continuous scanning"; one loop reads as a blink; the beam is given to the protagonist only once per film |
| Double shadow | `0 8·lift px …, 0 46·lift px 90·lift px` growing with hover height | If the shadow doesn't grow with height, the hover doesn't hold |
| Spotlight guidance | Wandering light passes 4 intermediate stations then locks on the card center, light pool radius 620→420→360 closing in, +6% pulse at the moment of lock; outer vignette 0.16→0.42 dimming | The intermediate stations make "random illumination" believable; heading straight for the target reads as procedural; the vignette is the other half of the spotlight |
| Floating annotation (optional) | Two lines of serif annotation emerge beside the card, translateZ 92px + bob period 44f (close to the card's 40f but out of sync) | "Empathy" rather than mirrored sync; the annotation must live in the same 3D space under the same camera perspective — flat stacked text breaks spatial unity |

(All of the above are shotcraft·spotlight-hero-card measured values)

Known pitfalls: no "zoom 2.6→2.58" tail-drift at the end; the breathing must be truly still; an opening crowd of multi-card dancing can't carry a first impression — start from a single protagonist + a full action arc; per-card glint was rejected twice in judgment cases, lighting strictly for the protagonist only.

Camera pairing: dolly-in push + a still hold after locking (see `camera-language.md`). When the zoom span is larger than 2x, stretch the duration logarithmically; no spring overshoot (huarec).

### ② Interface build-up

The "from nothing" entrance narrative of an interface. **Build order has grammar**: chrome (window frame/title bar) → skeleton (gray-bar placeholders) → content blocks stagger → data (numbers/charts come alive last). The audience has a free expectation of skeleton screens; the moment gray bars appear they know content is coming.

The three source cards divide labor by object: **one interface** progressively becoming real uses skeleton-reveal; **a set of rows/cards** embedding into a list uses row-embed; **a document** being written out uses document-typewriter-reveal.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Three-stage reveal | Sketch (seed swapped every 5f to "boil") → one-beat switch-to-real with 8f accelerated shrink-back + skeleton spring pop-in → skeleton rows stagger in at 6f → revealed rows stagger at 13f, 12f within a row | The switch-to-real beat must be fast and decisive; dragging it into a crossfade "jump" loses the effect; the three stages must be strictly isomorphic — misalignment reads as a page change |
| Word-by-word entrance | 2.5f/word floating up 14px; the last word of the last row +14f, half a beat late | The half-beat-late is the period of "loading complete"; all landing together is flat |
| Row embedding | Row i cue = 12 + i·9, flying 12f; `perspective(900px) translateY(−120·air) rotateX(16°·air)` | **rotateX flattening to horizontal is the key read of "embedding"**; pure translateY is just "dropping" |
| Embedding accent seam | A 2px accent-color seam on the bottom edge expands from center in 5f, fades out in 8f | Gives each embed a confirmation point, but must fade fast |
| Document block-by-block | Block g cue = 6 + g·3.5, each block wipes 8f; accent-color caret follows only the newest block | **"Block count × beat must first fit the budget" is the core arithmetic**; with too many blocks, cut blocks first, don't speed up; "there is always only one pen tip" — two carets flashing simultaneously means two authors |

(skeleton-reveal / row-embed / document-typewriter-reveal card measured values)

Known pitfalls: when the real-content layer pastes over a product screenshot, measure the skeleton gray-bar row heights and slots against the screenshot, don't lay them out from imagination; the sketch level doesn't draw details — if it looks too much like UI, levels one and two lose their difference; mock copy must not contain real customer/member names.

Camera pairing: the reveal segment pairs with a 1→1.34 gentle push (giving the visual motivation of "leaning in to see clearly"); no lateral camera moves during the whole build — the camera must stay steady while the interface is changing (huarec: no push during full-screen-level changes).

### ③ User typing simulation

Simulate a real person typing in an input field / terminal. This is **completely different from the existing Chunk Reveal (AI streaming output)**: AI output is irregular chunk emergence (best-practices §4.5, gsap-recipes §3.4 — keep using that, not rewritten here); user input is character-by-character, even, with a human hand's hesitation rhythm. Wrong-scenario writing is a frequent accident: making user typing into chunks reads as "the input field generating by itself".

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Typing speed | Body text 3f/char; terminal 2f/char; decorative small text 0.7f/char | "The final value after the first draft was deemed too fast and reworked"; interactive demos follow real human operation speed — this is a judgment-level iron rule |
| Cursor state machine | **Solid** while typing, switches to 8f-period blinking after finishing | Blinking mid-typing reads as lag; the solid→blink switch is itself the "done typing" signal |
| Backspace correction | Occasionally once: over-type 1-2 chars, pause 4-6f, backspace, type it right | "People make typos" is the cheapest realism; but it must be pre-written into the script (frame-deterministic), not random at runtime |
| Confirmation pause | Leave 11f (0.37s) of breathing from finish-typing to page response | Responding instantly after typing reads as machine-automated; the audience can't follow the causality |
| Code typing | Terminal 2f/char; syntax highlighting progressively colors as you type (the current token is colored as soon as it's done), not re-coloring the whole block after finishing | Re-coloring all at once is "paste", not "writing code"; highlighting lagging within half a token is imperceptible to the audience |
| Typing on a screenshot | A background patch covers the baked-in placeholder on the screenshot (keep the icon), the text layer types on top | Stacking text directly doubles over the baked-in placeholder |

(shotcraft·type-and-filter measured values)

The deterministic form of the backspace correction (pre-written script, not runtime drawing lots):

```js
// Compile "typo → pause → backspace → fix" into a character-event table; the timeline is just playback
const script = typeScript("nano-lab", {
  perChar: 3 / 30,                       // 3f/char
  typo: { at: 5, wrong: "0", pauseF: 5 } // at the 5th char, type a wrong "0", pause 5f then backspace
});
// script = [{t:0, text:"n"}, {t:0.1, text:"na"}, ... {t, text:"nano-0"},
//           {t+0.17, text:"nano-"}, {t+0.27, text:"nano-l"}, ...]
// The render layer looks up text by t; bidirectional seek is safe
```

Camera pairing: before typing, the camera first moves up/pushes in to the input field (give the shot first, then the action — the visibility axiom); the camera locks during typing.

### ④ Cursor operation narrative

The cursor is the only "person" in a UI demo. Use `assets/cursor.jsx` (CursorSprite / ClickRipple / hover-linkage hooks, two clock drivers, API in that file's header comment).

Trajectory algorithms aren't rewritten here: Bézier arcs + converging hand-jitter see best-practices §3.5, the GSAP proxy style see gsap-recipes §3.5. This form fills in the **click and linkage parameters**:

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Double-ring ripple | Two concentric rings, **start 3f apart**, radius 14→54 / 14→78px | A single ring is too light to see; the 3f offset is "the ripple of one click", much more and it looks like two clicks |
| Expand/fade decoupled | Expand out-cubic 22f, fade linear 26f | Expand should push, fade should be even; one curve handling both reads as "a flash and gone". Compact scenes can compress to 10f each (the compressed version type-and-filter uses) |
| Click anticipation | Cursor scale 0.85 (power1.in about 3f) → back.out rebound | Anticipation gives the click the weight of "pressing down" (same style as gsap-recipes §3.5) |
| Hover linkage | Cursor enters the target area, target lights up the same frame (brightness +6% or a hairline outline appears), leaves and it retracts | If the target doesn't respond, the cursor is just a sticker; declare linkage windows by trajectory progress, no runtime hit-testing |
| Cursor role split | Operation cursor (clicks carry payloads) vs performance cursor (displacement is the story; named collaborative-cursor duets/ensembles) | Use this form when the cursor needs to click things; purely narrative collaborative cursors are a different scene (shotcraft·collab-cursor-moves); they may coexist in one film but don't mix them |

Quick reference for the two performance-cursor forms (for collaboration/multiplayer themes; parameters from collab-cursor-moves):

| Form | Mechanism | Key parameters |
|---|---|---|
| dialogue-duet | Two named cursors (blue/green) approach in dialogue, orbit around each other in an up/down arc split (R≈270px), nameplates light/dark as the "lighting handoff", green cursor eases-in enlarged tens of times as a transition occlusion | All three Bézier displacements, no linear; same arc same direction on two cursors feels colliding — the up/down arc split is "yielding" |
| cast-ensemble | 5 colored cursors fly in staggered at delay 0/5/9/13/17f with spring, dual-frequency sine drift while resident (0.055/0.021 rad/f, amplitudes ±46/30px), one types a cameo | Nameplates fading in 12f late is "arriving and introducing yourself"; after converging, drift decays to 25% retention — a fully still cursor crowd reads as a freeze |

Known pitfalls: cursor movement must obey the visibility axiom throughout — if the target is off-screen, move the camera first, then the cursor; collaborative cursors' nameplate color = identity code, consistent through the whole film — changing color mid-film makes the audience think the person changed; drifting cursors must never cover the main content being read.

Camera pairing: after a click confirms, the camera pushes 16f (zoom≈2.2) through into the detail page — the standard "click → enter" handoff (type-and-filter); transition connection see `camera-language.md`.

### ⑤ UI state transitions on a timeline

Tab switches, modal pop-ups, page-route pushes. **Timeline-driven playback and an interactive prototype are two different code forms**; translate item by item when changing a prototype into a render draft:

| | Interactive prototype | Timeline playback (for rendering) |
|---|---|---|
| Trigger | `addEventListener('click')` | label / position parameter on the timeline |
| State switch | `classList.add` + CSS transition | Explicit tween (gsap-recipes §6.1 forbidden-zone rule) |
| Open/close | `display: none` switching | `autoAlpha` tween |
| Hover | `:hover` pseudo-class | Linkage windows declared by trajectory progress (form ④) |
| Randomness | `Math.random()` | mulberry32 seeded pre-generation (gsap-recipes §6.4) |

After editing, `grep "addEventListener\|classList\|transition:"` and zero out every hit. State must be a pure function of time — every bug that "looks fine in preview, breaks in render" traces back to this.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| modal / command palette | Background dims in 10f to rgba(20,20,20,0.45) + blur 10px; panel −20px → overshoot +8px (9f) → settle back (6f); candidate rows stagger at i·4f | Without the background dim, the panel has no "floating above"; the 8px overshoot is a "light landing", any more and it becomes a toy |
| tab switch | Indicator bar FLIP-glides (best-practices §4.1), old content fades out 5f sinking 8px, new content fades in 8f floating up | Indicator bar and content out of sync is a cheapness source: bar goes first, content follows half a beat |
| route push | New page pushes in full-width from the right in 12-16f, old page retreats 30% of the distance in the same direction + dims | The old page retreating a short distance (parallax) reads deeper than equal-distance push; equal distance is a "conveyor belt" |

(modal parameters are shotcraft·command-palette-summon measured values)

Known pitfalls: state transitions are the hotbed of "one shot, many effects" — in a single transition the tab switches, a toast pops, data scrolls, and the audience sees nothing; one shot performs exactly one state change.

Camera pairing: the camera must be still at the instant of a state switch, moving only after the switch finishes (huarec inter-shot grammar: changes are attention spending, don't stack spending with camera motion).

### ⑥ 3D interface tour

The shot that shows the "spatial feel" of a long interface / multi-screen interface. The two cards have clear divisions; picking the wrong card is the main accident of this form:

| Card | Mechanism | Suited for |
|---|---|---|
| steep-tilt-glide | **Camera still, page moves**: page tilted rotateY −60°, glides past the frame at its own uniform speed | Page as an "exhibit" parading past; content doesn't need to be read clearly, what's shown is volume and texture |
| graze-face-tour | **Camera moves, page still**: a group of pages floats fixed, the camera tours face-on | Need to see partial content clearly during the tour; the camera has a "visitor" persona |

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Tilt angle | rotateY −60°, live-practice verdict zone 55-65° | −45° was judged "not tilted enough"; beyond −70° content can't be read |
| Float height | 120-180px (graze-face-tour) | Too low hugs the ground with no "display" feel; too high breaks the shadow connection |
| Group stagger | Stagger the starts but overlap the descent in parallel | Fully sequential landing is "queueing for a photo"; overlapping is "a batch arriving" |
| Between-segment connection | Crossfade ≥8f | Hard cuts flash black; the tour is continuous space, no jump cuts allowed |

(shotcraft·steep-tilt-glide / graze-face-tour measured values)

Third variant for multi-page same-screen display (shotcraft·page-waterfall-wall): a 3-column page waterfall wall, rotateX 20° + perspective 1000px, adjacent columns' loop period difference ≥25% (e.g. 12/9/14s) with the middle column reversed. Suited for the closing segment's "the product has many pages" volume statement; content doesn't need to be read clearly. When the period difference is under 25%, the three columns periodically align and the "wall" instantly becomes a "table".

Known pitfalls: the two cards' mechanisms must not be mixed — page and camera moving simultaneously makes the audience lose the frame of reference (dizziness); the tour's page textures must be 2x minimum, tilt-magnification blurs them fastest.

Camera pairing: this form is itself the camera protagonist, so the shots before and after must be still (energy alternation); camera path and orbit vocabulary see `camera-language.md`.

### ⑦ Long-page scroll narrative

The "fast-scroll hard-brake" of a long landing page / document / timeline. Scrolling itself isn't content, **the brake point is**.

| Parameter | Typical value | Tuning feel |
|---|---|---|
| Brake curve | `Easing.out(Easing.exp)` one curve covering the whole distance in 50f | Segmented deceleration "pumps"; a single expo curve is naturally "violently scroll then gradually stop" |
| Motion blur | blur driven by inter-frame displacement difference; fast = blurred, stop = sharp | Constant blur is "a dirty lens"; blur only in the instant of motion, still frames always sharp (same conclusion as huarec) |
| Target-row emphasis | After stopping, target row scale 1.03, the rest dim to 0.38 | Don't dim to 0, context must remain; 1.03 is a "breath", not a "pop" |

(shotcraft·scroll-brake-moves measured values)

Budget management for multiple brake points (huarec comfort budget, moved over directly): interval between adjacent "scroll + brake" events ≥2.6-3.0s; ≤4-5 in any 15s window; each brake point holds ≥1.2s before scrolling again. Brake points are attention spending, more expensive than the scroll itself.

Known pitfalls: no push-in during scrolling — "push-in during scroll causes dizziness" (huarec: no camera moves on full-screen-level changes); when a brake point has no content emphasis (target row not raised, the rest not dimmed), the audience can't tell why it stopped here.

Camera pairing: after a hard brake, one light push-in (1.3x tier) into the target row is allowed, but only after it's completely stopped; tier table see `camera-language.md`.

### ⑧ feature callout annotations

"Point things out" on the real screenshot. Four sub-recipes with a shared principle: **the annotation is a guide, not part of the interface** — its style should separate one layer from the product UI (serif type / handwriting feel / accent color).

| Sub-recipe | Parameters | Tuning feel |
|---|---|---|
| Annotation line growing | SVG path stroke-dashoffset drawing, 12-18f, out-cubic; line first then text, text fades in 5f after the line arrives | Line and text together read as a sticker; the line is the time of "a finger sweeping across" |
| Highlight frame | Target area rounded-rect outline expands in 8f + outer dim 0.3 | Outline without dim doesn't gather the gaze; dimming beyond 0.5 becomes an interrogation lamp |
| Loupe | Circular loupe embedding a 2-3x high-res slice (not CSS-magnified screenshot base), 2px outline + soft shadow, pops in with 8f overshoot, follows the target with a 10-14f gentle move | The loupe must hold a high-res slice; magnifying a blurry texture is self-exposing weak assets; at most one loupe per shot |
| Line-to-explanation card | Explanation card floats in 3D space, translateZ at the 90px order + bob period close to but out of sync with the subject | Same 3D space, same camera; flat stacked text was rejected by judgment cases (same constraint as spotlight-hero-card's floating annotation) |
| before/after slider | Fast flick 12f (out-cubic 8%→76% overshoot rebound to 70%) → stop 18f → slow sweep 48f to a 40% freeze; speed ratio 5:1; after layer clip-path follows the handle; handle velocity-differential-driven scaleX micro-stretch peaking 1.18 | A speed ratio <3:1 makes the pacing contrast imperceptible; the fast flick declares "it changed", the slow sweep proves "where it changed"; stopping the slow sweep at 40% keeps the after in the frozen frame |

(slider is shotcraft·before-after-slider-scrub measured values)

Known pitfalls: the before/after versions must share layout and camera position, otherwise they read as two pages; before must use the real old state (inject old data / disabled features), don't hand-build a "deliberately ugly" fake before; corner badges go in the content area, don't cover the sidebar avatars.

Camera pairing: before the annotation appears, push the camera to the 1.3-1.45x tier so the target area fills the screen (huarec: content occupies 80% of the visible area), and the camera locks during annotations.

---

## §3.9 Placement of the Eight Forms in the Film's Energy Skeleton

A single form is just a shot; the finished film is arranged across the promo-energy-arc's four segments (shotcraft·director-layer trio; the storyboard discipline "carve out hold/rest frame budgets first, then arrange the effects" applies the same way):

| Energy segment | Duration share | Which forms go here | Reason |
|---|---|---|---|
| ① Brand opening | 8-12% | No UI forms | Wordmark holds ≥1s; UI shouldn't fight the opening |
| ② Single-protagonist legend | 12-15% | ① hero close-up or ② build-up | The highest-texture, slowest shot; only one slot in the whole film |
| ③ Feature ramp | 55-65% | ③④⑤⑦⑧ alternating, each shot bound to one unique feature | Medium-low-high energy alternation; ⑧ callout is a good filler for low-energy breathing slots |
| ④ Release finale | 13-16% | ⑥ 3D tour (family-photo variant) | The film's energy peak; multi-screen same-frame display then sign-off |

Sound-hook quick reference (only after visuals are locked; pin frames in relative expressions, shotcraft stage 5):

| Form | What sound to pin |
|---|---|
| ① hero close-up | Pop whoosh-big, beam sparkle, a single snap on reseat — three actions, three dedicated sounds |
| ② build-up | A pop on the switch-to-real beat, one very light tick per revealed row, a soft chime at the half-beat-late last word to close it out |
| ③ typing | Keyboard sounds exactly as long as the typing segment (truncated by character count); short — cut, long — trim |
| ④ click | Click is the loudest sound in the film (the top of the loudness hierarchy); ripples are silent |
| ⑤ state transition | A soft pop on modal pop-up, a whoosh-fast on route push |
| ⑥⑦ tour/scroll | Uniform segments silent or a very light hum, one muffled thud on the hard brake |
| ⑧ callout | Annotation-line growth pairs with a very light draw friction sound; slider fast flick whoosh + rebound tick, slow sweep silent |

---

## §4 Pacing Iron Rules (inherited from shotcraft judgment cases, UI demo specific)

1. **Interactive demos run at real human operation speed.** Typing 3f/char, movement before clicks, breathing before responses. The first draft of an interaction shot is almost always too fast — start writing at human speed (judgment case R3; type-and-filter was reworked for this).
2. **0.5s of stillness after mass motion.** Once the grid converges, the list embeds, the panel settles — the full board still for half a second before the next shot.
3. **Exits must stagger.** Non-target elements fade out staggered at 0.4f intervals by reading order — "disappearing simultaneously reads as a page crash", even a 0.4f difference is enough (type-and-filter).
4. **One shot, one effect.** One shot tells one UI behavior; two effects on one screen compete for attention and the audience sees neither.
5. **True stillness at the end.** No tail-drift in breathing slots or hold frames (zoom micro-changes, opacity micro-adjustments all count); "still" is a designed beat, not a slot that wasn't given an action.

---

## §5 Connection to the Three-Direction Gate / Asset Protocol

**How the three-direction board is produced**: the three directions of product UI animation aren't three visual skins, but **three camera-narrative interpretations of the same UI asset set**. The asset trio is collected once and reused across all three directions. For example, the same product screenshot: Direction A goes through form ① (single-protagonist hero close-up legend), Direction B goes through form ② (build-up telling generative capability from nothing), Direction C goes through forms ⑥+⑦ (tour + scroll narrative telling scale). Each direction board attaches 2-3 keyframe thumbnails, so what the original author picks is "how to tell this interface", not "which image looks better". The three-direction gate is a 100% hard gate; designated style doesn't exempt it either (existing SKILL.md rule).

**UI screenshot sourcing goes through `brand-asset-protocol.md`**: in that protocol, digital-product UI screenshots are first-class citizen assets (extremely high recognition contribution); the collection channels, the 5-10-2-8 quality bar, and brand-spec.md hardening all follow as-is. This file's only increment is one rule: when collecting, execute to the §1 asset-trio spec (2x full page + transparent slices + layout.json), collecting it all at once so both the camera-move and rebuild paths are covered.

**No hand-built fake UI**: when no real screenshot can be found, fall back per the protocol (ask the user for a real capture / official demo video frames), don't make do with a mockup generator, don't draw a "sort of looks right" interface in CSS. We're expressing this product, not "a product".

**There is only one exception**: when going down Path Two HTML rebuild, the rebuild itself is "a replica based on the real screenshot" — it must be checked block by block against the screenshot (typeface, corner radius, spacing, icons all measured from the screenshot), and after the rebuild, compare side-by-side captured frames against the screenshot. A "roughly similar" rebuilt interface hurts more than using the screenshot directly — audiences are extremely sensitive to errors in an interface they use every day.

---

## §6 Pre-Delivery Self-Check (UI demo specific, supplements best-practices §7)

- [ ] Did you go through the §1 decision tree? Didn't rebuild HTML in a scenario where "a screenshot is enough"?
- [ ] Do slice elements return to their real layout.json slots after animating?
- [ ] Are the cursor and operations inside the visible area the whole way (including the 8% margin)?
- [ ] Is user typing the 3f character-by-character rhythm, with only AI output as Chunk Reveal — no mixing the two?
- [ ] Is the cursor solid while typing and only blinking after? Does the click have a double-ring ripple?
- [ ] No leftover addEventListener / classList / CSS transition in state transitions?
- [ ] Do batch exits stagger ≥0.4f, with a full-board 0.5s stillness at the end?
- [ ] Does the whole film use contour light/glint on exactly one shot, given only to the protagonist?
- [ ] Is before/after the same layout and camera position, with before being the real old state?
- [ ] Is the three-direction board three camera interpretations of the same UI asset, not three skins?

---

## §7 Common Failure Modes Quick Reference

| Symptom | Root cause | Which section to return to |
|---|---|---|
| "Not enough tech feel", so particles/glow get added | The direction is wrong; the texture gap is in the real UI and the camera moves | Opening claim + §1 |
| Interface reads like a sticker floating on the canvas | No device frame, no shadow language | §1 device frame + form ① double shadow |
| Text blurs after push-in | Screenshot zoom insufficient or rasterization-resolution problem | §1 asset trio + camera-language.md |
| Interaction "feels scripted, not human" | Typing/clicks/responses all running at machine speed | Forms ③④ + §4 iron rule 1 |
| Preview fine, render breaks | Event-driven state got mixed into the timeline | Form ⑤ comparison table + gsap-recipes §6 |
| Audience says "a bit dizzy" | Camera and page moving at the same time, or brake points over budget | Forms ⑥⑦ + huarec budget |

---

## Appendix · Relation to Other Files

| File | Relation |
|---|---|
| `camera-language.md` | Camera vocabulary, camera-move motivation, camera rig implementation. This file says "which camera to pair with"; that one says "how to do the camera move" |
| `animation-best-practices.md` | The general reference for element-level motion grammar. §3.5 mouse trajectories, §4.1 FLIP, §4.5 Chunk Reveal are referenced by this file |
| `gsap-recipes.md` | The implementation-layer translation. §3.4/§3.5 proxy recipes, §6 seek-safety rules are the execution preconditions for all recipes in this file |
| `brand-asset-protocol.md` | The sourcing protocol for UI screenshots. This file's §1 asset trio is its spec'd extension |
| `assets/cursor.jsx` | The component implementation of form ④, used together with `browser_window.jsx` / `macos_window.jsx` |
| `apple-gallery-showcase.md` | Multi-output same-screen display goes there; single-product UI narrative goes through this file |

