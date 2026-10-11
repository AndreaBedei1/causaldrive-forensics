# Visual audit (visual_audit_final): S08/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S08 | run_0_crash | WARN | -2.0 | road_user_on_recorder: drawn bodies overlap from here | [02_tgm001.55.png](visual_audit_final/02_tgm001.55.png) | Known limitation: Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |
| S08 | run_0_crash | WARN | 1.0 | road_user_on_recorder: drawn bodies overlap from here | [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | Known limitation: Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |
| S08 | run_0_crash | WARN | 1.0 | road_user_on_recorder: drawn bodies overlap from here | [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | Known limitation: Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |
| S08 | run_0_crash | WARN | 1.0 | road_users_overlap: drawn bodies overlap from here | [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | Known limitation: Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |
| S08 | run_0_crash | WARN | 1.1 | road_user_on_recorder: drawn bodies overlap from here | [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | Known limitation: Residual contact handoff C:track_002; overlap and heading uncertainty after impact. Wide-support segment is UNKNOWN. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_final/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.55.png](visual_audit_final/02_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_002 (B)) |
| [03_tgm001.50.png](visual_audit_final/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,track_002 (A)) |
| [04_tgm000.20.png](visual_audit_final/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgp000.00.png](visual_audit_final/05_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [06_tgp000.05.png](visual_audit_final/06_tgp000.05.png) | +0.05 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [07_tgp000.50.png](visual_audit_final/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(C,track_002 (U1)) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_user_on_recorder | -2.00 | B / U1 | drawn bodies overlap from here |
| road_user_on_recorder | +1.00 | A / U1 | drawn bodies overlap from here |
| road_user_on_recorder | +1.00 | A / U3 | drawn bodies overlap from here |
| road_users_overlap | +1.00 | U1 / U3 | drawn bodies overlap from here |
| road_user_on_recorder | +1.10 | B / U3 | drawn bodies overlap from here |

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
