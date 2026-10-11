**T3_fusion.**  Road users that recorded nothing, canonical runs: centre error of the fused states against ground truth (instants where every source track was on the entity's own road user).

| estimate | states | median [m] | q75 [m] | p95 [m] |
|---|---|---|---|---|
| fused (all) | 958 | 0.53 | 0.98 | 1.43 |
| fused: box fit | 477 | 0.29 | 0.43 | 0.92 |
| fused: covariance intersection | 481 | 0.97 | 1.11 | 2.45 |
| single-track nominal box (baseline) | 1557 | 0.64 | 1.35 | 3.53 |

Recorder links: 44 correct, 0 wrong, 7 missed.  Merges of anonymous tracks: 23 correct, 0 false, 16 missed.  Declared uncertainty: 0.64 / 0.90 / 0.95 of the errors within 1 / 2 / 3 sigma (Gaussian 0.39 / 0.86 / 0.99).
