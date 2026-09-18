"""Omission repair: the counterfactual for something that did not happen.

Every other intervention edits a behaviour the vehicle performed. The most
interesting causal question about a stop-sign violation is about one it did not,
and there is no factual action to weaken -- so the replay has to supply the stop.

The whole risk of adding that capability is in one place: inserting safe
behaviour into a run and calling the avoided collision "causation". Do that
without care and every vehicle caused every collision it could have prevented,
which is the same error the advance/but-for fix already guards against, arriving
by a different route. These tests exist to keep the two apart.
"""

from __future__ import annotations

import pytest

from cdf.causal.attribution import establishes_but_for
from cdf.causal.counterfactuals import CounterfactualOutcome
from cdf.causal.interventions import (
    COUNTERFACTUAL_ROLES,
    INSERTABLE_KINDS,
    RUNNER_OPS,
    InterventionSpec,
    omission_repairs,
)
from cdf.common.config import Config
from cdf.common.schemas import (
    CausalEdgeType, Event, EventType, GraphDocument, GraphEdge, Provenance,
)
from cdf.simulation.scenario_base import ParticipantSpec, ScenarioSpec


def insertion(intervention_id="x", action_id="A_repair", participant="A",
              kind="stop", t_start=4.2, duration=2.5, repairs="") -> InterventionSpec:
    return InterventionSpec(
        intervention_id=intervention_id,
        action_id=action_id,
        op="insert_action",
        params={"participant": participant, "kind": kind,
                "t_start": t_start, "duration": duration, "params": {}},
        targets_participant=participant,
        repairs_non_action=repairs,
    )


def non_action(event_id, event_type, pid, t0, t1, confidence=1.0) -> Event:
    return Event(
        event_id=event_id, event_type=event_type, participant_id=pid,
        t_start=t0, t_peak=t1, t_end=t1, confidence=confidence,
        detail={"rule_id": "NA1", "monitored_interval": [t0, t1],
                "evidence_coverage": confidence},
        provenance=Provenance.FUSED,
    )


def graph(nodes) -> GraphDocument:
    return GraphDocument(
        graph_kind="causal", scope=Provenance.FUSED, run_id="t",
        scenario_id="S10", seed=0, nodes=list(nodes), edges=[],
    )


def scenario(participants=("A", "B")) -> ScenarioSpec:
    return ScenarioSpec(
        scenario_id="S10", name="single_stop_a",
        participants=[
            ParticipantSpec(participant_id=p, blueprint="vehicle.tesla.model3")
            for p in participants
        ],
    )


# --- the op exists and is validated ---------------------------------------


def test_insert_action_is_an_operation_the_runner_understands():
    assert "insert_action" in RUNNER_OPS


def test_an_inserted_action_must_be_of_a_kind_a_controller_executes():
    """The worst failure mode: the controller ignores it and the replay looks
    like a counterfactual that changed nothing -- indistinguishable from a real
    finding that the behaviour would not have helped."""
    with pytest.raises(ValueError, match="no controller executes"):
        insertion(kind="teleport")


def test_every_declared_insertable_kind_is_accepted():
    for kind in INSERTABLE_KINDS:
        assert insertion(kind=kind).params["kind"] == kind


def test_an_insertion_must_name_a_participant():
    with pytest.raises(ValueError, match="no participant"):
        insertion(participant="")


def test_an_insertion_of_zero_duration_is_rejected():
    with pytest.raises(ValueError, match="zero duration"):
        insertion(duration=0.0)


def test_an_insertion_cannot_start_before_the_run():
    with pytest.raises(ValueError, match="negative"):
        insertion(t_start=-1.0)


def test_an_insertion_needs_its_timing_parameters():
    with pytest.raises(ValueError, match="missing required parameter"):
        InterventionSpec("x", "A_repair", "insert_action",
                         {"participant": "A", "kind": "stop"})


# --- the role, which is what keeps the two cases apart --------------------


def test_an_insertion_that_repairs_an_omission_is_an_omission_repair():
    assert insertion(repairs="na-NA1-A-5.12").counterfactual_role == "omission_repair"


def test_an_insertion_that_repairs_nothing_is_a_prevention_opportunity():
    """Adding a brake for a vehicle under no obligation to brake asks whether
    someone could have avoided this, not whether an omission mattered."""
    assert insertion().counterfactual_role == "prevention_opportunity"


def test_advancing_a_safety_action_is_still_a_prevention_opportunity():
    spec = InterventionSpec("x", "A_brake", "advance", {"seconds": 0.5})
    assert spec.counterfactual_role == "prevention_opportunity"


def test_removing_a_factual_action_is_a_factual_removal():
    assert InterventionSpec("x", "A_brake", "disable").counterfactual_role == (
        "factual_removal"
    )


