"""Raw vehicle files -> local semantic trace -> sparse local event graph.

Only ``vehicles/<owner>/`` is read, plus the run's supplied incident context
(the known speed limit), and only the recorder's own clock is used:

    t_local = source_timestamp - clock_origin

where ``clock_origin`` is, by default, this recorder's first ego sample.  The
CARLA frame counter is shared by all recorders and is therefore never used.
Nothing in this module looks at another recorder.

FACTS in the 10 Hz trace carry the quantitative evidence (speed, pedals,
ranges, TTC, ...).  EVENTS are the semantic transitions derived from the same
evidence, mostly NAME_START / NAME_END pairs, and they are the graph nodes.
The same intervals also feed the recorder's PERCEIVED STATE (``world_state``):
true / false / UNKNOWN per state, attached to every event as the state just
before it and to every trace frame.
To add a state: compute its ``active_intervals``, pass them to
``state_events`` and register the per-sample values with the world.
"""

from __future__ import annotations

import bisect
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..recording.compact_observations import load_observation_stream
from .config import CollisionConfig, ReconstructionConfig, SemanticsConfig
from .models import (ACTION, FACT, OUTCOME, PERCEPTION, SAME_TRACK, GraphEdge, GraphNode,
                     LocalGraph, SemanticEvent, TraceFrame, display_order, precedes_edges)
from .tracking import (EgoTrajectory, LocalTrack, RadarMount, TrackSample,
                       build_local_tracks, ego_trajectory)
from .world_state import PerceivedWorld, span_values

# A pedal release shorter than this is a noisy dip, not the end of the action.
PEDAL_RELEASE_DEBOUNCE_S = 0.2
# After a stop the recorder is moving again only above this speed (hysteresis).
MOVING_SPEED_MPS = 1.0
# Track states (closing, critical TTC) shorter than this are flicker, unless
# they are still active when the track ends.
MIN_EPISODE_S = 0.3
# A track must leave the path corridor by this margin before EGO_PATH_EXIT.
PATH_HYSTERESIS_M = 0.5
# The camera sign tracker ends a track after this gap without a detection
# (traffic_signs.max_time_gap_s), unless the vehicle metadata says otherwise.
DEFAULT_SIGN_TRACK_GAP_S = 0.6
# Local sign continuity: a sign track that starts within this gap after an
# earlier one of the same class vanished, at the same image place (centres and
# sizes of their best detections), while the recorder stood still (so image
# positions are comparable), is the same sign reacquired.
SIGN_REACQUIRE_MAX_GAP_S = 5.0
SIGN_REACQUIRE_MAX_SPEED_MPS = 0.5
SIGN_REACQUIRE_MAX_TURN_DEG = 3.0
SIGN_REACQUIRE_MAX_CENTRE_PX = 15.0
SIGN_REACQUIRE_MAX_SIZE_RATIO = 1.25

Span = Tuple[int, Optional[int]]


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _local_time(record: Mapping[str, Any], clock_origin: float, key: str = "timestamp") -> float:
    return round(float(record[key]) - clock_origin, 4)


# --------------------------------------------------------------------------
# States: every semantic event below starts or ends a state interval
# --------------------------------------------------------------------------

def active_intervals(times: Sequence[float], values: Sequence[Any], turns_on: Callable[[Any], bool],
                     turns_off: Callable[[Any], bool], release_debounce_s: float = 0.0,
                     initially_on: Optional[bool] = None) -> List[Span]:
    """(start, end) sample indices of the intervals in which a state is active.

    The state turns on at the first sample where ``turns_on`` holds and off at
    the first sample where ``turns_off`` holds; values satisfying neither keep
    the current state (hysteresis).  A release is ignored when the state turns
    on again within ``release_debounce_s``.  ``end`` is the first inactive
    sample, or None when the state is still active at the last sample.
    """
    spans: List[Span] = []
    start: Optional[int] = None
    release: Optional[int] = None
    for index, value in enumerate(values):
        if start is None:
            active = initially_on if index == 0 and initially_on is not None else turns_on(value)
            if active:
                start = index
            continue
        if turns_on(value):
            release = None
        elif release is None and turns_off(value):
            release = index
        if release is not None and times[index] - times[release] >= release_debounce_s - 1e-6:
            spans.append((start, release))
            start = release = None
    if start is not None:
        spans.append((start, None))
    return spans


