#!/usr/bin/env python3
"""Fail closed if critical Python would break default-branch runtime."""
from __future__ import annotations

import argparse
import py_compile
import subprocess
import sys
from pathlib import Path


def compile_path(p: Path):
    try:
        py_compile.compile(str(p), doraise=True)
        return None
    except Exception as e:
        return "%s: %s" % (p, e)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--paths", nargs="*", default=[])
    ap.add_argument("--from-git-diff", default="")
    args = ap.parse_args()
    paths = [Path(p) for p in args.paths]
    if args.from_git_diff:
        r = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", args.from_git_diff],
            capture_output=True,
            text=True,
        )
        for line in r.stdout.splitlines():
            if line.endswith(".py"):
                paths.append(Path(line))
    for crit_name in (
        "scripts/verify_delivery_closure.py",
        "scripts/pr_queue_gc.py",
        "scripts/durable_hygiene.py",
    ):
        crit = Path(crit_name)
        if crit.exists() and crit not in paths:
            paths.append(crit)
    errors = []
    for p in paths:
        if not p.exists():
            continue
        err = compile_path(p)
        if err:
            errors.append(err)
        else:
            print("OK compile", p, flush=True)
    if errors:
        print("COMPILE_GATE_FAIL", flush=True)
        for e in errors:
            print(e, flush=True)
        return 1
    print("COMPILE_GATE_PASS", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
