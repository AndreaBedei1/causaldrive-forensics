"""The reported results, derived from the artifacts rather than transcribed.

Every number in the project's documentation comes from here, and this module
reads nothing but the files a campaign wrote. That is the whole point: a result
typed into a README by hand is a claim about a run that may no longer exist,
and the only defence against it drifting away from the truth is to make the
prose regenerable.

Three files are produced under ``<artifacts_root>/summary``:

``final_results.json``
    every number, nested, with the run counts each was averaged over;
``final_results.csv``
    the per-scenario table, one row per scenario;
``final_results.md``
    the two tables the write-up quotes, plus the campaign's headline figures.

Averaging rules, which are the part that can quietly mislead:

* A scenario designed **not** to collide has nothing to attribute. Its
  attribution F1 is a vacuous 1.0 and is excluded from the attribution means;
  what is reported for it instead is whether the system stayed silent.
* Runs are averaged per scenario first and then across scenarios, so a scenario
  with three seeds does not outweigh one with fewer.
* A metric that was not computed for a run is absent, never zero. A mean is
  reported with the number of runs behind it, so a figure resting on two runs
  cannot be mistaken for one resting on twenty.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from ..common.io import read_json, write_csv, write_json
from ..common.layout import RunLayout
from .suite import RUN_KIND_PRIMARY, _run_dirs, summary_dir

LOGGER = logging.getLogger(__name__)

__all__ = ["build_final_results", "write_final_results", "FINAL_COLUMNS"]

PathLike = Union[str, Path]

FINAL_COLUMNS: Tuple[str, ...] = (
    "scenario_id",
    "variant",
    "n_runs",
    "expect_collision",
    "incident_reconstructed",
    "contributors_ground_truth",
    "contributors_inferred",
    "attribution_class",
    "attribution_precision",
    "attribution_recall",
    "attribution_f1",
    "exact_set_match",
    "verdict",
    "collision_time_error_s",
    "collision_location_error_m",
    "cross_view_rmse_m",
    "causal_path_f1",
    "ancestry_recall",
    "node_f1_best_local",
    "node_f1_fused",
    "edge_f1_best_local",
    "edge_f1_fused",
    "edge_recall_fused",
    "edge_recall_ceiling",
)


def _mean(values: Sequence[Optional[float]]) -> Optional[float]:
    present = [float(v) for v in values if v is not None]
    return sum(present) / len(present) if present else None


def _round(value: Optional[float], digits: int = 4) -> Optional[float]:
    return None if value is None else round(float(value), digits)


def _get(block: Optional[Mapping[str, Any]], *path: str) -> Any:
    """Walk a nested mapping, returning ``None`` at the first missing step."""
    current: Any = block
    for key in path:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _verdict(row: Mapping[str, Any]) -> str:
    """One word for what the system did with this scenario.

    ``correct`` -- named exactly the designed contributors; ``partial`` -- named
    some of them and nobody else, or some plus somebody else; ``incorrect`` --
    named only vehicles that did not contribute; ``insufficient evidence`` --
    named nobody where somebody was designed; ``restrained`` -- correctly named
    nobody on a scenario designed not to collide; ``false attribution`` --
    named somebody there.
    """
    if not row["expect_collision"]:
        return "false attribution" if row["contributors_inferred"] else "restrained"
    if not row["contributors_inferred"]:
        return "insufficient evidence"
    if row["exact_set_match"]:
        return "correct"
    truth = set(row["contributors_ground_truth"])
    named = set(row["contributors_inferred"])
    return "partial" if truth & named else "incorrect"


def _run_rows(artifacts_root: Path) -> List[Dict[str, Any]]:
    """One row per scored run, reading only what that run wrote."""
    rows: List[Dict[str, Any]] = []
    for run_dir in _run_dirs(artifacts_root, kinds=(RUN_KIND_PRIMARY,)):
        layout = RunLayout.from_run_dir(run_dir)
        if not layout.metrics.exists():
            continue
        metrics = read_json(layout.metrics)
        ablation_path = layout.evaluation_dir / "method_ablation.json"
        ablation = read_json(ablation_path) if ablation_path.exists() else None
        reconstruction = (
            read_json(layout.incident_reconstruction)
            if layout.incident_reconstruction.exists() else None
        )

        sets = metrics.get("attribution_sets") or {}
        scene = metrics.get("scene_reconstruction") or {}
        paths = metrics.get("causal_paths") or {}
        graphs = metrics.get("graphs") or {}
        best_local = _get(graphs, "best_single_local", "metrics") or {}
        fused = graphs.get("fused") or {}

        # The replay's verdict when one ran; otherwise what the graph alone
        # concluded. Which of the two it is travels with the row.
        inferred = sets.get("predicted_participants") or []
        source = "counterfactual_replay"
        if not sets.get("scored"):
            inferred = _get(sets, "graph_only", "predicted_participants") or []
            source = "fused_graph_only"

        rows.append(
            {
                "run_path": run_dir.as_posix(),
                "scenario_id": metrics.get("scenario_id", ""),
                "variant": metrics.get("variant", ""),
                "seed": metrics.get("seed"),
                "expect_collision": bool(sets.get("expect_collision")),
                "incident_reconstructed": bool(
                    reconstruction and (reconstruction.get("incidents") or [])
                ),
                "n_reconstructed_collisions": (
                    reconstruction.get("n_collisions") if reconstruction else None
                ),
                "contributors_ground_truth": list(sets.get("truth_participants") or []),
                "contributors_inferred": list(inferred),
                "attribution_source": source,
                "attribution_class": (
                    sets.get("normalised_class")
                    or _get(sets, "graph_only", "attribution_class")
                ),
                "attribution_precision": (
                    sets.get("precision") if sets.get("scored")
                    else _get(sets, "graph_only", "precision")
                ),
                "attribution_recall": (
                    sets.get("recall") if sets.get("scored")
                    else _get(sets, "graph_only", "recall")
                ),
                "attribution_f1": (
                    sets.get("f1") if sets.get("scored")
                    else _get(sets, "graph_only", "f1")
                ),
                "exact_set_match": bool(
                    sets.get("exact_set_match") if sets.get("scored")
                    else _get(sets, "graph_only", "exact_set_match")
                ),
                "false_attribution": sets.get("false_attribution"),
                "vacuous_attribution": bool(sets.get("vacuous")),
                "collision_time_error_s": scene.get("collision_time_error_s"),
                "collision_location_error_m": scene.get("collision_location_error_m"),
                "collision_pair_recall": scene.get("collision_pair_recall"),
                "n_spurious_collisions": scene.get("n_spurious_collisions"),
                "collision_order_correct": scene.get("collision_order_correct"),
                "cross_view_rmse_m": _get(scene, "cross_view", "rmse_m"),
                "causal_path_precision": _get(paths, "path", "precision"),
                "causal_path_recall": _get(paths, "path", "recall"),
                "causal_path_f1": _get(paths, "path", "f1"),
                "ancestry_recall": _get(paths, "ancestry", "recall"),
                "node_f1_best_local": best_local.get("node_f1"),
                "node_f1_fused": fused.get("node_f1"),
                "edge_f1_best_local": best_local.get("edge_f1"),
                "edge_f1_fused": fused.get("edge_f1"),
                "edge_recall_fused": fused.get("edge_recall"),
                "edge_recall_ceiling": _get(
                    ablation, "reference_reachability", "strict_edge_recall_ceiling"
                ),
                "clock_offset_mae_s": _get(
                    metrics, "clock_alignment", "mean_abs_offset_error_s"
                ),
                "clock_drift_mae_ppm": _get(
                    metrics, "clock_alignment", "mean_abs_drift_error_ppm"
                ),
                "clock_alignment_residual_s": _get(
                    metrics, "clock_alignment", "alignment_residual"
                ),
                "ablation": _ablation_row(ablation),
                "model_check": _model_check_row(metrics.get("model_check")),
            }
        )
    rows.sort(key=lambda r: (r["scenario_id"], r["variant"], r["seed"] or 0))
    return rows


def _ablation_row(ablation: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """The three arms of one run's method ablation, flattened."""
    if not ablation:
        return {}
    out: Dict[str, Any] = {}
    for arm in ("best_local", "simple_fusion", "fusion_global_reasoning"):
        block = _get(ablation, "arms", arm) or {}
        for vocabulary in ("strict", "canonical"):
            for measure in ("nodes", "edges"):
                scores = _get(block, vocabulary, measure) or {}
                for metric in ("precision", "recall", "f1"):
                    out["{0}.{1}.{2}.{3}".format(arm, vocabulary, measure, metric)] = (
                        scores.get(metric)
                    )
    return out


