"""Raw vehicle files -> local semantic trace -> sparse local event graph.

Only ``vehicles/<owner>/`` is read, plus the run's supplied incident context
(the known speed limit), and only the recorder's own clock is used:

    t_local = source_timestamp - clock_origin

where ``clock_origin`` is, by default, this recorder's first ego sample.  The
CARLA frame counter is shared by all recorders and is therefore never used.
Nothing in this module looks at another recorder.

FACTS in the 10 Hz trace carry the quantitative evidence (speed, pedals,
ranges, TTC, relative motion, CPA, ...).  EVENTS are the semantic transitions
derived from the same evidence, mostly NAME_START / NAME_END pairs, and they
are the graph nodes.  The same intervals also feed the recorder's PERCEIVED
STATE (``world_state``): true / false / UNKNOWN per state, attached to every
event as the state just before it and to every trace frame.
To add a state: compute its ``active_intervals``, pass them to
``state_events`` and register the per-sample values with the world.
"""

from __future__ import annotations

import bisect
import json
import math
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..recording.compact_observations import load_radar_observations
from .config import CollisionConfig, ReconstructionConfig, SemanticsConfig
from .conflict import UNSAFE_FORWARD_GAP, ConflictAssessment, assess_conflict, occluded_by
from .models import (ACTION, FACT, OUTCOME, PERCEPTION, SAME_TRACK, GraphEdge, GraphNode,
                     LocalGraph, SemanticEvent, TraceFrame, display_order, precedes_edges)
from .tracking import (EgoFootprint, EgoState, EgoTrajectory, LocalTrack, RadarMount, RadarStream,
                       TrackSample, build_local_tracks, ego_trajectory)
from .world_state import UNKNOWN, PerceivedWorld, span_values

# A pedal release shorter than this is a noisy dip, not the end of the action.
PEDAL_RELEASE_DEBOUNCE_S = 0.2
# After a stop the recorder is moving again only above this speed (hysteresis).
MOVING_SPEED_MPS = 1.0
# Track states (closing, critical TTC) shorter than this are flicker, unless
# they are still active when the track ends.
MIN_EPISODE_S = 0.3
# A critical TTC must stay clearly resolved this long, without interruption, before it ends.
CRITICAL_RELEASE_DEBOUNCE_S = 0.2
# The camera sign tracker ends a track after this gap without a detection
# (traffic_signs.max_time_gap_s), unless the vehicle metadata says otherwise.
DEFAULT_SIGN_TRACK_GAP_S = 0.6
# Below this relative speed there is no closest point of approach to predict.
MIN_RELATIVE_SPEED_MPS = 0.3
# Qualitative motion relation of a track to the recorder (a TRACK_STATE fact).
SAME_DIRECTION_DEG, OPPOSING_DEG, CROSSING_DEG = 30.0, 150.0, (60.0, 120.0)
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
    """The BRAKE and THROTTLE states from the recorder's own pedals.

    BRAKE: at or above ``brake_onset_threshold``, ending below it.  THROTTLE:
    at or above ``throttle_on_threshold``, ending at or below
    ``throttle_off_threshold`` (hysteresis).  A release shorter than the
    debounce does not end either state.  The raw pedal and steering values
    (brake, throttle, steer) stay in the EGO_CONTROL facts.
    """
    if not controls:
        return []
    times = [_local_time(record, clock_origin) for record in controls]
    brake = [float(record["brake"]) for record in controls]
    level = cfg.brake_onset_threshold
    spans = active_intervals(times, brake, lambda value: value >= level, lambda value: value < level,
                             PEDAL_RELEASE_DEBOUNCE_S)
    throttle = [float(record["throttle"]) for record in controls]
    on, off = cfg.throttle_on_threshold, cfg.throttle_off_threshold
    throttle_spans = active_intervals(times, throttle, lambda value: value >= on, lambda value: value <= off,
                                      cfg.throttle_release_debounce_s)
    if world is not None:
        world.add_ego_state("BRAKE", times, spans)
        world.add_ego_state("THROTTLE", times, throttle_spans)
    return (state_events(owner, None, "BRAKE_START", "BRAKE_END", ACTION, "controls", times, spans)
            + state_events(owner, None, "THROTTLE_START", "THROTTLE_END", ACTION, "controls", times, throttle_spans))


def yaw_rates(ego: EgoTrajectory, window_s: float) -> List[float]:
    """Yaw rate [deg/s] at each ego sample: change of the unwrapped heading over
    the preceding ``window_s``, so a turn is never reported before its evidence
    (a spin starting at an impact does not appear before the impact).  Within
    the first window of the recording, that first window is used."""
    rates = []
    for state in ego.states:
        t0, t1 = state.t_local - window_s, state.t_local
        if t0 < ego.start:
            t0, t1 = ego.start, min(ego.start + window_s, ego.end)
        rates.append(0.0 if t1 - t0 < 1e-6 else math.degrees(ego.at(t1).heading - ego.at(t0).heading) / (t1 - t0))
    return rates


