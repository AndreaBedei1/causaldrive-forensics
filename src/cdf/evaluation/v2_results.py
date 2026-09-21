"""The V2 campaign blocks: clocks, perception, properties, responsibility, replays.

Everything here is aggregated from artifacts that already exist per run, so a
number in the final report can always be traced back to the run that produced
it. Nothing is recomputed from raw evidence and nothing is carried over from a
previous generation of the campaign.

Two rules run through all of it.

**Counts are summed, then divided once.** Averaging per-run ratios would let a
run that decided one property outweigh a run that decided eight, and a two-car
scenario outweigh a three-car one.

**An absence is reported as an absence.** A rate over no samples is ``None``,
never zero, and the sample count sits beside every rate so a reader can see what
it rests on. The stop-sign numbers in particular come from a handful of scenarios
and would be meaningless without their denominators.
"""

from __future__ import annotations

import logging
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from ..common.io import read_json
from ..common.layout import RunLayout
from .formal_metrics import aggregate_formal
from .responsibility_metrics import aggregate_responsibility

LOGGER = logging.getLogger(__name__)

__all__ = ["v2_blocks", "clock_block", "perception_block", "collision_order_block"]

PathLike = Union[str, Path]

#: Clock sources, in the order the hierarchy prefers them. ``ACQUISITION_START``
#: is not part of the fusion hierarchy: it is the harness marker used on runs
#: where nothing ever touched, and it is named separately so its recorders are
#: never counted as though a physical contact had placed them.
SOURCES: Tuple[str, ...] = (
    "REFERENCE", "CONTACT", "RADAR", "ACQUISITION_START", "UNRESOLVED",
)


def _maybe(path: Path) -> Optional[Dict[str, Any]]:
    try:
        return read_json(path) if path.exists() else None
    except Exception:  # pragma: no cover - a corrupt artifact is not a metric
        return None


def _rate(numerator: int, denominator: int) -> Optional[float]:
    return round(numerator / denominator, 4) if denominator else None


def _prf(matched: int, found: int, expected: int,
         reference: bool = True,
         no_reference_note: Optional[str] = None) -> Dict[str, Any]:
    """Precision and recall, or an honest statement that there is no reference.

    With ``reference=False`` nothing verified exists to score against. The
    detections are still reported, because how many there were is a fact; what
    cannot be said is whether they were right. Calling them false positives, or
    printing a precision of zero, would turn a missing reference into a measured
    failure. The stop-line detector is exactly this case: its reference is a
    position derived from the sign and the lane, and Town05 paints no bar there.
    """
    if not reference:
        return {
            "n_detected": found,
            "n_true_positive": None,
            "n_false_positive": None,
            "n_false_negative": None,
            "n_real": None,
            "precision": None,
            "recall": None,
            "f1": None,
            "reference": "unavailable",
            "note": no_reference_note or (
                "no reference exists for this quantity, so the detections are "
                "reported and not scored"
            ),
        }
    precision = _rate(matched, found)
    recall = _rate(matched, expected)
    f1 = None
    if precision and recall and (precision + recall) > 0:
        f1 = round(2 * precision * recall / (precision + recall), 4)
    return {
        "n_true_positive": matched,
        "n_false_positive": found - matched,
        "n_false_negative": expected - matched,
        "n_real": expected,
        "n_detected": found,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "reference": "verified",
    }


# --- clocks ---------------------------------------------------------------


def _true_offsets(layout: RunLayout) -> Dict[str, float]:
    """Each recorder's true offset, from the privileged record. Scoring only."""
    truth = _maybe(layout.oracle_dir / "clock_ground_truth.json")
    if not truth:
        return {}
    block = truth.get("participants") or truth.get("offsets") or truth
    if not isinstance(block, Mapping):
        return {}
    out: Dict[str, float] = {}
    for pid, value in block.items():
        if isinstance(value, Mapping):
            for key in ("offset_s", "true_offset_s", "offset"):
                if key in value:
                    out[str(pid)] = float(value[key])
                    break
        elif isinstance(value, (int, float)):
            out[str(pid)] = float(value)
    return out


def _true_scales(layout: RunLayout) -> Dict[str, float]:
    """Each recorder's true rate, from the privileged record. Scoring only."""
    truth = _maybe(layout.oracle_dir / "clock_ground_truth.json")
    block = (truth or {}).get("participants") or {}
    if not isinstance(block, Mapping):
        return {}
    out: Dict[str, float] = {}
    for pid, value in block.items():
        if isinstance(value, Mapping) and "true_scale" in value:
            out[str(pid)] = float(value["true_scale"])
    return out


