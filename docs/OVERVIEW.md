# Overview

## The problem

Several vehicles are involved in a collision. Each carried its own recorder,
which kept its own log: telemetry, control inputs, radar returns, local tracks,
a local collision trigger, its own clock. No vehicle saw the whole encounter. No
two agree on what time it was. Afterwards, the logs are pooled.

**What happened, and whose behaviour led to it?**

This is not an object-detection problem and it is not a trajectory-prediction
problem. It is a reconstruction problem with three properties that make it hard:

1. **Partial observation.** A forward radar cannot see the car that struck from
   behind. A vehicle occluded at the moment of impact recorded the collision but
   not who caused it. Any account built from one log is missing the part the
   other logs hold.
2. **No shared clock.** The recorders were never synchronised. Placing three
   descriptions on one timeline is itself an inference, made from the evidence
   the participants exchanged, and it has an error that propagates into every
   temporal claim downstream.
3. **The cause is often a chain, or a combination.** In a three-car pile-up, no
   single action need be individually decisive. "Who caused it" may have no
   single-vehicle answer, and a method that always produces one is wrong.

## What this project does

```
  vehicle A                vehicle B                vehicle C
  ┌──────────┐             ┌──────────┐             ┌──────────┐
  │ telemetry│             │ telemetry│             │ telemetry│     each vehicle
  │ controls │             │ controls │             │ controls │     sees only its
  │ radar    │             │ radar    │             │ radar    │     own instruments
  │ own clock│             │ own clock│             │ own clock│     and its own clock
  └────┬─────┘             └────┬─────┘             └────┬─────┘
       │ local events            │                        │
       │ local causal graph      │                        │
       └───────────┬─────────────┴────────────┬───────────┘
                   │      exchanged logs      │
                   ▼                          ▼
        ┌──────────────────────────────────────────────┐
        │  FUSION                                      │
        │   1. estimate a common timeline              │   no simulator clock
        │   2. resolve which track is which vehicle    │   no actor ids
        │   3. merge the local graphs                  │   no map, no lane ids
        │   4. infer causal edges ACROSS vehicles      │   ← the step that needs
        │   5. reconstruct chains into the outcome     │     all of the above
        └───────────────────────┬──────────────────────┘
                                ▼
        ┌──────────────────────────────────────────────┐
        │  ATTRIBUTION                                 │
        │   hypothesis from the graph alone            │
        │   then: replay the encounter without each    │
        │   candidate cause, and without SETS of them  │
        └───────────────────────┬──────────────────────┘
                                ▼
                    ┌───────────────────────┐
                    │ causal initiator?     │      scored against a privileged
                    │ shared contribution?  │  ◄── oracle that the reconstruction
                    │ joint contribution?   │      never sees
                    │ insufficient evidence?│
                    └───────────────────────┘
```

Every stage above the dashed line runs on vehicle-local evidence only. The
oracle exists solely to score it, and a test suite fails the build if any
inference module can so much as import the code that writes it.

## The five claims, and how each is checked

| Claim | Checked by |
|---|---|
| Independent recorders can be placed on one timeline from shared observations alone | offset and drift error against the true clock profiles |
| Merged logs reconstruct more of the incident than any single vehicle's | three-arm ablation over identical recordings |
| Causal reasoning *after* fusion recovers relations no vehicle could claim | the same ablation, changing one configuration key |
| The reconstruction names the right contributors | contributor sets against the scenario's designed causal template |
| It stays silent when there is nothing to attribute | false-attribution count on the negative controls |

Results for all five are in [RESULTS.md](RESULTS.md), generated from the
artifacts rather than transcribed.

## What it deliberately does not do

It does not determine **legal fault**. Fault depends on right of way, traffic
law, jurisdiction, duty of care, and what a driver could reasonably have
foreseen — none of which is in a recorder's log and none of which is inferred
here.

The vocabulary is: *causal initiator*, *causal contributor*, *shared causal
contribution*, *joint causal contribution*, *causal chain*, *insufficient
evidence*. A contribution score states what changed when the simulator re-ran
the encounter under a controlled modification. It is not a percentage of blame,
and a test walks every artifact to make sure the words *guilty*, *fault*,
*liable* and *responsible* never appear as a conclusion.

## Where to go next

| Question | Document |
|---|---|
| What can each layer legally read? | [DATA_BOUNDARY.md](DATA_BOUNDARY.md) |
| How is the code organised? | [ARCHITECTURE.md](ARCHITECTURE.md) |
| What are the nine scenarios? | [SCENARIOS.md](SCENARIOS.md) |
| How is the common timeline estimated? | [CLOCK_SYNCHRONIZATION.md](CLOCK_SYNCHRONIZATION.md) |
| How are the logs merged? | [GRAPH_FUSION.md](GRAPH_FUSION.md) |
| What is a causal edge, and where does it come from? | [CAUSAL_MODEL.md](CAUSAL_MODEL.md) |
| How is contribution established? | [COUNTERFACTUALS.md](COUNTERFACTUALS.md) |
| What properties are checked on the traces? | [MODEL_CHECKING.md](MODEL_CHECKING.md) |
| How do I look at a run? | [VIEWER.md](VIEWER.md) |
| How was the campaign run? | [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) |
| What did it find? | [RESULTS.md](RESULTS.md) |
| What does it get wrong? | [LIMITATIONS.md](LIMITATIONS.md) |
| How do I reproduce it? | [REPRODUCIBILITY.md](REPRODUCIBILITY.md) |
