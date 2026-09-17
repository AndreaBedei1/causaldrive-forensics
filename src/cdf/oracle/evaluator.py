"""Ground-truth answers used to score an already-finished reconstruction.

PRIVILEGED LAYER -- EVALUATION ONLY.

Everything here answers a question the pipeline has *already* answered on its
own. :func:`true_track_identity` says which vehicle a radar track was really
looking at; the fusion layer had to work that out from trajectory evidence alone,
and comparing the two is the whole point. :func:`oracle_outcome` says what really
happened; the local layer had to decide that from an impulse reading and its own
speed.

The ordering matters and is a hard rule: these functions are called *after*
inference, never during it. Their outputs go into ``evaluation/``, never back
into a local or fused artifact. Nothing in :mod:`cdf.local`, :mod:`cdf.fusion`,
:mod:`cdf.graph` or :mod:`cdf.checking` may import this module, and the anti
leakage suite enforces that by scanning imports rather than trusting convention.
"""

from __future__ import annotations

import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from ..common.config import Config
from ..common.schemas import OutcomeClass
from .events import (
    load_oracle_trace,
    pair_kinematics,
    participant_series,
    pre_impact_row,
    pre_impact_state,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_NEAR_MISS_SEPARATION_M",
    "DEFAULT_TRACK_IDENTITY_GATE_M",
    "DEFAULT_TRACK_IDENTITY_VOTE_FRACTION",
    "true_track_identity",
    "oracle_outcome",
    "oracle_summary",
]


#: Fallbacks used only when a caller supplies no :class:`~cdf.common.config.Config`.
#: Each mirrors an existing calibrated threshold so that the oracle and the layer
#: it scores talk about the same scale:
#:
#: * the near-miss separation matches ``recorder.triggers.near_miss.min_range_m``,
#:   the distance at which the onboard trigger already considers a target
#:   "genuinely close";
#: * the track-identity gate matches ``fusion.track_association.max_rmse_m``, the
#:   trajectory error fusion is allowed to accept.
DEFAULT_NEAR_MISS_SEPARATION_M = 12.0
DEFAULT_TRACK_IDENTITY_GATE_M = 6.0
#: A track has to spend most of its life on one vehicle before the oracle will
#: name that vehicle. Below this the track was smeared across several objects and
#: the honest ground truth is "no single answer".
DEFAULT_TRACK_IDENTITY_VOTE_FRACTION = 0.5


# ---------------------------------------------------------------------------
# Small accessors shared by the public functions
# ---------------------------------------------------------------------------


def _field(sample: Any, name: str, default: Optional[float] = None) -> Optional[float]:
    """Read one field from a :class:`~cdf.common.schemas.TrackSample` or a dict.

    Track samples reach this module either as typed records (from
    :class:`~cdf.common.evidence.ParticipantEvidence`) or as the raw JSON rows a
    test or a script just read off disk. Accepting both keeps the scoring path
    usable without forcing a full evidence load.
    """
    if isinstance(sample, dict):
        value = sample.get(name, default)
    else:
        value = getattr(sample, name, default)
    return None if value is None else float(value)


def _near_miss_separation_m(cfg: Optional[Config]) -> float:
    if cfg is None:
        return DEFAULT_NEAR_MISS_SEPARATION_M
    return float(
        cfg.get(
            "oracle.near_miss.min_separation_m",
            cfg.get("recorder.triggers.near_miss.min_range_m", DEFAULT_NEAR_MISS_SEPARATION_M),
        )
    )


def _pairs(participants: Sequence[str]) -> List[Tuple[str, str]]:
    ordered = sorted(str(p) for p in participants)
    return [
        (ordered[i], ordered[j])
        for i in range(len(ordered))
        for j in range(i + 1, len(ordered))
    ]


def _pair_key(a: str, b: str) -> str:
    """Order-independent label of a participant pair, e.g. ``"A|B"``."""
    return "{0}|{1}".format(*sorted([str(a), str(b)]))


