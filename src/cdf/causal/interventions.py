"""Enumeration of the controlled interventions worth replaying.

An intervention is a single, named modification of the scripted timeline:
*disable this action*, *start it 1.5 s later*, *brake at 40 % of the commanded
intensity*. Everything else about the run -- map, spawn state, seed, controller
gains, sensor configuration -- is held identical, which is what makes the replay
a controlled counterfactual rather than a different experiment. The modification
is applied by :func:`cdf.simulation.runner._apply_intervention` before the world
is created, so it changes behaviour from the first tick and never has to be
injected mid-run.

Which actions are worth replaying comes from two independent sources:

*The scenario author.* ``intervention_candidates`` in the scenario YAML lists the
actions the experiment was designed around. These are always enumerated, even
when the reconstruction never noticed them -- otherwise a reconstruction that
missed a cause could quietly remove that cause from the experiment.

*The reconstruction itself.* When a fused causal DAG is supplied,
:meth:`cdf.graph.analysis.GraphAnalyzer.candidate_intervention_nodes` ranks the
nodes whose removal destroys causal explanations of the outcome. Those nodes are
observed *events*, not scripted actions, so they are mapped back onto actions by
participant and time proximity: an event can only have been produced by an action
of the same participant that started shortly before it. This is what lets the
counterfactual layer follow evidence the scenario author did not anticipate.

The two rankings are merged, so an action that is both declared and graph-ranked
outranks one that is only declared, and the list is capped at
``counterfactual.max_interventions``. Dropped candidates are logged, never
silently discarded: a replay budget that hid a candidate would make an
attribution result unreproducible.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from ..common.config import Config
from ..common.schemas import GraphDocument
from ..graph.analysis import GraphAnalyzer
from ..simulation.controllers import ScriptedAction
from ..simulation.scenario_base import ParticipantSpec, ScenarioSpec

LOGGER = logging.getLogger(__name__)

__all__ = [
    "RUNNER_OPS",
    "INSERTABLE_KINDS",
    "COUNTERFACTUAL_ROLES",
    "InterventionSpec",
    "enumerate_interventions",
    "interventions_for_action",
    "omission_repairs",
]

#: Operations understood by :func:`cdf.simulation.runner._apply_intervention`.
#: ``disable`` removes the action, ``delay``/``advance`` shift its start time by
#: ``seconds``, ``scale`` multiplies ``param`` by ``factor``, ``set`` assigns
#: ``param`` the given ``value``, and ``insert_action`` adds a behaviour that did
#: not occur at all.
#:
#: The last one exists because every other op modifies something that happened,
#: and the most interesting causal question about a stop-sign violation is about
#: something that did not: "what if the vehicle had performed the required
#: stop?". There is no factual action to weaken, so without insertion the
#: omission could be described and never tested.
RUNNER_OPS: Tuple[str, ...] = (
    "disable", "delay", "advance", "scale", "set", "insert_action",
)

#: Required extra keys per operation, enforced at construction so that a broken
#: intervention fails here rather than after a two-minute simulator replay.
_REQUIRED_PARAMS: Dict[str, Tuple[str, ...]] = {
    "disable": (),
    "delay": ("seconds",),
    "advance": ("seconds",),
    "scale": ("param", "factor"),
    "set": ("param", "value"),
    "insert_action": ("participant", "kind", "t_start", "duration"),
}

#: Action kinds :class:`~cdf.simulation.controllers.ScriptedController` can
#: execute. Checked at construction: an inserted action of an unknown kind would
#: be silently ignored by the controller and the replay would look like a
#: counterfactual that changed nothing, which is the most misleading possible
#: failure.
INSERTABLE_KINDS: Tuple[str, ...] = (
    "brake", "stop", "hold", "set_speed", "lane_shift",
)

#: Replay order within one action: the strongest, most interpretable
#: intervention first, so that a truncated budget keeps the informative ones.
_OP_RANK: Dict[str, int] = {
    "disable": 0, "insert_action": 1, "scale": 2, "advance": 3, "delay": 4,
    "set": 5,
}

#: What kind of causal question a replay is asking. The distinction is the whole
#: point of the counterfactual layer and is carried on every intervention.
#:
#: ``factual_removal``
#:     remove, weaken or delay something that happened. Approximates its absence,
#:     so it can establish but-for causation.
#: ``prevention_opportunity``
#:     do more of a safety behaviour than was actually done -- sooner, harder. A
#:     collision avoided this way says the driver could have done better, not
#:     that what they did caused the crash.
#: ``omission_repair``
#:     supply a behaviour that did not occur *and was required*. This can
#:     establish the causal relevance of the omission -- but only where the
#:     omission itself is supported by evidence, which is what separates it from
#:     a prevention opportunity wearing the same clothes.
COUNTERFACTUAL_ROLES: Tuple[str, ...] = (
    "factual_removal", "prevention_opportunity", "omission_repair",
)


@dataclass
class InterventionSpec:
    """One controlled modification of one scripted action -- or of a set of them.

    A single-action intervention is the common case and is described by
    ``action_id``/``op``/``params``. When ``steps`` is non-empty the replay
    applies every step instead, which is what a joint counterfactual needs: two
    vehicles can each contribute without either being individually decisive, and
    the only way to find that out is to remove both in one replay.
    ``action_id`` then names the first step, so every consumer that reads a
    single action keeps working and sorts stably.
    """

    intervention_id: str
    """Stable, filesystem-safe identity; also the replay's artifact directory."""
    action_id: str
    op: str
    params: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    targets_participant: str = ""
    #: ``[{action_id, op, **params}, ...]``; empty means the single-action form.
    steps: List[Dict[str, Any]] = field(default_factory=list)
    repairs_non_action: str = ""
    """The event id of the non-action this insertion discharges, if any.

    Empty for every op that modifies a factual action. Set only when the replay
    supplies a behaviour the evidence says was required and absent, and it is
    what lets the attribution layer tell an omission repair from an ordinary
    safety improvement: both insert braking, and only one of them is about
    something the vehicle was obliged to do.
    """

    @property
    def counterfactual_role(self) -> str:
        """Which causal question this replay asks. See :data:`COUNTERFACTUAL_ROLES`.

        Derived rather than stored, so it cannot disagree with the operation it
        describes. An insertion that names no non-action is a prevention
        opportunity however safe the inserted behaviour is -- adding a brake for
        a vehicle under no obligation to brake answers "could this have been
        avoided?", not "did the omission matter?".
        """
        if self.op == "insert_action":
            return "omission_repair" if self.repairs_non_action else (
                "prevention_opportunity"
            )
        if self.op == "advance":
            return "prevention_opportunity"
        if self.op == "scale":
            try:
                if float(self.params.get("factor", 0.0)) > 1.0:
                    return "prevention_opportunity"
            except (TypeError, ValueError):
                pass
        return "factual_removal"

    @property
    def action_ids(self) -> Tuple[str, ...]:
        """Every action this replay modifies, sorted and deduplicated."""
        if self.steps:
            return tuple(sorted({str(step["action_id"]) for step in self.steps}))
        return (self.action_id,)

    @property
    def is_composite(self) -> bool:
        return len(self.action_ids) > 1

    def __post_init__(self) -> None:
        if self.steps:
            for step in self.steps:
                op = str(step.get("op", ""))
                if op not in RUNNER_OPS:
                    raise ValueError(
                        "unknown intervention op {0!r} in composite {1!r}".format(
                            op, self.intervention_id
                        )
                    )
                if not step.get("action_id"):
                    raise ValueError(
                        "a step of composite intervention {0!r} names no "
                        "action".format(self.intervention_id)
                    )
                missing = [k for k in _REQUIRED_PARAMS[op] if k not in step]
                if missing:
                    raise ValueError(
                        "step {0!r} (op={1}) of {2!r} is missing required "
                        "parameter(s) {3}".format(
                            step.get("action_id"), op, self.intervention_id, missing
                        )
                    )
            if len({str(step["action_id"]) for step in self.steps}) != len(self.steps):
                raise ValueError(
                    "composite intervention {0!r} modifies the same action twice; "
                    "one replay changes each action at most once".format(
                        self.intervention_id
                    )
                )
            return
        if self.op not in RUNNER_OPS:
            raise ValueError(
                "unknown intervention op {0!r} for action {1!r}; the runner "
                "understands {2}".format(self.op, self.action_id, list(RUNNER_OPS))
            )
        missing = [k for k in _REQUIRED_PARAMS[self.op] if k not in self.params]
        if missing:
            raise ValueError(
                "intervention {0!r} (op={1}) is missing required parameter(s) "
                "{2}".format(self.intervention_id, self.op, missing)
            )
        if not self.action_id:
            raise ValueError(
                "intervention {0!r} does not name an action to act on".format(
                    self.intervention_id
                )
            )
        if self.op == "insert_action":
            self._validate_insertion()

    def _validate_insertion(self) -> None:
        """Check an insertion before a replay spends two minutes discovering it.

        An inserted action of an unknown kind is the failure worth catching here:
        the controller would ignore it silently and the replay would look like a
        counterfactual that changed nothing -- indistinguishable from a genuine
        finding that the behaviour would not have helped.
        """
        kind = str(self.params.get("kind", ""))
        if kind not in INSERTABLE_KINDS:
            raise ValueError(
                "intervention {0!r} inserts an action of kind {1!r}, which no "
                "controller executes; a replay would silently change nothing. "
                "Known kinds: {2}".format(
                    self.intervention_id, kind, list(INSERTABLE_KINDS)
                )
            )
        if not str(self.params.get("participant", "")):
            raise ValueError(
                "intervention {0!r} inserts an action for no participant".format(
                    self.intervention_id
                )
            )
        for key in ("t_start", "duration"):
            try:
                value = float(self.params[key])
            except (TypeError, ValueError, KeyError):
                raise ValueError(
                    "intervention {0!r} has a non-numeric {1}".format(
                        self.intervention_id, key
                    )
                )
            if value < 0.0:
                raise ValueError(
                    "intervention {0!r} has a negative {1}; an action cannot "
                    "start before the run or last a negative time".format(
                        self.intervention_id, key
                    )
                )
        if float(self.params["duration"]) <= 0.0:
            raise ValueError(
                "intervention {0!r} inserts an action of zero duration, which "
                "the controller would never execute".format(self.intervention_id)
            )

    def as_runner_dict(self) -> Dict[str, Any]:
        """Exactly the mapping :func:`run_scenario` expects as ``intervention``.

        Only the keys the runner reads are emitted; ranking and bookkeeping stay
        on this object, so nothing that could perturb the replay travels with it.
        """
        if self.steps:
            return {
                "intervention_id": self.intervention_id,
                "steps": [dict(step) for step in self.steps],
            }
        payload: Dict[str, Any] = {
            "intervention_id": self.intervention_id,
            "action_id": self.action_id,
            "op": self.op,
        }
        payload.update(self.params)
        return payload

    def to_dict(self) -> Dict[str, Any]:
        """Serialisable record for the counterfactual manifest."""
        return {
            "intervention_id": self.intervention_id,
            "action_id": self.action_id,
            "action_ids": list(self.action_ids),
            "op": self.op,
            "params": dict(self.params),
            "description": self.description,
            "targets_participant": self.targets_participant,
            "steps": [dict(step) for step in self.steps],
            "composite": self.is_composite,
            "counterfactual_role": self.counterfactual_role,
            "repairs_non_action": self.repairs_non_action,
        }


