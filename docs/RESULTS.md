# Results

This page is the delivery snapshot for the final V2 factual campaign.

The active benchmark contains **16 scenarios, 34 variants and 102 CARLA runs**
(seeds 0, 1 and 2). S01-S09 remain hash-frozen; S10-S16 use the corrected
scenario definitions. Historical V1 material remains under
[`legacy/`](../legacy/README.md) and is not mixed with these figures.

The numerical snapshot below is read from the committed
[`results/final_results.json`](../results/final_results.json). One caveat is
important: commit `2b6df8a6` fixed a radar clock fit that could return the
search boundary as a high-confidence estimate. The final clock aggregate has
not yet been propagated through every offline artifact, so the pre-fix clock
MAE in the generated result file is not repeated here.

## Reconstruction

| Measure | Current value |
|---|---:|
| Scenario/variant combinations | 34 |
| Factual runs | 102 |
| Collision variants | 23 |
| Negative controls | 11 |
| Incidents reconstructed | 27 / 34 variants |
| Collision-pair recall | **0.9928** |
| Mean collision-time error | **0.0116 s** |
| Mean collision-location error | **0.0474 m** |
| Spurious collisions | **13** |
| Cross-view trajectory RMSE | **1.3148 m** |

For multi-impact incidents there are 20 applicable runs. The system claims an
order on 19 of them: **17 are correct, 2 wrong**, and 1 further run is reported
as `not_established`. Accuracy where an order is claimed is therefore
**89.5%**.

## S16: secondary collision

S16 is retained and consists of `consequential`, `independent` and
`avoided`, each run on three seeds.

| Variant | Runs | Collision-pair recall | Spurious collisions | Multi-impact order | Attribution |
|---|---:|---:|---:|---|---|
| `consequential` | 3 | **1.00** | **0** | **3/3 correct** | insufficient evidence |
| `independent` | 3 | **1.00** | **0** | **3/3 correct** | partial, F1 **0.444** |
| `avoided` | 3 | **1.00** | **0** | single-impact control | insufficient evidence |

The useful result is therefore clear: the reconstruction distinguishes the
physical sequence in both S16 multi-impact variants on all six final recordings.
The responsibility layer is weaker and does not reliably assign the intended
contributor in `consequential`.

## Physical and normative contribution

| Comparison | Precision | Recall | F1 |
|---|---:|---:|---:|
| Physical contributors | 0.689 | 0.708 | **0.699** |
| Normative contributors | 0.606 | 0.606 | **0.606** |

The exact physical contributor set is recovered on 38 of 102 runs (37.3%).
These figures describe causal/normative contribution, not legal fault.

## Formal/model checking

Across 102 runs and 972 property evaluations:

- **190 PASS**
- **316 FAIL**
- **466 UNKNOWN**

On the comparable reconstruction-vs-observable-ground-truth subset, agreement
is **72.6%** (114/157), with 10 false violations and 33 missed violations.
`UNKNOWN` is kept as a first-class outcome rather than folded into PASS.

## Perception

The STOP-sign detector has 51 TP, 66 FP and 0 FN in the current aggregate:
precision **43.6%**, recall **100%**. Stop-line and lane-marking precision are
not reported because there is no independent verified reference for them in
this campaign.

## Counterfactual status

The counterfactual implementation remains in the repository, but the fresh
campaign-wide replay sweep after the final S10-S16 restaging was interrupted.
Old counterfactual aggregates from the invalid geometries are therefore not
presented as final evidence. The final delivery claims the factual
reconstruction, formal checking and responsibility results above.

## Clock status

The final clock code rejects fits pinned to the configured search boundary and
returns `UNRESOLVED` instead. This specifically fixed affected S16/avoided
recorders. Because the complete 102-run offline reprocessing after that patch
has not yet been committed, this page deliberately does not quote a final
post-fix aggregate clock MAE.

