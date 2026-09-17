"""Merging the participants' independent causal reconstructions into one graph.

What fusion is allowed to do
----------------------------
Each participant arrived at its local graph alone, from its own telemetry, its
own controls and its own radar. Fusion may only:

* rename the *same* physical event, asserted by several participants, to a single
  fused node (identity comes from :mod:`cdf.fusion.track_association` and
  :mod:`cdf.fusion.event_alignment`, never from a simulator id);
* accumulate the confidence attached to concurring claims
  (:mod:`cdf.fusion.confidence`);
* record, rather than adjudicate, the places where the participants disagree.

What fusion must never do is make a claim disappear. When two participants assert
different relations between the same pair of nodes -- one says ``PREVENTS`` where
another says ``CONTRIBUTES_TO`` -- both edges survive into the fused graph and the
disagreement is written into ``diagnostics["contradictions"]`` and into each
edge's ``detail``. An investigator reading the artifact must be able to see that
the evidence conflicts; a single averaged edge would hide exactly the fact that
matters most.

The one structural guarantee imposed on the result is acyclicity: a causal DAG
with a cycle is not a causal model. Cycles can appear from fusion alone (``A``
asserts ``X -> Y`` while ``B`` asserts ``Y -> X``), so the last stage removes the
weakest edge of each cycle -- and records every removal, again, rather than
dropping it silently.

This module imports nothing from :mod:`cdf.oracle` or :mod:`cdf.simulation`.
"""

from __future__ import annotations

import inspect
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

import networkx as nx

from ..common.config import Config
from ..common.evidence import RunEvidence
from ..common.schemas import (
    SCHEMA_VERSIONS,
    Event,
    EventType,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
    assert_non_oracle,
    make_event_id,
    stable_digest,
)
from .confidence import fuse_confidence
from .event_alignment import EventGroup, align_event_records, resolve_subjects
from .track_association import STATUS_UNRESOLVED, TrackAssignment
from .aligned_evidence import AlignedRunEvidence, participant_is_aligned, require_common_time

