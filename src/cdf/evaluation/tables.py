"""Flattening of metric blocks into CSV rows with a stable column order.

A results table that changes its column order between runs cannot be diffed, and
a table whose columns depend on which optional keys happened to be present cannot
be concatenated across scenarios. Both are common ways for a results directory to
quietly stop being reproducible, so every table in this project declares its
columns explicitly here and :func:`cdf.common.io.write_csv` is always called with
them.

The row builders all take a whole run's ``metrics.json`` mapping rather than the
inner block, so that every row carries the run identity (scenario, variant, seed,
run id) and the aggregate tables are a plain concatenation. A block that is
``None`` -- because its inputs were absent -- produces **no rows** rather than a
row of zeros: an empty table says "not measured", a table full of zeros says
"measured and bad", and confusing the two would misreport the experiment.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence

__all__ = [
    "RUN_COLUMNS",
    "EVENT_MATCH_COLUMNS",
    "EDGE_MATCH_COLUMNS",
    "EVENT_METRICS_COLUMNS",
    "GRAPH_METRICS_COLUMNS",
    "FUSION_METRICS_COLUMNS",
    "ASSOCIATION_METRICS_COLUMNS",
    "ATTRIBUTION_METRICS_COLUMNS",
    "MODEL_CHECK_COLUMNS",
    "SCENARIO_VALIDATION_COLUMNS",
    "run_identity",
    "run_rows",
    "event_match_rows",
    "edge_match_rows",
    "event_metrics_rows",
    "graph_metrics_rows",
    "fusion_metrics_rows",
    "association_metrics_rows",
    "attribution_metrics_rows",
    "model_check_rows",
    "scenario_validation_rows",
    "concat",
]


#: Columns identifying the run every row belongs to. Prefixed onto every table.
_IDENT_COLUMNS: List[str] = ["scenario_id", "variant", "seed", "run_id", "run_dir"]


def run_identity(metrics: Mapping[str, Any]) -> Dict[str, Any]:
    """The run-identifying prefix shared by every row of every table."""
    return {
        "scenario_id": metrics.get("scenario_id", ""),
        "variant": metrics.get("variant", ""),
        "seed": metrics.get("seed", 0),
        "run_id": metrics.get("run_id", ""),
        "run_dir": metrics.get("run_dir", ""),
    }


def _with_ident(metrics: Mapping[str, Any], row: Mapping[str, Any]) -> Dict[str, Any]:
    out = run_identity(metrics)
    out.update(row)
    return out


def _block(metrics: Mapping[str, Any], name: str) -> Optional[Mapping[str, Any]]:
    """One metric block, or ``None`` when it was not computed."""
    block = metrics.get(name)
    return block if isinstance(block, Mapping) else None


# ---------------------------------------------------------------------------
# One row per run
# ---------------------------------------------------------------------------

RUN_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "outcome",
    "scenario_validation_passed",
    "n_participants",
    "event_f1_best_local",
    "event_f1_fused",
    "event_delta_f1",
    "node_f1_best_local",
    "node_f1_fused",
    "edge_f1_best_local",
    "edge_f1_fused",
    "delta_edge_f1",
    "delta_node_f1",
    "shd_best_local",
    "shd_fused",
    "delta_shd",
    "fusion_helped",
    "n_nodes_gained",
    "n_edges_gained",
    "association_f1",
    "association_precision",
    "association_recall",
    "attribution_f1",
    "primary_initiator_correct",
    "local_unknowns_honest",
    "unavailable_blocks",
]


def run_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """The single summary row for one run."""
    events = _block(metrics, "events")
    graphs = _block(metrics, "graphs")
    benefit = _block(metrics, "fusion_benefit")
    assoc = _block(metrics, "association")
    attr = _block(metrics, "attribution")
    unknowns = _block(metrics, "local_unknowns")
    validation = _block(metrics, "scenario_validation")

    graphs_best = _sub(graphs, "best_single_local", "metrics")
    graphs_fused = _block(graphs or {}, "fused")

    row: Dict[str, Any] = {
        "outcome": metrics.get("outcome", ""),
        "scenario_validation_passed": (
            validation.get("passed") if validation is not None else None
        ),
        "n_participants": metrics.get("n_participants"),
        "event_f1_best_local": _get(events, "best_local", "f1"),
        "event_f1_fused": _get(events, "fused", "f1"),
        "event_delta_f1": events.get("delta_f1") if events else None,
        "node_f1_best_local": graphs_best.get("node_f1") if graphs_best else None,
        "node_f1_fused": graphs_fused.get("node_f1") if graphs_fused else None,
        "edge_f1_best_local": graphs_best.get("edge_f1") if graphs_best else None,
        "edge_f1_fused": graphs_fused.get("edge_f1") if graphs_fused else None,
        "delta_edge_f1": graphs.get("delta_edge_f1") if graphs else None,
        "delta_node_f1": graphs.get("delta_node_f1") if graphs else None,
        "shd_best_local": (
            graphs_best.get("structural_hamming_distance") if graphs_best else None
        ),
        "shd_fused": (
            graphs_fused.get("structural_hamming_distance") if graphs_fused else None
        ),
        "delta_shd": graphs.get("delta_shd") if graphs else None,
        "fusion_helped": benefit.get("fusion_helped") if benefit else None,
        "n_nodes_gained": benefit.get("n_nodes_gained") if benefit else None,
        "n_edges_gained": benefit.get("n_edges_gained") if benefit else None,
        "association_f1": assoc.get("f1") if assoc else None,
        "association_precision": assoc.get("precision") if assoc else None,
        "association_recall": assoc.get("recall") if assoc else None,
        "attribution_f1": attr.get("f1") if attr else None,
        "primary_initiator_correct": _get(attr, "primary_initiator", "correct"),
        "local_unknowns_honest": unknowns.get("honest") if unknowns else None,
        "unavailable_blocks": ";".join(sorted((metrics.get("reasons") or {}).keys())),
    }
    return [_with_ident(metrics, row)]


def _get(block: Optional[Mapping[str, Any]], *path: str) -> Any:
    node: Any = block
    for part in path:
        if not isinstance(node, Mapping):
            return None
        node = node.get(part)
    return node


def _sub(block: Optional[Mapping[str, Any]], *path: str) -> Optional[Mapping[str, Any]]:
    node = _get(block, *path) if block is not None else None
    return node if isinstance(node, Mapping) else None


# ---------------------------------------------------------------------------
# Per-event and per-edge match tables
# ---------------------------------------------------------------------------

EVENT_MATCH_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "scope",
    "participant_id",
    "status",
    "pred_event_id",
    "truth_event_id",
    "dt_s",
    "abs_dt_s",
]


def event_match_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per matched pair, false positive and false negative.

    False negatives are included deliberately: a table listing only what was
    found would make a reconstruction that missed most of the run look complete.
    """
    events = _block(metrics, "events")
    if events is None:
        return []
    rows: List[Dict[str, Any]] = []

    def emit(scope: str, participant_id: str, block: Mapping[str, Any]) -> None:
        for pred_id, truth_id, dt in block.get("matches", []) or []:
            rows.append(
                _with_ident(
                    metrics,
                    {
                        "scope": scope,
                        "participant_id": participant_id,
                        "status": "matched",
                        "pred_event_id": pred_id,
                        "truth_event_id": truth_id,
                        "dt_s": float(dt),
                        "abs_dt_s": abs(float(dt)),
                    },
                )
            )
        for pred_id in block.get("unmatched_pred", []) or []:
            rows.append(
                _with_ident(
                    metrics,
                    {
                        "scope": scope,
                        "participant_id": participant_id,
                        "status": "false_positive",
                        "pred_event_id": pred_id,
                        "truth_event_id": "",
                        "dt_s": None,
                        "abs_dt_s": None,
                    },
                )
            )
        for truth_id in block.get("unmatched_truth", []) or []:
            rows.append(
                _with_ident(
                    metrics,
                    {
                        "scope": scope,
                        "participant_id": participant_id,
                        "status": "false_negative",
                        "pred_event_id": "",
                        "truth_event_id": truth_id,
                        "dt_s": None,
                        "abs_dt_s": None,
                    },
                )
            )

    for pid in sorted(events.get("per_participant", {}) or {}):
        emit("local", pid, events["per_participant"][pid])
    fused = events.get("fused_detail")
    if isinstance(fused, Mapping):
        emit("fused", "", fused)
    return rows


