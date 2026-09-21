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

Each run is written below `traces/<scenario>/run_<seed>/<variant>/`:

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
```

Vehicle files contain only that vehicle's pose, orientation, velocity,
acceleration, angular velocity, controls, collision impulse, radar detections
(frame, timestamp, depth, azimuth, altitude, radial velocity), and raw camera
frames with sensor metadata. Vehicle files never contain simulator actor IDs.

The separate ground-truth trace is privileged simulator state: it contains
participant actor IDs, full vehicle state, controls as recorded by the runner,
and raw collision counterparts. It is kept separate from vehicle observations.

The scenario set is the fixed S01-S16 set retained in the configuration files;
the runner does not generate new scenarios or alter their routes.
