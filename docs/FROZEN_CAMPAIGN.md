# Frozen robustness and generalization campaign: protocol

This document fixes the protocol of the campaign **before** any main result is collected.  The annotated tag
`pre-robustness-campaign` points to the commit that contains it, the reconstruction it evaluates, the evaluation
code and the driver scripts.  `results/frozen_campaign_manifest.json` (written by `scripts/freeze_manifest.py`
just before tagging) records the hashes, profiles, experiment matrix, seed schedule, raw-data hashes of the 22
canonical runs and the software versions.

## What is frozen

- The reconstruction (the single FINAL method, `configs/reconstruction.yaml`), its association and fusion
  thresholds, the semantic event definitions (`docs/event_definitions.md`) and the sensor models.
- The evaluation rules: `cdf.evaluation` (`reconstruction`, `fusion_metrics`, `run_metrics`, `event_oracle`,
  `pose_errors`, `campaign_metrics`), `scripts/stability_audit.py`, the aggregation of `scripts/campaign_report.py`.
- The perturbation profiles (`cdf.robustness.perturb`, documented in `docs/robustness_profiles.md`), the condition
  families and levels, the seed schedule (`scripts/robustness.py`).
- The held-out cases, their acceptance criteria and their metrics (`configs/heldout/frozen_campaign.yaml`).

During the campaign: no threshold tuning, no reconstruction change, no change of event definitions or evaluation
rules, no removal of difficult runs or cases, no choice of favourable seeds.  The jobs run with
`CDF_ANALYSIS_FREEZE_COMMIT=<tagged commit>`: every job's provenance (`cdf.evaluation.provenance`) refuses a
different commit or a modified tracked file, and records the commit, the code hash and the configuration hash.
A methodological defect found during the campaign stops the affected experiment; any fix is a new version whose
results are kept apart and labelled with their own commit.

## Separation of results

| | inputs | outputs |
|---|---|---|
| 1. ideal canonical baseline | `traces/` (22 runs, S01..S19) | `baseline` family of the robustness campaign; `docs/CANONICAL_VALIDATION.md` |
| 2. perturbed-sensor robustness | perturbed copies in `robustness/frozen_campaign/` (deleted after each job) | `results/robustness/frozen_campaign/` |
| 3. held-out generalization | new recordings in `heldout/frozen_campaign/` | `results/generalization/frozen_campaign/` |
| 4. configuration ablation | `gnss_refined` (mutual pose refinement on) | rows labelled `configuration: ablation_mutual_refinement` |

Canonical raw data under `traces/` are never modified.  Perturbed copies and held-out recordings are not
committed; jobs records, summaries, tables and figures are.

## Robustness experiment matrix (22 canonical runs)

| family | levels | stochastic | what it perturbs |
|---|---|---|---|
| baseline | none | no | nothing: must reproduce the canonical reconstruction |
| radar | low, nominal, high | yes | range, azimuth, elevation, radial velocity, detection dropout, clutter |
| gnss | rtk, consumer, degraded | yes | absolute pose (position, heading, velocity) through the pose source |
| gnss_refined | rtk, consumer, degraded | yes | as `gnss`, mutual pose refinement on: ABLATION |
| gnss_correlated | consumer, common fraction 0.5 / 0.9 / 1.0 | yes | correlated position error between recorders |
| combined | exact / RTK / consumer / consumer rho 0.9, each + 10 % impulse noise | yes | GNSS and collision impulse reports |
| radar_gnss_combined | {rtk, consumer, degraded} x {low, nominal, high} | yes | GNSS and radar on the same copy |
| impulse | 2, 5, 10, 20 % | yes | collision impulse magnitude |
| latency | 0.05, 0.10, 0.25, 0.50 s (one recorder) | no | collision report time |
| clock | constant offsets per recorder | no | every recorded timestamp |
| downsample | 10 Hz, 5 Hz | no | ego, control and radar sampling |
| dropout | one recorder, each in turn | no | a recorder's whole recording |
| outage | 1 s radar outage, each recorder | no | radar sweeps in [t_c - 2, t_c - 1] s |

Job counts (initial with 3 seeds, maximum with 8) are in the manifest.  The GNSS x radar family has 9 cells x 22
runs x 3 seeds = 594 initial jobs (1,584 at most).

