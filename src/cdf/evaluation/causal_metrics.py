"""Scoring the reasoning, not just the graph.

Node and edge F1 say how much of the oracle's graph a reconstruction reproduced.
They do not say whether the reconstruction *explains the incident*, which is the
thing this project claims to do. A system can score well on edges and still be
unable to answer "why did these two cars collide, and whose behaviour led to
it?"; it can also reconstruct the mechanism correctly and lose edge precision for
describing it in richer terms than the template does.

This module measures the explanation directly, in four groups:

**Scene reconstruction** -- did the merged account put the vehicles in the right
places at the right times, and locate the impact? Measured in metres and seconds
against the privileged trace, on the *simulator* clock, so a good position at the
wrong time counts as the error it is.

**Causal chains** -- did the reconstruction recover the paths from a behaviour to
the collision? Paths are compared by their canonical semantic signature, because
the oracle writes ``ORACLE_SCRIPTED_INTERVENTION`` where a vehicle recorded
``HARD_BRAKE`` and those are the same fact. Ancestry recall asks the weaker,
robust question: of the behaviours the template says led to the impact, how many
end up anywhere in the reconstructed ancestry of it?

**Attribution** -- are the named contributors the ones the scenario designed?
Scored as a *set* of participants, with exact-set accuracy reported separately
from element-wise F1, because naming one of two contributors is a different
failure from naming a third who was not involved.

**Restraint** -- on a run designed not to collide, does the system invent a
culprit? A false attribution here is worse than a missed one, and it is reported
as its own number rather than averaged away.

Everything here is evaluation-only and may read privileged state; nothing in it
is ever written back into an inference artifact.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple

from ..common.config import Config
from ..common.evidence import RunEvidence
from ..common.schemas import EventType, GraphDocument
from ..graph.analysis import GraphAnalyzer
from ..graph.canonical import canonical_edge_family, canonical_node_family

__all__ = [
    "ATTRIBUTION_CLASS_ALIASES",
    "evaluate_scene_reconstruction",
    "evaluate_causal_paths",
    "evaluate_attribution_sets",
    "prf1",
]


#: Class names that mean the same verdict in the two vocabularies the project
#: grew: the single-action classifier's and the set classifier's.
ATTRIBUTION_CLASS_ALIASES: Dict[str, str] = {
    "single_cause": "single_initiator",
    "single_initiator": "single_initiator",
    "multiple_causes": "shared_contribution",
    "shared_contribution": "shared_contribution",
    "joint_contribution": "joint_contribution",
    "contributing_but_not_necessary": "contributing_but_not_necessary",
    "no_cause_identified": "insufficient_evidence",
    "insufficient_evidence": "insufficient_evidence",
}

_OUTCOME = EventType.COLLISION.value


def prf1(
    truth: Set[str], predicted: Set[str]
) -> Dict[str, Any]:
    """Precision, recall and F1 of a predicted set against a true set.

    An empty truth set with an empty prediction is a *correct* answer, not an
    undefined one: it is what a negative control should produce. It scores 1.0
    and is flagged, so an aggregate can choose to exclude it rather than have it
    silently inflate a mean.
    """
    tp = len(truth & predicted)
    fp = len(predicted - truth)
    fn = len(truth - predicted)
    if not truth and not predicted:
        return {
            "precision": 1.0, "recall": 1.0, "f1": 1.0,
            "tp": 0, "fp": 0, "fn": 0, "vacuous": True,
            "truth": [], "predicted": [],
        }
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": round(precision, 6),
        "recall": round(recall, 6),
        "f1": round(f1, 6),
        "tp": tp, "fp": fp, "fn": fn,
        "vacuous": False,
        "truth": sorted(truth),
        "predicted": sorted(predicted),
    }


# ---------------------------------------------------------------------------
# Scene reconstruction
# ---------------------------------------------------------------------------


def _true_poses(oracle_trace: Mapping[str, Any]) -> Dict[str, List[Tuple[float, float, float]]]:
    """``{participant: [(t, x, y), ...]}`` from the privileged trace."""
    out: Dict[str, List[Tuple[float, float, float]]] = {}
    for frame in oracle_trace.get("frames", []) or []:
        t = float(frame.get("t", 0.0))
        for actor in frame.get("actors", []) or []:
            pid = actor.get("participant_id")
            if pid is None or actor.get("x") is None or actor.get("y") is None:
                continue
            out.setdefault(str(pid), []).append((t, float(actor["x"]), float(actor["y"])))
    for series in out.values():
        series.sort(key=lambda row: row[0])
    return out


def _pose_at(
    series: Sequence[Tuple[float, float, float]], t: float, max_gap: float
) -> Optional[Tuple[float, float]]:
    """Linear interpolation of a pose series at ``t``, within ``max_gap``."""
    if not series:
        return None
    lo, hi = 0, len(series) - 1
    if t <= series[0][0]:
        return (series[0][1], series[0][2]) if series[0][0] - t <= max_gap else None
    if t >= series[hi][0]:
        return (series[hi][1], series[hi][2]) if t - series[hi][0] <= max_gap else None
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if series[mid][0] <= t:
            lo = mid
        else:
            hi = mid
    t0, x0, y0 = series[lo]
    t1, x1, y1 = series[hi]
    if t1 - t0 <= 0.0:
        return (x0, y0)
    w = (t - t0) / (t1 - t0)
    return (x0 + w * (x1 - x0), y0 + w * (y1 - y0))


def _reconstructed_collisions(
    fused: Optional[GraphDocument], participants: Sequence[str]
) -> List[Dict[str, Any]]:
    """Collision claims the fused graph makes, time-ordered."""
    if fused is None:
        return []
    known = {str(p) for p in participants}
    out: List[Dict[str, Any]] = []
    for node in fused.nodes:
        value = node.event_type.value if hasattr(node.event_type, "value") else str(
            node.event_type
        )
        if value != _OUTCOME:
            continue
        pair = {str(node.participant_id)}
        if node.subject and str(node.subject) in known:
            pair.add(str(node.subject))
        for owner in node.owners or []:
            if str(owner) in known:
                pair.add(str(owner))
        out.append(
            {
                "outcome_id": node.event_id,
                "t": float(node.t_peak),
                "pair": sorted(pair),
                "confidence": float(node.confidence),
            }
        )
    out.sort(key=lambda row: (row["t"], row["outcome_id"]))
    return out


def evaluate_scene_reconstruction(
    run: RunEvidence,
    fused: Optional[GraphDocument],
    oracle_trace: Optional[Mapping[str, Any]],
    participants: Sequence[str],
    cfg: Config,
    time_scoring_reason: Optional[str] = None,
    raw_run: Optional[RunEvidence] = None,
    alignment: Optional[Mapping[str, Any]] = None,
    clock_truth: Optional[Mapping[str, Any]] = None,
    subject_map: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    """How close the merged account is to the truth, in metres and seconds.

    Two different questions live here and they must not be conflated.

    *Self-localisation* compares each participant's own exported position to its
    true pose. In this simulator that difference is zero by construction -- no
    localisation noise is modelled -- so the number verifies that the recorder
    copies the pose faithfully and says nothing about reconstruction quality. It
    is reported, labelled as such, and kept out of the headline.

    *Cross-view reconstruction* is the real measurement: where does one vehicle's
    radar, resolved to an identity and placed on the estimated common clock, put
    another vehicle, compared with where that vehicle truly was? It folds radar
    error, identity resolution and clock error into one number, which is exactly
    what a merged multi-vehicle account rests on. It is computed from the *raw*
    recordings and the *estimated* alignment, so the clock error lands in the
    number instead of being divided out of it.

    ``run`` and ``fused`` are expected on the simulator clock, which for an
    independent-clock run is what the evaluation's privileged inversion produces.
    When that inversion was impossible the reason is recorded and nothing is
    scored, because comparing a recorder's own clock to simulator time would
    charge the clock offset as position error.
    """
    if oracle_trace is None:
        return {
            "scored": False,
            "reason": "the run carries no privileged trace",
        }
    if time_scoring_reason:
        return {"scored": False, "reason": time_scoring_reason}

    max_gap = float(cfg.get("evaluation.reconstruction.max_pose_gap_s", 0.10))
    truth = _true_poses(oracle_trace)
    per_participant: Dict[str, Any] = {}

    for pid in sorted(str(p) for p in participants):
        series = truth.get(pid) or []
        if pid not in run.participant_ids or not series:
            per_participant[pid] = {"scored": False, "n_samples": 0}
            continue
        ts, xs, ys = run.get(pid).self_trajectory()
        errors: List[float] = []
        for t, x, y in zip(ts, xs, ys):
            pose = _pose_at(series, float(t), max_gap)
            if pose is None:
                continue
            errors.append(math.hypot(float(x) - pose[0], float(y) - pose[1]))
        if not errors:
            per_participant[pid] = {"scored": False, "n_samples": 0}
            continue
        per_participant[pid] = {
            "scored": True,
            "n_samples": len(errors),
            "rmse_m": round(math.sqrt(sum(e * e for e in errors) / len(errors)), 6),
            "mean_error_m": round(sum(errors) / len(errors), 6),
            "max_error_m": round(max(errors), 6),
        }

    cross_view = _cross_view_reconstruction(
        raw_run if raw_run is not None else run,
        truth,
        alignment or {},
        clock_truth or {},
        subject_map or {},
        max_gap,
    )

    # -- the impact ------------------------------------------------------
    true_pairs = [
        {"pair": sorted([str(p["a"]), str(p["b"])]), "t": float(p["t"])}
        for p in (oracle_trace.get("collision_pairs") or [])
    ]
    true_pairs.sort(key=lambda row: row["t"])
    claimed = _reconstructed_collisions(fused, participants)

    matched: List[Dict[str, Any]] = []
    used: Set[int] = set()
    for truth_row in true_pairs:
        best: Optional[Tuple[float, int]] = None
        for index, claim in enumerate(claimed):
            if index in used or claim["pair"] != truth_row["pair"]:
                continue
            gap = abs(claim["t"] - truth_row["t"])
            if best is None or gap < best[0]:
                best = (gap, index)
        if best is None:
            matched.append({"pair": truth_row["pair"], "t_true": round(truth_row["t"], 6),
                            "matched": False})
            continue
        used.add(best[1])
        claim = claimed[best[1]]
        row: Dict[str, Any] = {
            "pair": truth_row["pair"],
            "matched": True,
            "outcome_id": claim["outcome_id"],
            "t_true": round(truth_row["t"], 6),
            "t_reconstructed": round(claim["t"], 6),
            "time_error_s": round(abs(claim["t"] - truth_row["t"]), 6),
        }
        true_point = _midpoint(truth, truth_row["pair"], truth_row["t"], max_gap)
        recon_point = _midpoint_from_run(run, truth_row["pair"], claim["t"], max_gap)
        if true_point is not None and recon_point is not None:
            row["location_error_m"] = round(
                math.hypot(recon_point[0] - true_point[0], recon_point[1] - true_point[1]), 6
            )
        matched.append(row)

    spurious = [claimed[i] for i in range(len(claimed)) if i not in used]
    time_errors = [r["time_error_s"] for r in matched if r.get("matched")]
    location_errors = [
        r["location_error_m"] for r in matched if r.get("location_error_m") is not None
    ]

    ordering: Optional[bool] = None
    if len(true_pairs) >= 2:
        true_order = [r["pair"] for r in true_pairs]
        claim_order = [c["pair"] for c in claimed if c["pair"] in true_order]
        seen: List[List[str]] = []
        for pair in claim_order:
            if pair not in seen:
                seen.append(pair)
        ordering = seen == true_order

    return {
        "scored": True,
        "self_localisation": {
            "per_participant": per_participant,
            "note": (
                "zero by construction: this simulator models no localisation "
                "noise, so this verifies the recorder rather than the "
                "reconstruction and is not the headline trajectory error"
            ),
        },
        "cross_view": cross_view,
        "trajectory_rmse_m": cross_view.get("rmse_m"),
        "trajectory_rmse_source": "cross_view",
        "n_true_collisions": len(true_pairs),
        "n_reconstructed_collisions": len(claimed),
        "collisions": matched,
        "n_matched_collisions": len(time_errors),
        "n_spurious_collisions": len(spurious),
        "spurious_collisions": spurious,
        "collision_pair_recall": (
            round(len(time_errors) / len(true_pairs), 6) if true_pairs else None
        ),
        "collision_time_error_s": (
            round(sum(time_errors) / len(time_errors), 6) if time_errors else None
        ),
        "collision_location_error_m": (
            round(sum(location_errors) / len(location_errors), 6)
            if location_errors else None
        ),
        "collision_order_correct": ordering,
        "note": (
            "the impact point is the midpoint of the pair, taken from their own "
            "exported localisation. Because that localisation is exact in this "
            "simulator, the location error here is the distance the vehicles "
            "travelled during the reconstruction's time error -- it measures the "
            "clock, not the sensors; cross_view.rmse_m measures the sensors"
        ),
    }


def _cross_view_reconstruction(
    raw_run: RunEvidence,
    truth: Mapping[str, Sequence[Tuple[float, float, float]]],
    alignment: Mapping[str, Any],
    clock_truth: Mapping[str, Any],
    subject_map: Mapping[str, str],
    max_gap: float,
) -> Dict[str, Any]:
    """Where one vehicle's radar puts another, against where it truly was.

    The chain deliberately mirrors what fusion itself does: a track sample sits
    on the observer's own clock, the *estimated* alignment moves it to the common
    clock, and only the last hop -- common time to physical time, through the
    reference recorder's true profile -- is privileged, because the common
    clock's zero is arbitrary and nothing else can anchor it. A recorder whose
    offset was estimated badly therefore shows up here as metres of error, which
    is the honest accounting.
    """
    reference = alignment.get("reference")
    offsets = alignment.get("offsets") or {}
    ref_profile = clock_truth.get(str(reference)) if reference else None
    if not offsets or ref_profile is None:
        return {
            "scored": False,
            "reason": (
                "cross-view scoring needs the estimated alignment and the "
                "reference recorder's true clock profile"
            ),
        }
    # common time -> simulator time, through the reference recorder alone.
    ref_a = 1.0 / float(ref_profile["true_scale"])
    ref_b = -float(ref_profile["true_offset_s"]) * ref_a

    per_pair: List[Dict[str, Any]] = []
    squared: List[float] = []
    unresolved = 0
    for observer in sorted(raw_run.participant_ids):
        block = offsets.get(observer) or {}
        if "scale" not in block:
            continue
        scale = float(block.get("scale", 1.0))
        offset = float(block.get("offset_s", 0.0))
        evidence = raw_run.get(observer)
        for track_id in evidence.track_ids():
            subject = subject_map.get("{0}::{1}".format(observer, track_id))
            if subject is None:
                subject = subject_map.get(track_id)
            if not subject or subject not in truth:
                unresolved += 1
                continue
            ts, gxs, gys = evidence.track_trajectory(track_id)
            errors: List[float] = []
            for t_local, gx, gy in zip(ts, gxs, gys):
                t_sim = ref_a * (scale * float(t_local) + offset) + ref_b
                pose = _pose_at(truth[subject], t_sim, max_gap)
                if pose is None:
                    continue
                errors.append(math.hypot(float(gx) - pose[0], float(gy) - pose[1]))
            if not errors:
                continue
            squared.extend(e * e for e in errors)
            per_pair.append(
                {
                    "observer": observer,
                    "track_id": track_id,
                    "resolved_to": subject,
                    "n_samples": len(errors),
                    "rmse_m": round(
                        math.sqrt(sum(e * e for e in errors) / len(errors)), 6
                    ),
                    "mean_error_m": round(sum(errors) / len(errors), 6),
                    "max_error_m": round(max(errors), 6),
                }
            )
    per_pair.sort(key=lambda row: (row["observer"], row["track_id"]))
    return {
        "scored": bool(squared),
        "reason": None if squared else "no resolved track produced a comparable sample",
        "rmse_m": (
            round(math.sqrt(sum(squared) / len(squared)), 6) if squared else None
        ),
        "n_samples": len(squared),
        "n_scored_tracks": len(per_pair),
        "n_unresolved_tracks": unresolved,
        "per_track": per_pair,
        "note": (
            "radar-derived position of another vehicle, placed on the estimated "
            "common clock; includes radar error, identity resolution and clock "
            "alignment error together"
        ),
    }


def _midpoint(
    truth: Mapping[str, Sequence[Tuple[float, float, float]]],
    pair: Sequence[str],
    t: float,
    max_gap: float,
) -> Optional[Tuple[float, float]]:
    points = [_pose_at(truth.get(pid) or [], t, max_gap) for pid in pair]
    if any(p is None for p in points) or not points:
        return None
    return (
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
    )


def _midpoint_from_run(
    run: RunEvidence, pair: Sequence[str], t: float, max_gap: float
) -> Optional[Tuple[float, float]]:
    """The pair's midpoint at ``t`` from their own exported trajectories.

    Interpolated rather than snapped to the nearest sample: the reconstruction
    can be a few milliseconds out on a 0.05 s grid, and snapping would silently
    round that error to zero instead of reporting the centimetres it is worth.
    """
    points: List[Tuple[float, float]] = []
    for pid in pair:
        if pid not in run.participant_ids:
            return None
        ts, xs, ys = run.get(pid).self_trajectory()
        pose = _pose_at(list(zip(ts, xs, ys)), t, max_gap)
        if pose is None:
            return None
        points.append(pose)
    if not points:
        return None
    return (
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
    )


# ---------------------------------------------------------------------------
# Causal chains
# ---------------------------------------------------------------------------


def _signature(
    doc: GraphDocument, path: Sequence[str], nodes: Mapping[str, Any]
) -> Tuple[str, ...]:
    """Canonical semantic fingerprint of one path: families and relations.

    Node *identity* is deliberately not part of it. Two graphs written by
    different layers give the same fact different ids, and comparing ids would
    measure nothing but the id scheme.
    """
    edges = {(e.source, e.target): e for e in doc.edges}
    parts: List[str] = []
    for index, node_id in enumerate(path):
        node = nodes.get(node_id)
        if node is None:
            return tuple()
        parts.append(canonical_node_family(node))
        if index + 1 < len(path):
            edge = edges.get((node_id, path[index + 1]))
            if edge is None:
                return tuple()
            parts.append("-{0}->".format(canonical_edge_family(edge.edge_type)))
    return tuple(parts)


def _paths_to_collisions(
    doc: Optional[GraphDocument], cfg: Config, max_paths: int
) -> Tuple[List[Tuple[str, ...]], Set[str], int]:
    """``(path signatures, ancestor families, n_collisions)`` for one graph."""
    if doc is None:
        return [], set(), 0
    nodes = {n.event_id: n for n in doc.nodes}
    analyzer = GraphAnalyzer(doc, cfg)
    collisions = [
        n.event_id
        for n in doc.nodes
        if (n.event_type.value if hasattr(n.event_type, "value") else str(n.event_type))
        == _OUTCOME
    ]
    signatures: List[Tuple[str, ...]] = []
    families: Set[str] = set()
    for outcome_id in sorted(collisions):
        for node_id in analyzer.ancestors(outcome_id):
            node = nodes.get(node_id)
            if node is not None:
                families.add(canonical_node_family(node))
        for path in analyzer.causal_paths_to(outcome_id)[:max_paths]:
            signature = _signature(doc, path, nodes)
            if signature:
                signatures.append(signature)
    return signatures, families, len(collisions)


def evaluate_causal_paths(
    fused: Optional[GraphDocument],
    oracle_doc: Optional[GraphDocument],
    cfg: Config,
) -> Dict[str, Any]:
    """Did the reconstruction recover the chains that led to the collision?

    Two measures, deliberately: exact chain agreement, which is strict and
    brittle, and ancestry recall, which asks only whether each behaviour the
    template blames appears *somewhere* upstream of the impact. A system can be
    right about the mechanism and still phrase the chain differently, so both
    numbers are reported and neither is presented as the other.
    """
    if oracle_doc is None:
        return {"scored": False, "reason": "the run carries no oracle causal graph"}

    max_paths = int(cfg.get("evaluation.causal_paths.max_paths_per_outcome", 64))
    truth_paths, truth_families, n_true = _paths_to_collisions(oracle_doc, cfg, max_paths)
    pred_paths, pred_families, n_pred = _paths_to_collisions(fused, cfg, max_paths)

    truth_set = set(truth_paths)
    pred_set = set(pred_paths)
    path_score = prf1(
        {"|".join(s) for s in truth_set}, {"|".join(s) for s in pred_set}
    )
    ancestry = prf1(truth_families, pred_families)

    return {
        "scored": True,
        # "reference" is the oracle graph. Named for its role in the comparison
        # rather than its provenance, because these counts travel into the
        # viewer's evaluation panel and no key outside the privileged block may
        # be labelled as coming from the oracle.
        "scored_against": "oracle_causal_graph",
        "n_reference_collisions": n_true,
        "n_reconstructed_collisions": n_pred,
        "n_reference_paths": len(truth_set),
        "n_reconstructed_paths": len(pred_set),
        "path": {k: v for k, v in path_score.items() if k not in {"truth", "predicted"}},
        "ancestry": {
            "precision": ancestry["precision"],
            "recall": ancestry["recall"],
            "f1": ancestry["f1"],
            "missing_families": sorted(truth_families - pred_families),
            "extra_families": sorted(pred_families - truth_families),
        },
        "note": (
            "paths are compared by canonical family signature, not by node id: "
            "the oracle and the reconstruction name the same fact differently"
        ),
    }


# ---------------------------------------------------------------------------
# Attribution as a set of participants
# ---------------------------------------------------------------------------


def _truth_participants(initiators: Mapping[str, Any]) -> Set[str]:
    mapping = initiators.get("participant_of_action") or {}
    return {
        str(mapping[a])
        for a in initiators.get("action_ids") or []
        if mapping.get(a)
    }


def _predicted_participants(
    attribution: Optional[Mapping[str, Any]],
    initiators: Mapping[str, Any],
) -> Tuple[Set[str], List[str], str]:
    """``(participants, action_ids, source)`` the system actually named.

    The action-to-participant mapping is the scenario's, which is privileged and
    fine here: this is the evaluation translating a *claim the system already
    made* into comparable terms, not helping it make one.
    """
    if not attribution:
        return set(), [], "none"
    mapping = {
        str(k): str(v)
        for k, v in (initiators.get("participant_of_action") or {}).items()
        if v
    }
    classification = attribution.get("classification") or {}
    actions: List[str] = []
    source = "classification.necessary_actions"
    for key in ("necessary_actions", "sufficient_single_actions"):
        for action in classification.get(key) or []:
            if str(action) not in actions:
                actions.append(str(action))
    for entry in classification.get("minimal_prevention_sets") or []:
        for action in entry.get("actions") or []:
            if str(action) not in actions:
                actions.append(str(action))
        source = "classification.minimal_prevention_sets"
    if not actions:
        for row in attribution.get("contributions") or []:
            if row.get("is_cause") or row.get("necessary"):
                action = str(row.get("action_id") or "")
                if action and action not in actions:
                    actions.append(action)
                    source = "contributions"
    return ({mapping[a] for a in actions if a in mapping}, sorted(actions), source)


def evaluate_attribution_sets(
    attribution: Optional[Mapping[str, Any]],
    initiators: Mapping[str, Any],
    expect_collision: bool,
    graph_hypothesis: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Score the named contributors as a set, and score restraint separately.

    On a run designed not to collide there is nothing to attribute, and the only
    thing worth measuring is whether the system stayed silent. That is reported
    as ``false_attribution`` rather than folded into an F1, because a mean over
    runs would let a confident wrong answer on a negative control be cancelled
    out by a correct one elsewhere.
    """
    truth = _truth_participants(initiators) if expect_collision else set()
    predicted, actions, source = _predicted_participants(attribution, initiators)

    declared = None
    if attribution:
        declared = (attribution.get("classification") or {}).get("attribution_class")
    normalised = ATTRIBUTION_CLASS_ALIASES.get(str(declared), None) if declared else None

    acceptable = _acceptable_classes(truth, expect_collision)
    scores = prf1(truth, predicted)

    out: Dict[str, Any] = {
        "scored": attribution is not None,
        "expect_collision": bool(expect_collision),
        "truth_participants": sorted(truth),
        "truth_action_ids": sorted(initiators.get("action_ids") or []),
        "predicted_participants": sorted(predicted),
        "predicted_action_ids": actions,
        "predicted_source": source,
        "precision": scores["precision"],
        "recall": scores["recall"],
        "f1": scores["f1"],
        "vacuous": scores["vacuous"],
        "exact_set_match": bool(truth == predicted),
        "declared_class": declared,
        "normalised_class": normalised,
        "acceptable_classes": sorted(acceptable) if acceptable else None,
        "class_correct": (
            None if normalised is None or not acceptable
            else normalised in acceptable
        ),
        "insufficient_evidence": normalised == "insufficient_evidence",
    }
    if not expect_collision:
        out["false_attribution"] = bool(predicted)
        out["restraint_correct"] = not predicted
    if graph_hypothesis is not None:
        named = {
            str(c.get("participant_id"))
            for block in graph_hypothesis.get("collisions") or []
            for c in block.get("contributors") or []
            if c.get("participant_id")
        }
        graph_scores = prf1(truth, named)
        out["graph_only"] = {
            "predicted_participants": sorted(named),
            "precision": graph_scores["precision"],
            "recall": graph_scores["recall"],
            "f1": graph_scores["f1"],
            "exact_set_match": bool(truth == named),
            "note": (
                "named from the fused causal graph alone, before any replay; "
                "reported to show what reasoning contributes without the simulator"
            ),
        }
    return out


def _acceptable_classes(truth: Set[str], expect_collision: bool) -> Set[str]:
    """Which verdicts the scenario's own design admits as correct.

    The template says *which* behaviours caused the outcome. It does not say
    whether removing one alone would have been enough, and only the replay can
    settle that -- so a scenario with two declared contributors is answered
    correctly either by ``shared_contribution`` (each was independently enough)
    or by ``joint_contribution`` (neither was, both together were). Insisting on
    one of them would score the simulator's physics, not the method.
    """
    if not expect_collision:
        return {"insufficient_evidence"}
    if len(truth) == 1:
        return {"single_initiator"}
    if len(truth) >= 2:
        return {"shared_contribution", "joint_contribution"}
    return set()
