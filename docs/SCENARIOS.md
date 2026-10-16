# Canonical scenarios

19 scenarios, 22 runs, each reviewed manually in the replay.  Scenario definitions: `configs/scenarios/`; manifest of
the set: `scripts/validate_canonical.py`; automatic validation: [CANONICAL_VALIDATION.md](CANONICAL_VALIDATION.md);
sensors and recording prerequisites: [campaign_acquisition.md](campaign_acquisition.md).

| id | scenario | runs | what it tests |
|---|---|---|---|
| S01 | rear_end | crash | rear-end collision, two recorders |
| S02 | cut_in | crash | cut-in collision |
| S03 | crossing | crash | crossing collision at a junction |
| S04 | chain_collision | a_front_pushed, b_rear_first | three-car chain, two orders of contacts |
| S05 | occluded_chain_stop | crash | chain with an occluded leader |
| S06 | multidirection_crossing | crash | three vehicles from different directions |
| S07 | roundabout | merge_conflict | merge conflict in a roundabout, both drivers signalling (Town03) |
| S08 | single_stop_a | rolls_through | a vehicle rolls through a STOP while signalling its turn |
| S09 | all_way_stop | near_simultaneous | near-simultaneous arrivals at an all-way stop |
| S10 | intersection_pileup | deflected_into_c | pile-up, a car deflected into a third |
| S11 | secondary_collision | consequential | a secondary collision after the first |
| S12 | unobserved_causal_vehicle | crash | a causally relevant car that records nothing |
| S13 | anonymous_pair | abreast, platoon, passing | two nearby non-recording cars kept apart |
| S14 | dense_abreast | surrounded | dense abreast traffic, one sideswipe |
| S15 | dense_platoon | dense_platoon | dense column with adjacent traffic, rear-end |
| S16 | dense_overtaking | overtaking | identities through passes, sideswipe while overtaking |
| S17 | occlusion_reappearance | occlusion_reappearance | identity across an occlusion up to a collision |
| S18 | collision_ambiguity | collision_ambiguity | several similar cars around a rear-end contact |
| S19 | highway_curve | highway_curve | four-lane motorway curve (Town04) with side-by-side traffic and a cut-in |

## Run folders

```
traces\<id>\run_0_<run>\
  vehicles\<recorder>\    raw onboard recordings: radar, ego pose and motion, controls, collisions, lights, signs
  ground_truth\           simulator truth, read by the evaluation only
  reconstruction\         the reconstruction, regenerated from vehicles\ (local graphs, global\, evaluation\)
```

## Commands

```bat
conda activate carla

:: reconstruct one run from its raw recordings, then evaluate it against ground truth
python scripts\reconstruct_run.py traces\S11\run_0_consequential --evaluate

:: validate the whole canonical set (after reconstruction and evaluation)
python scripts\validate_canonical.py --out docs\CANONICAL_VALIDATION.md

:: record a scenario on the project's CARLA server (port 3000); use a scratch output for trials
python scripts\start_carla.py
python scripts\run_scenario.py --scenario S14 --output scratch\trial --no-autostart
python scripts\check_scenario_run.py scratch\trial\S14\run_0_surrounded --expect A-B
```
