"""Unit tests for cdf.graph.matching and cdf.graph.metrics.

Every case builds a synthetic graph whose correct answer is known by
construction and asserts the exact counts, not merely that the call returned.
"""

from __future__ import annotations

import copy
from typing import List, Optional

import pytest

from cdf.common.schemas import (
    CausalEdgeType,
    Event,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
)
from cdf.graph.matching import canonical_key, match_edges, match_events
from cdf.graph.metrics import (
    compare_local_vs_fused,
    event_metrics,
    graph_structure_metrics,
    prf1,
)

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
) -> Event:
    """A minimal but schema-valid event centred on ``t_peak``."""
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant_id,
        t_start=t_peak - 0.1,
        t_peak=t_peak,
        t_end=t_peak + 0.1,
        subject=subject,
        confidence=confidence,
        provenance=provenance,
    )


def make_doc(
    nodes: List[Event],
    edges: List[GraphEdge],
    owner: str = "A",
    scope: Provenance = Provenance.LOCAL,
) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal",
        scope=scope,
        owner=owner,
        run_id="run-test",
        scenario_id="S01",
        seed=7,
        nodes=list(nodes),
        edges=list(edges),
    )


def edge(source: str, target: str, edge_type: str = CONTRIB, confidence: float = 0.8) -> GraphEdge:
    return GraphEdge(
        source=source,
        target=target,
        edge_type=edge_type,
        confidence=confidence,
        provenance=Provenance.LOCAL,
    )


def diamond_doc() -> GraphDocument:
    """``R -> A -> C`` and ``R -> B -> C`` with ``C`` the collision outcome."""
    nodes = [
        make_event("R", EventType.THROTTLE_ONSET, 1.0),
        make_event("A", EventType.RANGE_DECREASING, 2.0, subject="A::T001"),
        make_event("B", EventType.BRAKE_ONSET, 3.0),
        make_event("C", EventType.COLLISION, 4.0),
    ]
    edges = [
        edge("R", "A"),
        edge("R", "B"),
        edge("A", "C", CAUSES),
        edge("B", "C", CAUSES),
    ]
    return make_doc(nodes, edges)


def clone(doc: GraphDocument) -> GraphDocument:
    """A structurally identical but independently allocated document."""
    return GraphDocument.from_dict(copy.deepcopy(doc.to_dict()))


# ---------------------------------------------------------------------------
# prf1
# ---------------------------------------------------------------------------


def test_prf1_known_counts():
    scores = prf1(tp=6, fp=2, fn=3)
    assert scores["precision"] == pytest.approx(6.0 / 8.0)
    assert scores["recall"] == pytest.approx(6.0 / 9.0)
    assert scores["f1"] == pytest.approx(2 * 0.75 * (2.0 / 3.0) / (0.75 + 2.0 / 3.0))


def test_prf1_is_zero_when_undefined():
    for scores in (prf1(0, 0, 0), prf1(0, 5, 0), prf1(0, 0, 5)):
        assert scores["precision"] == 0.0
        assert scores["recall"] == 0.0
        assert scores["f1"] == 0.0


def test_prf1_rejects_negative_counts():
    with pytest.raises(ValueError):
        prf1(-1, 0, 0)


# ---------------------------------------------------------------------------
# event matching
# ---------------------------------------------------------------------------


def test_event_matching_respects_tolerance():
    pred = [make_event("p1", EventType.HARD_BRAKE, 10.5)]
    truth = [make_event("t1", EventType.HARD_BRAKE, 10.0)]

    loose = match_events(pred, truth, tolerance_s=1.5)
    assert loose["n_matched"] == 1
    assert loose["matches"][0][0] == "p1"
    assert loose["matches"][0][1] == "t1"
    assert loose["matches"][0][2] == pytest.approx(0.5)
    assert loose["mean_abs_dt"] == pytest.approx(0.5)

    tight = match_events(pred, truth, tolerance_s=0.2)
    assert tight["n_matched"] == 0
    assert tight["unmatched_a"] == ["p1"]
    assert tight["unmatched_b"] == ["t1"]
    assert tight["mean_abs_dt"] == 0.0


