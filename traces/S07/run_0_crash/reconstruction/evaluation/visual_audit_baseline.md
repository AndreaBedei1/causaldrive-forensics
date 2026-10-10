# Visual audit (visual_audit_baseline): S07/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Occluded chain stop consistent (A critical on B, A into B); the recorder C also appears as the anonymous ghost B:track_001 (no B-C collision to associate it); shown on the source clock because C has no collision to be aligned.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S07 | run_0_crash | WARN | +0.00 .. +6.40 | ghost B:track_001 drawn on the recorder C (second body for C) | [03_tgp003.40.png](visual_audit_baseline/03_tgp003.40.png) | PHASE 1: associate anonymous tracks with recorders in a common frame |
| S07 | run_0_crash | WARN | - | replay on source time: recorder C is not collision-aligned | [01_tgp000.00.png](visual_audit_baseline/01_tgp000.00.png) | PHASE 2: documented; aligning a collision-free recorder is outside collision anchoring |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgp000.00.png](visual_audit_baseline/01_tgp000.00.png) | +0.00 | lead-in |
| [02_tgp000.50.png](visual_audit_baseline/02_tgp000.50.png) | +0.50 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgp003.40.png](visual_audit_baseline/03_tgp003.40.png) | +3.40 | CRITICAL_TTC_START(B,track_001) |
| [04_tgp004.35.png](visual_audit_baseline/04_tgp004.35.png) | +4.35 | CRITICAL_TTC_END(B,track_001) |
| [05_tgp005.70.png](visual_audit_baseline/05_tgp005.70.png) | +5.70 | before COLLISION(A,B) |
| [06_tgp005.90.png](visual_audit_baseline/06_tgp005.90.png) | +5.90 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [07_tgp006.40.png](visual_audit_baseline/07_tgp006.40.png) | +6.40 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
