# Final status

What was built, what was executed, what was measured, and what did not work.
No claim here is aspirational: every number is either printed by a command given
below or read from a file under `artifacts/`.

Read alongside [`docs/EXPERIMENTAL_FINDINGS.md`](docs/EXPERIMENTAL_FINDINGS.md)
(results), [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) (what the results do not
support) and [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md) (simulator behaviour
this code is shaped around).

---

## 1. State

| | |
|---|---|
| Repository | local only — `git remote -v` is empty, nothing was pushed |
| Branch | `main` |
| Python | 3.8.20 (conda env `carla`) |
| Simulator | CARLA 0.9.15, packaged Windows build, `Desktop/Carla9_15/WindowsNoEditor` |
| OS | Windows 11 Enterprise 10.0.26200 |

The master prompt's process constraints were followed: no GitHub repository was
created, no remote was added, nothing was pushed, the reference repository was
never modified, no MQTT broker or external service is used, no deep-learning
stack or ROS dependency was added, and no literature search was performed.

---

## 2. Commands actually executed

These are the commands that produced everything under `artifacts/`, in order.

```bash
# environment
python scripts/check_environment.py

# the 42-run campaign (recorded incrementally as scenarios were developed;
# see "What the recorded campaign actually is" in docs/EXPERIMENT_PROTOCOL.md)
python scripts/run_suite.py --all --seeds 0 1 2 --continue-on-error

# counterfactual replays
python scripts/run_counterfactual_campaign.py \
    --run artifacts/S01_rear_end/seed_000_crash \
    --run artifacts/S05_simultaneous_crossing/seed_000_crash \
    --run artifacts/S06_chain_collision/seed_000_a_front_pushed \
    --run artifacts/S06_chain_collision/seed_000_b_rear_first \
    --run artifacts/S07_partial_view/seed_000_occluded \
    --max-interventions 4 --attempts 4

# radar-degradation ablation
python scripts/run_ablation.py --scenario S01 --variant crash --seed 0 \
    --profiles radar_baseline radar_noisy radar_dropout radar_degraded

# re-derive every derived artifact under one build of the analysis code
python scripts/reprocess_runs.py --artifacts artifacts \
    --stages check evaluate figures viewer manifest
python scripts/generate_report.py --artifacts artifacts

# verification
python -m pytest -q -m "not carla"
python scripts/verify_evidence.py --artifacts artifacts
python scripts/extract_findings.py --section all
python scripts/generate_scenario_docs.py --check

# viewer
python scripts/serve_viewer.py --run artifacts/S07_partial_view/seed_000_occluded
```

---

## 3. Tests

`python -m pytest -q -m "not carla"` — **509 passed, 1 skipped**, 514 collected.

| group | count | what it covers |
|---|---|---|
| `tests/unit` | 447 | schemas, ring buffer, radar geometry and the stationary-target discriminator, tracking, event hysteresis, graph construction and invariants, fusion and association, model checking and counterexamples, metrics and campaign tables, counterfactual outcomes and attribution, simulator process management, the evidence manifest, the viewer bundle |
| `tests/integration` | 41 | the real pipeline end to end on synthetic runs (rear-end, cut-in, crossing, fusion improvement), plus assertions over the recorded artifacts themselves: the campaign is one experiment, the 183 persisted causal graphs are DAGs carrying the scope their location implies, and the CARLA smoke test |
| `tests/test_no_privileged_leakage.py` | 26 | the data boundary, from six independent directions |
| marked `carla` | 4 | live-server smoke test; skipped when nothing answers on `127.0.0.1:2000` |
| marked `slow` | 2 | the whole-campaign artifact scans (~95 s); in `make test`, out of `make test-fast` |

The one skipped test is an oracle-graph assertion whose synthetic fixture does
not build an oracle graph.

