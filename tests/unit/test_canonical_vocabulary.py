

def test_two_edges_that_restate_to_one_family_are_collapsed():
    """Several strict types map to positive_contribution.

    So a pair of nodes joined by both TRIGGERS and CONTRIBUTES_TO restates as the
    same edge twice, and the matcher rejects a document whose
    (source, target, edge_type) is not unique -- which took a three-vehicle run's
    evaluation down with a ValueError instead of a metric. The better-supported
    edge survives and the collapse is counted.
    """
    from cdf.common.schemas import CausalEdgeType, GraphDocument, GraphEdge, Provenance
    from cdf.graph.canonical import canonicalise

    doc = GraphDocument(
        graph_kind="causal", scope=Provenance.FUSED, owner=None,
        run_id="r", scenario_id="S", seed=0,
        nodes=[],
        edges=[
            GraphEdge(source="a", target="b",
                       edge_type=CausalEdgeType.TRIGGERS.value, confidence=0.4),
            GraphEdge(source="a", target="b",
                       edge_type=CausalEdgeType.CONTRIBUTES_TO.value, confidence=0.9),
        ],
    )
    out = canonicalise(doc)
    assert len(out.edges) == 1
    assert out.edges[0].confidence == 0.9, "the better-supported edge survives"
    assert out.meta["canonical_vocabulary"]["n_edges_collapsed"] == 1
