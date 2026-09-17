"""End-to-end cut-in reconstruction, driven with no simulator at all.

The scene is synthesised by :mod:`tests.fixtures.synthetic` and handed to the
production chain (:func:`cdf.local.pipeline.analyse_run`, then
:func:`cdf.fusion.pipeline.fuse_run`). Nothing is stubbed.

What the scene is
-----------------
B starts in the lane beside A, ahead of it, and moves laterally into A's path
while travelling slower. The point of the scenario is what A is *not* told: there
are no lane ids and no map. All A can observe is that a tracked object's lateral
offset collapses towards its own longitudinal axis while it stays ahead and the
range shrinks. Inferring a cut-in from that alone is the whole claim, so the
assertions below are about the lateral geometry of the track rather than about a
label.
"""

from __future__ import annotations


import pytest

from cdf.common.evidence import load_run
from cdf.common.schemas import EventType, Provenance
from cdf.fusion.pipeline import fuse_run
from cdf.fusion.track_association import STATUS_RESOLVED
from cdf.graph.export import load_graph
from cdf.local.pipeline import analyse_run

from fixtures.synthetic import synthetic_cut_in

#: Either of these is an acceptable expression of "the object moved into my
#: path": the extractor may name the lateral motion itself, or the crossing of
#: the observer's axis that the motion produces.
LATERAL_TYPES = (EventType.CUT_IN_LIKE_MOTION, EventType.LATERAL_CROSSING)


@pytest.fixture(scope="module")
def cut_in_run(tmp_path_factory, default_config):
    root = tmp_path_factory.mktemp("cut_in")
    layout = synthetic_cut_in(root, seed=0, cfg=default_config)
    analyses = analyse_run(layout.root, default_config)
    fusion = fuse_run(layout.root, default_config)
    return layout, analyses, fusion, load_run(layout.root)


def test_the_follower_tracks_the_cutting_in_vehicle(cut_in_run) -> None:
    """A must hold a track of B through the manoeuvre, or nothing else follows."""
    _layout, _analyses, _fusion, run = cut_in_run
    a = run.get("A")
    assert a.track_ids(), "A observed nothing at all; the fixture is not exercising radar"

    # The track that matters is the long-lived one.
    tracks = a.tracks_by_id()
    main_id = max(tracks, key=lambda t: len(tracks[t]))
    samples = tracks[main_id]
    assert len(samples) >= 20, "the principal track is too short to describe a manoeuvre"


def test_lateral_offset_collapses_while_the_target_stays_ahead(cut_in_run) -> None:
    """The measured geometry must actually be a cut-in, not merely be labelled one."""
    _layout, _analyses, _fusion, run = cut_in_run
    tracks = run.get("A").tracks_by_id()
    main_id = max(tracks, key=lambda t: len(tracks[t]))
    samples = sorted(tracks[main_id], key=lambda s: s.t)

    first, last = samples[0], samples[-1]
    # Started off to one side, ended near the observer's own axis.
    assert abs(first.rel_y) > abs(last.rel_y), (
        "lateral offset did not decrease: {0:.2f} -> {1:.2f}".format(first.rel_y, last.rel_y)
    )
    assert abs(last.rel_y) < 2.0, "the target never reached the observer's lane"
    # And stayed ahead throughout: a target that fell behind would be an overtake.
    assert min(s.rel_x for s in samples) > 0.0


def test_local_events_name_the_lateral_motion(cut_in_run) -> None:
    """A's own reconstruction must record the manoeuvre, attributed to a track."""
    _layout, analyses, _fusion, _run = cut_in_run
    events = analyses["A"].events
    lateral = [e for e in events if e.event_type in LATERAL_TYPES]
    assert lateral, "A recorded no lateral-motion event for the cut-in"
    for event in lateral:
        # Attributed to an anonymous local track, never to a participant.
        assert event.subject and event.subject.startswith("A::"), (
            "a local event names {0!r} rather than one of A's own track ids".format(event.subject)
        )
        assert event.provenance is Provenance.LOCAL


def test_closing_follows_the_cut_in(cut_in_run) -> None:
    """The manoeuvre must precede the closing it causes, not follow it."""
    _layout, analyses, _fusion, _run = cut_in_run
    events = analyses["A"].events
    lateral = [e for e in events if e.event_type in LATERAL_TYPES]
    closing = [
        e
        for e in events
        if e.event_type in (EventType.RANGE_DECREASING, EventType.RAPID_CLOSING,
                            EventType.LOW_TTC, EventType.CRITICAL_TTC)
    ]
    if not closing:
        pytest.skip("this synthesis produced no closing episode to order against")
    assert min(e.t_peak for e in lateral) <= max(e.t_peak for e in closing)


def test_fusion_resolves_the_cutting_in_track_to_the_other_participant(cut_in_run) -> None:
    """Identity comes from trajectory evidence; no actor id exists to consult."""
    _layout, _analyses, fusion, _run = cut_in_run
    resolved = {
        t: a for t, a in fusion.assignments.items() if a.status == STATUS_RESOLVED
    }
    assert resolved, "no track was resolved to a participant"
    for track_id, assignment in resolved.items():
        assert assignment.assigned_participant != assignment.observer_id
        assert track_id.startswith(assignment.observer_id + "::")
        assert assignment.rmse_m is not None and assignment.rmse_m < 6.0


def test_no_map_or_lane_identity_reaches_the_local_artifacts(cut_in_run) -> None:
    """A cut-in inferred from geometry must not acquire a lane id on the way out."""
    layout, _analyses, _fusion, _run = cut_in_run
    doc = load_graph(layout.causal_graph("A"), expect_scope=Provenance.LOCAL)
    blob = repr(doc.to_dict()).lower()
    for forbidden in ("lane_id", "road_id", "junction", "waypoint", "traffic_light"):
        assert forbidden not in blob, "local causal graph mentions {0!r}".format(forbidden)
