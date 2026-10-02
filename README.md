# CARLA raw-data acquisition

This repository runs the fixed scenario definitions in `configs/scenarios/`
and records raw CARLA observations. It does not alter scenario physics.

## Install and run

Install Python 3.8+, NumPy, Pillow, OpenCV, and PyYAML, plus the CARLA 0.9.15 Python
API matching the server. Start CARLA on port 2000 (or configure the host and
port in `configs/default.yaml`).

```text
python scripts/run_scenario.py --scenario S01 --variant crash
```

Useful options are `--seed`, `--output`, `--sensor-profile`, and
`--override key=value`. The runner executes one fixed scenario variant and
cleans up its CARLA actors.

## Radar sensor: one logical 360-degree surround radar

Every vehicle carries ONE logical radar, `surround` (`configs/sensors/radar_*.yaml`):
the aggregate coverage of the radars distributed around a car, as a single
sensor centred over the vehicle and above its roof.

| Property | Value |
|----------|-------|
| Mount | x = 0, y = 0, yaw = 0, pitch = 0 (vehicle frame: x forward, y right, origin at the vehicle origin on the ground) |
| Height | 0.30 m above the top of the vehicle's own bounding box: model3 1.78 m, audi.tt 1.69 m, nissan.patrol 2.16 m, mercedes.sprinter 2.87 m |
| Horizontal FOV | 360 deg |
| Vertical FOV | 30 deg (+-15 deg) |
| Points per second | 21600 in total |
| Range | 90 m, radial |
| Tick | 0.05 s (every simulation step) |

CARLA 0.9.15's `sensor.other.radar` cannot cover 180 degrees or more: it
traces its rays inside a cone around its x axis of lateral half-width
`tan(horizontal_fov / 2) * range`, so wider settings fold back. Measured on our
build: 200 -> +-80 deg, 270 -> +-45 deg, 359 -> +-0.5 deg, 360 -> a vertical
slice at 0 deg, 180 -> no return. The surround sensor is therefore six
co-located CARLA radars of 90 deg at yaws 0, 60, ..., 300 deg (15 deg overlap
each side, 3600 points per second each). `RadarSensor` merges them at
recording time: each sweep's azimuths are rotated by the radar's yaw into the
logical frame and wrapped to (-180, 180]; depth and radial velocity lie along
the line of sight and are unchanged. A CARLA radar's range bounds only the
forward component of a ray, so returns beyond 90 m radial are dropped. One
logical frame is written per tick: `vehicles/X/radar/observations.npz` with
`metadata.json` (logical mount, `physical_radars`, `incomplete_frames`,
`queue_drops`). Reconstruction and tracking see only the logical sensor.

Why these values (CARLA tests in an empty map, then on Town05):

- Height: a single absolute height cannot serve the campaign's roofs of
  1.39-2.57 m. At 2.8 m, just above the Sprinter's roof, a model3 sees nothing
  of a car within 2-4 m ahead or behind, or within 4-8 m beside it. At 0.30 m
  above its own roof, a car 0.3 m away is seen in every direction.
- Vertical FOV: from the roof the sensor looks down onto close, lower cars. An
  audi.tt 0.3 m beside a model3 was seen in 0-80 % of the sweeps at +-10 deg,
  depending on the mount height, and in every sweep at +-15 deg. The nearest
  return then lies 0.1-0.7 m from the true surface, ahead, beside or behind.
- Points per second: 10800 (= 6000 x 360/200, the former horizontal density)
  spread over 360 x 30 deg gave a car 25-40 m away 3-4x fewer returns than
  the former 200-degree radar. 21600 restores 0.5-1.3x of them at 25-60 m.
  The engine cost stays at about 12 ms per tick for three vehicles, and no
  callback was lost.

The vehicle's own bounding box is recorded as `ego_footprint` in
`vehicles/X/metadata.json` (vehicle frame). The reconstruction needs it to
turn ranges, measured from the centre, into clearances from the vehicle's skin.

## Stored streams

Each vehicle has independent compact radar and depth streams:

```text
vehicles/A/radar/observations.npz
vehicles/A/radar/metadata.json
vehicles/A/depth/observations.npz
vehicles/A/depth/metadata.json
```

Every NPZ uses the same four float32 columns:
`depth_m`, `azimuth_rad`, `altitude_rad`, `radial_velocity_mps`, with
`frames`, `timestamps`, and `offsets`. Variable-length frame slices are
`detections[offsets[i]:offsets[i+1]]`; no padding or auxiliary association
files are stored. Native radar data outside the comparison region is kept.

The radial-velocity column has a different sign per source, in files and in
the loader:

- Radar stores CARLA's native `RadarDetection.velocity`. CARLA 0.9.15
  documents it as velocity towards the sensor, but the recorded values are the
  range rate: negative while the range shrinks. Static scenery ahead of a
  recorder driving at speed v returns about `-v*cos(azimuth)`.
- Depth stores a closing speed, positive while the range shrinks. It is
  estimated locally from temporally associated compact depth observations:

```text
radial_velocity_mps = (previous_depth_m - current_depth_m) /
                      (current_timestamp - previous_timestamp)
```

For the same approaching object radar is negative and depth positive. Use
`closing_speed(values, source)` from `cdf.recording` (positive = approaching)
before comparing or mixing the two. Metadata says `radial_velocity_sign:
positive_away_from_sensor` with `radial_velocity_definition: carla_range_rate`
for radar, and `positive_towards_sensor` with `closing_speed` for depth. Radar
metadata written before this correction said `positive_towards_sensor`, a label
that was wrong for the stored values; every run now in `traces/` was recorded
after it.

The estimator version is `temporal_geometric_association_v1`. It uses only
depth range, azimuth, altitude, and actual CARLA sensor timestamps. It never
uses radar, ground truth, actor IDs, semantic labels, bounding boxes, or ego
velocity. It uses deterministic gated nearest-neighbour matching, optional
mutual matching, and leaves the velocity as `NaN` for first frames, missing or
out-of-order timestamps, ambiguous/non-mutual matches, invalid ranges, or
impossible velocity jumps. Missing callbacks therefore use their real larger
timestamp delta, not a fixed 0.05 s.

Default gates are configured in `depth_radial_velocity` in
`configs/default.yaml`: `max_dt_s=0.20`, azimuth 6°, altitude 4°,
`max_abs_radial_velocity_mps=60`, 0.50 m range margin, mutual matching, and a
loose 20 m/s velocity-jump check.

The source-agnostic loader is:

```python
from cdf.recording import load_observation_stream
stream = load_observation_stream(vehicle_dir, source="radar", common_region=True)
for observation_frame in stream:
    ranges = observation_frame["detections"][:, 0]
    radial_velocities = observation_frame["detections"][:, 3]
```

Changing only `source="radar"` to `source="depth"` selects the other stream;
the velocity column keeps that source's sign (see above).
`common_region=True` exposes the physical overlap (azimuth -45..45 degrees,
altitude -5..5 degrees, range 0..90 m) without changing native files. There is
no automatic fallback and no radar/depth fusion in this task. Radar and depth
keep their own `sensor_transform` metadata; comparable semantics do not imply
co-located sensors.

Depth images are processed in memory and not persisted. Observations first use
the existing 2° x 2° geometry, then retain one nearest non-ground return per
2° azimuth direction (at most about 45 detections per frame). RGB remains
800x600 at 10 Hz and is converted BGRA-to-RGB transiently; no RGB frame files
are written. The STOP/YIELD colour-and-shape detector tracks detections across
frames and writes one compact `traffic_signs.jsonl` record per confirmed track.
The versioned `scripts/validate_observations.py` exposes timestamp, angular,
range, and sign-deadband tolerances and reports them with every metric.
`scripts/evaluate_radial_oracle.py` is a separate privileged evaluation tool:
it uses ground-truth vehicle poses only offline to compare radar and depth
target-level velocities, both converted to closing speed, with a target-centre
closing-speed oracle. It is never imported by acquisition or the online depth
estimator.
Metric depth decoding is
`1000 * (R + 256*G + 65536*B) / (256**3 - 1)` metres for CARLA BGRA bytes.

