"""The log has to be readable, ordered and honest about its time axis.

Three properties matter enough to pin down. A log must be *deterministic*, or it
cannot be diffed between runs. A local log must carry no common time, or it is
claiming knowledge one vehicle cannot have. And a global log must say out loud
when a recorder could not be aligned, because the alternative -- quietly showing
unaligned rows next to aligned ones -- puts two different clocks in one column.
"""

from __future__ import annotations

import random

import pytest

from cdf.common.event_log import (
    LOG_COLUMNS,
    build_global_log,
    build_local_log,
    format_log,
    log_rows,
)
from cdf.common.schemas import Event, EventType, Evidence, Provenance


def make_event(
    event_id: str,
    event_type: EventType,
    participant: str,
    t: float,
    subject: str = None,
    **kwargs,
) -> Event:
    return Event(
        event_id=event_id,
        event_type=event_type,
        participant_id=participant,
        t_start=t - 0.1,
        t_peak=t,
        t_end=t + 0.1,
        subject=subject,
        **kwargs,
    )


@pytest.fixture
def two_vehicle_events():
    return [
        make_event("b1", EventType.STOP_SIGN_DETECTED, "B", 5.20,
                   confidence=0.94, source_sensors=["camera"]),
        make_event("b2", EventType.BRAKE_ONSET, "B", 5.74,
                   source_sensors=["controls"]),
        make_event("b3", EventType.FULL_STOP, "B", 6.00,
                   source_sensors=["telemetry"]),
        make_event("a1", EventType.CONFLICT_REGION_ENTRY, "A", 7.11, subject="B",
                   source_sensors=["radar"]),
        make_event("a2", EventType.COLLISION, "A", 8.77, subject="B",
                   values={"impulse": 4200.0}, source_sensors=["contact"]),
    ]


# --- determinism -----------------------------------------------------------


def test_row_order_does_not_depend_on_input_order(two_vehicle_events):
    """Shuffling the input must not change the log."""
    reference = [r["event_id"] for r in log_rows(two_vehicle_events)]
    rng = random.Random(20260918)
    for _ in range(12):
        shuffled = list(two_vehicle_events)
        rng.shuffle(shuffled)
        assert [r["event_id"] for r in log_rows(shuffled)] == reference


def test_events_at_the_same_instant_still_have_one_fixed_order():
    """A tie must be broken by data, never left to sort stability."""
    same_time = [
        make_event("z", EventType.BRAKE_ONSET, "B", 4.0),
        make_event("a", EventType.BRAKE_ONSET, "B", 4.0),
        make_event("m", EventType.BRAKE_ONSET, "A", 4.0),
    ]
    order = [r["event_id"] for r in log_rows(same_time)]
    assert order == [r["event_id"] for r in log_rows(list(reversed(same_time)))]
    # A sorts before B, and within B the event id decides.
    assert order == ["m", "a", "z"]


def test_rows_are_in_nondecreasing_time_order(two_vehicle_events):
    times = [r["t_local"] for r in log_rows(two_vehicle_events)]
    assert times == sorted(times)


# --- the local log claims only what one vehicle knows ----------------------


def test_a_local_log_has_no_common_time_column(two_vehicle_events):
    log = build_local_log("B", [e for e in two_vehicle_events
                                if e.participant_id == "B"])
    assert "t_common" not in log["columns"]
    assert all("t_common" not in row for row in log["rows"])


def test_a_local_log_says_whose_clock_it_is(two_vehicle_events):
    log = build_local_log("B", two_vehicle_events)
    assert log["participant_id"] == "B"
    assert log["provenance"] == Provenance.LOCAL.value
    assert "local" in log["clock"]


def test_a_local_log_counts_what_it_holds(two_vehicle_events):
    log = build_local_log("B", two_vehicle_events)
    assert log["n_rows"] == len(two_vehicle_events)
    assert log["counts_by_type"]["STOP_SIGN_DETECTED"] == 1
    assert sum(log["counts_by_type"].values()) == len(two_vehicle_events)


