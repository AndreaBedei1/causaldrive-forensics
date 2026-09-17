"""From a fused graph to "why did this collision happen?".

The chain is: nodes grouped into behavioural episodes, episodes at the roots of
the causal paths into a collision named as contributors, and the whole thing
rendered as sentences by template. These tests fix the two things that matter
about that: it must recover the chain that was actually there, and it must
decline to name anybody when the graph does not support naming anybody.
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
from cdf.graph.analysis import GraphAnalyzer
from cdf.graph.episodes import extract_episodes
from cdf.graph.reconstruction import (
    ancestors_of_outcome,
    build_attribution_hypothesis,
    build_incident_reconstruction,
    causal_paths_to_outcome,
    explain_outcome,
    root_contributors,
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
    values: Optional[Dict[str, Any]] = None,
    confidence: float = 0.9,
) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant,
        t_start=t,
        t_peak=t,
        t_end=t + 0.3,
        subject=subject,
        values=dict(values or {}),
        confidence=confidence,
        evidence=[],
        provenance=Provenance.FUSED,
        owners=[participant],
    )


def edge(
    source: str,
    target: str,
    edge_type: CausalEdgeType = CausalEdgeType.TRIGGERS,
    confidence: float = 0.8,
) -> GraphEdge:
    return GraphEdge(
        source=source, target=target, edge_type=edge_type.value,
        confidence=confidence, provenance=Provenance.FUSED, rule="r", detail={},
    )


def graph(nodes: List[Event], edges: List[GraphEdge]) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=Provenance.FUSED, owner=None, run_id="R",
        scenario_id="S06", seed=0, nodes=nodes, edges=edges, meta={},
    )


@pytest.fixture
def rear_end() -> GraphDocument:
    """B brakes hard, A closes on it and does not slow, A hits B."""
    return graph(
        [
            node("b_brake", EventType.HARD_BRAKE, "B", 4.0, values={"decel": 7.0}),
            node("b_decel", EventType.HARD_DECELERATION, "B", 4.2, values={"decel": 7.2}),
            node("closing", EventType.RANGE_DECREASING, "A", 4.6, subject="B"),
            node("ttc", EventType.CRITICAL_TTC, "A", 5.1, subject="B",
                 values={"ttc_s": 0.8}),
            node("hit", EventType.COLLISION, "A", 5.6, subject="B",
                 values={"delta_v": 9.0}),
        ],
        [
            edge("b_brake", "b_decel"),
            edge("b_decel", "closing", CausalEdgeType.INCREASES_RISK_OF),
            edge("closing", "ttc", CausalEdgeType.INCREASES_RISK_OF),
            edge("ttc", "hit", CausalEdgeType.TRIGGERS),
        ],
    )


# ---------------------------------------------------------------------------
# Ancestry and chains
# ---------------------------------------------------------------------------


def test_the_ancestry_of_the_collision_is_everything_that_led_to_it(cfg, rear_end) -> None:
    analyzer = GraphAnalyzer(rear_end, cfg)
    assert ancestors_of_outcome(analyzer, "hit") == [
        "b_brake", "b_decel", "closing", "ttc"
    ]


def test_the_chain_is_recovered_root_first(cfg, rear_end) -> None:
    paths = causal_paths_to_outcome(analyzer_for(cfg, rear_end), "hit")
    assert paths == [["b_brake", "b_decel", "closing", "ttc", "hit"]]


def analyzer_for(cfg, doc) -> GraphAnalyzer:
    return GraphAnalyzer(doc, cfg)


def test_a_node_outside_the_ancestry_is_not_in_any_chain(cfg, rear_end) -> None:
    """An unrelated manoeuvre elsewhere in the scene explains nothing here."""
    doc = graph(
        list(rear_end.nodes) + [node("c_lane", EventType.LANE_CHANGE_LIKE_MANEUVER, "C", 3.0)],
        list(rear_end.edges),
    )
    assert "c_lane" not in ancestors_of_outcome(analyzer_for(cfg, doc), "hit")
    assert all("c_lane" not in p for p in causal_paths_to_outcome(
        analyzer_for(cfg, doc), "hit"
    ))


def test_the_chain_of_two_impacts_keeps_its_order(cfg) -> None:
    doc = graph(
        [
            node("ab", EventType.COLLISION, "A", 5.9, subject="B"),
            node("bc", EventType.COLLISION, "C", 6.2, subject="B"),
        ],
        [edge("ab", "bc")],
    )
    recon = build_incident_reconstruction(doc, cfg, PARTICIPANTS)
    order = [c["outcome_id"] for c in recon["collision_order"]]
    assert order == ["ab", "bc"]
    assert recon["n_collisions"] == 2


# ---------------------------------------------------------------------------
# Episodes: behaviours, not node ids
# ---------------------------------------------------------------------------


def test_nodes_become_a_behaviour_with_a_name(cfg, rear_end) -> None:
    episodes = extract_episodes(rear_end, cfg, PARTICIPANTS)
    kinds = {(e.participant_id, e.kind) for e in episodes}
    assert ("B", "emergency_braking") in kinds, kinds
    for episode in episodes:
        assert episode.node_ids, "an episode must cite the nodes it summarises"
        assert episode.t_start <= episode.t_end
        assert episode.episode_id


def test_an_episode_never_claims_a_failure_to_yield(cfg) -> None:
    """Right of way is map and rule knowledge; fusion has neither."""
    from cdf.graph.episodes import EPISODE_KINDS

    assert "failure_to_yield" not in EPISODE_KINDS
    assert not any("yield" in k for k in EPISODE_KINDS)


def test_the_root_of_the_chain_is_reported_as_a_behaviour(cfg, rear_end) -> None:
    analyzer = analyzer_for(cfg, rear_end)
    episodes = extract_episodes(rear_end, cfg, PARTICIPANTS)
    roots = root_contributors(analyzer, "hit", episodes)
    assert roots, "the chain has a root and it belongs to a behaviour"
    assert all("b_brake" in r.node_ids or r.participant_id == "B" for r in roots)


# ---------------------------------------------------------------------------
# Attribution from the graph alone
# ---------------------------------------------------------------------------


def test_the_graph_names_the_behaviour_at_the_root_of_the_chain(cfg, rear_end) -> None:
    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, rear_end, cfg)
    block = hypothesis["collisions"][0]
    assert block["outcome_id"] == "hit"
    named = {c["participant_id"] for c in block["contributors"]}
    assert named == {"B"}, "only the behaviour at the root of the chain is named"
    for contributor in block["contributors"]:
        assert 0.0 < contributor["confidence"] <= 1.0
        assert contributor["episode_kind"]


def test_a_collision_nothing_explains_is_reported_as_unexplained(cfg) -> None:
    """A bare collision node with no ancestry must not produce a contributor."""
    doc = graph([node("hit", EventType.COLLISION, "A", 5.0, subject="B")], [])
    recon = build_incident_reconstruction(doc, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, doc, cfg)
    block = hypothesis["collisions"][0]
    assert block["contributors"] == []
    assert block["attribution_class"] == "insufficient_evidence"
    assert recon["incidents"][0]["chains"] == []


def test_a_vehicle_that_braked_and_avoided_it_is_not_a_contributor(cfg) -> None:
    """A preventive chain is reported as preventive, never as a contribution."""
    doc = graph(
        [
            node("c_brake", EventType.HARD_BRAKE, "C", 4.0, values={"decel": 8.0}),
            node("ttc", EventType.CRITICAL_TTC, "C", 4.4, subject="A",
                 values={"ttc_s": 0.9}),
            node("a_brake", EventType.HARD_BRAKE, "A", 5.0, values={"decel": 7.0}),
            node("hit", EventType.COLLISION, "A", 5.5, subject="B"),
        ],
        [
            edge("a_brake", "hit", CausalEdgeType.TRIGGERS),
            edge("c_brake", "ttc", CausalEdgeType.PREVENTS),
        ],
    )
    recon = build_incident_reconstruction(doc, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, doc, cfg)
    block = hypothesis["collisions"][0]
    assert "C" not in {c["participant_id"] for c in block["contributors"]}


def test_no_verdict_uses_the_language_of_blame(cfg, rear_end) -> None:
    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, rear_end, cfg)
    hypothesis_text = " ".join(
        _strings(hypothesis, skip_keys={"disclaimer"})
    ).lower()
    recon_text = " ".join(_strings(recon, skip_keys={"disclaimer"})).lower()
    for word in ("guilty", "guilt", "fault", "liable", "liability", "blame",
                 "culpab", "responsib"):
        assert word not in hypothesis_text, word
        assert word not in recon_text, word
    # The only place the word may appear is the disclaimer that denies it.
    denial = hypothesis["disclaimer"].lower()
    assert "not a finding of legal fault" in denial
    assert "not a fault percentage" in denial


def _strings(value, skip_keys=frozenset()):
    """Every string in a nested structure, minus the values of ``skip_keys``."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [
            s
            for key, item in value.items()
            if key not in skip_keys
            for s in _strings(item, skip_keys)
        ]
    if isinstance(value, (list, tuple)):
        return [s for item in value for s in _strings(item, skip_keys)]
    return []


