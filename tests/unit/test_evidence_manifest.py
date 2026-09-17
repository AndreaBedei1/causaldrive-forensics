"""Unit tests for the tamper-evident run inventory.

`evidence_manifest.json` is the project's integrity claim: a SHA-256 of every
file a run directory held when the manifest was written. The claim is only worth
anything if something checks it, and if the check actually fails when the bytes
change -- so the tests here plant each kind of disagreement and assert it is
caught, in the same spirit as the anti-leakage self-tests.
"""

from __future__ import annotations

import json
from pathlib import Path

from cdf.common.io import (
    read_json,
    verify_evidence_manifest,
    write_evidence_manifest,
)


def _run_dir(tmp_path: Path) -> Path:
    root = tmp_path / "seed_000_crash"
    (root / "vehicle_A").mkdir(parents=True)
    (root / "oracle").mkdir(parents=True)
    (root / "manifest.json").write_text(json.dumps({"run_id": "r1"}), encoding="utf-8")
    (root / "vehicle_A" / "events.json").write_text(
        json.dumps({"events": [{"event_type": "HARD_BRAKE"}]}), encoding="utf-8")
    (root / "oracle" / "oracle_summary.json").write_text(
        json.dumps({"collision_pairs": []}), encoding="utf-8")
    return root


def test_manifest_lists_every_file_but_itself(tmp_path: Path) -> None:
    root = _run_dir(tmp_path)

    path = write_evidence_manifest(root, extra={"stage": "recording"})
    doc = read_json(path)

    listed = sorted(e["path"] for e in doc["files"])
    assert listed == ["manifest.json", "oracle/oracle_summary.json",
                      "vehicle_A/events.json"]
    assert doc["n_files"] == 3
    assert doc["stage"] == "recording"
    assert all(len(e["sha256"]) == 64 for e in doc["files"])
    assert all(e["bytes"] > 0 for e in doc["files"])


def test_an_untouched_run_verifies(tmp_path: Path) -> None:
    root = _run_dir(tmp_path)
    write_evidence_manifest(root, extra={"stage": "recording"})

    report = verify_evidence_manifest(root)

    assert report["ok"] is True
    assert report["n_files"] == 3
    assert report["missing"] == []
    assert report["changed"] == []
    assert report["unlisted"] == []


def test_a_changed_byte_is_caught(tmp_path: Path) -> None:
    """The whole point: evidence that was altered after recording."""
    root = _run_dir(tmp_path)
    write_evidence_manifest(root)

    (root / "vehicle_A" / "events.json").write_text(
        json.dumps({"events": [{"event_type": "HARD_BRAKE"}, {"event_type": "COLLISION"}]}),
        encoding="utf-8",
    )
    report = verify_evidence_manifest(root)

    assert report["ok"] is False
    assert report["changed"] == ["vehicle_A/events.json"]
    assert report["missing"] == []


def test_a_deleted_file_is_caught(tmp_path: Path) -> None:
    root = _run_dir(tmp_path)
    write_evidence_manifest(root)

    (root / "oracle" / "oracle_summary.json").unlink()
    report = verify_evidence_manifest(root)

    assert report["ok"] is False
    assert report["missing"] == ["oracle/oracle_summary.json"]


def test_a_later_stage_artifact_is_unlisted_not_a_failure(tmp_path: Path) -> None:
    """Analysis and fusion add files after the recording manifest is written."""
    root = _run_dir(tmp_path)
    write_evidence_manifest(root, extra={"stage": "recording"})

    (root / "fusion").mkdir()
    (root / "fusion" / "fused_causal_graph.json").write_text("{}", encoding="utf-8")
    report = verify_evidence_manifest(root)

    assert report["ok"] is True, "a new artifact is not tampering"
    assert report["unlisted"] == ["fusion/fused_causal_graph.json"]


def test_rewriting_the_manifest_covers_the_later_artifacts(tmp_path: Path) -> None:
    root = _run_dir(tmp_path)
    write_evidence_manifest(root, extra={"stage": "recording"})
    (root / "fusion").mkdir()
    (root / "fusion" / "fused_causal_graph.json").write_text("{}", encoding="utf-8")

    write_evidence_manifest(root, extra={"stage": "reprocess"})
    report = verify_evidence_manifest(root)

    assert report["ok"] is True
    assert report["unlisted"] == []
    assert report["n_files"] == 4
    assert report["stage"] == "reprocess"


def test_a_run_without_a_manifest_does_not_pass_silently(tmp_path: Path) -> None:
    root = _run_dir(tmp_path)

    report = verify_evidence_manifest(root)

    assert report["ok"] is False
    assert "no evidence_manifest.json" in report["reason"]
