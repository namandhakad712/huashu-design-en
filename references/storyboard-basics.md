# Storyboard Basics · Lightweight Storyboarding and Shot Composition

> The storyboarding method to use before starting any animation, whether 5 seconds or 50 seconds. Core idea in one line: **every shot is first a moving cover image**.
>
> Method source: the frozen-frame rules (S1-S11) distilled from 300+ cover images in the cover library, the energy-skeleton precedents from the 106 shot cards in video-shotcraft, and the shot-budget axioms from the HuaRec Studio camera-direction system.

---

## 0 · Positioning: division of labor with the launch-film director's notes

This file is the **everyday lightweight version** of `launch-film-director-notes.md`. The 10,000-word launch film director's notes are a heavy process; everyday animations don't need that, but **the storyboarding step itself cannot be skipped** — skipping it results in timeline thinking (what element appears at which second), not visual thinking (what this frame looks like).

| Duration / type | Storyboard requirement | Rationale |
|---|---|---|
| < 20s animation, motion graphic, demo | The **lightweight storyboard card** in this file (§5, one line per shot) | Under 20s doesn't deserve 10,000 words, but each shot's composition must be thought through first |
| ≥ 20s animation | The `导演稿.md` required by the Gate File Protocol, **minimum requirement = the storyboard card format in this file** (§5, all eight fields, not one missing), on top of which you're free to add | SKILL.md "Gate File Protocol" |
| launch film / brand promo / "Apple-level" expectations | Upgrade the storyboard card baseline into 10,000-word director's notes | `launch-film-director-notes.md`; its Part IV 10-field-per-shot format is the heavy version of this file's eight fields |

Trigger boundary: when the user says "quickly make an animation" or "a simple demo," don't dump the 10,000-word process on them, but **still draw the storyboard cards**. The cost of a storyboard card is a dozen-odd minutes; the cost of skipping it is reworking the whole film (2026-07-17 B00 test: skipping visual design and writing code directly — the motion all passed, the visuals got vetoed in one vote).

Relationship to existing files:

- `animation-best-practices.md` governs "how it moves" (timing, easing, motion language); this file governs "what each frame looks like and how shots are ordered" — the two are orthogonal
- The Scene-based narrative in `cinematic-patterns.md` is a prerequisite for this file: scene division comes first, only then do you discuss each scene's frozen frame
- Camera implementation parameters (camera rig, the difference between zoom and dolly, camera easing) → `camera-language.md`; this file only references its vocabulary at the design level

---

## 1 · Core thesis: every shot is first a moving cover image

After 300+ covers for the cover library, one judgment crystallized: **a good cover = 1 concrete protagonist + ≤3 active elements + 1 clear gaze guide**. Design each shot of an animation as a static cover to this standard first, then make it move.

**Cover = frozen storyboard frame**. The test is extremely concrete: pause any random frame of the finished piece, and that frame should be usable directly as a cover. A frame that fails the cover test means the shot's composition wasn't designed — it's just elements moving along their own timelines stacked on top of each other.

Why animation breaks this rule even more easily: animation self-justifies with "elements appear at staggered times" — the previous one hasn't exited before the next enters, so every frame is crowded. Static covers have no such excuse, so the discipline of covers is exactly the discipline animation most lacks (cover library core insight #1).

The order is therefore fixed: **first lay out the frozen frame, then choreograph the motion**. The thumbnail pass in §6 is the executable version of this order.

---

## 2 · The Eleven Laws of the Frozen Frame

The cover library's S1-S11 rules rewritten for the animation context. This is the heart of the file; every shot's composition design is checked against each law one by one.

### Law 1 · Cover test (S1)

Each scene's frozen frame must have: **1 concrete protagonist + ≤3 active elements + 1 clear visual focal point**.

"≤3" is an **invariant per frame**, not a total per scene. When new elements enter, old elements must exit (fade-out, retreat to background, blur+dim all count as exiting); the active-element budget on screen is constant. When writing the timeline, count the on-screen elements at each point in time; if over budget, cut the entrance or exit early.

