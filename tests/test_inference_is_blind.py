"""Inference must be blind to the answer, proved by running it without one.

:mod:`tests.test_no_privileged_leakage` proves the inference packages never
*import* or *name* anything privileged. That is a static argument and a strong
one, but it cannot rule out a subtler dependency: a stage that silently behaves
differently when the oracle's artifacts happen to be on disk, or that keys on the
scenario label, or that has quietly come to rely on the designed causal template
being available.

So these tests take the opposite approach. They remove the privileged input
entirely -- the oracle subtree, the scenario identity, the causal template -- run
the real pipeline over the same recordings, and require the result to be
*identical*. An equality failure here is not a style violation; it means a
number somewhere in the campaign was produced with knowledge of the answer.

The comparison ignores nothing but the paths the artifacts were written to.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from cdf.common.clocks import LocalClock
from cdf.common.evidence import load_participant, save_participant
from cdf.common.io import read_json, write_json
from cdf.common.layout import RunLayout
from cdf.fusion.pipeline import fuse_run
from cdf.local.pipeline import analyse_run

from fixtures.synthetic import synthetic_partial_view

#: Fields that legitimately differ between two copies of the same run: where the
#: artifacts live, and how long the stage took.
VOLATILE_KEYS = frozenset(
    {"run_dir", "path", "root", "artifacts_root", "wall_time_s", "elapsed_s",
     "created_at", "timestamp", "generated_at"}
)

#: Labels an artifact records *about its own inputs*. These are bookkeeping, not
#: conclusions: ``scenario_id`` and ``variant`` are copied from the manifest so a
#: reader can tell which run produced the file, and ``config_hash`` identifies
#: the configuration the stage ran under. A test that changes the manifest label
#: or the configuration must expect these to follow, and must still demand that
#: every *claim* -- every node, edge, confidence, chain and named contributor --
#: is unchanged. That is the property being tested; these fields are not part of
#: it, and they are asserted on separately below.
PROVENANCE_KEYS = frozenset({"scenario_id", "variant", "config_hash"})


def _stable(value: Any, drop: frozenset) -> Any:
    """A copy of ``value`` with the given keys removed, recursively."""
    if isinstance(value, dict):
        return {
            k: _stable(v, drop) for k, v in sorted(value.items()) if k not in drop
        }
    if isinstance(value, list):
        return [_stable(v, drop) for v in value]
    return value


def _fusion_fingerprint(layout: RunLayout) -> Dict[str, Any]:
    """Everything fusion *concluded*, with the input labels stripped out."""
    drop = VOLATILE_KEYS | PROVENANCE_KEYS
    out: Dict[str, Any] = {}
    for name, path in (
        ("fused_causal", layout.fused_causal_graph),
        ("reconstruction", layout.incident_reconstruction),
        ("attribution", layout.causal_attribution),
        ("alignment", layout.fusion_dir / "time_alignment.json"),
        ("diagnostics", layout.fusion_diagnostics),
    ):
        out[name] = _stable(read_json(path), drop) if path.exists() else None
    assert out["fused_causal"] is not None, "the fused graph must exist to compare"
    return out


def _recorded_labels(layout: RunLayout) -> Dict[str, Any]:
    """The scenario labels the fused artifacts wrote down."""
    return {
        name: read_json(path).get("scenario_id")
        for name, path in (
            ("fused_causal", layout.fused_causal_graph),
            ("reconstruction", layout.incident_reconstruction),
            ("attribution", layout.causal_attribution),
        )
        if path.exists()
    }


def _recorded_run(root: Path, cfg) -> RunLayout:
    """A synthetic three-vehicle run on independent recorder clocks."""
    layout = synthetic_partial_view(root, seed=0, cfg=cfg)
    profiles = {}
    for pid in layout.participant_ids():
        evidence = load_participant(layout, pid)
        clock = LocalClock.for_participant(cfg, 0, pid, "synthetic_partial_view")
        for name in ("telemetry", "controls", "radar", "tracks", "triggers"):
            for sample in sorted(getattr(evidence, name), key=lambda s: s.t):
                sample.t, sample.frame = clock.stamp(sample.t, sample.frame)
        evidence.meta["time_domain"] = "participant_local"
        save_participant(layout, evidence)
        profiles[pid] = clock.ground_truth()
    write_json(layout.oracle_dir / "clock_ground_truth.json", {"participants": profiles})
    manifest = read_json(layout.manifest)
    manifest["clock_protocol"] = "independent_local_clocks"
    write_json(layout.manifest, manifest)
    return layout


@pytest.fixture(scope="module")
def baseline(tmp_path_factory, default_config):
    """The reference run: analysed and fused with every artifact present."""
    layout = _recorded_run(tmp_path_factory.mktemp("blind_baseline"), default_config)
    analyse_run(layout.root, default_config)
    fuse_run(layout.root, default_config)
    return layout, _fusion_fingerprint(layout)


def _copy_of(layout: RunLayout, destination: Path) -> RunLayout:
    """A fresh copy of the *recordings* only: every derived artifact is dropped."""
    shutil.copytree(layout.root, destination)
    copy = RunLayout.from_run_dir(destination)
    for derived in (copy.fusion_dir, copy.evaluation_dir, copy.checking_dir):
        if derived.exists():
            shutil.rmtree(derived)
    for pid in copy.participant_ids():
        for path in (copy.events(pid), copy.event_graph(pid), copy.event_graphml(pid),
                     copy.causal_graph(pid), copy.causal_graphml(pid)):
            if path.exists():
                path.unlink()
    return copy


# ---------------------------------------------------------------------------
# No oracle at all
# ---------------------------------------------------------------------------


def test_the_whole_pipeline_runs_and_agrees_with_no_oracle_on_disk(
    baseline, tmp_path, default_config
) -> None:
    """Delete the privileged subtree, re-derive everything, demand equality.

    If any inference stage were reading the oracle -- for the collision pair, the
    true clock offsets, the designed template -- this run would either fail or
    disagree. It must do neither.
    """
    source, expected = baseline
    copy = _copy_of(source, tmp_path / "no_oracle")
    shutil.rmtree(copy.oracle_dir)
    assert not copy.oracle_dir.exists()

    analyse_run(copy.root, default_config)
    fuse_run(copy.root, default_config)

    assert _fusion_fingerprint(copy) == expected, (
        "fusion reached a different conclusion once the oracle was removed"
    )
    assert not copy.oracle_dir.exists(), "inference must not create the oracle subtree"


def test_the_incident_is_still_reconstructed_without_the_oracle(
    baseline, tmp_path, default_config
) -> None:
    """Not merely equal -- the run must still actually explain something."""
    source, _expected = baseline
    copy = _copy_of(source, tmp_path / "no_oracle_content")
    shutil.rmtree(copy.oracle_dir)
    analyse_run(copy.root, default_config)
    fuse_run(copy.root, default_config)

    graph = read_json(copy.fused_causal_graph)
    assert graph["nodes"], "a fused graph with no nodes proves nothing"
    assert graph["edges"], "a fused graph with no edges proves nothing"
    reconstruction = read_json(copy.incident_reconstruction)
    assert reconstruction["episodes"], "no behaviour was named"
    assert reconstruction["participants"]


# ---------------------------------------------------------------------------
# No scenario identity
# ---------------------------------------------------------------------------


def test_relabelling_the_scenario_changes_nothing(
    baseline, tmp_path, default_config
) -> None:
    """The method may not recognise the scenario it is looking at.

    A rule keyed on ``S01`` would be a lookup table wearing a causal model's
    clothes. The scenario id is replaced with another scenario's -- and with
    nonsense -- and the fused conclusion must be identical both times.
    """
    source, expected = baseline
    for label in ("S09", "not_a_scenario", ""):
        copy = _copy_of(source, tmp_path / "relabelled_{0}".format(label or "blank"))
        manifest = read_json(copy.manifest)
        manifest["scenario_id"] = label
        if "variant" in manifest:
            manifest["variant"] = "some_other_variant"
        write_json(copy.manifest, manifest)

        analyse_run(copy.root, default_config)
        fuse_run(copy.root, default_config)

        assert _fusion_fingerprint(copy) == expected, (
            "fusion reached a different conclusion when the scenario was "
            "relabelled {0!r}".format(label)
        )
        # The label itself does follow the manifest, and should: an artifact
        # that did not record which run produced it would be worse, not better.
        assert set(_recorded_labels(copy).values()) == {label}


def test_the_scenario_label_is_never_a_causal_rule(src_root: Path) -> None:
    """No inference module may mention a scenario id at all."""
    import re

    pattern = re.compile(r"\bS0[1-9]\b")
    offenders: List[str] = []
    for package in ("local", "fusion", "graph", "checking", "causal"):
        for path in sorted((src_root / package).rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            # Docstrings may cite a scenario as an illustration; code may not.
            stripped = "\n".join(
                line for line in text.splitlines()
                if not line.lstrip().startswith("#")
            )
            for match in pattern.finditer(stripped):
                line = stripped[: match.start()].count("\n") + 1
                offenders.append("{0}:{1}".format(path.relative_to(src_root), line))
    # Anything found must live inside a docstring, which this cheap check cannot
    # tell apart -- so the assertion is on the *executable* mentions only.
    import ast

    real: List[str] = []
    for package in ("local", "fusion", "graph", "checking", "causal"):
        for path in sorted((src_root / package).rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            docstrings = set()
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                     ast.AsyncFunctionDef)):
                    doc = ast.get_docstring(node, clean=False)
                    if doc:
                        docstrings.add(doc)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    if node.value in docstrings:
                        continue
                    if pattern.search(node.value):
                        real.append(
                            "{0}:{1}: {2!r}".format(
                                path.relative_to(src_root), node.lineno, node.value[:60]
                            )
                        )
    assert real == [], "scenario ids used as values inside inference: {0}".format(real)


# ---------------------------------------------------------------------------
# No causal template
# ---------------------------------------------------------------------------


def test_removing_the_designed_causal_template_changes_nothing(
    baseline, tmp_path, default_config
) -> None:
    """The template is ground truth for scoring, never an input to inference."""
    source, expected = baseline
    without = default_config.with_overrides(
        {"scenario": {"causal_template": [], "expected_outcome": {},
                      "expected_culprit": None}}
    )
    copy = _copy_of(source, tmp_path / "no_template")
    analyse_run(copy.root, without)
    fuse_run(copy.root, without)

    assert _fusion_fingerprint(copy) == expected, (
        "fusion used the designed causal template"
    )
    # The configuration genuinely differed, so the recorded config hash must
    # differ too -- otherwise this test would be comparing two identical runs
    # and proving nothing.
    assert (
        read_json(copy.fusion_diagnostics)["config_hash"]
        != read_json(source.fusion_diagnostics)["config_hash"]
    ), "the two runs used the same configuration; the template was never removed"


def test_the_template_is_not_reachable_from_any_inference_module(
    src_root: Path
) -> None:
    """A grep is enough here: the key is distinctive and never legitimately read."""
    offenders: List[str] = []
    for package in ("local", "fusion", "graph", "checking"):
        for path in sorted((src_root / package).rglob("*.py")):
            text = path.read_text(encoding="utf-8")
            for lineno, line in enumerate(text.splitlines(), start=1):
                stripped = line.strip()
                if stripped.startswith("#") or not stripped:
                    continue
                for key in ("causal_template", "expected_culprit", "expected_outcome"):
                    if key in stripped and "scenario." in stripped:
                        offenders.append(
                            "{0}:{1}".format(path.relative_to(src_root), lineno)
                        )
    assert offenders == [], (
        "inference reads the scenario's declared answer: {0}".format(offenders)
    )