When the runner starts CARLA itself, `simulation.gpu: auto` queries
`nvidia-smi` and selects the adapter with the most free VRAM (then lowest
utilisation). Use `simulation.gpu: <index>` to request an adapter explicitly,
or `null` to leave Unreal's default. `scripts/start_carla.py` uses the same
selection path for manual starts.

CARLA runs with `-quality-level=Epic -unattended` (`simulation.quality_level`,
`simulation.unattended`). Low quality is avoided: in CARLA 0.9.15 it crashes
the engine deterministically in some scenarios (S05, S08 and S13 at fixed
ticks), because a camera scene capture renders a vehicle's skeletal mesh after
its mesh object was freed (`EXCEPTION_ACCESS_VIOLATION` in
`FSkeletalMeshSceneProxy::GetMeshElementsConditionallySelectable`, resolved
with the PDB shipped with CARLA). Vehicle physics (ego, controls, collisions)
is bit-identical in both modes. Radar returns and camera images are not:
Low mode removes foliage and changes materials, lights and post-processing, so
Low and Epic recordings must not be mixed in one campaign. `-unattended` makes
a crashed engine exit instead of waiting behind a "Fatal error" dialog.

## Validation

Synthetic estimator tests are in `tests/test_depth_observations.py`. After
acquisition, run the post-acquisition report helper (it never feeds radar into
the estimator):

```text
python scripts/validate_observations.py traces/S01/run_0_crash/vehicles/A --metrics
```

The helper reports finite depth coverage and compatible radar/depth matched
pairs, sign agreement, MAE, median absolute error, and RMSE, comparing both
sources as closing speed. Because radar and
depth sense different surfaces and have different native extrinsics, unmatched
returns and disagreement are expected and must be interpreted as sensing or
association differences rather than hidden with ground truth.

The separate `ground_truth/` trace contains privileged simulator state and is
never part of the vehicle-local estimator input. No generated scenario traces
should be committed.

## Reconstruction: local graphs -> global graph

`src/cdf/reconstruction/` turns the per-vehicle recordings of one run into
local event graphs and then into one global graph:

```text
vehicles/X/*  -> local trace (10 Hz, X's own clock)  -> local graph of X
                 anonymous radar tracks (track_001, ...; Kalman + RTS)
all local graphs -> graph-level alignment (matched COLLISION nodes)
                 -> identity association (track -> recorder, or stays anonymous)
                 -> global graph + global trace
```

```text
python scripts/reconstruct_run.py traces/S01/run_0_crash traces/S02/run_0_crash traces/S03/run_0_crash --evaluate
```

Output goes to `<run>/reconstruction/`: per recorder `local_trace.jsonl`,
`local_tracks.jsonl`, `local_graph.json|md|dot`; under `global/`
`alignment.json`, `associations.json`, `global_trace.jsonl`,
`global_graph.json|md|dot`; a plain-language `report.md`. SVG files are written
only when Graphviz `dot` is installed. `--evaluate` runs afterwards and writes
`reconstruction/evaluation/`.

Rules the code follows:

- A recorder's local reconstruction reads only `vehicles/<X>/` (ego, controls,
  collisions, traffic signs, radar) and the run's supplied
  `incident_context.json`. It never reads `ground_truth/`, the run's
  `metadata.json` (scenario design), other vehicles' files, actor IDs or the
  CARLA `frame` counter (shared by all recorders). External objects are
  anonymous radar tracks.
- The speed limit is supplied incident context, known a priori from the
  incident location: a scenario declares `context: {speed_limit_kmh: N}`, the
  runner copies it to `incident_context.json`, and the reconstruction uses it.
  It is neither perceived nor ground truth and is never inferred from the
  CARLA map. Without it no SPEED_LIMIT_EXCEEDED event can be derived.