The boundary suite is the one that matters. It parses every module under
`cdf.local`, `cdf.fusion`, `cdf.graph` and `cdf.checking` and resolves their
imports (relative ones included), re-checks the same claim in a fresh
interpreter, forbids the privileged simulator queries in any form, asserts no
persisted dataclass can *hold* a privileged quantity, scans every key of every
local, fused and checking artifact of all 42 recorded runs and their replays —
and then points the same scanner at the `oracle/` subtree and requires it to
**fail**, so a scan that passes everywhere cannot be mistaken for evidence.

---

## 4. Scenarios executed

**42 recorded runs**: 14 scenario/variant combinations at three seeds each, each
on a freshly started simulator process.

| Scenario | Map | Variants | Seeds | Outcome produced |
|---|---|---|---|---|
| S01 rear-end | Town05 | `crash`, `avoided` | 0,1,2 | collision / no contact |
| S02 cut-in | Town05 | `crash`, `avoided` | 0,1,2 | collision / no contact |
| S03 crossing | Town05 | `crash` | 0,1,2 | collision |
| S04 crossing + braking | Town05 | `yield` | 0,1,2 | no event (negative control) |
| S05 simultaneous crossing | Town05 | `crash` | 0,1,2 | collision |
| S06 chain collision | Town05 | `a_front_pushed`, `b_rear_first` | 0,1,2 | two ordered collisions |
| S07 partial view | Town05 | `occluded`, `full_view` | 0,1,2 | collision |
| S08 multi-direction crossing | Town05 | `crash` | 0,1,2 | collision |
| S09 roundabout | **Town04** | `merge_conflict` | 0,1,2 | collision |
| S10 signalised limitation | Town05 | `red_light_violation` | 0,1,2 | collision |

Scenario validation — the run produced the encounter its specification declares —
passes on **42 of 42** (`artifacts/summary/scenario_validation.csv`). Never more
than three participant vehicles; no pedestrians, bicycles or motorcycles; no
camera anywhere.

Town03 is not used by any scenario: every attempt to load it killed the server on
this build, so S09 runs on Town04 (`docs/ENVIRONMENT.md`, finding 4).

---

## 5. Results

All figures below are printed by `python scripts/extract_findings.py --section all`
and read from `artifacts/`. `docs/EXPERIMENTAL_FINDINGS.md` gives the reasoning;
this is the summary.

**Artifacts produced.** 66 run directories (42 recorded runs, 20 counterfactual
replays, 4 ablation runs), 3 211 files, 431 MB, 480 figures, 42 counterexample
reports, 66 evidence manifests — all 66 verified by
`python scripts/verify_evidence.py --artifacts artifacts`.

### Fusion versus a single ego view (H1, H2)

Scored against the privileged oracle graph, over all 42 runs:

| | value |
|---|---|
| mean Δ node F1 (fused − best single local) | **+0.060**, improved in **32 of 42** runs |
| mean Δ edge F1 | **−0.050**, improved in **0 of 42** runs |
| largest node gains | S07 +0.123, S06 +0.114, S08 +0.081 — the three-vehicle scenarios |

**Partially supported, and the split is systematic.** Fusion recovers *events*
no single ego view holds — on the occluded S07 run it more than doubles node
recall (0.231 → 0.500) and recovers the initiating `HARD_DECELERATION` of a
vehicle the rear participant never tracked — and it bridges causal reachability:
76 reachability pairs that exist in no single participant's graph, with the fused
collision ancestry spanning A, B **and** C. It does **not** improve edge
agreement, because causal edges are built locally, before fusion, so a cause seen
by one participant and an effect seen by another are merged as nodes but never
linked by a new edge. Fixing that needs a post-fusion causal rule pass, which
this implementation does not do. Reported as a negative result rather than
omitted.

### Track association without simulator identities

203 tracks reported; 106 have a true counterpart and 97 have none (post-impact
phantoms). Over the 106: **precision 0.974, recall 0.717, F1 0.826**, mean
trajectory RMSE **1.524 m**. Two wrong names in 78 commitments; the layer
declines to name a quarter of the identifiable tracks rather than guess. No CARLA
actor id is used at any point.

