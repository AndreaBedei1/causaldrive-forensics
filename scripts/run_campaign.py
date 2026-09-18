#!/usr/bin/env python
"""Record a full experimental campaign: every scenario, every variant, every seed.

::

    python scripts/run_campaign.py --artifacts artifacts_v2 \\
        --seeds 0 1 2 --attempts 3

The combinations are enumerated from the scenario files, never written down: the
campaign is "every variant every scenario declares, at every seed", and
:func:`cdf.cli.suite_combinations` is the single source of that list. Adding a
scenario file therefore adds it to the campaign, with no list to keep in step.

V1 and V2 do not share a root
-----------------------------

V2 changes the sensor suite and the timing semantics, so a V1 recording is not a
V2 result and averaging the two would produce a number describing neither. The
default root is now ``artifacts_v2``, and recording into a root that already
holds runs from the other generation is refused rather than merged -- the failure
mode being guarded against is the quiet one, where a campaign resumes into an old
directory and the summary tables come out of a mixture.

Why one subprocess per run rather than ``cdf suite``
---------------------------------------------------

A run is only reproducible from a freshly booted server: repeated runs in one
server session drift far enough to change an outcome class
(``docs/ENVIRONMENT.md``). Each run therefore gets its own process, which opens
its own session and leaves a clean one behind. That also contains the
interpreter abort this build shows after several simulator restarts in one
process -- it kills the child, not the campaign.

Stray engines are killed between attempts, and that is required for correctness
rather than tidiness: after an abort the teardown never runs, the orphaned engine
keeps holding the RPC port, and the next "fresh" server silently reconnects to
it.

Every run's fate is persisted -- completed, failed, retried, resumed, and why --
so a campaign is never reported as finished while a run failed quietly.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

LOGGER = logging.getLogger("campaign")

#: The engine image names; the launcher is deliberately absent because it exits
#: immediately and killing it stops nothing.
ENGINE_IMAGES = ("CarlaUE4-Win64-Shipping.exe", "CarlaUE4-Linux-Shipping")


def kill_stray_engines(settle_s: float = 5.0) -> int:
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
        LOGGER.info("killed %d stray engine(s)", killed)
        time.sleep(settle_s)
    return killed


def run_dir_for(artifacts_root: Path, scenario_id: str, variant: str, seed: int) -> Path:
    from cdf.common.config import load_run_config
    from cdf.common.layout import RunLayout
    from cdf.simulation.scenario_base import ScenarioSpec

    cfg = load_run_config(scenario_id=scenario_id)
    spec = ScenarioSpec.from_config(cfg, variant=variant)
    return RunLayout.create(
        artifacts_root, spec.scenario_id, spec.name, seed, spec.variant
    ).root


def run_state(run_dir: Path) -> Dict[str, Any]:
    """Whether this run is already recorded and validated."""
    validation = run_dir / "scenario_validation.json"
    manifest = run_dir / "manifest.json"
    if not manifest.exists() or not validation.exists():
        return {"complete": False, "reason": "not recorded"}
    try:
        with open(str(validation), encoding="utf-8") as handle:
            doc = json.load(handle)
    except (OSError, ValueError) as exc:
        return {"complete": False, "reason": "unreadable validation: {0}".format(exc)}
    passed = bool(doc.get("passed"))
    return {
        "complete": passed,
        "reason": "" if passed else "scenario validation failed: {0}".format(
            doc.get("problems")
        ),
        "problems": doc.get("problems"),
    }


def record_one(
    scenario_id: str, variant: str, seed: int, artifacts_root: Path,
    overrides: Sequence[str], log_dir: Optional[Path],
) -> int:
    cmd = [
        sys.executable, "-m", "cdf.cli", "run",
        "--scenario", scenario_id,
        "--variant", variant,
        "--seed", str(seed),
        "--artifacts", str(artifacts_root),
    ]
    for item in overrides:
        cmd += ["--config-overrides", item]
    env = dict(os.environ, PYTHONUNBUFFERED="1")
    src = str(Path(__file__).resolve().parents[1] / "src")
    env["PYTHONPATH"] = src + os.pathsep + env.get("PYTHONPATH", "")
    LOGGER.info("recording %s/%s seed %d", scenario_id, variant, seed)
    if log_dir is None:
        return subprocess.call(cmd, env=env)
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / "{0}_{1}_seed{2:03d}.log".format(scenario_id, variant, seed)
    with open(str(path), "w", encoding="utf-8") as handle:
        return subprocess.call(cmd, env=env, stdout=handle, stderr=subprocess.STDOUT)


#: A run recorded with a camera is V2; one recorded without is V1. The marker is
#: the artifact rather than the directory name, because a directory can be
#: renamed and a recording cannot be re-sensored.
def run_generation(run_dir: Path) -> Optional[str]:
    """``"v2"``, ``"v1"``, or ``None`` when the directory holds no run."""
    if not (run_dir / "manifest.json").is_file():
        return None
    for vehicle in sorted(run_dir.glob("vehicle_*")):
        if (vehicle / "video").is_dir() or (vehicle / "perception").is_dir():
            return "v2"
        if (vehicle / "local_log.json").is_file():
            return "v2"
    return "v1"


def generation_conflict(artifacts_root: Path) -> Optional[str]:
    """Whether this root already holds runs of a different generation.

    Returns the message to print, or ``None`` when the root is empty or
    consistent. Reported as a refusal rather than a warning: a campaign that
    resumed into the wrong root would produce summary tables computed over a
    mixture, and nothing downstream could tell.
    """
    if not artifacts_root.is_dir():
        return None
    found = {}
    # scenario / run only. The deeper manifests under counterfactual/replays are
    # replays of a run rather than runs, and counting them would let one V1 run
    # look like a dozen.
    for manifest in artifacts_root.glob("*/*/manifest.json"):
        generation = run_generation(manifest.parent)
        if generation:
            found.setdefault(generation, []).append(
                manifest.parent.relative_to(artifacts_root).as_posix()
            )
    if len(found) < 2:
        return None
    return (
        "{0} already holds runs of both generations: {1} v1 and {2} v2 (for "
        "example {3} and {4}). V2 changed the sensors and the timing semantics, "
        "so results averaged over a mixture describe neither campaign. Use a "
        "fresh root, or --allow-mixed-generations if the mixture is "
        "deliberate".format(
            artifacts_root, len(found["v1"]), len(found["v2"]),
            sorted(found["v1"])[0], sorted(found["v2"])[0],
        )
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--artifacts", default="artifacts_v2")
    parser.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    parser.add_argument("--scenarios", nargs="+", default=None)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--config-overrides", nargs="*", default=[])
    parser.add_argument("--fresh", action="store_true",
                        help="re-record every run, ignoring what is on disk")
    parser.add_argument("--keep-stray-engines", action="store_true")
    parser.add_argument(
        "--allow-mixed-generations", action="store_true",
        help=(
            "record into a root that already holds runs from the other "
            "generation. Only for deliberately re-recording one scenario in "
            "place; the resulting root must not be used for campaign averages"
        ),
    )
    parser.add_argument("--logs", default=None, help="per-run log directory")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    from cdf.cli import suite_combinations
    from cdf.common.config import available_scenarios

    scenarios = list(args.scenarios) if args.scenarios else available_scenarios()
    combinations = suite_combinations(scenarios, args.config_overrides)
    artifacts_root = Path(args.artifacts)
    conflict = generation_conflict(artifacts_root)
    if conflict and not args.allow_mixed_generations:
        print("REFUSING: " + conflict)
        return 2
    log_dir = Path(args.logs) if args.logs else artifacts_root / "logs"

    plan = [
        (scenario_id, variant, seed)
        for scenario_id, variant in combinations
        for seed in args.seeds
    ]
    print("{0} scenario/variant combination(s) x {1} seed(s) = {2} run(s)".format(
        len(combinations), len(args.seeds), len(plan)))

    results: List[Dict[str, Any]] = []
    for scenario_id, variant, seed in plan:
        run_dir = run_dir_for(artifacts_root, scenario_id, variant, seed)
        state = run_state(run_dir)
        row: Dict[str, Any] = {
            "scenario_id": scenario_id,
            "variant": variant,
            "seed": seed,
            "run_dir": run_dir.as_posix(),
            "attempts": 0,
            "exit_codes": [],
            "status": "pending",
        }
        if state["complete"] and not args.fresh:
            row["status"] = "resumed"
            row["reason"] = "already recorded and validated"
            results.append(row)
            print("  {0:<28} resumed".format("{0}/{1}/{2}".format(scenario_id, variant, seed)))
            continue

        while row["attempts"] < args.attempts and not state["complete"]:
            row["attempts"] += 1
            if not args.keep_stray_engines:
                kill_stray_engines()
            code = record_one(
                scenario_id, variant, seed, artifacts_root,
                args.config_overrides, log_dir,
            )
            row["exit_codes"].append(code)
            state = run_state(run_dir)

        row["status"] = "completed" if state["complete"] else "failed"
        row["reason"] = state.get("reason", "")
        if row["attempts"] > 1 and state["complete"]:
            row["status"] = "completed_after_retry"
        results.append(row)
        print("  {0:<28} {1} (attempts={2})".format(
            "{0}/{1}/{2}".format(scenario_id, variant, seed),
            row["status"], row["attempts"]))

    summary_dir = artifacts_root / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": "1.0.0",
        "artifacts_root": artifacts_root.as_posix(),
        "n_combinations": len(combinations),
        "seeds": list(args.seeds),
        "n_planned": len(plan),
        "n_completed": sum(1 for r in results if r["status"].startswith("completed")),
        "n_resumed": sum(1 for r in results if r["status"] == "resumed"),
        "n_failed": sum(1 for r in results if r["status"] == "failed"),
        "combinations": [list(c) for c in combinations],
        "runs": results,
    }
    out = summary_dir / "campaign_runs.json"
    out.write_text(json.dumps(report, indent=1, sort_keys=True), encoding="utf-8")
    print("")
    print("{0} completed, {1} resumed, {2} failed of {3} planned".format(
        report["n_completed"], report["n_resumed"], report["n_failed"], len(plan)))
    print("wrote {0}".format(out))
    if not args.keep_stray_engines:
        kill_stray_engines()
    return 0 if report["n_failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
