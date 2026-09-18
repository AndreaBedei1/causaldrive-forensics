"""Non-actions: the claims that are only as good as the watching behind them.

The brief is specific about what may and may not become a non-action node, and
each clause here is one of its requirements. The load-bearing ones are that a
response inside the window must suppress the claim, and that missing evidence
must produce UNKNOWN rather than an assertion -- a detector that skipped the
second would report its most confident failures on the runs where the sensors
worked worst.
"""

from __future__ import annotations

import pytest

from cdf.common.config import Config
from cdf.common.schemas import Event, EventType, Provenance
from cdf.graph.non_actions import (
    NON_ACTION_RULES,
    build_non_actions,
    coverage_from_samples,
)


def ev(event_id: str, event_type: EventType, t: float, pid: str = "A",
       subject: str = None) -> Event:
    return Event(
        event_id=event_id, event_type=event_type, participant_id=pid,
        t_start=t - 0.05, t_peak=t, t_end=t + 0.05, subject=subject,
    )


def types_of(result) -> list:
    return [e.event_type.value for e in result["events"]]


# --- an obligation has to have been observed -------------------------------


def test_nothing_is_asserted_without_an_observed_obligation():
    """A vehicle that simply drove along is not failing to do anything."""
    events = [
        ev("1", EventType.ACCELERATION, 2.0),
        ev("2", EventType.THROTTLE_ONSET, 2.1),
        ev("3", EventType.DECELERATION, 9.0),
    ]
    assert build_non_actions("A", events)["events"] == []


def test_a_stop_sign_alone_is_not_a_failure_to_stop():
    """The line was never crossed, so the obligation has not come due."""
    events = [ev("1", EventType.STOP_SIGN_DETECTED, 5.0)]
    assert build_non_actions("A", events)["events"] == []


def test_seeing_a_sign_and_crossing_the_line_without_stopping_is_asserted():
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    result = build_non_actions("A", events)
    assert types_of(result) == ["NO_STOP_AFTER_STOP_SIGN"]
    node = result["events"][0]
    assert node.detail["monitored_interval"] == [5.12, 5.88]
    assert node.detail["opened_by"] == "1"
    assert node.detail["closed_by"] == "2"


def test_stopping_before_the_line_suppresses_the_claim():
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.FULL_STOP, 5.60),
        ev("3", EventType.STOP_LINE_CROSSED, 6.40),
    ]
    assert build_non_actions("A", events)["events"] == []


def test_stopping_after_crossing_the_line_does_not_count():
    """The obligation is to stop *before* the line, so a later stop is not it."""
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
        ev("3", EventType.FULL_STOP, 7.00),
    ]
    assert types_of(build_non_actions("A", events)) == ["NO_STOP_AFTER_STOP_SIGN"]


# --- responding inside the window suppresses the claim ---------------------


def test_critical_ttc_with_no_response_asserts_both_missing_responses():
    """Neither braking nor steering happened; both are true and separate claims."""
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    assert sorted(types_of(build_non_actions("A", events))) == [
        "NO_BRAKING_RESPONSE", "NO_EVASIVE_RESPONSE",
    ]


def test_braking_in_time_suppresses_the_braking_claim_only():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 8.55),
    ]
    assert types_of(build_non_actions("A", events)) == ["NO_EVASIVE_RESPONSE"]


def test_steering_away_suppresses_the_evasive_claim_only():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.STEER_ONSET, 8.70),
    ]
    assert types_of(build_non_actions("A", events)) == ["NO_BRAKING_RESPONSE"]


def test_a_response_after_the_horizon_is_not_a_response():
    """Braking three seconds after a critical TTC did not answer it."""
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 11.50),
    ]
    assert "NO_BRAKING_RESPONSE" in types_of(build_non_actions("A", events))


def test_the_claim_names_the_vehicle_it_failed_to_respond_to():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    node = build_non_actions("A", events)["events"][0]
    assert node.participant_id == "A"
    assert node.subject == "B"


def test_a_stop_sign_failure_names_no_second_vehicle():
    """There is no other party to the obligation: the sign is not a vehicle."""
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    assert build_non_actions("A", events)["events"][0].subject is None


