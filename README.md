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

## Radar sensors: three radars on the body (front, left, right)

Every vehicle carries three CARLA radars on its own body (`configs/sensors/radar_baseline.yaml`),
placed from its own bounding box when spawned (`RadarSpec.mount_transform`):

| Radar | Mount (vehicle frame: x forward, y right, origin at the vehicle origin on the ground) | Yaw | Horizontal FOV |
|-------|------|-----|----------------|
| `front` | centre of the front face, 0.05 m beyond the box (x_max + 0.05, y = box centre) | 0 | 150 deg |
| `left` | middle of the left side, 0.05 m beyond the box (x = box centre, y_min - 0.05) | -90 | 140 deg |
| `right` | mirrored | +90 | 140 deg |

All three: vertical FOV 20 deg, range 90 m (radial), 12000 points per second, tick 0.05 s,
0.6 m above the road.  There is no rear radar: directly behind the vehicle lies a blind zone
(measured: a car within +-12 deg at 5 m and +-16 deg from 10 to 40 m is not seen; for a point
target the cone is 41-53 deg wide from 10 m on).  The front radar and a side radar overlap
from about 25 to 60-70 deg each side, so a target passing from the front to the side stays
one track.  The radars never see their own vehicle.

CARLA 0.9.15's `sensor.other.radar` cannot cover 180 degrees or more: it traces its rays in a
cone around its x axis of lateral half-width `tan(horizontal_fov / 2) * range`, so wider
settings fold back (measured: 200 -> +-80 deg, 360 -> a vertical slice).  A radar's range
bounds only the forward component of a ray, so returns beyond 90 m radial are dropped.  Each
radar is recorded as its own stream, `vehicles/X/radar/<front|left|right>/`, with its
resolved mount in its `metadata.json` (`sensor_transform`).  The reconstruction places every
return from its own radar's mount.

Why these values (private CARLA engine, Town05 and an empty map; car targets at 10 / 25 / 40 /
60 m, returns per sweep straight ahead 76 / 19 / 11 / 7, at the side 112 / 42 / 24 / 16):
150 / 140 deg keep the rear blind zone at about 30 deg for cars without a front / side gap;
a 20 deg vertical FOV keeps 1.5-2x more returns on cars at 40-60 m than 10 deg while 30 deg
adds mostly road; at 0.6 m the radar does not look over a car (a car hidden behind another car
returns nothing: only a taller van shows above it).

The vehicle's own bounding box is recorded as `ego_footprint` in `vehicles/X/metadata.json`
(vehicle frame): the reconstruction measures clearances from the vehicle's skin.

## Camera

One RGB camera per vehicle, 1280x720, 110 deg, 10 Hz, behind the windscreen at its top centre
in front of the interior mirror, per blueprint (`sensors.camera.mounts`: model3 x 0.50 / z
1.30, audi.tt 0.40 / 1.18, nissan.patrol 0.60 / 1.62, mercedes.sprinter 1.80 / 2.10; checked
visually so that no body part enters the image above the dashboard).  110 deg is the smallest
FOV that keeps a roadside STOP plate in view until the stop line (at 100 deg it left the image
0.4-0.7 m earlier; at 120 deg it was smaller and detected later).  Images are converted in
memory and never written; the STOP / YIELD detector runs on board (below).

## Recording start and post-impact behaviour

- Launch.  A moving vehicle is spawned `launch_ticks x dt x its speed` (0.6 s) back along its
  lane and launched over 12 ticks at its scripted initial velocity, in the gear its automatic
  gearbox would hold at that speed and at a nominal cruising throttle (0.5); its speed
  controller then starts from that throttle.  The recording starts with the vehicle at its
  scenario spawn point, cruising (|acceleration| <= 0.45 m/s^2 in the first second, every
  blueprint).  Without it CARLA engaged first gear at speed after the recording had started:
  10-20 m/s^2 of engine braking under full throttle for about 0.5 s, which looked like a
  braking target.
- `post_impact_mode: coast`: no pedals, no steering, gearbox in neutral, the brake held once
  the vehicle has come to rest.  With the clutch engaged CARLA's zero-throttle engine braking
  decelerates a car at 4-7 m/s^2, several times what a real car loses rolling off the pedals.
  `stop` (the default) brakes hard; `deflect` coasts and steers the vehicle off its line by a
  scripted offset (S15 only); `drive` keeps following the route.
- CARLA physics to keep in mind: a stationary braked vehicle that is struck does not move (it
  stops the striking car dead), so a chain push needs the struck car still rolling; a rear
  impact on a corner turns the struck car by a few degrees at most, a forward shunt carries it.

