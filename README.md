# carla-distributed-causal-forensics

Several vehicles crash. Each carried its own recorder, which kept its own log
and its own clock. No vehicle saw the whole encounter and no two agree on what
time it was. Afterwards the logs are pooled.

**What happened, and whose behaviour led to it?**

This project answers that question from the logs alone, in a CARLA simulation
where the true answer is known but deliberately withheld from every stage that
does the reasoning.

```
  vehicle A            vehicle B            vehicle C
  ┌─────────┐          ┌─────────┐          ┌─────────┐
  │telemetry│          │telemetry│          │telemetry│    each sees only its own
  │ controls│          │ controls│          │ controls│    instruments, and stamps
  │  radar  │          │  radar  │          │  radar  │    them with its own clock
  │own clock│          │own clock│          │own clock│
  └────┬────┘          └────┬────┘          └────┬────┘
       │  local events, local causal graph       │
       └──────────────┬──────────┬───────────────┘
                      │ exchanged logs
                      ▼
       ┌──────────────────────────────────────┐
       │ FUSION                               │  no simulator clock
       │  · estimate one common timeline      │  no actor ids
       │  · resolve which track is which car  │  no map or lane ids
       │  · merge the local graphs            │  no scenario label
       │  · infer causal edges ACROSS vehicles│  no designed causal template
       │  · reconstruct the chains            │
       └──────────────────┬───────────────────┘
                          ▼
       ┌──────────────────────────────────────┐
       │ ATTRIBUTION                          │
       │  hypothesis from the graph, then     │
       │  replay the encounter without each   │
       │  candidate cause — and without SETS  │
       └──────────────────┬───────────────────┘
                          ▼
     causal initiator · shared contribution · joint
     contribution · insufficient evidence
                          │
                          ▼  scored against a privileged oracle
                             the reconstruction never sees
```

Nothing above the oracle line may read privileged state. That is enforced three
ways: no inference module can import the code that writes it; no privileged
field name appears in any local or fused artifact; and — the test that matters
most — **deleting the oracle, relabelling the scenario and stripping the designed
causal template out of the configuration produces byte-identical conclusions.**

## What it produces

For each run, an account you can interrogate rather than a score you have to
trust:

> A and B collided at t = 6.51 s on the common clock.
>
> Because: B braking contributed to B slowing → B slowing led to A closing
> rapidly on B → A closing rapidly on B contributed to A's time-to-collision
> with B becoming critical → that resulted in the impact between A and B.
>
> **Single causal initiator.** Removing B's emergency brake alone prevented the
> collision in replay, and no other single action did.

Every sentence there is a field of an artifact, assembled in reading order.
There is no language model anywhere in this project.

**A contribution score states what changed when the encounter was re-run under a
controlled modification. It is not legal fault and not a fault percentage.**

## Install

```bash
git clone <this repo> && cd carla-distributed-causal-forensics
python -m pip install -e .
python -m cdf.cli env        # checks the CARLA connection and version
```

Requires CARLA 0.9.15 and Python 3.8. Start the simulator first; see
[docs/ENVIRONMENT.md](docs/ENVIRONMENT.md) for the flags this project assumes.

## Quick start

```bash
# one scenario, end to end
python -m cdf.cli run --scenario S06 --variant a_front_pushed --seed 0

# what would have prevented it
python -m cdf.cli counterfactuals --run artifacts/S06_chain_collision/seed_000_a_front_pushed

# look at it -- builds the bundle, serves it, opens a browser
python -m cdf.cli viewer --run artifacts/S06_chain_collision/seed_000_a_front_pushed
```

The viewer is a static page with no framework and no network access, so it opens
from an offline copy of the evidence. It has one tab per question an
investigation asks: what happened, where, why, when, who, was it checked, on what
evidence, and how well the method did. See [docs/VIEWER.md](docs/VIEWER.md).

## The full campaign

```bash
python scripts/run_campaign.py --artifacts artifacts_independent_clocks --seeds 0 1 2
python scripts/run_counterfactuals.py --artifacts artifacts_independent_clocks --seeds 0
python scripts/reprocess_runs.py --artifacts artifacts_independent_clocks \
                                 --stages evaluate ablate viewer
```

