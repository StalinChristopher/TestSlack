#!/usr/bin/env python3
"""
Merge extracted metrics into ci/performance-baseline.json and append ci/performance-history.json.
Run on pushes to main after UI performance tests.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--metrics", required=True, type=Path, help="JSON from extract_performance_metrics.py")
    p.add_argument("--baseline-out", default=Path("ci/performance-baseline.json"), type=Path)
    p.add_argument("--history-out", default=Path("ci/performance-history.json"), type=Path)
    p.add_argument("--max-history", type=int, default=100)
    args = p.parse_args()

    doc = json.loads(args.metrics.read_text(encoding="utf-8"))
    metrics = doc.get("metrics") or {}

    sha = os.environ.get("GITHUB_SHA", "local")
    now = datetime.now(timezone.utc).isoformat()

    baseline = {
        "schemaVersion": 1,
        "updatedAt": now,
        "gitSha": sha,
        "metrics": metrics,
    }
    args.baseline_out.parent.mkdir(parents=True, exist_ok=True)
    args.baseline_out.write_text(json.dumps(baseline, indent=2), encoding="utf-8")

    history: list = []
    if args.history_out.exists():
        history = json.loads(args.history_out.read_text(encoding="utf-8"))
        if not isinstance(history, list):
            history = []

    history.append(
        {
            "schemaVersion": 1,
            "recordedAt": now,
            "gitSha": sha,
            "metrics": metrics,
        }
    )
    history = history[-args.max_history :]
    args.history_out.write_text(json.dumps(history, indent=2), encoding="utf-8")

    print(f"Updated {args.baseline_out} and {args.history_out}")


if __name__ == "__main__":
    main()
