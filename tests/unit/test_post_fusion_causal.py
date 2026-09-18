"""The edges that only exist once the logs are merged.

These tests are about the discipline of the stage rather than its yield. An
inference layer that happily draws an arrow from a radar contact to a collision,
or backwards in time, or over the top of a claim a participant actually made,
would produce a graph that *looks* richer and means less. Each test below fixes
one of those.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import pytest

from cdf.common.config import load_run_config
from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.fusion.post_fusion_causal import (
    DEFAULT_GLOBAL_RULES,
    FORBIDDEN_CAUSAL_TYPES,
    ORIGIN_INFERRED,
    GlobalCausalRule,
    infer_global_causal_edges,
    node_subjects,
)

PARTICIPANTS = ["A", "B", "C"]


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


def node(
    event_id: str,
    event_type: EventType,
    participant: str,
    t: float,
    subject: Optional[str] = None,
    owners: Optional[List[str]] = None,
    confidence: float = 0.9,
) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant,
        t_start=t,
        t_peak=t,
        t_end=t + 0.2,
        subject=subject,
        values={},
        confidence=confidence,
        evidence=[],
        provenance=Provenance.FUSED,
        owners=list(owners or [participant]),
    )


def graph(nodes: List[Event], edges: Optional[List[GraphEdge]] = None) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal",
        scope=Provenance.FUSED,
        owner=None,
        run_id="R",
        scenario_id="S",
        seed=0,
        nodes=list(nodes),
        edges=list(edges or []),
        meta={},
    )


def infer(doc: GraphDocument, cfg, alignment=None, existing=None):
    return infer_global_causal_edges(
        doc, existing if existing is not None else doc.edges, {}, alignment, cfg,
        PARTICIPANTS,
    )


# ---------------------------------------------------------------------------
# The rule table itself
# ---------------------------------------------------------------------------


def test_every_rule_is_general_and_well_formed() -> None:
    """A rule may not name a scenario, and may not make an observation a cause."""
    names = [r.name for r in DEFAULT_GLOBAL_RULES]
    assert len(names) == len(set(names)), "rule names must be unique"
    for rule in DEFAULT_GLOBAL_RULES:
        endpoints = set(rule.cause_types) | set(rule.effect_types)
        assert not (endpoints & FORBIDDEN_CAUSAL_TYPES), rule.name
        assert 0.0 < rule.prior <= 1.0
        assert rule.max_lag_s > 0.0
        lowered = rule.name.lower()
        for forbidden in ("s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08",
                          "s09", "crash", "avoided", "yield", "cut_in"):
            assert forbidden not in lowered, (
                "rule {0!r} names a scenario or variant".format(rule.name)
            )


def test_a_rule_may_not_let_an_event_cause_itself() -> None:
    with pytest.raises(ValueError):
        GlobalCausalRule(
            name="bad", cause_types=(EventType.COLLISION.value,),
            effect_types=(EventType.COLLISION.value,),
            edge_type=CausalEdgeType.TRIGGERS, relation="same_pair",
            prior=0.5, max_lag_s=1.0, description="",
        )


def test_an_override_may_not_invent_cause_or_effect_types(cfg) -> None:
    """Configuration may tune a rule; it may not smuggle a new one in."""
    doc = graph([node("n1", EventType.HARD_BRAKE, "B", 1.0)])
    bad = cfg.with_overrides(
        {"fusion": {"post_fusion": {"overrides": {
            "remote_deceleration_closes_gap": {"cause_types": ["COLLISION"]}}}}}
    )
    with pytest.raises(KeyError):
        infer(doc, bad)
    unknown = cfg.with_overrides(
        {"fusion": {"post_fusion": {"overrides": {"no_such_rule": {"enabled": False}}}}}
    )
    with pytest.raises(KeyError):
        infer(doc, unknown)


# ---------------------------------------------------------------------------
# What the stage is for
# ---------------------------------------------------------------------------


def test_a_cross_participant_edge_is_created_that_no_vehicle_could_propose(cfg) -> None:
    """B's braking and the gap A measured closing: the whole point of the stage."""
    doc = graph([
        node("b_brake", EventType.HARD_BRAKE, "B", 4.0, owners=["B"]),
        node("b_decel", EventType.HARD_DECELERATION, "B", 4.3, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 4.8, subject="B", owners=["A"]),
    ])
    edges, diag = infer(doc, cfg)

    rules = {e.rule for e in edges}
    assert "remote_deceleration_closes_gap" in rules
    assert "remote_braking_contributes_to_closing" in rules
    cross = [e for e in edges if e.detail["cross_participant"]]
    assert cross, "the edge joins B's own log to A's; it is cross-participant"
    for edge in edges:
        assert edge.detail["origin"] == ORIGIN_INFERRED
        assert edge.provenance is Provenance.FUSED
        assert edge.detail["supporting_participants"]
        assert edge.detail["time_domain"] == "common"
        assert set(edge.detail["confidence_terms"]) >= {
            "rule_prior", "node_factor", "temporal_factor",
            "identity_factor", "clock_factor", "support_factor",
        }
    assert diag["n_added"] == len(edges)