## Participants that do not record; reactive actions

- `record: false` on a participant makes it a physical vehicle that is not a recorder: it is
  spawned, drives its script, is seen by the others' radars and cameras and is in
  `ground_truth/` (states, controls, collisions; `ground_truth/metadata.json` lists every
  participant with its `record` flag), but it carries no sensor and writes nothing under
  `vehicles/`.  The run's `metadata.json` lists the recorders only.  The reconstruction can
  therefore know it only as an anonymous radar track of a recorder.
- A scripted action may have a `trigger` instead of a `t_start`: it stays armed until a
  condition on the simulator's true state holds (within `window_s`), then starts `reaction_s`
  later.  Kinds: `envelope_entry`, the target participant's box enters a corridor `ahead_m` long
  ahead of the owner's front face, as wide as the owner plus `lateral_margin_m` a side;
  `corridor_clearance`, the target's box is inside that corridor (any length) within
  `clearance_m` of the owner's front face, measured exactly box to box on the part inside the
  corridor (a close cut-in; the firing record carries the measured clearance).  This is
  scenario construction with privileged information: firings go to
  `ground_truth/triggers.jsonl` only, never to `vehicles/`.  A trigger whose target is not in
  the run never fires.
- Privileged counterfactuals of a scenario (into a scratch `--output`, never into the campaign):
  `--without-participant C` removes a participant, `--disable-action <action_id>` never plays an
  action.

```text
python scripts/run_scenario.py --scenario S17 --variant crash --output <scratch> --without-participant C
python scripts/run_scenario.py --scenario S17 --variant crash --output <scratch> --disable-action A_evasive_swerve_left
```

S17 `unobserved_causal_vehicle` (crash) uses both.  Three lanes, one direction: A (audi.tt,
12 m/s) in the middle lane, B (nissan.patrol, 13 m/s) in the left lane 7 m behind and catching
up, C (model3, `record: false`) in the right lane 10 m ahead of A and 1 m/s slower.  At 2.0 s C
cuts into A's lane without braking (lane shift -3.5 m over 1.0 s, its left side in A's lane at
2.85 s); at 3.30 s C's box is inside A's corridor 2.3 m ahead box to box (`corridor_clearance`,
3 m) and after a 0.35 s reaction A swerves left (lane shift -3.5 m over 1.0 s; 2.0 m of
clearance when it starts) into B: A-B collision at 4.95 s (peak impulse 1577 N*s).  C touches
nobody (closest 0.59 m to A, 3.1 m to B) and speeds up to 16 m/s from 7.0 s.  Without C A
never swerves and A and B never touch (closest 1.5 m); with C but the swerve disabled A runs
into the back of C at 5.95 s and never touches B: `ground_truth/counterfactuals.json`,
privileged.  In the reconstruction C is `A:track_001` (anonymous; CLOSING; CRITICAL_TTC from
2.60 s for an unsafe forward gap, 3.3 m ahead of A where 16.8 m are needed; CUT_IN_FROM_RIGHT
from 2.75 s; EGO_PATH_ENTRY at 3.35 s; all before the collision) and, separately, `B:track_002`
and `B:track_003` (B, two lanes away and seeing C past A, observes no cut-in); no entity C
exists.  Research question: how does partial observability of a
causally relevant but non-colliding road user affect accident explanation and attribution?

## Stored streams

Each vehicle has independent compact streams, one per radar and one for depth:

```text
vehicles/A/radar/front/observations.npz    (and left/, right/)
vehicles/A/radar/front/metadata.json
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
the velocity column keeps that source's sign (see above).  With several radars
`load_observation_stream(..., source="radar", sensor_id="front")` picks one and
`load_radar_observations(vehicle_dir)` returns them all.
`common_region=True` exposes the physical overlap (azimuth -45..45 degrees,
altitude -5..5 degrees, range 0..90 m) without changing native files; the
radar/depth comparison of `scripts/validate_observations.py` uses the front radar. There is
no automatic fallback and no radar/depth fusion in this task. Radar and depth
keep their own `sensor_transform` metadata; comparable semantics do not imply
co-located sensors.

Depth images are processed in memory and not persisted. Observations first use
the existing 2° x 2° geometry, then retain one nearest non-ground return per
2° azimuth direction (at most about 45 detections per frame). RGB (section
Camera) is converted BGRA-to-RGB transiently; no RGB frame files are written.
The STOP/YIELD detector (`src/cdf/perception/traffic_signs.py`) looks for red
regions (HSV), keeps external contours that do not touch the image border, and
classifies their polygon: STOP is a compact regular octagon (compactness >= 0.85,
>= 6 vertices, aspect 0.70-1.15, red fraction 0.55-0.88) with white letters
(>= 0.30 of its inner area), not in the lower part of the image; YIELD is an
inverted triangle (3-4 vertices, box fill 0.38-0.62, solidity >= 0.8, white
interior >= 0.30, top edge >= 1.6 x the bottom).  Detections are tracked across
frames (centre gap <= 8 % of the image width, size ratio <= 1.8, stable aspect),
confirmed after 3, and a track is relevant to the path when the sign came within
30 deg of the camera axis and grew.  One compact `traffic_signs.jsonl` record per
confirmed track; no CARLA label, actor id or map lookup is used (all parameters
in `traffic_signs` of `configs/default.yaml`).
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
ticks; S05 and S13 are no longer in the campaign), because a camera scene capture renders a vehicle's skeletal mesh after
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
  - weaker than `min_new_impact_impulse` = 1000 N*s it continues the contact
    whatever its ratio (bodies scraping or pushing along each other);
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
  (`break_s`, `peak_ratio`, `evidence`, `reversal_deg`); a contact that
  absorbed later bursts lists them (`merged_bursts`: local time, peak).  In S06
  `a_front_pushed`, B is struck by A (4.80 s) and pushed into C (5.30 s): two
  COLLISIONs of B.  A strikes B again 0.15 s after B's impact on C: B's sensor
  merges that burst into its contact with C (0.17 of its peak), A reports it as
  its second contact.
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
  chain of matched collisions stay `UNALIGNED`.  A report left unmatched is
  then compared with the bursts that other recorders merged into their
  contacts (`merged_bursts`): the same impulse, between graphs already linked,
  at their clock offset, is the same contact (`merged_burst_of`).  It fixes no
  clock.  S06 `a_front_pushed` thus has its three contacts A-B, B-C, A-B.
- A local track is named after another recorder only at fusion. Every matched
  collision of the recorder names a partner; for that contact the track must
  be its recorder's only track that is persistent (tracked at least 1 s before
  the contact), continuous up to the contact (still observed within 0.5 s of
  it: TRACK_LOST at most 1.0 s before), approaching (clearance shrinking over its last second)
  and as fast as the partner says it was (speed RMSE at most 1.5 m/s). The
  1.0 s contact window (`fusion.contact_window_s`) is for association only.
  The tracker still ends a silent track after 0.5 s and reports TRACK_LOST.
  The clearance at the contact is evidence, not a veto: vehicle geometry and
  impact angle can keep it above 3.5 m, so beyond that it only lowers the
  confidence. Two or more such tracks for one contact are an ambiguity, unless
  exactly one of them touches the recorder at the contact (observed within one
  sample of it, within `touching_clearance_m` = 1.0 m) while every rival is at
  least `rival_clearance_m` = 2.0 m away (a long van seen as two tracks); a
  track compatible with two partners is a conflict: such tracks stay anonymous
  (`A:track_001`); every reason, and the collision the decision rests on, is
  in `associations.json`. Ground truth is never used.
- Radar detection velocity is used as stored: the range rate (negative while
  the range shrinks), whatever label older radar metadata carries.
- Geometry of the body radars.  Every return is placed from the position of
  the radar that produced it, along that radar's line of sight (mount from its
  metadata).  `range_m` stays the raw range from the observing radar.  With the
  recorded footprint (the vehicle's bounding box) every return and track also
  gets a clearance: the distance from the vehicle's rectangle to the observed
  surface point (0 inside).  A track's clearance belongs to its near surface:
  its returns spread over the target's visible body, so the tracked median
  point lies deeper than the bumper that touches first.  Per sweep the near
  surface is the 10th percentile of the returns' clearances; its depth behind
  the median point is smoothed over five sweeps.
  - CRITICAL_TTC predicts the recorder's footprint and the target's near
    surface (below); `closing_ttc_s = clearance / closing speed` stays a fact.
  - EGO_PATH and CUT_IN count a target as "ahead" when it is beyond the
    vehicle's front edge (`ahead_of_front_m`).
  - Identity association uses the clearance for the approach trend and at the
    contact.
  - The closest point of approach (relative position and velocity) is kept,
    plus `d_cpa_clearance_m`.
  - Returns from inside the footprint are the vehicle's own body and are
    dropped (`own_body_returns_dropped`; zero with the body mounts).
- Ego motion: each radar's own velocity is the displacement of ITS mount over
  the last sweep, from the recorder's own poses (position, heading, pitch,
  roll), because CARLA's radar measures its own motion the same way.  This
  includes the lever arm of a turning vehicle (a front radar 2.5 m ahead of the
  origin moves 0.87 m/s sideways at 20 deg/s) and the swing of the mount when
  the vehicle pitches or rolls.  Static scenery therefore stays static in turns,
  under braking and through an impact (tests/test_three_radars.py).  Doppler
  speeds are projected onto the horizontal plane.  The Kalman filter takes one
  Doppler row per radar that saw the track in a sweep, each along its own line
  of sight.
- A target that stops abruptly (it crashes: tens of m/s^2) changes its Doppler
  speed beyond the gate within one sweep.  A confirmed track whose previous
  sweep was free of foreign returns may then take at least
  `min_slowdown_returns` = 3 returns around it whose speed lies between
  standstill and the predicted one, and follows its target through the crash.
  A road crest or a guardrail next to a target is foreign clutter in every
  sweep and never qualifies.
- The target's acceleration (central difference of the smoothed velocity over
  +-0.15 s) is bounded by what the forward-filtered track shows up to that
  instant: the smoother would otherwise announce an abrupt stop up to 0.2 s
  before it happens.

Three levels are kept apart. Raw and track data feed the 10 Hz FACTS of
`local_trace.jsonl` (EGO_MOTION, EGO_CONTROL with the raw brake, throttle and
steer, TRACK_STATE: ranges, TTC, the track's own velocity `vx_mps`/`vy_mps`,
its Kalman uncertainty, the observing radar, its acceleration, its motion
relative to the recorder, the closest point of approach `t_cpa_s`/`d_cpa_m`/
`d_cpa_clearance_m`, a qualitative `motion_relation`, and the conflict
assessment behind CRITICAL_TTC: `ego_speed_mps`, `encounter`,
`collision_course`, `ttc_s` (first predicted overlap), `predicted_overlap_s`,
`target_acceleration_used_mps2`, `required_deceleration_mps2`, `avoidance_by`,
`braking_margin_mps2`, `unavoidable_by_braking`, `estimate_known`, `critical`,
`critical_reason`, and the safe-following-distance check: `forward_region`,
`forward_leader`, `longitudinal_clearance_m`, `lateral_body_gap_m`,
`time_headway_s`, `minimum_time_gap_s`, `required_safe_distance_m`,
`safe_distance_margin_m`, `line_of_sight_occluded`).  These conflict-model
outputs never reach the forensic packet given to an LLM.
The graph holds only semantic EVENTS, which are state transitions without
telemetry:

| Events | Meaning |
|--------|---------|
| BRAKE_START / BRAKE_END | brake at or above 0.1; releases shorter than 0.2 s do not split it |
| THROTTLE_START / THROTTLE_END | accelerator at or above 0.10, released at or below 0.05 (hysteresis); a release shorter than 0.2 s does not end it; the raw pedal stays a fact |
| TURN_LEFT / TURN_RIGHT_START / _END | the recorder's own yaw motion from its unwrapped heading: yaw rate at least 10 deg/s while moving, ends below 5 deg/s (0.3 s debounce), at least 0.5 s and 15 deg |
| MOVING_START / _END, STOP_START / _END | stop below 0.3 m/s, moving again above 1 m/s |
| SPEED_LIMIT_EXCEEDED_START / _END | above limit + 1 km/h, back at or below limit - 1 km/h (nested inside MOVING) |
| TRACK_APPEARED_FRONT / _LEFT / _RIGHT, TRACK_LOST | lifetime of an anonymous radar track; the appearance names where the track entered the radars' field: its bearing at the first detection within 5 deg of the recorder's heading (FRONT), else its side (negative = LEFT; a car closing in from behind appears on a side, out of the rear blind zone) |
| CLOSING_START / _END | closing at 1 m/s or more; ends below 0.5 m/s |
| CRITICAL_TTC_START / _END | either a 2-D collision course that braking can no longer avoid with the available deceleration (PREDICTED_OVERLAP), or a leader ahead closer than the safe following distance (UNSAFE_FORWARD_GAP), see below; ends once both reasons are clearly off (hysteresis) |
| EGO_PATH_ENTRY / EXIT | track enters / clearly leaves the straight-ahead 1.5 m corridor beyond the recorder's front edge (not a lane change) |
| CUT_IN_FROM_LEFT / _RIGHT_START / _END | a car ahead, moving within 25 deg of the recorder's heading, its body already within 1 m of the corridor, closes on the corridor from that side (see below); ends when the lateral motion settles |
| STOP_SIGN_DETECTED_START / _END, YIELD_... | camera sign track confirmed / last detected |
| COLLISION | one per contact (see the segmentation rule above); keeps its peak impulse for alignment |

A START at the first observation (recording start, or a track's first sample)
carries `active_at_first_observation`; an EGO_PATH_ENTRY that was never seen is
not invented; a state still active when observation ends has no END. A sign
END means this recorder stopped detecting the sign, not that its obligation
ended; `checks.sign_windows` lists the STOP_START events inside each window.

CRITICAL_TTC (`src/cdf/reconstruction/conflict.py`) is true for either of two
reasons, recorded per TRACK_STATE fact as `critical_reason`:

* PREDICTED_OVERLAP: a predicted 2-D collision course that braking can no longer
  avoid (questions 1-3 below): crossing, oblique and converging conflicts, a
  car from behind or from the side;
* UNSAFE_FORWARD_GAP: a leader ahead closer than the safe following distance
  (question 4), collision course or not: a car a few metres ahead at the
  recorder's own speed is never on a collision course, but if it braked the
  recorder would have no room to perceive, react and stop.

For PREDICTED_OVERLAP it asks three questions of every track sample, from the
recorder's own odometry and the track only:

1. Is there a real geometric threat?  The next `prediction_horizon_s` = 6 s are
   predicted every 0.05 s in the recorder's frame.  The recorder: its footprint
   inflated into an envelope (`critical_standstill_margin_m` = 1 m ahead and
   behind, `critical_lateral_margin_m` = 0.3 m at the sides) along its current
   path (constant speed and yaw rate: a circular arc).  The target: a nominal
   box (`target_length_m` x `target_width_m` = 4.6 x 1.9 m; the radar measures
   no size) behind its observed near surface (the corner towards the recorder
   seen obliquely, the facing side seen along an axis), at its estimated
   velocity; its velocity across the recorder's heading counts only beyond its
   uncertainty (a car keeps its lane unless the evidence says otherwise); a
   target decelerating at `target_braking_min_mps2` = 1 m/s^2 or more keeps
   that deceleration until it stops.  A collision course is an overlap of the
   two boxes; a target closing in radially that passes ahead of or behind the
   envelope never overlaps.
2. Are the times incompatible?  TTC = the first overlapping instant; the span of
   overlapping instants is the temporal occupancy overlap of the conflict area
   (`predicted_overlap_s`).
3. Is the avoidance margin insufficient?  The required deceleration a_req is the
   smallest one (bisection) that removes every overlap when the braking vehicle
   reacts after `critical_reaction_time_s` = 1 s and brakes along its path to a
   stop.  The braking vehicle is the recorder, or the target when even an
   instant stop of the recorder cannot avoid the overlap (a car closing in from
   behind).  CRITICAL when a_req >= `critical_deceleration_mps2` = 6 m/s^2.

4. Is the gap to a leader too short?  The clearance runs from the recorder's
   front face to the rear face of the target's nominal box along the recorder's
   heading (never the radar range, which is short for a car beside the
   recorder).  The required distance is the larger of the time-gap distance
   v x t_front(v), t_front from the UN R157 table (7.2 km/h 1.0 s, 10 km/h 1.1 s,
   20 km/h 1.2 s, 30 km/h 1.3 s, 40 km/h 1.4 s, 50 km/h 1.5 s, 60 km/h 1.6 s,
   linear in between, the ends held: no extrapolation above 60 km/h), at least
   2 m, and the braking distance v x 1 s + v^2 / (2 x 6) - v_lead^2 / (2 x 6)
   + 1 m (at least 1 m), where the lead's braking at
   `critical_lead_deceleration_mps2` = 6 m/s^2 is hypothetical: its measured
   acceleration is not used, the question is whether the present gap would
   suffice if it braked.  A leader moves in the same direction (within 30 deg),
   its body is ahead of the front face and either overlaps the corridor
   (+-`path_half_width_m` = 1.5 m) or lies within
   `critical_front_lateral_margin_m` = 1.0 m of it while approaching it
   laterally (`critical_front_lateral_speed_mps` = 0.3 m/s beyond the velocity
   uncertainty), and the recorder itself moves (at least 1 m/s).  Without a
   predicted overlap no TTC is invented (`ttc_s` stays null).

```text
CRITICAL_TTC_START  <=>  (collision course within 6 s and a_req >= 6 m/s^2)
                         or (leader and clearance < required distance)
