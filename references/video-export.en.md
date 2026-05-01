# Video Export: HTML Animation Export to MP4/GIF

After animation HTML is complete, users often ask "can I export video?" This guide gives the complete process.

## When to Export

**Export timing**:
- Animation fully runs through, visual verified (Playwright screenshot confirms each time point correct)
- User has watched in browser at least once, indicated effect OK
- **Don't** export while animation bugs not fixed — changes cost more after exporting to video

**Trigger phrases user might say**:
- "Can you export as video"
- "Convert to MP4"
- "Make a GIF"
- "60fps"

## Output Specs

Default give three formats at once, let user choose:

| Format | Spec | Suitable Scenario | Typical Size (30s) |
|---|---|---|---|
| MP4 25fps | 1920×1080 · H.264 · CRF 18 | WeChat embed, Video号, YouTube | 1-2 MB |
| MP4 60fps | 1920×1080 · minterpolate interpolation · H.264 · CRF 18 | High framerate display, Bilibili, portfolio | 1.5-3 MB |
| GIF | 960×540 · 15fps · palette optimized | Twitter/X, README, Slack preview | 2-4 MB |

## Toolchain

Two scripts in `scripts/`:

### 1. `render-video.js` — HTML → MP4

Record a 25fps MP4 base version. Depends on global playwright.

```bash
NODE_PATH=$(npm root -g) node /path/to/claude-design/scripts/render-video.js <html file>
```

Optional parameters:
- `--duration=30` animation duration (seconds)
- `--width=1920 --height=1080` resolution
- `--trim=2.2` seconds to trim from video start (remove reload + font load time)
- `--fontwait=1.5` font loading wait time (seconds), increase when many fonts

Output: Same directory as HTML, same name `.mp4`.

### 2. `add-music.sh` — MP4 + BGM → MP4

Mix background music into silent MP4, select from built-in BGM library by scene (mood), or bring own audio. Auto-match duration, add fade in/out.

```bash
bash add-music.sh <input.mp4> [--mood=<name>] [--music=<path>] [--out=<path>]
```

**Built-in BGM library** (in `assets/bgm-<mood>.mp3`):

| `--mood=` | Style | Fit Scenario |
|-----------|------|---------|
| `tech` (default) | Apple Silicon / Apple launch, minimal synth + piano | Product launch, AI tools, Skill promotion |
| `ad` | upbeat modern electronic, with build + drop | Social media ads, product teasers, promo |
| `educational` | warm bright, light guitar/electric piano, inviting | Science, tutorial intro, course preview |
| `educational_alt` | Same category alternate, try another | Same as above |
| `tutorial` | lo-fi ambient, almost unnoticeable | Software demo, coding tutorial, long demo |
| `tutorial_alt` | Same category alternate | Same as above |

**Behavior**:
- Music trimmed to video duration
- 0.3s fade in + 1s fade out (avoid hard cut)
- Video stream `-c:v copy` no re-encode, audio AAC 192k
- `--music=<path>` has higher priority than `--mood`, can specify any external audio
- Wrong mood name lists all available options, won't silently fail

**Typical pipeline** (animation export trio + soundtrack):
```bash
node render-video.js animation.html                        # Record
bash convert-formats.sh animation.mp4                      # Derive 60fps + GIF
bash add-music.sh animation-60fps.mp4                    # Add default tech BGM
# Or for different scenarios:
bash add-music.sh tutorial-demo.mp4 --mood=tutorial
bash add-music.sh product-promo.mp4 --mood=ad --out=promo-final.mp4
```

### 3. `convert-formats.sh` — MP4 → 60fps MP4 + GIF

Generate 60fps version and GIF from existing MP4.

```bash
bash /path/to/claude-design/scripts/convert-formats.sh <input.mp4> [gif_width] [--minterpolate]
```

Output (same directory as input):
- `<name>-60fps.mp4` — default uses `fps=60` frame copy (wide compatibility); add `--minterpolate` for high-quality interpolation
- `<name>.gif` — palette optimized GIF (default 960 width, can change)

**60fps mode selection**:

| Mode | Command | Compatibility | Use Scenario |
|---|---|---|---|
| Frame copy (default) | `convert-formats.sh in.mp4` | QuickTime/Safari/Chrome/VLC all pass | General delivery, upload platforms, social media |
| minterpolate interpolation | `convert-formats.sh in.mp4 --minterpolate` | macOS QuickTime/Safari may refuse | Bilibili etc needing true interpolation, **must test target player locally before delivery** |

