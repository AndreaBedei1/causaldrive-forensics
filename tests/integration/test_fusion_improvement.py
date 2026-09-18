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

What V2 changed, and what it costs
----------------------------------
V1 aligned the clocks by fitting radar tracks, which could place a vehicle on the
common timeline without it ever touching anything. V2 aligns on shared physical
contact, and in this fixture the leader C never collides: A strikes B, and C only
brakes. So C has no contact anchor, and contact-based alignment cannot place it.

The alignment reports ``PARTIALLY_ALIGNED`` and names C as unaligned. C is then
absent from the fused graph entirely -- not silently dropped, but absent, which
has two consequences these tests pin down:

1. C's own account of braking never reaches the merged timeline.
2. B's radar track of C is never resolved to C, because association needs both
   ends on one clock. It stays ``B::T001``.

The recovery claim survives in a weaker and more precise form: the *initiating
event* does reach the blind participant, as B's observation of a decelerating
target rather than as C's own record of braking. That is what fusion contributes
here, and asserting the stronger form would assert something V2 does not do.

The strong claim -- the fused collision's ancestry reaching C by name -- is
asserted below against the recorded S07 run, where C is in contact and can be
aligned. Reporting the strong claim only where it holds is the point.
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
    # Specifically the initiating event: the leader slowing down, which A never
    # saw and B did. It arrives as B's observation of its target rather than as
    # C's own record, because C never made contact and so is not on the common
    # timeline -- see the module docstring and the limitation test below.
    assert any(
        owner == "B" and t == EventType.TARGET_DECELERATION for owner, t in gained
    ), (
        "fusion recovered no observation of the leader decelerating, so the "
        "initiating event did not reach the blind participant at all: {0}".format(
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
    assert any({"A", "B"} <= set(n.owners or []) for n in multi), (
        "no fused node carries both A and B, so nothing was recognised as the "
        "same physical fact seen from two viewpoints"
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


def test_a_participant_that_never_made_contact_cannot_be_placed_on_the_timeline(
    partial_view_run,
) -> None:
    """The cost of contact-based alignment, stated rather than left implicit.

    V1 fitted radar tracks and could place C without it ever touching anything.
    V2 anchors on shared contact, so a vehicle that only braked has nothing to
    anchor on. This is not a defect to be worked around by quietly falling back
    to the harness marker for one participant while the others rest on contact:
    that would put offsets of two different provenances on one timeline and
    report them identically. It is a limitation, and what matters is that it is
    declared.

    So this test asserts the declaration, not an absence. An implementation that
    started placing C would fail here, and should -- it would need to say how.
    """
    layout, _analyses, _fusion, _run = partial_view_run
    from cdf.common.io import read_json

    alignment = read_json(layout.clock_alignment)
    assert alignment["status"] == "PARTIALLY_ALIGNED", (
        "a run where one recorder never made contact should not report a clean "
        "alignment status; got {0}".format(alignment["status"])
    )
    assert "C" in (alignment.get("unaligned_participants") or []), (
        "C never collided and so has no contact anchor, but the alignment does "
        "not name it as unaligned: {0}".format(alignment)
    )
    assert (alignment.get("offsets") or {}).get("C", {}).get("offset_s") is None, (
        "C is named unaligned and still carries an offset, which is the worst of "
        "both: a reader would apply it"
    )
    # And the method did not fall back to the harness marker for the others.
    assert alignment["method"] == "shared_physical_contact"


def test_the_unaligned_participants_track_is_not_resolved_to_it(
    partial_view_run,
) -> None:
    """The second consequence: association needs both ends on one clock.

    B's radar track of C stays a track id. A reader of the merged graph sees
    that *something* ahead of B decelerated, not that C did. Naming it would
    require relating B's clock to C's, which is exactly what could not be done.
    """
    layout, _analyses, _fusion, _run = partial_view_run
    fused = load_graph(layout.fused_causal_graph, expect_scope=Provenance.FUSED)

    appearing: Set[str] = set()
    for node in fused.nodes:
        appearing.add(node.participant_id)
        appearing |= set(node.owners or [])
        if node.subject:
            appearing.add(node.subject)
    assert "C" not in appearing, (
        "C is unaligned, so nothing in the fused graph can be attributed to it; "
        "found {0}".format(sorted(x for x in appearing if x))
    )
    assert any("::" in x for x in appearing), (
        "the leader's motion should still be present as an unresolved track, "
        "otherwise the initiating event was lost rather than merely unnamed"
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
