#!/bin/bash
# verify-video.sh — Hard verification of the rendered artifact (PASS/FAIL, no agent eyeballing)
#
# Checks: resolution/fps, duration error, audio stream presence, leading/trailing black frames, LUFS loudness, file size
# Composition-side checks (lint/layout/motion/contrast) are handled by hyperframes check; this script only covers the artifact.
#
# Usage:
#   bash verify-video.sh video.mp4 [--duration=10] [--fps=60] [--width=1920] [--height=1080]
#                        [--no-audio]        # an intermediate artifact that deliberately has no audio; skips the audio+loudness checks
#                        [--allow-black-open] # skip the head-black-frame check when the video deliberately opens on black
#
# Exit code: 0 = all PASS; 1 = at least one FAIL

set -u
FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: bash verify-video.sh video.mp4 [--duration=N] [--fps=N] [--width=N] [--height=N] [--no-audio] [--allow-black-open]"
  exit 1
fi
shift || true

EXP_DURATION=""; EXP_FPS=""; EXP_W=""; EXP_H=""; NO_AUDIO=0; ALLOW_BLACK_OPEN=0
for a in "$@"; do
  case "$a" in
    --duration=*) EXP_DURATION="${a#*=}" ;;
    --fps=*)      EXP_FPS="${a#*=}" ;;
    --width=*)    EXP_W="${a#*=}" ;;
    --height=*)   EXP_H="${a#*=}" ;;
    --no-audio)   NO_AUDIO=1 ;;
    --allow-black-open) ALLOW_BLACK_OPEN=1 ;;
  esac
done

FAILS=0
pass() { echo "  ✓ PASS  $1"; }
fail() { echo "  ✗ FAIL  $1"; FAILS=$((FAILS+1)); }
warn() { echo "  ⚠ WARN  $1"; }

echo "▸ verify-video: $FILE"

# ---------- Basic stream info ----------
INFO=$(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,avg_frame_rate -show_entries format=duration,size -of default=noprint_wrappers=1 "$FILE" 2>/dev/null)
W=$(echo "$INFO" | grep '^width=' | cut -d= -f2)
H=$(echo "$INFO" | grep '^height=' | cut -d= -f2)
FPS_RAW=$(echo "$INFO" | grep '^avg_frame_rate=' | cut -d= -f2)
DUR=$(echo "$INFO" | grep '^duration=' | cut -d= -f2)
SIZE=$(echo "$INFO" | grep '^size=' | cut -d= -f2)
FPS=$(python3 -c "print(round(eval('${FPS_RAW:-0}' if '${FPS_RAW:-0}'!='0/0' else '0'),2))" 2>/dev/null || echo "?")

[ -z "$W" ] && { fail "Cannot read video stream (file corrupt or not a video)"; echo "✗ 1 FAIL"; exit 1; }
echo "  info: ${W}x${H} · ${FPS}fps · ${DUR%.*}s · $((SIZE/1024))KB"

# ---------- Resolution / fps ----------
if [ -n "$EXP_W" ]; then
  [ "$W" = "$EXP_W" ] && [ "$H" = "$EXP_H" ] && pass "Resolution ${W}x${H}" || fail "Resolution ${W}x${H}, expected ${EXP_W}x${EXP_H}"
fi
if [ -n "$EXP_FPS" ]; then
  python3 -c "exit(0 if abs($FPS-$EXP_FPS)<=0.5 else 1)" 2>/dev/null && pass "Frame rate ${FPS}fps" || fail "Frame rate ${FPS}fps, expected ${EXP_FPS}fps"
fi

# ---------- Duration error (±2% or ±0.2s, whichever is larger) ----------
if [ -n "$EXP_DURATION" ]; then
  python3 -c "
d=float('$DUR'); e=float('$EXP_DURATION')
tol=max(e*0.02,0.2)
exit(0 if abs(d-e)<=tol else 1)" 2>/dev/null && pass "Duration ${DUR%.*}s (expected ${EXP_DURATION}s)" || fail "Duration ${DUR}s, expected ${EXP_DURATION}s (2% tolerance)"
fi

# ---------- audio stream ----------
HAS_AUDIO=$(ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "$FILE" 2>/dev/null | head -1)
if [ "$NO_AUDIO" = "1" ]; then
  [ -z "$HAS_AUDIO" ] && pass "No audio track (--no-audio intermediate artifact)" || warn "--no-audio declared but an audio track exists"
else
  if [ -n "$HAS_AUDIO" ]; then
    pass "audio stream present"
    # ---------- LUFS loudness (final reference: -14 LUFS ±4) ----------
    LUFS=$(ffmpeg -i "$FILE" -af loudnorm=print_format=summary -f null - 2>&1 | grep 'Input Integrated' | grep -oE '\-?[0-9]+\.?[0-9]*')
    if [ -n "$LUFS" ]; then
      python3 -c "exit(0 if -18<=float('$LUFS')<=-10 else 1)" 2>/dev/null \
        && pass "Loudness ${LUFS} LUFS (target range -18 to -10)" \
        || warn "Loudness ${LUFS} LUFS is outside the -14±4 range; check the mix gain"
    fi
  else
    fail "No audio stream — skill iron rule: the default animation deliverable is an MP4 with SFX+BGM; silent = half-finished"
  fi
fi

# ---------- Leading/trailing black frames ----------
BLACK=$(ffmpeg -i "$FILE" -vf "blackdetect=d=0.1:pix_th=0.10" -an -f null - 2>&1 | grep -oE 'black_start:[0-9.]+ black_end:[0-9.]+' )
if [ -n "$BLACK" ]; then
  HEAD_BLACK=$(echo "$BLACK" | awk -F'[: ]' '$2<0.3{print}' | head -1)
  TOTAL=${DUR%.*}
  TAIL_BLACK=$(echo "$BLACK" | awk -F'[: ]' -v t="$TOTAL" '$4>t-0.3{print}' | head -1)
  if [ -n "$HEAD_BLACK" ] && [ "$ALLOW_BLACK_OPEN" = "0" ]; then
    fail "Head black frame ($HEAD_BLACK) — a classic symptom of a recording-start offset; for a deliberate black open use --allow-black-open"
  else
    [ -n "$HEAD_BLACK" ] && pass "Head black open (--allow-black-open declared)"
  fi
  [ -n "$TAIL_BLACK" ] && fail "Tail black frame ($TAIL_BLACK) — a classic symptom of loop jump-back or over-recorded duration"
  [ -z "$HEAD_BLACK" ] && [ -z "$TAIL_BLACK" ] && warn "Black-frame segments inside the video (ignore if this is a deliberate transition): $(echo "$BLACK" | head -2 | tr '\n' ' ')"
else
  pass "No black frames"
fi

# ---------- Summary ----------
echo ""
if [ "$FAILS" = "0" ]; then
  echo "◇ verify-video: all PASS"
  exit 0
else
  echo "✗ verify-video: ${FAILS} FAIL(s)"
  exit 1
fi
