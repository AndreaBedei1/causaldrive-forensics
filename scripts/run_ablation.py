#!/usr/bin/env python
"""Radar-degradation ablation: the same encounter through worse sensors.

Everything about the scenario is held fixed -- map, spawn state, seed, scripted
actions, controller parameters -- and only the radar profile changes. The
question is how far the reconstruction degrades when the evidence does, which is
the ablation the experiment protocol calls for and which the fusion and
association numbers cannot answer on their own.

Degradation is injected in the local radar front-end from a seeded stream rather
than requested from the simulator, so a degraded run is reproducible and the
*physics* of the encounter is identical across profiles. Only what the vehicles
could see differs.

    python scripts/run_ablation.py --scenario S01 --variant crash --seed 0 \
        --profiles radar_baseline radar_noisy radar_dropout radar_degraded

Results land under ``<artifacts>/ablation/<profile>/...`` so they never collide
with the main campaign, and a summary table is written to
``<artifacts>/summary/ablation.json``.
"""

from __future__ import annotations

import argparse
import logging
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cdf.common.config import load_run_config  # noqa: E402
from cdf.common.io import write_csv, write_json  # noqa: E402
from cdf.common.layout import RunLayout  # noqa: E402

LOGGER = logging.getLogger("ablation")


def _scenario_name(scenario: str, variant: Optional[str]) -> str:
    """The scenario's directory name, taken from its own specification."""
    from cdf.common.config import load_run_config as _load
    from cdf.simulation.scenario_base import ScenarioSpec
    return ScenarioSpec.from_config(_load(scenario_id=scenario), variant=variant).name


def completed_row(root: Path, profile: str, scenario: str, variant: Optional[str],
                  seed: int) -> Optional[Dict[str, Any]]:
    """A profile already recorded and scored, rebuilt from its run directory.

    The sweep restarts the simulator once per profile, and on this build the
    native client aborts the interpreter on the third simulator process of a
    process (``docs/ENVIRONMENT.md``, finding 10). Re-running the sweep therefore
    has to pick up where it stopped, or it can never get past the third profile.

    The row is rebuilt from the run directory's own artifacts and **not** read
    back out of a previous ``summary/ablation.json``. A stale summary describes
    whatever ran last time; the run directory describes what is on disk now.
    Reading the summary would have quietly carried an old sweep's numbers into a
    new one whenever the run directories were re-recorded under the same paths.
    """
    from cdf.common.io import read_json as _read
    from cdf.common.layout import RunLayout

    run_dir = Path(RunLayout.create(
        root / "ablation" / profile, scenario, _scenario_name(scenario, variant),
        seed, variant).root)
    metrics_path = run_dir / "evaluation" / "metrics.json"
    manifest_path = run_dir / "manifest.json"
    if not metrics_path.exists() or not manifest_path.exists():
        return None
    try:
        metrics = _read(metrics_path)
        manifest = _read(manifest_path)
    except (OSError, ValueError):
        return None

    graphs = metrics.get("graphs") or {}
    best = ((graphs.get("best_single_local") or {}).get("metrics")) or {}
    fused = graphs.get("fused") or {}
    assoc = metrics.get("association") or {}

    per_observer: Dict[str, int] = {}
    n_tracks = 0
    assoc_path = run_dir / "fusion" / "association_report.json"
    if assoc_path.exists():
        try:
            report = _read(assoc_path)
        except (OSError, ValueError):
            report = {}
        for assignment in report.get("assignments") or []:
            observer = str(assignment.get("observer_id") or "?")
            per_observer[observer] = per_observer.get(observer, 0) + 1
            n_tracks += 1

    validation: Dict[str, Any] = {}
    validation_path = run_dir / "scenario_validation.json"
    if validation_path.exists():
        try:
            validation = _read(validation_path)
        except (OSError, ValueError):
            validation = {}

    return {
        "profile": profile,
        "scenario": manifest.get("scenario_id"),
        "variant": manifest.get("variant"),
        "seed": manifest.get("seed"),
        "outcome": manifest.get("outcome"),
        "validation_passed": validation.get("passed"),
        "n_tracks_total": n_tracks,
        "tracks_by_participant": per_observer,
        "assoc_correct": assoc.get("n_correct"),
        "assoc_incorrect": assoc.get("n_incorrect"),
        "assoc_unresolved": assoc.get("n_unresolved"),
        "assoc_precision": assoc.get("precision"),
        "assoc_mean_rmse_m": assoc.get("mean_rmse_m"),
        "best_local_edge_f1": best.get("edge_f1"),
        "best_local_node_f1": best.get("node_f1"),
        "fused_edge_f1": fused.get("edge_f1"),
        "fused_node_f1": fused.get("node_f1"),
        "fused_node_recall": fused.get("node_recall"),
        "n_resolved": None,
        "run_dir": str(run_dir),
        "resumed": True,
    }


