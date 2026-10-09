"""Model policy of the LLM experiments (no real API call: every transport here is fake).

OpenAI is locked to gpt-6-luna with reasoning effort high and never falls back; Gemini runs
gemini-3.8-flash (primary) or gemini-3.5-flash-lite (second model), both with thinking level high
and no legacy sampling parameters; one analysis keeps one model for both stages, a quota error stops
it; secrets never reach a file; the packet sent to every model is the same; the semantic trace never
reaches a request body; a hallucinated identity is still detected.
"""

import copy
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.cdf.llm.payload_audit import PayloadAuditError, PayloadAuditor
from src.cdf.llm.pipeline import AnalysisOptions, load_llm_config, run_analysis, verify_analysis
from src.cdf.llm.prompts import packet_text
from src.cdf.llm.providers import (GeminiProvider, ModelNotAllowed, OpenAIProvider, allowed_models, default_model,
                                   make_provider)
from src.cdf.llm.providers.base import ProviderError
from src.cdf.llm.schemas import INVALID_IDENTITY_HALLUCINATION

from test_llm_pipeline import S17, SECRET, FakeTransport, copy_run_for_llm, stage1_answer

CONFIG = load_llm_config()
OPENAI = dict(CONFIG["providers"]["openai"])
GEMINI = dict(CONFIG["providers"]["gemini"])
LEGACY_GEMINI_KEYS = ("temperature", "topP", "topK", "candidateCount", "seed", "thinkingBudget")


def stage2_answer():
    return {"formulas": [{"formula_id": "phi_1", "claim_ref": "causal_chain[0]",
                          "claim": "the tracked road user cut in before the collision",
                          "formula_text": "F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, A:track_001)",
                          "formula_ast": {"root": "n1", "nodes": [
                              {"id": "n1", "op": "EVENTUALLY", "children": ["n2"], "lo": -3.0, "hi": 0.0,
                               "event_type": None, "state": None, "actor_id": None, "subject_id": None},
                              {"id": "n2", "op": "EVENT", "children": [], "lo": None, "hi": None,
                               "event_type": "CUT_IN_FROM_RIGHT_START", "state": None, "actor_id": "A",
                               "subject_id": "A:track_001"}]}}],
            "untestable_claims": []}


