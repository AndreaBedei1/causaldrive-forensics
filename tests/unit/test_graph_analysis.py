"""Unit tests for cdf.graph.analysis.GraphAnalyzer.

The graphs are hand-built so that every expected ancestor set, path list, cut
vertex and knowledge gain is known exactly before the call is made.
"""

from __future__ import annotations

import copy
from typing import List, Optional

import networkx as nx
import pytest

from cdf.common.config import Config
from cdf.common.schemas import (
    CausalEdgeType,
    Evidence,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.graph.analysis import GraphAnalyzer

CONTRIB = CausalEdgeType.CONTRIBUTES_TO.value
CAUSES = CausalEdgeType.CAUSES_OUTCOME.value


def make_event(
    event_id: str,
    event_type: EventType,
    t_peak: float,
    participant_id: str = "A",
    subject: Optional[str] = None,
    confidence: float = 1.0,
    provenance: Provenance = Provenance.LOCAL,
    owners: Optional[List[str]] = None,
    t_start: Optional[float] = None,
    t_end: Optional[float] = None,
) -> Event:
    """A minimal but schema-valid event."""
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant_id,
        t_start=t_peak - 0.1 if t_start is None else t_start,
        t_peak=t_peak,
        t_end=t_peak + 0.1 if t_end is None else t_end,
        subject=subject,
        confidence=confidence,
        provenance=provenance,
        owners=list(owners) if owners else [],
    )


def edge(
    source: str,
    target: str,
    edge_type: str = CONTRIB,
    confidence: float = 0.8,
    provenance: Provenance = Provenance.LOCAL,
) -> GraphEdge:
    return GraphEdge(
        source=source,
        target=target,
        edge_type=edge_type,
        confidence=confidence,
        provenance=provenance,
    )


def make_doc(
    nodes: List[Event],
    edges: List[GraphEdge],
    owner: Optional[str] = "A",
    scope: Provenance = Provenance.LOCAL,
) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal",
        scope=scope,
        owner=owner,
        run_id="run-test",
        scenario_id="S01",
        seed=11,
        nodes=list(nodes),
        edges=list(edges),
        meta={"note": "hand-built"},
    )


def diamond() -> GraphDocument:
    """``R -> A -> C`` and ``R -> B -> C``; ``C`` is the collision."""
    nodes = [
        make_event("R", EventType.THROTTLE_ONSET, 1.0),
        make_event("A", EventType.RANGE_DECREASING, 2.0, subject="A::T001"),
        make_event("B", EventType.BRAKE_ONSET, 3.0),
        make_event("C", EventType.COLLISION, 4.0),
    ]
    edges = [edge("R", "A"), edge("R", "B"), edge("A", "C", CAUSES), edge("B", "C", CAUSES)]
    return make_doc(nodes, edges)


def chain() -> GraphDocument:
    """``R -> X -> C``: ``X`` is the only explanation of the outcome."""
    nodes = [
        make_event("R", EventType.THROTTLE_ONSET, 1.0),
        make_event("X", EventType.CRITICAL_TTC, 2.0, subject="A::T001"),
        make_event("C", EventType.COLLISION, 3.0),
    ]
    return make_doc(nodes, [edge("R", "X"), edge("X", "C", CAUSES)])


# ---------------------------------------------------------------------------
# structure queries
# ---------------------------------------------------------------------------


def test_outcome_nodes_only_lists_outcome_types():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.outcome_nodes() == ["C"]


def test_ancestors_and_descendants_on_the_diamond():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.ancestors("C") == ["R", "A", "B"]  # ordered by t_peak
    assert analyzer.ancestors("R") == []
    assert analyzer.descendants("R") == ["A", "B", "C"]
    assert analyzer.descendants("C") == []
    assert analyzer.ancestors("A") == ["R"]


def test_causal_paths_to_enumerates_both_branches():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.causal_paths_to("C") == [["R", "A", "C"], ["R", "B", "C"]]
    assert analyzer.all_paths_to_outcome() == {"C": [["R", "A", "C"], ["R", "B", "C"]]}


def test_causal_paths_respect_the_cutoff():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.causal_paths_to("C", cutoff=1) == []
    assert len(analyzer.causal_paths_to("C", cutoff=2)) == 2


