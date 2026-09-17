#!/usr/bin/env python
"""Re-hash recorded runs and check them against their evidence manifests.

::

    python scripts/verify_evidence.py --artifacts artifacts
    python scripts/verify_evidence.py --run artifacts/S01_rear_end/seed_000_crash

`evidence_manifest.json` records a SHA-256 of every file a run directory held
when it was written. This is the other half of that: a manifest nobody checks
proves nothing.

Three kinds of disagreement are reported separately, because they mean different
things. A **missing** or **changed** file means the run directory no longer holds
the evidence it claims to, and the run fails verification. An **unlisted** file
is a file on disk the manifest does not mention -- normal when later stages have
added artifacts since the manifest was written, which is why each manifest
records the stage that wrote it. Refresh a stale manifest with

    python scripts/reprocess_runs.py --artifacts artifacts --stages manifest

Exit status is 0 when every run verified, 1 otherwise.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cdf.common.io import verify_evidence_manifest  # noqa: E402


def discover_runs(artifacts_root: Path) -> List[Path]:
    """Every recorded run, counterfactual replays and ablation runs included."""
    return [m.parent for m in sorted(artifacts_root.rglob("manifest.json"))
            if m.parent.name != "summary"]


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--run", dest="runs", action="append", default=None,
                        help="verify only this run; repeat for several")
    parser.add_argument("--show-unlisted", action="store_true",
                        help="also list files the manifest does not mention")
    args = parser.parse_args(argv)

    runs = ([Path(r) for r in args.runs] if args.runs
            else discover_runs(Path(args.artifacts)))
    if not runs:
        print("no runs found under {0}".format(args.artifacts))
        return 1

    failures: List[Dict[str, Any]] = []
    no_manifest = 0
    for run_dir in runs:
        report = verify_evidence_manifest(run_dir)
        if not report["ok"] and report.get("reason"):
            no_manifest += 1
            print("  {0:<62} NO MANIFEST".format(str(run_dir)[-62:]))
            continue
        status = "ok" if report["ok"] else "FAILED"
        extra = ""
        if report["missing"]:
            extra += " missing={0}".format(len(report["missing"]))
        if report["changed"]:
            extra += " changed={0}".format(len(report["changed"]))
        if report["unlisted"]:
            extra += " unlisted={0}".format(len(report["unlisted"]))
        print("  {0:<62} {1:<7} {2} file(s){3}".format(
            str(run_dir)[-62:], status, report["n_files"], extra))
        if args.show_unlisted:
            for rel in report["unlisted"]:
                print("        unlisted: {0}".format(rel))
        if not report["ok"]:
            failures.append(dict(report, run=str(run_dir)))
            for rel in report["missing"]:
                print("        MISSING: {0}".format(rel))
            for rel in report["changed"]:
                print("        CHANGED: {0}".format(rel))

    print("")
    print("{0} run(s) checked, {1} verified, {2} failed, {3} without a manifest".format(
        len(runs), len(runs) - len(failures) - no_manifest, len(failures), no_manifest))
    return 0 if not failures and not no_manifest else 1


if __name__ == "__main__":
    raise SystemExit(main())