CRITICAL_TTC_END    <=>  (a_req < 0.75 x 6 m/s^2 or no collision course)
                         and (no leader or clearance > 1.10 x required distance)
```

No claim either way (UNKNOWN) while the track's estimate is not known: position
or velocity std above 1 m / 1 m/s, or the track younger than
`critical_min_track_age_s` = 0.5 s (the smoother's uncertainty at a track's first
samples already draws on later data).  For a target ahead in the same lane
question 3 is the stopping-capability check against a lead car that keeps its
speed or its measured deceleration (at 14 m/s behind a stopped car: critical
within 33.7 m of the vehicle origin); question 4 adds the room needed if the
lead braked.  Cars behind, beside the recorder, two lanes away, or keeping
their own lane next to the corridor are never critical for the gap alone
(they still are on a 2-D collision course); a car next to the corridor counts
only while it moves toward it, because in 3.5 m lanes a car keeping the next
lane sits only about 1 m outside the 3 m corridor and the nominal box placed
from a radar track misses its real side by up to ~0.7 m.  A track seen past
another tracked vehicle (its line of sight crosses that vehicle's box, grown by
`occlusion_margin_m` = 0.5 m) gives no UNSAFE_FORWARD_GAP (and no CUT_IN)
evidence either way.

References, as engineering anchors only.  Art. 149 of the Italian Highway Code
(keep a distance from the vehicle ahead that allows stopping in time and avoids
collisions) and Directive 2006/126/EC (adequate distance to the vehicles in
front and at the side; a speed that allows stopping within the visible free
road) prescribe no numbers.  UN Regulation No. 157 (ALKS) gives minimum
following time gaps for automated lane keeping systems of categories M1 / N1
and names the temporary disruption of the following distance by a cutting-in
vehicle; it is a technical reference for ALKS, not a universal law of human
TTC.  UN Regulation No. 152 (AEBS) asks for a braking demand of at least
5.0 m/s^2 when an imminent car-to-car collision is detected.  There is no single
European critical-TTC threshold for human driving: the 1 s reaction time and
the 6 m/s^2 decelerations are modelling assumptions of this reconstruction
(`configs/reconstruction.yaml`), not values prescribed by EU or UNECE rules.
Limits: constant velocity and yaw rate (no intent, no lane geometry: a target
turning in a roundabout is predicted straight), a nominal target size, braking
as the only avoidance manoeuvre, one track at a time for the prediction.
`closing_ttc_s = clearance / closing speed` (line of sight) remains a fact in
TRACK_STATE.

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

The appearance side is local evidence only: the track's own bearing from the
vehicle origin at its first detection (`track_appeared_front_deg`), never ground
truth. A lead car in the recorder's lane appears FRONT, crossing traffic emerging
on the right appears RIGHT, a car overtaking from behind appears on its side
once it leaves the rear blind zone; a follower directly behind is never seen.
A target present from the start appears where it was first seen.

CUT_IN is a kinematic observation, not a normative judgement. The closest point
of approach of the relative motion stays a quantitative fact (`t_CPA =
-(r.v)/|v|^2`, `d_CPA = |r + v t_CPA|` in TRACK_STATE); no event is derived
from it. A CUT_IN needs a car ahead moving roughly in the recorder's
direction (so crossing traffic is never a cut-in) that approaches the corridor
laterally at 0.3 m/s or more for 0.5 s, starting at least 0.5 m outside it,
having closed 0.5 m, due to reach it within 3 s, and whose nominal body is
already within `cut_in_preentry_margin_m` = 1.0 m of the corridor (pre-entry):
a car still crossing a lane further away is not cutting in yet (it may be
heading for the lane next to the recorder's), and a car seen past another
tracked vehicle gives no evidence either way. The side is the
recorder's own view (negative lateral = left). It ENDS when the lateral
approach stays below 0.2 m/s for 0.3 s; a COLLISION does not end it, and a lost
track leaves it UNKNOWN. Thresholds are global (`configs/reconstruction.yaml`),
never per scenario. Limitations: the corridor is straight ahead, so on a curved
road an adjacent-lane car could look like a cut-in; the lateral motion is
relative, so a recorder changing lanes toward a car sees that car cut in. A track estimate with
position std above 1 m or velocity std above 1 m/s supports no cut-in claim.

Every event node carries `perceived_state_before`: the recorder's own semantic
state just BEFORE the event, built only from its own evidence
(`world_state.py`). Events at one timestamp are simultaneous and share an
identical state; their transitions are applied together, after it. Each
`local_trace.jsonl` frame holds the state at that frame (after its
transitions):

```text
ego:      MOVING, STOP, BRAKE, THROTTLE, TURN_LEFT, TURN_RIGHT, SPEED_LIMIT_EXCEEDED
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
OCCLUSION (vehicle or static scenery), RAW_SENSOR, FILTER or TRACKER.  Each of
the three radars is evaluated from its own mount and field of view.

