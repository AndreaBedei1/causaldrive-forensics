# Robustness campaign: protocol

> **Historical (archived 2026-10-22).**  Protocol of the campaign run on the canonical recordings that preceded the deterministic re-acquisition of 2026-10-22 (Git history before commit `34162ca7`, tag `robustness-campaign-final`).  Current dataset and results: [README](../../README.md), [G0_ERROR_ANALYSIS](../G0_ERROR_ANALYSIS.md); next campaign: [CAMPAIGN_V3](../CAMPAIGN_V3.md).


The protocol of the robustness study of the frozen reconstruction on the 22 canonical runs (S01..S19).  Results:
[ROBUSTNESS_CAMPAIGN.md](ROBUSTNESS_CAMPAIGN.md); perturbation profiles: [robustness_profiles.md](../robustness_profiles.md);
manifest: `results/robustness_campaign_manifest.json` (`scripts/campaign_manifest.py`).

## History and scope

- 2026-10-15: the protocol was frozen before any main result (tag `pre-robustness-campaign`, commit 5d7adf76):
  reconstruction, configuration, event definitions, evaluation rules, perturbation profiles, matrix and seed
  schedule.  The preregistered campaign also contained a collision-report latency family and a held-out set of
  automatically generated scenarios.
- 2026-10-15/16: the campaign ran (revisions v2, v2.1, v2.2 below; 3862 jobs in total).
- 2026-10-16: the author fixed the scientific scope of the study to the robustness experiments on the 22 manually
  reviewed canonical runs.  The latency family (88 jobs) and the held-out set were removed from the study and from the
  active repository (code, configuration, records, reports); they remain only in the Git history (tag
  `robustness-campaign-v2.2`, commit 1183f522).  The retained 35 conditions, their 3,774 jobs and their
  measurements are unchanged; the active version is tagged `robustness-campaign-final`.

The retained matrix is therefore a subset of the preregistered one, not a separate preregistration.

## What is frozen

- The reconstruction (the single FINAL method, `configs/reconstruction.yaml`), its association and fusion
  thresholds, the semantic event definitions (`docs/event_definitions.md`) and the sensor models.  The manifest
  holds a hash of the reconstruction sources (`src/cdf/reconstruction`, `common`, `recording`, `perception`,
  `configs/reconstruction.yaml`) computed both at the frozen tag and on the current tree: they are equal.
- The evaluation rules: `cdf.evaluation` (`reconstruction`, `fusion_metrics`, `run_metrics`, `event_oracle`,
  `pose_errors`, `campaign_metrics`), `scripts/stability_audit.py`, the aggregation of `scripts/campaign_report.py`.
- The perturbation profiles (`cdf.robustness.perturb`), the families and levels, the seed schedule
  (`scripts/robustness.py`).

No threshold was tuned and no run or seed was removed during the campaign.  Every job checks at its start that the
checkout is the campaign's commit with no modified tracked file (`CDF_ANALYSIS_FREEZE_COMMIT`, set by the
controller) and records commit, code hash and configuration hash (`provenance`).

## Experiment matrix (22 canonical runs, 35 conditions)

| family | levels | stochastic | what it perturbs |
|---|---|---|---|
| baseline | none | no | nothing: must reproduce the canonical reconstruction |
| radar | low, nominal, high | yes | range, azimuth, elevation, radial velocity, detection dropout, clutter |
| gnss | rtk, consumer, degraded | yes | absolute pose (position, heading, velocity) through the pose source |
| gnss_refined | rtk, consumer, degraded | yes | as `gnss`, mutual pose refinement forced on (ablation) |
| gnss_correlated | consumer, common fraction 0.5 / 0.9 / 1.0 | yes | correlated position error between recorders |
| combined | exact / RTK / consumer / consumer rho 0.9, each + 10 % impulse noise | yes | GNSS and collision impulse reports |
| radar_gnss_combined | {rtk, consumer, degraded} x {low, nominal, high} | yes | GNSS and radar on the same copy |
| impulse | 2, 5, 10, 20 % | yes | collision impulse magnitude |
| clock | constant offsets per recorder | no | every recorded timestamp |
| downsample | 10 Hz, 5 Hz | no | ego, control and radar sampling |
| dropout | one recorder, each in turn | no | a recorder's whole recording |
| outage | 1 s radar outage, each recorder | no | radar sweeps in [t_c - 2, t_c - 1] s |

2102 initial jobs, 5292 at most (manifest).  Seeds: every stochastic condition starts with seeds 0, 1, 2; seeds 3,
4, ... (at most 7) are added per (family, level) while the standard error over seeds of any pooled metric exceeds its
tolerance (association accuracy, collision recall, event preservation and runs aligned 0.02; fused centre error
0.05 m).  Deterministic conditions run once (seed 0).  Every random stream is keyed by SHA-256 of (seed, sensor,
profile, recorder, axis or radar), independent of family, worker and execution order: the GNSS x radar jobs draw
exactly the radar errors of the `radar` jobs and the GNSS errors of the `gnss` jobs of the same run, level and seed.
The streams are not keyed by run: one seed is one realization shared by all 22 runs.

