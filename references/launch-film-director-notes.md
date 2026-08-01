# Launch Film Workflow: Write 10,000-Word Director's Notes First, Then Make the Animation

> The standard workflow for high-spec visual work (≥ 20 seconds, includes brand narrative, includes slogan reveal, may be promoted on X / WeChat / Bilibili).
>
> Trigger conditions: the task is a "product upgrade promo / brand launch film / launch trailer / superbowl-tier ad / brand campaign / hero animation video", and **the user has clear expectations for quality** (such as "Super Bowl quality" "10x detail" "Apple-level").
>
> Anti-trigger: don't use this workflow for "quick animation demo" "simple motion graphic" "single icon animation" — it will be over-engineered.

---

## 1. Why Write the Director's Notes First

Practical lesson (huashu-md-html v2.0 project, 2026-05-11):

In the first round, we went straight to writing HTML and produced a "programmer-perspective animation" — each capability got equal effort, the rhythm was uniform, the slogans collided, and there was no narrative arc.
In the second round, following the user's instruction to "stop, first write a 10,000-word shot-by-shot script from an Apple director's perspective," we wrote v5-director-notes.md (11,500 characters, 13 shots of shot-by-shot spec), then implemented against the script — passed in one go, every pause frame held up, and the rhythm had a real climax.

**The core difference**: writing the script is think; writing HTML is execute. Once you've thought it through, execution is mechanical translation. If you execute first, every shot is an on-the-spot decision, and chaos is inevitable.

Writing the director's notes isn't "putting on airs" — it's sedimenting every visual decision into a document **before touching the code** — every shot has already been visualized in the head, reasoned through, and traced against context. During HTML implementation you no longer need to make creative decisions; you only need to translate faithfully.

---

## 2. Trigger Judgment (Ask Yourself 3 Questions First)

Before starting the launch film workflow, ask:

1. **Does this film carry brand narrative?** (a thesis / slogan reveal / upgrade ritual feel) — yes → go through the director's notes workflow
2. **Will the audience pause to look at it?** (might screenshot, make an X poster, make a cover, slow review) — yes → every frame must hold up
3. **Does the client/user have a "I want it to be like XXX" reference?** (Apple / Anthropic / Nike / Penguin / a specific director) — yes → the visual context must be made explicit

If any is "yes," go through the workflow. If all three are "no," skip it and just use the standard workflow in [animations.md](animations.md).

> 🔴 **Front gate (prior to this workflow)**: launch films must also pass SKILL.md's three-direction hard gate first — one "direction board" per direction (a real still frame of the hero keyframe + color palette + character sentence + references). Only after the user picks a direction do the 10,000-word director's notes unfold around the chosen direction. Style keywords like "Apple-level" do not grant an exemption (confirmed in the HuaStudio practice, 2026-07-18).

---

## 3. The 5-Part Structure of the Director's Notes

The 10,000-word (10000-12000 Chinese characters / equivalent English) director's notes must contain these 5 parts. **Missing any part counts as incomplete, and quality will suffer**.

### Part I · Director's Statement (creative thesis, ~1500-2000 words)

Answer 5 questions:

1. **What is this film NOT?** (explicit exclusions — e.g. "this is not a feature showcase" "not a demo")
2. **The core thesis in one line** — when the audience leaves, which single sentence do they remember?
3. **Whose context are we in dialogue with?** — list 5-8 visual references (director / designer / brand / photographer / work title + year), and say what was learned from each
4. **Three audience profiles + a commitment to each**: primary audience / secondary audience / outer audience, one paragraph each
5. **Rhythm philosophy** — a description of the slow-beat / acceleration / peak / gentle-close curve, and which second the emotional climax lands on (**not necessarily the last second**)

End with an anti-slop checklist: **what this film will not do** (listed concretely, not vaguely).

### Part II · Visual System (full-spectrum visual spec, ~1500-2500 words)

This is the engineered visual spec. Once complete, any executor handed it can produce consistent visuals.

Required subsections:

