#!/usr/bin/env bash
# mix-voiceover.sh · Mix a voiceover (main vocal track) + optional BGM into an MP4
#
# Usage:
#   bash mix-voiceover.sh <video.mp4> --voiceover=<voice.mp3> [options]
#
# Required:
#   --voiceover=<path>    Path to voiceover mp3 (main vocal track, from narrate-pipeline.mjs)
#
# Optional:
#   --bgm=<path>          BGM mp3 path (overrides --bgm-mood)
#   --bgm-mood=<name>     Pick a preset BGM from assets/ (educational / tech / tutorial / ...)
#   --bgm-volume=<0-1>    Static BGM volume, default 0.18 (relative to the voice)
#   --no-ducking          Disable sidechain ducking (on by default: BGM automatically yields while the voice is speaking)
#   --voice-volume=<0-2>  Voice volume multiplier, default 1.0
#   --out=<path>          Output path, default <input>-voiced.mp4
#
# Behavior:
#   - Video stream is stream-copied (no re-encode, fast)
#   - The voice is always the main track and is required; BGM is optional
#   - Ducking on by default: while the voice is speaking, BGM is compressed to about -10dB; it recovers when the voice pauses
#   - Output length = video length (if voice/BGM is shorter it gets trailing silence; if longer it is truncated)
#
# Examples:
#   bash mix-voiceover.sh anim.mp4 --voiceover=narration/voiceover.mp3
#   bash mix-voiceover.sh anim.mp4 --voiceover=v.mp3 --bgm-mood=educational
#   bash mix-voiceover.sh anim.mp4 --voiceover=v.mp3 --bgm=~/Music/song.mp3 --bgm-volume=0.12
#   bash mix-voiceover.sh anim.mp4 --voiceover=v.mp3 --bgm-mood=tech --no-ducking
#
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS_DIR="$SCRIPT_DIR/../assets"

INPUT=""
VOICEOVER=""
BGM=""
BGM_MOOD=""
BGM_VOLUME="0.18"
VOICE_VOLUME="1.0"
DUCKING="1"
OUTPUT=""

for arg in "$@"; do
  case "$arg" in
    --voiceover=*)    VOICEOVER="${arg#*=}" ;;
    --bgm=*)          BGM="${arg#*=}" ;;
    --bgm-mood=*)     BGM_MOOD="${arg#*=}" ;;
    --bgm-volume=*)   BGM_VOLUME="${arg#*=}" ;;
    --voice-volume=*) VOICE_VOLUME="${arg#*=}" ;;
    --no-ducking)     DUCKING="0" ;;
    --out=*)          OUTPUT="${arg#*=}" ;;
    -*)               echo "Unknown option: $arg" >&2; exit 1 ;;
    *)                INPUT="$arg" ;;
  esac
done

if [ -z "$INPUT" ] || [ ! -f "$INPUT" ]; then
  echo "Usage: bash mix-voiceover.sh <video.mp4> --voiceover=<v.mp3> [--bgm=<b.mp3> | --bgm-mood=<name>]" >&2
  exit 1
fi
if [ -z "$VOICEOVER" ] || [ ! -f "$VOICEOVER" ]; then
  echo "✗ Missing --voiceover=<path>" >&2
  exit 1
fi

# Resolve the BGM source
if [ -z "$BGM" ] && [ -n "$BGM_MOOD" ]; then
  BGM="$ASSETS_DIR/bgm-${BGM_MOOD}.mp3"
fi
if [ -n "$BGM" ] && [ ! -f "$BGM" ]; then
  echo "✗ BGM file not found: $BGM" >&2
  echo "  Available moods: $(ls "$ASSETS_DIR" 2>/dev/null | grep -E '^bgm-.*\.mp3$' | sed 's/^bgm-//;s/\.mp3$//' | tr '\n' ' ')" >&2
  exit 1
fi

# Output path
if [ -z "$OUTPUT" ]; then
  base="${INPUT%.*}"
  OUTPUT="${base}-voiced.mp4"
fi

# Video duration (used by apad tail-silence and the ending fade-out)
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$INPUT") || {
  echo "✗ cannot read video duration (ffprobe required): $INPUT" >&2
  exit 1
}
FADE_ST=$(awk -v d="$DUR" 'BEGIN{printf "%.3f", d-0.5}')

echo "─ mix-voiceover ──────────────"
echo "  Video:    $INPUT"
echo "  Voice:    $VOICEOVER (vol=$VOICE_VOLUME)"
if [ -n "$BGM" ]; then
  echo "  BGM:      $BGM (vol=$BGM_VOLUME, ducking=$DUCKING)"
else
  echo "  BGM:      (none)"
fi
echo "  Output:   $OUTPUT"
echo "──────────────────────────────"

# ── ffmpeg filter graph ─────────────────────────────────────
if [ -z "$BGM" ]; then
  # Voice only (padded with tail silence up to the video length when the voiceover is shorter)
  ffmpeg -y -i "$INPUT" -i "$VOICEOVER" \
    -filter_complex "[1:a]volume=${VOICE_VOLUME},apad=whole_dur=${DUR}[a]" \
    -map 0:v -map "[a]" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUTPUT"
elif [ "$DUCKING" = "1" ]; then
  # Voice + BGM + sidechain ducking
  # Note 1: [voice] must be asplit into two paths — sidechaincompress and amix
  #   each consume one; a label can only be consumed once, reusing it fails
  #   with Invalid argument.
  # Note 2: the voiceover is apadded to the video length BEFORE amix
  #   (duration=first follows the first input), otherwise the BGM gets cut
  #   the moment the voice stops and the rest of the video goes dead silent.
  ffmpeg -y -i "$INPUT" -i "$VOICEOVER" -i "$BGM" \
    -filter_complex "
      [1:a]volume=${VOICE_VOLUME},apad=whole_dur=${DUR},asplit=2[voice_sc][voice_mix];
      [2:a]volume=${BGM_VOLUME},aloop=loop=-1:size=2e9[bgm_lo];
      [bgm_lo][voice_sc]sidechaincompress=threshold=0.04:ratio=8:attack=5:release=300:makeup=1[bgm_ducked];
      [voice_mix][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=0,apad=whole_dur=${DUR},afade=t=out:st=${FADE_ST}:d=0.5:curve=tri[a]
    " \
    -map 0:v -map "[a]" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUTPUT"
else
  # Voice + BGM static mix (voice padded to video length first; BGM loops to fill the whole video)
  ffmpeg -y -i "$INPUT" -i "$VOICEOVER" -i "$BGM" \
    -filter_complex "
      [1:a]volume=${VOICE_VOLUME},apad=whole_dur=${DUR}[voice];
      [2:a]volume=${BGM_VOLUME},aloop=loop=-1:size=2e9[bgm];
      [voice][bgm]amix=inputs=2:duration=first:dropout_transition=0,apad=whole_dur=${DUR}[a]
    " \
    -map 0:v -map "[a]" \
    -c:v copy -c:a aac -b:a 192k -shortest \
    "$OUTPUT"
fi

echo "✓ Done: $OUTPUT"
