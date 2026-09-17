"""Lightweight structural causal model abstracted from a reconstructed DAG.

A reconstructed causal DAG (local or fused) is a graph of *evidence claims*: its
nodes are events extracted from onboard measurements and its edges are rule
hypotheses with confidences. A structural causal model is a different object: a
set of named variables and the functional dependences between them. This module
performs that abstraction -- one variable per graph node, one directed edge per
causal claim -- so that the counterfactual layer has a stable vocabulary to talk
about ("do(A_late_brake) = off") independently of how many redundant event nodes
the extractor happened to emit.

Interventional semantics -- read this before using :meth:`StructuralCausalModel.intervene`
---------------------------------------------------------------------------------------
``do(X = x)`` here means exactly what it means in Pearl's calculus: the
mechanism that normally sets ``X`` is replaced by an external assignment, so the
edges *into* ``X`` are cut while the edges *out of* ``X`` remain. What this
module does **not** do is predict the consequences of that assignment. It has no
structural equations, no fitted parameters and no distribution over exogenous
noise; propagating a value through it would amount to inventing physics.

In this project an intervention is realised **physically**: the identical
scenario is replayed in the simulator -- same map, same spawn state, same seed,
same controller parameters -- with one named scripted action disabled, delayed,
advanced or weakened (see :mod:`cdf.causal.interventions` and
:func:`cdf.simulation.runner.run_scenario`). The outcome is then *measured*, not
inferred. :meth:`StructuralCausalModel.intervene` exists to state which graph a
replay corresponds to and to keep the bookkeeping honest; every number that ends
up in an attribution report comes from a real replay.

This module is pure and observational: it reads a :class:`GraphDocument` and
nothing else, so it is equally usable on a local, a fused or an oracle graph.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import (
    OUTCOME_EVENT_TYPES,
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    to_jsonable,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    "VARIABLE_KINDS",
    "ACTION_EVENT_TYPES",
    "DEFAULT_VALUE_KEYS",
    "SCMVariable",
    "StructuralCausalModel",
    "scm_from_graph",
    "variable_kind",
    "describe_event",
    "observed_value",
]

#: The three roles a variable can play. ``action`` variables are the only ones a
#: physical intervention can target: they correspond to something a participant
#: *did*, which a scripted action can remove or weaken. ``state`` variables are
#: consequences of behaviour and geometry, ``outcome`` variables terminate a
#: chain.
VARIABLE_KINDS: Tuple[str, ...] = ("action", "state", "outcome")

#: Event types that record a commanded action rather than an observed state.
#: Kept deliberately narrow: an intervention handle must be something a driver or
#: controller *does*, not something that happens to the vehicle.
ACTION_EVENT_TYPES: Tuple[EventType, ...] = (
    EventType.BRAKE_ONSET,
    EventType.HARD_BRAKE,
    EventType.THROTTLE_ONSET,
    EventType.STEER_ONSET,
    EventType.LANE_CHANGE_LIKE_MANEUVER,
)

#: Preference order used to pick the single scalar that characterises an event.
#: An event may carry several measured quantities; the SCM keeps one so that
#: ``observed_value`` is comparable across replays. The order runs from the most
#: decision-relevant quantity (time to collision) to the least.
DEFAULT_VALUE_KEYS: Tuple[str, ...] = (
    "ttc_s",
    "ttc",
    "range_m",
    "closing_rate_mps",
    "accel_long_mps2",
    "target_accel_long_mps2",
    "speed_mps",
    "brake_cmd",
    "throttle_cmd",
    "steer_cmd",
    "lateral_offset_m",
    "lateral_rate_mps",
    "impulse",
)

_CAUSAL_EDGE_VALUES: Tuple[str, ...] = tuple(t.value for t in CausalEdgeType)


@dataclass
class SCMVariable:
    """One variable of the structural causal model.

    ``observed_value`` is the value this variable actually took in the run the
    model was abstracted from -- the *factual* value. It is never a prediction:
    a counterfactual value only ever comes from a replayed run.
    """

    name: str
    kind: str
    """One of :data:`VARIABLE_KINDS`."""
    participant: Optional[str] = None
    """Participant the variable belongs to; ``None`` for a variable that no
    single participant owns."""
    description: str = ""
    observed_value: Optional[float] = None

    def __post_init__(self) -> None:
        if self.kind not in VARIABLE_KINDS:
            raise ValueError(
                "SCMVariable {0!r} has unknown kind {1!r}; expected one of {2}".format(
                    self.name, self.kind, list(VARIABLE_KINDS)
                )
            )
        if not str(self.name):
            raise ValueError("SCMVariable needs a non-empty name")
        if self.observed_value is not None:
            self.observed_value = float(self.observed_value)


@dataclass
class StructuralCausalModel:
    """Variables and the directed dependences between them.

    The model is a container plus graph queries; it holds no structural
    equations (see the module docstring for why).
    """

    variables: Dict[str, SCMVariable] = field(default_factory=dict)
    edges: List[Tuple[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        # A dangling edge means the caller lost a variable somewhere; silently
        # dropping it would make the topology quietly wrong, so it is fatal.
        dangling: List[Tuple[str, str]] = []
        seen: Dict[Tuple[str, str], bool] = {}
        deduped: List[Tuple[str, str]] = []
        for edge in self.edges:
            src, dst = str(edge[0]), str(edge[1])
            if src not in self.variables or dst not in self.variables:
                dangling.append((src, dst))
                continue
            if src == dst:
                raise ValueError(
                    "self-loop {0!r} -> {0!r} is not a causal dependence".format(src)
                )
            if (src, dst) in seen:
                continue
            seen[(src, dst)] = True
            deduped.append((src, dst))
        if dangling:
            raise ValueError(
                "structural causal model has {0} edge(s) referring to unknown "
                "variables: {1}".format(len(dangling), dangling[:5])
            )
        self.edges = deduped

    # -- queries ----------------------------------------------------------

    def _require(self, name: str) -> str:
        if name not in self.variables:
            raise KeyError(
                "no variable {0!r} in the model (it has {1} variables)".format(
                    name, len(self.variables)
                )
            )
        return name

    def parents(self, name: str) -> List[str]:
        """Direct causes of ``name``, sorted for determinism."""
        self._require(name)
        return sorted({src for (src, dst) in self.edges if dst == name})

    def children(self, name: str) -> List[str]:
        """Direct effects of ``name``, sorted for determinism."""
        self._require(name)
        return sorted({dst for (src, dst) in self.edges if src == name})

    def ancestors(self, name: str) -> List[str]:
        """Every variable that can reach ``name``, sorted."""
        self._require(name)
        seen: Dict[str, bool] = {}
        frontier = list(self.parents(name))
        while frontier:
            node = frontier.pop()
            if node in seen:
                continue
            seen[node] = True
            frontier.extend(self.parents(node))
        return sorted(seen.keys())

    def topological_order(self) -> List[str]:
        """Variables ordered so that every cause precedes its effects.

        Ties are broken by name, so the order is reproducible across runs and
        machines. A cycle is a modelling bug -- a causal DAG that is not acyclic
        cannot be replayed coherently -- so it raises rather than returning a
        partial order.
        """
        indegree = {name: 0 for name in self.variables}
        outgoing: Dict[str, List[str]] = {name: [] for name in self.variables}
        for src, dst in self.edges:
            indegree[dst] += 1
            outgoing[src].append(dst)

        ready = sorted(n for n, d in indegree.items() if d == 0)
        order: List[str] = []
        while ready:
            node = ready.pop(0)
            order.append(node)
            newly_ready: List[str] = []
            for child in outgoing[node]:
                indegree[child] -= 1
                if indegree[child] == 0:
                    newly_ready.append(child)
            if newly_ready:
                ready = sorted(ready + newly_ready)

        if len(order) != len(self.variables):
            remaining = sorted(n for n in self.variables if n not in set(order))
            raise ValueError(
                "structural causal model contains a cycle; {0} variable(s) could "
                "not be ordered: {1}".format(len(remaining), remaining[:8])
            )
        return order

    def kind_of(self, name: str) -> str:
        """The role (``action``/``state``/``outcome``) of one variable."""
        return self.variables[self._require(name)].kind

    def variables_of_kind(self, kind: str) -> List[str]:
        """Names of every variable with the given role, sorted."""
        if kind not in VARIABLE_KINDS:
            raise ValueError(
                "unknown variable kind {0!r}; expected one of {1}".format(
                    kind, list(VARIABLE_KINDS)
                )
            )
        return sorted(n for n, v in self.variables.items() if v.kind == kind)

    # -- intervention -----------------------------------------------------

    def intervene(self, name: str, value: Optional[float]) -> "StructuralCausalModel":
        """Return the mutilated model corresponding to ``do(name = value)``.

        The incoming edges of ``name`` are removed -- the variable is now set
        from outside the system -- and its ``observed_value`` is replaced by the
        assigned value. Outgoing edges are untouched, because the downstream
        mechanisms are exactly what the replay is meant to exercise.

        This returns a *graph*, not a prediction. The assigned value becomes real
        only when :func:`cdf.causal.counterfactuals.run_counterfactual_suite`
        re-runs the scenario with the corresponding scripted action modified; the
        resulting outcome is then measured from that run's evidence.
        """
        self._require(name)
        variables = {key: replace(var) for key, var in self.variables.items()}
        variables[name] = replace(
            self.variables[name],
            observed_value=None if value is None else float(value),
        )
        edges = [(src, dst) for (src, dst) in self.edges if dst != name]
        return StructuralCausalModel(variables=variables, edges=edges)

    # -- serialisation ----------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """JSON-serialisable view, with variables sorted by name."""
        return {
            "n_variables": len(self.variables),
            "n_edges": len(self.edges),
            "kind_counts": {
                kind: len(self.variables_of_kind(kind)) for kind in VARIABLE_KINDS
            },
            "variables": [
                to_jsonable(self.variables[name]) for name in sorted(self.variables)
            ],
            "edges": [[src, dst] for (src, dst) in sorted(self.edges)],
        }

    def __len__(self) -> int:
        return len(self.variables)

    def __repr__(self) -> str:
        return "StructuralCausalModel(variables={0}, edges={1})".format(
            len(self.variables), len(self.edges)
        )


# ---------------------------------------------------------------------------
# Abstraction from a causal DAG
# ---------------------------------------------------------------------------


def scm_from_graph(
    doc: GraphDocument, cfg: Optional[Config] = None
) -> StructuralCausalModel:
    """Abstract a causal DAG into a structural causal model.

    One variable per graph node (named by its ``event_id``, which is already
    globally unique and carries provenance) and one edge per causal claim. Edges
    whose type is not a :class:`~cdf.common.schemas.CausalEdgeType` are dropped
    with a warning: an event-graph relation such as ``PRECEDES`` is a temporal
    observation, not a dependence, and letting it through would smuggle a
    non-causal claim into an interventional object. ``PREVENTS`` edges *are*
    kept -- the sign of a mechanism lives in the mechanism, not in the topology.

    ``causal.scm.min_edge_confidence`` (default 0.0, i.e. keep every claim) lets
    a caller abstract only the confident part of a reconstruction.
    """
    if not isinstance(doc, GraphDocument):
        raise TypeError(
            "scm_from_graph expects a GraphDocument, got {0!r}".format(type(doc))
        )
    if doc.graph_kind != "causal":
        raise ValueError(
            "scm_from_graph needs a causal DAG, got graph_kind={0!r}. An event "
            "graph records temporal relations, which are not causal "
            "dependences.".format(doc.graph_kind)
        )

    min_conf = float(cfg.get("causal.scm.min_edge_confidence", 0.0)) if cfg else 0.0
    value_keys: Sequence[str] = (
        [str(k) for k in cfg.get("causal.scm.value_keys", list(DEFAULT_VALUE_KEYS))]
        if cfg
        else list(DEFAULT_VALUE_KEYS)
    )

    variables: Dict[str, SCMVariable] = {}
    for node in doc.nodes:
        if node.event_id in variables:
            raise ValueError(
                "duplicate node id {0!r} in causal graph {1}".format(
                    node.event_id, doc.run_id or doc.scenario_id
                )
            )
        variables[node.event_id] = SCMVariable(
            name=node.event_id,
            kind=variable_kind(node),
            participant=node.participant_id or None,
            description=describe_event(node),
            observed_value=observed_value(node, value_keys),
        )

    edges: List[Tuple[str, str]] = []
    n_non_causal = 0
    n_low_confidence = 0
    for edge in doc.edges:
        if str(edge.edge_type) not in _CAUSAL_EDGE_VALUES:
            n_non_causal += 1
            continue
        if float(edge.confidence) < min_conf:
            n_low_confidence += 1
            continue
        edges.append((edge.source, edge.target))

    if n_non_causal:
        LOGGER.warning(
            "scm_from_graph dropped %d non-causal edge(s) from a graph declared "
            "causal (%s)",
            n_non_causal,
            doc.run_id or doc.scenario_id,
        )
    if n_low_confidence:
        LOGGER.info(
            "scm_from_graph dropped %d edge(s) below confidence %.2f",
            n_low_confidence,
            min_conf,
        )

    return StructuralCausalModel(variables=variables, edges=edges)


def variable_kind(event: Event) -> str:
    """Classify one event node as an ``action``, a ``state`` or an ``outcome``."""
    etype = _event_type_of(event)
    if etype is None:
        return "state"
    if etype in OUTCOME_EVENT_TYPES:
        return "outcome"
    if etype in ACTION_EVENT_TYPES:
        return "action"
    return "state"


def describe_event(event: Event) -> str:
    """Human-readable one-liner for an event node, used in reports."""
    subject = event.subject
    about = (
        " concerning subject {0}".format(subject)
        if subject and subject != "self"
        else ""
    )
    return "{0}{1}, observed by {2} at t={3:.2f}s".format(
        _event_type_value(event), about, event.participant_id, float(event.t_peak)
    )


def observed_value(
    event: Event, value_keys: Sequence[str] = DEFAULT_VALUE_KEYS
) -> Optional[float]:
    """The single scalar that best characterises an event, or ``None``.

    Preference order is explicit (``value_keys``) rather than dictionary order so
    that the same event always yields the same variable value; when none of the
    preferred keys is present the alphabetically first measured key is used,
    which is arbitrary but reproducible.
    """
    values = event.values or {}
    for key in value_keys:
        if key in values:
            return float(values[key])
    for key in sorted(values):
        return float(values[key])
    return None


def _event_type_of(event: Event) -> Optional[EventType]:
    """The typed event type, or ``None`` for an unrecognised value."""
    try:
        return EventType(event.event_type)
    except ValueError:
        LOGGER.warning(
            "event %s carries unknown event_type %r; treated as a state variable",
            event.event_id,
            event.event_type,
        )
        return None


def _event_type_value(event: Event) -> str:
    etype = event.event_type
    return etype.value if isinstance(etype, EventType) else str(etype)
