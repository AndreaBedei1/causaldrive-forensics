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

The 22 canonical runs were re-acquired on 2026-10-22 with a deterministic acquisition.  Recorded twice, 21 of the
22 runs are bit-identical ([reproducibility](docs/REPRODUCIBILITY.md)).

Results of the reconstruction with an ideal pose, G0 ([error analysis](docs/G0_ERROR_ANALYSIS.md)):

| quantity | G0 result |
|---|---|
| collisions | 27/27 detected with the correct participants, 0 invented.  Every contact is between two recording vehicles, whose own collision reports are matched |
| road users that record nothing | 45/45 observable vehicles represented; 20 duplicates in dense traffic (S14-S19) |
| position of road users | median error 0.21 m in steady motion, 0.33 m in turns |
| speed of road users | median error 0.03 m/s in steady motion, 0.06 m/s in turns |
| CRITICAL_TTC warnings | 43/43 justified warnings issued before the impact (median lead time 1.55 s) |

Limits:
* G0 is a reference condition: a synthetic GNSS/INS with zero added error, not a real receiver.
* The dataset has no contact involving a vehicle that records nothing.

Degradation study:
* **Campaign v3** is prepared and smoke-tested, not run ([design](docs/CAMPAIGN_V3.md)).  It covers RTK and
  degraded GNSS, radar at nominal, severe and extreme levels, combined and asymmetric degradations, and several
  seeds.
* **Earlier campaign.**  The robustness campaign of 2026-10-15/16 refers to the previous recordings
  ([archived report](docs/archive/ROBUSTNESS_CAMPAIGN.md)).

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

Start two CARLA 0.9.15 servers, one per viewer, each in its own terminal:

```bat
conda activate carla
python scripts\start_carla.py --carla-root F:\Carla9_15\WindowsNoEditor --port 3000
```

```bat
conda activate carla
python scripts\start_carla.py --carla-root F:\Carla9_15\WindowsNoEditor --port 3100
```

In a third terminal, open the menu of the 22 canonical runs and pick one:

```bat
conda activate carla
python scripts\review_canonical_runs.py --port 3000 --gt-port 3100 --res 960x540
```

For each run the menu opens two viewers side by side, synchronised:
* left, the GROUND TRUTH viewer: what CARLA simulated, every vehicle on its true trajectory, with the physical
  contacts;
* right, the RECONSTRUCTION viewer: what the algorithm estimated from the sensors.  Recording vehicles are drawn at
  the pose the reconstruction used, reconstructed road users are boxes, and each recorder's panel lists what it
  perceived and when.

Control time (SPACE, LEFT/RIGHT, speed keys) in the left window; the right one follows the same instant.  Only that
instant, the play state and the speed cross between them.  Other keys: N/P next/previous event, C camera, TAB next
vehicle, F focus its panel, H help.

The labels are each viewer's own clock (`t_contact`, `t_global`).  They read the same in 21 of the 22 runs.  In S04
`b_rear_first` the left one reads 1.55 s more.  Full guide and how to read the screen: [docs/REPLAY.md](docs/REPLAY.md).

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

To rerun the earlier robustness campaign on the previous recordings (about 170 CPU-hours; pause and resume at any
time):

```bat
git checkout robustness-campaign-final
set CDF_CAMPAIGN_RESULTS=results\robustness\my_run
scripts\campaign.bat workers 20
scripts\campaign.bat start
scripts\campaign.bat status
```

Protocol, controller commands and verification: [docs/archive/FROZEN_CAMPAIGN.md](docs/archive/FROZEN_CAMPAIGN.md).

## Repository

| path | content |
|---|---|
| `src/cdf/` | reconstruction, evaluation, replay and simulation code |
| `configs/` | reconstruction parameters, scenario definitions, sensor setup |
| `scripts/` | command-line tools (replay, reconstruction, validation, campaign) |
| `traces/` | the 22 canonical runs: raw recordings, ground truth, reconstruction |
| `results/` | study results: G0 scorecard and reproducibility checks (current), robustness campaign (previous recordings) |
| `docs/` | method, scenarios, viewers, analyses, campaign design; `docs/archive/`: documents of the previous recordings |

Full map, data separation and the state of every branch: [docs/REPOSITORY.md](docs/REPOSITORY.md).

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
| Reproducibility of the acquisitions | [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) |
| Sensors versus ground truth | [SENSORS_AND_GROUND_TRUTH.md](docs/SENSORS_AND_GROUND_TRUTH.md) |
| G0 results and error analysis | [G0_ERROR_ANALYSIS.md](docs/G0_ERROR_ANALYSIS.md) |
| Campaign v3 (prepared, not run) | [CAMPAIGN_V3.md](docs/CAMPAIGN_V3.md) |
| Repository map, branches, data | [REPOSITORY.md](docs/REPOSITORY.md) |
| Earlier robustness campaign (previous recordings) | [report](docs/archive/ROBUSTNESS_CAMPAIGN.md), [protocol](docs/archive/FROZEN_CAMPAIGN.md) |
| Perturbation profiles | [robustness_profiles.md](docs/robustness_profiles.md) |
| Stability review and audit | [STABILITY_REVIEW.md](docs/STABILITY_REVIEW.md), [STABILITY_AUDIT.md](docs/STABILITY_AUDIT.md) |
| Positioning, related work and limitations | [paper_positioning.md](docs/paper_positioning.md), [bibliography.md](docs/bibliography.md) |
