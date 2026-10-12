> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase2): S15/run_0_deflected_into_c

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

C's track of B now linked to B (phase-0 ghost resolved).  Remaining: U1 = B:track_001, which follows C and then A after the A-B contact (identity switch, left anonymous): drawn on C, then drifting between C and A; B's CRITICAL_TTC on it from +0.15 concerns that mixed track.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S15 | run_0_deflected_into_c | WARN | -2.10 .. +1.40 | U1 (B:track_001) drawn on the recorder C, then between C and A: a track that switched body stays anonymous | [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | limitation: identity per track (segment-wise identity is future work) |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm003.80.png](visual_audit_phase2/01_tgm003.80.png) | -3.80 | lead-in |
| [02_tgm001.30.png](visual_audit_phase2/02_tgm001.30.png) | -1.30 | CRITICAL_TTC_START(B,track_002 (A)) |
| [03_tgm001.25.png](visual_audit_phase2/03_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.20.png](visual_audit_phase2/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.05.png](visual_audit_phase2/05_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,track_001 (C)); EGO_PATH_ENTRY(B,track_002 (A)); CRITICAL_TTC_START(C,track_001 (A)) |
| [06_tgp000.00.png](visual_audit_phase2/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [07_tgp000.15.png](visual_audit_phase2/07_tgp000.15.png) | +0.15 | CRITICAL_TTC_START(B,track_001 (U1)) |
| [08_tgp000.50.png](visual_audit_phase2/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [09_tgp000.55.png](visual_audit_phase2/09_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.70.png](visual_audit_phase2/10_tgp000.70.png) | +0.70 | before COLLISION(A,C) |
| [11_tgp000.90.png](visual_audit_phase2/11_tgp000.90.png) | +0.90 | CRITICAL_TTC_END(A,track_001 (C)); CRITICAL_TTC_END(C,track_001 (A)); COLLISION(A,C) |
| [12_tgp001.25.png](visual_audit_phase2/12_tgp001.25.png) | +1.25 | CRITICAL_TTC_END(B,track_001 (U1)) |
| [13_tgp001.40.png](visual_audit_phase2/13_tgp001.40.png) | +1.40 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_user_on_recorder | -2.10 | C / U1 | drawn bodies overlap from here |
| road_user_on_recorder | +2.80 | A / U1 | drawn bodies overlap from here |

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
