# Implementation checklist

Ticked only where the item was verified in the code or in a produced artifact.
Every item is ticked as of the final campaign; where a claim rests on a
measurement rather than on code being present, the note says which artifact
carries it.

## Repository

- [x] local Git repository, branch `main`
- [x] no GitHub remote, nothing pushed (`git remote -v` is empty)
- [x] clean package structure under `src/cdf/`
- [x] install instructions (`README.md`, `docs/ENVIRONMENT.md`)
- [x] dependency files tested: `pyproject.toml`, `requirements.txt`, `environment.yml`

## Data boundary

- [x] three structurally separate layers: `cdf.local`, `cdf.fusion`, `cdf.oracle`
- [x] no camera sensor anywhere in the package (asserted by test)
- [x] no privileged leakage into local records (record schemas have no such field)
- [x] automated anti-leakage tests — `tests/test_no_privileged_leakage.py`,
      26 tests: `ast`-level import isolation with correct relative-import
      resolution, forbidden simulator-API call detection, camera scan, schema
      field scan, recursive artifact key scan over synthetic **and** recorded
      runs, oracle-only event-type scan, scope-guard check, and self-tests that
      plant violations to prove each detector fires
- [x] the scan is not vacuous: the oracle subtree is asserted to *contain* the
      privileged fields the local subtree must not
- [x] CARLA actor ids are not used for track fusion — association scores
      trajectory RMSE, velocity and heading consistency only
- [x] collision identity split at the sensor: `drain_local()` strips the
      counterparty, `drain_privileged()` is oracle-only

## Recorder

- [x] 20 s pre-event rolling buffer
- [x] 5 s post-event capture
- [x] both configurable (`recorder.pre_event_s`, `recorder.post_event_s`)
- [x] bounded memory — ring buffer capacity asserted never to exceed
      `pre_event_s * sample_rate_hz`
- [x] persisted evidence artifacts with schema versions and a retention record

## Local pipeline

- [x] own telemetry, own controls, own radar
- [x] radar front-end: plausibility filter, stationary-target discriminator,
      clustering
- [x] multi-frame tracking with anonymous ids and one-to-one assignment
- [x] typed event extraction with hysteresis and debouncing
- [x] event graph (temporal/observational relations only)
- [x] causal DAG (causal hypotheses only), acyclicity enforced with recorded
      rejections

## Fusion

- [x] explicit clock alignment with diagnostics
- [x] track-to-participant association from trajectory evidence
      (Hungarian assignment, RESOLVED / AMBIGUOUS / UNRESOLVED)
