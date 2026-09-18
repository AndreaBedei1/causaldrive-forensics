"""Comparing a reconstruction with the observable ground truth, row by row.

The metric this produces is the project's primary result, so it is built to be
*inspected* rather than trusted. Every number here is backed by a row naming the
two events it came from, the time each side put them at, and — where they did not
match — which of the several ways to fail applies.

Three things this does that the older comparison did not:

**It compares over the shared vocabulary.** Both graphs are reduced to the types
:mod:`cdf.graph.ontology` says both sides may assert. A reconstruction is not
penalised for failing to emit something no reconstruction can emit, and a
reference is not credited for asserting something no reconstruction can check.
What was set aside is counted and named, never silently dropped.

**It treats an outcome as the unordered pair it is.** A collision between A and B
is one physical event. One graph may record it as ``COLLISION(A, subject=B)`` and
the other as ``COLLISION(B, subject=A)``; those are the same claim, and a matcher
that misses that reports a false positive and a false negative for an event both
sides got right.

**It distinguishes the ways an edge can be wrong.** A missing edge, an invented
edge, an edge between the right events with the wrong relation, and an edge drawn
backwards are four different failures with four different diagnoses, and
collapsing them into "not matched" throws away most of what a diff is for.
"""

from __future__ import annotations

import dataclasses
import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.schemas import Event, EventType, GraphDocument
from ..graph.matching import match_edges, match_events
from ..graph.ontology import OUTCOME_TYPES, comparable_view, family
from .causal_metrics import prf1

LOGGER = logging.getLogger(__name__)

__all__ = [
    "compare_graphs",
    "normalise_outcome_pairs",
    "NODE_MATCH_COLUMNS",
    "EDGE_MATCH_COLUMNS",
]


NODE_MATCH_COLUMNS: Tuple[str, ...] = (
    "status",
    "event_type",
    "participant",
    "subject",
    "reference_id",
    "inferred_id",
    "reference_t",
    "inferred_t",
    "abs_timing_error_s",
    "inferred_confidence",
    "observed_by",
)

EDGE_MATCH_COLUMNS: Tuple[str, ...] = (
    "status",
    "edge_type",
    "source_type",
    "source_participant",
    "target_type",
    "target_participant",
    "reference_source",
    "reference_target",
    "inferred_source",
    "inferred_target",
    "inferred_confidence",
    "inferred_rule",
    "origin",
)


def normalise_outcome_pairs(doc: Optional[GraphDocument]) -> Optional[GraphDocument]:
    """Put every outcome event's pair in a fixed order.

    A collision, a near miss and a post-impact stop are facts about a pair of
    vehicles, not about one of them observing the other. Which vehicle a graph
    happens to file the event under is an artifact of who recorded it first, and
    two graphs that disagree about that are not disagreeing about anything
    physical. Ordering the pair lexically makes the two comparable.

    ``POST_IMPACT_STOP`` is deliberately left alone: it is about one vehicle
    coming to rest, and the subject, when present, names the impact rather than a
    second party to the event.
    """
    if doc is None:
        return None
    nodes: List[Event] = []
    for node in doc.nodes:
        value = node.event_type.value if hasattr(node.event_type, "value") else str(
            node.event_type
        )
        if (
            value in OUTCOME_TYPES
            and value != EventType.POST_IMPACT_STOP.value
            and node.subject
            and str(node.subject) < str(node.participant_id)
        ):
            nodes.append(dataclasses.replace(
                node,
                participant_id=str(node.subject),
                subject=str(node.participant_id),
            ))
        else:
            nodes.append(node)
    return dataclasses.replace(doc, nodes=nodes)


def _prepare(doc: Optional[GraphDocument]) -> Optional[GraphDocument]:
    """The view of a graph the primary comparison actually looks at."""
    return normalise_outcome_pairs(comparable_view(doc))


def _describe(node: Optional[Event]) -> Dict[str, Any]:
    if node is None:
        return {}
    return {
        "event_type": node.event_type.value if hasattr(node.event_type, "value")
        else str(node.event_type),
        "participant": str(node.participant_id),
        "subject": str(node.subject) if node.subject else "",
        "t_peak": round(float(node.t_peak), 6),
        "confidence": round(float(node.confidence), 6),
        "observed_by": ",".join(sorted(str(o) for o in (node.owners or []))),
    }


