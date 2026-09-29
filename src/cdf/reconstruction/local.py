"""Raw vehicle files -> local semantic trace -> sparse local event graph.

Only ``vehicles/<owner>/`` is read and only the recorder's own clock is used:

    t_local = source_timestamp - clock_origin

where ``clock_origin`` is, by default, this recorder's first ego sample.  The
CARLA frame counter is shared by all recorders and is therefore never used.
Nothing in this module looks at another recorder.

Continuous information becomes FACTS in the 10 Hz trace; discrete changes
become EVENTS, keep their exact local time, and are the nodes of the graph.
To add a new event type, write one more extractor below and call it in
``reconstruct_vehicle``.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..recording.compact_observations import load_observation_stream
from .config import CollisionConfig, ReconstructionConfig, SemanticsConfig
from .models import (ACTION, FACT, OUTCOME, PERCEPTION, PRECEDES, SAME_TRACK,
                     GraphEdge, GraphNode, LocalGraph, SemanticEvent, TraceFrame, same_time_rank)
from .tracking import (EgoTrajectory, LocalTrack, RadarMount, TrackSample,
                       build_local_tracks, ego_trajectory)

# The throttle must have been below its threshold this long before a new onset counts.
THROTTLE_REARM_S = 0.5
# A brake release shorter than this is a noisy dip, not the end of a braking episode.
BRAKE_RELEASE_DEBOUNCE_S = 0.2
# After a full stop the recorder must exceed this speed before another stop counts.
STOP_REARM_SPEED_MPS = 1.0
# Track episodes (closing, critical TTC) shorter than this are flicker, unless
# they last until the track ends.
MIN_EPISODE_S = 0.3
# A track must leave the path corridor by this margin before re-entering counts.
PATH_HYSTERESIS_M = 0.5


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _local_time(record: Mapping[str, Any], clock_origin: float, key: str = "timestamp") -> float:
    return round(float(record[key]) - clock_origin, 4)


# --------------------------------------------------------------------------
# Event extractors: each returns a list of SemanticEvent in local time
# --------------------------------------------------------------------------

def brake_episodes(owner: str, controls: Sequence[Mapping[str, Any]], clock_origin: float,
                   ego: EgoTrajectory, cfg: SemanticsConfig) -> List[SemanticEvent]:
    """One BRAKE_EPISODE per continuous braking action, from press to release.

    An episode starts at the first sample at or above ``brake_onset_threshold``
    and ends at the first sample below it, unless the brake comes back within
    BRAKE_RELEASE_DEBOUNCE_S (a short dip does not split one action).  An
    episode still active when the recording ends is ``released = False`` and
    ends at the last control sample.
    """
    times = [_local_time(record, clock_origin) for record in controls]
    brakes = [float(record["brake"]) for record in controls]
    spans = []  # (index of the first braking sample, index of the release sample or None)
    start: Optional[int] = None
    release: Optional[int] = None
    for index, brake in enumerate(brakes):
        if brake >= cfg.brake_onset_threshold:
            if start is None:
                start = index
            release = None  # braking again: the dip was shorter than the debounce
        elif start is not None:
            if release is None:
                release = index
            if times[index] - times[release] >= BRAKE_RELEASE_DEBOUNCE_S - 1e-6:
                spans.append((start, release))
                start = release = None
    if start is not None:
        spans.append((start, release))
    return [_brake_episode(owner, controls, times, brakes, ego, first, release) for first, release in spans]


def _brake_episode(owner: str, controls: Sequence[Mapping[str, Any]], times: List[float],
                   brakes: List[float], ego: EgoTrajectory, first: int, release: Optional[int]) -> SemanticEvent:
    """Summarise one braking interval; the samples themselves stay in the trace."""
    released = release is not None
    last = release - 1 if released else len(brakes) - 1  # last braking sample of the episode
    start_t = times[first]
    end_t = times[release] if released else times[-1]
    pressed = brakes[first:last + 1]
    speed_start = ego.at(start_t).speed
    speed_end = ego.at(end_t).speed
    speeds = [speed_start, speed_end] + [state.speed for state in ego.states
                                         if start_t <= state.t_local <= end_t]
    return SemanticEvent(
        type="BRAKE_EPISODE", kind=ACTION, actor_id=owner, t_local=start_t,
        attributes={"start_t_local": start_t, "end_t_local": end_t,
                    "duration_s": round(end_t - start_t, 3),
                    "peak_brake": round(max(pressed), 3),
                    "mean_brake": round(sum(pressed) / len(pressed), 3),
                    "speed_start_mps": round(speed_start, 2), "speed_end_mps": round(speed_end, 2),
                    "min_speed_mps": round(min(speeds), 2),
                    "delta_speed_mps": round(speed_end - speed_start, 2),
                    "released": released,
                    "began_before_recording": first == 0,
                    "n_samples": len(pressed),
                    "t_source": float(controls[first]["timestamp"])},
        source="controls")


def throttle_onsets(owner: str, controls: Sequence[Mapping[str, Any]], clock_origin: float,
                    ego: EgoTrajectory, cfg: SemanticsConfig) -> List[SemanticEvent]:
    """Strong throttle: first sample at or above ``throttle_onset_threshold``
    after the throttle stayed below it for THROTTLE_REARM_S."""
    events = []
    below_since: Optional[float] = None
    for record in controls:
        t_local = _local_time(record, clock_origin)
        value = float(record["throttle"])
        if value < cfg.throttle_onset_threshold:
            if below_since is None:
                below_since = t_local
            continue
        if below_since is not None and t_local - below_since >= THROTTLE_REARM_S:
            events.append(SemanticEvent(
                type="THROTTLE_ONSET", kind=ACTION, actor_id=owner, t_local=t_local,
                attributes={"throttle": round(value, 3), "speed_mps": round(ego.at(t_local).speed, 2),
                            "t_source": float(record["timestamp"])},
                source="controls"))
        below_since = None
    return events


def full_stops(owner: str, ego: EgoTrajectory, cfg: SemanticsConfig) -> List[SemanticEvent]:
    """The recorder's speed drops below ``full_stop_speed_mps`` after it was moving."""
    events = []
    armed = False
    states = ego.states
    for index, state in enumerate(states):
        if state.speed > STOP_REARM_SPEED_MPS:
            armed = True
        elif armed and state.speed < cfg.full_stop_speed_mps:
            armed = False
            restart = next((later.t_local for later in states[index:]
                            if later.speed > STOP_REARM_SPEED_MPS), None)
            events.append(SemanticEvent(
                type="FULL_STOP", kind=FACT, actor_id=owner, t_local=state.t_local,
                attributes={"speed_mps": round(state.speed, 3),
                            "stopped_for_s": round((restart if restart is not None else ego.end) - state.t_local, 2),
                            "stopped_until_recording_end": restart is None},
                source="ego"))
    return events


