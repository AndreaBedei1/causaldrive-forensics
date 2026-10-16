#!/usr/bin/env python3
"""The manifest of the robustness campaign on the 22 canonical runs (the final analysis scope).

    python scripts/campaign_manifest.py [--out results/robustness_campaign_manifest.json]

It records what a reproduction must match: the frozen reconstruction (commit of the tag
``pre-robustness-campaign``, configuration hash, and a hash of the reconstruction sources computed both at that
commit and now, which must be equal), the hash of the current campaign code (``provenance.code_hash``: every job
records it), the hashes of the driver and evaluation scripts, the raw data of the 22 canonical runs, the
perturbation profiles, the experiment matrix with its seed schedule, and the software versions.
``scripts/campaign_controller.py`` refuses to start when the checkout differs from it.

Scope: the campaign was preregistered on 2026-10-15 (tag ``pre-robustness-campaign``) with two further components,
a collision-report latency family and a held-out set of automatically generated scenarios.  Both were removed from
the study on 2026-10-16 by the author's decision on its scientific scope; their code, configuration and results
remain only in the Git history (``robustness-campaign-v2.2``, commit 1183f522).  The retained 35 conditions are
the preregistered ones, run with the frozen reconstruction.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]

FROZEN_TAG = "pre-robustness-campaign"
SCRIPTS = ["robustness.py", "campaign_controller.py", "campaign_report.py", "campaign_manifest.py", "stability_audit.py",
           "validate_canonical.py", "reconstruct_run.py"]
# The reconstruction under test: these sources and the configuration are those of the frozen tag.
RECONSTRUCTION_SOURCES = ("src/cdf/reconstruction", "src/cdf/common", "src/cdf/recording", "src/cdf/perception",
                          "configs/reconstruction.yaml")


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


def _git(*args: str) -> Optional[str]:
    out = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True)
    return out.stdout.decode("utf-8", "replace").strip() if out.returncode == 0 else None


def reconstruction_hash(commit: Optional[str] = None) -> str:
    """SHA-256 over the reconstruction sources (path and content, line endings normalised), from the working tree
    or from a commit's Git objects."""
    digest = hashlib.sha256()
    if commit is None:
        names = []
        for item in RECONSTRUCTION_SOURCES:
            path = ROOT / item
            names += [p.relative_to(ROOT).as_posix() for p in (path.rglob("*.py") if path.is_dir() else [path])]
        contents = {n: (ROOT / n).read_bytes() for n in names}
    else:
        listing = _git("ls-tree", "-r", "--name-only", commit, "--", *RECONSTRUCTION_SOURCES) or ""
        names = [n for n in listing.splitlines() if n.endswith(".py") or n.endswith(".yaml")]
        contents = {}
        for n in names:
            out = subprocess.run(["git", "show", commit + ":" + n], cwd=str(ROOT), capture_output=True)
            contents[n] = out.stdout
    for name in sorted(contents):
        digest.update(name.encode("utf-8") + b"\0")
        digest.update(contents[name].replace(b"\r\n", b"\n") + b"\0")
    return digest.hexdigest()