EDGE_MATCH_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "scope",
    "participant_id",
    "status",
    "pred_source",
    "pred_target",
    "truth_source",
    "truth_target",
    "edge_type",
    "confidence",
    "rule",
]


def edge_match_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per matched, missing, extra and reversed causal edge."""
    graphs = _block(metrics, "graphs")
    if graphs is None:
        return []
    rows: List[Dict[str, Any]] = []

    def emit(scope: str, participant_id: str, block: Mapping[str, Any]) -> None:
        for status, key in (
            ("matched", "matched_edges"),
            ("missing", "missing_edges"),
            ("extra", "extra_edges"),
            ("reversed", "reversed_edges"),
        ):
            for e in block.get(key, []) or []:
                rows.append(
                    _with_ident(
                        metrics,
                        {
                            "scope": scope,
                            "participant_id": participant_id,
                            "status": status,
                            "pred_source": e.get("a_source", ""),
                            "pred_target": e.get("a_target", ""),
                            "truth_source": e.get("b_source", ""),
                            "truth_target": e.get("b_target", ""),
                            "edge_type": e.get("edge_type", ""),
                            "confidence": e.get("confidence"),
                            "rule": e.get("rule") or "",
                        },
                    )
                )

    for pid in sorted(graphs.get("per_participant", {}) or {}):
        emit("local", pid, graphs["per_participant"][pid])
    fused = graphs.get("fused")
    if isinstance(fused, Mapping):
        emit("fused", "", fused)
    return rows


# ---------------------------------------------------------------------------
# Aggregate tables
# ---------------------------------------------------------------------------

EVENT_METRICS_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "scope",
    "participant_id",
    "precision",
    "recall",
    "f1",
    "n_pred",
    "n_truth",
    "n_matched",
    "n_false_positive",
    "n_false_negative",
    "mean_abs_timing_error",
    "median_abs_timing_error",
    "max_abs_timing_error",
    "tolerance_s",
]


def event_metrics_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per participant plus one for the fused event list."""
    events = _block(metrics, "events")
    if events is None:
        return []
    rows: List[Dict[str, Any]] = []
    keys = [c for c in EVENT_METRICS_COLUMNS if c not in _IDENT_COLUMNS + ["scope", "participant_id"]]
    for pid in sorted(events.get("per_participant", {}) or {}):
        block = events["per_participant"][pid]
        row = {"scope": "local", "participant_id": pid}
        row.update({k: block.get(k) for k in keys})
        rows.append(_with_ident(metrics, row))
    fused = events.get("fused")
    if isinstance(fused, Mapping):
        row = {"scope": "fused", "participant_id": ""}
        row.update({k: fused.get(k) for k in keys})
        rows.append(_with_ident(metrics, row))
    return rows


