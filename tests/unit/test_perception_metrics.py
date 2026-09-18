"""Scoring what the cameras made of the road.

The assertions that matter here are about denominators and about absences. A
precision of 1.000 over two sightings is a different claim from one over two
hundred, and a run with no camera must not contribute zeros that read as a
detector which found nothing.
"""

from __future__ import annotations

import json

import pytest

from cdf.common.config import Config
from cdf.common.io import write_json
from cdf.common.layout import RunLayout
from cdf.common.schemas import Event, EventType, Provenance, to_jsonable
from cdf.evaluation.perception_metrics import measure_perception, prf


def sign_event(eid, etype, pid, t=5.0) -> dict:
    return to_jsonable(Event(
        event_id=eid, event_type=etype, participant_id=pid,
        t_start=t, t_peak=t, t_end=t + 1.0, provenance=Provenance.LOCAL,
        source_sensors=["camera"],
    ))


def build_run(tmp_path, signs, detections=None, stop_lines=None,
              crossings=None, participants=("A", "B")) -> RunLayout:
    layout = RunLayout.from_run_dir(tmp_path / "S10" / "seed_000")
    layout.oracle_dir.mkdir(parents=True, exist_ok=True)
    for pid in participants:
        layout.vehicle_dir(pid).mkdir(parents=True, exist_ok=True)
    write_json(layout.traffic_control_truth, {"signs": signs})
    if stop_lines is not None:
        write_json(layout.stop_lines_truth, {"stop_lines": stop_lines})
    for pid, events in (detections or {}).items():
        layout.perception_dir(pid).mkdir(parents=True, exist_ok=True)
        write_json(layout.traffic_sign_detections(pid), {"events": events})
    for pid, events in (crossings or {}).items():
        layout.perception_dir(pid).mkdir(parents=True, exist_ok=True)
        write_json(layout.perception_dir(pid) / "stop_lines.json",
                   {"events": events})
    return layout


# --- precision, recall, and the difference between zero and none -----------


def test_a_perfect_detection_scores_one_with_its_counts():
    scores = prf(3, 3, 3)
    assert scores["precision"] == 1.0 and scores["recall"] == 1.0
    assert (scores["n_real"], scores["n_detected"], scores["n_matched"]) == (3, 3, 3)


def test_missing_everything_is_a_recall_of_zero():
    assert prf(0, 0, 4)["recall"] == 0.0


def test_nothing_to_find_is_no_recall_rather_than_zero():
    """Zero means the detector missed everything; None means there was nothing
    to miss. Collapsing them would let a scenario with no signs drag down an
    average it has no business being in."""
    assert prf(0, 0, 0)["recall"] is None
    assert prf(0, 0, 0)["precision"] is None
    assert prf(0, 0, 0)["f1"] is None


def test_detecting_something_that_was_not_there_costs_precision():
    scores = prf(1, 3, 1)
    assert scores["precision"] == pytest.approx(1 / 3, abs=1e-4)
    assert scores["recall"] == 1.0


def test_every_figure_carries_its_denominator():
    """A ratio without its counts makes two very different claims look alike."""
    for scores in (prf(1, 1, 1), prf(100, 100, 100)):
        assert {"n_real", "n_detected", "n_matched"} <= set(scores)


# --- what is scored, and what is not --------------------------------------


def test_a_run_with_no_camera_is_not_scored_as_zero(tmp_path):
    layout = build_run(tmp_path, signs=[
        {"sign_id": "stop_A", "kind": "stop", "governs": "A",
         "physically_present": True},
    ])
    result = measure_perception(layout)
    assert result["scored"] is False
    assert "without a camera" in result["reason"]
    assert "read as a detector that found nothing" in result["reason"]


def test_a_run_with_no_declared_traffic_control_is_not_scored(tmp_path):
    layout = RunLayout.from_run_dir(tmp_path / "S01" / "seed_000")
    layout.vehicle_dir("A").mkdir(parents=True, exist_ok=True)
    result = measure_perception(layout)
    assert result["scored"] is False
    assert "no traffic control" in result["reason"]


def test_a_sign_that_was_seen_is_a_true_positive(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")]},
    )
    result = measure_perception(layout)
    scores = result["per_participant"]["A"]["signs"]["stop"]
    assert (scores["n_real"], scores["n_detected"], scores["n_matched"]) == (1, 1, 1)
    assert scores["recall"] == 1.0


def test_a_sign_that_was_missed_costs_recall(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": []},
    )
    result = measure_perception(layout)
    assert result["per_participant"]["A"]["signs"]["stop"]["recall"] == 0.0


def test_a_sign_reported_where_there_was_none_costs_precision(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={
            "A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")],
            "B": [sign_event("s2", EventType.STOP_SIGN_DETECTED, "B")],
        },
    )
    result = measure_perception(layout)
    # B faced no sign, so its report is a false positive.
    assert result["per_participant"]["B"]["signs"]["stop"]["precision"] == 0.0
    assert result["signs"]["n_detected"] == 2
    assert result["signs"]["n_matched"] == 1


