"""Scoring of track-to-participant identity resolution against ground truth.

EVALUATION LAYER -- reads both the inference side and the oracle side.

The fusion layer answers "which participant is this anonymous radar track?" from
trajectory evidence alone (see :mod:`cdf.fusion.track_association`). This module
grades that answer. It is the one place in the project where an inferred identity
and the simulator's true identity meet, and the ordering matters: the true
identity comes from :func:`cdf.oracle.evaluator.true_track_identity` and is looked
up **only after** the inference has been made and persisted, never during it.

Ground truth is not redefined here. Resolving a track to a vehicle is the oracle
layer's job precisely because it must not reuse the association layer's own
procedure -- a reference computed the same way would agree with the inference for
the wrong reasons. This module only *counts*.

Why a reject option changes the scoring
---------------------------------------
``UNRESOLVED`` is a legitimate verdict, not a failure, so this cannot be scored
as plain accuracy. A system that names a participant for every track is not
better than one that abstains when the evidence is thin -- it is merely louder,
and in a forensic setting a confident wrong identity is the most damaging
possible output. The scoring therefore separates the two error modes:

* **precision** -- of the identities the system *did* claim, how many were right.
  Abstentions never enter this number, so abstaining is never rewarded.
* **recall** -- of the tracks that really were another participant, how many were
  correctly named. Abstentions *do* enter this number when
  ``evaluation.association.count_unresolved_as_miss`` is set (the default), which
  is what stops abstention from being a free way to keep precision at 1.0.

A track the oracle cannot attribute to any participant (a reflection off a wall,
a track smeared across two objects) enters neither number. It is not an
opportunity to be right and it is not evidence of being wrong.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

import numpy as np

from ..common.config import Config
from ..common.evidence import RunEvidence
from ..common.geometry import resample_trajectory
from ..graph.metrics import prf1
from ..oracle.events import participant_series
from ..oracle.evaluator import true_track_identity as _oracle_true_track_identity

LOGGER = logging.getLogger(__name__)

__all__ = [
    "VERDICT_CORRECT",
    "VERDICT_INCORRECT",
    "VERDICT_UNRESOLVED",
    "VERDICT_NO_GROUND_TRUTH",
    "as_trace_mapping",
    "true_track_identities",
    "evaluate_association",
]

#: Per-track verdicts. ``NO_GROUND_TRUTH`` is kept distinct from ``INCORRECT``:
#: a track the oracle cannot attribute to any participant is not evidence that
#: the association layer was wrong.
VERDICT_CORRECT = "correct"
VERDICT_INCORRECT = "incorrect"
VERDICT_UNRESOLVED = "unresolved"
VERDICT_NO_GROUND_TRUTH = "no_ground_truth"


# ---------------------------------------------------------------------------
# Privileged trace access
# ---------------------------------------------------------------------------


def as_trace_mapping(trace: Any) -> Dict[str, Any]:
    """Normalise a privileged trace to the shape :mod:`cdf.oracle` expects.

    :func:`cdf.oracle.events.load_oracle_trace` returns
    ``{"frames": [...], "participants": [...], ...}``, but a caller (or a test)
    may legitimately hold only the raw rows of ``oracle_trace.jsonl.gz``. Both
    are accepted and converted here rather than at every call site, because
    reshaping ground truth by hand is where a privileged field gets dropped.
    """
    if trace is None:
        return {"frames": [], "participants": []}
    if isinstance(trace, Mapping):
        frames = list(trace.get("frames", []) or [])
        participants = [str(p) for p in (trace.get("participants", []) or [])]
        if not participants:
            participants = _participants_in(frames)
        out = dict(trace)
        out["frames"] = frames
        out["participants"] = participants
        return out
    if isinstance(trace, Sequence) and not isinstance(trace, (str, bytes)):
        frames = [f for f in trace if isinstance(f, Mapping)]
        return {"frames": frames, "participants": _participants_in(frames)}
    raise TypeError(
        "oracle trace must be the mapping from cdf.oracle.events.load_oracle_trace "
        "or a sequence of frames, got {0!r}".format(type(trace))
    )


def _participants_in(frames: Sequence[Mapping[str, Any]]) -> List[str]:
    seen: List[str] = []
    for frame in frames:
        for actor in frame.get("actors", []) or []:
            pid = str(actor.get("participant_id", ""))
            if pid and pid not in seen:
                seen.append(pid)
    return sorted(seen)


def _mean_distance_to(
    trace: Mapping[str, Any], participant_id: str, samples: Sequence[Any]
) -> Optional[float]:
    """Mean planar distance between a track's estimate and a true trajectory.

    Reported alongside the verdict as *diagnostic* evidence -- it is what makes a
    wrong identity readable ("the track sat 14 m from the vehicle it was assigned
    to") -- and is deliberately not what decides the verdict; that is the oracle's
    call.
    """
    rows = participant_series(dict(trace), participant_id)
    if not rows or not samples:
        return None
    ts = [float(r["t"]) for r in rows]
    xs = [float(r["x"]) for r in rows]
    ys = [float(r["y"]) for r in rows]
    qt = [float(getattr(s, "t", None) if not isinstance(s, Mapping) else s["t"]) for s in samples]
    gx = np.asarray(
        [float(getattr(s, "gx", 0.0) if not isinstance(s, Mapping) else s.get("gx", 0.0))
         for s in samples],
        dtype=float,
    )
    gy = np.asarray(
        [float(getattr(s, "gy", 0.0) if not isinstance(s, Mapping) else s.get("gy", 0.0))
         for s in samples],
        dtype=float,
    )
    rx, ry, valid = resample_trajectory(ts, xs, ys, qt)
    if not bool(np.any(valid)):
        return None
    d = np.sqrt((gx - rx) ** 2 + (gy - ry) ** 2)
    return float(np.nanmean(d[valid]))


# ---------------------------------------------------------------------------
# Ground-truth identity table
# ---------------------------------------------------------------------------


def true_track_identities(
    run: RunEvidence, trace: Any, cfg: Config
) -> Dict[str, Dict[str, Any]]:
    """Ground-truth identity of every local radar track in a run.

    PRIVILEGED. A thin loop over
    :func:`cdf.oracle.evaluator.true_track_identity` -- one call per track, with
    the observing participant excluded from the candidates by that function --
    plus the diagnostic mean distance used in the report. Returns
    ``track_id -> {"observer_id", "true_participant", "mean_distance_m",
    "n_samples"}`` with ``true_participant`` ``None`` when the oracle names
    nobody.
    """
    mapping = as_trace_mapping(trace)
    out: Dict[str, Dict[str, Any]] = {}
    for observer_id in run.participant_ids:
        by_track = run.get(observer_id).tracks_by_id()
        for track_id in sorted(by_track):
            samples = by_track[track_id]
            true_pid = _oracle_true_track_identity(mapping, observer_id, samples, cfg)
            out[track_id] = {
                "observer_id": observer_id,
                "true_participant": true_pid,
                "n_samples": len(samples),
                "mean_distance_m": (
                    _mean_distance_to(mapping, true_pid, samples)
                    if true_pid is not None
                    else None
                ),
            }
    return out


# ---------------------------------------------------------------------------
# Assignment normalisation
# ---------------------------------------------------------------------------

_ASSIGNMENT_FIELDS = (
    "track_id",
    "observer_id",
    "assigned_participant",
    "confidence",
    "status",
    "rmse_m",
    "overlap_s",
    "runner_up",
    "runner_up_margin",
    "reason",
)


def _as_row(item: Any, fallback_track_id: Optional[str] = None) -> Dict[str, Any]:
    """One assignment as a plain dict, whether it is a dataclass or JSON."""
    row: Dict[str, Any] = {}
    for name in _ASSIGNMENT_FIELDS:
        if isinstance(item, Mapping):
            row[name] = item.get(name)
        else:
            row[name] = getattr(item, name, None)
    if not row.get("track_id"):
        row["track_id"] = fallback_track_id
    if not row.get("track_id"):
        raise ValueError(
            "assignment record carries no track_id and none could be inferred: {0!r}".format(item)
        )
    row["confidence"] = float(row.get("confidence") or 0.0)
    row["overlap_s"] = float(row.get("overlap_s") or 0.0)
    return row


def _assignment_rows(assignments: Any) -> List[Dict[str, Any]]:
    """Normalise the accepted assignment containers to a list of dicts.

    Accepts the in-memory ``{track_id: TrackAssignment}`` of
    :func:`cdf.fusion.track_association.associate_tracks`, a bare sequence of
    those records, and the ``assignments`` list of a persisted
    ``fusion/association_report.json``.
    """
    if assignments is None:
        return []
    if isinstance(assignments, Mapping):
        rows = [_as_row(v, str(k)) for k, v in assignments.items()]
    elif isinstance(assignments, Sequence) and not isinstance(assignments, (str, bytes)):
        rows = [_as_row(v) for v in assignments]
    else:
        raise TypeError(
            "assignments must be a mapping or sequence of TrackAssignment records, "
            "got {0!r}".format(type(assignments))
        )
    rows.sort(key=lambda r: str(r["track_id"]))
    return rows


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def evaluate_association(
    assignments: Any, run: RunEvidence, trace: Any, cfg: Config
) -> Dict[str, Any]:
    """Score identity resolution against the oracle's true track identities.

    Parameters
    ----------
    assignments:
        The fusion layer's verdicts (see :func:`_assignment_rows` for the
        accepted shapes). These must already be final: this function is called
        after inference, never inside it.
    run:
        The run's local evidence, supplying the track samples the oracle resolves.
    trace:
        The privileged oracle trace, in either accepted shape.
    cfg:
        Supplies ``evaluation.association.count_unresolved_as_miss`` and, through
        the oracle, the identity-resolution thresholds.

    Returns
    -------
    dict
        Counts (``n_correct`` / ``n_incorrect`` / ``n_unresolved``), precision,
        recall, F1, mean assignment confidence, mean trajectory RMSE, and a
        per-track table carrying both the claimed and the true identity.
    """
    count_unresolved_as_miss = bool(
        cfg.get("evaluation.association.count_unresolved_as_miss", True)
    )
    rows = _assignment_rows(assignments)
    identity = true_track_identities(run, trace, cfg)

    table: List[Dict[str, Any]] = []
    n_correct = n_incorrect = n_unresolved = n_no_truth = 0
    confidences: List[float] = []
    rmses: List[float] = []

    for row in rows:
        track_id = str(row["track_id"])
        truth_entry = identity.get(track_id, {})
        true_pid = truth_entry.get("true_participant")
        assigned = row.get("assigned_participant")

        if true_pid is None:
            verdict = VERDICT_NO_GROUND_TRUTH
            n_no_truth += 1
        elif assigned is None:
            verdict = VERDICT_UNRESOLVED
            n_unresolved += 1
        elif str(assigned) == str(true_pid):
            verdict = VERDICT_CORRECT
            n_correct += 1
        else:
            verdict = VERDICT_INCORRECT
            n_incorrect += 1

        confidences.append(float(row.get("confidence") or 0.0))
        if row.get("rmse_m") is not None:
            rmses.append(float(row["rmse_m"]))

        table.append(
            {
                "track_id": track_id,
                "observer_id": row.get("observer_id") or truth_entry.get("observer_id"),
                "status": row.get("status"),
                "assigned_participant": assigned,
                "true_participant": true_pid,
                "verdict": verdict,
                "confidence": float(row.get("confidence") or 0.0),
                "rmse_m": row.get("rmse_m"),
                "overlap_s": float(row.get("overlap_s") or 0.0),
                "runner_up": row.get("runner_up"),
                "true_identity_distance_m": truth_entry.get("mean_distance_m"),
                "true_identity_n_samples": truth_entry.get("n_samples"),
                "assignment_reason": row.get("reason", ""),
            }
        )

    n_with_truth = n_correct + n_incorrect + n_unresolved
    fn = (n_incorrect + n_unresolved) if count_unresolved_as_miss else n_incorrect
    scores = prf1(n_correct, n_incorrect, fn)

    named_conf = [
        float(r["confidence"]) for r in table if r["verdict"] != VERDICT_UNRESOLVED
    ]
    unscored = sorted(set(identity) - {r["track_id"] for r in table})
    if unscored:
        # A track the fusion layer never reported on is not silently forgotten.
        LOGGER.info(
            "%d track(s) present in the evidence carry no association verdict: %s",
            len(unscored),
            ", ".join(unscored),
        )
    return {
        "n_tracks": len(rows),
        "n_correct": n_correct,
        "n_incorrect": n_incorrect,
        "n_unresolved": n_unresolved,
        "n_unscorable": n_no_truth,
        "n_scorable": n_with_truth,
        "precision": scores["precision"],
        "recall": scores["recall"],
        "f1": scores["f1"],
        "accuracy": (float(n_correct) / float(n_with_truth)) if n_with_truth else None,
        "mean_confidence": (
            float(sum(confidences) / len(confidences)) if confidences else None
        ),
        "mean_confidence_named_only": (
            float(sum(named_conf) / len(named_conf)) if named_conf else None
        ),
        "mean_rmse_m": float(sum(rmses) / len(rmses)) if rmses else None,
        "count_unresolved_as_miss": count_unresolved_as_miss,
        "n_tracks_without_verdict": len(unscored),
        "tracks_without_verdict": unscored,
        "tracks": table,
    }
