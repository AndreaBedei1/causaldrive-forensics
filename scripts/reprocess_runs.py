#!/usr/bin/env python
"""Re-derive every offline stage over already-recorded runs.

Recording needs the simulator; everything after it does not. When an inference
stage changes -- a new event threshold, a richer oracle reference, a corrected
metric -- the honest response is to re-derive the affected artifacts from the
recorded evidence rather than to re-run the simulator, which would also change
the evidence and confound the comparison.

Stages, each independently selectable:

``analyse``  local event extraction and local graphs (``cdf.local.pipeline``)
``fuse``     association and graph fusion (``cdf.fusion.pipeline``)
``oracle``   privileged events and the oracle reference graph
``check``    finite-trace property monitoring
``evaluate`` scoring against the oracle
``ablate``   re-derive fusion with and without post-fusion causal reasoning and
             score both against the oracle, beside the best single viewpoint
``clocks``   re-score the same recording under three clock protocols: a
             synchronized control, independent clocks left uncorrected, and
             independent clocks with the estimated alignment
``figures``  per-run figures
``viewer``   the viewer bundle

Usage::

    python scripts/reprocess_runs.py --artifacts artifacts --stages oracle evaluate
    python scripts/reprocess_runs.py --all-stages
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
from cdf.common.io import read_json, write_json  # noqa: E402
from cdf.common.layout import RunLayout  # noqa: E402
from cdf.evaluation.clock_ablation import run_clock_ablation  # noqa: E402
from cdf.evaluation.method_ablation import ablate_run  # noqa: E402

LOGGER = logging.getLogger("reprocess")

def _round(value, digits=4):
    """Round a metric for the console table, passing ``None`` through."""
    return None if value is None else round(float(value), digits)


ALL_STAGES = ("analyse", "fuse", "oracle", "check", "evaluate", "ablate",
              "clocks", "figures", "viewer", "manifest")


def discover_runs(artifacts_root: Path) -> List[Path]:
    """Every directory that looks like a recorded run, in a stable order."""
    out: List[Path] = []
    for manifest in sorted(artifacts_root.rglob("manifest.json")):
        # A counterfactual replay lives under <run>/counterfactual/replays/<id>/
        # and is scored through its parent, so it is not a run in its own right.
        if "counterfactual" in manifest.parts:
            continue
        out.append(manifest.parent)
    return out


def config_for_run(manifest, scenario_id):
    """The configuration to re-derive a recorded run under.

    The run's own recorded parameters are the base: re-analysing a recording
    under today's thresholds would describe a run that was never made. Keys the
    recording has no value for -- stages added since it was recorded -- are
    filled from the current defaults, which is the only way a new stage can be
    applied to an old recording at all. The result is that every threshold the
    recording depended on is the one it was recorded with, and nothing else is
    silently invented.
    """
    from cdf.common.config import Config

    current = load_run_config(scenario_id=scenario_id)
    recorded = manifest.get("config")
    if not isinstance(recorded, dict) or not recorded:
        return current

    def merge(base, patch):
        """`patch` wins, except where `base` supplies a key `patch` lacks."""
        out = dict(patch)
        for key, value in base.items():
            if key not in out:
                out[key] = value
            elif isinstance(value, dict) and isinstance(out[key], dict):
                out[key] = merge(value, out[key])
        return out

    merged = merge(current.data, recorded)
    return Config(merged, sources=["current defaults", "run manifest"])


def run_stages(run_dir: Path, stages: Sequence[str]) -> Dict[str, Any]:
    """Apply the requested stages to one run, recording per-stage outcomes."""
    from cdf.checking.trace_checker import TraceChecker
    from cdf.common.evidence import load_run
    from cdf.evaluation.suite import evaluate_run
    from cdf.fusion.pipeline import fuse_run
    from cdf.local.pipeline import analyse_run
    from cdf.oracle.graph import build_and_persist
    from cdf.simulation.scenario_base import ScenarioSpec
    from cdf.evaluation.figures import render_run_figures
    from cdf.viewer.bundle import write_bundle
    from cdf.common.io import write_evidence_manifest

    layout = RunLayout.from_run_dir(run_dir)
    manifest = read_json(layout.manifest)
    scenario_id = str(manifest.get("scenario_id", ""))
    variant = str(manifest.get("variant", "")) or None

    cfg = config_for_run(manifest, scenario_id)
    result: Dict[str, Any] = {"run": str(run_dir), "scenario": scenario_id, "variant": variant}

    for stage in stages:
        try:
            if stage == "analyse":
                out = analyse_run(layout, cfg, persist=True)
                result[stage] = {pid: a.summary()["n_events"] for pid, a in out.items()}
            elif stage == "fuse":
                fusion = fuse_run(layout, cfg, persist=True)
                result[stage] = fusion.summary()["n_resolved"]
            elif stage == "oracle":
                spec = ScenarioSpec.from_config(cfg, variant=variant)
                events, _eg, cg = build_and_persist(layout.root, spec, cfg)
                result[stage] = {
                    "n_events": len(events),
                    "n_edges": len(cg.edges),
                    "template": cg.meta.get("n_realised_template_edges"),
                    "mechanical": cg.meta.get("n_mechanical_edges"),
                }
            elif stage == "check":
                run = load_run(layout.root, with_radar=False)
                report = TraceChecker(cfg).check_and_persist(layout, run)
                result[stage] = report.get("summary")
            elif stage == "evaluate":
                spec = ScenarioSpec.from_config(cfg, variant=variant)
                metrics = evaluate_run(layout.root, cfg, spec=spec)
                graphs = metrics.get("graphs") or {}
                best = (graphs.get("best_single_local") or {}).get("metrics") or {}
                result[stage] = {
                    "fused_edge_f1": _round(( graphs.get("fused") or {}).get("edge_f1")),
                    "best_local_edge_f1": _round(best.get("edge_f1")),
                    "delta_edge_f1": _round(graphs.get("delta_edge_f1")),
                    "best_local": graphs.get("best_local_participant_id"),
                }
            elif stage == "ablate":
                ablation = ablate_run(layout, cfg, persist=True)
                arms = ablation["arms"]
                result[stage] = {
                    arm: _round((arms.get(arm, {}).get("strict", {})
                                 .get("edges") or {}).get("f1"))
                    for arm in ("best_local", "simple_fusion",
                                "fusion_global_reasoning")
                }
            elif stage == "clocks":
                report = run_clock_ablation(layout.root, cfg)
                result[stage] = {
                    mode: _round(
                        (block.get("clock") or {}).get("mean_abs_offset_error_s")
                    )
                    for mode, block in report["modes"].items()
                }
            elif stage == "figures":
                made = render_run_figures(layout.root, cfg)
                result[stage] = len(made)
            elif stage == "viewer":
                write_bundle(layout.root, cfg)
                result[stage] = "ok"
            elif stage == "manifest":
                # Rewritten last: the recording-time manifest cannot cover the
                # artifacts that analysis, fusion, the oracle, checking,
                # evaluation and the viewer bundle add afterwards.
                written = write_evidence_manifest(
                    layout.root, extra={"stage": "reprocess",
                                        "run_id": manifest.get("run_id")})
                result[stage] = read_json(written).get("n_files")
            else:
                raise ValueError("unknown stage {0!r}".format(stage))
        except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
            LOGGER.error("%s: stage %s failed: %s", run_dir.name, stage, exc)
            LOGGER.debug("%s", traceback.format_exc())
            result[stage] = {"error": "{0}: {1}".format(type(exc).__name__, exc)}
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--stages", nargs="+", default=["oracle", "evaluate"])
    parser.add_argument("--all-stages", action="store_true")
    parser.add_argument("--scenarios", nargs="+", default=None)
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.WARNING if args.verbose == 0 else logging.INFO,
        format="%(levelname)s %(name)s: %(message)s",
    )

    stages = list(ALL_STAGES) if args.all_stages else list(args.stages)
    root = Path(args.artifacts)
    runs = discover_runs(root)
    if args.scenarios:
        wanted = {s.upper() for s in args.scenarios}
        runs = [r for r in runs if r.parent.name.split("_")[0].upper() in wanted]

    print("reprocessing {0} run(s), stages: {1}".format(len(runs), ", ".join(stages)))
    rows: List[Dict[str, Any]] = []
    failed = 0
    for run_dir in runs:
        row = run_stages(run_dir, stages)
        rows.append(row)
        errs = [s for s in stages if isinstance(row.get(s), dict) and "error" in row[s]]
        if errs:
            failed += 1
            print("  FAIL {0:<52} {1}".format(run_dir.name, ", ".join(errs)))
        else:
            summary = row.get("evaluate") or row.get("oracle") or "ok"
            print("  ok   {0:<52} {1}".format(
                "{0}/{1}".format(run_dir.parent.name, run_dir.name), summary))

    write_json(root / "summary" / "reprocess_report.json", {"runs": rows, "stages": stages})
    print("{0} ok, {1} failed".format(len(rows) - failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