__all__ = ["fuse_graphs"]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def fuse_graphs(
    run: RunEvidence,
    local_docs: Mapping[str, GraphDocument],
    assignments: Mapping[str, TrackAssignment],
    cfg: Config,
    graph_kind: str = "causal",
) -> Tuple[GraphDocument, Dict[str, Any]]:
    """Fuse the participants' local graphs into one ``FUSED`` graph document.

    Parameters
    ----------
    run:
        The run's local evidence, used for run identification and for naming the
        counterpart of an own-recorded relational event (see
        :mod:`cdf.fusion.event_alignment`).
    local_docs:
        ``participant_id -> GraphDocument``; every document must have scope
        ``LOCAL`` and the requested ``graph_kind``.
    assignments:
        The track association result; it supplies the identities without which
        cross-participant merging would be guesswork.

    Returns
    -------
    ``(fused_document, diagnostics)``. The document has ``scope=FUSED`` and
    ``owner=None`` because it belongs to no single participant.
    """
    require_common_time(run)
    unresolved = [p for p in local_docs if not participant_is_aligned(run,p)]
    docs: Dict[str, GraphDocument] = {}
    for pid in sorted(local_docs.keys()):
        doc = local_docs[pid]
        assert_non_oracle(doc, "graph fusion input for participant {0!r}".format(pid))
        if pid in unresolved:
            continue
        if doc.scope is not Provenance.LOCAL:
            raise ValueError(
                "fusion expects LOCAL graphs; participant {0!r} supplied scope {1!r}".format(
                    pid, doc.scope.value
                )
            )
        if doc.graph_kind != graph_kind:
            raise ValueError(
                "participant {0!r} supplied a {1!r} graph but fusion was asked for "
                "{2!r}".format(pid, doc.graph_kind, graph_kind)
            )
        docs[pid] = run.align_graph(pid,doc) if isinstance(run,AlignedRunEvidence) else doc

    subject_map = resolve_subjects(assignments)
    groups, align_diagnostics = align_event_records(
        {pid: doc.nodes for pid, doc in docs.items()}, subject_map, cfg, run=run
    )

    node_index: Dict[str, Tuple[str, Event]] = {}
    for pid, doc in docs.items():
        for node in doc.nodes:
            if node.event_id in node_index:
                raise ValueError(
                    "event id {0!r} appears in the local graphs of both {1!r} and "
                    "{2!r}; local ids must be unique per participant".format(
                        node.event_id, node_index[node.event_id][0], pid
                    )
                )
            node_index[node.event_id] = (pid, node)

    fused_nodes, node_map = _merge_nodes(groups, node_index, cfg)
    fused_edges, contradictions, rejected_edges = _merge_edges(docs, node_map, cfg)

    fused = GraphDocument(
        graph_kind=graph_kind,
        scope=Provenance.FUSED,
        owner=None,
        run_id=run.run_id,
        scenario_id=run.scenario_id,
        seed=run.seed,
        nodes=fused_nodes,
        edges=fused_edges,
        meta={},
    )

    enforce = bool(cfg.get("fusion.enforce_dag", graph_kind == "causal"))
    dag_notes: List[str] = []
    if enforce:
        fused, dag_notes = _enforce_dag(fused, cfg, rejected_edges)

    added = _fusion_added(fused, docs, node_map, cfg)
    diagnostics = _build_diagnostics(
        run=run,
        docs=docs,
        groups=groups,
        fused=fused,
        contradictions=contradictions,
        rejected_edges=rejected_edges,
        assignments=assignments,
        align_diagnostics=align_diagnostics,
        added=added,
        dag_notes=dag_notes,
        enforced_dag=enforce,
        cfg=cfg,
        graph_kind=graph_kind,
    )
    fused.meta = {
        "time_domain": "common",
        "time_reference": run.time_alignment["reference"] if run.time_alignment else "synchronized_baseline",
        "fusion": {
            "n_merged_groups": diagnostics["n_merged_groups"],
            "n_contradictions": len(contradictions),
            "n_rejected_edges": len(rejected_edges),
            "confidence_method": str(
                cfg.get("fusion.confidence_fusion.method", "noisy_or")
            ),
            "config_hash": cfg.hash,
            "enforced_dag": enforce,
        }
    }
    diagnostics["unresolved_time_participants"] = unresolved
    diagnostics["unresolved_local_graphs"] = {
        p: {"n_nodes":len(local_docs[p].nodes),"n_edges":len(local_docs[p].edges),
            "status":"UNRESOLVED_TIME_ALIGNMENT","retained":"original local graph; excluded from common-time fusion"}
        for p in unresolved}
    return fused, diagnostics


# ---------------------------------------------------------------------------
# Node merging
# ---------------------------------------------------------------------------


def _merge_nodes(
    groups: Sequence[EventGroup],
    node_index: Mapping[str, Tuple[str, Event]],
    cfg: Config,
) -> Tuple[List[Event], Dict[str, str]]:
    """Collapse each alignment group into one fused :class:`Event`.

    ``node_map`` (local event id -> fused event id) is returned alongside, because
    edge remapping is meaningless without it.
    """
    fused_nodes: List[Event] = []
    node_map: Dict[str, str] = {}

    for group in groups:
        members: List[Event] = []
        for eid in group.members:
            if eid not in node_index:
                raise KeyError(
                    "alignment group references unknown event id {0!r}".format(eid)
                )
            members.append(node_index[eid][1])

        rep = _representative(members, group)
        owners = sorted({o for m in members for o in (m.owners or [m.participant_id])})
        confidences = [float(m.confidence) for m in members]
        confidence = fuse_confidence(confidences, cfg)
        t_peak = _weighted_mean([float(m.t_peak) for m in members], confidences)
        t_start = min(float(m.t_start) for m in members)
        ends = [float(m.t_end) for m in members if m.t_end is not None]
        t_end = max(ends) if ends else None
        subject = _fused_subject(rep, group)

        evidence: List[Evidence] = []
        for m in members:
            evidence.extend(m.evidence)
        for m in members:
            evidence.append(
                Evidence(
                    kind="event",
                    ref=m.event_id,
                    t_start=float(m.t_start),
                    t_end=float(m.t_end) if m.t_end is not None else None,
                    detail={
                        "participant_id": m.participant_id,
                        "event_type": _type_value(m.event_type),
                        "confidence": float(m.confidence),
                        "local_subject": m.subject or "",
                    },
                )
            )

        # The digest of the member set enters the id payload so that two groups
        # that happen to share type, owner, time and subject still receive
        # distinct -- and reproducible -- identifiers.
        subject_for_id = "{0}|{1}".format(
            subject or "-", stable_digest("|".join(sorted(group.members)))[:8]
        )
        fused_id = make_event_id(
            Provenance.FUSED.value,
            rep.participant_id,
            _type_value(rep.event_type),
            t_peak,
            subject_for_id,
        )
        if any(n.event_id == fused_id for n in fused_nodes):
            raise ValueError(
                "fused event id collision for {0!r}; group members: {1}".format(
                    fused_id, ", ".join(group.members)
                )
            )

        fused_nodes.append(
            Event(
                event_id=fused_id,
                event_type=rep.event_type,
                participant_id=rep.participant_id,
                t_start=t_start,
                t_peak=t_peak,
                t_end=t_end,
                subject=subject,
                values=_merge_values(members),
                confidence=confidence,
                evidence=evidence,
                provenance=Provenance.FUSED,
                source_sensors=sorted({s for m in members for s in m.source_sensors}),
                owners=owners,
                merged_from=sorted(group.members),
            )
        )
        for eid in group.members:
            node_map[eid] = fused_id

    fused_nodes.sort(key=lambda n: (n.t_peak, n.event_id))
    return fused_nodes, node_map


