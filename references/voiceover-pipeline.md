# Voiceover Pipeline · Narration-Driven Animation

> Upgrading animation from "silent footage + post-dubbing" to "**script first, then drive visuals by actual audio duration**" workflow.
> Use case: 5-20 minute concept explainer videos, tutorial videos, long-form knowledge content.
>
> Use together with `references/animation-best-practices.md` — this file handles **how to sync narration with visuals**,
> animation-best-practices handles **how each frame moves**.

---

## 🛑 Iron Rules · Read Before Writing Any Code

> **Emphasized as many times as needed: Failure mode #1 for narration animation is making a PowerPoint with voiceover.**

### Rule #1 · The Entire Piece is One Continuous Motion Narrative, Not a Set of Independent Scenes

PowerPoint = 7 slides. We're making **1 continuous X-minute movie**.

**Identity shift**:
- ❌ You're not "making content for 7 scenes"
- ✅ You're "letting one or several hero elements act on screen for X minutes"

**Visual skeleton = One or several hero elements spanning the entire video**:
- It appears at t=0 and exits only at the end
- Each cue is its **state change** (position / size / color / perspective / form), not "switching to a new element"
- Scene boundaries exist in the script, **but not in the visual** — audience can't see "this is scene 3", only sees continuous motion

**Counter-example (real pitfall from skill v1 · 2026-05-10)**:
- 7 `<Scene>` each with independent layout, scene switch = full-page opacity 1→0 to next page
- Each cue = `opacity: p, transform: translateY((1-p)*30px)` (monotone fade-up)
- Result: Audience's first reaction "like flipping through keynotes", entire piece quality = zero

**Correct pattern**:
- Pick 1-2 hero elements (e.g., demo uses "md" and "html" characters as skeleton)
- These two characters **stay on screen from start to finish**
- Each "scene" is actually a state change of the hero element
  - opening: two characters confront in center
  - md-side: md grows and takes over, html retreats to corner; data flows around md
  - html-side: html becomes main character; md retreats
  - the-real-question: two characters back to center, "≠" appears between them
  - the-split: two characters push to sides, middle expands
  - activity-proof: two characters alternate flashing on timeline
  - closing: two characters land at final answer position
- This way entire piece is "md and html performed on screen for X minutes", not 7 independent PPTs

**Minimal implementation skeleton** (copy and modify):

```jsx
// ── Step 1: Define hero target state in each scene (position/size/opacity) ──
const HERO_KEYS = {
  opening:    { md: { x: 50, y: 35, scale: 1.0, opacity: 1 }, html: { x: 50, y: 65, scale: 1.0, opacity: 1 } },
  'md-side':  { md: { x: 78, y: 50, scale: 1.6, opacity: 1 }, html: { x: 92, y: 8,  scale: 0.25, opacity: 0.4 } },
  'html-side':{ md: { x: 8,  y: 8,  scale: 0.25, opacity: 0.4 }, html: { x: 22, y: 50, scale: 1.6, opacity: 1 } },
  // ... one entry per scene, continuous motion from prev's end → this scene's start
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

  // First ~45% of scene duration for morphing from prev state, rest hold
  const transitionDur = Math.min(2.0, scene.duration * 0.45);
  const t = expoOut(Math.min(1, (time - scene.start) / transitionDur));
  const md   = lerpPos(from.md,   to.md,   t);
  const html = lerpPos(from.html, to.html, t);

  // Add subtle breathing for motion in every frame (Rule #3)
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

// ── Step 4: Main component —— hero under NarrationStage children, scene elements separate ──
const App = () => (
  <NarrationStage timeline={TIMELINE} audioSrc="_narration/voiceover.mp3" width={1920} height={1080}>
    <HeroAnchor /> {/* ← Not inside <Scene>, stays across entire video */}
    <Scene id="opening">{/* ... */}</Scene>
    <Scene id="md-side">{/* ... */}</Scene>
    {/* ... */}
  </NarrationStage>
);
```

### Rule #2 · Never Hard-Cut Between Scenes

Hard cut = "scene A ends, scene B starts" — use fade/slide/morph transitions instead.

**Scene transition patterns** (pick one per transition):
1. **Hero morph**: Hero element smoothly transitions to new state (recommended)
2. **Ripple expand**: Small element grows from center outward
3. **Slide through**: Current content slides left, new content slides in from right
4. **Cross dissolve**: Gentle fade cross (only for drastic content change, avoid overuse)

### Rule #3 · Every Frame Has Motion

"Static frame" = Death. Even if narration pauses, add subtle motion:

- **Breathing**: `scale = base + sin(time * frequency) * amplitude`
- **Particle flow**: Background particles never stop
- **Glow pulse**: Emissive elements breathe
- **Micro-sway**: Text blocks float slightly

---

## Narration Script Format

```markdown
---
title: What is LLM
gap: 0.5
---

## intro
Hello everyone. Today we'll explain what LLM is in 5 minutes.

## what-is
LLM stands for Large Language Model. [[cue:bigmodel]] It's a neural network with hundreds of billions of parameters.
```

**Frontmatter**:
| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Video title |
| `voice` | No | Voice ID (from .env if not set) |
| `speed` | No | Speech speed, default 1.0 |
| `gap` | No | Silence between scenes (seconds), default 0.3 |

**Scene format**:
- `## scene-id` — Scene header, scene ID must be unique
- `[[cue:cue-id]]` — Mark key moments in narration where animation triggers
- Plain text — Narration content

