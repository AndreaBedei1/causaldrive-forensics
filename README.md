# CARLA raw-data acquisition

This repository runs the fixed scenario definitions in `configs/scenarios/`
and records raw CARLA observations. It does not alter scenario physics.

## Install and run

Install Python 3.8+, NumPy, Pillow, and PyYAML, plus the CARLA 0.9.15 Python
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

Radar velocity is CARLA's native `RadarDetection.velocity`. CARLA 0.9.15
documents it as velocity towards the sensor, so positive means closing range
and negative means receding range. Depth velocity uses the same convention but
is estimated locally from temporally associated compact depth observations:

```text
radial_velocity_mps = (previous_depth_m - current_depth_m) /
                      (current_timestamp - previous_timestamp)
```

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

Changing only `source="radar"` to `source="depth"` selects the other stream.
`common_region=True` exposes the physical overlap (azimuth -45..45 degrees,
altitude -5..5 degrees, range 0..90 m) without changing native files. There is
no automatic fallback and no radar/depth fusion in this task. Radar and depth
keep their own `sensor_transform` metadata; comparable semantics do not imply
co-located sensors.

Depth images are processed in memory and not persisted. Observations are one
nearest-surface detection per approximately 2° x 2° angular bin (up to 225 per
frame). RGB remains 800x600 at 4 Hz, JPEG quality 90. Metric depth decoding is
`1000 * (R + 256*G + 65536*B) / (256**3 - 1)` metres for CARLA BGRA bytes.

## Validation

Synthetic estimator tests are in `tests/test_depth_observations.py`. After
acquisition, run the post-acquisition report helper (it never feeds radar into
the estimator):

```text
python scripts/validate_observations.py traces/S01/run_0_crash/vehicles/A --metrics
```

The helper reports finite depth coverage and compatible radar/depth matched
pairs, sign agreement, MAE, median absolute error, and RMSE. Because radar and
depth sense different surfaces and have different native extrinsics, unmatched
returns and disagreement are expected and must be interpreted as sensing or
association differences rather than hidden with ground truth.

The separate `ground_truth/` trace contains privileged simulator state and is
never part of the vehicle-local estimator input. No generated scenario traces
should be committed.
