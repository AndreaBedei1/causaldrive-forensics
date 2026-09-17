"""Unit tests for cdf.viewer.bundle and the static viewer page.

The bundle is the only thing the viewer ever reads, so these tests assert the
two properties the page depends on and cannot check for itself:

* the real run at ``artifacts/S01_rear_end/seed_000_crash`` produces a bundle
  whose numbers are the run's own -- both participants, A's radar track series,
  the fused causal graph, the oracle block -- and
* privileged material is reachable **only** under the top-level ``"oracle"``
  key, which is walked recursively rather than trusted.

Everything that can be asserted against the real artifacts is; the synthetic
fixtures exist only for the cases the real run does not exhibit (a series long
enough to be decimated).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

import pytest

from cdf.common.config import Config, load_run_config, repo_root
from cdf.common.io import write_json, write_jsonl_gz
from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    FORBIDDEN_LOCAL_FIELD_NAMES,
    FORBIDDEN_LOCAL_FIELD_SUBSTRINGS,
    SCHEMA_VERSIONS,
)
from cdf.viewer.bundle import (
    PRIVILEGED_WARNING,
    VIEWER_ASSETS,
    build_run_bundle,
    install_viewer_assets,
    viewer_assets_dir,
    write_bundle,
)

REAL_RUN = repo_root() / "artifacts" / "S01_rear_end" / "seed_000_crash"


@pytest.fixture(scope="module")
def cfg() -> Config:
    return load_run_config(scenario_id="S01")


@pytest.fixture(scope="module")
def real_bundle(cfg: Config) -> Dict[str, Any]:
    if not REAL_RUN.exists():
        pytest.skip("the reference run {0} is not present".format(REAL_RUN))
    return build_run_bundle(REAL_RUN, cfg)


# ---------------------------------------------------------------------------
# Structure walking helpers
# ---------------------------------------------------------------------------


def walk_keys(node: Any, path: str = "") -> Iterator[Tuple[str, str]]:
    """Yield ``(key, path)`` for every mapping key in a JSON-like structure."""
    if isinstance(node, dict):
        for key, value in node.items():
            here = "{0}.{1}".format(path, key) if path else str(key)
            yield str(key), here
            for item in walk_keys(value, here):
                yield item
    elif isinstance(node, list):
        for i, value in enumerate(node):
            for item in walk_keys(value, "{0}[{1}]".format(path, i)):
                yield item


# ---------------------------------------------------------------------------
# The real run
# ---------------------------------------------------------------------------


def test_real_run_bundle_contains_both_participants(real_bundle: Dict[str, Any]) -> None:
    assert real_bundle["schema_version"] == SCHEMA_VERSIONS["viewer"]
    assert sorted(real_bundle["participants"].keys()) == ["A", "B"]
    assert real_bundle["run"]["outcome"] == "collision"
    assert real_bundle["run"]["scenario_id"] == "S01"
    assert real_bundle["run"]["variant"] == "crash"
    assert real_bundle["run"]["dt"] > 0.0
    assert real_bundle["run"]["t_end"] > real_bundle["run"]["t_start"]

    for pid in ("A", "B"):
        block = real_bundle["participants"][pid]
        assert block["telemetry"], "participant {0} has no telemetry".format(pid)
        first = block["telemetry"][0]
        assert set(first) == {"t", "x", "y", "yaw", "speed", "accel_long"}
        assert block["controls"], "participant {0} has no controls".format(pid)
        assert set(block["controls"][0]) == {"t", "throttle", "brake", "steer"}
        # The event list is exactly what the participant's own artifact holds --
        # asserted against the file rather than against a remembered count, so
        # the test still means something after the run is regenerated.
        on_disk = json.loads(
            (REAL_RUN / "vehicle_{0}".format(pid) / "events.json").read_text(encoding="utf-8")
        )["events"]
        assert len(block["events"]) == len(on_disk)
        for event in block["events"]:
            assert event["participant_id"] == pid
            assert event["provenance"] == "local"


def test_real_run_track_series_is_A_and_shaped_for_the_viewer(
    real_bundle: Dict[str, Any]
) -> None:
    """A is the following vehicle: it holds the run's radar tracks, B holds none."""
    tracks_a = real_bundle["participants"]["A"]["tracks"]
    assert len(tracks_a) >= 1
    assert "A::T001" in tracks_a
    series = tracks_a["A::T001"]
    assert len(series) > 1
    assert set(series[0]) == {"t", "gx", "gy", "range_m", "ttc", "confidence"}
    assert all(0.0 <= s["confidence"] <= 1.0 for s in series)
    # Every track id is namespaced by its observer, never by an actor identity.
    assert all(tid.startswith("A::") for tid in tracks_a)
    assert real_bundle["participants"]["B"]["tracks"] == {}


