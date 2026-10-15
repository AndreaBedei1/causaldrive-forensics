#!/usr/bin/env python3
"""The manifest of the frozen reconstruction and experimental protocol (written before the campaign starts).

    python scripts/freeze_manifest.py [--out results/frozen_campaign_manifest.json] [--port 3000]

It records what the annotated tag ``pre-robustness-campaign`` freezes: the code and configuration hashes (the
same digests every job's provenance carries), the hashes of the evaluation and driver scripts, scenario and
held-out configurations, the raw data of the 22 canonical runs, the robustness profiles, the experiment matrix
with its seed schedule, and the software versions.  A file committed with the code cannot name its own commit:
the commit is the one the tag points to, and every job records it (``provenance.git_commit``; the campaign runs
with ``CDF_ANALYSIS_FREEZE_COMMIT`` set, which refuses any other commit or a modified tree).
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import platform
import sys
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]

SCRIPTS = ["robustness.py", "campaign_report.py", "generalization.py", "stability_audit.py", "validate_canonical.py",
           "run_scenario.py", "reconstruct_run.py", "hardening_refresh.py", "freeze_manifest.py"]


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def tree_hash(paths: List[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def raw_hash(run: Path) -> Dict[str, Any]:
    """SHA-256 over the raw recording (vehicles/, ground_truth/, metadata.json, incident_context.json)."""
    files = [p for p in run.rglob("*") if p.is_file() and p.relative_to(run).parts[0] in
             ("vehicles", "ground_truth", "metadata.json", "incident_context.json")]
    return {"files": len(files), "bytes": sum(p.stat().st_size for p in files), "sha256": tree_hash(files, run)}


def versions() -> Dict[str, Any]:
    out: Dict[str, Any] = {"python": sys.version, "platform": platform.platform()}
    try:
        from importlib import metadata
        out["packages"] = {d.metadata["Name"]: d.version for d in sorted(metadata.distributions(),
                                                                        key=lambda d: d.metadata["Name"].lower())}
    except Exception as exc:  # pragma: no cover
        out["packages_error"] = repr(exc)
    return out


def carla_versions(port: int) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    try:
        import carla
        out["client_module"] = getattr(carla, "__file__", None)
        client = carla.Client("127.0.0.1", port)
        client.set_timeout(10.0)
        out["client_version"] = client.get_client_version()
        out["server_version"] = client.get_server_version()
    except Exception as exc:
        out["error"] = repr(exc)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "frozen_campaign_manifest.json")
    parser.add_argument("--port", type=int, default=3000)
    parser.add_argument("--workers", type=int, required=True, help="the worker count decided for the campaign")
    args = parser.parse_args()
    from cdf.evaluation.provenance import code_hash, config_hash
    from cdf.reconstruction.config import load_config
    from cdf.robustness.perturb import GNSS_PROFILES, RADAR_PROFILES
    import robustness
    from validate_canonical import CANONICAL, canonical_runs
    runs = [Path(r) for r in canonical_runs()]
    cfg = load_config()
    matrix = {}
    for family, (levels, stochastic) in robustness.FAMILIES.items():
        jobs3 = sum(len(robustness.jobs_for(ROOT / run, family, [0, 1, 2])) for run in runs)
        jobs8 = sum(len(robustness.jobs_for(ROOT / run, family, list(range(8)))) for run in runs)
        matrix[family] = {"levels": [{"label": label, "parameter": parameter} for label, parameter in levels],
                          "stochastic": stochastic, "jobs_initial": jobs3, "jobs_max": jobs8 if stochastic else jobs3,
                          "configuration": "ablation_mutual_refinement" if family == "gnss_refined" else "frozen"}
    import yaml
    heldout = yaml.safe_load((ROOT / "configs" / "heldout" / "frozen_campaign.yaml").read_text(encoding="utf-8"))
    manifest = {
        "name": "pre-robustness-campaign",
        "statement": "reconstruction algorithm, configuration, event definitions, evaluation rules and experimental "
                     "protocol frozen before any main result is collected; any later revision is a new version with "
                     "separately identified results",
        "code_sha256": code_hash(),
        "reconstruction_config_sha256": config_hash(cfg.to_dict()),
        "reconstruction_config": cfg.to_dict(),
        "scripts_sha256": {name: file_hash(ROOT / "scripts" / name) for name in SCRIPTS},
        "scenario_configs_sha256": tree_hash(list((ROOT / "configs" / "scenarios").glob("*.yaml")), ROOT),
        "sensor_configs_sha256": tree_hash(list((ROOT / "configs" / "sensors").glob("*.yaml")), ROOT),
        "heldout_protocol_sha256": file_hash(ROOT / "configs" / "heldout" / "frozen_campaign.yaml"),
        "canonical_manifest": {"set": "S01..S19, 22 runs", "variants": CANONICAL,
                               "runs": {(ROOT / run).resolve().relative_to(ROOT.resolve()).as_posix(): raw_hash(ROOT / run) for run in runs}},
        "robustness": {
            "driver": "scripts/robustness.py --canonical --work robustness/frozen_campaign "
                      "--results results/robustness/frozen_campaign",
            "radar_profiles": {k: dataclasses.asdict(v) for k, v in RADAR_PROFILES.items()},
            "gnss_profiles": {k: dataclasses.asdict(v) for k, v in GNSS_PROFILES.items()},
            "profile_documentation": "docs/robustness_profiles.md",
            "matrix": matrix,
            "jobs_initial_total": sum(m["jobs_initial"] for m in matrix.values()),
            "jobs_max_total": sum(m["jobs_max"] for m in matrix.values()),
            "seed_schedule": {"stochastic": "seeds 0, 1, 2 first; then 3, 4, ... up to 7 while the standard error over "
                                            "seeds of any pooled metric exceeds its tolerance (robustness.TOLERANCES), "
                                            "decided per (family, level)",
                              "tolerances": robustness.TOLERANCES, "deterministic": "seed 0 only",
                              "streams": "SHA-256 of (seed, sensor, profile, recorder, axis/radar): independent of "
                                         "family, worker and execution order"},
            "max_attempts_per_job": 2, "workers": args.workers,
        },
        "generalization": {"protocol": "configs/heldout/frozen_campaign.yaml", "cases": len(heldout["cases"]),
                           "families": sorted({c["family"] for c in heldout["cases"]}), "seeds": heldout["protocol"]["seeds"],
                           "acceptance": heldout["protocol"]["acceptance"],
                           "recordings": "heldout/frozen_campaign/ (not committed)",
                           "results": "results/generalization/frozen_campaign/"},
        "evaluation": {"report": "scripts/campaign_report.py", "breakdowns": "src/cdf/evaluation/campaign_metrics.py",
                       "ground_truth_use": "evaluation only; never in the reconstruction"},
        "software": versions(),
        "carla": carla_versions(args.port),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=1, default=str) + "\n", encoding="utf-8")
    print("code", manifest["code_sha256"][:16], "config", manifest["reconstruction_config_sha256"][:16],
          "jobs initial", manifest["robustness"]["jobs_initial_total"], "max", manifest["robustness"]["jobs_max_total"])
    for family, m in matrix.items():
        print("  {0:20s} initial {1:4d} max {2:4d}".format(family, m["jobs_initial"], m["jobs_max"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
