"""Plain data model shared by every reconstruction stage.

Everything is a small dataclass with ``to_dict``/``from_dict`` for JSON.
Event types are plain strings, so a new event type needs a new extractor, not a
new class.  Kinds are ACTION (the recorder did something), FACT (a state of the
world or of the recorder), PERCEPTION (the recorder sensed something external)
and OUTCOME (a consequence such as a collision).

Graph events are semantic transitions, mostly NAME_START / NAME_END pairs (or
EGO_PATH_ENTRY / EGO_PATH_EXIT).  Quantitative evidence (speeds, pedal values,
ranges, TTC, ...) stays in the trace facts; ``attributes`` holds only what an
event genuinely needs, such as a collision's peak impulse used by alignment.
A START at the first observation (recording start, or a track's first sample)
has ``{"active_at_first_observation": true}``: the state was already active and
its real beginning was not observed.  A state still active when observation
ends has no END.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

ACTION = "ACTION"
FACT = "FACT"
PERCEPTION = "PERCEPTION"
OUTCOME = "OUTCOME"

# The two edge relations.  PRECEDES links an event to every event at the next
# later timestamp; events that share a timestamp are simultaneous at the
# recorder's resolution and are never linked by PRECEDES.  SAME_TRACK links a
# track's TRACK_APPEARED to every later event about that track; it groups
# events and carries no temporal meaning.
PRECEDES = "PRECEDES"
SAME_TRACK = "SAME_TRACK"

# Display and serialisation order of events that share a timestamp.  It only
# makes files stable and readable (a collision first, then state ends from the
# innermost state outwards, then state starts from the outermost inwards, and
# a lost track last, as the last thing known about it); it never creates a
# PRECEDES edge.  Unknown types come last.  ``display_order`` applies it,
# keeping a zero-length state's START before its own END.
SAME_TIME_ORDER = (
    "COLLISION",
    "CRITICAL_TTC_END", "CLOSING_END", "EGO_PATH_EXIT",
    "STOP_SIGN_DETECTED_END", "YIELD_SIGN_DETECTED_END",
    "HARD_BRAKE_END", "BRAKE_END", "STRONG_THROTTLE_END",
    "SPEED_LIMIT_EXCEEDED_END", "MOVING_END", "STOP_END",
    "STOP_START", "MOVING_START", "SPEED_LIMIT_EXCEEDED_START",
    "STRONG_THROTTLE_START", "BRAKE_START", "HARD_BRAKE_START",
    "STOP_SIGN_DETECTED_START", "YIELD_SIGN_DETECTED_START",
    "TRACK_APPEARED", "EGO_PATH_ENTRY", "CLOSING_START", "CRITICAL_TTC_START",
    "TRACK_LOST",
)


def same_time_rank(event_type: str) -> int:
    if event_type in SAME_TIME_ORDER:
        return SAME_TIME_ORDER.index(event_type)
    return len(SAME_TIME_ORDER)


# Transition pairs that are not named NAME_START / NAME_END.
TRANSITION_PAIRS = {"EGO_PATH_ENTRY": ("EGO_PATH", True), "EGO_PATH_EXIT": ("EGO_PATH", False)}


def transition_of(event_type: str) -> Optional[Tuple[str, bool]]:
    """(state name, True for a start / False for an end), or None for instantaneous events."""
    if event_type in TRANSITION_PAIRS:
        return TRANSITION_PAIRS[event_type]
    if event_type.endswith("_START"):
        return event_type[:-len("_START")], True
    if event_type.endswith("_END"):
        return event_type[:-len("_END")], False
    return None


def display_order(items: Sequence[Any], time_of: Callable[[Any], float], type_of: Callable[[Any], str],
                  actor_of: Callable[[Any], Optional[str]], subject_of: Callable[[Any], Optional[str]]) -> List[Any]:
    """Sort by time, then SAME_TIME_ORDER.  A state that starts and ends at the
    same time (e.g. a sign seen for a single confirmation) keeps START before END."""
    def state_key(item: Any) -> Tuple[Any, ...]:
        return (transition_of(type_of(item))[0], actor_of(item), subject_of(item), round(time_of(item), 6))

    starting_now = {state_key(item) for item in items
                    if transition_of(type_of(item)) is not None and transition_of(type_of(item))[1]}

    def key(item: Any) -> Tuple[Any, ...]:
        transition = transition_of(type_of(item))
        ends_own_start = transition is not None and not transition[1] and state_key(item) in starting_now
        return (round(time_of(item), 6), ends_own_start, same_time_rank(type_of(item)), type_of(item),
                actor_of(item) or "", subject_of(item) or "")

    return sorted(items, key=key)


def precedes_edges(ordered: Sequence[Any], time_of: Callable[[Any], float],
                   id_of: Callable[[Any], str]) -> List["GraphEdge"]:
    """PRECEDES from every item to every item at the next later timestamp.

    ``ordered`` is sorted by time.  Items with equal times form one
    simultaneous group and get no PRECEDES among themselves.
    """
    groups: List[List[Any]] = []
    for item in ordered:
        if groups and abs(time_of(item) - time_of(groups[-1][0])) < 1e-6:
            groups[-1].append(item)
        else:
            groups.append([item])
    return [GraphEdge(id_of(earlier), id_of(later), PRECEDES)
            for first, second in zip(groups, groups[1:]) for earlier in first for later in second]


def _drop_none(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass
class SemanticEvent:
    """One fact or event, stamped with the recorder's own local time.

    ``actor_id`` is who performs or reports it (the recorder, e.g. ``A``).
    ``subject_id`` is the external thing it is about (e.g. ``track_001``).
    """

    type: str
    kind: str
    actor_id: str
    t_local: float
    subject_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    source: str = ""
    confidence: Optional[float] = None
    event_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none({
            "event_id": self.event_id, "type": self.type, "kind": self.kind,
            "actor_id": self.actor_id, "subject_id": self.subject_id,
            "t_local": self.t_local, "attributes": copy.deepcopy(self.attributes),
            "source": self.source or None, "confidence": self.confidence,
        })

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SemanticEvent":
        return cls(type=data["type"], kind=data["kind"], actor_id=data["actor_id"],
                   t_local=data["t_local"], subject_id=data.get("subject_id"),
                   attributes=copy.deepcopy(data.get("attributes", {})),
                   source=data.get("source", ""), confidence=data.get("confidence"),
                   event_id=data.get("event_id"))


@dataclass
class TraceFrame:
    """What one recorder knows at one instant of its own clock."""

    t_local: float
    facts: List[SemanticEvent] = field(default_factory=list)
    events: List[SemanticEvent] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"t_local": self.t_local,
                "facts": [fact.to_dict() for fact in self.facts],
                "events": [event.to_dict() for event in self.events]}


@dataclass
class GraphNode:
    """A semantic event promoted to a node of a local event graph."""

    node_id: str
    event_type: str
    kind: str
    actor_id: str
    subject_id: Optional[str]
    t_local: float
    attributes: Dict[str, Any]
    source: str
    confidence: Optional[float]

    @classmethod
    def from_event(cls, event: SemanticEvent) -> "GraphNode":
        if not event.event_id:
            raise ValueError("an event needs an id before it becomes a graph node")
        return cls(node_id=event.event_id, event_type=event.type, kind=event.kind,
                   actor_id=event.actor_id, subject_id=event.subject_id,
                   t_local=event.t_local, attributes=copy.deepcopy(event.attributes),
                   source=event.source, confidence=event.confidence)

    def to_dict(self) -> Dict[str, Any]:
        return {"node_id": self.node_id, "event_type": self.event_type, "kind": self.kind,
                "actor_id": self.actor_id, "subject_id": self.subject_id,
                "t_local": self.t_local, "attributes": copy.deepcopy(self.attributes),
                "source": self.source, "confidence": self.confidence}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphNode":
        return cls(**{key: copy.deepcopy(data[key]) for key in (
            "node_id", "event_type", "kind", "actor_id", "subject_id", "t_local",
            "attributes", "source", "confidence")})


@dataclass
class GraphEdge:
    from_node: str
    to_node: str
    relation: str

    def to_dict(self) -> Dict[str, Any]:
        return {"from": self.from_node, "to": self.to_node, "relation": self.relation}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GraphEdge":
        return cls(from_node=data["from"], to_node=data["to"], relation=data["relation"])


@dataclass
class LocalGraph:
    """The sparse event graph of one recorder, entirely in its local time.

    ``tracks`` summarises the anonymous radar tracks the nodes refer to and
    ``recorder`` documents the local clock and frame conventions.
    """

    owner: str
    nodes: List[GraphNode] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    tracks: List[Dict[str, Any]] = field(default_factory=list)
    recorder: Dict[str, Any] = field(default_factory=dict)

    def node(self, node_id: str) -> GraphNode:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        raise KeyError(node_id)

    def to_dict(self) -> Dict[str, Any]:
        return {"graph_id": self.owner, "owner": self.owner,
                "recorder": copy.deepcopy(self.recorder),
                "nodes": [node.to_dict() for node in self.nodes],
                "edges": [edge.to_dict() for edge in self.edges],
                "tracks": copy.deepcopy(self.tracks)}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LocalGraph":
        return cls(owner=data["owner"],
                   nodes=[GraphNode.from_dict(node) for node in data["nodes"]],
                   edges=[GraphEdge.from_dict(edge) for edge in data["edges"]],
                   tracks=copy.deepcopy(data.get("tracks", [])),
                   recorder=copy.deepcopy(data.get("recorder", {})))


@dataclass
class GraphClock:
    """How one local graph's clock maps to global graph time.

    ``t_global = t_local + offset_to_global``.  The local graph itself is never
    changed; this object is the only place where the mapping lives.
    """

    graph: str
    status: str  # ALIGNED or UNALIGNED
    anchor_node: Optional[str] = None
    anchor_t_local: Optional[float] = None
    offset_to_global: Optional[float] = None
    reason: str = ""

    def to_global(self, t_local: float) -> Optional[float]:
        if self.offset_to_global is None:
            return None
        return round(t_local + self.offset_to_global, 4)

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "anchor_node": self.anchor_node,
                "anchor_t_local": self.anchor_t_local,
                "offset_to_global": self.offset_to_global, "reason": self.reason}


@dataclass
class Alignment:
    reference_event: Optional[str]
    graphs: Dict[str, GraphClock]
    matched_events: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        aligned = sorted(name for name, clock in self.graphs.items() if clock.status == "ALIGNED")
        relative = {}
        for first in aligned:
            for second in aligned:
                if first < second:
                    # How far the second clock reads ahead of the first one.
                    relative[second + " - " + first] = round(
                        self.graphs[second].anchor_t_local - self.graphs[first].anchor_t_local, 4)
        return {"method": "collision_anchor",
                "definition": "t_global = t_local + offset_to_global; t_global = 0 at the reference collision",
                "reference_event": self.reference_event,
                "graphs": {name: self.graphs[name].to_dict() for name in sorted(self.graphs)},
                "relative_clock_offsets_s": relative,
                "matched_events": copy.deepcopy(self.matched_events)}


@dataclass
class Association:
    """Fusion-stage decision about what one anonymous local track is."""

    local_graph: str
    local_track: str
    global_entity: str
    status: str  # ASSOCIATED or ANONYMOUS
    confidence: Optional[float]  # None when no identity is claimed
    evidence: List[str] = field(default_factory=list)
    source_graphs: List[str] = field(default_factory=list)
    candidate: Optional[str] = None
    # The failed checks that keep the track anonymous (empty when associated).
    blocking: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"local_graph": self.local_graph, "local_track": self.local_track,
                "global_entity": self.global_entity, "status": self.status,
                "confidence": self.confidence, "candidate": self.candidate,
                "evidence": list(self.evidence), "blocking": list(self.blocking),
                "source_graphs": list(self.source_graphs)}


@dataclass
class Observation:
    """Provenance: which local node a global node came from."""

    graph: str
    local_node: str
    t_local: float

    def to_dict(self) -> Dict[str, Any]:
        return {"graph": self.graph, "local_node": self.local_node, "t_local": self.t_local}


@dataclass
class GlobalNode:
    node_id: str
    event_type: str
    kind: str
    actor_id: Optional[str]
    subject_id: Optional[str]
    participants: List[str]
    t_global: Optional[float]
    attributes: Dict[str, Any]
    source: str
    confidence: Optional[float]
    observations: List[Observation]

    def to_dict(self) -> Dict[str, Any]:
        return {"node_id": self.node_id, "event_type": self.event_type, "kind": self.kind,
                "actor_id": self.actor_id, "subject_id": self.subject_id,
                "participants": list(self.participants), "t_global": self.t_global,
                "attributes": copy.deepcopy(self.attributes), "source": self.source,
                "confidence": self.confidence,
                "observations": [obs.to_dict() for obs in self.observations]}


@dataclass
class GlobalGraph:
    entities: List[Dict[str, Any]]
    nodes: List[GlobalNode]
    edges: List[GraphEdge]

    def to_dict(self) -> Dict[str, Any]:
        return {"entities": copy.deepcopy(self.entities),
                "nodes": [node.to_dict() for node in self.nodes],
                "edges": [edge.to_dict() for edge in self.edges]}