- Local time: `t_local = source timestamp - origin`, the origin being the
  recorder's own first ego sample (stored in `local_graph.json`, so the raw
  reading is `origin + t_local`). Local frame: origin and x axis at the
  recorder's first pose, y to its right.
- One COLLISION per contact, from the recorder's own collision sensor, which
  calls back once per sample (0.05 s) while the bodies touch and reports only
  the impulse magnitude. Callbacks without a missing sample between them form
  a burst. A burst after a pause of more than `merge_gap_s` = 0.5 s starts a
  new contact. A burst after a shorter, real break (at least one sample
  without a callback) is judged by its peak relative to the current contact's
  peak:
  - from `new_impact_ratio` = 0.75 it is a new impact;
  - below `min_impact_ratio` = 0.25 it is persistent contact (same contact);
  - in between, the recorder's own velocity jumps decide when both are
    impact-like, one at the contact's start and one at the burst's. An
    impact-like jump is a mean acceleration of at least 20 m/s^2 over the
    samples around the callback, twice what tyres can produce. Directions more
    than 90 deg apart mean struck from the other side (new contact); closer
    ones mean a rebound (same contact), which pushes the same way again.
    Without that evidence, a new contact from `undirected_impact_ratio` = 0.5.

  Measured in CARLA, persistent contact peaks at 0.25 x or less, rebounds of
  the same two bodies at up to 0.43-0.52 x, and a second body at 0.85-0.93 x.
  A contact opened within 0.5 s of the previous one carries `new_contact`
  (`break_s`, `peak_ratio`, `evidence`, `reversal_deg`). In S06
  `a_front_pushed`, B is struck by A and about 0.2 s later meets C: two
  COLLISIONs. A's 0.52 x rebound into B, pushing A backwards again, stays one
  contact, and the hundreds of small callbacks of B's persistent contact with
  C add none.
- No log is synchronised. Two COLLISION nodes of different graphs are the same
  contact when their peak impulses agree (equal and opposite impulses). A match
  also fixes the clock offset between its two graphs, so matches must agree in
  time: one between graphs already linked by other matches must imply the same
  offset within `clock_tolerance_s` = 0.1 s, or it is rejected
  (`rejected_matches`). `alignment.json` stores `t_global = t_local +
  offset_to_global`; the strongest matched contact only defines `t_global = 0`.
  Every matched contact can align a graph: one that shares a contact with an
  aligned graph is aligned through it (multi-hop: A-B by one collision and B-C
  by another put C on the same clock through B; `chain` lists the collisions).
  Local graphs are never modified. Recorders linked to the reference by no
  chain of matched collisions stay `UNALIGNED`.
- A local track is named after another recorder only at fusion. Every matched
  collision of the recorder names a partner; for that contact the track must
  be its recorder's only track that is persistent (tracked at least 1 s before
  the contact), continuous up to the contact (still observed within 0.5 s of
  it: TRACK_LOST at most 1.0 s before), approaching (clearance shrinking over its last second)
  and as fast as the partner says it was (speed RMSE at most 1.5 m/s). The
  1.0 s contact window (`fusion.contact_window_s`) is for association only.
  The tracker still ends a silent track after 0.5 s and reports TRACK_LOST.
  The clearance at the contact is evidence, not a veto: vehicle geometry,
  impact angle and a roof radar's view can keep it above 3.5 m, so beyond that
  it only lowers the confidence. Two or more such tracks for one contact are an ambiguity, a
  track compatible with two partners a conflict: both stay anonymous
  (`A:track_001`); every reason, and the collision the decision rests on, is
  in `associations.json`. Ground truth is never used.
- Radar detection velocity is used as stored: the range rate (negative while
  the range shrinks), whatever label older radar metadata carries.
