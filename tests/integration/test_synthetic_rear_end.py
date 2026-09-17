"""End-to-end rear-end reconstruction, driven with no simulator at all.

The run is synthesised by :mod:`tests.fixtures.synthetic` and then handed to the
*production* chain: :func:`cdf.local.pipeline.analyse_run`, then
:func:`cdf.fusion.pipeline.fuse_run`, then :class:`cdf.checking.trace_checker.TraceChecker`,
and finally an evaluation step that compares what the vehicles reconstructed
against the privileged trace. Nothing is stubbed and nothing is asserted about a
hard-coded number: every quantity below is read back off the artifacts the
pipeline wrote.

What the scene is
-----------------
A follows B in the same lane, five metres per second faster, and brakes too late
(``collide=True``) or just early enough (``collide=False``). The interesting
asymmetry is that B is the lead vehicle, so its forward radar sees nothing: any
account of the encounter that B alone could give is missing the entire
interaction. That is the same asymmetry the recorded S01 run exhibits.
"""

from __future__ import annotations

from typing import Dict, Tuple

import pytest

from cdf.common.evidence import RunEvidence, load_run
from cdf.common.layout import RunLayout
from cdf.common.schemas import CheckStatus, EventType, OutcomeClass, Provenance
from cdf.checking.trace_checker import TraceChecker
from cdf.fusion.pipeline import FusionResult, fuse_run
from cdf.fusion.track_association import STATUS_RESOLVED
from cdf.graph.analysis import GraphAnalyzer
from cdf.graph.export import load_graph
from cdf.local.pipeline import LocalAnalysis, analyse_run
from cdf.common.io import read_json

from fixtures.synthetic import oracle_check_input, synthetic_rear_end

#: Event types that express "the gap to the object ahead is running out". The
#: rear-end claim is that at least one of them explains the impact.
CLOSING_TYPES = (
    EventType.RANGE_DECREASING,
    EventType.RAPID_CLOSING,
    EventType.LOW_TTC,
    EventType.CRITICAL_TTC,
)


def _pipeline(layout: RunLayout, cfg) -> Tuple[Dict[str, LocalAnalysis], FusionResult, RunEvidence]:
    """Run the real local and fusion stages over a run directory."""
    analyses = analyse_run(layout.root, cfg)
    fusion = fuse_run(layout.root, cfg)
    return analyses, fusion, load_run(layout.root)


@pytest.fixture(scope="module")
def crash_run(tmp_path_factory, default_config):
    """A synthetic rear-end that ends in contact, fully analysed and fused."""
    root = tmp_path_factory.mktemp("rear_end_crash")
    layout = synthetic_rear_end(root, seed=0, collide=True, cfg=default_config)
    analyses, fusion, run = _pipeline(layout, default_config)
    return layout, analyses, fusion, run


@pytest.fixture(scope="module")
def avoided_run(tmp_path_factory, default_config):
    """The same encounter with A braking in time."""
    root = tmp_path_factory.mktemp("rear_end_avoided")
    layout = synthetic_rear_end(root, seed=0, collide=False, cfg=default_config)
    analyses, fusion, run = _pipeline(layout, default_config)
    return layout, analyses, fusion, run


# ---------------------------------------------------------------------------
# The central claim: A's own graph explains the impact by the closing gap
# ---------------------------------------------------------------------------


def test_local_causal_graph_links_closing_evidence_to_the_collision(crash_run) -> None:
    """A's local DAG must contain a directed path from closing/TTC to COLLISION.

    This is the whole point of the local layer: the striking vehicle, alone and
    with no privileged information, reconstructs *why* it hit something.
    """
    _layout, analyses, _fusion, _run = crash_run
    graph = analyses["A"].causal_graph
    analyzer = GraphAnalyzer(graph)

    collisions = [n for n in graph.nodes if n.event_type is EventType.COLLISION]
    assert collisions, "A recorded an impact but its causal graph has no COLLISION node"
    collision_id = collisions[0].event_id

    sources = [n for n in graph.nodes if n.event_type in CLOSING_TYPES]
    assert sources, "A's graph contains no closing/TTC evidence at all"

    paths = [
        (n.event_type.value, analyzer.shortest_causal_path(n.event_id, collision_id))
        for n in sources
    ]
    reached = [(t, p) for t, p in paths if p is not None]
    assert reached, (
        "no closing or TTC event reaches the COLLISION node in A's causal graph; "
        "closing events present: {0}".format(sorted(t for t, _ in paths))
    )

    # The explanation must be a real chain of typed causal edges, not a node that
    # happens to share a timestamp with the impact.
    for _type_value, path in reached:
        assert len(path) >= 2
    types_on_paths = {
        graph.node_by_id(node_id).event_type
        for _t, path in reached
        for node_id in path
    }
    assert EventType.CRITICAL_TTC in types_on_paths, (
        "the impact is not explained by a critical time-to-collision; path types: "
        "{0}".format(sorted(t.value for t in types_on_paths))
    )


