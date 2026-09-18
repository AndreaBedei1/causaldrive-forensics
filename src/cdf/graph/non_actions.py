"""Asserting that something did not happen.

Most of this project's events are claims that something *did* occur, and the
evidence for them is a signal. A non-action is the opposite claim -- that a
required response was absent -- and the evidence for it is the absence of a
signal, which is a much weaker thing to stand on. Absence of evidence becomes
evidence of absence only when you were actually looking, so every non-action
here has to earn four things before it exists:

1. **a real observed obligation or opportunity.** A stop sign the camera saw; a
   critical time-to-collision the radar measured. Never "the scenario configured
   a brake here" -- a non-action created from the scenario's intent would be
   measuring the experiment rather than the world, and would make the design
   reference and the reconstruction agree by construction.
2. **a bounded interval.** "B never yielded" is not checkable; "B did not
   decelerate between first seeing the sign and crossing the line" is.
3. **evidence covering that interval.** If the recorder dropped samples across
   the window, the response may simply not have been recorded. That is an
   ``UNKNOWN``, which this module reports separately and does *not* turn into a
   node.
4. **no qualifying response inside it.**

The fourth is the easy one. The third is the one that keeps the metric honest,
because a detector that skipped it would score its best on the runs where the
sensors worked worst.

Both the reconstruction and the privileged reference run through this same
module, from their own events and their own coverage. That is deliberate: the
rule for what counts as a non-action should not differ between the thing being
measured and the thing measuring it, or the comparison stops being about
whether the vehicle noticed and starts being about whose rule was laxer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import (
    Any, Callable, Dict, FrozenSet, List, Mapping, Optional, Sequence, Tuple,
)

from ..common.config import Config
from ..common.schemas import Event, EventType, Evidence, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = [
    "NON_ACTION_RULES",
    "NonActionRule",
    "build_non_actions",
]


@dataclass(frozen=True)
class NonActionRule:
    """One way a required response can be observed to be missing.

    ``opens`` are the event types that create the obligation or the opportunity.
    ``discharges`` are the ones that would satisfy it. ``window`` says where to
    look relative to the opening event, and ``closes`` -- when given -- means the
    window runs to the next event of that type instead of for a fixed horizon,
    which is how "did not stop *before crossing the line*" is expressed.
    """

    event_type: EventType
    opens: FrozenSet[str]
    discharges: FrozenSet[str]
    horizon_s: float
    rule_id: str
    obligation: str
    closes: Optional[FrozenSet[str]] = None
    lead_in: bool = False
    """Look *backwards* from the opening event rather than forwards.

    Entering a conflict region without having slowed is a claim about the
    approach, not about what happened afterwards.
    """
    requires_present: Optional[FrozenSet[str]] = None
    """Types that must be present in the window for the claim to hold.

    Only ``CONTINUED_ACCELERATION_DURING_CONFLICT`` uses this: it asserts that
    the vehicle went on accelerating, which is a presence rather than an
    absence, and belongs in this family because it is the same kind of claim
    about a response opportunity.
    """
    pairwise: bool = True
    """Whether the non-action concerns the vehicle the obligation came from.

    A missing brake is a failure to respond *to something*, so it carries that
    subject. A missing stop at a sign has no second vehicle and carries none.
    """


#: The rules, stated once. Each says what opens the window, what would close it
#: satisfactorily, and how long a reasonable response has.
NON_ACTION_RULES: Tuple[NonActionRule, ...] = (
    NonActionRule(
        event_type=EventType.NO_STOP_AFTER_STOP_SIGN,
        opens=frozenset({EventType.STOP_SIGN_DETECTED.value}),
        closes=frozenset({EventType.STOP_LINE_CROSSED.value}),
        discharges=frozenset({EventType.FULL_STOP.value}),
        horizon_s=12.0,
        rule_id="NA1",
        obligation="a stop sign was seen and its stop line was then crossed",
        pairwise=False,
    ),
    NonActionRule(
        event_type=EventType.NO_BRAKING_RESPONSE,
        opens=frozenset({EventType.CRITICAL_TTC.value}),
        discharges=frozenset({
            EventType.BRAKE_ONSET.value,
            EventType.HARD_BRAKE.value,
            EventType.DECELERATION.value,
            EventType.HARD_DECELERATION.value,
            EventType.FULL_STOP.value,
        }),
        horizon_s=1.5,
        rule_id="NA2",
        obligation="time-to-collision became critical",
    ),
    NonActionRule(
        event_type=EventType.NO_EVASIVE_RESPONSE,
        opens=frozenset({EventType.CRITICAL_TTC.value}),
        discharges=frozenset({
            EventType.STEER_ONSET.value,
            EventType.SIGNIFICANT_HEADING_CHANGE.value,
            EventType.LANE_CHANGE_LIKE_MANEUVER.value,
        }),
        horizon_s=1.5,
        rule_id="NA3",
        obligation="time-to-collision became critical",
    ),
    NonActionRule(
        event_type=EventType.NO_YIELD_RESPONSE,
        opens=frozenset({EventType.YIELD_SIGN_DETECTED.value}),
        closes=frozenset({EventType.CONFLICT_REGION_ENTRY.value}),
        discharges=frozenset({
            EventType.FULL_STOP.value,
            EventType.DECELERATION.value,
            EventType.HARD_DECELERATION.value,
            EventType.BRAKE_ONSET.value,
        }),
        horizon_s=12.0,
        rule_id="NA4",
        obligation="a yield sign was seen and a conflict region was then entered",
        pairwise=False,
    ),
    NonActionRule(
        event_type=EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION,
        opens=frozenset({EventType.CONFLICT_REGION_ENTRY.value}),
        discharges=frozenset({
            EventType.DECELERATION.value,
            EventType.HARD_DECELERATION.value,
            EventType.BRAKE_ONSET.value,
            EventType.HARD_BRAKE.value,
            EventType.FULL_STOP.value,
        }),
        horizon_s=2.5,
        rule_id="NA5",
        obligation="a conflict region was entered",
        lead_in=True,
    ),
    NonActionRule(
        event_type=EventType.CONTINUED_ACCELERATION_DURING_CONFLICT,
        opens=frozenset({
            EventType.CRITICAL_TTC.value,
            EventType.LOW_TTC.value,
        }),
        discharges=frozenset(),
        requires_present=frozenset({
            EventType.THROTTLE_ONSET.value,
            EventType.ACCELERATION.value,
        }),
        horizon_s=2.0,
        rule_id="NA6",
        obligation="time-to-collision was low or critical",
    ),
)


def _type_of(event: Event) -> str:
    return (
        event.event_type.value if hasattr(event.event_type, "value")
        else str(event.event_type)
    )


def _window_for(
    rule: NonActionRule,
    opening: Event,
    own_events: Sequence[Event],
) -> Optional[Tuple[float, float, Optional[Event]]]:
    """The interval to watch, and the event that closed it if one did.

    Returns ``None`` when the rule needs a closing event and none occurred: a
    stop sign nobody then drove past is not a failure to stop, it is a vehicle
    that has not reached the line yet, and asserting a non-action there would be
    inventing one.
    """
    t0 = float(opening.t_peak)
    if rule.lead_in:
        return (t0 - rule.horizon_s, t0, None)
    if rule.closes:
        later = [
            e for e in own_events
            if _type_of(e) in rule.closes and float(e.t_peak) > t0
            and float(e.t_peak) - t0 <= rule.horizon_s
        ]
        if not later:
            return None
        closing = min(later, key=lambda e: float(e.t_peak))
        return (t0, float(closing.t_peak), closing)
    return (t0, t0 + rule.horizon_s, None)


def _matches_subject(event: Event, subject: Optional[str]) -> bool:
    """Whether a response event answers an obligation about ``subject``.

    Own-motion responses have no subject of their own -- braking is braking,
    whoever it was for -- so they answer any obligation. A pairwise response is
    only an answer if it concerns the same vehicle.
    """
    if subject is None or not event.subject:
        return True
    return str(event.subject) == str(subject)


def build_non_actions(
    participant_id: str,
    events: Sequence[Event],
    coverage: Optional[Callable[[float, float], float]] = None,
    cfg: Optional[Config] = None,
    provenance: Provenance = Provenance.LOCAL,
    id_prefix: str = "na",
) -> Dict[str, Any]:
    """Derive this participant's non-actions from what it actually observed.

    ``coverage(t0, t1)`` returns the fraction of the interval for which evidence
    exists, between 0 and 1. Passing ``None`` means "fully covered", which is
    right for a privileged trace and wrong for a recorder -- a caller working
    from onboard data should supply a real one.

    Returns the events, and beside them the windows that were opened but could
    not be judged, so a reader can see what the detector declined to claim.
    """
    cfg = cfg if cfg is not None else Config({})
    min_coverage = float(cfg.get("non_actions.min_evidence_coverage", 0.8))

    own = [e for e in events if str(e.participant_id) == str(participant_id)]
    own_sorted = sorted(own, key=lambda e: (float(e.t_peak), e.event_id))

    out: List[Event] = []
    unknown: List[Dict[str, Any]] = []
    seen: set = set()

    for rule in NON_ACTION_RULES:
        for opening in own_sorted:
            if _type_of(opening) not in rule.opens:
                continue
            window = _window_for(rule, opening, own_sorted)
            if window is None:
                continue
            t0, t1, closing = window
            if t1 <= t0:
                continue

            covered = 1.0 if coverage is None else float(coverage(t0, t1))
            if covered < min_coverage:
                # The window was opened but not watched well enough to say
                # anything about it. This is the UNKNOWN case, and it stays out
                # of the graph: a node here would be a claim the evidence does
                # not support.
                unknown.append({
                    "event_type": rule.event_type.value,
                    "rule_id": rule.rule_id,
                    "participant_id": str(participant_id),
                    "subject": str(opening.subject) if opening.subject else None,
                    "monitored_interval": [round(t0, 4), round(t1, 4)],
                    "evidence_coverage": round(covered, 4),
                    "required_coverage": min_coverage,
                    "verdict": "UNKNOWN",
                    "reason": (
                        "the obligation was observed, but evidence covers only "
                        "{0:.0%} of the interval in which a response would have "
                        "appeared, so its absence cannot be asserted".format(covered)
                    ),
                })
                continue

            subject = str(opening.subject) if opening.subject else None
            in_window = [
                e for e in own_sorted
                if t0 <= float(e.t_peak) <= t1 and e.event_id != opening.event_id
            ]

            if rule.requires_present is not None:
                present = [
                    e for e in in_window if _type_of(e) in rule.requires_present
                ]
                if not present:
                    continue
                supporting = present
            else:
                discharged = [
                    e for e in in_window
                    if _type_of(e) in rule.discharges and _matches_subject(e, subject)
                ]
                if discharged:
                    continue
                supporting = []

            # One claim per (type, participant, subject, window). A vehicle that
            # sees the same threat resolved into several radar events should not
            # be accused of the same non-response several times.
            key = (rule.event_type.value, subject, round(t0, 2), round(t1, 2))
            if key in seen:
                continue
            seen.add(key)

            evidence = [Evidence(
                kind="event",
                ref=opening.event_id,
                t_start=t0,
                t_end=t1,
                detail={"role": "opened the obligation"},
            )]
            if closing is not None:
                evidence.append(Evidence(
                    kind="event", ref=closing.event_id, t_start=t0, t_end=t1,
                    detail={"role": "closed the window"},
                ))
            for support in supporting[:4]:
                evidence.append(Evidence(
                    kind="event", ref=support.event_id,
                    t_start=float(support.t_start), t_end=float(support.t_peak),
                    detail={"role": "the response that should not have continued"},
                ))

            out.append(Event(
                event_id="{0}-{1}-{2}-{3:.2f}".format(
                    id_prefix, rule.rule_id, participant_id, t0
                ),
                event_type=rule.event_type,
                participant_id=str(participant_id),
                t_start=t0,
                t_peak=t1,
                t_end=t1,
                subject=subject if rule.pairwise else None,
                values={
                    "monitored_s": round(t1 - t0, 4),
                    "evidence_coverage": round(covered, 4),
                },
                detail={
                    "rule_id": rule.rule_id,
                    "obligation": rule.obligation,
                    "monitored_interval": [round(t0, 4), round(t1, 4)],
                    "evidence_coverage": round(covered, 4),
                    "required_coverage": min_coverage,
                    "opened_by": opening.event_id,
                    "closed_by": closing.event_id if closing is not None else None,
                    "would_have_been_discharged_by": sorted(rule.discharges),
                    "verdict": "ASSERTED",
                },
                # Coverage is the whole basis of the claim, so it is also the
                # confidence: a window watched 82% of the time supports a
                # weaker assertion than one watched throughout.
                confidence=round(covered, 4),
                evidence=evidence,
                provenance=provenance,
                source_sensors=[],
            ))

    out.sort(key=lambda e: (float(e.t_peak), e.event_id))
    return {
        "events": out,
        "unknown": unknown,
        "n_asserted": len(out),
        "n_unknown": len(unknown),
        "note": (
            "a non-action is only asserted where an obligation was actually "
            "observed, the interval was bounded, and evidence covered it. "
            "Windows that failed the coverage test are listed as UNKNOWN rather "
            "than resolved either way"
        ),
    }


def coverage_from_samples(
    times: Sequence[float],
    expected_period_s: float,
    max_gap_factor: float = 3.0,
) -> Callable[[float, float], float]:
    """A coverage function built from when a sensor actually produced samples.

    Counts the fraction of an interval *not* inside a gap. A gap is a stretch
    between consecutive samples longer than ``max_gap_factor`` sampling periods;
    shorter ones are ordinary jitter and are not held against the recorder. An
    interval reaching beyond the recording is uncovered for the part that lies
    outside, which is what makes a window running past the end of a log honest
    rather than silently short.
    """
    ordered = sorted(float(t) for t in times)
    period = max(float(expected_period_s), 1e-6)
    threshold = period * float(max_gap_factor)

    def coverage(t0: float, t1: float) -> float:
        span = float(t1) - float(t0)
        if span <= 0.0:
            return 0.0
        if not ordered:
            return 0.0
        uncovered = 0.0
        # Anything before the first sample or after the last is not covered.
        uncovered += max(0.0, min(ordered[0], t1) - t0)
        uncovered += max(0.0, t1 - max(ordered[-1], t0))
        for i in range(len(ordered) - 1):
            a, b = ordered[i], ordered[i + 1]
            if b <= t0 or a >= t1:
                continue
            if b - a <= threshold:
                continue
            uncovered += max(0.0, min(b, t1) - max(a, t0))
        return float(max(0.0, min(1.0, 1.0 - uncovered / span)))

    return coverage