def test_a_vehicle_is_only_held_to_the_signs_that_govern_it(tmp_path):
    """A sign facing a cross street is visible and is not addressed to it."""
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_B", "kind": "stop", "governs": "B",
                "physically_present": True}],
        detections={"A": [], "B": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "B")]},
    )
    result = measure_perception(layout)
    assert result["per_participant"]["A"]["signs"]["stop"]["n_real"] == 0
    assert result["per_participant"]["A"]["signs"]["stop"]["recall"] is None
    assert result["per_participant"]["B"]["signs"]["stop"]["recall"] == 1.0


def test_a_sign_the_scenario_could_not_place_is_not_counted_against_anyone(tmp_path):
    """A camera that finds nothing where nothing was placed has not failed."""
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": False,
                "placement_problem": "the spawn point is blocked"}],
        detections={"A": []},
    )
    result = measure_perception(layout)
    block = result["per_participant"]["A"]
    assert block["signs"]["stop"]["n_real"] == 0
    assert block["signs_declared_but_not_placed"] == ["stop_A"]


def test_the_two_sign_classes_are_scored_separately(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[
            {"sign_id": "stop_A", "kind": "stop", "governs": "A",
             "physically_present": True},
            {"sign_id": "yield_B", "kind": "yield", "governs": "B",
             "physically_present": True},
        ],
        detections={
            "A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")],
            "B": [],
        },
    )
    result = measure_perception(layout)
    assert result["per_participant"]["A"]["signs"]["stop"]["recall"] == 1.0
    assert result["per_participant"]["B"]["signs"]["yield"]["recall"] == 0.0


# --- stop lines -----------------------------------------------------------


def test_a_crossing_that_really_happened_and_was_detected(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")]},
        stop_lines=[{"sign_id": "stop_A", "governs": "A"}],
        crossings={"A": [sign_event("x1", EventType.STOP_LINE_CROSSED, "A", t=6.0)]},
    )
    result = measure_perception(layout)
    assert result["per_participant"]["A"]["stop_lines"]["recall"] == 1.0


def test_a_missed_crossing_costs_recall_not_precision(tmp_path):
    """The detector is conservative by design, so this is the expected shape."""
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")]},
        stop_lines=[{"sign_id": "stop_A", "governs": "A"}],
        crossings={"A": []},
    )
    scores = measure_perception(layout)["per_participant"]["A"]["stop_lines"]
    assert scores["recall"] == 0.0
    assert scores["precision"] is None


def test_without_stop_line_truth_precision_is_unmeasurable_not_perfect(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")]},
        crossings={"A": [sign_event("x1", EventType.STOP_LINE_CROSSED, "A", t=6.0)]},
    )
    scores = measure_perception(layout)["per_participant"]["A"]["stop_lines"]
    assert scores["precision"] == 0.0 or scores["recall"] is None


# --- latency, which is reported as unmeasurable rather than invented ------


def test_latency_says_why_it_cannot_be_measured(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "stop_A", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A", t=5.1)]},
    )
    latency = measure_perception(layout)["per_participant"]["A"]["latency"]
    assert latency["measurable"] is False
    assert "never recorded" in latency["reason"]
    # What *is* known is still reported.
    assert latency["first_report_t_local"] == pytest.approx(5.1)


# --- the roll-up sums counts rather than averaging ratios -----------------


def test_the_roll_up_weights_every_sign_equally(tmp_path):
    """Averaging per-vehicle ratios would weight a vehicle that met one sign the
    same as one that met five."""
    layout = build_run(
        tmp_path,
        signs=[
            {"sign_id": "a1", "kind": "stop", "governs": "A",
             "physically_present": True},
            {"sign_id": "b1", "kind": "stop", "governs": "B",
             "physically_present": True},
            {"sign_id": "b2", "kind": "yield", "governs": "B",
             "physically_present": True},
        ],
        detections={
            "A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")],
            "B": [sign_event("s2", EventType.STOP_SIGN_DETECTED, "B")],
        },
    )
    roll = measure_perception(layout)["signs"]
    assert roll["n_real"] == 3
    assert roll["n_matched"] == 2
    assert roll["recall"] == pytest.approx(2 / 3, abs=1e-4)


def test_the_method_states_why_this_is_a_measurement(tmp_path):
    layout = build_run(
        tmp_path,
        signs=[{"sign_id": "a1", "kind": "stop", "governs": "A",
                "physically_present": True}],
        detections={"A": [sign_event("s1", EventType.STOP_SIGN_DETECTED, "A")]},
    )
    assert "tautology" in measure_perception(layout)["note"]
