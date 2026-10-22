# Campaign v3: design (prepared, NOT started)

**Status (2026-10-22):** infrastructure ready and smoke-tested on two runs.  The massive campaign must not start
before Andrea's visual validation of the 22 canonical runs and explicit approval, followed by the freeze (tag and
manifest) of code, configuration and dataset.

## Question

How do the reconstructed collisions, and the completeness and continuity of the trajectories, degrade from G0
(ideal GNSS/INS, unperturbed radar) to realistic GNSS and radar degradations, applied alone, combined and
asymmetrically?

## Conditions (`scripts/robustness.py`, families)

| family | levels | recorders degraded |
|---|---|---|
| `baseline` | G0 | none (must reproduce the canonical reconstruction exactly) |
| `gnss` | G1 RTK, G2 degraded (`docs/robustness_profiles.md`) | all |
| `radar_v3` | nominal, severe, extreme | all |
| `radar_asym` | nominal, severe, extreme | **subsets**: each recorder alone; with three or more recorders also all but each one (with three, every pair) |
| `radar_gnss_v3` | {G1, G2} x {nominal, severe} | all |

* **Reference.**  "Not degraded" means the G0 condition: CARLA's radar with no added error and the exact
  synthetic GNSS/INS.  In `radar_asym` the recorders outside the subset keep that radar.  Every job is compared with
  the G0 `baseline` job of the same run (paired).
* **Individual and collective effects.**  Compare, within the same population of runs and at the same level and
  seed:
  * `radar_asym` "alone": one recorder degraded;
  * `radar_asym` "all but one": only one recorder keeps the G0 radar;
  * `radar_v3`: all recorders degraded.

  The condition table is stratified by the number of recorders R.  "All but one" exists only for R = 3 (6 runs),
  so the three-way comparison uses the R = 3 rows.  With two recorders the design is exactly "only A, only B, both".
* **Paired random streams.**  Random streams are keyed by (seed, sensor, profile, recorder, radar or axis), never
  by the family or the subset.  A recorder degraded alone therefore receives exactly the errors it receives in every
  other subset and in `radar_v3` (test `test_campaign_v3.PairedAsymmetricStreams`).  The GNSS errors of
  `radar_gnss_v3` equal those of `gnss`.
* **Reconstruction configuration frozen.**  The tracker is not re-tuned per radar level.  The severe and extreme
  levels therefore measure robustness to a degradation the reconstruction does not model.  A tracker told the
  degraded accuracy, as a real system would be from its datasheet, could do better.  This is a design choice to
  state in the paper.
* 5G is only the transport of the RTK corrections.  No network performance is simulated.
* **Seeds.**  Stochastic families draw seeds 0, 1, 2, ... (at least 3, at most 8) until the standard error over
  seeds of every pooled metric is below its tolerance.  The tolerances cover:
  * the earlier metrics;
  * the identified-collision rate (0.02);
  * the represented share of observable road users (0.02).

## Results written by the runner

* **`jobs.jsonl`**: one line per attempt.  It holds the existing measurements (evaluation, fusion metrics,
  stability audit, event oracle, pose errors) and, for the v3 families, the `scorecard` (`cdf.evaluation.scorecard`).
  Failed jobs are kept with their error and stack trace and retried at most `--max-attempts` times.
* **`campaign_v3_jobs.csv`**: one row per job, i.e. per condition, seed, scenario and degraded recorder subset.
  Columns:
  * collisions detected, identified and invented, and the timing error;
  * observable and represented road users (vehicles that record nothing), missed vehicles, duplicates, recorder
    ghosts and phantoms;
  * position and speed errors (median and P95);
  * association errors;
  * semantics;
  * `d_*`, the paired change from the G0 baseline of the same run.
* **`campaign_v3_conditions.md`** and **`campaign_v3.json`**: one row per condition (family, level, degraded
  subset, number of recorders).  Per seed the jobs of a condition are pooled: rates are ratios of sums, while counts
  and paired changes are means per job.  The table then gives the mean over seeds ± SD.
* **`summary.md` / `summary.csv` / `figures/`**: the earlier per-condition table, kept for continuity.

## Size

For a run with R recorders and S seeds:

