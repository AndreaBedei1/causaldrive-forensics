#!/usr/bin/env python3
"""Export the admissible forensic facts of reconstructed runs (the only input an LLM may see).

    python scripts/export_forensic_facts.py traces/S17/run_0_crash
    python scripts/export_forensic_facts.py traces/S*/run_*

Writes ``<run>/reconstruction/llm/forensic_facts.jsonl``, ``forensic_packet.json``
and ``export_manifest.json``.  The packet passes the leak guard before it is
written; a violation aborts the export.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.llm.facts import export_forensic_facts  # noqa: E402
from cdf.llm.guard import LeakGuardError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Export admissible forensic facts for LLM analysis")
    parser.add_argument("run_dirs", nargs="+", type=Path)
    args = parser.parse_args()
    status = 0
    for run_dir in args.run_dirs:
        try:
            summary = export_forensic_facts(run_dir)
        except LeakGuardError as error:
            print("{0}: BLOCKED by the leak guard: {1}".format(run_dir, error), file=sys.stderr)
            status = 2
            continue
        print("{0}: {1} facts {2} -> {3} (run_id {4}, packet sha256 {5})".format(
            run_dir, summary["facts"], summary["fact_counts"], summary["output_dir"], summary["run_id"],
            summary["forensic_packet_sha256"][:16]))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
