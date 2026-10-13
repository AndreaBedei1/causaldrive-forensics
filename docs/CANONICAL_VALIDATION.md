# Canonical development set: automatic validation

Manifest: OK (S01..S19, 23 runs)

| run | status | collisions | recorder/identity decisions | merges (correct/false/missed) | boxes (max at once) | events | warnings / failures |
|---|---|---|---|---|--:|--:|---|
| S01/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 19 | - |
| S02/run_0_crash | PASS | 1/1 | correct link 1 | 0/0/0 | 0 | 26 | - |
| S02/run_0_critical_before_cut_in | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 31 | - |
| S03/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 34 | - |
| S04/run_0_a_front_pushed | PASS | 3/3 | correct link 2 | 0/0/0 | 0 | 35 | - |
| S04/run_0_b_rear_first | PASS | 2/2 | correct link 2 | 0/0/0 | 0 | 32 | - |
| S05/run_0_crash | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 30 | - |
| S06/run_0_crash | PASS | 1/1 | correct link 6 | 0/0/0 | 0 | 59 | - |
| S07/run_0_merge_conflict | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 35 | - |
| S08/run_0_rolls_through | PASS | 1/1 | correct link 2 | 0/0/0 | 0 | 34 | - |
| S09/run_0_near_simultaneous | PASS | 1/1 | correct link 4 | 0/0/0 | 0 | 50 | - |
| S10/run_0_deflected_into_c | PASS | 2/2 | correct link 6 | 0/0/0 | 0 | 67 | - |
| S11/run_0_consequential | WARN | 2/2 | correct link 6, missed link 1 | 0/0/0 | 1 | 51 | WARN: 1 missed recorder link(s) (a track of a recorder left anonymous) |
| S12/run_0_crash | PASS | 1/1 | anonymous 3, correct link 2 | 3/0/0 | 1 | 45 | - |
| S13/run_0_abreast | WARN | 1/1 | anonymous 7, correct link 2 | 4/0/5 | 3 | 47 | WARN: 5 missed merge(s) (unresolved identities, conservative) |
| S13/run_0_platoon | WARN | 1/1 | anonymous 7, correct link 2 | 4/0/5 | 3 | 44 | WARN: 5 missed merge(s) (unresolved identities, conservative) |
| S13/run_0_passing | PASS | 1/1 | anonymous 6, correct link 2 | 6/0/0 | 2 | 42 | - |
| S14/run_0_surrounded | WARN | 1/1 | anonymous 25, correct link 2 | 8/0/16 | 10 | 85 | WARN: 16 missed merge(s) (unresolved identities, conservative) |
| S15/run_0_dense_platoon | WARN | 1/1 | anonymous 18, correct link 1 | 8/0/7 | 8 | 68 | WARN: 7 missed merge(s) (unresolved identities, conservative) |
| S16/run_0_overtaking | WARN | 1/1 | anonymous 21, correct link 2 | 7/0/16 | 8 | 110 | WARN: 16 missed merge(s) (unresolved identities, conservative) |
| S17/run_0_occlusion_reappearance | WARN | 1/1 | anonymous 18, correct link 2 | 19/0/3 | 5 | 84 | WARN: 3 missed merge(s) (unresolved identities, conservative) |
| S18/run_0_far_to_near | WARN | 1/1 | anonymous 18, correct link 2 | 16/0/10 | 7 | 91 | WARN: 10 missed merge(s) (unresolved identities, conservative) |
| S19/run_0_collision_ambiguity | WARN | 1/1 | anonymous 16, correct link 2, missed link 1 | 6/0/9 | 9 | 74 | WARN: 1 missed recorder link(s) (a track of a recorder left anonymous); WARN: 9 missed merge(s) (unresolved identities, conservative) |
