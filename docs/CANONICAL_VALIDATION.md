# Canonical development set: automatic validation

Manifest: OK (S01..S19, 22 runs)

Reconstruction: the single reconstruction method, `configs/reconstruction.yaml` (configuration digest c224d6cae461); every run is checked to carry exactly this configuration.

Stability (privileged audit, `evaluation/stability.json`): EGO_PATH oscillations / phantom tracks / fragmentation losses / duplicate tracks; CUT_IN: true positives / without a true cut-in / missed.

| run | status | collisions | recorder/identity decisions | merges (correct/false/missed) | unresolved identities | semantic anomalies | stability (osc/phantom/frag/dup) | CUT_IN (TP/FP/missed) | boxes (max at once) | events | warnings / failures |
|---|---|---|---|---|--:|--:|---|---|--:|--:|---|
| S01/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 19 | - |
| S02/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 0 | 0/0/0/0 | 1/0/0 | 0 | 26 | - |
| S03/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 34 | - |
| S04/run_0_a_front_pushed | PASS | 2/2 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 35 | - |
| S04/run_0_b_rear_first | PASS | 2/2 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 32 | - |
| S05/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 30 | - |
| S06/run_0_crash | WARN | 1/1 | correct link 5, missed link 1 | 0/0/0 | 0 | 0 | 0/0/1/1 | 0/0/0 | 1 | 54 | WARN: 1 missed recorder link(s) (a track of a recorder left anonymous); WARN: 1 track loss(es) while the radar kept measuring the body; WARN: 1 simultaneous duplicate track(s) |
| S07/run_0_merge_conflict | WARN | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/1 | 0 | 34 | WARN: true cut-in not reported: [['B', 'A', 5.25]] |
| S08/run_0_rolls_through | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 35 | - |
| S09/run_0_near_simultaneous | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 52 | - |
| S10/run_0_deflected_into_c | PASS | 2/2 | correct link 6 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 58 | - |
| S11/run_0_consequential | PASS | 2/2 | correct link 4 | 0/0/0 | 0 | 0 | 0/0/0/0 | 0/0/0 | 0 | 50 | - |
| S12/run_0_crash | PASS | 1/1 | anonymous 3, correct link 2 | 3/0/0 | 2 | 0 | 0/0/0/0 | 2/0/0 | 1 | 42 | - |
| S13/run_0_abreast | PASS | 1/1 | anonymous 4, correct link 2 | 2/0/0 | 0 | 0 | 0/0/0/0 | 1/0/0 | 2 | 42 | - |
| S13/run_0_platoon | PASS | 1/1 | anonymous 5, correct link 2 | 4/0/0 | 0 | 0 | 0/0/0/0 | 1/0/0 | 2 | 43 | - |
| S13/run_0_passing | PASS | 1/1 | anonymous 5, correct link 2 | 4/0/0 | 2 | 0 | 0/0/0/0 | 1/0/0 | 2 | 42 | - |
| S14/run_0_surrounded | WARN | 1/1 | anonymous 21, correct link 2 | 11/0/8 | 4 | 0 | 0/0/0/0 | 0/0/1 | 8 | 61 | WARN: 8 missed merge(s) (unresolved identities, conservative); WARN: true cut-in not reported: [['B', 'A', 6.5]] |
| S15/run_0_dense_platoon | WARN | 1/1 | anonymous 18, correct link 1 | 8/0/7 | 2 | 0 | 0/0/0/0 | 0/0/0 | 8 | 56 | WARN: 7 missed merge(s) (unresolved identities, conservative) |
| S16/run_0_overtaking | WARN | 1/1 | anonymous 19, correct link 2 | 8/0/10 | 3 | 0 | 0/0/0/0 | 0/0/0 | 7 | 82 | WARN: 10 missed merge(s) (unresolved identities, conservative) |
| S17/run_0_occlusion_reappearance | WARN | 1/1 | anonymous 12, correct link 2 | 11/0/2 | 2 | 0 | 0/0/0/0 | 1/0/0 | 4 | 68 | WARN: 2 missed merge(s) (unresolved identities, conservative) |
| S18/run_0_collision_ambiguity | WARN | 1/1 | anonymous 15, correct link 1 | 7/0/5 | 1 | 0 | 0/0/0/0 | 0/0/0 | 7 | 58 | WARN: 5 missed merge(s) (unresolved identities, conservative) |
| S19/run_0_highway_curve | WARN | 1/1 | anonymous 16, correct link 2 | 10/0/11 | 3 | 0 | 0/0/0/0 | 1/0/0 | 6 | 70 | WARN: 11 missed merge(s) (unresolved identities, conservative) |
