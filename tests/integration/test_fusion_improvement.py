"""Does fusion recover what a single ego view cannot? Measured, not assumed.

This is the hypothesis test at the centre of the project (H1, and H2 in its
partial-observability form), so it is written to be *capable of failing*. It uses
:func:`tests.fixtures.synthetic.synthetic_partial_view`, where three vehicles run
in one lane and the rearmost participant never observes the leader at all: the
event that initiates the whole chain is absent from its evidence, and present in
the middle vehicle's.

Fixture honesty
---------------
The fixture emulates the occlusion by not generating those radar returns, which
is a *test* device. The real S07 measurement uses genuine sensor occlusion in
CARLA -- the intermediate vehicle physically blocks the line of sight -- and is
reported in ``docs/EXPERIMENTAL_FINDINGS.md``. What this test pins down is the
pipeline behaviour: given a participant that genuinely did not see the initiating
event, does fusion put it back?
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Set

import networkx as nx
import pytest

from cdf.common.config import load_run_config
from cdf.common.evidence import load_run
from cdf.common.layout import RunLayout
from cdf.common.schemas import EventType, Provenance
from cdf.fusion.pipeline import fuse_run
from cdf.graph.analysis import GraphAnalyzer
from cdf.graph.export import load_graph, to_networkx
from cdf.local.pipeline import analyse_run

from fixtures.synthetic import synthetic_partial_view

#: The recorded S07 run, used for the claims that need a real occlusion
#: rather than the fixture's emulation of one.
_REAL_S07 = Path(__file__).resolve().parents[2] / "artifacts" / "S07_partial_view" / "seed_000_occluded"


@pytest.fixture(scope="module")
def partial_view_run(tmp_path_factory, default_config):
    root = tmp_path_factory.mktemp("partial_view")
    layout = synthetic_partial_view(root, seed=0, cfg=default_config)
    analyses = analyse_run(layout.root, default_config)
    fusion = fuse_run(layout.root, default_config)
    return layout, analyses, fusion, load_run(layout.root)


def _track_owners(run, pid: str) -> int:
    return len(run.get(pid).track_ids())


def test_the_blind_participant_really_is_blind_to_the_leader(partial_view_run) -> None:
    """Guard the premise. If A can see C, the rest of this file measures nothing."""
    _layout, _analyses, _fusion, run = partial_view_run
    import math

    a = run.get("A")
    c_by_t = {round(s.t, 2): s for s in run.get("C").telemetry}
    for track_id, samples in a.tracks_by_id().items():
        errs = []
        for s in samples:
            c = c_by_t.get(round(s.t, 2))
            if c is not None:
                errs.append(math.hypot(s.gx - c.x, s.gy - c.y))
        if errs:
            assert min(errs) > 8.0, (
                "A's track {0} sits within {1:.1f} m of C, so A is not blind to it".format(
                    track_id, min(errs)
                )
            )


def test_the_middle_participant_does_observe_the_leader(partial_view_run) -> None:
    """The evidence fusion is supposed to contribute has to exist somewhere."""
    _layout, _analyses, _fusion, run = partial_view_run
    assert _track_owners(run, "B") >= 1, "B observed nothing; there is nothing to fuse in"


def test_fusion_recovers_events_absent_from_the_blind_local_graph(partial_view_run) -> None:
    """THE measurement: fused node recall must exceed the blind participant's.

    Scored against the fused graph itself rather than an oracle, so it isolates
    one question: does the fused reconstruction contain claims that the blind
    participant's own reconstruction does not?
    """
    layout, analyses, _fusion, _run = partial_view_run
    blind = load_graph(layout.causal_graph("A"), expect_scope=Provenance.LOCAL)
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)

    blind_owner_types: Set[Any] = {(n.participant_id, n.event_type) for n in blind.nodes}
    fused_owner_types: Set[Any] = set()
    for n in fused.nodes:
        for owner in n.owners or [n.participant_id]:
            fused_owner_types.add((owner, n.event_type))

    gained = fused_owner_types - blind_owner_types
    assert gained, (
        "fusion added nothing the blind participant did not already have; "
        "H1 is not supported by this run"
    )
    # Specifically, something owned by the vehicle A never observed.
    assert any(owner == "C" for owner, _t in gained), (
        "fusion recovered nothing owned by C, the participant A was blind to: {0}".format(
            sorted((o, t.value) for o, t in gained)
        )
    )


def test_the_recovered_evidence_is_merged_from_both_viewpoints(partial_view_run) -> None:
    """Recovery must be a genuine merge, not a relabelling.

    The asymmetric case is the one that matters: one participant's *observation*
    of another decelerating and that other's own record of decelerating are the
    same physical fact seen twice, and fusion has to recognise them as one node
    carrying both owners.
    """
    layout, _analyses, _fusion, _run = partial_view_run
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)

    multi = [n for n in fused.nodes if len(set(n.owners or [])) > 1]
    assert multi, "fusion produced no node owned by more than one participant"
    assert any("C" in set(n.owners or []) for n in multi), (
        "no fused node carries C, the participant the striker never observed"
    )
    for node in multi:
        assert len(node.merged_from) >= 2, (
            "a multi-owner node claims two owners but records one source"
        )


@pytest.mark.skipif(
    not (RunLayout.from_run_dir(_REAL_S07).fused_causal_graph.exists()),
    reason="the recorded S07 run is not present",
)
def test_real_run_outcome_reaches_back_to_the_initiating_vehicle() -> None:
    """On the RECORDED S07 run, the fused collision's ancestry must reach C.

    This is the strong form of the claim and it is asserted against the CARLA
    recording rather than the synthetic fixture, because the two differ: the
    fixture emulates occlusion by withholding radar returns and its shortened
    chain does not reproduce the full causal path, whereas the recording -- where
    the occlusion is physical -- does. Reporting the strong claim only where it
    actually holds is the point.
    """
    layout = RunLayout.from_run_dir(_REAL_S07)
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)
    graph = to_networkx(fused)
    analyzer = GraphAnalyzer(fused)

    collisions = [
        n
        for n in analyzer.outcome_nodes()
        if graph.nodes[n]["event_type"] == EventType.COLLISION.value
    ]
    assert collisions, "the recorded S07 run carries no collision node"

    reached: Set[str] = set()
    for node in collisions:
        for ancestor in nx.ancestors(graph, node):
            reached |= set(graph.nodes[ancestor]["event"].owners or [])
    assert "C" in reached, (
        "the fused collision's ancestry reaches {0}, never C -- fusion connected no "
        "evidence from the vehicle that initiated the chain".format(sorted(reached))
    )


def test_fusion_bridges_paths_no_single_participant_had(partial_view_run) -> None:
    """The diagnostics must name the reachability fusion actually created."""
    layout, _analyses, _fusion, _run = partial_view_run
    from cdf.common.io import read_json

    diagnostics = read_json(layout.fusion_diagnostics)
    added = diagnostics.get("fusion_added") or {}
    assert added.get("n_bridged_paths", 0) > 0, (
        "fusion reported no bridged reachability pair, so it merged nodes without "
        "connecting anything"
    )


def test_knowledge_gain_is_reported_against_the_oracle(partial_view_run) -> None:
    """The oracle-referenced form of the same measurement must agree in sign."""
    layout, _analyses, _fusion, _run = partial_view_run
    if not layout.oracle_causal_graph.exists():
        pytest.skip("this fixture does not build an oracle causal graph")

    cfg = load_run_config()
    reference = load_graph(layout.oracle_causal_graph, expect_scope=Provenance.ORACLE)
    blind = load_graph(layout.causal_graph("A"), expect_scope=Provenance.LOCAL)
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)

    tolerance = float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5))
    gain = GraphAnalyzer(fused, cfg).knowledge_gain(
        blind, reference, tolerance_s=tolerance
    )
    assert gain["self_node_recall"] >= gain["baseline_node_recall"], (
        "fusion recovered LESS of the ground truth than the blind participant "
        "alone ({0:.3f} < {1:.3f})".format(
            gain["self_node_recall"], gain["baseline_node_recall"]
        )
    )
