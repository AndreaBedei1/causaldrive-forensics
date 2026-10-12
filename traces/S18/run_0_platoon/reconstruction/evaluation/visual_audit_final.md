> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_final): S18/run_0_platoon

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_platoon | WARN | -6.2 | road_users_overlap: drawn bodies overlap from here | [01_tgm006.20.png](visual_audit_final/01_tgm006.20.png) | Known limitation: Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_final/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.70.png](visual_audit_final/02_tgm005.70.png) | -5.70 | CRITICAL_TTC_START(A,track_001 (U1)) |
| [03_tgm001.05.png](visual_audit_final/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.65.png](visual_audit_final/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [05_tgm000.35.png](visual_audit_final/05_tgm000.35.png) | -0.35 | CRITICAL_TTC_END(A,track_001 (U1)) |
| [06_tgm000.20.png](visual_audit_final/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_final/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_final/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U2 | drawn bodies overlap from here |

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
