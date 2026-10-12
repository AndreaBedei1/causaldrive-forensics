# Visual audit (visual_audit_replay_followup): S15/run_0_deflected_into_c

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

Sei associazioni nominate, A-B poi A-C: punti e corpi coerenti, senza il precedente frammento anonimo duplicato.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S15 | run_0_deflected_into_c | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm003.80.png](visual_audit_replay_followup/01_tgm003.80.png) | -3.80 | lead-in |
| [02_tgm001.30.png](visual_audit_replay_followup/02_tgm001.30.png) | -1.30 | CRITICAL_TTC_START(B,track_002 (A)) |
| [03_tgm001.25.png](visual_audit_replay_followup/03_tgm001.25.png) | -1.25 | CRITICAL_TTC_START(A,track_002 (B)) |
| [04_tgm000.20.png](visual_audit_replay_followup/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.05.png](visual_audit_replay_followup/05_tgm000.05.png) | -0.05 | CRITICAL_TTC_START(A,track_001 (C)); CRITICAL_TTC_START(C,track_001 (A)) |
| [06_tgp000.00.png](visual_audit_replay_followup/06_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); EGO_PATH_ENTRY(B,track_002 (A)); COLLISION(A,B) |
| [07_tgp000.50.png](visual_audit_replay_followup/07_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [08_tgp000.55.png](visual_audit_replay_followup/08_tgp000.55.png) | +0.55 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [09_tgp000.70.png](visual_audit_replay_followup/09_tgp000.70.png) | +0.70 | before COLLISION(A,C) |
| [10_tgp000.90.png](visual_audit_replay_followup/10_tgp000.90.png) | +0.90 | CRITICAL_TTC_END(A,track_001 (C)); CRITICAL_TTC_END(C,track_001 (A)); COLLISION(A,C) |
| [11_tgp001.40.png](visual_audit_replay_followup/11_tgp001.40.png) | +1.40 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