```text
python scripts/audit_radar_visibility.py traces/S15/run_0_deflected_into_c --json audit.json
```

## Interactive incident replay

```
python scripts/replay_run.py traces/S01/run_0_crash
python scripts/replay_run.py traces/S01/run_0_crash --speed 0.25 --start 0.45 --paused --follow A
python scripts/replay_run.py traces/S17/run_0_crash --camera follow --follow A
```

This is an offline visualization of recorded trajectories. It does not rerun
scenario physics and does not participate in reconstruction: every rendered
frame, each vehicle's `vehicles/<id>/ego.jsonl` pose is interpolated at the
playback time (position linearly, angles the short way round) and applied to a
physics-less CARLA actor, so 0.25x, 0.5x (default), 1x and 2x all show exactly
the recorded trajectories. The replay timeline is the recorded simulator time
(0 s = the earliest ego sample); reconstructed events are placed on it through
each local graph's own clock origin, for display only (this is not the
graph-level alignment). The viewer shows what the reconstruction knows, not
the simulator's ground truth. It reads only the recorders' own files
(`vehicles/<id>/ego.jsonl`, the recorded blueprint and footprint in
`vehicles/<id>/metadata.json`), the reconstruction outputs when present
(`reconstruction/<id>/local_graph.json`, `local_tracks.jsonl`, `local_trace.jsonl`,
`reconstruction/global/global_graph.json` and `associations.json`) and the global
`configs/reconstruction.yaml` (nominal target size, tracking gap). It never reads
`ground_truth/`, the run's own `metadata.json`, the scenario configuration or
`reconstruction/evaluation/`; only vehicles with their own `ego.jsonl` are
replayed. The map is recognised from the recorders' recorded positions: every
OpenDRIVE map shipped with the local CARLA installation is parsed client-side
and the one whose driving lanes hold all of them (at least 98%, 5 points ahead
of any other road network) is loaded, preferring the server's current map
between identical road networks (Town05 / Town05_Opt). Without a local
installation only the server's current map is checked; `--map` overrides the
choice (tests/test_replay_ghosts.py checks all of this with an audit hook on
every file opened).