def clock_block(run_dirs: Sequence[Path]) -> Dict[str, Any]:
    """How every recorder was placed on common time, and how far out it was.

    The error is relative to the reference, because that is the only thing an
    offset means: a common timeline is fixed up to a constant, and scoring the
    constant itself would measure the gauge rather than the alignment.
    """
    sources: Counter = Counter()
    statuses: Counter = Counter()
    errors: Dict[str, List[float]] = {s: [] for s in SOURCES}
    all_errors: List[float] = []
    # What fixing the scale to 1 leaves unmodelled. Not an estimator error: the
    # aligner never claims a rate, so this is the size of a deliberate
    # approximation, measured after the fact.
    drifts: List[float] = []
    longest_run_s = 0.0
    tick_s: Optional[float] = None
    unscored = 0
    n_participants = 0

    for run_dir in run_dirs:
        layout = RunLayout.from_run_dir(run_dir)
        alignment = _maybe(layout.clock_alignment)
        if not alignment:
            continue
        statuses[str(alignment.get("status", "?"))] += 1
        per_source = alignment.get("clock_sources") or {}
        offsets = alignment.get("offsets_s") or {}
        truth = _true_offsets(layout)
        reference = alignment.get("reference")
        base = truth.get(str(reference)) if reference else None

        scales = _true_scales(layout)
        ref_scale = scales.get(str(reference)) if reference else None
        manifest = _maybe(layout.manifest) or {}
        longest_run_s = max(longest_run_s, float(manifest.get("duration_sim_s") or 0.0))
        if tick_s is None and manifest.get("fixed_delta_seconds"):
            tick_s = float(manifest["fixed_delta_seconds"])

        # Runs aligned by the harness marker record no per-vehicle provenance.
        # Defaulting them to CONTACT would credit a physical impact that never
        # happened, and would fold each of their reference recorders, whose
        # error is zero by definition, into the contact average.
        marker = str(alignment.get("method", "")) == "acquisition_start_marker"
        fallback = "ACQUISITION_START" if marker else "CONTACT"

        for pid in sorted(set(per_source) | set(offsets)):
            n_participants += 1
            if pid in per_source:
                source = str(per_source[pid])
            elif pid == str(reference):
                source = "REFERENCE"
            elif pid in offsets:
                source = fallback
            else:
                source = "UNRESOLVED"
            sources[source] += 1
            got = offsets.get(pid)
            if got is None or base is None or pid not in truth:
                unscored += 1
                continue
            # t_common = t_local + offset, so the offset that would place this
            # recorder correctly is the negated difference of the true offsets.
            expected = -(truth[pid] - base)
            error = float(got) - expected
            errors.setdefault(source, []).append(error)
            all_errors.append(error)
            # The reference has no relative drift by definition; it is the
            # gauge. Counting its zero would dilute the control.
            if ref_scale and pid in scales and pid != str(reference):
                drifts.append(abs(scales[pid] / ref_scale - 1.0) * 1e6)

    def stats(values: Sequence[float]) -> Dict[str, Any]:
        if not values:
            return {"n": 0, "mae_s": None, "max_abs_s": None}
        absolute = [abs(v) for v in values]
        return {
            "n": len(values),
            "mae_s": round(sum(absolute) / len(absolute), 6),
            "max_abs_s": round(max(absolute), 6),
        }

    aligned = sum(sources[s] for s in ("REFERENCE", "CONTACT", "RADAR"))
    return {
        "n_runs": len(run_dirs),
        "n_participants": n_participants,
        "source_distribution": {s: sources.get(s, 0) for s in SOURCES},
        "run_status_distribution": dict(sorted(statuses.items())),
        "n_aligned": aligned,
        "n_unresolved": sources.get("UNRESOLVED", 0),
        "unresolved_rate": _rate(sources.get("UNRESOLVED", 0), n_participants),
        "offset_error": stats(all_errors),
        # The drift control. Reported so the size of the fixed-scale
        # approximation is on the record, never as an estimator score.
        "drift_estimated": False,
        "n_drift_scored": len(drifts),
        "unmodelled_drift_ppm": (
            round(sum(drifts) / len(drifts), 3) if drifts else None
        ),
        "unmodelled_drift_max_ppm": round(max(drifts), 3) if drifts else None,
        "unmodelled_drift_worst_s": (
            round(max(drifts) * 1e-6 * longest_run_s, 6)
            if drifts and longest_run_s else None
        ),
        "longest_run_s": round(longest_run_s, 3) if longest_run_s else None,
        "tick_s": tick_s,
        "drift_note": (
            "the aligner fits an offset and fixes scale to 1, so drift is not "
            "estimated. This is the true relative drift that choice leaves "
            "unmodelled, measured after the fact over the non-reference "
            "recorders; a reference has no relative drift by definition"
        ),
        "offset_error_by_source": {
            s: stats(errors.get(s, [])) for s in SOURCES
        },
        "n_participants_without_a_reference_offset": unscored,
        "note": (
            "error is relative to the run's reference recorder, because a common "
            "timeline is only fixed up to a constant. The source says how each "
            "recorder was placed: a physical contact, a fitted radar trajectory, "
            "or not at all"
        ),
    }


