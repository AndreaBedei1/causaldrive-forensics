# Visual audit (visual_audit_replay_followup): S18/run_0_abreast

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Due corpi finali distinti, nessun falso merge; restano duplicazioni iniziali e rinumerazione dei frammenti.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_abreast | WARN | -6.2 | U1/U3 duplicati all’inizio, ancora visibili a -6.00. | [01_tgm006.20.png](visual_audit_replay_followup/01_tgm006.20.png) | Frammentazione conservativa residua. |
| S18 | run_0_abreast | WARN | -5.7 | Cambio di box/identità U durante il passaggio tra frammenti. | [03_tgm005.70.png](visual_audit_replay_followup/03_tgm005.70.png) | Successivamente U2/U3 distinti; false merge 0. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_replay_followup/01_tgm006.20.png) | -6.20 | QA flag: road_users_overlap |
| [02_tgm006.00.png](visual_audit_replay_followup/02_tgm006.00.png) | -6.00 | QA flag: road_users_overlap |
| [03_tgm005.70.png](visual_audit_replay_followup/03_tgm005.70.png) | -5.70 | QA flag: road_user_box_jump |
| [04_tgm004.55.png](visual_audit_replay_followup/04_tgm004.55.png) | -4.55 | lead-in |
| [05_tgm001.55.png](visual_audit_replay_followup/05_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_001#segment_3 (U2)) |
| [06_tgm001.05.png](visual_audit_replay_followup/06_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [07_tgm000.65.png](visual_audit_replay_followup/07_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [08_tgm000.45.png](visual_audit_replay_followup/08_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_001#segment_3 (U2)) |
| [09_tgm000.20.png](visual_audit_replay_followup/09_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [10_tgp000.00.png](visual_audit_replay_followup/10_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [11_tgp000.50.png](visual_audit_replay_followup/11_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U2 | drawn bodies overlap from here |
| road_users_overlap | -6.20 | U1 / U3 | drawn bodies overlap from here |
| road_users_overlap | -6.00 | U2 / U3 | drawn bodies overlap from here |
| road_user_box_jump | -5.70 | U2 | box moved 4.0 m at 11.9 m/s |

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
