# Visual audit (visual_audit_hardening)

One row per run: the reviewer's verdict on the reconstruction-only replay frames (details and frames in each run's reconstruction/evaluation/visual_audit_hardening.md).

| scenario | run | verdict | frames | automatic flags | summary |
|---|---|---|---|---|---|
| S06 | run_0_a_front_pushed | PASS | 10 | 0 | Three recorders; both chain contacts named A-B and B-C at the right instants; no anonymous road user, no overlap, no jump. |
| S06 | run_0_b_rear_first | PASS | 8 | 0 | B-C first, then A-B, both named correctly (the case lost by the lower-bound-only rule during development); bodies stay apart. |
| S10 | run_0_rolls_through | PASS | 8 | 0 | The S10 regression is gone: A rolling through the stop is named as B's partner at the contact; no spurious road user. |
| S17 | run_0_crash | WARN | 12 | 1 | Collision A-B and the unobserved cut-in U1 are correct up to +0.5 s; the automatic flag reports a second anonymous body overlapping U1 from +1.75 s (post-impact duplicate, after the analysed window). |
| S18 | run_0_abreast | WARN | 9 | 1 | Collision A-B correct; anonymous U1 box jumps 3.7 m at -1.1 s (re-assignment between two abreast cars or a late merge). |
| S18 | run_0_platoon | WARN | 9 | 1 | Collision A-B correct; after the contact U3 (seen by B) and U4 (seen by A) are drawn on top of each other ahead: one car not merged (conservative, but a visible duplicate). |
| S18 | run_0_passing | WARN | 9 | 1 | Collision A-B correct; after the contact two anonymous bodies (U1 / U3) overlap: an unmerged cross-recorder duplicate. |
| S19 | run_0 | WARN | 11 | 3 | Contact A-B named correctly at the sideswipe, abreast rows kept apart near the recorders; at lead-in two single-observer tracks of one far car overlap (U2/U9 region) and at the far front U14/U15 overlap briefly. |
| S20 | run_0 | WARN | 12 | 1 | B rear-ends A, named correctly (the collision lost during development is back); a transient duplicate U5/U8 in the right lane at -1.05 s ends when B's track is lost. |
| S21 | run_0 | WARN | 18 | 11 | Sideswipe A-B named correctly; 25-35 m ahead a far group (U9/U10/U11, U14/U15) is drawn with overlapping bodies, U11 spins 46 deg and several boxes jump 4 m after the contact: far single-observer fragments, outside the relevance envelope, not merged. |
| S22 | run_0 | WARN | 19 | 2 | Merge contact A-B correct, the occluded car reappears as one road user near the recorders; overlapping pair U3/U6 at lead-in and a 3.8 m box jump of U2 at +3.7 s. |
| S23 | run_0 | WARN | 17 | 3 | Contact A-B after A swerves is named correctly; at long range (about 45 m, beyond the relevance envelope) U5/U6 overlap and U4/U5 touch; U2 drawn tilted and jumping 3.2 m at -6.3 s. |
| S24 | run_0 | WARN | 9 | 4 | A rear-ends B between C and D: partner B named correctly, not the abreast neighbours; U3 (seen by B) and U8 (seen by A) are one car in the right lane drawn twice; A starts a CRITICAL_TTC to B 0.45 s after their own contact while they stay touching. |