# ---------------------------------------------------------------------------
# Enumeration
# ---------------------------------------------------------------------------


def enumerate_interventions(
    spec: ScenarioSpec,
    fused_causal: Optional[GraphDocument] = None,
    cfg: Optional[Config] = None,
) -> List[InterventionSpec]:
    """Build the ranked list of interventions to replay for one scenario.

    Candidates come from the scenario's own ``intervention_candidates`` and, when
    ``fused_causal`` is given, from the reconstruction's ranked cut nodes mapped
    back onto scripted actions. The result is ordered best-first and truncated to
    ``counterfactual.max_interventions``; whatever is dropped is logged.
    """
    actions = _actions_by_id(spec)
    if not actions:
        LOGGER.warning(
            "scenario %s declares no scripted actions, so there is nothing to "
            "intervene on",
            spec.scenario_id,
        )
        return []

    declared_rank = _declared_ranks(spec, actions)
    graph_rank = _graph_ranks(spec, actions, fused_causal, cfg)

    ranked: List[Tuple[Tuple[int, int, int, str], str]] = []
    for action_id in sorted(set(list(declared_rank.keys()) + list(graph_rank.keys()))):
        cut_rank, paths_cut = graph_rank.get(action_id, (2, 0))
        declared = declared_rank.get(action_id, len(declared_rank) + 1)
        ranked.append(((cut_rank, -paths_cut, declared, action_id), action_id))
    ranked.sort()

    per_action: List[List[InterventionSpec]] = []
    for _key, action_id in ranked:
        action, participant = actions[action_id]
        reason = _rank_reason(action_id, declared_rank, graph_rank)
        per_action.append(
            interventions_for_action(action, participant.participant_id, cfg, reason)
        )

    # Allocate the budget BREADTH-FIRST: every candidate action gets its
    # strongest intervention (removing it entirely) before any action gets a
    # second, weaker one.
    #
    # Spending the budget depth-first instead silently answers the wrong
    # question. On the S06 chain collision it filled the budget with three
    # variations of the shared leading brake and dropped the one action that
    # distinguishes the two variants -- whether the middle vehicle reacted -- so
    # the two scenarios would have produced the same attribution for a reason
    # that had nothing to do with their causal structure.
    out: List[InterventionSpec] = []
    depth = 0
    while any(len(group) > depth for group in per_action):
        for group in per_action:
            if len(group) > depth:
                out.append(group[depth])
        depth += 1

    limit = int(cfg.get("counterfactual.max_interventions", 8)) if cfg else 8
    if limit > 0 and len(out) > limit:
        dropped = out[limit:]
        LOGGER.warning(
            "counterfactual budget of %d replay(s) reached for scenario %s: "
            "dropping %d lower-ranked intervention(s): %s",
            limit,
            spec.scenario_id,
            len(dropped),
            ", ".join(iv.intervention_id for iv in dropped),
        )
        out = out[:limit]
    return out