- **Complete color palette**: at least 8-10 colors, each with HEX + functional definition + maximum share of frame
- **Typography system**: at least 6 font-size levels, each with font name + weight + size + letter-spacing + usage
- **Grid system**: canvas size + outer margins + column grid + baseline grid + key safe zones + golden-ratio anchors
- **Animation system**: easing library (no more than 4) + duration dictionary + stagger rules + scene transition rules
- **Chrome elements**: small details threaded through the whole film (counter / chip / ticker / watermark / texture), each with position + entry/exit timing
- **Audio system**: 30-second BGM direction curve (layered) + SFX dictionary (10+ cues with timecode + volume + frequency-band isolation)
- **Anti-AI slop checklist**: a per-shot self-check table (10-15 items)

Iron law: **derive every visual decision from the Visual System; don't invent new values on the fly in the shot list**.

### Part III · Story Arc (narrative arc, ~500-800 words)

Three-act structure + emotion curve:

- **Act I · SETUP** (0 → first 1/5 of the runtime, e.g. 0-6s for a 30s film): the audience enters, the problem is posed
- **Act II · ESCALATION** (middle 2/3): the answer unfolds, the theme develops
- **Act III · PAYOFF** (final 1/4): transcendence, slogan reveal, brand stamp

Include an ASCII emotion-curve diagram + the emotional climax moment marker.

**Key decision**: the climax doesn't have to be at the end. For a 30s film, the climax usually lands at 22-25s (not 29s) — the final few seconds are resolution / decay, not the peak. Violating this rule invariably makes the work "strong start, weak ending."

### Part IV · Shot-by-Shot Storyboard (shot script, ~5000-7000 words · 60% of the length)

Each shot contains 11 fields (all required):

```
SHOT NN · NAME
[TIMECODE]    start/end time + duration
[FUNCTION]    this shot's function in the story arc (one sentence)
[VISUAL]      frame composition + element positions + motion direction
[CAMERA]      shot scale (extreme-wide/wide/medium/close/close-up, mapped to zoom steps) + camera move + one sentence of motivation; write why "static" is static too; push-ins must specify a concrete anchor (vocabulary and budget in camera-language.md; shot-scale system in storyboard-basics.md §3)
[TYPE]        typography spec (font / size / letter-spacing / line-height / color / alignment)
[ANIM]        each element's in/out timing + easing + duration + stagger + delay
[AUDIO]       music beat + SFX cue (each shot's BGM rhythm + required SFX schedule)
[CHROME]      corner-element states (which chrome is on / which fade in/out / which pulses)
[ANTI-SLOP]   which self-check items this shot passes + what 120% detail signature it has
[WHY]         the logic carrying over from the previous shot + the hook advancing the next shot
```

**Fields average 30-80 words → 400-700 words per shot → 12-15 shots → 5000-7000 words**.

Practical experience: after finishing the storyboard, **read it once** — if you delete any single shot, does the whole film still hold up? If it can be deleted, that shot is redundant; delete it.

### Part V · Production Manifest (build checklist, ~800-1200 words)

Engineering delivery checklist:

- Font loading URLs (with preconnect)
- CSS variables (directly pasteable)
- BGM sourcing criteria + Suno/Udio prompt keywords + backup libraries
- SFX dictionary (per-cue file paths + volumes, listed by timecode)
- **Keyframe verification plan**: timecodes for 12-15 pause-and-check keyframes, with the verification items for each frame listed (fonts / positions / chrome state)
- Recording parameters (fps / codec / bitrate / preset)
- ffmpeg audio mixing command (with audio stream verification)
- Deliverables list (mp4 / mp4-60fps / gif / poster.png / silent.mp4 / shot-list.csv)
- Full-pipeline time estimate (hour-level precision)

---

## 4. 5 Tips for Writing the Director's Notes

**4.1 Speak in the director's voice, not the PM's voice**

❌ "This shot displays the product features."
✅ "This is the hero shot — if the audience pauses anywhere, I want it to be here."

Director's notes are read by the executor, but also by your future self. First-person + judgment expression preserves more decision traces than descriptive expression.

**4.2 Cite specific works (with years), not just genre names**

