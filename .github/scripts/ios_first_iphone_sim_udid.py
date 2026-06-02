#!/usr/bin/env python3
"""Pick the first available iPhone Simulator from simctl JSON.

Default: print an xcodebuild -destination string (platform + name + OS), which
avoids brittle id=... UDIDs that differ per machine or Xcode install.

With --udid: print only the UDID (for simctl boot or legacy scripts).
"""

from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys


def runtime_version_tuple(runtime_key: str) -> tuple[int, ...]:
    m = re.search(r"\.SimRuntime\.iOS-(\d+)-(\d+)(?:-(\d+))?$", runtime_key)
    if not m:
        return (0, 0)
    parts = [int(m.group(1)), int(m.group(2))]
    if m.group(3) is not None:
        parts.append(int(m.group(3)))
    return tuple(parts)


def runtime_to_os_string(runtime_key: str) -> str | None:
    m = re.search(r"\.SimRuntime\.iOS-(\d+)-(\d+)(?:-(\d+))?$", runtime_key)
    if not m:
        return None
    if m.group(3) is not None:
        return f"{m.group(1)}.{m.group(2)}.{m.group(3)}"
    return f"{m.group(1)}.{m.group(2)}"


def first_iphone_sim(data: dict) -> tuple[str, str, str] | None:
    """Return (runtime_key, udid, name) for newest iOS runtime, first iPhone."""
    devices_by_runtime = data.get("devices", {})
    ios_runtimes = [
        rk
        for rk in devices_by_runtime
        if ".SimRuntime.iOS-" in rk and "iOS" in rk
    ]
    ios_runtimes.sort(key=runtime_version_tuple, reverse=True)

    for rk in ios_runtimes:
        for d in devices_by_runtime[rk]:
            if d.get("isAvailable") and "iPhone" in d.get("name", ""):
                return rk, d["udid"], d["name"]
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--udid",
        action="store_true",
        help="Print only the device UDID instead of an xcodebuild destination string.",
    )
    args = parser.parse_args()

    out = subprocess.check_output(
        ["xcrun", "simctl", "list", "devices", "available", "-j"],
        text=True,
    )
    data = json.loads(out)
    picked = first_iphone_sim(data)
    if picked is None:
        sys.stderr.write("No available iPhone simulator found\n")
        sys.exit(1)

    rk, udid, name = picked
    if args.udid:
        print(udid)
        return

    os_version = runtime_to_os_string(rk)
    if os_version is None:
        print(f"id={udid}")
        return

    # Include arch so xcodebuild never warns about multiple matching destinations
    # (arm64 and x86_64 share the same UDID on Apple-silicon runners).
    arch = "arm64" if platform.machine() == "arm64" else "x86_64"
    print(f"platform=iOS Simulator,name={name},OS={os_version},arch={arch}")


if __name__ == "__main__":
    main()
