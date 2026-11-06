# Module · Animation / Video / Promo Films

Everything timeline-driven goes here: HTML animation, product feature demos, launch films, narrated concept videos, MP4/GIF export. This is the skill's most capable module, so it has its own routing layer. Cross SKILL.md's narrow bridge first (the three-direction gate applies as usual — the draft shape is a direction board), then follow this manual.

## First, Decide What Kind of Film This Is

| Film | Main line | Must-read |
|---|---|---|
| Short animation / concept demo (<1 min, no narration) | The "general flow" below | `storyboard-basics.md` → `animation-pitfalls.md` → the backend files |
| Product UI is the protagonist (feature demos, commercial jobs, UI showcases) | General flow + UI showcase | `ui-demo-animation.md` (the screenshot-camera-moves vs HTML-rebuild decision tree, the eight UI showcase forms) + `assets/cursor.jsx` |
| Launch film / brand promo ("Apple-level" expectations) | Three-direction direction boards → after the pick, write the 10,000-word director's notes | `launch-film-director-notes.md`, `cinematic-patterns.md` |
| Long narrated video (≥1 min, one concept explained clearly) | Narration-driven: write the voiceover script first, then the picture | `voiceover-pipeline.md` + `assets/narration_stage.jsx` |
| Lots of same-kind material (20+ screenshots/works, the message is scale) | Gallery-style scenes | `hero-animation-case-study.md`, `apple-gallery-showcase.md` |
| Want multiple versions / multi-platform distribution | Multiple perspectives in parallel | `multi-perspective-parallel-case-study.md` |

## General Flow

1. **Three-direction direction boards**: 1 board per direction — 1–2 real HTML still-frame screenshots of the hero keyframe + a palette strip + a one-line positioning + the reference work's name. Not three finished films, but they must be genuinely rendered frames (`references/directions.md`). The three directions differ in motion language and materials, not just colors.
2. **Storyboard cards**: before any animation starts, produce lightweight storyboard cards — every shot is first a moving cover image (the format in `storyboard-basics.md` §5, with the [CAMERA] column and acceptance frame numbers). For films ≥20s the storyboard cards go into the director's notes (`导演稿.md`), together with **visual density clauses** — director's notes that only write narrative and camera moves will come back as wireframes (`animation-best-practices.md` §6.5).
3. **Camera language**: for shot-level motion like zoom / pan / transitions, read `camera-language.md` first (budget-driven, inter-shot grammar); implementation is in `gsap-recipes.md` §9.
4. **Pick a backend** (table below) and write the animation. Before touching anything, read `animation-pitfalls.md`.
5. **Look at frames**: capture frames at the key moments and actually look at them — clipping, collisions, empty frames, rhythm that only works on paper. Capture the first second after every scene change too.
6. **Sound**: the default delivery is an MP4 with SFX + BGM (see "Sound" below).
7. **Export and verify** (see "Export" below).

## Backends

| Backend | When to use | Read |
|---|---|---|
| **HyperFrames** (default for new animation) | Needs a rendered film, determinism, or 60fps | `hyperframes-backend.md` (selection boundaries, composition contract, old-demo migration) + `gsap-recipes.md` |
| **Stage + Sprite** (`assets/animations.jsx`) | Single-file delivery, purely interactive demos, weak runtime | `animations.md` |
| Narration-driven (`assets/narration_stage.jsx`) | Long videos with voiceover | `voiceover-pipeline.md` |

When hand-writing a Stage / Sprite (not using `animations.jsx`) you must implement two things, or video recording will break: set `window.__ready = true` synchronously on the first tick frame; force `loop = false` when `window.__recording === true` is detected.

## The Two Most Common Failures

- **A PowerPoint with voiceover**: every scene gets its own independent layout + text fade-up + whole-page opacity transitions. The film should be one continuous motion narrative: pick 1–2 hero elements that persist across scenes, each segment is a state change of that element, and scenes morph instead of cutting (`voiceover-pipeline.md`'s "iron rules").
- **Fake chrome drawn inside the frame**: a bottom progress bar, timecode, or copyright strap colliding with the Stage's built-in scrubber. The frame carries narrative content only (`animation-pitfalls.md` §11).

## Sound (on by default)

The silent version is a half-finished product. Build the BGM + SFX twin tracks together; BGM alone is one-third of the job done.

- Design the SFX cue list per `audio-design-rules.md`, using `assets/sfx/<category>/*.mp3` (37 prefabricated cues, `sfx-library.md`); a launch hero runs ~6 cues per 10s, tool demos 0–2 per 10s; `scripts/sfx-cues.sh` marks the cue points
- BGM: `scripts/add-music.sh` (6 scene-based music tracks)
- Before delivery, run `ffprobe -select_streams a` to confirm an audio track is present
- Skip only when the user says "no audio", "visuals only", or "I'll do my own voiceover"

## Export

- HyperFrames: `npm run check` (the five-gate audit; add `--no-contrast` for dark cinematic style) → `npx hyperframes render --fps 60` → `scripts/verify-video.sh`
- In-house pipeline: `scripts/render-video.js` (25fps intermediate) or `scripts/render-video-seek.js --fps=60` (per-frame seek — true 60fps, no black frames; use it when running on the Stage clock) → `scripts/convert-formats.sh` derives the 60fps MP4 and the palette-optimized GIF
- Narrated: `bash "$HD/scripts/render-narration.sh" demo.html --timeline=_narration/timeline.json [--bgm-mood=educational]` (internally calls `scripts/mix-voiceover.sh` to mix the voice; for standalone mixing you can call it directly too)
- After the final render, an optional AI film review (a cloud capability — bring your own key, explicit confirmation required, see SECURITY.md): `uv run "$HD/scripts/cloud/ai-review-video.py" --video <final film> --context 导演稿.md --yes`; with no key, use `scripts/verify-video.sh` to pull frames and review them by eye (`ai-video-review.md`)
- Full notes: `video-export.md`

**Watermark**: animation output carries "Created by Huashu-Design" by default (never added to slides, infographics, prototypes, or web pages); unofficial tribute animations for third-party brands get the "Unofficial · " prefix; drop it if the user says no. Template in the final section of `video-export.md`.

**Gate**: before rendering a long film ≥45s, `scripts/design-gate-hook.sh` checks for `direction-approved.md` and blocks the render when the file is missing; when the user explicitly says skip, let it through with `SKIP_DESIGN_GATE=1`.

## Starter Components

| File | Purpose |
|---|---|
| `assets/animations.jsx` | Stage + Sprite + useTime + Easing + interpolate |
| `assets/narration_stage.jsx` | NarrationStage + Scene + Cue + Subtitles (narration-driven) |
| `assets/cursor.jsx` | The cursor for product demos: four shapes, arcing trajectories, click ripples, frame determinism |
| `assets/ios_frame.jsx`, `android_frame.jsx`, `macos_window.jsx`, `browser_window.jsx` | Device and window shells |

## Engine Layer (reserved)

This module's methods (director's judgment, motion language, rhythm, sound design) and its execution engines (rendering, sound, verification) are two separate layers. What's listed above are the current engines; when a new engine is plugged in later, it attaches to the "Backends" table and the "Sound" and "Export" sections, and the method-layer files don't have to change with it.