GRAPH_METRICS_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "scope",
    "participant_id",
    "node_precision",
    "node_recall",
    "node_f1",
    "edge_precision",
    "edge_recall",
    "edge_f1",
    "structural_hamming_distance",
    "n_nodes_pred",
    "n_nodes_truth",
    "n_nodes_matched",
    "n_edges_pred",
    "n_edges_truth",
    "n_edges_matched",
    "n_missing_edges",
    "n_extra_edges",
    "n_reversed_edges",
    "tolerance_s",
]


def graph_metrics_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per local causal graph plus one for the fused graph."""
    graphs = _block(metrics, "graphs")
    if graphs is None:
        return []
    keys = [
        c
        for c in GRAPH_METRICS_COLUMNS
        if c not in _IDENT_COLUMNS + ["scope", "participant_id"]
    ]
    rows: List[Dict[str, Any]] = []
    for pid in sorted(graphs.get("per_participant", {}) or {}):
        block = graphs["per_participant"][pid]
        row: Dict[str, Any] = {"scope": "local", "participant_id": pid}
        row.update({k: block.get(k) for k in keys})
        rows.append(_with_ident(metrics, row))
    fused = graphs.get("fused")
    if isinstance(fused, Mapping):
        row = {"scope": "fused", "participant_id": ""}
        row.update({k: fused.get(k) for k in keys})
        rows.append(_with_ident(metrics, row))
    return rows


FUSION_METRICS_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "best_local_participant_id",
    "best_local_edge_f1",
    "fused_edge_f1",
    "delta_edge_f1",
    "best_local_node_f1",
    "fused_node_f1",
    "delta_node_f1",
    "best_local_shd",
    "fused_shd",
    "delta_shd",
    "fusion_helped",
    "n_nodes_gained",
    "n_edges_gained",
    "baseline_edge_recall",
    "fused_edge_recall",
    "gained_nodes",
    "gained_edges",
]


def fusion_metrics_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """The H1/H2 row: fused versus best single local, with the gain named."""
    benefit = _block(metrics, "fusion_benefit")
    if benefit is None:
        return []
    best = _block(benefit, "best_local") or {}
    fused = _block(benefit, "fused") or {}
    gain = _block(benefit, "knowledge_gain") or {}
    row = {
        "best_local_participant_id": benefit.get("best_local_participant_id"),
        "best_local_edge_f1": best.get("edge_f1"),
        "fused_edge_f1": fused.get("edge_f1"),
        "delta_edge_f1": benefit.get("delta_edge_f1"),
        "best_local_node_f1": best.get("node_f1"),
        "fused_node_f1": fused.get("node_f1"),
        "delta_node_f1": benefit.get("delta_node_f1"),
        "best_local_shd": best.get("structural_hamming_distance"),
        "fused_shd": fused.get("structural_hamming_distance"),
        "delta_shd": benefit.get("delta_shd"),
        "fusion_helped": benefit.get("fusion_helped"),
        "n_nodes_gained": benefit.get("n_nodes_gained"),
        "n_edges_gained": benefit.get("n_edges_gained"),
        "baseline_edge_recall": gain.get("baseline_edge_recall"),
        "fused_edge_recall": gain.get("self_edge_recall"),
        "gained_nodes": ";".join(
            "{0}@{1:.2f}".format(n.get("event_type"), float(n.get("t_peak", 0.0)))
            for n in benefit.get("gained_nodes", []) or []
        ),
        "gained_edges": ";".join(
            "{0}->{1}[{2}]".format(
                e.get("source_type"), e.get("target_type"), e.get("edge_type")
            )
            for e in benefit.get("gained_edges", []) or []
        ),
    }
    return [_with_ident(metrics, row)]


ASSOCIATION_METRICS_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "track_id",
    "observer_id",
    "status",
    "assigned_participant",
    "true_participant",
    "verdict",
    "confidence",
    "rmse_m",
    "overlap_s",
    "runner_up",
    "true_identity_distance_m",
    "true_identity_n_samples",
]


def association_metrics_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per radar track, with both the claimed and the true identity."""
    assoc = _block(metrics, "association")
    if assoc is None:
        return []
    keys = [c for c in ASSOCIATION_METRICS_COLUMNS if c not in _IDENT_COLUMNS]
    return [
        _with_ident(metrics, {k: track.get(k) for k in keys})
        for track in assoc.get("tracks", []) or []
    ]


