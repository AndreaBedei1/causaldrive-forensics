"""FACTS -> abductive explanation -> semantic hypotheses -> formula -> verification.

    forensic packet (admissible facts only, leak-guarded)
      -> Stage 1, one call: explanation + causal chain + responsibility + semantic hypotheses
      -> Stage 2, a separate call: the testable temporal claims as formulas (text + AST)
      -> both answers saved
      -> only now the semantic trace is loaded: three-valued verification of each formula,
         scoring of the semantic hypotheses (no model call)

Layout: ``<run>/reconstruction/llm/runs/<provider>_<model>_<UTC timestamp>/`` with
``request_metadata.json``, ``stage1_explanation.json``, ``stage2_formula.json``,
``verification.json``, ``evaluation.json`` (``request_preview.json`` for a dry
run; ``payload_audit.json`` with ``--audit-payload``).  Oracle-identity analyses
go under ``reconstruction/evaluation/llm_oracle/``.  Nothing here writes into
the reconstruction or feeds anything back into it.

One analysis, one model: Stage 1 and Stage 2 are always answered by the same
provider and model (recorded in ``request_metadata.json``); continuing an
analysis with another model is refused.  A quota error stops the analysis
(``QUOTA_EXHAUSTED`` at Stage 1, ``INCOMPLETE_QUOTA`` at Stage 2 with Stage 1
saved); nothing switches to another model.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml

from ..common.config import configs_dir, repo_root
from .evaluation import ScoringConfig, attribution_check, score_semantic_hypotheses
from .facts import (FACTS_SCHEMA_VERSION, PACKET_SCHEMA_VERSION, export_forensic_facts, load_packet,
                    packet_fact_ids, packet_sha256, sha256_text)
from .formal.grammar import GRAMMAR_VERSION
from .formal.parser import ast_from_table
from .formal.verifier import SEMANTICS, SemanticTrace
from .guard import LeakGuardError, check_packet, check_request
from .payload_audit import PayloadAuditError, PayloadAuditor
from .prompts import DEFAULT_PROMPTS, render_explanation, render_formalization
from .providers import ModelNotAllowed, ProviderError, ProviderUnavailable, allowed_models, make_provider
from .providers.base import Transport
from .schemas import (STAGE1_SCHEMA_VERSION, STAGE2_SCHEMA_VERSION, known_ids, stage1_schema, stage2_schema,
                      validate_stage1, validate_stage2)
from .vocabulary import load_vocabulary

STAGES = ("explanation", "formalize", "all")
STAGE1_FILE, STAGE2_FILE = "stage1_explanation.json", "stage2_formula.json"
DETERMINISM_NOTE = ("Model outputs are not reproducible: the reasoning models are sampled with their default "
                    "settings (no temperature or seed is pinned; reasoning effort / thinking level is recorded); "
                    "repeat runs are needed to measure the variation.")


def load_llm_config(path: Optional[Path] = None) -> Dict[str, Any]:
    data = yaml.safe_load(Path(path or configs_dir() / "llm.yaml").read_text(encoding="utf-8"))
    return data["llm"]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _utc_stamp() -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())


def _utc_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9.\-]+", "-", text).strip("-") or "model"


def _code_version() -> Optional[str]:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo_root()),
                                      stderr=subprocess.DEVNULL, timeout=10)
        return out.decode("ascii").strip()
    except (OSError, subprocess.SubprocessError):
        return None


def run_dir_of(analysis_dir: Path) -> Path:
    """The run directory an analysis directory belongs to."""
    analysis_dir = Path(analysis_dir).resolve()
    runs = analysis_dir.parent
    if runs.name != "runs":
        raise ValueError("{0} is not inside a runs/ directory".format(analysis_dir))
    if runs.parent.name == "llm":  # <run>/reconstruction/llm/runs/<x>
        return runs.parent.parent.parent
    if runs.parent.name == "llm_oracle":  # <run>/reconstruction/evaluation/llm_oracle/runs/<x>
        return runs.parent.parent.parent.parent
    raise ValueError("{0} is not an analysis directory".format(analysis_dir))


@dataclass
class AnalysisOptions:
    provider: str
    model: Optional[str] = None
    stage: str = "all"
    dry_run: bool = False
    oracle_identities: bool = False
    analysis_dir: Optional[Path] = None
    verify: bool = True
    audit_payload: bool = False


@dataclass
class AnalysisResult:
    analysis_dir: Path
    status: str
    messages: List[str] = field(default_factory=list)
    previews: Dict[str, Any] = field(default_factory=dict)


def _packet_for(run_dir: Path, oracle: bool) -> Dict[str, Any]:
    path = Path(run_dir) / "reconstruction" / "llm" / "forensic_packet.json"
    if not path.exists():
        export_forensic_facts(run_dir)
    packet = load_packet(run_dir)
    if not oracle:
        return packet
    from .oracle import oracle_identity_map, oracle_packet, save_oracle_packet, write_oracle_identities

    write_oracle_identities(run_dir)
    packet = oracle_packet(packet, oracle_identity_map(run_dir))
    save_oracle_packet(run_dir, packet)
    return packet


def _base_dir(run_dir: Path, oracle: bool) -> Path:
    if oracle:
        from .oracle import oracle_dir

        return oracle_dir(run_dir) / "runs"
    return Path(run_dir) / "reconstruction" / "llm" / "runs"


def _continued_model(analysis_dir: Path, provider: str, model: Optional[str]) -> str:
    """The model of an analysis being continued: one analysis, one provider and one model, always."""
    metadata = _read_json(Path(analysis_dir) / "request_metadata.json")
    if metadata.get("provider") != provider:
        raise ModelNotAllowed("{0} was started with provider {1}; it cannot be continued with {2}".format(
            analysis_dir, metadata.get("provider"), provider))
    if model and model != metadata.get("model"):
        raise ModelNotAllowed("one analysis uses one model: {0} was started with {1}; {2!r} is refused (start a new "
                              "analysis for another model)".format(analysis_dir, metadata.get("model"), model))
    return str(metadata.get("model"))


def _latest_with_stage1(base: Path, prefix: str) -> Optional[Path]:
    candidates = sorted(path for path in base.glob(prefix + "_*") if (path / STAGE1_FILE).exists()
                        and not path.name.endswith("_dryrun"))
    return candidates[-1] if candidates else None


def run_analysis(run_dir: Path, options: AnalysisOptions, config: Optional[Dict[str, Any]] = None,
                 transport: Optional[Transport] = None, echo: Callable[[str], None] = lambda _: None) -> AnalysisResult:
    if options.stage not in STAGES:
        raise ValueError("stage must be one of {0}".format(", ".join(STAGES)))
    run_dir = Path(run_dir)
    config = config or load_llm_config()
    vocabulary = load_vocabulary()
    settings = dict((config.get("providers") or {}).get(options.provider) or {})
    if not settings:
        raise ProviderUnavailable("provider {0!r} is not configured in configs/llm.yaml".format(options.provider))
    env_file = repo_root() / str(config.get("env_file", ".env"))
    model = options.model
    if options.analysis_dir is not None and (Path(options.analysis_dir) / "request_metadata.json").exists():
        model = _continued_model(Path(options.analysis_dir), options.provider, options.model)
    provider = make_provider(options.provider, settings, model=model, env_file=env_file, transport=transport)
    prompts = dict(DEFAULT_PROMPTS, **(config.get("prompts") or {}))

    packet = _packet_for(run_dir, options.oracle_identities)
    check_packet(packet)  # fail closed before anything else
    digest = packet_sha256(packet)
    base = _base_dir(run_dir, options.oracle_identities)
    prefix = "{0}_{1}".format(provider.name, _slug(provider.model))
    if options.analysis_dir is not None:
        analysis_dir = Path(options.analysis_dir)
    elif options.stage == "formalize":
        analysis_dir = _latest_with_stage1(base, prefix)
        if analysis_dir is None:
            raise FileNotFoundError("no earlier explanation for {0} under {1}; run --stage explanation first".format(
                prefix, base))
    else:
        analysis_dir = base / "{0}_{1}{2}".format(prefix, _utc_stamp(), "_dryrun" if options.dry_run else "")
    if not options.dry_run and not provider.available:
        # Nothing can be sent: report it, write nothing.
        return AnalysisResult(analysis_dir=analysis_dir, status="PROVIDER_UNAVAILABLE", messages=[
            "{0} is unavailable: set {1} in .env (see .env.example)".format(provider.name, provider.api_key_env)])
    analysis_dir.mkdir(parents=True, exist_ok=True)
    if options.oracle_identities:
        from .oracle import NOTICE, oracle_identity_map

        _write_json(analysis_dir / "oracle_identities.json",
                    {"_notice": NOTICE, "identities": oracle_identity_map(run_dir)})

    metadata_path = analysis_dir / "request_metadata.json"
    if metadata_path.exists():
        _continued_model(analysis_dir, provider.name, provider.model)  # one analysis, one model
    metadata = _read_json(metadata_path) if metadata_path.exists() else {
        "provider": provider.name, "model": provider.model, "api_key_env": provider.api_key_env,
        "model_policy": {"locked": bool(settings.get("model_locked")), "allowed_models": allowed_models(settings),
                         "fallback": "none: Stage 1 and Stage 2 use this model; an error or a quota stops the "
                                     "analysis"},
        "generation_settings": provider.generation_settings(),
        "prompt_versions": {"explanation": prompts["explanation"], "formalize": prompts["formalize"]},
        "facts_schema_version": FACTS_SCHEMA_VERSION, "packet_schema_version": PACKET_SCHEMA_VERSION,
        "response_schema_versions": {"explanation": STAGE1_SCHEMA_VERSION, "formalize": STAGE2_SCHEMA_VERSION},
        "grammar_version": GRAMMAR_VERSION, "vocabulary_version": vocabulary.version,
        "run_id": packet["run_id"], "forensic_packet_sha256": digest,
        "oracle_identities": bool(options.oracle_identities), "dry_run": bool(options.dry_run),
        "created_at": _utc_iso(), "code_version": _code_version(),
        "python": sys.version.split()[0], "platform": sys.platform,
        "determinism": DETERMINISM_NOTE, "stages": {}}
    if metadata.get("forensic_packet_sha256") != digest:
        raise ValueError("the packet changed since this analysis began ({0} != {1})".format(
            metadata.get("forensic_packet_sha256"), digest))
    metadata["provider_available"] = provider.available
    result = AnalysisResult(analysis_dir=analysis_dir, status="OK")
    auditor = PayloadAuditor(run_dir) if options.audit_payload else None
    if auditor is not None and (analysis_dir / "payload_audit.json").exists():
        # a continued analysis keeps the audit records of its earlier requests
        auditor.records = list(_read_json(analysis_dir / "payload_audit.json").get("requests", []))

    def save_metadata() -> None:
        _write_json(metadata_path, metadata)

    def audit_hook(stage: str, rendered) -> Optional[Callable[[str, Dict[str, Any]], None]]:
        if auditor is None:
            return None

        def check(url: str, body: Dict[str, Any]) -> None:
            try:
                auditor.check(stage, url, body, rendered.packet_json, rendered.exempt_blocks)
            finally:
                _write_json(analysis_dir / "payload_audit.json", auditor.report())
        return check

    def guarded(rendered) -> bool:
        try:
            check_request(rendered.text, packet, rendered.exempt_blocks, rendered.packet_json)
            return True
        except LeakGuardError as error:
            _write_json(analysis_dir / "guard_report.json", {"status": "BLOCKED", "template": rendered.template,
                                                             "violations": error.violations})
            result.status = "BLOCKED_BY_LEAK_GUARD"
            result.messages.append(str(error))
            metadata["status"] = result.status
            save_metadata()
            return False

    # --- dry run: render, guard, show; never call -------------------------------------------
    if options.dry_run:
        stage1 = render_explanation(packet, vocabulary, prompts["explanation"])
        if not guarded(stage1):
            return result
        placeholder = {"_placeholder": "the saved Stage-1 answer is inserted here"}
        stage2 = render_formalization(packet, vocabulary, placeholder, prompts["formalize"])
        if not guarded(stage2):
            return result
        preview = {
            "note": "dry run: nothing was sent; the API key header is redacted",
            "provider": provider.describe(),
            "explanation": dict(stage1.digest(), request=provider.preview(
                stage1.system, stage1.user, stage1_schema(vocabulary), "forensic_explanation")),
            "formalize": dict(stage2.digest(), request=provider.preview(
                stage2.system, stage2.user, stage2_schema(), "forensic_formalization")),
        }
        _write_json(analysis_dir / "request_preview.json", preview)
        for stage, rendered in (("explanation", stage1), ("formalize", stage2)):
            hook = audit_hook(stage, rendered)
            if hook is not None:
                try:
                    hook(preview[stage]["request"]["url"], preview[stage]["request"]["body"])
                except PayloadAuditError as error:
                    result.status = "BLOCKED_BY_PAYLOAD_AUDIT"
                    result.messages.append(str(error))
                    metadata["status"] = result.status
                    save_metadata()
                    return result
        metadata["status"] = "DRY_RUN"
        save_metadata()
        result.status = "DRY_RUN"
        result.previews = {"explanation": stage1, "formalize": stage2}
        return result

    def call(stage: str, rendered, schema: Dict[str, Any], schema_name: str) -> Optional[Dict[str, Any]]:
        entry = {"started_at": _utc_iso(), "model": provider.model, "prompt": rendered.digest(),
                 "schema_name": schema_name}
        metadata["stages"][stage] = entry
        try:
            response = provider.generate(rendered.system, rendered.user, schema, schema_name,
                                         before_send=audit_hook(stage, rendered))
        except PayloadAuditError as error:
            entry.update(status="BLOCKED_BY_PAYLOAD_AUDIT", error=str(error))
            result.status = "BLOCKED_BY_PAYLOAD_AUDIT"
            result.messages.append(str(error) + " (nothing was sent)")
            metadata["status"] = result.status
            save_metadata()
            return None
        except ProviderError as error:
            entry.update(error=str(error), error_kind=error.kind, http_status=error.status, attempts=error.attempts)
            if error.kind == "quota":
                entry["status"] = "QUOTA_EXHAUSTED"
                result.status = "INCOMPLETE_QUOTA" if stage == "formalize" else "QUOTA_EXHAUSTED"
                result.messages.append(
                    "{0} {1}: quota exhausted; no other model was tried.{2}".format(
                        provider.name, provider.model,
                        "  Stage 1 is saved; complete this analysis later with the same model: "
                        "--provider {0} --model {1} --stage formalize --analysis-dir {2}".format(
                            provider.name, provider.model, analysis_dir) if stage == "formalize" else ""))
            else:
                entry["status"] = "FAILED"
                result.status = "FAILED"
                result.messages.append(str(error))
            metadata["status"] = result.status
            save_metadata()
            return None
        entry.update(status="ANSWERED" if response.parsed is not None else "UNPARSABLE", **response.to_dict())
        save_metadata()
        return {"response": response, "prompt": rendered}

    fact_ids = packet_fact_ids(packet)
    stage1_path, stage2_path = analysis_dir / STAGE1_FILE, analysis_dir / STAGE2_FILE
    if options.stage in ("explanation", "all"):
        rendered = render_explanation(packet, vocabulary, prompts["explanation"])
        if not guarded(rendered):
            return result
        answer = call("explanation", rendered, stage1_schema(vocabulary), "forensic_explanation")
        if answer is None:
            return result
        response = answer["response"]
        validation = (validate_stage1(response.parsed, packet, vocabulary, fact_ids) if response.parsed is not None
                      else {"status": "INVALID", "schema_errors": [response.parse_error], "issues": []})
        _write_json(stage1_path, {
            "schema_version": STAGE1_SCHEMA_VERSION, "saved_at": _utc_iso(),
            "request": dict(rendered.digest(), system_prompt=rendered.system, user_prompt=rendered.user),
            "raw_response_text": response.text, "answer": response.parsed, "validation": validation,
            "provider_response": response.to_dict(), "raw_api_response": response.raw_response})
        metadata["stages"]["explanation"]["validation_status"] = validation["status"]
        save_metadata()
        echo("explanation: {0} ({1} issue(s))".format(validation["status"], len(validation["issues"])
                                                       + len(validation["schema_errors"])))

    if options.stage in ("formalize", "all"):
        if not stage1_path.exists():
            result.status = "NO_EXPLANATION"
            result.messages.append("no Stage-1 answer to formalise in {0}".format(analysis_dir))
            return result
        stage1 = _read_json(stage1_path)
        if stage1["answer"] is None or stage1["validation"]["schema_errors"]:
            result.status = "EXPLANATION_UNUSABLE"
            result.messages.append("the Stage-1 answer does not follow its schema; not formalised")
            return result
        rendered = render_formalization(packet, vocabulary, stage1["answer"], prompts["formalize"])
        if not guarded(rendered):
            return result
        answer = call("formalize", rendered, stage2_schema(), "forensic_formalization")
        if answer is None:
            return result
        response = answer["response"]
        validation = (validate_stage2(response.parsed, packet, vocabulary, stage1["answer"])
                      if response.parsed is not None
                      else {"status": "INVALID", "schema_errors": [response.parse_error], "issues": [], "formulas": []})
        _write_json(stage2_path, {
            "schema_version": STAGE2_SCHEMA_VERSION, "saved_at": _utc_iso(),
            "stage1_sha256": sha256_text(stage1_path.read_text(encoding="utf-8")),
            "request": dict(rendered.digest(), system_prompt=rendered.system, user_prompt=rendered.user),
            "raw_response_text": response.text, "answer": response.parsed, "validation": validation,
            "provider_response": response.to_dict(), "raw_api_response": response.raw_response})
        metadata["stages"]["formalize"]["validation_status"] = validation["status"]
        save_metadata()
        echo("formalize: {0} ({1} formula(s))".format(validation["status"], len(validation.get("formulas", []))))

    if options.verify and stage1_path.exists() and stage2_path.exists():
        verification, evaluation = verify_analysis(analysis_dir, config)
        echo("verification: {0}".format(verification["summary"]))
    metadata["status"] = result.status if result.status != "OK" else "COMPLETED"
    save_metadata()
    return result


def verify_analysis(analysis_dir: Path, config: Optional[Dict[str, Any]] = None, out_dir: Optional[Path] = None,
                    note: Optional[str] = None):
    """Deterministic, no model call: load the semantic trace (only now) and check the saved answers.

    By default verification.json and evaluation.json are (re)written in the analysis directory.  With
    ``out_dir`` they go there instead and the analysis directory is left untouched (a re-verification
    of unchanged answers against a regenerated semantic trace); ``note`` says why, and the digests of
    the trace files used are recorded.
    """
    analysis_dir = Path(analysis_dir)
    config = config or load_llm_config()
    stage1_path, stage2_path = analysis_dir / STAGE1_FILE, analysis_dir / STAGE2_FILE
    if not stage1_path.exists() or not stage2_path.exists():
        raise FileNotFoundError("verification needs both saved answers ({0}, {1})".format(STAGE1_FILE, STAGE2_FILE))
    stage1_text, stage2_text = stage1_path.read_text(encoding="utf-8"), stage2_path.read_text(encoding="utf-8")
    stage1, stage2 = json.loads(stage1_text), json.loads(stage2_text)
    run_dir = run_dir_of(analysis_dir)
    metadata = _read_json(analysis_dir / "request_metadata.json")
    vocabulary = load_vocabulary()
    settings = config.get("verification") or {}
    step = float(settings.get("time_step_s", 0.05))
    at = float(settings.get("evaluate_at_t_global", 0.0))

    # The semantic trace enters here, after both answers are on disk.
    trace_loaded_at = _utc_iso()
    trace = SemanticTrace.load(run_dir, vocabulary, step)
    rows = []
    formulas = (stage2.get("answer") or {}).get("formulas") or []
    checks = {row["formula_id"]: row for row in (stage2.get("validation") or {}).get("formulas", [])}
    for item in formulas:
        check = checks.get(item["formula_id"], {})
        row = {"formula_id": item["formula_id"], "claim_ref": item["claim_ref"], "claim": item["claim"],
               "formula_text": item["formula_text"], "text_matches_ast": check.get("text_matches_ast")}
        if not check.get("ast_valid"):
            row.update(result="INVALID", issues=check.get("issues", []))
        else:
            outcome = trace.evaluate(ast_from_table(item["formula_ast"]), at=at)
            row.update(outcome)
            hallucinated = [issue for issue in check.get("issues", [])
                            if issue["code"] == "INVALID_IDENTITY_HALLUCINATION"]
            if hallucinated:
                row["issues"] = hallucinated
        rows.append(row)
    summary = {label: sum(1 for row in rows if row["result"] == label)
               for label in ("TRUE", "FALSE", "UNKNOWN", "INVALID")}
    verification = {
        "semantics": SEMANTICS,
        "meaning": {"TRUE": "the reconstructed semantic trace satisfies the formula (consistency, not proof of "
                            "causation)",
                    "FALSE": "the reconstructed semantic trace contradicts the formula",
                    "UNKNOWN": "the trace cannot decide: road user not tracked, state not established, identity "
                               "not available, or outside the recorded interval",
                    "INVALID": "the formula is malformed or uses names outside the vocabulary"},
        "evaluated_at_t_global": at, "time_step_s": step,
        "trace_interval_t_global": [float(trace.grid[0]), float(trace.grid[-1])] if len(trace.grid) else None,
        "inputs": {"stage1_sha256": sha256_text(stage1_text), "stage2_sha256": sha256_text(stage2_text),
                   "stage1_saved_at": stage1.get("saved_at"), "stage2_saved_at": stage2.get("saved_at"),
                   "semantic_trace_loaded_at": trace_loaded_at,
                   "forensic_packet_sha256": metadata.get("forensic_packet_sha256")},
        "results": rows, "summary": summary}
    target = analysis_dir if out_dir is None else Path(out_dir)
    target.mkdir(parents=True, exist_ok=True)
    if out_dir is not None:
        global_dir = run_dir / "reconstruction" / "global"
        previous = {name: sha256_text((analysis_dir / name).read_text(encoding="utf-8"))
                    for name in ("verification.json", "evaluation.json") if (analysis_dir / name).exists()}
        verification["reverification"] = {
            "note": note or "re-verification of the saved answers against the current semantic trace; no model call",
            "answers_unchanged": True, "verified_at": _utc_iso(), "previous_outputs_sha256": previous,
            "semantic_trace_files_sha256": {name: sha256_text((global_dir / name).read_text(encoding="utf-8"))
                                            for name in ("global_graph.json", "global_trace.jsonl")
                                            if (global_dir / name).exists()}}
    _write_json(target / "verification.json", verification)

    identity_map = None
    if metadata.get("oracle_identities"):
        from .oracle import load_identity_map_for

        identity_map = load_identity_map_for(analysis_dir)
    packet = _analysis_packet(run_dir, metadata)
    answer = stage1.get("answer") or {}
    issues = (stage1.get("validation") or {}).get("issues", [])
    evaluation = {
        "note": "computed from the saved answers and the reconstructed semantic trace; no model call",
        "stage1_validation_status": (stage1.get("validation") or {}).get("status"),
        "stage1_issue_counts": _count_codes(issues),
        "stage2_validation_status": (stage2.get("validation") or {}).get("status"),
        "attribution": attribution_check(answer, trace) if answer else None,
        "semantic_hypotheses": score_semantic_hypotheses(
            answer, trace, known_ids(packet), ScoringConfig.from_mapping(config.get("evaluation")),
            identity_map=identity_map) if answer else None,
        "formulas": summary}
    if out_dir is not None:
        evaluation["reverification"] = verification["reverification"]
    _write_json(target / "evaluation.json", evaluation)
    return verification, evaluation


def _analysis_packet(run_dir: Path, metadata: Dict[str, Any]) -> Dict[str, Any]:
    if metadata.get("oracle_identities"):
        from .oracle import oracle_dir

        return _read_json(oracle_dir(run_dir) / "forensic_packet_oracle.json")["packet"]
    return load_packet(run_dir)


def _count_codes(issues: List[Dict[str, Any]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for issue in issues:
        out[issue["code"]] = out.get(issue["code"], 0) + 1
    return out