| Key | Action |
|-----|--------|
| SPACE | play / pause |
| R | restart |
| LEFT / RIGHT | seek -/+0.5 s (SHIFT: 0.05 s, one recorded sample) |
| N / P | jump to the next / previous reconstructed event (pauses) |
| 1 / 2 / 3 / 4 | 0.25x / 0.5x / 1.0x / 2.0x |
| C | camera: overview, follow selected recorder, free |
| TAB | next recorder (follow camera; SHIFT+TAB previous); ghosts are never selectable |
| T | hide / show the radar tracks of every recorder (`--hide-tracks` starts hidden) |
| G | anonymous tracks as ghost boxes or as dots (`--track-dots` starts with dots) |
| H | hide / show the key help |
| ESC | exit |

Mouse: drag to orbit (overview/follow) or look (free camera), wheel to zoom;
click the timeline to seek. Free camera: W/A/S/D/Q/E move, SHIFT faster.
Each vehicle has a letter badge above its roof and a panel on the right with
its recorded speed, its perceived state as the reconstruction wrote it in
`local_trace.jsonl` (its tracks with CLOSING, CRITICAL_TTC, IN_EGO_PATH,
CUT_IN..., lost tracks greyed with their states UNKNOWN, known signs; older
outputs without it show the open START..END pairs) and the events of the last
second, such as TRACK_APPEARED_LEFT, and the recorder's anonymous tracks alive
at that instant. A reconstructed COLLISION shows its participants from the
global graph. What each recorder's radar tracks is drawn in the scene in the
recorder's colour, each track from its own samples through its own observer's
recorded pose (tracks of different recorders are never compared or merged):

