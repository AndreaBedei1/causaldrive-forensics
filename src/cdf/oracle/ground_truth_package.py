"""Everything privileged a run knows, written where a reader can check it.

Two products come out of here, and keeping them apart is the point.

The **observable ground truth** is what a reconstruction is measured against: the
physical events, in the vocabulary a reconstruction shares, plus the exact
geometry they were measured from. A reader who doubts a pairwise claim can open
``radar_truth`` and see the range, bearing and range rate behind it.

The **scenario design reference** is what the experiment intended: the scripted
actions, the causal template, the designed contributors. It answers "did the
mechanism the scenario was built to demonstrate actually execute?", which is a
question about the experiment rather than about the world, and it is never the
reference a reconstruction is judged against. Conflating the two is what made the
old comparison unfair, and separating them is most of this refactor.

Both are evaluation-only. Nothing here is ever read by inference, and the
anti-leakage suite walks every artifact to make sure.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple, Union

from ..common.config import Config
from ..common.io import write_json, write_jsonl_gz
from ..common.layout import RunLayout
from ..common.schemas import Event, GraphDocument, Provenance, SCHEMA_VERSIONS
from ..graph.export import save_graph
from ..graph.ontology import describe as describe_ontology
from .events import load_oracle_trace
from .observable import build_observable_events, pairwise_truth
from .observable_graph import build_observable_causal_graph

LOGGER = logging.getLogger(__name__)

__all__ = [
    "build_ground_truth_package",
    "build_scenario_design_reference",
    "map_context_of",
]

PathLike = Union[str, Path]


def map_context_of(trace: Mapping[str, Any]) -> Dict[str, Any]:
    """The map facts the simulator knows, kept out of the comparable claim.

    The supervisor's design has the ground truth carrying the map, and it does --
    here. What it must not do is turn map knowledge into an *event type* a
    reconstruction has no way to emit, because that puts the reference back
    outside the shared vocabulary and makes the comparison unfair again in the
    old way. So lane, road and junction identity live in this file and in event
    ``detail``, as context a reader can use to interpret a claim, never as the
    claim itself.
    """
    per_participant: Dict[str, Any] = {}
    for frame in trace.get("frames", []) or []:
        t = float(frame.get("t", 0.0))
        for actor in frame.get("actors", []) or []:
            pid = str(actor.get("participant_id"))
            entry = per_participant.setdefault(pid, {
                "roads": [], "lanes": [], "junctions": [], "first_t": t, "last_t": t,
            })
            entry["last_t"] = t
            for key, bucket in (
                ("road_id", "roads"), ("lane_id", "lanes"), ("junction_id", "junctions")
            ):
                value = actor.get(key)
                if value is not None and value not in entry[bucket]:
                    entry[bucket].append(value)
    for entry in per_participant.values():
        for bucket in ("roads", "lanes", "junctions"):
            entry[bucket] = sorted(entry[bucket], key=lambda v: (str(type(v)), str(v)))
    return {
        "map_name": (trace.get("summary") or {}).get("map_name"),
        "per_participant": dict(sorted(per_participant.items())),
        "note": (
            "privileged map context. Present because the ground truth is "
            "supposed to carry the map; kept out of the comparable event "
            "vocabulary because a reconstruction has no map and a reference "
            "that asserted map-only event types could not be matched"
        ),
    }


#: Which observable event a scripted action of each kind should produce if it
#: actually fired. This is how the design reference checks itself against the
#: world: a brake that was configured but produced no braking did not execute.
_ACTION_EVIDENCE: Dict[str, Tuple[str, ...]] = {
    "brake": ("BRAKE_ONSET", "HARD_BRAKE", "DECELERATION", "HARD_DECELERATION"),
    "set_speed": ("THROTTLE_ONSET", "ACCELERATION", "DECELERATION"),
    "lane_shift": ("STEER_ONSET", "SIGNIFICANT_HEADING_CHANGE",
                   "LANE_CHANGE_LIKE_MANEUVER"),
}


def build_scenario_design_reference(
    trace: Mapping[str, Any],
    spec: Any,
    cfg: Config,
    observable: Optional[Sequence[Event]] = None,
) -> Dict[str, Any]:
    """What the scenario meant to do, and whether the trace shows it happening.

    This is the secondary reference. It holds the scripted actions and the
    designed causal template -- the things the old oracle mixed into its primary
    graph -- and it is used for scenario validation and for naming the designed
    contributors, never for scoring a reconstruction's graph.

    It also checks itself. A scenario can be configured to make B brake and then
    fail to make B brake, and a design reference that only restated the
    configuration would never notice. So each declared action is looked for in
    the observable events: a braking action should leave braking behind it. What
    is found, and what is not, is recorded per action.
    """
    actions: List[Dict[str, Any]] = []
    for participant in getattr(spec, "participants", []) or []:
        pid = str(getattr(participant, "participant_id", ""))
        for action in getattr(participant, "actions", []) or []:
            actions.append({
                "action_id": str(getattr(action, "action_id", "")),
                "participant_id": pid,
                "kind": str(getattr(action, "kind", "")),
                "t_start": getattr(action, "t_start", None),
                "enabled": bool(getattr(action, "enabled", True)),
                "params": dict(getattr(action, "params", {}) or {}),
            })

    # What the controller was actually configured with, which is not always what
    # the scenario file declares -- a counterfactual replay disables an action,
    # and the trace is where that shows up.
    configured: Dict[str, Dict[str, Any]] = {}
    interventions = (trace.get("summary") or {}).get("interventions") or {}
    if isinstance(interventions, Mapping):
        for pid, block in interventions.items():
            if not isinstance(block, Mapping):
                continue
            for entry in block.get("actions", []) or []:
                if isinstance(entry, Mapping) and entry.get("action_id"):
                    configured[str(entry["action_id"])] = {
                        "participant_id": str(pid),
                        "enabled": bool(entry.get("enabled", True)),
                        "t_start": entry.get("t_start"),
                        "kind": str(entry.get("kind", "")),
                    }

    for action in actions:
        record = configured.get(action["action_id"])
        action["configured_in_run"] = record is not None
        action["enabled_in_run"] = bool(record["enabled"]) if record else False
        action["evidence"] = _action_evidence(action, observable)

    template = list(getattr(spec, "causal_template", []) or [])
    mechanism = [a for a in actions if a["enabled_in_run"]]
    unrealised = [a["action_id"] for a in mechanism if not a["evidence"]["found"]]

    return {
        "schema_version": SCHEMA_VERSIONS.get("graph", "1.0.0"),
        "reference_kind": "scenario_design",
        "scenario_id": getattr(spec, "scenario_id", ""),
        "variant": getattr(spec, "variant", ""),
        "scripted_actions": actions,
        "causal_template": template,
        "expected_outcome": _expected_outcome(spec),
        "declared_action_ids": sorted(
            a["action_id"] for a in actions if a["action_id"]
        ),
        "enabled_action_ids": sorted(a["action_id"] for a in mechanism),
        "mechanism_executed": not unrealised,
        "actions_without_physical_evidence": sorted(unrealised),
        "note": (
            "the scenario's designed mechanism, and whether the trace shows it "
            "happening. Answers whether the experiment executed as intended; "
            "never the reference for judging how much of the incident a "
            "reconstruction recovered, because a scripted action is not a "
            "physical event any vehicle could observe"
        ),
    }


def _action_evidence(
    action: Mapping[str, Any], observable: Optional[Sequence[Event]]
) -> Dict[str, Any]:
    """Whether the observable events show this action actually happening."""
    if observable is None:
        return {"found": None, "reason": "observable events were not supplied"}
    wanted = _ACTION_EVIDENCE.get(str(action.get("kind", "")))
    if not wanted:
        return {
            "found": None,
            "reason": "no physical signature is defined for action kind "
                      "{0!r}".format(action.get("kind")),
        }
    pid = str(action.get("participant_id"))
    t_start = action.get("t_start")
    window = 3.0
    matches = [
        e for e in observable
        if str(e.participant_id) == pid
        and (e.event_type.value if hasattr(e.event_type, "value")
             else str(e.event_type)) in wanted
        and (t_start is None or abs(float(e.t_peak) - float(t_start)) <= window)
    ]
    return {
        "found": bool(matches),
        "expected_event_types": list(wanted),
        "window_s": window,
        "matched_event_ids": sorted(e.event_id for e in matches)[:8],
        "n_matched": len(matches),
    }


def _expected_outcome(spec: Any) -> Dict[str, Any]:
    outcome = getattr(spec, "expected_outcome", None)
    if outcome is None:
        return {}
    if isinstance(outcome, Mapping):
        return dict(outcome)
    return {
        key: getattr(outcome, key)
        for key in ("collision", "collision_pair", "min_separation_m")
        if hasattr(outcome, key)
    }


def build_ground_truth_package(
    run_dir: PathLike,
    cfg: Config,
    spec: Any = None,
    persist: bool = True,
) -> Dict[str, Any]:
    """Build (and optionally write) the privileged package for one run.

    Returns the events, the observable causal graph and the two context files,
    so a caller can use them without re-reading the disk.
    """
    layout = RunLayout.from_run_dir(run_dir)
    trace = load_oracle_trace(layout.root)
    participants = [str(p) for p in trace.get("participants", []) or []]

    events = build_observable_events(trace, cfg, spec=spec)
    causal = build_observable_causal_graph(
        events,
        trace,
        cfg,
        run_id=str((trace.get("summary") or {}).get("run_id", "")),
        scenario_id=str((trace.get("summary") or {}).get("scenario_id", "")),
        seed=int((trace.get("summary") or {}).get("seed", 0) or 0),
    )

    radar_rows: List[Dict[str, Any]] = []
    for observer in participants:
        for target in participants:
            if observer != target:
                radar_rows.extend(pairwise_truth(trace, observer, target))
    radar_rows.sort(key=lambda r: (r["t"], r["observer"], r["target"]))

    context = map_context_of(trace)
    design = (
        build_scenario_design_reference(trace, spec, cfg, observable=events)
        if spec is not None else None
    )

    if persist:
        layout.oracle_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.observable_events, {
            "schema_version": SCHEMA_VERSIONS["events"],
            "provenance": Provenance.ORACLE.value,
            "reference_kind": "oracle_observable",
            "ontology": describe_ontology(),
            "events": [_jsonable(e) for e in events],
        })
        save_graph(
            causal, layout.observable_causal_graph, layout.observable_causal_graphml
        )
        write_jsonl_gz(layout.radar_truth, radar_rows)
        write_json(layout.map_context, context)
        if design is not None:
            write_json(layout.scenario_design_graph, design)

    LOGGER.info(
        "observable ground truth for %s: %d events, %d causal edges "
        "(%d candidate edges refused by the trace)",
        layout.root.name, len(events), len(causal.edges),
        causal.meta.get("n_edges_refused_by_trace", 0),
    )
    return {
        "events": events,
        "causal_graph": causal,
        "radar_truth_rows": len(radar_rows),
        "map_context": context,
        "scenario_design": design,
    }


def _jsonable(event: Event) -> Dict[str, Any]:
    from ..common.schemas import to_jsonable

    return to_jsonable(event)