def interventions_for_action(
    action: ScriptedAction,
    participant_id: str,
    cfg: Optional[Config] = None,
    reason: str = "",
) -> List[InterventionSpec]:
    """The meaningful interventions for one scripted action, strongest first.

    The operations offered depend on what the action *is*: removing a brake and
    weakening it are different questions, and neither makes sense for an action
    with no intensity parameter. An operation that would provably do nothing (for
    example advancing an action that already starts at t=0) is skipped and
    logged, so the replay budget is never spent on a no-op.
    """
    kind = str(action.kind)
    ops: List[Tuple[str, Dict[str, Any]]] = [("disable", {})]

    if kind == "brake":
        factor = float(cfg.get("counterfactual.ops.brake.scale_factor", 0.4)) if cfg else 0.4
        advance_s = float(cfg.get("counterfactual.ops.brake.advance_s", 1.0)) if cfg else 1.0
        ops.append(("scale", {"param": "intensity", "factor": factor}))
        ops.append(("advance", {"seconds": advance_s}))
    elif kind == "set_speed":
        factor = (
            float(cfg.get("counterfactual.ops.set_speed.scale_factor", 0.8)) if cfg else 0.8
        )
        ops.append(("scale", {"param": "target_speed", "factor": factor}))
    elif kind == "lane_shift":
        delay_s = float(cfg.get("counterfactual.ops.lane_shift.delay_s", 1.5)) if cfg else 1.5
        advance_s = (
            float(cfg.get("counterfactual.ops.lane_shift.advance_s", 1.5)) if cfg else 1.5
        )
        ops.append(("delay", {"seconds": delay_s}))
        ops.append(("advance", {"seconds": advance_s}))
    else:
        LOGGER.info(
            "action %s has kind %r, for which only 'disable' is meaningful",
            action.action_id,
            kind,
        )

    out: List[InterventionSpec] = []
    for op, params in sorted(ops, key=lambda item: _OP_RANK[item[0]]):
        skip = _skip_reason(action, op, params)
        if skip:
            LOGGER.info(
                "skipping %s on action %s: %s", op, action.action_id, skip
            )
            continue
        out.append(
            InterventionSpec(
                intervention_id=_intervention_id(action.action_id, op, params),
                action_id=action.action_id,
                op=op,
                params=dict(params),
                description=_describe(action, participant_id, op, params, reason),
                targets_participant=participant_id,
            )
        )
    return out


