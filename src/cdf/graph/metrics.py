"""Reconstruction-quality metrics for events and graphs.

Every number published by the evaluation layer is computed here, from the
tolerance-correct matcher in :mod:`cdf.graph.matching`. Keeping the definitions
in one module is what makes "the fused graph beats the best single vehicle"
falsifiable: the same code path, the same tolerance and the same node
correspondence are used for the local graphs, for the fused graph and for the
oracle reference, so the deltas cannot be an artifact of three slightly
different comparison procedures.

Nothing here reads the configuration directly: tolerances arrive as explicit
arguments so that a caller cannot accidentally evaluate two graphs under two
different thresholds. Callers read ``evaluation.event_match.time_tolerance_s``
and ``evaluation.event_match.require_same_type`` from the :class:`Config` once
and pass them down.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from ..common.schemas import Event, GraphDocument
from .matching import match_edges, match_events

__all__ = [
    "prf1",
    "event_metrics",
    "graph_structure_metrics",
    "compare_local_vs_fused",
]


# ---------------------------------------------------------------------------
# Elementary counting
# ---------------------------------------------------------------------------


def prf1(tp: int, fp: int, fn: int) -> Dict[str, float]:
    """Precision, recall and F1 from raw counts.

    Undefined quantities return ``0.0`` rather than ``nan``: a graph that
    predicted nothing has precision 0, not "no opinion", and a downstream mean
    over scenarios must not be poisoned by a ``nan``. The convention is applied
    consistently so that an empty prediction and an entirely wrong prediction are
    scored the same, which is the conservative reading for a forensic claim.
    """
    tp_i, fp_i, fn_i = int(tp), int(fp), int(fn)
    if min(tp_i, fp_i, fn_i) < 0:
        raise ValueError(
            "prf1 counts must be non-negative, got tp={0}, fp={1}, fn={2}".format(tp, fp, fn)
        )
    precision = float(tp_i) / float(tp_i + fp_i) if (tp_i + fp_i) > 0 else 0.0
    recall = float(tp_i) / float(tp_i + fn_i) if (tp_i + fn_i) > 0 else 0.0
    f1 = (
        2.0 * precision * recall / (precision + recall)
        if (precision + recall) > 0.0
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


def _median(values: Sequence[float]) -> float:
    """Median of a sequence (``0.0`` when empty)."""
    if not values:
        return 0.0
    ordered = sorted(float(v) for v in values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


# ---------------------------------------------------------------------------
# Event-level metrics
# ---------------------------------------------------------------------------


def event_metrics(
    pred: Sequence[Event],
    truth: Sequence[Event],
    tolerance_s: float,
    require_same_type: bool = True,
    subject_map_pred: Optional[Mapping[str, str]] = None,
    subject_map_truth: Optional[Mapping[str, str]] = None,
    require_same_subject: bool = False,
    require_same_participant: bool = False,
) -> Dict[str, Any]:
    """Detection quality of an event list against a reference list.

    A matched pair is a true positive, an unmatched prediction a false positive
    and an unmatched reference event a false negative. The timing errors are
    reported separately (mean *and* median) because the two answer different
    questions: the mean exposes a systematic lag in the detector, the median is
    robust to the single badly-placed event that a burst of radar returns can
    produce.
    """
    result = match_events(
        pred,
        truth,
        tolerance_s=tolerance_s,
        require_same_type=require_same_type,
        subject_map_a=subject_map_pred,
        subject_map_b=subject_map_truth,
        require_same_subject=require_same_subject,
        require_same_participant=require_same_participant,
    )
    tp = result["n_matched"]
    fp = len(result["unmatched_a"])
    fn = len(result["unmatched_b"])
    abs_dts = [abs(dt) for _a, _b, dt in result["matches"]]
    out: Dict[str, Any] = dict(prf1(tp, fp, fn))
    out.update(
        {
            "n_matched": tp,
            "n_pred": len(pred),
            "n_truth": len(truth),
            "n_false_positive": fp,
            "n_false_negative": fn,
            "mean_abs_timing_error": (
                float(sum(abs_dts) / len(abs_dts)) if abs_dts else 0.0
            ),
            "median_abs_timing_error": _median(abs_dts),
            "max_abs_timing_error": float(max(abs_dts)) if abs_dts else 0.0,
            "tolerance_s": float(tolerance_s),
            "matches": list(result["matches"]),
            "unmatched_pred": list(result["unmatched_a"]),
            "unmatched_truth": list(result["unmatched_b"]),
        }
    )
    return out


# ---------------------------------------------------------------------------
# Graph-level metrics
# ---------------------------------------------------------------------------


def graph_structure_metrics(
    pred: GraphDocument,
    truth: GraphDocument,
    tolerance_s: float,
    require_same_type: bool = True,
    subject_map_pred: Optional[Mapping[str, str]] = None,
    subject_map_truth: Optional[Mapping[str, str]] = None,
    require_same_subject: bool = False,
    restrict_to_matched_nodes: bool = False,
) -> Dict[str, Any]:
    """Node and edge agreement between a reconstructed graph and a reference.

    Nodes are paired by :func:`cdf.graph.matching.match_events`; edges are then
    classified by :func:`cdf.graph.matching.match_edges` under that pairing.

    Structural Hamming distance
    ---------------------------
    ``structural_hamming_distance`` is the number of single-edge edits needed to
    turn the predicted graph into the reference *over the matched node set*::

        SHD = n_missing + n_extra + n_reversed

    where ``n_missing`` counts reference edges absent from the prediction,
    ``n_extra`` counts predicted edges absent from the reference, and
    ``n_reversed`` counts predicted edges whose endpoints are swapped with
    respect to a reference edge. A reversal costs **one** edit, not two: flipping
    an arrow is a single operation, and charging it twice would make a graph that
    found every causal pair but got one direction wrong look worse than a graph
    that missed the pair entirely.

    An edge touching a node the matcher could not pair is counted by default (a
    reference edge onto an undiscovered node is a genuine miss); pass
    ``restrict_to_matched_nodes`` for the shared-skeleton convention of
    ``evaluation.graph_match.use_matched_nodes_only``. See
    :func:`cdf.graph.matching.match_edges` for why the default is the inclusive
    one; ``n_edges_touching_unmatched_pred`` / ``..._truth`` report the affected
    edge counts either way.

    Edge precision/recall follow the same convention as any detection task: a
    reversal is simultaneously a wrong prediction (false positive) and a missed
    reference edge (false negative), so it is charged to both. Only exactly
    matching edges count as true positives.
    """
    node_result = match_events(
        pred.nodes,
        truth.nodes,
        tolerance_s=tolerance_s,
        require_same_type=require_same_type,
        subject_map_a=subject_map_pred,
        subject_map_b=subject_map_truth,
        require_same_subject=require_same_subject,
    )
    node_scores = prf1(
        node_result["n_matched"],
        len(node_result["unmatched_a"]),
        len(node_result["unmatched_b"]),
    )

    edge_result = match_edges(
        pred,
        truth,
        node_result["map_a_to_b"],
        restrict_to_matched_nodes=restrict_to_matched_nodes,
    )
    n_matched_e = edge_result["n_matched"]
    n_missing = edge_result["n_missing"]
    n_extra = edge_result["n_extra"]
    n_reversed = edge_result["n_reversed"]
    edge_scores = prf1(n_matched_e, n_extra + n_reversed, n_missing + n_reversed)

    abs_dts = [abs(dt) for _a, _b, dt in node_result["matches"]]
    return {
        "node_precision": node_scores["precision"],
        "node_recall": node_scores["recall"],
        "node_f1": node_scores["f1"],
        "edge_precision": edge_scores["precision"],
        "edge_recall": edge_scores["recall"],
        "edge_f1": edge_scores["f1"],
        "structural_hamming_distance": int(n_missing + n_extra + n_reversed),
        "n_nodes_pred": len(pred.nodes),
        "n_nodes_truth": len(truth.nodes),
        "n_nodes_matched": node_result["n_matched"],
        "n_edges_pred": len(pred.edges),
        "n_edges_truth": len(truth.edges),
        "n_edges_matched": n_matched_e,
        "n_missing_edges": n_missing,
        "n_extra_edges": n_extra,
        "n_reversed_edges": n_reversed,
        "n_unmappable_edges_pred": len(edge_result["unmappable_a"]),
        "n_unmappable_edges_truth": len(edge_result["unmappable_b"]),
        "n_edges_touching_unmatched_pred": edge_result["n_touching_unmatched_a"],
        "n_edges_touching_unmatched_truth": edge_result["n_touching_unmatched_b"],
        "missing_edges": edge_result["missing"],
        "extra_edges": edge_result["extra"],
        "reversed_edges": edge_result["reversed"],
        "matched_edges": edge_result["matched"],
        "node_matches": list(node_result["matches"]),
        "mean_abs_timing_error": float(sum(abs_dts) / len(abs_dts)) if abs_dts else 0.0,
        "median_abs_timing_error": _median(abs_dts),
        "tolerance_s": float(tolerance_s),
    }


def _rank_key(metrics: Mapping[str, Any], participant_id: str) -> Tuple[float, float, float, str]:
    """Ordering used to pick the best single local reconstruction.

    Edge F1 first (the structural claim under test), node F1 as a tie-break, then
    the *lower* structural Hamming distance, then the participant id so that the
    choice is reproducible when two participants score identically.
    """
    return (
        -float(metrics["edge_f1"]),
        -float(metrics["node_f1"]),
        float(metrics["structural_hamming_distance"]),
        str(participant_id),
    )


def compare_local_vs_fused(
    local_docs: Mapping[str, GraphDocument],
    fused: GraphDocument,
    truth: GraphDocument,
    tolerance_s: float,
    require_same_type: bool = True,
    subject_maps: Optional[Mapping[str, Mapping[str, str]]] = None,
    subject_map_truth: Optional[Mapping[str, str]] = None,
    restrict_to_matched_nodes: bool = False,
) -> Dict[str, Any]:
    """Score every local graph, the fused graph, and their difference.

    This is the central experimental comparison of the project: fusion is only
    worth its complexity if it beats the *best* single onboard reconstruction,
    not merely the average one -- averaging would let a participant that saw
    nothing flatter the fused result. The best local graph is therefore selected
    explicitly (see :func:`_rank_key`) and the reported deltas are against it.

    ``subject_maps`` optionally carries, per participant, the fusion layer's
    ``track_id -> participant_id`` resolution, so that a local graph's anonymous
    track subjects can be compared against the reference's participant labels.
    """
    if not local_docs:
        raise ValueError("compare_local_vs_fused requires at least one local graph")

    maps = dict(subject_maps or {})
    per_participant: Dict[str, Dict[str, Any]] = {}
    for pid in sorted(local_docs):
        per_participant[pid] = graph_structure_metrics(
            local_docs[pid],
            truth,
            tolerance_s=tolerance_s,
            require_same_type=require_same_type,
            subject_map_pred=maps.get(pid),
            subject_map_truth=subject_map_truth,
            restrict_to_matched_nodes=restrict_to_matched_nodes,
        )

    best_pid = sorted(
        per_participant, key=lambda p: _rank_key(per_participant[p], p)
    )[0]
    best = per_participant[best_pid]

    fused_metrics = graph_structure_metrics(
        fused,
        truth,
        tolerance_s=tolerance_s,
        require_same_type=require_same_type,
        subject_map_pred=maps.get("fused"),
        subject_map_truth=subject_map_truth,
        restrict_to_matched_nodes=restrict_to_matched_nodes,
    )

    return {
        "per_participant": per_participant,
        "best_single_local": {"participant_id": best_pid, "metrics": best},
        "best_local_participant_id": best_pid,
        "fused": fused_metrics,
        "delta_edge_f1": float(fused_metrics["edge_f1"]) - float(best["edge_f1"]),
        "delta_node_f1": float(fused_metrics["node_f1"]) - float(best["node_f1"]),
        "delta_shd": int(fused_metrics["structural_hamming_distance"])
        - int(best["structural_hamming_distance"]),
        "n_participants": len(per_participant),
        "tolerance_s": float(tolerance_s),
    }