def test_collision_is_attributed_to_a_track_never_to_a_participant(crash_run) -> None:
    """Locally, the struck object is an anonymous track -- never a named vehicle."""
    _layout, analyses, _fusion, run = crash_run
    graph = analyses["A"].causal_graph
    local_track_ids = set(run.get("A").track_ids())
    assert local_track_ids, "A held no radar track"

    for node in graph.nodes:
        if node.subject in (None, "", "self"):
            continue
        assert node.subject in local_track_ids, (
            "local event {0} names subject {1!r}, which is not one of A's own "
            "track ids".format(node.event_id, node.subject)
        )
        assert node.subject not in run.participant_ids, (
            "a local event names participant {0!r} directly".format(node.subject)
        )
        assert node.participant_id == "A"


def test_the_lead_vehicle_sees_nothing_of_the_encounter(crash_run) -> None:
    """B's forward radar holds no track, so B's own account omits the interaction.

    This asymmetry is what makes fusion worth doing; asserting it here stops the
    fixture from silently drifting into a scene where both vehicles see each
    other.
    """
    _layout, analyses, _fusion, run = crash_run
    assert run.get("B").tracks == []
    assert run.get("B").track_ids() == []

    interaction_nodes = [n for n in analyses["B"].causal_graph.nodes if n.subject]
    assert not interaction_nodes, (
        "B produced interaction events without any radar track: {0}".format(
            [n.event_type.value for n in interaction_nodes]
        )
    )
    # B still records its own behaviour, so the graph is not simply empty.
    assert analyses["B"].causal_graph.nodes


# ---------------------------------------------------------------------------
# Fusion: identity from trajectory evidence alone
# ---------------------------------------------------------------------------


def test_fusion_resolves_the_anonymous_track_to_the_lead_vehicle(crash_run) -> None:
    """A's track must be identified as B from shared trajectories, not from ids."""
    _layout, _analyses, fusion, _run = crash_run
    assert len(fusion.assignments) == 1, (
        "expected exactly one track to associate, got {0}".format(
            sorted(fusion.assignments)
        )
    )
    assignment = list(fusion.assignments.values())[0]
    assert assignment.observer_id == "A"
    assert assignment.status == STATUS_RESOLVED, assignment.reason
    assert assignment.assigned_participant == "B"
    assert assignment.rmse_m is not None and assignment.rmse_m >= 0.0
    assert fusion.subject_map[assignment.track_id] == "B"


def test_fused_graph_states_the_interaction_in_participant_terms(crash_run) -> None:
    """After fusion the collision is a claim about A and B, with both accounts kept."""
    layout, analyses, fusion, _run = crash_run
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    assert fused.nodes and fused.edges

    collisions = [n for n in fused.nodes if n.event_type is EventType.COLLISION]
    assert collisions, "the fused graph lost the collision"
    # A's account names B as the subject; B's own account of the same impact has
    # no subject at all, because B never observed anything.
    subjects = {n.participant_id: n.subject for n in collisions}
    assert subjects.get("A") == "B"

    # Fusion may not invent nodes: every fused node comes from a local one.
    local_ids = {
        n.event_id for analysis in analyses.values() for n in analysis.causal_graph.nodes
    }
    for node in fused.nodes:
        assert node.merged_from, "fused node {0} cites no local event".format(node.event_id)
        for ref in node.merged_from:
            assert ref in local_ids


# ---------------------------------------------------------------------------
# Finite-trace checking
# ---------------------------------------------------------------------------


def test_model_checking_reports_a_verdict_per_participant_and_property(
    crash_run, default_config
) -> None:
    """The checker must produce a full, scoped report over the recorded evidence."""
    _layout, _analyses, _fusion, run = crash_run
    report = TraceChecker(default_config).check_run(run)

    assert report["scope"] == Provenance.LOCAL.value
    assert report["config_hash"] == default_config.hash
    assert sorted(report["by_participant"]) == ["A", "B"]
    total = sum(report["summary"].values())
    assert total == len(report["properties"]) * 2

    statuses = {s.value for s in CheckStatus}
    for block in report["by_participant"].values():
        assert set(block["statuses"].values()) <= statuses


def test_braking_response_and_post_impact_stop_are_decided_for_the_striker(
    crash_run, default_config
) -> None:
    """A braked at the critical TTC and came to rest: both are decidable PASSes.

    B's post-collision verdict is a FAIL, and correctly so: the struck vehicle was
    still on the throttle at the instant of impact (it had no warning), and P3's
    window starts at the collision sample itself.
    """
    _layout, _analyses, _fusion, run = crash_run
    checker = TraceChecker(default_config)
    a_results = {r.property_id: r for r in checker.check_participant(run.get("A"))}
    b_results = {r.property_id: r for r in checker.check_participant(run.get("B"))}

    assert a_results["P1_brake_response"].status is CheckStatus.PASS
    assert a_results["P3_post_collision_stop"].status is CheckStatus.PASS
    assert a_results["P3_post_collision_stop"].witness["t_stop_s"] > 0.0

    # B never observed anything, so its radar-dependent properties are UNKNOWN --
    # not PASS. "No evidence" must never be reported as "no violation".
    assert b_results["P1_brake_response"].status is CheckStatus.UNKNOWN
    assert b_results["P2_no_throttle_while_closing"].status is CheckStatus.UNKNOWN
    assert b_results["P3_post_collision_stop"].status is CheckStatus.FAIL
    assert "throttle" in b_results["P3_post_collision_stop"].reason