# ---------------------------------------------------------------------------
# Candidate ranking
# ---------------------------------------------------------------------------


def _actions_by_id(spec: ScenarioSpec) -> Dict[str, Tuple[ScriptedAction, ParticipantSpec]]:
    """Every scripted action of the scenario, indexed by its id."""
    out: Dict[str, Tuple[ScriptedAction, ParticipantSpec]] = {}
    for participant in spec.participants:
        for action in participant.actions:
            out[action.action_id] = (action, participant)
    return out


def _declared_ranks(
    spec: ScenarioSpec, actions: Dict[str, Tuple[ScriptedAction, ParticipantSpec]]
) -> Dict[str, int]:
    """Position of each author-declared candidate, in declaration order."""
    ranks: Dict[str, int] = {}
    for index, action_id in enumerate(spec.intervention_candidates):
        if action_id not in actions:
            # ScenarioSpec.validate_static already rejects this; reaching here
            # means the spec was built by hand, so say so rather than crash.
            raise KeyError(
                "scenario {0} lists intervention candidate {1!r}, which is not a "
                "declared scripted action ({2})".format(
                    spec.scenario_id, action_id, sorted(actions)
                )
            )
        ranks[action_id] = index
    return ranks


def _graph_ranks(
    spec: ScenarioSpec,
    actions: Dict[str, Tuple[ScriptedAction, ParticipantSpec]],
    fused_causal: Optional[GraphDocument],
    cfg: Optional[Config],
) -> Dict[str, Tuple[int, int]]:
    """Map ranked cut nodes of a causal DAG onto scripted actions.

    Returns ``{action_id: (cut_rank, paths_cut)}`` where ``cut_rank`` is 0 for a
    node whose removal leaves an outcome unexplained and 1 for one that merely
    destroys some explanations. An action keeps the best evidence found for it.
    """
    if fused_causal is None:
        return {}

    max_lag_s = float(cfg.get("counterfactual.action_match.max_lag_s", 4.0)) if cfg else 4.0
    pre_s = float(cfg.get("counterfactual.action_match.max_lead_s", 0.5)) if cfg else 0.5

    analyzer = GraphAnalyzer(fused_causal, cfg)
    ranks: Dict[str, Tuple[int, int]] = {}
    for candidate in analyzer.candidate_intervention_nodes():
        action_id = _match_action(
            candidate.get("participant_id"),
            float(candidate.get("t_peak", 0.0)),
            actions,
            max_lag_s=max_lag_s,
            pre_s=pre_s,
        )
        if action_id is None:
            LOGGER.debug(
                "causal node %s (participant %s, t=%.2f) has no scripted action "
                "close enough to intervene on",
                candidate.get("event_id"),
                candidate.get("participant_id"),
                float(candidate.get("t_peak", 0.0)),
            )
            continue
        cut_rank = 0 if candidate.get("disconnects_outcome") else 1
        paths_cut = int(candidate.get("paths_cut", 0))
        best = ranks.get(action_id)
        if best is None or (cut_rank, -paths_cut) < (best[0], -best[1]):
            ranks[action_id] = (cut_rank, paths_cut)
    if ranks:
        LOGGER.info(
            "causal graph nominated %d scripted action(s) for replay: %s",
            len(ranks),
            sorted(ranks),
        )
    return ranks


