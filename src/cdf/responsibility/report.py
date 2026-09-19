"""What is said about each participant, and why.

The brief is blunt about this: do not hide everything behind one score. So the
report is eight separate findings per vehicle, each traceable to its evidence,
and the summary verdict is one of three words rather than a number.

    physical causal contributor    yes / no / uncertain
    but-for contribution           yes / no / not tested
    traffic-control violations     the rules broken, with what showed it
    temporal-property failures     which properties failed, and where
    non-action evidence            what the vehicle did not do, and when watched
    mitigating actions             what it did that reduced the outcome
    prevention opportunities       what would have helped but was not its doing
    responsibility evidence        supported / partial / insufficient

The last is a summary of the other seven and adds nothing new. *Supported* means
a rule was broken and the vehicle's own behaviour independently reaches the
outcome. *Partial* means one of those without the other -- a rule broken with no
causal path, or a causal path with nothing done wrong. *Insufficient* means
neither, which for most participants in most runs is the right answer.

Why there is no percentage
--------------------------

A number invites arithmetic: 70% and 30%, summing to a whole, apportioning
something. Nothing here sums. Two vehicles can both be supported contributors,
or neither can be, and a share of an incident is not a quantity this method
measures -- or that any method could measure from telemetry. The vocabulary
throughout is causal and normative: contributor, violation, evidence. Never
fault, never liability, never blame.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.schemas import SCHEMA_VERSIONS, Event, EventType, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = ["EVIDENCE_LEVELS", "build_responsibility_report"]

#: The three verdicts, and nothing between them.
EVIDENCE_LEVELS = ("supported", "partial", "insufficient")

_VIOLATION_TYPES = (
    "STOP_RULE_VIOLATION", "YIELD_RULE_VIOLATION", "SOLID_LINE_VIOLATION",
    "UNSAFE_CONFLICT_ENTRY",
)


def _type_of(event: Event) -> str:
    return (
        event.event_type.value if hasattr(event.event_type, "value")
        else str(event.event_type)
    )


def _entry_is_about(entry: Mapping[str, Any], participant: str) -> bool:
    """Whether a replay contribution concerns this vehicle.

    The graph-only hypothesis names a participant. A replay-backed contribution
    names the *action* it intervened on, because that is what an intervention
    targets, and every scenario names its actions `<participant>_<what>` --
    A_roll_through, B_brake. Matching on that prefix is what connects the two.
    Without it the replays were recorded and every vehicle in a run that had been
    replayed a dozen times still reported "not tested".
    """
    named = entry.get("participant_id")
    if named is not None:
        return str(named) == str(participant)
    action = str(entry.get("action_id") or "")
    return action.startswith("{0}_".format(participant))



def _but_for(
    attribution: Optional[Mapping[str, Any]], participant: str
) -> Dict[str, Any]:
    """What the counterfactual replays established for this vehicle.

    Deliberately three-valued, and "not tested" is the common case: replaying a
    counterfactual needs the simulator, and a run analysed offline has no such
    evidence either way. Reporting that as "no" would turn an absence of
    experiment into a finding.
    """
    if not attribution:
        return {
            "verdict": "not tested",
            "reason": (
                "no counterfactual replay was available for this run, so "
                "but-for causation was neither established nor ruled out"
            ),
        }
    for entry in attribution.get("contributions", []) or []:
        if not _entry_is_about(entry, participant):
            continue
        established = entry.get("establishes_causation")
        if established is None:
            continue
        return {
            "verdict": "yes" if established else "no",
            "interventions": entry.get("interventions", []),
            "reason": entry.get("rationale", ""),
        }
    return {
        "verdict": "not tested",
        "reason": "no intervention in the replay set targeted this vehicle",
    }


def build_responsibility_report(
    responsibility_graph: Mapping[str, Any],
    events: Sequence[Event],
    formal_results: Optional[Mapping[str, Any]] = None,
    attribution: Optional[Mapping[str, Any]] = None,
    priority: Optional[Mapping[str, Any]] = None,
    cfg: Optional[Config] = None,
    run_id: str = "",
    scenario_id: str = "",
    seed: int = 0,
) -> Dict[str, Any]:
    """The per-participant account, with every finding kept separate."""
    cfg = cfg if cfg is not None else Config({})
    participants = list(responsibility_graph.get("participants") or [])
    nodes = list(responsibility_graph.get("nodes") or [])
    per_participant = dict(responsibility_graph.get("per_participant") or {})
    by_event = {e.event_id: e for e in events}

    findings: Dict[str, Any] = {}
    for pid in participants:
        own_nodes = [n for n in nodes if n["participant"] == pid]
        violations = [n for n in own_nodes if n["node_type"] in _VIOLATION_TYPES]
        mitigations = [
            n for n in own_nodes if n["node_type"] == "MITIGATING_RESPONSE"
        ]
        contribution = per_participant.get(pid, {})
        physically_relevant = bool(contribution.get("physically_relevant"))
        property_failures = list(contribution.get("property_failures") or [])

        non_actions = [
            {
                "event_id": e.event_id,
                "event_type": _type_of(e),
                "subject": str(e.subject) if e.subject else None,
                "monitored_interval": (e.detail or {}).get("monitored_interval"),
                "evidence_coverage": (e.detail or {}).get("evidence_coverage"),
                "obligation": (e.detail or {}).get("obligation"),
            }
            for e in events
            if str(e.participant_id) == pid
            and (e.detail or {}).get("rule_id", "").startswith("NA")
        ]

        but_for = _but_for(attribution, pid)
        prevention = _prevention_opportunities(attribution, pid)

        if violations and physically_relevant:
            level = "supported"
            why = (
                "a benchmark rule was broken and this vehicle's own behaviour "
                "independently reaches the outcome in the physical graph"
            )
        elif violations or physically_relevant or property_failures:
            level = "partial"
            why = _partial_reason(bool(violations), physically_relevant,
                                  bool(property_failures))
        else:
            level = "insufficient"
            why = (
                "no benchmark rule was observed to be broken and no path from "
                "this vehicle's own behaviour reaches the outcome"
            )

        findings[pid] = {
            "physical_causal_contributor": (
                "yes" if physically_relevant
                else ("uncertain" if not contribution else "no")
            ),
            "physical_path": contribution.get("path", []),
            "but_for_contribution": but_for,
            "traffic_control_violations": [
                {
                    "node_id": n["node_id"], "node_type": n["node_type"],
                    "t": n["t"], "basis": n["basis"],
                    "benchmark_rule": (n.get("detail") or {}).get("obligation"),
                }
                for n in violations
            ],
            "temporal_property_failures": property_failures,
            "non_action_evidence": non_actions,
            "mitigating_actions": [
                {"node_id": n["node_id"], "t": n["t"], "basis": n["basis"]}
                for n in mitigations
            ],
            "prevention_opportunities": prevention,
            "responsibility_evidence": level,
            "why": why,
        }

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "scope": Provenance.FUSED.value,
        "run_id": run_id,
        "scenario_id": scenario_id,
        "seed": int(seed),
        "participants": participants,
        "priority": dict(priority or {}),
        "findings": findings,
        "vocabulary": {
            "supported": (
                "a benchmark rule was broken and the vehicle's own behaviour "
                "independently reaches the outcome"
            ),
            "partial": "one of those two without the other",
            "insufficient": "neither",
            "not_a_fault_finding": (
                "these are causal and normative findings. They are not "
                "statements of legal fault, liability or blame, and nothing "
                "here is a share or a percentage of anything"
            ),
        },
        "note": (
            "eight findings per participant, each traceable to its evidence. "
            "The summary level adds nothing the seven above it do not already "
            "say; it exists so a reader can scan, not so a reader can skip"
        ),
    }


def _partial_reason(
    has_violation: bool, physically_relevant: bool, has_property_failure: bool
) -> str:
    if has_violation and not physically_relevant:
        return (
            "a benchmark rule was broken, but no path from this vehicle's own "
            "behaviour reaches the outcome. Breaking a rule near an incident is "
            "not the same as contributing to it"
        )
    if physically_relevant and not has_violation and not has_property_failure:
        return (
            "this vehicle's behaviour reaches the outcome physically, but "
            "nothing it did was observed to break a rule. A vehicle that brakes "
            "lawfully and is struck from behind is causally involved and has "
            "done nothing wrong"
        )
    if has_property_failure and not has_violation:
        return (
            "a safety property failed, but no traffic-control rule was observed "
            "to be broken"
        )
    return "some evidence of contribution, without both halves of the claim"


def _prevention_opportunities(
    attribution: Optional[Mapping[str, Any]], participant: str
) -> List[Dict[str, Any]]:
    """Things that would have helped, which is not the same as things that caused.

    Advancing or strengthening a safety action can avert an outcome without the
    original action having caused it. Keeping these out of the but-for column is
    the distinction the counterfactual engine exists to protect, and folding
    them in would make every vehicle that could have braked sooner a cause of
    what happened.
    """
    if not attribution:
        return []
    out: List[Dict[str, Any]] = []
    for entry in attribution.get("contributions", []) or []:
        if str(entry.get("participant_id")) != str(participant):
            continue
        for opportunity in entry.get("prevention_opportunities", []) or []:
            out.append({
                "intervention": opportunity.get("intervention"),
                "effect": opportunity.get("effect"),
                "note": (
                    "an opportunity to prevent, not evidence of causing. The "
                    "action would have helped had it come sooner or been "
                    "stronger; that does not make the action as performed a "
                    "cause of the outcome"
                ),
            })
    return out