### Finite-trace model checking

396 property evaluations over the 42 runs: **72 PASS, 171 FAIL, 153 UNKNOWN**
(38.6%). The FAIL count is expected — these scenarios are built so at least one
vehicle does not respond adequately. The UNKNOWN count is the result that
matters: each carries an explicit reason, and every one of the 171 FAILs carries
a counterexample trace with its violating intervals.

### Counterfactual attribution

20 replays across 5 runs, each on a freshly started engine, each differing from
the factual run in exactly one scripted action.

| run | predicted | oracle reference | P | R | F1 |
|---|---|---|---|---|---|
| S01 `crash` | `single` — `B_emergency_brake` | `single` — same | 1.00 | 1.00 | **1.00** |
| S05 `crash` | `single` — `A_no_yield` | `shared` — A, B | 1.00 | 0.50 | 0.67 |
| S06b `b_rear_first` | `single` — `C_emergency_brake` | `shared` — B, C | 1.00 | 0.50 | 0.67 |
| S06a `a_front_pushed` | `insufficient_evidence` | `single` — `C_emergency_brake` | 0.00 | 0.00 | 0.00 |
| S07 `occluded` | `insufficient_evidence` | `shared` — B, C | 0.00 | 0.00 | 0.00 |

**No false positive in 20 replays.** Every failure is a false negative — an
action the scenario declares causal that controlled replay could not demonstrate.
The sharpest single result is S06 (H4): removing the leading vehicle's brake
prevents *every* impact in `b_rear_first` (16.53 m separation) and leaves the
first impact of `a_front_pushed` exactly where it was, from near-identical
layouts and near-identical end states.

### Robustness

The same S01 encounter through four radar profiles: every profile still produces
the collision, passes validation, and names the other vehicle correctly.
Frame dropout is what hurts (node F1 0.286 against 0.375 at baseline, two
associations left `UNRESOLVED`); point noise is tolerated. The heaviest
degradation scores the *highest* node F1 (0.409) because it suppresses the
post-impact phantom tracks — which is a warning that oracle-referenced node F1 is
not a monotone measure of sensing quality, and is reported as such.

### The data boundary

Verified mechanically, not asserted: no module under `cdf.local`, `cdf.fusion`,
`cdf.graph` or `cdf.checking` can reach `cdf.oracle`, `cdf.simulation` or
`carla`; no persisted local record type can *hold* a privileged quantity; and
every key of every local, fused and checking artifact of all 66 run directories
is clean. The same scanner pointed at `oracle/` **fails**, which is what shows it
can see a leak. Demonstrated end to end on S07 (participant A tracks only B, 23.9
m from C, while B tracks C) and S10 (the oracle emits `ORACLE_SIGNAL_VIOLATION`;
the local and fused artifacts contain no signal claim at all).

---

## 6. What did not work

Recorded because they cost real time and shape the code, not as excuses. The
simulator findings are detailed in `docs/ENVIRONMENT.md`.

### Unresolved

**The CARLA client aborts the interpreter mid-suite.** On the third simulator
process of a run, `world.apply_settings()` triggers `Fatal Python error:
Aborted` inside the native client — no Python traceback, no Windows error report,
shell exit status 127. Reproducible. The obvious hypothesis (background streaming
clients of killed servers accumulating in the process) was acted on —
`SimulatorSession.release_client()` — and **did not fix it**; the cause is not
established. The counterfactual campaign gets through it by structure, not
repair: `counterfactual.resume` reuses replays already on disk and the driver
retries, so successive attempts need fewer restarts. The five suites needed 4, 3,
4, 4 and 4 attempts; the ablation needed 3. This is a workaround and is recorded
as one in `docs/LIMITATIONS.md` §14.

### Resolved, but they invalidated work

