"""The temporal-logic layer, and the one rule it exists to enforce.

Section 36 of the brief names the cases: stop before line, TTC response,
collision then rest, non-action consistency, and -- underlined -- that missing
evidence must never become PASS. The last is the reason for three-valued
semantics at all, and it has two sources that are really one: a window running
past the end of the recording, and a window across a sensor dropout. In both the
response might have happened and not been recorded, so neither a pass nor a
failure is available.
"""

from __future__ import annotations

import pytest

from cdf.common.config import Config
from cdf.common.schemas import CheckStatus, Event, EventType
from cdf.formal.evaluator import Verdict, evaluate
from cdf.formal.properties import PROPERTIES, property_by_id
from cdf.formal.report import check_all, check_property, describe_properties
from cdf.formal.syntax import (
    ANY, SELF, SUBJECT,
    Always, And, Eventually, Historically, Not, Occurs, Once, Or, render,
)
from cdf.formal.trace import EventTrace

PASS, FAIL, UNKNOWN = CheckStatus.PASS, CheckStatus.FAIL, CheckStatus.UNKNOWN


def ev(eid, etype, t, pid="A", subject=None) -> Event:
    return Event(
        event_id=eid, event_type=etype, participant_id=pid,
        t_start=t - 0.02, t_peak=t, t_end=t + 0.02, subject=subject,
    )


def trace_of(events, t_start=0.0, t_end=25.0, coverage=None, aligned=("A", "B", "C")):
    return EventTrace.from_events(
        events, t_start=t_start, t_end=t_end, coverage=coverage,
        time_axis="common", aligned_participants=aligned,
    )


def check(formula, events, t, binding=None, **kwargs) -> Verdict:
    return evaluate(
        formula, trace_of(events, **kwargs), t, binding or {SELF: "A", SUBJECT: "B"},
    )


# --- atoms and connectives -------------------------------------------------


def test_an_atom_holds_where_its_event_is():
    events = [ev("1", EventType.BRAKE_ONSET, 5.0)]
    assert check(Occurs(EventType.BRAKE_ONSET), events, 5.0).status is PASS
    assert check(Occurs(EventType.BRAKE_ONSET), events, 6.0).status is FAIL


def test_an_atom_is_bound_to_the_vehicle_the_property_is_about():
    events = [ev("1", EventType.BRAKE_ONSET, 5.0, pid="B")]
    assert check(Occurs(EventType.BRAKE_ONSET, who=SELF), events, 5.0).status is FAIL
    assert check(
        Occurs(EventType.BRAKE_ONSET, who=SUBJECT), events, 5.0
    ).status is PASS
    assert check(Occurs(EventType.BRAKE_ONSET, who=ANY), events, 5.0).status is PASS


def test_an_atom_can_require_a_particular_subject():
    events = [ev("1", EventType.CRITICAL_TTC, 5.0, pid="A", subject="B")]
    assert check(
        Occurs(EventType.CRITICAL_TTC, who=SELF, about=SUBJECT), events, 5.0
    ).status is PASS
    assert check(
        Occurs(EventType.CRITICAL_TTC, who=SELF, about=SUBJECT), events, 5.0,
        binding={SELF: "A", SUBJECT: "C"},
    ).status is FAIL


def test_kleene_and_is_false_as_soon_as_one_conjunct_is():
    """FAIL & UNKNOWN is FAIL: the other operand cannot rescue it."""
    events = [ev("1", EventType.BRAKE_ONSET, 5.0)]
    formula = And(
        Not(Occurs(EventType.BRAKE_ONSET)),
        Eventually(0.0, 5.0, Occurs(EventType.FULL_STOP)),  # runs past the end
    )
    assert check(formula, events, 5.0, t_end=6.0).status is FAIL


def test_kleene_or_is_true_as_soon_as_one_disjunct_is():
    events = [ev("1", EventType.BRAKE_ONSET, 5.0)]
    formula = Or(
        Occurs(EventType.BRAKE_ONSET),
        Eventually(0.0, 5.0, Occurs(EventType.FULL_STOP)),
    )
    assert check(formula, events, 5.0, t_end=6.0).status is PASS