def test_root_causes_are_the_in_degree_zero_ancestors():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.root_causes("C") == ["R"]
    assert analyzer.root_causes() == ["R"]
    assert analyzer.root_causes("A") == ["R"]
    assert analyzer.root_causes("R") == []


def test_root_causes_of_a_forest_without_outcomes():
    nodes = [
        make_event("p", EventType.THROTTLE_ONSET, 1.0),
        make_event("q", EventType.STEER_ONSET, 2.0),
        make_event("r", EventType.ACCELERATION, 3.0),
    ]
    analyzer = GraphAnalyzer(make_doc(nodes, [edge("p", "q")]))
    assert analyzer.outcome_nodes() == []
    assert analyzer.root_causes() == ["p", "r"]


def test_shortest_causal_path():
    analyzer = GraphAnalyzer(diamond())
    assert analyzer.shortest_causal_path("R", "C") in (["R", "A", "C"], ["R", "B", "C"])
    assert len(analyzer.shortest_causal_path("R", "C")) == 3
    assert analyzer.shortest_causal_path("A", "B") is None


def test_unknown_node_fails_loudly():
    analyzer = GraphAnalyzer(diamond())
    with pytest.raises(KeyError):
        analyzer.ancestors("nope")
    with pytest.raises(KeyError):
        analyzer.remove_edge("R", "C")


# ---------------------------------------------------------------------------
# slicing -- payloads preserved, analyzer untouched
# ---------------------------------------------------------------------------


def test_slices_preserve_payloads_and_do_not_mutate_the_analyzer():
    doc = diamond()
    doc.nodes[0].evidence.append(Evidence(kind="controls", ref="A", t_start=0.9, t_end=1.1))
    analyzer = GraphAnalyzer(doc)

    reduced, _report = analyzer.remove_node("A")
    assert sorted(reduced.node_ids()) == ["B", "C", "R"]
    # The surviving payloads are the very same records, evidence included.
    assert reduced.node_by_id("R") is doc.node_by_id("R")
    assert reduced.node_by_id("R").evidence[0].ref == "A"
    assert len(reduced.edges) == 2

    # The analyzer still describes the intact graph.
    assert analyzer.graph.number_of_nodes() == 4
    assert analyzer.graph.number_of_edges() == 4
    assert len(doc.nodes) == 4
    assert analyzer.ancestors("C") == ["R", "A", "B"]


def test_vehicle_subgraph_keeps_co_owned_nodes():
    nodes = [
        make_event("a1", EventType.HARD_BRAKE, 1.0, participant_id="A"),
        make_event("b1", EventType.CUT_IN_LIKE_MOTION, 2.0, participant_id="B"),
        make_event(
            "f1",
            EventType.COLLISION,
            3.0,
            participant_id="B",
            owners=["A", "B"],
            provenance=Provenance.FUSED,
        ),
    ]
    doc = make_doc(nodes, [edge("a1", "f1", CAUSES), edge("b1", "f1", CAUSES)], owner=None)
    analyzer = GraphAnalyzer(doc)

    sub_a = analyzer.vehicle_subgraph("A")
    assert sorted(sub_a.node_ids()) == ["a1", "f1"]
    assert [(e.source, e.target) for e in sub_a.edges] == [("a1", "f1")]
    assert sub_a.owner == "A"

    sub_b = analyzer.vehicle_subgraph("B")
    assert sorted(sub_b.node_ids()) == ["b1", "f1"]


def test_filter_by_confidence_drops_nodes_and_their_edges():
    nodes = [
        make_event("R", EventType.THROTTLE_ONSET, 1.0, confidence=0.9),
        make_event("A", EventType.RANGE_DECREASING, 2.0, confidence=0.2),
        make_event("C", EventType.COLLISION, 3.0, confidence=0.95),
    ]
    edges = [edge("R", "A", CONTRIB, confidence=0.7), edge("A", "C", CAUSES, confidence=0.9)]
    analyzer = GraphAnalyzer(make_doc(nodes, edges))

    filtered = analyzer.filter_by_confidence(min_node=0.5)
    assert sorted(filtered.node_ids()) == ["C", "R"]
    assert filtered.edges == []

    edge_filtered = analyzer.filter_by_confidence(min_edge=0.8)
    assert sorted(edge_filtered.node_ids()) == ["A", "C", "R"]
    assert [(e.source, e.target) for e in edge_filtered.edges] == [("A", "C")]


