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
vehicles/A/radar.jsonl
vehicles/A/camera/metadata.jsonl
vehicles/A/camera/frames/
vehicles/A/depth_observations.jsonl
```

Vehicle files contain only that vehicle's pose, orientation, velocity,
acceleration, angular velocity, controls, collision impulse, radar detections
(frame, timestamp, depth, azimuth, altitude, radial velocity), RGB PNG frames,
and compact geometric depth observations. Ego, controls, ground truth, and
radar run at 20 Hz; RGB is intentionally sampled at 4 Hz, while depth is
requested at 20 Hz and records the callbacks delivered by CARLA.
RGB, depth, and radar are recorded independently; no sensor selection or
combination is performed. Vehicle files never contain simulator actor IDs.

Depth observations are produced in memory from the configured 20 Hz CARLA
depth stream;
full depth images are not persisted. Radar and depth detections share the same
fields (`depth`, `azimuth`, `altitude`, `radial_velocity`). Depth radial velocity
is currently `null` and is reserved for a later temporal implementation. The
common comparison region is ±45° horizontal, ±5° vertical, and 0–90 m;
observations are sparsified into 2° azimuth × 2° altitude bins (at most 225
detections per frame). RGB remains the full 90° visual image.

For a depth pixel stored as BGRA bytes, metric depth is decoded as
`1000 * (R + 256*G + 65536*B) / (256**3 - 1)` metres. Depth metadata retains
the original CARLA frame and timestamp, sensor transform, and compact
detections; no full depth image is written.

The separate ground-truth trace is privileged simulator state: it contains
participant actor IDs, full vehicle state, controls as recorded by the runner,
and raw collision counterparts. It is kept separate from vehicle observations.

The runner uses the fixed scenario definitions retained in the configuration
files and does not generate new scenarios or alter their routes.
