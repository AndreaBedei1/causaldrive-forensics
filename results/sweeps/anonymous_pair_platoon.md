# Sweep anonymous_pair_platoon (S18, base variant platoon)

The non-recording C and D in one lane ahead of A, D behind C at a varied distance and both at about the same speed; A drifts into B for the alignment.  The fusion must keep C and D apart.

Runs complete: 40; failed: none.  Outcomes: crash 40, borderline 0, no crash 0.
Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T03:30:14Z.

Totals: collisions_reconstructed 41, associations_correct 80, associations_decided 80, anonymous_tracks 230, links_correct 80, links_wrong 0, links_missed 0, merges_correct 101, merges_false 0, merges_missed 128, entities 144

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| fused_centre_error_median_m | 40 | 0.440 | 0.349 | 0.512 | 0.730 | 0.906 |
| single_track_centre_error_median_m | 40 | 0.390 | 0.328 | 0.483 | 0.578 | 0.632 |
| record_wall_s | 40 | 34.355 | 31.955 | 37.432 | 42.926 | 46.520 |
| reconstruct_wall_s | 40 | 6.425 | 5.325 | 7.447 | 8.857 | 10.000 |
| evaluate_wall_s | 40 | 5.945 | 5.320 | 7.105 | 8.428 | 9.440 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/7 | 0.291 |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.284 |
| 2 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.547 |
| 3 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.346 |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.441 |
| 5 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.273 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/5 | 0.362 |
| 7 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.906 |
| 8 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.482 |
| 9 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.298 |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/5 | 0.396 |
| 11 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.324 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.483 |
| 13 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.367 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.442 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.510 |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.465 |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.462 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.492 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/7 | 0.276 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/9 | 0.438 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.423 |
| 22 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.730 |
| 23 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.303 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.381 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.314 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.604 |
| 27 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.359 |
| 28 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.558 |
| 29 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.487 |
| 30 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.482 |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.559 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/4 | 0.412 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.364 |
| 34 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.612 |
| 35 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/5 | 0.286 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.349 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/7 | 0.580 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.740 |
| 39 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.519 |
