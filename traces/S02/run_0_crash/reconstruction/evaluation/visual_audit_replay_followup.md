# Visual audit (visual_audit_replay_followup): S02/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

CUT_IN visibile a -3.65; a -3.55/-3.45 CRITICAL ancora assente, poi attivo a -3.40. Contatto posteriore A-B a 0. Nessun anonimo.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S02 | run_0_crash | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.30.png](visual_audit_replay_followup/01_tgm005.30.png) | -5.30 | lead-in |
| [02_tgm003.65.png](visual_audit_replay_followup/02_tgm003.65.png) | -3.65 | CUT_IN_FROM_LEFT_START(A,track_001 (B)) |
| [03_tgm003.55.png](visual_audit_replay_followup/03_tgm003.55.png) | -3.55 | continuity / event order at -3.55 s |
| [04_tgm003.45.png](visual_audit_replay_followup/04_tgm003.45.png) | -3.45 | continuity / event order at -3.45 s |
| [05_tgm003.40.png](visual_audit_replay_followup/05_tgm003.40.png) | -3.40 | CRITICAL_TTC_START(A,track_001 (B)) |
| [06_tgm002.85.png](visual_audit_replay_followup/06_tgm002.85.png) | -2.85 | EGO_PATH_ENTRY(A,track_001 (B)) |
| [07_tgm000.20.png](visual_audit_replay_followup/07_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [08_tgm000.15.png](visual_audit_replay_followup/08_tgm000.15.png) | -0.15 | CUT_IN_FROM_LEFT_END(A,track_001 (B)) |
| [09_tgp000.00.png](visual_audit_replay_followup/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_001 (B)); COLLISION(A,B) |
| [10_tgp000.50.png](visual_audit_replay_followup/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
