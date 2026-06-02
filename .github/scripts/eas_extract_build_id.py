#!/usr/bin/env python3
"""Parse JSON from `eas build --json` (stdout captured to a file) and print the EAS build id."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def extract_id(data: object) -> str | None:
    if isinstance(data, dict):
        if "id" in data and isinstance(data["id"], str):
            return data["id"]
        build = data.get("build")
        if isinstance(build, dict) and isinstance(build.get("id"), str):
            return build["id"]
        for key in ("builds", "data"):
            inner = data.get(key)
            if isinstance(inner, list) and inner:
                found = extract_id(inner[0])
                if found:
                    return found
    if isinstance(data, list) and data:
        return extract_id(data[0])
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: eas_extract_build_id.py <path-to-json-file>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"eas_extract_build_id: missing file {path}", file=sys.stderr)
        return 1
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        print("eas_extract_build_id: empty JSON file", file=sys.stderr)
        return 1
    data = None
    for chunk in (raw, *reversed(raw.splitlines())):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            data = json.loads(chunk)
            break
        except json.JSONDecodeError:
            continue
    if data is None:
        print("eas_extract_build_id: could not parse JSON from file", file=sys.stderr)
        return 1
    build_id = extract_id(data)
    if not build_id:
        print("eas_extract_build_id: could not find build id in JSON", file=sys.stderr)
        return 1
    print(build_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