def test_the_chain_of_two_impacts_is_recovered_without_naming_a_scenario(cfg) -> None:
    doc = graph([
        node("ab", EventType.COLLISION, "A", 5.9, subject="B", owners=["A", "B"]),
        node("bc", EventType.COLLISION, "C", 6.3, subject="B", owners=["C"]),
    ])
    edges, _diag = infer(doc, cfg)
    chain = [e for e in edges if e.rule == "global_impact_propagates_to_next_impact"]
    assert len(chain) == 1
    assert chain[0].source == "ab" and chain[0].target == "bc"


def test_two_impacts_far_apart_in_time_are_not_chained(cfg) -> None:
    """Sharing a vehicle is not enough; a chain reaction is also prompt.

    S14's independent_impacts variant is built on this: B rear-ends A, and eight
    seconds later C rolls into the stationary pile. The same three vehicles and
    the same pair structure as the chain variant, and no causal link between the
    two impacts. A rule that chained them on shared membership alone would give
    the same answer to both variants, which is exactly what that pair of
    scenarios exists to detect.
    """
    doc = graph([
        node("ab", EventType.COLLISION, "A", 7.4, subject="B", owners=["A", "B"]),
        node("bc", EventType.COLLISION, "C", 15.1, subject="B", owners=["C"]),
    ])
    edges, diag = infer(doc, cfg)
    assert not [
        e for e in edges if e.rule == "global_impact_propagates_to_next_impact"
    ]


def test_the_chain_window_is_what_separates_the_two_s14_variants(cfg) -> None:
    """Directly at the boundary, so a widened lag cannot pass unnoticed.

    Half a second apart chains; eight seconds apart does not. Whoever changes
    the window has to change this test and say why.
    """
    close = graph([
        node("ab", EventType.COLLISION, "A", 5.9, subject="B", owners=["A", "B"]),
        node("bc", EventType.COLLISION, "C", 6.4, subject="B", owners=["C"]),
    ])
    far = graph([
        node("ab", EventType.COLLISION, "A", 5.9, subject="B", owners=["A", "B"]),
        node("bc", EventType.COLLISION, "C", 13.9, subject="B", owners=["C"]),
    ])
    chained = lambda doc: [
        e for e in infer(doc, cfg)[0]
        if e.rule == "global_impact_propagates_to_next_impact"
    ]
    assert len(chained(close)) == 1
    assert chained(far) == []


def test_two_impacts_sharing_no_vehicle_are_never_chained(cfg) -> None:
    """Two unrelated pairs colliding a moment apart is a coincidence, not a chain."""
    doc = graph([
        node("ab", EventType.COLLISION, "A", 5.9, subject="B", owners=["A", "B"]),
        node("cd", EventType.COLLISION, "C", 6.3, subject="D", owners=["C", "D"]),
    ])
    edges, _diag = infer(doc, cfg)
    assert not [
        e for e in edges if e.rule == "global_impact_propagates_to_next_impact"
    ]


def test_an_unorderable_pair_of_impacts_asserts_no_chain(cfg) -> None:
    """Two impacts closer together than the clock error are not evidence of order."""
    doc = graph([
        node("ab", EventType.COLLISION, "A", 5.90, subject="B", owners=["A"]),
        node("bc", EventType.COLLISION, "C", 5.91, subject="B", owners=["C"]),
    ])
    alignment = {"offsets": {
        "A": {"confidence": 0.9, "residual": 0.30},
        "B": {"confidence": 0.9, "residual": 0.30},
        "C": {"confidence": 0.9, "residual": 0.30},
    }}
    edges, diag = infer(doc, cfg, alignment=alignment)
    assert not [e for e in edges if e.rule == "global_impact_propagates_to_next_impact"]
    reasons = {r["reason"] for r in diag["rejected"]}
    assert "order_not_resolved_beyond_clock_uncertainty" in reasons


# ---------------------------------------------------------------------------
# The three disciplines
# ---------------------------------------------------------------------------


def test_a_radar_contact_never_causes_anything(cfg) -> None:
    doc = graph([
        node("seen", EventType.RADAR_TRACK_APPEARED, "A", 1.0, subject="B"),
        node("hit", EventType.COLLISION, "A", 3.0, subject="B", owners=["A", "B"]),
    ])
    edges, _diag = infer(doc, cfg)
    touched = {e.source for e in edges} | {e.target for e in edges}
    assert "seen" not in touched, "an observation is evidence, never a cause"


def test_no_edge_runs_backwards_in_time(cfg) -> None:
    """The effect is recorded well before the cause: nothing may be concluded."""
    doc = graph([
        node("b_decel", EventType.HARD_DECELERATION, "B", 6.0, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 1.0, subject="B", owners=["A"]),
    ])
    edges, _diag = infer(doc, cfg)
    assert edges == []


