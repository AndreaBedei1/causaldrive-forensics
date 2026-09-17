"""Combination rules for the confidence attached to fused nodes and edges.

What these numbers are -- and are not
-------------------------------------
The values combined here are **evidence-accumulation heuristics, not calibrated
probabilities**. A local event's confidence expresses how cleanly the underlying
signal crossed its threshold (how many radar points supported the track, how far
above the hysteresis band the deceleration went); it is not the output of a
fitted probabilistic model and no frequency interpretation is claimed for it.
Consequently the fused value must not be read as ``P(event | evidence)``. It is a
monotone, auditable summary answering one question: *did several independent
onboard recorders support the same claim, and how strongly?*

The three supported rules make different assumptions:

* ``noisy_or`` -- treats each contribution as an independent chance to establish
  the claim, so corroboration by a second participant strictly increases the
  result. This is the default because independence is the interesting property of
  this architecture: the recorders share no sensor and no clock discipline.
  It is also the most optimistic rule, which is why it is capped.
* ``max`` -- keeps the strongest single piece of evidence and refuses to let
  agreement between weak observations manufacture certainty.
* ``mean`` -- averages, so a weak observation *dilutes* a strong one; appropriate
  when the contributions are believed to be measurements of one quantity rather
  than independent attempts to detect it.

The cap exists so that no fused claim can ever reach 1.0: certainty is not
reachable by accumulating heuristics.
"""

from __future__ import annotations

from typing import Sequence

from ..common.config import Config

__all__ = [
    "SUPPORTED_METHODS",
    "noisy_or",
    "fuse_confidence",
]

#: Methods accepted by :func:`fuse_confidence`.
SUPPORTED_METHODS = ("noisy_or", "max", "mean")


def noisy_or(values: Sequence[float], cap: float = 0.99) -> float:
    """``1 - prod(1 - v)``, clamped to ``[0, cap]``.

    Each input is clamped to ``[0, 1]`` first, so a malformed upstream confidence
    cannot flip the sign of a product and produce a nonsensical result. An empty
    sequence yields ``0.0``: no evidence is not weak evidence.

    ``noisy_or([0.5, 0.5]) == 0.75`` -- two independent half-strength
    observations support the claim more than either alone.
    """
    complement = 1.0
    seen = False
    for v in values:
        seen = True
        complement *= 1.0 - _clamp01(v)
    if not seen:
        return 0.0
    return max(0.0, min(float(cap), 1.0 - complement))


def fuse_confidence(values: Sequence[float], cfg: Config) -> float:
    """Combine contributing confidences with the configured rule.

    The rule is read from ``fusion.confidence_fusion.method`` and the ceiling from
    ``fusion.confidence_fusion.cap``. An unknown method raises: silently falling
    back to a default would make the number in the artifact untraceable to the
    configuration hash stamped next to it.

    See the module docstring: the result is an evidence-accumulation score, not a
    calibrated probability.
    """
    method = str(cfg.get("fusion.confidence_fusion.method", "noisy_or"))
    cap = float(cfg.get("fusion.confidence_fusion.cap", 0.99))

    if method not in SUPPORTED_METHODS:
        raise ValueError(
            "unknown fusion.confidence_fusion.method {0!r}; supported: {1}".format(
                method, ", ".join(SUPPORTED_METHODS)
            )
        )

    clamped = [_clamp01(v) for v in values]
    if not clamped:
        return 0.0

    if method == "noisy_or":
        return noisy_or(clamped, cap=cap)
    if method == "max":
        return max(0.0, min(cap, max(clamped)))
    return max(0.0, min(cap, sum(clamped) / float(len(clamped))))


def _clamp01(value: float) -> float:
    """Clamp to ``[0, 1]``."""
    return max(0.0, min(1.0, float(value)))