# --- the global log is honest about alignment ------------------------------


def test_common_time_appears_only_for_aligned_participants(two_vehicle_events):
    """B is aligned with a +0.5 s offset; A is not aligned at all."""
    alignment = {
        "status": "PARTIALLY_ALIGNED",
        "reference": "B",
        "converters": {"B": lambda t: t + 0.5},
    }
    log = build_global_log(two_vehicle_events, alignment=alignment)
    by_id = {r["event_id"]: r for r in log["rows"]}
    assert by_id["b1"]["t_common"] == pytest.approx(5.70)
    assert by_id["a1"]["t_common"] is None
    assert log["aligned_participants"] == ["B"]
    assert log["unaligned_participants"] == ["A"]
    assert log["common_time_available"] is False


def test_a_fully_aligned_run_says_so(two_vehicle_events):
    alignment = {
        "status": "CONTACT_ALIGNED",
        "reference": "A",
        "converters": {"A": lambda t: t, "B": lambda t: t + 0.25},
    }
    log = build_global_log(two_vehicle_events, alignment=alignment)
    assert log["common_time_available"] is True
    assert log["unaligned_participants"] == []
    assert log["aligned_participants"] == ["A", "B"]


def test_with_no_alignment_nothing_gets_a_common_time(two_vehicle_events):
    """The no-collision case. Simulator time must never fill in silently."""
    log = build_global_log(two_vehicle_events, alignment=None)
    assert log["alignment_status"] == "UNALIGNED_NO_SHARED_CONTACT"
    assert all(row["t_common"] is None for row in log["rows"])
    assert log["common_time_available"] is False
    assert "never used as a fallback" in log["note"]


def test_rows_are_ordered_by_common_time_when_it_exists():
    """B is 3 s behind A's clock, so the merged order is not the local order."""
    events = [
        make_event("a_late", EventType.BRAKE_ONSET, "A", 9.0),
        make_event("b_early", EventType.HARD_BRAKE, "B", 7.0),
    ]
    alignment = {
        "status": "CONTACT_ALIGNED",
        "reference": "A",
        "converters": {"A": lambda t: t, "B": lambda t: t + 3.0},
    }
    log = build_global_log(events, alignment=alignment)
    # On B's own clock 7.0 < 9.0; on common time 10.0 > 9.0.
    assert [r["event_id"] for r in log["rows"]] == ["a_late", "b_early"]
    assert log["rows"][1]["t_common"] == pytest.approx(10.0)


def test_a_converter_that_fails_leaves_the_row_unaligned(two_vehicle_events):
    """A broken converter must degrade to 'unaligned', not crash or invent."""
    def broken(_t):
        raise ValueError("no offset")

    log = build_global_log(
        two_vehicle_events,
        alignment={"status": "PARTIALLY_ALIGNED", "converters": {"B": broken}},
    )
    assert all(row["t_common"] is None for row in log["rows"])


# --- the columns a reader was promised -------------------------------------


def test_every_row_carries_the_promised_columns(two_vehicle_events):
    log = build_global_log(
        two_vehicle_events,
        alignment={"converters": {"A": lambda t: t, "B": lambda t: t}},
    )
    for row in log["rows"]:
        for column in LOG_COLUMNS:
            assert column in row, column


def test_the_subject_column_is_filled_for_pairwise_events(two_vehicle_events):
    rows = {r["event_id"]: r for r in log_rows(two_vehicle_events)}
    assert rows["a1"]["subject"] == "B"
    assert rows["b2"]["subject"] == ""


def test_the_sensor_column_names_the_instrument(two_vehicle_events):
    rows = {r["event_id"]: r for r in log_rows(two_vehicle_events)}
    assert rows["b1"]["source_sensor"] == "camera"
    assert rows["a1"]["source_sensor"] == "radar"