def test_event_matching_requires_same_type_by_default():
    pred = [make_event("p1", EventType.HARD_BRAKE, 5.0)]
    truth = [make_event("t1", EventType.BRAKE_ONSET, 5.0)]
    assert match_events(pred, truth, tolerance_s=1.0)["n_matched"] == 0
    assert match_events(pred, truth, tolerance_s=1.0, require_same_type=False)["n_matched"] == 1


def test_event_matching_is_globally_optimal_not_greedy():
    # A greedy nearest-first pass takes (p_a, t_b) because 0.1 is the smallest
    # single error, leaving a total of 0.1 + 0.45 = 0.55. The optimal assignment
    # is (p_a, t_a) + (p_b, t_b) with a total of 0.30 + 0.05 = 0.35.
    pred = [
        make_event("p_a", EventType.LOW_TTC, 1.30, subject="A::T001"),
        make_event("p_b", EventType.LOW_TTC, 1.45, subject="A::T001"),
    ]
    truth = [
        make_event("t_a", EventType.LOW_TTC, 1.00, subject="A::T001"),
        make_event("t_b", EventType.LOW_TTC, 1.40, subject="A::T001"),
    ]
    result = match_events(pred, truth, tolerance_s=0.5)
    assert result["n_matched"] == 2
    assert result["map_a_to_b"] == {"p_a": "t_a", "p_b": "t_b"}
    total = sum(abs(dt) for _a, _b, dt in result["matches"])
    assert total == pytest.approx(0.35)


def test_event_matching_is_one_to_one():
    pred = [
        make_event("p1", EventType.RAPID_CLOSING, 2.0),
        make_event("p2", EventType.RAPID_CLOSING, 2.05),
    ]
    truth = [make_event("t1", EventType.RAPID_CLOSING, 2.0)]
    result = match_events(pred, truth, tolerance_s=1.0)
    assert result["n_matched"] == 1
    assert len(result["unmatched_a"]) == 1


def test_event_matching_rejects_duplicate_ids():
    dup = [
        make_event("same", EventType.LOW_TTC, 1.0),
        make_event("same", EventType.LOW_TTC, 2.0),
    ]
    with pytest.raises(ValueError):
        match_events(dup, [], tolerance_s=1.0)


def test_subject_map_resolves_track_ids_across_graphs():
    pred = [make_event("p1", EventType.LOW_TTC, 3.0, participant_id="A", subject="A::T004")]
    truth = [make_event("t1", EventType.LOW_TTC, 3.0, participant_id="A", subject="B")]

    unresolved = match_events(pred, truth, tolerance_s=1.0, require_same_subject=True)
    assert unresolved["n_matched"] == 0

    resolved = match_events(
        pred,
        truth,
        tolerance_s=1.0,
        require_same_subject=True,
        subject_map_a={"A::T004": "B"},
    )
    assert resolved["n_matched"] == 1


def test_canonical_key_buckets_time_and_resolves_subject():
    ev = make_event("e", EventType.LOW_TTC, 2.4, participant_id="A", subject="A::T002")
    assert canonical_key(ev, time_bucket_s=1.0) == ("LOW_TTC", "A", "A::T002", 2)
    assert canonical_key(ev, {"A::T002": "B"}, 1.0) == ("LOW_TTC", "A", "B", 2)
    # A self event resolves to the "self" sentinel whatever the raw value is.
    own = make_event("o", EventType.HARD_BRAKE, 0.0, subject=None)
    assert canonical_key(own, time_bucket_s=1.0)[2] == "self"


# ---------------------------------------------------------------------------
# graph structure metrics
# ---------------------------------------------------------------------------


