# LLM abductive forensics

FACTS -> abductive explanation -> semantic hypotheses -> temporal formulas -> formal verification on the
reconstructed semantic trace.

Research question (first studied on S17): *how does partial observability of a causally relevant but
non-colliding road user affect accident explanation and attribution?*

## 1. Three bodies of information, kept apart

| | what | who may read it |
|---|---|---|
| admissible facts | measured ego motion and controls, radar tracks (identified only where the reconstruction associated them), sign detections, collision reports, the supplied context (speed limit, road environment) | the model (`reconstruction/llm/forensic_packet.json`) |
| reconstructed semantic trace | events (`CRITICAL_TTC_*`, `CUT_IN_*`, `BRAKE_*`, ...), perceived states, local / global graphs, `report.md` | the deterministic verifier only, after both model answers are saved |
| privileged ground truth | simulator states, true identities, scenario configuration, counterfactual runs | the privileged evaluation and the oracle mode only (`reconstruction/evaluation/`) |

Nothing produced by the LLM pipeline is written back into the reconstruction; the reconstruction was not
changed for it.

## 2. Pipeline

```
 <run>/reconstruction/                      (semantic reconstruction, unchanged)
   <R>/local_trace.jsonl --facts only-->  ┐
   <R>/local_graph.json  --clock, collision reports, footprint
   global/alignment.json --offsets, collision matching
   global/associations.json --ASSOCIATED / ANONYMOUS
 <run>/vehicles/<R>/{metadata.json, traffic_signs.jsonl}
 <run>/incident_context.json                                      │
                                                                  ▼
                     scripts/export_forensic_facts.py   (cdf.llm.facts, allowlist)
                                                                  │
                    reconstruction/llm/forensic_facts.jsonl  (canonical, one fact per line)
                    reconstruction/llm/forensic_packet.json  (same facts, columnar; neutral run_id)
                                                                  │  leak guard: fail closed
                                                                  ▼
 Stage 1 (one call)   prompts/accident_abduction_v1.txt + packet + supplied context + vocabulary
                      -> explanation, primary_hypothesis, causal_chain, responsibility,
                         alternative_hypotheses, semantic_hypotheses, unresolved_entities
                      -> validated (schema, ids, fact ids, event types); saved as given
                                                                  │
 Stage 2 (a separate call)  prompts/formalize_hypothesis_v1.txt + packet + Stage-1 answer
                      + vocabulary + grammar -> formulas (formula_text + formula_ast), untestable claims
                      -> validated (grammar, AST, references); saved as given
                                                                  │  both answers on disk
                                                                  ▼
 verifier (no model call)   loads the semantic trace only now -> TRUE / FALSE / UNKNOWN per formula
 evaluation                 semantic hypotheses vs trace events: TP / FP / FN, precision, recall, F1,
                            hallucination and identity-hallucination rates, attribution kind

 oracle branch (--oracle-identities, PRIVILEGED - NOT ADMISSIBLE INPUT)
   anonymous tracks renamed to their true identities -> reconstruction/evaluation/llm_oracle/
```

## 3. Admissible facts (`cdf.llm.facts`)

| type | fields |
|---|---|
| EGO_MOTION | recorder, t_local_s, t_global_s, speed, acceleration, yaw rate, x / y, heading (recorder frame) |
| EGO_CONTROL | throttle, brake, steer (raw) |
| TRACK_STATE | recorder, observed_subject, local_track_id, identity_status, radar, range, clearance, bearing, longitudinal / lateral, x / y, vx / vy, target speed, estimated target acceleration, relative longitudinal / lateral speed, pos / vel std, measured, t_cpa, d_cpa, d_cpa_clearance, closing speed, closing_ttc_s (geometric) |
| SIGN_DETECTION | recorder, sign id, class, confidence, first / confirmed / last time (local and global), relevant_to_own_path, min bearing, number of detections |
| COLLISION_OBSERVATION | participants (recorders whose reports matched), per-recorder report (local / global time, peak impulse), matching (status, impulse similarity, confidence), time_origin |

