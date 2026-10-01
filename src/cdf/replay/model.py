"""Replay model: recorded trajectories, a playback clock and reconstructed events.

Pure Python (no CARLA, no pygame) and read-only; used by scripts/replay_run.py.

Timeline.  Every recorder of a CARLA run stamps its samples with simulator
time, so the recorded source timestamps form one visualization clock:

    replay_time = source_timestamp - run_start

where ``run_start`` is the earliest recorded ego sample.  A reconstructed event
of recorder X is shown at ``X's clock origin + t_local - run_start``.  This
mapping exists for display only: it is not the graph-level alignment, and
nothing is ever written back to a trace or a graph.
"""

from __future__ import annotations

import json
import math
from bisect import bisect_right
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..reconstruction.models import transition_of
from ..reconstruction.world_state import compact_state

FALLBACK_BLUEPRINT = "vehicle.tesla.model3"
SPEEDS = (0.25, 0.5, 1.0, 2.0)
_EPS = 1e-6


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def lerp(a: float, b: float, f: float) -> float:
    return a + (b - a) * f


def lerp_angle_deg(a: float, b: float, f: float) -> float:
    """Interpolate from ``a`` to ``b`` (degrees) the shorter way round."""
    return a + ((b - a + 180.0) % 360.0 - 180.0) * f


# --------------------------------------------------------------------------
# Recorded trajectories
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Pose:
    """A CARLA transform: world-frame metres and degrees."""

    x: float
    y: float
    z: float
    yaw: float
    pitch: float = 0.0
    roll: float = 0.0


class Trajectory:
    """The recorded poses of one vehicle, interpolated between samples.

    Position and recorded speed interpolate linearly, angles the shorter way
    round.  Outside the recorded span the first or last pose is held; nothing
    is extrapolated.
    """

    def __init__(self, times: Sequence[float], poses: Sequence[Pose], speeds: Optional[Sequence[float]] = None):
        if not times or len(times) != len(poses):
            raise ValueError("a trajectory needs one pose per timestamp")
        self.times: List[float] = []
        self.poses: List[Pose] = []
        self.speeds: List[float] = []
        for index in sorted(range(len(times)), key=lambda i: times[i]):
            if self.times and times[index] <= self.times[-1] + _EPS:
                continue  # a repeated timestamp adds nothing to interpolate
            self.times.append(float(times[index]))
            self.poses.append(poses[index])
            self.speeds.append(float(speeds[index]) if speeds is not None else 0.0)

    @classmethod
    def from_records(cls, records: Sequence[Mapping[str, Any]]) -> "Trajectory":
        """From ego.jsonl records (timestamp, x, y, z, yaw_deg, pitch_deg, roll_deg, velocity)."""
        times, poses, speeds = [], [], []
        for record in records:
            times.append(float(record["timestamp"]))
            poses.append(Pose(float(record["x"]), float(record["y"]), float(record["z"]), float(record["yaw_deg"]),
                              float(record.get("pitch_deg", 0.0)), float(record.get("roll_deg", 0.0))))
            velocity = record.get("velocity") or {}
            speeds.append(math.hypot(float(velocity.get("x", 0.0)), float(velocity.get("y", 0.0))))
        return cls(times, poses, speeds)

    @property
    def start(self) -> float:
        return self.times[0]

    @property
    def end(self) -> float:
        return self.times[-1]

    def _bracket(self, t: float) -> Tuple[int, float]:
        if t <= self.times[0]:
            return 0, 0.0
        if t >= self.times[-1]:
            return len(self.times) - 1, 0.0
        index = bisect_right(self.times, t) - 1
        return index, (t - self.times[index]) / (self.times[index + 1] - self.times[index])

    def pose_at(self, t: float) -> Pose:
        index, f = self._bracket(t)
        a = self.poses[index]
        if f == 0.0:
            return a
        b = self.poses[index + 1]
        return Pose(lerp(a.x, b.x, f), lerp(a.y, b.y, f), lerp(a.z, b.z, f), lerp_angle_deg(a.yaw, b.yaw, f),
                    lerp_angle_deg(a.pitch, b.pitch, f), lerp_angle_deg(a.roll, b.roll, f))

    def speed_at(self, t: float) -> float:
        index, f = self._bracket(t)
        if f == 0.0:
            return self.speeds[index]
        return lerp(self.speeds[index], self.speeds[index + 1], f)