Seeds: every stochastic condition starts with seeds 0, 1, 2; seeds 3, 4, ... (at most 7) are added per (family,
level) while the standard error over seeds of any pooled metric exceeds its tolerance (association accuracy,
collision recall, event preservation and runs aligned 0.02; fused centre error 0.05 m).  Deterministic conditions
run once (seed 0).  Every random stream is keyed by SHA-256 of (seed, sensor, profile, recorder, axis or radar),
independent of family, worker and execution order: the GNSS x radar jobs draw exactly the radar errors of the
`radar` jobs and the GNSS errors of the `gnss` jobs of the same run, level and seed.

Execution: `scripts/robustness.py --canonical` resolves the runs from the manifest (no shell wildcard), writes
one line per finished attempt to `jobs.jsonl` immediately, retries a failed job once (`--max-attempts 2`), never
reruns a complete one, and deletes each perturbed copy after its job.  A smoke test (baseline, radar, GNSS,
GNSS x radar, GNSS + impulse, one missing recorder) precedes the full matrix, in a separate results folder.

## Held-out generalization

32 predeclared cases (`configs/heldout/frozen_campaign.yaml`), 11 families: rear-end, cut-in, crossing,
roundabout, chain, occlusion, non-recording causal vehicle, adjacent-lane traffic, dense groups, overtaking,
highway curve; collision and non-collision cases.  Each changes physical properties of a canonical scenario only:
blueprints never used in the canonical set (cars, vans, a light truck), separations, speeds, manoeuvre timing,
which manoeuvres happen, non-recording vehicles.  The simulator is deterministic: one recording per case (seed 0).
Before recording only a static check is run (spawns and routes resolve, no overlapping spawns; no simulation).
Acceptance (privileged checks of the simulation, never of the reconstruction): complete run; every participant on
a driving lane before its first contact; no speed above its highest scripted speed + 3 m/s before contact;
|pitch|, |roll| <= 10 deg before contact and <= 60 deg throughout.  Every actual outcome is kept (an unintended
contact or a missed intended one is reported, never re-recorded); an invalid recording is reported individually
and left out of the aggregates.  Ground truth is used only by the acceptance check and the evaluation.

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

The affected experiment (the v1 run of the matrix) was stopped after 255 records (254 complete, 1 failed) and
revised.  v2 changes evaluation and driver code only (`scripts/`; the code hash of `src/cdf` and `configs/`, the
configuration, the profiles, seeds and matrix are those of the freeze):

- `closure_violations` skips a collision without global time (its closure is undefined);
- `robustness.extra_evaluation` runs the distance-band breakdown, the stability audit and the event oracle each on
  its own: one that raises is recorded under `evaluation_errors` (reported as partial evaluations) and the job keeps
  its other measurements;
- `campaign_report` pairs runs by `Sxx/run_...` whatever the path spelling;
- `scripts/campaign_controller.py` (with `scripts/campaign.bat`) replaces the fixed process pool: same jobs, keys,
  seeds, seed rule and records, one process per job, adaptive concurrency, persistent pause / resume.

Equivalence: both changes only act where v1 raised, so every job v1 completed has the result v2 would give; those
254 records are kept and every record names its commit (`provenance.git_commit`).  The v1 failure is attempted
again under v2 (attempts are counted per version) and its v1 record stays in `jobs.jsonl` for the audit trail.
The 14 jobs running when the v1 pool was stopped wrote nothing and run again with the same seeds and keys
(`results/robustness/frozen_campaign/control/handover_v1_to_v2.json`).

## Revision v2.1 (tag `robustness-campaign-v2.1`): controller only

`scripts/campaign_controller.py` only; the jobs run the same code as v2 (same `robustness.run_job`, evaluation and
records; attempts count over v2 and v2.1 together).  The v2 controller estimated other users' load as total CPU
minus the CPU of the jobs alive at each sample, which counted every job that ended within the interval as other
load (measured 10.5 cores against 8.0 measured directly), and it lowered concurrency to 6.  v2.1 measures every
process directly, makes its first decision after one interval, applies the per-worker efficiency rule only when the
machine is saturated (below that, little CPU per job means I/O, not contention), refreshes the live state every
minute, and on start adopts job processes a previous controller left running (no running job lost at the switch).

## Revision v2.2 (tag `robustness-campaign-v2.2`): controller only

A persistent concurrency setting (`scripts\campaign.bat workers N`, `workers auto`; `control/settings.json`): with a
fixed N the CPU rules (other users' load, oversubscription) do not apply, the safety rules (RAM, page file, disk)
still lower the target.  Set to 20 workers on Andrea's request (other users' load would otherwise keep the campaign
at 8-12 workers).  Jobs run the same code as v2.