Why changed default to frame copy? minterpolate output H.264 elementary stream has known compat bug — previously default minterpolate hit "macOS QuickTime won't open" issue multiple times. See `animation-pitfalls.md` §14.

`gif_width` parameter:
- 960 (default) — social platforms universal
- 1280 — clearer but larger
- 600 — Twitter/X priority loading

## Complete Process (Standard Recommendation)

After user says "export video":

```bash
cd <project directory>

# Assuming $SKILL points to this skill's root (replace according to your installation)

# 1. Record 25fps base MP4
NODE_PATH=$(npm root -g) node "$SKILL/scripts/render-video.js" my-animation.html

# 2. Derive 60fps MP4 and GIF
bash "$SKILL/scripts/convert-formats.sh" my-animation.mp4

# Output list:
# my-animation.mp4         (25fps · 1-2 MB)
# my-animation-60fps.mp4   (60fps · 1.5-3 MB)
# my-animation.gif         (15fps · 2-4 MB)
```

## Technical Details (for Troubleshooting)

### Playwright recordVideo pitfalls

- Frame rate fixed at 25fps, can't directly record 60fps (Chromium headless compositor ceiling)
- Starts recording from context creation, must use `trim` to cut loading time at start
- Default webm format, needs ffmpeg convert to H.264 MP4 for universal playback

`render-video.js` handles above.

### ffmpeg minterpolate parameters

Current config: `minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`

- `mi_mode=mci` — motion compensation interpolation
- `mc_mode=aobmc` — adaptive overlapped block motion compensation
- `me_mode=bidir` — bidirectional motion estimation
- `vsbmc=1` — variable size block motion compensation

Good for CSS **transform animations** (translate/scale/rotate).
For **pure fade** may produce slight ghosting — if user complains, degrade to simple frame copy:

```bash
ffmpeg -i input.mp4 -r 60 -c:v libx264 ... output.mp4
```

### Why GIF palette needs two passes

GIF only has 256 colors. Single-pass GIF compresses entire animation colors to 256-color universal palette, for beige bottom + orange delicate color combo will be blurry.

Two passes:
1. `palettegen=stats_mode=diff` — scan whole clip first, generate **optimal palette for this animation**
2. `paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle` — encode with this palette, rectangle diff only updates changed areas, significantly reduces file

For fade transitions, `dither=bayer` is smoother than `none`, but file slightly larger.

## Pre-flight Check (Before Export)

30-second self-check before export:

- [ ] HTML fully runs in browser, no console errors
- [ ] Animation frame 0 is complete initial state (not blank loading)
- [ ] Animation last frame is stable ending (not half-cut)
- [ ] Fonts/images/emoji all render correctly (reference `animation-pitfalls.md`)
- [ ] Duration parameter matches actual animation duration in HTML
- [ ] HTML Stage detects `window.__recording` forces loop=false (must check for hand-written Stage; `assets/animations.jsx` has this built-in)
- [ ] End Sprite has `fadeOut={0}` (video last frame doesn't fade out)
- [ ] Has "Created by Huashu-Design" watermark (must add for animation scenarios; third-party brand work adds "非官方出品 · " prefix. See SKILL.md § "Skill Promotion Watermark")

## Delivery Notes

Standard format to user after export complete:

```
**Complete Delivery**

| File | Format | Spec | Size |
|---|---|---|---|
| foo.mp4 | MP4 | 1920×1080 · 25fps · H.264 | X MB |
| foo-60fps.mp4 | MP4 | 1920×1080 · 60fps (motion interpolation) · H.264 | X MB |
| foo.gif | GIF | 960×540 · 15fps · palette optimized | X MB |

**Notes**
- 60fps uses minterpolate for motion estimation interpolation, good for transform animations
- GIF uses palette optimization, 30s animation can compress to ~3MB

Let me know if you want different sizes or frame rates.
```

## Common User Follow-up Requests

| User Says | Response |
|---|---|
| "Too large" | MP4: raise CRF to 23-28; GIF: lower resolution to 600 or fps to 10 |
| "GIF too blurry" | Raise `gif_width` to 1280; or suggest MP4 instead (WeChat Moments also supports) |
| "Need vertical 9:16" | Change HTML source to `--width=1080 --height=1920`, re-record |
| "Add watermark" | ffmpeg add `-vf "drawtext=..."` or `overlay=` a PNG |
| "Need transparent background" | MP4 doesn't support alpha; use WebM VP9 + alpha or APNG |
| "Want lossless" | Change CRF to 0 + preset veryslow (file will be 10× larger) |