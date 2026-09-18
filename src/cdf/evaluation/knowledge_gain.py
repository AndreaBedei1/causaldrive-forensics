"""Which account first recovers each fact, and what nothing recovers.

An F1 comparison says how much of the ground truth each account reproduced. It
does not say *which parts*, and that is the question this project is actually
about: is there anything the merged logs know that no single vehicle could have
known, and anything the reasoning stage knows that the merge alone did not?

So every ground-truth node and edge is labelled with the earliest account that
recovered it:

``A``, ``B``, ``C``
    exactly one vehicle had it, from its own log;
``multiple_local``
    more than one vehicle had it independently -- the merge did not create this,
    it deduplicated it;
``simple_fusion``
    no single vehicle had it, and pooling the logs produced it. For a node this
    means an identity resolution or a clock alignment made it findable; for an
    edge it means the edge's two endpoints came from different vehicles;
``global_reasoning``
    the merge did not have it either, and the post-fusion causal stage inferred
    it;
``unrecovered``
    nothing found it.

The last category is the honest one and usually the largest. It is reported
whole, with its node and edge types, because a knowledge-gain figure that only
counted successes would be describing a different experiment.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.schemas import Event, GraphDocument
from .graph_comparison import compare_graphs

LOGGER = logging.getLogger(__name__)

__all__ = ["measure_knowledge_gain", "ACCOUNT_ORDER"]

#: Accounts in the order a fact could first have been recovered. Earlier is
#: weaker evidence of gain: a fact one vehicle already had is not something
#: fusion contributed.
ACCOUNT_ORDER: Tuple[str, ...] = (
    "local", "simple_fusion", "global_reasoning",
)


def _matched_reference_ids(result: Mapping[str, Any]) -> Set[str]:
    if not result.get("scored"):
        return set()
    return {
        row["reference_id"] for row in result.get("node_rows") or []
        if row.get("status") == "matched" and row.get("reference_id")
    }


def _matched_reference_edges(result: Mapping[str, Any]) -> Set[Tuple[str, str, str]]:
    if not result.get("scored"):
        return set()
    out: Set[Tuple[str, str, str]] = set()
    for row in result.get("edge_rows") or []:
        if row.get("status") != "true_positive":
            continue
        source = row.get("reference_source") or ""
        target = row.get("reference_target") or ""
        if source and target:
            out.add((source, target, row.get("edge_type", "")))
    return out


def measure_knowledge_gain(
    reference: Optional[GraphDocument],
    locals_by_participant: Mapping[str, GraphDocument],
    simple_fusion: Optional[GraphDocument],
    global_inferred: Optional[GraphDocument],
    cfg: Config,
    subject_map: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """Label every ground-truth node and edge with what first recovered it."""
    if reference is None:
        return {"scored": False, "reason": "no observable ground truth for this run"}

    per_local: Dict[str, Dict[str, Any]] = {
        pid: compare_graphs(doc, reference, cfg, label="local:" + pid,
                            subject_map=subject_map)
        for pid, doc in sorted(locals_by_participant.items())
    }
    local_nodes: Dict[str, Set[str]] = {
        pid: _matched_reference_ids(result) for pid, result in per_local.items()
    }
    local_edges: Dict[str, Set[Tuple[str, str, str]]] = {
        pid: _matched_reference_edges(result) for pid, result in per_local.items()
    }

    fusion_result = (
        compare_graphs(simple_fusion, reference, cfg, label="simple_fusion",
                       subject_map=subject_map)
        if simple_fusion is not None else {"scored": False}
    )
    global_result = (
        compare_graphs(global_inferred, reference, cfg, label="global_inferred",
                       subject_map=subject_map)
        if global_inferred is not None else {"scored": False}
    )

    fusion_nodes = _matched_reference_ids(fusion_result)
    fusion_edges = _matched_reference_edges(fusion_result)
    global_nodes = _matched_reference_ids(global_result)
    global_edges = _matched_reference_edges(global_result)

    reference_nodes = {n.event_id: n for n in reference.nodes}
    node_rows: List[Dict[str, Any]] = []
    for node_id, node in sorted(reference_nodes.items()):
        holders = sorted(pid for pid, ids in local_nodes.items() if node_id in ids)
        node_rows.append({
            "reference_id": node_id,
            "event_type": node.event_type.value if hasattr(node.event_type, "value")
            else str(node.event_type),
            "participant": str(node.participant_id),
            "subject": str(node.subject) if node.subject else "",
            "t_peak": round(float(node.t_peak), 6),
            "local_holders": holders,
            "first_recovered_by": _first_recovered(
                holders, node_id in fusion_nodes, node_id in global_nodes
            ),
        })

    edge_rows: List[Dict[str, Any]] = []
    for edge in reference.edges:
        key = (edge.source, edge.target, edge.edge_type)
        holders = sorted(pid for pid, keys in local_edges.items() if key in keys)
        source = reference_nodes.get(edge.source)
        target = reference_nodes.get(edge.target)
        edge_rows.append({
            "source": edge.source,
            "target": edge.target,
            "edge_type": edge.edge_type,
            "source_type": _type_of(source),
            "target_type": _type_of(target),
            "cross_vehicle": bool(
                source is not None and target is not None
                and str(source.participant_id) != str(target.participant_id)
            ),
            "local_holders": holders,
            "first_recovered_by": _first_recovered(
                holders, key in fusion_edges, key in global_edges
            ),
        })

    return {
        "scored": True,
        "nodes": _summarise(node_rows, len(reference_nodes)),
        "edges": _summarise(edge_rows, len(reference.edges)),
        "node_rows": node_rows,
        "edge_rows": edge_rows,
        "cross_vehicle_edges": _cross_vehicle_summary(edge_rows),
        "per_local_participant": {
            pid: {
                "n_nodes_recovered": len(local_nodes[pid]),
                "n_edges_recovered": len(local_edges[pid]),
            }
            for pid in sorted(local_nodes)
        },
        "note": (
            "each ground-truth fact is labelled with the earliest account that "
            "recovered it. A fact one vehicle already had is not something "
            "fusion contributed, so 'multiple_local' counts as deduplication "
            "rather than gain"
        ),
    }


def _type_of(node: Optional[Event]) -> str:
    if node is None:
        return ""
    return node.event_type.value if hasattr(node.event_type, "value") else str(
        node.event_type
    )


def _first_recovered(
    local_holders: Sequence[str], in_fusion: bool, in_global: bool
) -> str:
    """The earliest account that had this fact."""
    if len(local_holders) == 1:
        return local_holders[0]
    if len(local_holders) > 1:
        return "multiple_local"
    if in_fusion:
        return "simple_fusion"
    if in_global:
        return "global_reasoning"
    return "unrecovered"


def _summarise(rows: Sequence[Mapping[str, Any]], total: int) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for row in rows:
        key = row["first_recovered_by"]
        counts[key] = counts.get(key, 0) + 1
    single_local = sum(
        n for key, n in counts.items()
        if key not in ("multiple_local", "simple_fusion", "global_reasoning",
                       "unrecovered")
    )
    return {
        "n_reference": total,
        "by_account": dict(sorted(counts.items())),
        "n_single_local": single_local,
        "n_multiple_local": counts.get("multiple_local", 0),
        "n_only_after_fusion": counts.get("simple_fusion", 0),
        "n_only_after_global_reasoning": counts.get("global_reasoning", 0),
        "n_unrecovered": counts.get("unrecovered", 0),
        "fraction_only_after_fusion": (
            round(counts.get("simple_fusion", 0) / total, 6) if total else None
        ),
        "fraction_only_after_global_reasoning": (
            round(counts.get("global_reasoning", 0) / total, 6) if total else None
        ),
        "fraction_unrecovered": (
            round(counts.get("unrecovered", 0) / total, 6) if total else None
        ),
    }


def _cross_vehicle_summary(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Edges whose endpoints belong to different vehicles.

    These are the ones no single vehicle could draw even in principle: one end
    is an event it never observed. If distributed fusion adds anything to causal
    reconstruction, this is where it has to show up.
    """
    cross = [r for r in rows if r["cross_vehicle"]]
    recovered = [r for r in cross if r["first_recovered_by"] != "unrecovered"]
    by_account: Dict[str, int] = {}
    for row in cross:
        by_account[row["first_recovered_by"]] = (
            by_account.get(row["first_recovered_by"], 0) + 1
        )
    return {
        "n_cross_vehicle": len(cross),
        "n_recovered": len(recovered),
        "recall": round(len(recovered) / len(cross), 6) if cross else None,
        "by_account": dict(sorted(by_account.items())),
        "note": (
            "an edge between events belonging to different vehicles cannot be "
            "drawn inside one vehicle's log: one endpoint is an event it never "
            "observed. Any of these recovered by a single local graph would "
            "indicate a bug rather than a capability"
        ),
    }