def _model_check_row(block: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """The verdict tally for one run, as the checking stage records it.

    ``UNKNOWN`` is a first-class verdict here, not a missing ``PASS``: a finite
    trace that never exhibits a property's premise cannot satisfy or violate it,
    and reporting that as a pass would claim evidence the run does not contain.
    """
    if not block:
        return {}
    counts = block.get("counts") or {}
    return {
        "n_pass": int(counts.get("PASS", 0)),
        "n_fail": int(counts.get("FAIL", 0)),
        "n_unknown": int(counts.get("UNKNOWN", 0)),
        "n_properties": int(block.get("n_results") or 0),
    }


def build_final_results(artifacts_root: PathLike) -> Dict[str, Any]:
    """Every reported number for one campaign, derived from its artifacts."""
    root = Path(artifacts_root)
    if not root.exists():
        raise FileNotFoundError("artifacts root does not exist: {0}".format(root))
    runs = _run_rows(root)
    if not runs:
        raise FileNotFoundError(
            "no scored run under {0}; run the evaluation stage before building "
            "the final results".format(root)
        )

    # Per scenario/variant first, then across them: three seeds of one scenario
    # must not outweigh a scenario that has fewer.
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in runs:
        groups.setdefault((row["scenario_id"], row["variant"]), []).append(row)

    per_scenario: List[Dict[str, Any]] = []
    for (scenario_id, variant), rows in sorted(groups.items()):
        first = rows[0]
        merged = {
            "scenario_id": scenario_id,
            "variant": variant,
            "n_runs": len(rows),
            "expect_collision": first["expect_collision"],
            "incident_reconstructed": all(r["incident_reconstructed"] for r in rows),
            "contributors_ground_truth": first["contributors_ground_truth"],
            # The inferred set is the one the runs agree on; a disagreement
            # across seeds is itself reported rather than averaged away.
            "contributors_inferred": _consensus(
                [r["contributors_inferred"] for r in rows]
            ),
            "contributors_disagree_across_seeds": len(
                {tuple(sorted(r["contributors_inferred"])) for r in rows}
            ) > 1,
            "attribution_source": first["attribution_source"],
            "attribution_class": _consensus_scalar(
                [r["attribution_class"] for r in rows]
            ),
            "exact_set_match": all(r["exact_set_match"] for r in rows),
        }
        for field in (
            "attribution_precision", "attribution_recall", "attribution_f1",
            "collision_time_error_s", "collision_location_error_m",
            "collision_pair_recall", "cross_view_rmse_m",
            "causal_path_precision", "causal_path_recall", "causal_path_f1",
            "ancestry_recall", "node_f1_best_local", "node_f1_fused",
            "edge_f1_best_local", "edge_f1_fused", "edge_recall_fused",
            "edge_recall_ceiling", "clock_offset_mae_s", "clock_drift_mae_ppm",
            "clock_alignment_residual_s",
        ):
            merged[field] = _round(_mean([r[field] for r in rows]))
        merged["n_spurious_collisions"] = sum(
            int(r["n_spurious_collisions"] or 0) for r in rows
        )
        merged["false_attribution"] = any(bool(r["false_attribution"]) for r in rows)
        merged["verdict"] = _verdict(merged)
        per_scenario.append(merged)

    collisions = [s for s in per_scenario if s["expect_collision"]]
    controls = [s for s in per_scenario if not s["expect_collision"]]

    headline = {
        "n_runs": len(runs),
        "n_scenario_variants": len(per_scenario),
        "n_collision_variants": len(collisions),
        "n_negative_controls": len(controls),
        "attribution": {
            "note": (
                "means are over the scenario variants designed to collide; a "
                "negative control has nothing to attribute and its vacuous 1.0 "
                "would flatter the mean"
            ),
            "precision": _round(_mean([s["attribution_precision"] for s in collisions])),
            "recall": _round(_mean([s["attribution_recall"] for s in collisions])),
            "f1": _round(_mean([s["attribution_f1"] for s in collisions])),
            "exact_set_accuracy": _round(
                _mean([1.0 if s["exact_set_match"] else 0.0 for s in collisions])
            ),
            "n_correct": sum(1 for s in collisions if s["verdict"] == "correct"),
            "n_partial": sum(1 for s in collisions if s["verdict"] == "partial"),
            "n_incorrect": sum(1 for s in collisions if s["verdict"] == "incorrect"),
            "n_insufficient_evidence": sum(
                1 for s in collisions if s["verdict"] == "insufficient evidence"
            ),
        },
        "restraint": {
            "note": (
                "a scenario designed not to collide has no contributor; naming "
                "one is a false attribution and is counted, never averaged"
            ),
            "n_controls": len(controls),
            "n_false_attributions": sum(1 for s in controls if s["verdict"] ==
                                        "false attribution"),
            "n_restrained": sum(1 for s in controls if s["verdict"] == "restrained"),
        },
        "reconstruction": {
            "n_incidents_reconstructed": sum(
                1 for s in per_scenario if s["incident_reconstructed"]
            ),
            "collision_time_error_s": _round(
                _mean([s["collision_time_error_s"] for s in per_scenario])
            ),
            "collision_location_error_m": _round(
                _mean([s["collision_location_error_m"] for s in per_scenario])
            ),
            "collision_pair_recall": _round(
                _mean([s["collision_pair_recall"] for s in per_scenario])
            ),
            "cross_view_rmse_m": _round(
                _mean([s["cross_view_rmse_m"] for s in per_scenario])
            ),
            "n_spurious_collisions": sum(
                int(s["n_spurious_collisions"] or 0) for s in per_scenario
            ),
        },
        "causal_paths": {
            "precision": _round(_mean([s["causal_path_precision"] for s in per_scenario])),
            "recall": _round(_mean([s["causal_path_recall"] for s in per_scenario])),
            "f1": _round(_mean([s["causal_path_f1"] for s in per_scenario])),
            "ancestry_recall": _round(
                _mean([s["ancestry_recall"] for s in per_scenario])
            ),
        },
        "clock": {
            "offset_mae_s": _round(
                _mean([s["clock_offset_mae_s"] for s in per_scenario]), 6
            ),
            "drift_mae_ppm": _round(
                _mean([s["clock_drift_mae_ppm"] for s in per_scenario]), 3
            ),
            "alignment_residual_s": _round(
                _mean([s["clock_alignment_residual_s"] for s in per_scenario]), 6
            ),
            "note": (
                "error of the estimated transform against the recorder's true "
                "clock profile; the residual is what the fit itself reported, "
                "without reference to the truth"
            ),
        },
    }

    return {
        "artifacts_root": root.as_posix(),
        "campaign": _campaign_identity(root),
        "headline": headline,
        "method_ablation": _ablation_summary(runs),
        "model_checking": _model_check_summary(runs),
        "per_scenario": per_scenario,
        "runs": runs,
        "note": (
            "generated by cdf.evaluation.final_results from the artifacts under "
            "artifacts_root; every figure is read from a file the campaign wrote"
        ),
    }


def _consensus(values: Sequence[Sequence[str]]) -> List[str]:
    """The set every run agreed on, or the union when they disagreed.

    Reporting the union on disagreement is the conservative choice for a table
    that also carries a disagreement flag: it never hides a name a run produced.
    """
    sets = [frozenset(v) for v in values]
    if not sets:
        return []
    if len(set(sets)) == 1:
        return sorted(sets[0])
    union: set = set()
    for item in sets:
        union |= item
    return sorted(union)


def _consensus_scalar(values: Sequence[Optional[str]]) -> Optional[str]:
    present = [v for v in values if v]
    if not present:
        return None
    if len(set(present)) == 1:
        return present[0]
    return "mixed: " + ", ".join(sorted(set(present)))


def _campaign_identity(root: Path) -> Dict[str, Any]:
    path = root / "campaign.json"
    return read_json(path) if path.exists() else {}


def _ablation_summary(runs: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """The three-arm comparison, averaged over every run that carries one."""
    scored = [r for r in runs if r.get("ablation")]
    if not scored:
        return {
            "n_runs": 0,
            "note": (
                "no run carries a method ablation; produce them with "
                "scripts/reprocess_runs.py --stages ablate"
            ),
        }
    out: Dict[str, Any] = {"n_runs": len(scored)}
    for arm in ("best_local", "simple_fusion", "fusion_global_reasoning"):
        block: Dict[str, Any] = {}
        for vocabulary in ("strict", "canonical"):
            for measure in ("nodes", "edges"):
                for metric in ("precision", "recall", "f1"):
                    key = "{0}.{1}.{2}.{3}".format(arm, vocabulary, measure, metric)
                    block["{0}_{1}_{2}".format(vocabulary, measure, metric)] = _round(
                        _mean([r["ablation"].get(key) for r in scored])
                    )
        out[arm] = block

    ceilings = [r["edge_recall_ceiling"] for r in scored]
    achieved = [r["ablation"].get("fusion_global_reasoning.strict.edges.recall")
                for r in scored]
    at_ceiling = sum(
        1 for c, a in zip(ceilings, achieved)
        if c is not None and a is not None and abs(float(a) - float(c)) < 1e-6
    )
    out["strict_edge_recall_ceiling"] = _round(_mean(ceilings))
    out["n_runs_at_ceiling"] = at_ceiling
    out["note"] = (
        "each arm is the same recording re-fused under one changed key, scored "
        "against the same reference. A large part of that reference is "
        "unmatchable strictly -- its edges leave scripted-action nodes no "
        "reconstruction can emit -- so the ceiling is reported beside the score"
    )
    return out


def _model_check_summary(runs: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    scored = [r["model_check"] for r in runs if r.get("model_check")]
    return {
        "n_runs": len(scored),
        "n_pass": sum(int(m.get("n_pass") or 0) for m in scored),
        "n_fail": sum(int(m.get("n_fail") or 0) for m in scored),
        "n_unknown": sum(int(m.get("n_unknown") or 0) for m in scored),
        "n_properties": sum(int(m.get("n_properties") or 0) for m in scored),
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "--"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return "{0:.{1}f}".format(value, digits)
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value) or "none"
    return str(value)


def render_markdown(results: Mapping[str, Any]) -> str:
    """The two tables the write-up quotes, plus the campaign's headline."""
    headline = results["headline"]
    campaign = results.get("campaign") or {}
    lines: List[str] = []
    lines.append("# Final results")
    lines.append("")
    lines.append(
        "Generated by `cdf.evaluation.final_results` from `{0}`. Every figure "
        "below is read from an artifact the campaign wrote; none is "
        "transcribed.".format(results["artifacts_root"])
    )
    lines.append("")
    if campaign:
        lines.append(
            "Campaign `{0}`, clock protocol `{1}`.".format(
                campaign.get("campaign_id", "?"),
                campaign.get("clock_protocol", "?"),
            )
        )
        lines.append("")
    lines.append(
        "{0} runs over {1} scenario/variant combinations "
        "({2} designed to collide, {3} negative controls).".format(
            headline["n_runs"], headline["n_scenario_variants"],
            headline["n_collision_variants"], headline["n_negative_controls"],
        )
    )
    lines.append("")

    # -- per scenario --------------------------------------------------
    lines.append("## Per scenario")
    lines.append("")
    lines.append(
        "| Scenario | Incident reconstructed | Causal contributors GT | "
        "Causal contributors inferred | Attribution class | P | R | F1 | Verdict |"
    )
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for row in results["per_scenario"]:
        lines.append(
            "| {0} / {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} |".format(
                row["scenario_id"], row["variant"],
                _fmt(row["incident_reconstructed"]),
                _fmt(row["contributors_ground_truth"]),
                _fmt(row["contributors_inferred"]),
                _fmt(row["attribution_class"]),
                _fmt(row["attribution_precision"]),
                _fmt(row["attribution_recall"]),
                _fmt(row["attribution_f1"]),
                row["verdict"],
            )
        )
    lines.append("")
    lines.append(
        "A negative control has no designed contributor. Its precision, recall "
        "and F1 are vacuously 1.0 and are excluded from the means below; what "
        "is measured for it is whether the system named anybody, reported as "
        "`restrained` or `false attribution`."
    )
    lines.append("")

    # -- method ablation -----------------------------------------------
    ablation = results.get("method_ablation") or {}
    lines.append("## What each layer of the method was worth")
    lines.append("")
    if not ablation.get("n_runs"):
        lines.append("_{0}_".format(ablation.get("note", "no ablation available")))
    else:
        lines.append(
            "| Method | Node F1 | Edge F1 | Edge recall | Canonical edge recall | "
            "Causal Path F1 | Attribution F1 |"
        )
        lines.append("|---|---|---|---|---|---|---|")
        labels = (
            ("best_local", "Best Local"),
            ("simple_fusion", "Simple Fusion"),
            ("fusion_global_reasoning", "Fusion + Global Causal Reasoning"),
        )
        paths = results["headline"]["causal_paths"]
        attribution = results["headline"]["attribution"]
        for key, label in labels:
            arm = ablation.get(key) or {}
            # Causal-path and attribution F1 are properties of the full
            # reconstruction; they are quoted only on the row that produced
            # them rather than invented for the two ablated arms.
            is_full = key == "fusion_global_reasoning"
            lines.append(
                "| {0} | {1} | {2} | {3} | {4} | {5} | {6} |".format(
                    label,
                    _fmt(arm.get("strict_nodes_f1")),
                    _fmt(arm.get("strict_edges_f1")),
                    _fmt(arm.get("strict_edges_recall")),
                    _fmt(arm.get("canonical_edges_recall")),
                    _fmt(paths["f1"]) if is_full else "n/a",
                    _fmt(attribution["f1"]) if is_full else "n/a",
                )
            )
        lines.append("")
        lines.append(
            "Averaged over {0} runs. Strict edge recall has a ceiling of "
            "**{1}** on this campaign: that fraction of the reference's edges "
            "leave a scripted-action node, which is a privileged event type no "
            "reconstruction can emit. {2} of {0} runs reach their own ceiling "
            "exactly.".format(
                ablation["n_runs"],
                _fmt(ablation.get("strict_edge_recall_ceiling")),
                ablation.get("n_runs_at_ceiling"),
            )
        )
        lines.append("")
        lines.append(
            "Causal-path F1 and attribution F1 describe the complete "
            "reconstruction and are not defined for the two ablated arms, which "
            "produce a graph but no chains or named contributors; they are "
            "marked `n/a` rather than filled with a number that would not mean "
            "the same thing."
        )
    lines.append("")

    # -- headline figures ----------------------------------------------
    lines.append("## Headline figures")
    lines.append("")
    recon = headline["reconstruction"]
    attribution = headline["attribution"]
    restraint = headline["restraint"]
    paths = headline["causal_paths"]
    rows = [
        ("incidents reconstructed",
         "{0} of {1} scenario variants".format(
             recon["n_incidents_reconstructed"], headline["n_scenario_variants"])),
        ("collision time error", _fmt(recon["collision_time_error_s"], 4) + " s"),
        ("collision location error", _fmt(recon["collision_location_error_m"], 4) + " m"),
        ("collision pair recall", _fmt(recon["collision_pair_recall"])),
        ("spurious collisions", str(recon["n_spurious_collisions"])),
        ("cross-view trajectory RMSE", _fmt(recon["cross_view_rmse_m"]) + " m"),
        ("clock offset MAE", _fmt(headline["clock"]["offset_mae_s"], 5) + " s"),
        ("clock drift error", _fmt(headline["clock"]["drift_mae_ppm"], 2) + " ppm"),
        ("clock fit residual (self-reported)",
         _fmt(headline["clock"]["alignment_residual_s"], 4) + " s"),
        ("causal path P / R / F1", "{0} / {1} / {2}".format(
            _fmt(paths["precision"]), _fmt(paths["recall"]), _fmt(paths["f1"]))),
        ("causal ancestry recall", _fmt(paths["ancestry_recall"])),
        ("attribution P / R / F1", "{0} / {1} / {2}".format(
            _fmt(attribution["precision"]), _fmt(attribution["recall"]),
            _fmt(attribution["f1"]))),
        ("exact contributor-set accuracy", _fmt(attribution["exact_set_accuracy"])),
        ("scenarios correct / partial / insufficient",
         "{0} / {1} / {2}".format(
             attribution["n_correct"], attribution["n_partial"],
             attribution["n_insufficient_evidence"])),
        ("false attributions on negative controls",
         "{0} of {1}".format(restraint["n_false_attributions"],
                             restraint["n_controls"])),
    ]
    checks = results.get("model_checking") or {}
    if checks.get("n_runs"):
        rows.append(
            ("model checking PASS / FAIL / UNKNOWN",
             "{0} / {1} / {2}".format(checks["n_pass"], checks["n_fail"],
                                      checks["n_unknown"]))
        )
    lines.append("| Measure | Value |")
    lines.append("|---|---|")
    for label, value in rows:
        lines.append("| {0} | {1} |".format(label, value))
    lines.append("")
    lines.append(
        "*A contribution score states what changed when the encounter was "
        "re-run under a controlled modification. It is not a finding of legal "
        "fault and not a fault percentage.*"
    )
    lines.append("")
    return "\n".join(lines)


def write_final_results(artifacts_root: PathLike) -> Dict[str, Path]:
    """Build the results and write the three files; returns their paths."""
    results = build_final_results(artifacts_root)
    out_dir = summary_dir(artifacts_root)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "final_results.json"
    csv_path = out_dir / "final_results.csv"
    md_path = out_dir / "final_results.md"

    write_json(json_path, results)
    write_csv(
        csv_path,
        [
            {
                column: (
                    ";".join(row[column]) if isinstance(row.get(column), list)
                    else row.get(column)
                )
                for column in FINAL_COLUMNS
            }
            for row in results["per_scenario"]
        ],
        FINAL_COLUMNS,
    )
    md_path.write_text(render_markdown(results), encoding="utf-8")

    LOGGER.info(
        "final results: %d runs over %d scenario variants -> %s",
        results["headline"]["n_runs"],
        results["headline"]["n_scenario_variants"],
        out_dir,
    )
    return {"json": json_path, "csv": csv_path, "markdown": md_path}
