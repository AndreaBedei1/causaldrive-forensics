# Experiment protocol

---

## 1. The experimental unit

One **run** = one `(scenario, variant, seed)` triple, executed end to end and
persisted under `artifacts/<SCENARIO>_<name>/seed_<nnn>[_<variant>]/`
(`RunLayout.create`).

Its identity is `make_run_id(scenario_id, seed, variant, config_hash)`:

```
S01-crash-seed000-0b81b521
```

The trailing token is the first 8 hex of `Config.hash`, a 16-hex digest of the
*fully merged* configuration (defaults + sensor profile + scenario + overrides,
normalised and key-sorted). A run therefore carries the exact parameter set that
produced it in its own name, and two runs whose ids differ only in that token are
the same experiment under different parameters.

### Seeds

The seed is a single integer threaded through everything the client controls:

| Consumer | Use |
|---|---|
| `ScenarioWorld.rng` | deterministic blueprint colour selection |
| Traffic Manager | `set_random_device_seed(seed)` (background behaviour only; never in the safety-critical path) |
| `ParticipantAgent._rng` | `(seed * 1000003) ^ (hash(participant_id) & 0xFFFF)` -- a **separate stream per participant**, so adding a third vehicle cannot perturb the first two's degraded-radar draws |
| `RadarFrontEnd` | consumes that stream for `apply_degradation` |

The recommended campaign is `SEEDS = 0 1 2` (`make suite SEEDS="0 1 2"`). Repeated
seeds are **not** a noise-averaging device in the statistical sense: given a fresh
simulator, a re-run of seed 0 reproduces seed 0 exactly. They vary the parts of
the scenario the seed actually controls, and they guard against a result that
depends on one lucky initial condition.

#### The simulator must be restarted between runs

Reproducibility is conditional on that "given a fresh simulator", and it was
measured rather than assumed. Running S05 three times **in one server session**
with an identical specification and seed gave minimum separations of 6.996 m,
6.687 m and 6.228 m -- drifting monotonically, with final positions a metre
apart. Running the same specification twice, each on a **freshly started server
process**, reproduced it exactly: 3.453 m minimum separation, collision at
t = 3.75 s, identical final pose.

The drift is accumulated simulator state we cannot reach through the API: actors
are destroyed and world settings restored between runs regardless. And it is not
a small numerical nuisance -- the drifted result and the reproducible one differ
by enough to flip the outcome class (near miss versus collision).

Every recorded run therefore starts its own simulator process, at a cost of about
45 s per run. Reusing one server for a whole campaign is roughly three times
faster and produces results that cannot be reproduced.

The same applies with more force to counterfactual replays, which are explicitly
*comparisons*: `counterfactual.restart_server_per_replay` defaults to true so
that the factual and counterfactual runs differ in the intervention rather than
in accumulated state.

### Variants

A variant is a deep-merge over the base `scenario` block, with per-participant
deltas keyed by participant id (`participant_overrides`). The variants that exist:

| Scenario | Variants | Role of the non-default |
|---|---|---|
| S01 | `crash`, `avoided` | negative control: same geometry, timely response |
| S02 | `crash`, `avoided` | negative control: same geometry and cut-in, timely response |
| S06 | `a_front_pushed`, `b_rear_first` | same layout, **opposite causal order** |
| S07 | `occluded`, `full_view` | control: A on the baseline radar instead of narrow-FOV |
| S03, S04, S05, S08 | single variant each | S04 is itself the negative control for S03 |

Variants and seeds are orthogonal: the campaign is scenarios x variants x seeds.

### Sensor profiles

`configs/sensors/` holds five profiles, selected by `sensors.profile` or per
participant by `ParticipantSpec.sensor_profile`:

| Profile | FOV | Range | Degradation |
|---|---|---|---|
| `radar_baseline` | 120° | 90 m | none |
| `radar_narrow_fov` | **30°** | 100 m | none |
| `radar_noisy` | 120° | 90 m | 10 % point dropout; σ = 0.45 m / 0.020 rad / 0.40 m/s |
| `radar_dropout` | 120° | 90 m | 35 % frame dropout, 30 % point dropout, light noise |
| `radar_degraded` | **45°** | 70 m | 25 % frame + 25 % point dropout; σ = 0.60 m / 0.030 rad / 0.60 m/s |

