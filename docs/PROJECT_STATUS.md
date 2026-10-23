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

## Freeze and campaign

* **Frozen:** tag `campaign-v3` = `df12f759`; manifest `results/robustness/campaign_v3/manifest.json` in the campaign
  worktree `F:\CarlaGraph_campaign_v3` (status FROZEN; code `83713ba5...`, configuration `830087c6...`, 22 raw runs).
* **Checks before the freeze:** full suite 727 passed and 6 failed, all six fixed in `df12f759` (replay tests
  122/122); reconstruction 22/22 byte-identical in four processes; G0 validator 14 PASS, 8 WARN, 0 FAIL; smoke test
  from the frozen worktree 33/33 jobs complete with every check passed (`F:\CarlaGraph_v3smoke_1023\`).
* **Launched** on 2026-10-23 at 05:36 (controller detached; `scripts\campaign_v3.bat status` in the worktree).
* **Incident (2026-10-23, before the freeze):** a scratch determinism script joined absolute run paths under its
  work folder and removed four canonical runs (S01, S02, S03, S04 `a_front_pushed`).  They were restored from git
  (141/141 raw files match their SHA-256) and regenerated; the script now refuses any target outside its work
  folder.
* **Incident (2026-10-23, during the campaign):** ten job processes ended with "exit code 1 without a result" and an
  empty stderr trace.  Two ended at 10:14:10, eight between 10:20:52 and 10:21:43, about 6.5 s apart.  The jobs had run
  15-486 s and were independent of each other.  Exit code 1 without a traceback is what `taskkill /F` leaves, and the
  controller terminates jobs only on `stop-now`, which was not requested: the processes were terminated from outside
  the campaign.  A concurrent session on this machine had listed the campaign's job processes and used `taskkill /F`
  in that window; it is the likely source, but no record ties it to these PIDs.  The ten failed attempts stay in
  `jobs.jsonl`.  They belong to nine jobs; one completed on the controller's own retry.  A killed job's record has no
  provenance, so a restarted controller does not count it as an attempt: the campaign was paused (10:31) and resumed
  (10:32, freeze verified again), and the other eight jobs (one had used both attempts) ran again from the frozen
  code.

## Next steps

* Report (`docs/CAMPAIGN_V3_REPORT.md`, `results/campaign_v3/`) once the campaign is COMPLETE.
* Merge into `main` with the paper commits; tag; close the work branch.
