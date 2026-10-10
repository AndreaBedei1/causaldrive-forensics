# Visual audit (visual_audit_baseline): S16/run_0_consequential

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

B into A at 0.00, A into the van C at +1.05; episodes end at their collisions; the van C (a recorder) appears as several anonymous ghosts; the episode of C on A stays open when C loses the track of A 0.15 s before their contact.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S16 | run_0_consequential | WARN | -5.55 .. | van C drawn with up to 3 extra ghosts (A:track_002, B:track_002/003/004) | [03_tgm000.35.png](visual_audit_baseline/03_tgm000.35.png) | PHASE 1: association and stitching |
| S16 | run_0_consequential | WARN | +0.05 .. +0.90 | CRITICAL_TTC(C, A) open at TRACK_LOST 0.15 s before the A-C contact | [11_tgp000.85.png](visual_audit_baseline/11_tgp000.85.png) | track lost before the contact: no partner can be attributed; reported |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.55.png](visual_audit_baseline/01_tgm005.55.png) | -5.55 | lead-in |
| [02_tgm005.05.png](visual_audit_baseline/02_tgm005.05.png) | -5.05 | CRITICAL_TTC_START(B,track_001 (A)) |
| [03_tgm000.35.png](visual_audit_baseline/03_tgm000.35.png) | -0.35 | CRITICAL_TTC_START(A,track_001 (C)) |
| [04_tgm000.20.png](visual_audit_baseline/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.15.png](visual_audit_baseline/05_tgm000.15.png) | -0.15 | EGO_PATH_ENTRY(A,track_002) |
| [06_tgm000.10.png](visual_audit_baseline/06_tgm000.10.png) | -0.10 | CUT_IN_FROM_LEFT_START(A,track_001 (C)) |
| [07_tgp000.00.png](visual_audit_baseline/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.05.png](visual_audit_baseline/08_tgp000.05.png) | +0.05 | CRITICAL_TTC_START(C,track_001 (A)) |
| [09_tgp000.20.png](visual_audit_baseline/09_tgp000.20.png) | +0.20 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.50.png](visual_audit_baseline/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.85.png](visual_audit_baseline/11_tgp000.85.png) | +0.85 | before COLLISION(A,C) |
| [12_tgp001.05.png](visual_audit_baseline/12_tgp001.05.png) | +1.05 | CRITICAL_TTC_END(A,track_001 (C)); COLLISION(A,C) |
| [13_tgp001.30.png](visual_audit_baseline/13_tgp001.30.png) | +1.30 | CUT_IN_FROM_LEFT_END(A,track_001 (C)) |
| [14_tgp001.55.png](visual_audit_baseline/14_tgp001.55.png) | +1.55 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

| check | t_global [s] | subject | detail |
|---|---|---|---|
| duplicate_ghost_across_observers | -4.65 | A:track_002 / B:track_003 | centres within 3.0 m from here |
| duplicate_ghost_across_observers | -3.85 | A:track_002 / B:track_002 | centres within 3.0 m from here |

Reconstruction commit: `215170a1d7f1a87cc455eb85d718183c1fcee7b9`.