def state_events(owner: str, subject: Optional[str], start_type: str, end_type: str, kind: str,
                 source: str, times: Sequence[float], spans: Sequence[Span],
                 announce_initial: bool = True) -> List[SemanticEvent]:
    """One start event and (unless still active at the end) one end event per interval.

    An interval active at the first sample began before it was observed: its
    start is marked ``active_at_first_observation``, or skipped entirely when
    ``announce_initial`` is False (a transition such as EGO_PATH_ENTRY that
    was never seen must not be invented).
    """
    events = []
    for start, end in spans:
        if start > 0 or announce_initial:
            attributes = {"active_at_first_observation": True} if start == 0 else {}
            events.append(SemanticEvent(type=start_type, kind=kind, actor_id=owner, subject_id=subject,
                                        t_local=times[start], attributes=attributes, source=source))
        if end is not None:
            events.append(SemanticEvent(type=end_type, kind=kind, actor_id=owner, subject_id=subject,
                                        t_local=times[end], source=source))
    return events


def _gaps(spans: Sequence[Span], count: int) -> List[Span]:
    """The intervals between active intervals (a stop is the time between movements)."""
    gaps: List[Span] = []
    cursor = 0
    for start, end in spans:
        if start > cursor:
            gaps.append((cursor, start))
        if end is None:
            return gaps
        cursor = end
    if cursor < count:
        gaps.append((cursor, None))
    return gaps


def _lasting(spans: Sequence[Span], times: Sequence[float]) -> List[Span]:
    """Drop flicker: intervals shorter than MIN_EPISODE_S, unless still active at the end."""
    return [(start, end) for start, end in spans
            if end is None or times[end] - times[start] >= MIN_EPISODE_S - 1e-6]


# --------------------------------------------------------------------------
# Event extractors: each returns SemanticEvents in the recorder's local time
# --------------------------------------------------------------------------

def control_events(owner: str, controls: Sequence[Mapping[str, Any]], clock_origin: float,
                   cfg: SemanticsConfig, world: Optional[PerceivedWorld] = None) -> List[SemanticEvent]:
    """BRAKE, HARD_BRAKE and STRONG_THROTTLE states from the recorder's own pedals.

    HARD_BRAKE nests inside BRAKE because its threshold is higher.  Pedal values
    stay in the EGO_CONTROL facts.
    """
    if not controls:
        return []
    times = [_local_time(record, clock_origin) for record in controls]
    brake = [float(record["brake"]) for record in controls]
    throttle = [float(record["throttle"]) for record in controls]

    def pedal_state(name: str, values: List[float], level: float) -> List[SemanticEvent]:
        spans = active_intervals(times, values, lambda value: value >= level, lambda value: value < level,
                                 PEDAL_RELEASE_DEBOUNCE_S)
        if world is not None:
            world.add_ego_state(name, times, spans)
        return state_events(owner, None, name + "_START", name + "_END", ACTION, "controls", times, spans)

    return (pedal_state("BRAKE", brake, cfg.brake_onset_threshold)
            + pedal_state("HARD_BRAKE", brake, cfg.hard_brake_threshold)
            + pedal_state("STRONG_THROTTLE", throttle, cfg.strong_throttle_threshold))


