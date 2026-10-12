# Sweep cut_in (S02, base variant crash)

B, slower, cuts from the left lane into A's lane ahead of A, then slows; A brakes late.  The gap, B's speed, the moment of the cut-in and A's braking vary: rear-end crashes, near misses and safe stops.

Runs complete: 40; failed: none.  Outcomes: crash 17, borderline 2, no crash 21.
Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:23Z.

Totals: collisions_reconstructed 17, associations_correct 83, associations_decided 83, anonymous_tracks 24, links_correct 83, links_wrong 0, links_missed 12, merges_correct 0, merges_false 0, merges_missed 1, entities 24

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 2.110 | 0.000 | 6.411 | 12.393 | 13.574 |
| max_abs_t_global_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.250 |
| max_abs_relative_offset_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| fused_centre_error_median_m | 10 | 0.634 | 0.513 | 0.881 | 2.252 | 2.817 |
| single_track_centre_error_median_m | 10 | 0.668 | 0.598 | 1.078 | 1.796 | 2.034 |
| record_wall_s | 40 | 33.540 | 32.407 | 34.953 | 41.495 | 42.340 |
| reconstruct_wall_s | 40 | 2.685 | 2.400 | 3.275 | 4.642 | 4.890 |
| evaluate_wall_s | 40 | 10.405 | 6.503 | 12.078 | 14.211 | 15.790 |

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
| 14 | no_crash | 13.574 | - | 2 | 3/3 | 3/0/1 | 0/0/0 | 0.670 |
| 15 | no_crash | 3.409 | - | 2 | 3/3 | 3/0/1 | 0/0/0 | 0.807 |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 18 | no_crash | 4.135 | - | 2 | 3/3 | 3/0/1 | 0/0/0 | 0.597 |
| 19 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 20 | no_crash | 8.796 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 22 | no_crash | 5.015 | - | 2 | 3/3 | 3/0/1 | 0/0/0 | 0.536 |
| 23 | no_crash | 11.096 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/2 | 0/0/1 | 1.563 |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 26 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 2.817 |
| 27 | no_crash | 3.95 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 28 | no_crash | 2.101 | - | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 29 | no_crash | 2.118 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 30 | no_crash | 11.438 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 31 | borderline | 0.395 | - | 2 | 2/2 | 2/0/1 | 0/0/0 | 0.409 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 33 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.285 |
| 34 | no_crash | 6.733 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 35 | no_crash | 12.422 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 36 | no_crash | 7.887 | - | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 38 | no_crash | 3.744 | - | 2 | 2/2 | 2/0/1 | 0/0/0 | 0.506 |
| 39 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/2 | 0/0/0 | 0.906 |
