#!/usr/bin/env python3
"""Validate normalized Bilibili exports and reject credential leakage."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED = ("following.json", "favorites.json", "history.json")
OPTIONAL = ("watch-later.json", "feed.json", "export-summary.json")
SENSITIVE = re.compile(
    r"SESSDATA|bili_jct|ac_time_value|buvid3|buvid4|DedeUserID|credential\.json",
    re.I,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    errors = []
    for name in REQUIRED:
        if not (args.directory / name).exists():
            errors.append(f"missing required file: {name}")
    for name in (*REQUIRED, *OPTIONAL):
        path = args.directory / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON {name}: {exc}")
        if SENSITIVE.search(text):
            errors.append(f"sensitive credential marker in {name}")
    if errors:
        print("\n".join(errors))
        return 1
    print("export validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