# --------------------------------------------------------------------------
# Playback clock
# --------------------------------------------------------------------------

class PlaybackClock:
    """Replay time from 0 to ``duration``, advanced by wall time.

    At speed s one wall second advances the replay by s seconds.  Only the
    sampling instant changes with s; the recorded trajectory never does.
    """

    def __init__(self, duration: float, speed: float = 0.5, start: float = 0.0, playing: bool = True):
        if duration < 0:
            raise ValueError("duration must not be negative")
        if speed <= 0:
            raise ValueError("speed must be positive")
        self.duration = float(duration)
        self.speed = float(speed)
        self.time = self._clamp(start)
        self.playing = bool(playing) and not self.at_end

    def _clamp(self, t: float) -> float:
        return min(max(float(t), 0.0), self.duration)

    @property
    def at_end(self) -> bool:
        return self.time >= self.duration - _EPS

    def advance(self, wall_dt: float) -> None:
        if self.playing and wall_dt > 0:
            self.time = self._clamp(self.time + wall_dt * self.speed)
            if self.at_end:
                self.playing = False

    def toggle(self) -> None:
        """Pause or resume; resuming at the end starts again from 0."""
        if not self.playing and self.at_end:
            self.time = 0.0
        self.playing = not self.playing

    def pause(self) -> None:
        self.playing = False

    def seek(self, delta: float) -> None:
        self.time = self._clamp(self.time + delta)

    def seek_to(self, t: float) -> None:
        self.time = self._clamp(t)

    def restart(self) -> None:
        self.time = 0.0

    def set_speed(self, speed: float) -> None:
        if speed <= 0:
            raise ValueError("speed must be positive")
        self.speed = float(speed)


# --------------------------------------------------------------------------
# Reconstructed events (read from existing outputs, never recomputed)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class ReplayEvent:
    time: float  # replay time
    actor: str  # the recorder whose local graph holds the event
    event_type: str
    subject: Optional[str]
    node_id: str


@dataclass(frozen=True)
class StateInterval:
    """One START..END (or ENTRY..EXIT) pair of a recorder's local graph, in replay time."""

    actor: str
    state: str
    subject: Optional[str]
    start: float
    end: Optional[float]  # None: still active when observation ended

    def active_at(self, t: float) -> bool:
        return self.start - _EPS <= t and (self.end is None or t < self.end - _EPS)


def state_intervals(events: Sequence[ReplayEvent], observed_from: float = 0.0) -> List[StateInterval]:
    """Pair the START/END transitions of one recorder's events (in graph order).

    An END without an observed START (a track first seen inside the ego path,
    whose entry was never seen) is shown from the subject's first appearance,
    or from ``observed_from`` (the recorder's first sample) for its own states.
    """
    open_: Dict[Tuple[str, Optional[str]], ReplayEvent] = {}
    appeared: Dict[Optional[str], float] = {}
    out: List[StateInterval] = []
    for event in events:
        if event.event_type == "TRACK_APPEARED":
            appeared.setdefault(event.subject, event.time)
        transition = transition_of(event.event_type)
        if transition is None:
            continue
        state, starts = transition
        key = (state, event.subject)
        if starts:
            if key in open_:
                out.append(StateInterval(event.actor, state, event.subject, open_[key].time, event.time))
            open_[key] = event
            continue
        begin = open_.pop(key, None)
        since = begin.time if begin is not None else appeared.get(event.subject, observed_from)
        out.append(StateInterval(event.actor, state, event.subject, since, event.time))
    for (state, subject), begin in open_.items():
        out.append(StateInterval(begin.actor, state, subject, begin.time, None))
    return sorted(out, key=lambda item: (item.start, item.state, item.subject or ""))


@dataclass
class PerceivedStates:
    """A recorder's perceived state per trace frame (``local_trace.jsonl``), on the replay timeline.

    Read as written by the reconstruction: the state AT each frame time, after
    its transitions.  Between frames the latest frame holds (frames are 0.1 s apart).
    """

    times: List[float]
    states: List[Dict[str, Any]]

    def state_at(self, t: float) -> Optional[Dict[str, Any]]:
        index = bisect_right(self.times, t + _EPS) - 1
        return None if index < 0 else self.states[index]


