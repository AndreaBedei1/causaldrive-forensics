"""The contract that makes a reconstruction and the ground truth comparable.

A structural metric compares two graphs. It is only meaningful if both graphs are
*allowed to say the same things*, and until this module existed they were not.

The privileged oracle emitted ``ORACLE_SCRIPTED_INTERVENTION`` -- a record that
the scenario script fired -- and ``ORACLE_RIGHT_OF_WAY_CONFLICT``, which is a
judgement about traffic law. No reconstruction built from telemetry, controls and
radar has any node of either kind, so every edge touching one was unmatchable no
matter how well the incident was reconstructed. Meanwhile the reconstruction
emitted fifteen event types the oracle never produced, so every one of those was
counted as a false positive. The comparison was unfair in both directions at
once, and the resulting F1 measured the vocabulary gap rather than the method.

This module states the vocabulary the two sides share, and classifies every type
that is *not* shared into the reason it is not:

**Comparable** -- a physical fact about the world that both an exact simulator
trace and an onboard reconstruction can assert. These are the only types that
take part in the primary graph comparison.

**Sensor-relative** -- a fact about an instrument rather than the world. A radar
track appearing is real and worth recording, but there is no privileged
counterpart to it: the simulator has no radar tracks, it has vehicles. These are
excluded from the primary comparison rather than counted as errors.

**Design-reference** -- privileged knowledge of what the scenario *intended*.
Kept, because "did the designed mechanism actually execute?" is a real question,
and answered against the scenario design reference rather than against the
reconstruction.

The same three-way split applies to causal relations, though there the shared
vocabulary is the whole of it.

Nothing here is a translation table. :mod:`cdf.graph.canonical` is that, and it
stays for genuinely equivalent intensity variants -- ``DECELERATION`` against
``HARD_DECELERATION`` -- which is a much smaller claim than mapping a scripted
intervention onto a physical brake.
"""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional, Tuple

from ..common.schemas import CausalEdgeType, EventType

__all__ = [
    "COMPARABLE_EVENT_TYPES",
    "SENSOR_RELATIVE_EVENT_TYPES",
    "DESIGN_REFERENCE_EVENT_TYPES",
    "COMPARABLE_EDGE_TYPES",
    "OWN_MOTION_TYPES",
    "PAIRWISE_TYPES",
    "ROAD_CONTROL_TYPES",
    "NON_ACTION_TYPES",
    "OUTCOME_TYPES",
    "SUBJECT_SEMANTICS",
    "is_comparable",
    "exclusion_reason",
    "comparable_view",
    "describe",
]


# ---------------------------------------------------------------------------
# What a vehicle does, observable from its own controls and motion alone
# ---------------------------------------------------------------------------

#: One vehicle, no subject. The oracle reads these from exact controls and exact
#: velocity; a vehicle reads them from its own controls and its own telemetry.
#: Same fact, different instrument.
OWN_MOTION_TYPES: FrozenSet[str] = frozenset({
    EventType.VEHICLE_STARTED.value,
    EventType.ACCELERATION.value,
    EventType.DECELERATION.value,
    EventType.HARD_DECELERATION.value,
    EventType.BRAKE_ONSET.value,
    EventType.HARD_BRAKE.value,
    EventType.THROTTLE_ONSET.value,
    EventType.STEER_ONSET.value,
    EventType.SIGNIFICANT_HEADING_CHANGE.value,
    EventType.LANE_CHANGE_LIKE_MANEUVER.value,
    EventType.FULL_STOP.value,
})

# ---------------------------------------------------------------------------
# What the vehicle met on the road
# ---------------------------------------------------------------------------

#: Traffic control and road geometry, as *observed*. Both sides may assert these
#: and they mean the same thing on both sides, but they are reached by genuinely
#: different routes: the vehicle reads a sign off its camera and a marking
#: crossing off its lane sensor, while the privileged reference reads both off
#: the exact map. That difference is the point -- it is what makes perception
#: precision and recall a real measurement rather than a tautology.
ROAD_CONTROL_TYPES: FrozenSet[str] = frozenset({
    EventType.STOP_SIGN_DETECTED.value,
    EventType.YIELD_SIGN_DETECTED.value,
    EventType.STOP_LINE_DETECTED.value,
    EventType.STOP_LINE_CROSSED.value,
    EventType.LANE_MARKING_CROSSED.value,
    EventType.SOLID_LINE_CROSSED.value,
    EventType.ROAD_BOUNDARY_CROSSED.value,
})

# ---------------------------------------------------------------------------
# What did not happen
# ---------------------------------------------------------------------------