def turn_events(owner: str, ego: EgoTrajectory, cfg: SemanticsConfig,
                world: Optional[PerceivedWorld] = None) -> List[SemanticEvent]:
    """TURN_LEFT and TURN_RIGHT states: the yaw motion the recorder really
    performed, from its own odometry (never from the steer command).

    A turn starts when the yaw rate reaches ``turn_yaw_rate_on_dps`` while the
    recorder moves at ``turn_min_speed_mps`` or more, and ends when it stays
    below ``turn_yaw_rate_off_dps`` longer than ``turn_release_debounce_s``.  It
    must last ``turn_min_duration_s`` and change the heading by
    ``turn_min_heading_change_deg``, so lane changes and road curvature are not
    turns.  CARLA's yaw grows clockwise seen from above (x forward, y right): a
    left turn has a negative yaw rate.  This was checked on the recordings: in
    every driven turn the sign of the yaw change, the side the vehicle moved to
    and the sign of the steer command agree.  A spin after an impact is real yaw
    motion too and is reported as such.
    """
    times = [state.t_local for state in ego.states]
    headings = [state.heading for state in ego.states]
    speeds = [state.speed for state in ego.states]
    rates = yaw_rates(ego, cfg.turn_yaw_rate_window_s)
    events: List[SemanticEvent] = []
    for name, sign in (("TURN_LEFT", -1.0), ("TURN_RIGHT", 1.0)):
        def turns_on(index: int, sign: float = sign) -> bool:
            return speeds[index] >= cfg.turn_min_speed_mps and sign * rates[index] >= cfg.turn_yaw_rate_on_dps

        def turns_off(index: int, sign: float = sign) -> bool:
            return speeds[index] < cfg.turn_min_speed_mps or sign * rates[index] < cfg.turn_yaw_rate_off_dps

        kept = []
        for start, end in active_intervals(times, list(range(len(times))), turns_on, turns_off,
                                           cfg.turn_release_debounce_s):
            last = len(times) - 1 if end is None else end
            # The heading change counts from the turn's onset: back over the ramp where the yaw
            # rate already exceeded the off threshold, and the window that measured it.
            onset = start
            while onset > 0 and not turns_off(onset - 1):
                onset -= 1
            before = ego.at(max(times[onset] - cfg.turn_yaw_rate_window_s, ego.start)).heading
            change = sign * math.degrees(headings[last] - before)
            if (times[last] - times[start] >= cfg.turn_min_duration_s - 1e-6
                    and change >= cfg.turn_min_heading_change_deg):
                kept.append((start, end))
        if world is not None:
            world.add_ego_state(name, times, kept)
        events += state_events(owner, None, name + "_START", name + "_END", FACT, "ego", times, kept)
    return events


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


def sample_period(ego: EgoTrajectory) -> float:
    """The recorder's own sample period: the median interval between its ego samples.

    0 when unknown (a single sample): then every pause between callbacks is a break.
    """
    times = [float(t) for t in ego.times]
    return statistics.median(b - a for a, b in zip(times, times[1:])) if len(times) > 1 else 0.0


def velocity_jump(ego: EgoTrajectory, t_local: float, period: float) -> Tuple[float, float]:
    """The recorder's own velocity change from one sample before ``t_local`` to one after:
    (mean acceleration in m/s^2, direction in radians in the local frame)."""
    before, after = ego.at(t_local - period), ego.at(t_local + period)
    dvx, dvy = after.vx - before.vx, after.vy - before.vy
    return math.hypot(dvx, dvy) / (2.0 * period), math.atan2(dvy, dvx)


def impact_direction_angle(ego: EgoTrajectory, contact_t: float, burst_t: float, period: float,
                           cfg: CollisionConfig) -> Optional[float]:
    """Angle (deg) between the recorder's own velocity jumps at a contact's start and at a later burst.

    None unless both are impact-like (mean acceleration of at least
    ``impact_acceleration_mps2`` across the callback: no tyre can do that).
    """
    if period <= 0.0:
        return None
    first, second = velocity_jump(ego, contact_t, period), velocity_jump(ego, burst_t, period)
    if min(first[0], second[0]) < cfg.impact_acceleration_mps2:
        return None
    return abs(math.degrees(math.remainder(second[1] - first[1], 2.0 * math.pi)))