def load_perceived_states(path: Path, origin: float, run_start: float) -> Optional[PerceivedStates]:
    """None when the trace predates perceived states (the viewer then pairs START/END events)."""
    times, states = [], []
    for row in _read_jsonl(path):
        if row.get("perceived_state") is not None:
            times.append(round(origin + float(row["t_local"]) - run_start, 6))
            states.append(row["perceived_state"])
    return PerceivedStates(times, states) if states else None


@dataclass
class LocalEvents:
    recorder: str
    origin: float  # source timestamp of the recorder's t_local = 0
    events: List[ReplayEvent]
    intervals: List[StateInterval]


def load_local_events(path: Path, run_start: float) -> LocalEvents:
    """Events of one local_graph.json on the replay timeline (read-only)."""
    graph = _read_json(path)
    owner = str(graph["owner"])
    origin = float(graph["recorder"]["clock"]["origin_source_timestamp"])
    offset = origin - run_start
    events = [ReplayEvent(round(offset + float(node["t_local"]), 6), owner, str(node["event_type"]),
                          node.get("subject_id"), str(node["node_id"])) for node in graph["nodes"]]
    return LocalEvents(owner, origin, events, state_intervals(events, observed_from=round(offset, 6)))


@dataclass(frozen=True)
class CollisionMark:
    time: float
    participants: Tuple[str, ...]
    node_id: str


def load_collisions(path: Path, origins: Mapping[str, float], run_start: float) -> List[CollisionMark]:
    """COLLISION nodes of global_graph.json; participants as the fusion reported them."""
    marks = []
    for node in _read_json(path)["nodes"]:
        if node["event_type"] != "COLLISION":
            continue
        times = [origins[obs["graph"]] + float(obs["t_local"]) - run_start
                 for obs in node.get("observations", []) if obs["graph"] in origins]
        if times:
            marks.append(CollisionMark(round(min(times), 6), tuple(node.get("participants") or ()), str(node["node_id"])))
    return sorted(marks, key=lambda mark: mark.time)


def load_identities(path: Path) -> Dict[Tuple[str, str], str]:
    """(recorder, local track) -> entity, for the fusion's ASSOCIATED decisions only."""
    return {(str(item["local_graph"]), str(item["local_track"])): str(item["global_entity"])
            for item in _read_json(path) if item.get("status") == "ASSOCIATED"}


# --------------------------------------------------------------------------
# Reconstructed anonymous tracks
# --------------------------------------------------------------------------

def local_to_world(origin: Pose, x_local: float, y_local: float) -> Tuple[float, float]:
    """Inverse of the reconstruction's local frame (origin = first ego pose, x forward, y right)."""
    c0, s0 = math.cos(math.radians(origin.yaw)), math.sin(math.radians(origin.yaw))
    return origin.x + c0 * x_local - s0 * y_local, origin.y + s0 * x_local + c0 * y_local


@dataclass
class TrackPath:
    """One anonymous radar track of a recorder, in world coordinates on the replay timeline."""

    recorder: str
    track_id: str
    times: List[float]
    points: List[Tuple[float, float]]
    measured: List[Optional[Tuple[float, float]]]
    ranges: List[Optional[float]] = field(default_factory=list)  # TRACK_STATE facts, as recorded
    closing_speeds: List[Optional[float]] = field(default_factory=list)

    def position_at(self, t: float) -> Optional[Tuple[float, float]]:
        """Interpolated track position, or None outside the tracked span."""
        if not self.times or t < self.times[0] - _EPS or t > self.times[-1] + _EPS:
            return None
        index = max(0, min(bisect_right(self.times, t) - 1, len(self.times) - 1))
        if index == len(self.times) - 1:
            return self.points[index]
        f = (t - self.times[index]) / (self.times[index + 1] - self.times[index])
        (x0, y0), (x1, y1) = self.points[index], self.points[index + 1]
        return lerp(x0, x1, f), lerp(y0, y1, f)

    def _latest(self, t: float) -> Optional[int]:
        if not self.times or t < self.times[0] - _EPS or t > self.times[-1] + _EPS:
            return None
        return max(0, bisect_right(self.times, t + _EPS) - 1)

    def measurement_at(self, t: float) -> Optional[Tuple[float, float]]:
        """The radar measurement of the latest sample at or before ``t`` (None if unmeasured)."""
        index = self._latest(t)
        return None if index is None else self.measured[index]

    def facts_at(self, t: float) -> Tuple[Optional[float], Optional[float]]:
        """(range, closing speed) of the latest sample at or before ``t``, as the reconstruction wrote them."""
        index = self._latest(t)
        if index is None or not self.ranges:
            return None, None
        return self.ranges[index], self.closing_speeds[index]


