"""A variant that declares a collision has to have produced one.

`scenario_validation.json` asks whether the declared pair touched. Touching is
not colliding: `S13/accelerates_into_gap` passed that check on two seeds with
contacts of 17.7 and 98.0 N.s, which is one car's corner brushing another's as
it goes past, and failed outright on the third. Two of three "successes" were a
scrape, and nothing in the suite said so.

So the campaign itself is checked here, from the privileged record, for the
things a per-run validation either cannot see or was not asked: that a declared
collision was a collision, that the pairs and their order match what the variant
declares, and that nobody drove into the scenery. These are properties of the
recorded evidence, so they are re-checkable at any time without a simulator --
which is the point, because the validation written at record time is frozen in
the file and the rules may need to get stricter after it.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

import pytest

from cdf.common.config import Config, deep_merge, load_yaml
from cdf.simulation.scenario_base import ScenarioSpec

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = REPO_ROOT / "artifacts_v2"
SCENARIO_DIR = REPO_ROOT / "configs" / "scenarios"

#: Below this a participant-pair contact is a scrape, not a collision. The
#: benchmark's real impacts run from about 2900 N.s upwards; the contacts this
#: floor exists to catch measured 17.7 and 98.0. Anything between is a judgement
#: call nobody has had to make yet, and 500 sits in that empty band.
MIN_COLLISION_IMPULSE_NS = 500.0


def _runs() -> Iterator[Tuple[Path, Dict[str, Any]]]:
    for manifest_path in sorted(ARTIFACTS.glob("*/*/manifest.json")):
        if "counterfactual" in manifest_path.parts or "ablation" in manifest_path.parts:
            continue
        with open(str(manifest_path), encoding="utf-8") as handle:
            yield manifest_path.parent, json.load(handle)


pytestmark = pytest.mark.skipif(
    not any(ARTIFACTS.glob("*/*/manifest.json")),
    reason="no recorded campaign under artifacts_v2/",
)


def _spec(scenario_id: str, variant: str) -> ScenarioSpec:
    matches = sorted(SCENARIO_DIR.glob("{0}_*.yaml".format(scenario_id.lower())))
    assert matches, scenario_id
    base = load_yaml(str(REPO_ROOT / "configs" / "default.yaml"))
    cfg = Config(deep_merge(base, load_yaml(str(matches[0]))))
    return ScenarioSpec.from_config(cfg, variant=variant)


def _first_contacts(run_dir: Path) -> Dict[Tuple[str, str], Tuple[float, float]]:
    """Each participant pair's first contact: ``(t, impulse)``."""
    summary_path = run_dir / "oracle" / "oracle_summary.json"
    if not summary_path.is_file():
        return {}
    with open(str(summary_path), encoding="utf-8") as handle:
        summary = json.load(handle)
    first: Dict[Tuple[str, str], Tuple[float, float]] = {}
    rows = [c for c in summary.get("collisions", []) if c.get("is_participant_pair")]
    for contact in sorted(rows, key=lambda c: float(c["t"])):
        key = tuple(sorted([str(contact["participant_id"]),
                            str(contact["other_participant_id"])]))
        if key not in first:
            first[key] = (float(contact["t"]), float(contact.get("impulse") or 0.0))
    return first


CASES = [
    (run_dir, manifest) for run_dir, manifest in _runs()
] if ARTIFACTS.is_dir() else []
IDS = ["{0}/{1}".format(m.get("scenario_id"), run_dir.name) for run_dir, m in CASES]


@pytest.mark.parametrize("run_dir,manifest", CASES, ids=IDS)
def test_a_declared_collision_was_a_collision(run_dir: Path, manifest: Dict[str, Any]) -> None:
    spec = _spec(str(manifest["scenario_id"]), str(manifest["variant"]))
    if spec.expected_outcome != "collision":
        pytest.skip("this variant declares no collision")
    contacts = _first_contacts(run_dir)
    weak = {
        "{0}-{1}".format(*pair): round(impulse, 1)
        for pair, (_t, impulse) in sorted(contacts.items())
        if impulse < MIN_COLLISION_IMPULSE_NS
    }
    assert contacts, "{0} declares a collision and recorded no contact".format(run_dir)
    assert not weak, (
        "{0}: contact(s) {1} are below {2:.0f} N.s. A variant that declares a "
        "collision and produces a scrape has not staged its encounter, and "
        "passing on the strength of two bumpers touching is how "
        "S13/accelerates_into_gap went unnoticed"
        .format(run_dir, weak, MIN_COLLISION_IMPULSE_NS)
    )