def collision_episodes(owner: str, collisions: Sequence[Mapping[str, Any]], clock_origin: float,
                       cfg: CollisionConfig) -> List[SemanticEvent]:
    """Collapse the collision sensor's per-frame callbacks into one event per contact."""
    episodes: List[Dict[str, Any]] = []
    for record in sorted(collisions, key=lambda item: float(item["timestamp"])):
        t_local = _local_time(record, clock_origin)
        impulse = float(record["impulse"])
        if episodes and t_local - episodes[-1]["last"] <= cfg.merge_gap_s:
            episodes[-1]["last"] = t_local
            episodes[-1]["impulses"].append(impulse)
        else:
            episodes.append({"first": t_local, "last": t_local, "impulses": [impulse],
                             "t_source": float(record["timestamp"])})
    return [SemanticEvent(
        type="COLLISION", kind=OUTCOME, actor_id=owner, t_local=episode["first"],
        attributes={"peak_impulse": round(max(episode["impulses"]), 2),
                    "total_impulse": round(sum(episode["impulses"]), 2),
                    "duration_s": round(episode["last"] - episode["first"], 3),
                    "n_callbacks": len(episode["impulses"]),
                    "t_source": episode["t_source"]},
        source="collision_sensor", confidence=1.0) for episode in episodes]


SIGN_EVENT_TYPES = {"STOP": "STOP_SIGN_DETECTED", "YIELD": "YIELD_SIGN_DETECTED"}


def sign_detections(owner: str, signs: Sequence[Mapping[str, Any]], clock_origin: float) -> List[SemanticEvent]:
    """One event per confirmed camera sign track, at its confirmation time."""
    events = []
    for record in signs:
        event_type = SIGN_EVENT_TYPES.get(str(record.get("class", "")).upper())
        if event_type is None:
            continue
        events.append(SemanticEvent(
            type=event_type, kind=PERCEPTION, actor_id=owner,
            subject_id="sign_" + str(record["sign_track_id"]),
            t_local=_local_time(record, clock_origin, "timestamp_confirmed"),
            attributes={"first_seen_t_local": _local_time(record, clock_origin, "timestamp_first"),
                        "last_seen_t_local": _local_time(record, clock_origin, "timestamp_last"),
                        "n_detections": record.get("n_detections"),
                        "relevant_to_ego_path": record.get("relevant_to_ego_path"),
                        "t_source": float(record["timestamp_confirmed"])},
            source="camera", confidence=round(float(record.get("best_confidence", 0.0)), 3)))
    return events