def load_tracks(path: Path, recorder: str, frame_origin: Pose, clock_origin: float, run_start: float) -> List[TrackPath]:
    grouped: Dict[str, TrackPath] = {}
    for row in _read_jsonl(path):
        track = grouped.setdefault(row["track_id"], TrackPath(recorder, row["track_id"], [], [], []))
        track.times.append(round(clock_origin + float(row["t_local"]) - run_start, 6))
        track.points.append(local_to_world(frame_origin, float(row["x_m"]), float(row["y_m"])))
        measured = row.get("measured") and row.get("meas_x_m") is not None
        track.measured.append(local_to_world(frame_origin, float(row["meas_x_m"]), float(row["meas_y_m"]))
                              if measured else None)
        track.ranges.append(row.get("range_m"))
        track.closing_speeds.append(row.get("closing_speed_mps"))
    return [grouped[key] for key in sorted(grouped)]


# --------------------------------------------------------------------------
# A recorded run
# --------------------------------------------------------------------------

@dataclass
class Participant:
    participant_id: str
    blueprint: str
    blueprint_source: str  # "recorded", "scenario" or "fallback"
    trajectory: Trajectory
    frame_origin: Pose  # first ego record in file order: the reconstruction's local frame


def scenario_setup(scenario_id: str, variant: Optional[str]) -> Tuple[str, Dict[str, str]]:
    """(map name, participant blueprints) from the scenario configuration."""
    from ..common.config import load_run_config
    from ..simulation.scenario_base import ScenarioSpec

    spec = ScenarioSpec.from_config(load_run_config(scenario_id), variant=variant)
    return spec.map_name, {p.participant_id: p.blueprint for p in spec.participants}