def motion_events(owner: str, ego: EgoTrajectory, cfg: SemanticsConfig,
                  speed_limit_kmh: Optional[float], world: Optional[PerceivedWorld] = None) -> List[SemanticEvent]:
    """MOVING and STOP states and, given a supplied speed limit, SPEED_LIMIT_EXCEEDED.

    A stop starts when moving ends (below ``full_stop_speed_mps``) and ends when
    moving restarts (above MOVING_SPEED_MPS).  Exceeding the limit needs a
    speed far above the stop thresholds, so it always nests inside MOVING.
    """
    times = [state.t_local for state in ego.states]
    speeds = [state.speed for state in ego.states]
    moving = active_intervals(times, speeds, lambda speed: speed > MOVING_SPEED_MPS,
                              lambda speed: speed < cfg.full_stop_speed_mps,
                              initially_on=speeds[0] >= cfg.full_stop_speed_mps)
    stopped = _gaps(moving, len(times))
    events = state_events(owner, None, "MOVING_START", "MOVING_END", FACT, "ego", times, moving)
    events += state_events(owner, None, "STOP_START", "STOP_END", FACT, "ego", times, stopped)
    if world is not None:
        world.add_ego_state("MOVING", times, moving)
        world.add_ego_state("STOP", times, stopped)
    if speed_limit_kmh is not None:
        limit = float(speed_limit_kmh) / 3.6
        margin = cfg.speed_limit_hysteresis_kmh / 3.6
        speeding = active_intervals(times, speeds, lambda speed: speed > limit + margin,
                                    lambda speed: speed <= limit - margin)
        events += state_events(owner, None, "SPEED_LIMIT_EXCEEDED_START", "SPEED_LIMIT_EXCEEDED_END",
                               FACT, "ego", times, speeding)
        if world is not None:
            world.add_ego_state("SPEED_LIMIT_EXCEEDED", times, speeding)
    elif world is not None:
        world.add_ego_unknown("SPEED_LIMIT_EXCEEDED", times[0])  # no limit supplied: cannot be established
    return events


def collision_events(owner: str, collisions: Sequence[Mapping[str, Any]], clock_origin: float,
                     cfg: CollisionConfig) -> List[SemanticEvent]:
    """One COLLISION per contact: callbacks closer than ``merge_gap_s`` are one contact.

    Only the peak impulse is kept: graph alignment needs it to recognise the
    same contact in two recorders.  Every callback stays in the raw log.
    """
    contacts: List[Dict[str, Any]] = []
    for record in sorted(collisions, key=lambda item: float(item["timestamp"])):
        t_local = _local_time(record, clock_origin)
        impulse = float(record["impulse"])
        if contacts and t_local - contacts[-1]["last"] <= cfg.merge_gap_s:
            contacts[-1]["last"] = t_local
            contacts[-1]["peak"] = max(contacts[-1]["peak"], impulse)
        else:
            contacts.append({"first": t_local, "last": t_local, "peak": impulse})
    return [SemanticEvent(type="COLLISION", kind=OUTCOME, actor_id=owner, t_local=contact["first"],
                          attributes={"peak_impulse": round(contact["peak"], 2)},
                          source="collision_sensor", confidence=1.0) for contact in contacts]


SIGN_STATES = {"STOP": "STOP_SIGN_DETECTED", "YIELD": "YIELD_SIGN_DETECTED"}


def _stood_still(ego: EgoTrajectory, start: float, end: float) -> bool:
    """The recorder did not move or turn between two of its own instants (odometry only)."""
    during = [state for state in ego.states if start - 1e-6 <= state.t_local <= end + 1e-6]
    turn = abs(math.degrees(ego.at(end).heading - ego.at(start).heading))
    return (bool(during) and turn <= SIGN_REACQUIRE_MAX_TURN_DEG
            and all(state.speed <= SIGN_REACQUIRE_MAX_SPEED_MPS for state in during))


def _same_image_place(first: Sequence[float], second: Sequence[float]) -> bool:
    (x1, y1, w1, h1), (x2, y2, w2, h2) = first, second
    if min(w1, h1, w2, h2) <= 0:
        return False
    centre = math.hypot((x1 + w1 / 2.0) - (x2 + w2 / 2.0), (y1 + h1 / 2.0) - (y2 + h2 / 2.0))
    return (centre <= SIGN_REACQUIRE_MAX_CENTRE_PX and max(w1 / w2, w2 / w1) <= SIGN_REACQUIRE_MAX_SIZE_RATIO
            and max(h1 / h2, h2 / h1) <= SIGN_REACQUIRE_MAX_SIZE_RATIO)


