> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_baseline): S08/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Multi-direction crossing A-B consistent; recorder C seen as two ghosts (A:track_001, B:track_001) and the tracks of A and B by C anonymous; post-impact ghost heading of B:track_001 rotated about 45 deg while B spins.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S08 | run_0_crash | WARN | +2.10 .. | two ghosts of the recorder C (A:track_001, B:track_001) | [04_tgp003.90.png](visual_audit_baseline/04_tgp003.90.png) | PHASE 1: association with recorder poses |
| S08 | run_0_crash | WARN | +4.60 | box heading of B:track_001 off by about 45 deg after the impact of B (observer spinning) | [07_tgp004.60.png](visual_audit_baseline/07_tgp004.60.png) | post-impact; reported as a limitation |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgp000.00.png](visual_audit_baseline/01_tgp000.00.png) | +0.00 | lead-in |
| [02_tgp002.55.png](visual_audit_baseline/02_tgp002.55.png) | +2.55 | CRITICAL_TTC_START(A,track_002 (B)) |
| [03_tgp002.60.png](visual_audit_baseline/03_tgp002.60.png) | +2.60 | CRITICAL_TTC_START(B,track_002 (A)) |
| [04_tgp003.90.png](visual_audit_baseline/04_tgp003.90.png) | +3.90 | before COLLISION(A,B) |
| [05_tgp004.10.png](visual_audit_baseline/05_tgp004.10.png) | +4.10 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [06_tgp004.15.png](visual_audit_baseline/06_tgp004.15.png) | +4.15 | EGO_PATH_ENTRY(A,track_001) |
| [07_tgp004.60.png](visual_audit_baseline/07_tgp004.60.png) | +4.60 | after COLLISION(A,B) |
| [08_tgp004.65.png](visual_audit_baseline/08_tgp004.65.png) | +4.65 | EGO_PATH_ENTRY(C,track_002) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| duplicate_ghost_across_observers | +2.10 | A:track_001 / B:track_001 | centres within 3.0 m from here |
| duplicate_ghost_same_observer | +4.20 | C:track_001 / C:track_002 | centres within 3.0 m from here |

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
