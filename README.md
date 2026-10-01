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
metadata written before this correction (including the S01-S03 and S15 runs in
`traces/`) says `positive_towards_sensor`; that label is wrong for the stored
radar values, which are unchanged.

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
- No log is synchronised. Two COLLISION nodes of different graphs are the same
  contact when their peak impulses agree (equal and opposite impulses);
  `alignment.json` stores `t_global = t_local + offset_to_global` with
  `t_global = 0` at that contact. Local graphs are never modified. Recorders
  without a matched collision stay `UNALIGNED` (no multi-hop alignment yet).
- A local track is named after another recorder only at fusion, and only when
  it was persistent, at contact range at the matched collision, the only such
  track, and its speed matches that recorder's own speed. Otherwise it stays
  anonymous (`A:track_001`) with the blocking reason in `associations.json`.
- Radar detection velocity is used as stored: the range rate (negative while
  the range shrinks), whatever label older radar metadata carries.

Three levels are kept apart. Raw and track data feed the 10 Hz FACTS of
`local_trace.jsonl` (EGO_MOTION, EGO_CONTROL, TRACK_STATE: speeds, pedals,
ranges, TTC, the track's own velocity `vx_mps`/`vy_mps`, its Kalman
uncertainty, its motion relative to the recorder, the closest point of
approach `t_cpa_s`/`d_cpa_m`, and a qualitative `motion_relation`). The graph
holds only semantic EVENTS, which are state transitions without telemetry:

| Events | Meaning |
|--------|---------|
| BRAKE_START / BRAKE_END | brake at or above 0.1; releases shorter than 0.2 s do not split it |
| HARD_BRAKE_START / _END | brake at or above 0.9 (nested inside BRAKE) |
| STRONG_THROTTLE_START / _END | throttle at or above 0.8 |
| MOVING_START / _END, STOP_START / _END | stop below 0.3 m/s, moving again above 1 m/s |
| SPEED_LIMIT_EXCEEDED_START / _END | above limit + 1 km/h, back at or below limit - 1 km/h (nested inside MOVING) |
| TRACK_APPEARED / TRACK_LOST | lifetime of an anonymous radar track |
| CLOSING_START / _END | closing at 1 m/s or more; ends below 0.5 m/s |
| CRITICAL_TTC_START / _END | range / closing speed at most 2 s while closing; ends at the latest with CLOSING |
| EGO_PATH_ENTRY / EXIT | track enters / clearly leaves the straight-ahead 1.5 m corridor (not a lane change) |
| PREDICTED_PATH_CONFLICT_START / _END | the relative motion's closest approach lies ahead within 4 s and 1.5 m; ends once it is past, beyond 5 s or 2.5 m |
| CUT_IN_FROM_LEFT / _RIGHT_START / _END | a car ahead, moving within 25 deg of the recorder's heading, closes on the corridor from that side (see below); ends when the lateral motion settles |
| STOP_SIGN_DETECTED_START / _END, YIELD_... | camera sign track confirmed / last detected |
| COLLISION | one per contact (callbacks within 0.5 s); keeps its peak impulse for alignment |

A START at the first observation (recording start, or a track's first sample)
carries `active_at_first_observation`; an EGO_PATH_ENTRY that was never seen is
not invented; a state still active when observation ends has no END. A sign
END means this recorder stopped detecting the sign, not that its obligation
ended; `checks.sign_windows` lists the STOP_START events inside each window.

PREDICTED_PATH_CONFLICT and CUT_IN are kinematic observations, not normative
judgements, and neither predicts a collision with certainty. The conflict uses
the target's position r and the relative velocity v in the recorder's frame:
`t_CPA = -(r.v)/|v|^2`, `d_CPA = |r + v t_CPA|`; it needs a future t_CPA within
the horizon and a small miss distance (with hysteresis and a 0.2 s release
debounce). A CUT_IN needs a car ahead moving roughly in the recorder's
direction (so crossing traffic is never a cut-in) that approaches the corridor
laterally at 0.3 m/s or more for 0.5 s, starting at least 0.5 m outside it,
having closed 0.5 m, and due to reach it within 3 s. The side is the
recorder's own view (negative lateral = left). It ENDS when the lateral
approach stays below 0.2 m/s for 0.3 s; a COLLISION does not end it, and a lost
track leaves it UNKNOWN. Thresholds are global (`configs/reconstruction.yaml`),
never per scenario. Limitation: the corridor is straight ahead, so on a curved
road an adjacent-lane car could look like a cut-in. A track estimate with
position std above 1 m or velocity std above 1 m/s supports neither state.

Every event node carries `perceived_state_before`: the recorder's own semantic
state just BEFORE the event, built only from its own evidence
(`world_state.py`). Events at one timestamp are simultaneous and share an
identical state; their transitions are applied together, after it. Each
`local_trace.jsonl` frame holds the state at that frame (after its
transitions):

```text
ego:      MOVING, STOP, BRAKE, HARD_BRAKE, STRONG_THROTTLE, SPEED_LIMIT_EXCEEDED
external: track_NNN -> visible, CLOSING, CRITICAL_TTC, IN_EGO_PATH,
                       PREDICTED_PATH_CONFLICT, CUT_IN_FROM_LEFT, CUT_IN_FROM_RIGHT
signs:    sign-N    -> class, visible, known, relevant_to_ego_path
```

Values are true, false or "UNKNOWN". UNKNOWN means the recorder cannot tell:
before its first sample, without a supplied speed limit, while a track
estimate is too uncertain, and for every state of a track after TRACK_LOST
(then `visible` is false). A loss never invents an END. A sign that leaves view
stays `known` (visible false): nothing admissible tells when its controlled
point has been passed, so knowledge is not cleared. Names stay local
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
and SAME_TRACK, which links a track's TRACK_APPEARED to every other event whose
subject is the same local track. SAME_TRACK is exactly "same subject_id" made
explicit for graph queries: it groups events and implies no order.
Adding a state means computing its active intervals in `local.py`.
Parameters are in `configs/reconstruction.yaml`.

`src/cdf/evaluation/reconstruction.py` is the only code that reads
`ground_truth/`; it compares the written files with the simulator state
(collision participants, clock anchors, identity decisions, track accuracy)
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
python scripts/replay_run.py traces/S01/run_0_crash --speed 0.25 --start 0.45 --paused --show-tracks
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
| TAB | next vehicle (follow camera, radar tracks) |
| T | show the selected recorder's anonymous radar tracks |
| H | hide / show the key help |
| ESC | exit |

Mouse: drag to orbit (overview/follow) or look (free camera), wheel to zoom;
click the timeline to seek. Free camera: W/A/S/D/Q/E move, SHIFT faster.
Each vehicle has a letter badge above its roof and a panel on the right with
its recorded speed, its perceived state as the reconstruction wrote it in
`local_trace.jsonl` (visible tracks with CLOSING, CRITICAL_TTC, PATH_CONFLICT,
CUT_IN..., lost tracks greyed with their states UNKNOWN, known signs; older
outputs without it show the open START..END pairs) and the events of the last
second. A reconstructed COLLISION shows its participants
from the global graph. Track markers show the reconstruction's own range and
closing speed; they are drawn at road height because tracks are planar.

The viewer starts CARLA if none is running (`--no-autostart` to only connect)
and stops a server it started on exit (`--keep-server` to leave it running).
It renders through its own camera into a pygame window, runs the world in
synchronous mode while open, and on exit destroys its actors and restores the
world settings.
