"""LLM forensic pipeline: exporter, leak guard, providers (mocked), schemas, formal logic, verifier, scoring.

No test calls a real API: every provider request goes through a fake transport.
"""

import copy
import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.cdf.llm import facts as facts_module
from src.cdf.llm.evaluation import ScoringConfig, attribution_check, score_semantic_hypotheses
from src.cdf.llm.facts import (TRACK_STATE_FIELDS, TRACK_STATE_REMOVED, build_forensic_facts, build_packet,
                               export_forensic_facts, iter_packet_facts, packet_fact_ids, packet_sha256)
from src.cdf.llm.formal.parser import (FormulaError, ast_from_table, check_ast, equivalent, parse_formula, to_table,
                                       to_text)
from src.cdf.llm.formal.verifier import FALSE, TRUE, UNKNOWN, Recorder, SemanticTrace, TraceEvent
from src.cdf.llm.guard import LeakGuardError, check_packet, check_prompt_text
from src.cdf.llm.pipeline import AnalysisOptions, load_llm_config, run_analysis, verify_analysis
from src.cdf.llm.prompts import load_template, render_explanation, render_formalization
from src.cdf.llm.providers import GeminiProvider, OpenAIProvider, make_provider
from src.cdf.llm.providers.base import ProviderUnavailable, load_env_file, resolve_api_key
from src.cdf.llm.schemas import (INVALID_EVENT_TYPE, INVALID_IDENTITY_HALLUCINATION, known_ids, stage1_schema,
                                 stage2_schema, validate_json_schema, validate_stage1, validate_stage2)
from src.cdf.llm.vocabulary import load_vocabulary
from src.cdf.reconstruction.config import ReconstructionConfig
from src.cdf.reconstruction.models import SAME_TIME_ORDER
from src.cdf.reconstruction.pipeline import reconstruct_run

from synthetic_run import make_run

ROOT = Path(__file__).resolve().parents[1]
S17 = ROOT / "traces" / "S17" / "run_0_crash"
SECRET = "sk-test-DO-NOT-LEAK-0123456789abcdef"
VOCABULARY = load_vocabulary()


def copy_run_for_llm(source: Path, target: Path) -> Path:
    """Only what the exporter and the verifier read (plus the privileged evaluation, for oracle tests)."""
    for path in source.rglob("*"):
        rel = path.relative_to(source)
        keep = (rel.parts[0] == "reconstruction" and "llm" not in rel.parts
                or rel.name in ("incident_context.json",)
                or (rel.parts[0] == "vehicles" and rel.name in ("metadata.json", "traffic_signs.jsonl")))
        if path.is_file() and keep:
            (target / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target / rel)
    return target


def synthetic_run(root: Path) -> Path:
    run = make_run(root, speed_limit_kmh=50)
    reconstruct_run(run, ReconstructionConfig())
    return run


def stage1_answer(actor="A:track_001", subject="A:track_001", fact="F0003", event="CUT_IN_FROM_RIGHT_START",
                  time=-2.3, text="An unidentified road user (A:track_001) moved into A's lane."):
    return {
        "explanation": text,
        "primary_hypothesis": "A swerved left to avoid the road user that cut in and struck B.",
        "causal_chain": [{"step": 1, "claim": "the tracked road user moved into A's lane", "actor_id": actor,
                          "time_reference": "GLOBAL", "estimated_time": time, "evidence_fact_ids": [fact]}],
        "responsibility": {"actor": actor, "assessment": "initiated the conflict", "confidence": 0.6,
                           "limitations": ["the road user is not a recorder"]},
        "alternative_hypotheses": [{"hypothesis": "A changed lane without need", "responsible_actor": "A",
                                    "plausibility": 0.3, "evidence_fact_ids": [fact]}],
        "semantic_hypotheses": [
            {"event_type": event, "actor_id": "A", "subject_id": subject, "time_reference": "GLOBAL",
             "estimated_time": time, "time_window": None, "confidence": 0.7, "evidence_fact_ids": [fact]},
            {"event_type": "COLLISION", "actor_id": "A", "subject_id": "B", "time_reference": "GLOBAL",
             "estimated_time": 0.0, "time_window": None, "confidence": 0.9, "evidence_fact_ids": [fact]}],
        "unresolved_entities": [{"entity_id": "A:track_001", "role": "cut in", "reason": "not a recorder"}],
    }


def formula_item(formula_id, text, claim_ref="semantic_hypotheses[0]"):
    return {"formula_id": formula_id, "claim_ref": claim_ref, "claim": "claim of " + formula_id,
            "formula_text": text, "formula_ast": to_table(parse_formula(text))}


class FakeTransport:
    """Answers like the provider's REST API; records every request (headers included, in memory only)."""

    def __init__(self, provider, answers, status=200):
        self.provider, self.answers, self.status, self.calls = provider, list(answers), status, []

    def __call__(self, url, headers, body, timeout_s):
        self.calls.append({"url": url, "headers": dict(headers), "body": body})
        answer = self.answers.pop(0) if self.answers else {}
        if self.status != 200:
            return self.status, {"error": {"message": "rejected " + headers.get("Authorization", "")}}
        text = json.dumps(answer)
        if self.provider == "openai":
            return 200, {"id": "resp_1", "model": "gpt-test", "status": "completed",
                         "output": [{"type": "reasoning", "summary": []},
                                    {"type": "message", "content": [{"type": "output_text", "text": text}]}],
                         "usage": {"input_tokens": 1000, "output_tokens": 200, "total_tokens": 1200,
                                   "output_tokens_details": {"reasoning_tokens": 50}}}
        return 200, {"responseId": "g1", "modelVersion": "gemini-test",
                     "candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": text}]}}],
                     "usageMetadata": {"promptTokenCount": 1000, "candidatesTokenCount": 200, "totalTokenCount": 1200}}


# ---------------------------------------------------------------------------------------------
# Secrets and .env
# ---------------------------------------------------------------------------------------------

