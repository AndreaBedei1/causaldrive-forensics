"""Cross-participant clock alignment, the first stage of the fusion layer.

Why this stage exists
---------------------
Fusion must be defensible as a procedure applied to *exchanged logs*, not as a
convenience that quietly borrows the simulator's shared clock. Every downstream
comparison (trajectory matching in :mod:`cdf.fusion.track_association`, event
merging in :mod:`cdf.fusion.event_alignment`) assumes that two participants'
timestamps denote the same physical instant. That assumption is made explicit
here: an offset is *estimated* per participant from the sample grids alone, the
residual is reported, and a suspicious offset becomes a diagnostic rather than a
silent distortion of every later result.

In a synchronous CARLA run the correct answer is an offset of ~0 with a residual
of ~0, so this stage doubles as a cheap integrity check on the recorded logs: a
non-zero estimate means the two logs were not produced by the same server tick
sequence and everything downstream should be read with that in mind.

Only participant-owned telemetry timestamps are used. No map data, no actor ids,
no privileged state.
"""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.evidence import RunEvidence
from ..common.timeline import build_common_grid, resolve_offsets

__all__ = [
    "align_participants",
    "apply_offset",
    "aligned_spans",
]


def apply_offset(times: Sequence[float], offset_s: float) -> List[float]:
    """Shift ``times`` into the reference participant's clock.

    The sign convention is the one fixed by
    :func:`cdf.common.timeline.estimate_clock_offset`:
    ``t_reference ~= t_participant + offset_s``.
    """
    off = float(offset_s)
    return [float(t) + off for t in times]


def aligned_spans(
    run: RunEvidence, offsets: Dict[str, Dict[str, Any]]
) -> Dict[str, Tuple[float, float]]:
    """Per-participant telemetry span expressed in the reference clock.

    Kept separate from :func:`align_participants` so that callers which already
    hold an alignment result can re-derive spans without re-estimating offsets.
    """
    out: Dict[str, Tuple[float, float]] = {}
    for pid, span in sorted(run.spans().items()):
        entry = offsets.get(pid)
        off = float(entry["offset_s"]) if entry else 0.0
        out[pid] = (float(span[0]) + off, float(span[1]) + off)
    return out


def align_participants(run: RunEvidence, cfg: Config) -> Dict[str, Any]:
    """Estimate every participant's clock offset and the common observable span.

    Returns a serialisable mapping::

        {"reference": pid | None,
         "offsets": {pid: {"offset_s", "residual_s", "n_samples",
                           "confidence", "notes", "method", "is_reference"}},
         "common_span": [t0, t1] | None,
         "grid_dt": float,
         "diagnostics": [ {...}, ... ]}

    ``common_span`` is the *intersection* of the offset-corrected telemetry spans:
    outside it at most one participant was recording, so no cross-participant
    claim can be made there. ``None`` means the logs do not overlap at all, which
    is reported as a diagnostic instead of being papered over.
    """
    max_offset_s = float(cfg.get("fusion.time_alignment.max_offset_s", 1.0))
    grid_dt = float(cfg.get("fusion.time_alignment.grid_dt", 0.05))
    # Not present in configs/default.yaml -- see module notes in the task report.
    max_residual_s = float(cfg.get("fusion.time_alignment.max_residual_s", grid_dt))

    diagnostics: List[Dict[str, Any]] = []
    streams: Dict[str, List[float]] = {}

    for pid in run.participant_ids:
        times = run.get(pid).times()
        if not times:
            diagnostics.append(
                {
                    "kind": "empty_telemetry",
                    "severity": "warning",
                    "participant_id": pid,
                    "message": (
                        "participant {0} exported no telemetry; it cannot be "
                        "time-aligned and is excluded from fusion".format(pid)
                    ),
                }
            )
            continue
        streams[pid] = times

    if not streams:
        diagnostics.append(
            {
                "kind": "no_alignable_participants",
                "severity": "error",
                "participant_id": None,
                "message": "no participant exported telemetry; alignment is undefined",
            }
        )
        return {
            "reference": None,
            "offsets": {},
            "common_span": None,
            "grid_dt": grid_dt,
            "diagnostics": diagnostics,
        }

    estimates = resolve_offsets(streams)
    reference = estimates[sorted(estimates.keys())[0]].reference_id

    offsets: Dict[str, Dict[str, Any]] = {}
    for pid in sorted(estimates.keys()):
        est = estimates[pid]
        offsets[pid] = {
            "offset_s": float(est.offset_s),
            "residual_s": float(est.residual_s),
            "n_samples": int(est.n_samples),
            "confidence": float(est.confidence),
            "method": est.method,
            "is_reference": pid == reference,
            "notes": list(est.notes),
        }

        if pid == reference:
            continue

        if est.n_samples == 0 or not math.isfinite(est.residual_s):
            diagnostics.append(
                {
                    "kind": "offset_not_estimable",
                    "severity": "error",
                    "participant_id": pid,
                    "message": (
                        "no sample of {0} fell within the search window of the "
                        "reference {1}; the offset defaulted to 0 and every "
                        "cross-participant claim involving {0} is unsupported".format(
                            pid, reference
                        )
                    ),
                }
            )
            continue

        if abs(est.offset_s) > max_offset_s:
            diagnostics.append(
                {
                    "kind": "offset_exceeds_limit",
                    "severity": "error",
                    "participant_id": pid,
                    "offset_s": float(est.offset_s),
                    "max_offset_s": max_offset_s,
                    "message": (
                        "estimated clock offset {0:.6f}s for {1} exceeds "
                        "fusion.time_alignment.max_offset_s={2}s".format(
                            est.offset_s, pid, max_offset_s
                        )
                    ),
                }
            )
        elif abs(est.offset_s) > 1e-6:
            diagnostics.append(
                {
                    "kind": "non_zero_offset",
                    "severity": "warning",
                    "participant_id": pid,
                    "offset_s": float(est.offset_s),
                    "message": (
                        "non-zero clock offset {0:.6f}s estimated for {1}; a "
                        "synchronous run should yield ~0".format(est.offset_s, pid)
                    ),
                }
            )

        if est.residual_s > max_residual_s:
            diagnostics.append(
                {
                    "kind": "high_offset_residual",
                    "severity": "warning",
                    "participant_id": pid,
                    "residual_s": float(est.residual_s),
                    "max_residual_s": max_residual_s,
                    "message": (
                        "median alignment residual {0:.6f}s for {1} exceeds "
                        "{2:.6f}s; sample grids do not coincide".format(
                            est.residual_s, pid, max_residual_s
                        )
                    ),
                }
            )

    corrected = aligned_spans(run, offsets)
    grid = build_common_grid([corrected[pid] for pid in sorted(corrected.keys())], grid_dt)
    common_span: Optional[List[float]] = None
    if grid is None:
        diagnostics.append(
            {
                "kind": "no_common_span",
                "severity": "error",
                "participant_id": None,
                "message": (
                    "offset-corrected telemetry spans do not intersect: "
                    + ", ".join(
                        "{0}=[{1:.3f}, {2:.3f}]".format(pid, sp[0], sp[1])
                        for pid, sp in sorted(corrected.items())
                    )
                ),
            }
        )
    else:
        common_span = [float(grid.t0), float(grid.t1)]

    return {
        "reference": reference,
        "offsets": offsets,
        "common_span": common_span,
        "grid_dt": grid_dt,
        "diagnostics": diagnostics,
    }
