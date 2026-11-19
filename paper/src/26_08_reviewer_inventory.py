#!/usr/bin/env python3
"""
26_08_reviewer_inventory.py  (READ-ONLY; run on the author's Mac)

Purpose
-------
Inventory the existing files that can answer the reviewer-risk items of the
ARGUS SRL manuscript BEFORE any new analysis is written:

  R1  Circularity: C3 prior and the reference both come from the JMA catalog.
      -> look for the independent DPRI truth for Central Tottori 2016
         (23_01 / 23_02 / 23_03 scripts and their outputs).
  R2  Practical meaning of a sub-km gain.
      -> look for the GMPE / intensity impact calculation (21_10).
  R3  Gain vs. time since the mainshock (few past events early on).
      -> look for per-event result files of the frozen tests
         (21_04, 21_20, 25_06*, 22_04 ...) and print their columns, so the
         next script can be written against the real column names.

Nothing is modified, created, or deleted. Output is printed only; paste it
back into the chat.

Usage
-----
  python3 26_08_reviewer_inventory.py
  python3 26_08_reviewer_inventory.py --roots ~/ARGUS_prereg_21_04 ~/SWIFT
"""
import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_ROOTS = ["~/ARGUS_prereg_21_04", "~/SWIFT", "~/SERAPH_V4", "~/ARGUS"]

# (label, substrings that must appear in the file name, case-insensitive)
TARGETS = [
    ("R1 DPRI truth / memory audit", ["23_01", "23_02", "23_03", "dpri"]),
    ("R2 GMPE / intensity impact", ["21_10"]),
    ("R3 per-event results", ["per_event", "perevent"]),
]
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".ipynb_checkpoints"}
MAX_FILES_PER_TARGET = 200


def human(n):
    for u in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.0f}{u}"
        n /= 1024
    return f"{n:.1f}TB"


def peek(path: Path):
    """Return a short, read-only description of the file content."""
    suf = path.suffix.lower()
    try:
        if suf == ".json":
            with open(path, "r", encoding="utf-8") as f:
                obj = json.load(f)
            if isinstance(obj, dict):
                keys = list(obj.keys())
                return f"json dict, {len(keys)} keys: {keys[:25]}"
            if isinstance(obj, list):
                first = obj[0] if obj else None
                k = list(first.keys())[:25] if isinstance(first, dict) else type(first).__name__
                return f"json list, n={len(obj)}, first item keys: {k}"
            return f"json {type(obj).__name__}"
        if suf in (".csv", ".tsv"):
            delim = "\t" if suf == ".tsv" else ","
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                r = csv.reader(f, delimiter=delim)
                header = next(r, [])
                n = sum(1 for _ in r)
            return f"{suf[1:]} rows={n}, columns({len(header)}): {header[:40]}"
        if suf in (".py", ".md", ".txt", ".log"):
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = [next(f, "") for _ in range(12)]
            text = " | ".join(l.strip() for l in lines if l.strip())
            return "head: " + text[:400]
    except Exception as e:  # report, never fail
        return f"(could not read: {type(e).__name__}: {e})"
    return ""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", default=DEFAULT_ROOTS)
    args = ap.parse_args()

    roots = [Path(os.path.expanduser(r)) for r in args.roots]
    print("26_08 reviewer inventory (read-only)")
    print("python", sys.version.split()[0], "| time", time.strftime("%Y-%m-%d %H:%M:%S"))
    for r in roots:
        print(f"root {r}: {'exists' if r.is_dir() else 'NOT FOUND'}")

    hits = {label: [] for label, _ in TARGETS}
    for root in roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                low = fn.lower()
                for label, keys in TARGETS:
                    if any(k in low for k in keys):
                        hits[label].append(Path(dirpath) / fn)

    for label, _ in TARGETS:
        files = sorted(set(hits[label]))
        print("\n" + "=" * 78)
        print(f"{label}: {len(files)} file(s)")
        print("=" * 78)
        for p in files[:MAX_FILES_PER_TARGET]:
            st = p.stat()
            mt = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
            print(f"- {p}  [{human(st.st_size)}, {mt}]")
            d = peek(p)
            if d:
                print(f"    {d}")
        if len(files) > MAX_FILES_PER_TARGET:
            print(f"  ... {len(files) - MAX_FILES_PER_TARGET} more not shown")

    print("\nDONE (nothing was written)")


if __name__ == "__main__":
    main()