def _episodes(samples: Sequence[TrackSample], starts: Callable[[TrackSample], bool],
              continues: Callable[[TrackSample], bool]) -> List[Tuple[int, int]]:
    """Index ranges where ``starts`` switches on and ``continues`` holds (hysteresis)."""
    found = []
    begin: Optional[int] = None
    for index, sample in enumerate(samples):
        if begin is None:
            if starts(sample):
                begin = index
        elif not continues(sample):
            found.append((begin, index - 1))
            begin = None
    if begin is not None:
        found.append((begin, len(samples) - 1))
    last = len(samples) - 1
    return [(a, b) for a, b in found
            if b == last or samples[b].t_local - samples[a].t_local >= MIN_EPISODE_S]


def _track_event(owner: str, track: LocalTrack, event_type: str, sample: TrackSample,
                 attributes: Dict[str, Any]) -> SemanticEvent:
    return SemanticEvent(type=event_type, kind=PERCEPTION, actor_id=owner, subject_id=track.track_id,
                         t_local=round(sample.t_local, 4), attributes=attributes, source="radar")


def _where(sample: TrackSample) -> Dict[str, Any]:
    return {"range_m": round(sample.range_m, 2), "bearing_deg": round(sample.bearing_deg, 1),
            "lateral_m": round(sample.lateral_m, 2), "closing_speed_mps": round(sample.closing_speed_mps, 2)}


def track_events(owner: str, track: LocalTrack, recording_end: float, cfg: SemanticsConfig) -> List[SemanticEvent]:
    """Semantic transitions of one anonymous radar track."""
    samples = track.samples
    first = samples[0]
    in_path = first.longitudinal_m > 0 and abs(first.lateral_m) <= cfg.path_half_width_m
    events = [_track_event(owner, track, "TRACK_APPEARED", first, dict(
        _where(first), speed_mps=round(first.speed_mps, 2), in_ego_path=in_path))]

    # ENTERED_EGO_PATH: from clearly outside the straight-ahead corridor to inside it.
    outside_side: Optional[str] = None
    for index, sample in enumerate(samples):
        inside = sample.longitudinal_m > 0 and abs(sample.lateral_m) <= cfg.path_half_width_m
        if inside and outside_side is not None:
            before = samples[max(index - 2, 0)]
            dt = max(sample.t_local - before.t_local, 1e-6)
            events.append(_track_event(owner, track, "ENTERED_EGO_PATH", sample, dict(
                _where(sample), from_side=outside_side,
                longitudinal_m=round(sample.longitudinal_m, 2),
                lateral_speed_mps=round((sample.lateral_m - before.lateral_m) / dt, 2))))
            outside_side = None
        elif abs(sample.lateral_m) > cfg.path_half_width_m + PATH_HYSTERESIS_M:
            outside_side = "left" if sample.lateral_m < 0 else "right"

    threshold = cfg.closing_speed_threshold_mps
    for a, b in _episodes(samples, lambda s: s.closing_speed_mps >= threshold,
                          lambda s: s.closing_speed_mps >= threshold / 2.0):
        episode = samples[a:b + 1]
        events.append(_track_event(owner, track, "CLOSING", samples[a], dict(
            _where(samples[a]),
            peak_closing_speed_mps=round(max(s.closing_speed_mps for s in episode), 2),
            min_range_m=round(min(s.range_m for s in episode), 2),
            end_t_local=samples[b].t_local, duration_s=round(samples[b].t_local - samples[a].t_local, 2))))

    critical = cfg.critical_ttc_s
    for a, b in _episodes(samples,
                          lambda s: s.ttc_s is not None and s.ttc_s <= critical and s.closing_speed_mps >= threshold,
                          lambda s: s.ttc_s is not None and s.ttc_s <= critical):
        episode = samples[a:b + 1]
        events.append(_track_event(owner, track, "CRITICAL_TTC", samples[a], dict(
            _where(samples[a]), ttc_s=samples[a].ttc_s,
            min_ttc_s=min(s.ttc_s for s in episode if s.ttc_s is not None),
            end_t_local=samples[b].t_local)))

    last = samples[-1]
    if last.t_local < recording_end - 1e-3:
        events.append(_track_event(owner, track, "TRACK_LOST", last, dict(
            _where(last), tracked_for_s=round(last.t_local - first.t_local, 2))))
    return events