All five mount one front radar at `(x 2.2, y 0.0, z 1.0)`, yaw 0°, 10° vertical
FOV, `sensor_tick_s = 0.05`. Degradation is applied **after acquisition** in the
local front-end, never by asking the simulator for a worse sensor, so every
profile is reproducible from the seed and "what would B have seen with a degraded
radar?" is a controlled, re-runnable experiment.

---

## 2. Gate progression

Each gate must hold before the next result means anything. Every gate is a
recorded artifact, not a judgement call.

### Gate 0 -- environment

`import_carla()` succeeds; a server answers at `simulation.host:port`;
`connect_with_retry` reports matching client/server versions.
**Artifact:** `environment_block()` inside `manifest.json` (Python version, CARLA
version, platform, git commit, package version).

### Gate 1 -- the scenario is well formed

`ScenarioSpec.validate_static()`: 2--3 participants, unique participant ids,
unique action ids, `expected_collision_pairs` naming real participants, every
`intervention_candidates` entry a declared action, a known `expected_outcome`.
A problem **raises** before the simulator is touched.

### Gate 2 -- the run produced its declared encounter

`validate_run(spec, oracle, agents, cfg)` → `scenario_validation.json` with
`passed` and an explicit `problems` list, also copied into `RunManifest.notes`:

* the expected outcome occurred (collision / near miss / no event);
* every `expected_collision_pairs` entry occurred, and any
  `expected_collision_order` matched;
* the `validation.encounter_pair` came closer than `min_separation_below_m`
  (measured with the privileged `OracleLogger.min_separation`);
* every participant recorded radar frames, and missed at most 25 % of them;
* every participant actually moved (privileged max speed ≥ 0.5 m/s).

**A failed Gate 2 invalidates every downstream number for that run.** This is what
stops a scenario that quietly stopped colliding -- because a controller gain or a
map changed -- from poisoning a campaign average.

### Gate 3 -- the evidence is usable

Per participant: the recorder's `meta["recorder"]` block (retained counts, window,
discards) and `sensor_health` (frames seen, missed, queue drops). A participant
with zero tracks is *not* a gate failure -- it is a legitimate result (B in S01) --
but a participant with zero *radar frames* is.

### Gate 4 -- local inference ran

`vehicle_*/events.json`, `event_graph.json`, `causal_graph.json` exist with
`scope = local`; the causal graph is acyclic (verified, not assumed, by
`build_causal_graph`).

### Gate 5 -- fusion ran

`fusion/association_report.json`, `fused_causal_graph.json` (scope `fused`) and
`fusion_diagnostics.json` exist; `diagnostics["dag"]["is_dag"]` is true; the
time-alignment diagnostics carry no `error`-severity entry.

### Gate 6 -- the oracle exists

`oracle/oracle_trace.jsonl.gz` and `oracle/oracle_summary.json` exist.
`load_oracle_trace()` raises rather than returning an empty trace, because a
silent empty trace would turn every downstream comparison into a vacuous pass.

### Gate 7 -- evaluation

`evaluate_run` writes `evaluation/metrics.json`. Its central discipline:
**absent is not zero.** Every metric block is computed only when its inputs exist;
when they do not, the block is `None` and a `reasons` entry names the missing
artifact. A run whose oracle graph was never built must not be reported as a
reconstruction that scored 0.0 -- that is a fabricated result and it would drag
every campaign average down. `_assert_evaluation_path` enforces that nothing is
ever written back into `vehicle_*/` or `fusion/`.

---

## 3. Metric definitions

All comparison metrics are computed by `cdf.graph.metrics`, from the
tolerance-correct matcher in `cdf.graph.matching`. The *same* code path, tolerance
and node correspondence are used for every local graph, for the fused graph and
for the oracle reference, so a delta cannot be an artifact of three slightly
different comparison procedures.

### 3.1 Matching

`match_events(a, b, tolerance_s, require_same_type, …)` is a **globally optimal
one-to-one assignment** (Hungarian, `scipy.optimize.linear_sum_assignment`)
minimising total absolute timing error, not a greedy nearest-neighbour pass: a
greedy pass over a dense burst of events (`RANGE_DECREASING` fires repeatedly
while a target closes) can consume the partner of a later, better pair and inflate
the false-negative count. Inadmissible pairs are priced at `1e9` and dropped
afterwards.

The solve runs on **canonically ordered** copies of both lists, so the result is a
function of the two event *sets* and not of the caller's listing order; three
numerically negligible tie-breakers (prefer the same participant `1e-6`, the same
subject `1e-7`, the same event id `1e-9`) make the optimum unique in the common
cases.