def test_a_derived_event_says_derived_rather_than_naming_no_sensor():
    """A non-action has no sensor of its own; it must not show an empty cell."""
    event = make_event("n1", EventType.NO_BRAKING_RESPONSE, "A", 8.0, subject="B")
    assert log_rows([event])[0]["source_sensor"] == "derived"


def test_non_action_detail_survives_into_the_log():
    """The monitored interval is the whole justification and must reach a reader."""
    event = make_event(
        "n1", EventType.NO_BRAKING_RESPONSE, "A", 8.0, subject="B",
        detail={"monitored_interval": [7.2, 8.0], "evidence_coverage": 0.97},
    )
    row = log_rows([event])[0]
    assert row["detail"]["monitored_interval"] == [7.2, 8.0]
    assert row["detail"]["evidence_coverage"] == 0.97


def test_evidence_is_summarised_not_dumped():
    event = make_event(
        "e1", EventType.HARD_BRAKE, "A", 3.0,
        evidence=[Evidence(kind="controls", ref="c-1"),
                  Evidence(kind="controls", ref="c-2"),
                  Evidence(kind="controls", ref="c-3"),
                  Evidence(kind="controls", ref="c-4")],
    )
    summary = log_rows([event])[0]["evidence"]
    assert "controls:c-1" in summary
    assert "+1 more" in summary


# --- the plain-text rendering ---------------------------------------------


def test_format_log_labels_the_axis_it_is_using(two_vehicle_events):
    local = format_log(build_local_log("B", two_vehicle_events))
    assert "t_local" in local.splitlines()[0]

    aligned = format_log(build_global_log(
        two_vehicle_events,
        alignment={"converters": {"A": lambda t: t, "B": lambda t: t}},
    ))
    assert "t_common" in aligned.splitlines()[0]


def test_format_log_shows_a_pairwise_event_as_a_pair(two_vehicle_events):
    text = format_log(build_local_log("A", two_vehicle_events))
    assert "A-B" in text


def test_format_log_says_how_much_it_truncated(two_vehicle_events):
    text = format_log(build_local_log("B", two_vehicle_events), limit=2)
    assert "3 more rows" in text


def test_an_unaligned_row_is_rendered_as_a_dash_not_a_zero(two_vehicle_events):
    """Showing 0.00 for 'unknown' would be a fabricated timestamp."""
    text = format_log(build_global_log(
        two_vehicle_events,
        alignment={"converters": {"B": lambda t: t}},
    ))
    assert "    --  A" in text


def test_a_recorder_the_alignment_excluded_is_named_even_with_no_rows():
    """The case that only shows up on a real partial alignment.

    A recorder with no common time usually contributes no fused events at all,
    so a log deriving its aligned set from the rows would report a clean single
    timeline while silently omitting a whole vehicle.
    """
    events = [
        make_event("a1", EventType.BRAKE_ONSET, "A", 5.0),
        make_event("b1", EventType.HARD_BRAKE, "B", 5.5),
    ]
    log = build_global_log(events, alignment={
        "status": "PARTIALLY_ALIGNED",
        "offsets_s": {"A": 0.0, "B": 0.2},
        "unaligned_participants": ["C"],
    })
    assert log["unaligned_participants"] == ["C"]
    assert log["participants_with_no_rows"] == ["C"]
    assert log["common_time_available"] is False
    assert sorted(log["aligned_participants"]) == ["A", "B"]


def test_offsets_from_the_artifact_are_what_the_log_applies():
    """The transform shown is the one the alignment published, not a copy."""
    events = [make_event("b1", EventType.HARD_BRAKE, "B", 5.0)]
    log = build_global_log(events, alignment={
        "status": "CONTACT_ALIGNED", "offsets_s": {"B": 1.25},
    })
    assert log["rows"][0]["t_common"] == pytest.approx(6.25)
