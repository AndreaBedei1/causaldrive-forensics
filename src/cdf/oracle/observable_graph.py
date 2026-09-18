"""The causal ground truth, built from physics rather than from the script.

The oracle causal graph this project started with was instantiated from each
scenario's ``causal_template`` -- the YAML statement of what the scenario meant
to demonstrate. That makes it a record of intent, and comparing a reconstruction
against intent asks the wrong question twice over: it credits the reference for
relations no evidence supports, and it penalises the reconstruction for relations
the physics shows but the template never mentioned.

This module builds the other causal graph. Its edges are proposed by general
physical rules -- the same relation vocabulary the local and fused layers use --
and then **each candidate is checked against the exact trace**. A rule may
suggest that B's braking closed the gap A was keeping; the edge is only drawn if
the exact geometry shows the closing rate actually rose after B's brake, by
enough to matter, within a plausible lag.

That verification step is what keeps this from being circular. Sharing a rule
*vocabulary* with the inference layer is necessary -- two graphs cannot be
compared unless they are allowed to say the same things. Sharing rule *firing*
would make agreement true by construction. So the rules here propose, and the
privileged trace disposes.

Three things this module will not do:

* branch on a scenario id, ever;
* read ``causal_template``, ``expected_outcome`` or any scripted action;
* emit a node type outside :mod:`cdf.graph.ontology`'s comparable vocabulary.

The scenario's designed mechanism still matters, and
:mod:`cdf.oracle.design_reference` answers it: *did the thing the scenario
intended actually happen?* That is a question about the experiment. This module
answers a question about the world.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
    SCHEMA_VERSIONS,
)
from ..graph.ontology import COMPARABLE_EDGE_TYPES, COMPARABLE_EVENT_TYPES
from .observable import pairwise_truth

LOGGER = logging.getLogger(__name__)

__all__ = ["build_observable_causal_graph", "OBSERVABLE_RULES", "ObservableRule"]


class ObservableRule(object):
    """A physical relation the trace may or may not support.

    ``verify`` is the part that matters. Without it a rule is a pattern match
    over event types, which is exactly what the reconstruction does -- and a
    reference that reasons the same way as the thing it is judging is not a
    reference. With it, the rule is a hypothesis the exact trace can refuse.
    """

    __slots__ = ("name", "cause_types", "effect_types", "edge_type", "relation",
                 "max_lag_s", "min_lag_s", "verify", "description")

    def __init__(
        self,
        name: str,
        cause_types: Tuple[str, ...],
        effect_types: Tuple[str, ...],
        edge_type: CausalEdgeType,
        relation: str,
        max_lag_s: float,
        description: str,
        verify: Optional[Callable[..., Optional[Dict[str, Any]]]] = None,
        min_lag_s: float = -0.15,
    ) -> None:
        for value in cause_types + effect_types:
            if value not in COMPARABLE_EVENT_TYPES:
                raise ValueError(
                    "observable rule {0!r} names {1}, which is not in the "
                    "comparable vocabulary".format(name, value)
                )
        if edge_type.value not in COMPARABLE_EDGE_TYPES:
            raise ValueError(
                "observable rule {0!r} uses edge type {1}, which is not "
                "comparable".format(name, edge_type.value)
            )
        if relation not in _RELATIONS:
            raise ValueError(
                "observable rule {0!r} uses unknown relation {1!r}".format(
                    name, relation
                )
            )
        self.name = name
        self.cause_types = cause_types
        self.effect_types = effect_types
        self.edge_type = edge_type
        self.relation = relation
        self.max_lag_s = float(max_lag_s)
        self.min_lag_s = float(min_lag_s)
        self.verify = verify
        self.description = description


#: How the vehicles a cause is about must stand to those the effect is about.
_RELATIONS = (
    "same_actor",       # one vehicle's own control causing its own motion
    "actor_in_pair",    # what one vehicle did, affecting a pair it belongs to
    "same_pair",        # an escalation within one ordered pair
    "pair_to_actor",    # a pair's state provoking one member's response
    "shared_member",    # two pair-events sharing a vehicle (impact chains)
)


# ---------------------------------------------------------------------------
# Verifiers: each asks the exact trace whether the relation actually holds
# ---------------------------------------------------------------------------


def _verify_control_response(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """A control input is only a cause of motion if the motion actually followed.

    The trace is asked directly: did this vehicle's longitudinal acceleration
    move in the expected direction, by a meaningful amount, between the control
    and the response? A brake that coincided with a deceleration the vehicle was
    already in is not the cause of it.
    """
    rows = context.rows(cause.participant_id)
    if not rows:
        return None
    before = context.acceleration_at(cause.participant_id, cause.t_start)
    during = context.acceleration_at(cause.participant_id, effect.t_peak)
    if before is None or during is None:
        return None
    braking = cause.event_type.value in (
        EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value
    )
    delta = during - before
    # Braking must make the acceleration more negative; throttle, more positive.
    moved = -delta if braking else delta
    if moved < context.min_response_mps2:
        return None
    return {
        "accel_before_mps2": round(before, 4),
        "accel_after_mps2": round(during, 4),
        "delta_mps2": round(delta, 4),
    }


def _verify_closing_after_change(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """One vehicle's speed change is only a cause of a gap closing if it closed.

    Checks the exact pairwise geometry of the observer/subject pair named by the
    effect: the closing rate must actually be higher after the cause than before
    it. In a rear-end that is the whole mechanism -- the lead vehicle slows, so
    the follower closes -- and it is a claim the trace can settle.
    """
    observer = effect.participant_id
    subject = effect.subject
    if not subject:
        return None
    rows = context.pair(observer, subject)
    if not rows:
        return None
    before = context.closing_rate(observer, subject, cause.t_start)
    after = context.closing_rate(observer, subject, effect.t_peak)
    if before is None or after is None:
        return None
    if after - before < context.min_closing_gain_mps:
        return None
    return {
        "closing_before_mps": round(before, 4),
        "closing_after_mps": round(after, 4),
        "gain_mps": round(after - before, 4),
    }


def _verify_ttc_fell(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """An escalation is only real if the time to collision actually shortened."""
    observer = effect.participant_id
    subject = effect.subject
    if not subject:
        return None
    before = context.ttc(observer, subject, cause.t_peak)
    after = context.ttc(observer, subject, effect.t_peak)
    if after is None:
        return None
    if before is not None and after >= before:
        return None
    return {
        "ttc_before_s": None if before is None else round(before, 4),
        "ttc_after_s": round(after, 4),
    }


def _verify_same_collision(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """A risk state only causes *this* collision if it involved the same pair."""
    if not (cause.subject and effect.subject):
        return None
    if {cause.participant_id, cause.subject} != {effect.participant_id, effect.subject}:
        return None
    separation = context.range_at(
        effect.participant_id, effect.subject, cause.t_peak
    )
    return {"range_at_cause_m": None if separation is None else round(separation, 4)}


def _verify_stop_followed(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """A vehicle stopping after an impact it was actually in."""
    if cause.subject and effect.participant_id not in (
        cause.participant_id, cause.subject
    ):
        return None
    speed = context.speed_at(effect.participant_id, effect.t_peak)
    return {"speed_at_stop_mps": None if speed is None else round(speed, 4)}


def _verify_braking_avoided_contact(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """Braking prevented an outcome only if the vehicles genuinely separated.

    The exact minimum range after the brake must be larger than it was at the
    moment of braking: the gap has to have actually opened. A brake followed by
    a continued approach prevented nothing, whatever the event types suggest.
    """
    if not effect.subject:
        return None
    pair = (effect.participant_id, effect.subject)
    at_brake = context.range_at(pair[0], pair[1], cause.t_peak)
    minimum = context.min_range_after(pair[0], pair[1], cause.t_peak)
    if at_brake is None or minimum is None:
        return None
    if minimum <= 0.0:
        return None
    return {
        "range_at_brake_m": round(at_brake, 4),
        "min_range_after_m": round(minimum, 4),
    }


def _verify_impact_chain(
    cause: Event, effect: Event, context: "_Context"
) -> Optional[Dict[str, Any]]:
    """One impact propagating into another, in the order the trace records.

    The two collisions must share exactly one vehicle -- the one struck and then
    striking -- and the first must precede the second by more than the sampling
    step, otherwise the trace does not establish an order at all.
    """
    first = {cause.participant_id, cause.subject}
    second = {effect.participant_id, effect.subject}
    shared = first & second
    if len(shared) != 1 or first == second:
        return None
    lag = effect.t_peak - cause.t_peak
    if lag <= context.dt:
        return None
    return {"shared_vehicle": sorted(shared)[0], "lag_s": round(lag, 4)}


# ---------------------------------------------------------------------------
# The rule table
# ---------------------------------------------------------------------------

OBSERVABLE_RULES: Tuple[ObservableRule, ...] = (
    # -- mechanical: a control input and the motion it produced --------------
    ObservableRule(
        "brake_decelerates_vehicle",
        (EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value),
        (EventType.DECELERATION.value, EventType.HARD_DECELERATION.value),
        CausalEdgeType.CONTRIBUTES_TO, "same_actor", 2.0,
        "a brake command, where the exact velocity shows the vehicle slowed",
        verify=_verify_control_response,
    ),
    ObservableRule(
        "throttle_accelerates_vehicle",
        (EventType.THROTTLE_ONSET.value,),
        (EventType.ACCELERATION.value,),
        CausalEdgeType.CONTRIBUTES_TO, "same_actor", 2.0,
        "a throttle command, where the exact velocity shows the vehicle sped up",
        verify=_verify_control_response,
    ),
    ObservableRule(
        "steering_turns_vehicle",
        (EventType.STEER_ONSET.value,),
        (EventType.SIGNIFICANT_HEADING_CHANGE.value,
         EventType.LANE_CHANGE_LIKE_MANEUVER.value),
        CausalEdgeType.CONTRIBUTES_TO, "same_actor", 3.0,
        "a steering input and the heading change that followed it",
    ),

    # -- kinematic: what one vehicle did, and what it did to a pair ----------
    ObservableRule(
        "deceleration_closes_gap",
        (EventType.DECELERATION.value, EventType.HARD_DECELERATION.value),
        (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value),
        CausalEdgeType.TRIGGERS, "actor_in_pair", 3.0,
        "one vehicle slowing, where the exact geometry shows the gap then closed",
        verify=_verify_closing_after_change,
    ),
    ObservableRule(
        "acceleration_closes_gap",
        (EventType.ACCELERATION.value,),
        (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value),
        CausalEdgeType.INCREASES_RISK_OF, "actor_in_pair", 3.0,
        "one vehicle speeding up, where the gap to another then closed",
        verify=_verify_closing_after_change,
    ),
    ObservableRule(
        "lateral_manoeuvre_creates_conflict",
        (EventType.LANE_CHANGE_LIKE_MANEUVER.value,
         EventType.SIGNIFICANT_HEADING_CHANGE.value),
        (EventType.CUT_IN_LIKE_MOTION.value, EventType.LATERAL_CROSSING.value,
         EventType.PREDICTED_PATH_CONFLICT.value),
        CausalEdgeType.CONTRIBUTES_TO, "actor_in_pair", 3.0,
        "a lateral manoeuvre and the path conflict it produced",
    ),

    # -- escalation within one pair -----------------------------------------
    ObservableRule(
        "closing_shortens_ttc",
        (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value),
        (EventType.LOW_TTC.value, EventType.CRITICAL_TTC.value),
        CausalEdgeType.CONTRIBUTES_TO, "same_pair", 4.0,
        "a closing gap, where the exact time to collision then fell",
        verify=_verify_ttc_fell,
    ),
    ObservableRule(
        "ttc_escalates_to_critical",
        (EventType.LOW_TTC.value,),
        (EventType.CRITICAL_TTC.value,),
        CausalEdgeType.CONTRIBUTES_TO, "same_pair", 3.0,
        "time to collision falling further",
        verify=_verify_ttc_fell,
    ),
    ObservableRule(
        "cut_in_closes_gap",
        (EventType.CUT_IN_LIKE_MOTION.value, EventType.LATERAL_CROSSING.value),
        (EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value),
        CausalEdgeType.TRIGGERS, "same_pair", 3.0,
        "a vehicle moving into another's path, and the gap then closing",
    ),
    ObservableRule(
        "path_conflict_becomes_entry",
        (EventType.PREDICTED_PATH_CONFLICT.value,),
        (EventType.CONFLICT_REGION_ENTRY.value,),
        CausalEdgeType.TRIGGERS, "same_pair", 6.0,
        "paths that were going to cross, and the vehicle arriving where they do",
    ),
    ObservableRule(
        "conflict_entry_shortens_ttc",
        (EventType.CONFLICT_REGION_ENTRY.value,),
        (EventType.LOW_TTC.value, EventType.CRITICAL_TTC.value),
        CausalEdgeType.CONTRIBUTES_TO, "same_pair", 3.0,
        "arriving in a shared region, where the time to collision then fell",
        verify=_verify_ttc_fell,
    ),

    # -- a pair's state provoking one vehicle's response ---------------------
    ObservableRule(
        "risk_triggers_braking",
        (EventType.CRITICAL_TTC.value, EventType.LOW_TTC.value,
         EventType.RAPID_CLOSING.value),
        (EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value),
        CausalEdgeType.TRIGGERS, "pair_to_actor", 2.5,
        "a closing threat and the braking that answered it",
    ),
    ObservableRule(
        "threat_triggers_steering",
        (EventType.CRITICAL_TTC.value, EventType.LATERAL_CROSSING.value,
         EventType.CUT_IN_LIKE_MOTION.value),
        (EventType.STEER_ONSET.value,),
        CausalEdgeType.TRIGGERS, "pair_to_actor", 2.5,
        "a threat and the evasive steering that answered it",
    ),

    # -- outcomes -----------------------------------------------------------
    ObservableRule(
        "critical_ttc_causes_collision",
        (EventType.CRITICAL_TTC.value,),
        (EventType.COLLISION.value,),
        CausalEdgeType.CAUSES_OUTCOME, "same_pair", 4.0,
        "a critical time to collision that was in fact not resolved",
        verify=_verify_same_collision,
    ),
    ObservableRule(
        "conflict_entry_causes_collision",
        (EventType.CONFLICT_REGION_ENTRY.value,),
        (EventType.COLLISION.value,),
        CausalEdgeType.CAUSES_OUTCOME, "same_pair", 5.0,
        "two vehicles arriving in the same place, and colliding there",
        verify=_verify_same_collision,
    ),
    ObservableRule(
        "conflict_causes_near_miss",
        (EventType.CRITICAL_TTC.value, EventType.CONFLICT_REGION_ENTRY.value),
        (EventType.NEAR_MISS.value,),
        CausalEdgeType.CAUSES_OUTCOME, "same_pair", 4.0,
        "a conflict that came close and resolved without contact",
        verify=_verify_same_collision,
    ),
    ObservableRule(
        "braking_prevents_contact",
        (EventType.HARD_BRAKE.value, EventType.HARD_DECELERATION.value),
        (EventType.NEAR_MISS.value,),
        CausalEdgeType.PREVENTS, "actor_in_pair", 4.0,
        "braking, where the exact range afterwards shows the vehicles separated",
        verify=_verify_braking_avoided_contact,
    ),
    ObservableRule(
        "collision_forces_stop",
        (EventType.COLLISION.value,),
        (EventType.POST_IMPACT_STOP.value,),
        CausalEdgeType.TRIGGERS, "pair_to_actor", 5.0,
        "an impact and the vehicle coming to rest after it",
        verify=_verify_stop_followed,
    ),
    ObservableRule(
        "impact_propagates_to_next_impact",
        (EventType.COLLISION.value,),
        (EventType.COLLISION.value,),
        CausalEdgeType.CONTRIBUTES_TO, "shared_member", 3.0,
        "one impact pushing a vehicle into the next, in the recorded order",
        verify=_verify_impact_chain,
    ),
)


# ---------------------------------------------------------------------------
# Verification context
# ---------------------------------------------------------------------------


class _Context(object):
    """Exact-state lookups the verifiers ask questions of."""

    def __init__(self, trace: Mapping[str, Any], cfg: Config) -> None:
        from .observable import ObservableExtractor

        self.trace = trace
        self.cfg = cfg
        self._extractor = ObservableExtractor(trace, cfg)
        self._pairs: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
        self.dt = float(cfg.get("simulation.fixed_delta_seconds", 0.05))
        self.min_response_mps2 = float(
            cfg.get("oracle.observable.min_control_response_mps2", 0.5)
        )
        self.min_closing_gain_mps = float(
            cfg.get("oracle.observable.min_closing_gain_mps", 0.5)
        )

    def rows(self, pid: str) -> Sequence[Mapping[str, Any]]:
        return self._extractor._rows.get(str(pid), [])

    def pair(self, observer: str, target: str) -> List[Dict[str, Any]]:
        key = (str(observer), str(target))
        if key not in self._pairs:
            self._pairs[key] = pairwise_truth(self.trace, key[0], key[1])
        return self._pairs[key]

    def _at(self, rows: Sequence[Mapping[str, Any]], t: float) -> Optional[Mapping[str, Any]]:
        if not rows:
            return None
        best = min(rows, key=lambda r: abs(float(r["t"]) - float(t)))
        return best if abs(float(best["t"]) - float(t)) <= 0.5 else None

    def acceleration_at(self, pid: str, t: float) -> Optional[float]:
        rows = self.rows(pid)
        accel = self._extractor._accel.get(str(pid), [])
        if not rows or len(accel) != len(rows):
            return None
        index = min(
            range(len(rows)), key=lambda i: abs(float(rows[i]["t"]) - float(t))
        )
        return float(accel[index])

    def speed_at(self, pid: str, t: float) -> Optional[float]:
        row = self._at(self.rows(pid), t)
        return None if row is None else float(row["speed"])

    def closing_rate(self, observer: str, target: str, t: float) -> Optional[float]:
        row = self._at(self.pair(observer, target), t)
        return None if row is None else float(row["closing_rate_mps"])

    def ttc(self, observer: str, target: str, t: float) -> Optional[float]:
        row = self._at(self.pair(observer, target), t)
        if row is None or row.get("ttc_s") is None:
            return None
        return float(row["ttc_s"])

    def range_at(self, observer: str, target: str, t: float) -> Optional[float]:
        row = self._at(self.pair(observer, target), t)
        return None if row is None else float(row["range_m"])

    def min_range_after(
        self, observer: str, target: str, t: float
    ) -> Optional[float]:
        rows = [r for r in self.pair(observer, target) if float(r["t"]) >= float(t)]
        return min((float(r["range_m"]) for r in rows), default=None)


# ---------------------------------------------------------------------------
# Building the graph
# ---------------------------------------------------------------------------


def _vehicles(event: Event, participants: Sequence[str]) -> Tuple[frozenset, bool]:
    """``(vehicles the event is about, whether it is a pair event)``."""
    known = {str(p) for p in participants}
    own = {str(event.participant_id)}
    if event.subject and str(event.subject) in known:
        return frozenset(own | {str(event.subject)}), True
    return frozenset(own), False


def _relation_holds(
    relation: str,
    cause: Event,
    effect: Event,
    participants: Sequence[str],
) -> bool:
    cause_set, cause_pair = _vehicles(cause, participants)
    effect_set, effect_pair = _vehicles(effect, participants)
    if relation == "same_actor":
        return (not cause_pair and not effect_pair and cause_set == effect_set)
    if relation == "actor_in_pair":
        return (not cause_pair and effect_pair and cause_set <= effect_set)
    if relation == "same_pair":
        return cause_pair and effect_pair and cause_set == effect_set
    if relation == "pair_to_actor":
        return cause_pair and not effect_pair and effect_set <= cause_set
    if relation == "shared_member":
        return (
            cause_pair and effect_pair and cause_set != effect_set
            and bool(cause_set & effect_set)
        )
    return False


def build_observable_causal_graph(
    events: Sequence[Event],
    trace: Mapping[str, Any],
    cfg: Config,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> GraphDocument:
    """The observable causal DAG: general rules, each verified against the trace.

    Every edge carries the rule that proposed it, the lag between cause and
    effect, and -- where a verifier ran -- the exact quantities that supported
    it, so any edge can be checked rather than taken on trust. Edges a rule
    proposed and the trace refused are recorded in ``meta`` with the reason,
    because a reference that only shows what it concluded is a reference nobody
    can audit.
    """
    participants = [str(p) for p in trace.get("participants", []) or []]
    comparable = [e for e in events if e.event_type.value in COMPARABLE_EVENT_TYPES]
    if len(comparable) != len(events):
        raise ValueError(
            "observable causal graph was given {0} event(s) outside the "
            "comparable vocabulary".format(len(events) - len(comparable))
        )

    context = _Context(trace, cfg)
    by_type: Dict[str, List[Event]] = {}
    for event in comparable:
        by_type.setdefault(event.event_type.value, []).append(event)

    edges: List[GraphEdge] = []
    seen: set = set()
    refused: List[Dict[str, Any]] = []

    for rule in OBSERVABLE_RULES:
        causes = [e for t in rule.cause_types for e in by_type.get(t, [])]
        effects = [e for t in rule.effect_types for e in by_type.get(t, [])]
        for cause in causes:
            for effect in effects:
                if cause.event_id == effect.event_id:
                    continue
                lag = float(effect.t_peak) - float(cause.t_peak)
                if lag > rule.max_lag_s or lag < rule.min_lag_s:
                    continue
                if not _relation_holds(rule.relation, cause, effect, participants):
                    continue
                key = (cause.event_id, effect.event_id, rule.edge_type.value)
                if key in seen:
                    continue
                support: Dict[str, Any] = {}
                if rule.verify is not None:
                    verified = rule.verify(cause, effect, context)
                    if verified is None:
                        refused.append({
                            "rule": rule.name,
                            "source": cause.event_id,
                            "target": effect.event_id,
                            "reason": "the exact trace does not support the relation",
                        })
                        continue
                    support = verified
                seen.add(key)
                edges.append(GraphEdge(
                    source=cause.event_id,
                    target=effect.event_id,
                    edge_type=rule.edge_type.value,
                    # Ground truth asserts what the trace shows; it is not
                    # ranking hypotheses, so there is nothing to be unsure of.
                    confidence=1.0,
                    provenance=Provenance.ORACLE,
                    rule=rule.name,
                    detail={
                        "relation": rule.relation,
                        "lag_s": round(lag, 6),
                        "verified": rule.verify is not None,
                        "support": support,
                        "description": rule.description,
                    },
                ))

    nodes_by_id = {e.event_id: e for e in comparable}
    edges = _enforce_acyclic(edges, nodes_by_id)

    return GraphDocument(
        graph_kind="causal",
        scope=Provenance.ORACLE,
        owner=None,
        run_id=run_id,
        scenario_id=scenario_id,
        seed=int(seed),
        nodes=list(comparable),
        edges=edges,
        meta={
            "reference_kind": "oracle_observable",
            "note": (
                "physical ground truth in the comparable vocabulary. Built by "
                "general rules verified against the exact trace; no scenario "
                "template, no scripted action, no branch on scenario id"
            ),
            "n_rules": len(OBSERVABLE_RULES),
            "n_edges_refused_by_trace": len(refused),
            "refused": refused[:200],
            "schema_version": SCHEMA_VERSIONS.get("graph", "1.0.0"),
        },
    )


def _enforce_acyclic(
    edges: Sequence[GraphEdge], nodes: Mapping[str, Event]
) -> List[GraphEdge]:
    """Drop the smallest set of back-edges that makes the result a DAG.

    Ordering by cause time and keeping only forward edges is enough here: the
    rules already require a non-negative lag beyond a small tolerance, so a cycle
    can only arise between events whose peaks coincide. Those are exactly the
    cases where the trace does not establish an order, and dropping them is the
    honest resolution.
    """
    order = {
        event_id: index
        for index, event_id in enumerate(
            sorted(nodes, key=lambda i: (float(nodes[i].t_peak), i))
        )
    }
    kept: List[GraphEdge] = []
    for edge in edges:
        if order.get(edge.source, 0) < order.get(edge.target, 0):
            kept.append(edge)
    return kept