def test_scaling_an_action_up_is_a_prevention_opportunity_not_a_removal():
    up = InterventionSpec("x", "A_brake", "scale", {"param": "intensity", "factor": 1.5})
    down = InterventionSpec("y", "A_brake", "scale", {"param": "intensity", "factor": 0.4})
    assert up.counterfactual_role == "prevention_opportunity"
    assert down.counterfactual_role == "factual_removal"


def test_every_role_produced_is_one_of_the_documented_ones():
    specs = [
        insertion(repairs="na-1"), insertion(),
        InterventionSpec("a", "x", "advance", {"seconds": 1.0}),
        InterventionSpec("b", "x", "disable"),
        InterventionSpec("c", "x", "delay", {"seconds": 1.0}),
        InterventionSpec("d", "x", "set", {"param": "p", "value": 1.0}),
    ]
    for spec in specs:
        assert spec.counterfactual_role in COUNTERFACTUAL_ROLES


def test_the_role_travels_into_the_manifest():
    record = insertion(repairs="na-NA1-A-5.12").to_dict()
    assert record["counterfactual_role"] == "omission_repair"
    assert record["repairs_non_action"] == "na-NA1-A-5.12"


# --- what may establish but-for causation ---------------------------------


def test_a_supported_omission_repair_may_establish_causation():
    cf = CounterfactualOutcome("r", op="insert_action",
                               repairs_non_action="na-NA1-A-5.12")
    assert establishes_but_for(cf) is True


def test_inserting_safe_behaviour_that_repairs_nothing_may_not():
    """Otherwise every vehicle caused every collision it could have prevented."""
    assert establishes_but_for(
        CounterfactualOutcome("e", op="insert_action")
    ) is False


def test_the_existing_advance_rule_is_unchanged():
    assert establishes_but_for(CounterfactualOutcome("a", op="advance")) is False
    assert establishes_but_for(CounterfactualOutcome("d", op="disable")) is True
    assert establishes_but_for(CounterfactualOutcome("l", op="delay")) is True


def test_scaling_down_still_establishes_and_scaling_up_still_does_not():
    down = CounterfactualOutcome("d", op="scale", params={"factor": 0.4})
    up = CounterfactualOutcome("u", op="scale", params={"factor": 1.6})
    assert establishes_but_for(down) is True
    assert establishes_but_for(up) is False


# --- proposing repairs from the reconstruction, not from the scenario -----


def test_a_supported_non_action_produces_a_repair():
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88)]
    repairs = omission_repairs(scenario(), graph(nodes))
    assert len(repairs) == 1
    repair = repairs[0]
    assert repair.op == "insert_action"
    assert repair.params["participant"] == "A"
    assert repair.params["kind"] == "stop"
    assert repair.repairs_non_action == "na-1"
    assert repair.counterfactual_role == "omission_repair"


def test_the_repair_starts_before_the_obligation_came_due():
    """A stop performed at the instant the window opened is already too late to
    be the stop that was required."""
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88)]
    repair = omission_repairs(scenario(), graph(nodes))[0]
    assert repair.params["t_start"] < 5.12
    assert repair.params["t_start"] >= 0.0


def test_a_repair_never_starts_before_the_run():
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 0.1, 0.5)]
    repair = omission_repairs(scenario(), graph(nodes))[0]
    assert repair.params["t_start"] == 0.0


def test_a_missing_braking_response_is_repaired_with_braking_not_a_stop():
    nodes = [non_action("na-1", EventType.NO_BRAKING_RESPONSE, "A", 8.42, 9.92)]
    repair = omission_repairs(scenario(), graph(nodes))[0]
    assert repair.params["kind"] == "brake"
    assert repair.params["params"]["intensity"] > 0.0


def test_a_weakly_supported_non_action_is_not_repaired():
    """Repairing an omission the evidence only half supports would attribute
    causation to a claim that was itself hedged."""
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88,
                        confidence=0.55)]
    assert omission_repairs(scenario(), graph(nodes)) == []


def test_the_confidence_bar_is_configurable():
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88,
                        confidence=0.55)]
    lenient = Config({"counterfactual": {"omission_repair": {"min_confidence": 0.5}}})
    assert len(omission_repairs(scenario(), graph(nodes), cfg=lenient)) == 1


def test_an_ordinary_event_produces_no_repair():
    nodes = [Event(event_id="e1", event_type=EventType.HARD_BRAKE,
                   participant_id="A", t_start=4.0, t_peak=4.1, t_end=4.2)]
    assert omission_repairs(scenario(), graph(nodes)) == []


