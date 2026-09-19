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

The recorded artifacts are far too large to commit, so the same three files are
also published to ``results/`` in the repository, which *is* committed. That is
the only reason the documentation can link to a results table at all: without it
every reference would point into a directory a fresh clone does not have, and
the claim that the numbers are checkable would be untrue.

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

from ..common.config import repo_root
from ..common.io import read_json, write_csv, write_json
from ..common.layout import RunLayout
from .suite import RUN_KIND_PRIMARY, _run_dirs, summary_dir
from .v2_results import v2_blocks

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
        clock_path = layout.evaluation_dir / "clock_ablation.json"
        clock_ablation = read_json(clock_path) if clock_path.exists() else None
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
                "clock_ablation": _clock_ablation_row(clock_ablation),
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


#: The three clock protocols, in the order they are reported.
CLOCK_ARMS: Tuple[str, ...] = (
    "A_synchronized",
    "B_independent_uncorrected",
    "C_independent_aligned",
)


def _clock_ablation_row(report: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """One run's A/B/C clock comparison, flattened.

    Arm A is a control rather than a separate physics run: the *same* recording
    is restamped onto the simulator clock using the true profiles. That keeps the
    comparison about time alone -- three arms over one set of physical events --
    instead of confounding the clock protocol with a different run.
    """
    if not report:
        return {}
    out: Dict[str, Any] = {}
    for arm in CLOCK_ARMS:
        block = (report.get("modes") or {}).get(arm) or {}
        graphs = block.get("graphs") or {}
        fused = graphs.get("fused") or {}
        out[arm] = {
            "offset_error_s": _get(block, "clock", "mean_abs_offset_error_s"),
            "drift_error_ppm": _get(block, "clock", "mean_abs_drift_error_ppm"),
            "node_f1": fused.get("node_f1"),
            "edge_f1": fused.get("edge_f1"),
            "edge_recall": fused.get("edge_recall"),
            "association_f1": _get(block, "association", "f1"),
            "n_merged_groups": block.get("n_merged_groups"),
        }
    return out


def _clock_ablation_summary(runs: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """The A/B/C comparison averaged over every run that carries one."""
    scored = [r for r in runs if r.get("clock_ablation")]
    if not scored:
        return {
            "n_runs": 0,
            "note": (
                "no run carries a clock ablation; produce them with "
                "scripts/reprocess_runs.py --stages clocks"
            ),
        }
    out: Dict[str, Any] = {"n_runs": len(scored)}
    for arm in CLOCK_ARMS:
        block: Dict[str, Any] = {}
        for metric in ("offset_error_s", "drift_error_ppm", "node_f1", "edge_f1",
                       "edge_recall", "association_f1"):
            block[metric] = _round(
                _mean([
                    (r["clock_ablation"].get(arm) or {}).get(metric) for r in scored
                ]),
                6 if metric.endswith("_s") else 4,
            )
        out[arm] = block
    out["note"] = (
        "one physical recording per run, scored three ways. A restamps the "
        "recorders onto the simulator clock using the true profiles and is a "
        "control, not a separate run; B takes each recorder's own timestamps at "
        "face value; C uses the alignment estimated from shared observations "
        "alone, which is the protocol the campaign reports"
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
            "n_scenarios_with_seed_disagreement": sum(
                1 for s in collisions if s["contributors_disagree_across_seeds"]
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
        # The V2 blocks: how each recorder was placed on common time and how far
        # out it was, what the cameras made of real signs, whether the property
        # verdicts matched the observable truth, who was named as a contributor
        # physically and normatively, whether multi-impact orders were recovered,
        # and what the replays established. Kept as their own blocks rather than
        # folded into the headline, because they are scored against different
        # references and a single aggregate would hide which.
        "v2": v2_blocks(root),
        "method_ablation": _ablation_summary(runs),
        "clock_ablation": _clock_ablation_summary(runs),
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
    """What campaign these artifacts are, and under which clock protocol.

    ``campaign.json`` is written by the V1 driver. A V2 root may not have one,
    and the identity is then read from the runs themselves -- which is the more
    reliable source anyway, since it is what each recording actually stamped.
    A root holding more than one protocol reports them all rather than picking
    one, because that is a root whose averages mean nothing.
    """
    path = root / "campaign.json"
    if path.exists():
        return read_json(path)
    protocols, ids = set(), set()
    for manifest in sorted(root.glob("*/*/manifest.json")):
        try:
            record = read_json(manifest)
        except Exception:  # pragma: no cover - a corrupt manifest is not identity
            continue
        protocols.add(str(record.get("clock_protocol") or "unrecorded"))
        if record.get("config_hash"):
            ids.add(str(record["config_hash"]))
    if not protocols:
        return {}
    return {
        "campaign": root.name,
        "clock_protocol": (
            sorted(protocols)[0] if len(protocols) == 1
            else "MIXED: " + ", ".join(sorted(protocols))
        ),
        "n_distinct_config_hashes": len(ids),
        "source": "read from the runs; this root carries no campaign.json",
    }


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
                campaign.get("campaign_id", campaign.get("campaign", "?")),
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
    lines.append("## Attribution against the scenario design")
    lines.append("")
    lines.append(
        "Scored against each scenario's declared causal template, which says what "
        "the experiment intended. That is a different question from the one the "
        "responsibility layer answers, and the two can disagree. On "
        "`S10/rolls_through` this table reads *incorrect* while the "
        "responsibility analysis reports A as supported, because a template names "
        "physical causes and the responsibility layer names normative "
        "contributors. The reconstruction itself is scored against the observable "
        "ground truth, in the sections below."
    )
    lines.append("")
    lines.append(
        "| Scenario | Incident reconstructed | Design-template contributors | "
        "Inferred | Attribution class | P | R | F1 | Verdict |"
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
    lines.append("## What each layer of the method was worth (design reference)")
    lines.append("")
    lines.append(
        "Structural figures here are scored against the scenario design "
        "reference, not against the observable ground truth. They are kept "
        "because a three-arm comparison is only meaningful against one fixed "
        "reference, and they should be read as a comparison between arms rather "
        "than as the V2 reconstruction result."
    )
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

    # -- clock ablation ------------------------------------------------
    clocks = results.get("clock_ablation") or {}
    lines.append("## What the clock alignment is worth")
    lines.append("")
    if not clocks.get("n_runs"):
        lines.append("_{0}_".format(clocks.get("note", "no clock ablation available")))
    else:
        lines.append(
            "| Clock protocol | Offset error [s] | Node F1 | Edge F1 | "
            "Edge recall | Association F1 |"
        )
        lines.append("|---|---|---|---|---|---|")
        labels = (
            ("A_synchronized", "A - synchronized (control)"),
            ("B_independent_uncorrected", "B - independent, uncorrected"),
            ("C_independent_aligned", "C - independent, estimated alignment"),
        )
        for key, label in labels:
            arm = clocks.get(key) or {}
            lines.append(
                "| {0} | {1} | {2} | {3} | {4} | {5} |".format(
                    label,
                    _fmt(arm.get("offset_error_s"), 5),
                    _fmt(arm.get("node_f1")),
                    _fmt(arm.get("edge_f1")),
                    _fmt(arm.get("edge_recall")),
                    _fmt(arm.get("association_f1")),
                )
            )
        lines.append("")
        lines.append("Averaged over {0} runs.".format(clocks["n_runs"]))
        lines.append("")
        lines.append(clocks.get("note", "").capitalize() + ".")
    lines.append("")

    # -- the V2 blocks ---------------------------------------------------
    _v2_markdown(lines, results.get("v2") or {})

    # -- headline figures ----------------------------------------------
    lines.append("## Headline figures (design reference, scenario-aggregated)")
    lines.append("")
    lines.append(
        "Aggregated per scenario variant and scored against the scenario design. "
        "The participant-weighted clock figures, the perception counts and the "
        "property verdicts are in their own sections above. The two clock "
        "averages differ because they average different populations, not because "
        "they disagree."
    )
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
        ("scenario-aggregated clock offset MAE",
         _fmt(headline["clock"]["offset_mae_s"], 5) + " s"),
        # Not an estimation error: the aligner pins scale to 1 on purpose, so
        # this figure is the true relative drift that choice leaves unmodelled.
        ("clock drift",
         "not estimated; scale pinned to 1 "
         "(unmodelled true drift {0} ppm)".format(
             _fmt(headline["clock"]["drift_mae_ppm"], 2))),
        ("clock fit residual (self-reported)",
         _fmt(headline["clock"]["alignment_residual_s"], 4) + " s"),
        ("causal path P / R / F1", "{0} / {1} / {2}".format(
            _fmt(paths["precision"]), _fmt(paths["recall"]), _fmt(paths["f1"]))),
        ("causal ancestry recall", _fmt(paths["ancestry_recall"])),
        ("design-template attribution P / R / F1", "{0} / {1} / {2}".format(
            _fmt(attribution["precision"]), _fmt(attribution["recall"]),
            _fmt(attribution["f1"]))),
        ("exact contributor-set accuracy", _fmt(attribution["exact_set_accuracy"])),
        ("scenarios correct / partial / incorrect / insufficient",
         "{0} / {1} / {2} / {3}".format(
             attribution["n_correct"], attribution["n_partial"],
             attribution["n_incorrect"],
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
    if checks.get("n_runs"):
        lines.append(
            "A model-checking FAIL is an observation about the recorded trace, "
            "not a defect in the checker: these are crash scenarios, and a "
            "vehicle that entered a conflict without responding, or applied "
            "throttle within three seconds of an impact, genuinely violated the "
            "property. UNKNOWN is a first-class verdict -- a finite trace that "
            "never exhibits a property's premise can neither satisfy nor violate "
            "it -- and is never folded into a pass rate."
        )
        lines.append("")
    lines.append(
        "*A contribution score states what changed when the encounter was "
        "re-run under a controlled modification. It is not a finding of legal "
        "fault and not a fault percentage.*"
    )
    lines.append("")
    return "\n".join(lines)


def write_final_results(
    artifacts_root: PathLike, publish_dir: Optional[PathLike] = "results"
) -> Dict[str, Path]:
    """Build the results, write the three files, and publish a committed copy.

    ``publish_dir`` is where the committed copy goes -- ``results/`` by default,
    relative to the repository root. Pass ``None`` to skip it, which is right
    for a scratch campaign nobody is going to quote.
    """
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

    paths = {"json": json_path, "csv": csv_path, "markdown": md_path}

    if publish_dir is not None:
        published = Path(publish_dir)
        if not published.is_absolute():
            published = repo_root() / published
        published.mkdir(parents=True, exist_ok=True)
        for kind, source in list(paths.items()):
            target = published / source.name
            target.write_bytes(source.read_bytes())
            paths["published_" + kind] = target
        # A committed copy that does not say which campaign it came from is a
        # table with no provenance, so the stamp travels with it.
        (published / "README.md").write_text(
            "# Generated results\n\n"
            "These files are written by `cdf.evaluation.final_results` from the\n"
            "artifacts of a recorded campaign. They are committed because the\n"
            "artifacts themselves are not: without them the documentation would\n"
            "link to tables a fresh clone does not have.\n\n"
            "Do not edit them by hand. Regenerate with:\n\n"
            "```bash\n"
            "python -c \"import sys; sys.path.insert(0,'src'); \\\n"
            "           from cdf.evaluation.final_results import write_final_results; \\\n"
            "           write_final_results('{0}')\"\n"
            "```\n\n"
            "Campaign: `{1}`, clock protocol `{2}`, {3} runs over {4} "
            "scenario/variant combinations.\n".format(
                results["artifacts_root"],
                (results.get("campaign") or {}).get(
                    "campaign_id",
                    (results.get("campaign") or {}).get("campaign", "?"),
                ),
                (results.get("campaign") or {}).get("clock_protocol", "?"),
                results["headline"]["n_runs"],
                results["headline"]["n_scenario_variants"],
            ),
            encoding="utf-8",
        )

    LOGGER.info(
        "final results: %d runs over %d scenario variants -> %s%s",
        results["headline"]["n_runs"],
        results["headline"]["n_scenario_variants"],
        out_dir,
        " (published to {0})".format(publish_dir) if publish_dir else "",
    )
    return paths



def _pct(value):
    return "--" if value is None else "{0:.1%}".format(value)


def _secs(value):
    return "--" if value is None else "{0:.6f} s".format(value)


def _sentence(text):
    """Capitalise a note written to be embedded, so it reads as a sentence."""
    text = (text or "").strip()
    return text[:1].upper() + text[1:] if text else text


def _tally(mapping):
    items = (mapping or {}).items()
    return ", ".join("{0} x{1}".format(k, v) for k, v in items) or "none"


def _prf_row(label, block):
    """One perception row. A quantity with no reference says so."""
    if block.get("reference") == "unavailable":
        return "| {0} | {1} detections | no reference | -- | -- | -- |".format(
            label, block.get("n_detected", 0)
        )
    return "| {0} | {1} | {2} | {3} | {4} | {5} |".format(
        label,
        block.get("n_true_positive", 0),
        block.get("n_false_positive", 0),
        block.get("n_false_negative", 0),
        _pct(block.get("precision")),
        _pct(block.get("recall")),
    )


def _v2_markdown(lines, v2):
    """The V2 blocks. Each is scored against its own reference and kept apart,
    because folding them into one headline would hide which reference a number
    came from."""
    if not v2:
        return

    clock = v2.get("clock") or {}
    by_source = clock.get("offset_error_by_source") or {}
    lines.append("## Clocks (participant-weighted)")
    lines.append("")
    lines.append(
        "How each recorder reached common time. A vehicle placed by a fitted "
        "trajectory is not making the same claim as one tied in by a physical "
        "impact, so the source is reported per participant rather than averaged "
        "away. Error is relative to each run's reference recorder: a common "
        "timeline is only fixed up to a constant."
    )
    lines.append("")
    lines.append(
        "Participant-weighted: every recorder counts once, so a three-vehicle run "
        "contributes three rows and a two-vehicle run two. *Recorders* is how "
        "many were placed by that source; *scored* is how many the error could be "
        "measured on, since an unresolved recorder has no offset to score. The "
        "headline table averages per scenario variant instead, which is why the "
        "two figures differ."
    )
    lines.append("")
    lines.append("| Source | Recorders | Scored | Offset MAE | Worst |")
    lines.append("|---|---|---|---|---|")
    for source, count in (clock.get("source_distribution") or {}).items():
        stats = by_source.get(source) or {}
        lines.append("| `{0}` | {1} | {2} | {3} | {4} |".format(
            source, count, stats.get("n", 0),
            _secs(stats.get("mae_s")), _secs(stats.get("max_abs_s"))))
    overall = clock.get("offset_error") or {}
    lines.append("| **all** | {0} | {1} | {2} | {3} |".format(
        clock.get("n_participants", 0), overall.get("n", 0),
        _secs(overall.get("mae_s")), _secs(overall.get("max_abs_s"))))
    lines.append("")
    lines.append("Run status: {0}. Unresolved recorders: {1} of {2}.".format(
        _tally(clock.get("run_status_distribution")),
        clock.get("n_unresolved", 0), clock.get("n_participants", 0)))
    lines.append("")

    perception = v2.get("perception") or {}
    lines.append("## Perception, from real campaign frames")
    lines.append("")
    lines.append(
        "A row reading *no reference* has nothing to score against. Its "
        "detections are counted, because how many there were is a fact, but "
        "whether they were right is not established; printing a precision of "
        "zero there would turn a missing reference into a measured failure. The "
        "reason is given under the table."
    )
    lines.append("")
    lines.append("| What | TP | FP | FN | Precision | Recall |")
    lines.append("|---|---|---|---|---|---|")
    unscored = []
    for key, label in (("stop_signs", "STOP signs"),
                       ("yield_signs", "Give-way signs"),
                       ("stop_lines", "Stop lines"),
                       ("lane_markings", "Lane markings")):
        block = perception.get(key) or {}
        lines.append(_prf_row(label, block))
        if block.get("reference") == "unavailable" and block.get("note"):
            unscored.append((label, block["note"]))
    lines.append("")
    for label, note in unscored:
        lines.append("*{0}, not scored.* {1}.".format(label, _sentence(note)))
        lines.append("")
    lines.append("A rate over no instances is `--`, never zero. {0}.".format(
        _sentence(perception.get("latency_note", "").rstrip("."))))
    lines.append("")

    formal = v2.get("formal") or {}
    lines.append("## Temporal properties")
    lines.append("")
    if not formal.get("scored"):
        lines.append("_{0}_".format(formal.get("reason", "not scored")))
    else:
        lines.append(
            "The same formulae run over the merged reconstruction and over the "
            "observable ground truth, so a disagreement is about the "
            "reconstruction rather than about two readings of the same word. "
            "UNKNOWN is never folded into PASS."
        )
        lines.append("")
        lines.append(
            "| Comparable | Agree | Agreement | False violations | Missed violations |")
        lines.append("|---|---|---|---|---|")
        lines.append("| {0} | {1} | {2} | {3} ({4}) | {5} ({6}) |".format(
            formal.get("n_comparable", 0), formal.get("n_agree", 0),
            _pct(formal.get("agreement")),
            formal.get("n_false_violations", 0),
            _pct(formal.get("false_violation_rate")),
            formal.get("n_missed_violations", 0),
            _pct(formal.get("missed_violation_rate"))))
        for label, key in (("False violations", "false_violations_by_property"),
                           ("Missed violations", "missed_violations_by_property"),
                           ("Undecided", "undecided_by_property")):
            broken = formal.get(key) or {}
            if broken:
                lines.append("")
                lines.append("{0} by property: {1}.".format(label, _tally(broken)))
    lines.append("")

    responsibility = v2.get("responsibility") or {}
    sets = responsibility.get("sets") or {}
    lines.append("## Contribution: physical and normative")
    lines.append("")
    lines.append(
        "Two different claims, scored apart. A vehicle that brakes hard is a "
        "physical cause of the crash behind it and has broken no rule. A scenario "
        "designing no rule violation has nothing for the normative comparison to "
        "score, and reports not applicable rather than zero."
    )
    lines.append("")
    if sets.get("scored"):
        physical = sets.get("physical_contributor_sets") or {}
        normative = sets.get("normative_contributor_sets")
        lines.append("| Comparison | Runs | Precision | Recall | F1 | Exact set match |")
        lines.append("|---|---|---|---|---|---|")
        lines.append("| Physical | {0} | {1} | {2} | {3} | {4} |".format(
            sets.get("n_runs", 0), _pct(physical.get("precision")),
            _pct(physical.get("recall")), _pct(physical.get("f1")),
            _pct(sets.get("exact_physical_match_rate"))))
        if normative:
            lines.append("| Normative | {0} | {1} | {2} | {3} | -- |".format(
                sets.get("n_runs_with_a_normative_reference", 0),
                _pct(normative.get("precision")), _pct(normative.get("recall")),
                _pct(normative.get("f1"))))
        else:
            lines.append("| Normative | 0 | -- | -- | -- | -- |")
        lines.append("")
        lines.append("Runs carrying a normative reference: {0} of {1}.".format(
            sets.get("n_runs_with_a_normative_reference", 0), sets.get("n_runs", 0)))
        for case in sets.get("hard_cases") or []:
            lines.append("")
            lines.append("- **{0}/{1}**: {2}".format(
                case.get("scenario"), case.get("variant"), case.get("why_it_is_hard")))
    else:
        lines.append("_{0}_".format(sets.get("reason", "not scored")))
    classes = responsibility.get("evidence_classes") or {}
    if classes:
        lines.append("")
        lines.append("Evidence classes over all findings: {0}.".format(_tally(classes)))
    lines.append("")

    order = v2.get("collision_order") or {}
    lines.append("## Collision order")
    lines.append("")
    lines.append("Verdicts: {0}.".format(_tally(order.get("verdicts"))))
    if order.get("n_multi_impact_runs"):
        lines.append("")
        lines.append("Multi-impact runs: {0}, correct on {1}.".format(
            order["n_multi_impact_runs"], _pct(order.get("correct_rate"))))
        lines.append("")
        lines.append("| Scenario | Variant | Seed | Verdict |")
        lines.append("|---|---|---|---|")
        for row in order.get("multi_impact_runs") or []:
            lines.append("| {0} | {1} | {2} | {3} |".format(
                row.get("scenario"), row.get("variant"),
                row.get("seed"), row.get("verdict")))
    lines.append("")
    lines.append(
        "`not established` is its own verdict, not a failure: impacts closer "
        "together than the recording can resolve, or an offset resting on a "
        "shared anchor, leave an order the method did not claim."
    )
    lines.append("")

    counterfactual = v2.get("counterfactual") or {}
    lines.append("## Counterfactuals")
    lines.append("")
    lines.append("But-for verdicts: {0}.".format(
        _tally(counterfactual.get("but_for_verdicts"))))
    roles = counterfactual.get("counterfactual_roles") or {}
    if roles:
        lines.append("")
        lines.append("Roles: {0}.".format(_tally(roles)))
    lines.append("")
    lines.append(
        "A prevention opportunity is not factual causation, and the role records "
        "which question each replay answered: removing what happened, supplying "
        "what did not, or improving what did."
    )
    lines.append("")
