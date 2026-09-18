"""The five responsibility cases from section 37, and the vocabulary rules.

Case D is the one worth writing the layer for. C hits B, B is shunted into A, and
B physically collides with A -- B's mass, B's momentum, B's collision sensor. Any
method that reads causal ancestry naively makes B a contributor to an impact B
had no way to avoid. Getting that right is the difference between a
reconstruction and a list of whoever was touching whom.
"""

from __future__ import annotations

import json

import pytest

from cdf.common.config import Config
from cdf.common.schemas import (
    CausalEdgeType, Event, EventType, GraphDocument, GraphEdge, Provenance,
)
from cdf.responsibility import (
    BENCHMARK_RULE, EVIDENCE_LEVELS, PRIORITY_VERDICTS,
    benchmark_priority, build_responsibility_graph, build_responsibility_report,
)


def ev(eid, etype, t, pid="A", subject=None, detail=None) -> Event:
    return Event(
        event_id=eid, event_type=etype, participant_id=pid,
        t_start=t - 0.05, t_peak=t, t_end=t + 0.05, subject=subject,
        detail=detail or {},
    )


def non_action(eid, etype, pid, t0, t1, subject=None, rule="NA1") -> Event:
    return Event(
        event_id=eid, event_type=etype, participant_id=pid,
        t_start=t0, t_peak=t1, t_end=t1, subject=subject,
        detail={
            "rule_id": rule, "monitored_interval": [t0, t1],
            "evidence_coverage": 1.0, "obligation": "an observed obligation",
        },
    )


def dag(nodes, edges) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=Provenance.FUSED, run_id="t", scenario_id="T",
        seed=0,
        nodes=list(nodes),
        edges=[
            GraphEdge(source=s, target=t, edge_type=CausalEdgeType.CONTRIBUTES_TO.value)
            for s, t in edges
        ],
    )


def node_types(graph, participant=None):
    return sorted(
        n["node_type"] for n in graph["nodes"]
        if participant is None or n["participant"] == participant
    )


# --- CASE A: a stop sign run, with causal relevance ------------------------


@pytest.fixture
def case_a():
    """A sees a stop sign, does not stop, enters the junction, hits B."""
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 5.12, pid="A"),
        ev("a2", EventType.STOP_LINE_CROSSED, 5.88, pid="A"),
        non_action("a3", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88),
        ev("a4", EventType.CONFLICT_REGION_ENTRY, 6.2, pid="A", subject="B"),
        ev("a5", EventType.COLLISION, 6.9, pid="A", subject="B"),
    ]
    graph = dag(events, [("a3", "a4"), ("a4", "a5"), ("a2", "a4")])
    return events, graph


def test_the_chain_from_sign_to_violation_is_built(case_a):
    events, graph = case_a
    result = build_responsibility_graph(events, physical_graph=graph)
    assert "STOP_REQUIRED" in node_types(result, "A")
    assert "STOP_RULE_VIOLATION" in node_types(result, "A")


def test_the_obligation_is_linked_to_the_violation_it_was_not_discharged_by(case_a):
    events, graph = case_a
    result = build_responsibility_graph(events, physical_graph=graph)
    relations = {(e["source"], e["target"], e["relation"]) for e in result["edges"]}
    obligation = [n for n in result["nodes"] if n["node_type"] == "STOP_REQUIRED"][0]
    violation = [
        n for n in result["nodes"] if n["node_type"] == "STOP_RULE_VIOLATION"
    ][0]
    assert (obligation["node_id"], violation["node_id"], "UNDISCHARGED_BY") in relations


def test_a_contribution_needs_both_halves(case_a):
    events, graph = case_a
    result = build_responsibility_graph(events, physical_graph=graph)
    assert "RESPONSIBILITY_CONTRIBUTION" in node_types(result, "A")
    assert result["per_participant"]["A"]["physically_relevant"] is True


