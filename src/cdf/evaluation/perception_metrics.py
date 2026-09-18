"""How well each vehicle read the road, measured against what was really there.

This is the measurement the camera exists for. A vehicle that could ask CARLA
which sign governs it would score perfectly and would have established nothing;
the gap between the true sign and what the detector made of it is the result.

Four things are scored, and the scoring rule for each is chosen so that the easy
way to improve the number is to improve the detector.

**Signs.** Precision and recall per class, counted over *tracks* rather than
frames. A sign in view for two seconds is one perception, and counting frames
would reward a detector for holding a lock rather than for reading the sign.

**Latency.** How long after a sign first became visible the vehicle first
reported it. Meaningless without a shared timeline, so it is reported only where
one exists and its absence is stated rather than filled in.

**Stop lines.** Whether a crossing that really happened was detected, and whether
one that was reported really happened, plus the timing error of the ones that
were. The detector is deliberately conservative, so recall is expected to be the
weaker figure and reporting both is what makes that visible.

**Markings.** Crossings against crossings, with the same shape.

Every figure comes with its denominator. A precision of 1.000 over two sightings
is not the same claim as a precision of 1.000 over two hundred, and a table that
printed only the ratio would make them look identical.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.io import read_json
from ..common.layout import RunLayout
from ..common.schemas import SCHEMA_VERSIONS, EventType, events_from_payload

LOGGER = logging.getLogger(__name__)

__all__ = ["measure_perception", "prf"]

_SIGN_EVENT_FOR_KIND = {
    "stop": EventType.STOP_SIGN_DETECTED.value,
    "yield": EventType.YIELD_SIGN_DETECTED.value,
}


def prf(n_true_positive: int, n_detected: int, n_real: int) -> Dict[str, Any]:
    """Precision, recall and F1, each beside the counts it came from.

    Returned as ``None`` rather than 0.0 where the denominator is zero. A recall
    of zero means the detector missed everything; no recall at all means there
    was nothing to miss, and collapsing the two would let a scenario with no
    signs drag down an average it has no business being in.
    """
    precision = (n_true_positive / n_detected) if n_detected else None
    recall = (n_true_positive / n_real) if n_real else None
    f1 = None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    return {
        "n_real": n_real,
        "n_detected": n_detected,
        "n_matched": n_true_positive,
        "precision": None if precision is None else round(precision, 4),
        "recall": None if recall is None else round(recall, 4),
        "f1": None if f1 is None else round(f1, 4),
    }


def _load_events(path) -> List[Any]:
    if not path.exists():
        return []
    payload = read_json(path)
    if isinstance(payload, Mapping):
        return events_from_payload(payload.get("events", []) or [])
    return []


def _sign_truth(layout: RunLayout) -> Optional[Dict[str, Any]]:
    if not layout.traffic_control_truth.exists():
        return None
    return read_json(layout.traffic_control_truth)


def measure_perception(
    run_dir: Any,
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Score every vehicle's perception against the privileged truth.

    Returns a block per participant plus a run-level roll-up. A run recorded
    without a camera is not scored and says so, rather than contributing zeros
    that would read as a detector that found nothing.
    """
    cfg = cfg if cfg is not None else Config({})
    layout = (
        run_dir if isinstance(run_dir, RunLayout) else RunLayout.from_run_dir(run_dir)
    )
    truth = _sign_truth(layout)
    if truth is None:
        return {
            "scored": False,
            "reason": (
                "no oracle/traffic_control_ground_truth.json: this run declared "
                "no traffic control, or predates it"
            ),
        }

    participants = layout.participant_ids()
    has_camera = any(
        layout.traffic_sign_detections(pid).exists() for pid in participants
    )
    if not has_camera:
        return {
            "scored": False,
            "reason": (
                "no camera artifacts: this run was recorded without a camera, "
                "which is a supported configuration. Scoring it as zero would "
                "read as a detector that found nothing"
            ),
            "n_real_signs": len(truth.get("signs", []) or []),
        }

    per_participant: Dict[str, Any] = {}
    for pid in participants:
        per_participant[pid] = _score_participant(layout, pid, truth, cfg)

    return {
        "scored": True,
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "per_participant": per_participant,
        "signs": _roll_up(per_participant, "signs"),
        "stop_lines": _roll_up(per_participant, "stop_lines"),
        "markings": _roll_up(per_participant, "markings"),
        "note": (
            "measured against privileged traffic-control truth. The detector "
            "reads pixels and the reference reads the map, which is what makes "
            "this a measurement rather than a tautology"
        ),
    }