def test_negating_unknown_stays_unknown():
    formula = Not(Eventually(0.0, 5.0, Occurs(EventType.FULL_STOP)))
    assert check(formula, [], 5.0, t_end=6.0).status is UNKNOWN


# --- the metric operators --------------------------------------------------


def test_eventually_finds_a_witness_in_its_window():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42), ev("2", EventType.BRAKE_ONSET, 8.9)]
    verdict = check(Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 8.42)
    assert verdict.status is PASS
    assert verdict.witness == ["2"]


def test_eventually_fails_when_the_window_is_fully_observed_and_empty():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42)]
    verdict = check(Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 8.42)
    assert verdict.status is FAIL
    assert "fully observed" in verdict.reason


def test_always_finds_its_counterexample():
    events = [ev("1", EventType.CRITICAL_TTC, 8.0), ev("2", EventType.THROTTLE_ONSET, 9.0)]
    verdict = check(
        Always(0.0, 2.0, Not(Occurs(EventType.THROTTLE_ONSET))), events, 8.0
    )
    assert verdict.status is FAIL
    assert verdict.witness == ["2"]


def test_always_passes_over_an_observed_window_with_no_violation():
    events = [ev("1", EventType.CRITICAL_TTC, 8.0)]
    verdict = check(
        Always(0.0, 2.0, Not(Occurs(EventType.THROTTLE_ONSET))), events, 8.0
    )
    assert verdict.status is PASS


def test_once_looks_backwards():
    events = [ev("1", EventType.FULL_STOP, 5.6), ev("2", EventType.STOP_LINE_CROSSED, 6.4)]
    assert check(Once(0.0, 2.0, Occurs(EventType.FULL_STOP)), events, 6.4).status is PASS
    assert check(
        Eventually(0.0, 2.0, Occurs(EventType.FULL_STOP)), events, 6.4
    ).status is FAIL


def test_historically_looks_backwards_universally():
    events = [ev("1", EventType.THROTTLE_ONSET, 5.0), ev("2", EventType.CRITICAL_TTC, 6.0)]
    verdict = check(
        Historically(0.0, 2.0, Not(Occurs(EventType.THROTTLE_ONSET))), events, 6.0
    )
    assert verdict.status is FAIL


def test_the_interval_a_verdict_covers_is_reported():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42)]
    verdict = check(Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 8.42)
    assert verdict.interval == pytest.approx((8.42, 9.92))


# --- missing evidence must never become PASS (or FAIL) ---------------------


def test_a_window_past_the_end_of_the_recording_is_unknown():
    """The braking may be in the part that was never recorded."""
    events = [ev("1", EventType.CRITICAL_TTC, 24.5)]
    verdict = check(
        Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 24.5, t_end=25.0
    )
    assert verdict.status is UNKNOWN
    assert verdict.unobserved is True
    assert "never observed" in verdict.reason


def test_a_window_before_the_start_of_the_recording_is_unknown():
    events = [ev("1", EventType.STOP_LINE_CROSSED, 1.0)]
    verdict = check(
        Once(0.0, 5.0, Occurs(EventType.FULL_STOP)), events, 1.0, t_start=0.0
    )
    assert verdict.status is UNKNOWN


def test_a_dropout_across_the_window_is_unknown_not_a_failure():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42)]
    verdict = check(
        Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 8.42,
        coverage=lambda a, b: 0.2,
    )
    assert verdict.status is UNKNOWN
    assert verdict.coverage == pytest.approx(0.2)
    assert "would not have been recorded" in verdict.reason


def test_a_witness_inside_a_poorly_covered_window_still_settles_it():
    """Something seen to happen happened, whatever else the sensor missed."""
    events = [ev("1", EventType.CRITICAL_TTC, 8.42), ev("2", EventType.BRAKE_ONSET, 8.6)]
    verdict = check(
        Eventually(0.0, 1.5, Occurs(EventType.BRAKE_ONSET)), events, 8.42,
        coverage=lambda a, b: 0.2,
    )
    assert verdict.status is PASS