Thirteen scenario/variant combinations across nine scenarios, three seeds, 39
runs. Results land in `artifacts_independent_clocks/summary/final_results.md`,
generated from the artifacts rather than transcribed.

## The nine scenarios

Frozen. `tests/test_scenario_freeze.py` pins the SHA-256 of each definition,
because a method that is improved by adjusting the scenario it is measured on
has not been improved.

| | Scenario | What it tests |
|---|---|---|
| S01 | rear-end | the simplest chain; `avoided` is a negative control |
| S02 | cut-in | a lateral manoeuvre as initiator; `avoided` is a control |
| S03 | crossing | two vehicles, no shared lane |
| S04 | crossing with braking | a **yield**: nobody collides, nobody may be blamed |
| S05 | simultaneous crossing | two contributors, neither obviously first |
| S06 | chain collision | three vehicles, two impacts, an order to recover |
| S07 | partial view | one vehicle occluded at the moment of impact |
| S08 | multi-direction crossing | three approach directions |
| S09 | roundabout merge | a merge conflict with curved geometry |

Details in [docs/SCENARIOS.md](docs/SCENARIOS.md).

## Results in brief

Full tables, generated from the artifacts, in [docs/RESULTS.md](docs/RESULTS.md).
The headline findings, including the ones that did not go the project's way:

- **Restraint holds.** Across the negative controls the system named nobody. A
  false attribution there would be worse than a missed one, so it is counted
  rather than averaged.
- **Reasoning after fusion recovers relations no vehicle could claim.** Canonical
  edge recall rises monotonically across best-local → merged → merged+reasoning.
- **Strict edge F1 does not improve, and on two scenarios the best single
  vehicle beats the merge.** This is reported rather than buried. The cause is
  measured, not guessed: most of the reference graph's edges leave a
  scripted-action node — a privileged event type no reconstruction can emit — so
  strict recall has a ceiling well below 1.0, and the merged account reaches
  that ceiling exactly on roughly half the campaign's runs. The exact counts are
  in the generated table, not here: a number transcribed into prose is a number
  that will eventually be wrong.
- **Attribution is partly right.** Exactly the designed contributors are named on
  some scenarios, a subset on others, and on one the wrong vehicle entirely.
  Per-scenario verdicts are in the results table.

## Tests

```bash
python -m pytest tests/ --ignore=tests/integration      # ~600 tests, no simulator
python -m pytest tests/integration                      # needs a running CARLA
```

## Documentation

| | |
|---|---|
| [OVERVIEW.md](docs/OVERVIEW.md) | the problem and the five claims |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | how the code is organised |
| [DATA_BOUNDARY.md](docs/DATA_BOUNDARY.md) | what each layer may read, and how it is enforced |
| [SCENARIOS.md](docs/SCENARIOS.md) | the nine encounters |
| [CLOCK_SYNCHRONIZATION.md](docs/CLOCK_SYNCHRONIZATION.md) | placing independent recorders on one timeline |
| [GRAPH_FUSION.md](docs/GRAPH_FUSION.md) | identity resolution and merging the graphs |
| [CAUSAL_MODEL.md](docs/CAUSAL_MODEL.md) | what a causal edge is and where it comes from |
| [COUNTERFACTUALS.md](docs/COUNTERFACTUALS.md) | replay, sets of actions, the five verdicts |
| [MODEL_CHECKING.md](docs/MODEL_CHECKING.md) | properties over finite traces |
| [VIEWER.md](docs/VIEWER.md) | the investigative interface |
| [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md) | how the campaign is run and scored |
| [RESULTS.md](docs/RESULTS.md) | what it found |
| [LIMITATIONS.md](docs/LIMITATIONS.md) | what it cannot do |
| [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) | reproducing all of it |

## Limitations

The short version: a simulator is not traffic; nine scenarios are not a
distribution; radar and localisation are modelled, not real; and causal
contribution under replay semantics is not legal fault. The long version is
[docs/LIMITATIONS.md](docs/LIMITATIONS.md), and it is worth reading before
quoting any number from here.

## Author

Andrea Bedei.

## License

See `LICENSE`.
