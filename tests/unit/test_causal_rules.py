"""Unit tests for :mod:`cdf.local.causal_rules` and :mod:`cdf.local.causal_graph`.

The rule table and the DAG builder are tested together because the table is only
meaningful through the graph it produces: the assertions here pin down the
interpretable chains the table must be able to express, the timing and subject
constraints that decide whether a rule fires, the shape of the confidence
function, and the acyclicity guarantee that the rest of the pipeline relies on.
"""

from __future__ import annotations

import math
from typing import List, Optional, Sequence

import networkx as nx
import pytest

from cdf.common.config import Config, load_run_config
from cdf.common.evidence import ParticipantEvidence
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventEdgeType,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
    make_event_id,
    make_track_id,
)
from cdf.graph.export import to_networkx
from cdf.local.causal_graph import build_causal_graph, confidence_terms, enforce_dag
from cdf.local.causal_rules import (
    DEFAULT_RULES,
    OBSERVATION_EVENT_TYPES,
    OVERRIDABLE_FIELDS,
    CausalRule,
    load_rules,
    rule_by_name,
    validate_rules,
)

PARTICIPANT = "A"
TRACK_1 = make_track_id(PARTICIPANT, 1)
TRACK_2 = make_track_id(PARTICIPANT, 2)

CAUSAL_EDGE_VALUES = set(e.value for e in CausalEdgeType)
EVENT_EDGE_VALUES = set(e.value for e in EventEdgeType)


def make_event(
    t: float,
    event_type: EventType,
    subject: Optional[str] = None,
    duration: float = 0.2,
    confidence: float = 1.0,
) -> Event:
    """A local event with a deterministic id, as the extractor would emit it."""
    return Event(
        event_id=make_event_id("local", PARTICIPANT, event_type.value, t, subject),
        event_type=event_type,
        participant_id=PARTICIPANT,
        t_start=t,
        t_peak=t,
        t_end=t + duration,
        subject=subject,
        confidence=confidence,
        provenance=Provenance.LOCAL,
    )


def evidence() -> ParticipantEvidence:
    return ParticipantEvidence(participant_id=PARTICIPANT)


def config(**causal_overrides) -> Config:
    """The real threshold registry, optionally with ``causal_rules`` overrides."""
    cfg = load_run_config()
    if causal_overrides:
        return cfg.with_overrides({"causal_rules": causal_overrides})
    return cfg


def build(events: Sequence[Event], cfg: Optional[Config] = None) -> GraphDocument:
    return build_causal_graph(
        events, evidence(), cfg or config(), run_id="R1", scenario_id="S01", seed=3
    )


def edge_between(doc: GraphDocument, source: Event, target: Event):
    matches = [
        e for e in doc.edges if e.source == source.event_id and e.target == target.event_id
    ]
    return matches[0] if matches else None


def rear_end_chain() -> List[Event]:
    """TARGET_DECELERATION -> RAPID_CLOSING -> CRITICAL_TTC -> HARD_BRAKE -> COLLISION."""
    return [
        make_event(0.0, EventType.RADAR_TRACK_APPEARED, TRACK_1),
        make_event(1.0, EventType.TARGET_DECELERATION, TRACK_1),
        make_event(2.0, EventType.RAPID_CLOSING, TRACK_1),
        make_event(3.0, EventType.CRITICAL_TTC, TRACK_1),
        make_event(3.6, EventType.HARD_BRAKE),
        make_event(4.4, EventType.COLLISION),
    ]


# ---------------------------------------------------------------------------
# The rule table itself
# ---------------------------------------------------------------------------


def test_default_rules_satisfy_the_table_invariants():
    validate_rules(DEFAULT_RULES)

    names = [r.name for r in DEFAULT_RULES]
    assert len(names) == len(set(names))
    for rule in DEFAULT_RULES:
        assert rule.edge_type in CAUSAL_EDGE_VALUES
        assert 0.0 < rule.prior <= 1.0
        assert rule.max_lag_s > 0.0
        assert rule.description.strip()
        assert not (rule.require_same_subject and rule.require_self_effect)