def compare_graphs(
    inferred: Optional[GraphDocument],
    reference: Optional[GraphDocument],
    cfg: Config,
    label: str = "inferred",
    subject_map: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """Score one reconstruction against the observable ground truth.

    Node correspondence is solved first, by a globally optimal assignment over
    events of the same type, the same participant and the same subject, within a
    time tolerance. Edges are then compared *through* that correspondence: an
    inferred edge counts only if both its endpoints matched a reference node and
    the reference has the same relation between those two nodes.

    Returns the metrics, and beside them the rows they were computed from.
    """
    if reference is None:
        return {
            "scored": False,
            "reason": "no observable ground truth for this run",
            "label": label,
        }

    reference_view = _prepare(reference)
    inferred_view = _prepare(inferred)
    tolerance = float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5))

    if inferred_view is None or not inferred_view.nodes:
        return {
            "scored": True,
            "label": label,
            "reason": "the reconstruction produced no comparable node",
            "nodes": _empty_scores(len(reference_view.nodes)),
            "edges": _empty_scores(len(reference_view.edges)),
            "node_rows": [
                {"status": "missing", **_describe(n), "reference_id": n.event_id}
                for n in reference_view.nodes
            ],
            "edge_rows": [],
            "ontology": _ontology_summary(inferred, reference, inferred_view,
                                          reference_view),
        }

    matched = match_events(
        inferred_view.nodes,
        reference_view.nodes,
        tolerance_s=tolerance,
        require_same_type=True,
        subject_map_a=subject_map,
        require_same_subject=True,
        require_same_participant=True,
    )
    node_map: Dict[str, str] = dict(matched.get("map_a_to_b") or {})

    inferred_by_id = {n.event_id: n for n in inferred_view.nodes}
    reference_by_id = {n.event_id: n for n in reference_view.nodes}

    node_rows: List[Dict[str, Any]] = []
    for inferred_id, reference_id in sorted(node_map.items()):
        a, b = inferred_by_id[inferred_id], reference_by_id[reference_id]
        node_rows.append({
            "status": "matched",
            **_describe(b),
            "reference_id": reference_id,
            "inferred_id": inferred_id,
            "reference_t": round(float(b.t_peak), 6),
            "inferred_t": round(float(a.t_peak), 6),
            "abs_timing_error_s": round(abs(float(a.t_peak) - float(b.t_peak)), 6),
            "inferred_confidence": round(float(a.confidence), 6),
        })
    for reference_id in sorted(set(reference_by_id) - set(node_map.values())):
        node = reference_by_id[reference_id]
        node_rows.append({
            "status": "missing",
            **_describe(node),
            "reference_id": reference_id,
            "inferred_id": "",
            "reference_t": round(float(node.t_peak), 6),
        })
    for inferred_id in sorted(set(inferred_by_id) - set(node_map)):
        node = inferred_by_id[inferred_id]
        node_rows.append({
            "status": "extra",
            **_describe(node),
            "reference_id": "",
            "inferred_id": inferred_id,
            "inferred_t": round(float(node.t_peak), 6),
            "inferred_confidence": round(float(node.confidence), 6),
        })

    edge_result = match_edges(inferred_view, reference_view, node_map)
    edge_rows = _edge_rows(edge_result, inferred_view, reference_view, node_map)

    timing = [
        r["abs_timing_error_s"] for r in node_rows if r["status"] == "matched"
    ]

    return {
        "scored": True,
        "label": label,
        "tolerance_s": tolerance,
        "nodes": {
            "n_reference": len(reference_view.nodes),
            "n_inferred": len(inferred_view.nodes),
            "n_matched": len(node_map),
            "precision": _ratio(len(node_map), len(inferred_view.nodes)),
            "recall": _ratio(len(node_map), len(reference_view.nodes)),
            "f1": _f1(
                _ratio(len(node_map), len(inferred_view.nodes)),
                _ratio(len(node_map), len(reference_view.nodes)),
            ),
            "mean_abs_timing_error_s": (
                round(sum(timing) / len(timing), 6) if timing else None
            ),
            "max_abs_timing_error_s": round(max(timing), 6) if timing else None,
        },
        "edges": {
            "n_reference": len(reference_view.edges),
            "n_inferred": len(inferred_view.edges),
            "n_matched": edge_result.get("n_matched", 0),
            "n_missing": len(edge_result.get("missing") or []),
            "n_extra": len(edge_result.get("extra") or []),
            "n_reversed": len(edge_result.get("reversed") or []),
            "precision": _ratio(
                edge_result.get("n_matched", 0), len(inferred_view.edges)
            ),
            "recall": _ratio(
                edge_result.get("n_matched", 0), len(reference_view.edges)
            ),
            "f1": _f1(
                _ratio(edge_result.get("n_matched", 0), len(inferred_view.edges)),
                _ratio(edge_result.get("n_matched", 0), len(reference_view.edges)),
            ),
        },
        "paths": _path_scores(inferred_view, reference_view, node_map, cfg),
        "node_rows": node_rows,
        "edge_rows": edge_rows,
        "ontology": _ontology_summary(inferred, reference, inferred_view,
                                      reference_view),
    }