class SecretsTests(unittest.TestCase):
    def test_env_file_is_ignored_by_git_and_the_example_is_not(self):
        ignored = subprocess.call(["git", "check-ignore", "-q", ".env"], cwd=str(ROOT))
        self.assertEqual(ignored, 0, ".env must be ignored by git")
        example = subprocess.call(["git", "check-ignore", "-q", ".env.example"], cwd=str(ROOT))
        self.assertEqual(example, 1, ".env.example must be tracked")
        self.assertNotIn(".env", subprocess.check_output(["git", "ls-files"], cwd=str(ROOT)).decode().split())

    def test_env_example_holds_no_key(self):
        values = load_env_file(ROOT / ".env.example")
        self.assertEqual(set(values), {"OPENAI_API_KEY", "GEMINI_API_KEY"})
        self.assertTrue(all(value == "" for value in values.values()))

    def test_keys_come_from_environment_or_env_file_and_missing_means_unavailable(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = Path(tmp) / ".env"
            env.write_text("# comment\nOPENAI_API_KEY=\nGEMINI_API_KEY=\"g-123\"\n", encoding="utf-8")
            with mock.patch.dict(os.environ, {}, clear=True):
                self.assertIsNone(resolve_api_key("OPENAI_API_KEY", env))
                self.assertEqual(resolve_api_key("GEMINI_API_KEY", env), "g-123")
                provider = make_provider("openai", {"model": "m"}, env_file=env)
                self.assertFalse(provider.available)
                with self.assertRaises(ProviderUnavailable):
                    provider.generate("s", "u", {"type": "object"}, "x")
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "from-env"}, clear=True):
                self.assertEqual(resolve_api_key("OPENAI_API_KEY", env), "from-env")

    def test_no_secret_is_written_anywhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = synthetic_run(Path(tmp) / "run")
            export_forensic_facts(run)
            packet = json.loads((run / "reconstruction" / "llm" / "forensic_packet.json").read_text(encoding="utf-8"))
            first = next(f["fact_id"] for f in iter_packet_facts(packet) if f["type"] == "EGO_MOTION")
            answer1 = stage1_answer(actor="A", subject="B", fact=first, event="BRAKE_START", time=-0.9,
                                    text="A braked before it struck B.")
            answer1["semantic_hypotheses"][0]["subject_id"] = None
            answer1["unresolved_entities"] = []
            answer2 = {"formulas": [formula_item("phi_1", "F[-2,0] event(BRAKE_START, A)")], "untestable_claims": []}
            transport = FakeTransport("openai", [answer1, answer2])
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
                result = run_analysis(run, AnalysisOptions(provider="openai"), load_llm_config(), transport=transport)
            self.assertEqual(result.status, "OK", result.messages)
            self.assertEqual(len(transport.calls), 2)
            self.assertEqual(transport.calls[0]["headers"]["Authorization"], "Bearer " + SECRET)
            self.assertNotIn(SECRET, transport.calls[0]["url"])
            for path in run.rglob("*"):
                if path.is_file():
                    self.assertNotIn(SECRET, path.read_text(encoding="utf-8", errors="ignore"), path)

    def test_a_failing_request_never_stores_the_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = synthetic_run(Path(tmp) / "run")
            transport = FakeTransport("openai", [{}], status=401)
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
                result = run_analysis(run, AnalysisOptions(provider="openai", stage="explanation"),
                                      load_llm_config(), transport=transport)
            self.assertEqual(result.status, "FAILED")
            self.assertNotIn(SECRET, " ".join(result.messages))
            for path in run.rglob("*.json"):
                self.assertNotIn(SECRET, path.read_text(encoding="utf-8"), path)


# ---------------------------------------------------------------------------------------------
# Exporter
# ---------------------------------------------------------------------------------------------

FORBIDDEN_IN_PACKET = ("events", "perceived_state", "critical", "collision_course", "required_deceleration",
                       "encounter", "motion_relation", "\"ttc_s\"", "scenario", "variant", "ground_truth",
                       "local_graph", "global_graph", "CUT_IN", "EGO_PATH", "CRITICAL_TTC", "BRAKE_START")


class ExporterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.run_path = synthetic_run(Path(cls.tmp.name) / "run")
        cls.summary = export_forensic_facts(cls.run_path)
        cls.out = cls.run_path / "reconstruction" / "llm"
        cls.packet = json.loads((cls.out / "forensic_packet.json").read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_never_reads_ground_truth_or_run_metadata(self):
        # make_run poisons ground_truth/ and metadata.json: reading them would have failed the export.
        self.assertTrue((self.run_path / "ground_truth" / "states.jsonl").read_text().startswith("POISON"))
        self.assertGreater(self.summary["facts"], 100)

    def test_packet_has_no_semantic_or_privileged_content(self):
        text = (self.out / "forensic_packet.json").read_text(encoding="utf-8")
        for token in FORBIDDEN_IN_PACKET:
            self.assertNotIn(token, text, token)
        check_packet(self.packet)
        facts_text = (self.out / "forensic_facts.jsonl").read_text(encoding="utf-8")
        for token in FORBIDDEN_IN_PACKET:
            self.assertNotIn(token, facts_text, token)

    def test_track_state_keeps_exactly_the_allowlist(self):
        allowed = {name for _, name in TRACK_STATE_FIELDS}
        rows = [json.loads(line) for line in (self.out / "forensic_facts.jsonl").read_text().splitlines()]
        tracks = [row for row in rows if row["type"] == "TRACK_STATE"]
        self.assertTrue(tracks)
        for row in tracks:
            self.assertEqual(set(row["values"]), allowed)
        self.assertEqual({row["type"] for row in rows} - {"EGO_MOTION", "EGO_CONTROL", "TRACK_STATE",
                                                          "SIGN_DETECTION", "COLLISION_OBSERVATION"}, set())
        manifest = json.loads((self.out / "export_manifest.json").read_text())
        self.assertEqual(set(manifest["removed_from_track_state"]), set(TRACK_STATE_REMOVED))
        self.assertTrue(set(manifest["dropped_attribute_occurrences"]) <= set(TRACK_STATE_REMOVED))

    def test_run_id_is_a_neutral_hash_and_no_path_is_named(self):
        self.assertRegex(self.packet["run_id"], r"^case-[0-9a-f]{16}$")
        text = (self.out / "forensic_packet.json").read_text(encoding="utf-8")
        self.assertNotIn("run", re.sub(r'"run_id"|recorder|forensic', "", text).lower().replace("ground", ""))

    def test_packet_hash_is_stable(self):
        facts, context = build_forensic_facts(self.run_path)
        again = build_packet(facts, context)
        self.assertEqual(packet_sha256(again), packet_sha256(self.packet))
        manifest = json.loads((self.out / "export_manifest.json").read_text())
        self.assertEqual(manifest["forensic_packet_sha256"], packet_sha256(self.packet))
        with tempfile.TemporaryDirectory() as tmp:
            second = export_forensic_facts(self.run_path, output_dir=Path(tmp))
            self.assertEqual(second["forensic_packet_sha256"], self.summary["forensic_packet_sha256"])
            self.assertEqual((Path(tmp) / "forensic_facts.jsonl").read_bytes(),
                             (self.out / "forensic_facts.jsonl").read_bytes())

    def test_packet_is_a_lossless_reorganisation_of_the_facts(self):
        canonical = [json.loads(line) for line in (self.out / "forensic_facts.jsonl").read_text().splitlines()]
        self.assertEqual(sorted(packet_fact_ids(self.packet)), sorted(row["fact_id"] for row in canonical))
        by_id = {row["fact_id"]: row for row in canonical}
        for item in iter_packet_facts(self.packet):
            row = by_id[item["fact_id"]]
            for key, value in item.items():
                if key in ("type", "fact_id"):
                    continue
                self.assertEqual(row.get(key, row.get("values", {}).get(key)), value, (item["fact_id"], key))

    def test_aligned_recorders_carry_global_time_and_the_collision_is_matched(self):
        rows = [json.loads(line) for line in (self.out / "forensic_facts.jsonl").read_text().splitlines()]
        collision = [row for row in rows if row["type"] == "COLLISION_OBSERVATION"]
        self.assertEqual(len(collision), 1)
        self.assertEqual(collision[0]["participants"], ["A", "B"])
        self.assertTrue(collision[0]["time_origin"])
        self.assertEqual(collision[0]["t_global_s"], 0.0)
        for row in rows:
            if row["type"] == "EGO_MOTION":
                offset = {item["recorder_id"]: item["clock"]["offset_to_global_s"]
                          for item in self.packet["known_recorders"]}[row["recorder"]]
                self.assertAlmostEqual(row["t_global_s"], row["t_local_s"] + offset, places=3)

    def test_unaligned_recorder_gets_no_global_time(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = synthetic_run(Path(tmp) / "run")
            alignment_path = run / "reconstruction" / "global" / "alignment.json"
            alignment = json.loads(alignment_path.read_text())
            alignment["graphs"]["B"].update(status="UNALIGNED", offset_to_global=None)
            alignment["matched_events"] = []
            alignment_path.write_text(json.dumps(alignment))
            facts, _ = build_forensic_facts(run)
            b_rows = [f for f in facts if f.get("recorder") == "B"]
            self.assertTrue(b_rows)
            self.assertTrue(all(f["t_global_s"] is None for f in b_rows))
            a_rows = [f for f in facts if f.get("recorder") == "A"]
            self.assertTrue(all(f["t_global_s"] is not None for f in a_rows))


@unittest.skipUnless((S17 / "reconstruction" / "llm" / "forensic_packet.json").exists(), "S17 not recorded")
class S17PacketTests(unittest.TestCase):
    """The non-recorder C never appears in the admissible input: only anonymous tracks."""

    @classmethod
    def setUpClass(cls):
        cls.text = (S17 / "reconstruction" / "llm" / "forensic_packet.json").read_text(encoding="utf-8")
        cls.packet = json.loads(cls.text)

    def test_c_is_not_revealed(self):
        ids = {entity["entity_id"] for entity in self.packet["entities"]}
        self.assertEqual(ids, {"A", "B", "A:track_001", "A:track_002", "B:track_001", "B:track_002"})
        self.assertEqual([r["recorder_id"] for r in self.packet["known_recorders"]], ["A", "B"])
        self.assertNotIn('"C"', self.text)
        self.assertNotIn("C:", self.text)
        facts_text = (S17 / "reconstruction" / "llm" / "forensic_facts.jsonl").read_text(encoding="utf-8")
        self.assertNotIn('"C"', facts_text)
        check_packet(self.packet)

    def test_anonymous_tracks_stay_anonymous_and_associated_ones_are_identified(self):
        entities = {e["entity_id"]: e for e in self.packet["entities"] if e["kind"] == "RADAR_TRACK"}
        self.assertEqual((entities["A:track_001"]["identity_status"], entities["A:track_001"]["observed_subject"]),
                         ("ANONYMOUS", "A:track_001"))
        self.assertEqual((entities["B:track_002"]["identity_status"], entities["B:track_002"]["observed_subject"]),
                         ("ANONYMOUS", "B:track_002"))
        self.assertEqual((entities["A:track_002"]["identity_status"], entities["A:track_002"]["observed_subject"]),
                         ("ASSOCIATED", "B"))
        self.assertEqual((entities["B:track_001"]["identity_status"], entities["B:track_001"]["observed_subject"]),
                         ("ASSOCIATED", "A"))
        for item in iter_packet_facts(self.packet):
            if item["type"] == "TRACK_STATE":
                expected_subject = entities[item["local_track_id"]]["observed_subject"]
                self.assertEqual(item["observed_subject"], expected_subject)

    def test_a_tracked_the_cut_in_road_user_for_seconds(self):
        track = next(e for e in self.packet["entities"] if e["entity_id"] == "A:track_001")
        self.assertLessEqual(track["first_t_global_s"], -5.0)
        self.assertGreaterEqual(track["last_t_global_s"], 0.0)
        self.assertGreater(track["samples"], 50)


# ---------------------------------------------------------------------------------------------
# Leak guard
# ---------------------------------------------------------------------------------------------

BLACKLIST = ("ground_truth", "expected", "culprit", "scenario_description", "scenario_name", "variant",
             "semantic_trace", "perceived_state", "events", "critical", "collision_course", "required_deceleration")


class LeakGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.run_path = synthetic_run(Path(cls.tmp.name) / "run")
        export_forensic_facts(cls.run_path)
        cls.packet = json.loads((cls.run_path / "reconstruction" / "llm" / "forensic_packet.json").read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_blacklisted_key_fails_closed(self):
        for token in BLACKLIST:
            poisoned = copy.deepcopy(self.packet)
            poisoned["supplied_context"][token] = "x"
            with self.assertRaises(LeakGuardError, msg=token):
                check_packet(poisoned)

    def test_semantic_names_scenario_names_and_paths_in_values_fail_closed(self):
        for value in ("CRITICAL_TTC_START at -1.6", "S17", "unobserved_causal_vehicle", "traces/S17/run_0_crash",
                      "deflected_into_c"):
            poisoned = copy.deepcopy(self.packet)
            poisoned["supplied_context"]["road_environment"] = value
            with self.assertRaises(LeakGuardError, msg=value):
                check_packet(poisoned)
        poisoned = copy.deepcopy(self.packet)
        poisoned["facts"]["TRACK_STATE"]["columns"].append("ttc_s")
        with self.assertRaises(LeakGuardError):
            check_packet(poisoned)

    def test_one_word_scenario_names_are_ordinary_language_in_the_supplied_context(self):
        packet = copy.deepcopy(self.packet)
        packet["supplied_context"]["road_environment"] = "urban junction, perpendicular crossing"
        check_packet(packet)
        packet["supplied_context"]["road_environment"] = "crossing"
        with self.assertRaises(LeakGuardError):
            check_packet(packet)
        packet["supplied_context"]["road_environment"] = "urban junction, multidirection_crossing"
        with self.assertRaises(LeakGuardError):
            check_packet(packet)

    def test_prompt_text_is_checked_too(self):
        with self.assertRaises(LeakGuardError):
            check_prompt_text("The expected culprit is C.")
        with self.assertRaises(LeakGuardError):
            check_prompt_text("This is scenario S17.")
        check_prompt_text("Explain the collision.")

    def test_shipped_templates_pass_the_guard(self):
        for name in ("accident_abduction_v1", "formalize_hypothesis_v1"):
            template = load_template(name)
            check_prompt_text(re.sub(r"\{\{[A-Z0-9_]+\}\}", " ", template.system + template.user))

    def test_poisoned_packet_never_reaches_the_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = synthetic_run(Path(tmp) / "run")
            export_forensic_facts(run)
            path = run / "reconstruction" / "llm" / "forensic_packet.json"
            packet = json.loads(path.read_text())
            packet["supplied_context"]["culprit"] = "B"
            path.write_text(json.dumps(packet))
            transport = FakeTransport("openai", [stage1_answer()])
            with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
                with self.assertRaises(LeakGuardError):
                    run_analysis(run, AnalysisOptions(provider="openai"), load_llm_config(), transport=transport)
            self.assertEqual(transport.calls, [])

    def test_poisoned_template_never_reaches_the_api(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = synthetic_run(Path(tmp) / "run")
            export_forensic_facts(run)
            prompts = Path(tmp) / "prompts"
            prompts.mkdir()
            (prompts / "bad_v1.txt").write_text("=== SYSTEM ===\nThe expected answer is B.\n{{VOCABULARY}}\n"
                                                "=== USER ===\n{{SUPPLIED_CONTEXT}}\n{{PACKET_JSON}}\n")
            config = load_llm_config()
            config["prompts"] = {"explanation": "bad_v1", "formalize": "formalize_hypothesis_v1"}
            transport = FakeTransport("openai", [stage1_answer()])
            with mock.patch("src.cdf.llm.prompts.prompts_dir", return_value=prompts), \
                    mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
                result = run_analysis(run, AnalysisOptions(provider="openai"), config, transport=transport)
            self.assertEqual(result.status, "BLOCKED_BY_LEAK_GUARD")
            self.assertEqual(transport.calls, [])
            self.assertTrue((result.analysis_dir / "guard_report.json").exists())


# ---------------------------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------------------------

class VocabularyTests(unittest.TestCase):
    def test_vocabulary_matches_the_reconstruction_event_types(self):
        self.assertEqual(sorted(VOCABULARY.event_names), sorted(SAME_TIME_ORDER))
        self.assertEqual(len(VOCABULARY.event_names), 33)

    def test_descriptions_carry_no_thresholds(self):
        for event in VOCABULARY.events:
            self.assertIsNone(re.search(r"\d", event.description + event.note), event.name)
            self.assertNotIn("m/s", event.description)
        rendered = VOCABULARY.render()
        for name in VOCABULARY.event_names:
            self.assertIn(name, rendered)

    def test_states_pair_every_start_with_its_end(self):
        paired = {name for pair in VOCABULARY.states.values() for name in pair}
        unpaired = set(VOCABULARY.event_names) - paired
        self.assertEqual(unpaired, {"TRACK_APPEARED_FRONT", "TRACK_APPEARED_LEFT", "TRACK_APPEARED_RIGHT",
                                    "TRACK_LOST", "COLLISION"})


# ---------------------------------------------------------------------------------------------
# Providers (mock transports) and schemas
# ---------------------------------------------------------------------------------------------

class ProviderTests(unittest.TestCase):
    schema = stage1_schema(VOCABULARY)

    def test_openai_request_uses_strict_json_schema_and_bearer_key(self):
        transport = FakeTransport("openai", [stage1_answer()])
        provider = OpenAIProvider("gpt-test", {"temperature": 0.0, "max_output_tokens": 100}, api_key=SECRET,
                                  transport=transport)
        response = provider.generate("sys", "user", self.schema, "forensic_explanation")
        body = transport.calls[0]["body"]
        self.assertEqual(body["text"]["format"]["type"], "json_schema")
        self.assertTrue(body["text"]["format"]["strict"])
        self.assertFalse(body["store"])
        self.assertEqual(body["temperature"], 0.0)
        self.assertEqual(response.parsed, stage1_answer())
        self.assertEqual(response.usage["input_tokens"], 1000)
        self.assertEqual(validate_json_schema(response.parsed, self.schema), [])
        self.assertNotIn(SECRET, json.dumps(response.to_dict()))

    def test_gemini_request_uses_response_json_schema_and_header_key(self):
        transport = FakeTransport("gemini", [stage1_answer()])
        provider = GeminiProvider("gemini-test", {"temperature": 0.0, "seed": 7}, api_key=SECRET,
                                  transport=transport)
        response = provider.generate("sys", "user", self.schema, "forensic_explanation")
        call = transport.calls[0]
        self.assertEqual(call["headers"]["x-goog-api-key"], SECRET)
        self.assertNotIn(SECRET, call["url"])
        self.assertTrue(call["url"].endswith("models/gemini-test:generateContent"))
        config = call["body"]["generationConfig"]
        self.assertEqual(config["responseMimeType"], "application/json")
        self.assertEqual(config["responseJsonSchema"], self.schema)
        self.assertEqual((config["temperature"], config["seed"]), (0.0, 7))
        self.assertEqual(response.parsed, stage1_answer())

    def test_openai_retries_without_temperature_when_the_model_rejects_it(self):
        calls = []

        def transport(url, headers, body, timeout_s):
            calls.append(body)
            if "temperature" in body:
                return 400, {"error": {"message": "Unsupported parameter: 'temperature' is not supported"}}
            return 200, {"output": [{"type": "message", "content": [{"type": "output_text", "text": "{}"}]}]}

        provider = OpenAIProvider("gpt-test", {"temperature": 0.0}, api_key=SECRET, transport=transport)
        response = provider.generate("s", "u", {"type": "object"}, "x")
        self.assertEqual(len(calls), 2)
        self.assertIsNone(response.parameters_sent["temperature"])
        self.assertTrue(any("temperature" in note for note in response.notes))

    def test_server_errors_are_retried_then_reported(self):
        statuses = [503, 200]

        def transport(url, headers, body, timeout_s):
            status = statuses.pop(0)
            return status, ({"error": {"message": "busy"}} if status != 200 else
                            {"candidates": [{"content": {"parts": [{"text": "{\"a\": 1}"}]}}]})

        provider = GeminiProvider("g", {"max_retries": 2}, api_key=SECRET, transport=transport, sleep=lambda s: None)
        response = provider.generate("s", "u", {"type": "object"}, "x")
        self.assertEqual([a["status"] for a in response.attempts], [503, 200])
        self.assertEqual(response.parsed, {"a": 1})

    def test_invalid_json_answer_is_reported_not_repaired(self):
        def transport(url, headers, body, timeout_s):
            return 200, {"output": [{"type": "message", "content": [{"type": "output_text", "text": "{oops"}]}]}

        response = OpenAIProvider("m", {}, api_key=SECRET, transport=transport).generate("s", "u", {}, "x")
        self.assertIsNone(response.parsed)
        self.assertIn("not valid JSON", response.parse_error)


class Stage1ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packet = {"known_recorders": [{"recorder_id": "A"}, {"recorder_id": "B"}],
                      "entities": [{"entity_id": "A"}, {"entity_id": "B"},
                                   {"entity_id": "A:track_001", "observed_subject": "A:track_001"},
                                   {"entity_id": "A:track_002", "observed_subject": "B"}]}
        cls.fact_ids = ["F0001", "F0002", "F0003"]

    def test_a_correct_answer_is_valid(self):
        report = validate_stage1(stage1_answer(), self.packet, VOCABULARY, self.fact_ids)
        self.assertEqual(report["status"], "VALID", report)

    def test_an_invented_actor_is_an_identity_hallucination_and_is_not_corrected(self):
        answer = stage1_answer(actor="C", subject="C", text="Vehicle C cut in.")
        before = copy.deepcopy(answer)
        report = validate_stage1(answer, self.packet, VOCABULARY, self.fact_ids)
        self.assertEqual(report["status"], "INVALID")
        codes = [(issue["code"], issue["path"]) for issue in report["issues"]]
        self.assertIn((INVALID_IDENTITY_HALLUCINATION, "$.responsibility.actor"), codes)
        self.assertIn((INVALID_IDENTITY_HALLUCINATION, "$.semantic_hypotheses[0].subject_id"), codes)
        self.assertIn((INVALID_IDENTITY_HALLUCINATION, "$.explanation"), codes)
        self.assertEqual(answer, before)

    def test_unknown_event_type_and_bad_fact_ids_are_rejected(self):
        answer = stage1_answer(event="SWERVE_START")
        report = validate_stage1(answer, self.packet, VOCABULARY, self.fact_ids)
        self.assertEqual(report["status"], "INVALID")
        self.assertTrue(any("SWERVE_START" in error for error in report["schema_errors"]))
        answer = stage1_answer(fact="F9999")
        report = validate_stage1(answer, self.packet, VOCABULARY, self.fact_ids)
        self.assertIn("INVALID_EVIDENCE_REFERENCE", {issue["code"] for issue in report["issues"]})

    def test_schema_is_strict_compatible(self):
        def walk(schema):
            if schema.get("type") == "object" or schema.get("type") == ["object", "null"]:
                self.assertIs(schema.get("additionalProperties"), False)
                self.assertEqual(sorted(schema["required"]), sorted(schema["properties"]))
            for key in ("properties",):
                for child in schema.get(key, {}).values():
                    walk(child)
            if "items" in schema:
                walk(schema["items"])
            for option in schema.get("anyOf", []):
                walk(option)
            for forbidden in ("minimum", "maximum", "pattern", "format", "oneOf", "allOf"):
                self.assertNotIn(forbidden, schema)

        walk(stage1_schema(VOCABULARY))
        walk(stage2_schema())


# ---------------------------------------------------------------------------------------------
# Formal logic
# ---------------------------------------------------------------------------------------------

class ParserTests(unittest.TestCase):
    def test_valid_formulas_parse_and_round_trip(self):
        for text in ("F[-5,0] (event(CUT_IN_FROM_RIGHT_START, A, A:track_001) AND F[0,2] state(BRAKE, A))",
                     "G[-1.5,0] NOT state(CLOSING, A, B) OR event(COLLISION, A, B)",
                     "BEFORE(event(EGO_PATH_ENTRY, A, A:track_001), event(COLLISION, A, B))",
                     "F[-inf,inf] event(STOP_SIGN_DETECTED_START, A, A:sign-0)",
                     "EVENTUALLY[-3,0] ALWAYS[0,0.5] state(TURN_LEFT, A)"):
            tree = parse_formula(text)
            self.assertTrue(equivalent(tree, parse_formula(to_text(tree))), text)
            self.assertTrue(equivalent(tree, ast_from_table(to_table(tree))), text)
        tree = parse_formula("F[-inf,2] event(BRAKE_START, A)")
        self.assertEqual((tree["op"], tree["lo"], tree["hi"]), ("EVENTUALLY", None, 2.0))
        self.assertTrue(equivalent(parse_formula("a_and"[0:0] + "event(BRAKE_START, A) AND state(STOP, B)"),
                                   parse_formula("state(STOP, B) AND event(BRAKE_START, A)")))

    def test_invalid_formulas_are_rejected(self):
        for text in ("F[0] event(BRAKE_START, A)", "event(BRAKE_START)", "(event(BRAKE_START, A)",
                     "event(BRAKE_START, A) AND", "UNTIL[0,1] event(BRAKE_START, A)", "F[0,1]",
                     "event(BRAKE_START, A) event(BRAKE_END, A)", "F[a,1] event(BRAKE_START, A)"):
            with self.assertRaises(FormulaError, msg=text):
                parse_formula(text)

    def test_node_tables_are_checked(self):
        table = to_table(parse_formula("F[-2,0] event(BRAKE_START, A)"))
        broken = copy.deepcopy(table)
        broken["nodes"][0]["children"] = ["n9"]
        with self.assertRaises(FormulaError):
            ast_from_table(broken)
        cyclic = copy.deepcopy(table)
        cyclic["nodes"][1]["children"] = ["n1"]
        cyclic["nodes"][1]["op"] = "NOT"
        with self.assertRaises(FormulaError):
            ast_from_table(cyclic)
        tree = parse_formula("F[2,-2] event(SWERVE_START, A, C)")
        codes = {problem["code"] for problem in check_ast(tree, VOCABULARY, {"A", "B"})}
        self.assertEqual(codes, {"INVALID_FORMULA", INVALID_EVENT_TYPE, INVALID_IDENTITY_HALLUCINATION})

    def test_stage2_validation_flags_text_ast_mismatch_and_bad_claims(self):
        packet = {"entities": [{"entity_id": "A"}, {"entity_id": "B"}]}
        good = formula_item("phi_1", "F[-2,0] event(BRAKE_START, A)")
        mismatch = formula_item("phi_2", "F[-2,0] event(BRAKE_START, A)")
        mismatch["formula_text"] = "F[-3,0] event(BRAKE_START, A)"
        orphan = formula_item("phi_3", "event(COLLISION, A, B)", claim_ref="causal_chain[7]")
        answer = {"formulas": [good, mismatch, orphan], "untestable_claims": []}
        report = validate_stage2(answer, packet, VOCABULARY, stage1_answer())
        rows = {row["formula_id"]: row for row in report["formulas"]}
        self.assertTrue(rows["phi_1"]["ast_valid"] and rows["phi_1"]["text_matches_ast"])
        self.assertFalse(rows["phi_2"]["text_matches_ast"])
        self.assertIn("INVALID_CLAIM_REFERENCE", {i["code"] for i in rows["phi_3"]["issues"]})


def toy_trace():
    """A and B aligned (offset 0) over [-3, 2] s; A tracks B as A:track_001 (associated) over [-3, 0] and an
    anonymous road user A:track_002 over [-3, -1] (then lost)."""
    a = Recorder("A", True, 0.0, -3.0, 2.0, tracks={"track_001": (-3.0, 0.0), "track_002": (-3.0, -1.0)})
    b = Recorder("B", True, 0.0, -3.0, 2.0)
    for k in range(51):
        t = round(-3.0 + 0.1 * k, 2)
        external = {}
        if t <= 0.0:
            external["track_001"] = {"CLOSING": t >= -1.0, "CRITICAL_TTC": "UNKNOWN" if t < -2.0 else t >= -0.5,
                                     "IN_EGO_PATH": False, "CUT_IN_FROM_LEFT": False, "CUT_IN_FROM_RIGHT": False}
        if t <= -1.0:
            external["track_002"] = {"CLOSING": False, "CRITICAL_TTC": False, "IN_EGO_PATH": t >= -2.0,
                                     "CUT_IN_FROM_LEFT": False, "CUT_IN_FROM_RIGHT": -2.5 <= t <= -1.5}
        ego = {"MOVING": True, "STOP": False, "BRAKE": t >= -0.8, "THROTTLE": t < -0.8, "TURN_LEFT": False,
               "TURN_RIGHT": False, "SPEED_LIMIT_EXCEEDED": False}
        a.frames.append((t, {"ego": ego, "external": external, "signs": {}}))
        b.frames.append((t, {"ego": dict(ego, BRAKE=False, THROTTLE=True), "external": {}, "signs": {}}))
    events = [TraceEvent("CUT_IN_FROM_RIGHT_START", "A", "A:track_002", ["A"], -2.5, {"A": -2.5}),
              TraceEvent("EGO_PATH_ENTRY", "A", "A:track_002", ["A"], -2.0, {"A": -2.0}),
              TraceEvent("CUT_IN_FROM_RIGHT_END", "A", "A:track_002", ["A"], -1.5, {"A": -1.5}),
              TraceEvent("TRACK_LOST", "A", "A:track_002", ["A"], -1.0, {"A": -1.0}),
              TraceEvent("CLOSING_START", "A", "B", ["A", "B"], -1.0, {"A": -1.0}),
              TraceEvent("BRAKE_START", "A", None, ["A"], -0.8, {"A": -0.8}),
              TraceEvent("CRITICAL_TTC_START", "A", "B", ["A", "B"], -0.5, {"A": -0.5}),
              TraceEvent("COLLISION", None, None, ["A", "B"], 0.0, {"A": 0.0, "B": 0.0}),
              TraceEvent("MOVING_START", "A", None, ["A"], -3.0, {"A": -3.0}, first_observation=True)]
    identity = {("A", "track_001"): "B", ("A", "track_002"): "A:track_002"}
    return SemanticTrace({"A": a, "B": b}, events, identity, VOCABULARY, step=0.05)


class VerifierTests(unittest.TestCase):
    trace = toy_trace()

    def result(self, text):
        return self.trace.evaluate(parse_formula(text), at=0.0)["result"]

    def test_true(self):
        self.assertEqual(self.result("F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, A:track_002)"), "TRUE")
        self.assertEqual(self.result("event(COLLISION, A, B)"), "TRUE")
        self.assertEqual(self.result("event(COLLISION, B, A:track_001)"), "TRUE")  # A:track_001 is B... and A
        self.assertEqual(self.result("BEFORE(event(EGO_PATH_ENTRY, A, A:track_002), event(BRAKE_START, A))"), "TRUE")
        self.assertEqual(self.result("F[-1,0] state(BRAKE, A) AND G[-0.4,0] state(CRITICAL_TTC, A, B)"), "TRUE")

    def test_false(self):
        self.assertEqual(self.result("F[-3,0] event(BRAKE_START, B)"), "FALSE")
        self.assertEqual(self.result("F[-3,-1] event(BRAKE_START, A)"), "FALSE")
        self.assertEqual(self.result("BEFORE(event(COLLISION, A, B), event(BRAKE_START, A))"), "FALSE")
        self.assertEqual(self.result("G[-2,0] state(THROTTLE, A)"), "FALSE")

    def test_unknown(self):
        # A road user the reconstruction never identified as C.
        self.assertEqual(self.result("F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)"), "UNKNOWN")
        # The anonymous track was lost at -1: whether it was closing afterwards is unobserved.
        self.assertEqual(self.result("F[-0.5,0] state(CLOSING, A, A:track_002)"), "UNKNOWN")
        # Not decided yet: the state was UNKNOWN (too young a track) there.
        self.assertEqual(self.result("G[-3,-2.5] state(CRITICAL_TTC, A, B)"), "UNKNOWN")
        # Window beyond the recording.
        self.assertEqual(self.result("F[1,4] event(STOP_START, A)"), "UNKNOWN")
        # A track has no events of its own.
        self.assertEqual(self.result("F[-3,0] event(BRAKE_START, A:track_002)"), "UNKNOWN")
        # B cannot be shown to observe A's anonymous track.
        self.assertEqual(self.result("F[-3,0] event(CLOSING_START, B, A:track_002)"), "UNKNOWN")
        # Whether the road user entered A's path again after A braked is unobserved: its track was lost.
        self.assertEqual(self.result("BEFORE(event(BRAKE_START, A), event(EGO_PATH_ENTRY, A, A:track_002))"),
                         "UNKNOWN")

    def test_absence_of_evidence_is_not_false(self):
        # After TRACK_LOST nothing is known about the cut-in road user, so "it never braked" is UNKNOWN,
        # and "the cut-in never ended" is UNKNOWN once the track is lost, not FALSE.
        self.assertEqual(self.result("G[-0.9,0] NOT state(CUT_IN_FROM_RIGHT, A, A:track_002)"), "UNKNOWN")

    def test_kleene_connectives(self):
        self.assertEqual(self.result("event(COLLISION, A, B) OR F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)"), "TRUE")
        self.assertEqual(self.result("F[-3,0] event(BRAKE_START, B) AND F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)"),
                         "FALSE")
        self.assertEqual(self.result("NOT F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)"), "UNKNOWN")


class ScoringTests(unittest.TestCase):
    trace = toy_trace()
    packet_ids = {"A", "B", "A:track_001", "A:track_002"}

    def hypothesis(self, event, actor, subject, t, window=None):
        return {"event_type": event, "actor_id": actor, "subject_id": subject, "time_reference": "GLOBAL",
                "estimated_time": t, "time_window": window, "confidence": 0.5, "evidence_fact_ids": []}

    def test_scores_with_tolerance(self):
        answer = {"semantic_hypotheses": [
            self.hypothesis("CUT_IN_FROM_RIGHT_START", "A", "A:track_002", -2.2),   # TP (0.3 s off)
            self.hypothesis("BRAKE_START", "A", None, -1.5),                         # FP: 0.7 s off
            self.hypothesis("COLLISION", "B", "A", 0.05),                            # TP (either order)
            self.hypothesis("CUT_IN_FROM_RIGHT_START", "A", "C", -2.5),              # FP, identity hallucination
            self.hypothesis("CRITICAL_TTC_START", "A", "A:track_001", -0.6),         # TP: A:track_001 is B
            self.hypothesis("TURN_LEFT_START", "A", None, -1.0, {"start": -2.0, "end": 0.0})]}  # FP, not in trace
        score = score_semantic_hypotheses(answer, self.trace, self.packet_ids, ScoringConfig(time_tolerance_s=0.5))
        self.assertEqual((score["TP"], score["FP"], score["FN"]), (3, 3, 5))
        self.assertEqual(score["reference_events"], 8)  # MOVING_START at first observation excluded
        self.assertAlmostEqual(score["precision"], 0.5)
        self.assertAlmostEqual(score["recall"], 3 / 8, places=4)
        self.assertAlmostEqual(score["f1"], 2 * 0.5 * 0.375 / 0.875, places=4)
        self.assertAlmostEqual(score["identity_hallucination_rate"], 1 / 6, places=4)
        self.assertAlmostEqual(score["hallucination_rate"], 2 / 6, places=4)  # C's cut-in and the left turn
        wider = score_semantic_hypotheses(answer, self.trace, self.packet_ids, ScoringConfig(time_tolerance_s=0.8))
        self.assertEqual(wider["TP"], 4)

    def test_attribution_kinds(self):
        self.assertEqual(attribution_check({"responsibility": {"actor": "A:track_002"}}, self.trace)["kind"],
                         "ANONYMOUS_TRACK")
        self.assertEqual(attribution_check({"responsibility": {"actor": "C"}}, self.trace)["kind"],
                         "NOT_IN_RECONSTRUCTION")
        self.assertEqual(attribution_check({"responsibility": {"actor": "A"}}, self.trace)["kind"], "RECORDER")
        self.assertEqual(attribution_check({"responsibility": {"actor": "UNKNOWN"}}, self.trace)["kind"], "UNKNOWN")

    def test_oracle_identity_map_lets_named_hypotheses_match(self):
        answer = {"semantic_hypotheses": [self.hypothesis("CUT_IN_FROM_RIGHT_START", "A", "C", -2.5)]}
        plain = score_semantic_hypotheses(answer, self.trace, self.packet_ids | {"C"})
        oracle = score_semantic_hypotheses(answer, self.trace, self.packet_ids | {"C"},
                                           identity_map={"A:track_002": "C"})
        self.assertEqual((plain["TP"], oracle["TP"]), (0, 1))


# ---------------------------------------------------------------------------------------------
# End to end with mock providers
# ---------------------------------------------------------------------------------------------

@unittest.skipUnless((S17 / "reconstruction" / "global" / "global_graph.json").exists(), "S17 not recorded")
class S17EndToEndTests(unittest.TestCase):
    """The main test case: the cause must be attributed to the anonymous track, never to "C"."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = copy_run_for_llm(S17, Path(self.tmp.name) / "S17" / "run_0_crash")
        export_forensic_facts(self.run)
        self.packet = json.loads((self.run / "reconstruction" / "llm" / "forensic_packet.json").read_text())
        self.ids = {f["fact_id"]: f for f in iter_packet_facts(self.packet)}
        self.cut_fact = min((abs(f["t_global_s"] + 2.3), i) for i, f in self.ids.items()
                            if f["type"] == "TRACK_STATE" and f["local_track_id"] == "A:track_001")[1]

    def tearDown(self):
        self.tmp.cleanup()

    def analyse(self, provider, answer1, answer2):
        transport = FakeTransport(provider, [answer1, answer2])
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET, "GEMINI_API_KEY": SECRET}):
            result = run_analysis(self.run, AnalysisOptions(provider=provider), load_llm_config(), transport=transport)
        self.assertEqual(len(transport.calls), 2)
        stage1_prompt = transport.calls[0]["body"]
        # Nothing about C and nothing from the semantic trace went out.
        sent = json.dumps(stage1_prompt)
        for token in ("CRITICAL_TTC_START at", "perceived_state", "global_graph", "S17", "unobserved_causal",
                      "causal_vehicle", '\\"C\\"'):
            self.assertNotIn(token, sent)
        return result

    def test_correct_attribution_to_the_anonymous_track(self):
        answer1 = stage1_answer(fact=self.cut_fact)
        answer2 = {"formulas": [
            formula_item("phi_1", "F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, A:track_001)"),
            formula_item("phi_2", "BEFORE(event(CUT_IN_FROM_RIGHT_START, A, A:track_001), event(COLLISION, A, B))",
                         claim_ref="causal_chain[0]"),
            formula_item("phi_3", "F[-3,0] event(BRAKE_START, A)", claim_ref="causal_chain[0]")],
            "untestable_claims": [{"claim_ref": "causal_chain[0]", "claim": "A meant to avoid it",
                                   "reason": "intention"}]}
        result = self.analyse("openai", answer1, answer2)
        self.assertEqual(result.status, "OK", result.messages)
        stage1 = json.loads((result.analysis_dir / "stage1_explanation.json").read_text())
        self.assertEqual(stage1["validation"]["status"], "VALID", stage1["validation"])
        verification = json.loads((result.analysis_dir / "verification.json").read_text())
        results = {row["formula_id"]: row["result"] for row in verification["results"]}
        self.assertEqual(results, {"phi_1": "TRUE", "phi_2": "TRUE", "phi_3": "FALSE"})
        self.assertIn("formal consistency", verification["semantics"])
        self.assertLessEqual(verification["inputs"]["stage2_saved_at"], verification["inputs"]["semantic_trace_loaded_at"])
        evaluation = json.loads((result.analysis_dir / "evaluation.json").read_text())
        self.assertEqual(evaluation["attribution"]["kind"], "ANONYMOUS_TRACK")
        self.assertEqual(evaluation["semantic_hypotheses"]["TP"], 2)
        self.assertEqual(evaluation["semantic_hypotheses"]["identity_hallucination_rate"], 0.0)
        metadata = json.loads((result.analysis_dir / "request_metadata.json").read_text())
        for key in ("provider", "model", "prompt_versions", "facts_schema_version", "forensic_packet_sha256",
                    "created_at", "stages", "determinism"):
            self.assertIn(key, metadata)
        self.assertEqual(metadata["stages"]["explanation"]["usage"]["input_tokens"], 1000)
        self.assertNotIn(SECRET, json.dumps(metadata))

    def test_naming_c_is_an_identity_hallucination(self):
        answer1 = stage1_answer(actor="C", subject="C", fact=self.cut_fact, text="Vehicle C cut in front of A.")
        answer2 = {"formulas": [formula_item("phi_1", "F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)")],
                   "untestable_claims": []}
        result = self.analyse("gemini", answer1, answer2)
        stage1 = json.loads((result.analysis_dir / "stage1_explanation.json").read_text())
        self.assertEqual(stage1["validation"]["status"], "INVALID")
        self.assertEqual(stage1["answer"]["responsibility"]["actor"], "C")  # recorded as given, not corrected
        codes = {issue["code"] for issue in stage1["validation"]["issues"]}
        self.assertIn(INVALID_IDENTITY_HALLUCINATION, codes)
        verification = json.loads((result.analysis_dir / "verification.json").read_text())
        self.assertEqual(verification["results"][0]["result"], "UNKNOWN")
        evaluation = json.loads((result.analysis_dir / "evaluation.json").read_text())
        self.assertEqual(evaluation["attribution"]["kind"], "NOT_IN_RECONSTRUCTION")
        self.assertEqual(evaluation["semantic_hypotheses"]["identity_hallucination_rate"], 0.5)

    def test_verifier_can_be_rerun_without_any_model_call(self):
        answer1 = stage1_answer(fact=self.cut_fact)
        answer2 = {"formulas": [formula_item("phi_1", "F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, A:track_001)")],
                   "untestable_claims": []}
        result = self.analyse("openai", answer1, answer2)
        first = json.loads((result.analysis_dir / "verification.json").read_text())
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("no network")):
            verification, _ = verify_analysis(result.analysis_dir, load_llm_config())
        self.assertEqual([r["result"] for r in verification["results"]], [r["result"] for r in first["results"]])

    def test_dry_run_never_calls_and_unavailable_provider_does_not_crash(self):
        transport = FakeTransport("openai", [])
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
            result = run_analysis(self.run, AnalysisOptions(provider="openai", dry_run=True), load_llm_config(),
                                  transport=transport)
        self.assertEqual((result.status, transport.calls), ("DRY_RUN", []))
        preview = json.loads((result.analysis_dir / "request_preview.json").read_text())
        self.assertEqual(preview["explanation"]["request"]["headers"]["Authorization"], "Bearer <redacted>")
        self.assertNotIn(SECRET, json.dumps(preview))
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": ""}), \
                mock.patch("src.cdf.llm.pipeline.repo_root", return_value=Path(self.tmp.name)):
            result = run_analysis(self.run, AnalysisOptions(provider="openai"), load_llm_config(), transport=transport)
        self.assertEqual(result.status, "PROVIDER_UNAVAILABLE")
        self.assertFalse((result.analysis_dir / "stage1_explanation.json").exists())
        self.assertEqual(transport.calls, [])

    def test_oracle_mode_is_kept_apart(self):
        if not (self.run / "reconstruction" / "evaluation" / "evaluation.json").exists():
            self.skipTest("no privileged evaluation")
        main_packet = (self.run / "reconstruction" / "llm" / "forensic_packet.json").read_bytes()
        answer1 = stage1_answer(actor="C", subject="C", fact=self.cut_fact, text="Vehicle C cut in front of A.")
        answer2 = {"formulas": [formula_item("phi_1", "F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, C)")],
                   "untestable_claims": []}
        transport = FakeTransport("openai", [answer1, answer2])
        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": SECRET}):
            result = run_analysis(self.run, AnalysisOptions(provider="openai", oracle_identities=True),
                                  load_llm_config(), transport=transport)
        self.assertIn("llm_oracle", result.analysis_dir.parts)
        self.assertEqual((self.run / "reconstruction" / "llm" / "forensic_packet.json").read_bytes(), main_packet)
        self.assertFalse((self.run / "reconstruction" / "llm" / "runs").exists())
        sent = json.dumps(transport.calls[0]["body"])
        self.assertIn('\\"C\\"', sent)  # the oracle packet names C ...
        self.assertNotIn("PRIVILEGED", sent)  # ... but carries no marker into the prompt
        stage1 = json.loads((result.analysis_dir / "stage1_explanation.json").read_text())
        self.assertEqual(stage1["validation"]["status"], "VALID", stage1["validation"])
        evaluation = json.loads((result.analysis_dir / "evaluation.json").read_text())
        self.assertEqual(evaluation["semantic_hypotheses"]["TP"], 2)
        notice = json.loads((self.run / "reconstruction" / "evaluation" / "llm_oracle" /
                             "oracle_identities.json").read_text())
        self.assertTrue(notice["_notice"].startswith("PRIVILEGED"))
        self.assertEqual(notice["identities"].get("A:track_001"), "C")

    def test_verifier_on_the_real_s17_trace(self):
        trace = SemanticTrace.load(self.run, VOCABULARY)
        def result(text):
            return trace.evaluate(parse_formula(text), at=0.0)["result"]
        self.assertEqual(result("F[-3,0] event(CUT_IN_FROM_RIGHT_START, A, A:track_001)"), "TRUE")
        self.assertEqual(result("BEFORE(event(EGO_PATH_ENTRY, A, A:track_001), event(COLLISION, A, B))"), "TRUE")
        self.assertEqual(result("F[-5,0] event(BRAKE_START, A)"), "FALSE")
        self.assertEqual(result("F[-5,0] event(CUT_IN_FROM_RIGHT_START, A, C)"), "UNKNOWN")
        self.assertEqual(result("F[3,4] state(CLOSING, A, A:track_001)"), "UNKNOWN")  # lost at +1.9 s
        self.assertEqual(result("F[-5,0] state(CLOSING, A, B)"), "TRUE")


if __name__ == "__main__":
    unittest.main()
