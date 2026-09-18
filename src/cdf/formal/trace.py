"""What a formula is evaluated against: events, a horizon, and what was watched.

Three things have to be known about a trace before a metric formula can be
decided over it, and the third is the one usually left out.

The **events** are obvious. The **horizon** -- where the recording starts and
stops -- matters because ``F[0,2] brake`` asked half a second before the log ends
cannot be answered: the braking might be in the part that was never recorded.
Returning FAIL there would be asserting something about unobserved time.

**Coverage** is the same problem inside the recording. A sensor that dropped
samples across a window leaves a hole with the same epistemic status as the
region past the horizon: a response may have happened and not been recorded. So
the trace carries a coverage function, and the evaluator treats a poorly covered
window exactly as it treats an unobserved one.

A trace can be built from one vehicle's log, on its own clock, or from the merged
global log on common time. The evaluator does not care which, but the caller
must: running a property about two vehicles over a trace whose recorders were
never aligned compares timestamps that do not share an axis, so
:meth:`EventTrace.is_multi_participant_safe` exists to be asked.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.schemas import Event

LOGGER = logging.getLogger(__name__)

__all__ = ["EventTrace"]

#: Two event times closer than this are the same instant. One frame at 20 Hz.
EPSILON_S = 1e-6


@dataclass
class EventTrace:
    """A finite, bounded, partially observed sequence of events."""

    events: List[Event] = field(default_factory=list)
    t_start: float = 0.0
    t_end: float = 0.0
    coverage: Optional[Callable[[float, float], float]] = None
    time_axis: str = "local"
    """``"local"`` or ``"common"``. Recorded so a report can never be ambiguous
    about which clock its intervals are in."""
    aligned_participants: Tuple[str, ...] = ()
    """Participants whose events are on the shared axis. On a local trace this
    is the single recorder."""

    @classmethod
    def from_events(
        cls,
        events: Sequence[Event],
        t_start: Optional[float] = None,
        t_end: Optional[float] = None,
        coverage: Optional[Callable[[float, float], float]] = None,
        time_axis: str = "local",
        aligned_participants: Sequence[str] = (),
    ) -> "EventTrace":
        ordered = sorted(events, key=lambda e: (float(e.t_peak), e.event_id))
        if t_start is None:
            t_start = float(ordered[0].t_peak) if ordered else 0.0
        if t_end is None:
            t_end = float(ordered[-1].t_peak) if ordered else 0.0
        return cls(
            events=list(ordered),
            t_start=float(t_start),
            t_end=float(t_end),
            coverage=coverage,
            time_axis=time_axis,
            aligned_participants=tuple(sorted(aligned_participants)),
        )

    # -- the horizon ------------------------------------------------------

    def contains_window(self, lo: float, hi: float) -> bool:
        """Whether the whole of ``[lo, hi]`` lies inside what was recorded."""
        return (lo >= self.t_start - EPSILON_S) and (hi <= self.t_end + EPSILON_S)

    def observed_window(self, lo: float, hi: float) -> Tuple[float, float]:
        """The part of ``[lo, hi]`` that was actually recorded (may be empty)."""
        return (max(lo, self.t_start), min(hi, self.t_end))

    def coverage_of(self, lo: float, hi: float) -> float:
        """Fraction of ``[lo, hi]`` for which evidence exists, in [0, 1].

        A trace with no coverage function reports full coverage. That is right
        for a privileged trace, which is complete by construction, and is why a
        caller working from onboard recordings should always supply one.
        """
        if hi <= lo:
            return 1.0
        if self.coverage is None:
            return 1.0
        try:
            return float(max(0.0, min(1.0, self.coverage(lo, hi))))
        except (TypeError, ValueError):  # pragma: no cover - defensive
            LOGGER.warning("coverage function failed over [%s, %s]", lo, hi)
            return 0.0

    # -- sampling ---------------------------------------------------------

    def instants_in(self, lo: float, hi: float) -> List[float]:
        """The instants at which a formula can change truth value in a window.

        Every atom in this fragment is an event occurrence, so the truth of any
        formula is constant between consecutive event times. Sampling at the
        event times inside the window is therefore exact rather than an
        approximation, which is the reason the fragment is restricted to
        occurrence atoms in the first place.
        """
        out: List[float] = []
        for event in self.events:
            t = float(event.t_peak)
            if lo - EPSILON_S <= t <= hi + EPSILON_S:
                if not out or abs(out[-1] - t) > EPSILON_S:
                    out.append(t)
        return out

    def at(
        self,
        t: float,
        event_type: str,
        participant: Optional[str] = None,
        subject: Optional[str] = None,
    ) -> List[Event]:
        """Events of this type at this instant, matching the bound participants.

        ``participant`` or ``subject`` of ``None`` means unconstrained.
        """
        out: List[Event] = []
        for event in self.events:
            if abs(float(event.t_peak) - float(t)) > EPSILON_S:
                continue
            value = (
                event.event_type.value if hasattr(event.event_type, "value")
                else str(event.event_type)
            )
            if value != event_type:
                continue
            if participant is not None and str(event.participant_id) != str(participant):
                continue
            if subject is not None and str(event.subject or "") != str(subject):
                continue
            out.append(event)
        return out

    def of_type(self, event_type: str) -> List[Event]:
        """Every event of a type, in time order. Used to find property triggers."""
        return [
            e for e in self.events
            if (e.event_type.value if hasattr(e.event_type, "value")
                else str(e.event_type)) == event_type
        ]

    # -- what the trace is safe to be asked -------------------------------

    def participants(self) -> Tuple[str, ...]:
        return tuple(sorted({str(e.participant_id) for e in self.events}))

    def is_multi_participant_safe(self) -> bool:
        """Whether timestamps from different vehicles may be compared here.

        A property relating one vehicle's braking to another's conflict entry is
        meaningless unless the two recorders share an axis. On a local trace
        there is only one recorder, so the question does not arise; on a merged
        trace it arises for every participant whose clock was never tied in.
        """
        present = set(self.participants())
        if len(present) <= 1:
            return True
        return present.issubset(set(self.aligned_participants))

    def describe(self) -> Dict[str, Any]:
        return {
            "n_events": len(self.events),
            "t_start": round(self.t_start, 4),
            "t_end": round(self.t_end, 4),
            "duration_s": round(self.t_end - self.t_start, 4),
            "time_axis": self.time_axis,
            "participants": list(self.participants()),
            "aligned_participants": list(self.aligned_participants),
            "multi_participant_safe": self.is_multi_participant_safe(),
            "has_coverage_model": self.coverage is not None,
        }