def test_a_participants_own_claim_is_never_displaced(cfg) -> None:
    existing = GraphEdge(
        source="b_decel", target="closing",
        edge_type=CausalEdgeType.INCREASES_RISK_OF.value,
        confidence=0.4, provenance=Provenance.FUSED, rule="a_local_rule",
        detail={"origin": "local"},
    )
    doc = graph(
        [
            node("b_decel", EventType.HARD_DECELERATION, "B", 4.0, owners=["B"]),
            node("closing", EventType.RANGE_DECREASING, "A", 4.5, subject="B",
                 owners=["A"]),
        ],
        [existing],
    )
    edges, diag = infer(doc, cfg)
    assert not [e for e in edges if (e.source, e.target) == ("b_decel", "closing")]
    assert "already_claimed_by_participants" in {r["reason"] for r in diag["rejected"]}


def test_an_unresolved_subject_takes_part_in_nothing(cfg) -> None:
    """A claim about "some track" cannot be related to a claim about a vehicle."""
    doc = graph([
        node("b_decel", EventType.HARD_DECELERATION, "B", 4.0, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 4.5, subject="A::T007",
             owners=["A"]),
    ])
    edges, _diag = infer(doc, cfg)
    assert edges == []


def test_disabling_the_stage_yields_the_union_of_local_claims(cfg) -> None:
    """The ablation switch must actually switch it off."""
    doc = graph([
        node("b_decel", EventType.HARD_DECELERATION, "B", 4.0, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 4.5, subject="B", owners=["A"]),
    ])
    off = cfg.with_overrides({"fusion": {"post_fusion": {"enabled": False}}})
    edges, diag = infer(doc, off)
    assert edges == []
    assert diag["enabled"] is False and diag["notes"]


def test_inference_is_deterministic(cfg) -> None:
    doc = graph([
        node("b_brake", EventType.HARD_BRAKE, "B", 4.0, owners=["B"]),
        node("b_decel", EventType.HARD_DECELERATION, "B", 4.3, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 4.8, subject="B", owners=["A"]),
        node("ttc", EventType.CRITICAL_TTC, "A", 5.2, subject="B", owners=["A"]),
        node("hit", EventType.COLLISION, "A", 5.6, subject="B", owners=["A", "B"]),
    ])
    first = [(e.source, e.target, e.edge_type, e.confidence) for e in infer(doc, cfg)[0]]
    second = [(e.source, e.target, e.edge_type, e.confidence) for e in infer(doc, cfg)[0]]
    assert first == second


def test_a_poorly_aligned_clock_widens_tolerance_and_lowers_confidence(cfg) -> None:
    """The allowance comes from the alignment's own residual, not a constant.

    A cause may be *timestamped* slightly after its effect without being
    impossible, because an event peak is an estimate; ``min_lag_s`` is that
    allowance. What the clock residual does is widen it, by exactly as much as
    the alignment admits it could be wrong -- so the pair below (0.25 s backward,
    beyond the 0.15 s peak allowance) is refused under a clock that claims to be
    exact and admitted under one that reports a 0.3 s residual.
    """
    doc = graph([
        node("b_decel", EventType.HARD_DECELERATION, "B", 4.50, owners=["B"]),
        node("closing", EventType.RANGE_DECREASING, "A", 4.25, subject="B",
             owners=["A"]),
    ])
    tight = {"offsets": {p: {"confidence": 1.0, "residual": 0.0} for p in PARTICIPANTS}}
    loose = {"offsets": {p: {"confidence": 0.6, "residual": 0.3} for p in PARTICIPANTS}}

    assert infer(doc, cfg, alignment=tight)[0] == []
    relaxed = infer(doc, cfg, alignment=loose)[0]
    assert relaxed, "a wider clock tolerance must admit the pair"
    assert relaxed[0].detail["clock_slack_s"] > 0.0
    assert relaxed[0].detail["confidence_terms"]["clock_factor"] == pytest.approx(0.6)


# ---------------------------------------------------------------------------
# Subject semantics
# ---------------------------------------------------------------------------


def test_node_subjects_names_the_vehicles_a_claim_is_about(cfg) -> None:
    own = node("x", EventType.HARD_BRAKE, "B", 1.0)
    assert node_subjects(own, cfg, PARTICIPANTS) == (frozenset({"B"}), False, True)

    remote = node("y", EventType.TARGET_DECELERATION, "A", 1.0, subject="B")
    vehicles, relational, resolved = node_subjects(remote, cfg, PARTICIPANTS)
    assert vehicles == frozenset({"B"}) and not relational and resolved

    pair = node("z", EventType.CRITICAL_TTC, "A", 1.0, subject="B")
    vehicles, relational, resolved = node_subjects(pair, cfg, PARTICIPANTS)
    assert vehicles == frozenset({"A", "B"}) and relational and resolved

    unnamed = node("w", EventType.COLLISION, "A", 1.0, subject=None)
    _vehicles, relational, resolved = node_subjects(unnamed, cfg, PARTICIPANTS)
    assert relational and not resolved
