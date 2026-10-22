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
* Radar files carry no actor id or label.  Vehicle-local collision files carry no partner identity: in the 22
  canonical runs every record is exactly `{frame, timestamp, impulse}`.  Every `ego.jsonl` carries exactly the
  fields its `pose_sensor` declares, plus `frame`.  Both checks are in `test_sensor_ground_truth_separation.py`.
* Residuals, declared:
  * `collisions.jsonl` keeps CARLA's exact impulse magnitude, i.e. an ideal crash sensor.  The `impulse`
    robustness family perturbs it.
  * `ego_footprint` is the recorder's own exact box: a vehicle knows its dimensions.
  * `vehicles/<R>/metadata.json` also holds `vehicle_transform`, the exact spawn pose of R from the scenario.  No
    code of the reconstruction or of the RECONSTRUCTION viewer reads it, and a boundary test forbids the key there.
    Moving it out of the recorder's files would need a re-acquisition, because the raw files are never edited.
  * `frame` / `timestamp` are the simulator's clock, so the recorders' clocks are perfectly synchronised in the raw
    data.  The reconstruction does not use that:
    * it aligns the recorders from their own observations, and the `clock` robustness family shifts the clocks to
      prove it;
    * the frame counter is ignored: a synthetic run with every `frame` value scrambled, in the JSONL streams and in
      the radar files, gives the same global graph (`test_the_reconstruction_ignores_the_simulator_frame_counter`).
      The comparison does detect a change: tripling one recorder's collision impulses, which the matching uses,
      changes the graph.

## The two viewers

* **GROUND TRUTH viewer** (`scripts/view_ground_truth.py`, model `cdf.replay.ground_truth`): reads only
  `ground_truth/`.  Every vehicle, recorder or not, on its true trajectory; the physical contact episodes
  (callbacks of one pair less than 0.5 s apart) as COLLISION banners and CONTACT_START / END in the panels.  Clock
  `t_contact`: seconds from the first true vehicle-vehicle contact.
* **RECONSTRUCTION viewer** (`scripts/replay_run.py`): reads only the recorders' files and the reconstruction
  outputs.
  * **Recorders.**  They are placed at **the pose the reconstruction used**:
    * in G0 that pose is the recorded synthetic GNSS/INS stream itself (`ego.jsonl`);
    * when it is not, because the GNSS/INS was perturbed or the fusion refined the poses, the reconstruction writes
      the poses it used to `reconstruction/global/recorder_poses.json` and the viewer draws those (tests
      `test_recorder_pose_output.py`).  In G0 the file is not written and every other output stays unchanged.
  * **Non-recorders.**  They appear only as the fused road users (U1, U2, ...) or as radar tracks.
  * **Clock.**  `t_global`, the reconstruction's own clock, anchored on its reference collision.

**Side by side.**  When the two viewers are opened together (`docs/REPLAY.md`), each runs on its own CARLA server.
* **What crosses.**  The GROUND TRUTH viewer sends only the instant it shows on the recording clock, its play state
  and its speed (`cdf.replay.sync`).
* **The follower's mapping.**  The RECONSTRUCTION viewer maps that instant through its own alignment and the
  recorders' timestamps.  No ground-truth position, identity, event or file reaches it.
* **The one assumption.**  The recorders' clock equals the simulator's, which is true in the canonical runs; the
  `clock` robustness family shifts it.

The two clocks are defined independently:
* `t_contact` = 0 at the first true vehicle-vehicle contact;
* `t_global` = 0 at the reconstruction's reference collision, its strongest matched contact.

In 21 of the 22 canonical runs these are the same instant.  In S04 `b_rear_first` the strongest contact (A-B) comes
1.55 s after the first one (B-C), so `t_contact` = `t_global` + 1.55 s there.  The review menu prints this offset
for every run where it is not zero.  To inspect a degraded condition, run its
job with `scripts/robustness.py --keep` and open the kept copy in the RECONSTRUCTION viewer.