def test_filter_by_provenance():
    nodes = [
        make_event("l1", EventType.HARD_BRAKE, 1.0, provenance=Provenance.LOCAL),
        make_event("f1", EventType.CUT_IN_LIKE_MOTION, 2.0, provenance=Provenance.FUSED),
        make_event("l2", EventType.COLLISION, 3.0, provenance=Provenance.LOCAL),
    ]
    edges = [
        edge("l1", "l2", CAUSES, provenance=Provenance.LOCAL),
        edge("f1", "l2", CAUSES, provenance=Provenance.FUSED),
    ]
    analyzer = GraphAnalyzer(make_doc(nodes, edges))

    local_only = analyzer.filter_by_provenance([Provenance.LOCAL])
    assert sorted(local_only.node_ids()) == ["l1", "l2"]
    assert [(e.source, e.target) for e in local_only.edges] == [("l1", "l2")]

    with pytest.raises(ValueError):
        analyzer.filter_by_provenance([])


def test_filter_by_time_uses_temporal_support_not_just_the_peak():
    nodes = [
        make_event("early", EventType.THROTTLE_ONSET, 2.0),
        make_event("inside", EventType.BRAKE_ONSET, 3.0),
        make_event("late", EventType.COLLISION, 4.0),
        # Peaks before the window but is still active inside it.
        make_event(
            "spanning",
            EventType.RANGE_DECREASING,
            1.2,
            subject="A::T001",
            t_start=1.0,
            t_end=5.0,
        ),
    ]
    analyzer = GraphAnalyzer(make_doc(nodes, []))
    kept = analyzer.filter_by_time(2.5, 3.5)
    assert sorted(kept.node_ids()) == ["inside", "spanning"]

    with pytest.raises(ValueError):
        analyzer.filter_by_time(3.0, 1.0)


def test_minimal_outcome_subgraph_drops_causally_irrelevant_nodes():
    doc = diamond()
    doc.nodes.append(make_event("U", EventType.LANE_CHANGE_LIKE_MANEUVER, 5.0))
    doc.edges.append(edge("R", "U"))
    analyzer = GraphAnalyzer(doc)

    minimal = analyzer.minimal_outcome_subgraph()
    assert sorted(minimal.node_ids()) == ["A", "B", "C", "R"]
    assert len(minimal.edges) == 4


# ---------------------------------------------------------------------------
# interventions
# ---------------------------------------------------------------------------


def test_remove_node_on_a_cut_vertex_disconnects_the_outcome():
    analyzer = GraphAnalyzer(chain())
    _reduced, report = analyzer.remove_node("X")
    assert report["outcome_still_reachable"] is False
    assert report["outcomes_disconnected"] == ["C"]
    assert report["lost_paths"] == 1
    assert report["lost_ancestors"] == ["R", "X"]


def test_remove_node_on_a_redundant_node_keeps_the_outcome_reachable():
    analyzer = GraphAnalyzer(diamond())
    _reduced, report = analyzer.remove_node("A")
    assert report["outcome_still_reachable"] is True
    assert report["outcomes_disconnected"] == []
    assert report["paths_before"] == 2
    assert report["paths_after"] == 1
    assert report["lost_paths"] == 1
    assert report["lost_ancestors"] == ["A"]


def test_remove_edge_reports_the_same_reachability_loss():
    diamond_analyzer = GraphAnalyzer(diamond())
    reduced, report = diamond_analyzer.remove_edge("A", "C")
    assert report["outcome_still_reachable"] is True
    assert report["lost_paths"] == 1
    assert len(reduced.nodes) == 4  # nodes are kept, only the claim is dropped
    assert ("A", "C") not in [(e.source, e.target) for e in reduced.edges]

    chain_analyzer = GraphAnalyzer(chain())
    _reduced2, report2 = chain_analyzer.remove_edge("X", "C")
    assert report2["outcome_still_reachable"] is False
    assert report2["outcomes_disconnected"] == ["C"]


