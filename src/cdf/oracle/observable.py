"""The ground truth a reconstruction can actually be measured against.

The oracle this project started with mixed two different things. Some of what it
emitted was physical -- the vehicles really did come together, one really did
decelerate. The rest was the scenario's own script: a node recording that the
YAML fired an action, and a node asserting who had right of way. Those second
kinds are privileged knowledge of *intent*, and no reconstruction built from
telemetry, controls and radar can emit anything like them. Every edge touching
one was unmatchable however well the incident had been reconstructed, and just
over half the reference's edges touched one.

The damage ran the other way too. The old oracle asserted seven physical event
types; the reconstruction asserts twenty-one. Every one of the fourteen it had no
counterpart for was scored as a false positive. So the comparison penalised the
reconstruction for what the reference could not say, *and* for what the reference
did not bother to say, and the resulting F1 measured the vocabulary gap rather
than the method.

This module builds the other ground truth: the **observable** one. It asserts
only facts that both an exact simulator trace and an onboard reconstruction can
assert, in the vocabulary of :mod:`cdf.graph.ontology`, measured from exact
state. A correct reconstruction can match it node for node.

Independent measurement, shared definitions
-------------------------------------------

The line this module has to walk is narrow. If the oracle and the local extractor
shared their detection code, agreement would be true by construction and the
metric would measure nothing. If they did not share their *definitions*, the two
would be measuring different phenomena and disagreement would mean nothing
either.

So the thresholds are shared -- both sides read ``events.*`` from the same
configuration, because "what counts as hard deceleration" must mean one thing --
and the measurement is independent:

============================  ============================  =====================
Fact                          Local evidence                Oracle evidence
============================  ============================  =====================
``HARD_DECELERATION``         own accelerometer             exact velocity
                                                            differentiated
``RANGE_DECREASING``          radar returns clustered into  exact positions of
                              a track and differenced       both vehicles
``CRITICAL_TTC``              range / range-rate from       exact relative
                              radar                         geometry
``COLLISION``                 own contact trigger, with     the privileged
                              the counterparty inferred     collision record
============================  ============================  =====================

Same event, same definition, different instrument. That is the comparison the
project is supposed to be making.

What this module will not do
----------------------------

It emits no scripted-intervention node, reads no ``causal_template``, and branches
on no scenario id. Those live in the scenario design reference, which answers a
different question -- "did the designed mechanism execute?" -- and is never the
reference for judging a reconstruction.

It also emits no radar-track events. The simulator has vehicles, not tracks;
there is no privileged counterpart to a track appearing, and inventing one would
be scoring the reconstruction against a fiction.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import Event, EventType, Evidence, Provenance, make_event_id
from ..graph.ontology import COMPARABLE_EVENT_TYPES

__all__ = [
    "build_observable_events",
    "ObservableExtractor",
    "pairwise_truth",
]


# ---------------------------------------------------------------------------
# Reading the privileged trace
# ---------------------------------------------------------------------------


def _series(trace: Mapping[str, Any], participant_id: str) -> List[Dict[str, Any]]:
    """Every recorded state of one participant, time-ordered."""
    out: List[Dict[str, Any]] = []
    for frame in trace.get("frames", []) or []:
        for actor in frame.get("actors", []) or []:
            if str(actor.get("participant_id")) == str(participant_id):
                row = dict(actor)
                row["t"] = float(frame.get("t", 0.0))
                out.append(row)
                break
    out.sort(key=lambda r: r["t"])
    return out


def _longitudinal_acceleration(rows: Sequence[Mapping[str, Any]]) -> List[float]:
    """Acceleration along the direction of travel, from exact velocity.

    Differentiated from the recorded velocity rather than taken from the
    simulator's own ``ax``/``ay``, which are world-frame and include gravity on a
    slope. A vehicle computes the same quantity from its accelerometer; this is
    the privileged way to the same number.
    """
    out: List[float] = []
    for index, row in enumerate(rows):
        if index == 0:
            out.append(0.0)
            continue
        previous = rows[index - 1]
        dt = float(row["t"]) - float(previous["t"])
        if dt <= 0.0:
            out.append(out[-1])
            continue
        out.append((float(row["speed"]) - float(previous["speed"])) / dt)
    return out


def pairwise_truth(
    trace: Mapping[str, Any], observer: str, target: str
) -> List[Dict[str, Any]]:
    """Exact relative geometry of one ordered pair, frame by frame.

    This is the privileged counterpart of a radar track: the range, bearing and
    range rate a perfect sensor would have measured. It is the evidence the
    pairwise events are built from, and it is persisted as ``radar_truth`` so a
    reader can check any pairwise claim against the geometry behind it.
    """
    a_rows = {round(float(r["t"]), 6): r for r in _series(trace, observer)}
    b_rows = {round(float(r["t"]), 6): r for r in _series(trace, target)}
    out: List[Dict[str, Any]] = []
    previous: Optional[Dict[str, Any]] = None
    for t in sorted(set(a_rows) & set(b_rows)):
        a, b = a_rows[t], b_rows[t]
        dx = float(b["x"]) - float(a["x"])
        dy = float(b["y"]) - float(a["y"])
        distance = math.hypot(dx, dy)

        # Bearing of the target in the observer's body frame: 0 straight ahead,
        # positive to the left, which is the convention the radar uses.
        yaw = math.radians(float(a["yaw"]))
        cos_yaw, sin_yaw = math.cos(yaw), math.sin(yaw)
        forward = dx * cos_yaw + dy * sin_yaw
        lateral = -dx * sin_yaw + dy * cos_yaw
        bearing = math.degrees(math.atan2(lateral, forward))

        dvx = float(b["vx"]) - float(a["vx"])
        dvy = float(b["vy"]) - float(a["vy"])
        # Range rate is the component of relative velocity along the line of
        # sight. Negative means closing, as a radar reports it.
        range_rate = ((dx * dvx + dy * dvy) / distance) if distance > 1e-6 else 0.0

        row = {
            "t": t,
            "observer": observer,
            "target": target,
            "range_m": distance,
            "bearing_deg": bearing,
            "longitudinal_m": forward,
            "lateral_m": lateral,
            "range_rate_mps": range_rate,
            "closing_rate_mps": -range_rate,
            "relative_vx": dvx,
            "relative_vy": dvy,
            "target_speed_mps": float(b["speed"]),
            "observer_speed_mps": float(a["speed"]),
        }
        if previous is not None:
            dt = t - previous["t"]
            if dt > 0:
                row["lateral_rate_mps"] = (lateral - previous["lateral_m"]) / dt
            else:
                row["lateral_rate_mps"] = 0.0
        else:
            row["lateral_rate_mps"] = 0.0
        # Time to collision along the line of sight, defined only while closing.
        row["ttc_s"] = (
            distance / -range_rate if range_rate < -1e-6 else None
        )
        out.append(row)
        previous = row
    return out


# ---------------------------------------------------------------------------
# Episodes
# ---------------------------------------------------------------------------


class _Episode(object):
    """A contiguous stretch during which a condition held."""

    __slots__ = ("t_start", "t_end", "t_peak", "peak_value", "n_samples")

    def __init__(self, t_start: float, t_end: float, t_peak: float,
                 peak_value: float, n_samples: int) -> None:
        self.t_start = t_start
        self.t_end = t_end
        self.t_peak = t_peak
        self.peak_value = peak_value
        self.n_samples = n_samples


def _episodes(
    times: Sequence[float],
    values: Sequence[Optional[float]],
    enter: float,
    release: float,
    min_duration_s: float,
    above: bool = True,
) -> List[_Episode]:
    """Hysteresis episode detection, identical in shape to the local extractor's.

    Sharing the *shape* of the detector is deliberate and is not the same as
    sharing the detector: what differs is the series fed into it. A vehicle feeds
    it radar estimates; this feeds it exact geometry. Using a different episode
    rule on each side would make every disagreement ambiguous between "the
    reconstruction was wrong" and "the two counted episodes differently".
    """
    out: List[_Episode] = []
    active = False
    start = peak_t = 0.0
    peak = 0.0
    count = 0

    def passes(value: float, threshold: float) -> bool:
        return value >= threshold if above else value <= threshold

    for t, raw in zip(times, values):
        if raw is None:
            value = None
        else:
            value = float(raw)
        if value is not None and passes(value, enter):
            if not active:
                active, start, peak, peak_t, count = True, t, value, t, 0
            count += 1
            if (value > peak) if above else (value < peak):
                peak, peak_t = value, t
        elif active and (value is None or not passes(value, release)):
            if t - start >= min_duration_s:
                out.append(_Episode(start, t, peak_t, peak, count))
            active = False
    if active and times and times[-1] - start >= min_duration_s:
        out.append(_Episode(start, times[-1], peak_t, peak, count))
    return out


# ---------------------------------------------------------------------------
# The extractor
# ---------------------------------------------------------------------------


class ObservableExtractor(object):
    """Measures the comparable vocabulary from one run's privileged trace."""

    def __init__(self, trace: Mapping[str, Any], cfg: Config) -> None:
        self.trace = trace
        self.cfg = cfg
        self.participants = [str(p) for p in trace.get("participants", []) or []]
        self._rows: Dict[str, List[Dict[str, Any]]] = {
            pid: _series(trace, pid) for pid in self.participants
        }
        self._accel: Dict[str, List[float]] = {
            pid: _longitudinal_acceleration(rows) for pid, rows in self._rows.items()
        }
        self.min_duration = float(cfg.get("events.min_duration_s", 0.10))
        self.hysteresis = float(cfg.get("events.hysteresis_ratio", 0.75))

    # -- helpers ----------------------------------------------------------

    def _times(self, pid: str) -> List[float]:
        return [float(r["t"]) for r in self._rows[pid]]

    def _event(
        self,
        event_type: EventType,
        participant_id: str,
        t_start: float,
        t_peak: float,
        t_end: float,
        values: Dict[str, float],
        subject: Optional[str] = None,
        evidence_kind: str = "privileged_state",
        detail: Optional[Dict[str, Any]] = None,
    ) -> Event:
        """One observable event, with the privileged evidence that produced it."""
        if event_type.value not in COMPARABLE_EVENT_TYPES:
            raise ValueError(
                "observable ground truth may only emit the comparable "
                "vocabulary; {0} is outside it".format(event_type.value)
            )
        event_id = make_event_id(
            "oracle_obs", participant_id, event_type.value, t_peak, subject
        )
        return Event(
            event_id=event_id,
            event_type=event_type,
            participant_id=participant_id,
            t_start=float(t_start),
            t_peak=float(t_peak),
            t_end=float(t_end),
            subject=subject,
            values={k: float(v) for k, v in values.items() if v is not None},
            # Ground truth is measured, not estimated: it is certain of what it
            # saw. The confidence field exists so a consumer can treat both
            # sides uniformly, not because the oracle is unsure.
            confidence=1.0,
            evidence=[
                Evidence(
                    kind=evidence_kind,
                    ref="oracle_trace",
                    t_start=float(t_start),
                    t_end=float(t_end),
                    detail=dict(detail or {}),
                )
            ],
            provenance=Provenance.ORACLE,
            owners=[participant_id] + ([subject] if subject else []),
        )

    # -- own motion -------------------------------------------------------

    def own_motion_events(self) -> List[Event]:
        """What each vehicle did, from its exact controls and exact velocity."""
        events: List[Event] = []
        for pid in self.participants:
            rows = self._rows[pid]
            if not rows:
                continue
            times = self._times(pid)
            accel = self._accel[pid]
            speeds = [float(r["speed"]) for r in rows]
            brake = [float(r.get("brake", 0.0)) for r in rows]
            throttle = [float(r.get("throttle", 0.0)) for r in rows]
            steer = [abs(float(r.get("steer", 0.0))) for r in rows]

            events.extend(self._vehicle_started(pid, times, speeds))
            events.extend(self._threshold_events(
                pid, times, accel, EventType.ACCELERATION,
                float(self.cfg.get("events.acceleration.enter_mps2", 1.5)),
                above=True, value_name="accel_mps2",
            ))
            events.extend(self._threshold_events(
                pid, times, accel, EventType.DECELERATION,
                float(self.cfg.get("events.deceleration.enter_mps2", -1.8)),
                above=False, value_name="accel_mps2",
            ))
            events.extend(self._threshold_events(
                pid, times, accel, EventType.HARD_DECELERATION,
                float(self.cfg.get("events.hard_deceleration.enter_mps2", -4.5)),
                above=False, value_name="accel_mps2",
            ))
            events.extend(self._threshold_events(
                pid, times, brake, EventType.BRAKE_ONSET,
                float(self.cfg.get("events.brake_onset.brake_cmd", 0.12)),
                above=True, value_name="brake_cmd",
            ))
            events.extend(self._threshold_events(
                pid, times, brake, EventType.HARD_BRAKE,
                float(self.cfg.get("events.hard_brake.brake_cmd", 0.65)),
                above=True, value_name="brake_cmd",
            ))
            events.extend(self._threshold_events(
                pid, times, throttle, EventType.THROTTLE_ONSET,
                float(self.cfg.get("events.throttle_onset.throttle_cmd", 0.25)),
                above=True, value_name="throttle_cmd",
            ))
            events.extend(self._threshold_events(
                pid, times, steer, EventType.STEER_ONSET,
                float(self.cfg.get("events.steer_onset.steer_cmd", 0.14)),
                above=True, value_name="steer_cmd",
            ))
            events.extend(self._heading_change(pid, rows))
            events.extend(self._lane_change_like(pid, rows))
        return events

    def _vehicle_started(
        self, pid: str, times: Sequence[float], speeds: Sequence[float]
    ) -> List[Event]:
        threshold = float(self.cfg.get("events.vehicle_started.speed_mps", 0.8))
        for t, speed in zip(times, speeds):
            if speed >= threshold:
                return [self._event(
                    EventType.VEHICLE_STARTED, pid, t, t, t,
                    {"speed_mps": speed},
                    detail={"threshold_mps": threshold},
                )]
        return []

    def _threshold_events(
        self,
        pid: str,
        times: Sequence[float],
        values: Sequence[float],
        event_type: EventType,
        enter: float,
        above: bool,
        value_name: str,
    ) -> List[Event]:
        release = enter * self.hysteresis
        found = _episodes(times, values, enter, release, self.min_duration, above)
        return [
            self._event(
                event_type, pid, ep.t_start, ep.t_peak, ep.t_end,
                {value_name: ep.peak_value},
                detail={"enter": enter, "release": release, "n_samples": ep.n_samples},
            )
            for ep in found
        ]

    def _heading_change(self, pid: str, rows: Sequence[Mapping[str, Any]]) -> List[Event]:
        """Total heading change exceeding a threshold within a window."""
        total_deg = float(self.cfg.get("events.heading_change.total_deg", 12.0))
        window_s = float(self.cfg.get("events.heading_change.window_s", 1.5))
        out: List[Event] = []
        last_end = -1e9
        for index, row in enumerate(rows):
            t0 = float(row["t"])
            if t0 < last_end:
                continue
            yaw0 = float(row["yaw"])
            for other in rows[index + 1:]:
                t1 = float(other["t"])
                if t1 - t0 > window_s:
                    break
                change = abs(_wrap_deg(float(other["yaw"]) - yaw0))
                if change >= total_deg:
                    out.append(self._event(
                        EventType.SIGNIFICANT_HEADING_CHANGE, pid, t0, t1, t1,
                        {"heading_change_deg": change},
                        detail={"window_s": window_s, "threshold_deg": total_deg},
                    ))
                    last_end = t1
                    break
        return out

    def _lane_change_like(
        self, pid: str, rows: Sequence[Mapping[str, Any]]
    ) -> List[Event]:
        """Lateral displacement relative to the vehicle's own heading.

        The privileged version of the same question a vehicle asks of its own
        trajectory: did I move sideways by more than a lane width without
        turning? The map is deliberately not consulted -- lane geometry is
        privileged in a way the reconstruction has no counterpart for, and using
        it here would put the reference outside the shared vocabulary again.
        """
        offset_m = float(self.cfg.get("events.lane_change_like.lateral_offset_m", 1.8))
        window_s = float(self.cfg.get("events.lane_change_like.window_s", 3.0))
        max_heading = float(
            self.cfg.get("events.lane_change_like.max_heading_change_deg", 45.0)
        )
        out: List[Event] = []
        last_end = -1e9
        for index, row in enumerate(rows):
            t0 = float(row["t"])
            if t0 < last_end:
                continue
            yaw0 = math.radians(float(row["yaw"]))
            x0, y0 = float(row["x"]), float(row["y"])
            for other in rows[index + 1:]:
                t1 = float(other["t"])
                if t1 - t0 > window_s:
                    break
                heading_change = abs(_wrap_deg(float(other["yaw"]) - float(row["yaw"])))
                if heading_change > max_heading:
                    break  # a turn, not a lane change
                dx, dy = float(other["x"]) - x0, float(other["y"]) - y0
                lateral = abs(-dx * math.sin(yaw0) + dy * math.cos(yaw0))
                if lateral >= offset_m:
                    out.append(self._event(
                        EventType.LANE_CHANGE_LIKE_MANEUVER, pid, t0, t1, t1,
                        {"lateral_offset_m": lateral,
                         "heading_change_deg": heading_change},
                        detail={"window_s": window_s, "threshold_m": offset_m},
                    ))
                    last_end = t1
                    break
        return out

    # -- pairwise ---------------------------------------------------------

    def pairwise_events(self) -> List[Event]:
        """What was true of each ordered pair, from exact relative geometry."""
        events: List[Event] = []
        for observer in self.participants:
            for target in self.participants:
                if observer == target:
                    continue
                rows = pairwise_truth(self.trace, observer, target)
                if not rows:
                    continue
                events.extend(self._pair_events(observer, target, rows))
        return events

    def _pair_events(
        self, observer: str, target: str, rows: Sequence[Mapping[str, Any]]
    ) -> List[Event]:
        out: List[Event] = []
        times = [float(r["t"]) for r in rows]
        closing = [float(r["closing_rate_mps"]) for r in rows]
        ttc = [r["ttc_s"] for r in rows]
        lateral_rate = [abs(float(r["lateral_rate_mps"])) for r in rows]
        ranges = [float(r["range_m"]) for r in rows]

        radar = "events.radar."
        out.extend(self._pair_threshold(
            observer, target, times, closing, EventType.RANGE_DECREASING,
            float(self.cfg.get(radar + "range_decreasing.min_rate_mps", 1.0)),
            above=True, value_name="closing_rate_mps",
            min_duration=float(
                self.cfg.get(radar + "range_decreasing.min_duration_s", 0.6)
            ),
            rows=rows,
        ))
        out.extend(self._pair_threshold(
            observer, target, times, closing, EventType.RAPID_CLOSING,
            float(self.cfg.get(radar + "rapid_closing.min_rate_mps", 6.0)),
            above=True, value_name="closing_rate_mps", rows=rows,
        ))
        # TTC episodes are "below a threshold", and an undefined TTC (not
        # closing) must break the episode rather than extend it.
        out.extend(self._pair_threshold(
            observer, target, times, ttc, EventType.LOW_TTC,
            float(self.cfg.get(radar + "low_ttc.ttc_s", 3.0)),
            above=False, value_name="ttc_s", rows=rows,
        ))
        out.extend(self._pair_threshold(
            observer, target, times, ttc, EventType.CRITICAL_TTC,
            float(self.cfg.get(radar + "critical_ttc.ttc_s", 1.6)),
            above=False, value_name="ttc_s", rows=rows,
        ))

        max_range = float(self.cfg.get(radar + "lateral_crossing.max_range_m", 45.0))
        gated = [
            rate if rng <= max_range else 0.0
            for rate, rng in zip(lateral_rate, ranges)
        ]
        out.extend(self._pair_threshold(
            observer, target, times, gated, EventType.LATERAL_CROSSING,
            float(self.cfg.get(radar + "lateral_crossing.min_lateral_rate_mps", 1.8)),
            above=True, value_name="lateral_rate_mps", rows=rows,
        ))
        out.extend(self._cut_in_like(observer, target, rows))
        return out

    def _pair_threshold(
        self,
        observer: str,
        target: str,
        times: Sequence[float],
        values: Sequence[Optional[float]],
        event_type: EventType,
        enter: float,
        above: bool,
        value_name: str,
        rows: Sequence[Mapping[str, Any]],
        min_duration: Optional[float] = None,
    ) -> List[Event]:
        release = enter * (self.hysteresis if above else (2.0 - self.hysteresis))
        found = _episodes(
            times, values, enter, release,
            self.min_duration if min_duration is None else min_duration,
            above,
        )
        by_time = {round(float(r["t"]), 6): r for r in rows}
        out: List[Event] = []
        for ep in found:
            row = by_time.get(round(ep.t_peak, 6), {})
            out.append(self._event(
                event_type, observer, ep.t_start, ep.t_peak, ep.t_end,
                {
                    value_name: ep.peak_value,
                    "range_m": row.get("range_m"),
                    "bearing_deg": row.get("bearing_deg"),
                },
                subject=target,
                detail={"enter": enter, "release": release,
                        "n_samples": ep.n_samples},
            ))
        return out

    def _cut_in_like(
        self, observer: str, target: str, rows: Sequence[Mapping[str, Any]]
    ) -> List[Event]:
        """A target moving toward the observer's path while ahead of it."""
        radar = "events.radar.cut_in_like."
        closing_rate = float(self.cfg.get(radar + "lateral_closing_mps", 1.2))
        max_offset = float(self.cfg.get(radar + "max_lateral_offset_m", 4.5))
        min_longitudinal = float(self.cfg.get(radar + "min_longitudinal_m", 4.0))
        window_s = float(self.cfg.get(radar + "window_s", 2.5))

        out: List[Event] = []
        last_end = -1e9
        for index, row in enumerate(rows):
            t0 = float(row["t"])
            if t0 < last_end:
                continue
            if float(row["longitudinal_m"]) < min_longitudinal:
                continue
            lateral0 = abs(float(row["lateral_m"]))
            for other in rows[index + 1:]:
                t1 = float(other["t"])
                if t1 - t0 > window_s:
                    break
                lateral1 = abs(float(other["lateral_m"]))
                dt = t1 - t0
                if dt <= 0:
                    continue
                rate = (lateral0 - lateral1) / dt
                if rate >= closing_rate and lateral1 <= max_offset:
                    out.append(self._event(
                        EventType.CUT_IN_LIKE_MOTION, observer, t0, t1, t1,
                        {
                            "lateral_closing_mps": rate,
                            "lateral_offset_m": lateral1,
                            "longitudinal_m": float(other["longitudinal_m"]),
                        },
                        subject=target,
                        detail={"window_s": window_s},
                    ))
                    last_end = t1
                    break
        return out

    # -- conflict ---------------------------------------------------------

    def conflict_events(self) -> List[Event]:
        """Where two paths cross, and whether both vehicles were there at once.

        A vehicle infers this from trajectories without a map. The oracle knows
        the exact paths, so its version of the same claim is exact -- but it is
        still the same claim, stated in the same vocabulary. Map data (lane,
        road, junction) goes into the event's ``detail`` as context a reader can
        use, never into its type, because a type the reconstruction cannot emit
        puts the reference back outside the shared vocabulary.
        """
        radius = float(self.cfg.get("indicators.conflict.region_radius_m", 6.0))
        max_gap = float(self.cfg.get("indicators.conflict.max_arrival_gap_s", 3.0))
        min_conf = float(self.cfg.get("events.radar.path_conflict.min_confidence", 0.35))
        events: List[Event] = []

        for i, a in enumerate(self.participants):
            for b in self.participants[i + 1:]:
                crossing = self._path_crossing(a, b, radius)
                if crossing is None:
                    continue
                point, t_a, t_b = crossing
                gap = abs(t_a - t_b)
                if gap > max_gap:
                    continue
                # Both directions: the claim "our paths cross" is symmetric, and
                # each vehicle would make it about the other.
                for observer, other, t_self, t_other in (
                    (a, b, t_a, t_b), (b, a, t_b, t_a)
                ):
                    confidence = max(0.0, 1.0 - gap / max_gap)
                    if confidence < min_conf:
                        continue
                    t0 = min(t_self, t_other)
                    events.append(self._event(
                        EventType.PREDICTED_PATH_CONFLICT, observer,
                        max(0.0, t0 - max_gap), t0, max(t_self, t_other),
                        {
                            "arrival_gap_s": gap,
                            "conflict_x": point[0],
                            "conflict_y": point[1],
                        },
                        subject=other,
                        detail=self._map_context(observer, t_self),
                    ))
                    events.append(self._event(
                        EventType.CONFLICT_REGION_ENTRY, observer,
                        t_self, t_self, t_self,
                        {
                            "arrival_gap_s": gap,
                            "region_radius_m": radius,
                            "conflict_x": point[0],
                            "conflict_y": point[1],
                        },
                        subject=other,
                        detail=self._map_context(observer, t_self),
                    ))
        return events

    def _path_crossing(
        self, a: str, b: str, radius: float
    ) -> Optional[Tuple[Tuple[float, float], float, float]]:
        """Where the two exact paths come within ``radius``, and when each arrived."""
        a_rows, b_rows = self._rows[a], self._rows[b]
        if not a_rows or not b_rows:
            return None
        best: Optional[Tuple[float, Tuple[float, float], float, float]] = None
        for ra in a_rows:
            for rb in b_rows:
                distance = math.hypot(
                    float(rb["x"]) - float(ra["x"]), float(rb["y"]) - float(ra["y"])
                )
                if distance > radius:
                    continue
                gap = abs(float(ra["t"]) - float(rb["t"]))
                point = (
                    (float(ra["x"]) + float(rb["x"])) / 2.0,
                    (float(ra["y"]) + float(rb["y"])) / 2.0,
                )
                if best is None or gap < best[0]:
                    best = (gap, point, float(ra["t"]), float(rb["t"]))
        if best is None:
            return None
        return best[1], best[2], best[3]

    def _map_context(self, pid: str, t: float) -> Dict[str, Any]:
        """Privileged map context, carried as detail rather than as a type."""
        row = _nearest_row(self._rows[pid], t)
        if row is None:
            return {}
        return {
            "map_context": {
                "road_id": row.get("road_id"),
                "lane_id": row.get("lane_id"),
                "section_id": row.get("section_id"),
                "junction_id": row.get("junction_id"),
                "is_junction": row.get("is_junction"),
            },
            "note": (
                "map context is privileged detail, not part of the comparable "
                "claim; the event type is one a reconstruction can also emit"
            ),
        }

    # -- outcomes ---------------------------------------------------------

    def outcome_events(self) -> List[Event]:
        """Collisions, near misses and what the vehicles did afterwards."""
        events: List[Event] = []
        seen: set = set()
        first_impact: Dict[str, float] = {}
        for record in self.trace.get("collision_pairs", []) or []:
            a, b = str(record["a"]), str(record["b"])
            t = float(record["t"])
            key = (tuple(sorted((a, b))), round(t, 3))
            if key in seen:
                continue
            seen.add(key)
            state = _nearest_row(self._rows.get(a, []), t)
            other = _nearest_row(self._rows.get(b, []), t)
            speed_a = float(state["speed"]) if state else None
            speed_b = float(other["speed"]) if other else None
            relative = None
            if state and other:
                relative = math.hypot(
                    float(state["vx"]) - float(other["vx"]),
                    float(state["vy"]) - float(other["vy"]),
                )
            # One node per collision, attributed to the pair. Both orderings
            # would be two nodes for one physical event.
            events.append(self._event(
                EventType.COLLISION, a, t, t, t,
                {
                    "impact_speed_mps": speed_a,
                    "other_speed_mps": speed_b,
                    "relative_impact_speed_mps": relative,
                },
                subject=b,
                evidence_kind="privileged_collision_record",
                detail={"source": "oracle collision sensor"},
            ))
            # A vehicle in a chain collision is struck twice but comes to rest
            # once. The stop is recorded against the *first* impact that led to
            # it, so the graph has one node for one physical event; attributing
            # it to each impact separately would double-count a vehicle stopping.
            for pid in (a, b):
                first_impact.setdefault(pid, t)
                first_impact[pid] = min(first_impact[pid], t)

        for pid, t_first in sorted(first_impact.items()):
            events.extend(self._post_impact_stop(pid, t_first))

        events.extend(self._near_misses(bool(seen)))
        return events

    def _post_impact_stop(self, pid: str, t_collision: float) -> List[Event]:
        speed_mps = float(self.cfg.get("events.outcome.post_impact_stop.speed_mps", 0.6))
        within_s = float(self.cfg.get("events.outcome.post_impact_stop.within_s", 4.0))
        for row in self._rows.get(pid, []):
            t = float(row["t"])
            if t < t_collision or t > t_collision + within_s:
                continue
            if float(row["speed"]) <= speed_mps:
                return [self._event(
                    EventType.POST_IMPACT_STOP, pid, t_collision, t, t,
                    {"speed_mps": float(row["speed"]),
                     "delay_s": t - t_collision},
                    detail={"threshold_mps": speed_mps, "within_s": within_s},
                )]
        return []

    def _near_misses(self, had_collision: bool) -> List[Event]:
        """A close approach that did not become contact.

        Suppressed for a pair that did collide: the collision is the outcome,
        and a near miss moments before it is the same encounter described twice.
        """
        min_separation = float(self.cfg.get(
            "oracle.near_miss.min_separation_m",
            self.cfg.get("recorder.triggers.near_miss.min_range_m", 12.0),
        ))
        critical_ttc = float(self.cfg.get("events.radar.critical_ttc.ttc_s", 1.6))
        collided = {
            tuple(sorted((str(r["a"]), str(r["b"]))))
            for r in (self.trace.get("collision_pairs", []) or [])
        }
        out: List[Event] = []
        for i, a in enumerate(self.participants):
            for b in self.participants[i + 1:]:
                if tuple(sorted((a, b))) in collided:
                    continue
                rows = pairwise_truth(self.trace, a, b)
                if not rows:
                    continue
                closest = min(rows, key=lambda r: float(r["range_m"]))
                if float(closest["range_m"]) > min_separation:
                    continue
                ttc_values = [
                    float(r["ttc_s"]) for r in rows if r["ttc_s"] is not None
                ]
                if not ttc_values or min(ttc_values) > critical_ttc:
                    continue
                t = float(closest["t"])
                out.append(self._event(
                    EventType.NEAR_MISS, a, t, t, t,
                    {"min_range_m": float(closest["range_m"]),
                     "min_ttc_s": min(ttc_values)},
                    subject=b,
                    detail={"separation_threshold_m": min_separation},
                ))
        return out


