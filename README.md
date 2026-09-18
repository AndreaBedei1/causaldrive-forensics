# CausalDrive Forensics

Reconstructing a road incident from what the vehicles involved recorded, and
nothing else.

## 1. The problem

After a collision there is no single record of what happened. There are several
vehicles, each with a short buffer of its own sensor data, each on its own clock,
none of which observed the others directly. The question is how much of the
incident can be recovered from those separate accounts — and, just as importantly,
what cannot be.

This is a simulation study. CARLA provides the incidents and the exact state that
grades the answers; the exact state is never available to the reconstruction.

## 2. Inputs

Each vehicle keeps, for a short rolling window:

| Input | What it gives |
|---|---|
| telemetry | its own position, velocity, acceleration, yaw and yaw rate |
| controls | its own throttle, brake, steer, handbrake, gear |
| radar | range, bearing and range rate to anonymous local tracks |
| front camera | 20 s before the event and 5 s after, for signs and road markings |
| lane sensor | that a road marking was crossed, and what sort |
| contact trigger | that an impact happened, when, and how hard — never who with |
| its own clock | offset and jitter of its own, shared with nobody |

What a vehicle may **not** see: any other vehicle's telemetry, the map, lane or
road ids, waypoints, traffic-light state, CARLA actor identities, the scenario
definition, or the simulator clock. `docs/DATA_BOUNDARY.md` states the boundary
and the tests that enforce it.

## 3. Pipeline

```
each vehicle          local events  →  local_log.json  →  physical graph
                                            ↓
fusion                hybrid clock alignment: contact, then radar
                      anonymous track → participant identity
                                            ↓
                                      global_log.json
                                            ↓
                                physical causal DAG
                                            ↓
formal methods        temporal properties: PASS / FAIL / UNKNOWN
                                            ↓
responsibility        obligations, violations, contribution
                                            ↓
counterfactual        replay, to test but-for causation
                                            ↓
evaluation            against privileged ground truth
```

Five things about this are deliberate and are what the design turns on:

- **the log comes before the graph.** A DAG is what the project is for; a table of
  timestamped facts is what a reader can check;
- **clocks are anchored on shared contact first**, and on an offset-only radar
  fit only where contact cannot reach. One impact fixes
  one offset and says nothing about drift (`docs/CLOCKS.md`);
- **the physical graph and the responsibility graph are separate**, so the physics
  can be accepted and the norm disputed (`docs/RESPONSIBILITY.md`);
- **properties are three-valued.** Time nobody watched is UNKNOWN, never PASS
  (`docs/FORMAL_METHODS.md`);
- **the ground truth speaks the reconstruction's vocabulary**, or the comparison
  measures the vocabulary gap instead of the method (`docs/EVENTS.md`).

## 4. Scenarios

Sixteen scenarios, 35 variants. S01–S09 are the original set and are hash-frozen:
improving a metric must be a change to the method, never to the scenario.
S10–S16 are new, and each isolates something the earlier nine could not
(`docs/SCENARIOS.md`).

| | |
|---|---|
| S01–S09 | rear-end, cut-in, crossing, chain collision, partial view, roundabout |
| S10, S11 | single stop sign, with either approach controlled — mirrors of each other |
| S12 | all-way stop, including an arrival too close to call |
| S13 | disputed lane change, where the deciding evidence is split across vehicles |
| S14 | three-car rear-end chain, with the pushed vehicle |
| S15 | intersection pile-up, with a bystander that acts in no variant |
| S16 | secondary collision: initiating versus consequential |

## 5. Run one scenario

CARLA must already be running. Start it yourself — the campaign does not launch
it:

```bash
python scripts/run_scenario.py --scenario S10 --variant rolls_through --seed 0 --artifacts artifacts_v2
```

That records the run and then analyses, fuses, checks and builds the viewer
bundle. To redo any of those stages later without a simulator:

```bash
python scripts/reprocess_runs.py --artifacts artifacts_v2 --scenarios S10 --refactor
```

A three-car scenario is the same command with a different id:

```bash
python scripts/run_scenario.py --scenario S14 --variant c_pushes_b --seed 0 --artifacts artifacts_v2
```

Before the first run, check that the simulator is reachable and the versions
match:

```bash
python -m cdf.cli env
```

The full campaign — every scenario, every variant, every seed, one fresh
simulator process per run:

```bash
python scripts/run_campaign.py --artifacts artifacts_v2 --seeds 0 1 2 --attempts 3
```

## 6. Open the viewer

```bash
python scripts/serve_viewer.py --run artifacts_v2/S10_single_stop_a/seed_000_rolls_through
```

Four sections — Reconstruction, Graph, Responsibility, Video — and nothing else.
Each renders what the artifacts say; where something is absent it says so rather
than showing an empty panel (`docs/VIEWER.md`).

## 7. Results

Committed under `results/`, regenerated from artifacts. Nothing there is
hand-transcribed.

V1 and V2 recordings are never mixed: V2 changed the sensors and the timing
semantics, so a figure averaged over both would describe neither. The campaign
refuses an artifacts root holding runs of both generations.

## 8. Limitations

The ones that most constrain how the results should be read
(`docs/LIMITATIONS.md` has the rest):

- **a vehicle that neither collides nor presents usable radar geometry stays
  unresolved.** Contact places it where there is an impact and an offset-only
  radar fit places it where there is not; where neither works the recorder keeps
  its own clock and says so, rather than being placed on a guess. The negative
  controls fall back on an explicit marker from the experiment harness, which is
  declared, labelled and reported apart. It is never simulator time;
- **the sign detector is classical colour-and-shape**, deterministic and with no
  training data. It will miss signs at distance and in shadow. Its precision and
  recall are measured and reported rather than assumed;
- **a stop-line crossing is inferred from the marking leaving the frame**, so the
  detector is deliberately conservative: it misses crossings rather than
  inventing them;
- **in a chain the middle vehicle often registers one impact, not two**, so one
  anchor relates both neighbours. The alignment names the recorder whose offset
  rests on that anchor and states that no error bound is determinable: a recorder
  that never registered the second impact has no measurement of when it happened.
  On the recorded chain this cost 200 ms on one offset and the order of two
  impacts, which is reported rather than absorbed;
- **nothing here is a finding of legal fault**, and no number is produced that
  could be read as a share of one.

## Documentation

| | |
|---|---|
| `docs/ARCHITECTURE.md` | how the pieces fit together |
| `docs/EVENTS.md` | the event vocabulary, and what may be compared |
| `docs/CLOCKS.md` | hybrid alignment: contact, then radar, then unresolved |
| `docs/FORMAL_METHODS.md` | the temporal logic |
| `docs/RESPONSIBILITY.md` | obligations, violations, the priority benchmark |
| `docs/SCENARIOS.md` | what each scenario is for |
| `docs/VIEWER.md` | the four sections |
| `docs/REPRODUCIBILITY.md` | running it again and getting the same answer |
| `docs/DATA_BOUNDARY.md` | what inference may not see, and how that is enforced |
| `docs/COUNTERFACTUALS.md` | replay, but-for causation, prevention |
| `docs/LIMITATIONS.md` | what this does not establish |
| `docs/V2_REFACTOR_AUDIT.md` | what changed from V1, and what was deliberately not changed |

## Licence

See `LICENSE`.
