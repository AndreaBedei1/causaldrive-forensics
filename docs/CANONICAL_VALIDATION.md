# Canonical development set: automatic validation

Manifest: OK (S01..S18, 22 runs)

Reconstruction: the single reconstruction method, `configs/reconstruction.yaml` (configuration digest 925ce7e1cd14); every run is checked to carry exactly this configuration.

| run | status | collisions | recorder/identity decisions | merges (correct/false/missed) | unresolved identities | semantic anomalies | boxes (max at once) | events | warnings / failures |
|---|---|---|---|---|--:|--:|--:|--:|---|
| S01/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 0 | 0 | 19 | - |
| S02/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 0 | 0 | 26 | - |
| S02/run_0_critical_before_cut_in | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0 | 31 | - |
| S03/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0 | 35 | - |
| S04/run_0_a_front_pushed | PASS | 3/3 | correct link 2 | 0/0/0 | 0 | 0 | 0 | 35 | - |
| S04/run_0_b_rear_first | PASS | 2/2 | correct link 2 | 0/0/0 | 0 | 0 | 0 | 32 | - |
| S05/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 0 | 0 | 31 | - |
| S06/run_0_crash | PASS | 1/1 | correct link 7 | 0/0/0 | 0 | 0 | 0 | 62 | - |
| S07/run_0_merge_conflict | PASS | 1/1 | correct link 3 | 0/0/0 | 0 | 0 | 0 | 32 | - |
| S08/run_0_rolls_through | PASS | 1/1 | correct link 4 | 0/0/0 | 0 | 0 | 0 | 46 | - |
| S09/run_0_near_simultaneous | PASS | 1/1 | correct link 5 | 0/0/0 | 0 | 0 | 0 | 55 | - |
| S10/run_0_deflected_into_c | PASS | 2/2 | correct link 6 | 0/0/0 | 0 | 0 | 0 | 92 | - |
| S11/run_0_consequential | PASS | 2/2 | anonymous 2, correct link 5 | 0/0/0 | 0 | 0 | 1 | 58 | - |
| S12/run_0_crash | PASS | 1/1 | anonymous 3, correct link 2 | 3/0/0 | 2 | 0 | 1 | 46 | - |
| S13/run_0_abreast | PASS | 1/1 | anonymous 4, correct link 2 | 2/0/0 | 0 | 0 | 2 | 40 | - |
| S13/run_0_platoon | PASS | 1/1 | anonymous 5, correct link 2 | 4/0/0 | 0 | 0 | 2 | 41 | - |
| S13/run_0_passing | PASS | 1/1 | anonymous 5, correct link 2 | 4/0/0 | 2 | 0 | 2 | 40 | - |
| S14/run_0_surrounded | WARN | 1/1 | anonymous 21, correct link 2 | 9/0/10 | 4 | 0 | 7 | 67 | WARN: 10 missed merge(s) (unresolved identities, conservative) |
| S15/run_0_dense_platoon | WARN | 1/1 | anonymous 19, correct link 1 | 8/0/5 | 0 | 0 | 8 | 57 | WARN: 5 missed merge(s) (unresolved identities, conservative) |
| S16/run_0_overtaking | WARN | 1/1 | anonymous 19, correct link 2 | 10/0/10 | 3 | 0 | 7 | 90 | WARN: 10 missed merge(s) (unresolved identities, conservative) |
| S17/run_0_occlusion_reappearance | WARN | 1/1 | anonymous 12, correct link 2 | 11/0/2 | 0 | 0 | 4 | 67 | WARN: 2 missed merge(s) (unresolved identities, conservative) |
| S18/run_0_collision_ambiguity | WARN | 1/1 | anonymous 15, correct link 1 | 8/0/4 | 2 | 0 | 6 | 61 | WARN: 4 missed merge(s) (unresolved identities, conservative) |