def test_graph_compared_to_itself_is_perfect():
    truth = diamond_doc()
    pred = clone(truth)
    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)

    assert m["n_nodes_matched"] == 4
    assert m["node_precision"] == 1.0
    assert m["node_recall"] == 1.0
    assert m["node_f1"] == 1.0
    assert m["n_edges_matched"] == 4
    assert m["edge_precision"] == 1.0
    assert m["edge_recall"] == 1.0
    assert m["edge_f1"] == 1.0
    assert m["structural_hamming_distance"] == 0
    assert m["missing_edges"] == []
    assert m["extra_edges"] == []
    assert m["reversed_edges"] == []


def test_self_comparison_survives_duplicate_timings():
    # Two nodes of the same type at the same instant: only the identity
    # tie-breaker keeps the assignment from swapping them and inventing edges.
    nodes = [
        make_event("n1", EventType.RANGE_DECREASING, 2.0, subject="A::T001"),
        make_event("n2", EventType.RANGE_DECREASING, 2.0, subject="A::T002"),
        make_event("out", EventType.NEAR_MISS, 3.0),
    ]
    doc = make_doc(nodes, [edge("n1", "out", CAUSES)])
    m = graph_structure_metrics(clone(doc), doc, tolerance_s=1.5)
    assert m["structural_hamming_distance"] == 0
    assert m["edge_f1"] == 1.0


def test_self_comparison_is_invariant_to_node_ordering():
    """Ambiguous zero-cost pairs must not be resolved by listing order.

    Two same-type, same-instant nodes give the assignment two equally cheap
    permutations. If it picks the swapped one the edge endpoints move and an
    identical graph scores SHD 2, so the matcher's identity preference is what
    makes this comparison a property of the graphs rather than of their order.
    """
    n1 = make_event("n1", EventType.RANGE_DECREASING, 2.0, subject="A::T001")
    n2 = make_event("n2", EventType.RANGE_DECREASING, 2.0, subject="A::T002")
    out = make_event("out", EventType.NEAR_MISS, 3.0)
    causal = [edge("n1", "out", CAUSES)]

    truth = make_doc([n1, n2, out], causal)
    reordered = make_doc([n2, n1, out], causal)

    m = graph_structure_metrics(reordered, truth, tolerance_s=1.5)
    assert [(a, b) for a, b, _dt in m["node_matches"]] == [
        ("n2", "n2"),
        ("n1", "n1"),
        ("out", "out"),
    ]
    assert m["structural_hamming_distance"] == 0
    assert m["edge_f1"] == 1.0


def test_one_missing_edge_costs_recall_only():
    truth = diamond_doc()
    pred = clone(truth)
    pred.edges = [e for e in pred.edges if not (e.source == "B" and e.target == "C")]

    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)
    assert m["n_missing_edges"] == 1
    assert m["n_extra_edges"] == 0
    assert m["n_reversed_edges"] == 0
    assert m["structural_hamming_distance"] == 1
    assert m["edge_precision"] == 1.0
    assert m["edge_recall"] < 1.0
    assert m["edge_recall"] == pytest.approx(3.0 / 4.0)
    assert (m["missing_edges"][0]["source"], m["missing_edges"][0]["target"]) == ("B", "C")


def test_one_spurious_edge_costs_precision_only():
    truth = diamond_doc()
    pred = clone(truth)
    pred.edges.append(edge("R", "C", CONTRIB))

    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)
    assert m["n_extra_edges"] == 1
    assert m["n_missing_edges"] == 0
    assert m["n_reversed_edges"] == 0
    assert m["structural_hamming_distance"] == 1
    assert m["edge_recall"] == 1.0
    assert m["edge_precision"] < 1.0
    assert m["edge_precision"] == pytest.approx(4.0 / 5.0)
    assert (m["extra_edges"][0]["source"], m["extra_edges"][0]["target"]) == ("R", "C")


