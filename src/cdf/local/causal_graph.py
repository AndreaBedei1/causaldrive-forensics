"""Local causal DAG: the hypotheses one vehicle can defend from its own evidence.

Construction is deliberately boring, and that is the point. Every edge is
proposed by exactly one named rule from :mod:`cdf.local.causal_rules`, is
accepted only when the observed timing and subject constraints of that rule hold,
carries a confidence computed by one published formula, and points back at the
two events it relates. Nothing here inspects a scenario id, a participant role or
any privileged quantity: the same code runs identically on every vehicle in every
run.

Confidence
----------
For a rule ``r`` firing on a cause ``c`` and an effect ``e`` separated by
``lag = e.t_peak - c.t_peak``::

    node_factor     = w * mean(c.confidence, e.confidence) + (1 - w)
    temporal_factor = exp(-|lag| / tau)
    confidence      = r.prior * node_factor * temporal_factor

with ``w = causal_rules.confidence.node_weight`` and
``tau = causal_rules.confidence.temporal_decay_s``. The three terms answer three
different questions -- how plausible is the rule at all, how solid is the
underlying detection, and how tightly did the two events actually follow each
other -- and each is stored on the edge so that a surprising number can be traced
to the term that produced it. ``w`` interpolates between "trust the rule" and
"trust the detector": at ``w = 0`` node confidence is ignored entirely.

The absolute value is the one documented refinement of the specified
``exp(-lag / tau)``, and it matters only inside the small negative band that
``causal_rules.min_lag_s`` tolerates for sampling jitter. For the ordinary case
``lag >= 0`` the two formulas are identical. For a negative lag the literal
formula would return a factor *greater than one* and inflate the edge above its
rule prior; merely clamping the lag at zero fixes that but introduces a subtler
error in its place, because every time-reversed pair would then score a flat
``1.0`` -- strictly better than any correctly ordered pair, however tight. Two
mirror-image rules (``own_lateral_manoeuvre_creates_conflict`` and
``lateral_threat_triggers_evasive_steering``) compete for exactly such pairs, and
the observed ordering is the only evidence that can separate them, so it must not
be thrown away. Decaying symmetrically keeps the factor bounded by one *and*
keeps a tighter observed coupling ahead of a looser one in either direction.

Acyclicity
----------
The rule table is intentionally not a DAG over event *types*: a steering input can
create a conflict and a conflict can provoke a steering input, and which of the
two happened is exactly what a reconstruction is supposed to decide. On concrete
events the observed ordering usually settles it, but jitter tolerance and
repeated events can still close a loop. :func:`enforce_dag` resolves that by
greedily accepting edges from strongest to weakest and rejecting any edge that
would close a cycle -- the weakest link in a contradictory loop loses -- and by
recording every rejection with a reason, so a suppressed hypothesis remains
visible in ``meta["rejected_edges"]`` instead of vanishing.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, Tuple

import networkx as nx

from ..common.config import Config
from ..common.evidence import ParticipantEvidence
from ..common.schemas import (
    Event,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
    to_jsonable,
)
from ..common.timeline import temporal_relation
from ..graph.export import to_networkx
from .causal_rules import CausalRule, load_rules
from .event_graph import event_interval, subject_key, validated_local_nodes

__all__ = [
    "MAX_JITTER_TOLERANCE_S",
    "confidence_terms",
    "propose_edges",
    "enforce_dag",
    "build_causal_graph",
]


#: Largest magnitude a negative ``causal_rules.min_lag_s`` may have.
#:
#: A negative minimum lag exists to absorb the fact that two event extractors
#: sampling the same tick can order their peaks by a few milliseconds either way.
#: It is *not* a licence for backwards causation: the project's stated contract is
#: that an effect occurring before its cause produces no edge, and a generously
#: negative value in a configuration file would quietly repeal that contract for
#: every rule at once. Half a second is already an order of magnitude more than
#: any plausible extractor jitter at a 20 Hz tick, so anything beyond it is a
#: configuration error and is refused rather than honoured.
MAX_JITTER_TOLERANCE_S: float = 0.5


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------


def confidence_terms(
    rule: CausalRule,
    cause: Event,
    effect: Event,
    lag_s: float,
    node_weight: float,
    temporal_decay_s: float,
) -> Dict[str, float]:
    """The three confidence terms and their product, as documented in the module.

    Returned as a mapping rather than a bare float so that the terms can be
    attached to the edge: an auditor should be able to see *why* an edge is weak
    (an uncertain detection, or a long delay) without recomputing anything.
    """
    if not 0.0 <= float(node_weight) <= 1.0:
        raise ValueError(
            "causal_rules.confidence.node_weight must lie in [0, 1], got {0!r}".format(
                node_weight
            )
        )
    if float(temporal_decay_s) <= 0.0:
        raise ValueError(
            "causal_rules.confidence.temporal_decay_s must be positive, got "
            "{0!r}".format(temporal_decay_s)
        )
    node_mean = 0.5 * (float(cause.confidence) + float(effect.confidence))
    node_factor = float(node_weight) * node_mean + (1.0 - float(node_weight))
    # Symmetric decay: identical to the published exp(-lag/tau) for lag >= 0, and
    # inside the tolerated negative jitter band it neither inflates the edge above
    # the rule prior nor rewards a time-reversed pair for running backwards.
    temporal_factor = math.exp(-abs(float(lag_s)) / float(temporal_decay_s))
    confidence = float(rule.prior) * node_factor * temporal_factor
    return {
        "rule_prior": float(rule.prior),
        "node_factor": node_factor,
        "temporal_factor": temporal_factor,
        "confidence": max(0.0, min(1.0, confidence)),
    }


# ---------------------------------------------------------------------------
# Rule application
# ---------------------------------------------------------------------------


def _rule_applies(rule: CausalRule, cause: Event, effect: Event) -> bool:
    """Whether the subject constraints of ``rule`` hold for this event pair."""
    if rule.require_same_subject:
        cause_subject = subject_key(cause)
        effect_subject = subject_key(effect)
        if cause_subject is None or effect_subject is None:
            return False
        if cause_subject != effect_subject:
            return False
    if rule.require_self_effect and subject_key(effect) is not None:
        return False
    return True


def propose_edges(
    nodes: Sequence[Event],
    rules: Sequence[CausalRule],
    owner: str,
    min_lag_s: float,
    node_weight: float,
    temporal_decay_s: float,
    min_edge_confidence: float,
    relation_tolerance_s: float,
) -> Tuple[List[GraphEdge], Dict[str, int]]:
    """Fire every rule over every ordered event pair and return the surviving edges.

    At most one edge is kept per ordered node pair: when several rules explain the
    same pair, the strongest hypothesis becomes the edge and the others are listed
    in its ``detail["alternatives"]``. Keeping both as parallel edges would make
    the document ambiguous about which claim the graph actually asserts, while
    dropping the alternatives silently would hide competing explanations.

    Returns the edges plus a small counter dictionary for the graph ``meta``.
    """
    stats = {"n_pairs_tested": 0, "n_candidates": 0, "n_below_min_confidence": 0}
    best: Dict[Tuple[str, str], GraphEdge] = {}

    for rule in rules:
        for cause in nodes:
            if not rule.matches_cause(cause.event_type):
                continue
            for effect in nodes:
                if effect.event_id == cause.event_id:
                    continue
                if not rule.matches_effect(effect.event_type):
                    continue
                stats["n_pairs_tested"] += 1
                lag = float(effect.t_peak) - float(cause.t_peak)
                if lag < float(min_lag_s) or lag > float(rule.max_lag_s):
                    continue
                if not _rule_applies(rule, cause, effect):
                    continue

                terms = confidence_terms(
                    rule, cause, effect, lag, node_weight, temporal_decay_s
                )
                stats["n_candidates"] += 1
                if terms["confidence"] < float(min_edge_confidence):
                    stats["n_below_min_confidence"] += 1
                    continue

                edge = _causal_edge(
                    rule, cause, effect, lag, terms, owner, relation_tolerance_s
                )
                key = (edge.source, edge.target)
                incumbent = best.get(key)
                if incumbent is None:
                    best[key] = edge
                elif edge.confidence > incumbent.confidence:
                    edge.detail["alternatives"] = list(
                        incumbent.detail.get("alternatives", [])
                    ) + [_alternative(incumbent)]
                    best[key] = edge
                else:
                    incumbent.detail.setdefault("alternatives", []).append(
                        _alternative(edge)
                    )

    edges = sorted(best.values(), key=lambda e: (e.source, e.target, e.edge_type))
    for edge in edges:
        alternatives = edge.detail.get("alternatives")
        if alternatives:
            edge.detail["alternatives"] = sorted(
                alternatives, key=lambda a: (-float(a["confidence"]), str(a["rule"]))
            )
    return edges, stats


def _alternative(edge: GraphEdge) -> Dict[str, Any]:
    """Compact record of a rule that explained the same pair less strongly."""
    return {
        "rule": edge.rule,
        "edge_type": edge.edge_type,
        "confidence": float(edge.confidence),
    }


def _causal_edge(
    rule: CausalRule,
    cause: Event,
    effect: Event,
    lag_s: float,
    terms: Dict[str, float],
    owner: str,
    relation_tolerance_s: float,
) -> GraphEdge:
    """Assemble one causal edge together with its justification."""
    cause_interval = event_interval(cause)
    effect_interval = event_interval(effect)
    relation = temporal_relation(
        cause_interval, effect_interval, tol=float(relation_tolerance_s)
    )
    detail: Dict[str, Any] = {
        "lag_s": round(float(lag_s), 6),
        "max_lag_s": float(rule.max_lag_s),
        "rule_prior": terms["rule_prior"],
        "node_factor": round(terms["node_factor"], 6),
        "temporal_factor": round(terms["temporal_factor"], 6),
        "rule_description": rule.description,
        "require_same_subject": bool(rule.require_same_subject),
        "require_self_effect": bool(rule.require_self_effect),
    }
    cause_subject = subject_key(cause)
    if cause_subject is not None:
        detail["cause_track"] = cause_subject
    effect_subject = subject_key(effect)
    if effect_subject is not None:
        detail["effect_track"] = effect_subject

    return GraphEdge(
        source=cause.event_id,
        target=effect.event_id,
        edge_type=rule.edge_type,
        confidence=float(terms["confidence"]),
        provenance=Provenance.LOCAL,
        rule=rule.name,
        temporal_relation=relation,
        evidence=[
            Evidence(
                kind="event",
                ref=cause.event_id,
                t_start=cause_interval.start,
                t_end=cause_interval.end,
                detail={"part": "cause", "event_type": cause.event_type.value},
            ),
            Evidence(
                kind="event",
                ref=effect.event_id,
                t_start=effect_interval.start,
                t_end=effect_interval.end,
                detail={"part": "effect", "event_type": effect.event_type.value},
            ),
        ],
        owners=[owner],
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Acyclicity
# ---------------------------------------------------------------------------


def enforce_dag(doc: GraphDocument) -> Tuple[GraphDocument, List[Dict[str, Any]]]:
    """Return an acyclic copy of ``doc`` plus the diagnostics of what was dropped.

    Edges are considered in descending confidence (ties broken deterministically
    by endpoints and type) and added one at a time; an edge whose target can
    already reach its source would close a cycle and is rejected instead. Greedy
    insertion in confidence order is the standard approximation to the maximum
    acyclic subgraph problem, and it has the property we care about forensically:
    the claim that survives a contradiction is the best-supported one.

    Each rejection is reported as ``{source, target, edge_type, rule, confidence,
    reason}``. The returned document always satisfies
    :func:`networkx.is_directed_acyclic_graph`.
    """
    node_ids = set(doc.node_ids())
    graph = nx.DiGraph()
    graph.add_nodes_from(sorted(node_ids))

    ordered = sorted(
        doc.edges,
        key=lambda e: (-float(e.confidence), str(e.source), str(e.target), str(e.edge_type)),
    )

    accepted: List[GraphEdge] = []
    rejected: List[Dict[str, Any]] = []
    for edge in ordered:
        if edge.source not in node_ids or edge.target not in node_ids:
            raise ValueError(
                "edge {0}->{1} ({2}) references an event that is not a node of the "
                "document; the graph is inconsistent".format(
                    edge.source, edge.target, edge.edge_type
                )
            )
        if edge.source == edge.target:
            rejected.append(_rejection(edge, "self loop: an event cannot cause itself"))
            continue
        if graph.has_edge(edge.source, edge.target):
            # A stronger edge already occupies this ordered pair; keeping both
            # would make the document ambiguous.
            rejected.append(
                _rejection(
                    edge,
                    "a stronger edge already connects this ordered pair",
                )
            )
            continue
        if nx.has_path(graph, edge.target, edge.source):
            rejected.append(
                _rejection(
                    edge,
                    "would close a cycle: {0} already reaches {1} through accepted, "
                    "more strongly supported edges".format(edge.target, edge.source),
                )
            )
            continue
        graph.add_edge(edge.source, edge.target)
        accepted.append(edge)

    accepted.sort(key=lambda e: (str(e.source), str(e.target), str(e.edge_type)))
    out = GraphDocument(
        graph_kind=doc.graph_kind,
        scope=doc.scope,
        owner=doc.owner,
        run_id=doc.run_id,
        scenario_id=doc.scenario_id,
        seed=doc.seed,
        nodes=list(doc.nodes),
        edges=accepted,
        meta=dict(doc.meta),
        schema_version=doc.schema_version,
    )
    return out, rejected


def _rejection(edge: GraphEdge, reason: str) -> Dict[str, Any]:
    return {
        "source": edge.source,
        "target": edge.target,
        "edge_type": edge.edge_type,
        "rule": edge.rule,
        "confidence": float(edge.confidence),
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def build_causal_graph(
    events: Sequence[Event],
    ev: ParticipantEvidence,
    cfg: Config,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> GraphDocument:
    """Build one participant's local causal DAG from its own events.

    Parameters
    ----------
    events:
        The participant's local events; they become the nodes unchanged. Nodes
        are kept even when no rule fires on them, because "this was observed and
        explains nothing" is itself a finding.
    ev:
        The same participant's evidence bundle; supplies the owner id and is the
        boundary against which every event's ``participant_id`` is checked.
    cfg:
        Threshold registry. Keys read: ``causal_rules.min_lag_s``,
        ``causal_rules.min_edge_confidence``,
        ``causal_rules.confidence.node_weight``,
        ``causal_rules.confidence.temporal_decay_s`` (plus everything
        :func:`~cdf.local.causal_rules.load_rules` reads) and
        ``simulation.fixed_delta_seconds`` as the temporal-relation tolerance.

    Returns
    -------
    GraphDocument
        ``graph_kind="causal"``, ``scope=LOCAL``, ``owner=ev.participant_id``,
        guaranteed acyclic, with the rejected-edge diagnostics in
        ``meta["rejected_edges"]`` and the rule table actually used in
        ``meta["rules"]``.
    """
    nodes = validated_local_nodes(events, ev.participant_id)
    rules = load_rules(cfg)

    min_lag_s = float(cfg.get("causal_rules.min_lag_s", -0.15))
    min_edge_confidence = float(cfg.get("causal_rules.min_edge_confidence", 0.25))
    node_weight = float(cfg.get("causal_rules.confidence.node_weight", 0.6))
    temporal_decay_s = float(cfg.get("causal_rules.confidence.temporal_decay_s", 3.0))
    relation_tolerance_s = float(cfg.get("simulation.fixed_delta_seconds", 0.05))

    # Validate every parameter here, before any pair is examined. The confidence
    # terms are also checked where they are used, but that check only fires once a
    # candidate pair exists: a trace that happens to produce none would otherwise
    # accept a nonsensical configuration in silence and stamp it into meta, which
    # is precisely the kind of unnoticed difference between two runs that this
    # pipeline exists to rule out.
    if not 0.0 <= min_edge_confidence <= 1.0:
        raise ValueError(
            "causal_rules.min_edge_confidence must lie in [0, 1], got {0!r}".format(
                min_edge_confidence
            )
        )
    if not 0.0 <= node_weight <= 1.0:
        raise ValueError(
            "causal_rules.confidence.node_weight must lie in [0, 1], got {0!r}".format(
                node_weight
            )
        )
    if temporal_decay_s <= 0.0:
        raise ValueError(
            "causal_rules.confidence.temporal_decay_s must be positive, got "
            "{0!r}".format(temporal_decay_s)
        )
    if min_lag_s < -MAX_JITTER_TOLERANCE_S:
        raise ValueError(
            "causal_rules.min_lag_s is {0!r}, which would accept an effect "
            "occurring up to {1:.2f}s before its cause. That value is a "
            "sampling-jitter tolerance, not a backwards-causation switch; it may "
            "not be more negative than -{2}s".format(
                min_lag_s, abs(min_lag_s), MAX_JITTER_TOLERANCE_S
            )
        )

    edges, stats = propose_edges(
        nodes=nodes,
        rules=rules,
        owner=ev.participant_id,
        min_lag_s=min_lag_s,
        node_weight=node_weight,
        temporal_decay_s=temporal_decay_s,
        min_edge_confidence=min_edge_confidence,
        relation_tolerance_s=relation_tolerance_s,
    )

    meta: Dict[str, Any] = {
        "note": (
            "every edge is a hypothesis proposed by one named rule, not an "
            "established fact; see meta['rules'] for the table that produced them"
        ),
        "n_nodes": len(nodes),
        "parameters": {
            "min_lag_s": min_lag_s,
            "min_edge_confidence": min_edge_confidence,
            "node_weight": node_weight,
            "temporal_decay_s": temporal_decay_s,
            "relation_tolerance_s": relation_tolerance_s,
        },
        "rule_statistics": stats,
        "rules": [to_jsonable(rule) for rule in rules],
    }

    doc = GraphDocument(
        graph_kind="causal",
        scope=Provenance.LOCAL,
        owner=ev.participant_id,
        run_id=run_id,
        scenario_id=scenario_id,
        seed=int(seed),
        nodes=nodes,
        edges=edges,
        meta=meta,
    )

    acyclic, rejected = enforce_dag(doc)
    acyclic.meta["rejected_edges"] = rejected
    counts: Dict[str, int] = {}
    for edge in acyclic.edges:
        counts[edge.edge_type] = counts.get(edge.edge_type, 0) + 1
    acyclic.meta["edge_counts"] = dict(sorted(counts.items()))

    # Cheap belt-and-braces check: the contract of this function is an acyclic
    # document, and a regression here would silently poison every downstream
    # analysis, so it is verified rather than assumed.
    if not nx.is_directed_acyclic_graph(to_networkx(acyclic)):
        raise AssertionError(
            "causal graph for participant {0!r} is cyclic after enforce_dag".format(
                ev.participant_id
            )
        )
    return acyclic
