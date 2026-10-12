# Visual audit (visual_audit_replay_followup): S08/run_0_crash

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **PASS**

C mantiene A/B distinti attraverso -0.45, il contatto e fino a +11. Nessun ghost anonimo duplicato. PASS visivo; EGO_PATH_ENTRY su A a +0.50 resta extra rispetto all’oracle.

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S08 | run_0_crash | PASS |  | - |  | - |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm004.10.png](visual_audit_replay_followup/01_tgm004.10.png) | -4.10 | lead-in |
| [02_tgm001.55.png](visual_audit_replay_followup/02_tgm001.55.png) | -1.55 | CRITICAL_TTC_START(A,track_002 (B)) |
| [03_tgm001.50.png](visual_audit_replay_followup/03_tgm001.50.png) | -1.50 | CRITICAL_TTC_START(B,track_002 (A)) |
| [04_tgm000.50.png](visual_audit_replay_followup/04_tgm000.50.png) | -0.50 | continuity / event order at -0.50 s |
| [05_tgm000.45.png](visual_audit_replay_followup/05_tgm000.45.png) | -0.45 | continuity / event order at -0.45 s |
| [06_tgm000.40.png](visual_audit_replay_followup/06_tgm000.40.png) | -0.40 | continuity / event order at -0.40 s |
| [07_tgm000.20.png](visual_audit_replay_followup/07_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [08_tgm000.05.png](visual_audit_replay_followup/08_tgm000.05.png) | -0.05 | continuity / event order at -0.05 s |
| [09_tgp000.00.png](visual_audit_replay_followup/09_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(A,track_002 (B)); CRITICAL_TTC_END(B,track_002 (A)); COLLISION(A,B) |
| [10_tgp000.05.png](visual_audit_replay_followup/10_tgp000.05.png) | +0.05 | continuity / event order at +0.05 s |
| [11_tgp000.40.png](visual_audit_replay_followup/11_tgp000.40.png) | +0.40 | continuity / event order at +0.40 s |
| [12_tgp000.50.png](visual_audit_replay_followup/12_tgp000.50.png) | +0.50 | EGO_PATH_ENTRY(C,track_001 (A)); after COLLISION(A,B) |
| [13_tgp000.95.png](visual_audit_replay_followup/13_tgp000.95.png) | +0.95 | continuity / event order at +0.95 s |
| [14_tgp001.00.png](visual_audit_replay_followup/14_tgp001.00.png) | +1.00 | continuity / event order at +1.00 s |
| [15_tgp001.90.png](visual_audit_replay_followup/15_tgp001.90.png) | +1.90 | continuity / event order at +1.90 s |
| [16_tgp002.15.png](visual_audit_replay_followup/16_tgp002.15.png) | +2.15 | continuity / event order at +2.15 s |
| [17_tgp011.00.png](visual_audit_replay_followup/17_tgp011.00.png) | +11.00 | continuity / event order at +11.00 s |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e`.

Execution working tree dirty: **YES**; actual execution provenance preserved in `visual_audit_replay_followup/audit.json`. No clean execution claimed.
