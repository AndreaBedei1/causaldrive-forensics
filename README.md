# CausalDrive Forensics

**Cooperative reconstruction of traffic accidents from partial onboard recordings.**

After a collision, each vehicle that recorded something holds only its own data, on its own clock: radar
detections, its own pose and motion, its controls and indicator lights, and the time and impulse of the contacts its
collision sensor felt.  Road users that recorded nothing leave no data at all.  This project reconstructs, from those
recordings alone, what happened between *all* road users: who was where, who was whom, what each vehicle could
perceive and when, and which vehicles collided in which order.  It is evaluated on 22 simulated accidents in CARLA
0.9.15, whose ground truth is used for the evaluation only.

**At a glance (G0, ideal GNSS/INS, 22 runs).**  26/26 collisions found with the right participants and none
invented; every one of the 45 observable vehicles that recorded nothing is represented; their positions are
estimated with a median error of 0.21 m in steady motion and 0.33 m in turns; 42/42 justified CRITICAL_TTC warnings
come before the impact.  The degradation study is in [Results](#results).

## Contents

1. [Problem](#problem)
2. [Architecture](#architecture)
3. [Simulator and the 22 scenarios](#simulator-and-the-22-scenarios)
4. [Sensors and cooperative reconstruction](#sensors-and-cooperative-reconstruction)
5. [Tracking: Kalman filter and RTS smoother](#tracking-kalman-filter-and-rts-smoother)
6. [Temporal alignment and identity association](#temporal-alignment-and-identity-association)
7. [Fusion of road users](#fusion-of-road-users)
8. [Collisions and semantic events](#collisions-and-semantic-events)
9. [Isolation of the ground truth](#isolation-of-the-ground-truth)
10. [Two viewers](#two-viewers)
11. [Reproducibility](#reproducibility)
12. [Degradation study: GNSS RTK over 5G and radar](#degradation-study-gnss-rtk-over-5g-and-radar)
13. [Tests and the campaign](#tests-and-the-campaign)
14. [Data layout](#data-layout)
15. [Results](#results)
16. [Limitations](#limitations)
17. [Installation and commands](#installation-and-commands)
18. [Documentation and references](#documentation-and-references)

## Problem

A multi-vehicle accident is usually reconstructed after the fact from traces on the road, damage and witnesses.
Modern vehicles record much more: their own position and motion, radar detections of the vehicles around them and
the time of every contact.  Each vehicle, however, records alone:

* on its own clock, not synchronised with any other vehicle;
* in its own frame, with its own pose error;
* with anonymous radar detections (a range, an angle and a radial speed, no identity);
* without knowing which other vehicles also recorded, or who the vehicles it saw were.

The question is whether these partial recordings, put together offline, reconstruct the accident: the collisions
and their participants, the trajectories of every road user (including those that recorded nothing), and what each
vehicle could perceive before the impact.  The project answers it on simulated accidents, where the truth is known,
and measures how the answer degrades when the pose (GNSS/INS) and the radar are worse than ideal.  It reconstructs
facts and perception; it does not assign liability.

## Architecture

```
vehicles/<R>/   raw recordings of each recording vehicle R (its own clock and frame)
   │
   ├─ 1. local reconstruction      per recorder, alone: ego motion, radar tracking (Kalman filter + RTS smoother),
   │                                local semantic events (CLOSING, CRITICAL_TTC, EGO_PATH_ENTRY, CUT_IN, ...)
   ├─ 2. temporal alignment        one global clock from the collisions the recorders felt in common
   │                                (else from what they observed of each other)
   ├─ 3. identity association      which radar track of a recorder is another recorder
   ├─ 4. road users                vehicles that recorded nothing, fused across observers (U1, U2, ...)
   └─ 5. global semantic graph     one event trace of the whole accident on the global clock
   │
reconstruction/                    local graphs, global graph and trace, road users, alignment, report
   │
   ├─ evaluation (privileged)      against ground_truth/, after the reconstruction, never read by it
   └─ replay                       two viewers: GROUND TRUTH and RECONSTRUCTION, side by side
```

The method is deterministic and offline.  It uses no ground truth, no scenario-specific rule and no external
service, and it leaves an ambiguous identity unresolved rather than guessing: a false merge of two vehicles is worse
than an unresolved one.  Code: `src/cdf/reconstruction/` (one method, parameters in `configs/reconstruction.yaml`,
each with its evidence in [docs/FINAL_PARAMETER_AUDIT.md](docs/FINAL_PARAMETER_AUDIT.md)).  Details:
[docs/METHOD.md](docs/METHOD.md).

## Simulator and the 22 scenarios

The accidents are simulated in CARLA 0.9.15 in synchronous mode at 20 Hz, with scripted participants and no traffic
manager, so that a recording is reproducible (`docs/REPRODUCIBILITY.md`).  The canonical set has 19 scenarios and 22
runs, each reviewed by eye in both viewers ([docs/SCENARIOS.md](docs/SCENARIOS.md)):

| scenarios | what they test |
|---|---|
| S01-S03 | rear-end, cut-in and junction crossing collisions between two recorders |
| S04 (two variants), S05, S10, S11 | chains and pile-ups: several collisions, their order, a car deflected into a third, an occluded leader, a secondary collision |
| S06, S08, S09 | three-way junction, rolling through a STOP, an all-way stop |
| S07 | a merge conflict in a roundabout (Town03_Opt) |
| S12, S13 (three variants) | road users that record nothing: a causally relevant car, two nearby cars kept apart |
| S14-S18 | dense traffic: abreast, platoon, overtaking, occlusion and reappearance, similar cars around a contact |
| S19 | a four-lane motorway curve (Town04) |

Every run has two or three recorders (16 and 6 runs) and up to eight vehicles that record nothing: 95 vehicles in
all, 50 of them recorders.

## Sensors and cooperative reconstruction

Each recording vehicle carries (`configs/sensors/`, [docs/SENSORS_AND_GROUND_TRUTH.md](docs/SENSORS_AND_GROUND_TRUTH.md)):

* **a GNSS/INS** (`ego.jsonl`, 20 Hz): position, heading, attitude, velocity, acceleration and angular rate.  In the
  reference condition **G0** it adds no error: G0 measures what radar, association and fusion lose on their own,
  and no claim about a real receiver is drawn from it;
* **three radars** (front 150 deg, left and right 140 deg, 90 m, 20 Hz): CARLA's detections, each a range, an azimuth,
  an elevation and a radial speed, with no identity and no label;
* **a collision sensor**: the time and impulse magnitude of each contact it feels, with the partner's identity
  removed;
* its own controls, indicator lights and a camera-based STOP / YIELD sign detector.

The **supplied incident context** (`incident_context.json`) holds what an investigation knows without any sensor:
the speed limit, the road environment and the road map of the location.  The reconstruction is *cooperative* only
offline: no data is exchanged between vehicles while driving, and the recordings are put together after the crash.

## Tracking: Kalman filter and RTS smoother

Each recorder's radar detections become anonymous tracks in its own frame (`reconstruction/tracking.py`):

* every detection is placed from its own radar's mount and its Doppler speed corrected for the recorder's motion;
* a detection joins a track inside the 99 % gate of the track's predicted covariance plus the spread of a vehicle
  body plus the radar's range-dependent polar noise; Doppler is tested along the line of sight only;
* a detection that two tracks explain about equally updates neither;
* each track is a constant-velocity Kalman filter (Kalman 1960) run forward, then smoothed backward with the
  Rauch-Tung-Striebel smoother (Rauch, Tung, Striebel 1965): the reconstruction is offline, so every estimate may
  use the measurements after it.

## Temporal alignment and identity association

* **Clocks.**  Two recorders that report a contact at the same moment, with equal and opposite impulses, bodies
  touching in their own pose streams and a pre-contact radar view that does not contradict the partner's speed, felt
  the same collision: the match fixes their clock offset.  The strongest matched collision is t_global = 0; chains of
  matches align three or more recorders, and a recorder without a shared collision can be aligned on what the others
  observed of it (`reconstruction/alignment.py`).
* **Recorder links.**  A radar track of recorder A is recorder B when B's own pose stream, carried into A's frame on
  the common clock, explains the track's positions and line-of-sight speeds within their uncertainty, and no other
  recorder does (`reconstruction/identity.py`).  One recorder per observer and instant.

## Fusion of road users

A vehicle that records nothing is seen by several recorders as separate anonymous tracks.  The fusion
(`reconstruction/anonymous.py`) joins tracks that are the same body in the common frame, under cannot-link
constraints (two tracks seen at once by one observer are two vehicles) and a one-to-one assignment, and combines
the observers' estimates by covariance intersection (Julier and Uhlmann 1997), which assumes nothing about their
correlation.  The result is a set of road users U1, U2, ... with a trajectory, a box and the observers that saw them;
a road user is never named after a participant of the scenario.

## Collisions and semantic events

* **Collisions** come from the recorders' collision sensors, matched across recorders as above.  The participants of
  a collision between two recorders are therefore named by both participants' own sensors, not recognised by radar:
  the radar identities are judged separately.  A contact of the same pair within 2 s after the previous one, the
  bodies never more than 1 m apart in between, is a **recontact** of that collision, not a new one.
* **Semantic events** of each recorder (`reconstruction/local.py`, definitions in
  [docs/event_definitions.md](docs/event_definitions.md)): closing, CRITICAL_TTC (a collision course that braking can
  no longer avoid, or an unsafe gap to a leader), EGO_PATH_ENTRY, CUT_IN (a lateral manoeuvre into the recorder's
  path, leaving the target's own lane), braking, stops, indicators, STOP / YIELD signs.  Lanes come from the
  OpenDRIVE map of the incident location.  The global graph places every event on the global clock, with the
  participants' identities where the association established them.

## Isolation of the ground truth

`ground_truth/` (every vehicle's true state and every contact with its partner) and the run's scenario metadata are
read only by the privileged evaluation (`src/cdf/evaluation/`), after the reconstruction has written its files.
The reconstruction reads `vehicles/` and `incident_context.json` only; tests check this by tracing every file the
reconstruction and the RECONSTRUCTION viewer open, and by poisoning the privileged files
(`tests/test_reconstruction_boundary.py`, `tests/test_replay_ghosts.py`, `tests/test_sensor_ground_truth_separation.py`).

## Two viewers

Two independent viewers draw a run in CARLA with the same window, camera, keys and speeds
([docs/REPLAY.md](docs/REPLAY.md)):

* **GROUND TRUTH** (`scripts/view_ground_truth.py`): what CARLA simulated: every vehicle on its true trajectory, the
  collisions (with their recontacts) as they happened;
* **RECONSTRUCTION** (`scripts/replay_run.py`): what the algorithm estimated: the recorders at their GNSS/INS pose,
  the fused road users as boxes, radar tracks, collisions and each recorder's events.

Side by side on two CARLA servers, either window drives both: play, pause, seek, speed, camera and ESC.  Only the
instant on the recording clock, the play state, the speed, the camera and the quit cross between them, never a
position or an event of the other viewer.

## Reproducibility

* **Acquisition.**  The 22 runs were recorded twice in separate processes: 21 are bit-identical, and S04
  `b_rear_first` differs by at most 3.1e-5 m from its A-B contact on, one or two float32 steps at those map
  coordinates, with the same contacts.  S10, the most chaotic impact, gave 6/6 bit-identical repeats
  ([docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)).  The SHA-256 of every raw file is recorded.
* **Reconstruction.**  Re-running the reconstruction on copies of the raw data reproduces every output file byte
  for byte (22/22 runs).
* **Campaign.**  Code, configuration, dataset and protocol are frozen at a tag with a manifest of hashes; every
  random stream is seeded by SHA-256 from (seed, sensor, profile, recorder, axis), never from the order of the jobs.

## Degradation study: GNSS RTK over 5G and radar

The robustness campaign v3 ([docs/CAMPAIGN_V3.md](docs/CAMPAIGN_V3.md)) reconstructs perturbed copies of the 22 runs
with the frozen method, paired with the G0 baseline of the same raw data
([docs/robustness_profiles.md](docs/robustness_profiles.md), sources in [docs/REFERENCES.md](docs/REFERENCES.md)):

| family | conditions | recorders degraded |
|---|---|---|
| GNSS | G1 RTK (P95 0.040 m, 0.14 deg, 0.016 m/s; measured RTK-INS figures), G2 degraded (P99.5 0.50 m, 0.60 deg, 0.20 m/s; stress targets) | all |
| radar | nominal (typical production accuracy), severe (field-of-view edges, twice the misses), extreme (severe with dense clutter: a stress test) | all |
| asymmetric radar | the three levels | each recorder alone; with three recorders, every pair |
| GNSS x radar | {G1, G2} x {nominal, severe} | all |
| asymmetric radar x GNSS | G2 x {nominal, severe} | radar on each subset, GNSS on all |

5G is only the transport of the RTK corrections: no network latency, availability or packet loss is simulated or
claimed.  The method is not re-tuned between conditions.  Stochastic conditions start with 3 seeds; the seed rule adds
one while the standard error over seeds of a headline metric exceeds its tolerance.  It added seeds 3 and 4 to the
two extreme radar conditions, and the campaign was closed there by decision (at most 5 seeds).

## Tests and the campaign

* `python -m pytest -q`: unit and integration tests, among them the ground-truth boundary, the recontact rule, the
  supplied map, the two-way viewer link, the scorecard definitions and the campaign's paired streams.  The
  byte-for-byte determinism of the reconstruction is checked separately, by reconstructing copies of the 22 runs
  ([docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md)).
* `scripts/validate_canonical.py`: the automatic validation of the 22 runs
  ([docs/CANONICAL_VALIDATION.md](docs/CANONICAL_VALIDATION.md)).
* `scripts/campaign_controller.py` (through `scripts/campaign_v3.bat`): the campaign runner.  It verifies the freeze
  against the manifest, runs every job in its own process, adapts the number of workers to the machine, survives the
  terminal, keeps failed jobs with their error, and resumes by skipping the complete ones.

## Data layout

| path | content | in git |
|---|---|---|
| `traces/<S>/run_0_<variant>/vehicles/` | raw recordings of the recorders | yes |
| `traces/.../ground_truth/` | simulator truth (privileged) | yes |
| `traces/.../incident_context.json` | supplied incident context | yes |
| `traces/.../reconstruction/` | the reconstruction and its evaluation (`evaluation/`) | yes |
| `results/` | G0 scorecard, reproducibility records, campaign v3 tables and figures | yes (tables, figures, summaries) |
| `results/robustness/campaign_v3/` | campaign v3 job records of every attempt (`jobs.jsonl.gz`), manifest, controller log | yes (records compressed, 3 MB; SHA-256 in `results/campaign_v3/index.md`) |

Full map and the state of every branch: [docs/REPOSITORY.md](docs/REPOSITORY.md).

## Results

### G0: ideal GNSS/INS and CARLA's radar ([docs/G0_ERROR_ANALYSIS.md](docs/G0_ERROR_ANALYSIS.md))

| quantity | result (22 runs, 95 vehicles, 50 recorders) |
|---|---|
| collisions | 26/26 detected with the right participants, 0 missed, 0 misattributed, 0 invented, report timing error 0.00 s; S04 `a_front_pushed` is one A-B collision with a recontact 0.65 s later.  All 26 are between two recorders, matched from their own collision sensors: this measures the matching of collision reports, not the recognition of a partner by radar |
| road users that record nothing | 45/45 observable vehicles represented; 20 duplicates (dense traffic, S14-S19); 1 recorder ghost (S06); 0 phantoms; represented time over observable time 0.99 median, lowest 0.45 (S16) |
| positions and speeds | centre error median 0.21 m (P95 0.73 m) in steady motion, 0.33 m (P95 1.02 m) in turns; speed error median 0.03 m/s steady, 0.06 m/s in turns |
| associations | 0 wrong recorder links, 0 false merges; 1 missed recorder link (S06); 43 merges left unresolved in dense traffic |
| CRITICAL_TTC | 42/42 justified warnings before the impact; lead time minimum 0.75 s, median 1.53 s |
| validation | 14 PASS, 8 WARN, 0 FAIL ([docs/CANONICAL_VALIDATION.md](docs/CANONICAL_VALIDATION.md)) |

### Degradation study (campaign v3, [docs/CAMPAIGN_V3_REPORT.md](docs/CAMPAIGN_V3_REPORT.md))

1816 jobs on the 22 runs, all complete, from the frozen tag `campaign-v3` (2026-10-23).  Each job is paired with the
G0 job of the same run.  Values are means over seeds; intervals, paired changes and every other measure are in the
report and in [`results/campaign_v3/`](results/campaign_v3/index.md).

| condition | collisions identified | phantoms / job | recorder ghosts / job | coverage | position P95 [m] | CRITICAL_TTC in time |
|---|---|---|---|---|---|---|
| G0 | 1.000 | 0.0 | 0.05 | 0.933 | 0.817 | 1.000 |
| GNSS G1 RTK | 1.000 | 0.0 | 0.05 | 0.933 | 0.848 | 1.000 |
| GNSS G2 degraded | 1.000 | 0.0 | 0.02 | 0.926 | 0.867 | 1.000 |
| radar nominal | 1.000 | 0.6 | 0.06 | 0.927 | 0.971 | 1.000 |
| radar severe | 0.987 | 68.7 | 0.50 | 0.874 | 1.335 | 0.984 |
| radar extreme | 0.954 | 102.4 | 1.79 | 0.887 | 1.556 | 0.919 |
| one radar severe | 0.995 | 30.5 | 0.26 | 0.906 | 1.079 | 0.993 |
| one radar extreme | 0.981 | 45.6 | 0.84 | 0.910 | 1.186 | 0.965 |
| G2 + severe radar | 1.000 | 69.6 | 0.52 | 0.871 | 1.332 | 0.976 |

* **Collisions.**  None of the 2344 true contacts is missed.  The 22 misattributed collisions all occur under severe
  or extreme radar, in four scenarios.  Each comes with an invented single-recorder node and a missed recorder link.
* **Road users that record nothing.**  Every observable vehicle stays represented.  Degraded radar lowers coverage
  (by up to 0.062), splits vehicles (up to 2.45 duplicates per job) and adds phantoms: 97-98 % of them are clutter far
  from any vehicle, and their number is proportional to the number of degraded radars.
* **GNSS.**  Degradation alone (recorder pose P95 0.033 m for G1, 0.311 m for G2) leaves collisions, completeness and
  associations unchanged.  It raises the speed error slightly and the unconfirmed CRITICAL_TTC alarms from 0.09 to
  0.20-0.21 per job.  GNSS and radar effects add up: only four interaction intervals exclude zero, all small.
* **CRITICAL_TTC.**  Warnings are missed only under severe or extreme radar.  Every missed warning was never raised;
  none came late.  S11 `consequential` is the most sensitive case.

## Limitations

* The accidents are simulated.  CARLA's radar casts rays and adds no noise, false alarm or resolution limit; the
  degradation profiles add Gaussian per-detection errors, independent misses and uniform clutter.  Real clutter is
  structured (guardrails, multipath) and real misses depend on the target.
* G0 is an ideal pose, a reference rather than a receiver.  The GNSS profiles are stationary Gaussian processes; they
  do not model RTK float or no-fix episodes, multipath jumps, outages or vertical errors.
* Every collision of the dataset is between two recorders: the identification of a collision with a vehicle that
  records nothing is not tested.
* The method is not re-tuned to a degraded sensor: the degraded conditions measure robustness to errors it does not
  model.
* In dense traffic the fusion leaves some vehicles split over several road users (duplicates) rather than risk a
  false merge.

## Installation and commands

Requirements: Windows, [Miniconda](https://docs.conda.io/en/latest/miniconda.html), and
[CARLA 0.9.15](https://github.com/carla-simulator/carla/releases/tag/0.9.15) (packaged Windows build).  The
reconstruction, the evaluation and the campaign run on saved recordings; CARLA is needed for the viewers, for
recording and, through its OpenDRIVE files, for the road maps.

```bat
git clone https://github.com/AndreaBedei1/causaldrive-forensics.git
cd causaldrive-forensics
conda env create -f environment.yml
conda activate carla
set CARLA_ROOT=F:\Carla9_15\WindowsNoEditor
python -m pytest -q
```

The environment is Python 3.8.20 with the `carla==0.9.15` client and an editable install of this checkout.  Set
`CARLA_ROOT` to the CARLA folder before reconstructing or testing: without it the reconstruction finds no road map
and runs without lanes, silently.

**Both viewers, side by side** (two CARLA servers, each in its own terminal, then the menu of the 22 runs):

```bat
python scripts\start_carla.py --carla-root %CARLA_ROOT% --port 3000
python scripts\start_carla.py --carla-root %CARLA_ROOT% --port 3100
python scripts\review_canonical_runs.py --port 3000 --gt-port 3100 --res 960x540 --speed 0.5
```

In the menu, `N` opens run N in both viewers (GROUND TRUTH left, RECONSTRUCTION right), `Ng` / `Nr` one of them.
Either window drives both: SPACE play/pause, LEFT/RIGHT seek, 1-4 speed, N/P next/previous event, C camera, ESC
closes both.

**One viewer alone** (one server):

```bat
python scripts\replay_run.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\view_ground_truth.py traces\S04\run_0_a_front_pushed --port 3000
python scripts\replay_run.py traces\S10\run_0_deflected_into_c --export out\rec --at -1 --at 0 --at 1
```

**Reconstruction, evaluation, validation:**

```bat
python scripts\reconstruct_run.py traces\S11\run_0_consequential --evaluate
python scripts\hardening_refresh.py --scope canonical --workers 6
python scripts\g0_scorecard.py --canonical --out results\g0_final
python scripts\validate_canonical.py --out docs\CANONICAL_VALIDATION.md
```

**Campaign v3** (from the worktree of the tag `campaign-v3`, [docs/CAMPAIGN_V3.md](docs/CAMPAIGN_V3.md)):

```bat
scripts\campaign_v3.bat start
scripts\campaign_v3.bat status
scripts\campaign_v3.bat pause
scripts\campaign_v3.bat resume
python scripts\campaign_v3_report.py --jobs results\robustness\campaign_v3\jobs.jsonl --out results\campaign_v3
```

The report command reads the uncompressed records (`jobs.jsonl.gz`, see
[`results/campaign_v3/index.md`](results/campaign_v3/index.md)); it regenerates the committed tables and figures
byte for byte.

## Documentation and references

| topic | page |
|---|---|
| Reconstruction method | [METHOD.md](docs/METHOD.md) |
| Semantic events and thresholds | [event_definitions.md](docs/event_definitions.md) |
| Parameters and their evidence | [FINAL_PARAMETER_AUDIT.md](docs/FINAL_PARAMETER_AUDIT.md) |
| Scenarios | [SCENARIOS.md](docs/SCENARIOS.md) |
| Sensors, recording and the ground-truth boundary | [SENSORS_AND_GROUND_TRUTH.md](docs/SENSORS_AND_GROUND_TRUTH.md), [campaign_acquisition.md](docs/campaign_acquisition.md) |
| Viewers | [REPLAY.md](docs/REPLAY.md) |
| Reproducibility | [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) |
| G0 results and error analysis | [G0_ERROR_ANALYSIS.md](docs/G0_ERROR_ANALYSIS.md), [CANONICAL_VALIDATION.md](docs/CANONICAL_VALIDATION.md), [STABILITY_AUDIT.md](docs/STABILITY_AUDIT.md) |
| Degradation profiles and their sources | [robustness_profiles.md](docs/robustness_profiles.md) |
| Campaign v3: design and report | [CAMPAIGN_V3.md](docs/CAMPAIGN_V3.md), [CAMPAIGN_V3_REPORT.md](docs/CAMPAIGN_V3_REPORT.md) |
| **All references** (sensor and profile sources, methods, related work) | [REFERENCES.md](docs/REFERENCES.md) |
| Repository map, branches, data | [REPOSITORY.md](docs/REPOSITORY.md), [PROJECT_STATUS.md](docs/PROJECT_STATUS.md) |
| Positioning of the paper | [paper_positioning.md](docs/paper_positioning.md) |
| Earlier robustness campaign (previous recordings) | [docs/archive/](docs/archive/) |