def test_candidate_intervention_nodes_rank_the_cut_vertex_first():
    # R -> M -> C, R -> L -> M: M is the cut vertex, L only a redundant branch,
    # U hangs off R and has nothing to do with the outcome.
    nodes = [
        make_event("R", EventType.THROTTLE_ONSET, 1.0),
        make_event("L", EventType.STEER_ONSET, 1.5),
        make_event("M", EventType.HARD_BRAKE, 2.0),
        make_event("C", EventType.COLLISION, 3.0),
        make_event("U", EventType.LANE_CHANGE_LIKE_MANEUVER, 3.5),
    ]
    edges = [
        edge("R", "M"),
        edge("R", "L"),
        edge("L", "M"),
        edge("M", "C", CAUSES),
        edge("R", "U"),
    ]
    analyzer = GraphAnalyzer(make_doc(nodes, edges))
    candidates = analyzer.candidate_intervention_nodes()
    ids = [c["event_id"] for c in candidates]

    assert ids[0] == "M"
    assert candidates[0]["disconnects_outcome"] is True
    assert candidates[0]["paths_cut"] == 2
    assert ids.index("M") < ids.index("L")
    # The causally irrelevant node is not a replay candidate at all.
    assert "U" not in ids
    # The outcome itself is never a candidate.
    assert "C" not in ids

    leaf = [c for c in candidates if c["event_id"] == "L"][0]
    assert leaf["disconnects_outcome"] is False
    assert leaf["paths_cut"] == 1

    assert set(candidates[0]) == {
        "event_id",
        "event_type",
        "participant_id",
        "t_peak",
        "paths_cut",
        "disconnects_outcome",
    }
    assert candidates[0]["event_type"] == "HARD_BRAKE"
    assert candidates[0]["t_peak"] == pytest.approx(2.0)


def test_candidate_intervention_nodes_is_empty_without_an_outcome():
    nodes = [
        make_event("p", EventType.THROTTLE_ONSET, 1.0),
        make_event("q", EventType.STEER_ONSET, 2.0),
    ]
    analyzer = GraphAnalyzer(make_doc(nodes, [edge("p", "q")]))
    assert analyzer.candidate_intervention_nodes() == []


# ---------------------------------------------------------------------------
# cross-graph comparison
# ---------------------------------------------------------------------------


def _reference_doc() -> GraphDocument:
    """Oracle view: A braked, B cut in, both contributed to the collision."""
    nodes = [
        make_event("g1", EventType.HARD_BRAKE, 1.0, participant_id="A"),
        make_event("g2", EventType.CUT_IN_LIKE_MOTION, 2.0, participant_id="B"),
        make_event("g3", EventType.COLLISION, 3.0, participant_id="A"),
    ]
    return make_doc(
        nodes, [edge("g1", "g3", CAUSES), edge("g2", "g3", CAUSES)], owner=None,
        scope=Provenance.ORACLE,
    )


def _poor_baseline_doc() -> GraphDocument:
    """Single-vehicle view: only A's own brake and the impact."""
    nodes = [
        make_event("a1", EventType.HARD_BRAKE, 1.0, participant_id="A"),
        make_event("a3", EventType.COLLISION, 3.0, participant_id="A"),
    ]
    return make_doc(nodes, [edge("a1", "a3", CAUSES)], owner="A")


def _rich_doc() -> GraphDocument:
    """Fused view: both causes, plus one claim the oracle does not support."""
    nodes = [
        make_event("f1", EventType.HARD_BRAKE, 1.0, participant_id="A", provenance=Provenance.FUSED),
        make_event(
            "f2", EventType.CUT_IN_LIKE_MOTION, 2.0, participant_id="B", provenance=Provenance.FUSED
        ),
        make_event("f3", EventType.COLLISION, 3.0, participant_id="A", provenance=Provenance.FUSED),
        make_event("f4", EventType.STEER_ONSET, 5.0, participant_id="A", provenance=Provenance.FUSED),
    ]
    edges = [edge("f1", "f3", CAUSES), edge("f2", "f3", CAUSES), edge("f4", "f3", CAUSES)]
    return make_doc(nodes, edges, owner=None, scope=Provenance.FUSED)


def test_compare_to_reports_both_directions():
    analyzer = GraphAnalyzer(_rich_doc())
    result = analyzer.compare_to(_poor_baseline_doc())

    assert set(result["nodes_only_self"]) == {"f2", "f4"}
    assert result["nodes_only_other"] == []
    assert result["n_nodes_both"] == 2
    assert result["n_edges_both"] == 1
    assert set(result["edges_only_self"]) == {
        ("f2", "f3", CAUSES),
        ("f4", "f3", CAUSES),
    }
    assert result["edges_only_other"] == []


