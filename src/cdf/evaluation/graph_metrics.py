"""Structural quality of the reconstructed causal graphs, and what fusion added.

EVALUATION LAYER -- reads both the inference side and the oracle side.

:func:`evaluate_graphs` is the descriptive half: node and edge precision/recall/F1
and structural Hamming distance for every local graph and for the fused graph,
all against the oracle graph, all through
:func:`cdf.graph.metrics.graph_structure_metrics`.

:func:`fusion_benefit` is the *hypothesis test* half. H1/H2 of this project claim
that merging independent onboard reconstructions recovers causal structure that
no single vehicle could have recovered alone. That claim is only meaningful if it
can fail, so this function is written so that it can:

* the baseline is the **best** single local graph, never the mean;
* the deltas are reported with their sign and a strictly-positive threshold, so a
  tie reads as "fusion added nothing";
* the gain is *named* -- the specific oracle-relevant nodes and edges the fused
  graph recovered and the best single view lacks -- so a positive delta can be
  inspected rather than believed.

Nothing here is ever assumed. If the oracle graph is missing the caller must
report the block as unavailable; this module refuses to score against an empty
reference rather than emit a zero that would read as a measured failure.
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..common.config import Config
from ..common.schemas import EventType, GraphDocument
from ..graph.analysis import GraphAnalyzer
from ..graph.metrics import compare_local_vs_fused, graph_structure_metrics
from .event_metrics import event_match_tolerance

__all__ = ["evaluate_graphs", "fusion_benefit", "graph_match_settings"]


def graph_match_settings(cfg: Config) -> Tuple[float, bool, bool]:
    """``(tolerance_s, require_same_type, use_matched_nodes_only)``.

    Read once and threaded through every comparison in this module so that the
    local numbers, the fused numbers and their difference are all evaluated under
    one contract.
    """
    tolerance_s, require_same_type = event_match_tolerance(cfg)
    return (
        tolerance_s,
        require_same_type,
        bool(cfg.get("evaluation.graph_match.use_matched_nodes_only", False)),
    )


def _subject_maps(
    participant_ids: List[str], subject_map: Optional[Mapping[str, str]]
) -> Dict[str, Dict[str, str]]:
    """Per-graph subject resolution for :func:`compare_local_vs_fused`.

    The fusion layer's ``track_id -> participant_id`` map is global (track ids
    carry their observer's prefix), so every graph gets the same mapping; the
    key ``"fused"`` is the one :func:`compare_local_vs_fused` looks up for the
    fused document.
    """
    smap = dict(subject_map or {})
    maps: Dict[str, Dict[str, str]] = {pid: dict(smap) for pid in participant_ids}
    maps["fused"] = dict(smap)
    return maps


def _require_reference(oracle_doc: Optional[GraphDocument], caller: str) -> GraphDocument:
    if oracle_doc is None or not oracle_doc.nodes:
        raise ValueError(
            "{0} needs a non-empty oracle graph as its reference; scoring against an "
            "empty reference would publish zeros that look like a measured failure "
            "(the caller should report the block as unavailable instead)".format(caller)
        )
    return oracle_doc


def evaluate_graphs(
    local_docs: Mapping[str, GraphDocument],
    fused_doc: Optional[GraphDocument],
    oracle_doc: Optional[GraphDocument],
    subject_map: Optional[Mapping[str, str]],
    cfg: Config,
) -> Dict[str, Any]:
    """Node/edge agreement of every local graph and the fused graph with the oracle.

    Returns the per-participant and fused metric blocks (precision, recall, F1,
    structural Hamming distance and the explicit missing/extra/reversed edge
    listings that ``edge_matches.csv`` is written from), plus the fused-minus-
    best-local deltas.

    When ``fused_doc`` is ``None`` only the local graphs are scored and the fused
    block is ``None`` with a ``fused_reason``: a run whose fusion stage never ran
    has no fused result, which is different from a fused result of zero.
    """
    reference = _require_reference(oracle_doc, "evaluate_graphs")
    if not local_docs:
        raise ValueError("evaluate_graphs needs at least one local graph")

    tolerance_s, require_same_type, matched_only = graph_match_settings(cfg)
    maps = _subject_maps(sorted(local_docs), subject_map)

    if fused_doc is None:
        per_participant = {
            pid: graph_structure_metrics(
                local_docs[pid],
                reference,
                tolerance_s=tolerance_s,
                require_same_type=require_same_type,
                subject_map_pred=maps.get(pid),
                restrict_to_matched_nodes=matched_only,
            )
            for pid in sorted(local_docs)
        }
        best_pid = _best_local_id(per_participant)
        return {
            "tolerance_s": tolerance_s,
            "require_same_type": require_same_type,
            "use_matched_nodes_only": matched_only,
            "n_participants": len(per_participant),
            "per_participant": per_participant,
            "best_local_participant_id": best_pid,
            "best_single_local": {
                "participant_id": best_pid,
                "metrics": per_participant[best_pid],
            },
            "fused": None,
            "fused_reason": "no fused causal graph was available for this run",
            "delta_edge_f1": None,
            "delta_node_f1": None,
            "delta_shd": None,
        }

    comparison = compare_local_vs_fused(
        local_docs,
        fused_doc,
        reference,
        tolerance_s=tolerance_s,
        require_same_type=require_same_type,
        subject_maps=maps,
        subject_map_truth=None,
        restrict_to_matched_nodes=matched_only,
    )
    out: Dict[str, Any] = dict(comparison)
    out["require_same_type"] = require_same_type
    out["use_matched_nodes_only"] = matched_only
    out["n_reference_nodes"] = len(reference.nodes)
    out["n_reference_edges"] = len(reference.edges)
    return out


def _best_local_id(per_participant: Mapping[str, Mapping[str, Any]]) -> str:
    """Same ranking as :func:`cdf.graph.metrics.compare_local_vs_fused` uses."""
    return sorted(
        per_participant,
        key=lambda p: (
            -float(per_participant[p]["edge_f1"]),
            -float(per_participant[p]["node_f1"]),
            float(per_participant[p]["structural_hamming_distance"]),
            str(p),
        ),
    )[0]


def _describe_node(doc: GraphDocument, event_id: str) -> Dict[str, Any]:
    """Human-readable descriptor of a node, so a gain can be read, not trusted."""
    node = doc.node_by_id(event_id)
    if node is None:
        raise KeyError(
            "node {0!r} was reported as gained but is absent from the graph it was "
            "reported from".format(event_id)
        )
    etype = node.event_type.value if isinstance(node.event_type, EventType) else str(
        node.event_type
    )
    return {
        "event_id": event_id,
        "event_type": etype,
        "participant_id": node.participant_id,
        "subject": node.subject,
        "t_peak": float(node.t_peak),
        "owners": list(node.owners),
    }


def _describe_edge(doc: GraphDocument, edge: Any) -> Dict[str, Any]:
    source, target, edge_type = edge
    src = doc.node_by_id(source)
    tgt = doc.node_by_id(target)
    return {
        "source": source,
        "target": target,
        "edge_type": edge_type,
        "source_type": (
            src.event_type.value if src is not None and isinstance(src.event_type, EventType)
            else (str(src.event_type) if src is not None else None)
        ),
        "target_type": (
            tgt.event_type.value if tgt is not None and isinstance(tgt.event_type, EventType)
            else (str(tgt.event_type) if tgt is not None else None)
        ),
        "t_source": float(src.t_peak) if src is not None else None,
        "t_target": float(tgt.t_peak) if tgt is not None else None,
    }


def fusion_benefit(
    local_docs: Mapping[str, GraphDocument],
    fused_doc: GraphDocument,
    oracle_doc: Optional[GraphDocument],
    cfg: Config,
    subject_map: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """Measure -- never assume -- what fusion added over the best single vehicle.

    Returns ``delta_edge_f1``, ``delta_node_f1`` and ``delta_shd`` of the fused
    graph against the best single local graph (both scored against the oracle),
    together with :meth:`cdf.graph.analysis.GraphAnalyzer.knowledge_gain`, which
    names the oracle-relevant nodes and edges the fused graph recovered and the
    baseline lacks.

    ``fusion_helped`` is deliberately strict: it is ``True`` only when the edge
    F1 strictly improved or the structural Hamming distance strictly fell. A run
    where fusion changes nothing reports ``False`` with zero deltas, and a run
    where fusion makes things worse reports negative deltas. Both are results,
    not bugs, and both must survive into the aggregate tables.
    """
    reference = _require_reference(oracle_doc, "fusion_benefit")
    if not local_docs:
        raise ValueError("fusion_benefit needs at least one local graph")
    if fused_doc is None:
        raise ValueError(
            "fusion_benefit needs a fused graph; report the block as unavailable "
            "when the fusion stage did not run"
        )

    tolerance_s, require_same_type, matched_only = graph_match_settings(cfg)
    maps = _subject_maps(sorted(local_docs), subject_map)

    comparison = compare_local_vs_fused(
        local_docs,
        fused_doc,
        reference,
        tolerance_s=tolerance_s,
        require_same_type=require_same_type,
        subject_maps=maps,
        subject_map_truth=None,
        restrict_to_matched_nodes=matched_only,
    )
    best_pid = str(comparison["best_local_participant_id"])
    baseline_doc = local_docs[best_pid]

    analyzer = GraphAnalyzer(fused_doc, cfg)
    # Same tolerance as the structural metrics above, so the gain reported here
    # and the F1 reported there describe one correspondence rather than two.
    gain = analyzer.knowledge_gain(
        baseline_doc,
        reference,
        subject_map_self=maps.get("fused"),
        subject_map_baseline=maps.get(best_pid),
        subject_map_reference=None,
        tolerance_s=tolerance_s,
    )

    delta_edge_f1 = float(comparison["delta_edge_f1"])
    delta_node_f1 = float(comparison["delta_node_f1"])
    delta_shd = int(comparison["delta_shd"])

    return {
        "tolerance_s": tolerance_s,
        "require_same_type": require_same_type,
        "use_matched_nodes_only": matched_only,
        "best_local_participant_id": best_pid,
        "best_local": comparison["best_single_local"]["metrics"],
        "fused": comparison["fused"],
        "delta_edge_f1": delta_edge_f1,
        "delta_node_f1": delta_node_f1,
        "delta_shd": delta_shd,
        "fusion_helped": bool(delta_edge_f1 > 0.0 or delta_shd < 0),
        "knowledge_gain": gain,
        "gained_nodes": [_describe_node(fused_doc, nid) for nid in gain["nodes_gained"]],
        "gained_edges": [_describe_edge(fused_doc, e) for e in gain["edges_gained"]],
        "n_nodes_gained": int(gain["n_nodes_gained"]),
        "n_edges_gained": int(gain["n_edges_gained"]),
        "n_participants": int(comparison["n_participants"]),
    }