def sign_continuity(signs: Sequence[Mapping[str, Any]], clock_origin: float,
                    ego: Optional[EgoTrajectory]) -> Dict[str, str]:
    """Camera tracker id -> local sign id.

    A sign track is the same sign as an earlier one (and takes its id) only on
    conservative local evidence: same class, it starts within
    SIGN_REACQUIRE_MAX_GAP_S of the earlier one's last detection, at the same
    image place, and the recorder stood still in between, so that image
    positions are comparable.  Otherwise it stays a sign of its own.
    """
    ordered = sorted(signs, key=lambda record: float(record["timestamp_first"]))
    local_id: Dict[str, str] = {}
    for index, record in enumerate(ordered):
        track_id = str(record["sign_track_id"])
        local_id[track_id] = track_id
        if ego is None or not record.get("best_bbox"):
            continue
        first = _local_time(record, clock_origin, "timestamp_first")
        for earlier in reversed(ordered[:index]):
            if str(earlier.get("class", "")).upper() != str(record.get("class", "")).upper():
                continue
            last = _local_time(earlier, clock_origin, "timestamp_last")
            if (0.0 <= first - last <= SIGN_REACQUIRE_MAX_GAP_S and earlier.get("best_bbox")
                    and _stood_still(ego, last, first) and _same_image_place(earlier["best_bbox"], record["best_bbox"])):
                local_id[track_id] = local_id[str(earlier["sign_track_id"])]
                break
    return local_id


def sign_events(owner: str, signs: Sequence[Mapping[str, Any]], clock_origin: float,
                recording_end: float, track_gap_s: float, ego: Optional[EgoTrajectory] = None,
                world: Optional[PerceivedWorld] = None) -> List[SemanticEvent]:
    """A detection window per confirmed camera sign track.

    START: the track is confirmed, i.e. the detection is reliably established.
    END: its last detection, provided the recording lasted long enough for the
    tracker to give the track up; a sign still in view at the end has no END.
    END means this recorder no longer perceives the sign (it is no longer
    VISIBLE), not that the legal obligation it imposes ended; the sign stays
    KNOWN in the perceived state.  A track that reacquires an earlier sign
    (``sign_continuity``) keeps that sign's id, with ``reacquired`` and its own
    ``sign_track`` id as attributes.
    """
    events = []
    local_id = sign_continuity(signs, clock_origin, ego)
    for record in sorted(signs, key=lambda item: float(item["timestamp_first"])):
        name = SIGN_STATES.get(str(record.get("class", "")).upper())
        if name is None:
            continue
        track_id = str(record["sign_track_id"])  # the camera tracker's own id, e.g. sign-0
        subject = local_id[track_id]
        confidence = round(float(record.get("best_confidence", 0.0)), 3)
        start = _local_time(record, clock_origin, "timestamp_confirmed")
        # The detector's image-only judgement whether the sign governs this path.
        attributes: Dict[str, Any] = {"relevant_to_ego_path": bool(record.get("relevant_to_ego_path"))}
        if subject != track_id:
            attributes.update(reacquired=True, sign_track=track_id)
        events.append(SemanticEvent(
            type=name + "_START", kind=PERCEPTION, actor_id=owner, subject_id=subject,
            t_local=start, attributes=attributes, source="camera", confidence=confidence))
        last = _local_time(record, clock_origin, "timestamp_last")
        end = last if recording_end - last > track_gap_s else None
        if end is not None:
            events.append(SemanticEvent(type=name + "_END", kind=PERCEPTION, actor_id=owner,
                                        subject_id=subject, t_local=end, source="camera", confidence=confidence,
                                        attributes={} if subject == track_id else {"sign_track": track_id}))
        if world is not None:
            world.add_sign_window(subject, str(record.get("class", "")).upper(), start, end,
                                  bool(record.get("relevant_to_ego_path")))
    return events