def _wrap_deg(value: float) -> float:
    """Wrap an angle difference into ``[-180, 180]``."""
    return (float(value) + 180.0) % 360.0 - 180.0


def _nearest_row(
    rows: Sequence[Mapping[str, Any]], t: float
) -> Optional[Mapping[str, Any]]:
    if not rows:
        return None
    return min(rows, key=lambda r: abs(float(r["t"]) - float(t)))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def build_observable_events(
    trace: Mapping[str, Any], cfg: Config, spec: Any = None
) -> List[Event]:
    """Every observable ground-truth event of one run.

    ``spec`` is accepted and used **only** to check that the participants the
    scenario declared are the ones the trace recorded. Nothing about the
    scenario's intent -- its actions, its causal template, its expected
    outcome -- reaches the events, which is the whole point of this module
    existing separately from :func:`cdf.oracle.events.build_oracle_events`.
    """
    participants = [str(p) for p in trace.get("participants", []) or []]
    if not participants:
        raise ValueError("oracle trace lists no participants; nothing to measure")
    if spec is not None:
        missing = [
            p for p in getattr(spec, "participant_ids", []) if p not in participants
        ]
        if missing:
            raise ValueError(
                "scenario {0} declares participant(s) {1} the privileged trace "
                "never recorded (recorded: {2})".format(
                    getattr(spec, "scenario_id", "?"), missing, participants
                )
            )

    extractor = ObservableExtractor(trace, cfg)
    events: List[Event] = []
    events.extend(extractor.own_motion_events())
    events.extend(extractor.pairwise_events())
    events.extend(extractor.conflict_events())
    events.extend(extractor.outcome_events())

    events.sort(key=lambda e: (
        float(e.t_peak), float(e.t_start), e.event_type.value,
        str(e.participant_id), str(e.subject or ""), str(e.event_id),
    ))

    seen: Dict[str, int] = {}
    for event in events:
        seen[event.event_id] = seen.get(event.event_id, 0) + 1
    duplicates = sorted(k for k, n in seen.items() if n > 1)
    if duplicates:
        raise ValueError(
            "observable extraction produced {0} duplicated event id(s): "
            "{1}".format(len(duplicates), duplicates[:5])
        )
    return events