def test_observations_are_never_causes_or_effects():
    for rule in DEFAULT_RULES:
        for event_type in tuple(rule.cause_types) + tuple(rule.effect_types):
            assert event_type not in OBSERVATION_EVENT_TYPES, (
                "rule {0!r} uses observation event {1}".format(
                    rule.name, event_type.value
                )
            )


def find_rules(cause: EventType, effect: EventType) -> List[CausalRule]:
    return [
        r
        for r in DEFAULT_RULES
        if r.matches_cause(cause) and r.matches_effect(effect)
    ]


@pytest.mark.parametrize(
    "cause, effect, edge_type",
    [
        (EventType.TARGET_DECELERATION, EventType.RAPID_CLOSING, None),
        (EventType.RAPID_CLOSING, EventType.CRITICAL_TTC, None),
        (EventType.CRITICAL_TTC, EventType.HARD_BRAKE, None),
        (EventType.CUT_IN_LIKE_MOTION, EventType.RAPID_CLOSING, None),
        (EventType.CUT_IN_LIKE_MOTION, EventType.LOW_TTC, None),
        (EventType.LATERAL_CROSSING, EventType.CONFLICT_REGION_ENTRY, None),
        (EventType.PREDICTED_PATH_CONFLICT, EventType.CONFLICT_REGION_ENTRY, None),
        (EventType.CONFLICT_REGION_ENTRY, EventType.CRITICAL_TTC, None),
        (
            EventType.RANGE_DECREASING,
            EventType.LOW_TTC,
            CausalEdgeType.INCREASES_RISK_OF,
        ),
        (EventType.HARD_BRAKE, EventType.NEAR_MISS, CausalEdgeType.PREVENTS),
        (EventType.CRITICAL_TTC, EventType.COLLISION, CausalEdgeType.CAUSES_OUTCOME),
    ],
)
def test_interpretable_chains_are_expressible(cause, effect, edge_type):
    rules = find_rules(cause, effect)
    assert rules, "no rule relates {0} -> {1}".format(cause.value, effect.value)
    if edge_type is not None:
        assert edge_type.value in {r.edge_type for r in rules}


def test_every_local_event_type_takes_part_in_at_least_one_rule():
    """A type nobody can reason about is a taxonomy/rule-table mismatch."""
    used = set()
    for rule in DEFAULT_RULES:
        used.update(rule.cause_types)
        used.update(rule.effect_types)
    from cdf.common.schemas import LOCAL_EVENT_TYPES

    missing = sorted(
        t.value
        for t in LOCAL_EVENT_TYPES
        if t not in used and t not in OBSERVATION_EVENT_TYPES
    )
    assert missing == []


# ---------------------------------------------------------------------------
# Configuration binding
# ---------------------------------------------------------------------------


def test_load_rules_returns_the_table_unchanged_by_default():
    rules = load_rules(config())
    assert [r.name for r in rules] == [r.name for r in DEFAULT_RULES]
    for rule, default in zip(rules, DEFAULT_RULES):
        assert rule.prior == default.prior
        assert rule.max_lag_s == min(default.max_lag_s, 4.0)


def test_overrides_change_prior_and_edge_type():
    cfg = config(
        overrides={
            "critical_ttc_triggers_hard_braking": {
                "prior": 0.25,
                "edge_type": CausalEdgeType.CONTRIBUTES_TO.value,
                "max_lag_s": 9.0,
            }
        }
    )
    rule = rule_by_name(load_rules(cfg), "critical_ttc_triggers_hard_braking")
    assert rule.prior == pytest.approx(0.25)
    assert rule.edge_type == CausalEdgeType.CONTRIBUTES_TO.value
    # An explicit window override is honoured as given, not clipped by the ceiling.
    assert rule.max_lag_s == pytest.approx(9.0)


