# CausalDrive Forensics

**Reconstructing traffic accidents from partial onboard recordings.**

After a collision, each vehicle that recorded something holds only its own data, on its own clock: radar returns,
pose and motion, controls and collision callbacks.  Road users that recorded nothing leave no data at all.  This
project reconstructs, from those recordings alone, what happened between *all* road users: who was where, who
was whom, what each vehicle could perceive, and when the collision occurred.  The reconstruction is evaluated on
simulated accidents in CARLA 0.9.15, whose ground truth is used for evaluation only.

## How it works

```
onboard recordings (one folder per recording vehicle)
  │
  ├─ local reconstruction     radar tracking, ego motion, local events (CLOSING, CRITICAL_TTC, CUT_IN, ...)
  ├─ temporal alignment       one global clock from shared collisions or mutual observations
  ├─ identity association     which radar track is which recording vehicle
  ├─ anonymous road users     vehicles that recorded nothing, fused from several radar views (U1, U2, ...)
  └─ global semantic graph    one event trace for the whole accident  →  replay and evaluation
```

The method is deterministic, uses no ground truth, no scenario-specific rules and no external services, and leaves
ambiguous identities unresolved rather than guessing.  Details: [docs/METHOD.md](docs/METHOD.md).

## Main results

Robustness of the frozen reconstruction on the 22 canonical runs: 35 perturbed conditions, 3,774 reconstructions
([full report](docs/ROBUSTNESS_CAMPAIGN.md)).

| condition | collisions with correct participants | identity accuracy (decided links) | fused position error, median / p95 |
|---|--:|--:|--:|
| unperturbed | 1.000 (27 / 27) | 1.000 | 0.27 m / 0.75 m |
| radar noise, nominal | 1.000 | 1.000 | 0.30 m / 0.83 m |
| radar noise, high (30 false returns per sweep) | 0.991 | 0.950 | 0.52 m / 2.05 m |
| consumer GNSS (about 2.5 m RMS) | 1.000 | 1.000 | 1.78 m / 2.58 m |
| degraded GNSS (about 6.9 m RMS) | 1.000 | 1.000 | 4.90 m / 7.17 m |

- No collision was attributed to the wrong vehicles in any of the 3,774 reconstructions; failures are missed
  contacts only.
- GNSS errors shift the reconstructed positions but create no wrong identity: the method links fewer tracks instead.
- Dense radar clutter is the breaking point: phantom road users appear and 42 % of the identity links of the
  vehicles involved in the accident are left unresolved.
- Results are on simulated data with modelled sensor errors; limitations are discussed in the report.

## Installation

Requirements: Windows, [Miniconda](https://docs.conda.io/en/latest/miniconda.html), and
[CARLA 0.9.15](https://github.com/carla-simulator/carla/releases/tag/0.9.15) (packaged Windows build) for the
replay and for recording.  Reconstruction, evaluation and the robustness campaign run on saved recordings and need
no CARLA server.

```bat
git clone https://github.com/AndreaBedei1/causaldrive-forensics.git
cd causaldrive-forensics
conda env create -f environment.yml
conda activate carla
python -m pytest -q
```

The environment is Python 3.8.20 with the `carla==0.9.15` client and an editable install of this checkout.  If CARLA
is not installed in a standard location, set its folder before starting the server:

```bat
set CARLA_ROOT=C:\path\to\CARLA_0.9.15\WindowsNoEditor
```

## Explore the scenarios

```bat
conda activate carla
python scripts\start_carla.py
```

In a second terminal, open the menu of the 22 canonical runs and pick one:

```bat
conda activate carla
python scripts\review_canonical_runs.py --port 3000
```

The replay shows the reconstruction: recording vehicles move along their own recorded poses, reconstructed road
users are boxes, and each recorder's panel lists what it perceived and when.  Keys: SPACE play/pause, LEFT/RIGHT
seek, N/P next/previous event, C camera, TAB next vehicle, F focus its panel, H help.  Full guide and how to read the
screen: [docs/REPLAY.md](docs/REPLAY.md).

## Reproduce the results

```bat
conda activate carla

:: reconstruct and evaluate one canonical run
python scripts\reconstruct_run.py traces\S11\run_0_consequential --evaluate

:: validate the whole canonical set
python scripts\validate_canonical.py --out docs\CANONICAL_VALIDATION.md

:: regenerate the robustness tables and figures from the committed job records
python scripts\campaign_report.py robustness
```

To rerun the robustness campaign itself (about 170 CPU-hours; pause and resume at any time):

```bat
git checkout robustness-campaign-final
set CDF_CAMPAIGN_RESULTS=results\robustness\my_run
scripts\campaign.bat workers 20
scripts\campaign.bat start
scripts\campaign.bat status
```

Protocol, controller commands and verification: [docs/FROZEN_CAMPAIGN.md](docs/FROZEN_CAMPAIGN.md).

## Repository

| path | content |
|---|---|
| `src/cdf/` | reconstruction, evaluation, replay and simulation code |
| `configs/` | reconstruction parameters, scenario definitions, sensor setup |
| `scripts/` | command-line tools (replay, reconstruction, validation, campaign) |
| `traces/` | the 22 canonical runs: raw recordings, ground truth, reconstruction |
| `results/` | robustness campaign: job records, tables, figures |
| `docs/` | method, scenarios, replay guide, campaign protocol and report |

## Documentation

| topic | page |
|---|---|
| Reconstruction method | [METHOD.md](docs/METHOD.md) |
| Semantic events and thresholds | [event_definitions.md](docs/event_definitions.md) |
| Parameters and their evidence | [FINAL_PARAMETER_AUDIT.md](docs/FINAL_PARAMETER_AUDIT.md) |
| Canonical scenarios and commands | [SCENARIOS.md](docs/SCENARIOS.md) |
| Validation of the canonical set | [CANONICAL_VALIDATION.md](docs/CANONICAL_VALIDATION.md) |
| Replay viewer | [REPLAY.md](docs/REPLAY.md) |
| Sensors and recording | [campaign_acquisition.md](docs/campaign_acquisition.md) |
| Robustness report | [ROBUSTNESS_CAMPAIGN.md](docs/ROBUSTNESS_CAMPAIGN.md) |
| Robustness protocol | [FROZEN_CAMPAIGN.md](docs/FROZEN_CAMPAIGN.md) |
| Perturbation profiles | [robustness_profiles.md](docs/robustness_profiles.md) |
| Stability review and audit | [STABILITY_REVIEW.md](docs/STABILITY_REVIEW.md), [STABILITY_AUDIT.md](docs/STABILITY_AUDIT.md) |
| Positioning, related work and limitations | [paper_positioning.md](docs/paper_positioning.md), [bibliography.md](docs/bibliography.md) |