def test_a_counterexample_inside_a_poorly_covered_window_still_settles_it():
    events = [ev("1", EventType.CRITICAL_TTC, 8.0), ev("2", EventType.THROTTLE_ONSET, 9.0)]
    verdict = check(
        Always(0.0, 2.0, Not(Occurs(EventType.THROTTLE_ONSET))), events, 8.0,
        coverage=lambda a, b: 0.1,
    )
    assert verdict.status is FAIL


# --- the properties from section 18 ---------------------------------------


def test_stop_sign_then_full_stop_before_the_line_passes():
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.FULL_STOP, 5.60),
        ev("3", EventType.STOP_LINE_CROSSED, 6.40),
    ]
    result = check_property(property_by_id("P1"), trace_of(events))
    assert result["status"] == PASS.value
    assert result["n_instances"] == 1


def test_stop_sign_then_crossing_at_speed_fails():
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    result = check_property(property_by_id("P1"), trace_of(events))
    assert result["status"] == FAIL.value
    assert result["counterexamples"][0]["trigger_event_id"] == "2"


def test_a_line_crossed_too_early_to_see_the_approach_is_unknown():
    """The recording starts after the sign would have been seen."""
    events = [ev("1", EventType.STOP_LINE_CROSSED, 0.30)]
    result = check_property(property_by_id("P1"), trace_of(events, t_start=0.0))
    assert result["status"] == UNKNOWN.value


def test_critical_ttc_answered_by_braking_passes():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 8.55),
    ]
    assert check_property(property_by_id("P3"), trace_of(events))["status"] == PASS.value


def test_critical_ttc_with_no_response_fails():
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    assert check_property(property_by_id("P3"), trace_of(events))["status"] == FAIL.value


def test_braking_then_accelerating_again_passes_p3_but_fails_p4():
    """Two different questions, and a method with only one would miss this."""
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.0, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 8.2),
        ev("3", EventType.THROTTLE_ONSET, 9.4),
    ]
    tr = trace_of(events)
    assert check_property(property_by_id("P3"), tr)["status"] == PASS.value
    assert check_property(property_by_id("P4"), tr)["status"] == FAIL.value


def test_collision_then_coming_to_rest_passes():
    events = [
        ev("1", EventType.COLLISION, 8.77, subject="B"),
        ev("2", EventType.POST_IMPACT_STOP, 10.2),
    ]
    assert check_property(property_by_id("P5"), trace_of(events))["status"] == PASS.value


def test_a_collision_near_the_end_of_the_window_is_unknown_not_a_failure():
    events = [ev("1", EventType.COLLISION, 23.5, subject="B")]
    result = check_property(property_by_id("P5"), trace_of(events, t_end=25.0))
    assert result["status"] == UNKNOWN.value


def test_crossing_a_solid_line_is_a_located_violation():
    events = [ev("1", EventType.SOLID_LINE_CROSSED, 7.2)]
    result = check_property(property_by_id("P6"), trace_of(events))
    assert result["status"] == FAIL.value
    assert result["counterexamples"][0]["t"] == 7.2
    assert "benchmark" in (result["benchmark_rule"] or "").lower()


def non_action(eid, t0, t1, pid="A", subject="B") -> Event:
    """A non-action node has the shape the detector gives it: it spans the
    window it monitored, rather than being an instant."""
    return Event(
        event_id=eid, event_type=EventType.NO_BRAKING_RESPONSE,
        participant_id=pid, t_start=t0, t_peak=t1, t_end=t1, subject=subject,
    )


def test_the_non_action_claim_is_checked_against_the_trace():
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        non_action("2", 8.42, 9.92),
    ]
    assert check_property(property_by_id("P8"), trace_of(events))["status"] == PASS.value


def test_a_non_action_contradicted_by_the_trace_fails():
    """The graph says A never braked; the trace shows A braking. One is wrong."""
    events = [
        ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 8.55),
        non_action("3", 8.42, 9.92),
    ]
    assert check_property(property_by_id("P8"), trace_of(events))["status"] == FAIL.value