def test_disabled_rule_disappears_from_the_table_and_from_the_graph():
    cfg = config(
        overrides={"critical_ttc_triggers_hard_braking": {"enabled": False}}
    )
    names = [r.name for r in load_rules(cfg)]
    assert "critical_ttc_triggers_hard_braking" not in names
    assert len(names) == len(DEFAULT_RULES) - 1

    events = rear_end_chain()
    critical = events[3]
    brake = events[4]
    assert edge_between(build(events), critical, brake) is not None
    assert edge_between(build(events, cfg), critical, brake) is None


def test_default_max_lag_ceiling_tightens_the_whole_table():
    cfg = config(default_max_lag_s=1.0)
    assert all(r.max_lag_s <= 1.0 for r in load_rules(cfg))


def test_unknown_override_names_fail_loudly():
    with pytest.raises(KeyError):
        load_rules(config(overrides={"no_such_rule": {"prior": 0.5}}))
    with pytest.raises(KeyError):
        load_rules(
            config(overrides={"critical_ttc_causes_collision": {"weight": 0.5}})
        )


def test_out_of_range_prior_override_fails_loudly():
    with pytest.raises(ValueError):
        load_rules(config(overrides={"critical_ttc_causes_collision": {"prior": 1.5}}))


def test_overridable_fields_are_exactly_the_documented_ones():
    assert set(OVERRIDABLE_FIELDS) == {
        "enabled",
        "prior",
        "max_lag_s",
        "edge_type",
        "require_same_subject",
        "require_self_effect",
    }


# ---------------------------------------------------------------------------
# Causal graph: the chain
# ---------------------------------------------------------------------------


def test_chain_reaches_the_collision_node():
    events = rear_end_chain()
    doc = build(events)
    graph = to_networkx(doc)

    collision = events[5].event_id
    ancestors = nx.ancestors(graph, collision)
    types = set(graph.nodes[n]["event_type"] for n in ancestors)
    assert {
        EventType.TARGET_DECELERATION.value,
        EventType.RAPID_CLOSING.value,
        EventType.CRITICAL_TTC.value,
    } <= types
    # And the chain is a real path, not three disconnected accusations.
    assert nx.has_path(graph, events[1].event_id, collision)

    critical_to_collision = edge_between(doc, events[3], events[5])
    assert critical_to_collision is not None
    assert critical_to_collision.edge_type == CausalEdgeType.CAUSES_OUTCOME.value
    assert critical_to_collision.rule == "critical_ttc_causes_collision"


def test_causal_graph_is_a_dag():
    doc = build(rear_end_chain())
    assert nx.is_directed_acyclic_graph(to_networkx(doc))


def test_causal_graph_uses_only_causal_edge_types():
    doc = build(rear_end_chain())
    kinds = set(e.edge_type for e in doc.edges)
    assert kinds
    assert kinds <= CAUSAL_EDGE_VALUES
    assert not (kinds & EVENT_EDGE_VALUES)


def test_no_causal_edge_touches_a_radar_observation():
    events = rear_end_chain()
    appearance = events[0].event_id
    doc = build(events)
    assert doc.node_by_id(appearance) is not None, "the observation stays a node"
    for edge in doc.edges:
        assert edge.source != appearance, "an observation is not a physical cause"
        assert edge.target != appearance


def test_every_edge_is_traceable_to_a_rule_and_its_two_events():
    doc = build(rear_end_chain())
    known = {r.name for r in DEFAULT_RULES}
    for edge in doc.edges:
        assert edge.rule in known
        assert edge.provenance is Provenance.LOCAL
        assert edge.owners == [PARTICIPANT]
        assert edge.temporal_relation
        refs = {(ev.detail.get("part"), ev.ref) for ev in edge.evidence}
        assert ("cause", edge.source) in refs
        assert ("effect", edge.target) in refs
        assert 0.0 <= edge.confidence <= 1.0


