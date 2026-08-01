# Voiceover Pipeline · Narration-Driven Animation

> Upgrading animation from "silent footage + post-dubbing" to a workflow where "**the narration comes first, then the audio's measured duration drives the visuals**".
> Use case: 5-20 minute concept explainer videos, tutorial videos, long-form knowledge content.
>
> Use together with `references/animation-best-practices.md` — this file handles **how to sync narration with visuals**,
> animation-best-practices handles **how each frame moves**.

---

## 🛑 Iron Rules · Read Before Writing Any Line of Code

> **It can't be emphasized enough: Failure mode #1 for narration animation is making a PowerPoint with voiceover.**

### Rule #1 · The Entire Piece is One Continuous Motion Narrative, Not a Set of Independent Scenes

PowerPoint is 7 slides. We're making **1 continuous movie that lasts X minutes**.

**Identity shift**:
- ❌ You're not "making content for 7 scenes"
- ✅ You're "letting one or several hero elements perform on screen for X minutes"

**Visual skeleton = One or several hero elements spanning the entire piece**:
- It appears at t=0 and doesn't leave until the end
- Each cue is its **state change** (position / size / color / perspective / form), not "switching to a new element"
- Scene boundaries exist in the script **but should not exist on screen** — the audience can't tell "this is scene 3", they only see one continuous motion

**Counter-example (real pitfall from skill v1 · 2026-05-10)**:
- 7 `<Scene>` components each with independent layout, scene switch = full-page opacity 1→0 into the next page
- Each cue = `opacity: p, transform: translateY((1-p)*30px)` (monotone fade-up)
- Result: The audience's first reaction was "like flipping through keynote pages", the whole piece's feel collapsed to zero

**Correct pattern**:
- Pick 1-2 hero elements (e.g., the demo in this article should pick the two characters "md" and "html" as the skeleton)
- These two characters **stay on screen from opening to closing**
- Each "scene" is actually one state change of the hero element
  - opening: the two characters face off at center screen
  - md-side: md grows large and bold to take over the frame, html retreats to a corner as small text; data floods in around md
  - html-side: html reverses into the protagonist; md retreats to a corner
  - the-real-question: the two characters return to center, but a "≠" separator appears between them
  - the-split: the two characters push apart to both sides, a blank gap expands in the middle
  - activity-proof: the two characters alternately flash on the timeline
  - closing: the two characters settle into the final answer position
- This way the whole piece is "md and html performed on screen for X minutes", not 7 independent PPTs

**Minimal implementation skeleton** (copy and modify directly):

```jsx
// ── Step 1: Define the hero's target state in each scene (position/size/opacity) ──
const HERO_KEYS = {
  opening:    { md: { x: 50, y: 35, scale: 1.0, opacity: 1 }, html: { x: 50, y: 65, scale: 1.0, opacity: 1 } },
  'md-side':  { md: { x: 78, y: 50, scale: 1.6, opacity: 1 }, html: { x: 92, y: 8,  scale: 0.25, opacity: 0.4 } },
  'html-side':{ md: { x: 8,  y: 8,  scale: 0.25, opacity: 0.4 }, html: { x: 22, y: 50, scale: 1.6, opacity: 1 } },
  // ... one entry per scene, continuous motion flows from the previous scene's final → this scene's from
};

// ── Step 2: easing + lerp utilities ──
const expoOut = t => t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
const lerp = (a, b, t) => a + (b - a) * t;
const lerpPos = (from, to, t) => ({
  x: lerp(from.x, to.x, t), y: lerp(from.y, to.y, t),
  scale: lerp(from.scale, to.scale, t),
  opacity: lerp(from.opacity ?? 1, to.opacity ?? 1, t),
});

// ── Step 3: HeroAnchor component —— mount directly under <NarrationStage>, NOT inside <Scene> ──
const HeroAnchor = () => {
  const { time, scene, timeline } = useNarration();
  if (!scene) return null;
  const idx = timeline.scenes.findIndex(s => s.id === scene.id);
  const prevId = idx > 0 ? timeline.scenes[idx - 1].id : scene.id;
  const from = HERO_KEYS[prevId];
  const to   = HERO_KEYS[scene.id];

  // Use the first ~45% of the scene to morph from the previous state to this scene's state, hold the rest
  const transitionDur = Math.min(2.0, scene.duration * 0.45);
  const t = expoOut(Math.min(1, (time - scene.start) / transitionDur));
  const md   = lerpPos(from.md,   to.md,   t);
  const html = lerpPos(from.html, to.html, t);

  // Add subtle breathing so any single frame has motion (Rule #3)
  const breath = 1 + Math.sin(time * 0.6) * 0.012;

  const renderHero = (label, pos, color) => (
    <div style={{
      position: 'absolute', left: `${pos.x}%`, top: `${pos.y}%`,
      transform: `translate(-50%, -50%) scale(${pos.scale * breath})`,
      opacity: pos.opacity, color, fontSize: 360, fontWeight: 800,
      lineHeight: 1, willChange: 'transform, opacity', pointerEvents: 'none',
    }}>{label}</div>
  );
  return <>
    {renderHero('md',   md,   '#1B4965')}
    {renderHero('html', html, '#C04A1A')}
  </>;
};

// ── Step 4: Main component —— hero lives under NarrationStage's children, scene-internal auxiliary elements are managed separately ──
const App = () => (
  <NarrationStage timeline={TIMELINE} audioSrc="_narration/voiceover.mp3" width={1920} height={1080}>
    <HeroAnchor />  {/* ← persists across scenes, the visual skeleton of the whole piece */}
    {/* scene-internal auxiliary elements use useSceneFade for a soft fade in/out, never hard-cut */}
    <MdSideAux />
    <HtmlSideAux />
    {/* ... */}
  </NarrationStage>
);
```

