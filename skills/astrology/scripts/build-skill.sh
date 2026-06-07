#!/usr/bin/env bash
# Build a .skill file for claude.ai web upload.
# A .skill file is a ZIP of the skill directory renamed to .skill.
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
cd "$SKILL_DIR"

VERSION=$(grep '"version"' "$REPO_ROOT/.claude-plugin/plugin.json" | head -1 | sed 's/.*: *"//;s/".*//')
OUTDIR="$REPO_ROOT/dist"
OUTFILE="$OUTDIR/astrology-${VERSION}.skill"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
zip -r "$OUTFILE" SKILL.md scripts/ references/ assets/ -x '*.pyc'

# Also create a latest alias for predictable download URL
cp "$OUTFILE" "$OUTDIR/astrology.skill"

echo "Built: $OUTFILE ($OUTDIR/astrology.skill)"
echo "Size:  $(du -h "$OUTFILE" | cut -f1)"
echo ""
echo "Upload to claude.ai: Settings → Capabilities → Skills → +"
echo "Or attach to a GitHub release for download."
