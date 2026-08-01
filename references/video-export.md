# Video Export: Exporting HTML Animations to MP4/GIF

Once an HTML animation is complete, users often ask, "Can you export it as a video?" This guide covers the full workflow.

## When to Export

**When to export**:
- The animation runs fully through and has been visually verified (Playwright screenshots confirm the state is correct at each time point)
- The user has watched it in the browser at least once and confirmed it looks OK
- **Do not** export while animation bugs are still unfixed — changes are far more expensive once it's a video

**Trigger phrases users might say**:
- "Can you export it as a video?"
- "Convert it to MP4"
- "Make it a GIF"
- "60fps"

## Output Specs

By default, produce all three formats at once and let the user choose:

| Format | Specs | Best for | Typical size (30s) |
|---|---|---|---|
| MP4 25fps | 1920×1080 · H.264 · CRF 18 | WeChat official-account embeds, Channels, YouTube | 1-2 MB |
| MP4 60fps | 1920×1080 · default frame copy (stable compatibility) · H.264 · CRF 18; high-quality interpolation requires explicit `--minterpolate`; for Stage-clock-driven animations use render-video-seek.js to record true native 60fps | High-frame-rate showcases, Bilibili, portfolios | 1.5-3 MB |
| GIF | 960×540 · 15fps · palette-optimized | Twitter/X, README, Slack previews | 2-4 MB |

## Toolchain

Two scripts live in `scripts/`:

### 1. `render-video.js` — HTML → MP4

Records a 25fps base MP4. Depends on the global playwright.

```bash
NODE_PATH=$(npm root -g) node /path/to/claude-design/scripts/render-video.js <html-file>
```

Optional arguments:
- `--duration=30` animation duration (seconds)
- `--width=1920 --height=1080` resolution
- `--trim=2.2` seconds trimmed from the start of the video (removes reload + font-loading time)
- `--fontwait=1.5` font-loading wait time (seconds); increase if there are many fonts

Output: a `.mp4` with the same name, in the same directory as the HTML.

### 2. `add-music.sh` — MP4 + BGM → MP4

Mixes background music into a silent MP4. Pick a track from the built-in BGM library by scene (mood), or supply your own audio. It auto-matches duration and adds fade in/out.

```bash
bash add-music.sh <input.mp4> [--mood=<name>] [--music=<path>] [--out=<path>]
```

**Built-in BGM library** (in `assets/bgm-<mood>.mp3`):

| `--mood=` | Style | Best for |
|-----------|------|---------|
| `tech` (default) | Apple Silicon / Apple keynote style, minimal synth + piano | Product launches, AI tools, Skill promotion |
| `ad` | Upbeat modern electronic with a build + drop | Social media ads, product teasers, promos |
| `educational` | Warm and bright, light guitar / electric piano, inviting | Science explainers, tutorial intros, course teasers |
| `educational-alt` | Same category, alternate track to try | Same as above |
| `tutorial` | Lo-fi ambient, almost imperceptible | Software demos, coding tutorials, long recordings |
| `tutorial-alt` | Same category, alternate track | Same as above |

**Behavior**:
- Music is trimmed to the video duration
- 0.3s fade in + 1s fade out (avoids hard cuts)
- Video stream is `-c:v copy` (no re-encode); audio is AAC 192k
- `--music=<path>` takes precedence over `--mood`; you can point to any external audio directly
- An invalid mood name lists all available options instead of failing silently

**Typical pipeline** (the three export formats + soundtrack):
```bash
node render-video.js animation.html                        # record the video
bash convert-formats.sh animation.mp4                      # derive 60fps + GIF
bash add-music.sh animation-60fps.mp4                      # add the default tech BGM
# or per different use cases:
bash add-music.sh tutorial-demo.mp4 --mood=tutorial
bash add-music.sh product-promo.mp4 --mood=ad --out=promo-final.mp4
```

### 3. `convert-formats.sh` — MP4 → 60fps MP4 + GIF

Generates a 60fps version and a GIF from an existing MP4.

```bash
bash /path/to/claude-design/scripts/convert-formats.sh <input.mp4> [gif_width] [--minterpolate]
```

Output (same directory as the input):
- `<name>-60fps.mp4` — frame copy at `fps=60` by default (broad compatibility); add `--minterpolate` to enable high-quality interpolation
- `<name>.gif` — a palette-optimized GIF (960 wide by default; adjustable)

**Choosing a 60fps mode**:

| Mode | Command | Compatibility | Use cases |
|---|---|---|---|
| Frame copy (default) | `convert-formats.sh in.mp4` | Works everywhere: QuickTime/Safari/Chrome/VLC | General delivery, upload platforms, social media |
| minterpolate interpolation | `convert-formats.sh in.mp4 --minterpolate` | May be rejected by macOS QuickTime/Safari | Showcase scenarios like Bilibili that need real interpolation; **test the target player locally before delivery** |

Why did the default switch to frame copy? The H.264 elementary stream that minterpolate produces has a known compat bug — when minterpolate was the default, we repeatedly hit "macOS QuickTime won't open it" issues. See `animation-pitfalls.md` §14 for details.

`gif_width` argument:
- 960 (default) — universal for social platforms
- 1280 — sharper but larger file
- 600 — Twitter/X loads it faster

### 4. `render-video-seek.js` — true 60fps / deterministic rendering (recommended for high-quality delivery)

The recordVideo path in `render-video.js` has three inherent limitations: the frame rate is locked to 25fps by the Chromium compositor, the black loading frames at the start require trimming, and 60fps can only be achieved afterwards via minterpolate interpolation (which has ghosting + a macOS QuickTime compatibility bug, see `animation-pitfalls.md §14`). When you need **true 60fps, deterministic output, or Bilibili/portfolio delivery**, switch to seek rendering.

It seeks to a timestamp frame by frame, screenshots each, then encodes the PNG sequence into an MP4 with ffmpeg. The core technique borrows the "frozen clock + seek screenshot" approach from HeyGen HyperFrames (Apache 2.0), but without pulling in any third-party packages — it only uses the playwright + ffmpeg already present in this skill, so it stays runtime-neutral.

```bash
NODE_PATH=$(npm root -g) node /path/to/claude-design/scripts/render-video-seek.js <html-file> --fps=60
```

Arguments: `--duration` · `--fps` (default 60) · `--width` · `--height` · `--concurrency` (default: 4 parallel workers) · `--settle` (how many rAFs to wait after seeking before screenshotting; default 2, raise it for layout-heavy animations) · `--keep-chrome`. Output is a `.mp4` with the same name, in the same directory as the HTML.

It directly solves all three recordVideo dead ends:
- **True native frame rate at any value**: `--fps=60` produces true 60fps (every frame is a real seek capture), no longer going through `convert-formats.sh`'s minterpolate interpolation, sidestepping the ghosting + macOS compatibility bug
- **No black frames at the start**: there's no screen recording, so there are no loading-period black frames at all; no `--trim` / `--fontwait` needed
- **Deterministic**: screenshots taken after seeking to a timestamp give the same output for the same input, unaffected by machine load or dropped frames

**Applicability boundary (important)**: only animations driven by a Stage clock are supported — the `<Stage>` from `assets/animations.jsx` or the `<NarrationStage>` from `narration_stage.jsx`, which respond to `window.__seekRender` to freeze their self-running clock and expose `window.__seek(t)`. Pure CSS `@keyframes` / Lottie / hand-written non-Stage animations don't respond to `__seek`; keep using `render-video.js` for those (the script errors and prompts if it can't detect `__seek`).

**Trade-offs**: because it screenshots frame by frame, long videos can take longer overall than recordVideo's real-time capture (mitigated by the multi-worker `--concurrency`); many temporary PNGs consume disk space, so consider closing other memory-heavy apps before rendering.

**Picking one of the two**: keep `render-video.js` as the default (zero risk, covers every animation type); when you need true 60fps / deterministic / high-quality delivery and the animation runs on a Stage clock, use `render-video-seek.js`. For long narrated animations, `render-narration.sh --seek` runs seek rendering + audio mixing in one go.

## Full Workflow (Standard Recommendation)

After the user says "export the video":

```bash
cd <project-directory>

# Assuming $SKILL points to this skill's root (replace per your install location)

# 1. Record the 25fps base MP4
NODE_PATH=$(npm root -g) node "$SKILL/scripts/render-video.js" my-animation.html

# 2. Derive the 60fps MP4 and GIF
bash "$SKILL/scripts/convert-formats.sh" my-animation.mp4

# Output list:
# my-animation.mp4         (25fps · 1-2 MB)
# my-animation-60fps.mp4   (60fps · 1.5-3 MB)
# my-animation.gif         (15fps · 2-4 MB)
```

## Technical Details (for Troubleshooting)

### Playwright recordVideo gotchas