def test_real_run_has_local_and_fused_causal_graphs(real_bundle: Dict[str, Any]) -> None:
    local_path = REAL_RUN / "vehicle_A" / "causal_graph.json"
    fused_path = REAL_RUN / "fusion" / "fused_causal_graph.json"
    if not (local_path.exists() and fused_path.exists()):
        pytest.skip("the reference run currently has no persisted causal graphs")

    local = real_bundle["participants"]["A"]["causal_graph"]
    assert local["scope"] == "local"
    assert local["owner"] == "A"
    assert len(local["nodes"]) == len(
        json.loads(local_path.read_text(encoding="utf-8"))["nodes"]
    )
    assert len(local["edges"]) > 0

    fused = real_bundle["fusion"]["causal_graph"]
    assert fused["scope"] == "fused"
    assert len(fused["nodes"]) == len(
        json.loads(fused_path.read_text(encoding="utf-8"))["nodes"]
    )
    assert fused["summary"]["is_dag"] is True
    # Fusion exists to produce a graph no single vehicle had: one spanning both
    # participants.
    assert {n["participant_id"] for n in fused["nodes"]} >= {"A", "B"}


def test_real_run_association_is_carried_with_its_evidence(
    real_bundle: Dict[str, Any]
) -> None:
    if not (REAL_RUN / "fusion" / "association_report.json").exists():
        pytest.skip("the reference run currently has no association report")
    assoc = real_bundle["fusion"]["association"]
    assert assoc, "the reference run associates at least one track"
    for row in assoc:
        # A track id is namespaced by its observer and by nothing else; the
        # identity on the right-hand side is the inference.
        assert row["track_id"].startswith(row["observer_id"] + "::")
        assert row["status"] in {"RESOLVED", "AMBIGUOUS", "UNRESOLVED"}
        # The claim must not travel without the numbers that justify it.
        assert 0.0 <= row["confidence"] <= 1.0
        assert row["overlap_s"] is not None
        # A RESOLVED claim must travel with the number that justifies it; an
        # UNRESOLVED one legitimately has no trajectory fit to report.
        if row["status"] == "RESOLVED":
            assert row["rmse_m"] is not None
    # A rear-ends B: the follower's track resolves onto the other participant.
    assert any(
        r["assigned_participant"] and r["assigned_participant"] != r["observer_id"]
        for r in assoc
    )


def test_real_run_oracle_block_is_present_and_badged(real_bundle: Dict[str, Any]) -> None:
    oracle = real_bundle["oracle"]
    assert oracle["_warning"] == PRIVILEGED_WARNING
    assert sorted(oracle["trajectories"].keys()) == ["A", "B"]
    for pid, series in oracle["trajectories"].items():
        assert len(series) > 1
        assert set(series[0]) == {"t", "x", "y", "yaw", "speed"}
    collisions = oracle["collisions"]
    assert collisions, "the reference run is a crash variant"
    partners = {(c["participant_id"], c["other_participant_id"]) for c in collisions}
    assert ("A", "B") in partners or ("B", "A") in partners
    span = (real_bundle["run"]["t_start"], real_bundle["run"]["t_end"])
    for c in collisions:
        assert span[0] <= c["t"] <= span[1] + real_bundle["run"]["dt"]