def test_another_vehicles_response_does_not_discharge_this_ones_obligation():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, pid="A", subject="B"),
        ev("2", EventType.BRAKE_ONSET, 8.50, pid="B"),
    ]
    assert "NO_BRAKING_RESPONSE" in types_of(build_non_actions("A", events))


# --- the lead-in rule looks backwards --------------------------------------


def test_entering_a_conflict_without_having_slowed_is_asserted():
    events = [
        ev("1", EventType.ACCELERATION, 5.0),
        ev("2", EventType.CONFLICT_REGION_ENTRY, 7.11, subject="B"),
    ]
    result = build_non_actions("A", events)
    assert "CONFLICT_ENTRY_WITHOUT_DECELERATION" in types_of(result)
    node = [e for e in result["events"]
            if e.event_type == EventType.CONFLICT_ENTRY_WITHOUT_DECELERATION][0]
    # The window is the approach, so it ends at entry rather than starting there.
    assert node.detail["monitored_interval"][1] == 7.11


def test_slowing_on_the_approach_suppresses_it():
    events = [
        ev("1", EventType.DECELERATION, 6.00),
        ev("2", EventType.CONFLICT_REGION_ENTRY, 7.11, subject="B"),
    ]
    assert "CONFLICT_ENTRY_WITHOUT_DECELERATION" not in types_of(
        build_non_actions("A", events)
    )


def test_slowing_long_before_the_approach_does_not_count():
    """Braking 8 s earlier for something else is not slowing for this conflict."""
    events = [
        ev("1", EventType.DECELERATION, 1.00),
        ev("2", EventType.CONFLICT_REGION_ENTRY, 9.00, subject="B"),
    ]
    assert "CONFLICT_ENTRY_WITHOUT_DECELERATION" in types_of(
        build_non_actions("A", events)
    )


# --- the one rule that asserts a presence ----------------------------------


def test_accelerating_through_a_low_ttc_is_asserted():
    events = [
        ev("1", EventType.LOW_TTC, 8.00, subject="B"),
        ev("2", EventType.THROTTLE_ONSET, 8.30),
    ]
    assert "CONTINUED_ACCELERATION_DURING_CONFLICT" in types_of(
        build_non_actions("A", events)
    )


def test_not_accelerating_through_a_low_ttc_asserts_nothing():
    events = [ev("1", EventType.LOW_TTC, 8.00, subject="B")]
    assert "CONTINUED_ACCELERATION_DURING_CONFLICT" not in types_of(
        build_non_actions("A", events)
    )


# --- insufficient evidence must not become an assertion --------------------


def test_a_gap_over_the_window_produces_unknown_not_a_node():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    result = build_non_actions("A", events, coverage=lambda t0, t1: 0.35)
    assert result["events"] == []
    assert result["n_unknown"] >= 1
    entry = result["unknown"][0]
    assert entry["verdict"] == "UNKNOWN"
    assert entry["evidence_coverage"] == 0.35
    assert "cannot be asserted" in entry["reason"]


def test_partial_coverage_above_the_bar_still_asserts_but_less_confidently():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    result = build_non_actions("A", events, coverage=lambda t0, t1: 0.85)
    node = result["events"][0]
    assert node.confidence == pytest.approx(0.85)
    assert node.detail["evidence_coverage"] == 0.85


def test_full_coverage_is_full_confidence():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    node = build_non_actions("A", events)["events"][0]
    assert node.confidence == pytest.approx(1.0)


def test_the_coverage_bar_is_configurable_and_respected():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    lenient = Config({"non_actions": {"min_evidence_coverage": 0.3}})
    result = build_non_actions("A", events, coverage=lambda t0, t1: 0.35, cfg=lenient)
    assert result["events"]


def test_an_unknown_window_still_records_what_it_could_not_judge():
    """A detector that stayed silent invisibly is indistinguishable from one
    that found nothing, so the declined windows have to be published."""
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    result = build_non_actions("A", events, coverage=lambda t0, t1: 0.1)
    entry = result["unknown"][0]
    assert entry["event_type"] == "NO_STOP_AFTER_STOP_SIGN"
    assert entry["monitored_interval"] == [5.12, 5.88]
    assert entry["required_coverage"] == 0.8