**Fully runnable reference**: `demos/md-html-narration/md-html-demo.html` (3 min 21 s, 7 scenes, 21 cues, battle-tested)

### Rule #2 · No "Hard Cuts" Between Scenes

| Wrong pattern (PowerPoint slop) | Correct pattern (cinematic) |
|---|---|
| Scene A does `opacity 1→0` while scene B does `opacity 0→1` | Scene A's core elements **morph into** B (position/size/color transform smoothly) |
| Each scene has an independent layout, elements appear/disappear | Elements **persist on screen**, only position and form change |
| `keepMounted=false`, components unmount the instant a scene switches | Hero uses `keepMounted=true`, sharing the same DOM node across scenes |
| Subtitle bars / data cards each fade in and out on their own | The subtitle bar is the only "non-hero" entry, and after holding it **exits together with the hero's motion** |

Implementation level:
- **Shared elements across scenes** → hoist the hero to a direct child of `<NarrationStage>`, **don't put it inside any `<Scene>`**
- Use the `useNarration()` hook in the hero to read `time`, `scene`, `isCueTriggered`, and decide the form yourself based on the current time
- `<Scene>` is only for managing the auxiliary elements that appear in that section (data cards, quote blocks, etc.), and **these auxiliary elements must not hard-cut either** — enter with expoOut + stagger, exit with a fade overlap into the next scene

### Rule #3 · Every Frame Must Have Motion

