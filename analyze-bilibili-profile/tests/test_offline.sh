#!/bin/sh
set -eu

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

python3 "$SKILL_DIR/scripts/validate_export.py" "$SKILL_DIR/tests/fixtures"
python3 "$SKILL_DIR/scripts/analyze_profile.py" \
  --input "$SKILL_DIR/tests/fixtures" \
  --output "$TMP_DIR/profile.md"

grep -q "B站兴趣画像" "$TMP_DIR/profile.md"
grep -q "AI、编程与开发工具" "$TMP_DIR/profile.md"
grep -q "前10位创作者" "$TMP_DIR/profile.md"

cp -R "$SKILL_DIR/tests/fixtures" "$TMP_DIR/leak"
printf '%s\n' '{"SESSDATA":"secret"}' > "$TMP_DIR/leak/feed.json"
if python3 "$SKILL_DIR/scripts/validate_export.py" "$TMP_DIR/leak"; then
  echo "validator failed to reject credentials" >&2
  exit 1
fi

echo "offline tests passed"