@pytest.mark.parametrize("run_dir,manifest", CASES, ids=IDS)
def test_the_pairs_that_collided_are_the_pairs_the_variant_declares(
    run_dir: Path, manifest: Dict[str, Any]
) -> None:
    spec = _spec(str(manifest["scenario_id"]), str(manifest["variant"]))
    observed = {
        pair for pair, (_t, impulse) in _first_contacts(run_dir).items()
        if impulse >= MIN_COLLISION_IMPULSE_NS
    }
    declared = {tuple(sorted(p)) for p in spec.expected_collision_pairs}
    assert declared.issubset(observed) or spec.expected_outcome != "collision", (
        "{0}: declared {1}, observed {2}".format(run_dir, sorted(declared), sorted(observed))
    )
    unexpected = sorted(observed - declared)
    assert not unexpected, (
        "{0}: {1} collided and the variant does not declare it"
        .format(run_dir, unexpected)
    )


#: Scenery contacts that are known, understood, and cannot be removed.
#:
#: S04 is hash-frozen, so its routes cannot be lengthened. Both vehicles drive
#: on past the junction and reach the end of the road: A at about t=12.8 and B
#: at about t=20.6, against an encounter that closed at 7.97 m at t=5.6. The
#: contact is after the measurement rather than in it, and the guard below only
#: honours this entry while that remains true -- a scenery contact that moved
#: into the encounter would fail here whatever this table says.
ALLOWED_SCENERY = {
    ("S04", "yield"): "frozen scenario; both vehicles run off the end of the road "
                      "long after the encounter they are recorded for",
}


def _encounter_time(run_dir: Path, summary: Dict[str, Any]) -> float:
    """When the thing being measured happened: the first impact, or the closest approach."""
    impacts = [float(c["t"]) for c in summary.get("collisions", [])
               if c.get("is_participant_pair")]
    if impacts:
        return min(impacts)
    validation_path = run_dir / "scenario_validation.json"
    if validation_path.is_file():
        with open(str(validation_path), encoding="utf-8") as handle:
            separation = (json.load(handle).get("checks") or {}).get("min_separation")
        if separation and separation.get("t") is not None:
            return float(separation["t"])
    return 0.0


@pytest.mark.parametrize("run_dir,manifest", CASES, ids=IDS)
def test_nobody_drove_into_the_scenery(run_dir: Path, manifest: Dict[str, Any]) -> None:
    """The signature of a vehicle that outran its route and started circling."""
    summary_path = run_dir / "oracle" / "oracle_summary.json"
    if not summary_path.is_file():
        pytest.skip("no oracle summary")
    with open(str(summary_path), encoding="utf-8") as handle:
        summary = json.load(handle)
    contacts = [c for c in summary.get("collisions", [])
                if not c.get("is_participant_pair")]
    if not contacts:
        return

    key = (str(manifest.get("scenario_id")), str(manifest.get("variant")))
    encounter_t = _encounter_time(run_dir, summary)
    allowed = key in ALLOWED_SCENERY

    offending = [
        "{0} hit {1} at t={2:.2f}".format(
            c.get("participant_id"), c.get("other_type_id") or "the world", float(c["t"])
        )
        for c in contacts
        if not (allowed and float(c["t"]) > encounter_t + 1.0)
    ]
    assert not offending, "{0}: {1}{2}".format(
        run_dir, offending,
        "" if not allowed else
        " -- allowed only after the encounter at t={0:.2f}".format(encounter_t),
    )


def test_the_campaign_is_actually_being_checked() -> None:
    """A glob that matched nothing would make every case above vacuous."""
    assert len(CASES) >= 39, len(CASES)