def test_reversed_edge_is_one_reversal_not_a_miss_plus_an_extra():
    truth = diamond_doc()
    pred = clone(truth)
    pred.edges = [e for e in pred.edges if not (e.source == "R" and e.target == "A")]
    pred.edges.append(edge("A", "R", CONTRIB))

    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)
    assert m["n_reversed_edges"] == 1
    assert m["n_missing_edges"] == 0
    assert m["n_extra_edges"] == 0
    assert m["structural_hamming_distance"] == 1
    rev = m["reversed_edges"][0]
    assert (rev["a_source"], rev["a_target"]) == ("A", "R")
    assert (rev["b_source"], rev["b_target"]) == ("R", "A")
    # A reversal is a wrong claim and a missed claim at once.
    assert m["edge_precision"] == pytest.approx(3.0 / 4.0)
    assert m["edge_recall"] == pytest.approx(3.0 / 4.0)


def test_edge_onto_an_unmatched_node_is_counted_by_default():
    truth = diamond_doc()
    pred = clone(truth)
    # An extra predicted node the reference does not contain, plus an edge to it.
    pred.nodes.append(make_event("X", EventType.STEER_ONSET, 12.0))
    pred.edges.append(edge("R", "X"))

    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)
    assert m["n_nodes_matched"] == 4
    assert m["node_recall"] == 1.0
    assert m["node_precision"] == pytest.approx(4.0 / 5.0)
    assert m["n_edges_touching_unmatched_pred"] == 1
    assert m["n_extra_edges"] == 1
    assert m["edge_precision"] == pytest.approx(4.0 / 5.0)
    assert m["structural_hamming_distance"] == 1

    restricted = graph_structure_metrics(
        pred, truth, tolerance_s=1.5, restrict_to_matched_nodes=True
    )
    assert restricted["n_unmappable_edges_pred"] == 1
    assert restricted["n_extra_edges"] == 0
    assert restricted["edge_precision"] == 1.0
    assert restricted["structural_hamming_distance"] == 0


def test_missing_node_also_loses_its_edges():
    """A reconstruction that never found a node cannot claim its causal edges."""
    truth = diamond_doc()
    pred = clone(truth)
    pred.nodes = [n for n in pred.nodes if n.event_id != "B"]
    pred.edges = [e for e in pred.edges if "B" not in (e.source, e.target)]

    m = graph_structure_metrics(pred, truth, tolerance_s=1.5)
    assert m["n_nodes_matched"] == 3
    assert m["node_recall"] == pytest.approx(3.0 / 4.0)
    assert m["n_missing_edges"] == 2
    assert m["n_extra_edges"] == 0
    assert m["edge_recall"] == pytest.approx(2.0 / 4.0)
    assert m["edge_precision"] == 1.0
    assert m["structural_hamming_distance"] == 2


def test_match_edges_uses_the_node_correspondence():
    a_nodes = [
        make_event("a1", EventType.BRAKE_ONSET, 1.0),
        make_event("a2", EventType.COLLISION, 2.0),
    ]
    b_nodes = [
        make_event("b1", EventType.BRAKE_ONSET, 1.05),
        make_event("b2", EventType.COLLISION, 2.05),
    ]
    a_doc = make_doc(a_nodes, [edge("a1", "a2", CAUSES)])
    b_doc = make_doc(b_nodes, [edge("b1", "b2", CAUSES)])

    node_match = match_events(a_doc.nodes, b_doc.nodes, tolerance_s=0.5)["map_a_to_b"]
    assert node_match == {"a1": "b1", "a2": "b2"}

    res = match_edges(a_doc, b_doc, node_match)
    assert res["n_matched"] == 1
    assert res["n_missing"] == res["n_extra"] == res["n_reversed"] == 0


def test_match_edges_rejects_duplicate_edge_keys():
    nodes = [make_event("n1", EventType.BRAKE_ONSET, 1.0), make_event("n2", EventType.COLLISION, 2.0)]
    doc = make_doc(nodes, [edge("n1", "n2"), edge("n1", "n2")])
    with pytest.raises(ValueError):
        match_edges(doc, doc, {"n1": "n1", "n2": "n2"})