def test_compare_to_is_symmetric():
    rich = GraphAnalyzer(_rich_doc())
    poor = GraphAnalyzer(_poor_baseline_doc())
    forward = rich.compare_to(_poor_baseline_doc())
    backward = poor.compare_to(_rich_doc())
    assert forward["n_nodes_both"] == backward["n_nodes_both"]
    assert forward["n_nodes_only_self"] == backward["n_nodes_only_other"]
    assert forward["n_edges_only_self"] == backward["n_edges_only_other"]


def test_knowledge_gain_lists_exactly_what_the_richer_graph_recovers():
    analyzer = GraphAnalyzer(_rich_doc())
    gain = analyzer.knowledge_gain(_poor_baseline_doc(), _reference_doc())

    # B's cut-in is the one oracle-supported node the single vehicle never had.
    assert gain["nodes_gained"] == ["f2"]
    assert gain["n_nodes_gained"] == 1
    assert gain["edges_gained"] == [("f2", "f3", CAUSES)]
    assert gain["n_edges_gained"] == 1

    assert gain["baseline_node_recall"] == pytest.approx(2.0 / 3.0)
    assert gain["self_node_recall"] == pytest.approx(1.0)
    assert gain["baseline_edge_recall"] == pytest.approx(0.5)
    assert gain["self_edge_recall"] == pytest.approx(1.0)


def test_knowledge_gain_is_zero_against_itself():
    doc = _rich_doc()
    analyzer = GraphAnalyzer(doc)
    gain = analyzer.knowledge_gain(copy.deepcopy(doc), _reference_doc())
    assert gain["nodes_gained"] == []
    assert gain["edges_gained"] == []
    assert gain["baseline_node_recall"] == gain["self_node_recall"] == pytest.approx(1.0)


def test_knowledge_gain_ignores_unsupported_claims():
    """The extra ``f4`` claim is a false positive, never a gain."""
    analyzer = GraphAnalyzer(_rich_doc())
    empty_baseline = make_doc([], [], owner="A")
    gain = analyzer.knowledge_gain(empty_baseline, _reference_doc())
    assert "f4" not in gain["nodes_gained"]
    assert gain["n_nodes_gained"] == 3
    assert gain["n_edges_gained"] == 2
    assert gain["baseline_node_recall"] == 0.0


# ---------------------------------------------------------------------------
# summary
# ---------------------------------------------------------------------------


def test_summary_reports_the_causal_quantities():
    analyzer = GraphAnalyzer(diamond())
    summary = analyzer.summary()
    assert summary["n_nodes"] == 4
    assert summary["n_edges"] == 4
    assert summary["is_dag"] is True
    assert summary["outcome_nodes"] == ["C"]
    assert summary["n_root_causes"] == 1
    assert summary["n_causal_paths_to_outcome"] == 2
    assert summary["longest_causal_path_nodes"] == 3
    assert summary["n_intervention_candidates"] == 3  # R, A, B
    assert summary["mean_node_confidence"] == pytest.approx(1.0)
    assert summary["mean_edge_confidence"] == pytest.approx(0.8)


def test_canonical_time_bucket_comes_from_the_configuration():
    """A finer bucket must separate two events a configured tolerance apart."""
    near = make_doc(
        [make_event("x1", EventType.HARD_BRAKE, 1.0, participant_id="A")], [], owner="A"
    )
    shifted = make_doc(
        [make_event("y1", EventType.HARD_BRAKE, 1.4, participant_id="A")], [], owner="A"
    )

    coarse = GraphAnalyzer(near, cfg=Config({"evaluation": {"event_match": {"canonical_time_bucket_s": 1.0}}}))
    assert coarse.compare_to(shifted)["n_nodes_both"] == 1

    fine = GraphAnalyzer(near, cfg=Config({"evaluation": {"event_match": {"canonical_time_bucket_s": 0.1}}}))
    result = fine.compare_to(shifted)
    assert result["time_bucket_s"] == pytest.approx(0.1)
    assert result["n_nodes_both"] == 0
    assert result["nodes_only_self"] == ["x1"]
    assert result["nodes_only_other"] == ["y1"]


def test_graph_property_exposes_the_networkx_view():
    analyzer = GraphAnalyzer(diamond())
    assert isinstance(analyzer.graph, nx.DiGraph)
    assert analyzer.graph.nodes["C"]["event_type"] == "COLLISION"
    assert nx.is_directed_acyclic_graph(analyzer.graph)
    assert len(analyzer) == 4
