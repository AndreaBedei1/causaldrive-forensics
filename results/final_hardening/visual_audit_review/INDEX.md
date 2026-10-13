# Visual audit (visual_audit_review)

One row per run: the reviewer's verdict on the reconstruction-only replay frames (details and frames in each run's reconstruction/evaluation/visual_audit_review.md).

| scenario | run | verdict | frames | automatic flags | summary |
|---|---|---|---|---|---|
| S19 | run_0 | WARN | 15 | 3 | Scenario as specified (9 cars, 3 abreast rows, one A-B contact). Partner B named; 0 false merges, 5 wrong samples of 1258. Far rows fragmented (H, J: several entities, J never relevant) and C, E, F, G, H also split while relevant (21 missed merges). |
| S20 | run_0 | WARN | 11 | 3 | Column of 4 + staggered side lanes, B rear-ends A, partner named; 0 wrong samples. G (beside A/B) drawn twice (U6 from A, U8 from B) while relevant; U8 spins at the impact. |
| S21 | run_0 | WARN | 19 | 11 | B passes A, A drifts into B, partner named (recorder link now correct). The other cars stay 20-40 m away: the dense passing is mostly ahead of the recorders. E split into several entities while relevant; far group with box jumps (U9) and 16 wrong samples on I (far, non relevant). |
| S22 | run_0 | WARN | 18 | 3 | V hides B from A, B reappears, both merge and collide, partner named; 0 wrong samples, B kept as one road user across the occlusion. G (following car) split while relevant; one lead-in overlap. |
| S23 | run_0 | FAIL | 17 | 2 | Contact A-B named and C/D never merged (2 wrong samples), but the scenario objective is not met: C and D, which A swerves around, stay split into 4 entities each while inside the relevance envelope (22 missed merges) instead of being resolved as they come close. |
| S24 | run_0 | WARN | 11 | 4 | A hits B between C and D: partner B named (not C or D); the post-contact same-pair CRITICAL_TTC is gone. A's view of B is split into 3 entities, D, E, F likewise (14 missed merges); A starts CRITICAL_TTC with U7 (D) after the impact (a different pair). |
| S06 | run_0_a_front_pushed | PASS | 10 | 0 | Both chain contacts named; no flag. |
| S06 | run_0_b_rear_first | PASS | 8 | 0 | B-C then A-B named; no flag. |
| S10 | run_0_rolls_through | WARN | 7 | 2 | Contact A-B matched and the recorder links kept; B's first track of the crossing A (22 m, -2.7..-1.5 s) stays anonymous (U1) and is drawn over A. |
| S17 | run_0_crash | WARN | 14 | 1 | Collision and unobserved cut-in U1 correct; post-impact overlap U1/U2 at +1.75 s. |
| S18 | run_0_abreast | PASS | 9 | 0 | Collision A-B, no flag, 0 false merges. |
| S18 | run_0_passing | WARN | 10 | 1 | Collision A-B; post-contact overlap U1/U3 (unmerged duplicate). |
| S18 | run_0_platoon | WARN | 9 | 1 | Collision A-B; the same-pair CRITICAL_TTC after the contact is gone; post-contact overlap U3/U4. |