def test_the_non_action_property_anchors_at_the_start_of_the_window():
    """Anchoring at the peak would search after the window and always confirm."""
    result = check_property(
        property_by_id("P8"),
        trace_of([ev("1", EventType.CRITICAL_TTC, 8.42, subject="B"),
                  non_action("2", 8.42, 9.92)]),
    )
    assert result["instances"][0]["anchor"] == "t_start"
    assert result["instances"][0]["t"] == 8.42


# --- vacuity, and the trap of counting it as success ----------------------


def test_a_property_whose_trigger_never_fired_is_vacuous_not_passed():
    result = check_property(property_by_id("P1"), trace_of([]))
    assert result["vacuous"] is True
    assert result["n_instances"] == 0
    assert "Vacuous rather than satisfied" in result["reason"]


def test_vacuous_properties_are_counted_apart_from_the_pass_rate():
    """Otherwise a run containing almost no obligations would score best."""
    events = [ev("1", EventType.CRITICAL_TTC, 8.42, subject="B")]
    report = check_all(trace_of(events))
    assert report["summary"]["n_vacuous"] > 0
    assert report["summary"]["n_checked"] < report["summary"]["n_properties"]
    assert report["summary"]["n_checked"] == (
        report["summary"]["n_pass"] + report["summary"]["n_fail"]
        + report["summary"]["n_unknown"]
    )


def test_one_failing_instance_fails_the_property_however_many_passed():
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 2.0),
        ev("2", EventType.FULL_STOP, 2.5),
        ev("3", EventType.STOP_LINE_CROSSED, 3.0),
        ev("4", EventType.STOP_SIGN_DETECTED, 10.0),
        ev("5", EventType.STOP_LINE_CROSSED, 10.8),
    ]
    result = check_property(property_by_id("P1"), trace_of(events))
    assert result["status"] == FAIL.value
    assert result["n_pass"] == 1 and result["n_fail"] == 1


def test_an_undecided_instance_prevents_a_pass_but_not_a_failure():
    events = [
        ev("1", EventType.CRITICAL_TTC, 5.0, subject="B"),
        ev("2", EventType.BRAKE_ONSET, 5.2),
        ev("3", EventType.CRITICAL_TTC, 24.6, subject="B"),
    ]
    result = check_property(property_by_id("P3"), trace_of(events, t_end=25.0))
    assert result["status"] == UNKNOWN.value
    assert result["n_pass"] == 1 and result["n_unknown"] == 1


# --- two vehicles need one clock ------------------------------------------


def test_a_two_vehicle_property_is_unknown_on_an_unaligned_trace():
    events = [
        ev("1", EventType.COLLISION, 8.0, pid="A", subject="B"),
        ev("2", EventType.COLLISION, 9.0, pid="B", subject="C"),
    ]
    tr = EventTrace.from_events(
        events, t_start=0.0, t_end=25.0, time_axis="local", aligned_participants=(),
    )
    result = check_property(property_by_id("P7"), tr)
    assert result["status"] == UNKNOWN.value
    assert "two different clocks" in result["reason"]


def test_the_same_property_is_decidable_once_the_clocks_are_aligned():
    events = [
        ev("1", EventType.COLLISION, 8.0, pid="A", subject="B"),
        ev("2", EventType.COLLISION, 9.0, pid="B", subject="C"),
    ]
    result = check_property(property_by_id("P7"), trace_of(events))
    assert result["status"] == PASS.value


def test_one_impact_reported_twice_by_two_recorders_is_caught():
    """Badly aligned duplicates show up as a pair colliding twice in a moment."""
    events = [
        ev("1", EventType.COLLISION, 8.00, pid="A", subject="B"),
        ev("2", EventType.COLLISION, 8.30, pid="A", subject="B"),
    ]
    assert check_property(property_by_id("P7"), trace_of(events))["status"] == FAIL.value


