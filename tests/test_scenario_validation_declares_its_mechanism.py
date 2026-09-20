"""Every V2 scenario has to state, in checks, the thing it claims to be about.

A scenario whose only declared check is "these two collided" passes on a run in
which the right cars touched for the wrong reasons, and that is precisely the
failure this set of scenarios spent its development on: a stop that happened
after the stop line, a push delivered by the pushed vehicle's own throttle, a
deflection that was an unconditional timed lane change, a second impact that
happened whether or not the first one did.

So the claim each variant makes is written into its ``validation:`` block, and
this test says which claim goes with which variant. It is deliberately a test of
the *configuration* rather than of a recording: it needs no simulator, it runs in
the ordinary suite, and it fails the moment somebody quietly drops a check to
make a run go green.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from cdf.common.config import Config, deep_merge, load_yaml
from cdf.simulation.scenario_base import ScenarioSpec

REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = REPO_ROOT / "configs" / "scenarios"

#: ``(scenario file, variant) -> the checks that variant's claim requires``.
#: Each entry is a sentence about physics turned into a key.
REQUIRED = {
    # A stop-sign scenario claims the vehicle stopped *before the line*, and
    # that the collision happened inside the junction rather than on approach.
    ("s10_single_stop_a.yaml", "*"): ["collision_near", "no_scenery_collision",
                                      "max_accumulated_turn_deg"],
    ("s11_single_stop_b.yaml", "*"): ["collision_near", "no_scenery_collision",
                                      "max_accumulated_turn_deg"],
    ("s12_all_way_stop.yaml", "*"): ["stop_point", "collision_near",
                                     "no_scenery_collision",
                                     "max_accumulated_turn_deg",
                                     "min_straightness"],
    # A lane-change scenario claims a lane change, which is a distance.
    ("s13_disputed_lane_change.yaml", "*"): ["min_lateral_displacement_m",
                                             "no_scenery_collision"],
    # The pushed vehicle claims it was pushed: no throttle of its own, and the
    # two impacts close enough together to be one event.
    ("s14_three_car_chain.yaml", "c_pushes_b"): ["coasting_after_impact",
                                                 "impact_interval_s"],
    # The deflection claims the same, across a junction.
    ("s15_intersection_pileup.yaml", "deflected_into_c"): ["coasting_after_impact",
                                                           "impact_interval_s",
                                                           "collision_near"],
    ("s15_intersection_pileup.yaml", "single_impact"): ["forbidden_collision_pairs"],
    # S16 is the pair of claims stated side by side, so each variant has to
    # carry the half that separates it from the other.
    ("s16_secondary_collision.yaml", "consequential"): ["coasting_after_impact",
                                                        "impact_interval_s",
                                                        "lateral_begins_at_impact"],
    ("s16_secondary_collision.yaml", "independent"): ["self_driven_between_impacts",
                                                      "impact_interval_s",
                                                      "min_lateral_displacement_m"],
    ("s16_secondary_collision.yaml", "avoided"): ["forbidden_collision_pairs"],
}

V2_FILES = sorted({name for name, _ in REQUIRED})


def _variants(name: str):
    block = load_yaml(str(SCENARIO_DIR / name))["scenario"]
    return list((block.get("variants") or {}).keys()) or ["default"]


def _spec(name: str, variant: str) -> ScenarioSpec:
    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    cfg = Config(deep_merge(base, load_yaml(str(SCENARIO_DIR / name))))
    return ScenarioSpec.from_config(cfg, variant=variant)


def _cases():
    for (name, variant), keys in sorted(REQUIRED.items()):
        wanted = _variants(name) if variant == "*" else [variant]
        for v in wanted:
            yield name, v, keys


@pytest.mark.parametrize("name,variant,keys", list(_cases()))
def test_the_variant_declares_the_checks_its_claim_needs(name, variant, keys):
    validation = _spec(name, variant).validation
    missing = [k for k in keys if k not in validation]
    assert missing == [], (
        "{0}/{1} no longer declares {2}. That check is what distinguishes this "
        "variant from a run where the right cars collided for the wrong "
        "reasons; restore it or explain in this table why the claim changed"
        .format(name, variant, missing)
    )


@pytest.mark.parametrize("name", V2_FILES)
def test_every_v2_variant_forbids_driving_into_the_scenery(name):
    """A vehicle that leaves the road has stopped performing the scenario.

    Unintended scenery collisions were how route exhaustion showed itself:
    a vehicle that outran its route chased a point behind itself, circled,
    and ended up in a guardrail. Nothing about that is the encounter, and a
    run containing one is not evidence of anything.
    """
    for variant in _variants(name):
        validation = _spec(name, variant).validation
        assert validation.get("no_scenery_collision") is True, (name, variant)


#: Scenarios whose encounter is a junction conflict. "They collided" is not the
#: claim; "they collided *in the junction*" is, and an impact on the approach
#: means one of them never got there.
JUNCTION_SCENARIOS = ("s10_single_stop_a.yaml", "s11_single_stop_b.yaml",
                      "s12_all_way_stop.yaml", "s15_intersection_pileup.yaml")


@pytest.mark.parametrize("name", JUNCTION_SCENARIOS)
def test_a_junction_scenario_requires_the_impact_inside_the_junction(name):
    for variant in _variants(name):
        near = _spec(name, variant).validation.get("collision_near") or {}
        if not near:
            continue
        assert near.get("require_in_junction") is True, (name, variant)


def test_s12_requires_both_vehicles_to_stop_outside_the_junction():
    """The scenario is about stopping *before* the line, not about stopping.

    A vehicle that brakes to rest inside the junction has obeyed nothing, and
    an earlier version of S12 did exactly that on every variant while passing
    a check that only asked whether it had stopped.
    """
    name = "s12_all_way_stop.yaml"
    for variant in _variants(name):
        stops = _spec(name, variant).validation.get("stop_point") or {}
        named = {pid: want for pid, want in stops.items() if want}
        assert named, (name, variant, "no stop point is checked at all")
        for pid, want in named.items():
            assert want.get("must_be_outside_junction", True) is True, (
                name, variant, pid)


@pytest.mark.parametrize("name", V2_FILES)
def test_every_v2_variant_bounds_how_far_a_vehicle_may_turn(name):
    """The number that catches circling, which no collision check would."""
    for variant in _variants(name):
        validation = _spec(name, variant).validation
        cap = validation.get("max_accumulated_turn_deg")
        assert cap is not None and float(cap) > 0.0, (name, variant)