**Cue marking rules**:
- Place `[[cue:xxx]]` at the exact moment you want animation to trigger
- Can be mid-sentence (triggers when narration reaches that word)
- Multiple cues per scene allowed

---

## Timeline Schema (Generated by narrate-pipeline.mjs)

```json
{
  "title": "What is LLM",
  "voice": "S_xxx",
  "speed": 1.0,
  "gap": 0.5,
  "totalDuration": 180.5,
  "scenes": [
    {
      "id": "intro",
      "start": 0,
      "end": 12.5,
      "duration": 12.5,
      "audio": "audio/intro.mp3",
      "text": "Hello everyone...",
      "cues": [
        { "id": "greeting", "offset": 2.0, "absoluteTime": 2.0 }
      ],
      "chunks": [
        { "text": "Hello everyone.", "start": 0, "end": 2.5, "absoluteStart": 0, "absoluteEnd": 2.5 }
      ]
    }
  ],
  "voiceover": "voiceover.mp3"
}
```

**Fields**:
| Field | Description |
|-------|-------------|
| `totalDuration` | Total audio length (seconds) |
| `scenes[].start` | Scene start time in total timeline |
| `scenes[].end` | Scene end time |
| `scenes[].cues` | Animation trigger points within scene |
| `scenes[].chunks` | Text chunks for subtitle display (split by ≤13 chars, no sentence boundary crossing) |
| `voiceover` | Final concatenated voiceover file path |

---

## NarrationStage API

```jsx
import { NarrationStage, Scene, Cue, useNarration } from './assets/narration_stage.jsx';
```

### Components

| Component | Props | Description |
|-----------|-------|-------------|
| `<NarrationStage>` | `timeline`, `audioSrc`, `width`, `height`, `background`, `controls` | Main stage, manages playback |
| `<Scene id="xxx">` | `id`, `keepMounted` | Scene container, renders when active |
| `<Cue id="xxx">` | `id`, `ramp` | Animation trigger, provides `triggered` boolean and `progress(0-1)` |

### Hooks

| Hook | Returns | Description |
|------|---------|-------------|
| `useNarration()` | `{ time, scene, sceneTime, isCueTriggered(id), cueProgress(id, ramp) }` | Current playback state |

### NarrationStage Props

| Prop | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `timeline` | object | Yes | — | Timeline JSON from narrate-pipeline |
| `audioSrc` | string | Yes | — | Path to voiceover.mp3 |
| `width` | number | No | 1920 | Video width |
| `height` | number | No | 1080 | Video height |
| `background` | string | No | '#0e0e0e' | Background color |
| `controls` | boolean | No | true | Show play/pause/seek controls |

---

## Subtitle System (Bilibili Style)

**Visual spec**:
- Text: `#1a1a1a` (dark ink) on light background
- Background: transparent with layered white glow (no box)
- Font: 32px sans-serif
- Position: bottom 90px (not edge-bound)
- Max characters: ≤13 Chinese characters per line

**splitChunkToLines algorithm**:
1. Split by sentence endings first: 。！？ 
2. Then merge by clause separators: ，、；：
3. Mixed English: count English as 0.5 character width
4. **Never cross sentence boundaries** — if a chunk crosses, split it

**Example**:
```
Input: "LLM全称Large Language Model，它是一个有几千亿参数的神经网络。"
Output:
  - "LLM全称Large"
  - "Language Model"
  - "它是一个有"
  - "几千亿参数"
  - "的神经网络"
```

---

## Standard Workflow (10 Steps)

1. **Write script** — Markdown file with `## scene-id` sections + `[[cue:id]]` markers
2. **Run narrate-pipeline** — `node scripts/narrate-pipeline.mjs --script demo.md --out-dir _narration`
3. **Verify timeline** — Check totalDuration, scenes, cues in timeline.json
4. **Answer 3 iron rules** — (1) What's the hero element? (2) How does it morph across 7 scenes? (3) Does every frame have motion?
5. **Create HTML** — Use NarrationStage + hero as child (NOT inside Scene)
6. **Implement cues** — Use `<Cue id="xxx">` for animation triggers
7. **Add subtitles** — Use timeline.chunks for subtitle display
8. **Test in browser** — Play audio, verify timing
9. **Record silent MP4** — `node scripts/render-video.js demo.html --duration=180`
10. **Mix voiceover** — `bash scripts/mix-voiceover.sh demo.mp4 --voiceover=_narration/voiceover.mp3`

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "TTS failed: 401" | Invalid API key | Check DOUBAO_TTS_API_KEY in .env |
| "voiceover.mp3 not found" | Pipeline not run | Run narrate-pipeline.mjs first |
| "scene not found" | Script scene ID mismatch | Ensure `## scene-id` matches timeline |
| "Subtitle overflow" | Text too long | Adjust splitChunkToLines algorithm |
| "Motion stops" | No subtle animation | Add breathing/pulse in idle frames |

---

## Quick Reference

```bash
# Generate voiceover + timeline
node scripts/narrate-pipeline.mjs --script demo.md --out-dir _narration

# Record video (silent)
node scripts/render-video.js demo.html --duration=180 --width=1920 --height=1080

# Mix voiceover + optional BGM
bash scripts/mix-voiceover.sh demo.mp4 --voiceover=_narration/voiceover.mp3 --bgm-mood=educational

# One-liner: script → video → final MP4
bash scripts/render-narration.sh demo.html --timeline=_narration/timeline.json
```

**Required env vars** (in .env):
```
DOUBAO_TTS_API_KEY=your_api_key
DOUBAO_TTS_VOICE_ID=your_voice_id
```