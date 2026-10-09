#!/usr/bin/env python3
"""Compare LLM analyses of one run (same forensic packet) side by side; no model call.

    python scripts/compare_llm_analyses.py traces/S17/run_0_crash <analysis_dir> [<analysis_dir> ...]
        [--unanswered <analysis_dir> ...] [--assessment assessment.md] [--out-name llm_comparison_S17]

Writes reconstruction/evaluation/<out-name>.md and .json: this is a privileged evaluation artifact
(it may set the answers against the ground truth of the run, e.g. who the anonymous tracks were), so
it lives with the other evaluation outputs and is never given to a model.  Four things are kept
apart, because a TRUE formula is formal consistency with the reconstructed trace, not proof of a
causal explanation:

1. causal-abductive quality (who and what started the conflict; read against the privileged
   reference of the run);
2. semantic event reconstruction (the Stage-1 hypotheses scored against the reconstructed semantic
   trace: TP / FP / FN, precision, recall, F1);
3. temporal-formula consistency (the verifier's TRUE / FALSE / UNKNOWN / INVALID);
4. identity hallucinations (ids that are not entities of the packet).

Costs are computed only where the provider returns the usage and configs/llm.yaml holds the published
price (OpenAI); otherwise none is stated.  ``--unanswered`` lists analyses that ended without an answer
(provider errors, quota) with every request's HTTP status.  ``--assessment`` appends an analyst's written
assessment, clearly labelled as such.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.llm.pipeline import load_llm_config  # noqa: E402


def _read(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _num(value: Any) -> int:
    return int(value or 0)


def _usage(stages: Dict[str, Any]) -> Dict[str, Any]:
    out = {"per_stage": {}, "total": {}}
    for stage, entry in stages.items():
        usage = entry.get("usage") or {}
        out["per_stage"][stage] = {"input_tokens": usage.get("input_tokens"),
                                   "cached_input_tokens": usage.get("cached_input_tokens"),
                                   "output_tokens": usage.get("output_tokens"),
                                   "reasoning_tokens": usage.get("reasoning_tokens"),
                                   "total_tokens": usage.get("total_tokens"),
                                   "latency_s": entry.get("latency_s"), "response_id": entry.get("response_id"),
                                   "model_reported": entry.get("model_reported"),
                                   "finish_reason": entry.get("finish_reason")}
    for key in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens", "total_tokens"):
        out["total"][key] = sum(_num(row[key]) for row in out["per_stage"].values())
    out["total"]["latency_s"] = round(sum(float(row["latency_s"] or 0.0) for row in out["per_stage"].values()), 3)
    return out


def _cost(provider: str, usage: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """USD from the returned usage and the published list price in configs/llm.yaml; None without a price."""
    prices = (config["providers"].get(provider) or {}).get("pricing_usd_per_1m_tokens")
    if not prices:
        return None
    total = usage["total"]
    cached = total["cached_input_tokens"]
    uncached = total["input_tokens"] - cached
    usd = (uncached * prices["input"] + cached * prices["cached_input"] + total["output_tokens"] * prices["output"]) / 1e6
    return {"usd": round(usd, 6), "basis": "returned usage x published list price ({0}, as of {1}); output tokens "
                                          "include reasoning tokens".format(prices.get("source"), prices.get("as_of")),
            "prices_usd_per_1m": {k: prices[k] for k in ("input", "cached_input", "output")}}


def summarise(analysis_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    analysis_dir = Path(analysis_dir)
    metadata = _read(analysis_dir / "request_metadata.json")
    stage1 = _read(analysis_dir / "stage1_explanation.json") if (analysis_dir / "stage1_explanation.json").exists() else {}
    stage2 = _read(analysis_dir / "stage2_formula.json") if (analysis_dir / "stage2_formula.json").exists() else {}
    verification = _read(analysis_dir / "verification.json") if (analysis_dir / "verification.json").exists() else {}
    evaluation = _read(analysis_dir / "evaluation.json") if (analysis_dir / "evaluation.json").exists() else {}
    audit = _read(analysis_dir / "payload_audit.json") if (analysis_dir / "payload_audit.json").exists() else None
    answer = stage1.get("answer") or {}
    issues = (stage1.get("validation") or {}).get("issues", [])
    hallucinated = sorted({str(i["value"]) for i in issues if i["code"] == "INVALID_IDENTITY_HALLUCINATION"})
    bad_facts = [i for i in issues if i["code"] == "INVALID_EVIDENCE_REFERENCE"]
    cited = sum(len(step.get("evidence_fact_ids") or []) for step in answer.get("causal_chain") or [])
    cited += sum(len(h.get("evidence_fact_ids") or []) for h in answer.get("semantic_hypotheses") or [])
    cited += sum(len(h.get("evidence_fact_ids") or []) for h in answer.get("alternative_hypotheses") or [])
    formulas = (stage2.get("validation") or {}).get("formulas", [])
    usage = _usage(metadata.get("stages") or {})
    return {
        "analysis_dir": str(analysis_dir.relative_to(ROOT)) if analysis_dir.is_absolute() else str(analysis_dir),
        "provider": metadata.get("provider"), "model": metadata.get("model"),
        "models_reported": sorted({str(row.get("model_reported")) for row in usage["per_stage"].values()}),
        "generation_settings": metadata.get("generation_settings"), "status": metadata.get("status"),
        "forensic_packet_sha256": metadata.get("forensic_packet_sha256"),
        "prompt_versions": metadata.get("prompt_versions"), "created_at": metadata.get("created_at"),
        "stage1": {"validation_status": (stage1.get("validation") or {}).get("status"),
                   "explanation": answer.get("explanation"), "primary_hypothesis": answer.get("primary_hypothesis"),
                   "responsibility": answer.get("responsibility"), "causal_chain": answer.get("causal_chain"),
                   "alternative_hypotheses": answer.get("alternative_hypotheses"),
                   "unresolved_entities": answer.get("unresolved_entities"),
                   "identity_hallucinations": hallucinated, "cited_fact_ids": cited,
                   "invalid_fact_references": len(bad_facts),
                   "issue_counts": evaluation.get("stage1_issue_counts")},
        "semantic_hypotheses": evaluation.get("semantic_hypotheses"),
        "attribution": evaluation.get("attribution"),
        "stage2": {"validation_status": (stage2.get("validation") or {}).get("status"),
                   "formulas": len(formulas), "valid": sum(1 for f in formulas if f.get("ast_valid")),
                   "invalid": sum(1 for f in formulas if not f.get("ast_valid")),
                   "untestable_claims": (stage2.get("answer") or {}).get("untestable_claims") or []},
        "verifier": {"summary": verification.get("summary"),
                     "results": [{key: row.get(key) for key in ("formula_id", "claim_ref", "formula_text", "result")}
                                 for row in verification.get("results") or []]},
        "security": {"leak_guard": "PASS (packet and prompts checked before each request; the analysis ran)"
                     if metadata.get("status") not in ("BLOCKED_BY_LEAK_GUARD",) else "BLOCKED",
                     "payload_audit": None if audit is None else [row["result"] for row in audit["requests"]],
                     "embedded_packet_sha256": None if audit is None else sorted(
                         {row["embedded_packet_sha256"] for row in audit["requests"]}),
                     "identity_hallucination_rate": (evaluation.get("semantic_hypotheses") or {}).get(
                         "identity_hallucination_rate")},
        "usage": usage, "cost": _cost(metadata.get("provider"), usage, config),
    }


def unanswered(analysis_dir: Path) -> Dict[str, Any]:
    """An analysis that produced no answer: its status and the HTTP status of every request it sent."""
    analysis_dir = Path(analysis_dir)
    metadata = _read(analysis_dir / "request_metadata.json")
    stages = {}
    for stage, entry in (metadata.get("stages") or {}).items():
        attempts = entry.get("attempts") or []
        last_error = attempts[-1].get("error") if attempts else entry.get("error")
        details = (((attempts[-1].get("error_body") or {}) if attempts else {}).get("error") or {}).get("details") or []
        quotas = ["{0} (limit {1})".format(v.get("quotaId"), v.get("quotaValue"))
                  for d in details if isinstance(d, dict) for v in d.get("violations") or [] if v.get("quotaId")]
        if quotas:
            last_error = "quota exceeded: " + ", ".join(quotas)
        stages[stage] = {"status": entry.get("status"), "started_at": entry.get("started_at"),
                         "http_statuses": [a.get("status") for a in attempts],
                         "error_kinds": [a.get("kind") for a in attempts], "last_error": last_error}
    return {"analysis_dir": str(analysis_dir.relative_to(ROOT)) if analysis_dir.is_absolute() else str(analysis_dir),
            "provider": metadata.get("provider"), "model": metadata.get("model"), "status": metadata.get("status"),
            "forensic_packet_sha256": metadata.get("forensic_packet_sha256"), "stages": stages}


def _fmt(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return "{0:.3f}".format(value).rstrip("0").rstrip(".") if abs(value) < 1000 else "{0:.0f}".format(value)
    return str(value)


def _label(item: Dict[str, Any]) -> str:
    settings = item.get("generation_settings") or {}
    level = settings.get("reasoning_effort") or settings.get("thinking_level")
    return "{0} ({1})".format(item["model"], level)


def render(run_dir: Path, items: List[Dict[str, Any]], assessment: Optional[str],
           failed: Optional[List[Dict[str, Any]]] = None) -> str:
    labels = [_label(item) for item in items]

    def row(name: str, values: List[Any]) -> str:
        return "| {0} | {1} |".format(name, " | ".join(_fmt(v) for v in values))

    head = "| | " + " | ".join(labels) + " |\n|---|" + "---|" * len(items)
    lines = ["# LLM comparison: {0}".format(run_dir.as_posix().split("traces/")[-1]), "",
             "PRIVILEGED evaluation artifact (reconstruction/evaluation/): it may cite the run's ground truth; it is "
             "never given to a model.  Every model received the same forensic packet, prompts, vocabulary, grammar "
             "and output schemas; each analysis used one model for both stages.  A TRUE formula means the temporal "
             "hypothesis is consistent with the reconstructed semantic trace, not that the causal explanation is "
             "proven.", "", "## Models", "", head]
    lines.append(row("provider", [i["provider"] for i in items]))
    lines.append(row("exact model id (requested)", [i["model"] for i in items]))
    lines.append(row("model reported by the API", [", ".join(i["models_reported"]) for i in items]))
    lines.append(row("reasoning / thinking", [json.dumps(i["generation_settings"]) for i in items]))
    lines.append(row("forensic packet SHA-256", [(i["forensic_packet_sha256"] or "")[:16] for i in items]))
    lines.append(row("embedded packet SHA-256 (audit)", [", ".join(x[:16] for x in (i["security"]["embedded_packet_sha256"] or []))
                                                         for i in items]))
    lines.append(row("prompt versions", [json.dumps(i["prompt_versions"]) for i in items]))
    lines.append(row("status", [i["status"] for i in items]))
    if failed:
        lines += ["", "### Analyses that ended without an answer", "",
                  "| analysis | model | status | stage: HTTP status of each request | last error |",
                  "|---|---|---|---|---|"]
        for entry in failed:
            for stage, info in entry["stages"].items():
                lines.append("| {0} | {1} | {2} | {3}: {4} | {5} |".format(
                    Path(entry["analysis_dir"]).name, entry["model"], entry["status"], stage,
                    ", ".join(str(code) for code in info["http_statuses"]),
                    " ".join((info["last_error"] or "").split()).replace("|", "/")[:160]))
        requests = sum(len(info["http_statuses"]) for entry in failed for info in entry["stages"].values())
        lines += ["", "{0} analyses, {1} requests, no answer (a failed request generates nothing; on the free "
                  "tier it still counts against the daily request quota).".format(len(failed), requests)]
    lines += ["", "## 1. Causal-abductive answer (Stage 1)", "", head]
    lines.append(row("validation", [i["stage1"]["validation_status"] for i in items]))
    lines.append(row("responsible actor", [(i["stage1"]["responsibility"] or {}).get("actor") for i in items]))
    lines.append(row("attribution kind", [(i["attribution"] or {}).get("kind") for i in items]))
    lines.append(row("confidence", [(i["stage1"]["responsibility"] or {}).get("confidence") for i in items]))
    lines.append(row("causal chain steps", [len(i["stage1"]["causal_chain"] or []) for i in items]))
    lines.append(row("alternative hypotheses", [len(i["stage1"]["alternative_hypotheses"] or []) for i in items]))
    lines.append(row("unresolved entities", [", ".join(e.get("entity_id", "?") for e in i["stage1"]["unresolved_entities"] or [])
                                            for i in items]))
    lines.append(row("identity hallucinations", [", ".join(i["stage1"]["identity_hallucinations"]) or "none"
                                                for i in items]))
    lines.append(row("cited fact ids / invalid", ["{0} / {1}".format(i["stage1"]["cited_fact_ids"],
                                                                       i["stage1"]["invalid_fact_references"])
                                                 for i in items]))
    for item, label in zip(items, labels):
        s1 = item["stage1"]
        lines += ["", "### {0}".format(label), "", "**Primary hypothesis.** {0}".format(s1["primary_hypothesis"]), "",
                  "**Explanation.** {0}".format(s1["explanation"]), "",
                  "**Responsibility.** {0} (confidence {1}): {2}".format(
                      (s1["responsibility"] or {}).get("actor"), (s1["responsibility"] or {}).get("confidence"),
                      (s1["responsibility"] or {}).get("assessment")), ""]
        limitations = (s1["responsibility"] or {}).get("limitations") or []
        if limitations:
            lines += ["Limitations stated: " + "; ".join(limitations), ""]
        lines += ["Causal chain:", ""]
        for step in s1["causal_chain"] or []:
            lines.append("{0}. [{1} {2}] {3} (actor {4}; facts {5})".format(
                step.get("step"), step.get("time_reference"), _fmt(step.get("estimated_time")), step.get("claim"),
                step.get("actor_id"), ", ".join(step.get("evidence_fact_ids") or [])))
        if s1["alternative_hypotheses"]:
            lines += ["", "Alternatives:", ""]
            for alt in s1["alternative_hypotheses"]:
                lines.append("- {0} (responsible {1}, plausibility {2})".format(
                    alt.get("hypothesis"), alt.get("responsible_actor"), _fmt(alt.get("plausibility"))))
        if s1["unresolved_entities"]:
            lines += ["", "Unresolved entities:", ""]
            for entity in s1["unresolved_entities"]:
                lines.append("- {0}: {1} ({2})".format(entity.get("entity_id"), entity.get("role"), entity.get("reason")))
    lines += ["", "## 2. Semantic event hypotheses (scored against the reconstructed semantic trace)", "", head]
    for key in ("hypotheses", "reference_events", "TP", "FP", "FN", "precision", "recall", "f1",
                "hallucination_rate", "identity_hallucination_rate", "mean_abs_time_error_s"):
        lines.append(row(key, [(i["semantic_hypotheses"] or {}).get(key) for i in items]))
    for item, label in zip(items, labels):
        rows = (item["semantic_hypotheses"] or {}).get("per_hypothesis") or []
        lines += ["", "### {0}: proposed nodes".format(label), "", "| event | actor | subject | time | outcome |",
                  "|---|---|---|---|---|"]
        for hyp in rows:
            lines.append("| {0} | {1} | {2} | {3} {4} | {5}{6} |".format(
                hyp["event_type"], hyp["actor_id"], hyp["subject_id"] or "-", hyp["time_reference"],
                _fmt(hyp["estimated_time"]), hyp["outcome"],
                "" if hyp["outcome"] != "TP" else " ({0:+.2f} s)".format(
                    (hyp.get("matched_event") or {}).get("t_global", 0) - (hyp["estimated_time"] or 0)
                    if hyp["time_reference"] == "GLOBAL" and hyp["estimated_time"] is not None else 0.0)))
    lines += ["", "## 3. Formulas (Stage 2) and verification", "", head]
    lines.append(row("Stage-2 validation", [i["stage2"]["validation_status"] for i in items]))
    lines.append(row("formulas", [i["stage2"]["formulas"] for i in items]))
    lines.append(row("valid / invalid", ["{0} / {1}".format(i["stage2"]["valid"], i["stage2"]["invalid"]) for i in items]))
    lines.append(row("untestable claims", [len(i["stage2"]["untestable_claims"]) for i in items]))
    for label_key in ("TRUE", "FALSE", "UNKNOWN", "INVALID"):
        lines.append(row("verifier " + label_key, [(i["verifier"]["summary"] or {}).get(label_key) for i in items]))
    for item, label in zip(items, labels):
        lines += ["", "### {0}: formulas".format(label), "", "| id | claim | formula | result |", "|---|---|---|---|"]
        for result in item["verifier"]["results"]:
            lines.append("| {0} | {1} | `{2}` | {3} |".format(result["formula_id"], result["claim_ref"],
                                                             result["formula_text"], result["result"]))
        if item["stage2"]["untestable_claims"]:
            lines += ["", "Untestable claims:", ""]
            for claim in item["stage2"]["untestable_claims"]:
                lines.append("- {0}: {1} ({2})".format(claim.get("claim_ref"), claim.get("claim"), claim.get("reason")))
    lines += ["", "## 4. Security", "", head]
    lines.append(row("leak guard", [i["security"]["leak_guard"] for i in items]))
    lines.append(row("pre-send payload audit", [", ".join(i["security"]["payload_audit"] or []) for i in items]))
    lines.append(row("identity hallucination rate", [i["security"]["identity_hallucination_rate"] for i in items]))
    lines += ["", "## 5. Usage and cost", "", head]
    for key in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens", "total_tokens", "latency_s"):
        lines.append(row(key + " (both stages)", [i["usage"]["total"][key] for i in items]))
    for stage in ("explanation", "formalize"):
        lines.append(row(stage + ": in / out / reasoning, s", [
            "{0} / {1} / {2}, {3}".format(*(_fmt((i["usage"]["per_stage"].get(stage) or {}).get(k))
                                            for k in ("input_tokens", "output_tokens", "reasoning_tokens",
                                                      "latency_s"))) for i in items]))
        lines.append(row(stage + ": response id", [(i["usage"]["per_stage"].get(stage) or {}).get("response_id")
                                                   for i in items]))
    lines.append(row("cost (USD)", ["{0:.4f}".format(i["cost"]["usd"]) if i["cost"] else "not stated (no published "
                                    "price in the configuration; free tier)" for i in items]))
    costs = [i["cost"] for i in items if i["cost"]]
    if costs:
        lines += ["", "Cost basis: " + costs[0]["basis"] + "."]
    lines += ["", "Gemini token counts: output tokens exclude the thinking tokens (thoughtsTokenCount, shown as "
              "reasoning); OpenAI: output tokens include the reasoning tokens."]
    if assessment:
        lines += ["", "## 6. Analyst assessment (written after reading the answers; not computed)", "", assessment.strip()]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("analysis_dirs", type=Path, nargs="+")
    parser.add_argument("--unanswered", type=Path, nargs="*", default=[],
                        help="analyses that ended without an answer (listed with their HTTP statuses)")
    parser.add_argument("--assessment", type=Path, default=None)
    parser.add_argument("--out-name", default="llm_comparison")
    args = parser.parse_args()
    config = load_llm_config()
    items = [summarise(path, config) for path in args.analysis_dirs]
    failed = [unanswered(path) for path in args.unanswered]
    digests = {item["forensic_packet_sha256"] for item in items + failed}
    if len(digests) != 1:
        print("STOP: the analyses did not receive the same forensic packet: {0}".format(sorted(digests)),
              file=sys.stderr)
        return 2
    out_dir = args.run_dir / "reconstruction" / "evaluation"
    out_dir.mkdir(parents=True, exist_ok=True)
    assessment = args.assessment.read_text(encoding="utf-8") if args.assessment else None
    report = {"run": str(args.run_dir), "analyses": items, "unanswered": failed}
    (out_dir / (args.out_name + ".json")).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                                     encoding="utf-8")
    (out_dir / (args.out_name + ".md")).write_text(render(args.run_dir, items, assessment, failed), encoding="utf-8")
    print(out_dir / (args.out_name + ".md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
