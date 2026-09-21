# CausalDrive Forensics

Distributed reconstruction and causal analysis of road incidents from
independent vehicle logs in CARLA.

![Three vehicles record the same chain collision on three unsynchronised clocks, shown at one instant on the estimated common timeline](docs/assets/causaldrive_hero.png)

## What is it?

After a collision there is no single record of what happened. There are several
vehicles, each holding a short buffer of its own sensor data: telemetry,
controls, radar returns to anonymous tracks, a front camera, a lane sensor and a
contact trigger. No vehicle sees another vehicle's data, and each runs on its own
clock, offset from the others by a fraction of a second it does not know.

Afterwards those logs are brought together. The system estimates the offsets
between the clocks from evidence the vehicles themselves recorded, matches each
anonymous radar track to the participant it really was, and merges everything
into one timeline. From that timeline it reconstructs the incident, builds a
physical causal graph of what led to what, checks temporal properties over the
trace, and runs a separate responsibility layer that asks which obligations were
violated and whether a violation lies on a physical causal path. Counterfactual
replays then test whether changing an action would have prevented the outcome.

CARLA's privileged state, the true positions, the true clocks, the map and the
actor identities, is used only afterwards, to grade the answers. It is never
available to the reconstruction. The output is a causal account, not a finding of
legal fault, and no number here is a share of one.

## How it works

```
Vehicle A log ─┐
Vehicle B log ─┼→  time alignment  →  identity association  →  global log
Vehicle C log ─┘                                                    │
                                                                    ▼
                                                       physical causal DAG
                                                                    │
                                                                    ▼
                                                     temporal properties
                                                                    │
                                                                    ▼
                                                         responsibility
                                                                    │
                                                                    ▼
                                                   counterfactual replay
```

Details in [Architecture](docs/ARCHITECTURE.md).

## What each vehicle records

| Input | What it gives |
|---|---|
| telemetry | its own position, velocity, acceleration, yaw and yaw rate |
| controls | its own throttle, brake, steer, handbrake, gear |
| radar | range, bearing and range rate to anonymous local tracks |
| RGB camera | video around the event, for signs and road markings |
| lane sensor | that a road marking was crossed, and what sort |
| contact trigger | that an impact happened, when, and how hard, never who with |
| local clock | its own offset and jitter, shared with nobody |

What a vehicle may not see is stated and enforced in
[Data boundary](docs/DATA_BOUNDARY.md).

## Benchmark

**16 scenarios, 34 variants, 102 final CARLA runs, 3 seeds.**

| Scenarios | What they cover |
|---|---|
| S01 to S09 | the original reconstruction benchmark: rear-end, cut-in, crossing, chain collision, partial view, roundabout. Hash-frozen, so a better metric must come from the method |
| S10 to S12 | STOP signs and priority: one approach controlled, the mirror case, and an all-way stop |
| S13 | disputed lane change, where the deciding evidence is split across two vehicles |
| S14 to S16 | multi-impact and secondary collisions: the pushed vehicle, the pile-up with a bystander, and the second impact that may be a consequence or its own doing |

Full descriptions in [Scenarios](docs/SCENARIOS.md).

## Main results

The current factual campaign contains **102 runs over 34 scenario/variant
combinations**. The figures below are read from the committed final campaign
artifacts. The clock aligner has since been patched to reject radar fits pinned
to its search bound, and the full 102-run offline dependency chain has been
regenerated with that fix.

| Result | Measured |
|---|---|
| Collision pairs | recall **1.000** |
| Collision timing | **0.0101 s** mean error; **0.0343 m** mean location error |
| Spurious collisions | **11** across 102 runs |
| Multi-impact ordering | **18/20** claimed orders correct (**90.0%**); 1 declined, 2 wrong |
| Clock alignment | scenario-aggregated offset MAE **0.007141 s**; 7 of 243 recorders unresolved |
| Physical contributors | precision 0.694, recall 0.708, **F1 0.701** |
| Normative contributors | precision/recall/**F1 0.606** on runs with a normative reference |
| Model checking | **190 PASS / 316 FAIL / 466 UNKNOWN** |
| Negative controls | **0 false attributions in 11 controls** |

### S16: secondary collision

S16 is retained in the final benchmark. Across its three seeds per variant,
collision-pair recall is **1.00** with **0 spurious collisions**. For the two
multi-impact variants, the reconstructed impact order is correct on **all 6/6
runs**: 3/3 for `consequential` and 3/3 for `independent`. Attribution is
harder: `independent` is partial (F1 0.444 in the current aggregate), while
`consequential` remains insufficient-evidence at the responsibility layer.

The fresh counterfactual sweep after the final scenario restaging was not
completed, so no campaign-wide fresh counterfactual aggregate is claimed here.

Full tables in [Results](docs/RESULTS.md).

## Explore

| | |
|---|---|
| [Overview](docs/OVERVIEW.md) | the longer version of this page: what makes the problem hard, and what is claimed |
| [Architecture](docs/ARCHITECTURE.md) | how the pieces fit together |
| [Events](docs/EVENTS.md) | the event vocabulary, and what may be compared |
| [Time synchronization](docs/CLOCKS.md) | contact first, radar second, unresolved last |
| [Scenarios](docs/SCENARIOS.md) | what each scenario is for |
| [Formal methods](docs/FORMAL_METHODS.md) | temporal properties, and why UNKNOWN is a verdict |
| [Responsibility](docs/RESPONSIBILITY.md) | obligations, violations, contribution |
| [Counterfactuals](docs/COUNTERFACTUALS.md) | replay, but-for causation, prevention |
| [Results](docs/RESULTS.md) | the final V2 campaign in full |
| [Limitations](docs/LIMITATIONS.md) | what this does not establish |
| [Viewer](docs/VIEWER.md) | the four sections: reconstruction, graph, responsibility, video |
| [Reproducibility](docs/REPRODUCIBILITY.md) | running it again and getting the same answer |
| [Data boundary](docs/DATA_BOUNDARY.md) | what inference may not see, and how that is enforced |
| [What changed from V1](docs/V2_REFACTOR_AUDIT.md) | the refactor, and what was deliberately not changed |
| [References](docs/REFERENCES.md) | the reading behind the design choices |

Earlier V1 material is kept under [`legacy/`](legacy/README.md). V1 and V2
recordings are never mixed: V2 changed the sensors and the timing semantics, so a
figure averaged over both would describe neither.

## Quick start

Start CARLA yourself. The project connects to a running simulator and does not
launch one:

```bash
python -m cdf.cli env
```

Run one scenario end to end, recording and then analysing it:

```bash
python scripts/run_scenario.py --scenario S10 --variant rolls_through --seed 0 --artifacts artifacts_v2
```

Open the viewer on that run:

```bash
python scripts/serve_viewer.py --run artifacts_v2/S10_single_stop_a/seed_000_rolls_through
```

The full campaign and every other command are in
[Reproducibility](docs/REPRODUCIBILITY.md).

## Licence

See [LICENSE](LICENSE).