Contract, from `configs/default.yaml`:

| Key | Value |
|---|---|
| `evaluation.event_match.time_tolerance_s` | **1.5 s** |
| `evaluation.event_match.require_same_type` | **true** |
| `evaluation.graph_match.use_matched_nodes_only` | **true** |
| `evaluation.association.count_unresolved_as_miss` | **true** |

### 3.2 Counting

```
precision = tp / (tp + fp)        recall = tp / (tp + fn)
f1        = 2 * p * r / (p + r)
```

with **0.0 for an undefined quantity, not `nan`**: a graph that predicted nothing
has precision 0, not "no opinion", and a mean over scenarios must not be poisoned
by a `nan`. An empty prediction and an entirely wrong prediction are scored the
same, which is the conservative reading for a forensic claim.

### 3.3 Event metrics (`event_metrics`)

A matched pair is a true positive, an unmatched prediction a false positive, an
unmatched reference event a false negative. Timing error is reported as **mean and
median** (plus max), because the two answer different questions: the mean exposes
a systematic lag in the detector, the median is robust to the single badly placed
event a burst of radar returns can produce.

### 3.4 Graph-structure metrics (`graph_structure_metrics`)

Nodes are paired by `match_events`; edges are then classified by `match_edges`
under that pairing, edge identity being `(mapped_source, mapped_target,
edge_type)`:

| Class | Meaning |
|---|---|
| `matched` | the same triple on both sides |
| `extra` | in the prediction only -- a false positive |
| `missing` | in the reference only |
| `reversed` | the *swapped* triple exists in the reference while the straight one does not |

A **reversal is its own category**, reported once, never as one `missing` plus one
`extra`: the pair of events *was* linked and only the direction of the claim is
wrong, which is a different failure.

```
SHD = n_missing + n_extra + n_reversed
```

A reversal costs **one** edit, not two -- flipping an arrow is a single operation,
and charging it twice would make a graph that found every causal pair but got one
direction wrong look worse than a graph that missed the pair entirely.

For precision/recall a reversal *is* charged to both sides (it is simultaneously a
wrong prediction and a missed reference edge), and only exact matches are true
positives:

```
edge_precision/recall = prf1( n_matched , n_extra + n_reversed , n_missing + n_reversed )
```

**Edges touching an unmatched node.** By default they are still counted -- a
reference edge onto a node the prediction never found is a genuine miss. This
matters for the central experiment: a vehicle that observed one third of a crash
must not be able to report perfect edge recall on the third it saw, because that
would make fusion look worthless. `restrict_to_matched_nodes` (the
`evaluation.graph_match.use_matched_nodes_only` convention) compares structure on
the shared skeleton instead; either way `n_edges_touching_unmatched_pred/truth`
report how many edges were affected, so the two conventions can be reconciled
after the fact.

### 3.5 The central comparison: local vs fused

`compare_local_vs_fused` scores every local graph, the fused graph, and their
difference. **Fusion is only worth its complexity if it beats the *best* single
onboard reconstruction, not the average one** -- averaging would let a participant
that saw nothing flatter the fused result. The best local graph is therefore
selected explicitly by `_rank_key`: edge F1 first (the structural claim under
test), node F1 as a tie-break, then the *lower* SHD, then the participant id for
reproducibility. Reported deltas (`delta_edge_f1`, `delta_node_f1`, `delta_shd`)
are against that baseline.

`fusion_benefit` adds the strict verdict:

```
fusion_helped = (delta_edge_f1 > 0.0) or (delta_shd < 0)
```

Deliberately strict. A run where fusion changes nothing reports `False` with zero
deltas; a run where fusion makes things *worse* reports negative deltas. **Both are
results, not bugs, and both survive into the aggregate tables.** Alongside it,
`knowledge_gain` names the oracle-relevant nodes and edges the fused graph
recovered and the best local baseline lacks (see `docs/GRAPH_FUSION.md` §8) --
claims the fused graph adds that the *reference* does not contain are false
positives, not gains.

### 3.6 Association metrics

