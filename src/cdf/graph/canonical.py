"""A canonical vocabulary for comparing graphs that were written by different layers.

The problem this solves
-----------------------

Three layers describe the same incident and each names things in its own terms.
The privileged oracle knows a *scripted action* fired and emits
``ORACLE_SCRIPTED_INTERVENTION``; the vehicle that executed it recorded a
``HARD_BRAKE`` command; both are the same physical fact. The strict structural
metric requires an exact type match, so the oracle edge

    ORACLE_SCRIPTED_INTERVENTION(B, "B_emergency_brake") --CONTRIBUTES_TO--> RANGE_DECREASING(A)

can never be matched by the reconstruction's

    HARD_BRAKE(B) --CONTRIBUTES_TO--> RANGE_DECREASING(A, B)

even when the reconstruction is exactly right. Across the nine scenarios most
oracle edges have a scripted action as their cause, so a large part of edge
recall is unreachable by vocabulary rather than by reconstruction quality.

What this module does, and what it deliberately does not do
-----------------------------------------------------------

:func:`canonicalise` returns a *copy* of a graph whose node types are replaced by
the family they belong to and whose edge types are replaced by their relation
family. Feeding two canonicalised graphs to the ordinary matcher then compares
what the claims *mean* rather than what they are called.

This is **evaluation-only**. It is never applied to a fused artifact, it never
travels back into inference, and it does not copy the oracle's rules into the
fusion layer: it is a translation table between vocabularies, applied
symmetrically to both sides.

It is also, unavoidably, a **weaker** test than the strict one. Collapsing
``LOW_TTC`` and ``CRITICAL_TTC`` into one family, or the four positive relations
into ``positive_contribution``, forgives distinctions a reconstruction might have
got wrong. For that reason the canonical numbers are always reported *beside* the
strict ones, never instead of them, and the strict numbers remain the headline
result. A reader who distrusts the translation can read the strict column and
ignore this one.
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, Optional

from ..common.schemas import CausalEdgeType, Event, EventType, GraphDocument

__all__ = [
    "NODE_FAMILIES",
    "EDGE_FAMILIES",
    "ACTION_KIND_FAMILIES",
    "canonical_node_family",
    "canonical_edge_family",
    "canonicalise",
]


#: Event types that make the same kind of physical claim. A family is only worth
#: having when a *different layer* would legitimately use a different member of
#: it for the same fact; unlisted types keep their own name and so still only
#: match themselves.
NODE_FAMILIES: Dict[str, str] = {
    # a commanded braking input
    EventType.BRAKE_ONSET.value: "braking_command",
    EventType.HARD_BRAKE.value: "braking_command",
    # the resulting loss of speed, however it was measured
    EventType.DECELERATION.value: "deceleration",
    EventType.HARD_DECELERATION.value: "deceleration",
    EventType.TARGET_DECELERATION.value: "deceleration",
    # a commanded or measured gain of speed
    EventType.THROTTLE_ONSET.value: "speed_increase",
    EventType.ACCELERATION.value: "speed_increase",
    EventType.VEHICLE_STARTED.value: "speed_increase",
    # moving across, or out of, the current path
    EventType.STEER_ONSET.value: "lateral_manoeuvre",
    EventType.SIGNIFICANT_HEADING_CHANGE.value: "lateral_manoeuvre",
    EventType.LANE_CHANGE_LIKE_MANEUVER.value: "lateral_manoeuvre",
    EventType.CUT_IN_LIKE_MOTION.value: "lateral_manoeuvre",
    # the gap between two vehicles shortening
    EventType.RANGE_DECREASING.value: "closing",
    EventType.RAPID_CLOSING.value: "closing",
    # the margin to contact collapsing
    EventType.LOW_TTC.value: "ttc_risk",
    EventType.CRITICAL_TTC.value: "ttc_risk",
    # two paths that will meet
    EventType.PREDICTED_PATH_CONFLICT.value: "path_conflict",
    EventType.CONFLICT_REGION_ENTRY.value: "path_conflict",
    EventType.LATERAL_CROSSING.value: "path_conflict",
    # outcomes keep their own identity: collapsing these would forgive the one
    # distinction a forensic reconstruction may never get wrong.
    EventType.COLLISION.value: "collision",
    EventType.NEAR_MISS.value: "near_miss",
    EventType.POST_IMPACT_STOP.value: "post_impact_stop",
    # observation, never a claim about behaviour
    EventType.RADAR_TRACK_APPEARED.value: "observation",
    EventType.RADAR_TRACK_LOST.value: "observation",
}


#: A scripted action is privileged knowledge of a command. The vehicle that
#: executed it recorded the command itself, so the two belong in one family --
#: chosen from the action's own declared kind, not from its name.
ACTION_KIND_FAMILIES: Dict[str, str] = {
    "brake": "braking_command",
    "set_speed": "speed_increase",
    "lane_shift": "lateral_manoeuvre",
    "steer": "lateral_manoeuvre",
}


#: Relation families. The four positive relations differ in strength, not in
#: direction; prevention is the one distinction that must survive, because a
#: system that confuses "contributed to the crash" with "prevented the crash"
#: has got the only thing that matters backwards.
EDGE_FAMILIES: Dict[str, str] = {
    CausalEdgeType.CONTRIBUTES_TO.value: "positive_contribution",
    CausalEdgeType.TRIGGERS.value: "positive_contribution",
    CausalEdgeType.INCREASES_RISK_OF.value: "positive_contribution",
    CausalEdgeType.CAUSES_OUTCOME.value: "positive_contribution",
    CausalEdgeType.PREVENTS.value: "preventive",
}


def _type_value(event_type: Any) -> str:
    return event_type.value if isinstance(event_type, EventType) else str(event_type)


def _action_kind(node: Event) -> str:
    """The declared kind of a scripted-action node, from its own record."""
    for ev in node.evidence or []:
        kind = str((ev.detail or {}).get("action_kind") or "").strip().lower()
        if kind:
            return kind
    values = node.values or {}
    for flag, kind in (
        ("kind_is_brake", "brake"),
        ("kind_is_speed", "set_speed"),
        ("kind_is_lateral", "lane_shift"),
    ):
        try:
            if float(values.get(flag, 0.0)) > 0.0:
                return kind
        except (TypeError, ValueError):
            continue
    return ""


def canonical_node_family(node: Event) -> str:
    """The canonical family of one node, or its own type when it has none."""
    type_value = _type_value(node.event_type)
    if type_value == EventType.ORACLE_SCRIPTED_INTERVENTION.value:
        kind = _action_kind(node)
        mapped = ACTION_KIND_FAMILIES.get(kind)
        if mapped is not None:
            return mapped
        # An action whose kind is unknown stays distinct rather than being
        # forced into a family it may not belong to.
        return "scripted_action"
    return NODE_FAMILIES.get(type_value, type_value)


def canonical_edge_family(edge_type: Any) -> str:
    value = edge_type.value if hasattr(edge_type, "value") else str(edge_type)
    return EDGE_FAMILIES.get(value, value)


def canonicalise(doc: Optional[GraphDocument]) -> Optional[GraphDocument]:
    """A copy of ``doc`` restated in the canonical vocabulary.

    Node ``event_type`` and edge ``edge_type`` become family labels; everything
    else -- ids, participants, subjects, timestamps, confidences, evidence -- is
    untouched, so the matcher's tolerance, tie-breaks and subject handling behave
    exactly as they do on the strict comparison.
    """
    if doc is None:
        return None
    nodes = []
    for node in doc.nodes:
        family = canonical_node_family(node)
        values = dict(node.values or {})
        nodes.append(
            dataclasses.replace(
                node,
                event_type=family,
                values=values,
            )
        )
    edges = [
        dataclasses.replace(edge, edge_type=canonical_edge_family(edge.edge_type))
        for edge in doc.edges
    ]
    meta = dict(doc.meta or {})
    meta["canonical_vocabulary"] = {
        "applied": True,
        "note": (
            "evaluation-only restatement of node and edge types into semantic "
            "families; see cdf.graph.canonical"
        ),
    }
    return GraphDocument(
        graph_kind=doc.graph_kind,
        scope=doc.scope,
        owner=doc.owner,
        run_id=doc.run_id,
        scenario_id=doc.scenario_id,
        seed=doc.seed,
        nodes=nodes,
        edges=edges,
        meta=meta,
    )