def _ratio(matched: int, total: int) -> float:
    return round(matched / total, 6) if total else 0.0


def _f1(precision: float, recall: float) -> float:
    return round(
        2 * precision * recall / (precision + recall), 6
    ) if (precision + recall) else 0.0


def _empty_scores(n_reference: int) -> Dict[str, Any]:
    return {
        "n_reference": n_reference, "n_inferred": 0, "n_matched": 0,
        "precision": 0.0, "recall": 0.0, "f1": 0.0,
    }


def _ontology_summary(
    inferred: Optional[GraphDocument],
    reference: GraphDocument,
    inferred_view: Optional[GraphDocument],
    reference_view: GraphDocument,
) -> Dict[str, Any]:
    """What the shared-vocabulary restriction set aside on each side."""
    def block(doc: Optional[GraphDocument]) -> Dict[str, Any]:
        if doc is None:
            return {}
        return dict((doc.meta or {}).get("ontology") or {})

    return {
        "inferred": block(inferred_view),
        "reference": block(reference_view),
        "note": (
            "the comparison is over the vocabulary both sides may assert; what "
            "each side said outside it is counted here rather than scored as an "
            "error"
        ),
    }


def _edge_rows(
    edge_result: Mapping[str, Any],
    inferred: GraphDocument,
    reference: GraphDocument,
    node_map: Mapping[str, str],
) -> List[Dict[str, Any]]:
    """One row per edge on either side, classified by how it fared."""
    inferred_nodes = {n.event_id: n for n in inferred.nodes}
    reference_nodes = {n.event_id: n for n in reference.nodes}
    rows: List[Dict[str, Any]] = []

    def endpoints(node_id: str, lookup: Mapping[str, Event]) -> Dict[str, str]:
        node = lookup.get(node_id)
        if node is None:
            return {"type": "", "participant": ""}
        return {
            "type": node.event_type.value if hasattr(node.event_type, "value")
            else str(node.event_type),
            "participant": str(node.participant_id),
        }

    for status_key, status in (
        ("matched", "true_positive"),
        ("missing", "missing_edge"),
        ("extra", "extra_edge"),
        ("reversed", "wrong_direction"),
    ):
        for entry in edge_result.get(status_key) or []:
            source = entry.get("source") or entry.get("a_source") or ""
            target = entry.get("target") or entry.get("a_target") or ""
            in_reference = status in ("missing_edge",)
            lookup = reference_nodes if in_reference else inferred_nodes
            src = endpoints(source, lookup)
            tgt = endpoints(target, lookup)
            rows.append({
                "status": status,
                "edge_type": entry.get("edge_type", ""),
                "source_type": src["type"],
                "source_participant": src["participant"],
                "target_type": tgt["type"],
                "target_participant": tgt["participant"],
                "reference_source": source if in_reference else
                (entry.get("b_source") or node_map.get(source, "")),
                "reference_target": target if in_reference else
                (entry.get("b_target") or node_map.get(target, "")),
                "inferred_source": "" if in_reference else source,
                "inferred_target": "" if in_reference else target,
                "inferred_confidence": entry.get("confidence"),
                "inferred_rule": entry.get("rule", ""),
                "origin": (entry.get("detail") or {}).get("origin", ""),
            })
    rows.sort(key=lambda r: (r["status"], r["source_type"], r["target_type"]))
    return rows


