"""Public clock-alignment API; estimation uses physical local evidence only."""

from .clock_alignment import align_participants, aligned_spans, estimate_track_clock


def apply_offset(times, offset_s):
    """Compatibility helper for pure additive transforms."""
    return [float(t) + float(offset_s) for t in times]


__all__ = [
    "align_participants",
    "aligned_spans",
    "estimate_track_clock",
    "apply_offset",
]
