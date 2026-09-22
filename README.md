# CARLA raw-data acquisition

This repository runs the fixed scenario definitions in `configs/scenarios/`
and records raw CARLA observations. It does not interpret those observations.

## Install and start CARLA

Install Python 3.8+ and PyYAML. Install the CARLA Python API from the wheel
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
vehicles/A/depth/metadata.jsonl
vehicles/A/depth/frames/
```

Vehicle files contain only that vehicle's pose, orientation, velocity,
acceleration, angular velocity, controls, collision impulse, radar detections
(frame, timestamp, depth, azimuth, altitude, radial velocity), raw RGB frames,
and raw depth-camera frames with sensor metadata. RGB, depth, and radar are
recorded independently; no sensor selection or combination is performed.
Vehicle files never contain simulator actor IDs.

Depth frames are lossless original CARLA BGRA bytes (`raw_bgra8`), not a
visualization. For a pixel stored as BGRA bytes, metric depth can later be
decoded as `1000 * (R + 256*G + 65536*B) / (256**3 - 1)` metres. Per-frame
metadata includes the frame, timestamp, sensor transform, width, height, FOV,
blueprint, file format, and filename.

The separate ground-truth trace is privileged simulator state: it contains
participant actor IDs, full vehicle state, controls as recorded by the runner,
and raw collision counterparts. It is kept separate from vehicle observations.

The scenario set is the fixed S01-S16 set retained in the configuration files;
the runner does not generate new scenarios or alter their routes.