def test_meta_carries_the_rule_table_and_the_rejection_diagnostics():
    doc = build(rear_end_chain())
    assert "rejected_edges" in doc.meta
    assert isinstance(doc.meta["rejected_edges"], list)
    assert len(doc.meta["rules"]) == len(DEFAULT_RULES)
    assert {r["name"] for r in doc.meta["rules"]} == {r.name for r in DEFAULT_RULES}
    assert doc.meta["parameters"]["min_edge_confidence"] == pytest.approx(0.25)


# ---------------------------------------------------------------------------
# Causal graph: timing and subject constraints
# ---------------------------------------------------------------------------


def test_effect_before_its_cause_produces_no_edge():
    critical = make_event(5.0, EventType.CRITICAL_TTC, TRACK_1)
    brake = make_event(4.0, EventType.HARD_BRAKE)
    doc = build([critical, brake])

    assert edge_between(doc, critical, brake) is None
    assert edge_between(doc, brake, critical) is None
    assert doc.edges == []


def test_effect_later_than_max_lag_produces_no_edge():
    rule = rule_by_name(list(DEFAULT_RULES), "critical_ttc_triggers_hard_braking")
    critical = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1)

    inside = make_event(rule.max_lag_s - 0.5, EventType.HARD_BRAKE)
    assert edge_between(build([critical, inside]), critical, inside) is not None

    outside = make_event(rule.max_lag_s + 0.5, EventType.HARD_BRAKE)
    assert edge_between(build([critical, outside]), critical, outside) is None


def test_same_subject_rules_do_not_cross_tracks():
    decel = make_event(1.0, EventType.TARGET_DECELERATION, TRACK_1)
    same = make_event(2.0, EventType.RAPID_CLOSING, TRACK_1)
    other = make_event(2.0, EventType.RAPID_CLOSING, TRACK_2)

    doc = build([decel, same, other])
    assert edge_between(doc, decel, same) is not None
    assert edge_between(doc, decel, other) is None


def test_self_effect_rules_require_an_ego_effect():
    """``critical_ttc_triggers_hard_braking`` must not fire on a track-scoped effect."""
    critical = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1)
    # HARD_DECELERATION is an effect type of the rule; tagging it with a track
    # subject makes it a claim about another object, which the rule forbids.
    mislabelled = make_event(0.5, EventType.HARD_DECELERATION, TRACK_1)
    ego = make_event(0.5, EventType.HARD_DECELERATION)

    assert edge_between(build([critical, mislabelled]), critical, mislabelled) is None
    assert edge_between(build([critical, ego]), critical, ego) is not None


def test_weak_edges_are_dropped_below_the_confidence_floor():
    critical = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1)
    brake = make_event(0.2, EventType.HARD_BRAKE)

    kept = edge_between(build([critical, brake]), critical, brake)
    assert kept is not None
    floor = kept.confidence + 0.01
    doc = build([critical, brake], config(min_edge_confidence=floor))
    assert edge_between(doc, critical, brake) is None
    assert doc.meta["rule_statistics"]["n_below_min_confidence"] > 0


# ---------------------------------------------------------------------------
# Confidence
# ---------------------------------------------------------------------------


def test_confidence_decreases_as_the_lag_grows():
    critical = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1)
    lags = [0.1, 0.5, 1.0, 1.8]
    confidences = []
    for lag in lags:
        brake = make_event(lag, EventType.HARD_BRAKE)
        edge = edge_between(build([critical, brake]), critical, brake)
        assert edge is not None, "lag {0} is inside the rule window".format(lag)
        confidences.append(edge.confidence)

    assert confidences == sorted(confidences, reverse=True)
    assert confidences[0] > confidences[-1]