# ---------------------------------------------------------------------------
# Track identity
# ---------------------------------------------------------------------------


def true_track_identity(
    trace: Dict[str, Any],
    observer_id: str,
    track_samples: Sequence[Any],
    cfg: Optional[Config] = None,
) -> Optional[str]:
    """Which participant a radar track was really looking at.

    This is the ground-truth answer to the question
    :mod:`cdf.fusion.track_association` had to solve from trajectory evidence
    alone. It is deliberately a *different* method: a per-sample nearest-true
    position vote with a distance gate, rather than an RMSE-scored assignment
    over the whole track. A reference that reproduced the inference procedure
    would agree with it for the wrong reasons.

    Parameters
    ----------
    trace:
        The mapping from :func:`cdf.oracle.events.load_oracle_trace`.
    observer_id:
        The participant whose radar holds the track. Excluded from the
        candidates: a vehicle cannot track itself.
    track_samples:
        The track's samples, as :class:`~cdf.common.schemas.TrackSample` records
        or as raw dicts. Only ``t``, ``gx`` and ``gy`` are used -- the estimated
        global position, which is exactly what the tracker claims about the world.
    cfg:
        Optional threshold registry. Keys read:
        ``oracle.track_identity.max_distance_m`` (defaulting to
        ``fusion.track_association.max_rmse_m``) and
        ``oracle.track_identity.min_vote_fraction``.

    Returns
    -------
    str or None
        The participant id the track was really on, or ``None`` when no vehicle
        accounts for enough of the track's life. ``None`` is a real answer: a
        track born on clutter genuinely has no true identity, and calling it a
        miss rather than a wrong answer would misreport the association metrics.
    """
    gate_m = DEFAULT_TRACK_IDENTITY_GATE_M
    min_fraction = DEFAULT_TRACK_IDENTITY_VOTE_FRACTION
    if cfg is not None:
        gate_m = float(
            cfg.get(
                "oracle.track_identity.max_distance_m",
                cfg.get("fusion.track_association.max_rmse_m", DEFAULT_TRACK_IDENTITY_GATE_M),
            )
        )
        min_fraction = float(
            cfg.get(
                "oracle.track_identity.min_vote_fraction",
                DEFAULT_TRACK_IDENTITY_VOTE_FRACTION,
            )
        )
    if gate_m <= 0.0:
        raise ValueError(
            "oracle.track_identity.max_distance_m must be positive, got {0!r}".format(gate_m)
        )
    if not 0.0 < min_fraction <= 1.0:
        raise ValueError(
            "oracle.track_identity.min_vote_fraction must lie in (0, 1], got "
            "{0!r}".format(min_fraction)
        )

    candidates = [
        str(p) for p in (trace.get("participants", []) or []) if str(p) != str(observer_id)
    ]
    if not candidates or not track_samples:
        return None

    series: Dict[str, List[Dict[str, Any]]] = {
        pid: participant_series(trace, pid) for pid in candidates
    }
    series = {pid: rows for pid, rows in series.items() if rows}
    if not series:
        return None

    votes: Dict[str, int] = {pid: 0 for pid in series}
    sum_distance: Dict[str, float] = {pid: 0.0 for pid in series}
    n_usable = 0

    for sample in track_samples:
        t = _field(sample, "t")
        gx = _field(sample, "gx")
        gy = _field(sample, "gy")
        if t is None or gx is None or gy is None:
            continue
        n_usable += 1
        best_pid: Optional[str] = None
        best_d = float("inf")
        for pid in sorted(series):
            row = _nearest_row(series[pid], t)
            if row is None:
                continue
            d = math.hypot(float(row["x"]) - gx, float(row["y"]) - gy)
            if d < best_d:
                best_d = d
                best_pid = pid
        if best_pid is not None and best_d <= gate_m:
            votes[best_pid] += 1
            sum_distance[best_pid] += best_d

    if n_usable == 0:
        return None

    winner = max(
        sorted(votes),
        key=lambda pid: (
            votes[pid],
            -(sum_distance[pid] / votes[pid]) if votes[pid] else float("-inf"),
        ),
    )
    if votes[winner] < min_fraction * n_usable:
        LOGGER.info(
            "oracle: track held by %s matches %s on only %d of %d samples (< %.0f%%); "
            "no true identity assigned",
            observer_id,
            winner,
            votes[winner],
            n_usable,
            100.0 * min_fraction,
        )
        return None
    return winner