- an ANONYMOUS track (the fusion identified no recorder with it) is a ghost:
  a wireframe box of the reconstruction's nominal target size (4.6 x 1.9 m,
  drawn 1.5 m high; the radar measures no size, so it is not a measured body)
  placed behind the observed near surface as the CRITICAL_TTC model places
  it, with an arrow along `atan2(vy, vx)` of the estimated velocity. When the
  speed does not fix a direction (below 1 m/s or within twice its
  uncertainty) the last reliable heading is held, or the box is drawn
  parallel to the recorder without an arrow; a heading is never invented. It
  is labelled `A:track_001 / ANONYMOUS [seen by A]`, solid while measured,
  dashed and `PREDICTED` while the tracker only predicts it;
- a track ASSOCIATED with a recorder is that recorder's replayed vehicle and
  gets no second body: a radar dot at the track estimate, a thin line from its
  observer and `A:track_002 → B`.

A track is interpolated at the render rate only between consecutive samples
of the same track at most `tracking.max_track_gap_s` apart, is never
extrapolated and disappears at its last sample (its TRACK_LOST). Ghosts and
dots are drawn at road height because tracks are planar; overlays are drawn
over the image without occlusion.

The viewer starts CARLA if none is running (`--no-autostart` to only connect)
and stops a server it started on exit (`--keep-server` to leave it running).
It renders through its own camera into a pygame window, runs the world in
synchronous mode while open, and on exit destroys its actors and restores the
world settings.  A participant with `record: false` (S17's third vehicle) has
no `ego.jsonl` and is not replayed or named: it appears only as the anonymous
tracks the recorders formed of it, A:track_001 and B:track_002, two separate
ghosts that overlap where both radars see it.

## LLM abductive forensics

FACTS -> abductive explanation -> semantic hypotheses -> temporal formulas ->
deterministic verification on the reconstructed semantic trace.  Details,
diagram and caveats: [docs/llm_abductive_forensics.md](docs/llm_abductive_forensics.md).

```text
python scripts/check_llm_access.py
python scripts/export_forensic_facts.py traces/S17/run_0_crash
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.8-flash
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider gemini --model gemini-3.5-flash-lite
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai
python scripts/run_llm_analysis.py traces/S17/run_0_crash --provider openai --dry-run
python scripts/verify_llm_analysis.py traces/S17/run_0_crash/reconstruction/llm/runs/<analysis>
python scripts/compare_llm_analyses.py traces/S17/run_0_crash <analysis> <analysis> ...
```

Model policy (`configs/llm.yaml`):

- **OpenAI is locked to `gpt-6-luna` with `reasoning.effort: high`** (Responses
  API, no temperature).  `--model` with another OpenAI model is refused, and
  nothing ever falls back to another OpenAI model: not after an error, not when
  the model is unavailable to the key or rejects a feature, not on a quota.  The
  analysis stops and reports.  Using another OpenAI model is Andrea's decision
  and needs his explicit approval (a change of `model` / `model_locked` in the
  configuration), never the tool's.
- **Gemini**: `gemini-3.8-flash` (primary, default) and `gemini-3.5-flash-lite`
  (second model, for comparison on the same packet and for new analyses once
  the 3.8 daily quota is used up), both with `thinkingConfig.thinkingLevel:
  high` and no `temperature` / `topP` / `topK` / `candidateCount` / `seed` /
  `thinkingBudget` (Gemini 3 keeps its default sampling).
- One analysis = one model for both stages.  A quota error stops it
  (`QUOTA_EXHAUSTED`, or `INCOMPLETE_QUOTA` with Stage 1 saved, to be completed
  later with the same model: `--stage formalize --analysis-dir <dir>`).
  Retries repeat the identical request, only after transient or rate-limit
  errors; an OpenAI client time-out is not retried.
- `scripts/check_llm_access.py` checks the keys and the model access from the
  model-metadata endpoints only (nothing generated) and prints only VALID /
  INVALID and YES / NO.  `--audit-payload` checks every request body against
  the run's semantic graphs and privileged files before it is sent.
- Each call's raw API response, response id, token usage (incl. reasoning /
  thinking tokens) and latency are saved with the answer; never a key.