def track_events(owner: str, track: LocalTrack, recording_end: float, cfg: SemanticsConfig,
                 world: Optional[PerceivedWorld] = None) -> List[SemanticEvent]:
    """TRACK_APPEARED / TRACK_LOST and the EGO_PATH, CLOSING and CRITICAL_TTC states of a track.

    Ranges, speeds and TTC stay in the TRACK_STATE facts.  With ``world``, the
    per-sample states are registered as the recorder's perceived state.
    """
    samples = track.samples
    times = [round(sample.t_local, 4) for sample in samples]
    subject = track.track_id
    events = [SemanticEvent(type="TRACK_APPEARED", kind=PERCEPTION, actor_id=owner, subject_id=subject,
                            t_local=times[0], source="radar")]

    # Inside: ahead and within the corridor.  Out again only when clearly beside
    # or behind the radar (at contact the target sits right at the radar plane).
    corridor = cfg.path_half_width_m
    path = active_intervals(times, samples,
                            lambda s: s.longitudinal_m > 0 and abs(s.lateral_m) <= corridor,
                            lambda s: (s.longitudinal_m < -PATH_HYSTERESIS_M
                                       or abs(s.lateral_m) > corridor + PATH_HYSTERESIS_M))
    # A track first seen inside the corridor has no observed entry.
    events += state_events(owner, subject, "EGO_PATH_ENTRY", "EGO_PATH_EXIT", PERCEPTION, "radar",
                           times, path, announce_initial=False)

    closing = cfg.closing_speed_threshold_mps
    spans = active_intervals(times, samples, lambda s: s.closing_speed_mps >= closing,
                             lambda s: s.closing_speed_mps < closing / 2.0)
    closing_spans = _lasting(spans, times)
    events += state_events(owner, subject, "CLOSING_START", "CLOSING_END", PERCEPTION, "radar",
                           times, closing_spans)

    # A critical TTC needs closing: it ends at the latest with CLOSING (at very
    # short range a slow residual closing speed would otherwise keep TTC low).
    critical = cfg.critical_ttc_s
    spans = active_intervals(times, samples,
                             lambda s: s.ttc_s is not None and s.ttc_s <= critical and s.closing_speed_mps >= closing,
                             lambda s: s.ttc_s is None or s.ttc_s > critical or s.closing_speed_mps < closing / 2.0)
    critical_spans = _lasting(spans, times)
    events += state_events(owner, subject, "CRITICAL_TTC_START", "CRITICAL_TTC_END", PERCEPTION, "radar",
                           times, critical_spans)

    lost_at = times[-1] if times[-1] < recording_end - 1e-3 else None
    if lost_at is not None:
        events.append(SemanticEvent(type="TRACK_LOST", kind=PERCEPTION, actor_id=owner, subject_id=subject,
                                    t_local=lost_at, source="radar"))
    if world is not None:
        count = len(times)
        world.add_track(subject, times, {
            "CLOSING": span_values(count, closing_spans),
            "CRITICAL_TTC": span_values(count, critical_spans),
            "IN_EGO_PATH": span_values(count, path),
        }, lost_at)
    return events


def number_events(owner: str, events: List[SemanticEvent]) -> List[SemanticEvent]:
    """Sort by local time (stable display order at equal times) and give graph ids."""
    ordered = display_order(events, lambda event: event.t_local, lambda event: event.type,
                            lambda event: event.actor_id, lambda event: event.subject_id)
    for index, event in enumerate(ordered, 1):
        event.event_id = "{0}:e{1:02d}".format(owner, index)
    return ordered


# --------------------------------------------------------------------------
# Facts and the 10 Hz local trace
# --------------------------------------------------------------------------

def _where(sample: TrackSample) -> Dict[str, Any]:
    return {"range_m": round(sample.range_m, 2), "bearing_deg": round(sample.bearing_deg, 1),
            "lateral_m": round(sample.lateral_m, 2), "closing_speed_mps": round(sample.closing_speed_mps, 2)}


def ego_motion_fact(owner: str, ego: EgoTrajectory, t_local: float) -> SemanticEvent:
    state = ego.at(t_local)
    before = ego.at(max(t_local - 0.1, ego.start))
    after = ego.at(min(t_local + 0.1, ego.end))
    dt = max(after.t_local - before.t_local, 1e-6)
    return SemanticEvent(type="EGO_MOTION", kind=FACT, actor_id=owner, t_local=t_local, source="ego",
                         attributes={"speed_mps": round(state.speed, 2),
                                     "acceleration_mps2": round((after.speed - before.speed) / dt, 2),
                                     "yaw_rate_dps": round(math.degrees(after.heading - before.heading) / dt, 1),
                                     "x_m": round(state.x, 2), "y_m": round(state.y, 2),
                                     "heading_deg": round(math.degrees(state.heading), 1)})


def ego_control_fact(owner: str, record: Mapping[str, Any], t_local: float) -> SemanticEvent:
    return SemanticEvent(type="EGO_CONTROL", kind=FACT, actor_id=owner, t_local=t_local, source="controls",
                         attributes={"throttle": round(float(record["throttle"]), 3),
                                     "brake": round(float(record["brake"]), 3),
                                     "steer": round(float(record["steer"]), 3)})