ATTRIBUTION_METRICS_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "precision",
    "recall",
    "f1",
    "n_true_positive",
    "n_false_positive",
    "n_false_negative",
    "reference_initiators",
    "predicted_candidates",
    "primary_initiator_reference",
    "primary_initiator_predicted",
    "primary_initiator_correct",
    "classification_reference",
    "classification_predicted",
    "classification_correct",
    "n_insufficient_evidence",
]


def attribution_metrics_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per run summarising causal attribution against the oracle."""
    attr = _block(metrics, "attribution")
    if attr is None:
        return []
    primary = _block(attr, "primary_initiator") or {}
    classification = _block(attr, "classification") or {}
    row = {
        "precision": attr.get("precision"),
        "recall": attr.get("recall"),
        "f1": attr.get("f1"),
        "n_true_positive": attr.get("n_true_positive"),
        "n_false_positive": attr.get("n_false_positive"),
        "n_false_negative": attr.get("n_false_negative"),
        "reference_initiators": ";".join(attr.get("reference_initiators", []) or []),
        "predicted_candidates": ";".join(attr.get("predicted_candidates", []) or []),
        "primary_initiator_reference": primary.get("reference", primary.get("oracle")),
        "primary_initiator_predicted": primary.get("predicted"),
        "primary_initiator_correct": primary.get("correct"),
        "classification_reference": classification.get("reference", classification.get("oracle")),
        "classification_predicted": classification.get("predicted"),
        "classification_correct": classification.get("correct"),
        "n_insufficient_evidence": attr.get("n_insufficient_evidence"),
    }
    return [_with_ident(metrics, row)]


MODEL_CHECK_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "property_id",
    "participant_id",
    "status",
    "reason",
]


def model_check_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per (property, participant) verdict, ``UNKNOWN`` included.

    ``UNKNOWN`` rows are the point of the three-valued monitor and are never
    filtered out here: dropping them would turn "the evidence could not decide"
    into a silent pass.
    """
    block = _block(metrics, "model_check")
    if block is None:
        return []
    return [
        _with_ident(
            metrics,
            {
                "property_id": r.get("property_id"),
                "participant_id": r.get("participant_id"),
                "status": r.get("status"),
                "reason": r.get("reason", ""),
            },
        )
        for r in block.get("results", []) or []
    ]