- The model sees only `reconstruction/llm/forensic_packet.json`: measured ego
  motion and controls, radar tracks through an allowlist (no conflict-model or
  semantic field), sign detections, collision reports, the supplied context,
  under a neutral `run_id`.  An anonymous track stays anonymous.  A leak guard
  refuses any packet or prompt that names events, perceived states, ground
  truth, the scenario or its variant; nothing is sent then.
- Stage 1 (explanation, causal chain, responsibility as causal attribution,
  semantic hypotheses with the vocabulary of `configs/semantic_vocabulary.yaml`)
  and Stage 2 (the testable claims as formulas of a small bounded temporal logic,
  text + AST) are separate calls, prompts versioned in `prompts/`.
- Only after both answers are saved does `cdf.llm.formal.verifier` read the
  semantic trace: TRUE / FALSE / UNKNOWN per formula (formal consistency of the
  hypothesis with the trace, not proof of causation); `cdf.llm.evaluation`
  scores the semantic hypotheses (TP / FP / FN, F1, hallucination rates).
- Providers: OpenAI (Responses API, strict JSON schema) and Gemini
  (`responseJsonSchema`), models in `configs/llm.yaml`.  Keys go in `.env`
  (ignored by git; copy `.env.example`); a provider without its key is reported
  unavailable.  `--oracle-identities` (privileged, evaluation only) writes under
  `reconstruction/evaluation/llm_oracle/`.
