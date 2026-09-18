"""The properties from the brief, as formulae rather than as prose.

Each one is a trigger and a formula. The trigger says which events open an
obligation; the formula says what must then hold, evaluated at the instant the
trigger fired with that event's participants bound. A property with no trigger in
a run is *vacuous*, reported as such and kept out of the accuracy figures --
counting "the vehicle never met a stop sign" as a pass would quietly inflate
every aggregate.

A note on what these are and are not. ``NO_STOP_AFTER_STOP_SIGN`` is an event in
the graph; ``P1`` here is a property over the trace. They overlap deliberately
and are checked against each other by P8, because two independent routes to the
same conclusion that disagree mean one of them is wrong -- which is worth
knowing, and is invisible if only one exists.

Nothing here mentions legal fault. A property failure is a normative violation
against a stated benchmark rule, which is what the responsibility layer consumes;
what a court would make of it is not a question this project can answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from ..common.schemas import EventType, Provenance
from .syntax import (
    ANY, SELF, SUBJECT,
    Always, And, Eventually, Formula, Historically, Implies, Not, Occurs, Once,
    Or, Since, render,
)

__all__ = ["PROPERTIES", "TemporalProperty", "property_by_id"]


@dataclass(frozen=True)
class TemporalProperty:
    """A named obligation: what opens it, and what must then be true."""

    property_id: str
    title: str
    trigger: EventType
    formula: Formula
    rationale: str
    benchmark_rule: Optional[str] = None
    """The stated rule this checks against, where it is a traffic-control rule
    rather than a physical-safety one. Named so a reader can see that the rule
    is a benchmark chosen for this experiment, not a universal legal one."""
    needs_two_vehicles: bool = False
    """Whether the formula relates events from two recorders, and so requires a
    trace whose clocks were actually aligned."""
    anchor: str = "t_peak"
    """Which instant of the trigger event the formula is evaluated at.

    Almost always the peak, which for an ordinary event is when it happened. A
    non-action is the exception: its t_peak is the *end* of the window it
    monitored, and the claim is about the whole of that window, so it anchors at
    t_start instead. Evaluating it at the peak would look for the response after
    the window it was supposed to be inside.
    """
    also_triggered_by: Tuple[EventType, ...] = ()
    """Further events that open the same obligation.

    One obligation can have more than one observable boundary, and insisting on a
    single one can make a property unfalsifiable in practice. The stop rule is
    the case that forced this: its natural boundary is the painted stop line, and
    Town05 paints no stop bar at any junction where it renders a stop sign, so
    ``STOP_LINE_CROSSED`` never fires on a real run and P1 was permanently
    vacuous. The vehicle still crosses into the junction, and its lane sensor
    records that.

    Adding a boundary does not weaken the property. The formula is an
    implication whose antecedent is "a stop sign was seen in the last twelve
    seconds", so a trigger that fires where no sign was seen -- an ordinary lane
    change -- is vacuously satisfied rather than violated.
    """

    @property
    def trigger_types(self) -> Tuple[EventType, ...]:
        """Every event that opens this obligation, the primary one first."""
        out = [self.trigger]
        for extra in self.also_triggered_by:
            if extra not in out:
                out.append(extra)
        return tuple(out)

    def describe(self) -> Dict[str, Any]:
        return {
            "property_id": self.property_id,
            "title": self.title,
            "trigger": self.trigger.value,
            "triggers": [t.value for t in self.trigger_types],
            "formula": render(self.formula),
            "rationale": self.rationale,
            "benchmark_rule": self.benchmark_rule,
            "needs_two_vehicles": self.needs_two_vehicles,
            "anchor": self.anchor,
        }


# --- A. stop before the line ----------------------------------------------

#: Crossing a stop line after seeing a stop sign requires a full stop in
#: between. Expressed from the crossing rather than the sign, because that is
#: the instant the obligation comes due and the interval behind it is bounded.
P1 = TemporalProperty(
    property_id="P1",
    title="a stop sign seen means a full stop before the line",
    trigger=EventType.STOP_LINE_CROSSED,
    # Town05 paints no stop bar at any junction where it renders a stop sign, so
    # on a real run the line is never seen to be crossed and this property could
    # never fire. Crossing into the junction is the same boundary by another
    # observation, and the lane sensor records it.
    also_triggered_by=(EventType.LANE_MARKING_CROSSED,),
    formula=Implies(
        Once(0.0, 12.0, Occurs(EventType.STOP_SIGN_DETECTED, who=SELF)),
        Not(Since(
            0.0, 12.0,
            Not(Occurs(EventType.FULL_STOP, who=SELF)),
            Occurs(EventType.STOP_SIGN_DETECTED, who=SELF),
        )),
    ),
    rationale=(
        "the stop has to fall between seeing the sign and reaching the line, "
        "which is why this needs Since rather than Once. O[0,12] FULL_STOP would "
        "be satisfied by a stop made before the sign was ever seen -- at a "
        "previous junction, say -- which is not the obligation"
    ),
    benchmark_rule=(
        "a vehicle facing a stop sign must come to a complete stop before the "
        "stop line. Stated as the benchmark rule for this experiment"
    ),
)

# --- B. yield response ------------------------------------------------------

P2 = TemporalProperty(
    property_id="P2",
    title="a yield sign seen means yielding before conflict entry",
    trigger=EventType.CONFLICT_REGION_ENTRY,
    formula=Implies(
        Once(0.0, 12.0, Occurs(EventType.YIELD_SIGN_DETECTED, who=SELF)),
        Not(Since(
            0.0, 12.0,
            Not(Or(
                Occurs(EventType.FULL_STOP, who=SELF),
                Occurs(EventType.DECELERATION, who=SELF),
                Occurs(EventType.HARD_DECELERATION, who=SELF),
                Occurs(EventType.BRAKE_ONSET, who=SELF),
            )),
            Occurs(EventType.YIELD_SIGN_DETECTED, who=SELF),
        )),
    ),
    rationale=(
        "the same shape as P1: yielding is a behaviour between seeing the sign "
        "and entering the conflict, so the window is set by the sign rather than "
        "by a constant"
    ),
    benchmark_rule=(
        "a vehicle facing a yield sign must give way to conflicting traffic "
        "before entering the conflict region. Benchmark rule for this experiment"
    ),
)

# --- C. response to a critical time-to-collision ---------------------------

P3 = TemporalProperty(
    property_id="P3",
    title="a critical time-to-collision gets a response",
    trigger=EventType.CRITICAL_TTC,
    formula=Eventually(0.0, 1.5, Or(
        Occurs(EventType.BRAKE_ONSET, who=SELF),
        Occurs(EventType.HARD_BRAKE, who=SELF),
        Occurs(EventType.HARD_DECELERATION, who=SELF),
        Occurs(EventType.DECELERATION, who=SELF),
        Occurs(EventType.STEER_ONSET, who=SELF),
        Occurs(EventType.SIGNIFICANT_HEADING_CHANGE, who=SELF),
    )),
    rationale=(
        "braking and swerving are both responses; the property is about whether "
        "the vehicle did anything, not about which of the two it chose"
    ),
)

# --- D. no acceleration into a critical conflict ---------------------------

P4 = TemporalProperty(
    property_id="P4",
    title="no acceleration into a critical conflict",
    trigger=EventType.CRITICAL_TTC,
    formula=Always(0.0, 2.0, And(
        Not(Occurs(EventType.THROTTLE_ONSET, who=SELF)),
        Not(Occurs(EventType.ACCELERATION, who=SELF)),
    )),
    rationale=(
        "distinct from P3 on purpose: a vehicle can brake and then accelerate "
        "again, which satisfies 'responded' while still making things worse"
    ),
)

# --- E. impact response -----------------------------------------------------

P5 = TemporalProperty(
    property_id="P5",
    title="a collision is followed by coming to rest",
    trigger=EventType.COLLISION,
    formula=Eventually(0.0, 8.0, Or(
        Occurs(EventType.POST_IMPACT_STOP, who=SELF),
        Occurs(EventType.FULL_STOP, who=SELF),
    )),
    rationale=(
        "the one property most often UNKNOWN rather than decided, because a "
        "collision near the end of a 25 s window leaves the eight seconds after "
        "it unrecorded. That is the correct answer there, not a failure"
    ),
)

# --- F. solid-line compliance ----------------------------------------------

P6 = TemporalProperty(
    property_id="P6",
    title="a solid line is not crossed",
    trigger=EventType.SOLID_LINE_CROSSED,
    formula=Not(Occurs(EventType.SOLID_LINE_CROSSED, who=SELF)),
    rationale=(
        "trivially false whenever it fires, which is the point: the trigger is "
        "the violation. Written this way so that the report carries the crossing "
        "as a located counterexample rather than as a bare count"
    ),
    benchmark_rule=(
        "a solid lane line may not be crossed. Benchmark rule for this "
        "experiment; real road rules admit exceptions this does not model"
    ),
)

# --- G. multi-impact order --------------------------------------------------

P7 = TemporalProperty(
    property_id="P7",
    title="one impact per pair on the merged timeline",
    trigger=EventType.COLLISION,
    formula=Always(
        0.1, 5.0, Not(Occurs(EventType.COLLISION, who=SELF, about=SUBJECT)),
    ),
    rationale=(
        "in a chain the merged log must contain each impact once. Two vehicles "
        "each reporting the same contact, badly aligned, shows up as the same "
        "pair colliding twice a fraction of a second apart -- which is a "
        "reconstruction failure and is visible from the trace alone. Note what "
        "this does *not* check: whether the two impacts of a chain are in the "
        "right order. Nothing internal to a trace can say that, because a "
        "consistently wrong order is still self-consistent; order correctness is "
        "measured against ground truth in the reconstruction metrics instead"
    ),
    needs_two_vehicles=True,
)

# --- H. non-action consistency ---------------------------------------------

P8 = TemporalProperty(
    property_id="P8",
    title="a claimed missing braking response really had no response",
    trigger=EventType.NO_BRAKING_RESPONSE,
    formula=And(
        Once(0.0, 3.0, Occurs(EventType.CRITICAL_TTC, who=SELF)),
        Not(Eventually(0.0, 1.5, Or(
            Occurs(EventType.BRAKE_ONSET, who=SELF),
            Occurs(EventType.HARD_BRAKE, who=SELF),
            Occurs(EventType.HARD_DECELERATION, who=SELF),
            Occurs(EventType.DECELERATION, who=SELF),
        ))),
    ),
    rationale=(
        "checks the non-action detector against the trace by a second route. "
        "The two agreeing proves little; the two disagreeing means one of them "
        "is wrong, and that is worth being able to see"
    ),
    # A non-action node spans the window it watched, and t_peak is the end of
    # it. Anchoring here at t_start puts the response window back where the
    # detector had it; anchoring at the peak would search the 1.5 s *after* the
    # window and find nothing, so every non-action would confirm itself.
    anchor="t_start",
)


#: Every property, in the order the brief lists them.
PROPERTIES: Tuple[TemporalProperty, ...] = (P1, P2, P3, P4, P5, P6, P7, P8)


def property_by_id(property_id: str) -> TemporalProperty:
    for prop in PROPERTIES:
        if prop.property_id == property_id:
            return prop
    raise KeyError("no such property: {0!r}".format(property_id))
