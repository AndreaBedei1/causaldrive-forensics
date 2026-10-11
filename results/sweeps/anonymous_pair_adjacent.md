# Sweep anonymous_pair_adjacent (S18, base variant abreast)

The non-recording C and D in adjacent lanes ahead of the recorders, D's longitudinal offset from C and its speed varied (abreast, passing, staggered); A drifts into B for the alignment.  The fusion must keep C and D apart.

Runs complete: 40; failed: none.  Outcomes: crash 40, borderline 0, no crash 0.
Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T03:36:36Z.

Totals: collisions_reconstructed 44, associations_correct 80, associations_decided 80, anonymous_tracks 207, links_correct 80, links_wrong 0, links_missed 0, merges_correct 143, merges_false 3, merges_missed 51, entities 98

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| fused_centre_error_median_m | 40 | 0.324 | 0.277 | 0.384 | 0.418 | 0.427 |
| single_track_centre_error_median_m | 40 | 0.402 | 0.366 | 0.446 | 0.568 | 0.683 |
| record_wall_s | 40 | 36.810 | 30.953 | 42.540 | 48.146 | 49.720 |
| reconstruct_wall_s | 40 | 10.130 | 8.940 | 12.525 | 15.924 | 25.730 |
| evaluate_wall_s | 40 | 9.660 | 8.518 | 11.502 | 20.017 | 26.020 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.206 |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.251 |
| 2 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 7/0/0 | 0.427 |
| 3 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 9/0/0 | 0.369 |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/1 | 0.367 |
| 5 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.268 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.339 |
| 7 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 7/0/0 | 0.386 |
| 8 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.401 |
| 9 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.209 |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.315 |
| 11 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.311 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.339 |
| 13 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.268 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/8 | 0.383 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.297 |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/2/2 | 0.327 |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.293 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.279 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 16/0/0 | 0.414 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/1 | 0.370 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.273 |
| 22 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 6/0/0 | 0.389 |
| 23 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.297 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.268 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.272 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/3 | 0.384 |
| 27 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.232 |
| 28 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/1/4 | 0.420 |
| 29 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.384 |
| 30 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.314 |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.418 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.415 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.236 |
| 34 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.332 |
| 35 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 5/0/11 | 0.381 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.281 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.291 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 5/0/4 | 0.390 |
| 39 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.321 |
