"""Unit tests for :mod:`cdf.local.indicators`.

Each test builds a synthetic participant whose ground truth is known analytically
(constant deceleration, a pure lateral step, two straight paths that cross at a
computable point) and asserts the numeric value the indicator must reproduce.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence

import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import ParticipantEvidence
from cdf.common.schemas import ControlSample, TelemetrySample, TrackSample
from cdf.local.indicators import (
    compute_own_indicators,
    compute_track_indicators,
    cumulative_heading_change,
    infer_conflict,
    lateral_path_offset,
    net_heading_change,
)

DT = 0.05
PID = "A"


# ---------------------------------------------------------------------------
# Builders
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def cfg() -> Config:
    """The real pipeline configuration -- the thresholds under test are its own."""
    return load_run_config()


def make_telemetry(
    times: Sequence[float],
    xs: Sequence[float],
    ys: Sequence[float],
    yaws: Sequence[float],
    speeds: Optional[Sequence[float]] = None,
    vxs: Optional[Sequence[float]] = None,
    vys: Optional[Sequence[float]] = None,
    accel_long: Optional[Sequence[float]] = None,
    yaw_rates: Optional[Sequence[float]] = None,
) -> List[TelemetrySample]:
    """Build a telemetry trace; omitted channels keep their schema default 0.0."""
    out: List[TelemetrySample] = []
    for i, t in enumerate(times):
        out.append(
            TelemetrySample(
                t=float(t),
                frame=i,
                participant_id=PID,
                x=float(xs[i]),
                y=float(ys[i]),
                z=0.0,
                yaw=float(yaws[i]),
                vx=0.0 if vxs is None else float(vxs[i]),
                vy=0.0 if vys is None else float(vys[i]),
                speed=0.0 if speeds is None else float(speeds[i]),
                accel_long=0.0 if accel_long is None else float(accel_long[i]),
                yaw_rate=0.0 if yaw_rates is None else float(yaw_rates[i]),
            )
        )
    return out


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
    rel_vx: Optional[Sequence[float]] = None,
    rel_vy: Optional[Sequence[float]] = None,
    confidence: float = 0.8,
) -> List[TrackSample]:
    """Build one radar track; ``range_m`` follows from the body-frame position."""
    out: List[TrackSample] = []
    for i, t in enumerate(times):
        out.append(
            TrackSample(
                t=float(t),
                frame=i,
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
                rel_vx=0.0 if rel_vx is None else float(rel_vx[i]),
                rel_vy=0.0 if rel_vy is None else float(rel_vy[i]),
                n_points=5,
                confidence=confidence,
                age=i,
            )
        )
    return out


def grid(n: int, dt: float = DT) -> List[float]:
    return [round(k * dt, 6) for k in range(n)]


# ---------------------------------------------------------------------------
# Window helpers
# ---------------------------------------------------------------------------


def test_cumulative_heading_change_accumulates_only_inside_the_window() -> None:
    """A 30 deg/s turn lasting 1 s registers 30 deg, then decays out of the window."""
    times = grid(81)  # 0 .. 4.0 s
    yaws = []
    for t in times:
        if t < 1.0:
            yaws.append(0.0)
        elif t < 2.0:
            yaws.append(30.0 * (t - 1.0))
        else:
            yaws.append(30.0)

    cum = cumulative_heading_change(times, yaws, 1.5)
    net = net_heading_change(times, yaws, 1.5)

    i_2 = times.index(2.0)
    i_3 = times.index(3.0)
    # At t = 2.0 the 1.5 s window [0.5, 2.0] contains the whole 30 deg turn.
    assert cum[i_2] == pytest.approx(30.0, abs=1e-6)
    assert net[i_2] == pytest.approx(30.0, abs=1e-6)
    # At t = 3.0 the window [1.5, 3.0] contains only its second half.
    assert cum[i_3] == pytest.approx(15.0, abs=1e-6)
    assert net[i_3] == pytest.approx(15.0, abs=1e-6)
    assert cum[0] == pytest.approx(0.0)


def test_cumulative_and_net_heading_separate_a_turn_from_an_excursion() -> None:
    """An out-and-back steering excursion nets out; a turn does not."""
    times = grid(61)  # 0 .. 3.0 s
    excursion = [10.0 * math.sin(math.pi * t / 3.0) for t in times]
    turn = [30.0 * t for t in times]

    cum_exc = cumulative_heading_change(times, excursion, 3.0)
    net_exc = net_heading_change(times, excursion, 3.0)
    cum_turn = cumulative_heading_change(times, turn, 3.0)
    net_turn = net_heading_change(times, turn, 3.0)

    # The excursion peaks at 10 deg and returns: ~20 deg of accumulated change,
    # ~0 net. The turn spends all of its accumulated change on a net change.
    assert cum_exc[-1] == pytest.approx(20.0, abs=0.2)
    assert net_exc[-1] == pytest.approx(0.0, abs=0.2)
    assert cum_turn[-1] == pytest.approx(90.0, abs=1e-6)
    assert net_turn[-1] == pytest.approx(90.0, abs=1e-6)


def test_lateral_path_offset_measures_sideways_drift_from_own_heading() -> None:
    """A pure +3.5 m sideways step shows up as a +3.5 m offset (body +y is right)."""
    times = grid(101)  # 0 .. 5.0 s
    xs = [10.0 * t for t in times]
    ys = [0.0 if t < 2.0 else min(3.5, 3.5 * (t - 2.0)) for t in times]
    yaws = [0.0] * len(times)

    offset = lateral_path_offset(times, xs, ys, yaws, 3.0)

    i_4 = times.index(4.0)
    # Window [1.0, 4.0]: reference pose heading 0 at y = 0, current y = 3.5.
    assert offset[i_4] == pytest.approx(3.5, abs=1e-6)
    assert offset[0] == pytest.approx(0.0)
    # A mirrored manoeuvre yields the opposite sign.
    mirrored = lateral_path_offset(times, xs, [-v for v in ys], yaws, 3.0)
    assert mirrored[i_4] == pytest.approx(-3.5, abs=1e-6)


# ---------------------------------------------------------------------------
# Own indicators
# ---------------------------------------------------------------------------


def test_compute_own_indicators_joins_controls_and_keeps_recorded_acceleration(
    cfg: Config,
) -> None:
    """Controls join by frame; a recorded acceleration is reported verbatim."""
    times = grid(41)  # 0 .. 2.0 s
    speeds = [max(0.0, 10.0 - 4.0 * t) for t in times]
    accels = [-4.0] * len(times)
    xs, x = [], 0.0
    for i, t in enumerate(times):
        xs.append(x)
        x += speeds[i] * DT

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, xs, [0.0] * len(times), [0.0] * len(times), speeds=speeds, accel_long=accels
        ),
        controls=[
            ControlSample(t=t, frame=i, participant_id=PID, throttle=0.0, brake=0.7, steer=-0.2)
            for i, t in enumerate(times)
        ],
    )

    ind = compute_own_indicators(ev, cfg)

    assert len(ind) == len(times)
    assert ind[10].accel_long == pytest.approx(-4.0)
    assert ind[10].speed == pytest.approx(speeds[10])
    assert ind[10].brake == pytest.approx(0.7)
    assert ind[10].steer == pytest.approx(-0.2)
    assert ind[10].throttle == pytest.approx(0.0)
    assert ind[10].frame == 10


def test_compute_own_indicators_reconstructs_acceleration_when_unrecorded(
    cfg: Config,
) -> None:
    """A recorder that stored no IMU channel still yields a usable acceleration."""
    times = grid(41)
    speeds = [max(0.0, 10.0 - 4.0 * t) for t in times]  # -4 m/s^2 until standstill
    xs, x = [], 0.0
    for i, _t in enumerate(times):
        xs.append(x)
        x += speeds[i] * DT

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times, xs, [0.0] * len(times), [0.0] * len(times), speeds=speeds
        ),
    )

    ind = compute_own_indicators(ev, cfg)
    # Interior samples (still braking, not yet stopped) must recover -4 m/s^2.
    assert ind[10].accel_long == pytest.approx(-4.0, abs=1e-6)
    assert ind[20].accel_long == pytest.approx(-4.0, abs=1e-6)

    # With the fallback disabled the unrecorded channel stays exactly zero.
    strict = cfg.with_overrides({"indicators": {"derived_fallback": False}})
    assert compute_own_indicators(ev, strict)[10].accel_long == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# Track indicators
# ---------------------------------------------------------------------------


def test_track_indicators_ttc_and_closest_approach_head_on(cfg: Config) -> None:
    """A target 30 m ahead closing at 10 m/s has TTC 3 s and a head-on CPA."""
    times = grid(21)  # 0 .. 1.0 s
    ranges = [30.0 - 10.0 * t for t in times]
    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(times, [0.0] * len(times), [0.0] * len(times), [0.0] * len(times)),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=ranges,
            rel_y=[0.0] * len(times),
            range_rate=[-10.0] * len(times),
            gx=ranges,
            gy=[0.0] * len(times),
            rel_vx=[-10.0] * len(times),
            rel_vy=[0.0] * len(times),
        ),
    )

    ti = compute_track_indicators(ev, cfg)["A::T001"]

    assert ti[0].ttc == pytest.approx(3.0, abs=1e-9)
    assert ti[0].t_cpa == pytest.approx(3.0, abs=1e-9)
    assert ti[0].d_cpa == pytest.approx(0.0, abs=1e-9)
    assert ti[0].range_m == pytest.approx(30.0)
    assert ti[0].longitudinal_m == pytest.approx(30.0)
    assert ti[0].lateral_offset_m == pytest.approx(0.0)
    # Halfway through the trace the range has shrunk by 5 m and TTC with it.
    assert ti[10].ttc == pytest.approx(2.5, abs=1e-9)


def test_track_indicators_ttc_is_none_when_not_closing_or_beyond_cap(cfg: Config) -> None:
    """TTC is evidence of closing, not a safety score: absence is reported as None."""
    times = grid(11)
    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(times, [0.0] * len(times), [0.0] * len(times), [0.0] * len(times)),
        tracks=(
            make_track(
                "A::T001",
                times,
                rel_x=[20.0 + 3.0 * t for t in times],
                rel_y=[0.0] * len(times),
                range_rate=[3.0] * len(times),  # receding
            )
            + make_track(
                "A::T002",
                times,
                rel_x=[80.0 - 0.5 * t for t in times],
                rel_y=[0.0] * len(times),
                range_rate=[-0.5] * len(times),  # 160 s away: beyond the cap
            )
        ),
    )

    by_id = compute_track_indicators(ev, cfg)
    assert all(s.ttc is None for s in by_id["A::T001"])
    assert all(s.ttc is None for s in by_id["A::T002"])


def test_track_indicators_infer_target_deceleration_from_range_rate(cfg: Config) -> None:
    """A range rate growing 2.5 m/s per second means the target sheds 2.5 m/s^2."""
    times = grid(41)  # 0 .. 2.0 s
    # Observer rolls at a constant 10 m/s, so all of the change belongs to the target.
    ranges, r = [], 50.0
    rates = [-2.5 * t for t in times]
    for i, _t in enumerate(times):
        ranges.append(r)
        r += rates[i] * DT

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times,
            [10.0 * t for t in times],
            [0.0] * len(times),
            [0.0] * len(times),
            speeds=[10.0] * len(times),
        ),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=ranges,
            rel_y=[0.0] * len(times),
            range_rate=rates,
            gx=[10.0 * times[i] + ranges[i] for i in range(len(times))],
            gy=[0.0] * len(times),
        ),
    )

    ti = compute_track_indicators(ev, cfg)["A::T001"]
    assert ti[20].target_accel_long == pytest.approx(-2.5, abs=1e-6)


def test_track_indicators_add_back_own_acceleration_along_the_line_of_sight(
    cfg: Config,
) -> None:
    """A steady range rate while *we* accelerate means the target accelerates too."""
    times = grid(41)
    speeds = [10.0 + 2.0 * t for t in times]
    xs, x = [], 0.0
    for i, _t in enumerate(times):
        xs.append(x)
        x += speeds[i] * DT

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times,
            xs,
            [0.0] * len(times),
            [0.0] * len(times),
            speeds=speeds,
            accel_long=[2.0] * len(times),
        ),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=[40.0] * len(times),  # range held constant
            rel_y=[0.0] * len(times),
            range_rate=[0.0] * len(times),
            gx=[xs[i] + 40.0 for i in range(len(times))],
            gy=[0.0] * len(times),
        ),
    )

    ti = compute_track_indicators(ev, cfg)["A::T001"]
    assert ti[20].target_accel_long == pytest.approx(2.0, abs=1e-6)


# ---------------------------------------------------------------------------
# Map-free conflict inference
# ---------------------------------------------------------------------------


def test_infer_conflict_simultaneous_arrival_scores_high(cfg: Config) -> None:
    """Two vehicles that reach the same point at the same instant: maximal score."""
    score, point, t_own, t_tgt = infer_conflict(
        -20.0, 0.0, 10.0, 0.0, 0.0, -20.0, 0.0, 10.0, cfg
    )
    assert point is not None
    assert point[0] == pytest.approx(0.0, abs=1e-6)
    assert point[1] == pytest.approx(0.0, abs=1e-6)
    assert t_own == pytest.approx(2.0, abs=1e-6)
    assert t_tgt == pytest.approx(2.0, abs=1e-6)
    assert score > 0.95


def test_infer_conflict_wide_arrival_gap_scores_zero(cfg: Config) -> None:
    """Crossing paths used ten seconds apart are not a conflict."""
    # The horizon is widened so that both predicted paths still *reach* the
    # crossing: this exercises the arrival-gap decay itself, not the horizon cut.
    wide = cfg.with_overrides({"indicators": {"conflict": {"prediction_horizon_s": 15.0}}})
    score, point, t_own, t_tgt = infer_conflict(
        -20.0, 0.0, 10.0, 0.0, 0.0, -120.0, 0.0, 10.0, wide
    )
    assert point is not None
    assert t_own == pytest.approx(2.0, abs=1e-6)
    assert t_tgt == pytest.approx(12.0, abs=1e-6)
    assert score == pytest.approx(0.0, abs=1e-9)

    # With the configured 4 s horizon the far vehicle never reaches the crossing,
    # so the same geometry yields no conflict at all.
    assert infer_conflict(-20.0, 0.0, 10.0, 0.0, 0.0, -120.0, 0.0, 10.0, cfg) == (
        0.0,
        None,
        None,
        None,
    )


def test_infer_conflict_score_decays_with_the_arrival_gap(cfg: Config) -> None:
    """Half the tolerated arrival gap costs half the score (linear decay)."""
    wide = cfg.with_overrides({"indicators": {"conflict": {"prediction_horizon_s": 6.0}}})
    max_gap = float(cfg.require("indicators.conflict.max_arrival_gap_s"))
    # Own arrives at t = 2.0; target starts 10 * (2 + max_gap/2) metres away.
    tgt_y = -10.0 * (2.0 + max_gap / 2.0)
    score, _point, t_own, t_tgt = infer_conflict(
        -20.0, 0.0, 10.0, 0.0, 0.0, tgt_y, 0.0, 10.0, wide
    )
    assert abs(t_tgt - t_own) == pytest.approx(max_gap / 2.0, abs=1e-6)
    assert score == pytest.approx(0.5, abs=1e-6)


def test_infer_conflict_parallel_paths_never_conflict(cfg: Config) -> None:
    """Paths that never cross score zero and report no conflict point."""
    assert infer_conflict(0.0, 0.0, 10.0, 0.0, 0.0, 5.0, 10.0, 0.0, cfg) == (
        0.0,
        None,
        None,
        None,
    )


def test_infer_conflict_requires_both_parties_to_be_moving(cfg: Config) -> None:
    """A near-stationary party has no predicted path, hence no conflict."""
    min_own = float(cfg.require("indicators.conflict.min_own_speed_mps"))
    slow = 0.5 * min_own
    assert infer_conflict(-20.0, 0.0, slow, 0.0, 0.0, -20.0, 0.0, 10.0, cfg)[0] == 0.0
    assert infer_conflict(-20.0, 0.0, 10.0, 0.0, 0.0, -20.0, 0.0, slow, cfg)[0] == 0.0


def test_track_indicators_report_the_inferred_conflict_point_globally(cfg: Config) -> None:
    """The conflict point travels with the track series, in the global frame."""
    times = grid(5)
    own_x = [-20.0 + 10.0 * t for t in times]
    tgt_y = [-20.0 + 10.0 * t for t in times]

    ev = ParticipantEvidence(
        participant_id=PID,
        telemetry=make_telemetry(
            times,
            own_x,
            [0.0] * len(times),
            [0.0] * len(times),
            speeds=[10.0] * len(times),
            vxs=[10.0] * len(times),
            vys=[0.0] * len(times),
        ),
        tracks=make_track(
            "A::T001",
            times,
            rel_x=[0.0 - own_x[i] for i in range(len(times))],
            rel_y=[tgt_y[i] - 0.0 for i in range(len(times))],
            range_rate=[-5.0] * len(times),
            gx=[0.0] * len(times),
            gy=tgt_y,
            gvx=[0.0] * len(times),
            gvy=[10.0] * len(times),
        ),
    )

    ti = compute_track_indicators(ev, cfg)["A::T001"]
    assert ti[0].conflict_score > 0.95
    assert ti[0].conflict_x == pytest.approx(0.0, abs=1e-6)
    assert ti[0].conflict_y == pytest.approx(0.0, abs=1e-6)
