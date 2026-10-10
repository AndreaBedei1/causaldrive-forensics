# Visual audit (visual_audit_phase2)

One row per run: the reviewer's verdict on the reconstruction-only replay frames (details and frames in each run's reconstruction/evaluation/visual_audit_phase2.md).

| scenario | run | verdict | frames | automatic flags | summary |
|---|---|---|---|---|---|
| S01 | run_0_crash | PASS | 5 | 0 | Rear-end: A critical on B 2.35 s before the contact; END with the COLLISION; bodies in contact. Unchanged since phase 0. |
| S02 | run_0_crash | PASS | 7 | 0 | B cuts in from the left ahead of A: CRITICAL_TTC, CUT_IN_FROM_LEFT and EGO_PATH_ENTRY in that order; unchanged since phase 0. |
| S02 | run_0_critical_before_cut_in | PASS | 9 | 0 | CRITICAL_TTC (-1.50) before CUT_IN_FROM_LEFT (-1.15) before EGO_PATH_ENTRY (-0.45); unchanged since phase 0. |
| S03 | run_0_crash | PASS | 6 | 0 | Crossing: both recorders critical about 1.5 s before; B strikes the side of A; both episodes end with the collision; unchanged. |
| S06 | run_0_a_front_pushed | PASS | 10 | 0 | Chain A->B->C with three contacts; every episode ends at the collision of its own pair; unchanged. |
| S06 | run_0_b_rear_first | PASS | 8 | 0 | B into C at -1.55, A critical on the stopped chain, A into B at 0.00; unchanged. |
| S07 | run_0_crash | WARN | 7 | 0 | Now replayed on t_global (phase 0: source clock).  Recorder C has no global clock -- its observed trajectory fits two offsets 0.35 s apart (C barely moves) -- so it is not replayed and the panel says so; B's track of C is the anonymous road user U1, drawn once. |
| S08 | run_0_crash | WARN | 8 | 2 | Phase-0 WARNs resolved: C aligned by its observed trajectory (on t_global), A's and B's tracks of C drawn as dots on C, C's track of A linked to A.  Remaining: U1 = C:track_002, B's track by C until the A-B contact, then the A-B pair (identity switch, left anonymous): a grey box on B before the contact, next to A after it. |
| S09 | run_0_merge_conflict | PASS | 7 | 0 | Roundabout merge: both episodes end at the collision (phase-0 FAIL fixed and preserved); EGO_PATH_ENTRY of A on B at -4.95 reflects the straight-ahead corridor (documented limitation). |
| S10 | run_0_rolls_through | PASS | 8 | 0 | Phase-0 WARN resolved: B's track of A is linked to A in the common frame (no second body on A, no post-impact ghost spin). |
| S12 | run_0_near_simultaneous | PASS | 7 | 0 | All-way stop: both critical about 1.2 s before, B enters the path of A, collision; unchanged. |
| S15 | run_0_deflected_into_c | WARN | 13 | 2 | C's track of B now linked to B (phase-0 ghost resolved).  Remaining: U1 = B:track_001, which follows C and then A after the A-B contact (identity switch, left anonymous): drawn on C, then drifting between C and A; B's CRITICAL_TTC on it from +0.15 concerns that mixed track. |
| S16 | run_0_consequential | WARN | 14 | 0 | Phase-0 WARN resolved: the van C's tracks (A:track_002, B:track_002, B:track_003) are linked to C, no extra bodies.  Remaining: U1 = B:track_004, a 0.3 s fragment ahead of C after the contacts; C's CRITICAL_TTC on A still open at TRACK_LOST 0.15 s before their contact (local semantics, unchanged). |
| S17 | run_0_crash | PASS | 11 | 0 | Phase-0 WARN resolved: the non-recorder C is one anonymous road user U1 (A:track_001 + B:track_002 + B:track_003), drawn once with its uncertainty; A critical on U1 from -2.35, CUT_IN -2.20, path entry -1.60, A-B and B-A end at the collision, A on U1 at +0.55. |
| S18 | run_0_abreast | WARN | 11 | 4 | Negative case passes: C and D are never one road user.  C is drawn twice (U1 = A:track_001, U2 = B's tracks: a missed merge), D once (U3 = A:track_003 + B:track_003).  A:track_001 starts on D (C and D 1.4 m apart side to side: A's radar clusters their returns) and settles on C: the drift is reconstructed as a CUT_IN_FROM_RIGHT and an EGO_PATH_ENTRY of A on U1 that did not happen. |
| S18 | run_0_passing | WARN | 12 | 2 | Negative case passes: C and D never fused.  D is one road user (U3 = A:track_004 + B:track_003 + B:track_005), C two (U1, U2).  As in abreast, A:track_001 starts on D and settles on C: a spurious CUT_IN_FROM_RIGHT / EGO_PATH_ENTRY of A on U1. |
| S18 | run_0_platoon | WARN | 8 | 1 | Negative case passes: C and D never fused.  D is U1 (A:track_001 + B:track_002 + B:track_004) with a short duplicate U2 (A:track_003) at the start; C is U3 then U4 (fragments). |
