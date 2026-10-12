# Visual audit (visual_audit_replay_followup): S18/run_0_passing

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Due corpi anonimi U1/U2 distinti in tutti gli otto frame; nessun collasso C/D e nessun flag QA.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S18 | run_0_passing | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm006.20.png](visual_audit_replay_followup/01_tgm006.20.png) | -6.20 | lead-in |
| [02_tgm005.55.png](visual_audit_replay_followup/02_tgm005.55.png) | -5.55 | CRITICAL_TTC_START(A,track_003 (U2)) |
| [03_tgm001.05.png](visual_audit_replay_followup/03_tgm001.05.png) | -1.05 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.65.png](visual_audit_replay_followup/04_tgm000.65.png) | -0.65 | CRITICAL_TTC_START(B,track_001 (A)) |
| [05_tgm000.45.png](visual_audit_replay_followup/05_tgm000.45.png) | -0.45 | CRITICAL_TTC_END(A,track_003 (U2)) |
| [06_tgm000.20.png](visual_audit_replay_followup/06_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [07_tgp000.00.png](visual_audit_replay_followup/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.50.png](visual_audit_replay_followup/08_tgp000.50.png) | +0.50 | after COLLISION(A,B) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