def number_events(owner: str, events: List[SemanticEvent], clock_origin: float) -> List[SemanticEvent]:
    """Sort by local time and give each event its graph id (A:e01, A:e02, ...)."""
    ordered = sorted(events, key=lambda event: (event.t_local, same_time_rank(event.type),
                                                 event.type, event.subject_id or ""))
    for index, event in enumerate(ordered, 1):
        event.event_id = "{0}:e{1:02d}".format(owner, index)
        event.attributes.setdefault("t_source", round(event.t_local + clock_origin, 6))
    return ordered


# --------------------------------------------------------------------------
# Facts and the 10 Hz local trace
# --------------------------------------------------------------------------

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
                clock_origin: float, trace_hz: float) -> List[TraceFrame]:
    """Sample what the recorder knows every 1/trace_hz seconds of its own clock.

    Each discrete event keeps its exact ``t_local`` and is listed once, in the
    first frame at or after it: frame t holds the events of (t - step, t].
    """
    step = 1.0 / trace_hz
    first = int(math.ceil(ego.start / step - 1e-6))
    last = int(math.floor(ego.end / step + 1e-6))
    by_frame: Dict[int, List[SemanticEvent]] = {}
    for event in events:
        index = min(max(int(math.ceil(event.t_local / step - 1e-6)), first), last)
        by_frame.setdefault(index, []).append(event)
    control_times = [_local_time(record, clock_origin) for record in controls]
    frames = []
    cursor = -1
    for index in range(first, last + 1):
        t_local = round(index * step, 4)
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
        frames.append(TraceFrame(t_local=t_local, facts=facts, events=by_frame.get(index, [])))
    return frames


# --------------------------------------------------------------------------
# Local graph: the trace's discrete events as nodes
# --------------------------------------------------------------------------

def build_local_graph(owner: str, trace: Sequence[TraceFrame], tracks: Sequence[LocalTrack],
                      recorder: Dict[str, Any]) -> LocalGraph:
    """Nodes are the trace's events; PRECEDES chains them in local time and
    SAME_TRACK links consecutive events about the same anonymous track."""
    events = sorted((event for frame in trace for event in frame.events), key=lambda event: event.event_id)
    nodes = [GraphNode.from_event(event) for event in events]
    edges = [GraphEdge(first.node_id, second.node_id, PRECEDES) for first, second in zip(nodes, nodes[1:])]
    previous: Dict[str, str] = {}
    for node in nodes:
        if node.subject_id and node.subject_id.startswith("track_"):
            if node.subject_id in previous:
                edges.append(GraphEdge(previous[node.subject_id], node.node_id, SAME_TRACK))
            previous[node.subject_id] = node.node_id
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


def reconstruct_vehicle(vehicle_dir: Path, cfg: ReconstructionConfig,
                        clock_origin: Optional[float] = None) -> LocalReconstruction:
    """vehicles/<owner>/ -> local trace, anonymous tracks and local event graph.

    ``clock_origin`` defaults to the recorder's first ego sample.  Passing
    another value emulates a recorder whose clock started at another moment;
    it exists for clock-robustness checks, never for synchronisation.
    """
    vehicle_dir = Path(vehicle_dir)
    owner = vehicle_dir.name
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
    events: List[SemanticEvent] = []
    events += brake_episodes(owner, controls, clock_origin, ego, semantics)
    events += throttle_onsets(owner, controls, clock_origin, ego, semantics)
    events += full_stops(owner, ego, semantics)
    events += collision_episodes(owner, collisions, clock_origin, cfg.collision)
    events += sign_detections(owner, signs, clock_origin)
    for track in tracks:
        events += track_events(owner, track, ego.end, semantics)
    events = number_events(owner, events, clock_origin)

    trace = build_trace(owner, ego, controls, tracks, events, clock_origin, cfg.trace_hz)
    recorder = {
        "owner": owner,
        "clock": {"origin_source_timestamp": clock_origin,
                  "definition": "t_local = source timestamp - origin (by default this recorder's first ego sample)"},
        "frame": {"definition": "origin = first ego position; x = first heading; "
                                "y = to the right of the first heading (CARLA convention)"},
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