# ---------------------------------------------------------------------------
# event metrics
# ---------------------------------------------------------------------------


def test_event_metrics_counts_and_timing_errors():
    truth = [
        make_event("t1", EventType.BRAKE_ONSET, 1.0),
        make_event("t2", EventType.LOW_TTC, 2.0, subject="A::T001"),
        make_event("t3", EventType.COLLISION, 3.0),
    ]
    pred = [
        make_event("p1", EventType.BRAKE_ONSET, 1.2),
        make_event("p2", EventType.LOW_TTC, 2.4, subject="A::T001"),
        make_event("p_spurious", EventType.STEER_ONSET, 9.0),
    ]
    m = event_metrics(pred, truth, tolerance_s=0.5)

    assert m["n_matched"] == 2
    assert m["n_false_positive"] == 1
    assert m["n_false_negative"] == 1
    assert m["precision"] == pytest.approx(2.0 / 3.0)
    assert m["recall"] == pytest.approx(2.0 / 3.0)
    assert m["f1"] == pytest.approx(2.0 / 3.0)
    assert m["mean_abs_timing_error"] == pytest.approx(0.3)
    assert m["median_abs_timing_error"] == pytest.approx(0.3)
    assert m["max_abs_timing_error"] == pytest.approx(0.4)


def test_event_metrics_with_empty_prediction():
    truth = [make_event("t1", EventType.COLLISION, 3.0)]
    m = event_metrics([], truth, tolerance_s=1.0)
    assert m["n_matched"] == 0
    assert m["precision"] == 0.0
    assert m["recall"] == 0.0
    assert m["f1"] == 0.0
    assert m["unmatched_truth"] == ["t1"]


# ---------------------------------------------------------------------------
# local vs fused
# ---------------------------------------------------------------------------


def _truth_for_fusion() -> GraphDocument:
    """Reference: two causes, each contributing to the same collision."""
    nodes = [
        make_event("gA", EventType.HARD_BRAKE, 1.0, participant_id="A"),
        make_event("gB", EventType.CUT_IN_LIKE_MOTION, 2.0, participant_id="B"),
        make_event("gC", EventType.COLLISION, 3.0, participant_id="A"),
    ]
    edges = [edge("gA", "gC", CAUSES), edge("gB", "gC", CAUSES)]
    return make_doc(nodes, edges, owner=None, scope=Provenance.ORACLE)


def test_compare_local_vs_fused_rewards_the_union():
    truth = _truth_for_fusion()

    # A saw its own hard brake and the collision but not B's cut-in.
    local_a = make_doc(
        [
            make_event("a1", EventType.HARD_BRAKE, 1.05, participant_id="A"),
            make_event("a2", EventType.COLLISION, 3.02, participant_id="A"),
        ],
        [edge("a1", "a2", CAUSES)],
        owner="A",
    )
    # B saw its own cut-in and the collision (which it attributes to A, the
    # canonical owner of the outcome node) but not A's brake.
    local_b = make_doc(
        [
            make_event("b1", EventType.CUT_IN_LIKE_MOTION, 1.95, participant_id="B"),
            make_event("b2", EventType.COLLISION, 3.04, participant_id="A"),
        ],
        [edge("b1", "b2", CAUSES)],
        owner="B",
    )
    fused = make_doc(
        [
            make_event("f1", EventType.HARD_BRAKE, 1.05, participant_id="A", provenance=Provenance.FUSED),
            make_event("f2", EventType.CUT_IN_LIKE_MOTION, 1.95, participant_id="B", provenance=Provenance.FUSED),
            make_event("f3", EventType.COLLISION, 3.03, participant_id="A", provenance=Provenance.FUSED),
        ],
        [edge("f1", "f3", CAUSES), edge("f2", "f3", CAUSES)],
        owner=None,
        scope=Provenance.FUSED,
    )

    result = compare_local_vs_fused(
        {"A": local_a, "B": local_b}, fused, truth, tolerance_s=0.5
    )

    assert result["fused"]["edge_f1"] == 1.0
    assert result["fused"]["structural_hamming_distance"] == 0
    assert result["per_participant"]["A"]["edge_recall"] == pytest.approx(0.5)
    assert result["per_participant"]["B"]["edge_recall"] == pytest.approx(0.5)
    assert result["delta_edge_f1"] > 0.0
    assert result["delta_node_f1"] > 0.0
    assert result["delta_shd"] < 0
    assert result["best_local_participant_id"] in ("A", "B")