❌ "Apple-inspired"
✅ "Apple 'Designed by Apple in California' (2013, dir. Mark Romanek) — what I'm learning is the slow beats + serif + big white canvas"

Citing specific works has these benefits: (a) any viewer can look it up online to compare (b) you force yourself to think through exactly which concrete technique you're borrowing (c) it prevents "vague inspiration."

**4.3 Trace every decision back to a first principle**

The whole film has one first principle (e.g. "Markdown is the new typewriter."). Every concrete decision — palette / type / rhythm / chrome — must be traceable back to that sentence.

Decisions that can't be traced are decoration; delete them.

**4.4 Writing anti-slop matters more than writing do-this**

A "what this film will not do" list (purple gradients / emoji / Lorem ipsum / Inter display / SVG-drawn people / rounded cards + left border accent) protects quality more than a "what this film does" list.

Positive decisions are infinite; the negative checklist is finite — but once the negative checklist is violated, it's slop.

**4.5 Don't implement immediately after writing — re-read it 30 minutes later**

While writing, your brain is in "production mode" and can't see inconsistencies. Reading your own storyboard 30 minutes later will reveal:
- Two shots with redundant functions (delete one)
- A shot with too big a narrative jump (add a transition)
- An emotional climax in the wrong place (move it)
- Chrome elements mismatched with shot count (realign)

Those 30 minutes save 2 hours of rework later.

---

## 5. Director's Notes → HTML Implementation Workflow

After finishing the director's notes, the HTML implementation steps:

