# Visual audit (visual_audit_final): S09/run_0_merge_conflict

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Reconstruction-only QA: no anomaly.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S09 | run_0_merge_conflict | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm007.95.png](visual_audit_final/01_tgm007.95.png) | -7.95 | lead-in |
| [02_tgm004.95.png](visual_audit_final/02_tgm004.95.png) | -4.95 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [03_tgm003.60.png](visual_audit_final/03_tgm003.60.png) | -3.60 | CRITICAL_TTC_START(B,track_001 (A)) |
| [04_tgm003.35.png](visual_audit_final/04_tgm003.35.png) | -3.35 | CRITICAL_TTC_START(A,track_001 (B)) |
| [05_tgm000.20.png](visual_audit_final/05_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [06_tgp000.00.png](visual_audit_final/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_final/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
