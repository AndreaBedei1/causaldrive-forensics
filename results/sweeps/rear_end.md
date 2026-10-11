# Sweep rear_end (S01, base variant crash)

A follows B in one lane at the same speed; B brakes hard at 4.0 s; A brakes after a reaction that varies, at a gap and speed that vary.  Spans rear-end crashes, near misses and safe stops.

Runs complete: 40; failed: none.  Outcomes: crash 8, borderline 4, no crash 28.
Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T03:23:07Z.

Totals: collisions_reconstructed 8, associations_correct 41, associations_decided 41, anonymous_tracks 2, links_correct 41, links_wrong 0, links_missed 2, merges_correct 0, merges_false 0, merges_missed 0, entities 2

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 5.910 | 0.727 | 11.348 | 17.597 | 18.190 |
| max_abs_t_global_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| max_abs_relative_offset_error_s | 40 | 0.050 | 0.000 | 0.050 | 0.050 | 0.050 |
| fused_centre_error_median_m | 2 | 0.539 | 0.501 | 0.578 | 0.609 | 0.616 |
| single_track_centre_error_median_m | 2 | 0.527 | 0.497 | 0.556 | 0.580 | 0.586 |
| record_wall_s | 40 | 29.175 | 28.040 | 31.218 | 75.262 | 169.800 |
| reconstruct_wall_s | 40 | 1.865 | 1.657 | 1.982 | 2.272 | 2.520 |
| evaluate_wall_s | 40 | 0.120 | 0.100 | 0.163 | 1.129 | 1.390 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.025 | A-B | 2 | 2/2 | 2/0/0 | 0/0/0 | - |
| 1 | no_crash | 17.866 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 2 | no_crash | 6.518 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 3 | no_crash | 6.749 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 4 | borderline | 0.408 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 5 | no_crash | 11.182 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 6 | no_crash | 13.66 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 7 | no_crash | 3.241 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 8 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 9 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 10 | no_crash | 18.19 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 11 | no_crash | 7.496 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 12 | no_crash | 10.439 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 13 | no_crash | 7.251 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 14 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 15 | no_crash | 17.15 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 16 | no_crash | 3.602 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 17 | no_crash | 2.161 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 18 | no_crash | 4.962 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 19 | borderline | 0.924 | - | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.616 |
| 20 | no_crash | 9.563 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 21 | no_crash | 13.608 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 22 | borderline | 0.724 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 23 | no_crash | 1.469 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 24 | borderline | 0.728 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 25 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 26 | no_crash | 7.36 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 27 | no_crash | 7.293 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 28 | no_crash | 12.41 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 29 | crash | 0.068 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 30 | no_crash | 14.844 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 31 | no_crash | 17.583 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 32 | no_crash | 4.529 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 33 | no_crash | 5.302 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 34 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 35 | no_crash | 10.003 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 36 | no_crash | 11.966 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 37 | no_crash | 11.846 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 38 | no_crash | 1.537 | - | 2 | 1/1 | 1/0/0 | 0/0/0 | - |
| 39 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 0/0/0 | 0.463 |
