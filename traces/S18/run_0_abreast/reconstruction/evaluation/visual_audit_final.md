# Visual audit (visual_audit_final): S18/run_0_abreast

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_abreast | WARN | -6.2 | road_users_overlap: drawn bodies overlap from here | [01_tgm005.25.png](visual_audit_final/01_tgm005.25.png) | Known limitation: Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |
| S18 | run_0_abreast | WARN | -6.2 | road_users_overlap: drawn bodies overlap from here | [01_tgm005.25.png](visual_audit_final/01_tgm005.25.png) | Known limitation: Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |
| S18 | run_0_abreast | WARN | -6.0 | road_users_overlap: drawn bodies overlap from here | [01_tgm005.25.png](visual_audit_final/01_tgm005.25.png) | Known limitation: Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |
| S18 | run_0_abreast | WARN | -5.7 | road_user_box_jump: box moved 4.5 m at 11.9 m/s | [01_tgm005.25.png](visual_audit_final/01_tgm005.25.png) | Known limitation: Radar identity ambiguity and conservative fragmentation; no C/D fusion. Mixed-body support is points only, not an asserted ghost box. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.25.png](visual_audit_final/01_tgm005.25.png) | -5.25 | lead-in |
| [02_tgm002.25.png](visual_audit_final/02_tgm002.25.png) | -2.25 | CRITICAL_TTC_START(A,track_001#segment_3 (U2)) |
| [03_tgm001.05.png](visual_audit_final/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.65.png](visual_audit_final/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [05_tgm000.45.png](visual_audit_final/05_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_001#segment_3 (U2)) |
| [06_tgm000.20.png](visual_audit_final/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_final/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_final/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_users_overlap | -6.20 | U1 / U2 | drawn bodies overlap from here |
| road_users_overlap | -6.20 | U1 / U3 | drawn bodies overlap from here |
| road_users_overlap | -6.00 | U2 / U3 | drawn bodies overlap from here |
| road_user_box_jump | -5.70 | U2 | box moved 4.5 m at 11.9 m/s |

Reconstruction commit: `fd8d2baed644db4a32c2eb502a2eeb9b32f70887`.
