# Visual audit (visual_audit_phase2): S09/run_0_merge_conflict

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Roundabout merge: both episodes end at the collision (phase-0 FAIL fixed and preserved); EGO_PATH_ENTRY of A on B at -4.95 reflects the straight-ahead corridor (documented limitation).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S09 | run_0_merge_conflict | PASS | -4.95 .. +0.50 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.95.png](visual_audit_phase2/01_tgm007.95.png) | -7.95 | lead-in |
| [02_tgm004.95.png](visual_audit_phase2/02_tgm004.95.png) | -4.95 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [03_tgm003.60.png](visual_audit_phase2/03_tgm003.60.png) | -3.60 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm003.35.png](visual_audit_phase2/04_tgm003.35.png) | -3.35 | CRITICAL_TTC_START(A,track_001 (B)) |
| [05_tgm000.20.png](visual_audit_phase2/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_phase2/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_phase2/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