- Geometry of the centred radar. A range is measured from the radar, at the
  vehicle centre, not from the vehicle's skin. With the recorded footprint
  (bounding box, half-length L/2 and half-width W/2 around the radar), every
  return and track also gets a clearance:

  ```text
  ego_extent(theta) = min((L/2) / |cos(theta)|, (W/2) / |sin(theta)|)   (a zero cosine or sine leaves the other side)
  clearance_m       = max(0, planar_range_m - ego_extent(theta))
  ```

  This is the free distance from the vehicle's edge to the observed surface
  along the bearing theta; the code takes the exit of the ray from the
  rectangle, which also covers an off-centre radar. A track's clearance
  belongs to its near surface. Its returns spread over the target's visible
  body, which from a roof is often the roof and rear window, so the tracked
  median point lies deeper than the bumper that touches first. Per sweep the
  near surface is the 10th percentile of the returns' clearances; its depth
  behind the median point is smoothed over five sweeps. The raw `range_m`
  stays in TRACK_STATE.
  - TTC is `clearance / closing speed`, and CRITICAL_TTC works on the
    clearance.
  - EGO_PATH and CUT_IN count a target as "ahead" when it is beyond the
    vehicle's front edge (`ahead_of_front_m`), not merely ahead of the radar.
  - Identity association uses the clearance for the approach trend and at the
    contact.
  - The closest point of approach (relative position and velocity) is
    unchanged, plus `d_cpa_clearance_m`.
  - Returns from inside the footprint come from the vehicle's own body and are
    dropped (`own_body_returns_dropped`).
- Ego motion: the radar's own velocity is its displacement over the last
  sweep, computed from the recorder's own poses (position, heading, pitch,
  roll), because CARLA's radar measures its own motion the same way. This
  includes the rotation about the vehicle origin and the roof's swing when the
  vehicle pitches or rolls. Static scenery therefore stays static in turns,
  under braking and through an impact. The instantaneous vehicle velocity
  differs by up to about 3 m/s at an impact: with it, 2.2 % of S05 B's static
  returns looked like moving targets after the crash. Doppler speeds are
  projected onto the horizontal plane, because a roof radar sees close targets
  from above. Points are clustered in the local Cartesian frame, so an azimuth
  crossing +-180 deg splits nothing.

Three levels are kept apart. Raw and track data feed the 10 Hz FACTS of
`local_trace.jsonl` (EGO_MOTION, EGO_CONTROL with the raw brake, throttle and
steer, TRACK_STATE: ranges, TTC, the track's own velocity `vx_mps`/`vy_mps`,
its Kalman uncertainty, its motion relative to the recorder, the closest point
of approach `t_cpa_s`/`d_cpa_m`, a qualitative `motion_relation`, and the
braking need behind CRITICAL_TTC: `ego_speed_mps`,
`target_longitudinal_speed_mps`, `closing_speed_mps`, `ttc_s`,
`speed_to_shed_mps`, `critical_ttc_threshold_s`, `required_deceleration_mps2`,
`braking_margin_mps2`, `unavoidable_by_braking`). The graph holds only semantic
EVENTS, which are state transitions without telemetry:

| Events | Meaning |
|--------|---------|
| BRAKE_START / BRAKE_END | brake at or above 0.1; releases shorter than 0.2 s do not split it |
| TURN_LEFT / TURN_RIGHT_START / _END | the recorder's own yaw motion from its unwrapped heading: yaw rate at least 10 deg/s while moving, ends below 5 deg/s (0.3 s debounce), at least 0.5 s and 15 deg |
| MOVING_START / _END, STOP_START / _END | stop below 0.3 m/s, moving again above 1 m/s |
| SPEED_LIMIT_EXCEEDED_START / _END | above limit + 1 km/h, back at or below limit - 1 km/h (nested inside MOVING) |
| TRACK_APPEARED_FRONT / _REAR / _LEFT / _RIGHT, TRACK_LOST | lifetime of an anonymous radar track; the appearance names where the track entered the 360-degree radar field: its azimuth at the first detection within 5 deg of the recorder's heading (FRONT) or of the opposite direction (REAR), else its sign (negative = LEFT) |
| CLOSING_START / _END | closing at 1 m/s or more; ends below 0.5 m/s |
| CRITICAL_TTC_START / _END | while closing, avoiding the target by braking would need at least the available deceleration (below); ends below 75 % of it, at the latest with CLOSING |
| EGO_PATH_ENTRY / EXIT | track enters / clearly leaves the straight-ahead 1.5 m corridor beyond the recorder's front edge (not a lane change) |
| CUT_IN_FROM_LEFT / _RIGHT_START / _END | a car ahead, moving within 25 deg of the recorder's heading, closes on the corridor from that side (see below); ends when the lateral motion settles |
| STOP_SIGN_DETECTED_START / _END, YIELD_... | camera sign track confirmed / last detected |
| COLLISION | one per contact (see the segmentation rule above); keeps its peak impulse for alignment |

