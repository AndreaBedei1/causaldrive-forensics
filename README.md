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
  touching it.  A part of a known body seen apart is never a second vehicle.  A target that crashes ahead
  keeps its track through the abrupt slowdown or rebound (no foreign return inside its own body region).
* **Alignment** on the collisions the recorders report: a pairing is refused when the pose streams put the
  bodies apart or a recorder's own radar view of the contact contradicts the partner's speed in the observed
  direction.
* **Identity** (`reconstruction/identity.py`).  Recorder links use the relative pose uncertainty and the
  line-of-sight (Doppler) velocity, and are conservative: one recorder per observer and instant unless
  same-body evidence joins two fragments.  Anonymous road users come from one-box evidence across observers,
  cannot-link constraints, one-to-one assignment and a stitch posterior against a new road user.  Two
  observers seeing one body at the same instants are tested on every shared instant, also outside the
  relevance envelope (no two superimposed boxes of one car); a brief overlap (5-9 instants) must pass at
  every instant, a long one (30+) by majority; after an observer's own collision its velocity estimates are
  not compared (geometry decides).  A track that is the same body as another observer's track of recorder X
  inherits X (and no other recorder).  Ambiguity stays UNRESOLVED.  A retrospective resolution may
  name an earlier observation from later evidence by several observers, against every other earlier
  candidate and a new road user; no sample, event or timestamp moves.
* **Semantics**: the recorder's path corridor follows the lane it drives in (public OpenDRIVE map of the CARLA
  installation, recognised from the recorder's own positions; at a junction the branch it takes later): cars
  following one bend are not in its path.  CUT_IN needs a lateral manoeuvre of the target toward that path,
  leaving its own lane, confirmed by its EGO_PATH_ENTRY; none starts after the recorder's own collision.
  CRITICAL_TTC is PREDICTED_OVERLAP (a collision course braking cannot avoid: crossings, merges) or
  UNSAFE_FORWARD_GAP, which only a leader can cause: a target in the recorder's path or in a confirmed cut-in,
  never a car abreast.  A collision course that only the target's motion across its own lane creates counts
  when that motion is confirmed (it enters the recorder's path or strikes it); otherwise the car keeps its
  lane (a car passing beside the recorder, whose radar point slides over its faces, is no threat).  A pair's
  episode ends at their collision (also when only the fusion knows that the track was the partner) and does
  not restart while they touch.
* **Global graph**: after two road users have touched, a CRITICAL_TTC between that same pair is suppressed in
  the global graph and the replay; the raw local evidence stays in the local graphs.

## Environment: Python 3.8 only

One checkout, one environment: the conda environment `carla` (Python 3.8.20, CARLA 0.9.15 client).  No other
Python version is supported.

```bat
conda activate carla
python --version                                   :: Python 3.8.20
python -c "import carla; print(carla.__file__)"    :: CARLA 0.9.15 client
python -c "import cdf; print(cdf.__file__)"        :: this checkout's src\cdf
```

CARLA 0.9.15 (`Desktop\Carla9_15\WindowsNoEditor`), the project's private server on **port 3000** (traffic
manager 8100; port 2000 is left to other users).  To recreate the environment:
`conda env create -f environment.yml` (Python 3.8.20, `requirements.txt`, editable install of this checkout).

## Replay the canonical scenarios

Start CARLA 0.9.15 first, either your own server (port 2000) or the project's private one (port 3000):

```bat
conda activate carla
:: the project's own server on port 3000 (Ctrl-C stops it); skip it when your CARLA already runs on port 2000
python scripts\start_carla.py
```

Then, in a second terminal, the review menu of the 22 canonical runs (pick a number, the replay opens; close it
to come back; `q` quits).  The .bat uses the server on port 2000; with the project's server pass `--port 3000`:

```bat
conda activate carla
:: your CARLA on port 2000
scripts\review_canonical_runs.bat
:: or the project's server on port 3000
python scripts\review_canonical_runs.py --port 3000
```

One run directly: `python scripts\replay_run.py traces\S14\run_0_surrounded --port 2000` (add `--start 5
--speed 0.25` to begin at 5 s in slow motion).

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

:: replay one run, or pick one from the review menu of the 22 canonical runs
python scripts\replay_run.py traces\S14\run_0_surrounded
scripts\review_canonical_runs.bat

