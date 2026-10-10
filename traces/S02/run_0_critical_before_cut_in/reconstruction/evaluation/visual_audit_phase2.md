# Visual audit (visual_audit_phase2): S02/run_0_critical_before_cut_in

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

CRITICAL_TTC (-1.50) before CUT_IN_FROM_LEFT (-1.15) before EGO_PATH_ENTRY (-0.45); unchanged since phase 0.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S02 | run_0_critical_before_cut_in | PASS | -1.50 .. +0.80 | none |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_phase2/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.50.png](visual_audit_phase2/02_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(A,track_001 (B)) |
| [03_tgm001.40.png](visual_audit_phase2/03_tgm001.40.png) | -1.40 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm001.15.png](visual_audit_phase2/04_tgm001.15.png) | -1.15 | CUT_IN_FROM_LEFT_START(A,track_001 (B)) |
| [05_tgm000.45.png](visual_audit_phase2/05_tgm000.45.png) | -0.45 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [06_tgm000.20.png](visual_audit_phase2/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_phase2/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [09_tgp000.80.png](visual_audit_phase2/09_tgp000.80.png) | +0.80 | CUT_IN_FROM_LEFT_END(A,track_001 (B)) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
