# Sweep anonymous_pair_platoon (S18, base variant platoon)

The non-recording C and D in one lane ahead of A, D behind C at a varied distance and both at about the same speed; A drifts into B for the alignment.  The fusion must keep C and D apart.

Runs complete: 40; failed: none.  Outcomes: crash 40, borderline 0, no crash 0.
Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:21Z.

Totals: collisions_reconstructed 41, associations_correct 80, associations_decided 80, anonymous_tracks 230, links_correct 80, links_wrong 0, links_missed 0, merges_correct 107, merges_false 0, merges_missed 122, entities 140

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.405 | 0.600 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| fused_centre_error_median_m | 40 | 0.429 | 0.345 | 0.519 | 0.767 | 0.906 |
| single_track_centre_error_median_m | 40 | 0.476 | 0.381 | 0.531 | 0.761 | 0.835 |
| record_wall_s | 40 | 34.355 | 31.955 | 37.432 | 42.926 | 46.520 |
| reconstruct_wall_s | 40 | 8.150 | 7.008 | 10.520 | 11.409 | 12.480 |
| evaluate_wall_s | 40 | 12.455 | 12.107 | 12.910 | 13.496 | 14.180 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/7 | 0.291 |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.284 |
| 2 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.547 |
| 3 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.346 |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.425 |
| 5 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.273 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.498 |
| 7 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.906 |
| 8 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.482 |
| 9 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.298 |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/5 | 0.396 |
| 11 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.324 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.468 |
| 13 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.341 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.442 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.510 |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.465 |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.460 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.476 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/7 | 0.276 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/6 | 0.647 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.418 |
| 22 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/5 | 0.764 |
| 23 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.303 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.383 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.314 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.681 |
| 27 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.359 |
| 28 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.558 |
| 29 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.479 |
| 30 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.432 |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.559 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/4 | 0.412 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.364 |
| 34 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/3 | 0.612 |
| 35 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/5 | 0.286 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.349 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.383 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.813 |
| 39 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.543 |
