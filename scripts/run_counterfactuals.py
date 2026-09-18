#!/usr/bin/env python
"""Replay every scenario variant of a campaign under its candidate interventions.

Counterfactual replay is the only thing that can turn a causal hypothesis read
off the graph into a statement about necessity, and it is also the most
expensive stage in the project: each replay is a complete re-run of the
encounter in the simulator. This driver runs them one scenario variant at a
time, in a fresh subprocess each, so that a crash in one leaves the rest of the
sweep intact and a partially finished sweep can be resumed.

The negative controls are included deliberately. A scenario designed not to
collide has nothing to attribute, and the useful measurement there is whether
the system stays silent -- which cannot be measured without running it.

Usage::

    python scripts/run_counterfactuals.py --artifacts artifacts_independent_clocks
    python scripts/run_counterfactuals.py --seeds 0 --attempts 2
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from cdf.common.io import read_json, write_json  # noqa: E402
from cdf.common.layout import RunLayout  # noqa: E402

LOGGER = logging.getLogger("counterfactuals")

STATUS_FILE = "counterfactual_runs.json"


def discover(artifacts_root: Path, seeds: Sequence[int]) -> List[Path]:
    """Every primary run of the requested seeds, in a stable order.

    A counterfactual replay is itself a run directory, so replays are excluded:
    replaying a replay would answer a question nobody asked.
    """
    out: List[Path] = []
    for manifest_path in sorted(artifacts_root.rglob("manifest.json")):
        if "counterfactual" in manifest_path.parts:
            continue
        try:
            manifest = read_json(manifest_path)
        except (OSError, ValueError):
            continue
        seed = manifest.get("seed")
        if seed is not None and int(seed) not in seeds:
            continue
        out.append(manifest_path.parent)
    return out


def already_done(run_dir: Path) -> bool:
    """Whether this run already carries a complete attribution."""
    layout = RunLayout.from_run_dir(run_dir)
    if not layout.causal_contribution.exists():
        return False
    try:
        payload = read_json(layout.causal_contribution)
    except (OSError, ValueError):
        return False
    return bool(payload.get("classification"))


def replay_protocol(run_dir: Path) -> Dict[str, Any]:
    """What protocol the replays of this run actually ran under.

    Each run is replayed in its own subprocess whose output this driver captures
    and, on success, discards. That is fine for progress chatter and not fine for
    the one warning a reader of the results has to see: a sweep whose replays
    silently shared a simulator session is not a sweep whose verdicts can be
    compared. So the protocol is read back out of the artifact the run wrote,
    rather than scraped out of a log that may never be looked at.
    """
    layout = RunLayout.from_run_dir(run_dir)
    if not layout.causal_contribution.exists():
        return {}
    try:
        return dict(read_json(layout.causal_contribution).get("replay_protocol") or {})
    except (OSError, ValueError):
        return {}


def run_one(
    run_dir: Path, artifacts_root: Path, attempts: int, fresh: bool = False
) -> Dict[str, Any]:
    """Replay one run's interventions in a subprocess, retrying on failure."""
    command = [
        sys.executable, "-m", "cdf.cli", "counterfactuals",
        "--artifacts", str(artifacts_root),
        "--run", str(run_dir),
        "-v",
    ]
    if fresh:
        command.extend(["--config-overrides", "counterfactual.resume=false"])
    last: Optional[str] = None
    for attempt in range(1, attempts + 1):
        started = time.time()
        result = subprocess.run(
            command, cwd=str(REPO), capture_output=True, text=True
        )
        elapsed = time.time() - started
        if result.returncode == 0:
            return {
                "status": "completed",
                "attempts": attempt,
                "seconds": round(elapsed, 1),
            }
        last = (result.stderr or result.stdout or "").strip().splitlines()
        last = last[-1] if last else "exit {0}".format(result.returncode)
        LOGGER.warning(
            "%s: attempt %d/%d failed: %s", run_dir.name, attempt, attempts, last
        )
    return {"status": "failed", "attempts": attempts, "error": last}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", default="artifacts_independent_clocks")
    parser.add_argument(
        "--seeds", type=int, nargs="+", default=[0],
        help="which seeds to replay; one seed per variant is the default because "
             "a replay sweep costs a full simulator run per intervention",
    )
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument(
        "--force", action="store_true",
        help="replay runs that already carry an attribution",
    )
    parser.add_argument(
        "--fresh", action="store_true",
        help=(
            "re-record every replay instead of reusing a completed one. Use this "
            "when the existing replays were recorded under a degraded protocol "
            "-- for instance back-to-back on one simulator session, which the "
            "configuration warns drifts enough to change an outcome class and "
            "would confound the very difference being measured"
        ),
    )
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(name)s: %(message)s"
    )
    artifacts_root = (REPO / args.artifacts).resolve()
    if not artifacts_root.exists():
        LOGGER.error("artifacts root does not exist: %s", artifacts_root)
        return 2

    runs = discover(artifacts_root, args.seeds)
    if not runs:
        LOGGER.error("no run with seed(s) %s under %s", args.seeds, artifacts_root)
        return 2

    print("{0} run(s) to replay".format(len(runs)))
    status: Dict[str, Any] = {}
    degraded_runs: List[str] = []
    for run_dir in runs:
        name = "{0}/{1}".format(run_dir.parent.name, run_dir.name)
        if not args.force and already_done(run_dir):
            print("  {0:<52} already attributed".format(name))
            status[name] = {"status": "skipped", "reason": "already attributed"}
            continue
        LOGGER.info("replaying %s", name)
        outcome = run_one(run_dir, artifacts_root, args.attempts, fresh=args.fresh)
        protocol = replay_protocol(run_dir)
        outcome["replay_protocol"] = protocol.get("effective")
        status[name] = outcome
        degraded = (
            protocol.get("effective")
            and protocol["effective"] != "fresh_server_per_replay"
        )
        if degraded:
            degraded_runs.append(name)
        print(
            "  {0:<52} {1} ({2}){3}".format(
                name, outcome["status"],
                "{0:.0f}s".format(outcome.get("seconds", 0.0))
                if outcome["status"] == "completed" else outcome.get("error", ""),
                "  [DEGRADED: replays shared a simulator session]" if degraded else "",
            )
        )

    summary_dir = artifacts_root / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        summary_dir / STATUS_FILE,
        {
            "seeds": list(args.seeds),
            "runs": status,
            "degraded_runs": degraded_runs,
        },
    )

    failed = [k for k, v in status.items() if v["status"] == "failed"]
    print(
        "{0} completed, {1} skipped, {2} failed".format(
            sum(1 for v in status.values() if v["status"] == "completed"),
            sum(1 for v in status.values() if v["status"] == "skipped"),
            len(failed),
        )
    )
    if degraded_runs:
        # Loud, and a non-zero exit: verdicts from replays that shared a session
        # are not comparable with each other, and a sweep that ends "13
        # completed" while that is true has reported success for nothing.
        print(
            "\n{0} run(s) replayed on a SHARED simulator session and are not "
            "reliably comparable:".format(len(degraded_runs))
        )
        for name in degraded_runs:
            print("  " + name)
        print(
            "Stop any simulator already holding the RPC port, set $CARLA_ROOT, "
            "and re-run with --force --fresh."
        )
    return 1 if (failed or degraded_runs) else 0


if __name__ == "__main__":
    raise SystemExit(main())
