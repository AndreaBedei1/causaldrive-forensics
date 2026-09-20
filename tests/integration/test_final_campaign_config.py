"""The final campaign has to be one experiment, and that has to be checkable.

A sibling of `test_recorded_campaign_config.py`, which guards the retained V1
baseline under `artifacts/`. This one guards the campaign the current results
are computed from, under `artifacts_v2/`, and it exists because that campaign is
no longer recorded in one sitting: the nine frozen scenarios were recorded once
and are reused, and the corrected scenarios were re-recorded afterwards. Reuse
is the right call -- re-recording a hash-frozen scenario would change evidence
nobody asked to change -- but it makes "one experiment" a claim rather than a
fact about the clock, so it is checked here instead of asserted in prose.

What must hold:

* every run stores its own merged configuration, so the claim is checkable from
  the artifacts rather than from a commit stamp;
* all seeds and variants of one scenario were recorded under the same
  parameters, because a seed recorded under different settings is not another
  sample of the same thing;
* the recorded configurations differ from the current tree only where the
  difference provably cannot reach a recording or a metric, and each such key
  is named below with its reason.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

import pytest

from cdf.common.config import load_run_config

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = REPO_ROOT / "artifacts_v2"

#: Differences between what a run recorded and the configuration in the tree
#: today, each with the argument for why it cannot have changed a result.
#:
#: `counterfactual.` is execution policy for replays, read when a replay is
#: launched and never during a recording or an evaluation.
#:
#: `fusion.time_alignment.max_offset_s` is a key that was removed by accident
#: and restored in 9577313. The nine frozen scenarios were recorded while it was
#: absent, so their manifests carry no value for it. The estimator's own default
#: is the same 1.0 the configuration now declares
#: (`cdf.fusion.clock_alignment`, `get("max_offset_s", 1)`), so the restoration
#: changed what the configuration says and not what the code does. It is also a
#: fusion parameter, and fusion is re-derived offline over every run in the
#: campaign with the configuration in the tree today.
ALLOWED_DIFFERENCES = {
    "fusion.time_alignment.max_offset_s": "restored declaration of the code default",
}
ALLOWED_PREFIXES = ("counterfactual.",)


def _flatten(node: Any, prefix: str = "") -> Dict[str, str]:
    """Dotted key -> canonical JSON value, so comparison is exact."""
    flat: Dict[str, str] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            path = "{0}.{1}".format(prefix, key) if prefix else str(key)
            flat.update(_flatten(value, path))
    else:
        flat[prefix] = json.dumps(node, sort_keys=True, default=str)
    return flat


def _recorded_runs() -> Iterator[Tuple[Path, Dict[str, Any]]]:
    for manifest in sorted(ARTIFACTS.glob("*/*/manifest.json")):
        if "counterfactual" in manifest.parts or "ablation" in manifest.parts:
            continue
        with open(str(manifest), encoding="utf-8") as handle:
            yield manifest.parent, json.load(handle)


pytestmark = pytest.mark.skipif(
    not any(ARTIFACTS.glob("*/*/manifest.json")),
    reason="no recorded campaign under artifacts_v2/",
)


def test_every_run_stores_its_own_configuration_and_commit() -> None:
    runs = list(_recorded_runs())
    assert runs, "no runs found"
    for run_dir, manifest in runs:
        assert manifest.get("config"), "{0} stores no configuration".format(run_dir)
        assert manifest.get("config_hash"), "{0} has no config hash".format(run_dir)
        assert manifest.get("git_commit"), "{0} has no commit".format(run_dir)


def test_every_run_used_the_independent_clock_protocol() -> None:
    """The campaign's defining property, and the one a stray run would break."""
    for run_dir, manifest in _recorded_runs():
        assert manifest.get("clock_protocol") == "independent_local_clocks", (
            run_dir, manifest.get("clock_protocol")
        )


def test_seeds_of_one_scenario_were_recorded_under_the_same_parameters() -> None:
    """Otherwise the three seeds are three experiments with one name."""
    per_scenario: Dict[str, Dict[str, Dict[str, str]]] = {}
    for run_dir, manifest in _recorded_runs():
        flat = {
            key: value
            for key, value in _flatten(manifest.get("config") or {}).items()
            if not key.startswith(ALLOWED_PREFIXES)
        }
        per_scenario.setdefault(str(manifest.get("scenario_id")), {})[str(run_dir)] = flat

    for scenario_id, runs in sorted(per_scenario.items()):
        reference_dir, reference = sorted(runs.items())[0]
        for run_dir, flat in sorted(runs.items()):
            differing = sorted(
                key for key in set(reference) | set(flat)
                if reference.get(key) != flat.get(key)
            )
            assert not differing, (
                "{0}: {1} and {2} were recorded under different parameters: {3}"
                .format(scenario_id, reference_dir, run_dir, differing)
            )


def test_the_campaign_differs_from_the_current_tree_only_where_it_cannot_matter() -> None:
    """Every drifting key has to be one somebody wrote down a reason for."""
    seen: Dict[Tuple[str, str], Tuple[Path, Dict[str, Any]]] = {}
    for run_dir, manifest in _recorded_runs():
        seen.setdefault(
            (str(manifest.get("scenario_id")), str(manifest.get("config_hash"))),
            (run_dir, manifest),
        )

    offenders: Dict[str, Any] = {}
    for (scenario_id, config_hash), (run_dir, manifest) in sorted(seen.items()):
        current = _flatten(load_run_config(scenario_id).data)
        recorded = _flatten(manifest.get("config") or {})
        differing = sorted(
            key for key in set(current) | set(recorded)
            if current.get(key) != recorded.get(key)
        )
        disallowed = [
            key for key in differing
            if key not in ALLOWED_DIFFERENCES and not key.startswith(ALLOWED_PREFIXES)
        ]
        if disallowed:
            offenders["{0}/{1}".format(scenario_id, config_hash[:8])] = disallowed

    assert not offenders, (
        "recorded runs differ from the current configuration in keys nobody has "
        "justified, so they are not the same experiment: {0}"
        .format(json.dumps(offenders, indent=1))
    )


def test_one_configuration_per_scenario() -> None:
    """Two configurations for one scenario means two experiments under one name."""
    hashes: Dict[str, set] = {}
    for _run_dir, manifest in _recorded_runs():
        hashes.setdefault(str(manifest.get("scenario_id")), set()).add(
            str(manifest.get("config_hash"))
        )
    multiple = {sid: sorted(h) for sid, h in hashes.items() if len(h) > 1}
    assert not multiple, multiple
