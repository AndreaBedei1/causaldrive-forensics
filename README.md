# CarlaGraph / causaldrive-forensics

Accident reconstruction from partial onboard recordings.  Each vehicle that recorded something contributes
only its own data, on its own clock: radar returns, pose and motion, controls and collision callbacks.  From
those recordings the project reconstructs what happened between all road users, including the ones that
recorded nothing, and replays the reconstruction.

```
onboard raw recordings (per recording vehicle)
  -> local reconstruction    radar tracks, ego motion, local semantic events (CLOSING, CRITICAL_TTC, CUT_IN, ...)
  -> temporal alignment      on the collisions the recorders share (else on what they observed of each other)
  -> identity association    which local track is which recorder; exclusive per observer and instant
  -> anonymous road users    road users that recorded nothing, fused from the recorders' radar views (U1, U2, ...)
  -> global semantic graph   one event trace on the global clock
  -> replay / evaluation
```

* Ground truth is used **only** for evaluation and scenario validation: never in tracking, fusion, alignment,
  collision matching or the normal replay.
* Road users that recorded nothing are reconstructed from the recorders' observations alone.
* The replay shows the reconstruction, not the simulator state: recorder vehicles are CARLA actors moved along
  their own recorded poses; reconstructed road users are boxes.
* No LLM or external API in the pipeline; no scenario-specific reconstruction rules.  Ambiguity is left
  unresolved: a false merge is worse than an unresolved identity.

## Reconstruction method

There is one reconstruction method; `configs/reconstruction.yaml` holds its parameters and no option selects
another algorithm ([parameter audit](docs/FINAL_PARAMETER_AUDIT.md)).

* **Radar tracking** (`reconstruction/tracking.py`).  A return joins a track when its Mahalanobis distance is
  inside the 99 % gate of S = the track's predicted covariance + the spread of a vehicle body + the radar's
  polar noise at the return's range (the lateral uncertainty grows with range).  Its Doppler speed is tested
  along its own line of sight only; the tangential velocity, which Doppler does not measure, is never tested.
  A return two tracks explain within a likelihood ratio of 20 is ambiguous and updates neither.  A track
  survives while its predicted position can still tell two bodies a car width apart (2 s cap), is confirmed
  after 0.2 s of support and 3 updates, and a recorder's own impact widens the covariance of the tracks
  touching it.  A part of a known body seen apart is never a second vehicle.
* **Alignment** on the collisions the recorders report: a pairing is refused when the pose streams put the
  bodies apart or a recorder's own radar view of the contact contradicts the partner's speed in the observed
  direction.
* **Identity** (`reconstruction/identity.py`).  Recorder links use the relative pose uncertainty and are
  conservative: one recorder per observer and instant unless same-body evidence joins two fragments.
  Anonymous road users come from one-box evidence across observers, cannot-link constraints, one-to-one
  assignment and a stitch posterior against a new road user; ambiguity stays UNRESOLVED.  A retrospective
  resolution may name an earlier observation from later strong evidence; no sample, event or timestamp moves.
* **Global graph**: after two road users have touched, a CRITICAL_TTC between that same pair is suppressed in
  the global graph and the replay; the raw local evidence stays in the local graphs.

## Environment (the only one)

```bat
conda activate carla
python --version                                   :: Python 3.8.20
python -c "import carla; print(carla.__file__)"    :: CARLA 0.9.15 client
python -c "import cdf; print(cdf.__file__)"        :: this checkout's src\cdf
```

CARLA 0.9.15 (`Desktop\Carla9_15\WindowsNoEditor`), the project's private server on **port 3000** (traffic
manager 8100; port 2000 is left to other users).  To recreate the environment:
`conda env create -f environment.yml` (Python 3.8.20, `requirements.txt`, editable install of this checkout).

## Commands

```bat
:: start the CARLA server on port 3000 (stops only the engine it started; Ctrl-C to quit)
python scripts\start_carla.py

:: record a scenario (writes traces\<id>\run_<seed>_<variant>; use a scratch --output for trials)
python scripts\run_scenario.py --scenario S14 --output scratch\trial
python scripts\check_scenario_run.py scratch\trial\S14\run_0_surrounded --expect A-B
python scripts\scenario_density.py scratch\trial\S14\run_0_surrounded

:: reconstruct and evaluate one run (evaluation reads ground truth only after the reconstruction is written)
python scripts\reconstruct_run.py traces\S11\run_0_consequential --evaluate

:: reconstruct + evaluate + fusion metrics + event oracle for one run, then validate the whole canonical set
python -c "import sys; sys.path[:0]=['scripts','src']; import hardening_refresh as h; h.refresh('traces/S11/run_0_consequential')"
python scripts\validate_canonical.py --out docs\CANONICAL_VALIDATION.md

:: replay one run, or pick one from the review menu of the 23 canonical runs
python scripts\replay_run.py traces\S14\run_0_surrounded
scripts\review_canonical_runs.bat

:: tests
python -m pytest -q
```

