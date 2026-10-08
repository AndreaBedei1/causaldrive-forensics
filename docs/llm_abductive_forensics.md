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
`surface_offset_m`, `relative_motion_angle_deg`, `ego_speed_mps`.  Never exported: events, perceived states,
graphs, the report, the evaluation, ground truth, the run's `metadata.json`, the scenario configuration.

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

## 7. Providers and reproducibility

- `cdf.llm.providers`: `BaseLLMProvider` with `OpenAIProvider` (Responses API, `text.format` strict JSON
  schema, `store: false`) and `GeminiProvider` (`generateContent`, `responseMimeType` +
  `responseJsonSchema`, key in the `x-goog-api-key` header).  Models in `configs/llm.yaml` (`gpt-5.6-sol`,
  `gemini-3.7-flash`), overridable with `--model`; urllib only, retries with back-off on 408/409/429/5xx.
- Keys: `OPENAI_API_KEY`, `GEMINI_API_KEY` from the environment or `.env` (ignored by git; `.env.example`
  tracked, empty).  Missing key = provider unavailable (exit code 3), no crash.  Keys are never printed,
  saved or put in errors (redacted).
- Per analysis (`reconstruction/llm/runs/<provider>_<model>_<UTC time>/`): `request_metadata.json` (provider,
  model, prompt and schema versions, packet SHA-256, timestamps, parameters sent, token usage, latency,
  attempts and errors), `stage1_explanation.json` and `stage2_formula.json` (prompts, raw answer, parsed
  answer, validation), `verification.json`, `evaluation.json`; `request_preview.json` for a dry run.
- Temperature 0 is sent (an OpenAI reasoning model that rejects it is called again without, and the analysis
  says so); Gemini also gets a fixed seed; the Responses API has no seed.  Determinism is not claimed: repeat
  runs are needed to measure variation (none yet).

## 8. Commands

```
python scripts/export_forensic_facts.py traces/S17/run_0_crash
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --dry-run
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --stage explanation
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --stage formalize
python scripts/verify_llm_analysis.py traces/S17/run_0_crash/reconstruction/llm/runs/<analysis>
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --oracle-identities   # privileged
```

## 9. Caveats

- No model has been called yet (no keys): providers, schemas and the pipeline are tested with mock transports
  that reproduce the documented response formats; the configured model names are the ones requested and are
  not verified against the providers' catalogues.
- The packet is large (S17: ~92 k characters, all facts at 10 Hz); no subsampling is applied.
- Recorder frames are not related to each other (no map frame): the model cannot overlay positions of
  different recorders directly; relative geometry comes from each recorder's own tracks.
- The same physical road user seen by two recorders is two anonymous ids unless the reconstruction associated
  them (S17: `A:track_001`, `B:track_002` and `B:track_003` are all C).
- Formulas can only be as precise as the trace: event times are quantised to 0.05 s, states to the 10 Hz
  perceived-state frames refined by the event times; a hypothesis about an unobserved interval is UNKNOWN.
- The evaluation's recall is against the complete reconstructed trace (including events no explanation would
  mention); it is a coverage figure, not an accuracy figure.
- Oracle mode is infrastructure only: no campaign has been run.
