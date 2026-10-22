#!/usr/bin/env python3
"""Menu for the manual review of the 22 canonical development runs.  Pick one: the GROUND TRUTH viewer opens first
(what CARLA simulated: every vehicle, true trajectories, physical contacts), and when its window closes the
RECONSTRUCTION viewer of the same run (what the algorithm estimated from the sensors); then the menu returns.
``12g`` opens only the ground truth of run 12, ``12r`` only its reconstruction (scripts/replay_run.py).  Both
viewers use the CARLA 0.9.15 server of ``--port`` (default: simulation.port of configs/default.yaml).

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


def server_line(extra) -> str:
    """The CARLA server the viewers will use: the ``--port`` passed on, else the configured one."""
    for k, arg in enumerate(extra):
        if arg == "--port" and k + 1 < len(extra):
            return "CARLA server at port {0}".format(extra[k + 1])
        if arg.startswith("--port="):
            return "CARLA server at port {0}".format(arg.split("=", 1)[1])
    return "CARLA server at the port of configs/default.yaml (simulation.port)"


def menu(runs, extra=()):
    print("\nCanonical development runs (replay on the {0}):".format(server_line(list(extra))))
    for number, run in enumerate(runs, 1):
        label = "{0} {1}".format(run.parent.name, run.name[len("run_0_"):])
        missing = "" if (run / "reconstruction").is_dir() else "   (no reconstruction!)"
        print("  {0:2d}  {1}{2}".format(number, label, missing))
    print("   N  ground truth, then reconstruction    Ng  ground truth only    Nr  reconstruction only    q  quit")


def main() -> int:
    runs = canonical_runs()
    extra = sys.argv[1:]
    while True:
        menu(runs, extra)
        try:
            choice = input("run number: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if choice in ("q", "quit", "exit", ""):
            return 0
        views = {"g": [True], "r": [False]}.get(choice[-1:], [True, False])
        number = choice[:-1] if choice[-1:] in ("g", "r") else choice
        if not number.isdigit() or not 1 <= int(number) <= len(runs):
            print("choose 1-{0} (optionally followed by g or r) or q".format(len(runs)))
            continue
        run = runs[int(number) - 1]
        for ground_truth in views:
            script = "view_ground_truth.py" if ground_truth else "replay_run.py"
            command = [sys.executable, str(ROOT / "scripts" / script), str(run.relative_to(ROOT))] + extra
            print(" ".join(command))
            subprocess.call(command, cwd=str(ROOT))


if __name__ == "__main__":
    raise SystemExit(main())
