**T1_canonical_runs.**  Canonical runs: recorders, road users that recorded nothing, and what the reconstruction recovered (privileged evaluation).

| run | recorders | unrecorded | contacts recon./true | aligned | alignment | max |offset err.| [s] | identities correct/decided | anonymous entities | max |t_global err.| [s] |
|---|---|---|---|---|---|---|---|---|---|
| S01/crash | A B | - | 1/1 | 2/2 | collision | 0.000 | 1/1 | 0 | 0.000 |
| S02/crash | A B | - | 1/1 | 2/2 | collision | 0.000 | 1/1 | 0 | 0.000 |
| S02/critical_before_cut_in | A B | - | 1/1 | 2/2 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S03/crash | A B | - | 1/1 | 2/2 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S06/a_front_pushed | A B C | - | 3/3 | 3/3 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S06/b_rear_first | A B C | - | 2/2 | 3/3 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S07/crash | A B C | - | 1/1 | 3/3 | collision, observed | 0.050 | 2/2 | 0 | 0.050 |
| S08/crash | A B C | - | 1/1 | 3/3 | collision, observed | 0.000 | 6/6 | 0 | 0.000 |
| S09/merge_conflict | A B | - | 1/1 | 2/2 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S10/rolls_through | A B | - | 1/1 | 2/2 | collision | 0.000 | 2/2 | 0 | 0.000 |
| S12/near_simultaneous | A B | - | 1/1 | 2/2 | collision | 0.000 | 4/4 | 0 | 0.000 |
| S15/deflected_into_c | A B C | - | 2/2 | 3/3 | collision | 0.000 | 6/6 | 0 | 0.000 |
| S16/consequential | A B C | - | 2/2 | 3/3 | collision | 0.000 | 6/6 | 1 | 0.100 |
| S17/crash | A B | C | 1/1 | 2/2 | collision | 0.000 | 2/2 | 1 | 0.000 |
| S18/abreast | A B | C D | 1/1 | 2/2 | collision | 0.000 | 2/2 | 4 | 0.000 |
| S18/passing | A B | C D | 1/1 | 2/2 | collision | 0.000 | 2/2 | 2 | 0.000 |
| S18/platoon | A B | C D | 1/1 | 2/2 | collision | 0.000 | 2/2 | 4 | 0.600 |

Alignment: by matched collisions, by observed trajectories, or the reference recorder's own clock (no matched collision).  Errors against simulator time (privileged).