def _path_scores(
    inferred: GraphDocument,
    reference: GraphDocument,
    node_map: Mapping[str, str],
    cfg: Config,
) -> Dict[str, Any]:
    """Whether the chains into each outcome were recovered.

    A path is compared by the sequence of ``(type, participant)`` pairs it runs
    through, in the reference's own terms: an inferred path is translated through
    the node correspondence first. That way a chain counts as recovered when it
    passes through the same physical events, whatever the reconstruction called
    their ids.

    Ancestry recall is the weaker, more robust question, and usually the more
    informative one: of the events the reference puts upstream of an outcome, how
    many does the reconstruction also put upstream of it?
    """
    from ..graph.analysis import GraphAnalyzer

    max_paths = int(cfg.get("evaluation.causal_paths.max_paths_per_outcome", 64))
    collision = EventType.COLLISION.value

    def outcomes(doc: GraphDocument) -> List[str]:
        return sorted(
            n.event_id for n in doc.nodes
            if (n.event_type.value if hasattr(n.event_type, "value")
                else str(n.event_type)) == collision
        )

    def signature(doc: GraphDocument, path: Sequence[str],
                  translate: Optional[Mapping[str, str]] = None) -> Tuple[str, ...]:
        nodes = {n.event_id: n for n in doc.nodes}
        out: List[str] = []
        for node_id in path:
            key = translate.get(node_id) if translate else node_id
            if key is None:
                return tuple()
            node = nodes.get(key) if translate else nodes.get(node_id)
            if node is None:
                return tuple()
            out.append("{0}@{1}".format(
                node.event_type.value if hasattr(node.event_type, "value")
                else str(node.event_type),
                node.participant_id,
            ))
        return tuple(out)

    reference_analyzer = GraphAnalyzer(reference, cfg)
    reference_paths: Set[Tuple[str, ...]] = set()
    reference_ancestry: Set[str] = set()
    reference_nodes = {n.event_id: n for n in reference.nodes}
    for outcome in outcomes(reference):
        for node_id in reference_analyzer.ancestors(outcome):
            node = reference_nodes.get(node_id)
            if node is not None:
                reference_ancestry.add("{0}@{1}".format(
                    node.event_type.value if hasattr(node.event_type, "value")
                    else str(node.event_type), node.participant_id))
        for path in reference_analyzer.causal_paths_to(outcome)[:max_paths]:
            sig = signature(reference, path)
            if sig:
                reference_paths.add(sig)

    inferred_analyzer = GraphAnalyzer(inferred, cfg)
    inferred_paths: Set[Tuple[str, ...]] = set()
    inferred_ancestry: Set[str] = set()
    for outcome in outcomes(inferred):
        for node_id in inferred_analyzer.ancestors(outcome):
            mapped = node_map.get(node_id)
            node = reference_nodes.get(mapped) if mapped else None
            if node is not None:
                inferred_ancestry.add("{0}@{1}".format(
                    node.event_type.value if hasattr(node.event_type, "value")
                    else str(node.event_type), node.participant_id))
        for path in inferred_analyzer.causal_paths_to(outcome)[:max_paths]:
            sig = signature(reference, path, translate=node_map)
            if sig:
                inferred_paths.add(sig)

    path_score = prf1(
        {"|".join(s) for s in reference_paths},
        {"|".join(s) for s in inferred_paths},
    )
    ancestry = prf1(reference_ancestry, inferred_ancestry)
    return {
        "n_reference_paths": len(reference_paths),
        "n_inferred_paths": len(inferred_paths),
        "precision": path_score["precision"],
        "recall": path_score["recall"],
        "f1": path_score["f1"],
        "ancestry_precision": ancestry["precision"],
        "ancestry_recall": ancestry["recall"],
        "ancestry_f1": ancestry["f1"],
        "ancestry_missing": sorted(reference_ancestry - inferred_ancestry),
        "note": (
            "paths are compared through the node correspondence, by the physical "
            "events they pass through rather than by node id"
        ),
    }