def test_a_rule_broken_with_no_causal_path_is_not_a_contribution():
    """A ran a stop sign a hundred metres from a collision it had no part in."""
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 5.12, pid="A"),
        ev("a2", EventType.STOP_LINE_CROSSED, 5.88, pid="A"),
        non_action("a3", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88),
        ev("b1", EventType.HARD_BRAKE, 9.0, pid="B"),
        ev("b2", EventType.COLLISION, 9.9, pid="B", subject="C"),
    ]
    graph = dag(events, [("b1", "b2")])
    result = build_responsibility_graph(events, physical_graph=graph)
    assert "STOP_RULE_VIOLATION" in node_types(result, "A")
    assert "RESPONSIBILITY_CONTRIBUTION" not in node_types(result, "A")


def test_a_causal_path_with_no_rule_broken_is_not_a_contribution():
    """B braked lawfully and was rear-ended. Causally involved, nothing wrong."""
    events = [
        ev("b1", EventType.HARD_BRAKE, 4.0, pid="B"),
        ev("a1", EventType.COLLISION, 5.5, pid="A", subject="B"),
    ]
    graph = dag(events, [("b1", "a1")])
    result = build_responsibility_graph(events, physical_graph=graph)
    assert "RESPONSIBILITY_CONTRIBUTION" not in node_types(result, "B")


def test_the_report_calls_that_case_partial_and_says_why():
    events = [
        ev("b1", EventType.HARD_BRAKE, 4.0, pid="B"),
        ev("a1", EventType.COLLISION, 5.5, pid="A", subject="B"),
    ]
    graph = dag(events, [("b1", "a1")])
    rgraph = build_responsibility_graph(events, physical_graph=graph)
    report = build_responsibility_report(rgraph, events)
    finding = report["findings"]["B"]
    assert finding["responsibility_evidence"] == "partial"
    assert "done nothing wrong" in finding["why"]


# --- CASE D: the pushed vehicle -------------------------------------------


@pytest.fixture
def case_d():
    """C hits B; B is shunted into A. B did nothing to cause the second impact."""
    events = [
        ev("c1", EventType.THROTTLE_ONSET, 3.0, pid="C"),
        ev("c2", EventType.CONTINUED_ACCELERATION_DURING_CONFLICT, 4.0, pid="C",
           subject="B"),
        ev("x1", EventType.COLLISION, 5.0, pid="C", subject="B"),
        ev("x2", EventType.COLLISION, 5.3, pid="B", subject="A"),
        ev("b1", EventType.VEHICLE_STARTED, 0.5, pid="B"),
    ]
    graph = dag(events, [
        ("c1", "c2"), ("c2", "x1"),
        ("x1", "x2"),        # the shunt: the first impact produced the second
    ])
    return events, graph


def test_the_pushed_vehicle_is_not_made_a_contributor(case_d):
    events, graph = case_d
    result = build_responsibility_graph(events, physical_graph=graph)
    assert "RESPONSIBILITY_CONTRIBUTION" not in node_types(result, "B")
    assert result["per_participant"]["B"]["physically_relevant"] is False
    # And specifically: B does not reach the impact it was shunted into.
    assert result["per_participant"]["B"]["outcomes"]["x2"]["reached"] is False


def test_striker_and_struck_are_told_apart_without_asking_who_hit_whom(case_d):
    """The collision record names two parties and not which struck which."""
    events, graph = case_d
    result = build_responsibility_graph(events, physical_graph=graph)
    assert result["per_participant"]["C"]["impacts_this_vehicle_caused"] == ["x1"]
    assert result["per_participant"]["B"]["impacts_this_vehicle_caused"] == []


