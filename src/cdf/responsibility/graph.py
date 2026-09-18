"""Obligations and violations, in a graph of their own.

The physical DAG says a hard brake closed a gap and the closing gap produced an
impact. It cannot say anyone *should* have done otherwise, because "should" is
not a physical relation and putting it in the same graph would mix two kinds of
claim that have to be separable -- a reader must be able to accept the physics
and dispute the norm, which is impossible once they share a node set.

So this is a second graph, over obligations. It is built *from* the physical
graph and the observed events, and its top-level claim requires both halves:

    STOP_SIGN_DETECTED(B)              a sign was seen
        -> STOP_REQUIRED(B)            so an obligation existed
    + NO_STOP_AFTER_STOP_SIGN(B)       and the vehicle did not discharge it
        -> STOP_RULE_VIOLATION(B)      so the rule was broken
    + a physical path to the collision
        -> RESPONSIBILITY_CONTRIBUTION(B)

Neither half alone is enough. A vehicle that ran a stop sign a hundred metres
from an unrelated collision broke a rule without contributing to the outcome; a
vehicle that braked perfectly legally and was rear-ended contributed physically
without breaking anything.

The pushed vehicle
------------------

The case that makes the "physical path" half subtle. C hits B, B is shunted into
A. B physically collides with A -- B's mass, B's momentum -- and a naive ancestry
check makes B a contributor to an impact B had no way to avoid.

The rule here is that a path may run *through* an impact only if the vehicle's own
behaviour independently reaches that impact. C accelerated into B, so C reaches
the first impact by its own doing and may follow it to the second: C pushed B into
A. Nothing B did reaches the first impact, so for B the route is closed.

Note what this does not assume. It never asks which vehicle struck which -- the
collision record deliberately does not say, and asking the simulator would be the
privileged shortcut the whole project avoids. Striker and struck fall out of the
graph instead.

And if B *had* done something that contributed to being hit, B would reach the
first impact and could follow it onwards -- correctly, because B's braking would
then really be in the chain that ends at A. Whether that counts against B is the
other half of the claim, and a vehicle that braked lawfully broke no rule however
involved it was.

Relevance is computed per outcome rather than pooled, because in a chain a
vehicle is often a contributor to one impact and not the other, and a single
yes/no would lose the distinction the chain scenarios exist to test.

Words this layer does not use
-----------------------------

Not fault, not guilt, not liability, not blame, and no percentages. What is
produced is a normative violation against a stated benchmark rule, plus evidence
of causal relevance, reported as supported, partial or insufficient. What a court
would make of any of it is a question this project cannot answer and does not.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.schemas import (
    SCHEMA_VERSIONS, CheckStatus, Event, EventType, GraphDocument, Provenance,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "RESPONSIBILITY_NODE_TYPES",
    "build_responsibility_graph",
]

#: The vocabulary of this graph. Deliberately *not* added to ``EventType``: an
#: obligation is not an observable event, and the event ontology exists to say
#: what a reconstruction and a privileged trace can both assert about the world.
RESPONSIBILITY_NODE_TYPES: Tuple[str, ...] = (
    "STOP_REQUIRED",
    "YIELD_REQUIRED",
    "PRIORITY_GRANTED",
    "PRIORITY_AMBIGUOUS",
    "STOP_RULE_VIOLATION",
    "YIELD_RULE_VIOLATION",
    "SOLID_LINE_VIOLATION",
    "UNSAFE_CONFLICT_ENTRY",
    "RESPONSIBILITY_CONTRIBUTION",
    "MITIGATING_RESPONSE",
)

#: Events that count as a vehicle's own behaviour when tracing a path from what
#: it did to what happened. A collision is not here: being in one is not a
#: behaviour, which is the whole of the pushed-vehicle case.
_OWN_BEHAVIOUR_TYPES: frozenset = frozenset({
    EventType.VEHICLE_STARTED.value, EventType.ACCELERATION.value,
    EventType.DECELERATION.value, EventType.HARD_DECELERATION.value,
    EventType.BRAKE_ONSET.value, EventType.HARD_BRAKE.value,
    EventType.THROTTLE_ONSET.value, EventType.STEER_ONSET.value,
    EventType.SIGNIFICANT_HEADING_CHANGE.value,
    EventType.LANE_CHANGE_LIKE_MANEUVER.value, EventType.FULL_STOP.value,
    EventType.STOP_LINE_CROSSED.value, EventType.SOLID_LINE_CROSSED.value,
    EventType.LANE_MARKING_CROSSED.value,
    EventType.NO_STOP_AFTER_STOP_SIGN.value,
    EventType.NO_BRAKING_RESPONSE.value, EventType.NO_YIELD_RESPONSE.value,
    EventType.NO_EVASIVE_RESPONSE.value,
    EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION.value,
    EventType.CONTINUED_ACCELERATION_DURING_CONFLICT.value,
})


def _type_of(node: Any) -> str:
    et = getattr(node, "event_type", None)
    return et.value if hasattr(et, "value") else str(et)


def _node(
    node_id: str,
    node_type: str,
    participant: str,
    t: Optional[float] = None,
    subject: Optional[str] = None,
    basis: Optional[Sequence[str]] = None,
    confidence: float = 1.0,
    detail: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "node_id": node_id,
        "node_type": node_type,
        "participant": str(participant),
        "subject": str(subject) if subject else None,
        "t": None if t is None else round(float(t), 4),
        "basis": list(basis or []),
        "confidence": round(float(confidence), 4),
        "detail": dict(detail or {}),
    }


def _adjacency(graph: Optional[GraphDocument]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    if graph is None:
        return out
    for edge in graph.edges:
        out.setdefault(edge.source, []).append(edge.target)
    return out


def _collisions_own_behaviour_reaches(
    adjacency: Mapping[str, List[str]],
    sources: Set[str],
    collisions: Set[str],
) -> Set[str]:
    """Which impacts this vehicle's own behaviour reaches without going through one.

    This is what separates the vehicle that did the pushing from the one that was
    pushed, and it is the only thing that can: the collision event itself records
    two parties without saying which struck which, and asking the simulator would
    be exactly the privileged shortcut this project exists to avoid.

    C accelerated into B, so C's own behaviour reaches that impact directly. B was
    hit; unless B did something that independently contributed to being hit, no
    chain of B's own behaviour reaches it at all.
    """
    reached: Set[str] = set()
    frontier = [s for s in sorted(sources) if s not in collisions]
    seen: Set[str] = set()
    while frontier:
        current = frontier.pop(0)
        if current in seen:
            continue
        seen.add(current)
        for nxt in sorted(adjacency.get(current, [])):
            if nxt in collisions:
                # Record it, and stop: what lies beyond an impact is reached
                # *through* the impact, which is a different claim.
                reached.add(nxt)
                continue
            frontier.append(nxt)
    return reached


def _reaches(
    adjacency: Mapping[str, List[str]],
    sources: Set[str],
    target: str,
    collisions: Set[str],
    passable: Set[str],
) -> Tuple[bool, List[str]]:
    """Can this vehicle's own behaviour reach this outcome?

    A collision on the way may be traversed only if it is in ``passable`` -- the
    set of impacts the vehicle's own behaviour independently reaches. That single
    condition settles the pushed-vehicle case in both directions.

    C accelerated into B and B was shunted into A. C reaches the first impact by
    its own doing, so it may pass through it and reach the second: C pushed B into
    A. B does not reach the first impact by anything it did, so the route is
    closed and B is not made a contributor to an impact it could not have avoided.

    And if B *had* done something that contributed to being hit -- braking hard
    for no reason, say -- then B may pass through, and B's braking really is in
    the chain that ends at A. Whether that is B's fault is not a question this
    function answers: the normative half of the claim is evaluated separately, and
    a vehicle that braked lawfully breaks no rule however involved it was.
    """
    if not sources:
        return False, []
    frontier: List[Tuple[str, List[str]]] = [
        (s, [s]) for s in sorted(sources) if s not in collisions
    ]
    seen: Set[str] = set()
    while frontier:
        current, path = frontier.pop(0)
        if current == target:
            return True, path
        if current in seen:
            continue
        seen.add(current)
        for nxt in sorted(adjacency.get(current, [])):
            if nxt == target:
                return True, path + [nxt]
            if nxt in collisions and nxt not in passable:
                continue
            frontier.append((nxt, path + [nxt]))
    return False, []


def build_responsibility_graph(
    events: Sequence[Event],
    physical_graph: Optional[GraphDocument] = None,
    formal_results: Optional[Mapping[str, Any]] = None,
    priority: Optional[Mapping[str, Any]] = None,
    cfg: Optional[Config] = None,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> Dict[str, Any]:
    """Build the normative graph for one run.

    ``physical_graph`` supplies causal relevance; ``formal_results`` supplies
    property failures; ``priority`` supplies the right-of-way benchmark verdict
    from :mod:`cdf.responsibility.priority`. All three are optional, and what is
    missing simply produces weaker evidence rather than a silent assumption.
    """
    cfg = cfg if cfg is not None else Config({})
    by_id = {e.event_id: e for e in events}
    participants = sorted({str(e.participant_id) for e in events})

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    def link(source: str, target: str, relation: str, why: str) -> None:
        edges.append({
            "source": source, "target": target, "relation": relation,
            "rationale": why,
        })

    # --- obligations, from what each vehicle actually saw -----------------
    obligations: Dict[str, List[str]] = {p: [] for p in participants}
    for event in sorted(events, key=lambda e: (float(e.t_peak), e.event_id)):
        kind = _type_of(event)
        pid = str(event.participant_id)
        if kind == EventType.STOP_SIGN_DETECTED.value:
            nid = "obl-stop-{0}-{1:.2f}".format(pid, float(event.t_peak))
            nodes.append(_node(
                nid, "STOP_REQUIRED", pid, float(event.t_peak),
                basis=[event.event_id], confidence=float(event.confidence),
                detail={"benchmark_rule": (
                    "a vehicle facing a stop sign must come to a complete stop "
                    "before the stop line"
                )},
            ))
            obligations[pid].append(nid)
        elif kind == EventType.YIELD_SIGN_DETECTED.value:
            nid = "obl-yield-{0}-{1:.2f}".format(pid, float(event.t_peak))
            nodes.append(_node(
                nid, "YIELD_REQUIRED", pid, float(event.t_peak),
                basis=[event.event_id], confidence=float(event.confidence),
                detail={"benchmark_rule": (
                    "a vehicle facing a yield sign must give way to conflicting "
                    "traffic before entering the conflict region"
                )},
            ))
            obligations[pid].append(nid)

    # --- violations: an obligation plus evidence it was not discharged ----
    violations: Dict[str, List[str]] = {p: [] for p in participants}

    def violation(
        node_type: str, pid: str, event: Event, obligation_id: Optional[str]
    ) -> None:
        nid = "vio-{0}-{1}-{2:.2f}".format(node_type[:4].lower(), pid,
                                           float(event.t_peak))
        nodes.append(_node(
            nid, node_type, pid, float(event.t_peak), subject=event.subject,
            basis=[event.event_id] + ([obligation_id] if obligation_id else []),
            confidence=float(event.confidence),
            detail=dict(event.detail or {}),
        ))
        violations[pid].append(nid)
        if obligation_id:
            link(obligation_id, nid, "UNDISCHARGED_BY",
                 "the obligation existed and the vehicle did not meet it")
        link(event.event_id, nid, "EVIDENCE_FOR",
             "the observed non-action is the evidence the rule was broken")

    for event in sorted(events, key=lambda e: (float(e.t_peak), e.event_id)):
        kind = _type_of(event)
        pid = str(event.participant_id)
        prior = [
            n for n in nodes
            if n["participant"] == pid and n["node_type"] in
            ("STOP_REQUIRED", "YIELD_REQUIRED")
            and n["t"] is not None and n["t"] <= float(event.t_peak)
        ]
        if kind == EventType.NO_STOP_AFTER_STOP_SIGN.value:
            stop_obligations = [n for n in prior if n["node_type"] == "STOP_REQUIRED"]
            violation("STOP_RULE_VIOLATION", pid, event,
                      stop_obligations[-1]["node_id"] if stop_obligations else None)
        elif kind == EventType.NO_YIELD_RESPONSE.value:
            yield_obligations = [
                n for n in prior if n["node_type"] == "YIELD_REQUIRED"
            ]
            violation("YIELD_RULE_VIOLATION", pid, event,
                      yield_obligations[-1]["node_id"] if yield_obligations else None)
        elif kind == EventType.SOLID_LINE_CROSSED.value:
            violation("SOLID_LINE_VIOLATION", pid, event, None)
        elif kind in (EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION.value,
                      EventType.CONTINUED_ACCELERATION_DURING_CONFLICT.value):
            # Both are the same normative failing seen from two sides: entering a
            # conflict without slowing, and going on accelerating once inside it.
            violation("UNSAFE_CONFLICT_ENTRY", pid, event, None)

    # --- mitigating behaviour --------------------------------------------
    # A response that reduced the severity of an outcome it did not cause.
    # Recorded because a report that listed only what each vehicle did wrong
    # would be a prosecution rather than a reconstruction.
    for event in sorted(events, key=lambda e: (float(e.t_peak), e.event_id)):
        kind = _type_of(event)
        if kind not in (EventType.HARD_BRAKE.value, EventType.BRAKE_ONSET.value,
                        EventType.HARD_DECELERATION.value,
                        EventType.STEER_ONSET.value):
            continue
        pid = str(event.participant_id)
        threat = [
            e for e in events
            if str(e.participant_id) == pid
            and _type_of(e) in (EventType.CRITICAL_TTC.value,
                                EventType.LOW_TTC.value)
            and 0.0 <= float(event.t_peak) - float(e.t_peak) <= 2.0
        ]
        if not threat:
            continue
        nid = "mit-{0}-{1:.2f}".format(pid, float(event.t_peak))
        nodes.append(_node(
            nid, "MITIGATING_RESPONSE", pid, float(event.t_peak),
            subject=threat[0].subject,
            basis=[event.event_id, threat[0].event_id],
            detail={"note": (
                "a response to a threat this vehicle was facing. Recorded as "
                "mitigating, which is not the same as establishing that it "
                "prevented anything"
            )},
        ))
        link(threat[0].event_id, nid, "PROMPTED",
             "the threat is what the response answered")

    # --- priority, where the benchmark could decide it --------------------
    if priority and priority.get("verdict"):
        verdict = str(priority["verdict"])
        if verdict == "AMBIGUOUS_PRIORITY":
            nodes.append(_node(
                "pri-ambiguous", "PRIORITY_AMBIGUOUS",
                participant=(priority.get("participants") or [""])[0],
                detail={"reason": priority.get("reason", ""),
                        "participants": priority.get("participants", [])},
                confidence=0.0,
            ))
        elif priority.get("has_priority"):
            nodes.append(_node(
                "pri-granted-{0}".format(priority["has_priority"]),
                "PRIORITY_GRANTED", str(priority["has_priority"]),
                detail={"reason": priority.get("reason", ""),
                        "benchmark_rule": priority.get("benchmark_rule", "")},
            ))

    # --- contribution: a violation *and* a physical path ------------------
    outcome_ids = sorted(
        e.event_id for e in events
        if _type_of(e) in (EventType.COLLISION.value, EventType.NEAR_MISS.value)
    )
    collision_ids = {
        e.event_id for e in events if _type_of(e) == EventType.COLLISION.value
    }
    adjacency = _adjacency(physical_graph)

    contributions: Dict[str, Dict[str, Any]] = {}
    for pid in participants:
        own_behaviour = {
            e.event_id for e in events
            if str(e.participant_id) == pid and _type_of(e) in _OWN_BEHAVIOUR_TYPES
        }
        passable = _collisions_own_behaviour_reaches(
            adjacency, own_behaviour, collision_ids
        )
        # Per outcome, not pooled. In a chain a vehicle can be a contributor to
        # the impact it caused and not to the one it was shunted into, and a
        # single yes/no over all outcomes would lose exactly that distinction --
        # which is the distinction the chain scenarios exist to test.
        per_outcome: Dict[str, Any] = {}
        path: List[str] = []
        for outcome in outcome_ids:
            reached, route = _reaches(
                adjacency, own_behaviour, outcome, collision_ids, passable
            )
            per_outcome[outcome] = {"reached": reached, "path": route}
            if reached and not path:
                path = route
        reachable = any(v["reached"] for v in per_outcome.values())

        failures = _property_failures(formal_results, pid)
        has_violation = bool(violations[pid])
        contributions[pid] = {
            "physically_relevant": reachable,
            "path": path,
            "outcomes": per_outcome,
            "outcomes_reached": sorted(
                k for k, v in per_outcome.items() if v["reached"]
            ),
            "outcomes_not_reached": sorted(
                k for k, v in per_outcome.items() if not v["reached"]
            ),
            "impacts_this_vehicle_caused": sorted(passable),
            "normative_violations": list(violations[pid]),
            "property_failures": failures,
        }
        if reachable and (has_violation or failures):
            nid = "contrib-{0}".format(pid)
            nodes.append(_node(
                nid, "RESPONSIBILITY_CONTRIBUTION", pid,
                basis=list(violations[pid]) + [f["property_id"] for f in failures],
                detail={
                    "physical_path": path,
                    "outcomes_reached": contributions[pid]["outcomes_reached"],
                    "outcomes_not_reached":
                        contributions[pid]["outcomes_not_reached"],
                    "requires": (
                        "both a normative violation and an independent physical "
                        "path from this vehicle's own behaviour to the outcome"
                    ),
                    "not_a_fault_finding": (
                        "a contribution to the causal and normative account of "
                        "the incident. Not a finding of legal fault, and not a "
                        "share of anything"
                    ),
                },
            ))
            for source in violations[pid]:
                link(source, nid, "SUPPORTS",
                     "the rule that was broken")
            if path:
                link(path[0], nid, "PHYSICALLY_RELEVANT_VIA",
                     "the vehicle's own behaviour reaches the outcome in the "
                     "physical graph without passing through an impact it received")

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "graph_kind": "responsibility",
        "scope": Provenance.FUSED.value,
        "run_id": run_id,
        "scenario_id": scenario_id,
        "seed": int(seed),
        "participants": participants,
        "node_types": list(RESPONSIBILITY_NODE_TYPES),
        "nodes": nodes,
        "edges": edges,
        "per_participant": contributions,
        "note": (
            "normative reasoning, kept apart from the physical graph on purpose: "
            "a reader must be able to accept the physics and dispute the norm. "
            "A responsibility contribution requires both a rule that was broken "
            "and a physical path from the vehicle's own behaviour to the "
            "outcome; neither alone is enough. This is never a finding of "
            "legal fault"
        ),
    }


def _property_failures(
    formal_results: Optional[Mapping[str, Any]], participant: str
) -> List[Dict[str, Any]]:
    """Temporal-property violations attributable to one vehicle."""
    if not formal_results:
        return []
    out: List[Dict[str, Any]] = []
    for result in formal_results.get("results", []) or []:
        if result.get("status") != CheckStatus.FAIL.value:
            continue
        instances = [
            i for i in result.get("instances", []) or []
            if i.get("status") == CheckStatus.FAIL.value
            and str(i.get("participant")) == str(participant)
        ]
        if instances:
            out.append({
                "property_id": result["property_id"],
                "title": result.get("title", ""),
                "n_failing_instances": len(instances),
                "first_at": instances[0].get("t"),
                "benchmark_rule": result.get("benchmark_rule"),
            })
    return out