Removed from TRACK_STATE (`TRACK_STATE_REMOVED`): `encounter`, `motion_relation`, `collision_course`, `ttc_s`,
`predicted_overlap_s`, `required_deceleration_mps2`, `avoidance_by`, `braking_margin_mps2`,
`unavoidable_by_braking`, `critical`, `target_acceleration_used_mps2`, `estimate_known`, `ahead_of_front_m`,
`surface_offset_m`, `relative_motion_angle_deg`, `ego_speed_mps`, and the safe-following-distance outputs of
the conflict model (`critical_reason`, `forward_region`, `forward_leader`, `longitudinal_clearance_m`,
`lateral_body_gap_m`, `time_headway_s`, `minimum_time_gap_s`, `time_gap_distance_m`, `required_safe_distance_m`,
`safe_distance_margin_m`, `line_of_sight_occluded`; the leak guard refuses them too).  Never exported: events,
perceived states, graphs, the report, the evaluation, ground truth, the run's `metadata.json`, the scenario
configuration.

- Identity: an ASSOCIATED track is exported as `observed_subject = B`, `local_track_id = A:track_002`,
  `identity_status = ASSOCIATED`; every other track as `observed_subject = A:track_001`, `ANONYMOUS`.  No
  association is added for the model.
- Time: an aligned recorder's facts carry `t_local_s` and `t_global_s = t_local_s + offset_to_global`; an
  unaligned recorder's carry `t_global_s = null` (no invented global time); a track gets the global time of
  its observer.
- `run_id` = `case-` + the first 16 hex digits of the SHA-256 of the canonical facts: never a directory name.
- Packet (`cdf.forensic_packet/1`): schema_version, facts_schema_version, run_id, supplied_context (marked as
  supplied), known_recorders (clock, observation window, footprint, radar coverage), entities,
  field_definitions, facts (columnar per type).  It reorganises the facts deterministically: no fact added,
  removed or interpreted (tested: lossless, stable hash).

Leak guard (`cdf.llm.guard`): a key containing `ground_truth`, `expected`, `culprit`, `scenario`, `variant`,
`semantic_trace`, `perceived_state`, `events`, `critical`, `collision_course`, `required_deceleration` (and
the other conflict-model names), a key `ttc_s`, any vocabulary event name inside the packet, any scenario id /
name / variant name, `traces/` path or run directory name: the export is refused and no request is sent.
The prompt templates' own text is checked the same way (the vocabulary, grammar and the model's previous
answer are the exempt blocks).

## 4. Vocabulary, prompts, schemas

- `configs/semantic_vocabulary.yaml`: the 33 event types of the reconstruction (tested identical to
  `cdf.reconstruction.models.SAME_TIME_ORDER`) with a one-line conceptual description and the accepted actor
  / subject; the 14 states as START / END pairs.  No thresholds, formulas or implementation details.
- `prompts/accident_abduction_v1.txt`, `prompts/formalize_hypothesis_v1.txt`: versioned; a change is a new
  file.  "Responsible" is defined as causal contribution through traffic behaviour, not a legal verdict;
  UNKNOWN is encouraged; ids must come from the packet.
- Stage-1 schema (`cdf.llm.stage1/1`): `explanation`, `primary_hypothesis`, `causal_chain[]` (step, claim,
  actor_id, time_reference, estimated_time, evidence_fact_ids), `responsibility` (actor, assessment,
  confidence, limitations), `alternative_hypotheses[]`, `semantic_hypotheses[]` (event_type from the
  vocabulary, actor_id, subject_id, time_reference, estimated_time, time_window, confidence,
  evidence_fact_ids), `unresolved_entities[]`.
- Stage-2 schema (`cdf.llm.stage2/1`): `formulas[]` (formula_id, claim_ref, claim, formula_text, formula_ast
  as a node table) and `untestable_claims[]`.
- Only keywords both providers accept in structured-output mode are used (type with `null` in a type list,
  properties, required, `additionalProperties: false`, items, enum, anyOf, description); ranges and
  cross-references are checked after the answer is saved.  An id that is not in the packet (for S17: "C") is
  `INVALID_IDENTITY_HALLUCINATION`, recorded and never corrected.

## 5. Temporal logic and verifier

Grammar (`cdf.llm.formal.grammar`): AND, OR, NOT, `F[a,b]` (EVENTUALLY), `G[a,b]` (ALWAYS), `BEFORE(p, q)`
(sugar for `F[-inf,inf](p AND F(0,inf] q)`), `event(TYPE, actor[, subject])`, `state(STATE, actor[,
subject])`.  Bounds in seconds relative to the evaluation instant (t_global = 0, the time-origin collision),
possibly negative or infinite.  The verifier evaluates only `formula_ast`; `formula_text` is parsed to report
whether the two agree.

