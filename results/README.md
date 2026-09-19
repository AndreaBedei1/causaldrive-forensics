# results

Generated from `artifacts_v2/` by `cdf.evaluation.final_results` and
`cdf.evaluation.supervisor_table`. Nothing here is hand-transcribed: every figure
is read from an artifact a run wrote, so a number that looks wrong can be traced
back to the run that produced it.

Regenerate with:

```bash
python scripts/evaluate.py --artifacts artifacts_v2
```

## What is here

| File | What it holds |
|---|---|
| `supervisor_table.md` / `.csv` | one row per run: outcome, clock source and quality, collision order, sign detection, line evidence, key formal verdict, physical and normative contributors, counterfactual result, main limitation |
| `final_results.md` / `.json` / `.csv` | the aggregates, per scenario first and then across them |

**Read the per-scenario table before the aggregates.** A mean over 35
scenario/variant combinations hides the thing the campaign is for: which
situations the method reconstructs and which it does not.

## What the campaign is

35 scenario/variant combinations recorded on three seeds — 105 runs, each a
separate CARLA recording with every vehicle on its own clock. Development and
calibration were done on **seed 99**, in `artifacts_v2_validation/`, which is
gitignored and never read by anything here. No threshold in the frozen
configuration was chosen by looking at seeds 0, 1 or 2.

## What is deliberately kept apart

**V1 and V2 are not mixed.** V2 changed the sensor suite (a camera and a lane
sensor were added), the clock method (contact first, then an offset-only radar
fit) and the reference the reconstruction is scored against. A figure averaged
over both generations would describe neither. The V1 tables live in
`legacy/results_v1/` and `docs/RESULTS.md`, both labelled historical.

**Physical and normative contribution are scored separately.** A vehicle that
brakes hard is a physical cause of the collision behind it and has broken no
rule. Where a scenario designs no rule violation there is nothing for the
normative comparison to score, and it reports *not applicable* rather than zero.

**A rate over no instances is a dash, not a zero.** The denominators sit beside
every rate. The give-way detector in particular has almost no sample in this
campaign, and a precision over nothing is not a result.

**UNKNOWN stays UNKNOWN.** A property the reconstruction could not decide has not
been got wrong, and folding it into PASS would make a run that observed nothing
look accurate.

## What these numbers are not

Contribution is not fault. Nothing here is a finding of legal liability and no
figure is a share of one. `docs/RESPONSIBILITY.md` states what the terms mean;
`docs/LIMITATIONS.md` states what the campaign cannot support.