| R | baseline | gnss | radar_v3 | radar_asym | radar_gnss_v3 | jobs per run |
|---|---|---|---|---|---|---|
| 2 | 1 | 2S | 3S | 6S (2 subsets) | 4S | 1 + 15S |
| 3 | 1 | 2S | 3S | 18S (6 subsets) | 4S | 1 + 27S |

On the 22 canonical runs (16 with two recorders, 6 with three), `jobs_for` counts:
* **1228 jobs at S = 3** (the minimum);
* **3238 jobs at S = 8** (the maximum).

## Verification (2026-10-22, before the freeze)

* **Smoke test.**  Runs S01 and S10, all five families, 2 seeds.  Before the subset generalisation: 68 jobs, 0
  failed, about 52 min with 6 workers.  Results are on F: in `F:\CarlaGraph_repro_20261022\campaign_v3_smoke\`.
* **Pair subsets end to end.**  S10, `radar_asym` severe, seed 0: the three "all but one" jobs (A+B, A+C, B+C) ran
  with the real runner and completed (`F:\CarlaGraph_repro_20261022\pair_subset_smoke\`).  Phantoms per job:
  * one recorder degraded: 8.7;
  * two: 17.3;
  * all three (`radar_v3`): 26.0.
* **Road users that record nothing.**  S13 abreast, baseline, GNSS G1/G2 and radar nominal/severe/extreme, 1 seed:
  6 jobs completed, and the completeness columns are filled (`F:\CarlaGraph_repro_20261022\mini_smoke_S13\`).
* **Resuming.**
  * Running the same command again on the finished smoke results started no job.
  * A copy with three job lines removed, simulating an interruption, re-ran exactly those three jobs and nothing
    else.  The two re-run baselines reproduced the canonical graph (`identical_graph`).
* **Smoke-test findings.**  In S01 and S10 every vehicle is a recorder, so the completeness of non-recording road
  users is not exercised there.
  * Collisions: 100 % identified with the correct participants at every level, 0 invented.
  * GNSS G1 and G2: no change in the scorecard numbers of these two runs.
  * Radar: anonymous road users without a true identity ("phantoms"), mean per job:

| level | all recorders degraded | one recorder degraded |
|---|---|---|
| nominal | 0.5 | 0.2 |
| severe | 64.5 | 25.9 |
| extreme | 95.2 (plus 2.0 recorder ghosts) | 38.4 (plus 0.8 recorder ghosts) |

  The phantoms add up over the recorders.  Summed over the recorders of a run degraded one at a time, they equal
  the all-degraded count: per seed, 129.5 against 129 under severe radar.  In this smoke test (2 runs x 2 seeds) the
  phantoms come from each degraded recorder's own tracks and add up approximately.  Independence is not claimed
  from so small a sample.

## Command (to be given only after approval and freeze)

```bat
python scripts\robustness.py --canonical --families baseline,gnss,radar_v3,radar_asym,radar_gnss_v3 ^
    --work robustness\campaign_v3 --results results\robustness\campaign_v3 --workers 8
```
To resume, re-run the same command: complete jobs are skipped.  `--summarize` rewrites every summary from
`jobs.jsonl`.

## Open points before the freeze

1. **"Phantoms" under severe radar.**  In the smoke test (S01, S10; 2 seeds) there are 26 to 101 anonymous road
   users without a true identity per job under `radar_v3 severe` and `extreme`, while the collisions stay identified.
   * **Identity rule.**  A road-user sample gets a true identity only when its box lies within
     `IDENTITY_MAX_BOX_DISTANCE_M` = 1.5 m of a true vehicle (`cdf.evaluation.fusion_metrics`).
   * **Why real vehicles end up counted.**  With a 2° azimuth sigma, the lateral error at 40 m is about 1.4 m
     (1 sigma).  Many fragments of real vehicles therefore fall outside the tolerance and are counted as phantoms.
     The phantom count under severe radar thus mixes real phantoms with mislocalised real vehicles.
   * **Decision needed before the campaign, and to document.**  Either the identity tolerance scales with the
     declared measurement uncertainty, or phantoms are split by their distance to the nearest true vehicle (a
     diagnostic that leaves the definition unchanged).
   * **Not changed here.**  Changing an evaluation tolerance to improve a statistic needs an explicit decision.
2. **Cost.**  Severe and extreme radar jobs are several times slower than G0 jobs, because clutter and noise create
   many short tracks.  Plan the worker count and the time accordingly.
