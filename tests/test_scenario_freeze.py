"""The nine scenario specifications are frozen.

S01-S09 were checked and corrected by hand. Every method improvement in this
project has to be a change to the *method*; calibrating a scenario until an
attribution comes out right would be the opposite of an experiment. The
SHA-256 of each YAML is therefore pinned here, and the suite fails the moment
one of them changes.

Updating a hash is a deliberate act with a written reason, never a side
effect of making a metric move. S10 was removed on purpose and must not come
back under any name.
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


def test_no_scenario_was_added_or_removed() -> None:
    """Exactly the nine frozen files, and nothing that looks like S10."""
    present = sorted(p.name for p in SCENARIO_DIR.glob("*.yaml"))
    assert present == sorted(FROZEN_SHA256), present
    assert not [p for p in present if p.startswith("s10")], "S10 must not return"
