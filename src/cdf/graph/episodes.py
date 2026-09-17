"""Behavioural episodes: what a vehicle *did*, read off the fused graph.

An attribution that names ``B_emergency_brake`` is naming a line of a scenario
file. A forensic reconstruction has to name something it can see in the evidence:
*this vehicle braked hard, here, and the gap ahead of it was closing at the
time*. A :class:`CausalEpisode` is that -- one stretch of one vehicle's observed
behaviour, with a physical label, an interval on the common clock, the fused
nodes that support it and a confidence inherited from them.

The vocabulary is deliberately physical and deliberately small
(:data:`EPISODE_KINDS`). In particular there is no ``failure_to_yield``: right of
way is a rule of the road, and this project models no rules of the road. What the
evidence supports is ``conflict_entry_without_deceleration`` -- the vehicle
entered a region its own sensors had already flagged as conflicting, and it did
not slow down. That is a statement about physics, and it is the honest form of
the same observation.

Nothing here reads a scenario, a variant, an action id or an oracle artifact.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.schemas import Event, EventType, GraphDocument

__all__ = ["CausalEpisode", "EPISODE_KINDS", "extract_episodes"]


#: The closed vocabulary. Each entry is a description of motion, not of duty.
EPISODE_KINDS: Tuple[str, ...] = (
    "emergency_braking",
    "braking_response",
    "late_braking_response",
    "sustained_acceleration",
    "lane_change_like_motion",
    "conflict_entry_without_deceleration",
    "closing_without_deceleration",
    "defensive_stop",
)

_BRAKE_HARD = frozenset(
    {EventType.HARD_BRAKE.value, EventType.HARD_DECELERATION.value}
)
_BRAKE_SOFT = frozenset(
    {EventType.BRAKE_ONSET.value, EventType.DECELERATION.value,
     EventType.TARGET_DECELERATION.value}
)
_BRAKING = _BRAKE_HARD | _BRAKE_SOFT
_SPEED_UP = frozenset(
    {EventType.THROTTLE_ONSET.value, EventType.ACCELERATION.value}
)
_LATERAL = frozenset(
    {EventType.LANE_CHANGE_LIKE_MANEUVER.value, EventType.CUT_IN_LIKE_MOTION.value,
     EventType.SIGNIFICANT_HEADING_CHANGE.value}
)
_CONFLICT_ENTRY = frozenset({EventType.CONFLICT_REGION_ENTRY.value})
_CLOSING = frozenset(
    {EventType.RANGE_DECREASING.value, EventType.RAPID_CLOSING.value}
)
_TTC_RISK = frozenset({EventType.LOW_TTC.value, EventType.CRITICAL_TTC.value})
_CRITICAL = frozenset({EventType.CRITICAL_TTC.value})
_NEAR_MISS = frozenset({EventType.NEAR_MISS.value})
_COLLISION = frozenset({EventType.COLLISION.value})


@dataclass
class CausalEpisode:
    """One stretch of one vehicle's observed behaviour."""

    episode_id: str
    participant_id: str
    kind: str
    t_start: float
    t_peak: float
    t_end: float
    node_ids: List[str]
    confidence: float
    #: The other vehicles this episode is about, when it is inherently relational
    #: (entering a conflict region concerns a pair).
    counterparts: List[str] = field(default_factory=list)
    description: str = ""
    detail: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "episode_id": self.episode_id,
            "participant_id": self.participant_id,
            "kind": self.kind,
            "t_start": round(float(self.t_start), 6),
            "t_peak": round(float(self.t_peak), 6),
            "t_end": round(float(self.t_end), 6),
            "node_ids": list(self.node_ids),
            "confidence": round(float(self.confidence), 6),
            "counterparts": list(self.counterparts),
            "description": self.description,
            "detail": dict(self.detail),
            "time_domain": "common",
        }


def _type_of(node: Event) -> str:
    return node.event_type.value if isinstance(node.event_type, EventType) else str(
        node.event_type
    )


