# Sensors versus ground truth

**Date:** 2026-10-22 (audit and changes on branch `work/reproducible-g0-20261022`).

The simulator's ground truth may be used for three things only: to run the simulation, to synthesise the sensor
measurements, and to evaluate the reconstruction.  This document lists what each recording file is, who may read
it, what the audit found, and what changed.

## Files of a run

| file | what it is | written from | read by the reconstruction |
|---|---|---|---|
| `ground_truth/states.jsonl` | true pose, velocity, acceleration, box of **every** vehicle at every frame | simulator state | **never** |
| `ground_truth/collisions.jsonl` | every collision callback with the other actor's identity | simulator | **never** |
| `ground_truth/controls.jsonl`, `metadata.json` | scripted controls, scenario, map, who records | scenario | **never** |
| `metadata.json` (run) | scenario design, timing of the acquisition | runner | **never** |
| `incident_context.json` | known context (legal speed limit) | scenario YAML | yes: supplied knowledge, not perception |
| `vehicles/<R>/ego.jsonl` | **synthetic GNSS/INS of recorder R** (position, heading, attitude, velocity, IMU acceleration and angular rate) | sensor model applied to R's simulated state | yes |
| `vehicles/<R>/radar/<id>/observations.npz` | CARLA radar detections: range, azimuth, elevation, radial velocity (no object id, no label) | CARLA radar sensor | yes |
| `vehicles/<R>/collisions.jsonl` | R's own collision sensor: time and impulse magnitude, **no partner identity** | CARLA collision sensor, identities stripped | yes |
| `vehicles/<R>/controls.jsonl`, `lights.jsonl` | R's own commands and indicator state (on-board CAN) | R's controller | yes |
| `vehicles/<R>/traffic_signs.jsonl` | STOP / YIELD detections of R's camera detector (no CARLA label) | image detector | yes |
| `vehicles/<R>/metadata.json` | sensor specs and mounts, R's own footprint, the declared pose sensor | configuration | yes (specs, footprint) |

## The `ego.jsonl` question

`ego.jsonl` **is** the recorder's true simulated state, sampled every tick: in profile **G0** the synthetic GNSS/INS
adds no error.  It is not read from `ground_truth/` by the reconstruction, but its content equals the truth.  That
is the definition of G0 and it is now declared in each recorder's metadata (`pose_sensor`: model synthetic
GNSS/INS, profile G0, added error none, rate 20 Hz, fields) and in this document:

* **G0 is a reference condition, not a receiver.**  A perfect pose is an upper bound: results in G0 measure what
  radar, association and fusion lose on their own.  No claim about a real receiver may be drawn from G0.
* **G1 (RTK) and G2 (degraded)** apply the documented error processes (`cdf.robustness.perturb.GNSS_PROFILES`,
  `docs/robustness_profiles.md`) to this stream before the reconstruction sees it.

**Leak found and fixed (commit `d9c4d4e8`).**  Under G1/G2 only the fusion's common-frame pose used the perturbed
stream; every recorder's *local* reconstruction kept reading the exact `ego.jsonl`: its ego motion compensation of
the radar, its map matching and lane semantics, and the cross-recorder speed checks.  A degraded receiver therefore
still benefited from exact odometry.  Now `pipeline.measured_ego_records` gives the local path the same measured
pose (position, heading, velocity) as the fusion.  G0 is unchanged (bit-identical: the recorded source returns the
recorded stream).  Remaining, documented: height, pitch and roll, and the IMU fields (acceleration, angular rate,
unused by the reconstruction) stay exact under G1/G2: an INS attitude assumed exact.

No odometry or IMU sensor that does not exist in the project is declared as measured: the reconstruction uses
exactly the fields listed above.

## Other checks of the audit

* Nothing in `cdf.reconstruction`, `cdf.robustness` or the reconstruction viewer reads `ground_truth/`, the run
  metadata, the scenario YAML or the simulator (tests `test_reconstruction_boundary.py`, `test_replay_ghosts.py`,
  `test_worked_example.py`: AST checks, poisoned ground truth, forbidden file opens).
* Radar files carry no actor id or label; vehicle-local collision files carry no partner identity.
* Residuals, declared: `collisions.jsonl` keeps CARLA's exact impulse magnitude (an ideal crash sensor; the
  `impulse` family perturbs it); `ego_footprint` is the recorder's own exact box (a vehicle knows its dimensions);
  `frame` / `timestamp` are the simulator's clock, i.e. the recorders' clocks are perfectly synchronised in the raw
  data — the reconstruction does not use that: it aligns recorders from their own observations, and the `clock`
  robustness family shifts the clocks to prove it.

## The two viewers

* **GROUND TRUTH viewer** (`scripts/view_ground_truth.py`, model `cdf.replay.ground_truth`): reads only
  `ground_truth/`.  Every vehicle, recorder or not, on its true trajectory; the physical contact episodes
  (callbacks of one pair less than 0.5 s apart) as COLLISION banners and CONTACT_START / END in the panels.  Clock
  `t_contact`: seconds from the first true vehicle-vehicle contact.
* **RECONSTRUCTION viewer** (`scripts/replay_run.py`): reads only the recorders' files and the reconstruction
  outputs.  Recorders are placed at their **sensor pose** (`ego.jsonl`, the G0 GNSS/INS; a perturbed pose source can
  be passed to `ReplayRun.load(pose_factory=...)`); non-recorders appear only as the fused road users (U1, U2, ...)
  or as radar tracks.  Clock `t_global`: the reconstruction's own clock, anchored on its reference collision.

When the reconstruction aligns the recorders on the first collision (all 22 canonical runs in G0), `t_global` and
`t_contact` coincide, so the same instant can be compared in both viewers.  Known limitation: the CARLA viewer of a
perturbed copy is not opened by the campaign scripts with its pose source, so for G1/G2 inspections the recorders'
drawn pose is the G0 one; the campaign evaluates G1/G2 numerically.