Execution: `scripts/campaign_controller.py` (`scripts\campaign.bat`) runs the jobs of `scripts/robustness.py`, one
process per job with single-threaded BLAS (verified node-for-node identical to the canonical reconstruction),
writes one line per finished attempt to `jobs.jsonl`, retries a failed job once, never repeats a complete one,
deletes each perturbed copy after its job, and can be paused and resumed at any time.  A smoke test (baseline,
radar, GNSS, GNSS x radar, GNSS + impulse, one missing recorder) preceded the campaign
(`results/robustness/frozen_campaign_smoke/`).  Canonical raw data under `traces/` are never modified.

## Measurements

The campaign uses the existing evaluation only (no new event oracle, no new detection threshold):

- correctness against simulator ground truth: true contacts detected and identified, wrong collision matches,
  unmatched reports, contact timing and clock alignment (`evaluation.reconstruction`, `run_metrics`); recorder
  links correct / wrong / missed, association accuracy, merges correct / false / missed, phantom entities,
  duplicate hypotheses, fused centre and velocity errors (median, p95, max) and their calibration
  (`fusion_metrics`); the same by distance band (0-10, 10-25, > 25 m: the track's median radar range) and for the
  incident participants (`campaign_metrics`); track losses, fragmentation, phantom tracks, EGO_PATH oscillations,
  CUT_IN against the audit's ground-truth criterion, CRITICAL_TTC closure, trajectory jumps
  (`stability_audit`); core events against the ground-truth coverage oracle (`event_oracle`);
- stability against the unperturbed reconstruction: core events preserved, added, and their time differences
  (`run_metrics.core_event_diff`);
- inputs: absolute and relative (simultaneous recorder pairs) pose error of the injected GNSS (`pose_errors`).

Aggregation and the GNSS x radar interaction analysis are defined in the docstring of `scripts/campaign_report.py`.
Synthetic CARLA perturbations are engineering models: they establish the operating envelope of the method on
simulated data and do not demonstrate real-world sensor performance.

## Revision v2 (tag `robustness-campaign-v2`): evaluation defect found during the campaign

Found on 2026-10-15 at job 191 of the v1 run (`radar high`, S16, seed 0): under heavy clutter a reconstructed
COLLISION node carried no global time (`t_global` null: the collision was not placed on the global clock), and the
frozen stability audit (`stability_audit.closure_violations`) compared null with a number and raised.  Because the
whole further evaluation of a job ran as one block, the job was recorded as failed with no measurement at all, and
exactly the most degraded cases would have been missing from the aggregates.  The reconstruction itself is not
involved.

The v1 run was stopped after 255 records (254 complete, 1 failed) and revised.  v2 changes evaluation and driver
code only (`scripts/`; reconstruction, configuration, profiles, seeds and matrix are those of the freeze):

- `closure_violations` skips a collision without global time (its closure is undefined);
- `robustness.extra_evaluation` runs the distance-band breakdown, the stability audit and the event oracle each on
  its own: one that raises is recorded under `evaluation_errors` and the job keeps its other measurements;
- `campaign_report` pairs runs by `Sxx/run_...` whatever the path spelling;
- `scripts/campaign_controller.py` replaces the fixed process pool: same jobs, keys, seeds, seed rule and records.

Equivalence: both changes only act where v1 raised, so every job v1 completed has the result v2 would give; those
254 records are kept and every record names its commit (`provenance.git_commit`).  The v1 failure was attempted
again under v2 and completed; its v1 record stays in `jobs.jsonl.gz` for the audit trail.  The 14 jobs running
when the v1 pool was stopped wrote nothing and ran again with the same seeds and keys.

## Revisions v2.1 and v2.2 (tags `robustness-campaign-v2.1`, `-v2.2`): controller only

The jobs run the same code as v2.  v2.1: the controller measures other users' CPU load directly (v2 counted the
CPU of jobs ending within a sample as other load and lowered concurrency to 6), decides after a warm-up, applies its
per-worker efficiency rule only when the machine is saturated, and adopts job processes a previous controller left
running.  v2.2: a persistent concurrency setting (`workers N`, `workers auto`); the campaign ran with 20 and then 24
workers at the author's request.

## Final version (tag `robustness-campaign-final`)

The scope change above: the latency family and its perturbation parameters (`CollisionPerturbation.latency_s`,
`latency_recorders`) and the held-out set (configuration, driver, records, report) removed; the reports
regenerated from the retained records; the manifest replaced by the final-scope manifest; the report reads the
committed `jobs.jsonl.gz`.  Reconstruction sources unchanged (manifest).  Jobs per commit among the 3,774 retained:
254 (pre-robustness-campaign), 82 (v2), 69 (v2.1), 3,369 (v2.2).