def _representative(members: Sequence[Event], group: EventGroup) -> Event:
    """Pick the member whose description of the event is taken as canonical.

    A vehicle's own account of its own behaviour is preferred over another
    vehicle's remote observation of it: the former rests on direct telemetry, the
    latter on a range-rate estimate. Ties are broken by confidence and finally by
    event id, so the choice is deterministic.
    """

    def sort_key(m: Event) -> Tuple[int, float, str]:
        own = 0 if (m.subject in (None, "", "self") and m.participant_id in group.vehicles) else 1
        return (own, -float(m.confidence), m.event_id)

    return sorted(members, key=sort_key)[0]


def _fused_subject(rep: Event, group: EventGroup) -> Optional[str]:
    """Subject of the fused node: a *participant id*, not a local track id.

    A local track id such as ``"A::T007"`` is meaningless outside ``A``'s own log,
    so the fused node names the participant the association stage identified. When
    the subject could not be resolved the original local label is kept verbatim --
    losing it would erase the only pointer back to the supporting evidence.
    """
    if not group.mergeable:
        return rep.subject
    others = [v for v in group.vehicles if v != rep.participant_id]
    if group.relational:
        return others[0] if others else None
    if group.vehicles and group.vehicles[0] != rep.participant_id:
        return group.vehicles[0]
    return None


def _merge_values(members: Sequence[Event]) -> Dict[str, float]:
    """Mean of each numeric measurement across the members that reported it.

    Keys reported by only one participant are kept as that participant's value:
    dropping them would discard a measurement, and imputing a zero would invent
    one.
    """
    buckets: Dict[str, List[float]] = {}
    for m in members:
        for key, value in sorted((m.values or {}).items()):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            buckets.setdefault(str(key), []).append(float(value))
    return {k: (sum(v) / float(len(v))) for k, v in sorted(buckets.items())}


def _weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    """Confidence-weighted mean, degrading to the plain mean at zero weight."""
    total = sum(max(0.0, float(w)) for w in weights)
    if total <= 0.0:
        return float(sum(values)) / float(len(values))
    return float(
        sum(float(v) * max(0.0, float(w)) for v, w in zip(values, weights)) / total
    )


def _type_value(event_type: Any) -> str:
    return event_type.value if isinstance(event_type, EventType) else str(event_type)


# ---------------------------------------------------------------------------
# Edge merging
# ---------------------------------------------------------------------------