#: An assertion that a required response was absent. Comparable, because the
#: privileged reference derives the same claims from exact state and exact
#: traffic control -- and because a method that invented non-actions would then
#: be caught by precision rather than rewarded.
#:
#: These are the only event types whose *absence of a signal* is the claim, so
#: they carry a monitored interval and an evidence-coverage figure in
#: ``detail``. A non-action with insufficient coverage is not emitted at all.
NON_ACTION_TYPES: FrozenSet[str] = frozenset({
    EventType.NO_STOP_AFTER_STOP_SIGN.value,
    EventType.NO_BRAKING_RESPONSE.value,
    EventType.NO_YIELD_RESPONSE.value,
    EventType.NO_EVASIVE_RESPONSE.value,
    EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION.value,
    EventType.CONTINUED_ACCELERATION_DURING_CONFLICT.value,
})

# ---------------------------------------------------------------------------
# What is true of a pair of vehicles
# ---------------------------------------------------------------------------

#: Two vehicles: ``participant_id`` observes, ``subject`` is observed. The oracle
#: computes these from exact relative geometry; a vehicle computes them from
#: radar returns it has resolved to a track. Same relation, different evidence.
PAIRWISE_TYPES: FrozenSet[str] = frozenset({
    EventType.RANGE_DECREASING.value,
    EventType.RAPID_CLOSING.value,
    EventType.LOW_TTC.value,
    EventType.CRITICAL_TTC.value,
    EventType.LATERAL_CROSSING.value,
    EventType.CUT_IN_LIKE_MOTION.value,
    EventType.PREDICTED_PATH_CONFLICT.value,
    EventType.CONFLICT_REGION_ENTRY.value,
})

#: What the encounter came to.
OUTCOME_TYPES: FrozenSet[str] = frozenset({
    EventType.NEAR_MISS.value,
    EventType.COLLISION.value,
    EventType.POST_IMPACT_STOP.value,
})

#: The primary comparison vocabulary: every type both sides may assert.
COMPARABLE_EVENT_TYPES: FrozenSet[str] = (
    OWN_MOTION_TYPES | PAIRWISE_TYPES | ROAD_CONTROL_TYPES
    | NON_ACTION_TYPES | OUTCOME_TYPES
)


# ---------------------------------------------------------------------------
# Excluded, and why
# ---------------------------------------------------------------------------

#: Facts about an instrument, not about the world. A radar track appearing tells
#: you something real about what a vehicle could see; it has no counterpart in a
#: simulator trace, which has vehicles rather than tracks. Excluded from the
#: primary comparison instead of scored as a false positive.
#:
#: ``TARGET_DECELERATION`` belongs here for a subtler reason: it is A's
#: *observation* that a track it is following slowed down. The physical fact
#: underneath it is B's own ``DECELERATION``, which both sides do emit, so the
#: canonical layer maps the two together and the primary comparison does not
#: need this type of its own.
SENSOR_RELATIVE_EVENT_TYPES: FrozenSet[str] = frozenset({
    EventType.RADAR_TRACK_APPEARED.value,
    EventType.RADAR_TRACK_LOST.value,
    EventType.TARGET_DECELERATION.value,
})

#: Privileged knowledge of what the scenario meant to do. These belong to the
#: scenario design reference, which answers "did the designed mechanism
#: execute?" -- a real question, and a different one from "was the incident
#: reconstructed?".
DESIGN_REFERENCE_EVENT_TYPES: FrozenSet[str] = frozenset({
    EventType.ORACLE_SCRIPTED_INTERVENTION.value,
    EventType.ORACLE_RIGHT_OF_WAY_CONFLICT.value,
    EventType.ORACLE_SIGNAL_VIOLATION.value,
})

#: Causal relations. Unlike the node vocabulary, this one was already shared:
#: local, fused and oracle all draw from the same five.
COMPARABLE_EDGE_TYPES: FrozenSet[str] = frozenset(
    e.value for e in CausalEdgeType
)


#: What ``participant_id`` and ``subject`` mean for each family, so a matcher
#: can decide identity without guessing.
SUBJECT_SEMANTICS: Dict[str, str] = {
    "own_motion": (
        "participant_id is the vehicle the event is about; subject is unused "
        "and must be None"
    ),
    "pairwise": (
        "participant_id is the observer, subject is the observed vehicle; the "
        "event is about the ordered pair"
    ),
    "outcome": (
        "participant_id and subject are the two vehicles involved; the pair is "
        "unordered and a matcher must treat (A,B) and (B,A) as the same event"
    ),
    "road_control": (
        "participant_id is the vehicle that met the sign, line or marking; "
        "subject is unused, because the other party is the road and not a "
        "vehicle"
    ),
    "non_action": (
        "participant_id is the vehicle that did not respond. subject names the "
        "vehicle it failed to respond to when the obligation arose from another "
        "vehicle, and is unused when the obligation came from traffic control"
    ),
}