def test_confidence_matches_the_published_formula():
    rule = rule_by_name(load_rules(config()), "critical_ttc_triggers_hard_braking")
    critical = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1, confidence=0.8)
    brake = make_event(1.0, EventType.HARD_BRAKE, confidence=0.6)
    edge = edge_between(build([critical, brake]), critical, brake)
    assert edge is not None

    node_weight, tau = 0.6, 3.0
    node_factor = node_weight * 0.5 * (0.8 + 0.6) + (1.0 - node_weight)
    expected = rule.prior * node_factor * math.exp(-1.0 / tau)
    assert edge.confidence == pytest.approx(expected)
    assert edge.detail["node_factor"] == pytest.approx(node_factor, abs=1e-6)
    assert edge.detail["lag_s"] == pytest.approx(1.0)


def test_lower_node_confidence_weakens_the_edge():
    strong_cause = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1, confidence=1.0)
    weak_cause = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1, confidence=0.2)
    brake = make_event(0.5, EventType.HARD_BRAKE)

    strong = edge_between(build([strong_cause, brake]), strong_cause, brake)
    weak = edge_between(build([weak_cause, brake]), weak_cause, brake)
    assert strong is not None and weak is not None
    assert weak.confidence < strong.confidence


def test_negative_lag_within_jitter_tolerance_cannot_exceed_the_rule_prior():
    rule = rule_by_name(list(DEFAULT_RULES), "critical_ttc_triggers_hard_braking")

    def terms_at(lag: float):
        return confidence_terms(
            rule,
            make_event(0.0, EventType.CRITICAL_TTC, TRACK_1),
            make_event(lag, EventType.HARD_BRAKE),
            lag_s=lag,
            node_weight=0.6,
            temporal_decay_s=3.0,
        )

    back = terms_at(-0.1)
    assert back["temporal_factor"] < 1.0
    assert back["confidence"] <= rule.prior + 1e-12

    # A time-reversed pair must not be *rewarded* for running backwards: the
    # tolerated jitter band exists to avoid discarding a coincident pair, not to
    # make it outscore a pair that was observed in the right order. Clamping the
    # lag at zero would give the reversed pair a flat factor of 1.0 and hand it
    # the win, which is exactly the evidence the ordering was supposed to supply.
    assert back["temporal_factor"] < terms_at(0.0)["temporal_factor"]
    assert back["temporal_factor"] == pytest.approx(
        terms_at(0.1)["temporal_factor"]
    )