def run_one(session: Any, scenario: str, variant: Optional[str], seed: int,
            profile: str, artifacts_root: Path) -> Dict[str, Any]:
    """Record, analyse, fuse and score one (scenario, profile) combination."""
    from cdf.evaluation.suite import evaluate_run
    from cdf.fusion.pipeline import fuse_run
    from cdf.local.pipeline import analyse_run
    from cdf.oracle.graph import build_and_persist
    from cdf.simulation.runner import run_scenario
    from cdf.simulation.scenario_base import ScenarioSpec

    cfg = load_run_config(scenario_id=scenario, sensor_profile=profile)
    spec = ScenarioSpec.from_config(cfg, variant=variant)

    root = artifacts_root / "ablation" / profile
    layout = RunLayout.create(root, spec.scenario_id, spec.name, seed, spec.variant)

    # A fresh simulator per run: reused servers drift enough to change an
    # outcome class, which would confound a comparison whose whole point is that
    # only the sensor differs (docs/ENVIRONMENT.md).
    session.fresh_world_for_map(spec.map_name)
    result = run_scenario(
        session.client(), cfg, spec, seed=seed, artifacts_root=str(root),
        persist=True, layout=layout,
    )

    analyse_run(layout.root, cfg)
    fusion = fuse_run(layout.root, cfg)
    build_and_persist(layout.root, spec, cfg)
    metrics = evaluate_run(layout.root, cfg, spec=spec)

    graphs = metrics.get("graphs") or {}
    best = ((graphs.get("best_single_local") or {}).get("metrics")) or {}
    fused = graphs.get("fused") or {}
    assoc = metrics.get("association") or {}
    evidence = {
        pid: {"n_tracks": len(ev.track_ids()), "n_track_samples": len(ev.tracks)}
        for pid, ev in result.evidence.items()
    }
    return {
        "profile": profile,
        "scenario": spec.scenario_id,
        "variant": spec.variant,
        "seed": seed,
        "outcome": result.manifest.outcome.value,
        "validation_passed": result.validation.get("passed"),
        "n_tracks_total": sum(v["n_tracks"] for v in evidence.values()),
        "tracks_by_participant": {p: v["n_tracks"] for p, v in evidence.items()},
        "assoc_correct": assoc.get("n_correct"),
        "assoc_incorrect": assoc.get("n_incorrect"),
        "assoc_unresolved": assoc.get("n_unresolved"),
        "assoc_precision": assoc.get("precision"),
        "assoc_mean_rmse_m": assoc.get("mean_rmse_m"),
        "best_local_edge_f1": best.get("edge_f1"),
        "best_local_node_f1": best.get("node_f1"),
        "fused_edge_f1": fused.get("edge_f1"),
        "fused_node_f1": fused.get("node_f1"),
        "fused_node_recall": fused.get("node_recall"),
        "n_resolved": fusion.summary().get("n_resolved"),
        "run_dir": str(layout.root),
    }


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default="S01")
    parser.add_argument("--variant", default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--profiles",
        nargs="+",
        default=["radar_baseline", "radar_noisy", "radar_dropout", "radar_degraded"],
    )
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--no-resume", action="store_true",
                        help="re-record every profile, even ones already scored")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.WARNING if args.verbose == 0 else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    from cdf.simulation.carla_client import session_from_config

    artifacts_root = Path(args.artifacts)
    cfg = load_run_config(scenario_id=args.scenario)
    rows: List[Dict[str, Any]] = []
    failures = 0

    pending = list(args.profiles)
    if not args.no_resume:
        for profile in list(pending):
            done = completed_row(artifacts_root, profile, args.scenario,
                                 args.variant, args.seed)
            if done is not None:
                rows.append(done)
                pending.remove(profile)
                print("  {0:<18} reusing the profile already on disk".format(profile))
    if not pending:
        print("every requested profile is already recorded")

    with session_from_config(cfg, autostart=True) as session:
        for profile in pending:
            try:
                row = run_one(session, args.scenario, args.variant, args.seed,
                              profile, artifacts_root)
                rows.append(row)
                print("  {0:<18} outcome={1:<10} tracks={2:<3} assoc_ok={3} "
                      "fused_node_f1={4}".format(
                          profile, row["outcome"], row["n_tracks_total"],
                          row["assoc_correct"],
                          "-" if row["fused_node_f1"] is None
                          else round(row["fused_node_f1"], 3)))
            except Exception as exc:  # noqa: BLE001 - recorded, never swallowed
                failures += 1
                LOGGER.error("profile %s failed: %s", profile, exc)
                LOGGER.debug("%s", traceback.format_exc())
                rows.append({"profile": profile,
                             "error": "{0}: {1}".format(type(exc).__name__, exc)})

    order = {name: i for i, name in enumerate(args.profiles)}
    rows.sort(key=lambda r: order.get(r.get("profile"), len(order)))

    out = artifacts_root / "summary"
    write_json(out / "ablation.json", {"scenario": args.scenario,
                                       "variant": args.variant,
                                       "seed": args.seed, "rows": rows})
    write_csv(out / "ablation.csv", [r for r in rows if "error" not in r])
    print("wrote {0} and {1}".format(out / "ablation.json", out / "ablation.csv"))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
