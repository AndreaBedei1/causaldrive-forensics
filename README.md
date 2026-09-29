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
  collisions, traffic signs, radar). It never reads `ground_truth/`, other
  vehicles' files, actor IDs or the CARLA `frame` counter (shared by all
  recorders). External objects are anonymous radar tracks.
- Local time: `t_local = source timestamp - origin`, the origin being the
  recorder's own first ego sample; each event keeps its raw `t_source`. Local
  frame: origin and x axis at the recorder's first pose, y to its right.
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

The event vocabulary is small: BRAKE_EPISODE, THROTTLE_ONSET (strong throttle),
FULL_STOP, STOP/YIELD_SIGN_DETECTED, TRACK_APPEARED, ENTERED_EGO_PATH, CLOSING,
CRITICAL_TTC (range-based), TRACK_LOST and COLLISION (callbacks within 0.5 s
form one contact). A BRAKE_EPISODE is one node per continuous braking action:
it is stamped at its start and records start, end, duration, peak and mean
brake, speed at start/end, minimum speed and whether the brake was released
before the recording ended; a release shorter than 0.2 s does not split it.
The individual brake values stay in the trace's EGO_CONTROL facts. Adding a
type means adding one extractor in `local.py`.
Graph edges are PRECEDES (time order) and SAME_TRACK. Parameters are in
`configs/reconstruction.yaml`.

`src/cdf/evaluation/reconstruction.py` is the only code that reads
`ground_truth/`; it compares the written files with the simulator state
(collision participants, clock anchors, identity decisions, track accuracy)
and reruns alignment with one recorder's clock shifted by 0.73 s to check that
the global graph does not change. Tests: `python -m pytest tests`.