def _merge_edges(
    docs: Mapping[str, GraphDocument], node_map: Mapping[str, str], cfg: Config
) -> Tuple[List[GraphEdge], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Remap, combine and (never silently) drop the participants' local edges."""
    keep_contradictions = bool(cfg.get("fusion.conflict.keep_contradictions", True))

    buckets: Dict[Tuple[str, str, str], List[Tuple[str, GraphEdge]]] = {}
    rejected: List[Dict[str, Any]] = []

    for pid in sorted(docs.keys()):
        for edge in docs[pid].edges:
            u = node_map.get(edge.source)
            v = node_map.get(edge.target)
            if u is None or v is None:
                rejected.append(
                    {
                        "reason": "endpoint_not_in_fused_graph",
                        "participant_id": pid,
                        "source": edge.source,
                        "target": edge.target,
                        "edge_type": edge.edge_type,
                        "message": (
                            "edge {0} -> {1} of {2} references an event that is not a "
                            "node of its own local graph".format(
                                edge.source, edge.target, pid
                            )
                        ),
                    }
                )
                continue
            if u == v:
                rejected.append(
                    {
                        "reason": "self_loop_after_merge",
                        "participant_id": pid,
                        "source": edge.source,
                        "target": edge.target,
                        "fused_node": u,
                        "edge_type": edge.edge_type,
                        "message": (
                            "both endpoints of {0} -> {1} merged into the fused node "
                            "{2}; the relation became a self-loop and was dropped".format(
                                edge.source, edge.target, u
                            )
                        ),
                    }
                )
                continue
            buckets.setdefault((u, v, edge.edge_type), []).append((pid, edge))

    # -- detect disagreements before building the surviving edges ----------
    by_pair: Dict[Tuple[str, str], List[str]] = {}
    for (u, v, etype) in buckets:
        by_pair.setdefault((u, v), []).append(etype)

    contradictions: List[Dict[str, Any]] = []
    conflicting_types: Dict[Tuple[str, str], List[str]] = {}
    for pair in sorted(by_pair.keys()):
        types = sorted(set(by_pair[pair]))
        if len(types) > 1:
            conflicting_types[pair] = types
            contradictions.append(
                {
                    "kind": "edge_type_disagreement",
                    "source": pair[0],
                    "target": pair[1],
                    "edge_types": types,
                    "claims": [
                        {
                            "participant_id": pid,
                            "edge_type": e.edge_type,
                            "confidence": float(e.confidence),
                            "rule": e.rule or "",
                        }
                        for etype in types
                        for pid, e in buckets[(pair[0], pair[1], etype)]
                    ],
                    "resolution": "kept_both" if keep_contradictions else "kept_strongest",
                    "message": (
                        "participants assert {0} between the same pair of fused "
                        "nodes".format(" and ".join(types))
                    ),
                }
            )

    for pair in sorted(by_pair.keys()):
        reverse = (pair[1], pair[0])
        if reverse in by_pair and pair < reverse:
            contradictions.append(
                {
                    "kind": "direction_disagreement",
                    "source": pair[0],
                    "target": pair[1],
                    "edge_types": sorted(set(by_pair[pair])),
                    "reverse_edge_types": sorted(set(by_pair[reverse])),
                    "resolution": "kept_both",
                    "message": (
                        "one participant asserts {0} -> {1} while another asserts the "
                        "reverse; both are kept and the cycle is resolved by the DAG "
                        "stage".format(pair[0], pair[1])
                    ),
                }
            )

    fused_edges: List[GraphEdge] = []
    for key in sorted(buckets.keys()):
        u, v, etype = key
        contributors = buckets[key]
        strongest = max(contributors, key=lambda pe: (float(pe[1].confidence), pe[0]))[1]

        source_edges = [
            {
                "participant_id": pid,
                "source": e.source,
                "target": e.target,
                "edge_type": e.edge_type,
                "confidence": float(e.confidence),
                "rule": e.rule or "",
                "temporal_relation": e.temporal_relation or "",
            }
            for pid, e in contributors
        ]
        detail: Dict[str, Any] = {
            "n_contributors": len(contributors),
            "contributing_participants": sorted({pid for pid, _ in contributors}),
            "source_edges": source_edges,
            "rules": sorted({e.rule for _pid, e in contributors if e.rule}),
        }
        if (u, v) in conflicting_types:
            detail["contradiction"] = {
                "competing_edge_types": [
                    t for t in conflicting_types[(u, v)] if t != etype
                ],
                "note": (
                    "another participant asserted a different relation between the "
                    "same pair of fused nodes; both claims are retained"
                ),
            }

        evidence: List[Evidence] = []
        for pid, e in contributors:
            evidence.extend(e.evidence)

        fused_edges.append(
            GraphEdge(
                source=u,
                target=v,
                edge_type=etype,
                confidence=fuse_confidence(
                    [float(e.confidence) for _pid, e in contributors], cfg
                ),
                provenance=Provenance.FUSED,
                rule=strongest.rule,
                temporal_relation=strongest.temporal_relation,
                evidence=evidence,
                owners=sorted(
                    {o for pid, e in contributors for o in (e.owners or [pid])}
                ),
                merged_from=sorted(
                    "{0}|{1}->{2}|{3}".format(pid, e.source, e.target, e.edge_type)
                    for pid, e in contributors
                ),
                detail=detail,
            )
        )

    if not keep_contradictions:
        fused_edges, dropped = _drop_weaker_claims(fused_edges, conflicting_types)
        rejected.extend(dropped)

    return fused_edges, contradictions, rejected


def _drop_weaker_claims(
    edges: Sequence[GraphEdge], conflicting_types: Mapping[Tuple[str, str], Sequence[str]]
) -> Tuple[List[GraphEdge], List[Dict[str, Any]]]:
    """Keep only the strongest edge type per pair (``keep_contradictions: false``).

    This is *not* the default and the discarded claims are still reported: the
    configuration can ask fusion to adjudicate, but never to forget.
    """
    keep: List[GraphEdge] = []
    dropped: List[Dict[str, Any]] = []
    best: Dict[Tuple[str, str], GraphEdge] = {}
    for e in edges:
        pair = (e.source, e.target)
        if pair not in conflicting_types:
            keep.append(e)
            continue
        current = best.get(pair)
        if current is None or (float(e.confidence), e.edge_type) > (
            float(current.confidence),
            current.edge_type,
        ):
            if current is not None:
                dropped.append(_dropped_record(current, "contradiction_adjudicated"))
            best[pair] = e
        else:
            dropped.append(_dropped_record(e, "contradiction_adjudicated"))
    keep.extend(best[p] for p in sorted(best.keys()))
    keep.sort(key=lambda e: (e.source, e.target, e.edge_type))
    return keep, dropped


def _dropped_record(edge: GraphEdge, reason: str) -> Dict[str, Any]:
    return {
        "reason": reason,
        "source": edge.source,
        "target": edge.target,
        "edge_type": edge.edge_type,
        "confidence": float(edge.confidence),
        "merged_from": list(edge.merged_from),
        "message": (
            "edge {0} -> {1} ({2}) was removed by the {3} stage".format(
                edge.source, edge.target, edge.edge_type, reason
            )
        ),
    }


# ---------------------------------------------------------------------------
# Acyclicity
# ---------------------------------------------------------------------------


def _enforce_dag(
    doc: GraphDocument, cfg: Config, rejected: List[Dict[str, Any]]
) -> Tuple[GraphDocument, List[str]]:
    """Make the fused graph acyclic without discarding a retained contradiction.

    The cycle-breaking *policy* is not reinvented here:
    :func:`cdf.local.causal_graph.enforce_dag` decides which edges survive, so a
    fused DAG is constrained exactly like a local one. It is applied to a reduced
    view of the graph in which each ordered node pair is represented by its
    strongest edge, because that routine -- correctly, for a single participant's
    graph -- keeps only one edge per ordered pair, whereas fusion is required to
    keep every competing claim between the same pair. Deciding acyclicity on the
    reduced view and then reinstating all edges of every surviving pair yields
    both properties at once: the shared policy, and no silently dropped claim.

    Every edge of a rejected pair is recorded in ``rejected`` together with the
    reason the policy gave for it.
    """
    notes: List[str] = []
    reduced = _with_edges(doc, _pair_representatives(doc))

    delegated = _delegate_enforce_dag(reduced, cfg, notes)
    if delegated is None:
        kept_doc, reasons = _greedy_acyclic(reduced)
        notes.append("acyclicity enforced by the fusion-local fallback")
    else:
        kept_doc, reasons = delegated

    kept_pairs = {(e.source, e.target) for e in kept_doc.edges}
    surviving: List[GraphEdge] = []
    for edge in doc.edges:
        pair = (edge.source, edge.target)
        if pair in kept_pairs:
            surviving.append(edge)
            continue
        record = _dropped_record(edge, "cycle_broken")
        record["policy_reason"] = reasons.get(
            pair, "removed to keep the fused graph acyclic"
        )
        rejected.append(record)
    doc = _with_edges(doc, surviving)

    if not _is_acyclic(doc):
        # Defensive: an acyclicity policy that returned a cyclic result must not
        # be able to publish a cyclic causal graph.
        notes.append(
            "the acyclicity policy left a cycle; the fusion-local fallback removed "
            "the weakest remaining edges"
        )
        doc = _break_cycles(doc, rejected)
    return doc, notes


def _pair_representatives(doc: GraphDocument) -> List[GraphEdge]:
    """One edge per ordered node pair: the best-supported of the competing claims."""
    best: Dict[Tuple[str, str], GraphEdge] = {}
    for edge in doc.edges:
        pair = (edge.source, edge.target)
        current = best.get(pair)
        if current is None or (float(edge.confidence), edge.edge_type) > (
            float(current.confidence),
            current.edge_type,
        ):
            best[pair] = edge
    return [best[p] for p in sorted(best.keys())]


def _delegate_enforce_dag(
    doc: GraphDocument, cfg: Config, notes: List[str]
) -> Optional[Tuple[GraphDocument, Dict[Tuple[str, str], str]]]:
    """Call ``cdf.local.causal_graph.enforce_dag`` when it is usable.

    The signature is inspected rather than assumed: the local module is developed
    independently of this one, and calling it with the wrong arity would be a
    crash instead of a diagnostic. An unusable signature or an uninterpretable
    return value declines delegation and says so in the diagnostics, so the
    artifact always records which code shaped the graph.
    """
    try:
        from ..local.causal_graph import enforce_dag  # type: ignore
    except ImportError as exc:
        notes.append("cdf.local.causal_graph.enforce_dag is unavailable ({0})".format(exc))
        return None

    params = [
        p
        for p in inspect.signature(enforce_dag).parameters.values()
        if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]
    required = [p for p in params if p.default is inspect.Parameter.empty]
    if not params or len(required) > 2:
        notes.append(
            "cdf.local.causal_graph.enforce_dag has an incompatible signature "
            "({0} required positional parameters)".format(len(required))
        )
        return None

    args: List[Any] = [doc]
    if len(required) == 2:
        args.append(cfg)
    coerced = _coerce_dag_result(enforce_dag(*args), doc)
    if coerced is None:
        notes.append(
            "cdf.local.causal_graph.enforce_dag returned a value fusion cannot interpret"
        )
        return None
    notes.append("acyclicity enforced by cdf.local.causal_graph.enforce_dag")
    return coerced


def _coerce_dag_result(
    result: Any, original: GraphDocument
) -> Optional[Tuple[GraphDocument, Dict[Tuple[str, str], str]]]:
    """Interpret the delegated routine's return value.

    A document, a ``(document, rejections)`` pair, a NetworkX graph or a plain
    edge list are all accepted: the shared routine's exact return shape is its own
    business, and what fusion needs from it is only which edges survived and, when
    offered, why the others did not.
    """
    doc: Optional[GraphDocument] = None
    reasons: Dict[Tuple[str, str], str] = {}

    if isinstance(result, GraphDocument):
        doc = result
    elif isinstance(result, nx.DiGraph):
        from ..graph.export import from_networkx

        doc = from_networkx(result, graph_kind=original.graph_kind, scope=original.scope)
    elif isinstance(result, (list, tuple)):
        for item in result:
            if isinstance(item, GraphDocument):
                doc = item
            elif isinstance(item, nx.DiGraph):
                from ..graph.export import from_networkx

                doc = from_networkx(
                    item, graph_kind=original.graph_kind, scope=original.scope
                )
            elif isinstance(item, (list, tuple)):
                reasons.update(_reasons_from(item))
        if doc is None and result and all(isinstance(i, GraphEdge) for i in result):
            doc = _with_edges(original, list(result))

    if doc is None:
        return None
    return doc, reasons


def _reasons_from(items: Sequence[Any]) -> Dict[Tuple[str, str], str]:
    """Extract ``(source, target) -> reason`` from a rejection list, if it is one."""
    out: Dict[Tuple[str, str], str] = {}
    for item in items:
        if isinstance(item, Mapping) and "source" in item and "target" in item:
            out[(str(item["source"]), str(item["target"]))] = str(
                item.get("reason", "rejected by the acyclicity policy")
            )
    return out


def _greedy_acyclic(
    doc: GraphDocument,
) -> Tuple[GraphDocument, Dict[Tuple[str, str], str]]:
    """Fallback policy: accept edges strongest-first and skip the cycle closers.

    It mirrors the policy of :func:`cdf.local.causal_graph.enforce_dag` so that a
    run produced without that module stays comparable with one produced with it.
    It exists only so that fusion cannot be blocked by an unavailable sibling.
    """
    ordered = sorted(
        doc.edges,
        key=lambda e: (-float(e.confidence), str(e.source), str(e.target), str(e.edge_type)),
    )
    g = nx.DiGraph()
    g.add_nodes_from(n.event_id for n in doc.nodes)
    kept: List[GraphEdge] = []
    reasons: Dict[Tuple[str, str], str] = {}
    for edge in ordered:
        if edge.source == edge.target:
            reasons[(edge.source, edge.target)] = "self loop: an event cannot cause itself"
            continue
        if nx.has_path(g, edge.target, edge.source):
            reasons[(edge.source, edge.target)] = (
                "would close a cycle: {0} already reaches {1} through better "
                "supported edges".format(edge.target, edge.source)
            )
            continue
        g.add_edge(edge.source, edge.target)
        kept.append(edge)
    return _with_edges(doc, kept), reasons


def _with_edges(doc: GraphDocument, edges: List[GraphEdge]) -> GraphDocument:
    """Copy of ``doc`` carrying a different edge list."""
    return GraphDocument(
        graph_kind=doc.graph_kind,
        scope=doc.scope,
        owner=doc.owner,
        run_id=doc.run_id,
        scenario_id=doc.scenario_id,
        seed=doc.seed,
        nodes=list(doc.nodes),
        edges=edges,
        meta=dict(doc.meta),
    )


def _is_acyclic(doc: GraphDocument) -> bool:
    return nx.is_directed_acyclic_graph(_structure(doc))


def _structure(doc: GraphDocument) -> nx.DiGraph:
    """Plain structural view: nodes and remapped edges, no payloads.

    Built here rather than with :func:`cdf.graph.export.to_networkx` because that
    helper collapses parallel edges of different types, which is fine for analysis
    but would hide a retained contradiction from the cycle search.
    """
    g = nx.DiGraph()
    for n in doc.nodes:
        g.add_node(n.event_id)
    for e in doc.edges:
        g.add_edge(e.source, e.target)
    return g


def _break_cycles(doc: GraphDocument, rejected: List[Dict[str, Any]]) -> GraphDocument:
    """Last-resort cycle removal: drop the weakest pair of every remaining cycle.

    Only reached when an acyclicity policy returned a cyclic graph, which would be
    a bug in that policy; the fused artifact must be a DAG regardless, and every
    edge removed here is recorded like any other rejection.
    """
    edges = list(doc.edges)
    guard = len(edges) + 1
    while guard >= 0:
        guard -= 1
        g = nx.DiGraph()
        for n in doc.nodes:
            g.add_node(n.event_id)
        for e in edges:
            g.add_edge(e.source, e.target)
        try:
            cycle = nx.find_cycle(g)
        except nx.NetworkXNoCycle:
            break

        pairs = [(str(item[0]), str(item[1])) for item in cycle]
        strength = {
            p: max(
                float(e.confidence) for e in edges if (e.source, e.target) == p
            )
            for p in pairs
        }
        victim = sorted(pairs, key=lambda p: (strength[p], p[0], p[1]))[0]
        for e in [e for e in edges if (e.source, e.target) == victim]:
            rejected.append(_dropped_record(e, "cycle_broken"))
        edges = [e for e in edges if (e.source, e.target) != victim]
    else:
        raise RuntimeError(
            "cycle removal did not terminate; the fused graph structure is inconsistent"
        )

    return _with_edges(doc, edges)


# ---------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------


def _fusion_added(
    fused: GraphDocument,
    docs: Mapping[str, GraphDocument],
    node_map: Mapping[str, str],
    cfg: Config,
) -> Dict[str, Any]:
    """What exists in the fused graph but in no single participant's graph.

    * A node is *added* when its evidence comes from more than one participant:
      no local graph contains that node, because no participant saw both sides.
    * An edge is *added* when it touches such a node: its endpoint does not exist
      in any local graph, so neither can the edge.
    * A *bridged path* is a reachability pair present in the fused graph and in no
      participant's own (remapped) subgraph -- the concrete payoff of fusion: a
      cause recorded by one vehicle now reaches an outcome recorded by another.
    """
    added_nodes = sorted(n.event_id for n in fused.nodes if len(set(n.owners)) > 1)
    added_set = set(added_nodes)
    added_edges = [
        {"source": e.source, "target": e.target, "edge_type": e.edge_type}
        for e in fused.edges
        if e.source in added_set or e.target in added_set
    ]

    fused_g = _structure(fused)
    local_reach: Set[Tuple[str, str]] = set()
    for pid, doc in sorted(docs.items()):
        sub = nx.DiGraph()
        for n in doc.nodes:
            mapped = node_map.get(n.event_id)
            if mapped is not None:
                sub.add_node(mapped)
        for e in doc.edges:
            u, v = node_map.get(e.source), node_map.get(e.target)
            if u is not None and v is not None and u != v:
                sub.add_edge(u, v)
        for n in sub.nodes():
            for d in nx.descendants(sub, n):
                local_reach.add((str(n), str(d)))

    bridged: List[Tuple[str, str]] = []
    for n in fused_g.nodes():
        for d in nx.descendants(fused_g, n):
            pair = (str(n), str(d))
            if pair not in local_reach:
                bridged.append(pair)
    bridged.sort()

    # The number of new reachability pairs grows quadratically with the graph, so
    # the listing is capped; the count is always reported in full.
    cap = int(cfg.get("fusion.diagnostics.max_bridged_paths", 200))
    return {
        "criterion": (
            "a node is added when its owners span more than one participant; an "
            "edge is added when it touches such a node; a bridged path is a "
            "reachability pair no single participant's graph contains"
        ),
        "nodes": added_nodes,
        "edges": sorted(added_edges, key=lambda d: (d["source"], d["target"], d["edge_type"])),
        "n_bridged_paths": len(bridged),
        "bridged_paths_truncated": len(bridged) > cap,
        "bridged_paths": [{"source": u, "target": v} for u, v in bridged[:cap]],
    }


def _build_diagnostics(
    run: RunEvidence,
    docs: Mapping[str, GraphDocument],
    groups: Sequence[EventGroup],
    fused: GraphDocument,
    contradictions: Sequence[Dict[str, Any]],
    rejected_edges: Sequence[Dict[str, Any]],
    assignments: Mapping[str, TrackAssignment],
    align_diagnostics: Sequence[Dict[str, Any]],
    added: Dict[str, Any],
    dag_notes: Sequence[str],
    enforced_dag: bool,
    cfg: Config,
    graph_kind: str,
) -> Dict[str, Any]:
    """Assemble the serialisable fusion diagnostics block."""
    unresolved = [
        {
            "track_id": assignments[t].track_id,
            "observer_id": assignments[t].observer_id,
            "overlap_s": float(assignments[t].overlap_s),
            "rmse_m": assignments[t].rmse_m,
            "confidence": float(assignments[t].confidence),
            "reason": assignments[t].reason,
        }
        for t in sorted(assignments.keys())
        if assignments[t].status == STATUS_UNRESOLVED
    ]

    merged_groups = [g for g in groups if g.size > 1]
    return {
        "schema_version": SCHEMA_VERSIONS["fusion_diagnostics"],
        "run_id": run.run_id,
        "scenario_id": run.scenario_id,
        "graph_kind": graph_kind,
        "config_hash": cfg.hash,
        "participants": sorted(docs.keys()),
        "n_input_nodes": {pid: len(doc.nodes) for pid, doc in sorted(docs.items())},
        "n_input_edges": {pid: len(doc.edges) for pid, doc in sorted(docs.items())},
        "n_alignment_groups": len(groups),
        "n_merged_groups": len(merged_groups),
        "n_fused_nodes": len(fused.nodes),
        "n_fused_edges": len(fused.edges),
        "merged_groups": [
            {
                "family": g.family,
                "vehicles": list(g.vehicles),
                "members": list(g.members),
                "t_peak_spread_s": float(g.t_peak_max - g.t_peak_min),
            }
            for g in merged_groups
        ],
        "contradictions": list(contradictions),
        "rejected_edges": list(rejected_edges),
        "unresolved_tracks": unresolved,
        "fusion_added": added,
        "alignment_diagnostics": list(align_diagnostics),
        "confidence_fusion": {
            "method": str(cfg.get("fusion.confidence_fusion.method", "noisy_or")),
            "cap": float(cfg.get("fusion.confidence_fusion.cap", 0.99)),
        },
        "dag": {
            "enforced": bool(enforced_dag),
            "is_dag": _is_acyclic(fused),
            "notes": list(dag_notes),
        },
    }
