#!/usr/bin/env python3
"""Read-only, resumable Bilibili exporter around a structured-output CLI."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import time
import urllib.request
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bili-command", default="bili")
    parser.add_argument("--home", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--history-pages", type=int, default=100)
    parser.add_argument("--feed-pages", type=int, default=20)
    parser.add_argument("--delay", type=float, default=0.35)
    return parser.parse_args()


class Exporter:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.command = shlex.split(args.bili_command)
        self.env = os.environ.copy()
        self.env["HOME"] = str(args.home.resolve())
        args.home.mkdir(parents=True, exist_ok=True)
        args.output.mkdir(parents=True, exist_ok=True)

    def run(self, *args: str, retries: int = 3) -> Any:
        command = [*self.command, *args, "--json"]
        error = ""
        for attempt in range(1, retries + 1):
            proc = subprocess.run(command, env=self.env, text=True, capture_output=True)
            if proc.returncode == 0:
                payload = json.loads(proc.stdout)
                if payload.get("ok", True):
                    return payload.get("data")
                error = json.dumps(payload, ensure_ascii=False)
            else:
                error = (proc.stderr or proc.stdout).strip()
            if attempt < retries:
                time.sleep(attempt * 2)
        raise RuntimeError(f"{' '.join(args)} failed: {error}")

    def save(self, name: str, data: Any) -> None:
        (self.args.output / name).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def follows(self) -> dict[str, Any]:
        first = self.run("following", "--page", "1")
        total = int(first.get("total", 0))
        items = list(first.get("items", []))
        seen = {item.get("id") for item in items}
        page = 2
        while len(items) < total:
            batch = self.run("following", "--page", str(page)).get("items", [])
            fresh = [item for item in batch if item.get("id") not in seen]
            if not fresh:
                break
            items.extend(fresh)
            seen.update(item.get("id") for item in fresh)
            page += 1
            time.sleep(self.args.delay)
        return {"reported_total": total, "exported": len(items), "items": items}

    def favorites(self) -> dict[str, Any]:
        output = []
        for folder in self.run("favorites"):
            items, seen, page = [], set(), 1
            while True:
                data = self.run("favorites", str(folder["id"]), "--page", str(page))
                batch = data.get("items", [])
                fresh = [item for item in batch if item.get("id") not in seen]
                items.extend(fresh)
                seen.update(item.get("id") for item in fresh)
                if not data.get("has_more") or not fresh:
                    break
                page += 1
                time.sleep(self.args.delay)
            output.append({**folder, "exported": len(items), "items": items})
        return {"exported": sum(x["exported"] for x in output), "folders": output}

    def history(self) -> dict[str, Any]:
        items, page_signatures = [], set()
        boundary = ""
        for page in range(1, self.args.history_pages + 1):
            try:
                data = self.run("history", "--page", str(page), "--max", "100")
            except RuntimeError:
                if page == 1:
                    raise
                boundary = f"API returned null/error at page {page}"
                break
            batch = (data or {}).get("items", [])
            signature = tuple(
                f"{item.get('id', '')}:{item.get('viewed_at', '')}" for item in batch
            )
            if not batch:
                boundary = f"empty page {page}"
                break
            if signature in page_signatures:
                boundary = f"repeated page {page}"
                break
            page_signatures.add(signature)
            items.extend(batch)
            if len(batch) < 100:
                boundary = f"short page {page}"
                break
            time.sleep(self.args.delay)
        unique = {
            (item.get("id", ""), item.get("viewed_at", "")): item for item in items
        }
        result = sorted(
            unique.values(), key=lambda item: item.get("viewed_at", ""), reverse=True
        )
        return {"exported": len(result), "boundary": boundary, "items": result}

    def watch_later(self) -> dict[str, Any]:
        data = self.run("watch-later")
        if data.get("count") and not data.get("items"):
            fallback = self.watch_later_fallback()
            if fallback is not None:
                return fallback
        return {
            "reported_count": data.get("count", 0),
            "exported": len(data.get("items", [])),
            "items": data.get("items", []),
            "fallback_required": bool(data.get("count") and not data.get("items")),
        }

    def watch_later_fallback(self) -> dict[str, Any] | None:
        credential_path = self.args.home / ".bilibili-cli" / "credential.json"
        if not credential_path.exists():
            return None
        credential = json.loads(credential_path.read_text(encoding="utf-8"))
        cookie_names = (
            ("SESSDATA", "sessdata"),
            ("bili_jct", "bili_jct"),
            ("DedeUserID", "dedeuserid"),
            ("buvid3", "buvid3"),
            ("buvid4", "buvid4"),
        )
        cookies = [
            f"{wire_name}={credential.get(file_name)}"
            for wire_name, file_name in cookie_names
            if credential.get(file_name)
        ]
        if not cookies:
            return None
        request = urllib.request.Request(
            "https://api.bilibili.com/x/v2/history/toview",
            headers={
                "Cookie": "; ".join(cookies),
                "Referer": "https://www.bilibili.com/",
                "User-Agent": "Mozilla/5.0",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
        if payload.get("code") != 0:
            raise RuntimeError(f"watch-later fallback failed: {payload.get('message')}")
        data = payload.get("data") or {}
        items = []
        for item in data.get("list") or []:
            owner = item.get("owner") or {}
            items.append(
                {
                    "id": item.get("bvid", ""),
                    "bvid": item.get("bvid", ""),
                    "title": item.get("title", ""),
                    "author": owner.get("name", ""),
                    "duration_seconds": item.get("duration", 0),
                    "added_at": item.get("add_at", 0),
                    "progress_seconds": item.get("progress", 0),
                }
            )
        return {
            "reported_count": data.get("count", 0),
            "exported": len(items),
            "items": items,
            "fallback_used": True,
        }

    def feed(self) -> dict[str, Any]:
        items, offset, seen = [], "", set()
        for _ in range(self.args.feed_pages):
            call = ["feed"] + (["--offset", offset] if offset else [])
            data = self.run(*call)
            batch = data.get("items", [])
            if not batch:
                break
            items.extend(batch)
            next_offset = str(data.get("next_offset", ""))
            if not next_offset or next_offset in seen:
                break
            seen.add(next_offset)
            offset = next_offset
            time.sleep(self.args.delay)
        return {"exported": len(items), "sample_limited": True, "items": items}


def main() -> int:
    args = parse_args()
    exporter = Exporter(args)
    jobs = {
        "following.json": exporter.follows,
        "favorites.json": exporter.favorites,
        "history.json": exporter.history,
        "watch-later.json": exporter.watch_later,
        "feed.json": exporter.feed,
    }
    summary = {}
    for name, job in jobs.items():
        try:
            data = job()
            exporter.save(name, data)
            summary[name] = {"ok": True, "exported": data.get("exported")}
        except Exception as exc:  # Keep successful datasets auditable.
            summary[name] = {"ok": False, "error": str(exc)}
    exporter.save("export-summary.json", summary)
    return 0 if all(item["ok"] for item in summary.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