def _match_action(
    participant_id: Optional[str],
    t_peak: float,
    actions: Dict[str, Tuple[ScriptedAction, ParticipantSpec]],
    max_lag_s: float,
    pre_s: float,
) -> Optional[str]:
    """The scripted action most likely to have produced an observed event.

    An action can only explain an event of the *same participant* that peaks
    after the action started (allowing ``pre_s`` of sampling and reaction jitter)
    and within ``max_lag_s`` of it. Among those the closest in time wins; ties
    break on the action id so the mapping is deterministic.
    """
    if not participant_id:
        return None
    best: Optional[Tuple[float, str]] = None
    for action_id, (action, participant) in actions.items():
        if participant.participant_id != participant_id:
            continue
        lag = float(t_peak) - float(action.t_start)
        if lag < -abs(pre_s) or lag > abs(max_lag_s):
            continue
        key = (abs(lag), action_id)
        if best is None or key < best:
            best = key
    return best[1] if best is not None else None


def _rank_reason(
    action_id: str,
    declared_rank: Dict[str, int],
    graph_rank: Dict[str, Tuple[int, int]],
) -> str:
    """Why this action is being replayed, recorded in the manifest."""
    parts: List[str] = []
    if action_id in declared_rank:
        parts.append("declared by the scenario")
    if action_id in graph_rank:
        cut_rank, paths_cut = graph_rank[action_id]
        parts.append(
            "nominated by the fused causal graph ({0}, cuts {1} causal path(s))".format(
                "disconnects the outcome" if cut_rank == 0 else "destroys explanations",
                paths_cut,
            )
        )
    return "; ".join(parts)