1. **Reuse starter components** (`assets/animations.jsx`'s Stage/Sprite/Easing/interpolate) — don't reinvent
2. **Paste CSS variables directly from Part II of the Visual System** — don't change colors ad hoc in the HTML
3. **Map the Sprite start/end timeline against the Part IV timecodes** — don't add shots on your own
4. **Extract chrome elements into independent components** (ChromeA/B/C/D), driven by useTime() for state switching
5. **Destination card content must be genuinely readable** (not fake bar lines) — this is the 120% detail signature most repeatedly cited in the v5 project
6. **Screenshot keyframes for verification immediately after finishing each shot** (via the `?t=NN` URL parameter + Playwright) — don't write the whole film first and verify all at once

---

## 6. Keyframe Verification Workflow

URL parameter implementation (must be added to the Stage component):

```js
const urlMatch = window.location.search.match(/[?&]t=([\d.]+)/);
const frozenTime = urlMatch ? parseFloat(urlMatch[1]) : null;
const [time, setTime] = useState(frozenTime != null ? frozenTime : 0);
const [playing, setPlaying] = useState(frozenTime == null);
```

→ Then `file:///path/animation.html?t=14.5` freezes directly at 14.5 seconds.

Batch screenshots:

```bash
for t in 0.5 2.5 4.9 7.0 10.5 13.5 16.5 19.0 21.5 23.4 25.5 28.0 29.9; do
  npx -y playwright screenshot \
    "file://$PWD/animation.html?t=$t" \
    "keyframes/t-$t.png" \
    --viewport-size=1920,1136 \
    --wait-for-timeout=2500
done
```

Every screenshot must be verified:
- [ ] Elements don't overflow the 1920×1080 canvas
- [ ] Letter-spacing and line-height are visually correct (not cramped, not scattered)
- [ ] Key typography details (period color / em-dash / italic / small caps) are recognizable
- [ ] Chrome element positions + states are correct
- [ ] The anti-AI slop checklist passes
- [ ] The 120% details worth seeing "when paused" exist

---

## 7. Multi-Perspective Parallel Strategy (advanced)

For complex projects (e.g. a launch film where you can't settle on a direction / you want to see several aesthetic differences / the client hasn't committed to a style) you can **launch multiple subagents in parallel to produce versions from different director perspectives**.

Production configuration (huashu-md-html project, 2026-05-11, 6 versions in parallel):

```
v5  · baseline (Anthropic / Penguin Classics publishing-house taste)
v5a · Wes Anderson (symmetry + vintage + chapter cards)
v5b · Saul Bass (paper-cut + 60s big type + geometric cuts)
v5c · Wong Kar-wai (Chinese serif + slow motion + nostalgia)
v5d · Massimo Vignelli (modernist grid + red and black)
v5e · Kenya Hara 原研哉 (minimalist Japanese + whitespace)
v5f · Yayoi Kusama 草間彌生 (polka dots + repetition + a single strong color)
```

Each subagent receives an independent brief:
- Project background (the same one)
- Required reading (the same v5-director-notes.md as a methodology template)
- **The specified artist DNA** (palette / type / visual language / rhythm / signature elements / reinforced anti-slop version, 30-50 words each)
- A unified task list (director-notes.md + animation.html + keyframes/ + README.md)
- Unified constraints (30s / 1920×1080 / file:// / Google Fonts)

Launch in parallel and run in the background; ~30-60 minutes later you get 6 complete versions.

When done, review and compare:
1. A table of each version's core aesthetic decisions
2. Side-by-side keyframe comparison (one frame at the same moment from each version)
3. Vote: which one best fits the user's actual needs

**Key**: don't let subagents reference each other — they must produce independently, or they'll all collapse into the "average." Each subagent's instructions should explicitly say "don't repeat v5's aesthetic."

---

## 8. Typical Scenarios That Trigger This Workflow

| User scenario | Triggers? | Notes |
|---------|---------|------|
| "Make a SaaS upgrade promo" | ✅ Triggers | Full workflow by default |
| "An Apple-level / Super Bowl quality video" | ✅ Triggers + upgrade | Strongly recommend multi-perspective parallel |
| "A 30-second brand launch film" | ✅ Triggers | |
| "Write a 10,000-word script for this project, then animate it" | ✅ Triggers | The user said so explicitly |
| "A simple motion graphic, rotate the logo" | ❌ Does not trigger | Use the animations.md standard workflow |
| "Make an onboarding animation demo" | ❌ Does not trigger | Use animations.md |
| "A tutorial video with voiceover" | ❌ Does not trigger | Go through voiceover-pipeline.md |
| "A single hero animation" | ⚠️ Depends on complexity | If it's high-spec hero, trigger; a regular hero uses hero-animation-case-study.md |

---

## 9. Reference Samples

A complete reference sample of director's notes (self-contained, inside this skill):

`assets/director-notes-samples/launch-film-30s-sample.md` (~78KB · 11,500 characters · 13 shots · all 5 parts present)

The original project locations (with the corresponding implementation HTML + keyframes):

- v5-director-notes.md (the director's notes, on the original author's local machine, not distributed with the repo)
- v5-six-forms.html (HTML implementation, on the original author's local machine, not distributed with the repo)
- v5-keyframes/ (keyframe verification screenshots, on the original author's local machine, not distributed with the repo)

When starting a new project, strongly recommend **reading this sample first** to understand the workload and density of detail before deciding whether to run the full workflow.

---

## 10. Anti-Patterns (Don't Do These)

❌ **Write a condensed 1000-word director's notes and get started**
→ A condensed version is guaranteed to miss some subsection of the Visual System, forcing you to keep returning to patch the spec during HTML implementation. If you're going to do it, go 10,000-word level; if you want to save effort, skip it entirely.

❌ **A storyboard with only 5-8 shots**
→ A 30-second film needs at least 12-15 shots (2-3 seconds per shot). Few shots = uniform rhythm = no climax.

❌ **Delivering the director's notes and stopping, without implementation**
→ The document isn't the deliverable; the animation is. Deliver the document and the animation together, with the document appended as the "design rationale."

❌ **Letting subagents see other versions during multi-perspective parallel**
→ Each subagent must stay independent, or they converge. Only compare at the review stage.

❌ **Skipping keyframe verification and recording MP4 directly**
→ Guaranteed rework. Keyframe verification is the cheapest quality gate.

❌ **Deferring animation detail decisions to "I'll think about it when I record"**
→ The recording stage is mechanical execution; it can't make creative decisions. Every decision must be fixed in the director's notes.

---

*Last revised: 2026-05-11*
*Real case: huashu-md-html v2.0 launch film (v5-director-notes.md)*
