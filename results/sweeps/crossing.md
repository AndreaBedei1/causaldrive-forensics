# Sweep crossing (S03, base variant crash)

A drives straight through a junction; B, on the crossing road, fails to yield and speeds up.  A's speed, B's distance to the junction and B's final speed vary: side impacts, near misses, clear passes.

Runs complete: 40; failed: none.  Outcomes: crash 18, borderline 7, no crash 15.
Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:22Z.

Totals: collisions_reconstructed 19, associations_correct 43, associations_decided 43, anonymous_tracks 54, links_correct 43, links_wrong 0, links_missed 54, merges_correct 11, merges_false 0, merges_missed 1, entities 43

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.362 | 0.000 | 2.104 | 4.406 | 10.076 |
| max_abs_t_global_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.350 |
| max_abs_relative_offset_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| fused_centre_error_median_m | 22 | 0.530 | 0.475 | 0.609 | 0.655 | 0.659 |
| single_track_centre_error_median_m | 22 | 0.775 | 0.614 | 0.862 | 0.921 | 0.934 |
| record_wall_s | 40 | 37.725 | 35.803 | 40.852 | 45.776 | 51.140 |
| reconstruct_wall_s | 40 | 2.570 | 2.275 | 2.732 | 3.131 | 3.530 |
| evaluate_wall_s | 40 | 7.975 | 6.902 | 9.223 | 10.568 | 11.230 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | no_crash | 3.796 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.623 |
| 1 | borderline | 0.649 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.608 |
| 2 | no_crash | 2.04 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.508 |
| 3 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 4 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 5 | borderline | 0.512 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.646 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 7 | borderline | 0.968 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.520 |
| 8 | no_crash | 10.076 | - | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.290 |
| 9 | borderline | 0.716 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.604 |
| 10 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 11 | crash | 0.02 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 12 | no_crash | 2.299 | - | 2 | 0/0 | 0/0/3 | 0/0/1 | 0.401 |
| 13 | no_crash | 2.297 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.540 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 16 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 17 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 18 | no_crash | 3.43 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.379 |
| 19 | no_crash | 2.842 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.637 |
| 20 | no_crash | 4.205 | - | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.567 |
| 21 | borderline | 0.0 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.659 |
| 22 | no_crash | 7.265 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.487 |
| 23 | borderline | 0.525 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.494 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 25 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 26 | no_crash | 1.132 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.560 |
| 27 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 28 | borderline | 0.213 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.435 |
| 29 | no_crash | 1.255 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.656 |
| 30 | crash | 0.0 | A-B | 2 | 4/4 | 4/0/0 | 0/0/0 | - |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 34 | no_crash | 1.005 | - | 2 | 0/0 | 0/0/3 | 1/0/0 | 0.507 |
| 35 | crash | 0.0 | A-B | 2 | 3/3 | 3/0/0 | 0/0/0 | - |
| 36 | no_crash | 3.021 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.410 |
| 37 | no_crash | 1.502 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.610 |
| 38 | no_crash | 4.256 | - | 2 | 0/0 | 0/0/2 | 0/0/0 | 0.471 |
| 39 | crash | 0.0 | A-B | 2 | 4/4 | 4/0/0 | 0/0/0 | - |
