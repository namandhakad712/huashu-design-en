#!/bin/bash
# design-gate-hook.sh — PreToolUse(Bash) hook: check the design-flow gate file before long-film renders
#
# Iron-rule background (set by Peanut, 2026-07-17): before huashu-design does any design it must ① run the asset
# protocol (brand-spec.md) ② show the user real visuals from three directions to pick from (direction-approved.md
# records the pick or the exemption reason).
# B00 (210s) field test: skipping direction confirmation and rendering the full film → full visual rework. This
# hook turns that lesson into a machine constraint:
# **For compositions ≥45 seconds, no direction-approved.md means no render** — the cost of reworking a long film
# far outweighs the cost of pausing once.
#
# Pass conditions (any one):
#   - Composition duration <45s or undeterminable (short films / experiments get low friction, governed by the SKILL.md gate protocol)
#   - direction-approved.md exists in the project directory (or up to two levels above)
#   - The command explicitly carries SKIP_DESIGN_GATE=1 (for when Peanut explicitly says skip; auditable)
#
# Security statement: this hook is **never installed automatically by the skill** — neither SKILL.md nor README
# contains any instruction to write into settings.json; it only takes effect after you manually wire it into
# settings.json. Behavior ceiling: on a matching long-film render command it exits 2 to block execution and
# prints the reason — no network requests, no file writes, no deletions. See SECURITY.md at the repo root.
#
# settings.json wiring: PreToolUse / matcher "Bash" / command pointing at this script

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
CWD=$(printf '%s' "$INPUT" | python3 -c "import json,sys;print(json.load(sys.stdin).get('cwd',''))" 2>/dev/null)

# Commands that merely talk about commands (echo/grep etc.) pass straight through — prevents false positives on plain text (QA Bug1)
FIRST=$(echo "$CMD" | sed -E 's/^[[:space:]]*//' | cut -d' ' -f1)
case "$FIRST" in echo|printf|grep|cat|ls|head|tail|wc|sed|awk) exit 0;; esac
# Only render commands are governed (npm run render and narrated long-film renders included)
echo "$CMD" | grep -qE "hyperframes(@[0-9.]+)? +render|render-video(-seek)?\.js|render-narration\.sh|npm +run +render\b" || exit 0
# Explicit skip (an auditable escape hatch)
echo "$CMD" | grep -q "SKIP_DESIGN_GATE=1" && exit 0

# Locate the project directory: the cd target in the command > the hook cwd
DIR="$CWD"
CDDIR=$(echo "$CMD" | grep -oE 'cd +"[^"]+"|cd +[^ &;]+' | head -1 | sed -E 's/^cd +//; s/"//g')
[ -n "$CDDIR" ] && [ -d "$CDDIR" ] && DIR="$CDDIR"

# Get the composition duration: hyperframes projects read data-duration from index.html; render-video-seek reads the --duration argument
DUR=""
D_ARG=$(echo "$CMD" | grep -oE '\-\-duration=[0-9]+' | head -1 | cut -d= -f2)
[ -n "$D_ARG" ] && DUR="$D_ARG"
if [ -z "$DUR" ] && [ -f "$DIR/index.html" ]; then
  DUR=$(grep -oE 'data-duration="[0-9.]+"' "$DIR/index.html" | head -1 | grep -oE '[0-9.]+' | cut -d. -f1)
fi
# Undeterminable duration or a short film → pass
[ -z "$DUR" ] && exit 0
[ "$DUR" -lt 45 ] 2>/dev/null && exit 0

# Long film: look for the gate file (project directory and two levels above)
for d in "$DIR" "$DIR/.." "$DIR/../.."; do
  [ -f "$d/direction-approved.md" ] && exit 0
done

cat >&2 << EOF
🛑 Design-flow gate: this composition is ${DUR}s (a ≥45s long film), but no direction-approved.md was found in the project.
huashu-design iron rule: before rendering a long film you must complete "three directions of real visuals for the user to choose from" (or an explicit user exemption), and write the pick/exemption record into the project directory's direction-approved.md (including: which versions were shown, screenshot paths, the user's verbatim pick).
Re-render after fixing this; when the user explicitly says skip to your face, prefix the command with SKIP_DESIGN_GATE=1 for an explicit pass.
(Basis: 2026-07-17 B00 field test — skipping direction confirmation on a 210s full film → full visual rework)
EOF
exit 2