def _nearest_row(rows: Sequence[Dict[str, Any]], t: float) -> Optional[Dict[str, Any]]:
    """The privileged state sampled closest in time to ``t``."""
    if not rows:
        return None
    return min(rows, key=lambda r: (abs(float(r["t"]) - float(t)), float(r["t"])))


# ---------------------------------------------------------------------------
# Outcome
# ---------------------------------------------------------------------------


def oracle_outcome(trace: Dict[str, Any], cfg: Optional[Config] = None) -> Dict[str, Any]:
    """The true outcome of a run: what hit what, how hard, and how close.

    A collision anywhere makes the run a ``COLLISION``. Otherwise a pair that came
    within the near-miss separation makes it a ``NEAR_MISS``, and anything else is
    ``NO_EVENT``. This mirrors the ordering the simulation runner uses, but
    decides it from exact separations instead of from whichever onboard trigger
    happened to arm -- which is precisely the disagreement the evaluation is
    meant to surface.

    Returns
    -------
    dict
        ``outcome``, ``collision_pairs`` (with impact times, impulses and impact
        speeds), ``min_separation`` per pair, and the thresholds used.
    """
    participants = [str(p) for p in (trace.get("participants", []) or [])]
    near_miss_m = _near_miss_separation_m(cfg)
    if near_miss_m <= 0.0:
        raise ValueError(
            "oracle.near_miss.min_separation_m must be positive, got {0!r}".format(near_miss_m)
        )

    impacts: Dict[Tuple[str, str], Dict[str, Any]] = {}
    for record in trace.get("collisions", []) or []:
        other = record.get("other_participant_id")
        if other is None:
            continue
        a, b = sorted([str(record["participant_id"]), str(other)])
        t = float(record["t"])
        if (a, b) not in impacts or t < float(impacts[(a, b)]["t"]):
            impacts[(a, b)] = {
                "a": a,
                "b": b,
                "t": t,
                "frame": int(record.get("frame", 0)),
                "impulse": float(record.get("impulse", 0.0)),
            }

    min_separation: Dict[str, Dict[str, Any]] = {}
    collision_pairs: List[Dict[str, Any]] = []
    closest_overall: Optional[Tuple[float, str, float]] = None

    for (a, b) in _pairs(participants):
        states = pair_kinematics(trace, a, b)
        if not states:
            continue
        closest = min(states, key=lambda s: (s.distance, s.t))
        min_separation[_pair_key(a, b)] = {
            "t": closest.t,
            "distance_m": closest.distance,
            "relative_speed_mps": closest.closing_speed,
        }
        if closest_overall is None or closest.distance < closest_overall[0]:
            closest_overall = (closest.distance, _pair_key(a, b), closest.t)

        impact = impacts.get((a, b))
        if impact is None:
            continue
        # Read the impact kinematics from the last pre-contact sample; see
        # :func:`cdf.oracle.events.pre_impact_state` for why.
        at_impact = pre_impact_state(states, float(impact["t"]))
        speeds = _speeds_before(trace, [a, b], float(impact["t"]))
        collision_pairs.append(
            {
                "a": a,
                "b": b,
                "t": float(impact["t"]),
                "frame": impact["frame"],
                "impulse": impact["impulse"],
                "relative_speed_mps": 0.0 if at_impact is None else at_impact.closing_speed,
                "separation_m": 0.0 if at_impact is None else at_impact.distance,
                "speeds_mps": speeds,
            }
        )

    collision_pairs.sort(key=lambda c: (float(c["t"]), c["a"], c["b"]))

    if collision_pairs:
        outcome = OutcomeClass.COLLISION
    elif closest_overall is not None and closest_overall[0] <= near_miss_m:
        outcome = OutcomeClass.NEAR_MISS
    else:
        outcome = OutcomeClass.NO_EVENT

    return {
        "outcome": outcome.value,
        "participants": participants,
        "collision_pairs": collision_pairs,
        "collision_order": [[c["a"], c["b"]] for c in collision_pairs],
        "n_collision_records": len(trace.get("collisions", []) or []),
        "min_separation": min_separation,
        "closest_pair": None if closest_overall is None else closest_overall[1],
        "closest_separation_m": None if closest_overall is None else closest_overall[0],
        "thresholds": {"near_miss_min_separation_m": near_miss_m},
    }


