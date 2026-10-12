# Visual audit (visual_audit_replay_followup): S16/run_0_consequential

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Resta un breve U1 con box van sovrapposto a C dopo l’urto e la perdita di A da C.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S16 | run_0_consequential | WARN | 1.35 | Frammento U1 nato a +1.25 e perso a +1.55; C→A termina a +0.90, A→C a +1.20. | [13_tgp001.35.png](visual_audit_replay_followup/13_tgp001.35.png) | Limite residuo dichiarato; nessuna ulteriore modifica fuori dagli obiettivi S02/S08. |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.55.png](visual_audit_replay_followup/01_tgm005.55.png) | -5.55 | lead-in |
| [02_tgm005.05.png](visual_audit_replay_followup/02_tgm005.05.png) | -5.05 | CRITICAL_TTC_START(B,track_001 (A)) |
| [03_tgm000.35.png](visual_audit_replay_followup/03_tgm000.35.png) | -0.35 | CRITICAL_TTC_START(A,track_001 (C)) |
| [04_tgm000.20.png](visual_audit_replay_followup/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.10.png](visual_audit_replay_followup/05_tgm000.10.png) | -0.10 | CUT_IN_FROM_LEFT_START(A,track_001 (C)) |
| [06_tgm000.05.png](visual_audit_replay_followup/06_tgm000.05.png) | -0.05 | EGO_PATH_ENTRY(A,track_002 (C)) |
| [07_tgp000.00.png](visual_audit_replay_followup/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_START(A,track_002 (C)); CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.05.png](visual_audit_replay_followup/08_tgp000.05.png) | +0.05 | CRITICAL_TTC_START(C,track_001 (A)) |
| [09_tgp000.25.png](visual_audit_replay_followup/09_tgp000.25.png) | +0.25 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.50.png](visual_audit_replay_followup/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.85.png](visual_audit_replay_followup/11_tgp000.85.png) | +0.85 | before COLLISION(A,C) |
| [12_tgp001.05.png](visual_audit_replay_followup/12_tgp001.05.png) | +1.05 | CRITICAL_TTC_END(A,track_001 (C)); COLLISION(A,C) |
| [13_tgp001.35.png](visual_audit_replay_followup/13_tgp001.35.png) | +1.35 | CUT_IN_FROM_LEFT_END(A,track_001 (C)) |
| [14_tgp001.55.png](visual_audit_replay_followup/14_tgp001.55.png) | +1.55 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
