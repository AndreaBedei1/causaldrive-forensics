# Project status (2026-10-22, stop point before Andrea's visual validation)

**Branch:** `work/reproducible-g0-20261022`, cut from `review/rtk5g-preflight`.
* Not merged and not pushed; `main` is untouched.
* `origin/main` has 4 newer commits with the paper (`paper/`), to be merged together with this work.

## Done

| item | evidence |
|---|---|
| Verified backup before any change | `F:\CarlaGraph_backup_20261022\`: git bundle of every ref and the untracked data, with SHA-256.  Re-verified before the approved removals (bundle ok, 21,311 files ok) |
| Reproducible CARLA acquisition | 4 causes found and fixed (`docs/REPRODUCIBILITY.md`).  S10: 6/6 repeats bit-identical, plus 2 more recordings at the end of the work, bitwise identical to the canonical one.  The 22 runs, acquired twice: 21/22 bit-identical, and S04 b_rear_first differs by 3e-5 m |
| New canonical set of 22 runs | re-acquired without the depth camera; integrity 22/22 (`scripts/check_dataset.py`); raw files match their SHA-256 list |
| Sensor / ground-truth separation | audit (`docs/SENSORS_AND_GROUND_TRUTH.md`); the local path uses the measured pose; the viewer draws, and turns the radar tracks with, the pose the reconstruction used; guard tests on the canonical data, the frame counter, `vehicle_transform` and a perturbed-pose reconstruction |
| G0 reconstruction and evaluation | `results/g0_scorecard_20261022/`; analysis in `docs/G0_ERROR_ANALYSIS.md` |
| Two viewers, side by side and synchronised | GROUND TRUTH and RECONSTRUCTION, each on its own CARLA server.  Only the instant, the play state and the speed cross between them (`cdf.replay.sync`).  Checked live on S04 b_rear_first (the run whose labels differ by 1.55 s) |
| Error analysis | collisions detected by impact sensors versus identities by radar; every contact is between two recorders; position error definition; completeness and the visual effect of duplicates; tracking by regime, including radar tracks of braking and colliding vehicles; every semantic disagreement checked against the ground truth |
| Campaign v3 infrastructure (not run) | families, asymmetric radar on recorder subsets (pairs run end to end), summaries stratified by number of recorders and paired with G0, intrusions matched as manoeuvres.  Smoke tests and resume checks pass.  Design in `docs/CAMPAIGN_V3.md` |
| Repository | `docs/REPOSITORY.md`: map, branches, local data and the approved removals; historical documents in `docs/archive/` |
| Independent review | fresh reviewer on the whole branch: 0 critical, 3 important, 10 minor.  All 3 important and 8 of the minor findings are fixed.  Of the other two, the scorecard details are open decision 6 below; the small robustness items are deferred (settle ticks inside `__enter__`, the Traffic Manager code default, a reverse check in `check_dataset.py`, stale docstrings) |

## Decisions taken (and why)

* **G0.**  It is a synthetic GNSS/INS with zero added error.  `ego.jsonl` is that stream, declared in each recorder's
  metadata, and the reconstruction never reads `ground_truth/`.  G0 is a reference condition, not a receiver.
* **Thresholds.**  No reconstruction threshold and no metric definition was changed to improve a number.  Metrics
  were added or made to match their own definition:
  * intrusions are matched as manoeuvres, as the scorecard docstring already stated;
  * completeness counts the road users that record nothing.
* **Asymmetric radar.**  Each recorder is degraded alone and, with three or more recorders, all but each one; the
  other recorders keep the G0 radar.  Random streams are keyed per recorder, so the comparisons are paired.
* **Removals.**  Only the approved ones, after the backup was verified; the incident with the worktree junction is
  in `docs/REPOSITORY.md`.

## Open decisions for Andrea (before the campaign freeze)

1. **Visual validation** of the 22 runs in the two viewers side by side (`docs/REPLAY.md`).
2. **Phantoms under severe radar.**  With 2 deg azimuth noise, fragments of real vehicles fall outside the 1.5 m
   identity gate and count as phantoms.  Choose: scale the gate with the declared accuracy, or split phantoms by
   their distance to the nearest true vehicle.
3. **Collision reports in the campaign.**  The v3 degradations do not touch them.  To measure collision
   identification under sensor noise, add the existing `impulse` family.
4. **Association v2** (`experiment/robust-offline-association`).  Re-evaluate it on the new canonical set: it
   targets the main G0 error (20 duplicates in S14-S19).
5. **Radar tracker under degraded levels.**  It stays frozen (current choice) or is configured from the declared
   accuracy.
6. **Scorecard details** (reviewer, minor):
   * collision recall over the contacts some sensor can report;
   * position errors without recorder ghosts;
   * `min_track_frames` read from the tracker configuration.
7. **Scenario coverage.**  No contact involves a vehicle that records nothing.  No non-recording vehicle brakes
   hard or collides; braking and contact are assessed on the recorders' own radar tracks.

## Tests

Full suite (`python -m pytest -q`, with `CARLA_ROOT=F:\Carla9_15\WindowsNoEditor`): see the stop-point report of
2026-10-22.  Without `CARLA_ROOT` the reconstruction silently runs without lanes and lane-dependent tests fail.

## Next steps, after Andrea's approval

* Settle the open decisions above.
* Freeze code, configuration and dataset: a tag and a manifest.
* Run campaign v3 with the command in `docs/CAMPAIGN_V3.md`: 1228-3238 jobs, resumable.