def _speeds_before(
    trace: Dict[str, Any], participants: Sequence[str], t: float
) -> Dict[str, float]:
    """True speed of each participant at the last sample before ``t``."""
    out: Dict[str, float] = {}
    for pid in participants:
        row = pre_impact_row(participant_series(trace, pid), t)
        if row is not None:
            out[str(pid)] = float(row["speed"])
    return out


# ---------------------------------------------------------------------------
# Run-level summary
# ---------------------------------------------------------------------------


def oracle_summary(
    run_dir: Union[str, Path], cfg: Optional[Config] = None
) -> Dict[str, Any]:
    """Everything the oracle can say about one run, read straight from disk.

    A convenience wrapper for reports and for the evaluation layer: it loads the
    privileged trace, derives the true outcome and adds the per-participant
    kinematic extremes that a reader needs to judge whether the scenario did what
    it was designed to do.

    This function only *reads*. It writes nothing, and in particular it never
    touches a local or fused artifact -- the evaluation layer is allowed to look
    at both sides of the boundary precisely because it changes neither.
    """
    trace = load_oracle_trace(run_dir)
    summary = trace.get("summary", {}) or {}
    frames = trace.get("frames", []) or []

    participants: Dict[str, Any] = {}
    for pid in trace.get("participants", []) or []:
        rows = participant_series(trace, pid)
        if not rows:
            participants[str(pid)] = {"n_samples": 0}
            continue
        speeds = [float(r["speed"]) for r in rows]
        participants[str(pid)] = {
            "n_samples": len(rows),
            "t_first": float(rows[0]["t"]),
            "t_last": float(rows[-1]["t"]),
            "max_speed_mps": max(speeds),
            "final_speed_mps": speeds[-1],
            "distance_travelled_m": _path_length(rows),
        }

    return {
        "run_dir": trace.get("run_dir", str(run_dir)),
        "run_id": str(summary.get("run_id", "")),
        "scenario_id": str(summary.get("scenario_id", "")),
        "variant": str(summary.get("variant", "")),
        "seed": int(summary.get("seed", 0)),
        "map_name": str(summary.get("map_name", "")),
        "n_frames": len(frames),
        "t_span": [float(frames[0]["t"]), float(frames[-1]["t"])] if frames else None,
        "participants": participants,
        "outcome": oracle_outcome(trace, cfg),
        "interventions": summary.get("interventions", {}) or {},
        "notes": list(summary.get("notes", []) or []),
    }


def _path_length(rows: Sequence[Dict[str, Any]]) -> float:
    """Planar distance actually travelled along the recorded true trajectory."""
    total = 0.0
    for i in range(1, len(rows)):
        total += math.hypot(
            float(rows[i]["x"]) - float(rows[i - 1]["x"]),
            float(rows[i]["y"]) - float(rows[i - 1]["y"]),
        )
    return total