SCENARIO_VALIDATION_COLUMNS: List[str] = _IDENT_COLUMNS + [
    "passed",
    "expected_outcome",
    "outcome",
    "n_problems",
    "problems",
    "min_separation_m",
    "n_collision_pairs",
]


def scenario_validation_rows(metrics: Mapping[str, Any]) -> List[Dict[str, Any]]:
    """One row per run recording whether the scenario did what it was designed to."""
    block = _block(metrics, "scenario_validation")
    if block is None:
        return []
    checks = _block(block, "checks") or {}
    separation = checks.get("min_separation") or {}
    row = {
        "passed": block.get("passed"),
        "expected_outcome": block.get("expected_outcome"),
        "outcome": metrics.get("outcome", ""),
        "n_problems": len(block.get("problems", []) or []),
        "problems": ";".join(str(p) for p in block.get("problems", []) or []),
        "min_separation_m": (
            separation.get("distance_m") if isinstance(separation, Mapping) else None
        ),
        "n_collision_pairs": len(checks.get("collision_pairs", []) or []),
    }
    return [_with_ident(metrics, row)]


def concat(rows_per_run: Sequence[Sequence[Mapping[str, Any]]]) -> List[Dict[str, Any]]:
    """Flatten per-run row lists into one table, preserving order."""
    out: List[Dict[str, Any]] = []
    for rows in rows_per_run:
        out.extend(dict(r) for r in rows)
    return out
