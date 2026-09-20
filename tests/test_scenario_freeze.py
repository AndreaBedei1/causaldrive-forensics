"""S01-S09 are frozen. The V2 scenarios are new files, and may not edit them.

S01-S09 were checked and corrected by hand. Every method improvement has to be a
change to the *method*; calibrating a scenario until an attribution comes out
right would be the opposite of an experiment. The SHA-256 of each YAML is pinned
here and the suite fails the moment one changes. Updating a hash is a deliberate
act with a written reason, never a side effect of making a metric move.

What this test does *not* forbid any more is adding scenarios. V2 introduces
S10-S16 -- single stop, all-way stop, disputed lane change, three-car chain,
intersection pile-up, secondary collision -- and they are additions rather than
edits. The distinction is the one that matters: a new scenario cannot make an old
result look better, because the old results are computed from the old scenarios
and those are byte-identical. A retuned scenario could, which is why the hashes
stay.

An earlier, unrelated scenario also numbered S10 was removed from this repository
for a different reason. The V2 S10 is a fresh single-stop scenario and shares
nothing with it but the number.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_DIR = REPO_ROOT / "configs" / "scenarios"

#: Frozen at the start of the final campaign. See the module docstring before
#: touching a line of this table.
FROZEN_SHA256 = {
    "s01_rear_end.yaml": "4ec797d5633eefacc8692f12ef48083b06281f3edf4e42bfcedcd727ddfad8cb",
    "s02_cut_in.yaml": "532ab3db8cfa64e7fb80e5a5265d14138be4d20d202454ce67e13ff20035fc7b",
    "s03_crossing.yaml": "3e2bb6af4a8db008645a02b1bbee364d051adb44f44ae48f5f55a0e84b933a7c",
    "s04_crossing_braking.yaml": "30990ec11aecc98cae44a25b11698f08889df89fcfc703b16ee9476ce40e8f02",
    "s05_simultaneous_crossing.yaml": "09bfc681e50ccd9a97c9571895aeec6bc4d59b57bdc7ff1296d3d3d9cdf05622",
    "s06_chain_collision.yaml": "64b17a7195992243fa21402cfddc70ceb667fee1d1954a76c591590440e071ce",
    "s07_partial_view.yaml": "ce1f7a553308473d935a5acd6700c2c631023d305e3875ffbefe2b8f7b1fcfa2",
    "s08_multidirection_crossing.yaml": "87c27cd08537ba10a1eed26d943894f024e2403d3d8f92babf16a98ec8ab9152",
    "s09_roundabout.yaml": "2f003c60d0b162b9e2f56be53c10cc8fdff26417b1992137ab6f86022f98d6ab",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with open(str(path), "rb") as handle:
        for block in iter(lambda: handle.read(1 << 16), b""):
            digest.update(block)
    return digest.hexdigest()


@pytest.mark.parametrize("name", sorted(FROZEN_SHA256))
def test_scenario_yaml_is_unchanged(name: str) -> None:
    path = SCENARIO_DIR / name
    assert path.is_file(), "frozen scenario {0} is missing".format(name)
    actual = _sha256(path)
    assert actual == FROZEN_SHA256[name], (
        "{0} changed (sha256 {1} != frozen {2}). Scenarios are frozen: improve "
        "the method, not the scenario.".format(name, actual, FROZEN_SHA256[name])
    )


#: The V2 additions. Listed so that adding a scenario is as deliberate as
#: changing one: a file here that nobody expected fails the test.
V2_SCENARIOS = {
    "s10_single_stop_a.yaml",
    "s11_single_stop_b.yaml",
    "s12_all_way_stop.yaml",
    "s13_disputed_lane_change.yaml",
    "s14_three_car_chain.yaml",
    "s15_intersection_pileup.yaml",
    "s16_secondary_collision.yaml",
}


def test_none_of_the_frozen_nine_went_missing() -> None:
    present = {p.name for p in SCENARIO_DIR.glob("*.yaml")}
    assert set(FROZEN_SHA256).issubset(present), sorted(
        set(FROZEN_SHA256) - present
    )


def test_the_scenario_set_is_exactly_the_nine_plus_the_declared_additions() -> None:
    """No scenario appears that nobody wrote down here."""
    present = {p.name for p in SCENARIO_DIR.glob("*.yaml")}
    unexpected = sorted(present - set(FROZEN_SHA256) - V2_SCENARIOS)
    assert unexpected == [], (
        "undeclared scenario file(s) {0}. Adding a scenario is deliberate: list "
        "it in V2_SCENARIOS with the reason it exists".format(unexpected)
    )


def test_every_declared_v2_scenario_is_present_and_loads() -> None:
    """A declared scenario that does not exist, or does not parse, is a bug."""
    from cdf.common.config import Config, deep_merge, load_yaml
    from cdf.simulation.scenario_base import ScenarioSpec

    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    for name in sorted(V2_SCENARIOS):
        path = SCENARIO_DIR / name
        assert path.is_file(), name
        block = load_yaml(str(path))["scenario"]
        variants = list((block.get("variants") or {}).keys()) or ["default"]
        for variant in variants:
            cfg = Config(deep_merge(base, load_yaml(str(path))))
            spec = ScenarioSpec.from_config(cfg, variant=variant)
            assert spec.participants, (name, variant)


def test_the_v2_scenarios_use_two_or_three_vehicles() -> None:
    """The brief caps it there, and the alignment story is built around it."""
    from cdf.common.config import Config, deep_merge, load_yaml
    from cdf.simulation.scenario_base import ScenarioSpec

    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    for name in sorted(V2_SCENARIOS):
        cfg = Config(deep_merge(base, load_yaml(str(SCENARIO_DIR / name))))
        spec = ScenarioSpec.from_config(cfg)
        assert 2 <= len(spec.participants) <= 3, (name, len(spec.participants))


def test_no_v2_causal_template_references_an_uncomparable_state() -> None:
    """A designed edge nothing could match measures the vocabulary, not the method.

    This is the check that keeps the new scenarios honest about what they are
    asking of a reconstruction: every state a template names has to map onto an
    event type both a privileged trace and an onboard reconstruction can assert.
    """
    from cdf.common.config import Config, deep_merge, load_yaml
    from cdf.graph.ontology import is_comparable
    from cdf.oracle.events import STATE_EVENT_TYPES
    from cdf.simulation.scenario_base import ScenarioSpec

    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    for name in sorted(V2_SCENARIOS):
        block = load_yaml(str(SCENARIO_DIR / name))["scenario"]
        variants = list((block.get("variants") or {}).keys()) or ["default"]
        for variant in variants:
            cfg = Config(deep_merge(base, load_yaml(str(SCENARIO_DIR / name))))
            spec = ScenarioSpec.from_config(cfg, variant=variant)
            for edge in spec.causal_template:
                for side in ("cause", "effect"):
                    node = edge.get(side) or {}
                    if node.get("kind") != "state":
                        continue
                    state = str(node.get("name"))
                    assert state in STATE_EVENT_TYPES, (name, variant, state)
                    assert is_comparable(STATE_EVENT_TYPES[state]), (name, state)


#: The final benchmark, counted from the configuration rather than asserted.
#: Written down here so that gaining or losing a variant is a deliberate act
#: with a reason, the same way changing a frozen scenario is: every published
#: figure is an average over exactly this set, and a set that drifts silently
#: makes two documents that quote different campaigns look like one.
FINAL_SCENARIOS = 16
FINAL_VARIANTS = 34
FINAL_SEEDS = 3


def test_the_benchmark_is_the_size_the_documentation_says_it_is() -> None:
    from cdf.cli import suite_combinations
    from cdf.common.config import available_scenarios

    combinations = suite_combinations(available_scenarios())
    scenarios = {scenario for scenario, _variant in combinations}

    assert len(scenarios) == FINAL_SCENARIOS, sorted(scenarios)
    assert len(combinations) == FINAL_VARIANTS, sorted(combinations)
    assert len(combinations) * FINAL_SEEDS == 102


def test_s14_has_not_regained_the_variant_that_faked_its_second_impact() -> None:
    """It produced that impact by having a stopped car creep into a wreck.

    The distinction it was testing -- that two impacts sharing a vehicle must
    not be chained merely for sharing it -- is what S16 tests between its
    consequential and independent variants, on a road situation rather than on
    a driver deliberately driving into stationary wreckage.
    """
    from cdf.cli import suite_combinations

    variants = {v for s, v in suite_combinations(["S14"])}
    assert variants == {"c_pushes_b", "b_hits_a_first"}, sorted(variants)


def test_no_v2_scenario_declares_an_unimplemented_sign_kind() -> None:
    """Only stop and give-way are detected, so only those may be placed."""
    from cdf.common.config import Config, deep_merge, load_yaml
    from cdf.simulation.scenario_base import ScenarioSpec

    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    for name in sorted(V2_SCENARIOS):
        cfg = Config(deep_merge(base, load_yaml(str(SCENARIO_DIR / name))))
        spec = ScenarioSpec.from_config(cfg)
        for sign in (spec.traffic_control or {}).get("signs", []) or []:
            assert str(sign["kind"]).lower() in ("stop", "yield"), (name, sign)
