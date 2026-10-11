# Visual audit (visual_audit_final): S16/run_0_consequential

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Short post-contact van fragment and C losing A before their contact remain documented limitations.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S16 | run_0_consequential | WARN |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.55.png](visual_audit_final/01_tgm005.55.png) | -5.55 | lead-in |
| [02_tgm005.05.png](visual_audit_final/02_tgm005.05.png) | -5.05 | CRITICAL_TTC_START(B,track_001 (A)) |
| [03_tgm000.35.png](visual_audit_final/03_tgm000.35.png) | -0.35 | CRITICAL_TTC_START(A,track_001 (C)) |
| [04_tgm000.20.png](visual_audit_final/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.15.png](visual_audit_final/05_tgm000.15.png) | -0.15 | EGO_PATH_ENTRY(A,track_002 (C)) |
| [06_tgm000.10.png](visual_audit_final/06_tgm000.10.png) | -0.10 | CUT_IN_FROM_LEFT_START(A,track_001 (C)) |
| [07_tgp000.00.png](visual_audit_final/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.05.png](visual_audit_final/08_tgp000.05.png) | +0.05 | CRITICAL_TTC_START(C,track_001 (A)) |
| [09_tgp000.20.png](visual_audit_final/09_tgp000.20.png) | +0.20 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.50.png](visual_audit_final/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.85.png](visual_audit_final/11_tgp000.85.png) | +0.85 | before COLLISION(A,C) |
| [12_tgp001.05.png](visual_audit_final/12_tgp001.05.png) | +1.05 | CRITICAL_TTC_END(A,track_001 (C)); COLLISION(A,C) |
| [13_tgp001.30.png](visual_audit_final/13_tgp001.30.png) | +1.30 | CUT_IN_FROM_LEFT_END(A,track_001 (C)) |
| [14_tgp001.55.png](visual_audit_final/14_tgp001.55.png) | +1.55 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