def test_compare_local_vs_fused_requires_a_local_graph():
    with pytest.raises(ValueError):
        compare_local_vs_fused({}, diamond_doc(), diamond_doc(), tolerance_s=1.0)


# ---------------------------------------------------------------------------
# adversarial review addition
# ---------------------------------------------------------------------------


def test_cross_graph_metrics_do_not_depend_on_node_listing_order():
    """Two *different* graphs must score the same however their nodes are listed.

    ``test_self_comparison_is_invariant_to_node_ordering`` only exercises the
    self-comparison case, where the assignment's identity tie-breaker
    (``_TIE_IDENTITY``) resolves the ambiguity because both sides share event
    ids. Across two genuinely independent reconstructions the ids never coincide,
    every tie-breaker applies uniformly, and the optimal assignment is then
    *genuinely* non-unique whenever a prediction sits equidistant between two
    reference events -- exactly the situation a burst of same-type events
    produces. The solver then resolves the tie by row/column index, i.e. by the
    order the caller happened to list the nodes in, and a published
    structural_hamming_distance becomes an artifact of document serialisation
    order rather than a property of the two graphs.

    Here both predicted HARD_BRAKE events sit at t=2.0, one second from each of
    the two reference events at t=1.0 and t=3.0, so both pairings cost exactly
    2.0. One of them maps the predicted edge onto the reference edge (SHD 0), the
    other maps it onto the reversed edge (SHD 1). The metric must commit to one
    answer for every permutation of either document.
    """
    pred_nodes = [
        make_event("p1", EventType.HARD_BRAKE, 2.0),
        make_event("p2", EventType.HARD_BRAKE, 2.0),
    ]
    truth_nodes = [
        make_event("t1", EventType.HARD_BRAKE, 1.0),
        make_event("t2", EventType.HARD_BRAKE, 3.0),
    ]
    pred_edges = [edge("p1", "p2")]
    truth_edges = [edge("t1", "t2")]

    seen = set()
    for pred_order in ([0, 1], [1, 0]):
        for truth_order in ([0, 1], [1, 0]):
            m = graph_structure_metrics(
                make_doc([pred_nodes[i] for i in pred_order], pred_edges),
                make_doc([truth_nodes[i] for i in truth_order], truth_edges),
                tolerance_s=1.5,
            )
            # The tie itself is real: both pairings are optimal at total |dt| 2.0.
            assert m["n_nodes_matched"] == 2
            assert m["mean_abs_timing_error"] == pytest.approx(1.0)
            seen.add(
                (
                    m["structural_hamming_distance"],
                    m["n_reversed_edges"],
                    m["n_missing_edges"],
                    m["n_extra_edges"],
                    round(m["edge_f1"], 12),
                    tuple(sorted((a, b) for a, b, _dt in m["node_matches"])),
                )
            )

    assert len(seen) == 1, "metrics depend on node listing order: {0}".format(sorted(seen))


def test_match_events_echoes_the_tolerance_when_one_side_is_empty():
    """The degenerate branch must not silently report a tolerance of zero."""
    result = match_events([], [make_event("t1", EventType.COLLISION, 3.0)], tolerance_s=1.5)
    assert result["tolerance_s"] == pytest.approx(1.5)
    assert result["n_matched"] == 0
    assert result["unmatched_b"] == ["t1"]
