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

Which clock the recovery rests on
---------------------------------
This scene is also the one that decided the final clock architecture, so the
tests below cover both sides of it.

V1 aligned the clocks by fitting radar tracks. V2 made shared physical contact
the anchor, which is right -- an impact fixes an instant with no geometric model
in between -- but here the leader C never collides: A strikes B, and C only
brakes. Contact alone therefore cannot place C, the alignment reports
``PARTIALLY_ALIGNED``, and C's whole account is lost: absent from the merged log,
absent from the fused graph, and its radar track never resolved to it, because
association needs both ends on one clock.

The final method keeps an offset-only radar fit *behind* contact for exactly this
case (:mod:`cdf.fusion.hybrid_alignment`). C is placed by radar, A and B stay on
their contact anchors, and every participant records which source placed it. With
that, the strong recovery claim holds on this fixture: fusion contributes C's own
record of braking to a participant that never saw C, and recognises B's
observation of C decelerating and C's own deceleration as one node with two
owners.

So the contact-only loss is asserted as an **ablation**, with the fallback
switched off, and the recovery is asserted on the method the results are actually
computed with. Neither is left as a remembered fact.

The fused collision's *ancestry* reaching C by name is a further claim again, and
it does not hold on this fixture -- the shortened chain does not reproduce the
full causal path. It is asserted below against the recorded S07 run instead.
Reporting each claim only where it holds is the point.
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
    # Specifically the initiating event: the leader braking, which A never saw.
    # It arrives as C's own record rather than as B's observation of a target,
    # because with C on the common timeline the two are recognised as one fact --
    # see the merge test below, which asserts that node carries both owners.
    assert any(owner == "C" for owner, _t in gained), (
        "fusion recovered nothing owned by C, the participant A was blind to. "
        "With the radar fallback behind contact C is on the common timeline, so "
        "its own account should arrive: {0}".format(
            sorted((o, t.value) for o, t in gained)
        )
    )
    braking = {EventType.BRAKE_ONSET, EventType.HARD_BRAKE, EventType.DECELERATION}
    assert any(owner == "C" and t in braking for owner, t in gained), (
        "the leader's braking is what initiates this chain, and it is the one "
        "thing A could not see. Recovering C's presence without it would not be "
        "recovering the initiating event: {0}".format(
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
    assert any("C" in set(n.owners or []) for n in multi), (
        "no fused node carries C. B's observation of C decelerating and C's own "
        "record of decelerating are the same physical fact seen twice, and that "
        "is the asymmetric merge this test exists for"
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


@pytest.fixture(scope="module")
def contact_only_run(tmp_path_factory, default_config):
    """The same scene with the radar fallback switched off: the ablation."""
    from cdf.common.config import Config, deep_merge

    root = tmp_path_factory.mktemp("partial_view_contact_only")
    layout = synthetic_partial_view(root, seed=0, cfg=default_config)
    cfg = Config(deep_merge(
        default_config.data,
        {"fusion": {"hybrid_alignment": {"radar_fallback": False}}},
    ))
    analyse_run(layout.root, cfg)
    fuse_run(layout.root, cfg)
    return layout


def test_contact_alone_cannot_place_a_participant_that_never_collided(
    contact_only_run,
) -> None:
    """The measured reason the final method keeps a fallback.

    A vehicle that only braked has no contact anchor, so contact alignment leaves
    it on its own clock. That is honest and it is expensive: a whole account goes
    missing. The loss is asserted here, with the fallback disabled, so it stays a
    measured quantity rather than a remembered one -- and so that the pair of
    tests below genuinely measures what the fallback buys.
    """
    from cdf.common.io import read_json

    alignment = read_json(contact_only_run.clock_alignment)
    assert "C" in (alignment.get("unaligned_participants") or []), (
        "C never collided and so has no contact anchor, but the alignment does "
        "not name it as unaligned: {0}".format(alignment.get("clock_sources"))
    )
    assert (alignment.get("offsets") or {}).get("C", {}).get("offset_s") is None, (
        "C is named unaligned and still carries an offset, which is the worst of "
        "both: a reader would apply it"
    )
    # No silent substitution: with the fallback off, nothing else placed C.
    assert alignment.get("clock_sources", {}).get("C") == "UNRESOLVED"


def test_contact_alone_leaves_the_leaders_track_unresolved(contact_only_run) -> None:
    """The second cost: association needs both ends on one clock.

    Without a common time for C, B's radar track of it stays a track id. A reader
    of the merged graph sees that *something* ahead of B decelerated, not that C
    did.
    """
    fused = load_graph(
        contact_only_run.fused_causal_graph, expect_scope=Provenance.FUSED
    )
    appearing: Set[str] = set()
    for node in fused.nodes:
        appearing.add(node.participant_id)
        appearing |= set(node.owners or [])
        if node.subject:
            appearing.add(node.subject)
    assert "C" not in appearing, (
        "with contact only, C is unaligned and nothing in the fused graph can be "
        "attributed to it; found {0}".format(sorted(x for x in appearing if x))
    )
    assert any("::" in x for x in appearing), (
        "the leader's motion should still be present as an unresolved track, "
        "otherwise the initiating event was lost rather than merely unnamed"
    )


def test_the_hybrid_places_the_non_colliding_participant_by_radar(
    partial_view_run,
) -> None:
    """And what the fallback buys, on the method the results are computed with.

    Read against the two ablation tests above, this is the measurement: contact
    alone loses C entirely; contact-then-radar places it, names the source, and
    keeps A and B on their physical anchors.
    """
    layout, _analyses, _fusion, _run = partial_view_run
    from cdf.common.io import read_json

    alignment = read_json(layout.clock_alignment)
    assert alignment["status"] == "HYBRID_ALIGNED"
    assert alignment["clock_sources"]["C"] == "RADAR"
    assert alignment["clock_sources"]["A"] in ("CONTACT", "REFERENCE")
    assert alignment["clock_sources"]["B"] in ("CONTACT", "REFERENCE")
    assert alignment["unaligned_participants"] == []
    # Offset only. A fallback that fitted a rate would claim more than a
    # twenty-second trajectory window supports.
    assert alignment["offsets"]["C"]["scale"] == 1.0
    assert alignment["offsets"]["C"]["drift_ppm"] is None
    assert alignment["drift"]["estimated"] is False
    # And the decision is on the record, not just its outcome.
    decision = alignment["decisions"]["C"]
    assert decision["source"] == "RADAR"
    assert decision["contact_offset_s"] is None
    assert decision["radar_evidence"]["confidence"] > 0.4


def test_the_hybrid_resolves_the_leaders_track_to_the_leader(
    partial_view_run,
) -> None:
    """With C on the common timeline, B's anonymous track can be named."""
    layout, _analyses, _fusion, _run = partial_view_run
    from cdf.common.io import read_json

    report = read_json(layout.association_report)
    resolved = {
        a["track_id"]: a["assigned_participant"]
        for a in report.get("assignments", [])
        if a.get("status") == "RESOLVED"
    }
    assert resolved.get("B::T001") == "C", (
        "B's track of the leader should resolve to C now that both ends are on "
        "one clock; resolved map was {0}".format(resolved)
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