def collision_events(owner: str, collisions: Sequence[Mapping[str, Any]], clock_origin: float,
                     cfg: CollisionConfig, ego: EgoTrajectory) -> List[SemanticEvent]:
    """One COLLISION per contact, from the recorder's own collision sensor.

    The sensor calls back once per sample while the bodies touch and reports
    the impulse magnitude only (no partner).  Callbacks without a missing
    sample between them form a burst.  A burst more than ``merge_gap_s`` after
    the previous callback starts a new contact.  A burst after a shorter break
    (at least one sample without a callback) is judged by its peak relative to
    the current contact's peak:

    - weaker than ``min_new_impact_impulse``: the same contact (scraping or
      pushing along each other), whatever the ratio;
    - at least ``new_impact_ratio``: a new contact (a new impact);
    - below ``min_impact_ratio``: the same contact (persistent contact);
    - in between, the recorder's own velocity jumps decide when both, at the
      contact's start and at the burst's, are impact-like: in directions more
      than ``reversal_angle_deg`` apart a new contact (struck from the other
      side), otherwise the same one (a rebound pushes the same way again);
      without such evidence a new contact from ``undirected_impact_ratio``.

    The COLLISION is at the contact's first callback and keeps its peak
    impulse, which graph alignment needs to recognise the same contact in
    another recorder; a contact started within ``merge_gap_s`` of the previous
    one also states why.  A contact that absorbed later bursts lists them
    (``merged_bursts``: local time, peak impulse): another recorder may have
    reported one of them as a contact of its own (struck again by a third body
    within the same contact, as B in S06).  Every callback stays in the raw log.
    """
    period = sample_period(ego)
    bursts: List[Dict[str, Any]] = []
    for record in sorted(collisions, key=lambda item: float(item["timestamp"])):
        t_local = _local_time(record, clock_origin)
        impulse = float(record["impulse"])
        if bursts and t_local - bursts[-1]["last"] <= 1.5 * period:
            bursts[-1]["last"] = t_local
            bursts[-1]["peak"] = max(bursts[-1]["peak"], impulse)
        else:
            bursts.append({"first": t_local, "last": t_local, "peak": impulse})

    contacts: List[Dict[str, Any]] = []
    for burst in bursts:
        current = contacts[-1] if contacts else None
        attributes: Dict[str, Any] = {}
        if current is not None and burst["first"] - current["last"] <= cfg.merge_gap_s:
            ratio = burst["peak"] / current["peak"] if current["peak"] > 0 else math.inf
            angle = None
            if burst["peak"] < cfg.min_new_impact_impulse:
                new, evidence = False, None
            elif ratio >= cfg.new_impact_ratio:
                new, evidence = True, "peak"
            elif ratio < cfg.min_impact_ratio:
                new, evidence = False, None
            else:
                angle = impact_direction_angle(ego, current["first"], burst["first"], period, cfg)
                if angle is not None:
                    new, evidence = angle > cfg.reversal_angle_deg, "reversed velocity jump"
                else:
                    new, evidence = ratio >= cfg.undirected_impact_ratio, "peak without direction evidence"
            if not new:
                current["last"] = burst["last"]
                current["peak"] = max(current["peak"], burst["peak"])
                current["merged"].append(burst)
                continue
            attributes["new_contact"] = {"break_s": round(burst["first"] - current["last"], 2),
                                         "peak_ratio": round(ratio, 2), "evidence": evidence}
            if angle is not None:
                attributes["new_contact"]["reversal_deg"] = round(angle)
        contacts.append(dict(burst, attributes=attributes, merged=[]))
    events = []
    for contact in contacts:
        attributes = dict({"peak_impulse": round(contact["peak"], 2)}, **contact["attributes"])
        if contact["merged"]:
            attributes["merged_bursts"] = [[round(b["first"], 3), round(b["peak"], 2)] for b in contact["merged"]]
        events.append(SemanticEvent(type="COLLISION", kind=OUTCOME, actor_id=owner, t_local=contact["first"],
                                    attributes=attributes, source="collision_sensor", confidence=1.0))
    return events


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
    END means this recorder no longer perceives the sign, not that the legal
    obligation it imposes ended; the sign stays KNOWN in the perceived state
    from its first window on.  A track that reacquires an earlier sign
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
            world.add_sign(subject, str(record.get("class", "")).upper(), start, bool(record.get("relevant_to_ego_path")))
    return events


@dataclass
class RelativeMotion:
    """A track sample's motion relative to the recorder, in the recorder's current frame."""

    longitudinal_speed_mps: float  # target minus recorder, along the recorder's heading
    lateral_speed_mps: float  # + = to the recorder's right
    heading_deg: Optional[float]  # target's direction of motion minus the recorder's heading
    t_cpa_s: Optional[float]  # time of closest approach of the relative motion (None: no relative motion)
    d_cpa_m: Optional[float]  # predicted miss distance at that time, from the recorder's vehicle origin
    known: bool  # the estimate is precise enough for semantic claims
    d_cpa_clearance_m: Optional[float] = None  # smallest predicted clearance (near surface to footprint)


