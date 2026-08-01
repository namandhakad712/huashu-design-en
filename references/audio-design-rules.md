# Audio Design Rules · huashu-design

> The audio recipe for every animation demo. Use together with `sfx-library.md` (the asset list).
> Battle-tested: huashu-design release hero v1–v9 iterations · a deep Gemini teardown of Anthropic's three official videos · 8000+ A/B comparisons

---

## Core Principle · The Dual-Track Audio System (Iron Law)

Animation audio **must be designed as two independent layers** — you can't get away with just one:

| Layer | Role | Time scale | Relationship to visuals | Frequency band |
|---|---|---|---|---|
| **SFX (beat layer)** | Marks every visual beat | 0.2–2s, short and punchy | **Tight sync** (frame-aligned) | **High frequencies, 800Hz+** |
| **BGM (ambient bed)** | Emotional foundation, soundstage | Continuous, 20–60s | Loose sync (section-level) | **Mid–low frequencies, <4kHz** |

**An animation with only BGM is crippled** — the audience subconsciously registers "the picture moves but nothing responds in sound", and that is the root of the cheap feel.

---

## Gold Standard · The Golden Ratio

These values are **hard engineering parameters** derived from measuring Anthropic's three official videos and comparing against our own v9 final cut — apply them directly:

### Volume
- **BGM volume**: `0.40–0.50` (relative to full scale 1.0)
- **SFX volume**: `1.00`
- **Loudness difference**: BGM sits **6–8 dB below** the SFX peak (prominence comes from the loudness gap, not from the SFX's absolute loudness)
- **amix setting**: `normalize=0` (never use normalize=1 — it flattens the dynamic range)

### Frequency-Band Isolation (P1 Hard Optimization)
Anthropic's secret isn't "loud SFX" — it's **frequency layering**:

```bash
[bgm_raw]lowpass=f=4000[bgm]      # BGM limited to the <4kHz mid–low band
[sfx_raw]highpass=f=800[sfx]      # SFX pushed up into the 800Hz+ mid–high band
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]
```

Why: the human ear is most sensitive around 2–5kHz (the so-called "presence band"). If the SFX all sit in that range and the BGM covers the full band, **the SFX gets masked by the BGM's high frequencies**. Push the SFX up with a highpass and pull the BGM down with a lowpass so each owns its slice of the spectrum, and SFX clarity jumps a full tier.

### Fades
- BGM in: `afade=in:st=0:d=0.3` (0.3s, avoids a hard cut)
- BGM out: `afade=out:st=N-1.5:d=1.5` (1.5s tail for a sense of closure)
- SFX has its own built-in envelope; no extra fade needed

---

## SFX Cue Design Rules

### Density (SFX per 10 seconds)
Measured across Anthropic's three videos, SFX density falls into three tiers:

| Video | SFX per 10s | Product personality | Scenario |
|---|---|---|---|
| Artifacts (ref-1) | **~9 per 10s** | Feature-dense, information-heavy | Complex tool demos |
| Code Desktop (ref-2) | **0** | Pure atmosphere, meditative | Dev tool in a focused state |
| Word (ref-3) | **~4 per 10s** | Balanced, office rhythm | Productivity tools |

**Heuristics**:
- Calm / focused product personality → low SFX density (0–3 per 10s), BGM carries the load
- Lively / information-heavy personality → high SFX density (6–9 per 10s), SFX drives the rhythm
- **Don't fill every visual beat** — whitespace is more premium than density. **Cutting 30–50% of the cues makes the rest more dramatic**.

### Cue Selection Priority
Not every visual beat needs an SFX. Choose by this priority:

**P0 must-have** (skipping these feels off):
- Typing (terminal / input)
- Click / selection (moments of user decision)
- Focus switch (when the visual protagonist changes)
- Logo reveal (brand closure)

**P1 recommended**:
- Element enter/exit (modal / card)
- Completion / success feedback
- AI generation start/end
- Major transitions (scene switches)

**P2 optional** (too many gets cluttered):
- hover / focus-in
- Progress ticks
- Decorative ambient

### Timestamp Alignment Precision
- **Same-frame alignment** (0ms error): clicks / focus switches / logo landings
- **1–2 frames early** (-33ms): fast whooshes (to give the audience psychological anticipation)
- **1–2 frames late** (+33ms): object landings / impacts (matches real physics)

---

## BGM Selection Decision Tree

The huashu-design skill ships with 6 BGM tracks (`assets/bgm-*.mp3`):

```
What's the animation's personality?
├─ Product launch / tech demo → bgm-tech.mp3 (minimal synth + piano)
├─ Tutorial / tool usage → bgm-tutorial.mp3 (warm, instructional)
├─ Education / explanations → bgm-educational.mp3 (curious, thoughtful)
├─ Marketing / brand promo → bgm-ad.mp3 (upbeat, promotional)
└─ Need a variant of the same style → bgm-*-alt.mp3 (alternate of each)
```

### Going Without BGM (Worth Considering)
See Anthropic's Code Desktop (ref-2): **0 SFX + pure lo-fi BGM** can be just as premium.

**When to skip BGM**:
- Animation is shorter than 10s (BGM never gets established)
- The product personality is "focused / meditative"
- The scene already has ambient sound or a voiceover
- SFX density is already high (avoids auditory overload)

---

## Scene Recipes (Ready to Use)

### Recipe A · Product Launch Hero (the same as huashu-design v9)
```
Duration: 25 seconds
BGM: bgm-tech.mp3 · 45% · band <4kHz
SFX density: ~6 per 10s

cues:
  Terminal typing → type × 4 (0.6s intervals)
  Enter           → enter
  Cards converge  → card × 4 (staggered 0.2s)
  Selection       → click
  Ripple          → whoosh
  4 focus moments → focus × 4
  Logo            → thud (1.5s)

Volume: BGM 0.45 / SFX 1.0 · amix normalize=0
```

### Recipe B · Tool Feature Demo (modeled on Anthropic's Code Desktop)
```
Duration: 30–45 seconds
BGM: bgm-tutorial.mp3 · 50%
SFX density: 0–2 per 10s (very sparse)

Strategy: let BGM + the explanatory voiceover drive; SFX only at **decisive moments** (file saves / command completion)
```

### Recipe C · AI Generation Demo
```
Duration: 15–20 seconds
BGM: bgm-tech.mp3 or no BGM
SFX density: ~8 per 10s (high density)

cues:
  User input           → type + enter
  AI starts processing → magic/ai-process (1.2s loop)
  Generation complete  → feedback/complete-done
  Result presented     → magic/sparkle

Highlight: ai-process can loop 2–3 times across the whole generation process
```

### Recipe D · Pure-Atmosphere Long Shot (modeled on Artifacts)
```
Duration: 10–15 seconds
BGM: none
SFX: 3–5 carefully designed cues used on their own

Strategy: every SFX is the protagonist; no "muddying together" from BGM.
Good for: single-product slow motion, close-up showcases
```

---

## ffmpeg Composition Templates

### Template 1 · Overlay a Single SFX onto a Video
```bash
ffmpeg -y -i video.mp4 -itsoffset 2.5 -i sfx.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Template 2 · Multi-SFX Timeline Mix (aligned to cue times)
```bash
ffmpeg -y \
  -i sfx-type.mp3 -i sfx-enter.mp3 -i sfx-click.mp3 -i sfx-thud.mp3 \
  -filter_complex "\
[0:a]adelay=1100|1100[a0];\
[1:a]adelay=3200|3200[a1];\
[2:a]adelay=7000|7000[a2];\
[3:a]adelay=21800|21800[a3];\
[a0][a1][a2][a3]amix=inputs=4:duration=longest:normalize=0[mixed]" \
  -map "[mixed]" -t 25 sfx-track.mp3
```
**Key parameters**:
- `adelay=N|N`: the first value is the left-channel delay (ms), the second the right channel; specify both so the stereo stays aligned
- `normalize=0`: preserves the dynamic range — critical!
- `-t 25`: truncates to the specified duration

### Template 3 · Video + SFX Track + BGM (with frequency isolation)
```bash
ffmpeg -y -i video.mp4 -i sfx-track.mp3 -i bgm.mp3 \
  -filter_complex "\
[2:a]atrim=0:25,afade=in:st=0:d=0.3,afade=out:st=23.5:d=1.5,\
     lowpass=f=4000,volume=0.45[bgm];\
[1:a]highpass=f=800,volume=1.0[sfx];\
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k final.mp4
```

---

## Failure Mode Quick Reference

| Symptom | Root cause | Fix |
|---|---|---|
| SFX inaudible | BGM's high frequencies mask it | Add `lowpass=f=4000` to BGM + `highpass=f=800` to SFX |
| SFX too loud / harsh | SFX absolute volume too high | Drop SFX to 0.7 and BGM to 0.3, keeping the gap |
| BGM and SFX rhythms clash | Wrong BGM choice (music with a strong beat) | Switch to an ambient / minimal-synth BGM |
| BGM cuts off abruptly at the end | No fade-out | `afade=out:st=N-1.5:d=1.5` |
| SFX overlap into a blur | Cues too dense + each SFX too long | Keep SFX under 0.5s and cue spacing ≥ 0.2s |
| WeChat article MP4 has no sound | WeChat sometimes mutes autoplay | Don't worry — users get sound once they tap in; GIFs are silent anyway |

---

## Working with the Visuals (Advanced)

### SFX Timbre Should Match the Visual Style
- Warm beige / paper-feel visuals → **wooden / soft** SFX timbres (Morse, paper snap, soft click)
- Cold black tech visuals → **metallic / digital** SFX timbres (beep, pulse, glitch)
- Hand-drawn / playful visuals → **cartoonish / exaggerated** SFX timbres (boing, pop, zap)

Our current `apple-gallery-showcase.md` warm beige base → pair with `keyboard/type.mp3` (mechanical) + `container/card-snap.mp3` (soft) + `impact/logo-reveal-v2.mp3` (cinematic bass)

### SFX Can Drive the Visual Rhythm
Advanced trick: **design the SFX timeline first, then adjust the visual animation to align with it** (not the other way around).
Since every SFX cue is a "clock tick", a visual that adapts to the SFX rhythm locks in very solidly — the reverse, SFX chasing the visuals, often feels off by ±1 frame and starts to grate.

---

## Quality Checklist (Self-Check Before Shipping)

- [ ] Loudness gap: SFX peak − BGM peak = -6 to -8 dB?
- [ ] Frequency bands: BGM lowpass 4kHz + SFX highpass 800Hz?
- [ ] amix normalize=0 (dynamic range preserved)?
- [ ] BGM fade-in 0.3s + fade-out 1.5s?
- [ ] SFX count appropriate (density chosen for the scene's personality)?
- [ ] Every SFX frame-aligned with its visual beat (within ±1 frame)?
- [ ] Logo reveal sound long enough (1.5s recommended)?
- [ ] Mute the BGM and listen: does the SFX alone carry enough rhythm?
- [ ] Mute the SFX and listen: does the BGM alone have emotional contour?

Each layer, heard on its own, should be self-sufficient. If it only sounds good when both layers are stacked, you haven't done it right.

---

## References

- SFX asset list: `sfx-library.md`
- Visual style reference: `apple-gallery-showcase.md`
- Deep audio analysis of Anthropic's three videos: AUDIO-BEST-PRACTICES.md (the original author's local material, not distributed with the repository)
- huashu-design v9 case study: hero-animation-v9-final.mp4 (the original author's local sample, not distributed with the repository)