Semantics (`cdf.llm.formal.verifier`): Kleene three-valued logic on a 0.05 s grid of global time.  UNKNOWN
when the subject was not being tracked by that recorder (before its appearance, after TRACK_LOST, a track of
another recorder), when the perceived state was UNKNOWN, when an id is not known to the reconstruction,
outside the recorded interval (finite bounds), or for a recorder without global time.  Absence of evidence is
FALSE only while the recorder was observing.  The verdict is called **formal consistency of the LLM
hypothesis with the reconstructed semantic trace**: TRUE does not prove that X caused Y.

## 6. Evaluation

Semantic hypotheses against every event of the trace (except, by default, states already active at the first
observation): one-to-one matching on type, actor, subject (identities resolved; COLLISION parties in either
order) and time within `time_tolerance_s` (0.5 s, `configs/llm.yaml`) or inside the hypothesis window widened
by it.  Reported: TP, FP, FN, precision, recall, F1, hallucination rate (no event of that type / actor /
subject at any time), identity hallucination rate (an id not in the packet), mean time error, and the kind of
the attributed actor (RECORDER, ANONYMOUS_TRACK, TRACK_IDENTIFIED_AS_RECORDER, NOT_IN_RECONSTRUCTION,
UNKNOWN).  On S17 a correct answer attributes the cut-in to `A:track_001`, never to "C".

## 7. Providers, models and reproducibility

- `cdf.llm.providers`: `BaseLLMProvider` with `OpenAIProvider` (Responses API, `text.format` strict JSON
  schema, `store: false`) and `GeminiProvider` (`generateContent`, `responseMimeType` +
  `responseJsonSchema`, key in the `x-goog-api-key` header); urllib only.
- Models (`configs/llm.yaml`):
  - OpenAI is **locked** to `gpt-6-luna` with `reasoning.effort: high`; no temperature is sent;
    `max_output_tokens` 32 000 (reasoning + answer; OpenAI advises reserving at least 25 000 for reasoning
    models).  `--model` with another OpenAI model is refused and nothing ever falls back to another OpenAI
    model (not after an error, an unavailable model, a rejected feature or a quota): the analysis stops and
    reports.  Changing the OpenAI model is Andrea's decision, with his explicit approval, made in the
    configuration (`model`, `model_locked`), never by the tool.
  - Gemini: `gemini-3.8-flash` (primary, default) and `gemini-3.5-flash-lite` (second model: comparison on
    the same packet, and new analyses once the 3.8 daily quota is used up), both with
    `generationConfig.thinkingConfig.thinkingLevel: high`; no `temperature`, `topP`, `topK`,
    `candidateCount`, `seed` or legacy `thinkingBudget` (Gemini 3 keeps its default sampling; the provider
    refuses these settings); `maxOutputTokens` 32 000 (thinking + answer; both models allow 65 536).
- One analysis = one model.  Stage 1 and Stage 2 always use the model recorded in `request_metadata.json`;
  continuing an analysis with another model is refused.  A quota error stops the analysis:
  `QUOTA_EXHAUSTED` at Stage 1, `INCOMPLETE_QUOTA` at Stage 2 with Stage 1 saved (complete it later with the
  same model, `--stage formalize --analysis-dir <dir>`).  Errors are classified (quota, rate limit,
  transient, network, time-out, fatal); retries repeat the identical request, only after transient or
  rate-limit errors (OpenAI at most once, never after a client time-out; a Gemini per-minute limit waits the
  delay the API asks for); no parameter is ever dropped or changed between attempts.
- Keys: `OPENAI_API_KEY`, `GEMINI_API_KEY` from the environment or `.env` (ignored by git; `.env.example`
  tracked, empty).  Missing key = provider unavailable (exit code 3), no crash.  Keys are never printed,
  saved or put in errors (redacted, including echoed error bodies).  `scripts/check_llm_access.py` checks
  them, and access to every configured model, from the model-metadata endpoints only (OpenAI
  `GET /v1/models/<model>`, Gemini `models.get`): nothing is generated, only VALID / INVALID and YES / NO are
  printed.