def test_a_non_action_for_a_vehicle_not_in_the_scenario_is_skipped():
    nodes = [non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "Z", 5.12, 5.88)]
    assert omission_repairs(scenario(), graph(nodes)) == []


def test_without_a_reconstruction_nothing_is_proposed():
    """Repairs come off the graph, never off the scenario: proposing them from
    the scenario definition would be testing the experiment's intent."""
    assert omission_repairs(scenario(), None) == []


def test_the_same_omission_is_not_repaired_twice():
    nodes = [
        non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88),
        non_action("na-2", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88),
    ]
    assert len(omission_repairs(scenario(), graph(nodes))) == 1


def test_two_vehicles_each_get_their_own_repair():
    nodes = [
        non_action("na-1", EventType.NO_STOP_AFTER_STOP_SIGN, "A", 5.12, 5.88),
        non_action("na-2", EventType.NO_STOP_AFTER_STOP_SIGN, "B", 6.10, 6.80),
    ]
    repairs = omission_repairs(scenario(), graph(nodes))
    assert sorted(r.targets_participant for r in repairs) == ["A", "B"]


def test_no_repair_rule_mentions_a_scenario():
    """Seven scenario-specific operations would have been easier to write and
    impossible to defend."""
    import inspect

    from cdf.causal import interventions

    source = inspect.getsource(interventions)
    for token in ("S10", "S11", "S12", "S13", "S14", "S15", "S16"):
        assert 'scenario_id == "{0}"'.format(token) not in source
        assert "== '{0}'".format(token) not in source


# --- the runner applies it -------------------------------------------------


def test_the_runner_inserts_the_action_into_the_participant_schedule():
    from cdf.simulation.runner import _apply_intervention

    spec = scenario()
    out = _apply_intervention(spec, {
        "intervention_id": "x", "action_id": "A_repair", "op": "insert_action",
        "participant": "A", "kind": "stop", "t_start": 4.5, "duration": 2.5,
        "params": {},
    })
    actions = {a.action_id: a for p in out.participants for a in p.actions}
    assert "A_repair" in actions
    assert actions["A_repair"].kind == "stop"
    assert actions["A_repair"].t_start == pytest.approx(4.5)
    assert actions["A_repair"].enabled is True


def test_the_factual_spec_is_not_mutated():
    from cdf.simulation.runner import _apply_intervention

    spec = scenario()
    _apply_intervention(spec, {
        "intervention_id": "x", "action_id": "A_repair", "op": "insert_action",
        "participant": "A", "kind": "stop", "t_start": 4.5, "duration": 2.5,
    })
    assert [a.action_id for p in spec.participants for a in p.actions] == []


def test_inserting_for_an_unknown_participant_fails_loudly():
    from cdf.simulation.runner import _apply_intervention

    with pytest.raises(KeyError, match="unknown participant"):
        _apply_intervention(scenario(), {
            "intervention_id": "x", "action_id": "Z_repair", "op": "insert_action",
            "participant": "Z", "kind": "stop", "t_start": 4.5, "duration": 2.5,
        })


def test_an_inserted_action_may_not_reuse_a_declared_id():
    """Otherwise the attribution cannot say which action it measured."""
    from cdf.simulation.controllers import ScriptedAction
    from cdf.simulation.runner import _apply_intervention

    spec = scenario()
    spec.participants[0].actions.append(
        ScriptedAction(action_id="A_brake", kind="brake", t_start=3.0, duration=2.0)
    )
    with pytest.raises(ValueError, match="already declares"):
        _apply_intervention(spec, {
            "intervention_id": "x", "action_id": "A_brake", "op": "insert_action",
            "participant": "A", "kind": "stop", "t_start": 4.5, "duration": 2.5,
        })


def test_the_schedule_stays_sorted_so_an_inserted_action_interleaves():
    from cdf.simulation.controllers import ScriptedAction
    from cdf.simulation.runner import _apply_intervention

    spec = scenario()
    spec.participants[0].actions.append(
        ScriptedAction(action_id="A_late", kind="brake", t_start=8.0, duration=2.0)
    )
    out = _apply_intervention(spec, {
        "intervention_id": "x", "action_id": "A_repair", "op": "insert_action",
        "participant": "A", "kind": "stop", "t_start": 4.5, "duration": 2.5,
    })
    order = [a.action_id for a in out.participants[0].actions]
    assert order == ["A_repair", "A_late"]


def test_the_replay_variant_names_the_intervention():
    from cdf.simulation.runner import _apply_intervention

    out = _apply_intervention(scenario(), {
        "intervention_id": "A_repair__omission_repair", "action_id": "A_repair",
        "op": "insert_action", "participant": "A", "kind": "stop",
        "t_start": 4.5, "duration": 2.5,
    })
    assert "omission_repair" in out.variant
