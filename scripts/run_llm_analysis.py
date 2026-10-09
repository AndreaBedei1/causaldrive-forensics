#!/usr/bin/env python3
"""Two-stage LLM forensic analysis of one reconstructed run, then deterministic verification.

    python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.8-flash
    python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.5-flash-lite
    python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai
    python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --dry-run
    python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --stage formalize \\
        --analysis-dir traces/S17/run_0_crash/reconstruction/llm/runs/<analysis>

Models (configs/llm.yaml): OpenAI is locked to gpt-6-luna with reasoning effort high (``--model``
with another OpenAI model is refused: changing it is Andrea's decision, made in configs/llm.yaml);
Gemini accepts gemini-3.8-flash (default) and gemini-3.5-flash-lite, both with thinking level high.
One analysis uses one model for both stages; nothing ever falls back to another model.  A quota
error stops the analysis (QUOTA_EXHAUSTED, or INCOMPLETE_QUOTA with Stage 1 saved: complete it
later with the same model, ``--stage formalize --analysis-dir``).

Stage 1 (explanation) and Stage 2 (formalize) are separate calls; ``all`` runs both and then the
verifier.  ``--dry-run`` renders and leak-checks the prompts, prints them and saves
request_preview.json without contacting anyone.  ``--audit-payload`` checks every request body
against the run's semantic trace and privileged files before it is sent (manual integration runs).
A provider without its API key (.env) is reported as unavailable.  ``--oracle-identities`` is
privileged evaluation infrastructure: anonymous tracks are renamed to their true simulator
identities and everything goes to reconstruction/evaluation/llm_oracle/ (never an admissible
analysis).  Keys are checked without generating anything by scripts/check_llm_access.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.llm.guard import LeakGuardError  # noqa: E402
from cdf.llm.pipeline import STAGES, AnalysisOptions, load_llm_config, run_analysis  # noqa: E402
from cdf.llm.providers import PROVIDERS, ModelNotAllowed, ProviderUnavailable  # noqa: E402

EXIT = {"COMPLETED": 0, "OK": 0, "DRY_RUN": 0, "BLOCKED_BY_LEAK_GUARD": 2, "BLOCKED_BY_PAYLOAD_AUDIT": 2,
        "PROVIDER_UNAVAILABLE": 3, "FAILED": 4, "NO_EXPLANATION": 5, "EXPLANATION_UNUSABLE": 5,
        "QUOTA_EXHAUSTED": 6, "INCOMPLETE_QUOTA": 6}


def main() -> int:
    parser = argparse.ArgumentParser(description="LLM abductive forensics with formal verification")
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    parser.add_argument("--model", default=None,
                        help="a model configs/llm.yaml allows (gemini: gemini-3.8-flash or gemini-3.5-flash-lite; "
                             "openai is locked to its configured model)")
    parser.add_argument("--stage", default="all", choices=STAGES)
    parser.add_argument("--dry-run", action="store_true", help="render, check and show the prompts; call nothing")
    parser.add_argument("--analysis-dir", type=Path, default=None,
                        help="continue this analysis (with --stage formalize), always with its own model")
    parser.add_argument("--no-verify", action="store_true", help="do not run the verifier after Stage 2")
    parser.add_argument("--audit-payload", action="store_true",
                        help="check every request body against the run's semantic trace and privileged files "
                             "before it is sent (privileged audit for manual integration runs)")
    parser.add_argument("--oracle-identities", action="store_true",
                        help="PRIVILEGED evaluation only: give the model the true identities of anonymous tracks")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--quiet", action="store_true", help="with --dry-run, do not print the prompts")
    args = parser.parse_args()
    options = AnalysisOptions(provider=args.provider, model=args.model, stage=args.stage, dry_run=args.dry_run,
                              oracle_identities=args.oracle_identities, analysis_dir=args.analysis_dir,
                              verify=not args.no_verify, audit_payload=args.audit_payload)
    try:
        result = run_analysis(args.run_dir, options, load_llm_config(args.config), echo=print)
    except ModelNotAllowed as error:
        print("REFUSED (nothing was sent): {0}".format(error), file=sys.stderr)
        return 7
    except LeakGuardError as error:
        print("BLOCKED by the leak guard (nothing was sent): {0}".format(error), file=sys.stderr)
        return 2
    except ProviderUnavailable as error:
        print("provider unavailable: {0}".format(error), file=sys.stderr)
        return 3
    if result.status == "DRY_RUN" and not args.quiet:
        for stage, prompt in result.previews.items():
            print("=" * 100)
            print("STAGE {0}: template {1} (sha256 {2})".format(stage, prompt.template, prompt.template_sha256[:16]))
            print("-" * 40 + " SYSTEM " + "-" * 40)
            print(prompt.system)
            print("-" * 40 + " USER (packet abridged) " + "-" * 40)
            print(prompt.user.replace(prompt.packet_json, "<forensic_packet.json, {0} characters>".format(
                len(prompt.packet_json))))
    for message in result.messages:
        print(message, file=sys.stderr)
    print("{0}: {1}".format(result.status, result.analysis_dir if result.analysis_dir.exists() else "nothing written"))
    return EXIT.get(result.status, 1)


if __name__ == "__main__":
    raise SystemExit(main())