def test_two_genuinely_different_impacts_in_a_chain_are_not_flagged():
    events = [
        ev("1", EventType.COLLISION, 8.00, pid="A", subject="B"),
        ev("2", EventType.COLLISION, 8.30, pid="B", subject="C"),
    ]
    assert check_property(property_by_id("P7"), trace_of(events))["status"] == PASS.value


# --- the formula is the thing that runs -----------------------------------


def test_every_property_renders_the_formula_that_was_evaluated():
    for prop in PROPERTIES:
        rendered = prop.describe()["formula"]
        assert rendered == render(prop.formula)
        assert rendered.strip()


def test_the_published_description_lists_every_property():
    described = describe_properties()
    assert len(described["properties"]) == len(PROPERTIES)
    assert set(described["verdicts"]) == {"PASS", "FAIL", "UNKNOWN", "vacuous"}
    assert "never becomes PASS" in described["note"]


def test_the_report_records_which_clock_its_intervals_are_in():
    report = check_all(trace_of([ev("1", EventType.CRITICAL_TTC, 8.0, subject="B")]))
    assert report["trace"]["time_axis"] == "common"
    assert report["trace"]["duration_s"] == 25.0


def test_the_unknown_rate_is_over_checked_properties_only():
    events = [ev("1", EventType.COLLISION, 24.9, subject="B")]
    report = check_all(trace_of(events, t_end=25.0))
    summary = report["summary"]
    assert summary["unknown_rate"] == pytest.approx(
        summary["n_unknown"] / summary["n_checked"]
    )


def test_a_formula_renders_readably():
    formula = Eventually(0.0, 1.5, Or(
        Occurs(EventType.BRAKE_ONSET, who=SELF),
        Occurs(EventType.STEER_ONSET, who=SELF),
    ))
    assert render(formula) == "F[0,1.5] (BRAKE_ONSET(self) | STEER_ONSET(self))"


# --- the Since operator, which sets its window from an event ---------------


def test_since_scopes_the_check_to_the_stretch_after_the_marker():
    """A stop made before the sign was seen does not discharge the obligation.

    This is what Once cannot express, and the reason Since exists: the stop at
    1.0 s is in the last twelve seconds, but it is not between the sign and the
    line, so the obligation is unmet.
    """
    from cdf.formal.syntax import Since

    events = [
        ev("1", EventType.FULL_STOP, 1.0),
        ev("2", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("3", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    # Once is satisfied by the earlier stop...
    assert check(Once(0.0, 12.0, Occurs(EventType.FULL_STOP)), events, 5.88).status is PASS
    # ...but the property, written with Since, is not.
    assert check_property(property_by_id("P1"), trace_of(events))["status"] == FAIL.value


def test_since_uses_the_most_recent_marker_not_the_first():
    """Two signs on one approach: the obligation is the nearer one's."""
    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 2.0),
        ev("2", EventType.FULL_STOP, 2.4),
        ev("3", EventType.STOP_SIGN_DETECTED, 8.0),
        ev("4", EventType.STOP_LINE_CROSSED, 8.6),
    ]
    assert check_property(property_by_id("P1"), trace_of(events))["status"] == FAIL.value


def test_since_reports_the_stretch_it_actually_checked():
    from cdf.formal.syntax import Since

    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.FULL_STOP, 5.60),
        ev("3", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    verdict = check(
        Since(0.0, 12.0, Not(Occurs(EventType.FULL_STOP)),
              Occurs(EventType.STOP_SIGN_DETECTED)),
        events, 5.88,
    )
    assert verdict.status is FAIL
    assert verdict.interval[0] == pytest.approx(5.12)


def test_a_gap_after_the_marker_leaves_since_undecided():
    from cdf.formal.syntax import Since

    events = [
        ev("1", EventType.STOP_SIGN_DETECTED, 5.12),
        ev("2", EventType.STOP_LINE_CROSSED, 5.88),
    ]
    verdict = check(
        Since(0.0, 12.0, Not(Occurs(EventType.FULL_STOP)),
              Occurs(EventType.STOP_SIGN_DETECTED)),
        events, 5.88, coverage=lambda a, b: 0.3,
    )
    assert verdict.status is UNKNOWN
