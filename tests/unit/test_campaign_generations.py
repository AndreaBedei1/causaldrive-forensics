"""V1 and V2 recordings must not end up averaged together.

The brief forbids mixing them, and the failure mode worth guarding is the quiet
one: a campaign resumed into an old directory, a summary table computed over the
mixture, and nothing downstream able to tell. So the generation is read off the
recording itself rather than off the directory name -- a directory can be renamed
and a recording cannot be re-sensored.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def campaign_module():
    spec = importlib.util.spec_from_file_location(
        "run_campaign", str(REPO_ROOT / "scripts" / "run_campaign.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_run(root: Path, scenario: str, run: str, generation: str) -> Path:
    run_dir = root / scenario / run
    (run_dir / "vehicle_A").mkdir(parents=True, exist_ok=True)
    (run_dir / "manifest.json").write_text(json.dumps({"run_id": run}))
    if generation == "v2":
        (run_dir / "vehicle_A" / "video").mkdir(exist_ok=True)
    return run_dir


# --- reading the generation off the recording ------------------------------


def test_a_run_with_camera_artifacts_is_v2(tmp_path):
    module = campaign_module()
    run_dir = make_run(tmp_path, "S10_single_stop_a", "seed_000_rolls_through", "v2")
    assert module.run_generation(run_dir) == "v2"


def test_a_run_without_them_is_v1(tmp_path):
    module = campaign_module()
    run_dir = make_run(tmp_path, "S01_rear_end", "seed_000_crash", "v1")
    assert module.run_generation(run_dir) == "v1"


def test_a_local_log_alone_is_enough_to_mark_a_run_v2(tmp_path):
    """The camera is optional in V2; the log-first data model is not."""
    module = campaign_module()
    run_dir = make_run(tmp_path, "S13_x", "seed_000_cut_in", "v1")
    (run_dir / "vehicle_A" / "local_log.json").write_text("{}")
    assert module.run_generation(run_dir) == "v2"


def test_a_directory_with_no_manifest_is_not_a_run(tmp_path):
    module = campaign_module()
    (tmp_path / "S01" / "seed_000").mkdir(parents=True)
    assert module.run_generation(tmp_path / "S01" / "seed_000") is None


# --- the refusal ----------------------------------------------------------


def test_an_empty_root_is_fine(tmp_path):
    module = campaign_module()
    assert module.generation_conflict(tmp_path) is None


def test_a_root_that_does_not_exist_yet_is_fine(tmp_path):
    module = campaign_module()
    assert module.generation_conflict(tmp_path / "artifacts_v2") is None


def test_a_root_of_one_generation_is_fine(tmp_path):
    module = campaign_module()
    make_run(tmp_path, "S01_rear_end", "seed_000_crash", "v1")
    make_run(tmp_path, "S02_cut_in", "seed_000_crash", "v1")
    assert module.generation_conflict(tmp_path) is None


def test_a_mixed_root_is_refused_and_says_which_runs(tmp_path):
    module = campaign_module()
    make_run(tmp_path, "S01_rear_end", "seed_000_crash", "v1")
    make_run(tmp_path, "S10_single_stop_a", "seed_000_rolls_through", "v2")
    message = module.generation_conflict(tmp_path)
    assert message is not None
    assert "both generations" in message
    assert "S01_rear_end/seed_000_crash" in message
    assert "S10_single_stop_a/seed_000_rolls_through" in message
    assert "describe neither campaign" in message


def test_counterfactual_replays_are_not_counted_as_runs(tmp_path):
    """A replay is a replay of a run, and counting them would make one V1 run
    look like a dozen -- and could manufacture a conflict that is not there."""
    module = campaign_module()
    run_dir = make_run(tmp_path, "S01_rear_end", "seed_000_crash", "v1")
    replay = run_dir / "counterfactual" / "replays" / "A_brake__disable"
    (replay / "vehicle_A").mkdir(parents=True)
    (replay / "manifest.json").write_text("{}")
    make_run(tmp_path, "S02_cut_in", "seed_000_crash", "v1")
    assert module.generation_conflict(tmp_path) is None
