"""Lane-marking crossings: one crossing per crossing.

The sensor reports on every tick a marking is being straddled, so a single lane
change arrives as a dozen reports. Section 46 asks for exactly two things --
that a crossing is recorded once, and that no false duplicates appear -- and
those are the same requirement seen from both sides.
"""

from __future__ import annotations

import pytest

from cdf.common.config import Config
from cdf.common.schemas import EventType
from cdf.local.lane_events import (
    MARKING_KINDS, build_lane_events, lane_events_from_records,
)


def report(t: float, *types: str, frame: int = 0) -> dict:
    return {"t": t, "frame": frame, "marking_types": list(types)}


def types_of(result) -> list:
    return [e.event_type.value for e in result["events"]]


# --- deduplication --------------------------------------------------------


def test_a_burst_of_reports_is_one_crossing():
    """A lane change straddles the line for most of a second."""
    records = [
        report(5.00 + i * 0.05, "LaneMarkingType.Broken") for i in range(14)
    ]
    crossings = lane_events_from_records(records)
    assert len(crossings) == 1
    assert crossings[0]["n_reports"] == 14
    assert crossings[0]["t_first"] == pytest.approx(5.00)


def test_two_lane_changes_a_second_apart_stay_two_crossings():
    records = (
        [report(5.00 + i * 0.05, "LaneMarkingType.Broken") for i in range(4)]
        + [report(7.00 + i * 0.05, "LaneMarkingType.Broken") for i in range(4)]
    )
    assert len(lane_events_from_records(records)) == 2


def test_the_merge_window_is_configurable():
    records = [
        report(5.0, "LaneMarkingType.Broken"),
        report(6.0, "LaneMarkingType.Broken"),
    ]
    tight = Config({"perception": {"lanes": {"merge_window_s": 0.2}}})
    wide = Config({"perception": {"lanes": {"merge_window_s": 2.0}}})
    assert len(lane_events_from_records(records, tight)) == 2
    assert len(lane_events_from_records(records, wide)) == 1


def test_one_crossing_produces_one_event_not_one_per_report():
    records = [
        report(5.00 + i * 0.05, "LaneMarkingType.Broken") for i in range(14)
    ]
    result = build_lane_events("A", records)
    assert types_of(result) == ["LANE_MARKING_CROSSED"]
    assert result["events"][0].detail["n_sensor_reports_merged"] == 14


def test_the_event_spans_the_straddle_rather_than_being_an_instant():
    records = [
        report(5.00 + i * 0.05, "LaneMarkingType.Broken") for i in range(10)
    ]
    event = build_lane_events("A", records)["events"][0]
    assert event.t_start == pytest.approx(5.00)
    assert event.t_end == pytest.approx(5.45)
    assert event.values["straddle_s"] == pytest.approx(0.45)


# --- what each marking type means ----------------------------------------


def test_a_solid_line_yields_both_the_specific_and_the_general_claim():
    """The normative layer needs the solid line; the physical layer needs the
    crossing. Both are true, and neither is a duplicate of the other."""
    result = build_lane_events("A", [report(5.0, "LaneMarkingType.Solid")])
    assert sorted(types_of(result)) == ["LANE_MARKING_CROSSED", "SOLID_LINE_CROSSED"]


def test_a_broken_line_yields_only_the_general_claim():
    result = build_lane_events("A", [report(5.0, "LaneMarkingType.Broken")])
    assert types_of(result) == ["LANE_MARKING_CROSSED"]


def test_a_curb_is_a_road_boundary_not_a_lane_marking():
    result = build_lane_events("A", [report(5.0, "LaneMarkingType.Curb")])
    assert types_of(result) == ["ROAD_BOUNDARY_CROSSED"]


def test_grass_is_also_a_road_boundary():
    result = build_lane_events("A", [report(5.0, "LaneMarkingType.Grass")])
    assert types_of(result) == ["ROAD_BOUNDARY_CROSSED"]


def test_mixed_solid_and_broken_counts_as_solid():
    """Crossing a solid-broken pair means a solid line was among what was crossed."""
    for marking in ("LaneMarkingType.SolidBroken", "LaneMarkingType.BrokenSolid",
                    "LaneMarkingType.SolidSolid"):
        result = build_lane_events("A", [report(5.0, marking)])
        assert "SOLID_LINE_CROSSED" in types_of(result), marking


def test_an_unclassified_marking_is_recorded_generically_and_less_confidently():
    """Better a weaker general claim than a guess at which sort of line it was."""
    result = build_lane_events("A", [report(5.0, "LaneMarkingType.Other")])
    assert types_of(result) == ["LANE_MARKING_CROSSED"]
    assert result["events"][0].confidence < 1.0
    assert result["events"][0].detail["marking_kind"] == "unclassified"


def test_a_report_with_no_marking_type_still_records_a_crossing():
    result = build_lane_events("A", [report(5.0)])
    assert types_of(result) == ["LANE_MARKING_CROSSED"]


def test_crossings_of_different_kinds_are_not_merged_together():
    """A vehicle crossing a broken line then a curb did two different things."""
    records = [
        report(5.00, "LaneMarkingType.Broken"),
        report(5.05, "LaneMarkingType.Curb"),
    ]
    result = build_lane_events("A", records)
    assert result["n_crossings"] == 2
    assert sorted(types_of(result)) == ["LANE_MARKING_CROSSED", "ROAD_BOUNDARY_CROSSED"]


def test_one_report_naming_two_markings_yields_both():
    records = [report(5.0, "LaneMarkingType.Solid", "LaneMarkingType.Curb")]
    result = build_lane_events("A", records)
    assert sorted(types_of(result)) == [
        "LANE_MARKING_CROSSED", "ROAD_BOUNDARY_CROSSED", "SOLID_LINE_CROSSED",
    ]


# --- reporting contracts -------------------------------------------------


def test_the_events_belong_to_the_participant_and_carry_no_subject():
    """The other party to a line crossing is the road, not a vehicle."""
    result = build_lane_events("B", [report(5.0, "LaneMarkingType.Solid")])
    for event in result["events"]:
        assert event.participant_id == "B"
        assert event.subject is None


def test_the_sensor_is_named_and_described_as_a_simulated_adas_signal():
    event = build_lane_events("A", [report(5.0, "LaneMarkingType.Solid")])["events"][0]
    assert event.source_sensors == ["lane"]
    assert "simulated ADAS" in event.detail["sensor"]


def test_the_result_says_how_many_raw_reports_became_how_many_events():
    records = [report(5.0 + i * 0.05, "LaneMarkingType.Solid") for i in range(10)]
    result = build_lane_events("A", records)
    assert result["n_raw_reports"] == 10
    assert result["n_crossings"] == 1
    assert result["n_events"] == 2


def test_events_come_out_in_time_order():
    records = [
        report(9.0, "LaneMarkingType.Curb"),
        report(3.0, "LaneMarkingType.Broken"),
    ]
    times = [e.t_peak for e in build_lane_events("A", records)["events"]]
    assert times == sorted(times)


def test_no_records_produce_no_events():
    result = build_lane_events("A", [])
    assert result["events"] == []
    assert result["n_crossings"] == 0


def test_every_mapped_marking_kind_has_an_event_type():
    from cdf.local.lane_events import _EVENT_FOR_KIND

    for kind in set(MARKING_KINDS.values()) | {"unclassified"}:
        assert kind in _EVENT_FOR_KIND, kind
