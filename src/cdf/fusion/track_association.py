"""Identity resolution: which participant is this anonymous radar track?

This module is the scientific core of the fusion layer. Each participant exports
radar tracks labelled with *locally generated* ids such as ``"A::T007"``; those
labels carry no identity information whatsoever (see
:func:`cdf.common.schemas.make_track_id`). Nothing in the exported evidence says
who the reflecting object was -- the simulator's actor ids are never recorded.

The association argument
------------------------
A radar track has, at every sample, a *global-frame position estimate* obtained
by composing the observer's own localisation with its own sensor measurement
(:func:`cdf.common.geometry.radar_detection_to_global`). Every participant also
exports its *own* localisation trace. If observer ``A``'s track ``A::T007`` is in
fact participant ``B``, then the track's trajectory and ``B``'s self-reported
trajectory are two independent estimates of the same physical path and must
coincide to within sensor and localisation error. This module turns that
statement into a cost, and resolves the resulting one-to-one matching problem per
observer with the Hungarian algorithm.

Three quantities enter the cost, because position alone is ambiguous when
vehicles travel in a platoon at similar offsets:

* **position** -- RMSE between the track trajectory and the candidate's own
  trajectory on their common time grid;
* **velocity** -- RMSE between the observer's estimate of the target's global
  velocity and the candidate's own reported velocity;
* **heading** -- cosine similarity of the two motion directions, which separates
  an oncoming vehicle from a leading one even when the paths nearly coincide.

Epistemic discipline
--------------------
``UNRESOLVED`` is a first-class, required outcome. When the evidence does not
single out a participant the assignment reports no participant at all, and when
the second-best candidate is nearly as good the assignment is ``AMBIGUOUS`` with
a reduced confidence and an explicit reason. Guessing would manufacture exactly
the kind of unsupported identity claim this project exists to avoid.

Nothing in this module reads a CARLA actor id, map topology, traffic-light state
or any oracle artifact: the only inputs are exported local logs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.geometry import resample_trajectory, trajectory_rmse
from ..common.schemas import SCHEMA_VERSIONS, to_jsonable
from ..common.timeline import Interval, TimeGrid

__all__ = [
    "STATUS_RESOLVED",
    "STATUS_AMBIGUOUS",
    "STATUS_UNRESOLVED",
    "AssociationCandidate",
    "TrackAssignment",
    "score_candidate",
    "associate_tracks",
    "association_report",
]


#: Assignment verdicts. ``UNRESOLVED`` is not a failure mode, it is an answer.
STATUS_RESOLVED = "RESOLVED"
STATUS_AMBIGUOUS = "AMBIGUOUS"
STATUS_UNRESOLVED = "UNRESOLVED"

#: Cost used for (track, participant) pairs that produced no candidate at all.
#: It must be finite so that :func:`scipy.optimize.linear_sum_assignment` stays
#: feasible on rectangular problems; pairs that end up matched at this cost are
#: filtered out afterwards.
_INFEASIBLE_COST = 1.0e6


# ---------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------


@dataclass
class AssociationCandidate:
    """One scored hypothesis: ``observer_id``'s ``track_id`` *is* ``participant_id``.

    Every field is kept (not just the winning cost) so that the association can be
    audited after the fact: a reviewer can see how close the runner-up was and on
    which of the three evidence channels the decision rested.
    """

    track_id: str
    observer_id: str
    participant_id: str

    overlap_s: float
    """Duration of the common time support of track and candidate trajectory."""
    n_samples: int
    """Number of grid samples on which the comparison was actually evaluated."""

    rmse_m: Optional[float] = None
    """Planar trajectory RMSE in metres, ``None`` when it could not be computed."""
    velocity_rmse: Optional[float] = None
    """RMSE between the two global velocity estimates, m/s."""
    heading_consistency: float = 0.5
    """Motion-direction agreement mapped to ``[0, 1]``; ``0.5`` means no evidence."""

    cost: float = _INFEASIBLE_COST
    score: float = 0.0
    """``1 / (1 + cost)``: a bounded, monotone decreasing transform of the cost."""


@dataclass
class TrackAssignment:
    """The verdict for one local track of one observer."""

    track_id: str
    observer_id: str

    assigned_participant: Optional[str] = None
    """``None`` means UNRESOLVED: the evidence did not identify a participant."""
    confidence: float = 0.0
    status: str = STATUS_UNRESOLVED

    rmse_m: Optional[float] = None
    overlap_s: float = 0.0

    runner_up: Optional[str] = None
    runner_up_margin: Optional[float] = None
    """``score(best) - score(runner_up)``; small means the two are interchangeable."""

    candidates: List[AssociationCandidate] = field(default_factory=list)
    reason: str = ""

    @property
    def is_resolved(self) -> bool:
        """Whether a participant was named (RESOLVED or AMBIGUOUS)."""
        return self.assigned_participant is not None


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_candidate(
    observer_ev: ParticipantEvidence,
    track_id: str,
    other_ev: ParticipantEvidence,
    cfg: Config,
) -> Optional[AssociationCandidate]:
    """Score the hypothesis that ``track_id`` observed by ``observer_ev`` is ``other_ev``.

    Returns ``None`` when the hypothesis is *rejected outright* -- too little
    temporal overlap, no comparable samples, or a trajectory RMSE beyond
    ``fusion.track_association.max_rmse_m``. A rejected hypothesis is not a
    high-cost hypothesis: it is removed from the matching problem entirely, which
    is what lets the Hungarian solver leave a track unassigned rather than
    forcing it onto the least-bad participant.
    """
    if observer_ev.participant_id == other_ev.participant_id:
        raise ValueError(
            "a participant cannot observe itself: track {0!r} belongs to {1!r}".format(
                track_id, observer_ev.participant_id
            )
        )

    min_overlap_s = float(cfg.get("fusion.track_association.min_overlap_s", 1.0))
    max_rmse_m = float(cfg.get("fusion.track_association.max_rmse_m", 6.0))
    w_pos = float(cfg.get("fusion.track_association.position_weight", 0.50))
    w_vel = float(cfg.get("fusion.track_association.velocity_weight", 0.35))
    w_head = float(cfg.get("fusion.track_association.heading_weight", 0.15))
    grid_dt = float(cfg.get("fusion.time_alignment.grid_dt", 0.05))
    # Neither key exists in configs/default.yaml; both are reported as contract
    # issues. They only normalise already-bounded quantities.
    max_vel_rmse = float(cfg.get("fusion.track_association.max_velocity_rmse_mps", 10.0))
    min_speed_for_heading = float(
        cfg.get("fusion.track_association.min_speed_for_heading_mps", 0.5)
    )

    track_span = observer_ev.track_span(track_id)
    other_span = other_ev.span()
    if track_span is None or other_span is None:
        return None

    common = Interval(*track_span).intersection(Interval(*other_span))
    if common is None or common.duration < min_overlap_s:
        return None

    grid = TimeGrid(t0=common.start, t1=common.end, dt=grid_dt).times()
    if len(grid) < 2:
        return None

    t_trk, gx, gy = observer_ev.track_trajectory(track_id)
    t_oth, ox, oy = other_ev.self_trajectory()
    trk_x, trk_y, trk_valid = resample_trajectory(t_trk, gx, gy, grid)
    oth_x, oth_y, oth_valid = resample_trajectory(t_oth, ox, oy, grid)

    n_samples = int(np.count_nonzero(trk_valid & oth_valid))
    if n_samples < 2:
        return None

    rmse = trajectory_rmse(trk_x, trk_y, oth_x, oth_y)
    if rmse is None or rmse > max_rmse_m:
        return None

    samples = _track_samples(observer_ev, track_id)
    trk_vx, trk_vy = _velocity_on_grid(
        [float(s.t) for s in samples],
        [float(s.gvx) for s in samples],
        [float(s.gvy) for s in samples],
        grid,
        trk_x,
        trk_y,
    )
    oth_vx, oth_vy = _velocity_on_grid(
        [float(s.t) for s in other_ev.telemetry],
        [float(s.vx) for s in other_ev.telemetry],
        [float(s.vy) for s in other_ev.telemetry],
        grid,
        oth_x,
        oth_y,
    )

    velocity_rmse = trajectory_rmse(trk_vx, trk_vy, oth_vx, oth_vy)
    heading = _heading_consistency(
        trk_vx, trk_vy, oth_vx, oth_vy, min_speed_for_heading
    )

    norm_rmse = _clamp01(float(rmse) / max_rmse_m) if max_rmse_m > 0.0 else 1.0
    if velocity_rmse is None:
        # No velocity evidence: fall back to the neutral middle of the range
        # rather than rewarding or punishing the candidate for missing data.
        norm_vel = 0.5
    else:
        norm_vel = _clamp01(float(velocity_rmse) / max_vel_rmse) if max_vel_rmse > 0.0 else 1.0

    cost = w_pos * norm_rmse + w_vel * norm_vel + w_head * (1.0 - heading)
    return AssociationCandidate(
        track_id=track_id,
        observer_id=observer_ev.participant_id,
        participant_id=other_ev.participant_id,
        overlap_s=float(common.duration),
        n_samples=n_samples,
        rmse_m=float(rmse),
        velocity_rmse=None if velocity_rmse is None else float(velocity_rmse),
        heading_consistency=float(heading),
        cost=float(cost),
        score=float(1.0 / (1.0 + cost)),
    )


def _track_samples(ev: ParticipantEvidence, track_id: str) -> List[Any]:
    """Samples of one track, time-ordered (small helper kept for readability)."""
    return sorted(
        (s for s in ev.tracks if s.track_id == track_id), key=lambda s: float(s.t)
    )


def _velocity_on_grid(
    times: Sequence[float],
    vxs: Sequence[float],
    vys: Sequence[float],
    grid: Sequence[float],
    fallback_x: np.ndarray,
    fallback_y: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Velocity samples on ``grid``, differentiating positions when needed.

    Some recorders emit a velocity field that is identically zero (for instance a
    tracker that only smooths position). Silently comparing two zero vectors would
    make every candidate look equally good on the velocity channel, so the
    position series is differentiated instead -- which is legitimate, being a
    function of the very same local evidence.
    """
    vx, vy, _valid = resample_trajectory(times, vxs, vys, grid)
    finite = np.isfinite(vx) & np.isfinite(vy)
    if np.any(finite) and float(np.nanmax(np.hypot(vx[finite], vy[finite]))) > 1e-6:
        return vx, vy
    return _finite_difference(np.asarray(grid, dtype=float), fallback_x, fallback_y)