def versions() -> Dict[str, Any]:
    out: Dict[str, Any] = {"python": sys.version, "platform": platform.platform()}
    try:
        from importlib import metadata
        out["packages"] = {d.metadata["Name"]: d.version for d in sorted(metadata.distributions(),
                                                                        key=lambda d: d.metadata["Name"].lower())}
    except Exception as exc:  # pragma: no cover
        out["packages_error"] = repr(exc)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=ROOT / "results" / "robustness_campaign_manifest.json")
    args = parser.parse_args()
    from cdf.evaluation.provenance import code_hash, config_hash
    from cdf.reconstruction.config import load_config
    from cdf.robustness.perturb import GNSS_PROFILES, RADAR_PROFILES
    import robustness
    from validate_canonical import CANONICAL, canonical_runs
    frozen = _git("rev-parse", FROZEN_TAG + "^{commit}")
    recon_now, recon_frozen = reconstruction_hash(), reconstruction_hash(frozen) if frozen else None
    if recon_frozen is not None and recon_now != recon_frozen:
        raise SystemExit("the reconstruction sources differ from the frozen tag: not this campaign")
    runs = [Path(r) for r in canonical_runs()]
    cfg = load_config()
    matrix = {}
    for family, (levels, stochastic) in robustness.FAMILIES.items():
        jobs3 = sum(len(robustness.jobs_for(ROOT / run, family, [0, 1, 2])) for run in runs)
        jobs8 = sum(len(robustness.jobs_for(ROOT / run, family, list(range(8)))) for run in runs)
        matrix[family] = {"levels": [{"label": label, "parameter": parameter} for label, parameter in levels],
                          "stochastic": stochastic, "jobs_initial": jobs3, "jobs_max": jobs8 if stochastic else jobs3,
                          "configuration": "ablation_mutual_refinement" if family == "gnss_refined" else "frozen"}
    manifest = {
        "name": "robustness campaign on the 22 canonical runs (final analysis scope)",
        "scope": "35 conditions in 12 families on the 22 manually reviewed canonical runs (S01..S19); preregistered "
                 "on 2026-10-15 together with a collision-report latency family and a held-out generalization set, "
                 "both removed from the study on 2026-10-16 (scientific scope); see the module docstring",
        "frozen_reconstruction": {"tag": FROZEN_TAG, "commit": frozen,
                                  "reconstruction_sources": list(RECONSTRUCTION_SOURCES),
                                  "reconstruction_sources_sha256": recon_now,
                                  "reconstruction_sources_sha256_at_tag": recon_frozen,
                                  "reconstruction_config_sha256": config_hash(cfg.to_dict()),
                                  "code_sha256_at_tag": "ac2cb70ad595af1cc12aeb7bd7c89c364baf861dec991599257f9bac4d76f5df"},
        "code_sha256": code_hash(),
        "reconstruction_config_sha256": config_hash(cfg.to_dict()),
        "reconstruction_config": cfg.to_dict(),
        "scripts_sha256": {name: file_hash(ROOT / "scripts" / name) for name in SCRIPTS},
        "sensor_configs_sha256": tree_hash(list((ROOT / "configs" / "sensors").glob("*.yaml")), ROOT),
        "canonical_manifest": {"set": "S01..S19, 22 runs", "variants": CANONICAL,
                               "runs": {(ROOT / run).resolve().relative_to(ROOT.resolve()).as_posix(): raw_hash(ROOT / run)
                                        for run in runs}},
        "robustness": {
            "launcher": "scripts/campaign_controller.py (scripts\\campaign.bat start|status|pause|resume)",
            "radar_profiles": {k: dataclasses.asdict(v) for k, v in RADAR_PROFILES.items()},
            "gnss_profiles": {k: dataclasses.asdict(v) for k, v in GNSS_PROFILES.items()},
            "profile_documentation": "docs/robustness_profiles.md",
            "matrix": matrix,
            "conditions": sum(len(m["levels"]) for m in matrix.values()),
            "jobs_initial_total": sum(m["jobs_initial"] for m in matrix.values()),
            "jobs_max_total": sum(m["jobs_max"] for m in matrix.values()),
            "seed_schedule": {"stochastic": "seeds 0, 1, 2 first; then 3, 4, ... up to 7 while the standard error over "
                                            "seeds of any pooled metric exceeds its tolerance (robustness.TOLERANCES), "
                                            "decided per (family, level)",
                              "tolerances": robustness.TOLERANCES, "deterministic": "seed 0 only",
                              "streams": "SHA-256 of (seed, sensor, profile, recorder, axis/radar): independent of "
                                         "family, worker and execution order, shared by all runs of a seed"},
            "max_attempts_per_job": 2,
        },
        "results": {"jobs": "results/robustness/frozen_campaign/jobs.jsonl.gz",
                    "report": "results/robustness/frozen_campaign/report/"},
        "software": versions(),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=1, default=str) + "\n", encoding="utf-8")
    print("conditions", manifest["robustness"]["conditions"], "jobs initial", manifest["robustness"]["jobs_initial_total"],
          "max", manifest["robustness"]["jobs_max_total"], "| reconstruction unchanged since", FROZEN_TAG,
          recon_now == recon_frozen, "| code", manifest["code_sha256"][:16])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