# --- coverage from real sample times ---------------------------------------


def test_a_dense_recording_covers_its_own_span():
    times = [i * 0.05 for i in range(200)]
    coverage = coverage_from_samples(times, expected_period_s=0.05)
    assert coverage(2.0, 4.0) == pytest.approx(1.0)


def test_a_dropout_shows_up_as_missing_coverage():
    """Samples run to 1.95 s, resume at 3.00 s: a 1.05 s hole in a 3 s window."""
    times = [i * 0.05 for i in range(0, 40)] + [i * 0.05 for i in range(60, 120)]
    coverage = coverage_from_samples(times, expected_period_s=0.05)
    assert coverage(1.0, 4.0) == pytest.approx(1.0 - 1.05 / 3.0, abs=0.02)


def test_a_window_entirely_inside_a_dropout_is_covered_not_at_all():
    times = [i * 0.05 for i in range(0, 40)] + [i * 0.05 for i in range(60, 120)]
    coverage = coverage_from_samples(times, expected_period_s=0.05)
    assert coverage(2.2, 2.8) == pytest.approx(0.0, abs=1e-6)


def test_a_window_past_the_end_of_the_recording_is_not_fully_covered():
    times = [i * 0.05 for i in range(100)]  # ends at 4.95 s
    coverage = coverage_from_samples(times, expected_period_s=0.05)
    assert coverage(4.0, 6.0) == pytest.approx(0.475, abs=0.02)


def test_ordinary_jitter_is_not_counted_as_a_gap():
    times = [0.0, 0.05, 0.12, 0.17, 0.22, 0.30, 0.35]
    coverage = coverage_from_samples(times, expected_period_s=0.05)
    assert coverage(0.0, 0.35) == pytest.approx(1.0)


def test_an_empty_recording_covers_nothing():
    assert coverage_from_samples([], expected_period_s=0.05)(0.0, 1.0) == 0.0


# --- structural contracts --------------------------------------------------


def test_every_rule_produces_a_type_in_the_non_action_family():
    from cdf.graph.ontology import NON_ACTION_TYPES

    for rule in NON_ACTION_RULES:
        assert rule.event_type.value in NON_ACTION_TYPES


def test_the_same_obligation_is_not_accused_twice():
    """Two radar events resolving the same threat are one failure, not two."""
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.CRITICAL_TTC, 8.42, subject="B"),
    ]
    result = build_non_actions("A", events)
    assert types_of(result).count("NO_BRAKING_RESPONSE") == 1


def test_nodes_are_emitted_in_time_order():
    events = [
        ev("1", EventType.CRITICAL_TTC, 9.0, subject="B"),
        ev("2", EventType.STOP_SIGN_DETECTED, 2.0),
        ev("3", EventType.STOP_LINE_CROSSED, 2.5),
    ]
    times = [e.t_peak for e in build_non_actions("A", events)["events"]]
    assert times == sorted(times)


def test_the_provenance_passed_in_is_what_the_nodes_carry():
    """The reference runs the same rules, so it must be able to mark them its own."""
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    result = build_non_actions(
        "A", events, provenance=Provenance.ORACLE, id_prefix="ona"
    )
    assert all(e.provenance == Provenance.ORACLE for e in result["events"])
    assert all(e.event_id.startswith("ona-") for e in result["events"])


def test_each_node_carries_the_rule_that_made_it():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    node = build_non_actions("A", events)["events"][0]
    assert node.detail["rule_id"] in {r.rule_id for r in NON_ACTION_RULES}
    assert node.detail["obligation"]
    assert node.detail["would_have_been_discharged_by"]


def test_the_opening_event_is_cited_as_evidence():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    node = build_non_actions("A", events)["events"][0]
    refs = {e.ref for e in node.evidence}
    assert "1" in refs


def test_events_belonging_to_other_participants_are_ignored():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, pid="B", subject="A"),
    ]
    assert build_non_actions("A", events)["events"] == []