def test_oracle_content_never_appears_outside_the_oracle_block(
    real_bundle: Dict[str, Any]
) -> None:
    """Walk the whole document: no privileged key outside ``bundle["oracle"]``."""
    outside = {k: v for k, v in real_bundle.items() if k != "oracle"}
    offenders: List[str] = []
    for key, path in walk_keys(outside):
        low = key.lower()
        if low in FORBIDDEN_LOCAL_FIELD_NAMES:
            offenders.append(path)
        elif any(sub in low for sub in FORBIDDEN_LOCAL_FIELD_SUBSTRINGS):
            offenders.append(path)
    assert offenders == [], "privileged field names outside oracle block: {0}".format(offenders)

    # ... and the word "oracle" itself is not a key anywhere outside it.
    assert [p for k, p in walk_keys(outside) if "oracle" in k.lower()] == []

    # The oracle block itself carries no simulator bookkeeping either: the
    # viewer is given where a vehicle truly was, not how CARLA numbered it.
    inside = [p for k, p in walk_keys(real_bundle["oracle"]) if k.lower() in {"actor_id", "other_actor_id", "lane_id", "road_id", "traffic_light_state"}]
    assert inside == []


def test_missing_counterfactual_block_is_omitted_and_noted(
    tmp_path: Path, cfg: Config
) -> None:
    """An absent block is reported as missing -- never faked, never a zero.

    Built against a copy of the reference run with the counterfactual artifacts
    removed, rather than against whatever the reference run happens to contain:
    the reference acquires a counterfactual block as soon as the replay campaign
    is run, and a test that depended on its absence would silently stop testing
    anything.
    """
    import shutil

    if not REAL_RUN.exists():
        pytest.skip("the recorded reference run is not present")
    stripped = tmp_path / "stripped_run"
    shutil.copytree(REAL_RUN, stripped)
    cf_dir = stripped / "counterfactual"
    if cf_dir.exists():
        shutil.rmtree(cf_dir)

    bundle = build_run_bundle(stripped, cfg)
    assert "counterfactual" not in bundle
    notes = [n for n in bundle["notes"] if n["block"] == "counterfactual"]
    assert len(notes) == 1
    assert notes[0]["status"] == "missing"
    assert "counterfactual_manifest.json" in notes[0]["paths"]


def test_present_counterfactual_block_is_carried(real_bundle: Dict[str, Any]) -> None:
    """Conversely, when the artifacts exist the bundle must carry them."""
    cf_dir = REAL_RUN / "counterfactual"
    if not any(cf_dir.glob("*.json")):
        pytest.skip("the reference run has not been replayed yet")
    assert "counterfactual" in real_bundle, (
        "the run carries counterfactual artifacts but the bundle dropped them"
    )


def test_bundle_is_json_serialisable_and_deterministic(real_bundle: Dict[str, Any], cfg: Config) -> None:
    first = json.dumps(real_bundle, sort_keys=True, allow_nan=False)
    second = json.dumps(build_run_bundle(REAL_RUN, cfg), sort_keys=True, allow_nan=False)
    assert first == second


# ---------------------------------------------------------------------------
# Decimation
# ---------------------------------------------------------------------------


def make_synthetic_run(root: Path, n_samples: int, participant: str = "A") -> Path:
    """A minimal but loadable run directory with one long telemetry series."""
    layout = RunLayout.create(root, "S99", "synthetic", 0)
    layout.vehicle_dir(participant).mkdir(parents=True, exist_ok=True)
    write_jsonl_gz(
        layout.telemetry(participant),
        [
            {
                "t": 0.05 * (i + 1),
                "frame": i,
                "participant_id": participant,
                "x": float(i) * 0.5,
                "y": 0.0,
                "z": 0.0,
                "yaw": 0.0,
                "speed": 10.0,
                "accel_long": 0.0,
            }
            for i in range(n_samples)
        ],
    )
    write_json(
        layout.manifest,
        {
            "run_id": "S99-synthetic-seed000",
            "scenario_id": "S99",
            "variant": "synthetic",
            "seed": 0,
            "map_name": "TownTest",
            "outcome": "no_event",
            "duration_sim_s": 0.05 * n_samples,
            "fixed_delta_seconds": 0.05,
            "n_frames": n_samples,
            "config_hash": "deadbeefdeadbeef",
        },
    )
    return layout.root


