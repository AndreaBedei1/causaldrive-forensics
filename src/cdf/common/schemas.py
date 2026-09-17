"""Versioned record schemas shared by every layer of the pipeline.

This module is the single source of truth for the on-disk evidence format. It is
deliberately dependency-free (standard library only) so that it can be imported
by the local participant pipeline, the fusion pipeline, the oracle pipeline and
the test-suite alike.

Layer discipline
----------------
The dataclasses below encode the data boundary described in ``docs/DATA_BOUNDARY.md``
*structurally*: a record produced by the local participant pipeline simply has no
field in which a privileged quantity (another actor's CARLA id, its true pose, a
map lane id, a traffic-light state, a scenario role label) could be stored. The
anti-leakage test-suite additionally scans serialised artifacts for the names in
:data:`FORBIDDEN_LOCAL_FIELD_NAMES` and :data:`FORBIDDEN_LOCAL_FIELD_SUBSTRINGS`.

Identifiers
-----------
* ``participant_id`` -- an opaque session label (``"A"``, ``"B"``, ``"C"``). It
  identifies *whose* recorder produced a record. It carries no role semantics and
  is never a CARLA actor id.
* ``track_id`` -- a *locally generated* anonymous track label of the form
  ``"A::T003"``. It is produced by our own radar tracker and has no relation to
  any CARLA actor id. Cross-vehicle identity is established only by the fusion
  layer, from observable trajectory evidence.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple

__all__ = [
    "SCHEMA_VERSIONS",
    "Provenance",
    "EventType",
    "EventEdgeType",
    "CausalEdgeType",
    "TriggerKind",
    "OutcomeClass",
    "CheckStatus",
    "TelemetrySample",
    "ControlSample",
    "RadarDetection",
    "RadarFrame",
    "TrackSample",
    "LocalTriggerRecord",
    "Evidence",
    "Event",
    "GraphEdge",
    "GraphDocument",
    "ParticipantManifest",
    "RunManifest",
    "FORBIDDEN_LOCAL_FIELD_NAMES",
    "FORBIDDEN_LOCAL_FIELD_SUBSTRINGS",
    "LOCAL_EVENT_TYPES",
    "ORACLE_ONLY_EVENT_TYPES",
    "OUTCOME_EVENT_TYPES",
    "make_track_id",
    "make_event_id",
    "stable_digest",
    "to_jsonable",
]


# ---------------------------------------------------------------------------
# Schema versions
# ---------------------------------------------------------------------------

#: Version stamped into each persisted artifact family. Bump a value whenever the
#: corresponding record layout changes in a backwards-incompatible way.
SCHEMA_VERSIONS: Dict[str, str] = {
    "telemetry": "1.0.0",
    "controls": "1.0.0",
    "radar": "1.0.0",
    "tracks": "1.0.0",
    "events": "1.0.0",
    "graph": "1.0.0",
    "manifest": "1.0.0",
    "association": "1.0.0",
    "fusion_diagnostics": "1.0.0",
    "model_check": "1.0.0",
    "counterfactual": "1.0.0",
    "evaluation": "1.0.0",
    "viewer": "1.0.0",
}


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------


class Provenance(str, Enum):
    """Which pipeline layer produced a record.

    ``ORACLE`` records must never be consumed by ``LOCAL`` or ``FUSED`` inference.
    """

    LOCAL = "local"
    FUSED = "fused"
    ORACLE = "oracle"


class TriggerKind(str, Enum):
    """What caused the rolling recorder to freeze its pre-event window."""

    COLLISION = "collision"
    NEAR_MISS = "near_miss"
    EMERGENCY_BRAKE = "emergency_brake"
    END_OF_RUN = "end_of_run"


class OutcomeClass(str, Enum):
    """Coarse outcome label of a scenario run (validation / evaluation only)."""

    COLLISION = "collision"
    NEAR_MISS = "near_miss"
    NO_EVENT = "no_event"


class CheckStatus(str, Enum):
    """Finite-trace property verdict.

    ``UNKNOWN`` is a first-class result: it is returned when the local evidence is
    insufficient to decide the property, which is a central epistemic feature of
    this project (see scenario S10).
    """

    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


class EventType(str, Enum):
    """Typed, versioned event taxonomy (see ``docs/EVENT_TAXONOMY.md``).

    Types are grouped into own-behaviour events (derived from a participant's own
    telemetry and controls), radar/interaction events (derived from that
    participant's own radar tracks) and outcome events.
    """

    # --- own behaviour (own telemetry + own controls only) ---
    VEHICLE_STARTED = "VEHICLE_STARTED"
    ACCELERATION = "ACCELERATION"
    DECELERATION = "DECELERATION"
    HARD_DECELERATION = "HARD_DECELERATION"
    BRAKE_ONSET = "BRAKE_ONSET"
    HARD_BRAKE = "HARD_BRAKE"
    THROTTLE_ONSET = "THROTTLE_ONSET"
    STEER_ONSET = "STEER_ONSET"
    SIGNIFICANT_HEADING_CHANGE = "SIGNIFICANT_HEADING_CHANGE"
    LANE_CHANGE_LIKE_MANEUVER = "LANE_CHANGE_LIKE_MANEUVER"

    # --- radar / interaction (own radar tracks only) ---
    RADAR_TRACK_APPEARED = "RADAR_TRACK_APPEARED"
    RADAR_TRACK_LOST = "RADAR_TRACK_LOST"
    RANGE_DECREASING = "RANGE_DECREASING"
    RAPID_CLOSING = "RAPID_CLOSING"
    LOW_TTC = "LOW_TTC"
    CRITICAL_TTC = "CRITICAL_TTC"
    LATERAL_CROSSING = "LATERAL_CROSSING"
    CUT_IN_LIKE_MOTION = "CUT_IN_LIKE_MOTION"
    PREDICTED_PATH_CONFLICT = "PREDICTED_PATH_CONFLICT"
    CONFLICT_REGION_ENTRY = "CONFLICT_REGION_ENTRY"
    TARGET_DECELERATION = "TARGET_DECELERATION"

    # --- outcome ---
    NEAR_MISS = "NEAR_MISS"
    COLLISION = "COLLISION"
    POST_IMPACT_STOP = "POST_IMPACT_STOP"

    # --- oracle-only (privileged; never produced by local/fused inference) ---
    ORACLE_SIGNAL_VIOLATION = "ORACLE_SIGNAL_VIOLATION"
    ORACLE_RIGHT_OF_WAY_CONFLICT = "ORACLE_RIGHT_OF_WAY_CONFLICT"
    ORACLE_SCRIPTED_INTERVENTION = "ORACLE_SCRIPTED_INTERVENTION"


#: Event types the oracle alone may emit. Their presence in a ``local`` or
#: ``fused`` artifact is a leakage bug and is asserted against by the test-suite.
ORACLE_ONLY_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.ORACLE_SIGNAL_VIOLATION,
    EventType.ORACLE_RIGHT_OF_WAY_CONFLICT,
    EventType.ORACLE_SCRIPTED_INTERVENTION,
)

#: Event types producible by the local participant pipeline.
LOCAL_EVENT_TYPES: Tuple[EventType, ...] = tuple(
    t for t in EventType if t not in ORACLE_ONLY_EVENT_TYPES
)

#: Terminal outcome events.
OUTCOME_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.COLLISION,
    EventType.NEAR_MISS,
    EventType.POST_IMPACT_STOP,
)


class EventEdgeType(str, Enum):
    """Event-graph relations. These are explicitly *not* causal claims."""

    PRECEDES = "PRECEDES"
    OBSERVED_FROM = "OBSERVED_FROM"
    SAME_TRACK = "SAME_TRACK"
    INTERACTS_WITH = "INTERACTS_WITH"
    ALIGNS_WITH = "ALIGNS_WITH"
    ASSOCIATED_WITH = "ASSOCIATED_WITH"


class CausalEdgeType(str, Enum):
    """Causal-DAG relations. Every instance is a hypothesis with evidence."""

    CONTRIBUTES_TO = "CONTRIBUTES_TO"
    TRIGGERS = "TRIGGERS"
    INCREASES_RISK_OF = "INCREASES_RISK_OF"
    PREVENTS = "PREVENTS"
    CAUSES_OUTCOME = "CAUSES_OUTCOME"


# ---------------------------------------------------------------------------
# Anti-leakage registries
# ---------------------------------------------------------------------------

#: Exact field names that must never appear anywhere inside a ``local`` or
#: ``fused`` artifact. Checked recursively over serialised JSON by
#: ``tests/test_no_privileged_leakage.py``.
FORBIDDEN_LOCAL_FIELD_NAMES: Tuple[str, ...] = (
    "other_actor_id",
    "carla_actor_id_other",
    "other_actor",
    "actor_id",
    "carla_id",
    "true_other_x",
    "true_other_y",
    "true_other_z",
    "true_other_yaw",
    "true_other_velocity",
    "true_other_speed",
    "lane_id",
    "road_id",
    "junction_id",
    "section_id",
    "waypoint",
    "map_waypoint",
    "traffic_light_state",
    "traffic_light_id",
    "signal_state",
    "ground_truth_role",
    "gt_role",
    "role",
    "oracle_label",
    "oracle_id",
    "expected_cause",
    "expected_culprit",
    "culprit",
    "causes",
    "scenario_role",
    "is_at_fault",
)

#: Substrings that flag a leaked privileged quantity regardless of the exact
#: field name (e.g. ``"gt_speed_other"``).
FORBIDDEN_LOCAL_FIELD_SUBSTRINGS: Tuple[str, ...] = (
    "ground_truth",
    "groundtruth",
    "privileged",
    "oracle",
    "true_other",
    "gt_other",
    "actor_id",
    "traffic_light",
    "waypoint",
    "lane_id",
    "road_id",
    "junction",
)


# ---------------------------------------------------------------------------
# Identifier helpers
# ---------------------------------------------------------------------------


def make_track_id(participant_id: str, index: int) -> str:
    """Build an anonymous local track identifier, e.g. ``make_track_id("A", 3)``.

    The identifier encodes only *who observed* the track and a monotone counter.
    It deliberately carries no information about the observed actor's identity.
    """
    return "{0}::T{1:03d}".format(participant_id, int(index))


def make_event_id(
    scope: str,
    owner: str,
    event_type: str,
    t_peak: float,
    subject: Optional[str] = None,
) -> str:
    """Build a deterministic, collision-resistant event identifier.

    Determinism matters: identical inputs must yield identical ids so that reruns
    of the same seed produce byte-comparable artifacts.
    """
    payload = "|".join(
        [scope, owner, event_type, "{0:.3f}".format(float(t_peak)), subject or "-"]
    )
    return "{0}:{1}:{2}:{3}".format(
        scope, owner, event_type, stable_digest(payload)[:10]
    )


def stable_digest(payload: Any) -> str:
    """SHA-256 hex digest of ``payload`` with deterministic JSON serialisation."""
    if not isinstance(payload, str):
        payload = json.dumps(to_jsonable(payload), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def to_jsonable(obj: Any) -> Any:
    """Recursively convert dataclasses/enums/tuples into JSON-serialisable data."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: to_jsonable(v) for k, v in dataclasses.asdict(obj).items()}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, float):
        # Guard against NaN/Inf which are not valid JSON.
        if obj != obj or obj in (float("inf"), float("-inf")):
            return None
        return obj
    return obj


# ---------------------------------------------------------------------------
# Local evidence records
# ---------------------------------------------------------------------------


@dataclass
class TelemetrySample:
    """One sample of a participant's own localisation and motion state.

    Sourced from the vehicle's own pose/IMU proxy. Contains no information about
    any other actor.
    """

    t: float
    """Simulation timestamp in seconds (CARLA ``elapsed_seconds``)."""
    frame: int
    """CARLA frame number."""
    participant_id: str

    x: float
    y: float
    z: float
    yaw: float
    """Heading in degrees, CARLA convention (clockwise-positive, x forward)."""
    pitch: float = 0.0
    roll: float = 0.0

    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    speed: float = 0.0
    """Ground speed magnitude in m/s."""

    ax: float = 0.0
    ay: float = 0.0
    az: float = 0.0
    accel_long: float = 0.0
    """Longitudinal acceleration in the vehicle body frame (m/s^2)."""
    accel_lat: float = 0.0
    """Lateral acceleration in the vehicle body frame (m/s^2)."""

    yaw_rate: float = 0.0
    """Angular velocity about the z axis in deg/s."""

    schema_version: str = SCHEMA_VERSIONS["telemetry"]


@dataclass
class ControlSample:
    """One sample of a participant's own actuator commands."""

    t: float
    frame: int
    participant_id: str

    throttle: float = 0.0
    brake: float = 0.0
    steer: float = 0.0
    hand_brake: bool = False
    reverse: bool = False
    gear: int = 0

    schema_version: str = SCHEMA_VERSIONS["controls"]


@dataclass
class RadarDetection:
    """A single raw radar return in sensor-polar coordinates.

    ``depth``/``azimuth``/``altitude``/``velocity`` mirror the CARLA radar
    detection fields; nothing identifies the reflecting actor.
    """

    depth: float
    """Range to the reflecting surface in metres."""
    azimuth: float
    """Azimuth angle in radians, positive to the right of sensor boresight."""
    altitude: float
    """Elevation angle in radians, positive upwards."""
    velocity: float
    """Radial (range-rate) velocity in m/s; negative means closing."""


@dataclass
class RadarFrame:
    """All detections produced by one radar sensor at one simulation step."""

    t: float
    frame: int
    participant_id: str
    sensor_id: str
    """Logical sensor name, e.g. ``"front"``. Not a CARLA actor id."""

    detections: List[RadarDetection] = field(default_factory=list)

    sensor_yaw: float = 0.0
    """Sensor mounting yaw relative to the vehicle body frame, degrees."""
    sensor_x: float = 0.0
    """Sensor mounting offset, vehicle body frame, metres."""
    sensor_y: float = 0.0
    sensor_z: float = 0.0

    schema_version: str = SCHEMA_VERSIONS["radar"]


@dataclass
class TrackSample:
    """One sample of a locally maintained radar track.

    All quantities are *estimates* derived from own localisation plus own radar
    observations. The global-frame fields are obtained by composing the
    participant's own pose with the radar-relative measurement; the true pose of
    the observed actor is never queried.
    """

    t: float
    frame: int
    participant_id: str
    track_id: str
    """Anonymous local track id, see :func:`make_track_id`."""

    # Participant body frame (x forward, y right, metres).
    rel_x: float = 0.0
    rel_y: float = 0.0
    # Global (map) frame estimate, metres.
    gx: float = 0.0
    gy: float = 0.0

    # Estimated global-frame velocity of the tracked object, m/s.
    gvx: float = 0.0
    gvy: float = 0.0

    range_m: float = 0.0
    azimuth_rad: float = 0.0
    range_rate: float = 0.0
    """Measured radial velocity, m/s; negative means closing."""

    rel_vx: float = 0.0
    """Relative velocity of the target w.r.t. the observer, body frame, m/s."""
    rel_vy: float = 0.0

    n_points: int = 0
    extent_x: float = 0.0
    extent_y: float = 0.0
    confidence: float = 0.0
    age: int = 0
    """Number of frames since the track was initialised."""
    misses: int = 0
    """Consecutive frames without an associated detection."""

    ttc: Optional[float] = None
    """Time-to-collision estimate in seconds, ``None`` when not defined."""

    schema_version: str = SCHEMA_VERSIONS["tracks"]


@dataclass
class LocalTriggerRecord:
    """A recorder trigger observed onboard a participant.

    For a collision trigger this holds only what an onboard unit could know: that
    an impact occurred, when, and how hard. The identity of the other party is
    deliberately absent.
    """

    t: float
    frame: int
    participant_id: str
    kind: TriggerKind
    collision_detected: bool = False
    impulse: float = 0.0
    """Impulse magnitude in N*s as reported by the onboard collision sensor."""
    detail: Dict[str, Any] = field(default_factory=dict)
    """Free-form derived quantities (e.g. ``min_ttc``). Never privileged data."""


# ---------------------------------------------------------------------------
# Events and graphs
# ---------------------------------------------------------------------------


@dataclass
class Evidence:
    """A pointer from an event or edge back to the raw records supporting it."""

    kind: str
    """One of ``"telemetry"``, ``"controls"``, ``"radar"``, ``"track"``,
    ``"trigger"``, ``"event"``, ``"oracle"``."""
    ref: str
    """Opaque reference, e.g. a track id or an event id."""
    t_start: Optional[float] = None
    t_end: Optional[float] = None
    detail: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Event:
    """A typed event extracted from a time series; also a graph node.

    An event is always attributed to the participant that observed it
    (``participant_id``) and, for interaction events, to the local track it
    concerns (``subject``).
    """

    event_id: str
    event_type: EventType
    participant_id: str
    """Session id of the observing participant; for fused/oracle nodes this is
    the canonical owner (see ``owners`` for the full set)."""

    t_start: float
    t_peak: float
    t_end: Optional[float] = None

    subject: Optional[str] = None
    """Local track id for interaction events; ``None`` (or ``"self"``) for
    own-behaviour events."""

    values: Dict[str, float] = field(default_factory=dict)
    """Measured quantities that characterise the event (e.g. ``{"ttc": 1.2}``)."""

    confidence: float = 1.0
    evidence: List[Evidence] = field(default_factory=list)
    provenance: Provenance = Provenance.LOCAL
    source_sensors: List[str] = field(default_factory=list)

    owners: List[str] = field(default_factory=list)
    """All participants that contributed an observation of this event. For a
    local event this is ``[participant_id]``; fusion extends it."""

    merged_from: List[str] = field(default_factory=list)
    """Ids of the local events merged into this (fused) event."""

    schema_version: str = SCHEMA_VERSIONS["events"]

    def __post_init__(self) -> None:
        if not self.owners:
            self.owners = [self.participant_id]

    @property
    def duration(self) -> float:
        """Event duration in seconds (0.0 when no end time is defined)."""
        if self.t_end is None:
            return 0.0
        return max(0.0, float(self.t_end) - float(self.t_start))


@dataclass
class GraphEdge:
    """A directed edge of an event graph or a causal DAG."""

    source: str
    target: str
    edge_type: str
    """An :class:`EventEdgeType` or :class:`CausalEdgeType` value."""

    confidence: float = 1.0
    provenance: Provenance = Provenance.LOCAL
    rule: Optional[str] = None
    """Name of the rule that proposed the edge (causal edges)."""
    temporal_relation: Optional[str] = None
    """e.g. ``"before"``, ``"overlaps"``, ``"within_1.50s"``."""
    evidence: List[Evidence] = field(default_factory=list)
    owners: List[str] = field(default_factory=list)
    merged_from: List[str] = field(default_factory=list)
    detail: Dict[str, Any] = field(default_factory=dict)

    @property
    def key(self) -> Tuple[str, str, str]:
        """Identity of the edge inside a graph document."""
        return (self.source, self.target, self.edge_type)


@dataclass
class GraphDocument:
    """A serialisable event graph or causal DAG.

    ``scope`` records which layer produced the graph and is the mechanism that
    keeps oracle graphs from silently entering inference: loaders assert on it.
    """

    graph_kind: str
    """``"event"`` or ``"causal"``."""
    scope: Provenance
    owner: Optional[str] = None
    """Participant id for a local graph; ``None`` for fused/oracle graphs."""

    run_id: str = ""
    scenario_id: str = ""
    seed: int = 0

    nodes: List[Event] = field(default_factory=list)
    edges: List[GraphEdge] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = SCHEMA_VERSIONS["graph"]

    # -- convenience ------------------------------------------------------

    def node_ids(self) -> List[str]:
        return [n.event_id for n in self.nodes]

    def node_by_id(self, event_id: str) -> Optional[Event]:
        for n in self.nodes:
            if n.event_id == event_id:
                return n
        return None

    def to_dict(self) -> Dict[str, Any]:
        return to_jsonable(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GraphDocument":
        """Rebuild a :class:`GraphDocument` from its JSON representation."""
        nodes = [_event_from_dict(n) for n in data.get("nodes", [])]
        edges = [_edge_from_dict(e) for e in data.get("edges", [])]
        return GraphDocument(
            graph_kind=data["graph_kind"],
            scope=Provenance(data["scope"]),
            owner=data.get("owner"),
            run_id=data.get("run_id", ""),
            scenario_id=data.get("scenario_id", ""),
            seed=int(data.get("seed", 0)),
            nodes=nodes,
            edges=edges,
            meta=data.get("meta", {}) or {},
            schema_version=data.get("schema_version", SCHEMA_VERSIONS["graph"]),
        )


def _evidence_from_dict(d: Dict[str, Any]) -> Evidence:
    return Evidence(
        kind=d.get("kind", "unknown"),
        ref=d.get("ref", ""),
        t_start=d.get("t_start"),
        t_end=d.get("t_end"),
        detail=d.get("detail", {}) or {},
    )


def _event_from_dict(d: Dict[str, Any]) -> Event:
    return Event(
        event_id=d["event_id"],
        event_type=EventType(d["event_type"]),
        participant_id=d["participant_id"],
        t_start=float(d["t_start"]),
        t_peak=float(d["t_peak"]),
        t_end=d.get("t_end"),
        subject=d.get("subject"),
        values=d.get("values", {}) or {},
        confidence=float(d.get("confidence", 1.0)),
        evidence=[_evidence_from_dict(e) for e in d.get("evidence", []) or []],
        provenance=Provenance(d.get("provenance", "local")),
        source_sensors=list(d.get("source_sensors", []) or []),
        owners=list(d.get("owners", []) or []),
        merged_from=list(d.get("merged_from", []) or []),
        schema_version=d.get("schema_version", SCHEMA_VERSIONS["events"]),
    )


def _edge_from_dict(d: Dict[str, Any]) -> GraphEdge:
    return GraphEdge(
        source=d["source"],
        target=d["target"],
        edge_type=d["edge_type"],
        confidence=float(d.get("confidence", 1.0)),
        provenance=Provenance(d.get("provenance", "local")),
        rule=d.get("rule"),
        temporal_relation=d.get("temporal_relation"),
        evidence=[_evidence_from_dict(e) for e in d.get("evidence", []) or []],
        owners=list(d.get("owners", []) or []),
        merged_from=list(d.get("merged_from", []) or []),
        detail=d.get("detail", {}) or {},
    )


# ---------------------------------------------------------------------------
# Run manifests
# ---------------------------------------------------------------------------


@dataclass
class ParticipantManifest:
    """Per-participant provenance block inside a run manifest."""

    participant_id: str
    blueprint: str
    spawn: Dict[str, float]
    controller: str
    controller_params: Dict[str, Any] = field(default_factory=dict)
    sensor_profile: str = "baseline"
    radar_sensors: List[Dict[str, Any]] = field(default_factory=list)
    n_telemetry: int = 0
    n_radar_frames: int = 0
    n_track_samples: int = 0
    n_events: int = 0
    triggers: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class RunManifest:
    """Complete, self-describing record of one scenario execution.

    Everything needed to reproduce the run byte-for-byte is captured here: the
    scenario id, the seed, every configuration value and its hash, the software
    commit, and the exact simulator/environment versions.
    """

    run_id: str
    scenario_id: str
    variant: str
    seed: int

    map_name: str
    fixed_delta_seconds: float
    synchronous_mode: bool

    config_hash: str
    config: Dict[str, Any] = field(default_factory=dict)

    participants: List[ParticipantManifest] = field(default_factory=list)

    started_at: str = ""
    finished_at: str = ""
    duration_sim_s: float = 0.0
    n_frames: int = 0

    outcome: OutcomeClass = OutcomeClass.NO_EVENT
    outcome_detail: Dict[str, Any] = field(default_factory=dict)

    git_commit: Optional[str] = None
    python_version: str = ""
    carla_version: str = ""
    platform: str = ""
    package_version: str = ""

    notes: List[str] = field(default_factory=list)
    schema_version: str = SCHEMA_VERSIONS["manifest"]


# ---------------------------------------------------------------------------
# Small validation helpers used by loaders and tests
# ---------------------------------------------------------------------------


def assert_non_oracle(doc: GraphDocument, context: str = "") -> None:
    """Raise if ``doc`` is an oracle artifact.

    Call this at every boundary where an inference stage loads a graph, so that a
    mis-wired path fails loudly instead of silently leaking ground truth.
    """
    if doc.scope is Provenance.ORACLE:
        raise ValueError(
            "privileged oracle graph reached an inference stage"
            + (" ({0})".format(context) if context else "")
        )


def field_names(record_type: type) -> Sequence[str]:
    """Names of the dataclass fields of ``record_type`` (used by tests)."""
    return tuple(f.name for f in dataclasses.fields(record_type))