def test_an_effect_that_precedes_its_cause_is_never_the_better_supported_one():
    """A reversed pair must not outrank an equally tight forward pair.

    ``causal_rules.min_lag_s`` tolerates a small negative lag so that two
    extractors resolving the same tick a few milliseconds apart do not lose an
    edge to rounding. That tolerance is the one place where the builder can state
    a hypothesis whose effect is timestamped *before* its cause, and it is
    therefore the one place where the temporal term can quietly invert the
    project's central claim -- that an effect occurring before its cause is not
    evidence for a causal link.

    The trap is specific. The published term is ``exp(-lag / tau)``, which for a
    negative lag exceeds one and would push an edge above its rule prior. Guarding
    that by clamping the lag at zero looks harmless and is not: every reversed
    pair then scores a flat ``1.0``, beating every correctly ordered pair however
    tightly coupled. Here that would rank a brake applied 0.1s *before* the
    critical TTC above an identical brake applied 0.1s *after* it -- the pipeline
    preferring the explanation that cannot physically hold. Nothing else in this
    file catches it: the mirror-rule test only asserts that one direction wins,
    not which, and every other confidence test uses a positive lag, where the
    clamp and the correct formula agree exactly.

    Within the jitter band the two orderings are deliberately scored *equally*
    rather than the forward one strictly higher: inside measurement error the
    ordering genuinely carries no information, so the rule prior is left to decide
    and the loser is recorded in ``rejected_edges``. The assertion is therefore
    'never worse for being in the right order', which is what the guard owes.
    """
    stimulus = make_event(3.0, EventType.CRITICAL_TTC, TRACK_1)
    brake_before = make_event(2.9, EventType.HARD_BRAKE)  # cannot be a response
    brake_after = make_event(3.1, EventType.HARD_BRAKE)  # the plausible response

    doc = build([stimulus, brake_before, brake_after])
    reversed_edge = edge_between(doc, stimulus, brake_before)
    forward_edge = edge_between(doc, stimulus, brake_after)

    # Both sit inside the tolerated band and the rule window, so the comparison is
    # about ranking and not about one of them having been filtered out.
    assert reversed_edge is not None and forward_edge is not None
    assert reversed_edge.detail["lag_s"] == pytest.approx(-0.1)
    assert forward_edge.detail["lag_s"] == pytest.approx(0.1)
    assert reversed_edge.rule == forward_edge.rule

    assert reversed_edge.confidence <= forward_edge.confidence + 1e-12, (
        "an effect timestamped before its cause is better supported than the same "
        "effect after it; the temporal term rewards running backwards"
    )
    assert reversed_edge.detail["temporal_factor"] < 1.0, (
        "a reversed pair scores a perfect temporal factor, so no forward pair can "
        "ever outrank it"
    )

    # The same property stated on the term itself: support depends on how tight
    # the coupling is, never on which side of zero the lag fell.
    rule = rule_by_name(load_rules(config()), reversed_edge.rule)
    symmetric = [
        confidence_terms(rule, stimulus, brake_after, lag, 0.6, 3.0)["temporal_factor"]
        for lag in (-0.4, -0.2, 0.2, 0.4)
    ]
    assert symmetric[0] == pytest.approx(symmetric[3])
    assert symmetric[1] == pytest.approx(symmetric[2])
    assert symmetric[1] > symmetric[0]

    # And the jitter tolerance may not be widened into a licence for backwards
    # causation from a configuration file.
    with pytest.raises(ValueError) as excinfo:
        build([stimulus, brake_before], config(min_lag_s=-5.0))
    assert "min_lag_s" in str(excinfo.value)


def test_invalid_confidence_parameters_fail_loudly():
    rule = rule_by_name(list(DEFAULT_RULES), "critical_ttc_causes_collision")
    cause = make_event(0.0, EventType.CRITICAL_TTC, TRACK_1)
    effect = make_event(1.0, EventType.COLLISION)
    with pytest.raises(ValueError):
        confidence_terms(rule, cause, effect, 1.0, node_weight=1.5, temporal_decay_s=3.0)
    with pytest.raises(ValueError):
        confidence_terms(rule, cause, effect, 1.0, node_weight=0.6, temporal_decay_s=0.0)


# ---------------------------------------------------------------------------
# enforce_dag
# ---------------------------------------------------------------------------


def cyclic_document() -> GraphDocument:
    """Three events wired into a cycle, with one deliberately weakest link."""
    a = make_event(0.0, EventType.CONFLICT_REGION_ENTRY, TRACK_1)
    b = make_event(0.4, EventType.STEER_ONSET)
    c = make_event(0.8, EventType.LATERAL_CROSSING, TRACK_1)

    def edge(source: Event, target: Event, confidence: float, rule: str) -> GraphEdge:
        return GraphEdge(
            source=source.event_id,
            target=target.event_id,
            edge_type=CausalEdgeType.TRIGGERS.value,
            confidence=confidence,
            provenance=Provenance.LOCAL,
            rule=rule,
            temporal_relation="before",
        )

    return GraphDocument(
        graph_kind="causal",
        scope=Provenance.LOCAL,
        owner=PARTICIPANT,
        nodes=[a, b, c],
        edges=[
            edge(a, b, 0.90, "rule_ab"),
            edge(b, c, 0.80, "rule_bc"),
            edge(c, a, 0.40, "rule_ca"),
        ],
    )


