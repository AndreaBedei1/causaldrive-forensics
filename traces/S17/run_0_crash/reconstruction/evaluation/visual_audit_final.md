# Visual audit (visual_audit_final): S17/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Reconstruction-only QA: no anomaly.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S17 | run_0_crash | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.95.png](visual_audit_final/01_tgm004.95.png) | -4.95 | lead-in |
| [02_tgm002.35.png](visual_audit_final/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,track_001 (U1)) |
| [03_tgm002.20.png](visual_audit_final/03_tgm002.20.png) | -2.20 | CUT_IN_FROM_RIGHT_START(A,track_001 (U1)) |
| [04_tgm001.60.png](visual_audit_final/04_tgm001.60.png) | -1.60 | EGO_PATH_ENTRY(A,track_001 (U1)) |
| [05_tgm001.15.png](visual_audit_final/05_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,track_002 (B)) |
| [06_tgm000.85.png](visual_audit_final/06_tgm000.85.png) | -0.85 | CUT_IN_FROM_RIGHT_END(A,track_001 (U1)) |
| [07_tgm000.80.png](visual_audit_final/07_tgm000.80.png) | -0.80 | CRITICAL_TTC_START(B,track_001 (A)) |
| [08_tgm000.20.png](visual_audit_final/08_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [09_tgp000.00.png](visual_audit_final/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [10_tgp000.50.png](visual_audit_final/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.55.png](visual_audit_final/11_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,track_001 (U1)) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