def test_oracle_properties_stay_unknown_without_signal_or_junction_truth(
    crash_run, default_config
) -> None:
    """The privileged checker is privileged, not omniscient.

    The synthetic scene has no junction and no signal, so the oracle properties
    must report ``UNKNOWN`` rather than manufacture a verdict -- and they must
    carry the ORACLE scope, keeping them out of the local report entirely.
    """
    layout, _analyses, _fusion, run = crash_run
    results = TraceChecker(default_config).check_oracle(oracle_check_input(layout))

    assert results, "no oracle properties were evaluated"
    for result in results:
        assert result.scope is Provenance.ORACLE
        assert result.status is CheckStatus.UNKNOWN, result.reason

    local_report = TraceChecker(default_config).check_run(run)
    local_ids = {r["property_id"] for r in local_report["results"]}
    assert local_ids.isdisjoint({r.property_id for r in results}), (
        "an oracle property leaked into the local checking report"
    )


# ---------------------------------------------------------------------------
# Evaluation: the reconstruction against the privileged truth
# ---------------------------------------------------------------------------


def test_reconstruction_matches_the_privileged_ground_truth(
    crash_run, default_config
) -> None:
    """Score the reconstruction against the oracle: outcome, timing and identity.

    This is the only place in the file that opens the ``oracle/`` subtree, and it
    reads it purely to score what the unprivileged layers already produced.
    """
    layout, analyses, fusion, _run = crash_run
    summary = read_json(layout.oracle_dir / "oracle_summary.json")
    pairs = summary["collision_pairs"]
    assert len(pairs) == 1, "the fixture is supposed to produce exactly one impact"
    truth_pair = {pairs[0]["a"], pairs[0]["b"]}
    truth_t = float(pairs[0]["t"])

    # 1. Outcome classification from local evidence alone.
    manifest = read_json(layout.manifest)
    assert manifest["outcome"] == OutcomeClass.COLLISION.value
    local_collisions = [
        n for n in analyses["A"].causal_graph.nodes if n.event_type is EventType.COLLISION
    ]
    assert local_collisions, "A did not reconstruct the collision it was part of"

    # 2. Timing, against the configured evaluation tolerance.
    tolerance = float(default_config.get("evaluation.event_match.time_tolerance_s", 1.5))
    error_s = abs(local_collisions[0].t_peak - truth_t)
    assert error_s <= tolerance, (
        "local collision time {0:.3f}s differs from the truth {1:.3f}s by "
        "{2:.3f}s".format(local_collisions[0].t_peak, truth_t, error_s)
    )

    # 3. Identity: fusion recovered the true pair from trajectory evidence only.
    resolved_pair = {"A", fusion.subject_map["A::T001"]}
    assert resolved_pair == truth_pair, (
        "fusion resolved the encounter as {0} but the truth is {1}".format(
            resolved_pair, truth_pair
        )
    )
    # The oracle -- and only the oracle -- names the other party directly.
    assert any(c["other_participant_id"] for c in summary["collisions"])


# ---------------------------------------------------------------------------
# The counterfactual variant: braking in time
# ---------------------------------------------------------------------------


def test_avoided_variant_produces_a_near_miss_and_no_collision(avoided_run) -> None:
    """Braking early enough turns the same encounter into a near miss.

    The two variants share every threshold and differ only in when A brakes, so
    the difference in the reconstruction is attributable to the behaviour rather
    than to the tuning.
    """
    layout, analyses, _fusion, run = avoided_run
    manifest = read_json(layout.manifest)
    assert manifest["outcome"] == OutcomeClass.NO_EVENT.value

    types = {n.event_type for n in analyses["A"].causal_graph.nodes}
    assert EventType.COLLISION not in types
    assert EventType.CRITICAL_TTC in types, (
        "the avoided variant must still be a genuine conflict, otherwise it "
        "measures nothing"
    )
    assert EventType.NEAR_MISS in types, (
        "a critical TTC that resolved without contact must be reported as a near "
        "miss"
    )
    assert run.get("A").collision_trigger() is None

    truth = read_json(layout.oracle_dir / "oracle_summary.json")
    assert truth["collision_pairs"] == [], (
        "the fixture reported a contact in the variant that is supposed to avoid it"
    )