def _vehicles(node: Event, participants: Set[str]) -> Tuple[str, List[str]]:
    """``(actor, counterparts)`` for a fused node, from its resolved subject."""
    observer = str(node.participant_id)
    subject = node.subject
    if subject in (None, "", "self") or str(subject) not in participants:
        return observer, []
    subject_s = str(subject)
    type_value = _type_of(node)
    if type_value in (_CLOSING | _TTC_RISK | _CONFLICT_ENTRY | _NEAR_MISS | _COLLISION):
        # Relational: the claim is about the pair; the actor is the observer.
        return observer, [subject_s]
    # Unary event about another vehicle: that vehicle is the actor.
    return subject_s, []


def extract_episodes(
    fused: GraphDocument, cfg: Config, participants: Sequence[str]
) -> List[CausalEpisode]:
    """Group the fused nodes into behavioural episodes, one vehicle at a time.

    Adjacent nodes of the same behaviour and the same vehicle, closer than
    ``graph.episodes.merge_gap_s``, are one episode: a brake command and the
    deceleration it produced are one act of braking, not two.
    """
    gap = float(cfg.get("graph.episodes.merge_gap_s", 1.5))
    late_margin = float(cfg.get("graph.episodes.late_response_margin_s", 0.0))
    quiet = float(cfg.get("graph.episodes.no_response_window_s", 2.5))
    known = set(str(p) for p in participants)

    nodes = sorted(fused.nodes, key=lambda n: (float(n.t_peak), n.event_id))
    typed: List[Tuple[Event, str, str, List[str]]] = []
    for node in nodes:
        actor, counterparts = _vehicles(node, known)
        typed.append((node, _type_of(node), actor, counterparts))

    # Per-vehicle indices the classifiers need.
    braking_times: Dict[str, List[float]] = {}
    critical_times: Dict[str, List[float]] = {}
    for node, type_value, actor, _counterparts in typed:
        if type_value in _BRAKING:
            braking_times.setdefault(actor, []).append(float(node.t_start))
        if type_value in _CRITICAL:
            critical_times.setdefault(actor, []).append(float(node.t_start))
    near_miss_pairs: List[Tuple[float, Set[str]]] = [
        (float(n.t_peak), {a} | set(c))
        for n, t, a, c in typed
        if t in _NEAR_MISS
    ]
    collision_pairs: List[Tuple[float, Set[str]]] = [
        (float(n.t_peak), {a} | set(c))
        for n, t, a, c in typed
        if t in _COLLISION
    ]

    episodes: List[CausalEpisode] = []
    open_groups: Dict[Tuple[str, str], List[Tuple[Event, List[str]]]] = {}

    def flush(key: Tuple[str, str]) -> None:
        group = open_groups.pop(key, None)
        if not group:
            return
        actor, bucket = key
        members = [n for n, _c in group]
        counterparts = sorted({c for _n, cs in group for c in cs})
        t_start = min(float(n.t_start) for n in members)
        t_end = max(float(n.t_end if n.t_end is not None else n.t_peak) for n in members)
        t_peak = min(float(n.t_peak) for n in members)
        confidence = max(float(n.confidence) for n in members)
        kind, description, detail = _classify(
            bucket,
            actor,
            counterparts,
            members,
            t_start,
            braking_times,
            critical_times,
            near_miss_pairs,
            collision_pairs,
            late_margin,
            quiet,
            typed,
        )
        if kind is None:
            return
        episodes.append(
            CausalEpisode(
                episode_id="episode:{0}:{1}:{2:.3f}".format(actor, kind, t_start),
                participant_id=actor,
                kind=kind,
                t_start=t_start,
                t_peak=t_peak,
                t_end=t_end,
                node_ids=sorted(n.event_id for n in members),
                confidence=confidence,
                counterparts=counterparts,
                description=description,
                detail=detail,
            )
        )

    for node, type_value, actor, counterparts in typed:
        bucket = _bucket(type_value)
        if bucket is None:
            continue
        key = (actor, bucket)
        current = open_groups.get(key)
        if current is not None:
            last = current[-1][0]
            last_end = float(last.t_end if last.t_end is not None else last.t_peak)
            if float(node.t_start) - last_end > gap:
                flush(key)
                current = None
        open_groups.setdefault(key, []).append((node, counterparts))

    for key in list(open_groups):
        flush(key)

    episodes.sort(key=lambda e: (e.t_start, e.participant_id, e.kind))
    return episodes


