"""Clock truth stays in evaluation; ablation cannot overwrite inference inputs."""

from hashlib import sha256
import pytest

from cdf.common.evidence import load_participant, save_participant
from cdf.common.io import read_json, write_json
from cdf.evaluation.clocks import evaluate_clock_alignment
from cdf.evaluation.clock_ablation import run_clock_ablation
from cdf.evaluation.suite import evaluate_run
from cdf.fusion.pipeline import fuse_run
from cdf.local.pipeline import analyse_run
from cdf.oracle.graph import build_and_persist
from cdf.simulation.scenario_base import ScenarioSpec
from cdf.common.config import load_run_config
from fixtures.synthetic import synthetic_partial_view


def test_clock_errors_use_relative_reference_not_absolute_time():
    truth = {
        "A": {"true_offset_s": 0.41, "true_scale": 1.001},
        "B": {"true_offset_s": -0.23, "true_scale": 0.999},
        "C": {"true_offset_s": 0.12, "true_scale": 1.002},
    }
    models = {}
    for pid, profile in truth.items():
        a = truth["B"]["true_scale"] / profile["true_scale"]
        b = truth["B"]["true_offset_s"] - a * profile["true_offset_s"]
        models[pid] = {"scale": a, "offset_s": b, "status": "ALIGNED"}
    result = evaluate_clock_alignment({"reference": "B", "offsets": models}, truth)
    assert result["mean_abs_offset_error_s"] == pytest.approx(0)
    assert result["mean_abs_drift_error_ppm"] == pytest.approx(0)
    assert result["n_resolved"] == 3
    models["C"] = {
        "status": "UNRESOLVED_TIME_ALIGNMENT",
        "scale": None,
        "offset_s": None,
    }
    result = evaluate_clock_alignment({"reference": "B", "offsets": models}, truth)
    assert result["n_resolved"] == 2
    assert result["participants"][2]["offset_error_s"] is None


def test_ablation_has_all_metrics_and_preserves_raw_and_fused_files(
    tmp_path, default_config
):
    cfg = default_config.with_overrides(
        {"fusion": {"time_alignment": {"max_offset_s": 2.0}}}
    )
    layout = synthetic_partial_view(tmp_path, cfg=cfg)
    truth = {}
    for pid, (offset, scale) in {
        "A": (-0.6, 1.0001),
        "B": (0.55, 0.9999),
        "C": (-0.15, 1.0),
    }.items():
        ev = load_participant(layout, pid)
        for name in ("telemetry", "controls", "radar", "tracks", "triggers"):
            for sample in getattr(ev, name):
                sample.t = scale * sample.t + offset
        ev.meta["time_domain"] = "participant_local"
        save_participant(layout, ev)
        truth[pid] = {
            "true_offset_s": offset,
            "true_scale": scale,
            "true_drift_ppm": (scale - 1) * 1e6,
        }
    write_json(layout.oracle_dir / "clock_ground_truth.json", {"participants": truth})
    manifest = read_json(layout.manifest)
    manifest["clock_protocol"] = "independent_local_clocks"
    write_json(layout.manifest, manifest)
    analyse_run(layout.root, cfg)
    fuse_run(layout.root, cfg)
    spec = ScenarioSpec.from_config(load_run_config("S06"), variant="a_front_pushed")
    build_and_persist(layout.root, spec, cfg)
    guarded = [
        p
        for p in layout.root.rglob("*")
        if p.is_file() and "evaluation" not in p.relative_to(layout.root).parts
    ]
    before = {p: sha256(p.read_bytes()).hexdigest() for p in guarded}
    report = run_clock_ablation(layout.root, cfg)
    assert before == {p: sha256(p.read_bytes()).hexdigest() for p in guarded}
    assert set(report["modes"]) == {
        "A_synchronized",
        "B_independent_uncorrected",
        "C_independent_aligned",
    }
    for row in report["modes"].values():
        assert {"precision", "recall", "f1"} <= set(row["association"])
        assert row["event_matching"]["fused"]["f1"] is not None
        assert row["graphs"]["fused"]["node_f1"] is not None
        assert row["graphs"]["fused"]["edge_f1"] is not None
    aligned = report["modes"]["C_independent_aligned"]["clock"]
    uncorrected = report["modes"]["B_independent_uncorrected"]["clock"]
    assert aligned["n_resolved"] == 3
    # Finite-extent radar centroids are not exact self-reported body origins.
    # Millisecond accuracy is tested separately on precise physical point traces;
    # this test checks honest scoring and improvement under surface-centroid bias.
    assert aligned["mean_abs_offset_error_s"] < 0.2
    assert aligned["mean_abs_offset_error_s"] < uncorrected["mean_abs_offset_error_s"]
    assert aligned["alignment_residual"] is not None
    assert (layout.evaluation_dir / "clock_ablation.json").exists()


def test_ablation_requires_oracle_profiles_in_evaluation(tmp_path, default_config):
    layout = synthetic_partial_view(tmp_path, cfg=default_config)
    with pytest.raises(ValueError, match="oracle/"):
        run_clock_ablation(layout.root, default_config)


def test_missing_clock_truth_cannot_produce_mixed_domain_metrics(
    tmp_path, default_config
):
    layout = synthetic_partial_view(tmp_path, cfg=default_config)
    manifest = read_json(layout.manifest)
    manifest["clock_protocol"] = "independent_local_clocks"
    write_json(layout.manifest, manifest)
    analyse_run(layout.root, default_config)
    fuse_run(layout.root, default_config)
    spec = ScenarioSpec.from_config(load_run_config("S06"), variant="a_front_pushed")
    build_and_persist(layout.root, spec, default_config)
    metrics = evaluate_run(layout.root, default_config)
    for key in ("events", "graphs", "association", "fusion_benefit"):
        assert metrics[key] is None
        assert "clock profiles" in metrics["reasons"][key]
    assert metrics["reconstruction"]["fused_causal"]["n_nodes"] > 0
