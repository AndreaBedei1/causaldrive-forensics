# Campaign v3: design and freeze

**Status (2026-10-23): COMPLETE.**  Approved by Andrea (2026-10-23, full campaign authorised).  Frozen at the tag
`campaign-v3` (code, configuration, dataset and protocol: `results/robustness/campaign_v3/manifest.json`) and run from
a separate worktree of that tag, so that later work on the repository could not change a job.  Ran from 05:36 to
14:28: 1816 jobs, all complete (section "Execution").  Results and report: `results/campaign_v3/` and
`docs/CAMPAIGN_V3_REPORT.md`.

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
| `radar_asym_gnss` | G2 x {nominal, severe} | radar: the subsets of `radar_asym`; GNSS: all |

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
* **Asymmetric radar under degraded GNSS.**  `radar_asym_gnss` repeats the subsets of `radar_asym` at the realistic
  radar levels with G2 GNSS on every recorder.  Its radar errors are those of `radar_asym` and its GNSS errors those
  of `gnss` degraded (same seed), so it pairs with both and with `radar_gnss_v3` (G2, every radar degraded).
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

| R | baseline | gnss | radar_v3 | radar_asym | radar_gnss_v3 | radar_asym_gnss | jobs per run |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 2S | 3S | 6S (2 subsets) | 4S | 4S (2 subsets) | 1 + 19S |
| 3 | 1 | 2S | 3S | 18S (6 subsets) | 4S | 12S (6 subsets) | 1 + 39S |

On the 22 canonical runs (16 with two recorders, 6 with three), `jobs_for` counts:
* **1636 jobs at S = 3** (the minimum): baseline 22, gnss 132, radar_v3 198, radar_asym 612, radar_gnss_v3 264,
  radar_asym_gnss 408;
* **4326 jobs at S = 8** (the maximum).

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

## Commands

The campaign ran from `F:\CarlaGraph_campaign_v3`, a `git worktree` of the tag `campaign-v3`.  That worktree was
removed after the campaign; its results folder is kept in `F:\CarlaGraph_campaign_v3_results\` and committed in
`results/robustness/campaign_v3/`.  To run again, create a worktree of the tag (`git worktree add <folder>
campaign-v3`) and use, from that folder:

```bat
scripts\campaign_v3.bat start      :: verify the freeze against the manifest, start the controller detached
scripts\campaign_v3.bat status     :: completed / failed / running / pending jobs, resources, estimated time left
scripts\campaign_v3.bat pause      :: running jobs finish and are recorded, then the controller exits
scripts\campaign_v3.bat resume     :: verify the freeze again and continue: complete jobs are skipped
```

The controller (`scripts/campaign_controller.py`) survives the terminal and the chat session.  It adapts the number
of workers to the machine's load and leaves room for other users.  Every finished attempt is a line of
`results\robustness\campaign_v3\jobs.jsonl`; a failed job is kept with its error and tried at most twice.
`python scripts\robustness.py --summarize --results results\robustness\campaign_v3` rewrites the summaries from
`jobs.jsonl`, also those of an interrupted campaign.

## Decisions taken at the freeze (2026-10-23)

1. **Phantoms.**  The identity rule is unchanged (`IDENTITY_MAX_BOX_DISTANCE_M` = 1.5 m).  Phantoms are split, as a
   diagnostic, by the median distance of their tracks to the nearest true vehicle box: near (<= 3 m, a displaced
   estimate of a vehicle) or far (clutter) (`cdf.evaluation.scorecard.PHANTOM_NEAR_M`).
2. **Scorecard definitions** (`cdf.evaluation.scorecard`, module docstring):
   * recall and the identified rate are over the reportable collisions;
   * a recontact reported as a collision of its own is a recontact split, not an invented collision;
   * road-user position and speed errors exclude recorder ghosts;
   * error statistics carry the RMSE;
   * the observability threshold is the run's own `min_track_frames`.
3. **Map.**  The road map is supplied incident context (`docs/REPRODUCIBILITY.md`, amendment 2026-10-23).
4. **Collisions with the wrong participants** count as detected but not identified: a true collision without a node
   naming its recorders is matched, second, to a node one of its own recorders reported at that time
   (`cdf.evaluation.reconstruction.match_collisions`).  Before, such a collision counted as missed and its node as
   invented (independent review of 2026-10-23).
5. **Identity of a radar track under perturbed GNSS.**  The evaluation places a recorder's local tracks with its
   true first pose: which vehicle a track followed is a physical fact, so a recorder's own pose error does not turn a
   real vehicle into a phantom; the position error of the fused road users is measured on the reconstruction's own
   poses.
6. **Seed rule.**  Decided per family and level over all its subsets and recorder strata (`need_more_seeds`); the
   strata report their own intervals over the seeds they share.
7. **Known properties of the frozen code** (final review of 2026-10-23; fixed on the branch after the tag, not in
   the campaign):
   * the legacy per-job `fused_centre_error_median_m` (`run_metrics`), which feeds the controller's own summary and
     the seed rule's 0.05 m tolerance, falls back to every road user, recorder ghosts included, when a job's only
     road users are ghosts.  It can only add seeds (never remove one) and does not enter the report's tables, which
     use the raw road-user errors without ghosts;
   * the frozen manifest's `scope` and `launcher` fields carry the text of the RTK/5G preflight; the campaign is the
     one described here and is launched with `scripts\campaign_v3.bat`;
   * a recontact reported by one recorder only is counted as an invented collision, not as a recontact split; the
     report checks the invented collisions of S04 `a_front_pushed` for that case.
8. **Authoritative tables.**  `scripts/campaign_v3_report.py` (errors pooled over all compared states, t intervals
   over seeds).  The controller's own summary (`campaign_v3_conditions.md`: median of the per-job medians) is kept
   for continuity.

## Execution (2026-10-23)

* **Size.**  1816 jobs: 1636 at three seeds, plus seeds 3 and 4 that the seed rule added to `radar_v3` extreme and
  `radar_asym` extreme (180 jobs).  `jobs.jsonl` holds 1826 records: the 1816 complete jobs and 10 failed attempts.
* **Seeds closed by decision.**  At 14:27 Andrea decided to add no seed beyond those already decided.  The controller
  was paused, and a final start with `--max-seeds 5` closed the campaign (COMPLETE, nothing left to run).  With 5
  seeds every tolerance is met except the legacy fused-centre error of `radar_asym` extreme (standard error 0.052 m
  against 0.05 m; decision 7).
* **External terminations.**  Ten job processes were terminated from outside the campaign (10:14, 10:20-10:21; exit
  code 1, no traceback).  The failed attempts stay in `jobs.jsonl`; a pause and resume re-queued the jobs, which then
  completed.
* **Priority and windows.**  From 12:19 the campaign ran with 22 fixed workers ahead of another project's load (an
  above-normal priority inherited through a Windows job object).  From 13:25 to 13:43 it ran below normal, as the
  controller starts its jobs.
  `campaign_v3.bat` started the controller with DETACHED_PROCESS, so Windows gave every job a visible console window.
  From 13:43 the same controller command ran with a hidden console shared by its jobs.  On the branch (after the
  campaign) `start_detached` now uses CREATE_NO_WINDOW (`tests/test_campaign_revision.py`).
* **Provenance.**  Every complete job carries the frozen commit `df12f759`, code hash `83713ba5...` and a clean tree.
  The controller verified the freeze at each of its five starts.  None of these events changed what a job computes.
  Details: `docs/PROJECT_STATUS.md`.

## Open points recorded before the freeze (2026-10-22)

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
