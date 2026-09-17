"""Unit tests for :mod:`cdf.fusion.track_association`.

Every fixture here is built from quantities a vehicle could actually record: own
poses, own velocities, and radar-derived global position estimates for anonymous
tracks. No fixture contains a simulator actor id, so a passing test is also
evidence that the association argument never needed one.

The four behaviours pinned below are the ones the scientific claim rests on:

* a track that follows a participant's own trajectory is assigned to *that*
  participant and not to a decoy;
* a track that follows nobody is left UNRESOLVED;
* two equally good explanations produce AMBIGUOUS, not a coin flip presented as
  fact;
* the one-to-one constraint is solved globally, so a track can lose its
  individually best candidate to a better-matching competitor.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple

import pytest

from cdf.common.config import load_run_config
from cdf.common.evidence import ParticipantEvidence, RunEvidence
from cdf.common.schemas import (
    FORBIDDEN_LOCAL_FIELD_NAMES,
    FORBIDDEN_LOCAL_FIELD_SUBSTRINGS,
    TelemetrySample,
    TrackSample,
    to_jsonable,
)
from cdf.fusion.track_association import (
    STATUS_AMBIGUOUS,
    STATUS_RESOLVED,
    STATUS_UNRESOLVED,
    associate_tracks,
    association_report,
    score_candidate,
)

DT = 0.05
N = 101
SPEED = 10.0


@pytest.fixture(scope="module")
def cfg():
    return load_run_config()


def _times(n: int = N, start: float = 0.0) -> List[float]:
    return [round(start + k * DT, 6) for k in range(n)]


def _straight(
    pid: str, y: float, x0: float = 0.0, speed: float = SPEED, times: Optional[List[float]] = None
) -> ParticipantEvidence:
    """A participant driving straight along ``+x`` in its own lane."""
    ts = times if times is not None else _times()
    telemetry = [
        TelemetrySample(
            t=t,
            frame=i,
            participant_id=pid,
            x=x0 + speed * t,
            y=y,
            z=0.0,
            yaw=0.0,
            vx=speed,
            vy=0.0,
            speed=speed,
        )
        for i, t in enumerate(ts)
    ]
    return ParticipantEvidence(participant_id=pid, telemetry=telemetry)


def _track(
    observer: ParticipantEvidence,
    track_id: str,
    path: Callable[[float], Tuple[float, float]],
    velocity: Tuple[float, float] = (SPEED, 0.0),
    times: Optional[List[float]] = None,
) -> None:
    """Attach a radar track to ``observer`` whose global estimate follows ``path``."""
    ts = times if times is not None else _times()
    for i, t in enumerate(ts):
        gx, gy = path(t)
        own = observer.telemetry[min(i, len(observer.telemetry) - 1)]
        observer.tracks.append(
            TrackSample(
                t=t,
                frame=i,
                participant_id=observer.participant_id,
                track_id=track_id,
                rel_x=gx - own.x,
                rel_y=gy - own.y,
                gx=gx,
                gy=gy,
                gvx=velocity[0],
                gvy=velocity[1],
                range_m=math.hypot(gx - own.x, gy - own.y),
                confidence=0.8,
                n_points=6,
                age=i,
            )
        )


def _run(*participants: ParticipantEvidence) -> RunEvidence:
    return RunEvidence(
        run_dir=Path("."),
        manifest={"run_id": "unit", "scenario_id": "S00", "seed": 0},
        participants={p.participant_id: p for p in participants},
    )


def _noise(t: float, amplitude: float = 0.15) -> float:
    """Deterministic, zero-mean measurement noise (no RNG: reruns must match)."""
    return amplitude * math.sin(3.0 * t)


def _keys(obj: Any, out: List[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.append(str(k))
            _keys(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _keys(v, out)


# ---------------------------------------------------------------------------
# The central case
# ---------------------------------------------------------------------------


def _leader_follower_decoy() -> RunEvidence:
    """``A`` follows ``B``; ``C`` drives a parallel lane 4.5 m away."""
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    c = _straight("C", y=4.5, x0=20.0)
    _track(
        a,
        "A::T001",
        lambda t: (20.0 + SPEED * t + _noise(t), 0.0 + _noise(t, 0.1)),
    )
    return _run(a, b, c)


def test_track_is_assigned_to_the_participant_whose_trajectory_it_follows(cfg):
    """The core claim: identity falls out of trajectory agreement alone."""
    run = _leader_follower_decoy()

    assignments = associate_tracks(run, cfg)

    assert sorted(assignments.keys()) == ["A::T001"]
    a = assignments["A::T001"]
    assert a.assigned_participant == "B"
    assert a.status == STATUS_RESOLVED
    assert a.confidence >= float(cfg.get("fusion.track_association.min_confidence"))
    assert a.confidence > 0.9
    assert a.rmse_m is not None and a.rmse_m < 0.5
    assert a.overlap_s == pytest.approx((N - 1) * DT, abs=1e-6)

    # The decoy was scored, considered, and beaten -- not simply absent.
    scored = {c.participant_id: c for c in a.candidates}
    assert set(scored) == {"B", "C"}
    assert scored["B"].cost < scored["C"].cost
    assert a.runner_up == "C"
    assert a.runner_up_margin is not None and a.runner_up_margin > float(
        cfg.get("fusion.track_association.ambiguity_margin")
    )

    # Position is what separated them: both drive the same direction at the same
    # speed, so the heading and velocity channels agree for either hypothesis.
    assert scored["B"].heading_consistency > 0.95
    assert scored["C"].heading_consistency > 0.95
    assert scored["B"].rmse_m < 1.0 < scored["C"].rmse_m


def test_association_uses_no_privileged_identifier(cfg):
    """The evidence and the report must be free of any actor-identity field."""
    run = _leader_follower_decoy()
    report = to_jsonable(association_report(associate_tracks(run, cfg), run, cfg))

    keys: List[str] = []
    _keys(report, keys)
    for key in keys:
        assert key not in FORBIDDEN_LOCAL_FIELD_NAMES, key
        lowered = key.lower()
        for bad in FORBIDDEN_LOCAL_FIELD_SUBSTRINGS:
            assert bad not in lowered, key

    # The same holds for the inputs: a track sample has nowhere to put an id.
    sample_keys: List[str] = []
    _keys(to_jsonable(run.get("A").tracks[0]), sample_keys)
    assert "track_id" in sample_keys
    for key in sample_keys:
        assert key not in FORBIDDEN_LOCAL_FIELD_NAMES, key

    assert report["counts"][STATUS_RESOLVED] == 1
    assert len(report["assignments"][0]["candidates"]) == 2


# ---------------------------------------------------------------------------
# Refusing to guess
# ---------------------------------------------------------------------------


def test_track_matching_nobody_stays_unresolved(cfg):
    """A track whose path fits no participant must name no participant."""
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    _track(a, "A::T009", lambda t: (20.0 + SPEED * t, 100.0))

    assignment = associate_tracks(_run(a, b), cfg)["A::T009"]

    assert assignment.assigned_participant is None
    assert assignment.status == STATUS_UNRESOLVED
    assert assignment.candidates == []
    assert "max_rmse_m" in assignment.reason


def test_too_short_an_overlap_is_not_enough_evidence(cfg):
    """Below ``min_overlap_s`` the comparison is refused outright."""
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    short = _times(n=8)  # 0.35 s < fusion.track_association.min_overlap_s
    _track(a, "A::T002", lambda t: (20.0 + SPEED * t, 0.0), times=short)

    assert (
        score_candidate(a, "A::T002", b, cfg) is None
    ), "a 0.35 s overlap must not produce a candidate"

    assignment = associate_tracks(_run(a, b), cfg)["A::T002"]
    assert assignment.status == STATUS_UNRESOLVED
    assert assignment.assigned_participant is None


def test_two_equally_good_explanations_are_ambiguous(cfg):
    """Interchangeable candidates must be reported as such, not resolved."""
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    c = _straight("C", y=1.0, x0=20.0)
    _track(a, "A::T001", lambda t: (20.0 + SPEED * t, 0.5))

    assignment = associate_tracks(_run(a, b, c), cfg)["A::T001"]

    assert assignment.status == STATUS_AMBIGUOUS
    assert assignment.assigned_participant in ("B", "C")
    assert assignment.runner_up in ("B", "C")
    assert assignment.runner_up != assignment.assigned_participant
    assert assignment.runner_up_margin is not None
    assert abs(assignment.runner_up_margin) < float(
        cfg.get("fusion.track_association.ambiguity_margin")
    )
    best = max(c.score for c in assignment.candidates)
    assert assignment.confidence < best, "an ambiguous verdict must cost confidence"
    assert "ambiguity_margin" in assignment.reason


def test_low_scoring_best_candidate_is_left_unresolved(cfg):
    """A match that is possible but weak must not be promoted to an identity."""
    strict = cfg.with_overrides(
        {"fusion": {"track_association": {"min_confidence": 0.95}}}
    )
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    _track(a, "A::T001", lambda t: (20.0 + SPEED * t, 3.0))

    assignment = associate_tracks(_run(a, b), strict)["A::T001"]

    assert assignment.status == STATUS_UNRESOLVED
    assert assignment.assigned_participant is None
    assert assignment.candidates, "the rejected hypothesis must still be reported"
    assert "min_confidence" in assignment.reason


# ---------------------------------------------------------------------------
# Global matching
# ---------------------------------------------------------------------------


def test_assignment_is_solved_globally_not_greedily(cfg):
    """One observer's tracks are distinct objects, so the matching is one-to-one.

    ``A::T101`` lies between the two lanes and fits ``B`` better than ``C`` does,
    but ``A::T102`` fits ``B`` almost perfectly and fits ``C`` not at all. The
    optimal joint assignment therefore hands ``B`` to ``A::T102`` and pushes
    ``A::T101`` onto ``C`` -- a greedy best-first matching would instead leave
    ``A::T102`` with nothing.
    """
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    c = _straight("C", y=7.0, x0=20.0)
    _track(a, "A::T101", lambda t: (20.0 + SPEED * t, 1.2))
    _track(a, "A::T102", lambda t: (20.0 + SPEED * t, 0.0))

    assignments = associate_tracks(_run(a, b, c), cfg)

    assert assignments["A::T102"].assigned_participant == "B"
    assert assignments["A::T101"].assigned_participant == "C"
    assert assignments["A::T101"].runner_up == "B"
    # The solver preferred a worse individual match to keep the matching feasible,
    # which must be visible as a non-positive margin and a downgraded status.
    assert assignments["A::T101"].runner_up_margin <= 0.0
    assert assignments["A::T101"].status == STATUS_AMBIGUOUS


def test_a_brief_perfect_coincidence_does_not_outrank_sustained_agreement(cfg):
    """Agreement *quality* alone must not be mistaken for agreement *evidence*.

    The cost is built from RMSE, velocity and heading -- all measures of how well
    two trajectories agree, none of them a measure of how long they were compared.
    A decoy that shares the road with the track for 1.2 s and then stops recording
    is scored on 1.2 s of exact agreement and reaches cost 0, hence score 1.0; the
    true match, followed for the whole run through a metre of radar bias, cannot
    beat that. Declaring the decoy RESOLVED *at confidence 1.0* would be the
    module's worst possible failure: a fabricated identity stated as certain.

    The decoy may still win the cost comparison -- that is what the specified
    formula says -- but the verdict must be AMBIGUOUS, must cost confidence, and
    must say that the winner rested on a fraction of the rival's evidence.
    """
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)  # the true match, observed for the full 5 s
    # C exists for only 1.2 s -- just over min_overlap_s -- and during that window
    # it sits exactly on A's (biased) estimate of the track.
    brief = _times(n=25, start=2.0)
    c = ParticipantEvidence(
        participant_id="C",
        telemetry=[
            TelemetrySample(
                t=t,
                frame=i,
                participant_id="C",
                x=20.0 + SPEED * t,
                y=2.0,
                z=0.0,
                yaw=0.0,
                vx=SPEED,
                vy=0.0,
                speed=SPEED,
            )
            for i, t in enumerate(brief)
        ],
    )
    # A's radar carries a 2 m lateral bias, so the true match is good, not exact.
    _track(a, "A::T001", lambda t: (20.0 + SPEED * t, 2.0))

    assignment = associate_tracks(_run(a, b, c), cfg)["A::T001"]

    by_pid = {cand.participant_id: cand for cand in assignment.candidates}
    assert by_pid["C"].overlap_s < by_pid["B"].overlap_s, "fixture precondition"
    assert by_pid["C"].cost < by_pid["B"].cost, (
        "fixture precondition: the brief decoy must win the specified cost formula"
    )

    assert assignment.status == STATUS_AMBIGUOUS, (
        "an identity resting on {0:.2f}s against a rival's {1:.2f}s was reported as "
        "{2}".format(by_pid["C"].overlap_s, by_pid["B"].overlap_s, assignment.status)
    )
    assert assignment.confidence < by_pid["C"].score
    assert assignment.confidence < 1.0
    assert "min_evidence_parity" in assignment.reason
    # Both hypotheses stay on the record so a reviewer can overturn the verdict.
    assert set(by_pid) == {"B", "C"}


def test_a_participant_cannot_observe_itself(cfg):
    """Self-association is a programming error and must fail loudly."""
    a = _straight("A", y=0.0, x0=0.0)
    _track(a, "A::T001", lambda t: (SPEED * t, 0.0))
    with pytest.raises(ValueError):
        score_candidate(a, "A::T001", a, cfg)


def test_velocity_channel_rejects_a_counter_moving_decoy(cfg):
    """Direction of travel is part of the evidence, not only position.

    ``D`` occupies almost the same stretch of road as the track but traverses it
    in the opposite direction; with the position gate widened enough to admit it,
    the heading channel must still mark it as the worse explanation.
    """
    lenient = cfg.with_overrides({"fusion": {"track_association": {"max_rmse_m": 60.0}}})
    a = _straight("A", y=0.0, x0=0.0)
    b = _straight("B", y=0.0, x0=20.0)
    d = ParticipantEvidence(
        participant_id="D",
        telemetry=[
            TelemetrySample(
                t=t,
                frame=i,
                participant_id="D",
                x=70.0 - SPEED * t,
                y=0.5,
                z=0.0,
                yaw=180.0,
                vx=-SPEED,
                vy=0.0,
                speed=SPEED,
            )
            for i, t in enumerate(_times())
        ],
    )
    _track(a, "A::T001", lambda t: (20.0 + SPEED * t, 0.0))

    good = score_candidate(a, "A::T001", b, lenient)
    bad = score_candidate(a, "A::T001", d, lenient)

    assert good is not None and bad is not None
    assert good.heading_consistency > 0.95
    assert bad.heading_consistency < 0.05
    assert good.cost < bad.cost
    assert bad.velocity_rmse is not None and bad.velocity_rmse > 15.0
