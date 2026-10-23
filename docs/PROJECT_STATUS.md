# Project status (2026-10-23, finalisation)

**Branch:** `work/reproducible-g0-20261022`, to be merged into `main` together with the paper commits of
`origin/main` (Lorenzo, `paper/` only; a trial merge is clean).

## Done in this phase

| item | evidence |
|---|---|
| S04 `a_front_pushed`: one collision, not two | A hits B (4.80 s), the bodies rebound by 0.15 m, A touches B again 0.65 s later.  A contact of the same pair within 2 s, the bodies never more than 1 m apart, is now a recontact of that collision in the reconstruction (own pose streams), the evaluation and both viewers (true boxes).  Regenerated 22 runs: only S04 `a_front_pushed` changes collision structure (commit `c884c288`, `tests/test_recontact.py`) |
| Road map as supplied incident context | the CARLA towns share coordinates: S06 recorder C fitted Town01 instead of Town05 (its tracking and path-entry events changed), S10 recorder B fitted no map.  `incident_context.json` now names the map (runner, and a documented amendment of the 22 files with old/new SHA-256); reconstruction, oracle, audit and RECONSTRUCTION viewer use it (`41d19dfb`, `tests/test_incident_map.py`) |
| Viewers | S07 (Town03_Opt) and S19 (Town04) open without `--map`, switching maps between runs; either window drives both (play, pause, seek, speed, camera, ESC) and only the instant, play state, speed, camera and quit cross; the GROUND TRUTH viewer no longer logs "reconstructed" events.  Checked live on two servers (`41d19dfb`, `8344b5f6`, `tests/test_replay_sync.py`) |
| Scorecard, final definitions | recall over reportable collisions; recontact splits apart from invented collisions; road-user errors without recorder ghosts; RMSE; phantoms near/far (diagnostic); the run's own `min_track_frames` (`5b8e0753`); wrong and missed recorder links counted by their exact verdicts: a wrong link was never counted before (`6e3883cd`) |
| Campaign v3, final design | new family `radar_asym_gnss` (asymmetric radar under G2 GNSS); raw road-user errors per job for exact pooled statistics; manifest options; launcher `scripts/campaign_v3.bat` (`2e3dc6ef`); report script with t intervals over seeds, paired changes and the GNSS x radar interaction (`2b013194`) |
| References | `docs/REFERENCES.md`: every source in one place, what it supports and the kind of evidence; DOIs re-resolved on Crossref (`bd024ccc`) |

## Decisions taken (and why)

* **Recontact.**  One physical collision may consist of several contact episodes when the bodies rebound and touch
  again; counting them as separate collisions misreports the accident.  The rule is physical (time and separation),
  identical in reconstruction, evaluation and viewers.
* **Map.**  An investigation knows where the incident happened; recognising the town from poses is an artefact of
  the simulator's overlapping coordinates.  The fallback recognition stays for runs without the key.
* **Phantoms.**  Split, as a diagnostic, by distance to the nearest true vehicle; the 1.5 m identity rule is unchanged.
* **Collision reports in the campaign.**  Not degraded (the `impulse` family is not scheduled): the requested
  degradations are GNSS and radar.  The earlier campaign studied impulse noise on the previous recordings.
* **Association.**  The frozen v1 association is the method under test; the experimental v2 association is not
  re-evaluated here (no new algorithm without a demonstrated need in G0).
* **Tracker.**  Not re-tuned to degraded radar: the degraded conditions measure robustness to errors it does not model.

## Next steps

* Freeze (tag `campaign-v3`, manifest), smoke test from the campaign worktree, launch the campaign.
* Report (`docs/CAMPAIGN_V3_REPORT.md`, `results/campaign_v3/`), README, merge into `main` with the paper commits.
