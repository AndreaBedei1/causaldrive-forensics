# Project status (2026-10-22, stop point before Andrea's visual validation)

**Branch:** `work/reproducible-g0-20261022`, cut from `review/rtk5g-preflight`.
* Not merged and not pushed; `main` is untouched.
* `origin/main` has 4 newer commits with the paper (`paper/`), to be merged together with this work.

## Done

| item | evidence |
|---|---|
| Verified backup before any change | `F:\CarlaGraph_backup_20261022\`: git bundle of every ref and the untracked data, with SHA-256 |
| Reproducible CARLA acquisition | 4 causes found and fixed (`docs/REPRODUCIBILITY.md`).  S10: 6/6 repeats bit-identical.  The 22 runs, acquired twice: 21/22 bit-identical, and S04 b_rear_first differs by 3e-5 m |
| New canonical set of 22 runs | re-acquired without the depth camera; integrity checked (`scripts/check_dataset.py`) |
| Sensor / ground-truth separation | audit (`docs/SENSORS_AND_GROUND_TRUTH.md`); the local path uses the measured pose; the viewer draws the pose the reconstruction used; guard tests on the canonical data and on the frame counter |
| G0 reconstruction and evaluation | `results/g0_scorecard_20261022/`; analysis in `docs/G0_ERROR_ANALYSIS.md` |
| Two viewers | GROUND TRUTH (`scripts/view_ground_truth.py`) and RECONSTRUCTION (`scripts/replay_run.py`), with matching clocks.  Both exported every run without error.  Review menu in `docs/REPLAY.md` |
| Error analysis | how collisions are identified (every contact is between two recorders); completeness and continuity; tracking by motion regime; every semantic disagreement checked against the ground truth |
| Campaign v3 infrastructure (not run) | families, asymmetric radar on recorder subsets, scorecard summaries per condition, seed, scenario and subset, paired with G0.  Smoke tests (68 + 6 jobs, 0 failed) and resume checks.  Design in `docs/CAMPAIGN_V3.md` |
| Repository | `docs/REPOSITORY.md` (map, branches, local data); historical documents in `docs/archive/` |

## Decisions taken (and why)

* **G0.**  It is a synthetic GNSS/INS with zero added error.  `ego.jsonl` is that stream, declared in each recorder's
  metadata, and the reconstruction never reads `ground_truth/`.  G0 is a reference condition, not a receiver.
* **Thresholds.**  No reconstruction threshold and no metric definition was changed to improve a number.
  Metrics were added (scorecard, regimes) or clarified.  Example: campaign completeness counts only the road users
  that record nothing.
* **Asymmetric radar.**  Each recorder is degraded alone and, with three or more recorders, all but each one; the
  other recorders keep the G0 radar.  Random streams are keyed per recorder, so the comparisons are paired.
* **Deletions.**  Nothing was deleted; the proposals are in `docs/REPOSITORY.md`.

## Open decisions for Andrea (before the campaign freeze)

1. **Visual validation** of the 22 runs in both viewers (`docs/REPLAY.md`).
2. **Phantoms under severe radar.**  With 2 deg azimuth noise, fragments of real vehicles fall outside the 1.5 m
   identity gate and count as phantoms.  Choose: scale the gate with the declared accuracy, or split phantoms by
   their distance to the nearest true vehicle (`docs/CAMPAIGN_V3.md`).
3. **Collision reports in the campaign.**  The v3 degradations do not touch them.  To measure collision
   identification under sensor noise, add the existing `impulse` family.
4. **Association v2** (`experiment/robust-offline-association`).  Re-evaluate it on the new canonical set: it
   targets the main G0 error (20 duplicates in S14-S19).
5. **Radar tracker under degraded levels.**  It stays frozen, i.e. not told the degraded accuracy (current
   choice), or it is configured from the declared accuracy.
6. **Scenario coverage.**  No contact involves a vehicle that records nothing.  No non-recording vehicle brakes
   hard or collides.  State this in the paper or add scenarios.
7. **Removals** of local data, closed branches and the temporary worktree (`docs/REPOSITORY.md`).

## Tests

Full suite (`python -m pytest -q`, with `CARLA_ROOT=F:\Carla9_15\WindowsNoEditor`): see the stop-point report of
2026-10-22.  Without `CARLA_ROOT` the reconstruction silently runs without lanes and lane-dependent tests fail.

## Next steps, after Andrea's approval

* Settle the open decisions above.
* Freeze code, configuration and dataset: a tag and a manifest, as for the earlier campaign.
* Run campaign v3 with the command in `docs/CAMPAIGN_V3.md`: 1228-3238 jobs, resumable.