# --- perception -----------------------------------------------------------


def perception_block(run_dirs: Sequence[Path]) -> Dict[str, Any]:
    """What the cameras made of the signs and markings that were really there.

    Real campaign frames only. The synthetic detector tests are unit tests and
    are not perception results; mixing them would report the fixture's difficulty
    rather than the road's.
    """
    kinds = {"stop": [0, 0, 0], "yield": [0, 0, 0]}   # matched, detected, real
    markings = [0, 0, 0]
    stop_lines = [0, 0, 0]
    n_scored = 0
    latency_measurable = 0
    declared_not_placed: List[str] = []

    for run_dir in run_dirs:
        layout = RunLayout.from_run_dir(run_dir)
        metrics = _maybe(layout.perception_metrics)
        if not metrics or not metrics.get("scored"):
            continue
        n_scored += 1
        for participant in (metrics.get("per_participant") or {}).values():
            for kind in ("stop", "yield"):
                block = ((participant.get("signs") or {}).get(kind)) or {}
                kinds[kind][0] += int(block.get("n_matched") or 0)
                kinds[kind][1] += int(block.get("n_detected") or 0)
                kinds[kind][2] += int(block.get("n_real") or 0)
            if ((participant.get("latency") or {}).get("measurable")):
                latency_measurable += 1
            for name in (participant.get("signs_declared_but_not_placed") or []):
                declared_not_placed.append(str(name))
        for name, bucket in (("markings", markings), ("stop_lines", stop_lines)):
            block = metrics.get(name) or {}
            bucket[0] += int(block.get("n_matched") or 0)
            bucket[1] += int(block.get("n_detected") or 0)
            bucket[2] += int(block.get("n_real") or 0)

    return {
        "n_runs_scored": n_scored,
        "source": "real CARLA campaign frames",
        "stop_signs": _prf(kinds["stop"][0], kinds["stop"][1], kinds["stop"][2]),
        "yield_signs": _prf(kinds["yield"][0], kinds["yield"][1], kinds["yield"][2]),
        # Neither of the next two has a reference in this campaign, for two
        # different reasons, and each says which.
        "stop_lines": _prf(
            stop_lines[0], stop_lines[1], stop_lines[2],
            reference=bool(stop_lines[2]),
            no_reference_note=(
                "the stop-line reference is a position derived from the sign "
                "and the lane, and Town05 paints no bar at these junctions, so "
                "no line here is physically verified. The crossings the "
                "detector reported are counted and not scored: calling them "
                "false positives would charge the detector with missing "
                "markings the map never painted"
            ),
        ),
        "lane_markings": _prf(
            markings[0], markings[1], markings[2],
            reference=False,
            no_reference_note=(
                "the lane sensor is an onboard ADAS signal, so the sensor is "
                "the measurement and there is no independent reference to "
                "score it against. Crossings are reported by type"
            ),
        ),
        "n_participants_with_measurable_latency": latency_measurable,
        "latency_note": (
            "detection latency needs a baseline for when each sign first became "
            "visible from the approach, which depends on speed and geometry and "
            "is not in the privileged record. Reported as unmeasurable rather "
            "than computed against a baseline that was never recorded"
        ),
        "signs_declared_but_not_placed": sorted(set(declared_not_placed)),
        "note": (
            "counts are over real campaign frames. A kind with no real instances "
            "reports None rather than zero: the give-way detector has almost no "
            "sample in this campaign and a rate over nothing is not a result"
        ),
    }


# --- collision order ------------------------------------------------------