def test_a_vehicle_that_contributed_to_being_hit_does_reach_what_followed():
    """B brakes hard, C runs into B, B is shunted into A.

    B's braking really is in the chain that ends at A, so the route is open --
    and whether that counts against B is the other half of the claim, answered
    by whether B broke any rule. Here B broke none.
    """
    events = [
        ev("b1", EventType.HARD_BRAKE, 4.0, pid="B"),
        ev("c1", EventType.CONTINUED_ACCELERATION_DURING_CONFLICT, 4.2, pid="C",
           subject="B"),
        ev("x1", EventType.COLLISION, 5.0, pid="C", subject="B"),
        ev("x2", EventType.COLLISION, 5.3, pid="B", subject="A"),
    ]
    graph = dag(events, [("b1", "x1"), ("c1", "x1"), ("x1", "x2")])
    result = build_responsibility_graph(events, physical_graph=graph)
    assert result["per_participant"]["B"]["outcomes"]["x2"]["reached"] is True
    # Involved, but nothing it did was observed to break a rule.
    assert "RESPONSIBILITY_CONTRIBUTION" not in node_types(result, "B")


def test_relevance_is_reported_per_outcome_not_pooled(case_d):
    events, graph = case_d
    result = build_responsibility_graph(events, physical_graph=graph)
    reached = result["per_participant"]["C"]["outcomes_reached"]
    assert reached == ["x1", "x2"]
    assert result["per_participant"]["B"]["outcomes_not_reached"] == ["x1", "x2"]


def test_the_vehicle_that_did_the_pushing_is(case_d):
    events, graph = case_d
    result = build_responsibility_graph(events, physical_graph=graph)
    assert result["per_participant"]["C"]["physically_relevant"] is True
    assert "RESPONSIBILITY_CONTRIBUTION" in node_types(result, "C")


def test_the_block_is_the_impact_received_not_the_participant():
    """B's own behaviour still counts for an outcome it reaches directly."""
    events = [
        ev("b1", EventType.HARD_BRAKE, 2.0, pid="B"),
        ev("x0", EventType.COLLISION, 3.0, pid="A", subject="B"),
        ev("b2", EventType.SOLID_LINE_CROSSED, 6.0, pid="B"),
        ev("x2", EventType.COLLISION, 7.0, pid="B", subject="C"),
    ]
    graph = dag(events, [("b1", "x0"), ("b2", "x2")])
    result = build_responsibility_graph(events, physical_graph=graph)
    # The later crossing reaches the later impact without passing an impact B
    # received, so B is a contributor there despite having been hit earlier.
    assert result["per_participant"]["B"]["physically_relevant"] is True


# --- CASE B / C: both stop, and the priority benchmark --------------------


def test_only_one_vehicle_faces_a_sign_so_the_other_has_priority():
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 5.0, pid="A"),
    ]
    result = benchmark_priority(events, participants=["A", "B"])
    assert result["verdict"] == "PRIORITY_TO_UNCONTROLLED"
    assert result["has_priority"] == "B"
    assert result["must_stop"] == ["A"]


def test_both_stop_and_a_clear_arrival_order_decides_it():
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
        ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
        ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
        ev("b2", EventType.FULL_STOP, 6.4, pid="B"),
    ]
    result = benchmark_priority(events, participants=["A", "B"])
    assert result["verdict"] == "PRIORITY_BY_ARRIVAL"
    assert result["has_priority"] == "A"
    assert result["arrival_gap_s"] == pytest.approx(1.4)


def test_a_near_simultaneous_arrival_stays_ambiguous():
    """0.1 s apart is not 'clearly first'. Refusing to break the tie is the result."""
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
        ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
        ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
        ev("b2", EventType.FULL_STOP, 5.1, pid="B"),
    ]
    result = benchmark_priority(events, participants=["A", "B"])
    assert result["verdict"] == "AMBIGUOUS_PRIORITY"
    assert result["has_priority"] is None
    assert "not a failure to compute one" in result["reason"]


def test_a_tie_break_applies_only_where_a_scenario_declares_one():
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
        ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
        ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
        ev("b2", EventType.FULL_STOP, 5.1, pid="B"),
    ]
    without = benchmark_priority(events, participants=["A", "B"])
    withit = benchmark_priority(events, participants=["A", "B"], tie_break="B")
    assert without["verdict"] == "AMBIGUOUS_PRIORITY"
    assert withit["verdict"] == "PRIORITY_BY_CONFIGURED_TIE_BREAK"
    assert withit["has_priority"] == "B"
    assert "local convention" in withit["reason"]


