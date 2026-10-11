# Collision impulses: symmetry and noise margin

Historical diagnosis of the fixed 10% relative gate. Its measurements and
execution provenance are retained. The final geometry-supported uncertainty
gate is evaluated in [technical hardening](../../docs/audit/technical_hardening.md).

CARLA's collision sensor gives both bodies of a contact the magnitude of the same contact impulse (ground-truth log: largest relative difference between the two reports of one contact, over all runs: 0.0).  The alignment pairs reports whose peak impulses agree within 10% (`fusion.impulse_tolerance`, an engineering assumption); a real recorder would estimate the impulse from its own sensors, with errors.  Per matched contact: its similarity, the most similar report of another contact (above 1 - tolerance it competes, and only the clock consistency of the earlier matches separates the two), and the probability that the pair still passes the test when every report carries an independent multiplicative Gaussian error (Monte Carlo, 20000 draws).

| run | contact | recorders | peaks [N s] | similarity | nearest other contact | P(pass) at 2% | P(pass) at 5% | P(pass) at 10% | P(pass) at 20% |
|---|---|---|---|--:|--:|--:|--:|--:|--:|
| S01/run_0_crash | collision_001 | A-B | 14394 / 14394 | 1.000 | 0.000 | 1.00 | 0.86 | 0.55 | 0.29 |
| S02/run_0_crash | collision_001 | A-B | 2900 / 2900 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S02/run_0_critical_before_cut_in | collision_001 | A-B | 604 / 604 | 1.000 | 0.000 | 1.00 | 0.86 | 0.55 | 0.29 |
| S03/run_0_crash | collision_001 | A-B | 12138 / 12138 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.28 |
| S06/run_0_a_front_pushed | collision_001 | A-B | 10281 / 10281 | 1.000 | 0.855 | 1.00 | 0.86 | 0.54 | 0.29 |
| S06/run_0_a_front_pushed | collision_002 (merged burst) | A-B | 1510 / 1510 | 1.000 | 0.147 | 1.00 | 0.86 | 0.54 | 0.29 |
| S06/run_0_a_front_pushed | collision_003 | B-C | 8788 / 8788 | 1.000 | 0.855 | 1.00 | 0.86 | 0.54 | 0.29 |
| S06/run_0_b_rear_first | collision_001 | A-B | 31706 / 31706 | 1.000 | 0.689 | 1.00 | 0.87 | 0.54 | 0.29 |
| S06/run_0_b_rear_first | collision_002 | B-C | 21842 / 21842 | 1.000 | 0.689 | 1.00 | 0.86 | 0.54 | 0.29 |
| S07/run_0_crash | collision_001 | A-B | 22183 / 22183 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S08/run_0_crash | collision_001 | A-B | 12137 / 12137 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S09/run_0_merge_conflict | collision_001 | A-B | 1905 / 1905 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S10/run_0_rolls_through | collision_001 | A-B | 12940 / 12940 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.28 |
| S12/run_0_near_simultaneous | collision_001 | A-B | 7661 / 7661 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S15/run_0_deflected_into_c | collision_001 | A-B | 10358 / 10358 | 1.000 | 0.181 | 1.00 | 0.86 | 0.55 | 0.29 |
| S15/run_0_deflected_into_c | collision_002 | A-C | 1880 / 1880 | 1.000 | 0.181 | 1.00 | 0.87 | 0.55 | 0.29 |
| S16/run_0_consequential | collision_001 | A-B | 4244 / 4244 | 1.000 | 0.076 | 1.00 | 0.86 | 0.54 | 0.29 |
| S16/run_0_consequential | collision_002 | A-C | 322 / 322 | 1.000 | 0.076 | 1.00 | 0.86 | 0.54 | 0.29 |
| S17/run_0_crash | collision_001 | A-B | 1577 / 1577 | 1.000 | 0.000 | 1.00 | 0.87 | 0.54 | 0.29 |
| S18/run_0_abreast | collision_001 | A-B | 1080 / 1080 | 1.000 | 0.000 | 1.00 | 0.86 | 0.55 | 0.29 |
| S18/run_0_passing | collision_001 | A-B | 1092 / 1092 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |
| S18/run_0_platoon | collision_001 | A-B | 1098 / 1098 | 1.000 | 0.000 | 1.00 | 0.86 | 0.54 | 0.29 |

Mean probability over the matched contacts that a pair still passes: 2% noise: 1.00, 5% noise: 0.86, 10% noise: 0.54, 20% noise: 0.29.
