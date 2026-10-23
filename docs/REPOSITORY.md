# Repository map, branches and data (2026-10-23)

This map was written on branch `work/reproducible-g0-20261022`, merged into `main` on 2026-10-23.  The removals
Andrea approved on 2026-10-22 were carried out after the backup was verified: the git bundle, and every file of the
manifest by SHA-256.  They are marked "removed" below.

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
| STABILITY_REVIEW, paper_positioning, REFERENCES (all references; formerly bibliography), REPOSITORY, PROJECT_STATUS | |

## Branches and worktrees

| branch / worktree | state | decision |
|---|---|---|
| `main` | this work merged (2026-10-23, approved by Andrea) with the paper commits of `origin/main` (`paper/` and `.gitignore`, LBacchiani), which the merge left untouched | pushed to origin without force |
| `work/reproducible-g0-20261022` | merged into `main` | **closed**: the local branch was deleted after the merge (it was never on origin).  Tags: `campaign-v3` (the frozen campaign code) and `campaign-v3-final` (the merge with the results) |
| `review/rtk5g-preflight` (`1c7a210b`, also on origin) | contained in `main` | kept; it can be deleted |
| `experiment/robust-offline-association` (`b786dcf2`, local only; worktree `.worktrees/robust-offline-association`) | candidate association v2: more merges, 0 false merges on its development set; safeguard policy open | **keep and re-evaluate** on the new canonical set: it targets the main G0 error (20 duplicates in S14-S19) |
| `experiment/radar-first-association` (`71b0d9ef`) | closed on 2026-10-18, verdict B | **removed**: branch and worktree; tag `archive/radar-first-association` keeps the commit |
| `experiment/rtk5g-oldtraces-overnight` (`8a323a2a`) | RTK/5G study on the previous recordings | **removed**: branch and worktree, after copying its untracked results to the backup; tag `archive/rtk5g-oldtraces-overnight` (and the `rtk5g-oldtraces-overnight-20261021*` tags) keep the commits |
| `local/gnss-free-multisensor-v2-design` (`a6c023b6`) | design documents for GNSS-free multisensor work | keep (future work) |
| `codex/gnss-free-radar-odometry-2a` (`14208c4c`, on origin) | another agent's work | branch kept; its stale worktree entry was pruned (the folder no longer existed) |
| `%TEMP%\CarlaGraph_original_1d596c1` (detached `1d596c1e`) | a temporary worktree with 1218 local changes | **removed**, after copying the 1117 changed files to `F:\CarlaGraph_backup_20261022\temp_worktree_CarlaGraph_original_1d596c1\` (SHA-256 checked; the 101 deleted paths are listed) |

**Incident during the removals (2026-10-22, 22:19).**
* **What happened.**  One of the two removed experiment worktrees held a junction to the main checkout's
  `traces/`.  `git worktree remove --force` followed it and deleted the 1343 tracked files of `traces/`.
* **Recovery.**  They were restored from the committed version, and all 783 raw files match the SHA-256 list of the
  canonical acquisition (`results/reproducibility_20261022/canonical_A_raw_sha256.txt`).  `check_dataset` passes
  22/22.  The one uncommitted change there (the S12 counterfactual summary) was regenerated.
* **Rule from now on.**  Look for junctions (`cmd /c dir /AL`) and remove them with `cmd /c rmdir` before removing
  any worktree.

## Local data outside Git

| folder | size | content | state |
|---|---|---|---|
| `scratch/` (locally excluded) | was 1.2 GB | outputs of past analyses | data **removed**; the 34 audit scripts kept (205 KB) |
| `sweeps/` (ignored) | 3.3 GB | raw recordings of the old scenario sweeps | **removed** |
| `stress_recordings/` (ignored) | 0.9 GB | an abandoned highway stress study | **removed** |
| `supplementary_work/` | 15 KB | empty remainder | **removed** |

Everything removed is in `F:\CarlaGraph_backup_20261022\untracked\`; each local file was checked there by SHA-256
before the removal.  Nothing needed by new simulations or by the campaign was removed: the code, configuration,
canonical traces and `scripts/hardening_refresh.py` all stay.

## Evidence of this work outside the repository (F:)

| folder | content |
|---|---|
| `F:\CarlaGraph_backup_20261022\` | the verified backup made before any change (git bundle of every ref, untracked data, SHA-256) |
| `F:\CarlaGraph_repro_20261022\` | reproducibility evidence and checks: S10 repeats (`baseline`, `fixed1-3`), the two acquisitions of the 22 runs (`canonical_A` installed in `traces/`, `canonical_B` the repeat), lab tests, campaign v3 smoke tests (`campaign_v3_smoke`, `mini_smoke_S13`, resume checks), S12 counterfactual runs, viewer frames (`viewer_review`, `semantic_cases`) |
| `F:\CarlaGraph_RTK5G_archive_20261021\` | the archive of the RTK/5G review (old and re-acquired 22-run sets) |
| `F:\CarlaGraph_campaign_v3_results\` | **campaign v3** results folder: the manifest of the freeze, `jobs.jsonl` (one line per attempt, 1826 records; compressed copy in `results/robustness/campaign_v3/`), the controller's summary, state and logs (`control\`).  Moved out of the campaign worktree `F:\CarlaGraph_campaign_v3\`, which was removed after the campaign (2026-10-23; no junction, clean `git worktree remove`), together with the empty scratch folders `F:\CarlaGraph_campaign_v3_work\` and `F:\CarlaGraph_v3smoke_work_1023\` |
| `F:\CarlaGraph_v3smoke_1023\` | the smoke test of the frozen campaign (33 jobs: S13 abreast in every family, S10 under G2 with each radar subset) |
| `F:\CarlaGraph_repro_20261022\g0_identical_campaign_v3\` | the determinism check of the frozen code: 22/22 runs byte-identical |

**Removing a worktree:** check it for junctions first (`cmd /c dir /AL /S <folder>`), move out any untracked result,
then `git worktree remove <folder>` without `--force`.  The incidents of 2026-10-22 (junction) and 2026-10-23
(absolute paths in a scratch script) are why; the campaign worktree was removed this way.

`canonical_A` on F: is byte-identical to the raw data in `traces/`.  It can go after approval; `canonical_B` is the
reproducibility evidence.
