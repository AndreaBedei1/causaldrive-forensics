"""Unit tests for :mod:`cdf.fusion.time_alignment`.

The alignment stage is the foundation every later cross-participant comparison
rests on, so these tests pin the two properties that matter: a synchronous run
must be recognised as synchronous (offset 0, residual 0), and an artificially
de-synchronised log must have its offset recovered to sub-millisecond accuracy.
Failure modes -- an un-estimable offset, an empty log, disjoint spans -- must be
surfaced as diagnostics instead of being silently absorbed.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import List

import pytest

from cdf.common.config import load_run_config
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import TelemetrySample
from cdf.fusion.time_alignment import align_participants, aligned_spans, apply_offset

DT = 0.05
N = 101


@pytest.fixture(scope="module")
def cfg():
    return load_run_config()


def _telemetry(pid: str, times: List[float]) -> List[TelemetrySample]:
    """A straight-line trace; only the timestamps matter for alignment."""
    return [
        TelemetrySample(
            t=float(t),
            frame=i,
            participant_id=pid,
            x=10.0 * float(t),
            y=0.0,
            z=0.0,
            yaw=0.0,
            vx=10.0,
            vy=0.0,
            speed=10.0,
        )
        for i, t in enumerate(times)
    ]


def _run(**streams: List[float]) -> RunEvidence:
    participants = {
        pid: ParticipantEvidence(participant_id=pid, telemetry=_telemetry(pid, times))
        for pid, times in streams.items()
    }
    return RunEvidence(run_dir=Path("."), manifest={"run_id": "unit", "seed": 0}, participants=participants)


def _grid(n: int = N, dt: float = DT, start: float = 0.0) -> List[float]:
    return [start + k * dt for k in range(n)]


def _kinds(result) -> List[str]:
    return [d["kind"] for d in result["diagnostics"]]


def test_identical_series_align_at_zero_offset(cfg):
    """Two recorders stepped by the same server must show no offset at all."""
    result = align_participants(_run(A=_grid(), B=_grid()), cfg)

    assert result["reference"] in ("A", "B")
    assert sorted(result["offsets"].keys()) == ["A", "B"]
    for pid in ("A", "B"):
        entry = result["offsets"][pid]
        assert abs(entry["offset_s"]) < 1e-9
        assert entry["residual_s"] < 1e-9
        assert entry["confidence"] > 0.99
    assert result["common_span"] == pytest.approx([0.0, (N - 1) * DT])
    assert "offset_exceeds_limit" not in _kinds(result)
    assert "non_zero_offset" not in _kinds(result)


def test_injected_offset_is_recovered_to_within_one_millisecond(cfg):
    """A deliberately shifted log must have its shift measured, not absorbed.

    The shift is chosen smaller than half the sampling period so that the nearest
    neighbour of each shifted sample is still its own grid point; a shift that is
    an exact multiple of the period is unobservable from timestamps alone.
    """
    shift = 0.017
    result = align_participants(
        _run(A=_grid(), B=[t + shift for t in _grid()]), cfg
    )

    # Whichever participant became the reference, the *relative* correction that
    # maps B's clock onto A's must equal -shift.
    relative = result["offsets"]["B"]["offset_s"] - result["offsets"]["A"]["offset_s"]
    assert relative == pytest.approx(-shift, abs=1e-3)
    assert result["offsets"]["B"]["n_samples"] == N
    assert result["offsets"]["B"]["residual_s"] < 1e-6
    assert "non_zero_offset" in _kinds(result)
    assert "offset_exceeds_limit" not in _kinds(result)

    corrected = aligned_spans(_run(A=_grid(), B=[t + shift for t in _grid()]), result["offsets"])
    assert corrected["A"][0] == pytest.approx(corrected["B"][0], abs=1e-3)


def test_non_overlapping_streams_report_an_unestimable_offset(cfg):
    """When no sample pair is close enough, the offset must be declared unknown.

    The nearest-neighbour estimator can only see offsets inside its search window;
    beyond it there is no evidence, and the honest output is a zero offset carrying
    zero confidence plus a loud diagnostic -- never a fabricated correction.
    """
    result = align_participants(_run(A=_grid(), B=_grid(start=60.0)), cfg)

    entry = result["offsets"]["B"]
    assert entry["n_samples"] == 0
    assert entry["confidence"] == 0.0
    assert not math.isfinite(entry["residual_s"])
    assert "offset_not_estimable" in _kinds(result)


def test_offset_above_the_configured_limit_is_flagged(cfg):
    """``fusion.time_alignment.max_offset_s`` is enforced as a diagnostic threshold."""
    strict = cfg.with_overrides(
        {"fusion": {"time_alignment": {"max_offset_s": 0.01}}}
    )
    result = align_participants(
        _run(A=_grid(), B=[t + 0.017 for t in _grid()]), strict
    )

    assert "offset_exceeds_limit" in _kinds(result)
    flagged = [d for d in result["diagnostics"] if d["kind"] == "offset_exceeds_limit"]
    assert flagged[0]["participant_id"] == "B"
    assert abs(flagged[0]["offset_s"]) == pytest.approx(0.017, abs=1e-3)


def test_empty_telemetry_participant_is_excluded_with_a_diagnostic(cfg):
    """A participant that exported nothing cannot be aligned and must say so."""
    run = _run(A=_grid(), B=_grid())
    run.participants["C"] = ParticipantEvidence(participant_id="C")

    result = align_participants(run, cfg)

    assert "C" not in result["offsets"]
    assert "empty_telemetry" in _kinds(result)
    assert result["common_span"] is not None


def test_disjoint_spans_yield_no_common_span(cfg):
    """Logs that never overlap support no cross-participant claim at all."""
    result = align_participants(
        _run(A=_grid(), B=_grid(start=60.0)), cfg
    )

    assert result["common_span"] is None
    assert "no_common_span" in _kinds(result)


def test_apply_offset_shifts_every_sample(cfg):
    """The public shift helper follows the documented sign convention."""
    times = [0.0, 0.5, 1.0]
    assert apply_offset(times, 0.25) == pytest.approx([0.25, 0.75, 1.25])
    assert apply_offset(times, -0.25) == pytest.approx([-0.25, 0.25, 0.75])
    assert apply_offset([], 1.0) == []


def test_grid_dt_comes_from_configuration(cfg):
    """The fusion grid step is a configured quantity, never a literal."""
    result = align_participants(_run(A=_grid(), B=_grid()), cfg)
    assert result["grid_dt"] == pytest.approx(
        float(cfg.get("fusion.time_alignment.grid_dt"))
    )
