#!/usr/bin/env python3
"""
Compare current performance metrics JSON to baseline on main.

Exit code:
  - 0 by default (informational table + optional GitHub warnings).
  - 1 only when PERF_FAIL_ON_REGRESSION=true AND a *gated* metric regresses past threshold.

Simulator CI is noisy; failing every PR on any metric >12% is usually undesirable.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


def _median(entry: dict) -> float | None:
    if not isinstance(entry, dict):
        return None
    if "median" in entry:
        return float(entry["median"])
    return None


def format_delta(before: float | None, after: float | None) -> str:
    if before is None or after is None:
        return "—"
    delta = after - before
    if before == 0:
        return f"{delta:+.4f} (baseline 0 — pct n/a)"
    pct = (delta / before) * 100.0
    sign = "+" if delta >= 0 else ""
    return f"{sign}{delta:.4f} ({sign}{pct:.1f}%)"


def _label_for_row(key: str, b: dict | None, c: dict | None) -> str:
    if isinstance(c, dict) and c.get("displayName"):
        return str(c.get("displayName"))
    if isinstance(b, dict) and b.get("displayName"):
        return str(b.get("displayName"))
    return key


def _should_gate_failure(label_lower: str, gate_parts: list[str]) -> bool:
    if not gate_parts:
        return True
    return any(p in label_lower for p in gate_parts)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--current", required=True, type=Path)
    p.add_argument("--baseline", required=True, type=Path)
    p.add_argument("--threshold", type=float, default=float(os.environ.get("PERF_REGRESSION_THRESHOLD", "0.12")))
    p.add_argument("--summary-out", dest="summary_out", type=Path, default=None)
    args = p.parse_args()

    threshold: float = args.threshold

    fail_on = os.environ.get("PERF_FAIL_ON_REGRESSION", "false").strip().lower() in ("1", "true", "yes")
    gate_raw = os.environ.get("PERF_REGRESSION_GATE_SUBSTRINGS", "applaunch")
    gate_parts = [s.strip().lower() for s in gate_raw.split(",") if s.strip()]

    cur = json.loads(args.current.read_text(encoding="utf-8"))
    baseline_file_missing = not args.baseline.exists()
    base_doc = json.loads(args.baseline.read_text(encoding="utf-8")) if not baseline_file_missing else {}

    cur_metrics: dict = cur.get("metrics") if isinstance(cur.get("metrics"), dict) else {}
    base_metrics: dict = base_doc.get("metrics") if isinstance(base_doc.get("metrics"), dict) else {}

    baseline_has_record = bool(base_doc.get("gitSha") or base_doc.get("updatedAt"))
    base_populated = len(base_metrics) > 0

    lines: list[str] = []
    lines.append("### Performance vs baseline (`main`)\n")
    lines.append("")
    lines.append("| Metric | Baseline | PR | Δ | Status |")
    lines.append("| --- | --- | --- | --- | --- |")

    failed = False
    all_keys = sorted(set(cur_metrics.keys()) | set(base_metrics.keys()))

    if baseline_file_missing or (not baseline_has_record and not base_populated):
        lines.append("| — | *no baseline yet* | — | — | ℹ️ |")
        lines.append("")
        lines.append(
            "**First-time setup:** `ci/performance-baseline.json` is missing or empty on `main`.\n\n"
            "Merge to `main` or run **Actions → Performance baseline (main)** to record a baseline."
        )
    elif baseline_has_record and not base_populated:
        lines.append("| — | *baseline exists but metrics empty* | — | — | ⚹ |")
        lines.append("")
        lines.append(
            "Baseline file on `main` has no metric values yet (extraction issue). PR metrics below are informational."
        )
        for key in sorted(cur_metrics.keys()):
            c = cur_metrics.get(key)
            cm = _median(c) if isinstance(c, dict) else None
            label = _label_for_row(key, None, c if isinstance(c, dict) else None)
            lines.append(f"| {label} | — | {cm if cm is not None else '—'} | — | PR only |")
    else:
        for key in all_keys:
            b = base_metrics.get(key)
            c = cur_metrics.get(key)
            bm = _median(b) if isinstance(b, dict) else None
            cm = _median(c) if isinstance(c, dict) else None
            label = _label_for_row(key, b if isinstance(b, dict) else None, c if isinstance(c, dict) else None)
            label_lower = label.lower()

            status = "—"
            if bm is not None and cm is not None:
                if bm == 0:
                    status = "✓ ok" if cm == 0 else "⚠️ noisy baseline"
                else:
                    rel = (cm - bm) / bm
                    if rel > threshold:
                        status = "❌ regression"
                        gated = _should_gate_failure(label_lower, gate_parts)
                        if fail_on and gated:
                            failed = True
                            print(f"::error::Gated regression: {label} ↑ {rel * 100:.1f}% (threshold {threshold * 100:.0f}%)")
                        elif fail_on and not gated:
                            status = "⚠️ above threshold (not gated)"
                            print(f"::notice::Non-gated drift: {label} ↑ {rel * 100:.1f}% — job still passes; tighten PERF_REGRESSION_GATE_SUBSTRINGS or threshold.")
                        else:
                            print(f"::warning::Regression (informational): {label} ↑ {rel * 100:.1f}% — job does not fail (set PERF_FAIL_ON_REGRESSION=true to enforce).")
                    elif rel < -threshold:
                        status = "✅ improved"
                    else:
                        status = "✓ ok"
            elif cm is not None and bm is None:
                status = "new"

            lines.append(
                f"| {label} | {bm if bm is not None else '—'} | {cm if cm is not None else '—'} "
                f"| {format_delta(bm, cm)} | {status} |"
            )

    lines.append("")
    lines.append(
        f"_Threshold: **{threshold * 100:.0f}%** relative increase. "
        f"**Fail job on regression:** `PERF_FAIL_ON_REGRESSION`={str(fail_on).lower()}; "
        f"**Only count metrics whose label contains:** {gate_raw!r} (comma substrings, case-insensitive)._"
    )

    report = "\n".join(lines)
    print(report)

    if args.summary_out:
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(report, encoding="utf-8")

    gh_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if gh_summary:
        Path(gh_summary).open("a", encoding="utf-8").write("\n" + report + "\n")

    if failed:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