def collision_order_block(run_dirs: Sequence[Path]) -> Dict[str, Any]:
    """Whether multi-impact runs recovered the order, from the supervisor cell.

    Read off the same string the per-scenario table shows, so the aggregate and
    the table can never disagree.
    """
    from .supervisor_table import _collision_order

    verdicts: Counter = Counter()
    rows: List[Dict[str, Any]] = []
    for run_dir in run_dirs:
        layout = RunLayout.from_run_dir(run_dir)
        manifest = _maybe(layout.manifest) or {}
        cell = _collision_order(
            _maybe(layout.global_log),
            _maybe(layout.observable_events),
            _maybe(layout.clock_alignment),
            manifest.get("fixed_delta_seconds"),
        )
        if cell in ("not fused", "no impact"):
            verdict = "not_applicable"
        elif cell.startswith("single impact"):
            verdict = "single_impact"
        elif "order not established" in cell:
            verdict = "not_established"
        elif "(correct)" in cell:
            verdict = "correct"
        elif "WRONG" in cell:
            verdict = "wrong"
        else:
            verdict = "no_reference"
        verdicts[verdict] += 1
        if verdict in ("correct", "wrong", "not_established"):
            rows.append({
                "scenario": manifest.get("scenario_id"),
                "variant": manifest.get("variant"),
                "seed": manifest.get("seed"),
                "verdict": verdict,
                "cell": cell,
            })

    multi = sum(verdicts[k] for k in ("correct", "wrong", "not_established"))
    # Declining to order two impacts is not the same as ordering them wrongly,
    # so the rate over claims is reported beside the rate over all multi-impact
    # runs. One says how often the method is right when it speaks; the other
    # says how often it speaks at all.
    claimed = verdicts.get("correct", 0) + verdicts.get("wrong", 0)
    return {
        "verdicts": dict(sorted(verdicts.items())),
        "n_multi_impact_runs": multi,
        "n_order_claimed": claimed,
        "n_order_declined": verdicts.get("not_established", 0),
        "accuracy_where_claimed": _rate(verdicts.get("correct", 0), claimed),
        "correct_rate": _rate(verdicts.get("correct", 0), multi),
        "multi_impact_runs": rows,
        "note": (
            "only runs with more than one impact can get an order wrong. "
            "'not established' is its own verdict, not a failure: two impacts "
            "closer together than the recording can resolve, or an offset "
            "resting on a shared anchor, leave an order the method did not claim"
        ),
    }


# --- responsibility and counterfactuals -----------------------------------


def _counterfactual_block(run_dirs: Sequence[Path]) -> Dict[str, Any]:
    roles: Counter = Counter()
    verdicts: Counter = Counter()
    n_reports = 0
    for run_dir in run_dirs:
        layout = RunLayout.from_run_dir(run_dir)
        report = _maybe(layout.responsibility_report)
        if not report:
            continue
        n_reports += 1
        for finding in (report.get("findings") or {}).values():
            block = finding.get("but_for_contribution") or {}
            verdicts[str(block.get("verdict", "not tested"))] += 1
            role = block.get("counterfactual_role")
            if role:
                roles[str(role)] += 1
    n_findings = sum(verdicts.values())
    n_not_tested = int(verdicts.get("not tested", 0))
    n_tested = n_findings - n_not_tested
    complete = n_findings > 0 and n_tested == n_findings
    return {
        "n_reports": n_reports,
        "n_findings": n_findings,
        "n_tested_findings": n_tested,
        "status": (
            "complete" if complete else
            "not_evaluated" if n_tested == 0 else
            "incomplete"
        ),
        "campaign_wide_aggregate_claimed": complete,
        "but_for_verdicts": dict(sorted(verdicts.items())),
        "counterfactual_roles": dict(sorted(roles.items())),
        "note": (
            "a campaign-wide aggregate is reported only when every finding was "
            "tested. A prevention opportunity is not factual causation. The "
            "role says which question a replay answered: removing what "
            "happened, supplying what did not, or improving what did"
        ),
    }


def _evidence_block(run_dirs: Sequence[Path]) -> Dict[str, Any]:
    classes: Counter = Counter()
    for run_dir in run_dirs:
        report = _maybe(RunLayout.from_run_dir(run_dir).responsibility_report)
        for finding in ((report or {}).get("findings") or {}).values():
            classes[str(finding.get("responsibility_evidence", "?"))] += 1
    return dict(sorted(classes.items()))


# --- the whole set --------------------------------------------------------


def v2_blocks(artifacts_root: PathLike, run_dirs: Optional[Sequence[Path]] = None) -> Dict[str, Any]:
    """Every V2 block, from the runs under ``artifacts_root``."""
    root = Path(artifacts_root)
    if run_dirs is None:
        from .suite import _run_dirs, RUN_KIND_PRIMARY

        run_dirs = _run_dirs(root, kinds=(RUN_KIND_PRIMARY,))
    run_dirs = list(run_dirs)

    formal_runs: List[Mapping[str, Any]] = []
    responsibility_runs: List[Mapping[str, Any]] = []
    for run_dir in run_dirs:
        layout = RunLayout.from_run_dir(run_dir)
        block = _maybe(layout.formal_metrics)
        if block:
            formal_runs.append(block)
        block = _maybe(layout.responsibility_metrics)
        if block:
            responsibility_runs.append(block)

    return {
        "clock": clock_block(run_dirs),
        "perception": perception_block(run_dirs),
        "formal": aggregate_formal(formal_runs),
        "responsibility": {
            "sets": aggregate_responsibility(responsibility_runs),
            "evidence_classes": _evidence_block(run_dirs),
        },
        "collision_order": collision_order_block(run_dirs),
        "counterfactual": _counterfactual_block(run_dirs),
    }
