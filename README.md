# CARLA raw-data acquisition

This repository runs the fixed scenario definitions in `configs/scenarios/`
and records raw CARLA observations. It does not interpret those observations.

## Install and start CARLA

Install Python 3.8+, NumPy, Pillow, and PyYAML. Install the CARLA Python API from the wheel
shipped with the CARLA server (the API and server versions must match). Start
CARLA on port 2000, or set `simulation.host`, `simulation.port`, and
`simulation.carla_root` in `configs/default.yaml`.

## Run one scenario

```text
python scripts/run_scenario.py --scenario S01
```

Useful options are `--variant`, `--seed`, `--output`, `--sensor-profile`, and
`--override key=value`. The runner executes one configured scenario variant and
then cleans up its CARLA actors.

## Sensors and files

For example, the default S01 run is written below
`traces/S01/run_0_crash/`:

```text
metadata.json
ground_truth/metadata.json
ground_truth/states.jsonl
ground_truth/controls.jsonl
ground_truth/collisions.jsonl
vehicles/A/ego.jsonl
vehicles/A/controls.jsonl
vehicles/A/collisions.jsonl
vehicles/A/radar/observations.npz
vehicles/A/radar/metadata.json
vehicles/A/camera/metadata.jsonl
vehicles/A/camera/metadata.json
vehicles/A/camera/frames/
vehicles/A/depth/observations.npz
vehicles/A/depth/metadata.json
```

Vehicle files contain only that vehicle's pose, orientation, velocity,
acceleration, angular velocity, controls, collision impulse, RGB JPEG frames,
and independent compact radar/depth observation streams. Ego, controls,
ground truth, and radar run at 20 Hz; RGB is sampled at 4 Hz, while depth is
requested at 20 Hz and records the callbacks delivered by CARLA. Vehicle files
never contain simulator actor IDs.

Depth observations are produced in memory from the configured 20 Hz CARLA
depth stream; full depth images are not persisted. Radar and depth are stored
as compressed NumPy NPZ streams with the same four float32 detection columns:
`depth_m`, `azimuth_rad`, `altitude_rad`, and `radial_velocity_mps`. Depth
`radial_velocity_mps` is `NaN` (`radial_velocity_status: not_estimated`) and
is reserved for temporal estimation in a later stage. Radar velocity remains
the measured CARLA value. The common comparison region is ±45° horizontal,
±5° vertical, and 0–90 m; depth observations are sparsified into 2° azimuth ×
2° altitude bins (at most 225 detections per frame). RGB remains the full 90°
visual image and is stored as visually high-quality lossy JPEG at quality 90.

Each NPZ stores `frames` (int64), `timestamps` (float64), `offsets` (int64),
and `detections` (float32 `[N,4]`). The detections for frame `i` are
`detections[offsets[i]:offsets[i+1]]`; variable frame sizes are not padded.
Sensor metadata stores the schema, units, transform, FOV, rate, and callback
statistics once. For a depth pixel stored as BGRA bytes, metric depth is
decoded in memory as `1000 * (R + 256*G + 65536*B) / (256**3 - 1)` metres.
When a sensor profile defines multiple radars, each sensor is written under
`vehicles/A/radar/<sensor_id>/` with the same NPZ schema.

The separate ground-truth trace is privileged simulator state: it contains
participant actor IDs, full vehicle state, controls as recorded by the runner,
and raw collision counterparts. It is kept separate from vehicle observations.

The runner uses the fixed scenario definitions retained in the configuration
files and does not generate new scenarios or alter their routes.
