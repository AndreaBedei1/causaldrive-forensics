"""Unit tests for the finite-trace property monitor.

Every test builds a synthetic participant trace whose ground truth is known by
construction (a known TTC profile, a known braking onset, a known collision time)
and asserts the *numeric* consequences: the verdict, the violating interval in
seconds, and the witness values that decided it.

The epistemic tests matter most: a trace with no radar evidence must come back
``UNKNOWN`` and never ``PASS``, because "I saw nothing" is not "nothing happened".
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

import pytest

from cdf.checking.counterexamples import (
    COUNTEREXAMPLE_COLUMNS,
    build_counterexample_report,
    extract_counterexample,
)
from cdf.checking.properties import (
    LOCAL_PROPERTIES,
    O1_SIGNAL_COMPLIANCE,
    O2_RIGHT_OF_WAY,
    ORACLE_PROPERTIES,
    P1_BRAKE_RESPONSE,
    P2_NO_THROTTLE_CLOSING,
    P3_POST_COLLISION_STOP,
    P4_CONFLICT_NO_RESPONSE,
    PropertyResult,
    build_state_trace,
)
from cdf.checking.trace_checker import TraceChecker, summarise_results
from cdf.common.config import Config, configs_dir, load_yaml
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import (
    CheckStatus,
    ControlSample,
    Event,
    EventType,
    LocalTriggerRecord,
    Provenance,
    TelemetrySample,
    TrackSample,
    TriggerKind,
    make_event_id,
    make_track_id,
)

DT = 0.05
DURATION = 10.0


# ---------------------------------------------------------------------------
# Fixtures / builders
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def cfg() -> Config:
    """The real threshold registry -- tests assert against shipped defaults."""
    return Config(load_yaml(configs_dir() / "default.yaml"))


def _times(dt: float = DT, duration: float = DURATION) -> List[float]:
    return [i * dt for i in range(int(round(duration / dt)) + 1)]


def _const(value: float) -> Callable[[float], float]:
    return lambda t: float(value)


def _evidence(
    participant_id: str = "A",
    speed: Optional[Callable[[float], float]] = None,
    throttle: Optional[Callable[[float], float]] = None,
    brake: Optional[Callable[[float], float]] = None,
    steer: Optional[Callable[[float], float]] = None,
    tracks: Optional[Sequence[TrackSample]] = None,
    triggers: Optional[Sequence[LocalTriggerRecord]] = None,
    events: Optional[Sequence[Event]] = None,
    duration: float = DURATION,
    dt: float = DT,
    with_controls: bool = True,
) -> ParticipantEvidence:
    """A synthetic participant recording driven by explicit signal functions."""
    speed = speed or _const(10.0)
    throttle = throttle or _const(0.0)
    brake = brake or _const(0.0)
    steer = steer or _const(0.0)

    telemetry: List[TelemetrySample] = []
    controls: List[ControlSample] = []
    for i, t in enumerate(_times(dt, duration)):
        telemetry.append(
            TelemetrySample(
                t=t,
                frame=i,
                participant_id=participant_id,
                x=0.0,
                y=0.0,
                z=0.0,
                yaw=0.0,
                speed=float(speed(t)),
                vx=float(speed(t)),
            )
        )
        if with_controls:
            controls.append(
                ControlSample(
                    t=t,
                    frame=i,
                    participant_id=participant_id,
                    throttle=float(throttle(t)),
                    brake=float(brake(t)),
                    steer=float(steer(t)),
                )
            )
    return ParticipantEvidence(
        participant_id=participant_id,
        telemetry=telemetry,
        controls=controls,
        tracks=list(tracks or []),
        triggers=list(triggers or []),
        events=list(events or []),
    )


def _closing_track(
    participant_id: str,
    t_from: float,
    t_to: float,
    r0: float,
    range_rate: float,
    index: int = 1,
    min_range: float = 1.0,
    dt: float = DT,
    duration: float = DURATION,
) -> List[TrackSample]:
    """A track closing at a constant range rate (negative = closing).

    Range therefore falls linearly, which makes the resulting TTC profile exactly
    ``range / |range_rate|`` -- a closed form the tests assert against.
    """
    track_id = make_track_id(participant_id, index)
    out: List[TrackSample] = []
    for i, t in enumerate(_times(dt, duration)):
        if t < t_from - 1e-9 or t > t_to + 1e-9:
            continue
        rng = r0 + range_rate * (t - t_from)
        if rng < min_range:
            continue
        out.append(
            TrackSample(
                t=t,
                frame=i,
                participant_id=participant_id,
                track_id=track_id,
                rel_x=rng,
                rel_y=0.0,
                range_m=rng,
                range_rate=range_rate,
                rel_vx=range_rate,
                n_points=6,
                confidence=0.9,
                age=i,
            )
        )
    return out


def _event(
    participant_id: str, event_type: EventType, t: float, duration: float = 0.4
) -> Event:
    return Event(
        event_id=make_event_id("local", participant_id, event_type.value, t, "s"),
        event_type=event_type,
        participant_id=participant_id,
        t_start=t,
        t_peak=t,
        t_end=t + duration,
        subject=make_track_id(participant_id, 1),
        provenance=Provenance.LOCAL,
    )


def _collision_trigger(participant_id: str, t: float) -> LocalTriggerRecord:
    return LocalTriggerRecord(
        t=t,
        frame=int(round(t / DT)),
        participant_id=participant_id,
        kind=TriggerKind.COLLISION,
        collision_detected=True,
        impulse=820.0,
    )


def _run(participants: Dict[str, ParticipantEvidence]) -> RunEvidence:
    return RunEvidence(
        run_dir=Path("."),
        manifest={"run_id": "R_test", "scenario_id": "S01", "seed": 7},
        participants=dict(participants),
    )


# The closing track used by most tests: range 40 m falling at 10 m/s from t=0.
# TTC = range/10, so TTC crosses the shipped critical threshold of 1.6 s exactly
# when range reaches 16 m, i.e. at t = 2.4 s.
CRITICAL_ONSET = 2.4


def _approaching_tracks(participant_id: str = "A") -> List[TrackSample]:
    return _closing_track(participant_id, t_from=0.0, t_to=DURATION, r0=40.0, range_rate=-10.0)


# ---------------------------------------------------------------------------
# State trace
# ---------------------------------------------------------------------------


def test_state_trace_flattens_streams_and_derives_ttc(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    trace = build_state_trace(ev, cfg)

    assert len(trace) == len(_times())
    at_zero = trace[0]
    assert at_zero.speed == pytest.approx(10.0)
    assert at_zero.throttle == pytest.approx(0.4)
    assert at_zero.min_range == pytest.approx(40.0)
    # TTC = 40 / 10
    assert at_zero.min_ttc == pytest.approx(4.0, abs=1e-6)
    assert at_zero.closing_rate == pytest.approx(10.0)
    assert at_zero.active_track_ids == [make_track_id("A", 1)]

    # Track ends when the range would fall below 1 m, i.e. t = 3.9 s.
    tail = [s for s in trace if s.t > 4.0]
    assert tail and all(s.min_ttc is None and not s.active_track_ids for s in tail)


def test_state_trace_marks_missing_controls_as_none(cfg: Config) -> None:
    ev = _evidence(with_controls=False, tracks=_approaching_tracks())
    trace = build_state_trace(ev, cfg)
    assert all(s.throttle is None and s.brake is None for s in trace)
    assert all(s.speed is not None for s in trace)


# ---------------------------------------------------------------------------
# P1 -- brake response
# ---------------------------------------------------------------------------


def test_p1_pass_when_braking_promptly(cfg: Config) -> None:
    """Braking 0.2 s after the critical-TTC onset is well inside the 1.2 s window."""
    ev = _evidence(
        brake=lambda t: 0.8 if t >= CRITICAL_ONSET + 0.2 else 0.0,
        throttle=lambda t: 0.0 if t >= CRITICAL_ONSET + 0.2 else 0.3,
        tracks=_approaching_tracks(),
    )
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.violating_intervals == []
    assert res.counterexample_ref is None
    assert res.witness["n_episodes"] == 1
    assert res.witness["n_responded"] == 1
    assert res.witness["max_response_latency_s"] == pytest.approx(0.2, abs=DT + 1e-6)
    assert res.parameters["ttc_critical_s"] == pytest.approx(1.6)


def test_p1_fail_when_never_braking(cfg: Config) -> None:
    """No brake at all after a critical TTC -> FAIL over [onset, onset+window]."""
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert len(res.violating_intervals) == 1
    start, end = res.violating_intervals[0]
    assert start == pytest.approx(CRITICAL_ONSET, abs=DT)
    assert end == pytest.approx(CRITICAL_ONSET + 1.2, abs=DT)
    assert res.counterexample_ref is not None
    assert res.witness["n_violations"] == 1
    assert res.witness["min_ttc_observed"] == pytest.approx(0.1, abs=0.01)


def test_p1_unknown_without_any_track_evidence(cfg: Config) -> None:
    """The key epistemic test: no radar evidence is UNKNOWN, never PASS."""
    ev = _evidence(throttle=_const(0.4))  # telemetry + controls, no tracks, no events
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert res.status is not CheckStatus.PASS
    assert res.violating_intervals == []
    assert "no radar track" in res.reason
    assert res.witness["n_track_samples"] == 0
    assert res.parameters["ttc_critical_s"] == pytest.approx(1.6)


def test_p1_unknown_when_ttc_never_becomes_critical(cfg: Config) -> None:
    """Track evidence exists but the antecedent never holds -> vacuous, so UNKNOWN."""
    ev = _evidence(
        tracks=_closing_track("A", t_from=0.0, t_to=DURATION, r0=60.0, range_rate=-1.0)
    )
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert "vacuously" in res.reason
    assert res.witness["n_episodes"] == 0
    assert res.witness["min_ttc_observed"] > 1.6


def test_p1_unknown_when_trace_ends_inside_the_response_window(cfg: Config) -> None:
    """A truncated recording cannot refute the property."""
    short = 2.6  # critical onset at 2.4 s, deadline at 3.6 s -> off-record
    ev = _evidence(
        throttle=_const(0.4),
        duration=short,
        tracks=_closing_track(
            "A", t_from=0.0, t_to=short, r0=40.0, range_rate=-10.0, duration=short
        ),
    )
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert "ends before" in res.reason
    assert res.witness["n_undecidable"] == 1


def test_p1_unknown_when_an_evidence_gap_sits_inside_the_response_window(
    cfg: Config,
) -> None:
    """A control blackout across the deadline must not be read as "did not brake".

    The trace is otherwise identical to the FAIL case, so the only thing that
    can change the verdict is whether the monitor notices that it stopped seeing
    the control stream. A monitor that only asks "is there *any* brake sample in
    the window?" reports FAIL here -- it would be claiming to have witnessed the
    absence of a response across 1.1 s it never recorded.

    The mirror assertion matters just as much: a one-sample drop-out is well
    inside ``max_gap_s`` and must still decide, otherwise the property degrades
    into UNKNOWN on any imperfect recording and stops being informative.
    """

    def _with_control_blackout(t_from: float, t_to: float) -> ParticipantEvidence:
        ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
        ev.controls = [
            c for c in ev.controls if not (t_from - 1e-9 <= c.t <= t_to + 1e-9)
        ]
        return ev

    # Critical-TTC onset is 2.40 s and the response deadline 3.60 s. Blank the
    # controls across almost all of that window, leaving the endpoints.
    blacked_out = _with_control_blackout(2.45, 3.55)
    trace = build_state_trace(blacked_out, cfg)
    inside = [s for s in trace if 2.45 - 1e-9 <= s.t <= 3.55 + 1e-9]
    assert inside and all(s.brake is None for s in inside), (
        "the drop-out must survive the stream join as None, not be filled in "
        "from a neighbouring sample"
    )

    res = P1_BRAKE_RESPONSE.evaluate(blacked_out, cfg, {"participant_id": "A"})
    assert res.status is CheckStatus.UNKNOWN
    assert res.status is not CheckStatus.FAIL
    assert res.violating_intervals == []
    assert res.counterexample_ref is None
    assert "evidence gap" in res.reason
    assert res.witness["n_undecidable"] == 1
    assert res.witness["n_violations"] == 0
    gap = res.witness["undecidable_episodes"][0]["gap_s"]
    assert gap > res.parameters["max_gap_s"]
    # Only the deadline endpoints survive, so the unobserved stretch is the
    # whole 1.2 s response window.
    assert gap == pytest.approx(1.2, abs=2 * DT)

    # A single missing sample is not an evidence gap: the verdict still stands.
    one_sample = _with_control_blackout(3.0, 3.0)
    still_fails = P1_BRAKE_RESPONSE.evaluate(one_sample, cfg, {"participant_id": "A"})
    assert still_fails.status is CheckStatus.FAIL
    assert still_fails.violating_intervals[0][0] == pytest.approx(CRITICAL_ONSET, abs=DT)


# ---------------------------------------------------------------------------
# P2 -- no sustained throttle while closing
# ---------------------------------------------------------------------------


def test_p2_fail_when_throttle_held_through_a_closing_episode(cfg: Config) -> None:
    """Closing at 8 m/s with throttle 0.5 for 4 s breaks the 1 s grace period."""
    ev = _evidence(
        throttle=_const(0.5),
        tracks=_closing_track("A", t_from=2.0, t_to=6.0, r0=40.0, range_rate=-8.0),
    )
    res = P2_NO_THROTTLE_CLOSING.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert len(res.violating_intervals) == 1
    start, end = res.violating_intervals[0]
    assert start == pytest.approx(2.0, abs=DT)
    assert end == pytest.approx(6.0, abs=DT)
    assert res.witness["longest_throttle_while_closing_s"] == pytest.approx(4.0, abs=DT)
    assert res.witness["max_closing_rate_mps"] == pytest.approx(8.0)
    assert res.parameters["grace_s"] == pytest.approx(1.0)


def test_p2_pass_when_throttle_stays_below_threshold(cfg: Config) -> None:
    ev = _evidence(
        throttle=_const(0.1),  # below the 0.20 command threshold
        tracks=_closing_track("A", t_from=2.0, t_to=6.0, r0=40.0, range_rate=-8.0),
    )
    res = P2_NO_THROTTLE_CLOSING.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.violating_intervals == []
    assert res.witness["n_closing_episodes"] == 1


def test_p2_unknown_without_range_rate_evidence(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.9))
    res = P2_NO_THROTTLE_CLOSING.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert "no range-rate evidence" in res.reason


def test_p2_unknown_when_nothing_ever_closes_fast(cfg: Config) -> None:
    ev = _evidence(
        throttle=_const(0.9),
        tracks=_closing_track("A", t_from=0.0, t_to=DURATION, r0=60.0, range_rate=-1.0),
    )
    res = P2_NO_THROTTLE_CLOSING.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert "vacuously" in res.reason
    assert res.witness["max_closing_rate_mps"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# P3 -- post-collision stop
# ---------------------------------------------------------------------------


def _decelerating_speed(t_impact: float) -> Callable[[float], float]:
    """10 m/s until impact, then a hard 8 m/s^2 deceleration to standstill."""
    return lambda t: 10.0 if t < t_impact else max(0.0, 10.0 - 8.0 * (t - t_impact))


def test_p3_unknown_when_no_collision_occurred(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.3))
    res = P3_POST_COLLISION_STOP.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert "vacuously" in res.reason
    assert res.violating_intervals == []


def test_p3_pass_when_vehicle_stops_after_the_collision(cfg: Config) -> None:
    t_impact = 5.0
    ev = _evidence(
        speed=_decelerating_speed(t_impact),
        throttle=lambda t: 0.3 if t < t_impact else 0.0,
        brake=lambda t: 0.0 if t < t_impact else 1.0,
        triggers=[_collision_trigger("A", t_impact)],
    )
    res = P3_POST_COLLISION_STOP.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.witness["t_collision_s"] == pytest.approx(t_impact)
    # 10 -> below 1 m/s at 8 m/s^2 takes 1.125 s.
    assert res.witness["stop_latency_s"] == pytest.approx(1.125, abs=DT + 1e-6)
    assert res.witness["max_throttle_in_window"] == pytest.approx(0.0)


def test_p3_fail_when_still_throttling_after_the_collision(cfg: Config) -> None:
    t_impact = 5.0
    ev = _evidence(speed=_const(10.0), throttle=_const(0.6), triggers=[_collision_trigger("A", t_impact)])
    res = P3_POST_COLLISION_STOP.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert res.violating_intervals
    start, end = res.violating_intervals[0]
    assert start == pytest.approx(t_impact, abs=DT)
    assert end == pytest.approx(t_impact + 3.0, abs=DT)
    assert res.witness["max_throttle_in_window"] == pytest.approx(0.6)
    assert res.parameters["max_throttle"] == pytest.approx(0.05)


def test_p3_fail_when_vehicle_never_slows_down(cfg: Config) -> None:
    """Throttle released but speed never falls below the stop threshold."""
    t_impact = 5.0
    ev = _evidence(
        speed=_const(9.0),
        throttle=_const(0.0),
        triggers=[_collision_trigger("A", t_impact)],
    )
    res = P3_POST_COLLISION_STOP.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert res.violating_intervals[0][0] == pytest.approx(t_impact)
    assert "never fell below" in res.reason


def test_p3_unknown_when_window_is_truncated(cfg: Config) -> None:
    t_impact = 5.0
    ev = _evidence(
        speed=_const(9.0),
        throttle=_const(0.0),
        duration=6.0,  # window would end at 8.0 s
        triggers=[_collision_trigger("A", t_impact)],
    )
    res = P3_POST_COLLISION_STOP.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert res.witness["truncated_window"] is True


# ---------------------------------------------------------------------------
# P4 -- detected conflict without an evasive response
# ---------------------------------------------------------------------------


def test_p4_fail_when_conflict_gets_no_evasive_response(cfg: Config) -> None:
    ev = _evidence(
        throttle=_const(0.4),
        events=[_event("A", EventType.PREDICTED_PATH_CONFLICT, 3.0)],
    )
    res = P4_CONFLICT_NO_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert len(res.violating_intervals) == 1
    start, end = res.violating_intervals[0]
    assert start == pytest.approx(3.0)
    assert end == pytest.approx(6.0)  # lookahead 3.0 s, no earlier outcome
    assert res.counterexample_ref is not None
    assert res.witness["n_conflicts"] == 1
    assert res.witness["n_violations"] == 1


def test_p4_window_is_clipped_at_the_outcome(cfg: Config) -> None:
    """A collision 1 s after the conflict ends the response opportunity there."""
    ev = _evidence(
        throttle=_const(0.4),
        events=[_event("A", EventType.CONFLICT_REGION_ENTRY, 3.0)],
        triggers=[_collision_trigger("A", 4.0)],
    )
    res = P4_CONFLICT_NO_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    start, end = res.violating_intervals[0]
    assert start == pytest.approx(3.0)
    assert end == pytest.approx(4.0)
    assert res.witness["outcome_t_s"] == pytest.approx(4.0)


def test_p4_pass_when_the_driver_brakes(cfg: Config) -> None:
    ev = _evidence(
        brake=lambda t: 0.6 if t >= 3.4 else 0.0,
        events=[_event("A", EventType.PREDICTED_PATH_CONFLICT, 3.0)],
    )
    res = P4_CONFLICT_NO_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.witness["max_response_latency_s"] == pytest.approx(0.4, abs=DT + 1e-6)


def test_p4_pass_when_the_driver_steers(cfg: Config) -> None:
    ev = _evidence(
        steer=lambda t: -0.3 if t >= 3.2 else 0.0,
        events=[_event("A", EventType.PREDICTED_PATH_CONFLICT, 3.0)],
    )
    res = P4_CONFLICT_NO_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.witness["max_abs_steer_after_first_conflict"] == pytest.approx(0.3)


def test_p4_unknown_without_a_detected_conflict(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    res = P4_CONFLICT_NO_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.UNKNOWN
    assert res.witness["n_conflicts"] == 0


# ---------------------------------------------------------------------------
# Counterexamples
# ---------------------------------------------------------------------------


def test_extract_counterexample_covers_interval_plus_padding_and_no_more(
    cfg: Config,
) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    res = P1_BRAKE_RESPONSE.evaluate(ev, cfg, {"participant_id": "A"})
    assert res.status is CheckStatus.FAIL
    interval = res.violating_intervals[0]

    ce = extract_counterexample(ev, interval, cfg, pad_s=1.0)

    lo, hi = ce["padded_interval"]
    assert lo == pytest.approx(interval[0] - 1.0)
    assert hi == pytest.approx(interval[1] + 1.0)

    ts = [row["t"] for row in ce["samples"]]
    assert ts, "counterexample must not be empty"
    # ... no sample outside the padded window ...
    assert min(ts) >= lo - 1e-9
    assert max(ts) <= hi + 1e-9
    # ... and the padding is actually populated, not clipped away.
    assert min(ts) <= lo + DT + 1e-9
    assert max(ts) >= hi - DT - 1e-9
    # ... and the violating interval itself is strictly inside the sample span.
    assert min(ts) < interval[0]
    assert max(ts) > interval[1]
    assert len(ts) == pytest.approx((hi - lo) / DT + 1, abs=1.0)
    assert ts == sorted(ts)

    assert ce["columns"] == list(COUNTEREXAMPLE_COLUMNS)
    assert set(ce["samples"][0].keys()) == set(COUNTEREXAMPLE_COLUMNS)
    assert ce["participant_id"] == "A"
    assert ce["subsampled"] is False

    inside = ce["conditions"]["inside_violating_interval"]
    assert len(inside) == 1
    assert inside[0][0] == pytest.approx(interval[0], abs=DT)
    assert inside[0][1] == pytest.approx(interval[1], abs=DT)

    critical = ce["conditions"]["critical_ttc"]
    assert critical and critical[0][0] == pytest.approx(CRITICAL_ONSET, abs=DT)
    assert ce["conditions"]["braking"] == []
    assert ce["summary"]["max_brake"] == pytest.approx(0.0)
    assert ce["summary"]["max_throttle"] == pytest.approx(0.4)
    assert ce["summary"]["track_ids"] == [make_track_id("A", 1)]


def test_extract_counterexample_respects_the_size_bound(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    small = cfg.with_overrides({"checking": {"counterexample": {"max_samples": 10}}})

    ce = extract_counterexample(ev, (1.0, 8.0), small, pad_s=1.0)

    assert ce["subsampled"] is True
    assert ce["n_samples"] <= 11
    assert ce["n_samples_available"] > ce["n_samples"]
    lo, hi = ce["padded_interval"]
    ts = [row["t"] for row in ce["samples"]]
    assert min(ts) >= lo - 1e-9 and max(ts) <= hi + 1e-9
    # The bounds of the window survive decimation.
    assert min(ts) <= lo + DT + 1e-9
    assert max(ts) >= hi - DT - 1e-9


def test_extract_counterexample_rejects_a_reversed_interval(cfg: Config) -> None:
    ev = _evidence()
    with pytest.raises(ValueError):
        extract_counterexample(ev, (4.0, 2.0), cfg)


def test_build_counterexample_report_links_refs_to_traces(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    run = _run({"A": ev})
    results = TraceChecker(cfg).check_participant(ev)
    failures = [r for r in results if r.status is CheckStatus.FAIL]
    assert failures, "the synthetic trace must produce at least one FAIL"

    report = build_counterexample_report(results, run, cfg)

    assert report["n_counterexamples"] == len(failures)
    assert report["run_id"] == "R_test"
    for res in failures:
        assert res.counterexample_ref in report["counterexamples"]
        payload = report["counterexamples"][res.counterexample_ref]
        assert payload["property_id"] == res.property_id
        assert payload["parameters"] == res.parameters
        assert payload["violating_intervals"] == [
            [a, b] for a, b in res.violating_intervals
        ]
        assert payload["samples"]
    assert sorted(row["counterexample_ref"] for row in report["index"]) == sorted(
        report["counterexamples"].keys()
    )
    assert report["skipped"] == []


def test_check_and_persist_writes_both_artifacts(cfg: Config, tmp_path) -> None:
    """Regression: the results referenced counterexamples nobody wrote.

    Every FAIL carries a `counterexample_ref`. For the whole recorded campaign
    those references resolved to nothing, because `counterexamples.json` was
    never produced -- the report builder existed, was tested, and was not
    wired into any pipeline. The viewer, which resolves the refs, showed
    "counterexample report missing" for all 171 of them.
    """
    from cdf.common.io import read_json
    from cdf.common.layout import RunLayout

    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    run = _run({"A": ev})
    layout = RunLayout.create(tmp_path, "S01", "rear_end", 0, "crash").ensure()

    report = TraceChecker(cfg).check_and_persist(layout, run)

    assert layout.model_check_results.exists()
    assert layout.counterexamples.exists()

    results = read_json(layout.model_check_results)["results"]
    cex = read_json(layout.counterexamples)["counterexamples"]
    refs = [r["counterexample_ref"] for r in results if r["status"] == "FAIL"]
    assert refs, "the synthetic trace must produce at least one FAIL"
    dangling = [ref for ref in refs if ref not in cex]
    assert not dangling, "counterexample refs resolving to nothing: {0}".format(dangling)
    assert report["summary"]["FAIL"] == len(refs)


def test_check_run_and_check_run_with_results_agree(cfg: Config) -> None:
    """The two entry points must not be able to describe different verdicts."""
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    run = _run({"A": ev})
    checker = TraceChecker(cfg)

    plain = checker.check_run(run)
    report, results = checker.check_run_with_results(run)

    assert plain == report
    assert [r.to_dict() for r in results] == report["results"]


def test_build_counterexample_report_records_unexplainable_failures(cfg: Config) -> None:
    """A FAIL for a participant that is not in the bundle is reported, not dropped."""
    ev = _evidence()
    run = _run({"A": ev})
    orphan = PropertyResult(
        property_id="P1_brake_response",
        status=CheckStatus.FAIL,
        participant_id="Z",
        violating_intervals=[(1.0, 2.0)],
        parameters={"ttc_critical_s": 1.6},
        reason="synthetic",
    )
    report = build_counterexample_report([orphan], run, cfg)

    assert report["n_counterexamples"] == 0
    assert len(report["skipped"]) == 1
    assert report["skipped"][0]["participant_id"] == "Z"


# ---------------------------------------------------------------------------
# Oracle properties (privileged, kept separate)
# ---------------------------------------------------------------------------


def _oracle_trace(
    signal_for_a: Optional[str] = "red",
    with_privileged_fields: bool = True,
    duration: float = 6.0,
) -> Dict[str, Any]:
    """Privileged trace: A enters a junction at 2 s, B at 3 s.

    A is the yielding party (``has_right_of_way`` False) and B has priority, so
    their overlap in [3, 4] s is a right-of-way violation by A.
    """
    samples: List[Dict[str, Any]] = []
    for i, t in enumerate(_times(DT, duration)):
        a: Dict[str, Any] = {"x": float(t), "y": 0.0, "speed": 8.0}
        b: Dict[str, Any] = {"x": 0.0, "y": float(t), "speed": 9.0}
        if with_privileged_fields:
            a["in_junction"] = 2.0 <= t <= 4.0
            a["has_right_of_way"] = False
            a["signal_state"] = signal_for_a
            b["in_junction"] = 3.0 <= t <= 5.0
            b["has_right_of_way"] = True
            b["signal_state"] = "green"
        samples.append({"t": t, "actors": {"A": a, "B": b}})
    return {"run_id": "R_test", "scenario_id": "S07", "samples": samples}


def test_oracle_properties_are_unknown_without_privileged_fields(cfg: Config) -> None:
    trace = _oracle_trace(with_privileged_fields=False)
    results = TraceChecker(cfg).check_oracle(trace)

    assert results, "the oracle checker must return one result per property/actor"
    assert all(r.status is CheckStatus.UNKNOWN for r in results)
    assert all(r.scope is Provenance.ORACLE for r in results)
    assert all("absent" in r.reason for r in results)
    assert all(r.parameters for r in results)


def test_oracle_signal_property_detects_a_red_light_entry(cfg: Config) -> None:
    trace = _oracle_trace(signal_for_a="red")
    res = O1_SIGNAL_COMPLIANCE.evaluate(trace, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.FAIL
    assert res.scope is Provenance.ORACLE
    assert len(res.violating_intervals) == 1
    assert res.violating_intervals[0][1] == pytest.approx(2.0, abs=DT)
    entries = res.witness["per_participant"]["A"]["entries"]
    assert len(entries) == 1
    assert entries[0]["signal_at_entry"] == "red"


def test_oracle_signal_property_passes_on_a_green_entry(cfg: Config) -> None:
    trace = _oracle_trace(signal_for_a="Green")
    res = O1_SIGNAL_COMPLIANCE.evaluate(trace, cfg, {"participant_id": "A"})

    assert res.status is CheckStatus.PASS
    assert res.violating_intervals == []


def test_oracle_right_of_way_property_detects_the_yielding_party(cfg: Config) -> None:
    trace = _oracle_trace()

    failing = O2_RIGHT_OF_WAY.evaluate(trace, cfg, {"participant_id": "A"})
    assert failing.status is CheckStatus.FAIL
    assert failing.scope is Provenance.ORACLE
    start, end = failing.violating_intervals[0]
    assert start == pytest.approx(3.0, abs=DT)
    assert end == pytest.approx(4.0, abs=DT)
    assert failing.witness["per_participant"]["A"]["priority_participants"] == ["B"]

    # B holds right of way, so the antecedent never applies to it.
    priority = O2_RIGHT_OF_WAY.evaluate(trace, cfg, {"participant_id": "B"})
    assert priority.status is CheckStatus.UNKNOWN
    assert "yield" in priority.reason


def test_oracle_right_of_way_is_unknown_with_a_single_actor(cfg: Config) -> None:
    trace = _oracle_trace()
    for sample in trace["samples"]:
        sample["actors"].pop("B")
    res = O2_RIGHT_OF_WAY.evaluate(trace, cfg, {"participant_id": "A"})
    assert res.status is CheckStatus.UNKNOWN
    assert "at least two actors" in res.reason


# ---------------------------------------------------------------------------
# TraceChecker
# ---------------------------------------------------------------------------


def test_check_participant_runs_every_local_property(cfg: Config) -> None:
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    results = TraceChecker(cfg).check_participant(ev)

    assert [r.property_id for r in results] == [p.property_id for p in LOCAL_PROPERTIES]
    assert all(r.participant_id == "A" for r in results)
    assert all(r.scope is Provenance.LOCAL for r in results)


def test_every_result_carries_reproducible_parameters(cfg: Config) -> None:
    """A verdict must be replayable from the thresholds it recorded."""
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    results = TraceChecker(cfg).check_participant(ev)

    expected = {
        "P1_brake_response": ("ttc_critical_s", "response_window_s", "brake_cmd"),
        "P2_no_throttle_while_closing": ("closing_rate_mps", "grace_s", "throttle_cmd"),
        "P3_post_collision_stop": ("window_s", "max_throttle", "stop_speed_mps"),
        "P4_conflict_without_response": (
            "lookahead_s",
            "min_evasive_brake",
            "min_evasive_steer",
        ),
    }
    for res in results:
        assert res.parameters, res.property_id
        for key in expected[res.property_id]:
            assert key in res.parameters, (res.property_id, key)
        # Sampling tolerances change verdicts, so they are part of the record.
        assert "match_tolerance_s" in res.parameters
        assert "max_gap_s" in res.parameters
        assert res.reason, res.property_id


def test_check_run_aggregates_by_participant_and_by_property(cfg: Config) -> None:
    failing = _evidence("A", throttle=_const(0.4), tracks=_approaching_tracks())
    braking = _evidence(
        "B",
        brake=lambda t: 0.8 if t >= CRITICAL_ONSET + 0.2 else 0.0,
        tracks=_approaching_tracks("B"),
    )
    report = TraceChecker(cfg).check_run(_run({"A": failing, "B": braking}))

    assert report["schema_version"]
    assert report["scope"] == Provenance.LOCAL.value
    assert report["config_hash"] == cfg.hash
    assert len(report["results"]) == 2 * len(LOCAL_PROPERTIES)

    totals = report["summary"]
    assert set(totals.keys()) == {"PASS", "FAIL", "UNKNOWN"}
    assert sum(totals.values()) == len(report["results"])

    assert sorted(report["by_participant"].keys()) == ["A", "B"]
    assert report["by_participant"]["A"]["statuses"]["P1_brake_response"] == "FAIL"
    assert report["by_participant"]["B"]["statuses"]["P1_brake_response"] == "PASS"

    p1 = report["by_property"]["P1_brake_response"]
    assert p1["summary"]["FAIL"] == 1
    assert p1["summary"]["PASS"] == 1
    assert "F[0,response_window_s]" in p1["formal"]

    # No privileged verdict may leak into the local report.
    assert all(row["scope"] == Provenance.LOCAL.value for row in report["results"])


def test_check_run_results_are_json_shaped(cfg: Config) -> None:
    import json

    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    report = TraceChecker(cfg).check_run(_run({"A": ev}))
    text = json.dumps(report, sort_keys=True)
    assert '"status": "FAIL"' in text
    assert "Provenance" not in text and "CheckStatus" not in text


def test_check_oracle_is_separate_and_oracle_scoped(cfg: Config) -> None:
    checker = TraceChecker(cfg)
    oracle_results = checker.check_oracle(_oracle_trace())

    assert len(oracle_results) == len(ORACLE_PROPERTIES) * 2  # two actors
    assert all(r.scope is Provenance.ORACLE for r in oracle_results)
    assert {r.property_id for r in oracle_results} == {
        p.property_id for p in ORACLE_PROPERTIES
    }
    # The local registry and the oracle registry are disjoint.
    assert not ({p.property_id for p in LOCAL_PROPERTIES} & {
        p.property_id for p in ORACLE_PROPERTIES
    })


def test_checker_refuses_an_oracle_property_in_the_local_registry(cfg: Config) -> None:
    with pytest.raises(ValueError):
        TraceChecker(cfg, properties=[O1_SIGNAL_COMPLIANCE])


def test_checker_can_be_restricted_by_configuration(cfg: Config) -> None:
    restricted = cfg.with_overrides(
        {"checking": {"enabled_properties": ["P1_brake_response"]}}
    )
    ev = _evidence(throttle=_const(0.4), tracks=_approaching_tracks())
    results = TraceChecker(restricted).check_participant(ev)
    assert [r.property_id for r in results] == ["P1_brake_response"]

    with pytest.raises(KeyError):
        TraceChecker(cfg.with_overrides({"checking": {"enabled_properties": ["nope"]}}))


def test_summarise_results_reports_all_three_verdicts() -> None:
    counts = summarise_results([])
    assert counts == {"PASS": 0, "FAIL": 0, "UNKNOWN": 0}
