# Stability audit (privileged: ground truth used for evaluation only)

Track losses: *fragm.* = the radar kept measuring the true body in at least half of the next 0.5 s (a tracker decision), *sparse* = it measured it only now and then, *no returns* = a sensing loss.

| run | rec | tracks | births | lost | fragm. | sparse | no returns | phantom | dup s | ENTRY | EXIT | osc. | path jumps | traj. jumps |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| S01/run_0_crash | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S01/run_0_crash | B | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S02/run_0_crash | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S02/run_0_crash | B | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| S03/run_0_crash | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S03/run_0_crash | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S04/run_0_a_front_pushed | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S04/run_0_a_front_pushed | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S04/run_0_a_front_pushed | C | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S04/run_0_b_rear_first | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| S04/run_0_b_rear_first | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S04/run_0_b_rear_first | C | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S05/run_0_crash | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S05/run_0_crash | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S05/run_0_crash | C | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S06/run_0_crash | A | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S06/run_0_crash | B | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S06/run_0_crash | C | 3 | 3 | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| S07/run_0_merge_conflict | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S07/run_0_merge_conflict | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S08/run_0_rolls_through | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S08/run_0_rolls_through | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S09/run_0_near_simultaneous | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S09/run_0_near_simultaneous | B | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 |
| S10/run_0_deflected_into_c | A | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S10/run_0_deflected_into_c | B | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | None | 0 |
| S10/run_0_deflected_into_c | C | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S11/run_0_consequential | A | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| S11/run_0_consequential | B | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S11/run_0_consequential | C | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S12/run_0_crash | A | 2 | 2 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| S12/run_0_crash | B | 3 | 3 | 2 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S13/run_0_abreast | A | 3 | 3 | 2 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| S13/run_0_abreast | B | 3 | 3 | 2 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S13/run_0_platoon | A | 3 | 3 | 2 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| S13/run_0_platoon | B | 4 | 4 | 3 | 0 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S13/run_0_passing | A | 3 | 3 | 2 | 0 | 0 | 2 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| S13/run_0_passing | B | 4 | 4 | 3 | 0 | 1 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S14/run_0_surrounded | A | 9 | 9 | 2 | 0 | 0 | 2 | 0 | 0 | 4 | 1 | 0 | 1 | 0 |
| S14/run_0_surrounded | B | 14 | 14 | 8 | 0 | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S15/run_0_dense_platoon | A | 10 | 10 | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S15/run_0_dense_platoon | B | 9 | 9 | 8 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S16/run_0_overtaking | A | 11 | 11 | 6 | 0 | 0 | 6 | 0 | 0 | 4 | 0 | 0 | 0 | 0 |
| S16/run_0_overtaking | B | 10 | 10 | 6 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S17/run_0_occlusion_reappearance | A | 8 | 8 | 4 | 0 | 0 | 4 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| S17/run_0_occlusion_reappearance | B | 6 | 6 | 5 | 0 | 0 | 5 | 0 | 0 | 2 | 0 | 0 | 1 | 0 |
| S18/run_0_collision_ambiguity | A | 10 | 10 | 9 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S18/run_0_collision_ambiguity | B | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| S19/run_0_highway_curve | A | 11 | 11 | 9 | 0 | 4 | 5 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| S19/run_0_highway_curve | B | 7 | 7 | 5 | 0 | 0 | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| **total** | | 169 | 169 | 88 | 2 | 8 | 78 | 0 | 0.00 | 35 | 4 | 0 | 10 | 3 |

| run | CUT_IN found | true | TP | FP | missed | onset errors (s) | closure violations | wrong links | false merges | missed merges |
|---|--:|--:|--:|---|---|---|--:|--:|--:|--:|
| S01/run_0_crash | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S02/run_0_crash | 1 | 1 | 1 | - | - | [-0.1] | 0 | 0 | 0 | 0 |
| S03/run_0_crash | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S04/run_0_a_front_pushed | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S04/run_0_b_rear_first | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S05/run_0_crash | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S06/run_0_crash | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S07/run_0_merge_conflict | 0 | 1 | 0 | - | [('B', 'A', 5.25)] | - | 0 | 0 | 0 | 0 |
| S08/run_0_rolls_through | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S09/run_0_near_simultaneous | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S10/run_0_deflected_into_c | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S11/run_0_consequential | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 0 |
| S12/run_0_crash | 2 | 2 | 2 | - | - | [0.0, 0.0] | 0 | 0 | 0 | 0 |
| S13/run_0_abreast | 1 | 1 | 1 | - | - | [0.0] | 0 | 0 | 0 | 0 |
| S13/run_0_platoon | 1 | 1 | 1 | - | - | [-0.0] | 0 | 0 | 0 | 0 |
| S13/run_0_passing | 1 | 1 | 1 | - | - | [-0.0] | 0 | 0 | 0 | 0 |
| S14/run_0_surrounded | 0 | 1 | 0 | - | [('B', 'A', 6.5)] | - | 0 | 0 | 0 | 8 |
| S15/run_0_dense_platoon | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 7 |
| S16/run_0_overtaking | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 10 |
| S17/run_0_occlusion_reappearance | 1 | 1 | 1 | - | - | [0.05] | 0 | 0 | 0 | 2 |
| S18/run_0_collision_ambiguity | 0 | 0 | 0 | - | - | - | 0 | 0 | 0 | 5 |
| S19/run_0_highway_curve | 1 | 1 | 1 | - | - | [0.05] | 0 | 0 | 0 | 11 |

Losses, phantoms, duplicates and oscillations in detail: the JSON output.
