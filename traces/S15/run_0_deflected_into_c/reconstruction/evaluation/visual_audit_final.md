> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_final): S15/run_0_deflected_into_c

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Contact handoff may begin before wide support is confirmed; post-impact fragments remain anonymous.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S15 | run_0_deflected_into_c | WARN | 2.2 | road_user_on_recorder: drawn bodies overlap from here | [11_tgp001.40.png](visual_audit_final/11_tgp001.40.png) | Known limitation: Contact handoff may begin before wide support is confirmed; post-impact fragments remain anonymous. |
| S15 | run_0_deflected_into_c | WARN | 2.2 | road_user_on_recorder: drawn bodies overlap from here | [11_tgp001.40.png](visual_audit_final/11_tgp001.40.png) | Known limitation: Contact handoff may begin before wide support is confirmed; post-impact fragments remain anonymous. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm003.80.png](visual_audit_final/01_tgm003.80.png) | -3.80 | lead-in |
| [02_tgm001.30.png](visual_audit_final/02_tgm001.30.png) | -1.30 | CRITICAL_TTC_START(B,track_002 (A)) |
| [03_tgm001.25.png](visual_audit_final/03_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.20.png](visual_audit_final/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.05.png](visual_audit_final/05_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,track_001 (C)); EGO_PATH_ENTRY(B,track_002 (A)); CRITICAL_TTC_START(C,track_001 (A)) |
| [06_tgp000.00.png](visual_audit_final/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_final/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [08_tgp000.55.png](visual_audit_final/08_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(A,track_001 (C)); CRITICAL_TTC_START(B,track_001#segment_1 (C)) |
| [09_tgp000.70.png](visual_audit_final/09_tgp000.70.png) | +0.70 | before COLLISION(A,C) |
| [10_tgp000.90.png](visual_audit_final/10_tgp000.90.png) | +0.90 | CRITICAL_TTC_END(A,track_001 (C)); CRITICAL_TTC_END(C,track_001 (A)); COLLISION(A,C) |
| [11_tgp001.40.png](visual_audit_final/11_tgp001.40.png) | +1.40 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_user_on_recorder | +2.20 | A / U2 | drawn bodies overlap from here |
| road_user_on_recorder | +2.20 | C / U2 | drawn bodies overlap from here |

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