# ---------------------------------------------------------------------------
# Naming and description
# ---------------------------------------------------------------------------


def _skip_reason(
    action: ScriptedAction, op: str, params: Dict[str, Any]
) -> Optional[str]:
    """Why an operation would be a no-op on this action, or ``None``."""
    if op == "advance" and float(action.t_start) <= 0.0:
        return "the action already starts at t=0, so it cannot be advanced"
    if op in ("scale", "set"):
        key = str(params.get("param"))
        if key not in (action.params or {}):
            return "the action has no parameter {0!r} (it has {1})".format(
                key, sorted(action.params or {})
            )
        if op == "scale" and float(params.get("factor", 1.0)) == 1.0:
            return "a scale factor of 1.0 changes nothing"
        if op == "scale" and float(action.params[key]) == 0.0:
            return "parameter {0!r} is already 0.0, so scaling it changes nothing".format(key)
    if op in ("delay", "advance") and float(params.get("seconds", 0.0)) == 0.0:
        return "a shift of 0.0 s changes nothing"
    return None


def _number_slug(value: float) -> str:
    """``1.5`` -> ``"1_5"``: readable and safe as a directory name."""
    text = "{0:g}".format(float(value))
    return text.replace("-", "neg").replace(".", "_")


def _intervention_id(action_id: str, op: str, params: Dict[str, Any]) -> str:
    """Stable identity, used as the replay directory name and as a report key."""
    if op == "disable":
        return "{0}__disable".format(action_id)
    if op in ("delay", "advance"):
        return "{0}__{1}_{2}s".format(action_id, op, _number_slug(params["seconds"]))
    if op == "scale":
        return "{0}__scale_{1}_{2}".format(
            action_id, params["param"], _number_slug(params["factor"])
        )
    return "{0}__set_{1}_{2}".format(
        action_id, params["param"], _number_slug(params["value"])
    )


def _describe(
    action: ScriptedAction,
    participant_id: str,
    op: str,
    params: Dict[str, Any],
    reason: str,
) -> str:
    """One sentence stating exactly what the replay changes, and why."""
    if op == "disable":
        what = "{0} never performs {1}".format(participant_id, action.action_id)
    elif op == "delay":
        what = "{0} starts {1} {2:g} s later (t={3:g}s -> t={4:g}s)".format(
            participant_id,
            action.action_id,
            float(params["seconds"]),
            float(action.t_start),
            float(action.t_start) + float(params["seconds"]),
        )
    elif op == "advance":
        what = "{0} starts {1} {2:g} s earlier (t={3:g}s -> t={4:g}s)".format(
            participant_id,
            action.action_id,
            float(params["seconds"]),
            float(action.t_start),
            max(0.0, float(action.t_start) - float(params["seconds"])),
        )
    elif op == "scale":
        key = str(params["param"])
        current = float((action.params or {}).get(key, 0.0))
        what = "{0} performs {1} with {2} scaled to {3:g} (from {4:g})".format(
            participant_id,
            action.action_id,
            key,
            current * float(params["factor"]),
            current,
        )
    else:
        what = "{0} performs {1} with {2} set to {3:g}".format(
            participant_id, action.action_id, params["param"], float(params["value"])
        )
    return "{0}; everything else in the run is held identical{1}".format(
        what, " [{0}]".format(reason) if reason else ""
    )


# ---------------------------------------------------------------------------
# Omission repair
# ---------------------------------------------------------------------------