:: tests
python -m pytest -q
```

## Frozen robustness and generalization campaign

Protocol: [docs/FROZEN_CAMPAIGN.md](docs/FROZEN_CAMPAIGN.md) (tag `pre-robustness-campaign`); results and figures
under `results/robustness/frozen_campaign/` and `results/generalization/frozen_campaign/`; the report (written after the campaign):
[docs/ROBUSTNESS_CAMPAIGN.md](docs/ROBUSTNESS_CAMPAIGN.md).

```bat
:: from a clean checkout of the tag; every job refuses another commit or a modified tracked file
git checkout pre-robustness-campaign
set CDF_ANALYSIS_FREEZE_COMMIT=<commit of the tag>
python scriptsreeze_manifest.py --workers 14

:: robustness: every family on the 22 canonical runs (resumable: rerun the same command after an interruption)
python scriptsobustness.py --canonical --workers 14 --work robustnessrozen_campaign --results resultsobustnessrozen_campaign
python scripts\campaign_report.py robustness

:: held-out generalization (private CARLA on port 3000): static check, record, evaluate, report
python scripts\generalization.py check
python scripts\generalization.py record
python scripts\generalization.py evaluate --workers 8
python scripts\generalization.py report
```

## Canonical scenarios (development set: 19 scenarios, 22 runs)

| id | scenario | runs | purpose |
|---|---|---|---|
| S01 | rear_end | crash | rear-end collision, two recorders |
| S02 | cut_in | crash | cut-in collision |
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
| S14 | dense_abreast | surrounded | dense abreast traffic ahead of the recorders (nobody behind), one sideswipe |
| S15 | dense_platoon | dense_platoon | dense column with adjacent traffic, rear-end |
| S16 | dense_overtaking | overtaking | identities through passes, sideswipe while overtaking |
| S17 | occlusion_reappearance | occlusion_reappearance | identity across an occlusion up to a collision (nobody behind) |
| S18 | collision_ambiguity | collision_ambiguity | several similar cars around a rear-end contact, on the straight after a bend |
| S19 | highway_curve | highway_curve | four-lane motorway curve (Town04, radius about 185 m) with side-by-side traffic; a cut-in on the curve ends in a rear-end contact |

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
| TAB | next recorder (follow camera); its panel is the full one |
| F | focus: the selected recorder's panel takes the right-hand column, the others shrink to their headers (F again: normal layout) |
| PgUp / PgDn | the full panel's events: older / newer (every event reachable) |
| T | radar tracks on / off |
| G | ghost boxes or dots for unfused tracks |
| H | help |
| R | restart |
| ESC | quit |
| free camera | W/A/S/D/Q/E move (SHIFT faster), mouse drag to look, wheel to zoom |

The upper-left panel shows the run, its time, the replay state, the camera and the last and next event.
The panel of each recorder on the right shows what that recorder perceives and does, in two sections.  Its
CURRENT state: its own (`ego: MOVING, BRAKE, INDICATOR_LEFT`; the turn indicators from its own light log, the
replayed vehicle's indicator blinking too, absent when the recording has no light log), one line per local track holding an active state, named after
the fusion's identity (`track_001 (B): CLOSING, CRITICAL_TTC`), its anonymous tracks and the road users it sees
-- at most 8 lines, then `... +N more`, its own state and the alerts (CRITICAL_TTC, CUT_IN) kept first.  Then
its RECENT EVENTS, newest first, each with its age and the global subject, and for a path entry or exit what
changed the occupancy (`-0.4 s  EGO_PATH_ENTRY → C (by own lateral motion)`), the recorder's own COLLISION events
in red and counted in the section line: up to 15 at a time for the selected recorder (TAB; PgUp / PgDn scroll
through its whole history when they do not fit, long lines wrap), the 3 latest for the others.  F (or `--focus`)
gives the selected recorder the whole column down to the timeline, the others reduced to their headers, e.g.
`python scripts/replay_run.py traces/S04/run_0_a_front_pushed --focus --follow B`.  UNKNOWN states
and the measured/predicted provenance stay in the reconstruction files.  A coloured
line joins a recorder to a vehicle it holds CRITICAL_TTC or CUT_IN about, and to the nearest vehicle in its
path, labelled with their body-to-body clearance (`1.4 m`).

## Documentation

- [Event definitions](docs/event_definitions.md): semantic events, body geometry and thresholds.
- [Parameter audit](docs/FINAL_PARAMETER_AUDIT.md): every reconstruction parameter, its category and evidence.
- [Robustness profiles](docs/robustness_profiles.md): pose, radar and impulse perturbations of the campaign.
- [Frozen campaign protocol](docs/FROZEN_CAMPAIGN.md) and [report](docs/ROBUSTNESS_CAMPAIGN.md).
- [Sensors and acquisition](docs/campaign_acquisition.md): radar geometry and recording prerequisites.
- [Paper positioning](docs/paper_positioning.md): framing, logging prerequisites, related work, limitations.
- [Bibliography](docs/bibliography.md).
