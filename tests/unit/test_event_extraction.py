"""Unit tests for :mod:`cdf.local.event_extractor`.

The traces here are analytically specified (a ramped brake application, a signal
that chatters exactly across its threshold, a two-stage radar approach) so that
the expected event *count*, ordering and timing are known in advance. Counting
matters as much as detecting: an extractor without hysteresis and debouncing
produces dozens of duplicates from the same manoeuvre, and several tests below
fail loudly if either mechanism is removed.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, List, Optional, Sequence

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import ParticipantEvidence
from cdf.common.schemas import (
    ControlSample,
    Event,
    EventType,
    LocalTriggerRecord,
    ORACLE_ONLY_EVENT_TYPES,
    Provenance,
    TelemetrySample,
    TrackSample,
    TriggerKind,
)
from cdf.local.event_extractor import EventExtractor

DT = 0.05
PID = "A"


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def cfg() -> Config:
    """The real pipeline configuration; every threshold asserted on comes from it."""
    return load_run_config()


def grid(n: int, dt: float = DT) -> List[float]:
    """``n`` evenly spaced timestamps, rounded so equality tests stay exact."""
    return [round(k * dt, 6) for k in range(n)]


def make_telemetry(
    times: Sequence[float],
    xs: Sequence[float],
    ys: Sequence[float],
    yaws: Sequence[float],
    speeds: Optional[Sequence[float]] = None,
    accel_long: Optional[Sequence[float]] = None,
) -> List[TelemetrySample]:
    return [
        TelemetrySample(
            t=float(t),
            frame=i,
            participant_id=PID,
            x=float(xs[i]),
            y=float(ys[i]),
            z=0.0,
            yaw=float(yaws[i]),
            speed=0.0 if speeds is None else float(speeds[i]),
            accel_long=0.0 if accel_long is None else float(accel_long[i]),
        )
        for i, t in enumerate(times)
    ]


def make_controls(
    times: Sequence[float],
    throttle: Sequence[float],
    brake: Sequence[float],
    steer: Sequence[float],
) -> List[ControlSample]:
    return [
        ControlSample(
            t=float(t),
            frame=i,
            participant_id=PID,
            throttle=float(throttle[i]),
            brake=float(brake[i]),
            steer=float(steer[i]),
        )
        for i, t in enumerate(times)
    ]


def make_track(
    track_id: str,
    times: Sequence[float],
    rel_x: Sequence[float],
    rel_y: Sequence[float],
    range_rate: Sequence[float],
    gx: Optional[Sequence[float]] = None,
    gy: Optional[Sequence[float]] = None,
    gvx: Optional[Sequence[float]] = None,
    gvy: Optional[Sequence[float]] = None,
    frame_offset: int = 0,
) -> List[TrackSample]:
    return [
        TrackSample(
            t=float(t),
            frame=frame_offset + i,
            participant_id=PID,
            track_id=track_id,
            rel_x=float(rel_x[i]),
            rel_y=float(rel_y[i]),
            gx=0.0 if gx is None else float(gx[i]),
            gy=0.0 if gy is None else float(gy[i]),
            gvx=0.0 if gvx is None else float(gvx[i]),
            gvy=0.0 if gvy is None else float(gvy[i]),
            range_m=math.hypot(float(rel_x[i]), float(rel_y[i])),
            azimuth_rad=math.atan2(float(rel_y[i]), float(rel_x[i])),
            range_rate=float(range_rate[i]),
            n_points=6,
            confidence=0.8,
            age=i,
        )
        for i, t in enumerate(times)
    ]


def integrate_x(times: Sequence[float], speeds: Sequence[float]) -> List[float]:
    xs, x = [], 0.0
    for i in range(len(times)):
        xs.append(x)
        x += float(speeds[i]) * DT
    return xs


def by_type(events: Sequence[Event]) -> Dict[EventType, List[Event]]:
    out: Dict[EventType, List[Event]] = {}
    for e in events:
        out.setdefault(e.event_type, []).append(e)
    return out


# ---------------------------------------------------------------------------
# Scenario fixtures
# ---------------------------------------------------------------------------


def braking_evidence() -> ParticipantEvidence:
    """Cruise at 15 m/s, then one ramped brake application down to standstill."""
    times = grid(81)  # 0 .. 4.0 s
    speeds, accels, brake, throttle = [], [], [], []
    for t in times:
        if t < 1.0:
            speeds.append(15.0)
            accels.append(0.0)
            brake.append(0.0)
            throttle.append(0.5)
        elif t < 3.5:
            speeds.append(max(0.0, 15.0 - 6.0 * (t - 1.0)))
            accels.append(-6.0)
            brake.append(min(0.9, 0.2 + 1.4 * (t - 1.0)))
            throttle.append(0.0)
        else:
            speeds.append(0.0)
            accels.append(0.0)
            brake.append(0.0)
            throttle.append(0.0)
    n = len(times)
    return ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, speeds), [0.0] * n, [0.0] * n, speeds, accels
        ),
        controls=make_controls(times, throttle, brake, [0.0] * n),
    )


def approaching_track_evidence(
    triggers: Optional[List[LocalTriggerRecord]] = None,
) -> ParticipantEvidence:
    """A stationary observer watching a two-stage approach.

    Stage 1 closes at 8 m/s down to 20 m (TTC bottoms out at 2.55 s -- low but not
    critical), stage 2 holds station, stage 3 closes at 12 m/s down to 3.2 m
    (critical TTC). The staging is what makes the three event peaks distinct:
    with a single monotone approach every TTC threshold would share one argmin.
    """
    own_times = grid(141)  # 0 .. 7.0 s
    n_own = len(own_times)
    track_times = grid(109)  # 0 .. 5.4 s

    def rng_at(t: float) -> float:
        if t <= 2.5:
            return 40.0 - 8.0 * t
        if t <= 4.0:
            return 20.0
        return 20.0 - 12.0 * (t - 4.0)

    def rate_at(t: float) -> float:
        if t < 2.5:
            return -8.0
        if t < 4.0:
            return 0.0
        return -12.0

    ranges = [rng_at(t) for t in track_times]
    rates = [rate_at(t) for t in track_times]
    n_trk = len(track_times)

    return ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            own_times, [0.0] * n_own, [0.0] * n_own, [0.0] * n_own
        ),
        tracks=make_track(
            "A::T001",
            track_times,
            rel_x=ranges,
            rel_y=[0.0] * n_trk,
            range_rate=rates,
            gx=ranges,
            gy=[0.0] * n_trk,
            gvx=rates,
            gvy=[0.0] * n_trk,
        ),
        triggers=list(triggers or []),
    )


# ---------------------------------------------------------------------------
# Own-behaviour events: hysteresis and debouncing
# ---------------------------------------------------------------------------


def test_single_braking_manoeuvre_yields_exactly_one_event_per_type(cfg: Config) -> None:
    """One ramped brake application is one BRAKE_ONSET and one HARD_BRAKE."""
    events = EventExtractor(cfg).extract(braking_evidence())
    grouped = by_type(events)

    assert len(grouped[EventType.BRAKE_ONSET]) == 1
    assert len(grouped[EventType.HARD_BRAKE]) == 1
    assert len(grouped[EventType.DECELERATION]) == 1
    assert len(grouped[EventType.HARD_DECELERATION]) == 1

    onset = grouped[EventType.BRAKE_ONSET][0]
    hard = grouped[EventType.HARD_BRAKE][0]

    # The onset opens the instant the command passes 0.12 and peaks on the plateau.
    assert onset.t_start == pytest.approx(1.0, abs=1e-6)
    assert onset.t_start < onset.t_peak
    assert 1.45 <= onset.t_peak <= 1.6
    assert onset.t_end is not None and onset.t_end > onset.t_peak
    assert onset.values["brake_cmd"] == pytest.approx(0.9, abs=1e-6)

    # The hard-brake threshold (0.65) is crossed later on the same ramp.
    assert 1.30 < hard.t_start < 1.40
    assert onset.t_start < hard.t_start <= hard.t_peak
    assert hard.subject is None
    assert hard.provenance is Provenance.LOCAL
    assert hard.source_sensors == ["controls"]


def test_hysteresis_collapses_a_signal_chattering_across_the_threshold(
    cfg: Config,
) -> None:
    """A brake command oscillating either side of 0.12 is ONE event, not twenty."""
    times = grid(81)  # 0 .. 4.0 s
    brake = []
    for k, t in enumerate(times):
        if 1.0 <= t < 3.0:
            brake.append(0.14 if k % 2 == 0 else 0.10)
        else:
            brake.append(0.0)
    n = len(times)

    enter = float(cfg.require("events.brake_onset.brake_cmd"))
    # The trace really does cross the enter threshold on every other sample: a
    # memoryless detector would emit one event per crossing.
    crossings = sum(
        1
        for k in range(1, n)
        if brake[k] >= enter > brake[k - 1]
    )
    assert crossings == 20

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, [10.0 * t for t in times], [0.0] * n, [0.0] * n, speeds=[10.0] * n
        ),
        controls=make_controls(times, [0.0] * n, brake, [0.0] * n),
    )

    onsets = by_type(EventExtractor(cfg).extract(ev))[EventType.BRAKE_ONSET]
    assert len(onsets) == 1
    assert onsets[0].t_start == pytest.approx(1.0, abs=1e-6)
    assert onsets[0].t_end == pytest.approx(2.95, abs=1e-6)


def test_debounce_merges_episodes_split_by_single_sample_dropouts(cfg: Config) -> None:
    """A held brake punctuated by dropouts is one manoeuvre, not eight."""
    times = grid(61)  # 0 .. 3.0 s
    brake = [0.0 if (k % 8 == 0 and k > 0) else 0.5 for k in range(len(times))]
    n = len(times)

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, [10.0 * t for t in times], [0.0] * n, [0.0] * n, speeds=[10.0] * n
        ),
        controls=make_controls(times, [0.0] * n, brake, [0.0] * n),
    )

    onsets = by_type(EventExtractor(cfg).extract(ev))[EventType.BRAKE_ONSET]
    assert len(onsets) == 1
    assert onsets[0].t_start == pytest.approx(0.0, abs=1e-6)
    assert onsets[0].t_end == pytest.approx(3.0, abs=1e-6)


def test_vehicle_started_fires_once_at_the_first_departure(cfg: Config) -> None:
    """Pulling away is reported once, at the moment the speed threshold is passed."""
    times = grid(121)  # 0 .. 6.0 s
    speeds = [0.0 if t < 1.0 else min(10.0, 4.0 * (t - 1.0)) for t in times]
    n = len(times)
    thr = float(cfg.require("events.vehicle_started.speed_mps"))

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, speeds), [0.0] * n, [0.0] * n, speeds=speeds
        ),
        controls=make_controls(
            times, [0.0 if t < 1.0 else 0.6 for t in times], [0.0] * n, [0.0] * n
        ),
    )

    started = by_type(EventExtractor(cfg).extract(ev))[EventType.VEHICLE_STARTED]
    assert len(started) == 1
    assert started[0].values["speed_mps"] >= thr
    # 4 m/s^2 from rest crosses 0.8 m/s a fifth of a second after release.
    assert started[0].t_peak == pytest.approx(1.2, abs=0.06)


# ---------------------------------------------------------------------------
# Lane change versus turn
# ---------------------------------------------------------------------------


def _manoeuvre_evidence(
    yaw_of: Callable[[float], float],
    steer_of: Callable[[float], float],
    n: int = 161,
) -> ParticipantEvidence:
    """Drive at 10 m/s along a heading profile, integrating the resulting path."""
    times = grid(n)
    yaws = [float(yaw_of(t)) for t in times]
    steers = [float(steer_of(t)) for t in times]
    xs, ys, x, y = [], [], 0.0, 0.0
    for i in range(len(times)):
        xs.append(x)
        ys.append(y)
        x += 10.0 * math.cos(math.radians(yaws[i])) * DT
        y += 10.0 * math.sin(math.radians(yaws[i])) * DT
    return ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(times, xs, ys, yaws, speeds=[10.0] * len(times)),
        controls=make_controls(times, [0.4] * len(times), [0.0] * len(times), steers),
    )


def test_lane_change_like_manoeuvre_is_inferred_from_offset_and_steering(
    cfg: Config,
) -> None:
    """A sideways step with an out-and-back heading excursion reads as a lane change."""
    amp = 15.75  # deg; integrates to a ~3.5 m lateral step over two seconds

    def yaw_of(t: float) -> float:
        return amp * math.sin(math.pi * (t - 2.0) / 2.0) if 2.0 <= t <= 4.0 else 0.0

    def steer_of(t: float) -> float:
        return 0.3 * math.sin(math.pi * (t - 2.0) / 2.0) if 2.0 <= t <= 4.0 else 0.0

    grouped = by_type(EventExtractor(cfg).extract(_manoeuvre_evidence(yaw_of, steer_of)))
    lane = grouped.get(EventType.LANE_CHANGE_LIKE_MANEUVER, [])

    assert len(lane) == 1
    event = lane[0]
    lat_thr = float(cfg.require("events.lane_change_like.lateral_offset_m"))
    max_turn = float(cfg.require("events.lane_change_like.max_heading_change_deg"))
    assert abs(event.values["lateral_offset_m"]) >= lat_thr
    assert event.values["lateral_offset_m"] > 0.0  # drifted to the right
    assert event.values["heading_change_deg"] <= max_turn
    # The heading came back to where it started: that is what makes it a lane
    # change rather than a change of direction.
    assert event.values["net_heading_change_deg"] <= 0.5 * event.values["heading_change_deg"]
    assert 2.0 <= event.t_start <= 5.0


def test_a_turn_never_reports_a_lane_change_like_manoeuvre(cfg: Config) -> None:
    """A 90 deg turn produces a large offset but must not be called a lane change."""

    def yaw_of(t: float) -> float:
        if t < 2.0:
            return 0.0
        if t <= 5.0:
            return 30.0 * (t - 2.0)
        return 90.0

    def steer_of(t: float) -> float:
        return 0.5 if 2.0 <= t <= 5.0 else 0.0

    grouped = by_type(EventExtractor(cfg).extract(_manoeuvre_evidence(yaw_of, steer_of)))

    assert EventType.LANE_CHANGE_LIKE_MANEUVER not in grouped
    # The manoeuvre is still reported -- as what it is.
    assert len(grouped[EventType.SIGNIFICANT_HEADING_CHANGE]) >= 1
    assert grouped[EventType.SIGNIFICANT_HEADING_CHANGE][0].values["heading_change_deg"] >= float(
        cfg.require("events.heading_change.total_deg")
    )
    assert len(grouped[EventType.STEER_ONSET]) == 1


# ---------------------------------------------------------------------------
# Radar / interaction events
# ---------------------------------------------------------------------------


def test_approaching_track_escalates_from_closing_to_critical(cfg: Config) -> None:
    """RANGE_DECREASING, then LOW_TTC, then CRITICAL_TTC, with increasing peaks."""
    events = EventExtractor(cfg).extract(approaching_track_evidence())
    grouped = by_type(events)

    for wanted in (
        EventType.RANGE_DECREASING,
        EventType.RAPID_CLOSING,
        EventType.LOW_TTC,
        EventType.CRITICAL_TTC,
    ):
        assert wanted in grouped, "missing {0}".format(wanted.value)

    t_closing = min(e.t_peak for e in grouped[EventType.RANGE_DECREASING])
    t_low = min(e.t_peak for e in grouped[EventType.LOW_TTC])
    t_critical = min(e.t_peak for e in grouped[EventType.CRITICAL_TTC])
    assert t_closing < t_low < t_critical

    low_ttc = float(cfg.require("events.radar.low_ttc.ttc_s"))
    critical_ttc = float(cfg.require("events.radar.critical_ttc.ttc_s"))
    assert grouped[EventType.LOW_TTC][0].values["ttc_s"] <= low_ttc
    assert grouped[EventType.CRITICAL_TTC][0].values["ttc_s"] <= critical_ttc

    # Interaction events name the local track they concern, never an actor.
    for event_type in (EventType.LOW_TTC, EventType.CRITICAL_TTC, EventType.RANGE_DECREASING):
        for e in grouped[event_type]:
            assert e.subject == "A::T001"
            assert e.source_sensors == ["radar"]
            assert [ref.ref for ref in e.evidence] == ["A::T001"]
            assert 0.0 < e.confidence <= 1.0


def test_track_lifecycle_reports_appearance_then_loss(cfg: Config) -> None:
    """A track that ends mid-recording is lost; one running to the end is not."""
    own_times = grid(121)  # 0 .. 6.0 s
    n_own = len(own_times)
    lost_times = grid(41)  # 0 .. 2.0 s, shifted below to 1.0 .. 3.0 s
    lost_times = [round(t + 1.0, 6) for t in lost_times]
    kept_times = [round(4.0 + k * DT, 6) for k in range(41)]  # 4.0 .. 6.0 s

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            own_times, [0.0] * n_own, [0.0] * n_own, [0.0] * n_own
        ),
        tracks=(
            make_track(
                "A::T001",
                lost_times,
                rel_x=[25.0] * len(lost_times),
                rel_y=[3.0] * len(lost_times),
                range_rate=[0.0] * len(lost_times),
            )
            + make_track(
                "A::T002",
                kept_times,
                rel_x=[30.0] * len(kept_times),
                rel_y=[-2.0] * len(kept_times),
                range_rate=[0.0] * len(kept_times),
            )
        ),
    )

    grouped = by_type(EventExtractor(cfg).extract(ev))
    appeared = grouped[EventType.RADAR_TRACK_APPEARED]
    lost = grouped[EventType.RADAR_TRACK_LOST]

    assert sorted(e.subject for e in appeared) == ["A::T001", "A::T002"]
    assert [e.subject for e in lost] == ["A::T001"]

    first = [e for e in appeared if e.subject == "A::T001"][0]
    assert first.t_peak == pytest.approx(1.0, abs=1e-6)
    assert lost[0].t_peak == pytest.approx(3.0, abs=1e-6)
    assert first.t_peak < lost[0].t_peak
    assert lost[0].values["track_duration_s"] == pytest.approx(2.0, abs=1e-6)


def test_lateral_crossing_is_reported_for_a_target_sweeping_across(cfg: Config) -> None:
    """A target traversing left to right in front of us crosses the lateral gate."""
    times = grid(81)  # 0 .. 4.0 s
    rel_y = [-20.0 + 8.0 * t for t in times]  # 8 m/s lateral sweep
    n = len(times)

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(times, [0.0] * n, [0.0] * n, [0.0] * n),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=[20.0] * n,
            rel_y=rel_y,
            range_rate=[0.0] * n,
        ),
    )

    grouped = by_type(EventExtractor(cfg).extract(ev))
    crossing = grouped[EventType.LATERAL_CROSSING]
    assert len(crossing) == 1
    assert crossing[0].values["lateral_rate_mps"] == pytest.approx(8.0, abs=1e-6)
    assert crossing[0].values["range_m"] <= float(
        cfg.require("events.radar.lateral_crossing.max_range_m")
    )


def test_predicted_path_conflict_is_reported_for_crossing_trajectories(
    cfg: Config,
) -> None:
    """Two straight paths meeting simultaneously yield a conflict and a region entry."""
    times = grid(61)  # 0 .. 3.0 s
    n = len(times)
    own_x = [-25.0 + 10.0 * t for t in times]
    tgt_y = [-25.0 + 10.0 * t for t in times]

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, own_x, [0.0] * n, [0.0] * n, speeds=[10.0] * n
        ),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=[0.0 - own_x[i] for i in range(n)],
            rel_y=[tgt_y[i] for i in range(n)],
            range_rate=[-10.0] * n,
            gx=[0.0] * n,
            gy=tgt_y,
            gvx=[0.0] * n,
            gvy=[10.0] * n,
        ),
    )

    grouped = by_type(EventExtractor(cfg).extract(ev))
    conflicts = grouped[EventType.PREDICTED_PATH_CONFLICT]
    assert len(conflicts) == 1
    assert conflicts[0].confidence >= float(
        cfg.require("events.radar.path_conflict.min_confidence")
    )
    assert conflicts[0].values["conflict_x"] == pytest.approx(0.0, abs=0.5)
    assert conflicts[0].values["conflict_y"] == pytest.approx(0.0, abs=0.5)

    entries = grouped[EventType.CONFLICT_REGION_ENTRY]
    assert len(entries) == 1
    radius = float(cfg.require("indicators.conflict.region_radius_m"))
    assert entries[0].values["distance_to_conflict_m"] <= radius
    # We reach the inferred region only after having predicted it.
    assert conflicts[0].t_start <= entries[0].t_start


# ---------------------------------------------------------------------------
# Outcome events
# ---------------------------------------------------------------------------


def test_collision_trigger_yields_exactly_one_collision_event(cfg: Config) -> None:
    """One onboard impact trigger becomes one COLLISION event at the trigger time."""
    times = grid(121)  # 0 .. 6.0 s
    speeds = []
    for t in times:
        if t < 3.0:
            speeds.append(10.0)
        elif t < 3.5:
            speeds.append(max(0.0, 10.0 - 20.0 * (t - 3.0)))
        else:
            speeds.append(0.0)
    n = len(times)

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, speeds), [0.0] * n, [0.0] * n, speeds=speeds
        ),
        controls=make_controls(times, [0.0] * n, [0.0] * n, [0.0] * n),
        triggers=[
            LocalTriggerRecord(
                t=3.0,
                frame=60,
                participant_id=PID,
                kind=TriggerKind.COLLISION,
                collision_detected=True,
                impulse=800.0,
            )
        ],
    )

    grouped = by_type(EventExtractor(cfg).extract(ev))
    collisions = grouped[EventType.COLLISION]
    assert len(collisions) == 1
    assert collisions[0].t_peak == pytest.approx(3.0, abs=1e-9)
    assert collisions[0].t_start == pytest.approx(3.0, abs=1e-9)
    assert collisions[0].values["impulse"] == pytest.approx(800.0)
    assert collisions[0].source_sensors == ["collision"]
    # The onboard record cannot name the other party.
    assert collisions[0].subject is None

    stops = grouped[EventType.POST_IMPACT_STOP]
    assert len(stops) == 1
    assert stops[0].t_start == pytest.approx(3.0, abs=1e-9)
    assert 3.0 < stops[0].t_peak <= 3.0 + float(
        cfg.require("events.outcome.post_impact_stop.within_s")
    )
    assert stops[0].values["speed_mps"] <= float(
        cfg.require("events.outcome.post_impact_stop.speed_mps")
    )


def test_unresolved_critical_ttc_becomes_a_near_miss(cfg: Config) -> None:
    """A critical approach that ends without an impact is a near miss."""
    grouped = by_type(EventExtractor(cfg).extract(approaching_track_evidence()))

    near = grouped[EventType.NEAR_MISS]
    critical = grouped[EventType.CRITICAL_TTC]
    assert len(near) == 1
    assert near[0].subject == "A::T001"
    assert near[0].t_peak == pytest.approx(critical[0].t_peak, abs=1e-9)
    # The derived event cites the critical-TTC event it was inferred from.
    assert critical[0].event_id in [e.ref for e in near[0].evidence]


def test_critical_ttc_followed_by_an_impact_is_not_a_near_miss(cfg: Config) -> None:
    """The absence of a collision is what makes a near miss; supply one and it goes."""
    ev = approaching_track_evidence(
        triggers=[
            LocalTriggerRecord(
                t=5.4,
                frame=108,
                participant_id=PID,
                kind=TriggerKind.COLLISION,
                collision_detected=True,
                impulse=1200.0,
            )
        ]
    )
    grouped = by_type(EventExtractor(cfg).extract(ev))

    assert len(grouped[EventType.COLLISION]) == 1
    assert len(grouped[EventType.CRITICAL_TTC]) == 1
    assert EventType.NEAR_MISS not in grouped


def test_near_miss_trigger_is_reported_directly(cfg: Config) -> None:
    """A recorder near-miss trigger becomes a NEAR_MISS even with no radar track."""
    times = grid(61)
    n = len(times)
    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, [10.0 * t for t in times], [0.0] * n, [0.0] * n, speeds=[10.0] * n
        ),
        triggers=[
            LocalTriggerRecord(
                t=2.0,
                frame=40,
                participant_id=PID,
                kind=TriggerKind.NEAR_MISS,
                detail={"min_ttc": 0.7, "track_id": "A::T009"},
            )
        ],
    )

    near = by_type(EventExtractor(cfg).extract(ev))[EventType.NEAR_MISS]
    assert len(near) == 1
    assert near[0].t_peak == pytest.approx(2.0, abs=1e-9)
    assert near[0].subject == "A::T009"
    assert near[0].values["min_ttc"] == pytest.approx(0.7)


# ---------------------------------------------------------------------------
# Global invariants
# ---------------------------------------------------------------------------


def test_events_are_sorted_uniquely_identified_and_strictly_local(cfg: Config) -> None:
    """Whole-bundle invariants every consumer of the event stream relies on."""
    base = braking_evidence()
    approach = approaching_track_evidence()
    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=base.telemetry,
        controls=base.controls,
        tracks=approach.tracks,
        triggers=[
            LocalTriggerRecord(
                t=3.6,
                frame=72,
                participant_id=PID,
                kind=TriggerKind.COLLISION,
                collision_detected=True,
                impulse=450.0,
            )
        ],
    )

    events = EventExtractor(cfg).extract(ev)
    assert len(events) > 8

    peaks = [e.t_peak for e in events]
    assert peaks == sorted(peaks)

    ids = [e.event_id for e in events]
    assert len(set(ids)) == len(ids)

    for e in events:
        assert e.provenance is Provenance.LOCAL
        assert e.participant_id == PID
        assert e.owners == [PID]
        assert e.event_type not in ORACLE_ONLY_EVENT_TYPES
        assert e.t_start <= e.t_peak
        if e.t_end is not None:
            assert e.t_peak <= e.t_end + 1e-9
        assert 0.0 <= e.confidence <= 1.0
        assert e.subject is None or e.subject.startswith(PID + "::")
        assert e.evidence, "every event must point back at its supporting records"


def test_extraction_is_deterministic(cfg: Config) -> None:
    """Re-running the extractor on the same evidence reproduces identical events."""
    extractor = EventExtractor(cfg)
    first = extractor.extract(approaching_track_evidence())
    second = EventExtractor(cfg).extract(approaching_track_evidence())

    assert [e.event_id for e in first] == [e.event_id for e in second]
    assert [(e.t_start, e.t_peak, e.t_end) for e in first] == [
        (e.t_start, e.t_peak, e.t_end) for e in second
    ]


def test_empty_evidence_produces_no_events(cfg: Config) -> None:
    """A participant that recorded nothing yields nothing -- never an exception."""
    assert EventExtractor(cfg).extract(ParticipantEvidence(participant_id=PID)) == []


def test_invalid_hysteresis_ratio_fails_loudly(cfg: Config) -> None:
    """A misconfigured hysteresis ratio is a configuration bug, not a silent default."""
    with pytest.raises(ValueError):
        EventExtractor(cfg.with_overrides({"events": {"hysteresis_ratio": 1.5}}))
    with pytest.raises(ValueError):
        EventExtractor(cfg.with_overrides({"events": {"hysteresis_ratio": 0.0}}))


# ---------------------------------------------------------------------------
# Adversarial regressions
# ---------------------------------------------------------------------------


def test_a_recording_that_opens_mid_drive_reports_no_departure(cfg: Config) -> None:
    """VEHICLE_STARTED claims a transition, so it needs the standstill on record.

    The recorder is a rolling buffer: a retained trace routinely opens with the
    vehicle already rolling. A speed episode that is already open on the very
    first sample is evidence that the *recording* started, not that the vehicle
    did. Asserting a departure there is a fabricated own-behaviour claim, and
    ``own_acceleration_closes_gap`` in the causal rule table would go on to blame
    that departure for every range the vehicle then closed.
    """
    times = grid(121)  # 0 .. 6.0 s
    n = len(times)
    cruising = [12.0] * n  # never below the 0.8 m/s threshold, not once

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, cruising), [0.0] * n, [0.0] * n, speeds=cruising
        ),
        controls=make_controls(times, [0.3] * n, [0.0] * n, [0.0] * n),
    )

    grouped = by_type(EventExtractor(cfg).extract(ev))
    assert EventType.VEHICLE_STARTED not in grouped

    # The guard must not cost us a genuine departure that the same trace *does*
    # witness: stopping and pulling away again is still reported.
    stop_go = [12.0 if t < 1.0 else (0.0 if t < 3.0 else min(12.0, 5.0 * (t - 3.0))) for t in times]
    ev_stop_go = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, stop_go), [0.0] * n, [0.0] * n, speeds=stop_go
        ),
        controls=make_controls(times, [0.3] * n, [0.0] * n, [0.0] * n),
    )
    started = by_type(EventExtractor(cfg).extract(ev_stop_go))[EventType.VEHICLE_STARTED]
    assert len(started) == 1
    # The departure is the one at 3 s, not the motion the trace opened with.
    assert started[0].t_peak == pytest.approx(3.2, abs=0.1)


def test_hysteresis_holds_for_negative_and_inverted_thresholds(cfg: Config) -> None:
    """The sign handling of the release threshold is exercised in both directions.

    ``events.hysteresis_ratio`` scales the enter threshold towards the non-event
    region, which for a negative floor (deceleration <= -1.8) means *less*
    negative and for a positive ceiling (TTC <= 3.0 s) means *larger*. Getting
    either sign wrong does not produce duplicates -- it produces an immediate
    close on every sample, one-sample episodes that the duration filter then
    discards, and the events vanish entirely. Both branches are asserted here
    because both are silent when broken.
    """
    times = grid(121)  # 0 .. 6.0 s
    n = len(times)

    # --- negative floor: a deceleration chattering either side of -1.8 m/s^2.
    decel_enter = float(cfg.require("events.deceleration.enter_mps2"))
    accels = []
    for k, t in enumerate(times):
        if 1.0 <= t < 4.0:
            accels.append(decel_enter - 0.1 if k % 2 == 0 else decel_enter + 0.1)
        else:
            accels.append(0.0)
    # The trace genuinely re-crosses the enter threshold on every other sample.
    assert sum(1 for k in range(1, n) if accels[k] <= decel_enter < accels[k - 1]) == 30

    speeds, v = [], 20.0
    for a in accels:
        speeds.append(max(0.0, v))
        v += a * DT
    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, integrate_x(times, speeds), [0.0] * n, [0.0] * n, speeds, accels
        ),
        controls=make_controls(times, [0.0] * n, [0.0] * n, [0.0] * n),
    )
    decels = by_type(EventExtractor(cfg).extract(ev))[EventType.DECELERATION]
    assert len(decels) == 1
    assert decels[0].t_start == pytest.approx(1.0, abs=1e-6)
    assert decels[0].t_end == pytest.approx(3.95, abs=1e-6)
    assert decels[0].values["accel_long_mps2"] == pytest.approx(decel_enter - 0.1, abs=1e-6)

    # --- positive ceiling: a TTC chattering either side of the 3.0 s gate, held
    #     at a fixed range so only the range rate moves.
    low_ttc = float(cfg.require("events.radar.low_ttc.ttc_s"))
    rng = 30.0
    rates = []
    for k, t in enumerate(times):
        ttc = (low_ttc - 0.1) if k % 2 == 0 else (low_ttc + 0.1)
        rates.append(-rng / (ttc if 1.0 <= t < 4.0 else 12.0))
    ev_track = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(times, [0.0] * n, [0.0] * n, [0.0] * n),
        tracks=make_track(
            "A::T001", times, rel_x=[rng] * n, rel_y=[0.0] * n, range_rate=rates
        ),
    )
    lows = by_type(EventExtractor(cfg).extract(ev_track))[EventType.LOW_TTC]
    assert len(lows) == 1
    assert lows[0].t_start == pytest.approx(1.0, abs=1e-6)
    assert lows[0].values["ttc_s"] == pytest.approx(low_ttc - 0.1, abs=1e-6)
