"""Three-valued evaluation of a metric formula over a finite, partial trace.

The whole design turns on one rule: **missing evidence never becomes PASS, and
never becomes FAIL either.** Both would be assertions about time nobody watched.

Two situations produce ``UNKNOWN``, and they are the same situation seen twice.
A window running past the end of the recording contains time that was not
observed. A window inside the recording but across a sensor dropout contains time
that was not observed either. In both cases an ``Eventually`` that found nothing
has not established absence -- only that it did not see anything -- and an
``Always`` that found no violation has not established universality.

So the temporal operators check three things in order:

1. is there a witness (or a counterexample) in the part that *was* observed? That
   settles it, because a thing seen to happen happened regardless of what else
   was missed;
2. if not, was the whole interval observed and covered? If not, ``UNKNOWN``;
3. only then, the negative verdict.

The Boolean connectives are Kleene's: ``UNKNOWN`` propagates unless the other
operand already decides the result. ``FAIL & UNKNOWN`` is ``FAIL`` -- one false
conjunct is enough whatever the other turns out to be -- and symmetrically for
``PASS | UNKNOWN``.

Every verdict carries where it was decided and by what, so a report can say "B
did not brake in [8.42, 9.92], and here is the interval and the events in it"
rather than only "FAIL".
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..common.config import Config
from ..common.schemas import CheckStatus
from .syntax import (
    ANY, SELF, SUBJECT,
    Always, And, Eventually, Formula, Historically, Implies, Not, Occurs, Once,
    Or, Since, render,
)
from .trace import EventTrace

LOGGER = logging.getLogger(__name__)

__all__ = ["Verdict", "evaluate", "Binding"]

#: Which participant each placeholder stands for while a formula is evaluated.
Binding = Mapping[str, Optional[str]]


@dataclass
class Verdict:
    """A three-valued result, with the reason it came out that way."""

    status: CheckStatus
    interval: Tuple[float, float]
    witness: List[str] = field(default_factory=list)
    """Event ids that made the verdict -- a witness for PASS, a counterexample
    for FAIL."""
    reason: str = ""
    unobserved: bool = False
    """Whether the verdict is UNKNOWN because time was not observed, as opposed
    to some other cause."""
    coverage: Optional[float] = None

    @property
    def decided(self) -> bool:
        return self.status is not CheckStatus.UNKNOWN

    def as_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "interval": [round(self.interval[0], 4), round(self.interval[1], 4)],
            "witness": list(self.witness),
            "reason": self.reason,
            "unobserved": self.unobserved,
            "coverage": None if self.coverage is None else round(self.coverage, 4),
        }


def _resolve(placeholder: Optional[str], binding: Binding) -> Optional[str]:
    """Turn ``SELF`` / ``SUBJECT`` / ``ANY`` into an id, or into 'unconstrained'."""
    if placeholder is None or placeholder == ANY:
        return None
    return binding.get(placeholder)


def _kleene_and(parts: List[Verdict], interval, reason_pass: str) -> Verdict:
    failed = [v for v in parts if v.status is CheckStatus.FAIL]
    if failed:
        return Verdict(
            CheckStatus.FAIL, interval,
            witness=[w for v in failed for w in v.witness],
            reason=failed[0].reason or "a conjunct was false",
        )
    unknown = [v for v in parts if v.status is CheckStatus.UNKNOWN]
    if unknown:
        return Verdict(
            CheckStatus.UNKNOWN, interval,
            reason=unknown[0].reason or "a conjunct could not be decided",
            unobserved=any(v.unobserved for v in unknown),
        )
    return Verdict(
        CheckStatus.PASS, interval,
        witness=[w for v in parts for w in v.witness], reason=reason_pass,
    )


def _kleene_or(parts: List[Verdict], interval, reason_fail: str) -> Verdict:
    passed = [v for v in parts if v.status is CheckStatus.PASS]
    if passed:
        return Verdict(
            CheckStatus.PASS, interval,
            witness=[w for v in passed for w in v.witness],
            reason=passed[0].reason or "a disjunct was true",
        )
    unknown = [v for v in parts if v.status is CheckStatus.UNKNOWN]
    if unknown:
        return Verdict(
            CheckStatus.UNKNOWN, interval,
            reason=unknown[0].reason or "a disjunct could not be decided",
            unobserved=any(v.unobserved for v in unknown),
        )
    return Verdict(CheckStatus.FAIL, interval, reason=reason_fail)


def _window_status(
    trace: EventTrace,
    lo: float,
    hi: float,
    min_coverage: float,
) -> Tuple[bool, float, str]:
    """Whether ``[lo, hi]`` was watched well enough to decide anything over it."""
    coverage = trace.coverage_of(lo, hi)
    if not trace.contains_window(lo, hi):
        return False, coverage, (
            "the interval [{0:.2f}, {1:.2f}] runs outside the recording "
            "[{2:.2f}, {3:.2f}], so what happened there was never observed"
            .format(lo, hi, trace.t_start, trace.t_end)
        )
    if coverage < min_coverage:
        return False, coverage, (
            "evidence covers only {0:.0%} of [{1:.2f}, {2:.2f}], so a response "
            "in the gap would not have been recorded".format(coverage, lo, hi)
        )
    return True, coverage, ""


def evaluate(
    formula: Formula,
    trace: EventTrace,
    t: float,
    binding: Binding,
    cfg: Optional[Config] = None,
) -> Verdict:
    """Evaluate ``formula`` at instant ``t`` of ``trace`` under ``binding``."""
    cfg = cfg if cfg is not None else Config({})
    min_coverage = float(cfg.get("formal.min_evidence_coverage", 0.8))
    return _evaluate(formula, trace, float(t), binding, min_coverage)


def _evaluate(
    formula: Formula,
    trace: EventTrace,
    t: float,
    binding: Binding,
    min_coverage: float,
) -> Verdict:
    if isinstance(formula, Occurs):
        return _occurs(formula, trace, t, binding)

    if isinstance(formula, Not):
        inner = _evaluate(formula.phi, trace, t, binding, min_coverage)
        if inner.status is CheckStatus.UNKNOWN:
            return Verdict(
                CheckStatus.UNKNOWN, inner.interval, reason=inner.reason,
                unobserved=inner.unobserved, coverage=inner.coverage,
            )
        flipped = (
            CheckStatus.FAIL if inner.status is CheckStatus.PASS else CheckStatus.PASS
        )
        return Verdict(
            flipped, inner.interval, witness=inner.witness,
            reason="negation of: {0}".format(inner.reason or render(formula.phi)),
        )

    if isinstance(formula, And):
        parts = [
            _evaluate(term, trace, t, binding, min_coverage)
            for term in formula.terms
        ]
        return _kleene_and(parts, (t, t), "every conjunct held")

    if isinstance(formula, Or):
        parts = [
            _evaluate(term, trace, t, binding, min_coverage)
            for term in formula.terms
        ]
        return _kleene_or(parts, (t, t), "no disjunct held")

    if isinstance(formula, Implies):
        antecedent = _evaluate(formula.antecedent, trace, t, binding, min_coverage)
        if antecedent.status is CheckStatus.FAIL:
            return Verdict(
                CheckStatus.PASS, (t, t),
                reason="the antecedent did not hold, so the implication is vacuous",
            )
        consequent = _evaluate(formula.consequent, trace, t, binding, min_coverage)
        if antecedent.status is CheckStatus.UNKNOWN:
            if consequent.status is CheckStatus.PASS:
                return consequent
            return Verdict(
                CheckStatus.UNKNOWN, (t, t), reason=antecedent.reason,
                unobserved=antecedent.unobserved,
            )
        return consequent

    if isinstance(formula, (Eventually, Once)):
        return _existential(formula, trace, t, binding, min_coverage)

    if isinstance(formula, (Always, Historically)):
        return _universal(formula, trace, t, binding, min_coverage)

    if isinstance(formula, Since):
        return _since(formula, trace, t, binding, min_coverage)

    raise TypeError("not a formula of this fragment: {0!r}".format(formula))


def _occurs(
    formula: Occurs, trace: EventTrace, t: float, binding: Binding
) -> Verdict:
    who = _resolve(formula.who, binding)
    about = _resolve(formula.about, binding)
    value = (
        formula.event_type.value if hasattr(formula.event_type, "value")
        else str(formula.event_type)
    )
    hits = trace.at(t, value, participant=who, subject=about)
    if hits:
        return Verdict(
            CheckStatus.PASS, (t, t), witness=[e.event_id for e in hits],
            reason="{0} at t={1:.2f}".format(value, t),
        )
    return Verdict(
        CheckStatus.FAIL, (t, t),
        reason="no {0} at t={1:.2f}".format(value, t),
    )


def _bounds(formula: Formula, t: float) -> Tuple[float, float]:
    """The absolute interval a metric operator looks at from ``t``."""
    if isinstance(formula, (Eventually, Always)):
        return (t + formula.lo, t + formula.hi)
    return (t - formula.hi, t - formula.lo)


def _existential(
    formula: Formula,
    trace: EventTrace,
    t: float,
    binding: Binding,
    min_coverage: float,
) -> Verdict:
    """``F`` and ``O``: does phi hold anywhere in the interval?"""
    lo, hi = _bounds(formula, t)
    for instant in trace.instants_in(lo, hi):
        inner = _evaluate(formula.phi, trace, instant, binding, min_coverage)
        if inner.status is CheckStatus.PASS:
            # A witness settles it. What was missed elsewhere in the window
            # cannot unmake something that was seen to happen.
            return Verdict(
                CheckStatus.PASS, (lo, hi), witness=inner.witness,
                reason=inner.reason,
            )
    observed, coverage, why = _window_status(trace, lo, hi, min_coverage)
    if not observed:
        return Verdict(
            CheckStatus.UNKNOWN, (lo, hi), reason=why, unobserved=True,
            coverage=coverage,
        )
    return Verdict(
        CheckStatus.FAIL, (lo, hi), coverage=coverage,
        reason="{0} never held in [{1:.2f}, {2:.2f}], which was fully observed"
               .format(render(formula.phi), lo, hi),
    )


def _since(
    formula: Since,
    trace: EventTrace,
    t: float,
    binding: Binding,
    min_coverage: float,
) -> Verdict:
    """Find the most recent marker, then check phi over the stretch since it.

    The two-stage shape is what gives this operator its value: the interval that
    phi has to hold over is not known until the marker is found, so its length
    varies with the run. That is exactly the situation a fixed-interval operator
    cannot express.
    """
    lo, hi = t - formula.hi, t - formula.lo
    marker_at: Optional[float] = None
    marker_witness: List[str] = []
    for instant in trace.instants_in(lo, hi):
        inner = _evaluate(formula.marker, trace, instant, binding, min_coverage)
        if inner.status is CheckStatus.PASS:
            marker_at, marker_witness = instant, inner.witness

    if marker_at is None:
        observed, coverage, why = _window_status(trace, lo, hi, min_coverage)
        if not observed:
            return Verdict(
                CheckStatus.UNKNOWN, (lo, hi), reason=why, unobserved=True,
                coverage=coverage,
            )
        return Verdict(
            CheckStatus.FAIL, (lo, hi), coverage=coverage,
            reason="{0} never held in [{1:.2f}, {2:.2f}]".format(
                render(formula.marker), lo, hi),
        )

    # The marker is inside the recording, so the stretch from it to now is too;
    # only a gap in the evidence can leave this undecided.
    for instant in trace.instants_in(marker_at, t):
        if instant <= marker_at + 1e-9:
            continue
        inner = _evaluate(formula.phi, trace, instant, binding, min_coverage)
        if inner.status is CheckStatus.FAIL:
            return Verdict(
                CheckStatus.FAIL, (marker_at, t), witness=inner.witness,
                reason="{0} failed at t={1:.2f}, after {2} at t={3:.2f}".format(
                    render(formula.phi), instant, render(formula.marker), marker_at),
            )
    coverage = trace.coverage_of(marker_at, t)
    if coverage < min_coverage:
        return Verdict(
            CheckStatus.UNKNOWN, (marker_at, t), coverage=coverage, unobserved=True,
            reason=(
                "evidence covers only {0:.0%} of the stretch since {1} at "
                "t={2:.2f}".format(coverage, render(formula.marker), marker_at)
            ),
        )
    return Verdict(
        CheckStatus.PASS, (marker_at, t), witness=marker_witness, coverage=coverage,
        reason="{0} held throughout [{1:.2f}, {2:.2f}], after {3}".format(
            render(formula.phi), marker_at, t, render(formula.marker)),
    )


def _universal(
    formula: Formula,
    trace: EventTrace,
    t: float,
    binding: Binding,
    min_coverage: float,
) -> Verdict:
    """``G`` and ``H``: does phi hold throughout the interval?"""
    lo, hi = _bounds(formula, t)
    for instant in trace.instants_in(lo, hi):
        inner = _evaluate(formula.phi, trace, instant, binding, min_coverage)
        if inner.status is CheckStatus.FAIL:
            # A counterexample settles it, for the same reason a witness does.
            return Verdict(
                CheckStatus.FAIL, (lo, hi), witness=inner.witness,
                reason="{0} failed at t={1:.2f}".format(render(formula.phi), instant),
            )
    observed, coverage, why = _window_status(trace, lo, hi, min_coverage)
    if not observed:
        return Verdict(
            CheckStatus.UNKNOWN, (lo, hi), reason=why, unobserved=True,
            coverage=coverage,
        )
    return Verdict(
        CheckStatus.PASS, (lo, hi), coverage=coverage,
        reason="{0} held throughout [{1:.2f}, {2:.2f}]"
               .format(render(formula.phi), lo, hi),
    )