def test_a_vehicle_that_never_stopped_leaves_arrival_order_undefined():
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
        ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
        ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
    ]
    result = benchmark_priority(events, participants=["A", "B"])
    assert result["verdict"] == "AMBIGUOUS_PRIORITY"
    assert result["did_not_complete_a_stop"] == ["B"]
    # And it says which question this is *not* answering.
    assert "separate question" in result["reason"]


def test_no_observed_control_is_not_the_same_as_no_rule():
    result = benchmark_priority([], participants=["A", "B"])
    assert result["verdict"] == "NO_CONTROL_OBSERVED"
    assert "does not follow that no rule applied" in result["reason"]


def test_every_priority_verdict_is_documented_and_carries_the_rule():
    cases = [
        ([], ["A", "B"]),
        ([ev("a1", EventType.STOP_SIGN_DETECTED, 5.0, pid="A")], ["A", "B"]),
        ([ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
          ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
          ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
          ev("b2", EventType.FULL_STOP, 6.4, pid="B")], ["A", "B"]),
    ]
    for events, pids in cases:
        result = benchmark_priority(events, participants=pids)
        assert result["verdict"] in PRIORITY_VERDICTS
        assert result["benchmark_rule"] == BENCHMARK_RULE
        assert "not a statement of law" in result["benchmark_rule"]


def test_the_priority_verdict_reaches_the_graph():
    events = [ev("a1", EventType.STOP_SIGN_DETECTED, 5.0, pid="A")]
    priority = benchmark_priority(events, participants=["A", "B"])
    result = build_responsibility_graph(events, priority=priority)
    assert "PRIORITY_GRANTED" in node_types(result, "B")


def test_an_ambiguous_priority_is_recorded_as_ambiguous_in_the_graph():
    events = [
        ev("a1", EventType.STOP_SIGN_DETECTED, 4.0, pid="A"),
        ev("b1", EventType.STOP_SIGN_DETECTED, 4.2, pid="B"),
        ev("a2", EventType.FULL_STOP, 5.0, pid="A"),
        ev("b2", EventType.FULL_STOP, 5.1, pid="B"),
    ]
    priority = benchmark_priority(events, participants=["A", "B"])
    result = build_responsibility_graph(events, priority=priority)
    assert "PRIORITY_AMBIGUOUS" in node_types(result)


# --- CASE E: mitigating behaviour -----------------------------------------


def test_braking_at_a_threat_is_recorded_as_mitigating():
    events = [
        ev("a1", EventType.CRITICAL_TTC, 8.0, pid="A", subject="B"),
        ev("a2", EventType.HARD_BRAKE, 8.4, pid="A"),
    ]
    result = build_responsibility_graph(events)
    assert "MITIGATING_RESPONSE" in node_types(result, "A")


def test_braking_unprompted_by_any_threat_is_not():
    events = [ev("a2", EventType.HARD_BRAKE, 8.4, pid="A")]
    assert "MITIGATING_RESPONSE" not in node_types(build_responsibility_graph(events))


# --- the report: eight findings, no score ---------------------------------


def test_the_report_gives_every_finding_the_brief_asks_for(case_a):
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    finding = report["findings"]["A"]
    for key in (
        "physical_causal_contributor", "but_for_contribution",
        "traffic_control_violations", "temporal_property_failures",
        "non_action_evidence", "mitigating_actions",
        "prevention_opportunities", "responsibility_evidence",
    ):
        assert key in finding, key


def test_a_supported_finding_names_both_halves(case_a):
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    finding = report["findings"]["A"]
    assert finding["responsibility_evidence"] == "supported"
    assert finding["traffic_control_violations"]
    assert finding["physical_causal_contributor"] == "yes"


def test_an_untested_counterfactual_is_not_reported_as_a_negative(case_a):
    """No replay was run, so but-for is neither established nor ruled out."""
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    but_for = report["findings"]["A"]["but_for_contribution"]
    assert but_for["verdict"] == "not tested"
    assert "neither established nor ruled out" in but_for["reason"]


