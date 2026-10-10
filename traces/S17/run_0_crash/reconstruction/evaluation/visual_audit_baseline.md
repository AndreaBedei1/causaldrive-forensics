# Visual audit (visual_audit_baseline): S17/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Consistent semantics: A critical on the cutting-in C from -2.35, CUT_IN -2.20, path entry -1.60; A-B and B-A end at the collision, A on C at +0.55; C (records nothing) is drawn as three ghosts.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S17 | run_0_crash | WARN | -4.95 .. | C seen as A:track_001, B:track_002 and B:track_003 (three ghosts about 1.5-2 m apart) | [02_tgm002.35.png](visual_audit_baseline/02_tgm002.35.png) | PHASE 1: one anonymous entity U1 |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.95.png](visual_audit_baseline/01_tgm004.95.png) | -4.95 | lead-in |
| [02_tgm002.35.png](visual_audit_baseline/02_tgm002.35.png) | -2.35 | CRITICAL_TTC_START(A,track_001) |
| [03_tgm002.20.png](visual_audit_baseline/03_tgm002.20.png) | -2.20 | CUT_IN_FROM_RIGHT_START(A,track_001) |
| [04_tgm001.60.png](visual_audit_baseline/04_tgm001.60.png) | -1.60 | EGO_PATH_ENTRY(A,track_001) |
| [05_tgm001.15.png](visual_audit_baseline/05_tgm001.15.png) | -1.15 | CRITICAL_TTC_START(A,track_002 (B)) |
| [06_tgm000.85.png](visual_audit_baseline/06_tgm000.85.png) | -0.85 | CUT_IN_FROM_RIGHT_END(A,track_001) |
| [07_tgm000.80.png](visual_audit_baseline/07_tgm000.80.png) | -0.80 | CRITICAL_TTC_START(B,track_001 (A)) |
| [08_tgm000.20.png](visual_audit_baseline/08_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [09_tgp000.00.png](visual_audit_baseline/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [10_tgp000.50.png](visual_audit_baseline/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.55.png](visual_audit_baseline/11_tgp000.55.png) | +0.55 | CRITICAL_TTC_END(A,track_001) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| duplicate_ghost_across_observers | -4.95 | A:track_001 / B:track_002 | centres within 3.0 m from here |
| duplicate_ghost_across_observers | +1.45 | A:track_001 / B:track_003 | centres within 3.0 m from here |

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