Identity resolution is scored against the oracle's true track identities, and the
true identity is looked up **only after** the inference has been made and
persisted. Because `UNRESOLVED` is a legitimate verdict, this cannot be scored as
plain classification: per-track verdicts are `correct`, `incorrect`, `unresolved`
and **`no_ground_truth`** -- a track the oracle cannot attribute to any
participant (road furniture, a reflection) is *not* evidence that association was
wrong. `evaluation.association.count_unresolved_as_miss` (true) decides whether an
abstention counts against recall. Reported: the four counts, precision, recall,
F1, mean assignment confidence, mean trajectory RMSE, and a per-track table
carrying both the claimed and the true identity.

### 3.7 Attribution metrics

`evaluate_attribution` compares the causal actions the counterfactual layer put
forward against the scenario's designed initiators (`causal_template`), and
reports -- **separately, on purpose**:

* the causal-action **set** score (precision / recall / F1);
* **primary-initiator accuracy**, only where the scenario declares exactly one
  initiator; elsewhere `None` with a reason, because there is no unambiguous right
  answer to be accurate about;
* whether the **single-vs-shared** classification was right (S05 must come out
  `shared_contribution`);
* the count of **insufficient-evidence** cases -- a first-class result: a system
  that abstains on an undecidable action is behaving correctly.

An action linked to the outcome by a `PREVENTS` edge is **not** an initiator
(`DEFAULT_PREVENTIVE_EDGE_TYPES`): in S01, A's late brake acted against the crash
and merely arrived too late. Counting it as a cause would reward a system for
naming the victim.

**There is deliberately no aggregate "fault score".** A single number would invite
exactly the reading this project rejects. See `docs/CAUSAL_MODEL.md` §6.

### 3.8 The epistemic check

`evaluate_local_unknowns` takes each name in the scenario's
`expected_local_unknowns` and asserts it is **absent** from the local and fused
output and **present** in the oracle output. Scenario specifications may declare
privileged events such as `signal_violation`; a system that "recovered" one
locally has hallucinated, and this check is what makes that a measurable failure
rather than an anecdote.

### 3.9 Model-checking metrics

The verdict counts per property and per participant from
`checking/model_check_results.json`, with all three keys (`PASS` / `FAIL` /
`UNKNOWN`) always emitted -- a consumer must never have to guess whether a missing
key means zero or means the checker did not run. `UNKNOWN` rates are a *reported
result*, not a defect rate.

---

## 4. Evaluation methodology

1. **The oracle is read last, and never by inference.** `cdf.evaluation` is the
   only layer that opens local, fused and oracle artifacts in one process, and it
   writes exclusively under `evaluation/` (and `artifacts/summary/` for a
   campaign).
2. **One contract per campaign.** `event_match_tolerance(cfg)` and
   `graph_match_settings(cfg)` return the settings as a *tuple*, read once and
   threaded through every comparison, so no call site can read one setting and
   forget the other and make two "identical" comparisons incomparable.
3. **Absent blocks are `None` with a reason**, never zero-filled. A block with no
   rows produces **no rows** in the CSV rather than a row of zeros: an empty table
   says "not measured", a table full of zeros says "measured, and it failed".
4. **Stable columns.** Every table declares its columns explicitly in
   `cdf.evaluation.tables`, so results directories stay diffable and concatenable
   across scenarios.
5. **Ground truth is measured, not assumed.** `build_oracle_events` shares **no
   code** with the local extractor -- scoring a reconstruction against a reference
   produced by the same code would measure nothing but numerical noise -- and it
   reads the scripted action schedule from the *trace*, not from the spec, so a
   counterfactual replay is scored against what the controller actually executed.

Per-run artifacts: `evaluation/metrics.json`, `event_matches.csv`,
`edge_matches.csv`, `attribution_metrics.json`.

---

## 5. Radar calibration procedure

Every threshold in `radar_processing` was tuned against **measured** CARLA 0.9.15
output on the reference machine, not copied from any reference implementation.
These are the measurements that drove it.

### 5.1 Measured conventions of the tested build

| Fact | Consequence in the code |
|---|---|
| **Range-rate is negative when closing.** | The sign convention is documented on `RadarDetection.velocity`, `TrackSample.range_rate` and `TrackIndicators.range_rate`, and `time_to_collision_1d` returns `None` unless `range_rate < -1e-3`. The extractor's closing signal is `-range_rate`. |
| **Azimuth is positive to the right** of sensor boresight. | `polar_to_body` maps `(depth, azimuth, altitude)` with `+y` to the right; `RadarSpec.mount_yaw_deg` rotates the sensor frame into the body frame. |
| **A raw frame carries ~145 detections, most of them road surface.** | Plausibility filtering is mandatory, not cosmetic: `radar_processing.filter.min_altitude_rad = -0.05` / `max_altitude_rad = 0.25` is the gate that removes the sub-sensor-plane road returns. |
| **The first frame after spawn can contain a ~100 m/s artifact**, physically impossible for a road vehicle. | `radar_processing.filter.max_abs_velocity_mps = 60.0` rejects it; `ScenarioWorld.warmup()` (20 ticks) and `ParticipantAgent.drain_radar_queues()` additionally discard the warm-up frames so the artifact is never attributed to the first recorded tick. |