**Self-check method**: **Pause at any arbitrary frame** during playback (not the second a cue fires).
- If the frame looks "**completely still**" → wrong. Go add underlying motion (background drift / hero subtle scale / camera pan / parallax)
- There should always be an **underlying motion** running (even if it's not the focus):
  - The hero element's `scale: 1 ↔ 1.02` 5-second breathing loop
  - Background `translateX: 0 ↔ -20px` slow drift
  - Data cards keep a subtle `translateY` jitter (Perlin noise) after entering
- A completely still frame = PowerPoint slop

### Rule #4 · Easing / Stagger / Hold Are the Baseline

| Item | Must | Forbidden |
|---|---|---|
| Easing | `expoOut` as main axis (`cubic-bezier(0.16, 1, 0.3, 1)`), `overshoot` for emphasis, `spring` for landing | `linear`, `ease`, CSS defaults |
| Multi-element entry | 30ms stagger (each enters 30ms later) | One-shot: everything appears at once |
| Before key cues | hold 0.3-0.5s so the audience can "see" it (the previous scene's elements rest 0.3s first, then the cue fires) | Seamlessly cutting to the next scene right after a line |
| Ending | Cut off abruptly, hold the last frame 1s | fade to black |

For detailed rules see §1-§4 of `animation-best-practices.md`.

### Self-Check · First Viewer Reaction

When it's done, show it to someone who hasn't seen it (or watch it yourself 24 hours later). **What is their first reaction?**

| Reaction | Rating | Action |
|---|---|---|
| "This is a PPT with voiceover" | Failed | Go back and redo it |
| "The visuals switch along with the sound" | Below passing | Lacks continuous narrative; hero element doesn't exist or doesn't span the piece |
| "This thing is moving" | Passing | But nothing memorable |
| "I want to keep watching" | Good | Pacing is right |
| "I want to screenshot this part" | Great | You did it |

---

## Workflow (High Level)

```
                ┌──────────────────────────┐
                │  narration script .md   │
                │  (## scene +            │
                │  [[cue:xx]] key lines)  │
                └──────────────┬───────────┘
                               │
                  narrate-pipeline.mjs
                               │
                               ▼
            ┌──────────────────────────────┐
            │ voiceover.mp3 (concatenated) │
            │ timeline.json (measured)     │
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌─────────────────┐      ┌──────────────────┐
    │ HTML animation  │      │ Record MP4 + mix │
    │ (NarrationStage)│      │ render-narration │
    │ live with audio │      │ → final release  │
    │ sync            │      │ MP4              │
    └─────────────────┘      └──────────────────┘
       Delivery form 1          Delivery form 2
```

## Narration Script Format

Put it anywhere in the project directory, filename suggested as `script.md`:

```markdown
---
title: What is LLM
voice: S_JSdgdWk22   # optional, overrides the default voice in .env
speed: 1.0           # optional, 0.5-2.0
gap: 0.4             # silence between scenes in seconds, default 0.3
---

## intro
Hello everyone, today in 5 minutes we'll explain what LLM is.

## what-is
LLM stands for Large Language Model, [[cue:bigmodel]]it's a neural network with hundreds of billions of parameters.
Essentially it's a predictor that continues text.

## demo
For example you type "today's weather", [[cue:input]]the model predicts what the next character most likely is.
[[cue:predict]]Maybe "great out", maybe "pretty nice".
```

**Rules**:
- Scene titles `## scene-id` are English/digits + hyphens (e.g., `## what-is`, `## scene-1`)
- `[[cue:xx]]` is placed **in the middle of a key sentence** — the script splits the text at that position at runtime, and the instant right after the cue is the visual's trigger point
- Cue ids are listened for in the animation HTML with `<Cue id="xx">`
- When writing narration, **focus on rhythm + short sentences** — long sentences come out flat through TTS

## timeline.json Schema

```ts
{
  title: string,
  voice: string | null,
  speed: number,
  gap: number,
  totalDuration: number,        // measured seconds of the whole voiceover.mp3
  voiceover: 'voiceover.mp3',   // path relative to timeline.json
  scenes: [
    {
      id: string,
      start: number,            // this scene's start time within the full audio
      end: number,
      duration: number,
      audio: 'audio/<id>.mp3',  // this scene's standalone audio (child segments already concatenated before merging)
      text: string,             // the full scene text with [[cue:xx]] markers stripped
      // chunks is the source for subtitle display — each chunk is a child segment cut by cues, carrying TTS-measured time windows
      chunks: [
        {
          text: string,            // child segment text
          start: number,           // relative time within the scene
          end: number,
          absoluteStart: number,   // absolute time on the full track (aligned to voiceover.mp3)
          absoluteEnd: number,
          // words: character-level timestamps (measured and returned by TTS enable_subtitle, on by default; --no-timestamps turns it off)
          // note: text is the TN-normalized text ("2025"→"二零二五"), punctuation is attached to the preceding character
          words: [
            { text: string, start: number, end: number, absoluteStart: number, absoluteEnd: number }
          ],
        }
      ],
      cues: [
        {
          id: string,
          offset: number,       // relative time within the scene
          absoluteTime: number, // absolute time on the full timeline
        }
      ]
    }
  ]
}
```

`absoluteTime` and `absoluteStart/End` are all **actually measured** — the pipeline splits the scene text into child segments by cue and TTSes each separately, and the times = accumulating the measured durations of the preceding child segments. **They are not approximations estimated linearly by character count**.

## Subtitles

> **Subtitles are on by default** — long narration videos without subtitles see a significant drop in retention. NarrationStage ships `<Subtitles />` ready to use out of the box.

### Usage (one line)

```jsx
const { NarrationStage, Subtitles } = NarrationStageLib;
<NarrationStage timeline={TIMELINE} audioSrc="...">
  {/* your hero / scene content */}
  <Subtitles />  {/* ← automatically takes the active text from timeline.scenes[].chunks */}
</NarrationStage>
```

### Visual Rules (Bilibili style · anti-PowerPoint)

| Item | Rule | Counter-example |
|---|---|---|
| Background | **No background** (no black bar, no backdrop-blur) | Semi-transparent black + blur = the subtitle bar weighs down the picture = PPT feel |
| Text color | **Dark ink `#1a1a1a` + white glow on light backgrounds**; white text + black glow on dark backgrounds | White text + black outline on a light background = blurry text |
| Font size | 32px (1080p video) | <24px is hard to read, >40px steals the main visual |
| Font | `PingFang SC` / `Noto Sans SC` (sans-serif, Bilibili standard) | Serif fonts look like movie subtitles |
| Position | bottom: 90px (not edge-bound) | Hugging the bottom edge looks cheap |
| Line length | **≤ 12-13 characters** (for mixed CN/EN, count English as 0.5 character) | >15 characters per line can't be read fully on mobile |
| Line-breaking | **Never truncate across a sentence period**: first split by 。！？, then merge each sentence by 、；： to ≤maxLen | Hard-cutting by character count turns "this is good" into "this is goo" + "d" |

`<Subtitles />` runs by the above rules by default, no props needed. For dark backgrounds: `<Subtitles color="#fff" haloColor="rgba(0,0,0,0.85)" />`.

### Karaoke Mode (character-level highlight)

```jsx
<Subtitles karaoke />                          {/* the word being read lights up in brand orange #e8590c */}
<Subtitles karaoke karaokeColor="#0a84ff" />   {/* custom highlight color */}
```

- Depends on the `words` character-level timestamps in timeline chunks (output by default from narrate-pipeline.mjs; Doubao TTS v3 `enable_subtitle`, requires a 2.0 resource, CN/EN only)
- Shows the whole line, colors character by character; line-breaking reuses the ≤maxLen + no-period-crossing rules (lines built from words, strictly aligned with pronunciation)
- When a chunk has no `words`, it automatically falls back to normal chunk mode — no checks needed on the caller side

### Line-Splitting Algorithm (built into narration_stage.jsx)

```js
splitChunkToLines(text, maxLen = 13)
// 1. Split sentences at strong punctuation (。！？\n)
// 2. Each sentence ≤ maxLen is kept as is
// 3. Otherwise slice by weak punctuation (，、；：), merging up to ≤ maxLen
// 4. Fallback hard cut (rare)
// Mixed CN/EN: English/digits count as 0.5 character for visual width
```

If a line ends up noticeably too long or too short after splitting a chunk, **move the cue position in the narration script** (cues split the scene finer) — don't fiddle with the line-splitting logic in the frontend.

## NarrationStage API

```jsx
import 'assets/narration_stage.jsx';
const { NarrationStage, Scene, Cue, useNarration } = NarrationStageLib;

<NarrationStage
  timeline={TIMELINE}                  // timeline.json contents
  audioSrc="_narration/voiceover.mp3"  // path relative to the current HTML
  width={1920} height={1080}
  background="#f5f1e8"
  controls={true}                      // show the bottom playback bar when live
>
  {/* hero element: persists across scenes —— put it directly as a NarrationStage child */}
  <HeroAnchor />

  {/* scene-internal auxiliary elements: only appear in that scene */}
  <Scene id="intro">
    <Cue id="bigmodel">{(triggered, progress) => (
      <SomeElement style={{ opacity: progress }} />
    )}</Cue>
  </Scene>
</NarrationStage>
```

**Hooks**:
- `useNarration()` returns `{ time, scene, sceneTime, isCueTriggered, cueProgress }`
- Read it directly inside custom components, no props needed

**Scene component**:
- By default only mounts when `scene.id === id`
- Add `keepMounted` to stay mounted (use when animations continue across scenes)

**Cue component**:
- children must be `(triggered, progress) => ReactNode`
- progress is the 0→1 ramp value after the cue fires (default 0.6s ramp)

## Time Source (Dual Track)

NarrationStage auto-detects `window.__recording`:
- **Live playback mode** (default): follows the audio element's currentTime; pausing / dragging to seek stay in sync
- **Video recording mode** (render-video.js sets `window.__recording = true`): rAF wall-clock self-driven starting from 0, exposing `window.__seek(t)` for render-video.js to reset

## The Three Scripts

| Script | Input | Output |
|---|---|---|
| `scripts/cloud/tts-doubao.mjs` | single text segment | single mp3 + measured duration |
| `scripts/narrate-pipeline.mjs` | narration script .md | voiceover.mp3 + timeline.json |
| `scripts/mix-voiceover.sh` | video + voiceover.mp3 [+ BGM] | MP4 with audio |
| `scripts/render-narration.sh` | narration HTML + timeline.json | final MP4 (record + mix in one go) |

## .env Configuration

> ⚠️ TTS is an optional cloud capability: the narration script text is sent to the official Doubao TTS API (openspeech.bytedance.com),
> using your own key. The first script call needs explicit confirmation via `--yes` or `HUASHU_CLOUD_OK=1`,
> and the endpoint is hard-validated against the byte-dance official domain allowlist. Data-flow statement is in the repo root `SECURITY.md`.

`.env` in the skill root directory (already gitignored):

```
DOUBAO_TTS_API_KEY=<your_api_key>
DOUBAO_TTS_VOICE_ID=zh_female_xiaohe_uranus_bigtts
DOUBAO_TTS_ENDPOINT=https://openspeech.bytedance.com/api/v3/tts/unidirectional
```

You can also use the console's App ID + Access Token authentication:

```
DOUBAO_APP_ID=<your_app_id>
DOUBAO_ACCESS_KEY=<your_access_token>
DOUBAO_TTS_VOICE_ID=zh_female_xiaohe_uranus_bigtts
```

`DOUBAO_TTS_RESOURCE_ID` is auto-inferred from the voice by default: `S_` cloned voices use `seed-icl-1.0`, `uranus` official voices use `seed-tts-2.0`, other official voices use `seed-tts-1.0`.

## Standard Workflow (10 Steps)

1. **Write the narration script**: the script is the source code. Write the full spoken text first, mark scene titles `## scene-id`, add `[[cue:xx]]` before key sentences
2. **Run narrate-pipeline**: `node scripts/narrate-pipeline.mjs --script script.md --out-dir _narration --yes` (`--yes`= confirm sending text to Doubao TTS)
3. **Listen to the whole voiceover.mp3**: if the pacing is off, go back and revise the script. **This step sets the quality ceiling of the whole piece**
4. **🛑 Answer the iron rules before designing**: what's the hero element? What state is it in each scene? How does it morph across scenes? Don't write code if you can't answer
5. **Write the animation HTML**: use NarrationStage + one or several hero elements performing across scenes
6. **Live preview**: open the HTML in a browser, click ▶ Play, watch visuals + narration sync
7. **First-viewer self-check**: score it with the "Self-Check · First Viewer Reaction" table above. On failure, go back to Step 4 and redo
8. **Record the video**: `bash scripts/render-narration.sh demo.html --timeline=_narration/timeline.json` (automatically records a silent MP4 + mixes in the voiceover)
9. **Optional BGM**: add `--bgm-mood=educational` to render-narration (or tech / tutorial, etc.)
10. **Deliver**: browser HTML (for live demos) + final MP4 (for publishing)

## Error Handling

| Problem | Solution |
|---|---|
| TTS API errors | Check `DOUBAO_TTS_API_KEY` in .env, or whether `DOUBAO_APP_ID` + `DOUBAO_ACCESS_KEY` are correct |
| A scene's audio is clearly longer/shorter than the script | There are strange punctuation marks or emoji in that scene's text and TTS parses it wrong → revise the script |
| cue absoluteTime is off | ffmpeg has a problem when stitching child segments in the scene → check mp3 encoding consistency |
| Black screen in the recorded video | render-video.js didn't receive the `window.__ready` signal → check that NarrationStage mounted properly |
| Stuttering in the recorded video | The animation does heavy layout (lots of box-shadow / blur) → simplify or pre-composite |
| Live playback audio out of sync | The audio element loads slowly → add `preload="auto"` or preload locally |

## When Not to Use This Pipeline

- **<60s short animations**: just do a silent animation + post-dubbing (add-music.sh + a standalone TTS) — no need for timeline driving
- **Pure BGM videos**: use `add-music.sh` to add preset BGM
- **Replacing TTS with real voice recording**: replace `voiceover.mp3` with the real recording, hand-write the timeline or measure scene durations with ffprobe + a helper script to generate it → the rest of the flow stays the same

---

**One last reminder**: go back to the iron rules before writing code. **Don't make a PowerPoint with voiceover**.