# ---------------------------------------------------------------------------
# The sentences
# ---------------------------------------------------------------------------


def test_the_explanation_is_assembled_from_the_record(cfg, rear_end) -> None:
    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, rear_end, cfg)
    answer = explain_outcome(recon, hypothesis, "hit")

    assert "A" in answer["headline"] and "B" in answer["headline"]
    assert "5.6" in answer["headline"] or "5.60" in answer["headline"]
    assert answer["chains"], "the explanation must show the chain it rests on"
    assert isinstance(answer["uncertainties"], list)
    assert answer["attribution"]["class"] in {
        "single_initiator", "shared_contribution", "joint_contribution",
        "contributing_but_not_necessary", "insufficient_evidence",
    }


def test_the_explanation_is_deterministic(cfg, rear_end) -> None:
    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    hypothesis = build_attribution_hypothesis(recon, rear_end, cfg)
    first = explain_outcome(recon, hypothesis, "hit")
    second = explain_outcome(recon, hypothesis, "hit")
    assert first == second


def test_asking_about_an_outcome_that_was_not_reconstructed_is_an_error(
    cfg, rear_end
) -> None:
    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    with pytest.raises(KeyError):
        explain_outcome(recon, None, "no_such_node")


def test_the_reconstruction_records_no_privileged_field(cfg, rear_end) -> None:
    """Nothing in the reconstruction may come from the oracle's own vocabulary."""
    import json

    recon = build_incident_reconstruction(rear_end, cfg, PARTICIPANTS)
    text = json.dumps(recon)
    for forbidden in ("actor_id", "carla_id", "causal_template", "expected_culprit",
                      "true_offset", "lane_id", "road_id", "junction"):
        assert forbidden not in text, forbidden