def track_state_fact(owner: str, track_id: str, sample: TrackSample, t_local: float) -> SemanticEvent:
    return SemanticEvent(type="TRACK_STATE", kind=FACT, actor_id=owner, subject_id=track_id,
                         t_local=t_local, source="radar", attributes=dict(
                             _where(sample), longitudinal_m=round(sample.longitudinal_m, 2),
                             ttc_s=None if sample.ttc_s is None else round(sample.ttc_s, 2),
                             speed_mps=round(sample.speed_mps, 2),
                             x_m=round(sample.x_m, 2), y_m=round(sample.y_m, 2),
                             pos_std_m=round(sample.pos_std_m, 2), measured=sample.measured))


def build_trace(owner: str, ego: EgoTrajectory, controls: Sequence[Mapping[str, Any]],
                tracks: Sequence[LocalTrack], events: Sequence[SemanticEvent],
                clock_origin: float, trace_hz: float,
                world: Optional[PerceivedWorld] = None) -> List[TraceFrame]:
    """Sample what the recorder knows every 1/trace_hz seconds of its own clock.

    When the recording ends between two grid instants, one last frame is added
    at the recording end, so no fact is extrapolated and no event is listed
    before it happens.  Each discrete event keeps its exact ``t_local`` and is
    listed once, in the first frame at or after it: frame t holds the events of
    (previous frame, t].  With ``world``, each frame also holds the recorder's
    perceived state at t (after the transitions at t).
    """
    step = 1.0 / trace_hz
    first = int(math.ceil(ego.start / step - 1e-6))
    last = int(math.floor(ego.end / step + 1e-6))
    times = [round(index * step, 4) for index in range(first, last + 1)]
    if ego.end - times[-1] > 1e-6:
        times.append(round(ego.end, 4))
    by_frame: Dict[int, List[SemanticEvent]] = {}
    for event in events:
        index = min(bisect.bisect_left(times, event.t_local - 1e-6), len(times) - 1)
        by_frame.setdefault(index, []).append(event)
    control_times = [_local_time(record, clock_origin) for record in controls]
    frames = []
    cursor = -1
    for index, t_local in enumerate(times):
        facts = [ego_motion_fact(owner, ego, t_local)]
        while cursor + 1 < len(controls) and control_times[cursor + 1] <= t_local + 1e-6:
            cursor += 1
        if cursor >= 0:
            facts.append(ego_control_fact(owner, controls[cursor], t_local))
        for track in tracks:
            if track.first_t - 1e-6 <= t_local <= track.last_t + 1e-6:
                sample = track.sample_near(t_local)
                if sample is not None:
                    facts.append(track_state_fact(owner, track.track_id, sample, t_local))
        frames.append(TraceFrame(t_local=t_local, facts=facts, events=by_frame.get(index, []),
                                 perceived_state=None if world is None else world.snapshot(t_local, before=False)))
    return frames


# --------------------------------------------------------------------------
# Local graph: the trace's discrete events as nodes
# --------------------------------------------------------------------------

def build_local_graph(owner: str, trace: Sequence[TraceFrame], tracks: Sequence[LocalTrack],
                      recorder: Dict[str, Any]) -> LocalGraph:
    """Nodes are the trace's events.  PRECEDES links each event to the events of
    the next later local time (simultaneous events stay unordered); SAME_TRACK
    links a track's TRACK_APPEARED to every later event about that track."""
    events = sorted((event for frame in trace for event in frame.events), key=lambda event: event.event_id)
    nodes = [GraphNode.from_event(event) for event in events]
    edges = precedes_edges(nodes, lambda node: node.t_local, lambda node: node.node_id)
    appeared = {node.subject_id: node.node_id for node in nodes if node.event_type == "TRACK_APPEARED"}
    for node in nodes:
        origin = appeared.get(node.subject_id) if node.subject_id else None
        if origin is not None and origin != node.node_id:
            edges.append(GraphEdge(origin, node.node_id, SAME_TRACK))
    return LocalGraph(owner=owner, nodes=nodes, edges=edges,
                      tracks=[track.summary() for track in tracks], recorder=recorder)


@dataclass
class LocalReconstruction:
    """Everything one recorder produces on its own, in its own clock and frame."""

    owner: str
    clock_origin: float
    ego: EgoTrajectory
    tracks: List[LocalTrack]
    trace: List[TraceFrame]
    graph: LocalGraph


