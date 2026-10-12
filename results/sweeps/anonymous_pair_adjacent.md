# Sweep anonymous_pair_adjacent (S18, base variant abreast)

The non-recording C and D in adjacent lanes ahead of the recorders, D's longitudinal offset from C and its speed varied (abreast, passing, staggered); A drifts into B for the alignment.  The fusion must keep C and D apart.

Runs complete: 40; failed: none.  Outcomes: crash 40, borderline 0, no crash 0.
Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:21Z.

Totals: collisions_reconstructed 44, associations_correct 80, associations_decided 80, anonymous_tracks 212, links_correct 80, links_wrong 0, links_missed 0, merges_correct 155, merges_false 0, merges_missed 59, entities 98

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.562 | 0.850 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| fused_centre_error_median_m | 40 | 0.316 | 0.273 | 0.379 | 0.418 | 0.442 |
| single_track_centre_error_median_m | 40 | 0.471 | 0.422 | 0.500 | 0.661 | 0.754 |
| record_wall_s | 40 | 36.810 | 30.953 | 42.540 | 48.146 | 49.720 |
| reconstruct_wall_s | 40 | 14.795 | 12.335 | 16.552 | 20.509 | 22.520 |
| evaluate_wall_s | 40 | 14.770 | 13.395 | 15.930 | 17.458 | 20.560 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.212 |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.251 |
| 2 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 7/0/0 | 0.419 |
| 3 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/2 | 0.442 |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/6 | 0.366 |
| 5 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.268 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.321 |
| 7 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 7/0/0 | 0.386 |
| 8 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.296 |
| 9 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.209 |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.313 |
| 11 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.311 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/5 | 0.345 |
| 13 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.269 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/8 | 0.383 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.333 |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.376 |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.293 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.259 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 16/0/0 | 0.383 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 7/0/9 | 0.396 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.273 |
| 22 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 6/0/0 | 0.396 |
| 23 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.297 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.271 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.247 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/3 | 0.378 |
| 27 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.232 |
| 28 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/9 | 0.404 |
| 29 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.284 |
| 30 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.314 |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.418 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.367 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.231 |
| 34 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.319 |
| 35 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 5/0/11 | 0.377 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/2 | 0.281 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 4/0/0 | 0.279 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 5/0/4 | 0.388 |
| 39 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 2/0/0 | 0.321 |
