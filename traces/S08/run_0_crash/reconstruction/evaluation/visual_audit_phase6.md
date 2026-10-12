> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase6): S08/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Phase-0 WARNs resolved: C aligned by its observed trajectory (on t_global), A's and B's tracks of C drawn as dots on C, C's track of A linked to A.  Remaining: U1 = C:track_002, B's track by C until the A-B contact, then the A-B pair (identity switch, left anonymous): a grey box on B before the contact, next to A after it.  Phase 6: frames pixel-identical to the phase-2 frames inspected then; the verdict stands.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S08 | run_0_crash | WARN | -2.00 .. +1.70 | U1 (C:track_002) drawn on the recorder B, then near A after the A-B contact: a track that switched body stays anonymous | [05_tgp000.00.png](visual_audit_phase6/05_tgp000.00.png) | limitation: identity per track (segment-wise identity is future work) |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_phase6/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.55.png](visual_audit_phase6/02_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_002 (B)) |
| [03_tgm001.50.png](visual_audit_phase6/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,track_002 (A)) |
| [04_tgm000.20.png](visual_audit_phase6/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgp000.00.png](visual_audit_phase6/05_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [06_tgp000.05.png](visual_audit_phase6/06_tgp000.05.png) | +0.05 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [07_tgp000.50.png](visual_audit_phase6/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [08_tgp000.55.png](visual_audit_phase6/08_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(C,track_002 (U1)) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| road_user_on_recorder | -2.00 | B / U1 | drawn bodies overlap from here |
| road_user_on_recorder | +1.00 | A / U1 | drawn bodies overlap from here |

Reconstruction commit: `c80eab47ec83dcc66909751b0514f1bcb4d5066e`.
