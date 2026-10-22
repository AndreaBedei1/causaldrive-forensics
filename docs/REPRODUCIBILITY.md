# Reproducibility of the CARLA acquisitions

**Date:** 2026-10-22. **Branch:** `work/reproducible-g0-20261022`. CARLA 0.9.15 (private server, port 3000),
Python 3.8.20 (conda `carla`), synchronous mode, `fixed_delta_seconds` 0.05, substepping 0.01 s x 10.

This document separates three kinds of determinism:

* **physics** — the simulated vehicles (ground truth): same scenario, seed and configuration must give the same
  trajectories, contacts and post-impact motion;
* **acquisition** — the sensor streams written from that physics (radar sweeps, GNSS/INS pose, collision
  callbacks, camera counters): one sample per tick, no loss, the same frames;
* **reconstruction** — the same raw data must give the same reconstruction (pure offline computation).

## What was wrong

Repeating a scenario with the same seed gave different trajectories.  S10 `deflected_into_c`, recorded four times
with the code at `1c7a210b`: positions up to **0.33 m** apart, speeds up to 2.0 m/s, the A–C contact sometimes one
continuous episode of 182 ticks and sometimes three short ones; the vehicles already differed by 2–6 cm at the
first recorded frame (`results/reproducibility_20261022/s10_repeats.json`, stage `baseline`).

Root causes, each isolated by an experiment (lab scripts on the same server; every claim below was measured, not
inferred):

| # | cause | evidence | fix (commit `0685286f`) |
|---|---|---|---|
| 1 | The Traffic Manager was created in synchronous mode although no scenario drives a vehicle with it. | 3 vehicles, spawn/launch/drive, 5 client processes: with an idle TM up to 0.59 m apart; without it 10/10 bit-identical. | `simulation.traffic_manager_enabled: false` |
| 2 | Actors were spawned right after switching the server from asynchronous to synchronous mode; the frame in flight still has a wall-clock step. | without settle ticks 1 process in 5 off by a discrete 0.062 m; with 10 empty synchronous ticks 10/10 identical. | `simulation.sync_settle_ticks: 10` (`ScenarioWorld.__enter__`) |
| 3 | `apply_control`, `set_target_velocity`, `set_light_state` are asynchronous RPCs: one can be executed after the tick it was meant for (the "launch outlier": one vehicle one tick of travel off in ~1 run in 4). | S10 with 1 and 2 fixed: 1 of 4 repeats with C 0.287 m ahead at t = 0 (= 6 m/s x one tick). | commands queued and sent with `client.apply_batch_sync` before `world.tick()` (`ScenarioWorld.send`) |
| 4 | The controller switched to its post-impact behaviour when the asynchronous collision callback happened to arrive (0, 1 or 2 ticks late); S10's deflection ramp starts at that instant. | identical first contacts, different post-impact contact sequences. | reaction `impact_reaction_ticks` (1) after the collision's own frame; radar sweeps of the frame are awaited first (barrier); a callback arriving too late is counted in `metadata.json: late_impact_notifications` |

A negative result is worth stating: the RGB camera, the radars and their callback load do **not** affect the
physics (lab: 3 vehicles with cameras and radars, heavy callbacks, 4/4 bit-identical), nor does the elapsed
simulation time on the server.

## Results after the fixes

* **S10**, 6 repeats: 6/6 bit-identical ground truth over the whole run, identical collision callbacks and contact
  episodes (`s10_repeats.json`, stage `fixed3`).
* **All 22 canonical runs**, recorded twice (sets A and B, separate client processes): **21/22 bit-identical**
  (positions, speeds, yaw, controls, collision callbacks).  S04 `b_rear_first` differs by at most
  **3.1e-5 m**, 9.8e-5 m/s, 6.4e-4 deg from the A–B contact tick on: one or two float32 ULPs at those map
  coordinates, the same contact episodes (`canonical_A_vs_B.json`).
* `late_impact_notifications` = 0 in all 44 recordings.

**Declared criterion** (used from now on to accept a re-acquisition): identical contact episodes (pair, start,
end, number of ticks), and ground-truth positions within 1e-3 m and speeds within 1e-2 m/s of the reference run.
All 22 runs meet it; 21 meet it exactly.

**What CARLA does not guarantee.** PhysX contact resolution is not bit-exact across processes in every case (S04
residual above).  In a long, continuous, low-impulse contact such a rounding difference can be amplified: in one
lab repeat of S10 before fix 3 was complete, a 6e-7 difference in a steering command three ticks after the A–B
impact grew to 5.8 mm.  We therefore never claim bit-exact physics in general; we measure every acquisition against
the criterion above (`scripts/repro_check.py`).  Changing CARLA version, GPU driver or physics settings requires the
check to be repeated.

## Acquisition integrity of the new canonical set

`scripts/check_dataset.py --root <set>`: 22/22 PASS for set A, which is now the raw data under `traces/`
(`results/reproducibility_20261022/canonical_A_integrity.json`, SHA-256 of every raw file in
`canonical_A_raw_sha256.txt`).  Per run: ground truth contiguous at 20 Hz for every participant; each recorder's
`ego.jsonl`, `controls.jsonl`, `lights.jsonl` and every radar one sample per frame on the same frames; RGB camera
one frame per 0.1 s with no drop or duplicate; no depth stream (disabled since 2026-10-21); every collision a
recorder logged is in the ground truth at the same frame.

The depth camera is no longer acquired.  It was never an input of the reconstruction or of the campaign metrics
(`docs/RTK5G_PREFLIGHT_REVIEW.md`, section "Aggiornamento protocollo: depth camera").

## Old versus new canonical set

`scripts/compare_reacquisition.py --old-root traces@1c7a210b --new-root canonical_A`: the collision signatures are
identical in 21/22 runs, most runs bit-identical or within centimetres.  S10 differs, as expected: the old
recording's 186-tick continuous A–C contact was one of the non-reproducible outcomes; the new recording (A–C
4.75–6.0 s, then two short re-contacts) is the reproducible one.  The old raw data remain in Git history and in
`F:\CarlaGraph_backup_20261022`.

## Reproducing

```bat
python scripts\start_carla.py --carla-root F:\Carla9_15\WindowsNoEditor
python scripts\run_scenario.py --scenario S10 --variant deflected_into_c --output <dir> --no-autostart --override simulation.real_time_pacing=false
python scripts\repro_check.py --runs <dir1>\S10\run_0_deflected_into_c <dir2>\S10\run_0_deflected_into_c
python scripts\check_dataset.py --root <dir>
```
