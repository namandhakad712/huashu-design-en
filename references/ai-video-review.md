# AI Video Review Loop (scripts/cloud/ai-review-video.py)

> The final-render MP4 is fed to a video understanding model (seed-2.0-lite), which produces a structured review report against a fixed checklist.
> Positioning: the **last quality gate after final render, before delivery**, replacing manual full re-watching. It does not replace frame-by-frame verify-video.sh.
> ⚠️ Optional cloud capability: the compressed video segments are sent to the official Volcano Ark API (ark.cn-beijing.volces.com),
> using your own ARK_API_KEY, requiring explicit confirmation via `--yes` or `HUASHU_CLOUD_OK=1`. See `SECURITY.md` in the repo root.
> Don't want the cloud: `scripts/verify-video.sh` extracts frames for manual review, fully local.

## When to use

- After the final 60fps render is out, run it once before delivery/mixing
- Run it again once the SFX mix is out (onset cross-check only applies when an audio track exists)
- Re-check after re-rendering to fix major issues
- Don't run it at the 30fps test-render stage (resolution/pacing not finalized — wasteful API calls)

## How to use

```bash
cd <project-dir> && unset ALL_PROXY   # script is already proxy-immune; unset is a double safeguard
uv run ~/.claude/skills/huashu-design/scripts/cloud/ai-review-video.py \
  --video <final>.mp4 \
  --context <director-notes>.md \      # highly recommended: the model uses it to distinguish "design intent" from "bug"
  --yes                      # confirm sending video segments to Volcano Ark (or HUASHU_CLOUD_OK=1)
```

- Configure ARK_API_KEY in the `.env` file at the skill root (already gitignored) or as an environment variable; the script only reads this one variable

- The report is saved next to the video: `<video-name>-AI-review.md` (`--output` to change)
- `--segment-len` defaults to 60-second segments; `--model` defaults to doubao-seed-2-0-lite-260215
- Measured on a 210-second video: 6 API calls, 6-10 minutes, ~180k tokens in / 20k out (lite tier, cost at the penny level)

## Call pipeline (three layers, not pure model)

1. **ffmpeg objective detection** (deterministic, misses nothing):
   - `silencedetect` → SFX onset timeline (the model **cannot hear** the video's audio track, verified 2026-07-17)
   - `freezedetect` → list of fully static segments ≥3s
2. **Model reviews segment by segment**: each 60s segment is compressed and submitted for review (1280 wide/15fps/crf28, ~0.5MB/minute for flat animation); each segment's prompt contains the checklist + director's notes + that segment's onset/static-segment data, with timestamps converted to original-video time
3. **Model low-res full-video pass**: the whole video is submitted separately at 960 wide/10fps, specifically checking cross-segment narrative coherence / hero continuity / overall pacing
4. A text summarization call merges items ①-⑧; per-segment raw records + objective detection data are all retained in the report appendix

## Checklist and severity

① black frames / incomplete render ② text cropping/typos ③ overlapping/occluding elements ④ narrative coherence (transitions identified using camera-language.md §7's three-layer vocabulary: six forms [white-flow / black-dip / defocus-relay / black-title-card / whip-pan / mask-wipe], hidden-cut, travel [shared-element reset / letter-counter traversal]; a bare cut = unwrapped hard cut, recorded as ⚡)
⑤ hero continuity ⑥ pacing dead segments (objective checklist + model judgment on whether it's a deliberate hold or genuinely dead) ⑦ SFX cueing (onset + on-screen event cross-check) ⑧ imbalanced composition / empty space

⚠️ fatal = must fix before delivery | ⚡ important = noticeably impairs viewing | 💡 suggestion = nice to have

## Limitations (read before using the report)

- **The model cannot hear audio**: ⑦ is a one-way check of "whether the frame has an event at the track's onset moment"; it cannot judge whether the right SFX was chosen, whether the volume is right, or whether the BGM mood is right
- **Cannot see frame-level detail**: 1-2 frame flickers, subtle jitter, precise color-value deviations, and sub-pixel alignment are missed; these still rely on frame extraction from verify-video.sh for manual review
- **Transition-type judgments lean strict**: after compressing to 15fps, a fast crossfade may be reported as a "hard cut"; when the segment and full-video passes contradict, the summary marks the item "inconclusive" — extract frames to confirm any inconclusive item before changing it
- **"Deliberate hold vs dead segment" is the model's opinion**: long holds where b-roll pads voiceover are often let through; when watching the final film on its own, judge these yourself
- Call failures (network/key/quota) are written honestly into the report header; the review results are never fabricated, and the time range of a failed segment is flagged

## Measured baseline

First run target: B00-first-3-minutes-mainline-SFX.mp4 (210s). The model independently spotted the inter-act transition problem and pointed in the right direction on the hero breakpoint, but misreported fades as hard cuts; pure-model dead-segment detection only hit 3/14, and after wiring in freezedetect it covered everything. Conclusion: the objective detection layer is the lower-bound guarantee of this loop, while the model handles semantic judgment.
