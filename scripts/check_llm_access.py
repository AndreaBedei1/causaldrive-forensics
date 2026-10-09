#!/usr/bin/env python3
"""Check the LLM API keys and model access without generating anything (no tokens, no cost).

    python scripts/check_llm_access.py

OpenAI: GET /v1/models/<model> (model retrieval).  Gemini: GET /v1beta/models/<model> (models.get).
Every configured model is checked (OpenAI: the locked model; Gemini: primary and secondary).  Only
VALID / INVALID and YES / NO are printed; a failure is described by its HTTP status and the provider's
error status, with every secret redacted.  The keys come from the environment or .env and are never
printed, logged or written (not even their length or a part of them).  Access to a model here means
its metadata is served to the key; quotas are only seen by a generation request.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.common.config import repo_root  # noqa: E402
from cdf.llm.pipeline import load_llm_config  # noqa: E402
from cdf.llm.providers import allowed_models, make_provider  # noqa: E402

LABELS = {"openai": "OpenAI", "gemini": "Gemini"}


def _word(value, yes, no):
    return yes if value is True else (no if value is False else "UNKNOWN")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--details", action="store_true", help="also print the non-secret model metadata (limits)")
    args = parser.parse_args()
    config = load_llm_config(args.config)
    env_file = repo_root() / str(config.get("env_file", ".env"))
    ok = True
    for name in ("openai", "gemini"):
        settings = dict(config["providers"][name])
        key_line, model_lines = None, []
        for model in allowed_models(settings):
            provider = make_provider(name, settings, model=model, env_file=env_file)
            result = provider.check_access()
            if key_line is None or result["key_valid"] is not None:
                key_line = "{0} API key: {1}".format(LABELS[name], _word(result["key_valid"], "VALID", "INVALID")
                                                     if provider.available else "MISSING")
            line = "{0} access: {1}".format(model, _word(result["model_access"], "YES", "NO"))
            if result["model_access"] is not True:
                ok = False
                line += "  (HTTP {0}: {1})".format(result["http_status"], result["error"])
            model_lines.append(line)
            if args.details and result["model_metadata"]:
                model_lines.append("    " + json.dumps(result["model_metadata"], sort_keys=True))
        print(key_line)
        for line in model_lines:
            print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
