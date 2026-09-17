"""The recorded campaign must be one experiment, not eleven.

The 39 runs under ``artifacts/`` were recorded over a working day, across
several commits, as the scenarios were developed and defects were fixed. That is
only legitimate if nothing which *governs* a recording or its evaluation changed
between them -- otherwise the runs are not comparable with each other, and the
campaign-level aggregates in ``docs/EXPERIMENTAL_FINDINGS.md`` would be adding
up different experiments.

Each run stores its own fully merged configuration in ``manifest.json``, so the
claim is checkable rather than a matter of trust. These tests check it.

The replay namespace allowed to differ is ``counterfactual.*``: those keys control
how replays are *executed* (whether the simulator is restarted before each one,
whether a completed replay is reused) and cannot reach a recording, a local
reconstruction, a fusion, a model check or a metric. Everything else -- the
simulation step, the radar profiles, the event thresholds, the fusion gates, the
checking and evaluation parameters, and every scenario specification -- must be
byte-identical across every run and identical to the configuration in force now.

A recording is also allowed to predate a *stage that did not exist yet*. The
retained campaign under ``artifacts/`` is the synchronized-clock baseline; the
clock protocol and post-fusion causal reasoning were added afterwards, so keys
under :data:`MIGRATION_NAMESPACES` are permitted **only when the recording does
not carry them at all**. A key the recording does carry must still match
exactly: that is the difference between adding a stage and quietly retuning the
one the campaign was recorded under.

Skipped when the artifacts are not present, so a fresh clone still passes.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

import pytest

from cdf.common.config import load_run_config

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = REPO_ROOT / "artifacts"

#: Keys that may legitimately differ: replay *execution*, never recording.
ALLOWED_PREFIX = "counterfactual."

#: Namespaces introduced after the retained baseline was recorded. A key under
#: one of these is tolerated only when the recording has no value for it -- an
#: absent key means the stage did not exist, a *different* value would mean the
#: stage was retuned between runs of one campaign.
MIGRATION_NAMESPACES = (
    "clocks.",
    "fusion.time_alignment.",
    "fusion.post_fusion.",
    "fusion.event_alignment.counterpart_",
    "fusion.event_alignment.mutual_impact_",
    "evaluation.canonical_vocabulary.",
    "evaluation.reconstruction.",
    "evaluation.causal_paths.",
    "graph.episodes.",
    "graph.reconstruction.",
    "graph.attribution.",
)


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
    """Every recorded run, excluding replays and ablation runs."""
    for manifest in sorted(ARTIFACTS.glob("*/*/manifest.json")):
        parts = manifest.parts
        if "counterfactual" in parts or "ablation" in parts:
            continue
        with open(str(manifest), encoding="utf-8") as handle:
            yield manifest.parent, json.load(handle)


def _configs() -> Dict[Tuple[str, str], Tuple[Path, Dict[str, Any]]]:
    """One representative run per (scenario, recorded config hash)."""
    out: Dict[Tuple[str, str], Tuple[Path, Dict[str, Any]]] = {}
    for run_dir, manifest in _recorded_runs():
        key = (str(manifest.get("scenario_id")), str(manifest.get("config_hash")))
        out.setdefault(key, (run_dir, manifest))
    return out


pytestmark = pytest.mark.skipif(
    not any(ARTIFACTS.glob("*/*/manifest.json")),
    reason="no recorded campaign under artifacts/",
)


def _current_flat(scenario_id: str) -> Dict[str, str]:
    cfg = load_run_config(scenario_id=scenario_id)
    data = cfg.as_dict() if hasattr(cfg, "as_dict") else cfg.data
    return _flatten(data)


def test_every_run_stores_its_merged_configuration() -> None:
    """A run that does not carry its parameters cannot be reproduced at all."""
    runs = list(_recorded_runs())
    assert runs, "no recorded runs found"
    for run_dir, manifest in runs:
        assert manifest.get("config"), "{0} has no merged config".format(run_dir)
        assert manifest.get("config_hash"), "{0} has no config hash".format(run_dir)
        assert manifest.get("git_commit"), "{0} has no git commit".format(run_dir)


def test_recorded_configs_differ_from_the_current_one_only_in_replay_execution() -> None:
    """Whatever drifted must not be able to reach a recording or a metric."""
    offenders: Dict[str, Any] = {}
    for (scenario_id, config_hash), (run_dir, manifest) in sorted(_configs().items()):
        current = _current_flat(scenario_id)
        recorded = _flatten(manifest.get("config") or {})
        differing = sorted(
            key for key in set(current) | set(recorded)
            if current.get(key) != recorded.get(key)
        )
        # The retained campaign predates independent clocks and is a separate
        # synchronized-clock baseline. Permit only newly introduced protocol
        # fields that it did not record; existing scientific settings still match.
        legacy = (
            manifest.get("clock_protocol", "synchronized_clock_baseline")
            == "synchronized_clock_baseline"
        )

        def protocol_migration(key):
            return (
                legacy
                and key not in recorded
                and any(key.startswith(ns) for ns in MIGRATION_NAMESPACES)
            )
        disallowed = [k for k in differing if not k.startswith(ALLOWED_PREFIX) and not protocol_migration(k)]
        if disallowed:
            offenders["{0}/{1}".format(scenario_id, config_hash[:8])] = disallowed

    assert not offenders, (
        "recorded runs differ from the current configuration outside "
        "`{0}*`, so they are not the same experiment: {1}".format(
            ALLOWED_PREFIX, json.dumps(offenders, indent=1)
        )
    )


def test_runs_of_one_scenario_share_their_recording_parameters() -> None:
    """Seeds and variants of a scenario must be comparable with each other."""
    per_scenario: Dict[str, Dict[str, Dict[str, str]]] = {}
    for run_dir, manifest in _recorded_runs():
        scenario_id = str(manifest.get("scenario_id"))
        flat = {
            key: value
            for key, value in _flatten(manifest.get("config") or {}).items()
            if not key.startswith(ALLOWED_PREFIX)
        }
        per_scenario.setdefault(scenario_id, {})[str(run_dir)] = flat

    for scenario_id, runs in sorted(per_scenario.items()):
        reference_dir, reference = sorted(runs.items())[0]
        for run_dir, flat in sorted(runs.items()):
            differing = sorted(
                key for key in set(reference) | set(flat)
                if reference.get(key) != flat.get(key)
            )
            assert not differing, (
                "{0}: {1} and {2} were recorded under different parameters: "
                "{3}".format(scenario_id, reference_dir, run_dir, differing)
            )