def _value(event_type: Any) -> str:
    return event_type.value if hasattr(event_type, "value") else str(event_type)


def is_comparable(event_type: Any) -> bool:
    """Whether this type takes part in the primary graph comparison."""
    return _value(event_type) in COMPARABLE_EVENT_TYPES


def family(event_type: Any) -> Optional[str]:
    """Which comparable family a type belongs to, or ``None`` if it is not one.

    One of ``own_motion``, ``pairwise``, ``road_control``, ``non_action`` or
    ``outcome``. :data:`SUBJECT_SEMANTICS` says what ``participant_id`` and
    ``subject`` mean in each.
    """
    value = _value(event_type)
    if value in OWN_MOTION_TYPES:
        return "own_motion"
    if value in PAIRWISE_TYPES:
        return "pairwise"
    if value in ROAD_CONTROL_TYPES:
        return "road_control"
    if value in NON_ACTION_TYPES:
        return "non_action"
    if value in OUTCOME_TYPES:
        return "outcome"
    return None


def exclusion_reason(event_type: Any) -> Optional[str]:
    """Why this type is not compared, or ``None`` when it is.

    A metric that silently drops a node is a metric that can be gamed by
    emitting more of whatever it drops, so every exclusion has a stated reason
    and the reason travels into the diff artifact.
    """
    value = _value(event_type)
    if value in COMPARABLE_EVENT_TYPES:
        return None
    if value in SENSOR_RELATIVE_EVENT_TYPES:
        return (
            "sensor-relative: a fact about an instrument rather than about the "
            "world, with no privileged counterpart to compare against"
        )
    if value in DESIGN_REFERENCE_EVENT_TYPES:
        return (
            "design reference: privileged knowledge of what the scenario "
            "intended, scored against the scenario design reference rather "
            "than against a reconstruction"
        )
    return "not declared in the comparable ontology"


def comparable_view(doc: Any) -> Any:
    """A copy of a graph document holding only its comparable part.

    Nodes outside the shared vocabulary are dropped, and so is any edge that
    touched one -- an edge whose endpoint is gone is not an edge. The dropped
    counts are recorded in ``meta["ontology"]`` so a reader can see what the
    primary comparison did and did not look at.
    """
    import dataclasses

    if doc is None:
        return None
    kept = [n for n in doc.nodes if is_comparable(n.event_type)]
    kept_ids = {n.event_id for n in kept}
    edges = [e for e in doc.edges if e.source in kept_ids and e.target in kept_ids]

    dropped_nodes: Dict[str, int] = {}
    for node in doc.nodes:
        if node.event_id in kept_ids:
            continue
        dropped_nodes[_value(node.event_type)] = (
            dropped_nodes.get(_value(node.event_type), 0) + 1
        )

    meta = dict(doc.meta or {})
    meta["ontology"] = {
        "applied": "comparable_view",
        "n_nodes_kept": len(kept),
        "n_nodes_dropped": len(doc.nodes) - len(kept),
        "n_edges_kept": len(edges),
        "n_edges_dropped": len(doc.edges) - len(edges),
        "dropped_node_types": dict(sorted(dropped_nodes.items())),
        "reasons": {
            t: exclusion_reason(t) for t in sorted(dropped_nodes)
        },
        "note": (
            "the primary comparison is over the vocabulary both a privileged "
            "trace and an onboard reconstruction can assert; what was left out "
            "is listed here rather than silently discarded"
        ),
    }
    return dataclasses.replace(doc, nodes=kept, edges=edges, meta=meta)


def describe() -> Dict[str, Any]:
    """The contract, as data, for artifacts and tests."""
    return {
        "comparable_event_types": sorted(COMPARABLE_EVENT_TYPES),
        "comparable_edge_types": sorted(COMPARABLE_EDGE_TYPES),
        "families": {
            "own_motion": sorted(OWN_MOTION_TYPES),
            "pairwise": sorted(PAIRWISE_TYPES),
            "outcome": sorted(OUTCOME_TYPES),
        },
        "subject_semantics": dict(SUBJECT_SEMANTICS),
        "excluded": {
            "sensor_relative": sorted(SENSOR_RELATIVE_EVENT_TYPES),
            "design_reference": sorted(DESIGN_REFERENCE_EVENT_TYPES),
        },
        "note": (
            "the primary graph comparison uses comparable_event_types only. A "
            "type outside it is excluded with a stated reason rather than "
            "counted as an error, because a reconstruction cannot be penalised "
            "for failing to emit something no reconstruction could emit, and a "
            "reference cannot be credited for asserting something no "
            "reconstruction could check"
        ),
    }