@dataclass
class ReplayRun:
    run_dir: Path
    name: str
    scenario_id: Optional[str]
    variant: Optional[str]
    participants: List[Participant]
    start: float  # source timestamp of replay time 0
    duration: float
    local_events: Dict[str, LocalEvents] = field(default_factory=dict)
    collisions: List[CollisionMark] = field(default_factory=list)
    identities: Dict[Tuple[str, str], str] = field(default_factory=dict)
    tracks: Dict[str, List[TrackPath]] = field(default_factory=dict)
    perceived: Dict[str, PerceivedStates] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, run_dir: Path, scenario_blueprints: Optional[Mapping[str, str]] = None) -> "ReplayRun":
        run_dir = Path(run_dir)
        notes: List[str] = []
        meta: Dict[str, Any] = {}
        try:
            meta = _read_json(run_dir / "metadata.json")
        except (OSError, ValueError):
            notes.append("run metadata.json missing or unreadable")
        vehicles_dir = run_dir / "vehicles"
        present = sorted(p.name for p in vehicles_dir.iterdir() if (p / "ego.jsonl").exists())
        ids = [str(pid) for pid in meta.get("participants", []) if str(pid) in present] or present
        if not ids:
            raise ValueError("no vehicles/<id>/ego.jsonl under " + str(run_dir))

        participants = []
        for pid in ids:
            records = _read_jsonl(vehicles_dir / pid / "ego.jsonl")
            blueprint, source = None, "fallback"
            try:
                blueprint = _read_json(vehicles_dir / pid / "metadata.json").get("blueprint")
                source = "recorded" if blueprint else source
            except (OSError, ValueError):
                pass
            if not blueprint and scenario_blueprints and scenario_blueprints.get(pid):
                blueprint, source = scenario_blueprints[pid], "scenario"
            if not blueprint:
                blueprint = FALLBACK_BLUEPRINT
                notes.append("{0}: no recorded blueprint; using {1}".format(pid, FALLBACK_BLUEPRINT))
            first = records[0]
            participants.append(Participant(pid, str(blueprint), source, Trajectory.from_records(records),
                                            Pose(float(first["x"]), float(first["y"]), float(first["z"]),
                                                 float(first["yaw_deg"]))))
        start = min(p.trajectory.start for p in participants)
        end = max(p.trajectory.end for p in participants)
        run = cls(run_dir=run_dir, name="{0} / {1}".format(run_dir.parent.name, run_dir.name),
                  scenario_id=meta.get("scenario_id"), variant=meta.get("variant"), participants=participants,
                  start=start, duration=round(end - start, 6), notes=notes)
        run._load_reconstruction()
        return run

    def _load_reconstruction(self) -> None:
        rec = self.run_dir / "reconstruction"
        for participant in self.participants:
            pid = participant.participant_id
            graph = rec / pid / "local_graph.json"
            if not graph.exists():
                self.notes.append("{0}: no local_graph.json; no events shown".format(pid))
                continue
            local = load_local_events(graph, self.start)
            self.local_events[pid] = local
            tracks = rec / pid / "local_tracks.jsonl"
            if tracks.exists():
                self.tracks[pid] = load_tracks(tracks, pid, participant.frame_origin, local.origin, self.start)
            trace = rec / pid / "local_trace.jsonl"
            perceived = load_perceived_states(trace, local.origin, self.start) if trace.exists() else None
            if perceived is not None:
                self.perceived[pid] = perceived
        origins = {pid: local.origin for pid, local in self.local_events.items()}
        if (rec / "global" / "global_graph.json").exists():
            self.collisions = load_collisions(rec / "global" / "global_graph.json", origins, self.start)
        if (rec / "global" / "associations.json").exists():
            self.identities = load_identities(rec / "global" / "associations.json")

    # -- queries --------------------------------------------------------------

    def participant(self, participant_id: str) -> Participant:
        return next(p for p in self.participants if p.participant_id == participant_id)

    def all_events(self) -> List[ReplayEvent]:
        return sorted((e for local in self.local_events.values() for e in local.events),
                      key=lambda e: (e.time, e.actor, e.node_id))

    def recent_events(self, actor: str, t: float, window: float) -> List[ReplayEvent]:
        """Events of ``actor`` in (t - window, t]."""
        local = self.local_events.get(actor)
        if local is None:
            return []
        return [e for e in local.events if t - window < e.time <= t + _EPS]

    def active_states(self, actor: str, t: float) -> List[StateInterval]:
        local = self.local_events.get(actor)
        return [] if local is None else [item for item in local.intervals if item.active_at(t)]

    def perceived_lines(self, actor: str, t: float) -> Optional[List[str]]:
        """The recorder's own perceived state at ``t`` as compact lines (tracks named
        as in ``subject_name``); None when the reconstruction wrote no perceived state."""
        perceived = self.perceived.get(actor)
        if perceived is None:
            return None
        return compact_state(perceived.state_at(t), lambda track: self.subject_name(actor, track))

    def collisions_near(self, t: float, window: float) -> List[CollisionMark]:
        """Collisions in (t - window, t]."""
        return [mark for mark in self.collisions if t - window < mark.time <= t + _EPS]

    def event_times(self) -> List[float]:
        times = sorted({e.time for e in self.all_events()} | {m.time for m in self.collisions})
        return [t for t in times if 0.0 - _EPS <= t <= self.duration + _EPS]

    def next_event_time(self, t: float) -> Optional[float]:
        return next((x for x in self.event_times() if x > t + _EPS), None)

    def previous_event_time(self, t: float) -> Optional[float]:
        return next((x for x in reversed(self.event_times()) if x < t - _EPS), None)

    def subject_name(self, actor: str, subject: Optional[str]) -> str:
        """``track_001 (B)`` when the fusion associated the track, else the local name."""
        if subject is None:
            return ""
        entity = self.identities.get((actor, subject))
        return subject if entity is None else "{0} ({1})".format(subject, entity)


# --------------------------------------------------------------------------
# Camera geometry (CARLA / Unreal conventions: x forward, y right, z up)
# --------------------------------------------------------------------------

Vector = Tuple[float, float, float]


