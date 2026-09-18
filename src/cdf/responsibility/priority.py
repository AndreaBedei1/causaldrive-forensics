"""Who had priority, under a rule this experiment states rather than inherits.

Right of way is where a forensic reconstruction is most tempted to overreach.
The three cases below are decidable from observable evidence; real traffic law is
not, and the gap between them is not something more code can close. So the rule
used here is written out in full, attached to every verdict it produces, and
labelled a benchmark -- a convention adopted for this experiment so that results
are comparable across runs, not a claim about any jurisdiction.

The three cases
---------------

**One vehicle faces a stop sign.** That vehicle must stop; the other has
benchmark priority. This is the clearest case and the one the scenarios lean on.

**Both face stop signs.** Both must stop. Priority then goes to whichever
completed its stop clearly first -- first to stop, first to go.

**Neither faces one.** Nothing here decides it, and the verdict says so rather
than reaching for a default.

The part that matters most
--------------------------

"Clearly first" needs a threshold, and two vehicles that stopped within a tenth
of a second of each other were not clearly anything. Rather than break the tie,
the answer is ``AMBIGUOUS_PRIORITY``: a real outcome, reported as such, and not a
failure of the method. A right-side tie-break is applied only where a scenario
explicitly configures one, because it is a local convention rather than a
universal, and silently applying it would put a jurisdiction's rule into results
that do not name one.

Everything is computed from observed events -- which vehicle saw a sign, when
each came to rest. The privileged map is not consulted; the reference builds the
same structure from privileged traffic control, and the two are compared.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.schemas import Event, EventType

LOGGER = logging.getLogger(__name__)

__all__ = ["PRIORITY_VERDICTS", "benchmark_priority"]

#: Every verdict this module can return.
PRIORITY_VERDICTS = (
    "PRIORITY_TO_UNCONTROLLED",   # one vehicle faced a sign, the other did not
    "PRIORITY_BY_ARRIVAL",        # both faced signs; one stopped clearly first
    "PRIORITY_BY_CONFIGURED_TIE_BREAK",
    "AMBIGUOUS_PRIORITY",
    "NO_CONTROL_OBSERVED",
)

#: The benchmark, stated once and attached to every verdict.
BENCHMARK_RULE = (
    "Benchmark right-of-way rule adopted for this experiment, not a statement "
    "of law in any jurisdiction: (1) where one approach is controlled by a stop "
    "sign and the other is not, the uncontrolled approach has priority; (2) "
    "where both are controlled, priority goes to the vehicle that completed its "
    "stop first by a clear margin; (3) where neither holds, priority is "
    "ambiguous and is reported as such"
)


def _type_of(event: Event) -> str:
    return (
        event.event_type.value if hasattr(event.event_type, "value")
        else str(event.event_type)
    )


def _first_at(events: Sequence[Event], pid: str, kind: str) -> Optional[float]:
    times = [
        float(e.t_peak) for e in events
        if str(e.participant_id) == pid and _type_of(e) == kind
    ]
    return min(times) if times else None


def benchmark_priority(
    events: Sequence[Event],
    participants: Optional[Sequence[str]] = None,
    cfg: Optional[Config] = None,
    tie_break: Optional[str] = None,
) -> Dict[str, Any]:
    """Decide priority between the vehicles in a conflict, or decline to.

    ``tie_break`` is the scenario's explicitly configured tie-break, if it has
    one -- a participant id, meaning "this vehicle wins a simultaneous arrival
    under the convention this scenario declares". Left ``None``, a simultaneous
    arrival stays ambiguous.
    """
    cfg = cfg if cfg is not None else Config({})
    margin = float(cfg.get("responsibility.priority.clear_margin_s", 0.5))

    pids = sorted(participants or {str(e.participant_id) for e in events})
    controlled = {
        pid: _first_at(events, pid, EventType.STOP_SIGN_DETECTED.value)
        for pid in pids
    }
    stopped = {
        pid: _first_at(events, pid, EventType.FULL_STOP.value) for pid in pids
    }
    facing = sorted(p for p in pids if controlled[p] is not None)
    free = sorted(p for p in pids if controlled[p] is None)

    base = {
        "participants": pids,
        "benchmark_rule": BENCHMARK_RULE,
        "stop_sign_seen_by": facing,
        "no_stop_sign_seen_by": free,
        "stop_completed_at": {
            p: None if v is None else round(v, 4) for p, v in sorted(stopped.items())
        },
        "clear_margin_s": margin,
    }

    if not facing:
        return dict(base, **{
            "verdict": "NO_CONTROL_OBSERVED",
            "has_priority": None,
            "must_stop": [],
            "reason": (
                "no vehicle observed a stop sign, so this benchmark has nothing "
                "to decide from. It does not follow that no rule applied -- only "
                "that none was observed"
            ),
        })

    if len(facing) == 1 and len(free) == 1:
        return dict(base, **{
            "verdict": "PRIORITY_TO_UNCONTROLLED",
            "has_priority": free[0],
            "must_stop": facing,
            "reason": (
                "{0} faced a stop sign and {1} did not, so under the benchmark "
                "rule {1} has priority and {0} must stop".format(facing[0], free[0])
            ),
        })

    if len(facing) >= 2:
        completed = {p: stopped[p] for p in facing if stopped[p] is not None}
        if len(completed) < len(facing):
            missing = sorted(set(facing) - set(completed))
            return dict(base, **{
                "verdict": "AMBIGUOUS_PRIORITY",
                "has_priority": None,
                "must_stop": facing,
                "did_not_complete_a_stop": missing,
                "reason": (
                    "both approaches are controlled, but {0} never completed a "
                    "stop, so the first-to-stop ordering the rule depends on "
                    "does not exist. Whether {0} failed to stop is a separate "
                    "question and is answered by the stop-rule violation, not "
                    "here".format(", ".join(missing))
                ),
            })
        order = sorted(completed.items(), key=lambda kv: (kv[1], kv[0]))
        gap = float(order[1][1] - order[0][1])
        if gap >= margin:
            return dict(base, **{
                "verdict": "PRIORITY_BY_ARRIVAL",
                "has_priority": order[0][0],
                "must_stop": facing,
                "arrival_gap_s": round(gap, 4),
                "reason": (
                    "both stopped; {0} completed its stop {1:.2f} s before {2}, "
                    "which clears the {3:.2f} s margin, so {0} has priority"
                    .format(order[0][0], gap, order[1][0], margin)
                ),
            })
        if tie_break and tie_break in facing:
            return dict(base, **{
                "verdict": "PRIORITY_BY_CONFIGURED_TIE_BREAK",
                "has_priority": tie_break,
                "must_stop": facing,
                "arrival_gap_s": round(gap, 4),
                "reason": (
                    "the two stops are {0:.2f} s apart, inside the {1:.2f} s "
                    "margin, so arrival does not decide it. This scenario "
                    "explicitly configures a tie-break in favour of {2}; it is a "
                    "local convention, applied here only because the scenario "
                    "declares it".format(gap, margin, tie_break)
                ),
            })
        return dict(base, **{
            "verdict": "AMBIGUOUS_PRIORITY",
            "has_priority": None,
            "must_stop": facing,
            "arrival_gap_s": round(gap, 4),
            "reason": (
                "both stopped, {0:.2f} s apart, which is inside the {1:.2f} s "
                "margin. Arrival order does not decide it and no tie-break is "
                "configured, so priority is ambiguous. This is a result, not a "
                "failure to compute one".format(gap, margin)
            ),
        })

    return dict(base, **{
        "verdict": "AMBIGUOUS_PRIORITY",
        "has_priority": None,
        "must_stop": facing,
        "reason": (
            "the observed pattern of traffic control does not match any case "
            "the benchmark rule covers"
        ),
    })
