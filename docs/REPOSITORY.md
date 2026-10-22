# Repository map, branches and data (2026-10-22)

This map was written on branch `work/reproducible-g0-20261022`.  Nothing listed here was deleted.  Every removal
proposed below waits for Andrea's approval.

## What lives where

| path | content | who may read it |
|---|---|---|
| `traces/<S>/<run>/vehicles/<R>/` | **raw sensor data** of recorder R: synthetic GNSS/INS (`ego.jsonl`), radar detections, own collision sensor, controls, lights, sign detections, sensor metadata | the reconstruction |
| `traces/<S>/<run>/ground_truth/` | **privileged ground truth**: every vehicle's state, collisions with identities, controls, triggers, S12 counterfactuals | simulation set-up, evaluation, GROUND TRUTH viewer |
| `traces/<S>/<run>/reconstruction/` | **reconstruction outputs** (local and global graphs, tracks, road users, alignment) | RECONSTRUCTION viewer, evaluation |
| `traces/<S>/<run>/reconstruction/evaluation/` | **privileged evaluation** of that reconstruction | analysis only |
| `results/` | study results (see `results/README.md`: current versus historical) | |
| `docs/` | method, protocols, analyses; `docs/archive/` holds documents of the previous canonical set | |
| `src/cdf/` | code: `simulation`, `recording`, `reconstruction`, `evaluation`, `replay`, `robustness` | |
| `scripts/` | command-line tools | |
| `configs/` | configuration, scenarios, sensor set-up | |
| `tests/` | unit and regression tests (`python -m pytest`, with `CARLA_ROOT` set, see below) | |

Since 2026-10-22 there is one canonical dataset: the 22 runs in `traces/`, acquired with the deterministic
acquisition (`docs/REPRODUCIBILITY.md`).  The previous recordings remain in Git history (before commit
`34162ca7`) and in the backup.  No second copy of the dataset is kept in the repository.

**Hazard.**  The reconstruction finds the OpenDRIVE maps through `CARLA_ROOT`.  Without it, it runs without lanes
and raises no error, and lane-dependent events and tests then differ.  Set
`CARLA_ROOT=F:\Carla9_15\WindowsNoEditor` before reconstructing or testing.

## Documents

| current | historical (`docs/archive/`, previous canonical set) |
|---|---|
| METHOD, event_definitions, FINAL_PARAMETER_AUDIT, SCENARIOS, REPLAY, campaign_acquisition | FROZEN_CAMPAIGN (protocol of the 2026-10-15/16 robustness campaign) |
| REPRODUCIBILITY, SENSORS_AND_GROUND_TRUTH, G0_ERROR_ANALYSIS, CANONICAL_VALIDATION, STABILITY_AUDIT | ROBUSTNESS_CAMPAIGN (its report) |
| CAMPAIGN_V3, robustness_profiles | RTK5G_PREFLIGHT_REVIEW (review of the RTK/5G profiles on the previous recordings) |
| STABILITY_REVIEW, paper_positioning, bibliography, REPOSITORY | |

## Branches and worktrees

| branch / worktree | state | decision |
|---|---|---|
| `main` (local `1d596c1e`; `origin/main` is 4 commits ahead with the paper: `paper/`, LBacchiani, 2026-10-22) | protected | untouched; merging this work needs Andrea's approval, and the paper commits must be merged too |
| `work/reproducible-g0-20261022` | this work (from `review/rtk5g-preflight`) | **keep**: to be reviewed and approved |
| `review/rtk5g-preflight` (`1c7a210b`, also on origin) | contained in the work branch | keep until the work branch is merged |
| `experiment/robust-offline-association` (`b786dcf2`, local only; worktree `.worktrees/robust-offline-association`) | candidate association v2: more merges, 0 false merges on its development set; safeguard policy open | **keep and re-evaluate**.  It targets the main G0 error (20 duplicates in S14-S19), but its numbers refer to the previous recordings.  Re-run it on the new canonical set before deciding |
| `experiment/radar-first-association` (`71b0d9ef`, local only; worktree `.worktrees/radar-first-association`) | closed on 2026-10-18, verdict B (works only with a perfect ego pose) | **archive**: proposal to tag `archive/radar-first-association` and remove the worktree and branch, after approval |
| `experiment/rtk5g-oldtraces-overnight` (`8a323a2a`, local; worktree with 4 untracked result folders, copied to the backup) | RTK/5G study on the previous recordings, reviewed in RTK5G_PREFLIGHT_REVIEW | **archive**: superseded by the new canonical set; tags `rtk5g-oldtraces-overnight-20261021*` already exist |
| `local/gnss-free-multisensor-v2-design` (`a6c023b6`) | design documents for GNSS-free multisensor work | keep (future work) |
| `codex/gnss-free-radar-odometry-2a` (`14208c4c`, on origin) | another agent's work; its worktree folder no longer exists (`git worktree list`: prunable) | keep the branch; `git worktree prune` only removes the stale entry (proposal) |
| `%TEMP%\CarlaGraph_original_1d596c1` (detached `1d596c1e`) | a temporary worktree with 1218 local changes (regenerated traces); origin unknown | **check**, then remove after approval |

## Local data outside Git

All of it is copied, with SHA-256, in `F:\CarlaGraph_backup_20261022\untracked\`.

| folder | size | content | proposal |
|---|---|---|---|
| `scratch/` (locally excluded) | 1.2 GB | scripts and outputs of past analyses | remove the local copy after approval (backup kept) |
| `sweeps/` (ignored) | 3.3 GB | raw recordings of the old scenario sweeps | as above |
| `stress_recordings/` (ignored) | 0.9 GB | an abandoned highway stress study | as above |
| `supplementary_work/` | 15 KB | empty remainder | remove after approval |

## Evidence of this work outside the repository (F:)

| folder | content |
|---|---|
| `F:\CarlaGraph_backup_20261022\` | the verified backup made before any change (git bundle of every ref, untracked data, SHA-256) |
| `F:\CarlaGraph_repro_20261022\` | reproducibility evidence and checks: S10 repeats (`baseline`, `fixed1-3`), the two acquisitions of the 22 runs (`canonical_A` installed in `traces/`, `canonical_B` the repeat), lab tests, campaign v3 smoke tests (`campaign_v3_smoke`, `mini_smoke_S13`, resume checks), S12 counterfactual runs, viewer frames (`viewer_review`, `semantic_cases`) |
| `F:\CarlaGraph_RTK5G_archive_20261021\` | the archive of the RTK/5G review (old and re-acquired 22-run sets) |

`canonical_A` on F: is byte-identical to the raw data in `traces/`.  It can go after approval; `canonical_B` is the
reproducibility evidence.
