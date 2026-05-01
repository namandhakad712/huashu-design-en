# Audio Design Rules · huashu-design

> All animation demos should use audio recipes. Use together with `sfx-library.md` (asset inventory).
> Battle-tested: huashu-design hero v1-v9 iteration · Anthropic three official videos' Gemini deep analysis · 8000+ A/B comparisons

---

## Core Principle · Audio Dual-Track System (Iron Law)

Animation audio **must be designed in two independent layers**, can't do just one:

| Layer | Function | Time Scale | Relationship to Visual | Frequency Band |
|---|---|---|---|---|
| **SFX (Rhythm Layer)** | Mark each visual beat | 0.2-2 seconds sharp | **Strong sync** (frame-level alignment) | **High frequency 800Hz+** |
| **BGM (Ambient Bed)** | Emotional bed, soundscape | Continuous 20-60 seconds | Weak sync (paragraph level) | **Mid-low frequency <4kHz** |

**Animations with only BGM are crippled** — audience subconsciously perceives "image moving but no sound response", that's the root of cheapness.

---

## Gold Standard · Golden Ratio

These values are **engineering hard parameters** from actual measurement of Anthropic three official videos + our v9 final version comparison, use directly:

### Volume
- **BGM volume**: `0.40-0.50` (relative to full scale 1.0)
- **SFX volume**: `1.00`
- **Loudness difference**: BGM **-6 to -8 dB** lower than SFX peak (don't rely on SFX absolute loudness for prominence, rely on loudness difference)
- **amix parameter**: `normalize=0` (never use normalize=1, compresses dynamic range flat)

### Frequency Band Isolation (P1 Hard Optimization)
Anthropic's secret isn't "SFX is loud", it's **frequency layering**:

```bash
[bgm_raw]lowpass=f=4000[bgm]      # BGM limited to <4kHz mid-low frequency
[sfx_raw]highpass=f=800[sfx]      # SFX pushed to 800Hz+ mid-high frequency
[bgm][sfx]amix=inputs=2:duration=first:normalize=0[a]
```

Why: Human ear most sensitive to 2-5kHz range (i.e., "presence frequency"), if SFX all in this range and BGM covers full band, **SFX gets masked by BGM's high frequency**. Using highpass to push SFX up + lowpass to push BGM down, both occupy their own spectrum side, SFX clarity goes up a level.

### Fade
- BGM in: `afade=in:st=0:d=0.3` (0.3s, avoid hard cut)
- BGM out: `afade=out:st=N-1.5:d=1.5` (1.5s long tail, sense of closure)
- SFX has built-in envelope, no extra fade needed

---

## SFX Cue Design Rules

### Density (SFX per 10 seconds)
Measured density in Anthropic three videos has three levels:

| Video | SFX per 10s | Product Personality | Scenario |
|---|---|---|---|
| Artifacts (ref-1) | **~9/10s** | Function-dense, information-heavy | Complex tool demo |
| Code Desktop (ref-2) | **0** | Pure atmosphere, meditative | Dev tool focused state |
| Word (ref-3) | **~4/10s** | Balanced, office rhythm | Productivity tool |

**Heuristic**:
- Product personality calm/focused → SFX density low (0-3/10s), BGM dominant
- Product personality lively/information-heavy → SFX density high (6-9/10s), SFX drives rhythm
- **Don't fill every visual beat** — whitespace is more premium than density. **Deleting 30-50% of cues makes remaining more dramatic**.

### Cue Selection Priority
Not every visual beat needs SFX. Select by this priority:

**P0 Must-have** (omission feels wrong):
- Typing (terminal/input)
- Click/selection (user decision moment)
- Focus switch (visual protagonist transfer)
- Logo reveal (brand closure)

**P1 Recommended**:
- Element enter/exit (modal/card)
- Completion/success feedback
- AI generation start/end
- Major transition (scene switch)

**P2 Optional** (too many gets messy):
- Hover/focus-in
- Progress tick
- Decorative ambient

### Timestamp Alignment Precision
- **Same-frame alignment** (0ms error): click/focus switch/logo land
- **1-2 frames ahead** (-33ms): fast whoosh (give audience psychological expectation)
- **1-2 frames behind** (+33ms): object landing/impact (matches real physics)

---

## BGM Selection Decision Tree

huashu-design skill comes with 6 BGM tracks (`assets/bgm-*.mp3`):

```
What's the animation personality?
├─ Product launch / tech demo → bgm-tech.mp3 (minimal synth + piano)
├─ Tutorial / tool usage → bgm-tutorial.mp3 (warm, instructional)
├─ Education / explanation → bgm-educational.mp3 (curious, thoughtful)
├─ Marketing / brand promo → bgm-ad.mp3 (upbeat, promotional)
└─ Need variant of same style → bgm-*-alt.mp3 (respective alternatives)
```

### Scenarios Without BGM (Worth Considering)
Reference Anthropic Code Desktop (ref-2): **0 SFX + pure Lo-fi BGM** can also be premium.

**When to choose no BGM**:
- Animation duration <10s (BGM can't establish)
- Product personality is "focus/meditative"
- Scene itself has ambient sound/voiceover
- SFX density is already high (avoid auditory overload)

---

## Scene Recipes (Ready to Use)

### Recipe A · Product Launch Hero (huashu-design v9 same)
```
Duration: 25 seconds
BGM: bgm-tech.mp3 · 45% · frequency <4kHz
SFX density: ~6/10s

cues:
  Terminal typing → type × 4 (0.6s interval)
  Enter         → enter
  Cards converge → card × 4 (staggered 0.2s)
  Selection     → click
  Ripple        → whoosh
  4 focuses     → focus × 4
  Logo          → thud (1.5s)

Volume: BGM 0.45 / SFX 1.0 · amix normalize=0
```

### Recipe B · Tool Feature Demo (Reference Anthropic Code Desktop)
```
Duration: 30-45 seconds
BGM: bgm-tutorial.mp3 · 50%
SFX density: 0-2/10s (very few)

Strategy: Let BGM + voiceover drive, SFX only at **decisive moments** (file save/command execution complete)
```

### Recipe C · AI Generation Demo
```
Duration: 15-20 seconds
BGM: bgm-tech.mp3 or no BGM
SFX density: ~8/10s (high density)

cues:
  User input   → type + enter
  AI starts    → magic/ai-process (1.2s loop)
  Generation complete → feedback/complete-done
  Result shows → magic/sparkle

Highlight: ai-process can loop 2-3 times throughout generation process
```

### Recipe D · Pure Atmosphere Long Shot (Reference Artifacts)
```
Duration: 10-15 seconds
BGM: none
SFX: individually use 3-5 carefully designed cues

Strategy: Each SFX is protagonist, no "muddled together" issue from BGM.
Suitable: Single product slow-motion, close-up showcase
```

---

## ffmpeg Composition Templates

### Template 1 · Single SFX overlay to video
```bash
ffmpeg -y -i video.mp4 -itsoffset 2.5 -i sfx.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:normalize=0[a]" \
  -map 0:v -map "[a]" output.mp4
```

### Template 2 · Multi SFX timeline composition (align by cue time)
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
- `adelay=N|N`: first is left channel delay (ms), second is right, write twice to ensure stereo alignment
- `normalize=0`: preserve dynamic range, key!
- `-t 25`: truncate to specified duration

### Template 3 · Video + SFX track + BGM (with frequency isolation)
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

| Symptom | Root Cause | Fix |
|---|---|---|
| SFX inaudible | BGM high frequency masks | Add `lowpass=f=4000` to BGM + `highpass=f=800` to SFX |
| SFX too loud/harsh | SFX absolute volume too large | Lower SFX to 0.7, also lower BGM to 0.3, maintain difference |
| BGM and SFX rhythm conflict | Wrong BGM (used music with strong beat) | Switch to ambient/minimal synth BGM |
| Animation ends BGM cuts suddenly | No fade out | `afade=out:st=N-1.5:d=1.5` |
| SFX overlaps becomes mud | cues too dense + each SFX too long | Control SFX duration within 0.5s, cue interval ≥ 0.2s |
| WeChat MP4 no sound | WeChat sometimes mutes auto-play | Don't worry, user gets sound when clicking; GIF has no sound anyway |

---

## Integration with Visual (Advanced)

### SFX timbre must match visual style
- Warm beige/paper visual → SFX use **wooden/soft** timbre (Morse, paper snap, soft click)
- Cold black tech visual → SFX use **metal/digital** timbre (beep, pulse, glitch)
- Hand-drawn/childlike visual → SFX use **cartoon/exaggerated** timbre (boing, pop, zap)

Our current `apple-gallery-showcase.md` warm beige background → pairs with `keyboard/type.mp3` (mechanical) + `container/card-snap.mp3` (soft) + `impact/logo-reveal-v2.mp3` (cinematic bass)

### SFX can guide visual rhythm
Advanced technique: **First design SFX timeline, then adjust visual animation to align with SFX** (not the other way around).
Because each SFX cue is a "clock tick", visual animation adapting to SFX rhythm is very stable — conversely SFX chasing visual, often ±1 frame off feels wrong.

---

## Quality Check List (Self-Check Before Release)

- [ ] Loudness difference: SFX peak - BGM peak = -6 to -8 dB?
- [ ] Frequency band: BGM lowpass 4kHz + SFX highpass 800Hz?
- [ ] amix normalize=0 (preserve dynamic range)?
- [ ] BGM fade-in 0.3s + fade-out 1.5s?
- [ ] SFX count appropriate (select density by scene personality)?
- [ ] Each SFX aligned with visual beat (within ±1 frame)?
- [ ] Logo reveal sound duration enough (recommend 1.5s)?
- [ ] Listen with BGM off: SFX alone rhythmic enough?
- [ ] Listen with SFX off: BGM alone has emotional variation?

Any single layer alone should be self-consistent. If only good when two layers combined, it's not done well.

---

## References

- SFX asset list: `sfx-library.md`
- Visual style reference: `apple-gallery-showcase.md`
- Anthropic three videos deep audio analysis: `/Users/alchain/Documents/写作/01-公众号写作/项目/2026.04-huashu-design发布/参考动画/AUDIO-BEST-PRACTICES.md`
- huashu-design v9实战 case: `/Users/alchain/Documents/写作/01-公众号写作/项目/2026.04-huashu-design发布/配图/hero-animation-v9-final.mp4`