def test_long_series_is_decimated_and_the_factor_is_recorded(
    tmp_path: Path, cfg: Config
) -> None:
    run_dir = make_synthetic_run(tmp_path, n_samples=5000)
    limited = cfg.with_overrides({"output": {"viewer_max_samples": 100}})
    bundle = build_run_bundle(run_dir, limited)

    series = bundle["participants"]["A"]["telemetry"]
    meta = bundle["participants"]["A"]["sampling"]["telemetry"]
    assert bundle["sampling"]["max_samples"] == 100
    assert len(series) <= 100
    assert meta["n_source"] == 5000
    assert meta["n_emitted"] == len(series)
    assert meta["stride"] == 50
    assert meta["decimated"] is True
    # Endpoints survive: a trajectory that silently loses its last sample would
    # stop short of the event it is meant to explain.
    assert series[0]["t"] == pytest.approx(0.05)
    assert series[-1]["t"] == pytest.approx(0.05 * 5000)


def test_short_series_is_left_alone(tmp_path: Path, cfg: Config) -> None:
    run_dir = make_synthetic_run(tmp_path, n_samples=40)
    bundle = build_run_bundle(run_dir, cfg)
    meta = bundle["participants"]["A"]["sampling"]["telemetry"]
    assert meta == {"n_source": 40, "n_emitted": 40, "stride": 1, "decimated": False}
    assert len(bundle["participants"]["A"]["telemetry"]) == 40


def test_default_max_samples_comes_from_config(tmp_path: Path, cfg: Config) -> None:
    """With no ``output.viewer_max_samples`` set, the documented default holds."""
    run_dir = make_synthetic_run(tmp_path, n_samples=10)
    bundle = build_run_bundle(run_dir, cfg)
    assert bundle["sampling"]["max_samples"] == int(
        cfg.get("output.viewer_max_samples", 1200)
    )


def test_synthetic_run_omits_every_absent_block(tmp_path: Path, cfg: Config) -> None:
    run_dir = make_synthetic_run(tmp_path, n_samples=10)
    bundle = build_run_bundle(run_dir, cfg)
    for block in ("fusion", "oracle", "checking", "counterfactual", "evaluation"):
        assert block not in bundle
        assert [n for n in bundle["notes"] if n["block"] == block], block


def test_not_a_run_directory_fails_loudly(tmp_path: Path, cfg: Config) -> None:
    empty = tmp_path / "not_a_run"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        build_run_bundle(empty, cfg)
    with pytest.raises(FileNotFoundError):
        build_run_bundle(tmp_path / "absent", cfg)


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------


def test_write_bundle_lands_in_the_layout_with_the_page(
    tmp_path: Path, cfg: Config
) -> None:
    run_dir = make_synthetic_run(tmp_path, n_samples=30)
    path = write_bundle(run_dir, cfg)
    layout = RunLayout.from_run_dir(run_dir)
    assert path == layout.viewer_bundle
    assert path.name == "run_data.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["run"]["scenario_id"] == "S99"
    # The page fetches run_data.json relative to itself, so it must be beside it.
    for asset in VIEWER_ASSETS:
        assert (layout.viewer_dir / asset).exists()


def test_install_viewer_assets_reports_a_missing_page(tmp_path: Path) -> None:
    installed = install_viewer_assets(tmp_path / "out")
    assert sorted(p.name for p in installed) == sorted(VIEWER_ASSETS)


# ---------------------------------------------------------------------------
# The static page itself
# ---------------------------------------------------------------------------


def test_index_html_is_self_contained() -> None:
    index = viewer_assets_dir() / "index.html"
    text = index.read_text(encoding="utf-8")
    assert 'src="app.js"' in text
    assert 'href="styles.css"' in text
    # No CDN, no web font, no analytics: the page must open from an offline copy.
    assert "http://" not in text
    assert "https://" not in text
    assert "run_data.json" in text or "run_data.json" in (
        viewer_assets_dir() / "app.js"
    ).read_text(encoding="utf-8")


def test_app_js_fetches_the_bundle_and_badges_every_perspective() -> None:
    app = (viewer_assets_dir() / "app.js").read_text(encoding="utf-8")
    assert "fetch('run_data.json')" in app
    assert PRIVILEGED_WARNING in app
    assert "LOCAL RECONSTRUCTION" in app
    assert "FUSED RECONSTRUCTION" in app
    assert "INSUFFICIENT EVIDENCE" in app
