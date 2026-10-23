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
* **Priority (2026-10-23, 12:19, at Andrea's request):** the campaign takes the machine's 22 cores ahead of the other
  load (a WSL virtual machine of another project, 13-18 cores).  Concurrency is fixed at 22 (`campaign_v3.bat workers
  22`).  A helper outside the frozen code puts the controller and every job process into Windows job objects whose
  only limit is the above-normal priority class.  The controller starts each job below normal, and a job's own `git`
  children (its provenance check) would start at normal priority and be starved; with the job objects, every
  descendant runs above normal.  Campaign share of the CPU rose from about 3.6 to about 15-16 cores; throughput rose
  from about 100 to about 470 jobs per hour on the short jobs left (12:50).  Priority changes neither the code nor what
  a job computes; job wall times before and after 12:19 are not comparable.
* **Background again (2026-10-23, 13:24, at Andrea's request: the machine must stay usable):** the helper was
  stopped.  Lowering a process inside a job object with a priority limit has no effect without the job's handle, so
  `stop-now` interrupted the 18 running jobs (not recorded, pending again, no attempt counted) and `resume` (13:25,
  freeze verified again) started a fresh controller.  Its jobs run below normal, as the frozen controller starts them,
  with 22 fixed workers: they use every core nobody else needs and yield to any other work.
* **No console windows, priority back (2026-10-23, 13:43, at Andrea's request):** what disturbed the desktop was a
  console window per job.  `campaign_v3.bat` starts the controller with DETACHED_PROCESS, so it has no console and
  Windows gives each job a visible one; with 22 short jobs a window opened every few seconds.  After a `stop-now` (21
  jobs pending again, not recorded), a keeper outside the frozen code started the same controller command with the
  bat's environment and a hidden console (CREATE_NO_WINDOW).  Every job and `git` child shares that invisible console.
  The controller is in a job object with the above-normal priority class, so every descendant inherits it, and the
  fixed 22 workers are kept.  The keeper also replaces the earlier watchdog: it restarts the controller, hidden,
  if it ends without COMPLETE, REFUSED or a pause request.
* **Seeds closed (2026-10-23, 14:27, Andrea's decision: no seed beyond those already decided).**  The seed rule had
  added seeds 3 and 4 to `radar_v3` extreme and `radar_asym` extreme (14:03-14:16).  The controller was paused before
  it could add a fifth seed, and a last start with `--max-seeds 5` closed the campaign.
* **COMPLETE (2026-10-23, 14:28):** 1816 jobs, all complete, 0 failed in the end; 1826 records with the 10 killed
  attempts.  All complete jobs carry the frozen commit and code hash from a clean tree; the 22 baseline jobs reproduce
  the canonical reconstruction exactly.

## After the campaign (2026-10-23)

* **Report:** `docs/CAMPAIGN_V3_REPORT.md`; tables and figures in `results/campaign_v3/` (index with SHA-256).  The
  job records are committed compressed in `results/robustness/campaign_v3/jobs.jsonl.gz` (3.1 MB; 27.5 MB
  uncompressed), with the manifest, the controller's own summary and its log.  The report script regenerates every
  committed table and figure byte for byte from them: the figures no longer embed a date, and their SVG ids are fixed
  (`tests/test_campaign_v3_report.py`).
* **Controller launch fixed on the branch:** `start_detached` uses CREATE_NO_WINDOW instead of DETACHED_PROCESS, so a
  future campaign started with `campaign_v3.bat` opens no window per job (`tests/test_campaign_revision.py`).  The
  frozen tag is unchanged.

## Next steps

* Merge into `main` with the paper commits; tag; close the work branch.
