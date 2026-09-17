#!/usr/bin/env python
"""Run counterfactual suites over several recorded runs, surviving interpreter aborts.

::

    python scripts/run_counterfactual_campaign.py \\
        --run artifacts/S01_rear_end/seed_000_crash \\
        --run artifacts/S06_chain_collision/seed_000_b_rear_first \\
        --max-interventions 4 --attempts 4

Why this exists rather than a loop over ``scripts/run_counterfactuals.py``:

* On the tested build the native CARLA client aborts the **whole interpreter**
  part-way through a suite -- ``Fatal Python error: Aborted`` inside
  ``world.apply_settings()`` on the third simulator process (see finding 10 in
  ``docs/ENVIRONMENT.md``). It cannot be caught in-process, so each suite runs as
  a **subprocess**: the abort kills the child, not the campaign.
* ``counterfactual.resume`` means a retry picks up from the replays already on
  disk, so each attempt needs fewer simulator restarts than the last and the
  suite converges instead of looping forever.
* **Stray engines are killed between attempts, and this matters for
  correctness, not tidiness.** When the interpreter aborts, the teardown never
  runs and the engine process survives holding the RPC port. The next attempt's
  "fresh" server would then fail to bind, the client would silently reconnect to
  the orphan, and the replays would share the accumulated state that restarting
  exists to prevent (findings 8 and 9). Pass ``--keep-stray-engines`` only when
  you are managing the simulator yourself.

A suite is complete when its contribution report names an outcome for every
intervention that was asked for. A suite that exhausts its attempts is reported
as ``INCOMPLETE`` and is **not** quietly treated as a result.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

LOGGER = logging.getLogger("counterfactual_campaign")

#: The engine image names the packaged builds run under. The launcher
#: (``CarlaUE4.exe``) is deliberately absent: it exits immediately and killing it
#: leaves the engine running (``docs/ENVIRONMENT.md``, finding 9).
ENGINE_IMAGES = ("CarlaUE4-Win64-Shipping.exe", "CarlaUE4-Linux-Shipping")


def kill_stray_engines(settle_s: float = 5.0) -> int:
    """Kill every simulator engine process on this machine. Returns the count.

    Destructive by design and only called between attempts: after an aborted
    attempt the orphaned engine still holds the RPC port, and leaving it there
    silently invalidates every replay that follows.
    """
    killed = 0
    for image in ENGINE_IMAGES:
        try:
            out = subprocess.check_output(
                ["tasklist", "/FI", "IMAGENAME eq {0}".format(image), "/FO", "CSV", "/NH"],
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        for line in out.decode("utf-8", "replace").splitlines():
            parts = [p.strip('" ') for p in line.split('","')]
            if len(parts) < 2 or parts[0].lower() != image.lower():
                continue
            try:
                pid = int(parts[1])
            except ValueError:
                continue
            subprocess.call(["taskkill", "/F", "/PID", str(pid)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            killed += 1
    if killed:
        LOGGER.info("killed %d stray simulator engine(s)", killed)
        time.sleep(settle_s)  # let the OS release the RPC port
    return killed


def contribution_state(run_dir: Path, expected: Optional[int]) -> Dict[str, Any]:
    """How far a suite got, read from its persisted contribution report."""
    path = run_dir / "counterfactual" / "causal_contribution.json"
    if not path.exists():
        return {"complete": False, "n_contributions": 0, "reason": "no contribution report"}
    try:
        with open(str(path), encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, ValueError) as exc:
        return {"complete": False, "n_contributions": 0,
                "reason": "unreadable report: {0}".format(exc)}
    n = len(doc.get("contributions") or [])
    failures = len((doc.get("classification") or {}).get("failures") or [])
    complete = n >= expected if expected else n > 0
    return {
        "complete": bool(complete),
        "n_contributions": n,
        "n_failures": failures,
        "attribution_class": (doc.get("classification") or {}).get("attribution_class"),
        "reason": "" if complete else "{0} replay outcome(s), expected {1}".format(n, expected),
    }


def run_suite_once(run_dir: Path, max_interventions: Optional[int],
                   extra: Sequence[str]) -> int:
    """One attempt at one suite, as a subprocess. Returns its exit status."""
    cmd = [sys.executable, str(Path(__file__).with_name("run_counterfactuals.py")),
           "--run", str(run_dir)]
    if max_interventions is not None:
        cmd += ["--config-overrides",
                "counterfactual.max_interventions={0}".format(int(max_interventions))]
    cmd += list(extra)
    LOGGER.info("running %s", " ".join(cmd))
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    return subprocess.call(cmd, env=env)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", dest="runs", action="append", required=True,
                        metavar="RUN_DIR",
                        help="recorded run to replay; repeat for several")
    parser.add_argument("--max-interventions", type=int, default=None,
                        help="override counterfactual.max_interventions")
    parser.add_argument("--attempts", type=int, default=4,
                        help="attempts per suite before reporting it INCOMPLETE")
    parser.add_argument("--fresh", action="store_true",
                        help="delete each run's counterfactual/ directory first, "
                             "discarding replays already on disk")
    parser.add_argument("--keep-stray-engines", action="store_true",
                        help="do NOT kill orphaned engines between attempts "
                             "(only when you manage the simulator yourself)")
    parser.add_argument("--report", default=None,
                        help="write a JSON campaign report here")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args, extra = parser.parse_known_args(argv)

    logging.basicConfig(
        level=logging.INFO if args.verbose == 0 else logging.DEBUG,
        format="%(levelname)s %(name)s: %(message)s",
    )

    results: List[Dict[str, Any]] = []
    for raw in args.runs:
        run_dir = Path(raw)
        if not (run_dir / "manifest.json").exists():
            LOGGER.error("not a recorded run (no manifest.json): %s", run_dir)
            results.append({"run": str(run_dir), "complete": False,
                            "reason": "no manifest.json", "attempts": 0})
            continue

        if args.fresh:
            # Resume matches replays by configuration hash, which proves the
            # PARAMETERS agree -- not that the recording was sound. A campaign
            # invalidated by something outside the configuration (a simulator
            # lifecycle defect, say) has replays whose hash still matches, and
            # would be silently resumed into the new results. Discarding them
            # has to be an explicit act.
            doomed = run_dir / "counterfactual"
            if doomed.exists():
                LOGGER.info("--fresh: removing %s", doomed)
                shutil.rmtree(str(doomed))

        state = contribution_state(run_dir, args.max_interventions)
        attempt = 0
        exits: List[int] = []
        while not state["complete"] and attempt < args.attempts:
            attempt += 1
            if not args.keep_stray_engines:
                kill_stray_engines()
            LOGGER.info("%s: attempt %d/%d", run_dir, attempt, args.attempts)
            exits.append(run_suite_once(run_dir, args.max_interventions, extra))
            state = contribution_state(run_dir, args.max_interventions)
            LOGGER.info("%s: %d replay outcome(s) after attempt %d",
                        run_dir, state["n_contributions"], attempt)

        row = dict(state, run=str(run_dir), attempts=attempt, exit_codes=exits)
        results.append(row)
        LOGGER.info("%s: %s", run_dir, "COMPLETE" if state["complete"] else "INCOMPLETE")

    complete = [r for r in results if r.get("complete")]
    print("")
    print("{0} of {1} suite(s) complete".format(len(complete), len(results)))
    for r in results:
        print("  {0:<58} {1:<11} attempts={2} replays={3}".format(
            r["run"][-58:], "COMPLETE" if r.get("complete") else "INCOMPLETE",
            r.get("attempts"), r.get("n_contributions")))
        if not r.get("complete"):
            print("      {0}".format(r.get("reason")))

    if args.report:
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"suites": results}, indent=1, sort_keys=True),
                       encoding="utf-8")
        print("wrote {0}".format(out))

    return 0 if len(complete) == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