def test_enforce_dag_rejects_the_weakest_link_of_a_cycle_with_a_reason():
    doc = cyclic_document()
    acyclic, rejected = enforce_dag(doc)

    assert nx.is_directed_acyclic_graph(to_networkx(acyclic))
    assert len(acyclic.edges) == 2
    assert len(rejected) == 1

    report = rejected[0]
    assert set(report.keys()) == {
        "source",
        "target",
        "edge_type",
        "rule",
        "confidence",
        "reason",
    }
    assert report["rule"] == "rule_ca"
    assert report["confidence"] == pytest.approx(0.40)
    assert "cycle" in report["reason"]
    # The surviving edges are the two strongest ones.
    assert {e.rule for e in acyclic.edges} == {"rule_ab", "rule_bc"}
    # The input document is not mutated.
    assert len(doc.edges) == 3


def test_enforce_dag_rejects_a_self_loop():
    doc = cyclic_document()
    node = doc.nodes[0]
    doc.edges.append(
        GraphEdge(
            source=node.event_id,
            target=node.event_id,
            edge_type=CausalEdgeType.TRIGGERS.value,
            confidence=0.99,
            provenance=Provenance.LOCAL,
            rule="rule_self",
        )
    )
    acyclic, rejected = enforce_dag(doc)

    assert nx.is_directed_acyclic_graph(to_networkx(acyclic))
    reasons = {r["rule"]: r["reason"] for r in rejected}
    assert "self loop" in reasons["rule_self"]
    assert all(e.source != e.target for e in acyclic.edges)


def test_enforce_dag_keeps_an_already_acyclic_document_intact():
    doc = cyclic_document()
    doc.edges = doc.edges[:2]
    acyclic, rejected = enforce_dag(doc)
    assert rejected == []
    assert len(acyclic.edges) == 2


def test_enforce_dag_rejects_an_edge_with_an_unknown_endpoint():
    doc = cyclic_document()
    doc.edges[0].target = "local:A:GHOST:0000000000"
    with pytest.raises(ValueError) as excinfo:
        enforce_dag(doc)
    assert "not a node" in str(excinfo.value)


def test_builder_reports_cycles_it_had_to_break():
    """A steer/conflict pair close enough in time to be explained both ways.

    ``own_lateral_manoeuvre_creates_conflict`` and
    ``lateral_threat_triggers_evasive_steering`` are deliberate mirror images, so
    within the tolerated jitter window both fire and one must be rejected.
    """
    steer = make_event(1.0, EventType.STEER_ONSET)
    conflict = make_event(1.05, EventType.CONFLICT_REGION_ENTRY, TRACK_1)
    doc = build([steer, conflict])

    assert nx.is_directed_acyclic_graph(to_networkx(doc))
    pairs = {(e.source, e.target) for e in doc.edges}
    assert len(pairs) == 1, "only one direction may survive"
    rejected = doc.meta["rejected_edges"]
    assert rejected and any("cycle" in r["reason"] for r in rejected)


# ---------------------------------------------------------------------------
# Boundary guards and determinism
# ---------------------------------------------------------------------------


def test_foreign_participant_event_is_rejected():
    events = rear_end_chain()
    stray = make_event(2.0, EventType.HARD_BRAKE)
    stray.participant_id = "B"
    with pytest.raises(ValueError):
        build(events + [stray])


def test_oracle_event_type_is_rejected():
    with pytest.raises(ValueError):
        build(rear_end_chain() + [make_event(2.0, EventType.ORACLE_SIGNAL_VIOLATION)])


def test_build_is_deterministic():
    events = rear_end_chain()
    first = build(events)
    second = build(list(reversed(events)))
    signature = lambda doc: [
        (e.source, e.target, e.edge_type, e.rule, round(e.confidence, 9))
        for e in doc.edges
    ]
    assert signature(first) == signature(second)


def test_empty_event_list_yields_an_empty_dag():
    doc = build([])
    assert doc.nodes == [] and doc.edges == []
    assert doc.graph_kind == "causal" and doc.scope is Provenance.LOCAL
    assert doc.meta["rejected_edges"] == []