A START at the first observation (recording start, or a track's first sample)
carries `active_at_first_observation`; an EGO_PATH_ENTRY that was never seen is
not invented; a state still active when observation ends has no END. A sign
END means this recorder stopped detecting the sign, not that its obligation
ended; `checks.sign_windows` lists the STOP_START events inside each window.

CRITICAL_TTC comes from a braking-avoidability margin, not from a fixed TTC.
The TTC itself stays physical and local: `TTC = clearance / closing_speed`, the
closing speed along the line of sight from the recorder's own odometry and the
track's estimated velocity (never ground truth, never another recorder's log).
To avoid the target by braking the recorder must lose

```text
v_shed = v_ego - min(max(v_target_long, 0), v_ego)
a_req  = v_shed^2 / (2 * (v_shed * (TTC - t_r) - d0))      (infinite if the bracket <= 0)
critical  <=>  closing >= 1 m/s  and  a_req >= a
          <=>  TTC <= critical_ttc_threshold_s = t_r + v_shed / (2 a) + d0 / v_shed
```

where `v_target_long` is the target's speed along the recorder's heading (down
to it for a car ahead in the same direction; to a standstill for a standing,
crossing or oncoming target). `t_r = 1.0 s` (reaction time; driver brake
reaction times of roughly 0.7-1.5 s are reported), `a = 6 m/s^2` (hard,
non-emergency braking on a dry road; emergency braking reaches about 8-10) and
`d0 = 1 m` are global assumptions in `configs/reconstruction.yaml`, not a norm:
test protocols use fixed TTC values (Euro NCAP CCFhol 1.5 s, UNECE R152 AEBS
tests from TTC >= 4 s), and no single speed-dependent legal threshold exists.
The threshold therefore grows with the speed to shed: a target at the
recorder's own speed is never critical, a standing target is critical earlier
for a fast recorder. The state ends once `a_req` falls below 75 % of `a`
(hysteresis, 0.2 s debounce) and at the latest with CLOSING.
Limitation: TTC ignores the lateral offset, so oncoming traffic in the next
lane can be briefly critical.

TURN_LEFT / TURN_RIGHT describe the motion the recorder really performed, from
its own odometry (`ego.jsonl`): the unwrapped heading, its rate over the
preceding 0.2 s (so a spin that starts at an impact is never reported before
it), a minimum speed of 1 m/s, hysteresis (10 / 5 deg/s), a 0.3 s debounce, at
least 0.5 s and 15 deg of heading change counted from the turn's onset (lane
changes stay below about 10 deg). In CARLA the yaw grows clockwise seen from
above, so a left turn has a negative yaw rate; this was checked on the
recordings, where the yaw change, the side the vehicle moved to and the steer
sign agree in every driven turn. The steer command itself stays a fact. A
spin after an impact is real yaw motion and is reported as a turn.

Temporal safety relations (`checks.temporal_safety_relations`, also in
`global_graph.json`, `global_graph.md` and `report.md`) state, per track, in the
recorder's own clock: whether a CUT_IN started before the critical TTC
(`CUT_IN_* < CRITICAL_TTC_START < COLLISION` when all three hold) or the
critical TTC was already active at the cut-in (`CRITICAL_TTC_START <=
CUT_IN_*_START`), whether EGO_PATH_ENTRY came before or after the critical TTC,
and the deltas in seconds. A recorder can collide more than once: the
COLLISION is its first one at or after the track's critical TTC start (without
one, after the cut-in or path entry), and in the global graph, once the track
is identified, its first such collision with that entity (`collision_with`).
They are temporal properties only, not causes.