def _bucket(type_value: str) -> Optional[str]:
    """Which behavioural bucket a node type belongs to, if any."""
    if type_value in _BRAKING:
        return "braking"
    if type_value in _SPEED_UP:
        return "speed_up"
    if type_value in _LATERAL:
        return "lateral"
    if type_value in _CONFLICT_ENTRY:
        return "conflict_entry"
    if type_value in _CLOSING:
        return "closing"
    return None


def _classify(
    bucket: str,
    actor: str,
    counterparts: Sequence[str],
    members: Sequence[Event],
    t_start: float,
    braking_times: Mapping[str, Sequence[float]],
    critical_times: Mapping[str, Sequence[float]],
    near_miss_pairs: Sequence[Tuple[float, Set[str]]],
    collision_pairs: Sequence[Tuple[float, Set[str]]],
    late_margin: float,
    quiet: float,
    typed: Sequence[Tuple[Event, str, str, List[str]]],
) -> Tuple[Optional[str], str, Dict[str, Any]]:
    """Name the behaviour, and say in words what the evidence shows."""
    types = {_type_of(n) for n in members}
    detail: Dict[str, Any] = {"node_types": sorted(types)}

    if bucket == "braking":
        hard = bool(types & _BRAKE_HARD)
        criticals = [t for t in critical_times.get(actor, ()) if t <= t_start]
        resolved = [
            t for t, pair in near_miss_pairs
            if actor in pair and t >= t_start - quiet
        ]
        # Braking is only *defensive* if the encounter it answered ended without
        # contact. A vehicle that braked and then collided anyway did not make a
        # defensive stop, whatever near miss it had survived earlier.
        struck = [
            t for t, pair in collision_pairs
            if actor in pair and t >= t_start - quiet
        ]
        if criticals:
            detail["critical_ttc_at_s"] = round(max(criticals), 6)
            detail["response_lag_s"] = round(t_start - max(criticals), 6)
            if t_start > max(criticals) + late_margin:
                return (
                    "late_braking_response",
                    "{0} braked {1:.2f}s after its own time-to-collision had already "
                    "become critical".format(actor, t_start - max(criticals)),
                    detail,
                )
        if resolved and not struck:
            detail["near_miss_at_s"] = round(min(resolved), 6)
            return (
                "defensive_stop",
                "{0} braked and the encounter ended without contact".format(actor),
                detail,
            )
        if struck:
            detail["collision_at_s"] = round(min(struck), 6)
        if hard:
            return (
                "emergency_braking",
                "{0} applied hard braking".format(actor),
                detail,
            )
        return ("braking_response", "{0} braked".format(actor), detail)

    if bucket == "speed_up":
        return (
            "sustained_acceleration",
            "{0} accelerated".format(actor),
            detail,
        )

    if bucket == "lateral":
        return (
            "lane_change_like_motion",
            "{0} moved laterally out of its path".format(actor),
            detail,
        )

    if bucket == "conflict_entry":
        braked = [
            t for t in braking_times.get(actor, ()) if t_start - quiet <= t <= t_start
        ]
        detail["braking_before_entry"] = [round(t, 6) for t in braked]
        if braked:
            return (None, "", detail)
        return (
            "conflict_entry_without_deceleration",
            "{0} entered a region its own sensors had flagged as conflicting with "
            "{1} and did not slow down beforehand".format(
                actor, ", ".join(counterparts) or "another vehicle"
            ),
            detail,
        )

    if bucket == "closing":
        braked = [t for t in braking_times.get(actor, ()) if t >= t_start - quiet]
        detail["braking_after_closing"] = [round(t, 6) for t in braked]
        if braked:
            return (None, "", detail)
        return (
            "closing_without_deceleration",
            "{0} kept closing on {1} without braking".format(
                actor, ", ".join(counterparts) or "another vehicle"
            ),
            detail,
        )

    return (None, "", detail)
