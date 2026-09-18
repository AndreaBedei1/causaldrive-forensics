# results

Generated from artifacts by `cdf.evaluation.final_results`. Nothing here is
hand-transcribed; §42 of the V2 brief requires that, and a number typed in by
hand is a number nobody can regenerate.

## Current state

**Empty, pending the V2 campaign.** V2 changed the sensor suite and the timing
semantics, so a V1 recording is not a V2 result and averaging the two would
produce a figure describing neither. The V1 tables have been moved to
`legacy/results_v1/` rather than overwritten, and the V2 tables appear here once
`artifacts_v2/` has been recorded.

Recording it needs a simulator, which the analysis stages do not:

```bash
python scripts/run_campaign.py --artifacts artifacts_v2 --seeds 0 1 2 --attempts 3
```

Then:

```bash
python -c "import sys; sys.path.insert(0,'src'); \
           from cdf.evaluation.final_results import write_final_results; \
           write_final_results('artifacts_v2')"
```

`run_campaign.py` refuses an artifacts root that already holds runs of the other
generation, so the two cannot be mixed by accident.

## What was measured before

The V1 campaign — 39 runs, 9 scenarios, under `artifacts_independent_clocks/` —
is summarised in `legacy/results_v1/`. Its headline structural figures were
computed against the **scenario template**, which asserts scripted actions no
reconstruction can emit, and are not comparable with anything generated here.

Reprocessing those same recordings against the observable ground truth gave:

| Account | node F1 | edge F1 |
|---|---|---|
| best single vehicle | 0.400 | 0.153 |
| simple fusion | 0.613 | 0.301 |
| fusion + global causal reasoning | 0.613 | 0.358 |

Against the template the same recordings scored 0.065 and 0.051, with fusion
appearing to *hurt*. The method did not change between those two rows; only what
it was compared against did. That is the whole argument for the refactor, and
`docs/EVENTS.md` explains why the old comparison was unfair in both directions.

Those figures are V1 recordings analysed with V2 code. They are stated here for
that argument alone and are not the V2 result.
