> **Snapshot storico precedente al follow-up.** Per il run corrente vedere [visual_audit_replay_followup](visual_audit_replay_followup.md) e `gt_audit_replay_followup.md`. Immagini e giudizi qui sotto conservati come storia.

# Visual audit (visual_audit_phase2): S16/run_0_consequential

Reconstruction-only frames (top-down replay: recorded recorder poses, radar tracks as drawn by the replay, reconstructed events and states); no ground truth.  Reviewer verdict per finding.

Run verdict: **WARN**

Phase-0 WARN resolved: the van C's tracks (A:track_002, B:track_002, B:track_003) are linked to C, no extra bodies.  Remaining: U1 = B:track_004, a 0.3 s fragment ahead of C after the contacts; C's CRITICAL_TTC on A still open at TRACK_LOST 0.15 s before their contact (local semantics, unchanged).

| scenario | run | verdict | t_global [s] | problem | frame | solution |
|---|---|---|---|---|---|---|
| S16 | run_0_consequential | WARN | +1.25 .. +1.55 | U1 (B:track_004, 0.3 s) drawn just ahead of the van C after the A-C contact | [13_tgp001.30.png](visual_audit_phase2/13_tgp001.30.png) | limitation: evidence after a recorder's contact with a third body is not used for links |
| S16 | run_0_consequential | WARN | +0.05 .. +0.90 | CRITICAL_TTC(C, A) open at TRACK_LOST 0.15 s before the A-C contact | [08_tgp000.05.png](visual_audit_phase2/08_tgp000.05.png) | unchanged since phase 0; reported as a limitation |

## Frames

| frame | t_global [s] | content |
|---|---|---|
| [01_tgm005.55.png](visual_audit_phase2/01_tgm005.55.png) | -5.55 | lead-in |
| [02_tgm005.05.png](visual_audit_phase2/02_tgm005.05.png) | -5.05 | CRITICAL_TTC_START(B,track_001 (A)) |
| [03_tgm000.35.png](visual_audit_phase2/03_tgm000.35.png) | -0.35 | CRITICAL_TTC_START(A,track_001 (C)) |
| [04_tgm000.20.png](visual_audit_phase2/04_tgm000.20.png) | -0.20 | before COLLISION(A,B) |
| [05_tgm000.15.png](visual_audit_phase2/05_tgm000.15.png) | -0.15 | EGO_PATH_ENTRY(A,track_002 (C)) |
| [06_tgm000.10.png](visual_audit_phase2/06_tgm000.10.png) | -0.10 | CUT_IN_FROM_LEFT_START(A,track_001 (C)) |
| [07_tgp000.00.png](visual_audit_phase2/07_tgp000.00.png) | +0.00 | CRITICAL_TTC_END(B,track_001 (A)); COLLISION(A,B) |
| [08_tgp000.05.png](visual_audit_phase2/08_tgp000.05.png) | +0.05 | CRITICAL_TTC_START(C,track_001 (A)) |
| [09_tgp000.20.png](visual_audit_phase2/09_tgp000.20.png) | +0.20 | EGO_PATH_ENTRY(A,track_001 (C)) |
| [10_tgp000.50.png](visual_audit_phase2/10_tgp000.50.png) | +0.50 | after COLLISION(A,B) |
| [11_tgp000.85.png](visual_audit_phase2/11_tgp000.85.png) | +0.85 | before COLLISION(A,C) |
| [12_tgp001.05.png](visual_audit_phase2/12_tgp001.05.png) | +1.05 | CRITICAL_TTC_END(A,track_001 (C)); COLLISION(A,C) |
| [13_tgp001.30.png](visual_audit_phase2/13_tgp001.30.png) | +1.30 | CUT_IN_FROM_LEFT_END(A,track_001 (C)) |
| [14_tgp001.55.png](visual_audit_phase2/14_tgp001.55.png) | +1.55 | after COLLISION(A,C) |

## Automatic flags (reasons to look, not verdicts)

none

Reconstruction commit: `c79b1e627cbfaa5c042749291876597e922509f7`.
