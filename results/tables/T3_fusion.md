**T3_fusion.**  Road users that recorded nothing, canonical runs: centre error of the fused states against ground truth (instants where every source track was on the entity's own road user).

| estimate | states | median [m] | q75 [m] | p95 [m] |
|---|---|---|---|---|
| fused (all) | 925 | 0.45 | 0.85 | 1.53 |
| fused: box fit | 390 | 0.27 | 0.38 | 1.01 |
| fused: covariance intersection | 535 | 0.68 | 1.13 | 2.12 |
| single-track nominal box (baseline) | 1402 | 0.62 | 1.22 | 3.53 |

Recorder links: 42 correct, 0 wrong, 3 missed.  Merges of anonymous tracks: 15 correct, 0 false, 10 missed.  Declared uncertainty: 0.55 / 0.91 / 0.96 of the errors within 1 / 2 / 3 sigma (Gaussian 0.39 / 0.86 / 0.99).