## Canonical scenarios (development set: 19 scenarios, 23 runs)

| id | scenario | runs | purpose |
|---|---|---|---|
| S01 | rear_end | crash | rear-end collision, two recorders |
| S02 | cut_in | crash, critical_before_cut_in | cut-in collision; critical state before the cut-in |
| S03 | crossing | crash | crossing collision at a junction |
| S04 | chain_collision | a_front_pushed, b_rear_first | three-car chain, two orders of contacts |
| S05 | occluded_chain_stop | crash | chain with an occluded leader |
| S06 | multidirection_crossing | crash | three vehicles from different directions |
| S07 | roundabout | merge_conflict | merge conflict in a roundabout (Town03_Opt) |
| S08 | single_stop_a | rolls_through | a vehicle rolls through a STOP |
| S09 | all_way_stop | near_simultaneous | near-simultaneous arrivals at an all-way stop |
| S10 | intersection_pileup | deflected_into_c | pile-up, a car deflected into a third |
| S11 | secondary_collision | consequential | a secondary collision after the first |
| S12 | unobserved_causal_vehicle | crash | a causally relevant car that records nothing |
| S13 | anonymous_pair | abreast, platoon, passing | two nearby non-recording cars kept apart |
| S14 | dense_abreast | surrounded | dense abreast traffic around the recorders, one sideswipe |
| S15 | dense_platoon | dense_platoon | dense column with adjacent traffic, rear-end |
| S16 | dense_overtaking | overtaking | identities through passes, sideswipe while overtaking |
| S17 | occlusion_reappearance | occlusion_reappearance | identity across an occlusion up to a collision |
| S18 | far_to_near | far_to_near | far ambiguous identities resolved as cars approach |
| S19 | collision_ambiguity | collision_ambiguity | several similar cars within the pose uncertainty of a contact |

Run folders: `traces\<id>\run_0_<run>\` with the raw recordings (`vehicles\`), the privileged
`ground_truth\` (evaluation only) and the reconstruction (`reconstruction\`, regenerated from the raw recordings
with the method above).
Validation of the set: [docs/CANONICAL_VALIDATION.md](docs/CANONICAL_VALIDATION.md).  The final experimental
campaign (frozen code, parameters and scenarios; predeclared held-out seeds) has not been run.

## Replay controls

| key | action |
|---|---|
| SPACE | play / pause |
| LEFT / RIGHT | seek 0.5 s (SHIFT: 0.05 s) |
| N / P | next / previous reconstructed event |
| 1-4 | speed 0.25 / 0.5 / 1 / 2x |
| C | camera: overview -> follow each recorder vehicle in turn -> free -> overview |
| TAB | next recorder (follow camera) |
| T | radar tracks on / off |
| G | ghost boxes or dots for unfused tracks |
| H | help |
| R | restart |
| ESC | quit |
| free camera | W/A/S/D/Q/E move (SHIFT faster), mouse drag to look, wheel to zoom |

The panels on the right list, per recorder, its recent semantic events first, then its confirmed states per
global road user (CRITICAL_TTC, CUT_IN, IN_EGO_PATH) and its own braking; at most a few lines.  Raw track ids,
UNKNOWN states and the measured/predicted provenance stay in the reconstruction files.

## Documentation

- [Event definitions](docs/event_definitions.md): semantic events, body geometry and thresholds.
- [Parameter audit](docs/FINAL_PARAMETER_AUDIT.md): every reconstruction parameter, its category and evidence.
- [Robustness profiles](docs/robustness_profiles.md): pose, radar and impulse perturbations of the campaign.
- [Sensors and acquisition](docs/campaign_acquisition.md): radar geometry and recording prerequisites.
- [Paper positioning](docs/paper_positioning.md): framing, logging prerequisites, related work, limitations.
- [Bibliography](docs/bibliography.md).