def _sign_track_gap(vehicle_dir: Path) -> float:
    """The camera sign tracker's gap, as recorded in the vehicle's own metadata."""
    path = vehicle_dir / "metadata.json"
    if path.exists():
        signs = json.loads(path.read_text(encoding="utf-8")).get("traffic_signs") or {}
        if "max_time_gap_s" in signs:
            return float(signs["max_time_gap_s"])
    return DEFAULT_SIGN_TRACK_GAP_S


def reconstruct_vehicle(vehicle_dir: Path, cfg: ReconstructionConfig, clock_origin: Optional[float] = None,
                        context: Optional[Mapping[str, Any]] = None) -> LocalReconstruction:
    """vehicles/<owner>/ -> local trace, anonymous tracks and local event graph.

    ``context`` is the supplied incident context (``speed_limit_kmh``); it is
    known a priori, not perceived.  ``clock_origin`` defaults to the recorder's
    first ego sample; another value emulates a recorder whose clock started at
    another moment (clock-robustness checks only, never synchronisation).
    """
    vehicle_dir = Path(vehicle_dir)
    owner = vehicle_dir.name
    context = dict(context or {})
    ego_records = read_jsonl(vehicle_dir / "ego.jsonl")
    if not ego_records:
        raise ValueError("no ego.jsonl records in " + str(vehicle_dir))
    controls = read_jsonl(vehicle_dir / "controls.jsonl")
    collisions = read_jsonl(vehicle_dir / "collisions.jsonl")
    signs = read_jsonl(vehicle_dir / "traffic_signs.jsonl")
    if clock_origin is None:
        clock_origin = float(ego_records[0]["timestamp"])
    ego = ego_trajectory(ego_records, clock_origin)

    tracks: List[LocalTrack] = []
    if (vehicle_dir / "radar").exists():
        radar = load_observation_stream(vehicle_dir, source="radar")
        tracks = build_local_tracks(radar, ego, RadarMount.from_metadata(radar.metadata),
                                    clock_origin, cfg.tracking)

    semantics = cfg.semantics
    world = PerceivedWorld()
    events: List[SemanticEvent] = []
    events += control_events(owner, controls, clock_origin, semantics, world)
    events += motion_events(owner, ego, semantics, context.get("speed_limit_kmh"), world)
    events += collision_events(owner, collisions, clock_origin, cfg.collision)
    events += sign_events(owner, signs, clock_origin, ego.end, _sign_track_gap(vehicle_dir), ego, world)
    for track in tracks:
        events += track_events(owner, track, ego.end, semantics, world=world)
    events = number_events(owner, events)

    trace = build_trace(owner, ego, controls, tracks, events, clock_origin, cfg.trace_hz, world=world)
    frame_times = [frame.t_local for frame in trace]
    for event in events:
        # The state just before the event: all events at one timestamp share it.
        state = world.snapshot(event.t_local, before=True)
        # The latest trace frame before the event: its facts are the quantities behind this state.
        earlier = bisect.bisect_left(frame_times, event.t_local - 1e-6) - 1
        state["facts_t_local"] = frame_times[earlier] if earlier >= 0 else None
        event.perceived_state_before = state
    recorder = {
        "owner": owner,
        "clock": {"origin_source_timestamp": clock_origin,
                  "definition": "t_local = source timestamp - origin (by default this recorder's first ego sample)"},
        "frame": {"definition": "origin = first ego position; x = first heading; "
                                "y = to the right of the first heading (CARLA convention)"},
        "incident_context": context or None,
        "start_t_local": round(ego.start, 4),
        "end_t_local": round(ego.end, 4),
        "trace_hz": cfg.trace_hz,
        "trace_frames": len(trace),
        "inputs": sorted(name for name in ("ego.jsonl", "controls.jsonl", "collisions.jsonl",
                                           "traffic_signs.jsonl", "radar")
                         if (vehicle_dir / name).exists()),
    }
    graph = build_local_graph(owner, trace, tracks, recorder)
    return LocalReconstruction(owner=owner, clock_origin=clock_origin, ego=ego,
                               tracks=tracks, trace=trace, graph=graph)
