"""Readable finite counterexamples for failed finite-trace properties.

A ``FAIL`` verdict is only useful if a human can see what happened. A violating
interval alone is a pair of numbers; what an investigator needs is the short
stretch of trace around it, with the quantities the property talked about lined
up sample by sample, plus a statement of *which condition held where*.

That is what this module produces. Three design choices matter:

* **Padding.** The window is widened by ``pad_s`` on both sides, because the
  interesting part is usually the approach to the violation -- what the driver
  was doing just before, and whether anything changed just after.
* **Bounded size.** The output is rendered in the viewer next to the graph, so a
  long violation is decimated to at most ``max_samples`` rows by a deterministic
  stride that always keeps the first and last sample. Decimation never widens the
  window: every emitted row lies inside the padded interval.
* **Own evidence only.** A counterexample is extracted from one participant's own
  :class:`~cdf.common.evidence.ParticipantEvidence`, so it contains exactly what
  that vehicle could have shown an investigator -- no privileged data, and no
  other participant's record.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.schemas import CheckStatus, SCHEMA_VERSIONS
from ..common.timeline import Interval
from .properties import (
    PropertyResult,
    TraceSample,
    build_state_trace,
    make_counterexample_ref,
    trace_parameters,
)

__all__ = [
    "COUNTEREXAMPLE_COLUMNS",
    "extract_counterexample",
    "build_counterexample_report",
]


#: Per-sample columns of an extracted counterexample, in emission order.
COUNTEREXAMPLE_COLUMNS: Tuple[str, ...] = (
    "t",
    "speed",
    "throttle",
    "brake",
    "steer",
    "min_range",
    "min_ttc",
    "active_track_ids",
)

_T_EPS = 1e-9


def extract_counterexample(
    ev: ParticipantEvidence,
    interval: Tuple[float, float],
    cfg: Config,
    pad_s: float = 1.0,
) -> Dict[str, Any]:
    """Extract the trace around ``interval`` from one participant's evidence.

    Parameters
    ----------
    ev:
        The participant whose own recording is being explained.
    interval:
        ``(t_start, t_end)`` of the violation, in simulation seconds.
    cfg:
        Supplies the condition thresholds annotated onto the trace and the
        ``checking.counterexample.max_samples`` size bound.
    pad_s:
        Seconds of context added on each side. Callers that want the configured
        default should read ``checking.counterexample.pad_s`` and pass it
        explicitly, which is what :func:`build_counterexample_report` does.

    Returns
    -------
    dict
        A JSON-serialisable counterexample: the padded sample window, the
        condition spans, and a small numeric summary.
    """
    t0, t1 = float(interval[0]), float(interval[1])
    if t1 < t0:
        raise ValueError(
            "counterexample interval end {0} precedes start {1}".format(t1, t0)
        )
    pad = float(pad_s)
    if pad < 0.0:
        raise ValueError("counterexample pad_s must be non-negative, got {0}".format(pad))

    padded = Interval(t0, t1).expanded(pad)
    trace = build_state_trace(ev, cfg)
    window = [
        s
        for s in trace
        if padded.start - _T_EPS <= s.t <= padded.end + _T_EPS
    ]

    max_samples = int(cfg.get("checking.counterexample.max_samples", 240))
    if max_samples < 2:
        raise ValueError(
            "checking.counterexample.max_samples must be >= 2, got {0}".format(max_samples)
        )
    emitted, subsampled = _decimate(window, max_samples)

    thresholds = _condition_thresholds(cfg)
    conditions = _condition_spans(window, thresholds, (t0, t1), cfg, ev)

    return {
        "schema_version": SCHEMA_VERSIONS["model_check"],
        "participant_id": ev.participant_id,
        "interval": [t0, t1],
        "padded_interval": [padded.start, padded.end],
        "pad_s": pad,
        "columns": list(COUNTEREXAMPLE_COLUMNS),
        "samples": [_sample_row(s) for s in emitted],
        "n_samples": len(emitted),
        "n_samples_available": len(window),
        "subsampled": subsampled,
        "condition_parameters": thresholds,
        "conditions": conditions,
        "summary": _numeric_summary(window, (t0, t1)),
        "trace_parameters": trace_parameters(ev, cfg),
    }


def build_counterexample_report(
    results: Sequence[PropertyResult], run: RunEvidence, cfg: Config
) -> Dict[str, Any]:
    """Build the run-level counterexample artifact for every ``FAIL`` verdict.

    One counterexample is produced per failed :class:`PropertyResult`, spanning
    the hull of that result's violating intervals (the individual intervals are
    kept inside the payload, so a multi-episode failure stays legible). Results
    that cannot be explained -- a participant missing from the run bundle, a
    ``FAIL`` carrying no interval -- are recorded in ``skipped`` rather than
    dropped, because a counterexample that quietly disappears is worse than one
    that is reported as unavailable.
    """
    pad = float(cfg.get("checking.counterexample.pad_s", 1.0))
    counterexamples: Dict[str, Any] = {}
    index: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []

    for res in results:
        if res.status is not CheckStatus.FAIL:
            continue
        if not res.violating_intervals:
            skipped.append(
                {
                    "property_id": res.property_id,
                    "participant_id": res.participant_id,
                    "why": "FAIL verdict carries no violating interval",
                }
            )
            continue
        if res.participant_id not in run.participants:
            skipped.append(
                {
                    "property_id": res.property_id,
                    "participant_id": res.participant_id,
                    "why": "participant is not present in this run's evidence bundle",
                }
            )
            continue

        hull = (
            min(float(a) for a, _ in res.violating_intervals),
            max(float(b) for _, b in res.violating_intervals),
        )
        ev = run.get(res.participant_id)
        payload = extract_counterexample(ev, hull, cfg, pad_s=pad)
        payload["property_id"] = res.property_id
        payload["status"] = res.status.value
        payload["reason"] = res.reason
        payload["parameters"] = dict(res.parameters)
        payload["witness"] = dict(res.witness)
        payload["violating_intervals"] = [
            [float(a), float(b)] for a, b in res.violating_intervals
        ]

        ref = res.counterexample_ref or make_counterexample_ref(
            res.property_id, res.participant_id, hull[0], hull[1]
        )
        payload["counterexample_ref"] = ref
        counterexamples[ref] = payload
        index.append(
            {
                "counterexample_ref": ref,
                "property_id": res.property_id,
                "participant_id": res.participant_id,
                "interval": [hull[0], hull[1]],
                "n_samples": payload["n_samples"],
            }
        )

    index.sort(key=lambda row: (row["participant_id"], row["property_id"], row["interval"][0]))
    return {
        "schema_version": SCHEMA_VERSIONS["model_check"],
        "run_id": run.run_id,
        "scenario_id": run.scenario_id,
        "seed": run.seed,
        "config_hash": cfg.hash,
        "pad_s": pad,
        "n_counterexamples": len(counterexamples),
        "index": index,
        "counterexamples": counterexamples,
        "skipped": skipped,
    }


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _sample_row(s: TraceSample) -> Dict[str, Any]:
    """One counterexample row; ``None`` is preserved to mark missing evidence."""
    return {
        "t": float(s.t),
        "speed": s.speed,
        "throttle": s.throttle,
        "brake": s.brake,
        "steer": s.steer,
        "min_range": s.min_range,
        "min_ttc": s.min_ttc,
        "active_track_ids": list(s.active_track_ids),
    }


def _decimate(
    window: Sequence[TraceSample], max_samples: int
) -> Tuple[List[TraceSample], bool]:
    """Keep at most ``max_samples`` rows, preserving the first and the last.

    A fixed stride is used rather than any adaptive scheme so that the same
    violation always yields the same rows -- counterexamples are artifacts and
    must be byte-reproducible.
    """
    n = len(window)
    if n <= max_samples:
        return (list(window), False)
    stride = (n + max_samples - 1) // max_samples
    kept = [window[i] for i in range(0, n, stride)]
    if kept[-1] is not window[n - 1]:
        kept.append(window[n - 1])
    return (kept, True)


def _condition_thresholds(cfg: Config) -> Dict[str, float]:
    """Thresholds used to annotate the trace, taken from the property registry."""
    return {
        "critical_ttc_s": float(
            cfg.get("checking.P1_brake_response.ttc_critical_s", 1.6)
        ),
        "brake_cmd": float(cfg.get("checking.P1_brake_response.brake_cmd", 0.25)),
        "closing_rate_mps": float(
            cfg.get("checking.P2_no_throttle_while_closing.closing_rate_mps", 5.0)
        ),
        "throttle_cmd": float(
            cfg.get("checking.P2_no_throttle_while_closing.throttle_cmd", 0.20)
        ),
        "stop_speed_mps": float(
            cfg.get("checking.P3_post_collision_stop.stop_speed_mps", 1.0)
        ),
        "steer_cmd": float(
            cfg.get("checking.P4_conflict_without_response.min_evasive_steer", 0.15)
        ),
    }


def _condition_spans(
    window: Sequence[TraceSample],
    thresholds: Dict[str, float],
    interval: Tuple[float, float],
    cfg: Config,
    ev: ParticipantEvidence,
) -> Dict[str, List[List[float]]]:
    """Time spans over which each named condition held, inside the padded window.

    This is the "which condition held where" summary: it lets a reader see, at a
    glance, that (say) the critical-TTC condition started at 2.40 s while braking
    only began at 4.10 s, without scanning the sample table.
    """
    max_gap = trace_parameters(ev, cfg)["max_gap_s"]
    t0, t1 = float(interval[0]), float(interval[1])

    predicates = {
        "critical_ttc": lambda s: s.min_ttc is not None
        and s.min_ttc <= thresholds["critical_ttc_s"],
        "closing_fast": lambda s: s.closing_rate is not None
        and s.closing_rate >= thresholds["closing_rate_mps"],
        "braking": lambda s: s.brake is not None and s.brake >= thresholds["brake_cmd"],
        "throttle_applied": lambda s: s.throttle is not None
        and s.throttle > thresholds["throttle_cmd"],
        "steering": lambda s: s.steer is not None
        and abs(s.steer) >= thresholds["steer_cmd"],
        "stopped": lambda s: s.speed is not None
        and s.speed < thresholds["stop_speed_mps"],
        "missing_control_evidence": lambda s: s.throttle is None or s.brake is None,
        "no_track_evidence": lambda s: not s.active_track_ids,
        "inside_violating_interval": lambda s: t0 - _T_EPS <= s.t <= t1 + _T_EPS,
    }

    out: Dict[str, List[List[float]]] = {}
    for name, pred in predicates.items():
        flags = [bool(pred(s)) for s in window]
        out[name] = [
            [float(window[a].t), float(window[b].t)]
            for a, b in _spans(window, flags, max_gap)
        ]
    return out


def _spans(
    window: Sequence[TraceSample], flags: Sequence[bool], max_gap: float
) -> List[Tuple[int, int]]:
    """Maximal contiguous index ranges where ``flags`` holds (see properties._runs)."""
    runs: List[Tuple[int, int]] = []
    start: Optional[int] = None
    for i, f in enumerate(flags):
        if f:
            if start is None:
                start = i
            elif float(window[i].t) - float(window[i - 1].t) > float(max_gap):
                runs.append((start, i - 1))
                start = i
        elif start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, len(flags) - 1))
    return runs


def _numeric_summary(
    window: Sequence[TraceSample], interval: Tuple[float, float]
) -> Dict[str, Any]:
    """Headline numbers of the violation, for a one-line rendering in the viewer."""
    t0, t1 = float(interval[0]), float(interval[1])
    inside = [s for s in window if t0 - _T_EPS <= s.t <= t1 + _T_EPS]
    scope = inside if inside else list(window)

    def _max(attr: str) -> Optional[float]:
        vals = [getattr(s, attr) for s in scope if getattr(s, attr) is not None]
        return float(max(vals)) if vals else None

    def _min(attr: str) -> Optional[float]:
        vals = [getattr(s, attr) for s in scope if getattr(s, attr) is not None]
        return float(min(vals)) if vals else None

    steers = [abs(float(s.steer)) for s in scope if s.steer is not None]
    tracks = sorted({tid for s in window for tid in s.active_track_ids})
    speeds = [s for s in scope if s.speed is not None]
    return {
        "duration_s": t1 - t0,
        "max_brake": _max("brake"),
        "max_throttle": _max("throttle"),
        "max_abs_steer": max(steers) if steers else None,
        "min_ttc": _min("min_ttc"),
        "min_range": _min("min_range"),
        "min_speed": _min("speed"),
        "speed_at_start": float(speeds[0].speed) if speeds else None,
        "speed_at_end": float(speeds[-1].speed) if speeds else None,
        "track_ids": tracks,
    }