def _finite_difference(
    t: np.ndarray, x: np.ndarray, y: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Central-difference derivative of a resampled planar trajectory."""
    if t.size < 2:
        return np.full(t.shape, np.nan), np.full(t.shape, np.nan)
    dt = float(t[1] - t[0])
    if dt <= 0.0:
        return np.full(t.shape, np.nan), np.full(t.shape, np.nan)
    return np.gradient(x, dt), np.gradient(y, dt)


def _heading_consistency(
    ax: np.ndarray,
    ay: np.ndarray,
    bx: np.ndarray,
    by: np.ndarray,
    min_speed: float,
) -> float:
    """Mean cosine similarity of two motion directions, mapped to ``[0, 1]``.

    Samples where either object is essentially stationary carry no directional
    information and are skipped; when no sample qualifies the result is ``0.5``,
    the neutral value, so that "no evidence" never masquerades as agreement.
    """
    n = min(ax.size, ay.size, bx.size, by.size)
    cosines: List[float] = []
    for i in range(n):
        a = (float(ax[i]), float(ay[i]))
        b = (float(bx[i]), float(by[i]))
        if not all(math.isfinite(v) for v in a + b):
            continue
        na = math.hypot(a[0], a[1])
        nb = math.hypot(b[0], b[1])
        if na < min_speed or nb < min_speed:
            continue
        cosines.append((a[0] * b[0] + a[1] * b[1]) / (na * nb))
    if not cosines:
        return 0.5
    mean_cos = sum(cosines) / float(len(cosines))
    return _clamp01(0.5 * (1.0 + mean_cos))


def _clamp01(value: float) -> float:
    """Clamp to ``[0, 1]``."""
    return max(0.0, min(1.0, float(value)))


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------


def associate_tracks(run: RunEvidence, cfg: Config) -> Dict[str, TrackAssignment]:
    """Resolve every participant's local tracks to participants, observer by observer.

    Each observer poses an independent assignment problem: its tracks are distinct
    physical objects, so at most one of them can be any given participant. That
    constraint is exactly a rectangular linear assignment problem and is solved
    optimally with :func:`scipy.optimize.linear_sum_assignment` rather than
    greedily, so that a locally attractive but globally wrong pairing cannot win.

    The returned mapping is keyed by track id (already globally unique because it
    embeds the observer, e.g. ``"A::T007"``).
    """
    min_confidence = float(cfg.get("fusion.track_association.min_confidence", 0.40))
    ambiguity_margin = float(cfg.get("fusion.track_association.ambiguity_margin", 0.12))
    # Not in configs/default.yaml -- reported as a contract issue. Controls how
    # much confidence an ambiguous assignment retains at zero margin.
    ambiguous_floor = float(
        cfg.get("fusion.track_association.ambiguous_confidence_factor", 0.5)
    )
    # Not in configs/default.yaml -- reported as a contract issue. The cost is a
    # pure *quality* score (RMSE, velocity, heading) with no term for the *amount*
    # of evidence, so a candidate that was only observable for a sliver of the
    # track's life can reach cost 0 -- and therefore score 1.0 -- simply by
    # coinciding with it briefly. This floor is the parity below which the winning
    # comparison is not commensurable with its rival's.
    min_evidence_parity = float(
        cfg.get("fusion.track_association.min_evidence_parity", 0.5)
    )

    assignments: Dict[str, TrackAssignment] = {}
    participant_ids = run.participant_ids

    for observer_id in participant_ids:
        observer_ev = run.get(observer_id)
        track_ids = observer_ev.track_ids()
        others = [pid for pid in participant_ids if pid != observer_id]

        by_track: Dict[str, List[AssociationCandidate]] = {}
        for track_id in track_ids:
            scored: List[AssociationCandidate] = []
            for other_id in others:
                cand = score_candidate(observer_ev, track_id, run.get(other_id), cfg)
                if cand is not None:
                    scored.append(cand)
            scored.sort(key=lambda c: (c.cost, c.participant_id))
            by_track[track_id] = scored

        matched = _solve_assignment(track_ids, others, by_track)

        for track_id in track_ids:
            scored = by_track[track_id]
            best_for_track = scored[0] if scored else None
            chosen = matched.get(track_id)

            if chosen is None:
                assignments[track_id] = TrackAssignment(
                    track_id=track_id,
                    observer_id=observer_id,
                    assigned_participant=None,
                    confidence=float(best_for_track.score) if best_for_track else 0.0,
                    status=STATUS_UNRESOLVED,
                    rmse_m=best_for_track.rmse_m if best_for_track else None,
                    overlap_s=float(best_for_track.overlap_s) if best_for_track else 0.0,
                    runner_up=None,
                    runner_up_margin=None,
                    candidates=list(scored),
                    reason=_unassigned_reason(scored, others, cfg),
                )
                continue

            alternatives = [c for c in scored if c.participant_id != chosen.participant_id]
            runner = max(alternatives, key=lambda c: c.score) if alternatives else None
            margin = None if runner is None else float(chosen.score - runner.score)

            if chosen.score < min_confidence:
                assignments[track_id] = TrackAssignment(
                    track_id=track_id,
                    observer_id=observer_id,
                    assigned_participant=None,
                    confidence=float(chosen.score),
                    status=STATUS_UNRESOLVED,
                    rmse_m=chosen.rmse_m,
                    overlap_s=float(chosen.overlap_s),
                    runner_up=None if runner is None else runner.participant_id,
                    runner_up_margin=margin,
                    candidates=list(scored),
                    reason=(
                        "best candidate {0} scored {1:.3f}, below "
                        "fusion.track_association.min_confidence={2:.3f}; "
                        "identity left unresolved".format(
                            chosen.participant_id, chosen.score, min_confidence
                        )
                    ),
                )
                continue

            parity, parity_rival = _evidence_parity(chosen, alternatives)
            thin_evidence = parity is not None and parity < min_evidence_parity

            if (margin is not None and margin < ambiguity_margin) or thin_evidence:
                margin_factor = (
                    1.0
                    if margin is None or margin >= ambiguity_margin
                    else (
                        max(0.0, margin) / ambiguity_margin if ambiguity_margin > 0 else 1.0
                    )
                )
                parity_factor = (
                    1.0
                    if not thin_evidence
                    else (parity / min_evidence_parity if min_evidence_parity > 0 else 1.0)
                )
                factor = min(margin_factor, parity_factor)
                shrunk = float(
                    chosen.score * (ambiguous_floor + (1.0 - ambiguous_floor) * factor)
                )
                if thin_evidence:
                    reason = (
                        "{0} was compared over only {1:.2f}s while {2} was observable "
                        "for {3:.2f}s: the winning comparison rests on {4:.0%} of the "
                        "evidence available for its closest rival, below "
                        "fusion.track_association.min_evidence_parity={5:.2f}. A short "
                        "coincidence is not the same evidence as sustained agreement, "
                        "so the identity is reported as a best guess, not as "
                        "established".format(
                            chosen.participant_id,
                            chosen.overlap_s,
                            parity_rival.participant_id if parity_rival else "-",
                            parity_rival.overlap_s if parity_rival else float("nan"),
                            parity,
                            min_evidence_parity,
                        )
                    )
                else:
                    reason = (
                        "{0} (score {1:.3f}) and {2} (score {3:.3f}) differ by "
                        "{4:.3f} < fusion.track_association.ambiguity_margin={5:.3f}"
                        "{6}; best guess reported with reduced confidence".format(
                            chosen.participant_id,
                            chosen.score,
                            runner.participant_id if runner else "-",
                            runner.score if runner else float("nan"),
                            margin,
                            ambiguity_margin,
                            (
                                " (a competing track of the same observer claimed the "
                                "better-matching participant)"
                                if margin is not None and margin < 0.0
                                else ""
                            ),
                        )
                    )
                assignments[track_id] = TrackAssignment(
                    track_id=track_id,
                    observer_id=observer_id,
                    assigned_participant=chosen.participant_id,
                    confidence=shrunk,
                    status=STATUS_AMBIGUOUS,
                    rmse_m=chosen.rmse_m,
                    overlap_s=float(chosen.overlap_s),
                    runner_up=runner.participant_id if runner else None,
                    runner_up_margin=margin,
                    candidates=list(scored),
                    reason=reason,
                )
                continue

            assignments[track_id] = TrackAssignment(
                track_id=track_id,
                observer_id=observer_id,
                assigned_participant=chosen.participant_id,
                confidence=float(chosen.score),
                status=STATUS_RESOLVED,
                rmse_m=chosen.rmse_m,
                overlap_s=float(chosen.overlap_s),
                runner_up=runner.participant_id if runner else None,
                runner_up_margin=margin,
                candidates=list(scored),
                reason=(
                    "trajectory RMSE {0:.3f}m over {1:.2f}s ({2} samples), "
                    "heading consistency {3:.3f}".format(
                        chosen.rmse_m if chosen.rmse_m is not None else float("nan"),
                        chosen.overlap_s,
                        chosen.n_samples,
                        chosen.heading_consistency,
                    )
                ),
            )

    return assignments


def _solve_assignment(
    track_ids: Sequence[str],
    others: Sequence[str],
    by_track: Mapping[str, Sequence[AssociationCandidate]],
) -> Dict[str, AssociationCandidate]:
    """Optimal one-to-one matching of one observer's tracks onto participants."""
    if not track_ids or not others:
        return {}

    cost = np.full((len(track_ids), len(others)), _INFEASIBLE_COST, dtype=float)
    lookup: Dict[Tuple[int, int], AssociationCandidate] = {}
    col_of = {pid: j for j, pid in enumerate(others)}
    for i, track_id in enumerate(track_ids):
        for cand in by_track[track_id]:
            j = col_of[cand.participant_id]
            cost[i, j] = cand.cost
            lookup[(i, j)] = cand

    rows, cols = linear_sum_assignment(cost)
    out: Dict[str, AssociationCandidate] = {}
    for i, j in zip(rows.tolist(), cols.tolist()):
        cand = lookup.get((int(i), int(j)))
        if cand is not None:
            out[track_ids[int(i)]] = cand
    return out


def _evidence_parity(
    chosen: AssociationCandidate, alternatives: Sequence[AssociationCandidate]
) -> Tuple[Optional[float], Optional[AssociationCandidate]]:
    """How much evidence the winner rests on, relative to its best-supported rival.

    The cost in :func:`score_candidate` measures only how *well* two trajectories
    agree, never over how much of the track's life they were compared. A decoy
    that shares the road with the track for a second and then disappears is
    therefore scored on a second of perfect agreement, and beats the true match
    measured over the whole run with a metre of radar bias. Reporting that as a
    resolved identity -- at confidence 1.0, since cost 0 gives score 1 -- would be
    exactly the unsupported claim this module exists to refuse.

    Returns ``(parity, rival)`` where ``parity`` is
    ``chosen.overlap_s / rival.overlap_s`` for the rival with the longest
    comparison window, or ``(None, None)`` when there is no rival to compare
    against (a lone candidate is judged on its own merits and on
    ``min_overlap_s``/``min_confidence`` alone).
    """
    if not alternatives:
        return None, None
    rival = max(alternatives, key=lambda c: (c.overlap_s, c.participant_id))
    if rival.overlap_s <= 0.0 or chosen.overlap_s >= rival.overlap_s:
        return None, None
    return float(chosen.overlap_s) / float(rival.overlap_s), rival


def _unassigned_reason(
    scored: Sequence[AssociationCandidate], others: Sequence[str], cfg: Config
) -> str:
    """Explain, in words a reviewer can check, why a track named no participant."""
    if not others:
        return "no other participant exported evidence for this run"
    if not scored:
        return (
            "no participant trajectory matched within "
            "fusion.track_association.max_rmse_m={0} over at least "
            "fusion.track_association.min_overlap_s={1}s".format(
                cfg.get("fusion.track_association.max_rmse_m", 6.0),
                cfg.get("fusion.track_association.min_overlap_s", 1.0),
            )
        )
    return (
        "every plausible participant was claimed by a better-matching track of "
        "the same observer; this track therefore names no participant"
    )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def association_report(
    assignments: Mapping[str, TrackAssignment], run: RunEvidence, cfg: Config
) -> Dict[str, Any]:
    """Build the serialisable association report written to ``fusion/``.

    Every candidate of every track is included, not just the winner: the point of
    the artifact is that a third party can re-derive the verdict, see the margin
    that separated the winner from the runner-up, and disagree with it.
    """
    thresholds = {
        "min_overlap_s": float(cfg.get("fusion.track_association.min_overlap_s", 1.0)),
        "max_rmse_m": float(cfg.get("fusion.track_association.max_rmse_m", 6.0)),
        "position_weight": float(cfg.get("fusion.track_association.position_weight", 0.50)),
        "velocity_weight": float(cfg.get("fusion.track_association.velocity_weight", 0.35)),
        "heading_weight": float(cfg.get("fusion.track_association.heading_weight", 0.15)),
        "min_confidence": float(cfg.get("fusion.track_association.min_confidence", 0.40)),
        "ambiguity_margin": float(cfg.get("fusion.track_association.ambiguity_margin", 0.12)),
        "min_evidence_parity": float(
            cfg.get("fusion.track_association.min_evidence_parity", 0.5)
        ),
        "max_velocity_rmse_mps": float(
            cfg.get("fusion.track_association.max_velocity_rmse_mps", 10.0)
        ),
        "min_speed_for_heading_mps": float(
            cfg.get("fusion.track_association.min_speed_for_heading_mps", 0.5)
        ),
    }

    by_status: Dict[str, int] = {
        STATUS_RESOLVED: 0,
        STATUS_AMBIGUOUS: 0,
        STATUS_UNRESOLVED: 0,
    }
    per_observer: Dict[str, Dict[str, Any]] = {}
    rows: List[Dict[str, Any]] = []

    for track_id in sorted(assignments.keys()):
        a = assignments[track_id]
        by_status[a.status] = by_status.get(a.status, 0) + 1
        obs = per_observer.setdefault(
            a.observer_id,
            {"n_tracks": 0, STATUS_RESOLVED: 0, STATUS_AMBIGUOUS: 0, STATUS_UNRESOLVED: 0},
        )
        obs["n_tracks"] += 1
        obs[a.status] = obs.get(a.status, 0) + 1
        rows.append(to_jsonable(a))

    return {
        "schema_version": SCHEMA_VERSIONS["association"],
        "run_id": run.run_id,
        "scenario_id": run.scenario_id,
        "participants": run.participant_ids,
        "config_hash": cfg.hash,
        "thresholds": thresholds,
        "counts": by_status,
        "per_observer": {k: per_observer[k] for k in sorted(per_observer.keys())},
        "assignments": rows,
    }