def relative_motion(sample: TrackSample, own: EgoState, cfg: SemanticsConfig,
                    footprint: Optional[EgoFootprint] = None) -> RelativeMotion:
    """Constant-velocity closest point of approach of the target relative to the recorder.

    r = (longitudinal, lateral) of the tracked point from the recorder's vehicle
    origin and v = target velocity - recorder velocity, both in the recorder's
    frame (non-rotating): t_CPA = -(r . v) / |v|^2 and d_CPA = |r + v t_CPA|.
    ``d_cpa_clearance_m`` is the smallest distance between the recorder's
    footprint and the target's near surface along that straight relative path
    over the conflict horizon (0 when the path enters the footprint).  Relative
    coordinates: unchanged by where the radars sit.
    """
    c, s = math.cos(own.heading), math.sin(own.heading)
    dvx, dvy = sample.vx_mps - own.vx, sample.vy_mps - own.vy
    v_long, v_lat = c * dvx + s * dvy, -s * dvx + c * dvy
    heading = None
    if sample.speed_mps >= 1.0:
        heading = (math.degrees(math.atan2(sample.vy_mps, sample.vx_mps) - own.heading) + 180.0) % 360.0 - 180.0
    speed2 = v_long * v_long + v_lat * v_lat
    t_cpa = d_cpa = d_cpa_clearance = None
    if speed2 >= MIN_RELATIVE_SPEED_MPS ** 2:
        t_cpa = -(sample.longitudinal_m * v_long + sample.lateral_m * v_lat) / speed2
        cpa_long, cpa_lat = sample.longitudinal_m + v_long * t_cpa, sample.lateral_m + v_lat * t_cpa
        d_cpa = math.hypot(cpa_long, cpa_lat)
        horizon = cfg.prediction_horizon_s
        start = (sample.longitudinal_m, sample.lateral_m)
        end = (sample.longitudinal_m + v_long * horizon, sample.lateral_m + v_lat * horizon)
        if footprint is not None:
            miss, _ = footprint.segment_distance(start, end)
        else:
            fraction = min(max(t_cpa / horizon, 0.0), 1.0)
            miss = math.hypot(start[0] + fraction * (end[0] - start[0]), start[1] + fraction * (end[1] - start[1]))
        d_cpa_clearance = max(miss - sample.surface_offset_m, 0.0)
    known = sample.pos_std_m <= cfg.max_position_std_m and sample.vel_std_mps <= cfg.max_velocity_std_mps
    return RelativeMotion(v_long, v_lat, heading, t_cpa, d_cpa, known, d_cpa_clearance)


def motion_relation(sample: TrackSample, motion: RelativeMotion, cfg: SemanticsConfig) -> str:
    """SAME_DIRECTION / OPPOSING / CROSSING, or UNKNOWN (slow, uncertain or oblique); a fact only."""
    if not motion.known or motion.heading_deg is None or sample.speed_mps < cfg.cut_in_min_target_speed_mps:
        return UNKNOWN
    angle = abs(motion.heading_deg)
    if angle <= SAME_DIRECTION_DEG:
        return "SAME_DIRECTION"
    if angle >= OPPOSING_DEG:
        return "OPPOSING"
    if CROSSING_DEG[0] <= angle <= CROSSING_DEG[1]:
        return "CROSSING"
    return UNKNOWN


def appearance_side(bearing_deg: float, cfg: SemanticsConfig) -> str:
    """FRONT, LEFT or RIGHT: where a track entered the recorder's radar field.

    From the track's own bearing at its first detection, seen from the
    recorder's vehicle origin (negative = left): within
    ``track_appeared_front_deg`` of the heading it appeared in front, otherwise
    on that side.  There is no rear radar: directly behind lies a blind zone, and
    a track first seen in a rear quarter appeared on that side.
    """
    if abs(bearing_deg) <= cfg.track_appeared_front_deg:
        return "FRONT"
    return "LEFT" if bearing_deg < 0 else "RIGHT"


def mark_occlusions(tracks: Sequence[LocalTrack], ego: EgoTrajectory, footprint: Optional[EgoFootprint],
                    cfg: SemanticsConfig) -> None:
    """Flag every track sample seen past another track of this recorder (``conflict.occluded_by``).

    Local to the recorder (its own tracks only).  An occluded sample gives no
    CUT_IN evidence and no UNSAFE_FORWARD_GAP evidence either way: a radar target
    behind or right beside a nearer vehicle returns only part of its body, and its
    returns can mix with that vehicle's (S16: the van seen past A from B; S17: C
    seen past A from B).  The collision-course prediction is not affected.
    """
    for track in tracks:
        others = [other for other in tracks if other is not track]
        for sample in track.samples:
            present = [near for near in (other.sample_near(sample.t_local) for other in others) if near is not None]
            sample.occluded = bool(present) and occluded_by(sample, ego.at(sample.t_local), present, footprint, cfg)


