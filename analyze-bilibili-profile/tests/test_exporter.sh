#!/bin/sh
set -eu

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/fake_bili.py" <<'PY'
#!/usr/bin/env python3
import json
import sys

args = [x for x in sys.argv[1:] if x != "--json"]
command = args[0]
data = None

if command == "following":
    page = int(args[args.index("--page") + 1])
    items = (
        [{"id": str(i), "name": f"UP{i}", "sign": ""} for i in range(1, 21)]
        if page == 1
        else [{"id": "21", "name": "UP21", "sign": ""}]
    )
    data = {"page": page, "total": 21, "items": items}
elif command == "favorites" and len(args) == 1:
    data = [{"id": 10, "title": "科普", "media_count": 2}]
elif command == "favorites":
    data = {
        "folder_id": 10,
        "page": 1,
        "has_more": False,
        "items": [
            {"id": "BV1", "title": "物理科普", "upper": {"name": "UP1"}},
            {"id": "BV2", "title": "AI原理", "upper": {"name": "UP2"}},
        ],
    }
elif command == "history":
    data = {
        "page": 1,
        "count": 2,
        "items": [
            {"id": "BV1", "title": "AI模型", "author": "UP1", "viewed_at": "2026-01-02T00:00:00"},
            {"id": "BV2", "title": "历史解释", "author": "UP2", "viewed_at": "2026-01-01T00:00:00"},
        ],
    }
elif command == "watch-later":
    data = {"count": 1, "items": [{"id": "BV3", "title": "稍后", "author": "UP3"}]}
elif command == "feed":
    data = {"items": [{"id": "D1", "title": "动态"}], "next_offset": ""}
else:
    print(json.dumps({"ok": False, "error": "unexpected args", "args": args}))
    raise SystemExit(1)

print(json.dumps({"ok": True, "schema_version": "1", "data": data}, ensure_ascii=False))
PY
chmod +x "$TMP_DIR/fake_bili.py"

python3 "$SKILL_DIR/scripts/export_bilibili.py" \
  --bili-command "python3 $TMP_DIR/fake_bili.py" \
  --home "$TMP_DIR/home" \
  --output "$TMP_DIR/export" \
  --delay 0

python3 "$SKILL_DIR/scripts/validate_export.py" "$TMP_DIR/export"
python3 - "$TMP_DIR/export" <<'PY'
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
assert json.loads((root / "following.json").read_text())["exported"] == 21
assert json.loads((root / "favorites.json").read_text())["exported"] == 2
assert json.loads((root / "history.json").read_text())["boundary"] == "short page 1"
assert json.loads((root / "watch-later.json").read_text())["exported"] == 1
assert json.loads((root / "feed.json").read_text())["exported"] == 1
PY

echo "exporter tests passed"
