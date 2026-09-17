"""Event-detection quality of the local and fused reconstructions.

EVALUATION LAYER -- reads both the inference side and the oracle side.

This module answers one question: *how much of what actually happened did each
onboard recorder find, and did merging the recorders find more?* It is a thin,
deliberately dumb wrapper around :func:`cdf.graph.metrics.event_metrics`, which
owns the tolerance-correct matcher. Keeping the counting in one place is what
makes the local/fused comparison honest -- the per-participant numbers, the
best-local number and the fused number all come out of the *same* matcher under
the *same* tolerance, so a delta cannot be an artifact of three slightly
different comparison procedures.

Two conventions are worth stating, because both could be silently gamed:

*The baseline is the best single vehicle, never the average.* Averaging the
participants would let a vehicle that observed nothing (the lead car in a
rear-end, which has no radar track at all) drag the baseline down and flatter
fusion. The delta reported here is against the strongest single onboard
reconstruction.

*Nothing is written back.* This layer may read a local artifact, a fused artifact
and an oracle artifact in the same process, but it only ever returns data; the
suite persists it under ``evaluation/``.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import Event
from ..graph.metrics import event_metrics as _detection_metrics

__all__ = ["evaluate_events", "event_match_tolerance"]


def event_match_tolerance(cfg: Config) -> Tuple[float, bool]:
    """The single event-matching contract every block in this layer evaluates under.

    Returned as a pair so that no call site can read one of the two settings and
    forget the other, which would make two "identical" comparisons incomparable.
    """
    return (
        float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5)),
        bool(cfg.get("evaluation.event_match.require_same_type", True)),
    )


def _rank_key(metrics: Mapping[str, Any], participant_id: str) -> Tuple[float, float, str]:
    """Ordering used to pick the best single local event list.

    F1 first, recall as the tie-break (a forensic reconstruction that finds more
    of what happened is preferable to one that is merely conservative), then the
    participant id so the choice is reproducible.
    """
    return (-float(metrics["f1"]), -float(metrics["recall"]), str(participant_id))


def _strip(metrics: Mapping[str, Any]) -> Dict[str, Any]:
    """Scalar view of one metrics block, without the per-pair listings."""
    return {
        k: v
        for k, v in metrics.items()
        if k not in ("matches", "unmatched_pred", "unmatched_truth")
    }


def evaluate_events(
    local_events: Mapping[str, Sequence[Event]],
    fused_events: Sequence[Event],
    oracle_events: Sequence[Event],
    subject_map: Optional[Mapping[str, str]],
    cfg: Config,
) -> Dict[str, Any]:
    """Score every local event list and the fused one against the oracle's.

    Parameters
    ----------
    local_events:
        ``participant_id -> events`` as extracted by the local pipeline.
    fused_events:
        The merged event list produced by the fusion layer.
    oracle_events:
        The privileged reference. Empty input is an error rather than a score of
        zero: with no reference there is nothing to be right or wrong about, and
        silently returning zeros would publish a fabricated failure.
    subject_map:
        The fusion layer's ``track_id -> participant_id`` resolution, applied to
        the *predictions* so that an anonymous local track subject and the
        oracle's participant label can be compared. ``None`` leaves raw track ids
        in place, which is correct when fusion resolved nothing.
    cfg:
        Supplies ``evaluation.event_match.time_tolerance_s`` and
        ``evaluation.event_match.require_same_type``.

    Returns
    -------
    dict
        ``per_participant`` (full metrics incl. the matched pairs, so
        ``event_matches.csv`` can be written without re-running the matcher),
        ``best_local``, ``fused`` and the fused-minus-best-local deltas.
    """
    if not oracle_events:
        raise ValueError(
            "evaluate_events needs a non-empty oracle event list; with no reference "
            "the precision/recall of a reconstruction is undefined (the caller "
            "should report the block as unavailable instead)"
        )
    if not local_events:
        raise ValueError(
            "evaluate_events needs at least one participant's local events; got an "
            "empty mapping"
        )

    tolerance_s, require_same_type = event_match_tolerance(cfg)
    smap = dict(subject_map or {})

    per_participant: Dict[str, Dict[str, Any]] = {}
    for pid in sorted(local_events):
        per_participant[pid] = _detection_metrics(
            list(local_events[pid]),
            list(oracle_events),
            tolerance_s=tolerance_s,
            require_same_type=require_same_type,
            subject_map_pred=smap,
            subject_map_truth=None,
        )

    best_pid = sorted(per_participant, key=lambda p: _rank_key(per_participant[p], p))[0]
    best = per_participant[best_pid]

    fused: Optional[Dict[str, Any]] = None
    if fused_events:
        fused = _detection_metrics(
            list(fused_events),
            list(oracle_events),
            tolerance_s=tolerance_s,
            require_same_type=require_same_type,
            subject_map_pred=smap,
            subject_map_truth=None,
        )

    out: Dict[str, Any] = {
        "tolerance_s": tolerance_s,
        "require_same_type": require_same_type,
        "n_reference_events": len(oracle_events),
        "n_participants": len(per_participant),
        "per_participant": per_participant,
        "best_local_participant_id": best_pid,
        "best_local": _strip(best),
        "fused": _strip(fused) if fused is not None else None,
        "fused_detail": fused,
        "subject_map": dict(sorted(smap.items())),
    }
    if fused is None:
        out["fused_reason"] = "no fused event list was available for this run"
        out["delta_f1"] = None
        out["delta_recall"] = None
        out["delta_precision"] = None
        out["fusion_helped"] = None
    else:
        out["delta_f1"] = float(fused["f1"]) - float(best["f1"])
        out["delta_recall"] = float(fused["recall"]) - float(best["recall"])
        out["delta_precision"] = float(fused["precision"]) - float(best["precision"])
        # A strictly positive F1 delta is the only thing that counts as help; a
        # tie is reported as "no help" so that a null result cannot be dressed up.
        out["fusion_helped"] = bool(out["delta_f1"] > 0.0)
    return out
