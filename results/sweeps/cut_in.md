# Sweep cut_in (S02, base variant crash)

B, slower, cuts from the left lane into A's lane ahead of A, then slows; A brakes late.  The gap, B's speed, the moment of the cut-in and A's braking vary: rear-end crashes, near misses and safe stops.

Runs complete: 40; failed: none.  Outcomes: crash 17, borderline 2, no crash 21.
Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T03:24:16Z.

Totals: collisions_reconstructed 17, associations_correct 83, associations_decided 83, anonymous_tracks 12, links_correct 83, links_wrong 0, links_missed 4, merges_correct 0, merges_false 0, merges_missed 0, entities 12

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 2.110 | 0.000 | 6.411 | 12.393 | 13.574 |
| max_abs_t_global_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| max_abs_relative_offset_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| fused_centre_error_median_m | 4 | 1.184 | 0.751 | 1.801 | 2.614 | 2.817 |
| single_track_centre_error_median_m | 4 | 1.325 | 1.005 | 1.639 | 1.955 | 2.034 |
| record_wall_s | 40 | 33.540 | 32.407 | 34.953 | 41.495 | 42.340 |
| reconstruct_wall_s | 40 | 2.930 | 2.520 | 3.348 | 3.756 | 4.210 |
| evaluate_wall_s | 40 | 0.195 | 0.160 | 1.915 | 2.853 | 3.320 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | no_crash | 8.514 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 2 | no_crash | 4.766 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 3 | no_crash | 12.391 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 5 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 7 | no_crash | 10.432 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 8 | no_crash | 2.695 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 9 | no_crash | 2.26 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 11 | no_crash | 6.304 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 13 | borderline | 0.868 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 14 | no_crash | 13.574 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 15 | no_crash | 3.409 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 18 | no_crash | 4.135 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 19 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 20 | no_crash | 8.796 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 22 | no_crash | 5.015 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 23 | no_crash | 11.096 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/1 | 0/0/0 | 1.462 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 26 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 2.817 |
| 27 | no_crash | 3.95 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 28 | no_crash | 2.101 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 29 | no_crash | 2.118 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 30 | no_crash | 11.438 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 31 | borderline | 0.395 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 33 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.285 |
| 34 | no_crash | 6.733 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 35 | no_crash | 12.422 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 36 | no_crash | 7.887 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 38 | no_crash | 3.744 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 39 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.906 |