> Self-check: pause at three random points in time, count the on-screen active elements — does any frame exceed 3?

### Law 2 · The zoom endpoint must be a concrete anchor (S2)

push-in / zoom endpoints can only be: brand logo, a key number, that button in the UI, that line of code, a character's expression. **Background textures, atmosphere elements, and decorative graphics don't deserve a zoom**. Pushing in on something with no information is telling the audience "there's really nothing worth looking at here."

HuaRec precedent adds a cut: **a zoom under 1.25x isn't worth doing** (the visual change is below perception threshold, pure shakiness; the only exception is the opening 1.06x establishing micro-push). When designing the storyboard, write down the anchor for every [CAMERA] push-in; if you can't write an anchor, delete that camera move.

> Self-check: can the endpoint of this shot's push-in be named with a noun (that button / that number / that logo)? If not, cut the camera move.

### Law 3 · Gaze and arrows = the shot's motion script (S3)

The static-cover rule that "the character's gaze points at the subject, one image carries only one arrow" translates to animation as: **the guide line in the frozen frame is the camera-motion instruction for that shot**. The camera follows the gaze, pushes along the arrow, pans along the UI's reading direction.

A scene has only 1 guide line. If you can't find the guide line in the frozen frame, that means this shot has no idea how it should move. Don't invent a camera move at that point — go back and fix the composition (cover library core insight #3).

> Self-check: show the frozen frame to someone for 3 seconds — does their gaze path match the camera motion you planned?

### Law 4 · Text and image division of labor, two tracks (S4 + cover library C series)

The text track and image track are two independent timelines with non-overlapping duties:

| Rule | Content | Source |
|---|---|---|
| Text carries the hook | Hard cap of 2-6 characters per shot's big text; 2-4 characters best for the main copy; text says the hook, the image carries the atmosphere — don't force the image to act out the text | Cover library C1/C3 tests |
| Two-beat entrance | Big text enters on a fixed two-beat rhythm: **action word slams in first, attributive color block fills in after** ("Tested" slams full-screen, then the "Claude 4.8" color block attaches) | Cover library C5 |
| Text lands in negative space | Text always lands in the negative space reserved in the composition — doesn't cover the protagonist, doesn't cover the focal point | Cover library C2 |
| Solid strong color | Decorative text must be solid strong color; **hollow white text with colored outline is absolutely forbidden** | Cover library G restricted zone |

> Self-check: cover the image and leave only the text — is the hook still there? Cover the text and leave only the image — does the composition still hold? Both questions must pass for a clean division of labor.

### Law 5 · Percentage spatial language (S5)

Composition descriptions in storyboard cards must be written at percentage granularity: "product screenshot occupying the top-right 60% with perspective, character at bottom-left 25%, big text pressing against the top edge of the screenshot, 10% safe margin from all four edges."

This isn't ceremony — it's an engineering interface: **percentage language maps directly to CSS/GSAP layout parameters**, so the implementing agent can translate it directly without making composition decisions. Writing "put product on the left, text on the right" is as good as not writing it (gbro composition-template comparison test: prompts at percentage granularity produce a full grade better output than vague descriptions).

> Self-check: does this shot's composition description contain at least 3 percentage numbers? If not, it's still literary description, not a spec.

### Law 6 · Foreground / midground / background = three parallax layers (S6)

When designing the frozen frame, explicitly write out what the foreground / midground / background are and who occludes whom. This layering is natural parallax material: three layers, three speeds, and the changing occlusion relationship is the source of depth.

Implementation parameters copy the shotcraft precedents directly: parallax layer speed coefficients 0.35 / 0.7 / 1.4, **inter-layer speed ratio ≥2x to be distinguishable**, layer count ≤4.

> Self-check: can you say what this frame's foreground / midground / background each are, and who occludes whom? If not, it's not yet layered.

### Law 7 · setup → payoff, opening frame plants suspense (S7)

Each scene's opening frozen frame leaves a gap (an unfinished bridge, a number not yet revealed, half a screen of blank space), and the shot's motion is responsible for closing it. The "from A to B" structure is naturally a transition narrative: the previous shot's payoff can be the next shot's setup.

The anti-pattern is "the opening frame already lays out all the information, then elements just animate in place" — that's a moving poster, not a shot.

> Self-check: place this shot's opening frame and ending frame side by side — can the viewer say "what got fulfilled"?

### Law 8 · Objectification + process-feel when choosing imagery (S8)

Abstract concepts must be objectified into visible physical actions, and **prioritize actions with a sense of process**: "connect" = a bridge assembling segment by segment, "price cut" = the price tag $89 crossed out digit by digit to become $29, "AI-heavy" = the manuscript paper staggering full of tidy gray blocks.

The action itself is the animation script: once the right imagery is chosen, the visual focal point and camera motion grow out of the imagery on their own — no need to invent motion effects separately. The method is to first do a Feynman-style translation (how does this concept "happen"?), and only after translating talk about art style (cover library core insight #4).

> Self-check: can this imagery be summarized with one verb (assemble, cross out, grow, land)? Imagery that can only be described with nouns has no process feel — pick another.

### Law 9 · Style × composition orthogonal (S9)

The cover library's most important architectural insight, migrated as-is: **the style skin is fixed once for the whole film** (color palette, fonts, materials, background logic), **the composition template changes scene by scene** (this shot a centered close-up, next shot a three-column grid, then a diagonal two-zone split).

Scene switch = composition switch, absolutely not style switch. Changing style across the film is a disaster; one composition for the whole film is hypnotic. Link to the three-direction gate: the direction board the user selects is that "fixed once" style skin.

> Self-check: compare any two shots — style (palette / fonts / materials) should show no discernible difference, composition should be clearly different at a glance. If it's reversed, the architecture is wrong.

### Law 10 · Restricted-zone inheritance (S10)

All the cover library's aesthetic restricted zones are inherited, and be especially wary of animation's occupational disease: **glowing particles, data streams, holographic HUDs, cyber-neon are the handiest lazy materials in motion graphics — and they're all in the restricted zone**. Hands itch more when making animation than static images; keep them in check.

The right solution for a tech feel = real UI screenshots (3D floating card form) + clean big text + light background. The deep-blue background #0D1117 + neon glow combination remains forbidden as before (details same as SKILL.md §6.2).

> Self-check: is there any element in the frame that is "glowing"? If so, first suspect you're being lazy with an occupational habit, and argue for keep or remove one by one.

### Law 11 · The 3-meter test (S11)

Pause any frame, and the largest word in the frame must be readable from 3 meters away. **Don't shrink font sizes because "it's going to move anyway"** — viewers give each frame less attention in animation than in static images, so font sizes can only be bigger, not smaller. Together with the visual-density clause in `animation-best-practices.md` §6.5, the two form lower and upper bounds: the density clause prevents emptiness, the 3-meter test prevents sacrificing readability while crowding.

> Self-check: shrink a keyframe screenshot to phone-screen size — can the largest word still be read?

---

## 3 · Shot-Size System: five zoom levels

The traditional film/video five levels — extreme long, long, medium, close-up, extreme close-up — map to five zoom levels in HTML animation (the level values match `camera-language.md` §4.3; for implementation details defer to it):

| Shot size | zoom level | What you see | Typical use | Source |
|---|---|---|---|---|
| Extreme long shot | 0.78x | Whole scene + environment negative space | Opening establishing, closing group shot | shotcraft full-page camera 0.78 |
| Long shot | 1x (establishing micro-push 1.06x) | Complete interface / complete scene | Narrative baseline, home of most shots | HuaRec establishing 1.06x precedent |
| Medium shot | 1.3-1.45x | One functional block | The workhorse level for feature demos | HuaRec light push / medium push level |
| Close-up | 1.8x | Single component / single data point | Emphasizing a specific interaction | HuaRec heavy push level |
| Extreme close-up | 2.3x (upper limit) | Law 2's concrete anchors | Key numbers, that button, the logo | HuaRec magnification cap 2.3x |

Two notes:

- The same level can be implemented with zoom (scale, no parallax) or dolly (perspective + translateZ, with parallax); the feel is completely different. The selection rules for both and the camera rig syntax are in `camera-language.md`; at the storyboard level you only need to write the level and motivation in the [CAMERA] column
- Levels are design vocabulary, not shackles: 1.5x, 2.0x are all legal; the point of levels is to give words like "medium shot" and "close-up" definite numeric meaning in the storyboard table

### Shot-size rhythm between adjacent shots

| Rule | Content | Basis |
|---|---|---|
| Avoid same-level cuts | Two adjacent shots at the same level read as "the image jumped" rather than "we changed shots" — there's no sense of transition; differ by at least one level | HuaRec "magnification <1.25x isn't worth shooting" extended across shots |
| Avoid two-level jumps | Extreme long straight-cut to extreme close-up (0.78x → 2.3x) is dizzying; if you must jump, it has to be a deliberate punch-in paired with a transition (white flash / whip-pan) as cushion | HuaRec comfort budget |
| Focuses close → merge shots | Adjacent shots with very close focus points should be merged into one shot; re-level with the combined bounding box | HuaRec inter-shot grammar |
| Focus at mid distance → pan instead | Rather than the "pull out then push in" pumping, prefer one shot one level wider panning across | HuaRec "change to pan" precedent |
| Focus far apart → drop a shot | Two focal points jumping diagonally across: never shoot two zooms back to back — cut one or insert a long-shot transition | HuaRec "drop shot" precedent |
| Duration scales with magnitude | Transition duration for shot-size changes is not a constant: `duration = 0.55 × |ln(zoomTo/zoomFrom)| / ln2`, clamp [0.30, 0.94]s; a fixed duration is a source of amateurism | HuaRec logarithmic scaling formula |
| Rhythm budget | Interval between adjacent shot-size changes ≥2.6s; within any 15s window, shot-size changes ≤4-5 times | HuaRec comfort budget A2 |
| Curtain-closing law | The finished film always ends on a long shot / extreme long shot, with a ≥0.8s long-shot pause before the end; **never end abruptly in a pushed-in state** | HuaRec curtain-closing precedent |

---

## 4 · Energy Skeleton: carve out the hold budget first, then arrange the motion effects

Multi-shot films (≥10s) don't distribute shots evenly; apply shotcraft's promo-energy-arc four-phase skeleton:

| Phase | Duration share | Energy | Content | Hard metric |
|---|---|---|---|---|
| ① Opening | 8-12% | Low | Brand / theme reveal | Wordmark settled hold ≥1s |
| ② Single protagonist portrait | 12-15% | Low-medium · slowest in the film | One complete action arc for the protagonist (enter → hover → settle) | Action arc ≥3s, the segment with the highest production quality |
| ③ Feature ramp | 55-65% | Medium-high ⇄ low alternating | Each shot ties to one unique feature, energy alternating high and low | After every 1-2 feature shots, insert a **breathing text card** (low energy, large negative space, 2-6 characters) |
| ④ Closing | 13-16% | Peak of the film | Group shot + sign-off | Closing hold; curtain returns to long shot (§3 law) |

**Scheduling discipline: carve out the hold / rest frame budget first, then arrange the motion effects** (shotcraft fill-in-the-blank process precedent). Specific order:

1. List the feature inventory, count the number of shots N
2. First carve the inviolable static time out of the total budget: wordmark hold ≥1s, batch motion-effects tail 0.5s static, opening action arc ≥3s, ending ≥0.8s long-shot pause, 0.5s hover before a key result (best-practices §4.4)
3. Only the remaining time goes to motion effects, arranged high-low alternating — no two consecutive high-energy shots
4. Pick a transition for each seam (§7); transition frames are carved from the adjacent shots' budgets, not added on top

The breathing text card's composition also has a fixed form: 2-6 characters of big text + full-screen negative space + zero decoration. It is itself a frozen frame that passes the cover test (active elements = 1), and its job is to lower the energy of the feature-ramp segment and give the viewer time to digest. Don't turn the breathing text card into yet another information shot — that's as good as not inserting one.

Relationship to the five-act narrative in `animation-best-practices.md` §1: Slow-Fast-Boom-Stop is the rhythm curve for **a single scene / short piece** (≤15s in one breath); promo-energy-arc is the skeleton for **multi-shot films**; under 15s pick either, over 20s use the energy skeleton to order shots, and inside each shot use the feel of the five-act narrative.

---

## 5 · Lightweight Storyboard Card: this file's deliverable

One line per shot, all eight fields, not one missing. shotcraft's four-column table (#|time|shot|key motion) is the minimum config; here it's expanded to eight columns, with [CAMERA] as its own column (the launch film director's notes' 10 fields will subsequently be expanded to 11 — this field is the addition):

```
| # | time | shot size | [CAMERA] move + motivation | composition (percentage language) | key motion | transition to next shot | acceptance frame numbers |
```

Field writing requirements:

- **Time**: start-end seconds + implied duration; transition time is included in this shot's budget, not listed separately (§4 scheduling discipline item 4)
- **Shot size**: one of §3's five levels + zoom value
- **[CAMERA]**: camera move + one sentence of motivation; "static" is also a legal camera move, but write why it's static; every push-in must write its anchor (Law 2)
- **Composition**: percentage language (Law 5), including foreground/midground/background layering (Law 6)
- **Key motion**: this shot talks about only one motion effect (shotcraft "one shot one motion" precedent)
- **Transition to next shot**: pick from §7's decision table; never leave it blank, never write "direct cut" (a bare cut is only legal as a deliberate hidden-cut)
- **Acceptance frame numbers**: **pre-write 1-2 frame numbers per shot**; after implementation, capture exactly these frames for self-check (shotcraft "three reads per shot + pre-written acceptance frame numbers" precedent). The meaning of pre-writing: acceptance criteria are fixed before you start, leaving no fuzzy "it looks fine" space after implementation

### Example: complete 12s product animation storyboard table

Imaginary product: PicSort, a screenshot-organization tool. 1920×1080 · 30fps · 360 frames.

| # | Time | Shot size | [CAMERA] move + motivation | Composition (percentage language) | Key motion | Transition to next shot | Acceptance frames |
|---|---|---|---|---|---|---|---|
| 1 | 0-2.0s | Long shot 1x | Static; last 0.3s light push to 1.06x · establishing + planting suspense | Messy screenshot pile occupying center 70%, big text "3000 screenshots" landing in top 20% negative space, 10% safe margin from all four edges; foreground 2 screenshots slightly occluding the midground pile | Screenshots 30ms stagger landing on the desktop; big text two-beat entrance ("3000" slams in, "screenshots" color block fills in after) | Defocus relay (the messy pile blurs open) | f30 / f55 |
| 2 | 2.0-3.5s | Extreme close-up 2.3x | push-in 1x→2.3x · anchor = the date corner-tag at the bottom-right of a screenshot | Single screenshot occupying 80% centered with 2° perspective, date corner-tag at bottom-right 15%; remaining screenshots retreat to background blur | Push-in with background blur+dim in sync (focal-switch triple combo) | Shared element settles (this screenshot shrinks and flies into the next shot beside the input box) | f85 |
| 3 | 3.5-6.0s | Medium shot 1.4x | Horizontal pan following the cursor · guide line = the cursor's arc trajectory | Product UI occupying 85% with perspective, logo at top-left 10%, search box horizontally centered occupying 55%; cursor arcs in from bottom-left 25% | Typing 3f/character + Chunk Reveal on results; breathing 0.4s after typing completes | mask-wipe (the result panel's edge unfolds into the next shot's grid) | f130 / f165 |
| 4 | 6.0-8.5s | Long shot 1x | pull-out 1.4x→1x · motivation = showing the scale after organizing | 3-column category grid occupying 85%, each column header a color tag; top 15% negative space reserved for the next shot's numbers | Cards stagger into columns (30ms between columns), 0.5s static after full board | Flowing whitespace | f210 / f250 |
| 5 | 8.5-10.5s | Close-up 1.8x | Static · key result hold, don't steal the numbers' scene | "3000 → 12 categories" occupying center 60%, action word largest, attributive color block; large negative space around | digit-roll settling (tabular-nums), 0.6s hold after settling | Shared element settles (numbers shrink and rise to make way for the logo) | f290 |
| 6 | 10.5-12s | Long shot 1x | Static · curtain closing, ending on a long shot | Logo centered occupying 12%, one-line slogan below at 8%, rest all blank | Logo morph-closure (previous element collapses → expands), final frame hold ≥1s | None (end of film) | f330 / f359 |

Cross-checking this table reveals the skeleton: shot 1 is the suspense-planting setup (Law 7), shots 2-4 are the feature-ramp's shot-size alternation (extreme close-up → medium → long, no same-level cuts, no two-level jumps), shot 5 is the energy peak + hold budget, shot 6 is the long-shot curtain closing. Every shot has ≤3 on-screen active elements.

---

## 6 · Thumbnail Pass: gray-box validation before writing real code

The storyboard table is text; the thumbnail pass turns it into a visible composition check. Cost: within half an hour, an insurance policy on rework costs.

**Step 1 · Build the gray-box HTML**: a temporary HTML with one 1920×1080 `<section>` per keyframe. Lay out the composition with only solid color blocks + text labels: the protagonist as one dark gray block labeled "product UI 85%", the text area as a color block labeled "big text: 3000 screenshots", foreground elements as light gray blocks. No motion effects, no fonts, no color — just turning the storyboard's percentage language into visible blocks.

Beautification is forbidden in the gray-box phase (no font selection, color picking, or shadows): beauty is already settled by the direction board; the gray box validates only composition and rhythm. Starting to beautify = starting to avoid the composition problem.

**Step 2 · Do only 3-5 keyframes**: not every shot — pick the energy skeleton's key nodes: the opening setup frame, the hero frame of the portrait segment, one representative frame of the ramp segment, the peak frame, the curtain-closing frame.

**Step 3 · Playwright batch screenshots**:

```bash
for i in 1 2 3 4 5; do
  npx -y playwright screenshot "file://$PWD/thumbnails.html#f$i" \
    "thumbs/f$i.png" --viewport-size=1920,1080
done
```

**Step 4 · The three acceptance questions** (asked against the side-by-side thumbnails):

1. **With all text labels covered, can you still tell the composition differs across the 5 images?** If not, the rhythm didn't come through — the per-scene composition-template switching wasn't executed (Law 9; same origin as the thumbnail self-check in best-practices §1)
2. **Does each image pass the cover test on its own?** (Law 1: 1 protagonist + ≤3 elements + 1 focal point)
3. **Can you point out the guide line in each image?** For any you can't, go back and fix the composition — don't move forward (Law 3)

**Step 5 · Only after passing, write the real code.** Keep the gray-box HTML in the project directory as the composition baseline; when the implementation drifts, come back and compare against it.

**Relationship to the three-direction gate**: the three-direction hard gate's "direction board" (real hero keyframe still + color palette + character sentence) is essentially the **first thumbnail**. After the user picks a direction, the thumbnail pass is what expands that one board into the film's keyframe sequence: the direction board fixes the style skin, the thumbnail pass fixes per-shot composition — exactly Law 9's two orthogonal layers.

---

## 7 · Transition Decision Table: pick by narrative relationship

Transitions aren't decoration; they're the narrative logic at the seam. First determine the **narrative relationship** between the two adjacent shots, then pick the type. Implementation parameters for the transition vocabulary (duration, easing, mask syntax) are in `camera-language.md` §7's three-layer transition vocabulary.

| Narrative relationship between adjacent shots | First-choice transition | Alternative | Precedent basis |
|---|---|---|---|
| Time jump ("three days later" / "after organizing is complete") | Black-screen text card / flowing whitespace | whip-pan | shotcraft six forms: big contrast cushioned with white / black |
| Spatial pan (different regions of the same interface) | **One shot panning across, no cut at all** | hidden-cut | HuaRec "mid-distance change to pan": rather do one shot one level wider, no out-in pumping |
| Concept comparison (before/after, A vs B) | mask-wipe | Split-screen hard cut + white flash | shotcraft mask-wipe through-window precedent |
| Progression / causality (the answer to the setup is in the next shot) | Shared element settles (previous shot's element flies into being the next shot's protagonist) | morph | shotcraft travel two forms; same origin as the voiceover-pipeline iron law "hero morphs across scenes, no cut" |
| Large energy gap (breathing text card → high-energy shot) | Flowing whitespace / white-flash FlashCut | whip-pan | shotcraft: pick by energy gap at the seam |
| Small energy gap (adjacent feature shots in the ramp) | Defocus relay / cross-fade ≥8f | hidden-cut | shotcraft graze-face-tour "cross-fade between segments to prevent black flashing" |

Three disciplines:

1. **One seam uses one form only** — no stacking (white flash + whip-pan together is slop)
2. **Transition frames are carved from the adjacent shots' budgets** — no time added out of thin air; the storyboard table's time column already includes transitions
3. **Zero bare cuts in the whole film**. shotcraft precedent, verbatim: acclaimed released films never contain a single bare cut. If you want the "cut" feel, use a hidden-cut (hiding the cut point behind a full-screen element / white frame / motion peak) — that's a designed cut, not an undesigned one

Narrated films get one more rule: **move on pause** (HuaRec precedent). Shot changes and transitions snap to the gaps in speech, only earlier never later, upper limit 0.8s, because the viewer's cognitive cost of moving their gaze during an auditory gap is lowest. When running the voiceover pipeline, use the real gaps in timeline.json to set cut points.

---

## 8 · Pre-work Checklist (the definition of "storyboard done")

Before writing code, confirm all of the following exist:

- [ ] Storyboard table: one line per shot, all eight fields complete, saved in the project directory (the core section of `导演稿.md` for ≥20s)
- [ ] Every shot's frozen frame passed the applicable laws of the eleven; at minimum explicitly check Law 1 (cover test), Law 3 (guide line), Law 5 (percentage composition)
- [ ] The shot-size column has no same-level consecutive cuts, no two-level jumps (§3)
- [ ] The hold / rest budget was carved out first, breathing text cards inserted (§4)
- [ ] A transition type is written into the table for every seam; zero bare cuts in the film (§7)
- [ ] The 3-5 gray-box screenshots from the thumbnail pass passed the three acceptance questions (§6)
- [ ] Acceptance frame numbers pre-written for every shot, to be checked frame by frame after implementation (§5)

All seven items pass → the storyboard phase ends, enter implementation. When an implementation gets vetoed, first locate by layer: is it a motion-skeleton problem or a visual-craft problem (the best-practices §6.5 repair pattern); the storyboard table itself usually doesn't need rewriting.

---

*Written: 2026-07-23 · Sources: cover library S1-S11 frozen-frame rules + video-shotcraft energy skeleton precedents + HuaRec camera budget axioms*
*Sibling files: `camera-language.md` (camera implementation layer) · `launch-film-director-notes.md` (heavy version)*
