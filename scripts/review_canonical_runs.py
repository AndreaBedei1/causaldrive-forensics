#!/usr/bin/env python3
"""Menu for the manual review of the 23 canonical development runs: pick one, its interactive replay starts
(scripts/replay_run.py, CARLA server on port 3000); when the replay window closes the menu returns.

    conda activate carla
    python scripts/review_canonical_runs.py          (or scripts\\review_canonical_runs.bat)

Extra arguments are passed to replay_run.py (e.g. --speed 0.25).  One replay at a time.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_canonical import canonical_runs  # noqa: E402


def menu(runs):
    print("\nCanonical development runs (replay on the CARLA server at port 3000):")
    for number, run in enumerate(runs, 1):
        label = "{0} {1}".format(run.parent.name, run.name[len("run_0_"):])
        missing = "" if (run / "reconstruction").is_dir() else "   (no reconstruction!)"
        print("  {0:2d}  {1}{2}".format(number, label, missing))
    print("   q  quit")


def main() -> int:
    runs = canonical_runs()
    extra = sys.argv[1:]
    while True:
        menu(runs)
        try:
            choice = input("run number: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if choice in ("q", "quit", "exit", ""):
            return 0
        if not choice.isdigit() or not 1 <= int(choice) <= len(runs):
            print("choose 1-{0} or q".format(len(runs)))
            continue
        run = runs[int(choice) - 1]
        command = [sys.executable, str(ROOT / "scripts" / "replay_run.py"), str(run.relative_to(ROOT))] + extra
        print(" ".join(command))
        subprocess.call(command, cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
