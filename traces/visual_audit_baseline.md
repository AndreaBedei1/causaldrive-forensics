# Visual audit (visual_audit_baseline)

One row per run: the reviewer's verdict on the reconstruction-only replay frames (details and frames in each run's reconstruction/evaluation/visual_audit_baseline.md).

| scenario | run | verdict | frames | automatic flags | summary |
|---|---|---|---|---|---|
| S01 | run_0_crash | PASS | 5 | 0 | Rear-end: A critical on B 2.35 s before the contact (B braking ahead); END with the COLLISION; bodies in contact at the collision. |
| S02 | run_0_crash | PASS | 7 | 0 | B cuts in from the left ahead of A: CRITICAL_TTC, CUT_IN_FROM_LEFT and EGO_PATH_ENTRY in that order, collision of A's front with B's rear. |
| S02 | run_0_critical_before_cut_in | PASS | 9 | 0 | CRITICAL_TTC (-1.50) before CUT_IN_FROM_LEFT (-1.15) before EGO_PATH_ENTRY (-0.45); B rotated by the impact afterwards. |
| S03 | run_0_crash | PASS | 6 | 0 | Crossing: both recorders critical about 1.5 s before; B strikes the side of A; both episodes end with the collision. |
| S06 | run_0_a_front_pushed | PASS | 10 | 0 | Chain A->B->C: A-B at 0.00 ends the episode of A, B pushed into C at +0.50 ends the episode of B on C; second A-B contact at +0.65. |
| S06 | run_0_b_rear_first | PASS | 8 | 0 | B into C at -1.55 (END B->C), A critical on the stopped chain from -1.55, A into B at 0.00 (END A->B). |
| S07 | run_0_crash | WARN | 7 | 0 | Occluded chain stop consistent (A critical on B, A into B); the recorder C also appears as the anonymous ghost B:track_001 (no B-C collision to associate it); shown on the source clock because C has no collision to be aligned. |
| S08 | run_0_crash | WARN | 8 | 2 | Multi-direction crossing A-B consistent; recorder C seen as two ghosts (A:track_001, B:track_001) and the tracks of A and B by C anonymous; post-impact ghost heading of B:track_001 rotated about 45 deg while B spins. |
| S09 | run_0_merge_conflict | PASS | 7 | 0 | FAIL found and fixed: the CRITICAL_TTC of A on B ended 0.80 s before the collision while B, merging along a curve, was 2-3 m away and closing at 1.6-3.5 m/s (line-of-sight time to contact 0.66-0.83 s); the release now waits until no line-of-sight contact is imminent; both episodes end at the collision. |
| S10 | run_0_rolls_through | WARN | 8 | 2 | Junction collision consistent; the track of A by B stays anonymous (ghost box offset about 1.5 m on A) and its box jumps and spins right after the impact. |
| S12 | run_0_near_simultaneous | PASS | 7 | 0 | All-way stop: both critical about 1.2 s before, B enters the path of A, collision, rotation after. |
| S15 | run_0_deflected_into_c | WARN | 13 | 1 | B into A at 0.00, A deflected into C at +0.90, each episode ends at the collision of its own pair; B:track_001 switches from C to A at the A-C contact (ground truth); several anonymous ghosts of recorders. |
| S16 | run_0_consequential | WARN | 14 | 2 | B into A at 0.00, A into the van C at +1.05; episodes end at their collisions; the van C (a recorder) appears as several anonymous ghosts; the episode of C on A stays open when C loses the track of A 0.15 s before their contact. |
| S17 | run_0_crash | WARN | 11 | 2 | Consistent semantics: A critical on the cutting-in C from -2.35, CUT_IN -2.20, path entry -1.60; A-B and B-A end at the collision, A on C at +0.55; C (records nothing) is drawn as three ghosts. |