- Frame rate is fixed at 25fps; 60fps can't be recorded directly (Chromium headless compositor limit)
- Recording starts when the context is created, so `trim` must be used to cut the initial loading time
- Output is webm by default; ffmpeg must convert it to H.264 MP4 for universal playback

`render-video.js` already handles all of the above.

### ffmpeg minterpolate parameters

Current configuration: `minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1`

- `mi_mode=mci` — motion compensation interpolation
- `mc_mode=aobmc` — adaptive overlapped block motion compensation
- `me_mode=bidir` — bidirectional motion estimation
- `vsbmc=1` — variable-size block motion compensation

Works well for CSS **transform animations** (translate/scale/rotate).
For **pure fade** it may produce slight ghosting — if the user minds it, fall back to simple frame copy:

```bash
ffmpeg -i input.mp4 -r 60 -c:v libx264 ... output.mp4
```

### Why GIF palette needs two passes

GIF only supports 256 colors. A single-pass GIF compresses the entire animation's colors into one generic 256-color palette, which muddies delicate palettes like a beige background with orange accents.

Two passes:
1. `palettegen=stats_mode=diff` — scans the whole clip first and generates an **optimal palette specific to this animation**
2. `paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle` — encodes with this palette; rectangle diff only updates the changed regions, shrinking the file substantially

For fade transitions, `dither=bayer` is smoother than `none`, at the cost of a slightly larger file.

## Pre-flight Check (Before Export)

A 30-second self-check before exporting:

- [ ] The HTML ran through completely in a browser, with no console errors
- [ ] Frame 0 of the animation is the full initial state (not an empty loading state)
- [ ] The animation's last frame is a stable end state (not cut off mid-way)
- [ ] Fonts/images/emoji all render correctly (see `animation-pitfalls.md`)
- [ ] The duration argument matches the actual animation length in the HTML
- [ ] The Stage in the HTML checks `window.__recording` to force loop=false (must verify for hand-written Stages; built-in when using `assets/animations.jsx`)
- [ ] The final Sprite has `fadeOut={0}` (the video's last frame doesn't fade out)
- [ ] Contains the "Created by Huashu-Design" watermark (required for animation projects only; add the "Unofficial · " prefix for third-party brand work. See the "Skill promo watermark" section in SKILL.md)

## Notes to Include with Delivery

The standard note format to give the user after export:

```
**Complete Delivery**

| File | Format | Specs | Size |
|---|---|---|---|
| foo.mp4 | MP4 | 1920×1080 · 25fps · H.264 | X MB |
| foo-60fps.mp4 | MP4 | 1920×1080 · 60fps (frame copy by default; interpolated versions will be noted) · H.264 | X MB |
| foo.gif | GIF | 960×540 · 15fps · palette-optimized | X MB |

**Notes**
- 60fps uses frame copy by default (best compatibility); minterpolate interpolation is used only when explicitly requested (great for transform animations, though complex scenes are prone to artifacts); for true 60fps, use render-video-seek.js for direct per-frame seek recording
- GIFs are palette-optimized, so a 30s animation can be compressed to about 3MB

Let me know if you want a different size or frame rate.
```

## Common Follow-up Requests

| If the user says | How to respond |
|---|---|
| "Too large" | MP4: raise CRF to 23-28; GIF: lower resolution to 600 or fps to 10 |
| "GIF too blurry" | Raise `gif_width` to 1280; or suggest MP4 instead (WeChat Moments also supports it) |
| "Need vertical 9:16" | Change the HTML source's `--width=1080 --height=1920` and re-record |
| "Add a watermark" | Use ffmpeg's `-vf "drawtext=..."` or `overlay=` a PNG |
| "Need a transparent background" | MP4 doesn't support alpha; use WebM VP9 + alpha or APNG |
| "Want lossless" | Set CRF to 0 + preset veryslow (file will be ~10x larger) |

## Skill Promo Watermark Template (for Animation Exports Only)

SKILL.md requires animation MP4s/GIFs to carry the watermark by default. Template below (use `rgba(255,255,255,0.35)` on dark backgrounds; third-party brand animations get the "Unofficial · " prefix):

```jsx
<div style={{
  position: 'absolute', bottom: 24, right: 32,
  fontSize: 11, color: 'rgba(0,0,0,0.4)',
  letterSpacing: '0.15em', fontFamily: 'monospace',
  pointerEvents: 'none', zIndex: 100,
}}>
  Created by Huashu-Design
</div>
```
