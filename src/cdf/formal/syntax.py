"""Metric temporal logic over a finite event trace: the formulae themselves.

The previous version of this project carried a ``formal`` field next to each
property -- an MTL-looking string, written by hand, sitting beside Python that
computed the verdict separately. Nothing checked that the two agreed, and the
string appeared in the report as though it had been evaluated. This module is the
correction: the formula *is* the thing that runs, so the rendering and the
verdict cannot drift apart because they are the same object.

The fragment is small on purpose -- occurrence atoms, the Boolean connectives,
and four metric operators, two looking forward and two back. Everything §18 asks
for is expressible in it, and a reader can hold all of it in mind at once.

Times are relative to the instant a formula is evaluated at, and intervals are
closed. ``Eventually(0.0, 1.5, Occurs(BRAKE_ONSET))`` at t means: some braking
begins between t and t + 1.5 s inclusive.

Three placeholders bind atoms to the participants a property is about. A property
fires at a trigger event, and that event supplies ``SELF`` -- the vehicle the
obligation falls on -- and ``SUBJECT``, the vehicle the obligation is about,
where there is one. ``ANY`` matches whatever is there, for the cases where the
claim genuinely does not care.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple, Union

from ..common.schemas import EventType

__all__ = [
    "SELF", "SUBJECT", "ANY",
    "Formula", "Occurs", "Not", "And", "Or", "Implies",
    "Eventually", "Always", "Once", "Historically", "Since",
    "render",
]

#: The vehicle the property is about -- the one the trigger event belongs to.
SELF = "self"
#: The other party, where the trigger names one (the vehicle in a pairwise event).
SUBJECT = "subject"
#: Any participant. Used where the claim does not depend on who.
ANY = "any"


@dataclass(frozen=True)
class Occurs:
    """An event of this type happens, here, to these participants.

    ``who`` constrains the event's ``participant_id`` and ``about`` its
    ``subject``. ``about=None`` means the atom does not constrain the subject at
    all, which is different from requiring the subject to be absent -- braking is
    braking whoever it was for.
    """

    event_type: EventType
    who: str = SELF
    about: Optional[str] = None

    def __str__(self) -> str:
        parts = [str(self.who)]
        if self.about is not None:
            parts.append(str(self.about))
        return "{0}({1})".format(_name(self.event_type), ", ".join(parts))


@dataclass(frozen=True)
class Not:
    phi: "Formula"

    def __str__(self) -> str:
        return "!({0})".format(self.phi)


@dataclass(frozen=True)
class And:
    terms: Tuple["Formula", ...]

    def __init__(self, *terms: "Formula") -> None:
        object.__setattr__(self, "terms", tuple(terms))

    def __str__(self) -> str:
        return "({0})".format(" & ".join(str(t) for t in self.terms))


@dataclass(frozen=True)
class Or:
    terms: Tuple["Formula", ...]

    def __init__(self, *terms: "Formula") -> None:
        object.__setattr__(self, "terms", tuple(terms))

    def __str__(self) -> str:
        return "({0})".format(" | ".join(str(t) for t in self.terms))


@dataclass(frozen=True)
class Implies:
    antecedent: "Formula"
    consequent: "Formula"

    def __str__(self) -> str:
        return "({0} -> {1})".format(self.antecedent, self.consequent)


@dataclass(frozen=True)
class Eventually:
    """``F[lo,hi] phi`` -- phi holds somewhere in the future interval."""

    lo: float
    hi: float
    phi: "Formula"

    def __str__(self) -> str:
        return "F[{0:g},{1:g}] {2}".format(self.lo, self.hi, self.phi)


@dataclass(frozen=True)
class Always:
    """``G[lo,hi] phi`` -- phi holds throughout the future interval."""

    lo: float
    hi: float
    phi: "Formula"

    def __str__(self) -> str:
        return "G[{0:g},{1:g}] {2}".format(self.lo, self.hi, self.phi)


@dataclass(frozen=True)
class Once:
    """``O[lo,hi] phi`` -- phi held somewhere in the past interval.

    Needed because several obligations are about the approach rather than the
    aftermath: whether a vehicle had already stopped before it crossed a line is
    a question about what is behind it.
    """

    lo: float
    hi: float
    phi: "Formula"

    def __str__(self) -> str:
        return "O[{0:g},{1:g}] {2}".format(self.lo, self.hi, self.phi)


@dataclass(frozen=True)
class Historically:
    """``H[lo,hi] phi`` -- phi held throughout the past interval."""

    lo: float
    hi: float
    phi: "Formula"

    def __str__(self) -> str:
        return "H[{0:g},{1:g}] {2}".format(self.lo, self.hi, self.phi)


@dataclass(frozen=True)
class Since:
    """``phi S[lo,hi] psi`` -- psi held in the past window, and phi ever since.

    This is the operator that makes "between the sign and the line" sayable, and
    nothing else in the fragment can say it. ``O[0,12] FULL_STOP`` asks whether a
    stop happened in the last twelve seconds, which is not the obligation: a stop
    made before the sign was even seen would satisfy it. What the rule actually
    requires is that nothing violated it *in the stretch between* the sign and
    now, and that stretch has a length the formula cannot know in advance --
    hence an operator that finds the marker and then looks forward from wherever
    it turned out to be.

    ``marker`` is searched for in ``[t-hi, t-lo]``, most recent first; ``phi``
    must then hold at every instant in ``(marker, t]``.
    """

    lo: float
    hi: float
    phi: "Formula"
    marker: "Formula"

    def __str__(self) -> str:
        return "({0} S[{1:g},{2:g}] {3})".format(self.phi, self.lo, self.hi,
                                                 self.marker)


Formula = Union[
    Occurs, Not, And, Or, Implies, Eventually, Always, Once, Historically, Since
]


def _name(event_type: Any) -> str:
    return (
        event_type.value if hasattr(event_type, "value") else str(event_type)
    )


def render(formula: Formula) -> str:
    """The formula as text, for reports and for the viewer.

    This is a rendering *of* the object that gets evaluated, not a parallel
    description of it, which is the entire point of building the AST.
    """
    return str(formula)