The appearance side is local evidence only: the track's own azimuth from the
radar at its first detection (`track_appeared_front_deg`,
`track_appeared_rear_deg`), never ground truth. A lead car in the recorder's
lane appears FRONT, a follower in its lane REAR (the 360-degree radar sees
behind), and crossing traffic emerging on the right appears RIGHT. A target
present from the start appears where it was first seen.

CUT_IN is a kinematic observation, not a normative judgement. The closest point
of approach of the relative motion stays a quantitative fact (`t_CPA =
-(r.v)/|v|^2`, `d_CPA = |r + v t_CPA|` in TRACK_STATE); no event is derived
from it. A CUT_IN needs a car ahead moving roughly in the recorder's
direction (so crossing traffic is never a cut-in) that approaches the corridor
laterally at 0.3 m/s or more for 0.5 s, starting at least 0.5 m outside it,
having closed 0.5 m, and due to reach it within 3 s. The side is the
recorder's own view (negative lateral = left). It ENDS when the lateral
approach stays below 0.2 m/s for 0.3 s; a COLLISION does not end it, and a lost
track leaves it UNKNOWN. Thresholds are global (`configs/reconstruction.yaml`),
never per scenario. Limitation: the corridor is straight ahead, so on a curved
road an adjacent-lane car could look like a cut-in. A track estimate with
position std above 1 m or velocity std above 1 m/s supports no cut-in claim.

Every event node carries `perceived_state_before`: the recorder's own semantic
state just BEFORE the event, built only from its own evidence
(`world_state.py`). Events at one timestamp are simultaneous and share an
identical state; their transitions are applied together, after it. Each
`local_trace.jsonl` frame holds the state at that frame (after its
transitions):

```text
ego:      MOVING, STOP, BRAKE, TURN_LEFT, TURN_RIGHT, SPEED_LIMIT_EXCEEDED
external: track_NNN -> CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT, CUT_IN_FROM_RIGHT
signs:    sign-N    -> class, known, relevant_to_ego_path
```

Values are true, false or "UNKNOWN". UNKNOWN means the recorder cannot tell:
before its first sample, without a supplied speed limit, while a track
estimate is too uncertain, and for every state of a track after TRACK_LOST.
There is no separate visibility state: a track is in the state from its
TRACK_APPEARED_* on, TRACK_LOST turns all its states UNKNOWN (a loss never
invents an END), and the sign detection windows say when a sign is in view. A
sign stays `known` from its first detection: nothing admissible tells when its
controlled point has been passed, so knowledge is not cleared. Names stay local
(`track_001`, `sign-0`): global identities never enter a local state. The
global graph keeps, per node, the belief of each observing recorder, unrenamed.
The Markdown files render it compactly, once per timestamp.

Sign continuity: the camera tracker drops a sign after 0.6 s without a
detection. A new track of the same class that starts within 5 s at the same
image place (best-detection centres within 15 px, sizes within 25 %) while the
recorder stood still (speed at most 0.5 m/s, turn at most 3 deg) is the same
sign reacquired: its windows keep the first id, with `reacquired` and its own
`sign_track` id as attributes. Nothing else merges signs (no map or actor
identity).
LANE_DEPARTURE_START/_END and LEFT/RIGHT_TURN_SIGNAL_START/_END are reserved
names: the recordings contain no lane or indicator evidence, so nothing emits
them.

Graph edges are PRECEDES, which links an event to every event at the next
later time (events with equal times are simultaneous, their order unresolved),
and SAME_TRACK, which links a track's TRACK_APPEARED_* to every other event whose
subject is the same local track. SAME_TRACK is exactly "same subject_id" made
explicit for graph queries: it groups events and implies no order.
Adding a state means computing its active intervals in `local.py`.
Parameters are in `configs/reconstruction.yaml`.