#: What behaviour would have discharged each kind of omission, and for how long.
#: Stated once, in general terms, because a table keyed on scenario id would be
#: the scenario-specific rule the brief forbids.
#:
#: The durations are what it takes for the behaviour to be physically real: a
#: stop has to be held long enough to be a stop rather than a hesitation, and a
#: braking response has to last long enough to change the outcome it is being
#: tested against.
_REPAIR_FOR_NON_ACTION: Dict[str, Dict[str, Any]] = {
    "NO_STOP_AFTER_STOP_SIGN": {
        "kind": "stop", "duration": 2.5, "params": {},
        "why": "perform the stop the sign required",
    },
    "NO_YIELD_RESPONSE": {
        "kind": "stop", "duration": 2.0, "params": {},
        "why": "give way before entering the conflict",
    },
    "NO_BRAKING_RESPONSE": {
        "kind": "brake", "duration": 3.0, "params": {"intensity": 0.9},
        "why": "brake in response to the critical time-to-collision",
    },
    "CONFLICT_ENTRY_WITHOUT_DECELERATION": {
        "kind": "brake", "duration": 2.0, "params": {"intensity": 0.7},
        "why": "slow on the approach to the conflict",
    },
}


def omission_repairs(
    spec: ScenarioSpec,
    fused_causal: Optional[GraphDocument] = None,
    cfg: Optional[Config] = None,
) -> List[InterventionSpec]:
    """Propose an inserted behaviour for each supported non-action in the graph.

    Read off the *reconstruction*, not off the scenario. A non-action node exists
    only where an obligation was observed, the interval was bounded and the
    evidence covered it, so proposing a repair for one is proposing to test
    something the data already supports. Proposing repairs from the scenario
    definition instead would be testing the experiment's intent.

    Each proposal names the non-action it discharges, which is what makes it an
    omission repair rather than an ordinary safety improvement. The same inserted
    brake, offered for a vehicle under no obligation, is a prevention opportunity
    -- and :attr:`InterventionSpec.counterfactual_role` says so.
    """
    cfg = cfg if cfg is not None else Config({})
    if fused_causal is None:
        return []
    min_confidence = float(
        cfg.get("counterfactual.omission_repair.min_confidence", 0.8)
    )
    lead_in = float(cfg.get("counterfactual.omission_repair.lead_in_s", 0.6))
    participants = {p.participant_id for p in spec.participants}

    out: List[InterventionSpec] = []
    seen: set = set()
    for node in sorted(fused_causal.nodes, key=lambda n: (n.t_peak, n.event_id)):
        kind = (
            node.event_type.value if hasattr(node.event_type, "value")
            else str(node.event_type)
        )
        repair = _REPAIR_FOR_NON_ACTION.get(kind)
        if repair is None:
            continue
        pid = str(node.participant_id)
        if pid not in participants:
            continue
        if float(node.confidence) < min_confidence:
            # The node exists but the interval was not watched well enough to
            # stand on. Repairing an omission the evidence only half supports
            # would attribute causation to a claim that was itself hedged.
            LOGGER.debug(
                "omission repair skipped for %s: confidence %.2f below %.2f",
                node.event_id, float(node.confidence), min_confidence,
            )
            continue

        # The repair begins a little before the window opened, because a stop
        # performed at the instant the obligation came due is already too late
        # to be the stop that was required.
        interval = (node.detail or {}).get("monitored_interval") or [
            node.t_start, node.t_peak
        ]
        t_start = max(0.0, float(interval[0]) - lead_in)
        key = (pid, kind, round(t_start, 2))
        if key in seen:
            continue
        seen.add(key)

        action_id = "{0}_repair_{1}".format(pid, kind.lower())
        out.append(InterventionSpec(
            intervention_id="{0}__omission_repair".format(action_id),
            action_id=action_id,
            op="insert_action",
            params={
                "participant": pid,
                "kind": repair["kind"],
                "t_start": round(t_start, 3),
                "duration": repair["duration"],
                "params": dict(repair["params"]),
            },
            description=(
                "insert the behaviour {0} did not perform: {1} (repairing {2} "
                "asserted over {3})".format(
                    pid, repair["why"], kind, interval
                )
            ),
            targets_participant=pid,
            repairs_non_action=node.event_id,
        ))
    return out
