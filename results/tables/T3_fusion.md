**T3_fusion.**  Road users that recorded nothing, canonical runs: centre error of the fused states against ground truth (instants where every source track was on the entity's own road user).

| estimate | states | median [m] | q75 [m] | p95 [m] |
|---|---|---|---|---|
| fused (all) | 721 | 0.35 | 0.72 | 1.24 |
| fused: box fit | 451 | 0.26 | 0.36 | 0.76 |
| fused: covariance intersection | 270 | 0.77 | 0.99 | 3.47 |
| single-track nominal box (baseline) | 720 | 0.61 | 0.92 | 1.56 |

Recorder links: 46 correct, 0 wrong, 1 missed.  Merges of anonymous tracks: 17 correct, 0 false, 10 missed.  Declared uncertainty: 0.61 / 0.91 / 0.96 of the errors within 1 / 2 / 3 sigma (Gaussian 0.39 / 0.86 / 0.99).