Remaining filter gates: `min_range_m = 1.5`, `max_range_m = 90.0`,
`max_abs_azimuth_rad = 1.10` (slightly inside the nominal 120° FOV).

### 5.2 World-fixed clutter rejection

A stationary point observed from a sensor travelling forward at `own_speed`
produces a radial velocity of **exactly** `-own_speed * cos(azimuth)` (negative
because the range shrinks). The residual against that prediction,

```
stationarity_residual = | range_rate - ( -own_speed * cos(azimuth) ) |
```

is therefore near zero for road surface, kerbs, walls, poles and parked objects,
and close to the *relative* speed for anything actually moving. This is the classic
automotive-radar stationary-target discriminator, and it is **legitimate local
evidence**: it needs only the observer's own speed plus the bearing and range-rate
the sensor itself reported. Nothing about the observed object is required.

Three implementation details matter:

* the test pairs the measured range rate with **the bearing it was measured
  along** -- the sensor-frame azimuth rotated into the body frame by the mounting
  yaw. Using the body-frame centroid bearing instead introduces a parallax error
  of the order of the mounting offset (~2 m), which at short range is large enough
  to make roadside clutter look like a moving object;
* a cluster's verdict uses the **median** member residual, so a handful of returns
  smeared by a neighbouring moving object cannot drag a wall's verdict;
* the test gates **track birth only**
  (`radar_processing.stationary.reject_new_tracks = true`). An already-established
  track that later stops -- a vehicle braking to a halt, which is precisely the
  situation this project studies -- still associates normally and is never lost.

Tolerance: `radar_processing.stationary.tolerance_mps = 1.5`.

**Measured effect.** On S01 this test reduced participant A from **45 spurious
tracks to 1 correct one**, at **1.32 m mean position error**.

*(For reference, the committed `S01 / seed 0 / crash` artifact -- produced with
this calibration -- shows that single track `A::T001` associated to B with a
trajectory **RMSE of 1.356 m over 5.90 s** across 119 comparison samples. RMSE over
the association window and the calibration's mean position error are different
statistics; both are quoted as measured.)*

### 5.3 Clustering and tracking parameters

Tuned against the same measured frames:

| Stage | Key | Value | Rationale |
|---|---|---|---|
| Cluster | `cluster.eps_m` | 2.2 | neighbourhood radius in body-frame metres |
| | `cluster.min_points` | 3 | DBSCAN `minPts` (the point itself counts) |
| | `cluster.velocity_weight` | 0.6 | seconds converting a range-rate difference into a pseudo-metre, so two objects at the same place moving differently do not merge |
| | `cluster.max_clusters` | 24 | a saturated frame is exactly where far-field returns matter least, so the cap keeps the closest |
| Track | `tracking.gate_m` | 4.5 | association gate on the **global-frame** prediction -- gating in the body frame would let own yaw rate dominate the frame-to-frame displacement of a stationary object and blow the gate |
| | `tracking.max_misses` | 6 | coast through a dropout rather than shredding a track on one missed frame |
| | `tracking.min_hits_to_confirm` | 3 | with `confidence.min_confirm` 0.35; confirmation **latches**, because flickering confirmation would fragment the event stream built on top of it |
| | `tracking.position_alpha` / `velocity_alpha` | 0.55 / 0.35 | alpha-beta smoothing -- the right complexity for radar clusters at 20 Hz: no covariance to mis-initialise, graceful under the dropouts the degraded profiles inject |
| | `tracking.max_tracks` | 16 | capacity bound; least-confident evicted first, ties by creation order so an established track is never evicted by a fresh one of equal confidence |
| | `confidence.hit_gain` / `miss_decay` | 0.16 / 0.22 | decay faster than growth, so a fading track is dropped rather than lingering |