def rotation_axes(yaw: float, pitch: float, roll: float = 0.0) -> Tuple[Vector, Vector, Vector]:
    """World-frame forward, right and up unit vectors of a rotation in degrees."""
    cy, sy = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    cp, sp = math.cos(math.radians(pitch)), math.sin(math.radians(pitch))
    cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
    forward = (cp * cy, cp * sy, sp)
    right = (sr * sp * cy - cr * sy, sr * sp * sy + cr * cy, -sr * cp)
    up = (-(cr * sp * cy + sr * sy), cy * sr - cr * sp * sy, cr * cp)
    return forward, right, up


def project(point: Vector, camera: Pose, fov_deg: float, width: int, height: int) -> Optional[Tuple[float, float]]:
    """Pixel of a world point in a pinhole camera (horizontal FOV), None if behind it."""
    forward, right, up = rotation_axes(camera.yaw, camera.pitch, camera.roll)
    d = (point[0] - camera.x, point[1] - camera.y, point[2] - camera.z)
    depth = sum(a * b for a, b in zip(d, forward))
    if depth < 0.1:
        return None
    focal = width / (2.0 * math.tan(math.radians(fov_deg) / 2.0))
    across = sum(a * b for a, b in zip(d, right))
    upward = sum(a * b for a, b in zip(d, up))
    return width / 2.0 + focal * across / depth, height / 2.0 - focal * upward / depth


def look_at(eye: Vector, target: Vector) -> Tuple[float, float]:
    """(yaw, pitch) in degrees that point a camera at ``eye`` towards ``target``."""
    dx, dy, dz = target[0] - eye[0], target[1] - eye[1], target[2] - eye[2]
    return math.degrees(math.atan2(dy, dx)), math.degrees(math.atan2(dz, math.hypot(dx, dy)))


def overview_camera(points: Sequence[Vector], heading: float, zoom: float = 1.0, elevation: float = 30.0) -> Pose:
    """Above and behind the centroid of ``points`` along ``heading``, looking at it.

    The distance grows with the spread of the points so that vehicles ahead
    and behind the centroid stay inside a 16:9 frame at the default zoom.
    """
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)
    cz = sum(p[2] for p in points) / len(points)
    spread = max(math.hypot(p[0] - cx, p[1] - cy) for p in points)
    distance = zoom * max(20.0, 2.2 * spread + 10.0)
    back, rise = distance * math.cos(math.radians(elevation)), distance * math.sin(math.radians(elevation))
    eye = (cx - back * math.cos(math.radians(heading)), cy - back * math.sin(math.radians(heading)), cz + rise)
    yaw, pitch = look_at(eye, (cx, cy, cz))
    return Pose(eye[0], eye[1], eye[2], yaw, pitch, 0.0)


def follow_camera(vehicle: Pose, orbit: float = 0.0, distance: float = 9.0, height: float = 3.5) -> Pose:
    """Behind the vehicle (rotated by ``orbit`` degrees around it), looking just ahead of it."""
    yaw = math.radians(vehicle.yaw + orbit)
    eye = (vehicle.x - distance * math.cos(yaw), vehicle.y - distance * math.sin(yaw), vehicle.z + height)
    ahead = math.radians(vehicle.yaw)
    target = (vehicle.x + 3.0 * math.cos(ahead), vehicle.y + 3.0 * math.sin(ahead), vehicle.z + 1.0)
    cam_yaw, cam_pitch = look_at(eye, target)
    return Pose(eye[0], eye[1], eye[2], cam_yaw, cam_pitch, 0.0)


class FreeCamera:
    """A camera moved by the user: translate in its own frame, turn by yaw/pitch."""

    def __init__(self, pose: Pose):
        self.x, self.y, self.z, self.yaw, self.pitch = pose.x, pose.y, pose.z, pose.yaw, pose.pitch

    def move(self, forward: float, right: float, up: float) -> None:
        cy, sy = math.cos(math.radians(self.yaw)), math.sin(math.radians(self.yaw))
        self.x += forward * cy - right * sy
        self.y += forward * sy + right * cy
        self.z += up

    def turn(self, d_yaw: float, d_pitch: float) -> None:
        self.yaw = (self.yaw + d_yaw + 180.0) % 360.0 - 180.0
        self.pitch = max(-89.0, min(89.0, self.pitch + d_pitch))

    @property
    def pose(self) -> Pose:
        return Pose(self.x, self.y, self.z, self.yaw, self.pitch, 0.0)