**`CarlaUE4.exe` is a launcher, not the server.** It spawns
`CarlaUE4-Win64-Shipping.exe` and exits, so terminating the launched process left
the engine alive holding the RPC port — and every later "fresh" server silently
reconnected to the *first* one. Restarts that existed to give each replay an
independent simulator were giving it shared, drifting state while appearing to
work. **The first counterfactual campaign was run under this defect and was
discarded and re-run.** Comparing the two: every collision outcome, time, pair
order, attribution class and score is identical, and only the minimum separations
of replays that *avoided* collision moved (by up to 0.66 m). The defect changed
no conclusion here — but §2 of the findings records a case where the same drift
flipped an outcome between near-miss and collision, and which case this was could
not be known without re-running.

**Three features were documented and did not exist.** Found by auditing the
repository against its own documentation:

* `evidence_manifest.json` was never written — `write_evidence_manifest` was
  imported by the runner and never called, so the SHA-256 integrity claim in the
  README, in reproducibility obligation 3 and in the checklist was untrue. Now
  written, and `scripts/verify_evidence.py` checks it.
* The model-check results named a counterexample for every `FAIL`, and nothing
  wrote the file: 171 references resolving to nothing, and a viewer showing
  "counterexample report missing" for all of them. `build_counterexample_report`
  existed and was tested; no pipeline called it.
* `make test-carla` collected **zero** tests and reported success — the `carla`
  marker was registered and no test carried it.

Writing that smoke test immediately paid for itself: it failed on its first run
against a live server, because **`ScenarioWorld.cleanup()` did not actually
destroy its actors**. In synchronous mode a `destroy()` is a queued command
applied on the next tick, and cleanup restored the world settings — leaving
synchronous mode — without ever taking that tick, so every vehicle and sensor
survived the run that created them. It did not affect any recorded result,
because the protocol restarts the simulator for every run, and it would silently
corrupt the scene for anyone who reuses a server. Cleanup now ticks while still
synchronous and reports any actor that survives.

**Campaign aggregates included experiments that were not part of the campaign.**
`aggregate_runs` walked the artifacts tree with `rglob`, so counterfactual
replays and ablation runs were averaged into the campaign tables — 46 "runs" in a
42-run campaign, with the 14 replays listed as having failed to evaluate. `cdf
report` separately read a metrics key the evaluation layer no longer wrote, so
the fused-versus-local table never appeared at all.

**Two findings were wrong and are corrected.** §5.5 explained the 28 unresolved
associations as tracks corresponding to no participant; the metric counts only
tracks that *do* have a true counterpart, so they are genuine misses and the
honest reading is precision 0.974 *and* recall 0.717. §8's verdict totals were
stale.

### Worked around, in the simulator

Town03 could not be loaded at all (S09 runs on Town04 instead); the map cannot be
selected from the command line; reloading the currently loaded map kills the
server; a second map switch in one server process is unreliable; spawning at a
settled actor's transform fails, so all spawns derive from lane waypoints.

### Limits of the results themselves

Fusion does not improve oracle-referenced *edge* agreement in any of the 42 runs
(§5.3). But-for analysis cannot attribute an **omission** — S05's drivers fail to
yield, and the intervention API can weaken an action that exists but cannot
remove an absence. Scripted controllers do not react, so removing an upstream
cause does not propagate to a downstream response, which is why S06a and S07
return `insufficient_evidence`. All three are properties of the scenario design,
not of the replay machinery, and are stated in `docs/LIMITATIONS.md`.

---

## 7. What is not claimed

* No statement about **legal liability or fault**. The counterfactual layer
  reports *causal contribution under controlled replay semantics*, and every
  contribution artifact carries that disclaimer in its own payload.
* No **formal verification of CARLA**, of the scenarios, or of any vehicle
  controller. What runs is finite-trace monitoring of four properties over
  recorded traces, with `UNKNOWN` as a first-class verdict.
* No **statistical claim**. Three seeds per scenario with narrow perturbation is
  enough to show determinism and to catch gross sensitivity; it is not an
  estimate with a confidence interval.
* The confidence numbers produced by fusion are **evidence accumulation**
  (noisy-OR), not calibrated probabilities.