- [x] event identity resolution, including the asymmetric case (A observing B's
      deceleration vs B's own deceleration event)
- [x] provenance: every fused node and edge lists all contributing participants
- [x] documented confidence fusion (noisy-OR), with the caveat that it is
      evidence accumulation and not a calibrated probability
- [x] contradiction retention — disagreements are kept and reported, never
      silently dropped
- [x] fused graph remains a DAG

## Graph analysis

- [x] ancestors, descendants, all causal paths, shortest path, root causes
- [x] vehicle-specific subgraph; confidence, provenance and time filters
- [x] node and edge removal with reachability reports
- [x] minimal outcome subgraph and candidate intervention nodes
- [x] local vs fused comparison and knowledge gain
- [x] GraphML alongside JSON for every graph

## Oracle

- [x] independent oracle logger recording exact state, true collision pairs,
      map context and traffic-light state
- [x] oracle graph built from the scenario causal template plus exact
      kinematics — **not** by re-running the local rules on ground truth
      (asserted: the oracle modules do not import `cdf.local.causal_rules`)
- [x] one multi-vehicle ground-truth graph per run
- [x] unrealised template edges reported rather than invented
- [x] never consumed by local or fused inference (scope guard + tests)

## Model checking

- [x] local temporal properties P1–P4 over finite traces
- [x] PASS / FAIL / UNKNOWN, with UNKNOWN as a first-class verdict
- [x] counterexample traces with violating intervals — written by
      `TraceChecker.check_and_persist` alongside the results, so a `FAIL` can
      never name a counterexample that does not exist; 147 FAILs, 147
      counterexamples, 0 dangling, asserted by a test over the artifacts
- [x] oracle-only properties kept separate and unable to affect inference

## Counterfactuals

- [x] intervention API (`disable`, `delay`, `advance`, `scale`, `set`) over
      named scripted actions
- [x] deterministic replays — identical map, spawn state, seed and parameters,
      differing in exactly one intervention
- [x] simulator restarted before each replay, because repeated runs in one
      server session drift enough to confound the comparison
- [x] collision / severity outcome comparison
- [x] causal-contribution artifacts with the raw outcomes retained
- [x] **executed against the live simulator** — 20 replays across five runs,
      each on a genuinely fresh simulator engine (see the launcher/engine finding
      in `docs/ENVIRONMENT.md`); results in `docs/EXPERIMENTAL_FINDINGS.md` §9

## Scenarios

- [x] S01 rear-end (crash + avoided)
- [x] S02 cut-in (crash + avoided)
- [x] S03 crossing
- [x] S04 crossing + braking (negative control)
- [x] S05 simultaneous crossing
- [x] S06 chain collision (both causal orders, validated)
- [x] S07 partial/occluded view (occluded + full-view control)
- [x] S08 multi-direction crossing
- [x] S09 roundabout (Town04)
- [x] never more than three participant vehicles (asserted in
      `ScenarioSpec.validate_static` and in run validation)

## Evaluation

- [x] event detection metrics (precision / recall / F1 / timing error)
- [x] track association metrics against oracle identity, scored only after
      inference
- [x] graph structure metrics including structural Hamming distance
- [x] fusion benefit: local vs best-local vs fused vs oracle, plus knowledge gain
- [x] attribution metrics, including single vs shared contribution and
      insufficient-evidence cases
- [x] model-checking metrics
- [x] the generic epistemic-honesty check (`evaluate_local_unknowns`)
- [x] **robustness / ablation sweep executed** — single-vehicle vs fusion over
      all 39 runs, local vs privileged-oracle gap throughout, and a four-profile
      radar degradation ablation (`scripts/run_ablation.py`) holding the
      encounter fixed while varying only the sensor profile. Its baseline
      profile doubles as a reproducibility control: re-recording the campaign's
      S01 run at a later commit reproduced it to the last recorded digit
      (`docs/EXPERIMENTAL_FINDINGS.md` §10)

## Viewer

- [x] works on stored artifacts, requires no simulator
- [x] 2D bird's-eye reconstruction with timeline playback
- [x] per-participant local views, fused view, oracle view
- [x] oracle view badged `PRIVILEGED GROUND TRUTH — EVALUATION ONLY`
- [x] telemetry, controls and TTC plots
- [x] radar detections and tracks with confidence
- [x] event timeline and causal-graph panels
- [x] model-checking violations with counterexample intervals
- [x] `INSUFFICIENT EVIDENCE` shown rather than forcing a culprit
- [x] no camera panel
- [x] one-command local serving, bound to `127.0.0.1`

## Testing

- [x] unit tests across schemas, ring buffer, radar geometry, tracking, events,
      graphs, fusion, checking and metrics
- [x] synthetic integration tests that drive the real pipeline without CARLA
- [x] CARLA smoke test, marked and skipped when no server is reachable — four
      tests covering the handshake and version match, fixed-step synchronous
      stepping, spawning a vehicle and radar that delivers frames, and leaving
      the world unmodified
- [x] tests over the recorded artifacts, not only the builders: the campaign is
      one experiment, all 183 persisted causal graphs are DAGs carrying the
      scope their location implies, and no `FAIL` has a dangling counterexample
- [x] **509 tests passing, 1 skipped** (`pytest -q -m "not carla"`), 514
      collected (447 unit, 41 integration, 26 data-boundary). The skip is the oracle-graph assertion on a synthetic fixture
      that does not build one; the other 4 are the CARLA-marked smoke tests.
      Two tests are marked `slow` (the whole-campaign artifact scans, ~95 s)

## Results

- [x] aggregate CSV/JSON — `artifacts/summary/`: runs, event, graph, fusion,
      association, attribution, model-check and scenario-validation tables
- [x] figures — 480 PNGs across the campaign, including three cross-run summary
      figures (local-vs-fused edge F1, scenario outcomes, and the finite-trace
      verdict distribution)
- [x] scenario validation table — `artifacts/summary/scenario_validation.csv`;
      39 of 39 runs pass
- [x] `docs/EXPERIMENTAL_FINDINGS.md` written from actual outputs only, with
      `scripts/extract_findings.py` reproducing every number from the artifacts
- [x] `docs/LIMITATIONS.md`

## Reproducibility

- [x] exact commands in `README.md`
- [x] environment versions recorded (`docs/ENVIRONMENT.md`, every manifest)
- [x] seeds recorded, with the per-seed perturbation recorded explicitly
- [x] configuration and its hash recorded in every manifest
- [x] one-command scenario run, suite run, evaluation and viewer
- [x] simulator restarted per run, which is what actually makes runs reproducible
- [x] SHA-256 digests of every artifact in `evidence_manifest.json`, written at
      the end of a recording and refreshed by
      `scripts/reprocess_runs.py --stages manifest`; **63 of 63 run directories
      verify** with `scripts/verify_evidence.py`
