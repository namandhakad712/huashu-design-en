# HyperFrames Rendering Backend · Selection Boundaries and Operations Manual

> Introduced after passing real-world verification on 2026-07-17 (all five checks passed: toolchain / Chinese fonts / proxy environment / migration / 3D; key data is embedded in this doc).
> HyperFrames is HeyGen's open-source HTML→video framework (Apache 2.0): plain HTML + a paused GSAP timeline, deterministically rendered by a headless browser seeking frame by frame.

## Selection boundaries (check this table before starting)

| Scenario | Which rendering route |
|---|---|
| New animation projects (default) | **HyperFrames**. Audit suite included, 3D/GSAP/Lottie/shader all unlocked |
| Need 3D / particles / physical inertia / shader transitions | HyperFrames (the in-house Stage can't do it) |
| Reusing/revamping an old Stage demo | Migrate it while at it (adapter recipe below, 20-30 min each); if only re-rendering without changes, keep using render-video-seek.js |
| Weak runtime (no npm / can't install dependencies / single-file delivery for users to double-click open) | In-house Stage (assets/animations.jsx), old flow unchanged |
| Interactive demos (users play in the browser, no video export) | In-house Stage or plain HTML; HyperFrames is a rendering pipeline, not an interaction framework |
| Long narrated videos (Step 9.5, driven by narration_stage) | **In-house narration pipeline** (voiceover-pipeline.md + render-narration.sh), not HyperFrames for now — the dual time sources / subtitles / TTS timeline are deeply coupled to the in-house Stage; when both this row and "animations default to HyperFrames" apply, this row wins |
| Batch parametrized videos (mass customization / template text swaps) | Remotion (see roadmap direction 5, independent of this skill's main flow) |

**The design language always calls the shots**: narrative structure, the easing system, and the SFX/BGM dual-track system all still apply as before (animation-best-practices.md / audio-design-rules.md); HyperFrames is only the implementation and rendering tool. GSAP implementation recipes are in `references/gsap-recipes.md`.

## Project scaffolding

> ⚠️ Install warning: besides generating project files, `hyperframes init` also installs **19 hyperframes skills into `~/.claude/skills/`** (composition contract docs for the rendering backend — pure documentation, no executable hooks). If that bothers you, run `npx hyperframes docs` first to see the local doc list before deciding whether to init.

```bash
npx -y hyperframes init <project-name> --example blank   # non-interactive mode requires --example
cd <project-name> && npm install
```

Generates index.html / hyperframes.json / meta.json / package.json (pinned CLI version) + a project-level CLAUDE.md. init installs the 19 hyperframes skills into `~/.claude/skills/` (already installed on this machine). For the composition authoring contract, read the hyperframes-core skill's SKILL.md (init installs them into each runtime's skill directory; Claude Code defaults to `~/.claude/skills/`; runtimes without a skill mechanism just read `npx hyperframes docs` local docs instead). Local docs: `npx hyperframes docs <topic>` (data-attributes / gsap / rendering / troubleshooting).

**Version policy**: the project's package.json pins an exact version (currently verified: 0.7.61). It iterates extremely fast (300+ releases), so before upgrading run `npx hyperframes@latest upgrade --project . --check` to see the delta, run a regression demo once, then proceed.

## Composition contract quick reference (full version in hyperframes-core)

- Root container: `data-composition-id` + `data-start` + `data-duration` + `data-width/height`
- Every timed element: `class="clip"` + `data-start` + `data-duration` + `data-track-index`
- The timeline must be paused and registered: `window.__timelines["composition-id"] = gsap.timeline({paused:true})`
- Video assets use `muted`; the audio track is a separate `<audio>` element
- **Only deterministic logic allowed**: no `Date.now()` / `Math.random()` / runtime network fetch; use a seeded function for randomness
- Fonts: Google Fonts are auto-fetched by the compiler and injected as deterministic @font-face (cached at `~/.cache/hyperframes/fonts/`); for pure system fonts (PingFang SC, etc.), add a line `@font-face { font-family:"PingFang SC"; src: local("PingFang SC"); }` to pass lint
- Three.js goes through the `hf-seek` event adapter (`~/.claude/skills/hyperframes-animation/adapters/three.md`); the root container must explicitly set `data-duration`

## Migrating old demos · Adapter recipe (measured at 20-30 min each)

In-house Stage / plain render(t) animations don't need rewriting; four steps:

1. **Wrap in a container**: add an outer `#root` carrying the composition data attributes; making the whole `.stage` the single clip is easiest (`class="stage clip"` + data-start/duration/track-index); change `.stage` from fixed-centered to absolute inset:0, and pin html/body to 1920×1080
2. **Remove self-driving code**: delete the rAF tick loop, fitStage/resize listeners, the replay button, and the `__ready/__setTime/__seek` protocol entirely (the renderer doesn't need them)
3. **Attach a proxy tween** (the core 12 lines):
   ```js
   const proxy = { t: 0 };
   const tl = gsap.timeline({ paused: true });
   tl.to(proxy, { t: DURATION, duration: DURATION, ease: "none",
     onUpdate: () => render(proxy.t) }, 0);
   window.__timelines = window.__timelines || {};
   window.__timelines["main"] = tl;
   render(0);   // required: onUpdate doesn't fire when the timeline sits at t=0; without this the first frame may be uninitialized
   ```
4. **Scan for transitions**: search the whole file for `transition:` declarations. CSS transitions + class toggling follow the wall clock and are non-deterministic under frame-by-frame seeking; they must be converted into pure functions of t inside render(t) (lerp)

## Validation and rendering

```bash
npm run check                        # five-gate audit: lint+runtime+layout+motion+contrast
npx hyperframes check --no-contrast  # for dark cinematic style (see below)
npx -y hyperframes@<pin-version> render --fps 60   # final render; 30fps by default
```

- **check must be 0 errors before rendering** (except the contrast gate). lint catches a whole class of "no-warning visual bugs" — letterSpacing jitter, missing fonts, non-determinism, etc.
- **The contrast gate trade-off**: it checks against WCAG 4.5:1, which fundamentally conflicts with the low-contrast watermark / decorative text (16-40% opacity) of the dark cinematic style, and offers no per-element exemption. Dark cinematic outputs uniformly use `--no-contrast`; the other four gates must still be 0 errors. Don't skip it for light-background informational outputs — a contrast error there is usually a real problem
- **Two-stage rendering**: first render quickly at the default 30fps, and only after eyeball + frame-check pass, do the `--fps 60` final render. A 60fps 600-frame 1080p render measured about 20 seconds
- Validate the render output side (audio stream / black frames / loudness / duration) with `scripts/verify-video.sh` (see verification.md)

## Transparent channel (overlay stylized text / graphics stacked directly onto the edit track)

`npx hyperframes render --format mov` outputs ProRes 4444 (yuva444p12le, with alpha; verified 2026-07-17 — stacking on a colored backdrop keeps even soft shadows correctly semi-transparent); `--format webm` is also transparent and smaller; `--format png-sequence` produces RGBA frame sequences for AE/DaVinci. Key points on the composition side: set the html/body background to `transparent`, no base color underneath. Overlay assets such as stylized text / corner logos / lower-thirds now go directly onto the edit track with no keying needed. Note MOV is large (ProRes lossless-level, ~15MB per 4 seconds) — use it for delivery to editing; use webm for network transfer.

## Audio

`<audio>` elements inside a HyperFrames composition can go directly onto the timeline (BGM / voiceover rendered along with the film). The current audio flow is unchanged: the SFX/BGM dual-track system follows audio-design-rules.md, and post-mixing with add-music.sh / mix-voiceover.sh is also fine. Which route is better will be settled in practice; nothing is enforced for now. SFX cueing uses `scripts/sfx-cues.sh <video> <cue-table.tsv> <output>` (cue table = three columns: seconds / SFX path / volume dB, distilled from B00 in practice; edit the table and re-run — ~10 seconds to produce the film).

## Incremental pitfalls (relative to the in-house pipeline)

The in-house pipeline's pitfalls (animation-pitfalls.md §7/10/12/13 recording-protocol category, §6 font timing, §15/17 network category) **don't apply** on the HyperFrames backend: the recording protocol is handled internally by the framework, fonts are fetched at compile time, and CDNs work under a proxy (verified). Four new pitfalls in total, already recorded in animation-pitfalls.md §18-21: CSS transition non-determinism, the proxy tween's first frame, the contrast gate conflict, and the fromTo immediateRender phantom.