def test_a_counterfactual_result_is_used_when_there_is_one(case_a):
    events, graph = case_a
    attribution = {"contributions": [
        {"participant_id": "A", "establishes_causation": True,
         "rationale": "removing the crossing averted the collision in 6 of 6 replays"},
    ]}
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events,
        attribution=attribution,
    )
    assert report["findings"]["A"]["but_for_contribution"]["verdict"] == "yes"


def test_prevention_opportunities_are_kept_out_of_the_but_for_column(case_a):
    """Advancing a safety action prevents; it does not establish causation."""
    events, graph = case_a
    attribution = {"contributions": [
        {"participant_id": "A", "establishes_causation": False,
         "prevention_opportunities": [
             {"intervention": "advance A_brake by 0.5 s", "effect": "no collision"},
         ]},
    ]}
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events,
        attribution=attribution,
    )
    finding = report["findings"]["A"]
    assert finding["but_for_contribution"]["verdict"] == "no"
    assert len(finding["prevention_opportunities"]) == 1
    assert "not evidence of causing" in finding["prevention_opportunities"][0]["note"]


def test_non_action_evidence_carries_the_interval_it_was_watching(case_a):
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    evidence = report["findings"]["A"]["non_action_evidence"]
    assert evidence[0]["monitored_interval"] == [5.12, 5.88]
    assert evidence[0]["evidence_coverage"] == 1.0


def test_a_failing_temporal_property_reaches_the_report(case_a):
    events, graph = case_a
    formal = {"results": [{
        "property_id": "P1", "title": "stop before the line", "status": "FAIL",
        "benchmark_rule": "a stated benchmark",
        "instances": [{"status": "FAIL", "participant": "A", "t": 5.88}],
    }]}
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph, formal_results=formal),
        events, formal_results=formal,
    )
    failures = report["findings"]["A"]["temporal_property_failures"]
    assert failures and failures[0]["property_id"] == "P1"


def test_every_evidence_level_is_one_of_the_three(case_a):
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    for finding in report["findings"].values():
        assert finding["responsibility_evidence"] in EVIDENCE_LEVELS


# --- the vocabulary rule --------------------------------------------------


FORBIDDEN_WORDS = (
    "fault", "guilty", "guilt", "liability", "liable", "blame", "culprit",
)


def strings_in(value, path="$"):
    """Every string in a nested structure, with where it came from."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, sub in value.items():
            yield path + "." + str(key), str(key)
            for item in strings_in(sub, path + "." + str(key)):
                yield item
    elif isinstance(value, (list, tuple)):
        for i, sub in enumerate(value):
            for item in strings_in(sub, "{0}[{1}]".format(path, i)):
                yield item


def test_nothing_in_the_output_speaks_of_fault_or_liability(case_a, case_d):
    """The constraint that most shapes this layer, asserted over real output.

    Checked string by string rather than by counting over the whole blob: the
    only places these words may appear are the disclaimers that say what this
    layer is not, and a disclaimer always says so in the same string.
    """
    for events, graph in (case_a, case_d):
        rgraph = build_responsibility_graph(events, physical_graph=graph)
        report = build_responsibility_report(rgraph, events)
        for blob in (rgraph, report):
            for where, text in strings_in(blob):
                lowered = text.lower()
                for word in FORBIDDEN_WORDS:
                    if word not in lowered:
                        continue
                    assert ("not " in lowered or "never" in lowered
                            or "not_a_" in lowered), (where, word, text)


def test_no_share_or_percentage_is_ever_produced(case_a):
    events, graph = case_a
    report = build_responsibility_report(
        build_responsibility_graph(events, physical_graph=graph), events
    )
    assert "is a share or a percentage of anything" in json.dumps(report)
    for finding in report["findings"].values():
        assert not isinstance(finding["responsibility_evidence"], (int, float))