`src/cdf/evaluation/reconstruction.py` is the only code that reads
`ground_truth/`; it compares the written files with the simulator state
(each true contact against the COLLISION node of the same pair reported
closest to it, extra COLLISION nodes, every recorder's clock whatever chain
aligned it, identity decisions, track accuracy)
and reruns alignment with one recorder's clock shifted by 0.73 s to check that
the global graph does not change. Tests: `python -m pytest tests`.

`scripts/audit_radar_visibility.py` is a PRIVILEGED evaluation and debugging
tool, never imported by the reconstruction. It reads `ground_truth/` (true
poses and boxes) to explain radar coverage: per recorder and other vehicle, the
first sweep in range, inside the field of view, with a raw return, with a
usable return (passing the tracker's own filters), the track's birth and
confirmation, and its loss; it classifies a late first track as FOV,
OCCLUSION (vehicle or static scenery), RAW_SENSOR, FILTER or TRACKER.

```text
python scripts/audit_radar_visibility.py traces/S15/run_0_single_impact --json audit.json
```

## Interactive incident replay

```
python scripts/replay_run.py traces/S01/run_0_crash
python scripts/replay_run.py traces/S01/run_0_crash --speed 0.25 --start 0.45 --paused --follow A
```

This is an offline visualization of recorded trajectories. It does not rerun
scenario physics and does not participate in reconstruction: every rendered
frame, each vehicle's `vehicles/<id>/ego.jsonl` pose is interpolated at the
playback time (position linearly, angles the short way round) and applied to a
physics-less CARLA actor, so 0.25x, 0.5x (default), 1x and 2x all show exactly
the recorded trajectories. The replay timeline is the recorded simulator time
(0 s = the earliest ego sample); reconstructed events are placed on it through
each local graph's own clock origin, for display only (this is not the
graph-level alignment). The viewer only reads the run: `ego.jsonl`, the
recorded blueprint in `vehicles/<id>/metadata.json`, and, when present,
`reconstruction/<id>/local_graph.json`, `local_tracks.jsonl`, `local_trace.jsonl` and
`reconstruction/global/` (COLLISION participants, track identities). The map
comes from the scenario configuration of the run's `scenario_id`/`variant`;
`ground_truth/` is never read.

| Key | Action |
|-----|--------|
| SPACE | play / pause |
| R | restart |
| LEFT / RIGHT | seek -/+0.5 s (SHIFT: 0.05 s, one recorded sample) |
| N / P | jump to the next / previous reconstructed event (pauses) |
| 1 / 2 / 3 / 4 | 0.25x / 0.5x / 1.0x / 2.0x |
| C | camera: overview, follow selected vehicle, free |
| TAB | next vehicle (follow camera) |
| T | hide / show the perceived-track markers of every recorder (`--hide-tracks` starts hidden) |
| H | hide / show the key help |
| ESC | exit |

Mouse: drag to orbit (overview/follow) or look (free camera), wheel to zoom;
click the timeline to seek. Free camera: W/A/S/D/Q/E move, SHIFT faster.
Each vehicle has a letter badge above its roof and a panel on the right with
its recorded speed, its perceived state as the reconstruction wrote it in
`local_trace.jsonl` (its tracks with CLOSING, CRITICAL_TTC, IN_EGO_PATH,
CUT_IN..., lost tracks greyed with their states UNKNOWN, known signs; older
outputs without it show the open START..END pairs) and the events of the last
second, such as TRACK_APPEARED_LEFT. A reconstructed COLLISION shows its
participants from the global graph. What each recorder perceives is drawn in
the scene: for every track it is tracking, a dot in the recorder's colour at
the track's estimated position, labelled with the local id (`track_001`); a
lost track's dot disappears. Dots are drawn at road height because tracks are
planar.

The viewer starts CARLA if none is running (`--no-autostart` to only connect)
and stops a server it started on exit (`--keep-server` to leave it running).
It renders through its own camera into a pygame window, runs the world in
synchronous mode while open, and on exit destroys its actors and restores the
world settings.