Association is an **optimal** gated assignment, not nearest-neighbour-per-track:
the latter can assign two tracks to one cluster and swap identities whenever two
objects pass close together, and a swapped identity silently corrupts every causal
claim built on the track.

### 5.4 Recorder sizing, measured

Raw CARLA radar produces roughly 145 detections per frame per sensor; at 20 Hz
over a 45 s run that is ~130k detections per vehicle. The recorder must run inside
the simulation loop without unbounded growth, so each stream's ring buffer is
sized once at `pre_event_s * sample_rate_hz * records_per_step` and the multiplicity
is read from **the same configuration keys the producers use** -- with 16 tracks
per step, sizing the track buffer in plain samples would silently shorten its
history to 1.25 s instead of 20 s, and the track stream is precisely the
interaction evidence the extractor depends on.

Observed on the committed S01 run: `stream_capacity_samples` = 400 for telemetry,
controls and radar, **6400** for tracks; `radar_points_discarded = 0` (the 400
points-per-frame cap never bit); 48 samples discarded for falling outside the
frozen window; nothing discarded for capacity.

Bounding the evidence is **part of the experiment**, not an optimisation: the
central claim is that a useful causal reconstruction can be built from what a
vehicle could plausibly have retained, not from an omniscient recording.

---

## 6. Reproducibility obligations

A result counts as reproducible in this project when all of the following hold,
and all of them are checkable from the artifacts alone:

1. `manifest.json` carries the run id, the seed, the **full merged configuration**
   and its hash, the environment block and the git commit;
2. `scenario_validation.json` shows `passed: true` (Gate 2);
3. `evidence_manifest.json` carries a SHA-256 for every file in the run
   directory (`write_evidence_manifest`), and
   `python scripts/verify_evidence.py --artifacts artifacts` re-hashes them and
   reports any file that is missing or changed. The manifest records the stage
   that wrote it: a run writes one at the end of recording, and
   `scripts/reprocess_runs.py --stages manifest` rewrites it to cover the
   artifacts that analysis, fusion, the oracle, checking, evaluation and the
   viewer bundle add afterwards. A file on disk that the manifest does not list
   is reported as *unlisted*, not as a failure, because that is what a stale
   manifest looks like -- only a missing or altered file fails verification;
4. re-running the same seed **on a freshly started simulator** produces
   byte-comparable artifacts -- `write_json` sorts keys and writes atomically,
   `write_jsonl_gz` pins `mtime = 0`, event ids are SHA-256 digests of
   scope/owner/type/rounded-time/subject, and every sort in the pipeline carries
   explicit tie-breakers. Re-running against a server that has already executed
   other runs does **not** qualify: see "The simulator must be restarted between
   runs" above;
5. the configuration hash is stamped into the association report, the fusion
   diagnostics, the checking report and the counterfactual manifest as well as
   the run manifest, so a mismatch between what produced a run and what
   evaluated it is visible rather than silent.

### What the recorded campaign actually is

The 39 runs under `artifacts/` were **not** recorded in one pass under one
commit. They were recorded over a working day, across eleven commits, as the
scenarios were developed and defects were fixed; `manifest.json` records the
commit for each one. That is only legitimate if nothing which governs a
recording or its evaluation changed between them, and that is checkable, because
every run stores its own fully merged configuration rather than a reference to
one.

It was checked. Across all 39 runs and against the configuration in force at
HEAD, the *only* keys that differ anywhere are

* `counterfactual.resume` (all runs -- the key did not exist yet), and
* `counterfactual.restart_server_per_replay` (the two earliest S01 crash runs).

Both govern how a counterfactual replay is *executed*. Neither can reach a
recording, a local reconstruction, a fusion, a model check or a metric. Every
simulation, radar, event, graph, fusion, checking and evaluation parameter, and
every scenario specification, is identical across the whole campaign and
identical to HEAD.

`tests/integration/test_recorded_campaign_config.py` asserts exactly this, so
the claim fails loudly if a future edit changes a parameter that the recorded
campaign depended on. Evaluation is re-derived offline over every run in one
pass (`python scripts/reprocess_runs.py --stages evaluate figures viewer`), so
all 39 runs are scored by one build of the metrics code rather than by whatever
was current when each was recorded.

The honest summary is that the campaign is reproducible run-by-run from its
recorded parameters, and internally comparable, but it is not a single-commit
campaign. Re-recording all 39 runs at HEAD would make it one; it was not done,
and the artifacts say so.