- Per analysis (`reconstruction/llm/runs/<provider>_<model>_<UTC time>/`): `request_metadata.json` (provider,
  exact model id, model policy, reasoning / thinking settings, prompt and schema versions, packet SHA-256,
  timestamps, per stage: model, parameters sent, response id, model reported by the API, token usage with
  reasoning / thinking tokens, latency, attempts and errors), `stage1_explanation.json` and
  `stage2_formula.json` (prompts, raw answer text, parsed answer, validation, and the provider's raw response
  body), `verification.json`, `evaluation.json`; `payload_audit.json` with `--audit-payload` (each request
  body checked against the run's semantic graph node ids, privileged file and field names and unrecorded
  participants before it is sent; the embedded packet's SHA-256); `request_preview.json` for a dry run.
- Determinism is not claimed: reasoning models are sampled with their defaults; repeat runs are needed to
  measure the variation.

## 8. Commands

```
python scripts/check_llm_access.py
python scripts/export_forensic_facts.py traces/S17/run_0_crash
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.8-flash
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.5-flash-lite
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --dry-run
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --stage formalize --analysis-dir <dir>
python scripts/verify_llm_analysis.py traces/S17/run_0_crash/reconstruction/llm/runs/<analysis>
python scripts/verify_llm_analysis.py <analysis> --out-dir <analysis>/reverification_<date> --note "<why>"
python scripts/compare_llm_analyses.py traces/S17/run_0_crash <analysis> <analysis> ... [--reverified <subdir>]
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --oracle-identities   # privileged
```

## 9. Caveats

- First real calls: 2026-10-08/09, S17 only: one analysis each with gpt-6-luna and gemini-3.5-flash-lite;
  gemini-3.8-flash gave no answer (HTTP 503 overload, then the free-tier daily quota; the 8 attempts are
  kept), so the 3.8 vs 3.5 Flash-Lite comparison is still to be run.  See
  `traces/S17/run_0_crash/reconstruction/evaluation/llm_comparison_S17.md`.  The automated tests never call
  a provider: they use fake transports that reproduce the documented response formats.  One answer per
  model measures nothing about the variation between runs.
- Re-verification: when the reconstruction changes but the packet does not (2026-10-09: CRITICAL_TTC with
  the safe following distance, CUT_IN with a pre-entry region; all 14 packets byte-identical), the saved
  answers stay valid inputs and only the deterministic verifier is run again, into
  `<analysis>/reverification_<date>/` (`verify_llm_analysis.py --out-dir`): the analysis's own
  `verification.json` / `evaluation.json` stay as they were, the new ones carry a `reverification` block
  (why, when, digests of the previous outputs and of the semantic trace used).  No model is called.
- Gemini free tier: `gemini-3.8-flash` allows 20 generateContent requests per day per project, and requests
  that fail with HTTP 503 (model overloaded) count.  The transient retries (up to 3 requests per stage) can
  therefore use up the day's quota during an overload without a single answer (2026-10-08: 20 x 503, then
  429 `GenerateRequestsPerDayPerProjectPerModel-FreeTier`; reset at about 00:00 UTC).
- The packet is large (S17: ~92 k characters, all facts at 10 Hz); no subsampling is applied.
- Recorder frames are not related to each other (no map frame): the model cannot overlay positions of
  different recorders directly; relative geometry comes from each recorder's own tracks.
- The same physical road user seen by two recorders is two anonymous ids unless the reconstruction associated
  them (S17: `A:track_001`, `B:track_002` and `B:track_003` are all C).
- Formulas can only be as precise as the trace: event times are quantised to 0.05 s, states to the 10 Hz
  perceived-state frames refined by the event times; a hypothesis about an unobserved interval is UNKNOWN.
- The evaluation's recall is against the complete reconstructed trace (including events no explanation would
  mention); it is a coverage figure, not an accuracy figure.
- The vocabulary descriptions the model receives do not state the reconstruction's thresholds: a turn needs a
  heading change of at least 15 degrees (a lane-change-like swerve is not a turn), `TRACK_APPEARED_FRONT`
  means a first bearing within 5 degrees.  A model that calls S17's evasive swerve `TURN_LEFT_START`, or a
  track ahead-right "front", gets FALSE / FP for a granularity mismatch, not for an invented manoeuvre.
- Oracle mode is infrastructure only: no campaign has been run.
