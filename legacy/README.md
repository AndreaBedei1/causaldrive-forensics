# legacy

What V1 produced and V2 no longer speaks for.

Nothing here is on the active execution path. It is kept because deleting a
result is different from superseding one: these were real measurements of a real
campaign, and the argument that V2 is better rests on being able to look at what
it replaced.

| | |
|---|---|
| `FINAL_STATUS_v1.md` | the V1 status report, written before the observable ground truth existed. Its headline structural numbers were computed against the scenario template and are not comparable with anything under `results/` |
| `results_v1/` | the V1 result tables, from `artifacts_independent_clocks/` |

## Why these are not simply deleted

The V1 numbers are the reason the V2 refactor happened. Scored against the
scenario template, the same recordings gave best-local 0.065 and fusion 0.051 on
edge F1 -- with fusion appearing to *hurt*. Scored against a ground truth that
speaks the reconstruction's vocabulary, the same recordings give 0.153 and 0.358.
The method did not change between those two figures; only what it was compared
against did.

Keeping the first set visible is what makes that argument checkable.

## What is not here

The radar-based clock estimator, the template-based graph scoring and the
canonical-vocabulary machinery are all still under `src/`. They are no longer the
primary path but they are still *run* -- the clock and method ablations compare
against them -- so archiving them would mean either breaking those ablations or
importing from `legacy/` in the active path. They are labelled where they live
instead. See the deviations section of `docs/V2_REFACTOR_AUDIT.md`.
