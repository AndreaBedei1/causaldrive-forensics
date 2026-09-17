"""End-to-end crossing reconstruction, driven with no simulator and no map.

Two vehicles travel perpendicular straight paths that meet. Neither is told a
junction exists: the conflict has to be inferred by propagating both observed
motions and intersecting the predictions, which is what
:func:`cdf.local.indicators.infer_conflict` does from own pose and own radar
alone.

The assertions therefore test two things that are easy to conflate: that a
conflict *was* inferred, and that it was inferred from geometry rather than from
anything map-shaped leaking into the local artifacts.
"""

from __future__ import annotations

import math

import pytest

from cdf.common.evidence import load_run
from cdf.common.schemas import EventType, Provenance
from cdf.fusion.pipeline import fuse_run
from cdf.fusion.track_association import STATUS_RESOLVED
from cdf.graph.export import load_graph
from cdf.local.indicators import compute_track_indicators
from cdf.local.pipeline import analyse_run

from fixtures.synthetic import synthetic_crossing

CONFLICT_TYPES = (
    EventType.PREDICTED_PATH_CONFLICT,
    EventType.CONFLICT_REGION_ENTRY,
    EventType.LATERAL_CROSSING,
)


@pytest.fixture(scope="module")
def crossing_run(tmp_path_factory, default_config):
    root = tmp_path_factory.mktemp("crossing")
    layout = synthetic_crossing(root, seed=0, cfg=default_config)
    analyses = analyse_run(layout.root, default_config)
    fusion = fuse_run(layout.root, default_config)
    return layout, analyses, fusion, load_run(layout.root)


def test_the_paths_really_do_cross(crossing_run) -> None:
    """Guard the fixture itself: perpendicular headings, converging positions."""
    _layout, _analyses, _fusion, run = crossing_run
    a, b = run.get("A"), run.get("B")
    heading_a = a.telemetry[0].yaw
    heading_b = b.telemetry[0].yaw
    delta = abs(((heading_a - heading_b + 180.0) % 360.0) - 180.0)
    assert 60.0 < delta < 120.0, "the fixture is not a crossing (heading delta {0:.1f})".format(delta)

    def gap(i: int) -> float:
        return math.hypot(a.telemetry[i].x - b.telemetry[i].x, a.telemetry[i].y - b.telemetry[i].y)

    n = min(len(a.telemetry), len(b.telemetry))
    assert min(gap(i) for i in range(n)) < gap(0), "the vehicles never converged"


def test_conflict_is_inferred_from_trajectory_geometry_alone(crossing_run) -> None:
    """A non-zero conflict score must appear, computed from predicted paths."""
    layout, _analyses, _fusion, run = crossing_run
    from cdf.common.config import load_run_config

    cfg = load_run_config()
    scored = []
    for pid in run.participant_ids:
        per_track = compute_track_indicators(run.get(pid), cfg)
        for _tid, rows in per_track.items():
            scored.extend(r.conflict_score for r in rows)
    assert scored, "no track indicators were produced at all"
    assert max(scored) > 0.0, (
        "no conflict was inferred from two genuinely crossing predicted paths"
    )


def test_a_conflict_event_is_recorded_by_at_least_one_participant(crossing_run) -> None:
    _layout, analyses, _fusion, _run = crossing_run
    found = {
        pid: [e.event_type.value for e in a.events if e.event_type in CONFLICT_TYPES]
        for pid, a in analyses.items()
    }
    assert any(found.values()), "no participant recorded a conflict event: {0}".format(found)


def test_conflict_events_are_attributed_to_an_anonymous_track(crossing_run) -> None:
    """A crossing claim concerns an observed object, never a named participant."""
    _layout, analyses, _fusion, _run = crossing_run
    for pid, analysis in analyses.items():
        for event in analysis.events:
            if event.event_type not in CONFLICT_TYPES:
                continue
            assert event.subject and event.subject.startswith(pid + "::"), (
                "{0} attributed a conflict to {1!r}".format(pid, event.subject)
            )


def test_fusion_resolves_identity_across_the_crossing(crossing_run) -> None:
    """Two observers approaching from different bearings still resolve each other."""
    _layout, _analyses, fusion, _run = crossing_run
    resolved = {t: a for t, a in fusion.assignments.items() if a.status == STATUS_RESOLVED}
    assert resolved, "no track resolved; identity across a crossing was not established"
    for track_id, assignment in resolved.items():
        assert assignment.assigned_participant != assignment.observer_id
        assert track_id.startswith(assignment.observer_id + "::")


def test_local_artifacts_contain_no_junction_knowledge(crossing_run) -> None:
    """The inference is map-free, and the artifacts must show it."""
    layout, _analyses, _fusion, run = crossing_run
    for pid in run.participant_ids:
        doc = load_graph(layout.causal_graph(pid), expect_scope=Provenance.LOCAL)
        blob = repr(doc.to_dict()).lower()
        for forbidden in ("junction", "lane_id", "road_id", "waypoint", "traffic_light"):
            assert forbidden not in blob, (
                "{0}'s causal graph mentions {1!r}".format(pid, forbidden)
            )