def _critical_assessments(samples: Sequence[TrackSample], ego: EgoTrajectory, cfg: SemanticsConfig,
                          footprint: Optional[EgoFootprint] = None) -> List[ConflictAssessment]:
    first = samples[0].t_local if samples else 0.0
    return [assess_conflict(sample, ego.at(sample.t_local), footprint, cfg, sample.t_local - first)
            for sample in samples]


def critical_intervals(times: Sequence[float], assessments: Sequence[ConflictAssessment],
                       release_deceleration_mps2: float,
                       release_debounce_s: float = CRITICAL_RELEASE_DEBOUNCE_S) -> List[Span]:
    """(start, end) sample indices of the CRITICAL_TTC intervals (``conflict`` module docstring, point 5).

    The state turns on at the first critical sample.  It ends only after a run of
    clearly resolved samples (``ConflictAssessment.released``) lasting
    ``release_debounce_s``; ``end`` is the run's first sample.  Any sample that is
    not clearly resolved -- critical, an uncertain estimate, occluded while the
    forward gap was a reason, near contact, a required deceleration within the
    hysteresis band -- interrupts the run: unknown is not safe.  The forward-gap
    release counts only when that reason was active in the episode, so a reason
    that never applied cannot hold the state.  ``end`` is None while still active
    at the last sample.
    """
    spans: List[Span] = []
    start: Optional[int] = None
    release: Optional[int] = None
    forward_engaged = False
    for index, assessment in enumerate(assessments):
        if assessment.critical:
            if start is None:
                start, forward_engaged = index, False
            forward_engaged = forward_engaged or UNSAFE_FORWARD_GAP in (assessment.critical_reason or "")
            release = None
            continue
        if start is None:
            continue
        if not assessment.released(release_deceleration_mps2, forward_engaged):
            release = None
            continue
        if release is None:
            release = index
        if times[index] - times[release] >= release_debounce_s - 1e-6:
            spans.append((start, release))
            start = release = None
    if start is not None:
        spans.append((start, None))
    return spans


def cut_in_spans(times: Sequence[float], samples: Sequence[TrackSample], motions: Sequence[RelativeMotion],
                 cfg: SemanticsConfig, body_gaps: Sequence[float]) -> Tuple[List[Span], List[Span]]:
    """(from-left, from-right) intervals of a lateral merge toward the recorder's path.

    Kinematic only: a target ahead of the recorder's front edge, moving within ``cut_in_max_heading_deg`` of
    the recorder's heading (so not crossing traffic), approaches the corridor
    laterally at ``cut_in_lateral_speed_mps`` or more without interruption.
    The cut-in STARTS once that run has lasted ``cut_in_persistence_s``,
    began at least ``cut_in_outside_margin_m`` outside the corridor, has moved
    the target ``cut_in_min_displacement_m`` closer, the corridor is due
    within ``cut_in_horizon_s`` at the current lateral speed, and the target's
    nominal body is already within ``cut_in_preentry_margin_m`` of the corridor
    (``body_gaps``, per sample: ``conflict.ForwardGap.lateral_body_gap_m``): a
    car still crossing a lane further away may be heading for the lane next to
    the recorder's, not for its path.  The side at the start gives the
    direction, from the recorder's viewpoint (negative lateral = left).  It
    ENDS once the lateral approach has stayed below ``cut_in_settle_speed_mps``
    for ``cut_in_settle_s``: a collision does not end it by itself.  Uncertain
    samples, and samples seen past another tracked vehicle
    (``TrackSample.occluded``), give no evidence either way.
    """
    corridor = cfg.path_half_width_m
    left: List[Span] = []
    right: List[Span] = []
    run: Optional[Tuple[int, int, float]] = None  # (start index, side, |lateral| at the start)
    active: Optional[Tuple[int, int]] = None  # (start index, side)
    settle: Optional[int] = None
    for index, (sample, motion) in enumerate(zip(samples, motions)):
        if not motion.known or sample.occluded:
            run, settle = (None if active is None else run), None
            continue
        if active is not None:
            start, side = active
            if -side * motion.lateral_speed_mps < cfg.cut_in_settle_speed_mps:
                settle = index if settle is None else settle
                if times[index] - times[settle] >= cfg.cut_in_settle_s - 1e-6:
                    (left if side < 0 else right).append((start, settle))
                    active, run, settle = None, None, None
            else:
                settle = None
            continue
        side = -1 if sample.lateral_m < 0 else 1
        toward = -side * motion.lateral_speed_mps
        parallel = (motion.heading_deg is not None and abs(motion.heading_deg) <= cfg.cut_in_max_heading_deg
                    and sample.speed_mps >= cfg.cut_in_min_target_speed_mps)
        if not (sample.ahead_m > 0 and parallel and toward >= cfg.cut_in_lateral_speed_mps):
            run = None
            continue
        if run is None or run[1] != side:
            run = (index, side, abs(sample.lateral_m))
        lateral = abs(sample.lateral_m)
        due = lateral <= corridor or (lateral - corridor) / toward <= cfg.cut_in_horizon_s
        if (run[2] >= corridor + cfg.cut_in_outside_margin_m
                and run[2] - lateral >= cfg.cut_in_min_displacement_m
                and times[index] - times[run[0]] >= cfg.cut_in_persistence_s - 1e-6 and due
                and body_gaps[index] <= cfg.cut_in_preentry_margin_m + 1e-9):
            active, settle = (index, run[1]), None
    if active is not None:
        (left if active[1] < 0 else right).append((active[0], None))
    return left, right


