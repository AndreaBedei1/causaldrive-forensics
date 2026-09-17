"""Privileged event graph and causal DAG -- the reference the pipeline is scored against.

PRIVILEGED LAYER -- EVALUATION ONLY.

Where the oracle's causal structure comes from
----------------------------------------------
Not from the local rule engine. :mod:`cdf.local.causal_rules` proposes edges by
pattern-matching observable events against a table of hypotheses; re-running that
table over exact numbers would produce a "ground truth" that agrees with the
reconstruction by construction, and every metric computed against it would be
measuring the rule table against itself.

The oracle instead combines two things no participant can see:

**(a) the designed structure.** Each scenario's ``causal_template`` states, in the
scenario's own vocabulary, which behaviour is supposed to cause which state and
which state is supposed to produce the outcome. That is the experiment's
hypothesis, written down before the run.

**(b) the measured timeline.** :func:`cdf.oracle.events.build_oracle_events`
measures, from the privileged trace, *whether and when* each of those named
things actually happened.

:func:`build_oracle_causal_graph` instantiates (a) with (b). A template endpoint
that nothing in (b) realises does not become a node: the edge is dropped and
recorded in ``meta["unrealised_template_edges"]``. A scenario whose designed cause
never fired is a scenario that stopped working, and the oracle's job is to say so
rather than to draw the intended picture regardless.

Choosing among several realisations
-----------------------------------
One template endpoint can have several realising events -- ``closing`` may hold
during a spawn transient and again during the real encounter. The endpoint
assignment is therefore relaxed against the template's own edges: every endpoint
starts on its earliest realisation, and an edge whose cause would post-date its
effect pushes the effect forward (or, failing that, pulls the cause back) to the
nearest realisation that restores the order. This uses only the template's
topology and measured times -- no scenario is named anywhere -- and it converges
because every move is monotone in time. Edges that still run backwards after the
relaxation are kept (the design says they are causal) but listed in
``meta["temporally_inconsistent_edges"]``, because a cause that measurably follows
its effect is a finding about the scenario, not a detail to hide.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple, Union

import networkx as nx

from ..common.config import Config
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import (
    SCHEMA_VERSIONS,
    CausalEdgeType,
    Event,
    EventEdgeType,
    EventType,
    Evidence,
    GraphDocument,
    GraphEdge,
    Provenance,
    to_jsonable,
)
from ..common.timeline import Interval, temporal_relation
from ..graph.export import save_graph, to_networkx
from .events import (
    EVIDENCE_KIND,
    ORACLE_STATE_EVENT_TYPES,
    OUTCOME_EVENT_TYPES_BY_NAME,
    STATE_EVENT_TYPES,
    build_oracle_events,
    load_oracle_trace,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "TEMPLATE_RULE",
    "build_oracle_event_graph",
    "build_oracle_causal_graph",
    "persist_oracle",
    "build_and_persist",
]

#: ``GraphEdge.rule`` carried by every oracle causal edge. It names the *source*
#: of the claim, which is the whole point: an oracle edge is not an inference.
TEMPLATE_RULE = "scenario_causal_template"

#: Template endpoint kinds this module understands.
_ENDPOINT_KINDS = ("action", "state", "oracle_state", "outcome")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def _interval(event: Event) -> Interval:
    """The closed time interval an oracle event occupies."""
    t_start = float(event.t_start)
    t_peak = float(event.t_peak)
    t_end = t_peak if event.t_end is None else float(event.t_end)
    if t_end < t_start - 1e-6 or t_peak < t_start - 1e-6:
        raise ValueError(
            "oracle event {0} has an inverted time span: start={1}, peak={2}, "
            "end={3}".format(event.event_id, t_start, t_peak, t_end)
        )
    return Interval(min(t_start, t_peak), max(t_end, t_peak, t_start))


def _sorted_nodes(events: Sequence[Event]) -> List[Event]:
    """Events in a deterministic order: peak, onset, type, participant, id."""
    return sorted(
        events,
        key=lambda e: (
            float(e.t_peak),
            float(e.t_start),
            e.event_type.value,
            str(e.participant_id),
            str(e.event_id),
        ),
    )


def _validated_oracle_nodes(events: Sequence[Event]) -> List[Event]:
    """Sorted copy of ``events`` after the oracle-layer boundary check.

    The mirror image of :func:`cdf.local.event_graph.validated_local_nodes`: a
    *local* event reaching an oracle graph would silently turn an inference into
    part of the reference it is scored against, which is the one way the whole
    evaluation could quietly become circular.
    """
    for event in events:
        if event.provenance is not Provenance.ORACLE:
            raise ValueError(
                "event {0} has provenance {1!r} and cannot enter an oracle graph; the "
                "reference must be measured, never inferred".format(
                    event.event_id, event.provenance.value
                )
            )
    return _sorted_nodes(events)


def _run_identity(trace: Dict[str, Any]) -> Tuple[str, str, int]:
    """``(run_id, scenario_id, seed)`` of the run the trace came from."""
    summary = trace.get("summary", {}) or {}
    return (
        str(summary.get("run_id", "")),
        str(summary.get("scenario_id", "")),
        int(summary.get("seed", 0)),
    )


def _event_evidence(event: Event, part: str) -> Evidence:
    """Back-pointer from an edge to one of the events it relates."""
    span = _interval(event)
    return Evidence(
        kind=EVIDENCE_KIND,
        ref=event.event_id,
        t_start=span.start,
        t_end=span.end,
        detail={
            "part": part,
            "event_type": event.event_type.value,
            "participant": event.participant_id,
            "subject": event.subject,
        },
    )


def _non_negative_int(value: Any, dotted: str) -> int:
    """Coerce a configuration value to a non-negative int, or fail loudly."""
    try:
        out = int(value)
    except (TypeError, ValueError):
        raise TypeError("{0} must be an integer, got {1!r}".format(dotted, value))
    if out < 0:
        raise ValueError("{0} must not be negative, got {1!r}".format(dotted, value))
    return out


# ---------------------------------------------------------------------------
# Event graph
# ---------------------------------------------------------------------------


def build_oracle_event_graph(
    events: Sequence[Event],
    trace: Dict[str, Any],
    spec: Any,
    cfg: Config,
) -> GraphDocument:
    """Build the privileged event graph: what truly happened, and in what order.

    Like its local counterpart this document makes no causal claim. It carries
    two relations, both read directly off exact times:

    ``PRECEDES``
        each event to the next few events in the run. Unlike the local graph,
        this one spans *all* participants, because the oracle has one timeline
        rather than one per vehicle.
    ``INTERACTS_WITH``
        between two events of different participants whose padded intervals
        overlap. This is the relation the fusion layer has to reconstruct from
        trajectory evidence, so having the true version makes "did fusion connect
        the right pair of observations?" a measurable question.

    Parameters
    ----------
    events:
        Oracle events, typically from :func:`cdf.oracle.events.build_oracle_events`.
    trace:
        The mapping from :func:`cdf.oracle.events.load_oracle_trace`; supplies the
        run identity stamped into the document.
    spec:
        The scenario specification, recorded in ``meta`` for provenance. May be
        ``None``.
    cfg:
        Threshold registry. Keys read: ``oracle.event_graph.precedes_fanout``,
        ``oracle.event_graph.interacts_tolerance_s``,
        ``oracle.event_graph.interacts_max_per_event``,
        ``oracle.event_graph.max_edges`` and ``simulation.fixed_delta_seconds``.

    Returns
    -------
    GraphDocument
        ``graph_kind="event"``, ``scope=ORACLE``, ``owner=None`` -- the oracle
        belongs to no vehicle.
    """
    nodes = _validated_oracle_nodes(events)
    run_id, scenario_id, seed = _run_identity(trace)

    fanout = _non_negative_int(
        cfg.get("oracle.event_graph.precedes_fanout", 3), "oracle.event_graph.precedes_fanout"
    )
    interacts_max = _non_negative_int(
        cfg.get("oracle.event_graph.interacts_max_per_event", 4),
        "oracle.event_graph.interacts_max_per_event",
    )
    max_edges = _non_negative_int(
        cfg.get("oracle.event_graph.max_edges", 5000), "oracle.event_graph.max_edges"
    )
    pad_s = float(cfg.get("oracle.event_graph.interacts_tolerance_s", 0.5))
    if pad_s < 0.0:
        raise ValueError(
            "oracle.event_graph.interacts_tolerance_s must not be negative, got "
            "{0!r}".format(pad_s)
        )
    tolerance_s = float(cfg.get("simulation.fixed_delta_seconds", 0.05))
    if tolerance_s < 0.0:
        raise ValueError(
            "simulation.fixed_delta_seconds must not be negative, got {0!r}".format(tolerance_s)
        )

    edges: List[GraphEdge] = []
    for i, source in enumerate(nodes):
        for target in nodes[i + 1 : i + 1 + fanout]:
            edges.append(
                _relation_edge(
                    source,
                    target,
                    EventEdgeType.PRECEDES.value,
                    tolerance_s,
                    confidence=1.0,
                    detail={"gap_s": round(float(target.t_peak) - float(source.t_peak), 6)},
                )
            )

    for i, source in enumerate(nodes):
        source_span = _interval(source).expanded(pad_s)
        partners: List[Tuple[float, Event]] = []
        for target in nodes[i + 1 :]:
            if target.participant_id == source.participant_id:
                continue
            if source_span.intersects(_interval(target)):
                partners.append((abs(float(target.t_peak) - float(source.t_peak)), target))
        partners.sort(key=lambda item: (item[0], float(item[1].t_peak), item[1].event_id))
        for gap, target in partners[:interacts_max]:
            edges.append(
                _relation_edge(
                    source,
                    target,
                    EventEdgeType.INTERACTS_WITH.value,
                    tolerance_s,
                    # Both endpoints are measured, so the coincidence itself is
                    # exact; the pad is what makes it a judgement call, and it is
                    # reported rather than discounted.
                    confidence=1.0,
                    detail={
                        "peak_gap_s": round(float(gap), 6),
                        "overlap_pad_s": float(pad_s),
                        "participants": sorted(
                            {source.participant_id, target.participant_id}
                        ),
                    },
                )
            )

    truncated = 0 < max_edges < len(edges)
    if truncated:
        # ``PRECEDES`` merely restates timestamps, so it is the class to give up
        # first; within a class the shortest span is the most informative.
        edges = sorted(
            edges,
            key=lambda e: (
                0 if e.edge_type == EventEdgeType.INTERACTS_WITH.value else 1,
                round(float(e.detail.get("peak_gap_s", e.detail.get("gap_s", 0.0))), 6),
                str(e.source),
                str(e.target),
                str(e.edge_type),
            ),
        )[:max_edges]
    edges.sort(key=lambda e: (str(e.source), str(e.target), str(e.edge_type)))

    counts: Dict[str, int] = {}
    for edge in edges:
        counts[edge.edge_type] = counts.get(edge.edge_type, 0) + 1

    meta: Dict[str, Any] = {
        "note": (
            "privileged observational record: PRECEDES and INTERACTS_WITH are exact "
            "temporal relations over the true timeline, not causal claims"
        ),
        "n_nodes": len(nodes),
        "edge_counts": dict(sorted(counts.items())),
        "limits": {
            "precedes_fanout": fanout,
            "interacts_max_per_event": interacts_max,
            "interacts_tolerance_s": pad_s,
            "max_edges": max_edges,
        },
        "relation_tolerance_s": tolerance_s,
        "truncated": truncated,
        "participants": sorted({n.participant_id for n in nodes}),
        "scenario_variant": getattr(spec, "variant", None),
    }

    return GraphDocument(
        graph_kind="event",
        scope=Provenance.ORACLE,
        owner=None,
        run_id=run_id,
        scenario_id=scenario_id,
        seed=seed,
        nodes=nodes,
        edges=edges,
        meta=meta,
    )


def _relation_edge(
    source: Event,
    target: Event,
    edge_type: str,
    tolerance_s: float,
    confidence: float,
    detail: Dict[str, Any],
) -> GraphEdge:
    """Assemble one oracle event-graph edge with its temporal annotation."""
    return GraphEdge(
        source=source.event_id,
        target=target.event_id,
        edge_type=edge_type,
        confidence=float(confidence),
        provenance=Provenance.ORACLE,
        rule=None,
        temporal_relation=temporal_relation(
            _interval(source), _interval(target), tol=tolerance_s
        ),
        evidence=[_event_evidence(source, "source"), _event_evidence(target, "target")],
        owners=sorted(set(source.owners) | set(target.owners)),
        detail=detail,
    )


# ---------------------------------------------------------------------------
# Template endpoints
# ---------------------------------------------------------------------------


def _endpoint_key(endpoint: Dict[str, Any], index: int, role: str) -> Tuple[Any, ...]:
    """Hashable identity of one template endpoint.

    Two template entries naming the same thing must resolve to the *same* event,
    otherwise a chain that the scenario designed as ``x -> y -> z`` would come
    apart into two disconnected fragments.
    """
    kind = str(endpoint.get("kind", "")).strip()
    if kind not in _ENDPOINT_KINDS:
        raise ValueError(
            "causal_template entry {0} has {1} endpoint of unknown kind {2!r}; "
            "expected one of {3}".format(index, role, kind, list(_ENDPOINT_KINDS))
        )
    if kind == "outcome":
        name = str(endpoint.get("name", "")).strip()
        if name not in OUTCOME_EVENT_TYPES_BY_NAME:
            raise ValueError(
                "causal_template entry {0} names outcome {1!r}, which is not one of "
                "{2}".format(index, name, sorted(OUTCOME_EVENT_TYPES_BY_NAME))
            )
        parts = tuple(sorted(str(p) for p in endpoint.get("participants", []) or []))
        return ("outcome", name, parts)
    if kind == "action":
        action_id = str(endpoint.get("action_id", "")).strip()
        if not action_id:
            raise ValueError(
                "causal_template entry {0} has an {1} of kind 'action' without an "
                "action_id".format(index, role)
            )
        return ("action", str(endpoint.get("participant", "")), action_id)

    table = STATE_EVENT_TYPES if kind == "state" else ORACLE_STATE_EVENT_TYPES
    name = str(endpoint.get("name", "")).strip()
    if name not in table:
        raise ValueError(
            "causal_template entry {0} names {1} {2!r}, which the oracle does not "
            "measure; known {1}s are {3}".format(index, kind, name, sorted(table))
        )
    return (kind, str(endpoint.get("participant", "")), name)


def _candidates(key: Tuple[Any, ...], events: Sequence[Event]) -> List[Event]:
    """Every oracle event that realises an endpoint, earliest onset first."""
    kind = key[0]
    if kind == "outcome":
        _k, name, parts = key
        event_type = OUTCOME_EVENT_TYPES_BY_NAME[name]
        matches = [
            e
            for e in events
            if e.event_type is event_type
            and (not parts or tuple(sorted(set(e.owners))) == parts)
        ]
    elif kind == "action":
        _k, participant, action_id = key
        matches = [
            e
            for e in events
            if e.event_type is EventType.ORACLE_SCRIPTED_INTERVENTION
            and e.subject == action_id
            and (not participant or e.participant_id == participant)
        ]
    else:
        _k, participant, name = key
        table = STATE_EVENT_TYPES if kind == "state" else ORACLE_STATE_EVENT_TYPES
        event_type = table[name]
        matches = [
            e
            for e in events
            if e.event_type is event_type
            and e.subject == name
            and (not participant or e.participant_id == participant)
        ]
    return sorted(matches, key=lambda e: (float(e.t_start), float(e.t_peak), e.event_id))


def _key_text(key: Tuple[Any, ...]) -> str:
    """Readable form of an endpoint key, for diagnostics."""
    if key[0] == "outcome":
        return "outcome {0} of [{1}]".format(key[1], ", ".join(key[2]) or "any")
    return "{0} {1!r} of participant {2!r}".format(key[0], key[2], key[1] or "any")


def _resolve_endpoints(
    template_edges: Sequence[Tuple[int, Tuple[Any, ...], Tuple[Any, ...], str, str]],
    candidates: Dict[Tuple[Any, ...], List[Event]],
    tolerance_s: float,
) -> Dict[Tuple[Any, ...], Event]:
    """Pick one realising event per endpoint, consistent with the template order.

    See the module docstring for why a plain "earliest match" is not enough. The
    relaxation terminates: every accepted move assigns an endpoint a *later*
    candidate than it had (or the cause an *earlier* one), both strictly monotone
    over a finite candidate list, so no endpoint can be revisited indefinitely.
    """
    chosen: Dict[Tuple[Any, ...], Event] = {
        key: group[0] for key, group in candidates.items() if group
    }

    budget = 2 * len(template_edges) * max(1, max([len(g) for g in candidates.values()] or [1]))
    for _step in range(budget + 1):
        changed = False
        for (_index, cause_key, effect_key, _edge_type, _rationale) in template_edges:
            cause = chosen.get(cause_key)
            effect = chosen.get(effect_key)
            if cause is None or effect is None:
                continue
            if float(cause.t_start) <= float(effect.t_start) + tolerance_s:
                continue
            later = [
                e
                for e in candidates[effect_key]
                if float(e.t_start) >= float(cause.t_start) - tolerance_s
            ]
            if later:
                chosen[effect_key] = later[0]
                changed = True
                continue
            earlier = [
                e
                for e in candidates[cause_key]
                if float(e.t_start) <= float(effect.t_start) + tolerance_s
            ]
            if earlier:
                chosen[cause_key] = earlier[-1]
                changed = True
        if not changed:
            return chosen
    raise AssertionError(
        "causal-template endpoint relaxation did not converge in {0} passes; the "
        "template or the candidate set is inconsistent".format(budget)
    )


# ---------------------------------------------------------------------------
# Causal graph
# ---------------------------------------------------------------------------


MECHANICAL_RULE = "oracle_measured_mechanics"


def _mechanical_edges(
    nodes: Sequence[Event], tolerance_s: float
) -> List[GraphEdge]:
    """Ground-truth causal relations that no scenario template needs to declare.

    The causal template states the *designed* structure of a scenario -- the
    headline chain the experiment was built around. It deliberately says nothing
    about relations that are simply true of any vehicle: that a commanded brake
    decelerates the car, or that being struck brings it to a stop.

    Leaving those out makes the oracle an unfair reference. A reconstruction that
    correctly reports "B commanded a brake and B decelerated" is then charged a
    false positive for a claim that is, in fact, ground truth, and edge precision
    stops measuring correctness and starts measuring "absent from the template".

    These edges are derived from the privileged trace alone -- the scripted
    action timeline (exact) and the measured kinematic response (exact). They are
    NOT produced by importing or re-implementing the local rule table: the
    relations asserted here are far narrower than that table, and each one is
    established by a timing containment in ground truth rather than by a rule
    prior.

    Emitted, per participant:

    * a braking ``ORACLE_SCRIPTED_INTERVENTION`` -> a ``HARD_DECELERATION`` whose
      onset falls inside that action's commanded window;
    * a ``COLLISION`` -> that participant's ``POST_IMPACT_STOP``;
    * a ``COLLISION`` -> a ``HARD_DECELERATION`` beginning at or after impact.
    """
    by_participant: Dict[str, List[Event]] = {}
    for node in nodes:
        by_participant.setdefault(node.participant_id, []).append(node)

    out: List[GraphEdge] = []
    for participant, group in sorted(by_participant.items()):
        actions = [n for n in group if n.event_type == EventType.ORACLE_SCRIPTED_INTERVENTION]
        decels = [n for n in group if n.event_type == EventType.HARD_DECELERATION]
        collisions = [n for n in group if n.event_type == EventType.COLLISION]
        stops = [n for n in group if n.event_type == EventType.POST_IMPACT_STOP]

        for action in actions:
            if str(action.values.get("kind_is_brake", 1.0)) in ("0", "0.0"):
                continue
            if "brake" not in str(action.subject or "").lower() and not action.values.get(
                "intensity"
            ):
                # Only a braking command has a deceleration as its ground-truth
                # mechanical consequence; a lane shift or a speed change does not.
                continue
            window_end = float(action.t_end if action.t_end is not None else action.t_peak)
            for decel in decels:
                if action.t_start - tolerance_s <= decel.t_start <= window_end + tolerance_s:
                    out.append(
                        _mechanical_edge(
                            action,
                            decel,
                            CausalEdgeType.CONTRIBUTES_TO.value,
                            "a commanded brake decelerates the vehicle; the measured "
                            "deceleration begins inside the commanded window",
                            tolerance_s,
                        )
                    )
                    break

        for collision in collisions:
            for stop in stops:
                if stop.t_start >= collision.t_peak - tolerance_s:
                    out.append(
                        _mechanical_edge(
                            collision,
                            stop,
                            CausalEdgeType.TRIGGERS.value,
                            "the impact brings the struck vehicle to a stop",
                            tolerance_s,
                        )
                    )
                    break
            for decel in decels:
                if decel.t_start >= collision.t_peak - tolerance_s:
                    out.append(
                        _mechanical_edge(
                            collision,
                            decel,
                            CausalEdgeType.TRIGGERS.value,
                            "the impact decelerates the vehicle",
                            tolerance_s,
                        )
                    )
                    break
    return out


def _mechanical_edge(
    source: Event, target: Event, edge_type: str, rationale: str, tolerance_s: float
) -> GraphEdge:
    """One ground-truth mechanical edge, fully attributed to its evidence."""
    return GraphEdge(
        source=source.event_id,
        target=target.event_id,
        edge_type=edge_type,
        confidence=1.0,
        provenance=Provenance.ORACLE,
        rule=MECHANICAL_RULE,
        temporal_relation=temporal_relation(
            _interval(source), _interval(target), tol=tolerance_s
        ),
        evidence=[_event_evidence(source, "cause"), _event_evidence(target, "effect")],
        owners=sorted(set(source.owners) | set(target.owners)),
        detail={"rationale": rationale, "source": MECHANICAL_RULE},
    )


def build_oracle_causal_graph(
    events: Sequence[Event],
    trace: Dict[str, Any],
    spec: Any,
    cfg: Config,
) -> GraphDocument:
    """Instantiate the scenario's designed causal structure over measured events.

    Parameters
    ----------
    events:
        Oracle events. They all become nodes, including the ones no template edge
        touches: "this truly happened and explains nothing" is part of the
        reference, and dropping it would flatter the layer being scored.
    trace:
        The mapping from :func:`cdf.oracle.events.load_oracle_trace`.
    spec:
        The :class:`~cdf.simulation.scenario_base.ScenarioSpec` whose
        ``causal_template`` is being instantiated. ``None`` or an empty template
        yields an edgeless document, which is the honest result for a scenario
        that declares no designed structure.
    cfg:
        Threshold registry. Keys read: ``oracle.causal.jitter_tolerance_s``
        (defaulting to ``simulation.fixed_delta_seconds``).

    Returns
    -------
    GraphDocument
        ``graph_kind="causal"``, ``scope=ORACLE``, ``owner=None``, guaranteed
        acyclic. Diagnostics live in ``meta["unrealised_template_edges"]``,
        ``meta["temporally_inconsistent_edges"]`` and ``meta["rejected_edges"]``.

    Raises
    ------
    ValueError
        When the template is malformed: an unknown endpoint kind, an unknown
        state or outcome name, an action endpoint without an ``action_id`` or an
        unknown edge type. Every one of those is a configuration bug that would
        otherwise silently shrink the reference graph.
    """
    nodes = _validated_oracle_nodes(events)
    by_id = {n.event_id: n for n in nodes}
    run_id, scenario_id, seed = _run_identity(trace)

    tolerance_s = float(
        cfg.get(
            "oracle.causal.jitter_tolerance_s",
            cfg.get("simulation.fixed_delta_seconds", 0.05),
        )
    )
    if tolerance_s < 0.0:
        raise ValueError(
            "oracle.causal.jitter_tolerance_s must not be negative, got "
            "{0!r}".format(tolerance_s)
        )

    template = list(getattr(spec, "causal_template", []) or [])
    parsed: List[Tuple[int, Tuple[Any, ...], Tuple[Any, ...], str, str]] = []
    valid_edge_types = {e.value for e in CausalEdgeType}
    for index, entry in enumerate(template):
        if not isinstance(entry, dict):
            raise ValueError(
                "causal_template entry {0} is {1!r}, expected a mapping".format(index, entry)
            )
        edge_type = str(entry.get("edge", "")).strip()
        if edge_type not in valid_edge_types:
            raise ValueError(
                "causal_template entry {0} declares edge type {1!r}; expected one of "
                "{2}".format(index, edge_type, sorted(valid_edge_types))
            )
        cause_key = _endpoint_key(entry.get("cause", {}) or {}, index, "cause")
        effect_key = _endpoint_key(entry.get("effect", {}) or {}, index, "effect")
        parsed.append(
            (index, cause_key, effect_key, edge_type, str(entry.get("rationale", "")))
        )

    candidates: Dict[Tuple[Any, ...], List[Event]] = {}
    for (_index, cause_key, effect_key, _edge_type, _rationale) in parsed:
        for key in (cause_key, effect_key):
            if key not in candidates:
                candidates[key] = _candidates(key, nodes)

    chosen = _resolve_endpoints(parsed, candidates, tolerance_s)

    proposed: List[GraphEdge] = []
    unrealised: List[Dict[str, Any]] = []
    inconsistent: List[Dict[str, Any]] = []

    for (index, cause_key, effect_key, edge_type, rationale) in parsed:
        missing = [key for key in (cause_key, effect_key) if key not in chosen]
        if missing:
            unrealised.append(
                {
                    "template_index": index,
                    "edge_type": edge_type,
                    "cause": _key_text(cause_key),
                    "effect": _key_text(effect_key),
                    "rationale": rationale,
                    "unrealised_endpoints": [_key_text(k) for k in missing],
                    "reason": (
                        "no oracle event realises {0}; the designed {1} did not occur "
                        "in this run, so the edge is dropped rather than invented".format(
                            " or ".join(_key_text(k) for k in missing),
                            "cause" if cause_key in missing else "effect",
                        )
                    ),
                }
            )
            continue

        source = chosen[cause_key]
        target = chosen[effect_key]
        lag_s = float(target.t_start) - float(source.t_start)
        if lag_s < -tolerance_s:
            inconsistent.append(
                {
                    "template_index": index,
                    "edge_type": edge_type,
                    "source": source.event_id,
                    "target": target.event_id,
                    "lag_s": lag_s,
                    "reason": (
                        "the designed cause was measured {0:.3f}s after its effect; the "
                        "edge is kept because the design asserts it, but the timing "
                        "contradicts it".format(-lag_s)
                    ),
                }
            )
        proposed.append(
            GraphEdge(
                source=source.event_id,
                target=target.event_id,
                edge_type=edge_type,
                # The designed structure is ground truth by construction; the
                # uncertainty of this layer lives in the node times, not here.
                confidence=1.0,
                provenance=Provenance.ORACLE,
                rule=TEMPLATE_RULE,
                temporal_relation=temporal_relation(
                    _interval(source), _interval(target), tol=tolerance_s
                ),
                evidence=[_event_evidence(source, "cause"), _event_evidence(target, "effect")],
                owners=sorted(set(source.owners) | set(target.owners)),
                detail={
                    "template_index": index,
                    "rationale": rationale,
                    "cause": _key_text(cause_key),
                    "effect": _key_text(effect_key),
                    "lag_s": round(lag_s, 6),
                    "n_cause_candidates": len(candidates[cause_key]),
                    "n_effect_candidates": len(candidates[effect_key]),
                },
            )
        )

    mechanical = _mechanical_edges(nodes, tolerance_s)
    proposed = list(proposed) + mechanical

    accepted, rejected = _enforce_dag(proposed, set(by_id.keys()))

    counts: Dict[str, int] = {}
    for edge in accepted:
        counts[edge.edge_type] = counts.get(edge.edge_type, 0) + 1

    resolution: Dict[str, Any] = {}
    for key, group in sorted(candidates.items(), key=lambda kv: _key_text(kv[0])):
        picked = chosen.get(key)
        resolution[_key_text(key)] = {
            "event_id": None if picked is None else picked.event_id,
            "t_start": None if picked is None else float(picked.t_start),
            "n_candidates": len(group),
        }

    meta: Dict[str, Any] = {
        "note": (
            "every edge instantiates one entry of the scenario's declared "
            "causal_template over events measured from the privileged trace; no "
            "edge was inferred from the data and none came from the local rule engine"
        ),
        "source": TEMPLATE_RULE,
        "n_nodes": len(nodes),
        "n_template_edges": len(parsed),
        "n_realised_template_edges": sum(
            1 for e in accepted if e.rule == TEMPLATE_RULE
        ),
        "n_mechanical_edges": sum(1 for e in accepted if e.rule == MECHANICAL_RULE),
        "unrealised_template_edges": unrealised,
        "temporally_inconsistent_edges": inconsistent,
        "rejected_edges": rejected,
        "edge_counts": dict(sorted(counts.items())),
        "endpoint_resolution": resolution,
        "parameters": {"jitter_tolerance_s": tolerance_s},
        "scenario_variant": getattr(spec, "variant", None),
        "participants": sorted({n.participant_id for n in nodes}),
    }

    doc = GraphDocument(
        graph_kind="causal",
        scope=Provenance.ORACLE,
        owner=None,
        run_id=run_id,
        scenario_id=scenario_id,
        seed=seed,
        nodes=nodes,
        edges=accepted,
        meta=meta,
    )

    # The contract of this function is an acyclic document; a regression here
    # would poison every attribution metric computed against it, so it is
    # verified rather than assumed.
    if not nx.is_directed_acyclic_graph(to_networkx(doc)):
        raise AssertionError(
            "oracle causal graph for run {0!r} is cyclic after _enforce_dag".format(run_id)
        )
    if unrealised:
        LOGGER.warning(
            "oracle: %d of %d causal_template edges of scenario %s were not realised "
            "by this run; see meta['unrealised_template_edges']",
            len(unrealised),
            len(parsed),
            scenario_id or "?",
        )
    return doc


def _enforce_dag(
    edges: Sequence[GraphEdge], node_ids: Any
) -> Tuple[List[GraphEdge], List[Dict[str, Any]]]:
    """Keep the template edges that form a DAG; report the rest.

    Template edges are all equally authoritative (confidence 1.0), so they are
    considered in declaration order: the scenario author's ordering is the only
    tie-break that carries meaning, and it is deterministic.
    """
    graph = nx.DiGraph()
    graph.add_nodes_from(sorted(node_ids))

    accepted: List[GraphEdge] = []
    rejected: List[Dict[str, Any]] = []
    for edge in edges:
        if edge.source not in node_ids or edge.target not in node_ids:
            raise ValueError(
                "oracle causal edge {0}->{1} ({2}) references an event that is not a "
                "node of the document".format(edge.source, edge.target, edge.edge_type)
            )
        if edge.source == edge.target:
            rejected.append(
                _rejection(
                    edge,
                    "self loop: the template resolved both endpoints to the same "
                    "measured event, so it asserts that an event caused itself",
                )
            )
            continue
        if graph.has_edge(edge.source, edge.target):
            rejected.append(
                _rejection(edge, "an earlier template entry already connects this ordered pair")
            )
            continue
        if nx.has_path(graph, edge.target, edge.source):
            rejected.append(
                _rejection(
                    edge,
                    "would close a cycle: {0} already reaches {1} through earlier "
                    "template entries".format(edge.target, edge.source),
                )
            )
            continue
        graph.add_edge(edge.source, edge.target)
        accepted.append(edge)

    accepted.sort(key=lambda e: (str(e.source), str(e.target), str(e.edge_type)))
    return accepted, rejected


def _rejection(edge: GraphEdge, reason: str) -> Dict[str, Any]:
    return {
        "source": edge.source,
        "target": edge.target,
        "edge_type": edge.edge_type,
        "template_index": edge.detail.get("template_index"),
        "reason": reason,
    }


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


def persist_oracle(
    run_dir: Union[str, Path],
    events: Sequence[Event],
    event_graph: GraphDocument,
    causal_graph: GraphDocument,
) -> None:
    """Write the oracle events and both oracle graphs under ``oracle/``.

    Every path is resolved through :class:`~cdf.common.layout.RunLayout`, which
    is also what quarantines these artifacts: nothing outside ``oracle/`` is
    touched, and both graphs carry ``scope=ORACLE`` so that
    :func:`cdf.graph.export.load_graph` refuses to hand them to an inference stage.
    """
    for doc, expected_kind in ((event_graph, "event"), (causal_graph, "causal")):
        if doc.scope is not Provenance.ORACLE:
            raise ValueError(
                "refusing to persist a {0!r}-scoped graph under oracle/; the {1} graph "
                "has scope {2!r}".format(doc.scope.value, expected_kind, doc.scope.value)
            )
        if doc.graph_kind != expected_kind:
            raise ValueError(
                "expected the {0} graph, got graph_kind {1!r}".format(expected_kind, doc.graph_kind)
            )

    layout = RunLayout.from_run_dir(run_dir)
    layout.oracle_dir.mkdir(parents=True, exist_ok=True)

    write_json(
        layout.oracle_events,
        {
            "schema_version": SCHEMA_VERSIONS["events"],
            "provenance": Provenance.ORACLE.value,
            "run_id": event_graph.run_id,
            "scenario_id": event_graph.scenario_id,
            "seed": event_graph.seed,
            "participants": sorted({e.participant_id for e in events}),
            "n_events": len(events),
            "events": [to_jsonable(e) for e in events],
        },
    )
    # RunLayout names the causal GraphML explicitly but not the event one, so the
    # event graph's companion is derived from its own JSON path rather than by
    # re-spelling the directory here.
    save_graph(
        event_graph,
        layout.oracle_event_graph,
        layout.oracle_event_graph.with_suffix(".graphml"),
    )
    save_graph(causal_graph, layout.oracle_causal_graph, layout.oracle_causal_graphml)
    LOGGER.info(
        "oracle artifacts written: %d events, event graph %d/%d, causal graph %d/%d",
        len(events),
        len(event_graph.nodes),
        len(event_graph.edges),
        len(causal_graph.nodes),
        len(causal_graph.edges),
    )


def build_and_persist(
    run_dir: Union[str, Path], spec: Any, cfg: Config
) -> Tuple[List[Event], GraphDocument, GraphDocument]:
    """Measure, build and persist the whole oracle reconstruction of one run.

    The end-to-end entry point used by the CLI: load the privileged trace, measure
    its events, build both graphs, write them under ``oracle/`` and hand the three
    documents back so a caller can report on them without re-reading the disk.
    """
    trace = load_oracle_trace(run_dir)
    events = build_oracle_events(trace, spec, cfg)
    event_graph = build_oracle_event_graph(events, trace, spec, cfg)
    causal_graph = build_oracle_causal_graph(events, trace, spec, cfg)
    persist_oracle(run_dir, events, event_graph, causal_graph)
    return (events, event_graph, causal_graph)