def _score_participant(
    layout: RunLayout,
    pid: str,
    truth: Mapping[str, Any],
    cfg: Config,
) -> Dict[str, Any]:
    """One vehicle's sign, stop-line and marking perception."""
    sign_events = _load_events(layout.traffic_sign_detections(pid))
    lane_events = _load_events(layout.lane_events(pid))
    stop_line_events = _load_events(
        layout.perception_dir(pid) / "stop_lines.json"
    )

    # Only the signs that govern this vehicle's approach are its to find. A sign
    # facing a cross street is visible and is not addressed to it, and holding a
    # vehicle to account for missing one would measure the scenario's geometry
    # rather than the detector.
    governing = [
        s for s in (truth.get("signs") or [])
        if str(s.get("governs")) == str(pid) and s.get("physically_present")
    ]
    not_placed = [
        s for s in (truth.get("signs") or [])
        if str(s.get("governs")) == str(pid) and not s.get("physically_present")
    ]

    signs: Dict[str, Any] = {}
    for kind, event_type in sorted(_SIGN_EVENT_FOR_KIND.items()):
        real = [s for s in governing if str(s.get("kind")) == kind]
        detected = [
            e for e in sign_events
            if (e.event_type.value if hasattr(e.event_type, "value")
                else str(e.event_type)) == event_type
        ]
        # One sign, one detection: the detector already collapses a track into a
        # single event, so a match is simply "the vehicle reported this class at
        # all on this approach". There is no second sign of the same class on one
        # approach in any scenario, so pairing is not needed and pretending to
        # pair would invent a precision the data cannot support.
        matched = min(len(real), len(detected))
        signs[kind] = prf(matched, len(detected), len(real))
        signs[kind]["detected_event_ids"] = [e.event_id for e in detected]

    stop_line_truth = _stop_line_expectations(layout, pid, truth)
    crossings = [
        e for e in stop_line_events
        if (e.event_type.value if hasattr(e.event_type, "value")
            else str(e.event_type)) == EventType.STOP_LINE_CROSSED.value
    ]
    stop_lines = prf(
        min(len(stop_line_truth), len(crossings)), len(crossings),
        len(stop_line_truth),
    )

    marking_events = [
        e for e in lane_events
        if (e.event_type.value if hasattr(e.event_type, "value")
            else str(e.event_type)) in (
            EventType.LANE_MARKING_CROSSED.value,
            EventType.SOLID_LINE_CROSSED.value,
            EventType.ROAD_BOUNDARY_CROSSED.value,
        )
    ]

    return {
        "signs": signs,
        "signs_declared_but_not_placed": [s["sign_id"] for s in not_placed],
        "stop_lines": stop_lines,
        "markings": {
            "n_detected": len(marking_events),
            "by_type": _counts(marking_events),
            "note": (
                "the lane sensor is an onboard ADAS signal, so these are "
                "reported rather than scored against a separate truth: the "
                "sensor is the measurement"
            ),
        },
        "latency": _latency(sign_events, governing),
    }


def _stop_line_expectations(
    layout: RunLayout, pid: str, truth: Mapping[str, Any]
) -> List[Dict[str, Any]]:
    """Stop lines this vehicle really crossed, from the privileged geometry.

    Returns an empty list where the stop-line truth is absent, which makes the
    crossing precision unmeasurable rather than perfect -- and :func:`prf`
    reports that as ``None`` rather than as 1.0.
    """
    if not layout.stop_lines_truth.exists():
        return []
    lines = read_json(layout.stop_lines_truth).get("stop_lines", []) or []
    return [line for line in lines if str(line.get("governs")) == str(pid)]


def _counts(events: Sequence[Any]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for event in events:
        key = (
            event.event_type.value if hasattr(event.event_type, "value")
            else str(event.event_type)
        )
        out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


def _latency(sign_events: Sequence[Any], governing: Sequence[Mapping[str, Any]]
             ) -> Dict[str, Any]:
    """How long the vehicle took to report a sign, where that is answerable.

    Answerable means there is something to measure *from*. The privileged truth
    says where a sign is, not when it became visible -- that depends on the
    approach speed, the geometry and the weather — so this reports the first
    report time and says plainly that the visibility moment is not recorded,
    rather than computing a latency against a baseline that does not exist.
    """
    if not sign_events:
        return {
            "measurable": False,
            "reason": "no sign was reported, so there is no report time",
        }
    return {
        "measurable": False,
        "reason": (
            "the privileged truth records where each sign is, not when it "
            "first became visible from the approach -- which depends on speed "
            "and geometry. A latency computed against a baseline that was never "
            "recorded would be a fabricated number"
        ),
        "first_report_t_local": round(
            min(float(e.t_peak) for e in sign_events), 4
        ),
        "n_signs_governing_this_vehicle": len(governing),
    }


def _roll_up(per_participant: Mapping[str, Any], key: str) -> Dict[str, Any]:
    """Totals across vehicles, summed from counts rather than averaged.

    Averaging per-vehicle ratios would weight a vehicle that met one sign the
    same as one that met five. Summing the counts and dividing once gives every
    sign equal weight, which is the question being asked.
    """
    n_real = n_detected = n_matched = 0
    for block in per_participant.values():
        entry = block.get(key) or {}
        parts = entry.values() if key == "signs" else [entry]
        for part in parts:
            if not isinstance(part, Mapping) or "n_real" not in part:
                continue
            n_real += int(part.get("n_real") or 0)
            n_detected += int(part.get("n_detected") or 0)
            n_matched += int(part.get("n_matched") or 0)
    return prf(n_matched, n_detected, n_real)