def _stationary_ego() -> EgoTrajectory:
    return EgoTrajectory([EgoState(t_local=0.0, x=0.0, y=0.0, heading=0.0, vx=0.0, vy=0.0)])


def track_events(owner: str, track: LocalTrack, recording_end: float, cfg: SemanticsConfig,
                 ego: Optional[EgoTrajectory] = None, world: Optional[PerceivedWorld] = None,
                 footprint: Optional[EgoFootprint] = None) -> List[SemanticEvent]:
    """TRACK_APPEARED_FRONT/LEFT/RIGHT, TRACK_LOST and the EGO_PATH, CLOSING,
    CRITICAL_TTC and CUT_IN states of a track.

    The appearance side comes from the track's bearing at its first detection
    (``appearance_side``); CRITICAL_TTC from ``conflict.assess_conflict``.
    Ranges, speeds, TTC, braking needs and the relative motion stay in the
    TRACK_STATE facts.
    ``ego`` is the recorder's own trajectory (relative motion needs its
    velocity); without it the recorder is taken as standing still.
    """
    ego = ego or _stationary_ego()
    samples = track.samples
    times = [round(sample.t_local, 4) for sample in samples]
    motions = [relative_motion(sample, ego.at(sample.t_local), cfg, footprint) for sample in samples]
    subject = track.track_id
    events = [SemanticEvent(type="TRACK_APPEARED_" + appearance_side(samples[0].bearing_deg, cfg), kind=PERCEPTION,
                            actor_id=owner, subject_id=subject, t_local=times[0], source="radar")]

    # Inside: ahead of the recorder's front edge and within the corridor.  Out
    # again only when clearly beside or behind that edge (at contact the target
    # sits right at it).
    corridor, hysteresis = cfg.path_half_width_m, cfg.path_hysteresis_m
    path = active_intervals(times, samples,
                            lambda s: s.ahead_m > 0 and abs(s.lateral_m) <= corridor,
                            lambda s: (s.ahead_m < -hysteresis
                                       or abs(s.lateral_m) > corridor + hysteresis))
    # A track first seen inside the corridor has no observed entry.
    events += state_events(owner, subject, "EGO_PATH_ENTRY", "EGO_PATH_EXIT", PERCEPTION, "radar",
                           times, path, announce_initial=False)

    closing = cfg.closing_speed_threshold_mps
    spans = active_intervals(times, samples, lambda s: s.closing_speed_mps >= closing,
                             lambda s: s.closing_speed_mps < closing / 2.0)
    closing_spans = _lasting(spans, times)
    events += state_events(owner, subject, "CLOSING_START", "CLOSING_END", PERCEPTION, "radar",
                           times, closing_spans)

    # A critical TTC (``conflict.assess_conflict``): a predicted collision course that
    # braking cannot avoid with the available deceleration (PREDICTED_OVERLAP), or a
    # leader closer than the safe following distance (UNSAFE_FORWARD_GAP).  It ends only
    # once the conflict is clearly resolved for the release debounce (``critical_intervals``):
    # no collision course or a required deceleration below ``critical_release_ratio`` of
    # the available one, no near contact, and a leader of the episode clearly gone.  The
    # reason is in the TRACK_STATE facts (``critical_reason``).
    assessments = _critical_assessments(samples, ego, cfg, footprint)
    release = cfg.critical_release_ratio * cfg.critical_deceleration_mps2
    spans = critical_intervals(times, assessments, release, CRITICAL_RELEASE_DEBOUNCE_S)
    critical_spans = _lasting(spans, times)
    first_known_critical = next((index for index, a in enumerate(assessments) if a.known), len(assessments))
    events += state_events(owner, subject, "CRITICAL_TTC_START", "CRITICAL_TTC_END", PERCEPTION, "radar",
                           times, critical_spans)

    # A cut-in can be established only once the estimate is precise enough.
    first_known = next((index for index, motion in enumerate(motions) if motion.known), len(motions))
    body_gaps = [a.forward.lateral_body_gap_m for a in assessments]
    from_left, from_right = cut_in_spans(times, samples, motions, cfg, body_gaps)
    events += state_events(owner, subject, "CUT_IN_FROM_LEFT_START", "CUT_IN_FROM_LEFT_END",
                           PERCEPTION, "radar", times, from_left)
    events += state_events(owner, subject, "CUT_IN_FROM_RIGHT_START", "CUT_IN_FROM_RIGHT_END",
                           PERCEPTION, "radar", times, from_right)

    lost_at = times[-1] if times[-1] < recording_end - 1e-3 else None
    if lost_at is not None:
        events.append(SemanticEvent(type="TRACK_LOST", kind=PERCEPTION, actor_id=owner, subject_id=subject,
                                    t_local=lost_at, source="radar"))
    if world is not None:
        count = len(times)
        world.add_track(subject, times, {
            "CLOSING": span_values(count, closing_spans),
            "CRITICAL_TTC": span_values(count, critical_spans, first_known_critical),
            "IN_EGO_PATH": span_values(count, path),
            "CUT_IN_FROM_LEFT": span_values(count, from_left, first_known),
            "CUT_IN_FROM_RIGHT": span_values(count, from_right, first_known),
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
    return {"range_m": round(sample.range_m, 2), "radar": sample.radar, "clearance_m": round(sample.clearance_m, 2),
            "bearing_deg": round(sample.bearing_deg, 1),
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


def _rounded(value: Optional[float], digits: int) -> Optional[float]:
    return None if value is None else round(value, digits)


def track_state_fact(owner: str, track_id: str, sample: TrackSample, t_local: float,
                     motion: Optional[RelativeMotion] = None, cfg: Optional[SemanticsConfig] = None,
                     conflict: Optional[ConflictAssessment] = None) -> SemanticEvent:
    """Quantitative state of a track: geometry (raw range from the radar that
    observed it, clearance from the recorder's footprint), its own velocity and
    acceleration in the local frame, uncertainty, the motion relative to the
    recorder and the collision-course prediction behind CRITICAL_TTC."""
    attributes = dict(_where(sample), longitudinal_m=round(sample.longitudinal_m, 2),
                      ahead_of_front_m=round(sample.ahead_m, 2), surface_offset_m=round(sample.surface_offset_m, 2),
                      closing_ttc_s=_rounded(sample.closing_ttc_s, 2),
                      speed_mps=round(sample.speed_mps, 2), acceleration_mps2=round(sample.acceleration_mps2, 2),
                      x_m=round(sample.x_m, 2), y_m=round(sample.y_m, 2),
                      vx_mps=round(sample.vx_mps, 2), vy_mps=round(sample.vy_mps, 2),
                      pos_std_m=round(sample.pos_std_m, 2), vel_std_mps=round(sample.vel_std_mps, 2),
                      measured=sample.measured)
    if motion is not None:
        attributes.update(
            relative_longitudinal_speed_mps=round(motion.longitudinal_speed_mps, 2),
            relative_lateral_speed_mps=round(motion.lateral_speed_mps, 2),
            relative_motion_angle_deg=_rounded(motion.heading_deg, 1),
            motion_relation=motion_relation(sample, motion, cfg or SemanticsConfig()),
            t_cpa_s=_rounded(motion.t_cpa_s, 2), d_cpa_m=_rounded(motion.d_cpa_m, 2),
            d_cpa_clearance_m=_rounded(motion.d_cpa_clearance_m, 2))
    if conflict is not None:
        required = conflict.required_deceleration_mps2
        attributes.update(
            ego_speed_mps=round(conflict.ego_speed_mps, 2), encounter=conflict.encounter,
            collision_course=conflict.collision_course, ttc_s=conflict.ttc_s,
            predicted_overlap_s=None if conflict.overlap_s is None else list(conflict.overlap_s),
            target_acceleration_used_mps2=round(conflict.target_acceleration_mps2, 2),
            required_deceleration_mps2=None if required is None or math.isinf(required) else round(required, 2),
            avoidance_by=conflict.avoidance_by,
            braking_margin_mps2=_rounded(conflict.braking_margin_mps2, 2),
            unavoidable_by_braking=required is not None and math.isinf(required),
            estimate_known=conflict.known, critical=conflict.critical, critical_reason=conflict.critical_reason,
            line_of_sight_occluded=conflict.occluded, inside_safety_envelope=conflict.inside_envelope)
        forward = conflict.forward
        if forward is not None:
            attributes.update(
                forward_region=forward.region, forward_leader=forward.leader,
                longitudinal_clearance_m=round(forward.longitudinal_clearance_m, 2),
                lateral_body_gap_m=round(forward.lateral_body_gap_m, 2),
                time_headway_s=_rounded(forward.time_headway_s, 2),
                minimum_time_gap_s=round(forward.minimum_time_gap_s, 3),
                time_gap_distance_m=round(forward.time_gap_distance_m, 2),
                required_safe_distance_m=round(forward.required_distance_m, 2),
                safe_distance_margin_m=round(forward.margin_m, 2))
    return SemanticEvent(type="TRACK_STATE", kind=FACT, actor_id=owner, subject_id=track_id,
                         t_local=t_local, source="radar", attributes=attributes)


def build_trace(owner: str, ego: EgoTrajectory, controls: Sequence[Mapping[str, Any]],
                tracks: Sequence[LocalTrack], events: Sequence[SemanticEvent],
                clock_origin: float, trace_hz: float, semantics: Optional[SemanticsConfig] = None,
                world: Optional[PerceivedWorld] = None, footprint: Optional[EgoFootprint] = None) -> List[TraceFrame]:
    """Sample what the recorder knows every 1/trace_hz seconds of its own clock.

    When the recording ends between two grid instants, one last frame is added
    at the recording end, so no fact is extrapolated and no event is listed
    before it happens.  Each discrete event keeps its exact ``t_local`` and is
    listed once, in the first frame at or after it: frame t holds the events of
    (previous frame, t].  With ``world``, each frame also holds the recorder's
    perceived state at t (after the transitions at t).
    """
    semantics = semantics or SemanticsConfig()
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
                    own = ego.at(sample.t_local)
                    motion = relative_motion(sample, own, semantics, footprint)
                    conflict = assess_conflict(sample, own, footprint, semantics, sample.t_local - track.first_t)
                    facts.append(track_state_fact(owner, track.track_id, sample, t_local, motion, semantics, conflict))
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
    links a track's TRACK_APPEARED_* to every later event about that track."""
    events = sorted((event for frame in trace for event in frame.events), key=lambda event: event.event_id)
    nodes = [GraphNode.from_event(event) for event in events]
    edges = precedes_edges(nodes, lambda node: node.t_local, lambda node: node.node_id)
    appeared = {node.subject_id: node.node_id for node in nodes if node.event_type.startswith("TRACK_APPEARED")}
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


def vehicle_metadata(vehicle_dir: Path) -> Dict[str, Any]:
    """The vehicle's own metadata.json ({} if absent)."""
    path = Path(vehicle_dir) / "metadata.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


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
    # The recorder's own shape (its bounding box, recorded with its metadata):
    # radar returns get clearances from its skin.
    footprint_record = vehicle_metadata(vehicle_dir).get("ego_footprint")
    footprint = EgoFootprint.from_metadata(footprint_record)
    streams: List[RadarStream] = []
    radar_stats: Dict[str, Any] = {}
    if (vehicle_dir / "radar").exists():
        # Every radar with its own mount: returns are placed from where they were measured.
        streams = [RadarStream(RadarMount.from_metadata(observations.metadata), observations)
                   for observations in load_radar_observations(vehicle_dir)]
        tracks = build_local_tracks(streams, ego, clock_origin, cfg.tracking, footprint, radar_stats)

    semantics = cfg.semantics
    mark_occlusions(tracks, ego, footprint, semantics)
    world = PerceivedWorld()
    events: List[SemanticEvent] = []
    events += control_events(owner, controls, clock_origin, semantics, world)
    events += motion_events(owner, ego, semantics, context.get("speed_limit_kmh"), world)
    events += turn_events(owner, ego, semantics, world)
    events += collision_events(owner, collisions, clock_origin, cfg.collision, ego)
    events += sign_events(owner, signs, clock_origin, ego.end, _sign_track_gap(vehicle_dir), ego, world)
    for track in tracks:
        events += track_events(owner, track, ego.end, semantics, ego, world, footprint)
    events = number_events(owner, events)

    trace = build_trace(owner, ego, controls, tracks, events, clock_origin, cfg.trace_hz, semantics, world,
                        footprint)
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
        "radar": None if not streams else {
            "radars": [{"sensor_id": stream.sensor_id,
                        "mount": {"x": round(stream.mount.x, 4), "y": round(stream.mount.y, 4),
                                  "z": round(stream.mount.z, 4), "yaw_deg": round(math.degrees(stream.mount.yaw), 3),
                                  "pitch_deg": round(math.degrees(stream.mount.pitch), 3)}} for stream in streams],
            "ego_footprint": footprint_record,
            "geometry": ("every return placed from its own radar's mount; its Doppler speed corrected by that "
                         "radar's own displacement; clearance = distance from the recorder's footprint to the "
                         "return (a track: to its near surface)") if footprint is not None
            else "own footprint unknown: clearance = distance from the vehicle origin",
            "own_body_returns_dropped": radar_stats.get("own_body_returns_dropped", 0)},
    }
    graph = build_local_graph(owner, trace, tracks, recorder)
    return LocalReconstruction(owner=owner, clock_origin=clock_origin, ego=ego,
                               tracks=tracks, trace=trace, graph=graph)
