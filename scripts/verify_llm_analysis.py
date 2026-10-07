#!/usr/bin/env python3
"""Re-run the deterministic verification of a saved LLM analysis (no model call).

    python scripts/verify_llm_analysis.py traces/S17/run_0_crash/reconstruction/llm/runs/<provider>_<model>_<time>

Loads the reconstructed semantic trace only now, evaluates every formula of
stage2_formula.json (TRUE / FALSE / UNKNOWN / INVALID) and scores the semantic
hypotheses of stage1_explanation.json; writes verification.json and evaluation.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.llm.pipeline import load_llm_config, verify_analysis  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a saved LLM analysis against the semantic trace")
    parser.add_argument("analysis_dir", type=Path)
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    verification, evaluation = verify_analysis(args.analysis_dir, load_llm_config(args.config))
    for row in verification["results"]:
        print("{0:>8} {1}  [{2}] {3}".format(row["result"], row["formula_id"], row["claim_ref"], row["formula_text"]))
    print("summary:", json.dumps(verification["summary"]))
    hypotheses = evaluation.get("semantic_hypotheses") or {}
    print("semantic hypotheses: TP {0} FP {1} FN {2} precision {3} recall {4} F1 {5} hallucination {6} "
          "identity hallucination {7}".format(*(hypotheses.get(k) for k in (
              "TP", "FP", "FN", "precision", "recall", "f1", "hallucination_rate", "identity_hallucination_rate"))))
    print("attribution:", json.dumps(evaluation.get("attribution")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