def quota_error(per_day=True):
    quota = "GenerateRequestsPerDayPerProjectPerModel-FreeTier" if per_day else "GenerateRequestsPerMinute"
    return {"error": {"code": 429, "status": "RESOURCE_EXHAUSTED", "message": "You exceeded your current quota",
                      "details": [{"@type": "type.googleapis.com/google.rpc.QuotaFailure",
                                   "violations": [{"quotaId": quota}]},
                                  {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": "5s"}]}}


class ScriptedTransport(FakeTransport):
    """FakeTransport with a scripted status per call: an int status returns that error body."""

    def __init__(self, provider, answers, script):
        super().__init__(provider, answers)
        self.script = list(script)

    def __call__(self, url, headers, body, timeout_s):
        step = self.script.pop(0) if self.script else 200
        if step == 200:
            return super().__call__(url, headers, body, timeout_s)
        self.calls.append({"url": url, "headers": dict(headers), "body": body})
        status, data = step
        return status, data


@unittest.skipUnless((S17 / "reconstruction" / "global" / "global_graph.json").exists(), "S17 not recorded")
class _RunTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = copy_run_for_llm(S17, Path(self.tmp.name) / "S17" / "run_0_crash")
        (self.run / "ground_truth").mkdir(parents=True, exist_ok=True)  # read by the payload audit only
        for name in ("metadata.json", "triggers.jsonl"):
            shutil.copy2(S17 / "ground_truth" / name, self.run / "ground_truth" / name)
        self.env = mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET, "GEMINI_API_KEY": SECRET})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def analyse(self, provider, transport, model=None, stage="all", analysis_dir=None, audit=True):
        options = AnalysisOptions(provider=provider, model=model, stage=stage, analysis_dir=analysis_dir,
                                  audit_payload=audit)
        return run_analysis(self.run, options, CONFIG, transport=transport)

    def written_text(self, directory):
        return "\n".join(path.read_text(encoding="utf-8") for path in Path(directory).rglob("*") if path.is_file())


class ConfiguredModelsTests(unittest.TestCase):
    def test_openai_is_gpt_6_luna_with_high_reasoning_and_no_temperature(self):
        self.assertEqual(default_model(OPENAI), "gpt-6-luna")
        self.assertTrue(OPENAI["model_locked"])
        self.assertEqual(allowed_models(OPENAI), ["gpt-6-luna"])
        self.assertEqual(OPENAI["reasoning_effort"], "high")
        self.assertIsNone(OPENAI["temperature"])
        transport = FakeTransport("openai", [{}])
        provider = OpenAIProvider("gpt-6-luna", OPENAI, api_key=SECRET, transport=transport)
        provider.generate("s", "u", {"type": "object"}, "x")
        body = transport.calls[0]["body"]
        self.assertEqual((body["model"], body["reasoning"]), ("gpt-6-luna", {"effort": "high"}))
        self.assertNotIn("temperature", body)
        self.assertGreaterEqual(body["max_output_tokens"], 25000)  # OpenAI's advice for reasoning models

    def test_openai_never_accepts_another_model(self):
        for other in ("gpt-6.1-sol", "gpt-5.6-sol", "astra", "gpt-6-luna-latest"):
            with self.assertRaises(ModelNotAllowed) as caught:
                make_provider("openai", OPENAI, model=other, env_file=Path("missing.env"))
            self.assertIn("Andrea", str(caught.exception))
        self.assertEqual(make_provider("openai", OPENAI, model="gpt-6-luna", env_file=Path("missing.env")).model,
                         "gpt-6-luna")

    def test_gemini_models_and_thinking_level(self):
        self.assertEqual(default_model(GEMINI), "gemini-3.8-flash")
        self.assertEqual(GEMINI["primary_model"], "gemini-3.8-flash")
        self.assertEqual(GEMINI["secondary_model"], "gemini-3.5-flash-lite")
        self.assertEqual(allowed_models(GEMINI), ["gemini-3.8-flash", "gemini-3.5-flash-lite"])
        self.assertEqual(GEMINI["thinking_level"], "high")
        with self.assertRaises(ModelNotAllowed):
            make_provider("gemini", GEMINI, model="gemini-3.7-flash", env_file=Path("missing.env"))

    def test_both_gemini_models_think_high_and_send_no_legacy_sampling(self):
        for model in ("gemini-3.8-flash", "gemini-3.5-flash-lite"):
            transport = FakeTransport("gemini", [{}])
            with mock.patch.dict(os.environ, {"GEMINI_API_KEY": SECRET}):
                provider = make_provider("gemini", GEMINI, model=model, env_file=Path("missing.env"),
                                         transport=transport)
            provider.generate("s", "u", {"type": "object"}, "x")
            call = transport.calls[0]
            self.assertTrue(call["url"].endswith("/models/{0}:generateContent".format(model)))
            config = call["body"]["generationConfig"]
            self.assertEqual(config["thinkingConfig"], {"thinkingLevel": "high"})
            for key in LEGACY_GEMINI_KEYS:
                self.assertNotIn(key, config, (model, key))
                self.assertNotIn(key, config["thinkingConfig"], (model, key))
        for legacy in ({"temperature": 0.0}, {"seed": 7}, {"top_k": 10}, {"thinking_budget": 1024}):
            with self.assertRaises(ValueError):
                GeminiProvider("gemini-3.8-flash", dict(GEMINI, **legacy), api_key=SECRET)


class NoFallbackTests(unittest.TestCase):
    def provider(self, transport):
        return OpenAIProvider("gpt-6-luna", OPENAI, api_key=SECRET, transport=transport, sleep=lambda s: None)

    def test_openai_errors_stop_with_the_same_model_and_parameters(self):
        failures = [(404, {"error": {"code": "model_not_found", "message": "The model does not exist"}}),
                    (400, {"error": {"code": "unsupported_parameter", "message": "reasoning.effort not supported"}}),
                    (400, {"error": {"code": "invalid_json_schema", "message": "Invalid schema for response_format"}}),
                    (429, {"error": {"code": "insufficient_quota", "message": "You exceeded your current quota"}})]
        for status, data in failures:
            transport = ScriptedTransport("openai", [], [(status, data)] * 5)
            with self.assertRaises(ProviderError) as caught:
                self.provider(transport).generate("s", "u", {"type": "object"}, "x")
            self.assertEqual(len(transport.calls), 1, data)  # no retry, no other model, no other parameters
            self.assertEqual(transport.calls[0]["body"]["model"], "gpt-6-luna")
            self.assertEqual(transport.calls[0]["body"]["reasoning"], {"effort": "high"})
        self.assertEqual(caught.exception.kind, "quota")

    def test_transient_errors_repeat_the_identical_request_a_limited_number_of_times(self):
        transport = ScriptedTransport("openai", [], [(503, {"error": {"message": "busy"}})] * 5)
        with self.assertRaises(ProviderError):
            self.provider(transport).generate("s", "u", {"type": "object"}, "x")
        self.assertEqual(len(transport.calls), 1 + OPENAI["max_retries"])
        bodies = [json.dumps(call["body"], sort_keys=True) for call in transport.calls]
        self.assertEqual(len(set(bodies)), 1)

    def test_an_openai_client_timeout_is_not_retried(self):
        calls = []

        def transport(url, headers, body, timeout_s):
            calls.append(body)
            raise TimeoutError("read timed out")

        with self.assertRaises(ProviderError) as caught:
            self.provider(transport).generate("s", "u", {"type": "object"}, "x")
        self.assertEqual((len(calls), caught.exception.kind), (1, "timeout"))

    def test_a_gemini_daily_quota_stops_at_once_and_a_minute_limit_waits(self):
        transport = ScriptedTransport("gemini", [], [(429, quota_error(per_day=True))] * 5)
        provider = GeminiProvider("gemini-3.8-flash", GEMINI, api_key=SECRET, transport=transport, sleep=lambda s: None)
        with self.assertRaises(ProviderError) as caught:
            provider.generate("s", "u", {"type": "object"}, "x")
        self.assertEqual((len(transport.calls), caught.exception.kind), (1, "quota"))
        waits = []
        transport = ScriptedTransport("gemini", [{"ok": 1}], [(429, quota_error(per_day=False)), 200])
        provider = GeminiProvider("gemini-3.8-flash", GEMINI, api_key=SECRET, transport=transport, sleep=waits.append)
        response = provider.generate("s", "u", {"type": "object"}, "x")
        self.assertEqual((response.parsed, waits), ({"ok": 1}, [6.0]))
        self.assertTrue(all(call["url"].endswith("/gemini-3.8-flash:generateContent") for call in transport.calls))


class AnalysisModelTests(_RunTestCase):
    def test_one_model_for_both_stages_with_its_settings_recorded(self):
        for provider, model, level in (("gemini", "gemini-3.8-flash", ("thinking_level", "high")),
                                       ("gemini", "gemini-3.5-flash-lite", ("thinking_level", "high")),
                                       ("openai", None, ("reasoning_effort", "high"))):
            transport = FakeTransport(provider, [stage1_answer(), stage2_answer()])
            result = self.analyse(provider, transport, model=model)
            self.assertEqual(result.status, "OK", result.messages)
            metadata = json.loads((result.analysis_dir / "request_metadata.json").read_text())
            expected = model or "gpt-6-luna"
            self.assertEqual(metadata["model"], expected)
            self.assertEqual(metadata["generation_settings"][level[0]], level[1])
            self.assertEqual({stage["model"] for stage in metadata["stages"].values()}, {expected})
            self.assertEqual(len(transport.calls), 2)
            for call in transport.calls:
                if provider == "openai":
                    self.assertEqual((call["body"]["model"], call["body"]["reasoning"]["effort"]), (expected, "high"))
                else:
                    self.assertTrue(call["url"].endswith("/{0}:generateContent".format(expected)))
            for name in ("stage1_explanation.json", "stage2_formula.json"):
                saved = json.loads((result.analysis_dir / name).read_text())
                self.assertIsNotNone(saved["raw_api_response"])
                self.assertIn("usage", saved["provider_response"])

    def test_continuing_an_analysis_keeps_its_model(self):
        transport = FakeTransport("gemini", [stage1_answer()])
        first = self.analyse("gemini", transport, model="gemini-3.5-flash-lite", stage="explanation")
        with self.assertRaises(ModelNotAllowed):
            self.analyse("gemini", FakeTransport("gemini", [stage2_answer()]), model="gemini-3.8-flash",
                         stage="formalize", analysis_dir=first.analysis_dir)
        transport = FakeTransport("gemini", [stage2_answer()])
        second = self.analyse("gemini", transport, stage="formalize", analysis_dir=first.analysis_dir)
        self.assertEqual(second.status, "OK", second.messages)
        self.assertTrue(transport.calls[0]["url"].endswith("/gemini-3.5-flash-lite:generateContent"))
        audit = json.loads((first.analysis_dir / "payload_audit.json").read_text())
        self.assertEqual([(row["stage"], row["result"]) for row in audit["requests"]],
                         [("explanation", "PASS"), ("formalize", "PASS")])  # the earlier audit is kept

    def test_a_quota_error_between_the_stages_saves_stage_1_and_switches_nothing(self):
        transport = ScriptedTransport("gemini", [stage1_answer()], [200] + [(429, quota_error())] * 5)
        result = self.analyse("gemini", transport, model="gemini-3.8-flash")
        self.assertEqual(result.status, "INCOMPLETE_QUOTA")
        self.assertTrue((result.analysis_dir / "stage1_explanation.json").exists())
        self.assertFalse((result.analysis_dir / "stage2_formula.json").exists())
        self.assertEqual(len(transport.calls), 2)
        self.assertTrue(all(call["url"].endswith("/gemini-3.8-flash:generateContent") for call in transport.calls))
        metadata = json.loads((result.analysis_dir / "request_metadata.json").read_text())
        self.assertEqual((metadata["status"], metadata["stages"]["formalize"]["status"]),
                         ("INCOMPLETE_QUOTA", "QUOTA_EXHAUSTED"))
        with self.assertRaises(ModelNotAllowed):  # not completed with the other model
            self.analyse("gemini", FakeTransport("gemini", [stage2_answer()]), model="gemini-3.5-flash-lite",
                         stage="formalize", analysis_dir=result.analysis_dir)
        done = self.analyse("gemini", FakeTransport("gemini", [stage2_answer()]), stage="formalize",
                            analysis_dir=result.analysis_dir)
        self.assertEqual(done.status, "OK", done.messages)
        self.assertEqual(json.loads((result.analysis_dir / "request_metadata.json").read_text())["status"], "COMPLETED")

    def test_secrets_are_never_written(self):
        transport = FakeTransport("openai", [stage1_answer(), stage2_answer()])
        result = self.analyse("openai", transport)
        self.assertEqual(result.status, "OK", result.messages)
        self.assertNotIn(SECRET, self.written_text(result.analysis_dir))
        failing = ScriptedTransport("openai", [], [(401, {"error": {"message": "bad key " + SECRET}})])
        result = self.analyse("openai", failing)
        self.assertEqual(result.status, "FAILED")
        text = self.written_text(result.analysis_dir)
        self.assertNotIn(SECRET, text)
        self.assertIn("<redacted>", text)

    def test_every_model_receives_the_same_packet(self):
        digests, embedded = set(), set()
        for provider, model in (("gemini", "gemini-3.8-flash"), ("gemini", "gemini-3.5-flash-lite"),
                                ("openai", None)):
            result = self.analyse(provider, FakeTransport(provider, [stage1_answer(), stage2_answer()]), model=model)
            digests.add(json.loads((result.analysis_dir / "request_metadata.json").read_text())["forensic_packet_sha256"])
            audit = json.loads((result.analysis_dir / "payload_audit.json").read_text())
            embedded |= {row["embedded_packet_sha256"] for row in audit["requests"]}
            self.assertEqual([row["result"] for row in audit["requests"]], ["PASS", "PASS"])
        self.assertEqual((len(digests), len(embedded)), (1, 1))

    def test_the_semantic_trace_never_reaches_a_request_body(self):
        transport = FakeTransport("gemini", [stage1_answer(), stage2_answer()])
        self.analyse("gemini", transport, model="gemini-3.8-flash")
        node_ids = set()
        for graph in list(self.run.glob("reconstruction/*/local_graph.json")) + [
                self.run / "reconstruction" / "global" / "global_graph.json"]:
            node_ids |= {node["node_id"] for node in json.loads(graph.read_text())["nodes"]}
        for call in transport.calls:
            text = json.dumps(call["body"], ensure_ascii=False)
            for marker in ("perceived_state", "global_graph", "local_graph", "ground_truth", "triggers.jsonl"):
                self.assertNotIn(marker, text)
            for node_id in node_ids:
                self.assertNotIn('"{0}"'.format(node_id), text.replace('\\"', '"'))
        auditor = PayloadAuditor(self.run)
        packet = json.loads((self.run / "reconstruction" / "llm" / "forensic_packet.json").read_text())
        for leak in (" (see global_graph)", " (node g01)", " (vehicle \"C\")", " (ground_truth)"):
            poisoned = copy.deepcopy(transport.calls[0]["body"])
            poisoned["systemInstruction"]["parts"][0]["text"] += leak
            with self.assertRaises(PayloadAuditError, msg=leak):
                auditor.check("explanation", "url", poisoned, packet_text(packet), [])

    def test_a_named_unrecorded_vehicle_is_still_an_identity_hallucination(self):
        answer = stage1_answer(actor="C", text="Vehicle C cut in.")
        transport = FakeTransport("openai", [answer, stage2_answer()])
        result = self.analyse("openai", transport)
        saved = json.loads((result.analysis_dir / "stage1_explanation.json").read_text())
        self.assertEqual(saved["answer"]["responsibility"]["actor"], "C")  # kept as answered, never corrected
        codes = {issue["code"] for issue in saved["validation"]["issues"]}
        self.assertIn(INVALID_IDENTITY_HALLUCINATION, codes)
        evaluation = json.loads((result.analysis_dir / "evaluation.json").read_text())
        self.assertEqual(evaluation["attribution"]["kind"], "NOT_IN_RECONSTRUCTION")

    def test_a_reverification_leaves_the_saved_analysis_untouched(self):
        result = self.analyse("gemini", FakeTransport("gemini", [stage1_answer(), stage2_answer()]),
                              model="gemini-3.5-flash-lite")
        before = {path.name: path.read_bytes() for path in result.analysis_dir.iterdir() if path.is_file()}
        out = result.analysis_dir / "reverification_test"
        verification, evaluation = verify_analysis(result.analysis_dir, CONFIG, out_dir=out, note="trace regenerated")
        after = {path.name: path.read_bytes() for path in result.analysis_dir.iterdir() if path.is_file()}
        self.assertEqual(before, after)  # answers, verification and evaluation of the analysis unchanged
        saved = json.loads((out / "verification.json").read_text())
        self.assertEqual(saved["reverification"]["note"], "trace regenerated")
        self.assertTrue(saved["reverification"]["answers_unchanged"])
        self.assertEqual(set(saved["reverification"]["previous_outputs_sha256"]), {"verification.json", "evaluation.json"})
        self.assertIn("global_trace.jsonl", saved["reverification"]["semantic_trace_files_sha256"])
        self.assertEqual(json.loads((out / "evaluation.json").read_text())["reverification"], saved["reverification"])


if __name__ == "__main__":
    unittest.main()
