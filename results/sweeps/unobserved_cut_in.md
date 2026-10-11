# Sweep unobserved_cut_in (S17, base variant crash)

The non-recording C cuts into A's lane ahead of A; A swerves (privileged corridor trigger) when C is close, into B catching up in the left lane.  C's distance, speed and cut-in moment and B's distance vary: A-B crashes, swerves without contact, no swerve.

Runs complete: 40; failed: none.  Outcomes: crash 32, borderline 0, no crash 8.
Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T03:29:02Z.

Totals: collisions_reconstructed 23, associations_correct 76, associations_decided 76, anonymous_tracks 97, links_correct 76, links_wrong 0, links_missed 5, merges_correct 57, merges_false 0, merges_missed 8, entities 49

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 1.516 | 1.534 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| fused_centre_error_median_m | 40 | 0.117 | 0.097 | 0.135 | 0.388 | 1.901 |
| single_track_centre_error_median_m | 40 | 0.511 | 0.344 | 0.582 | 0.867 | 1.224 |
| record_wall_s | 40 | 30.060 | 27.913 | 33.195 | 38.562 | 44.940 |
| reconstruct_wall_s | 40 | 5.985 | 4.457 | 8.307 | 18.875 | 24.560 |
| evaluate_wall_s | 40 | 3.020 | 0.287 | 5.415 | 9.081 | 11.980 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.121 |
| 1 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.089 |
| 2 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.101 |
| 3 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.141 |
| 4 | no_crash | 1.515 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.088 |
| 5 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.114 |
| 6 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.117 |
| 7 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.108 |
| 8 | crash | 0.0 | A-C | 2 | 1/1 | 1/0/1 | 1/0/2 | 0.248 |
| 9 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.119 |
| 10 | no_crash | 1.514 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.093 |
| 11 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.135 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.169 |
| 13 | no_crash | 1.534 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.092 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.122 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.129 |
| 16 | no_crash | 1.513 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.085 |
| 17 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.135 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.159 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.131 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.133 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.116 |
| 22 | no_crash | 1.512 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.091 |
| 23 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 0/0/1 | 0.134 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.100 |
| 25 | no_crash | 1.515 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.087 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.098 |
| 27 | crash | 0.0 | A-C | 2 | 1/1 | 1/0/2 | 1/0/3 | 0.669 |
| 28 | no_crash | 1.514 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.073 |
| 29 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.114 |
| 30 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.147 |
| 31 | crash | 0.0 | A-B | 2 | 1/1 | 1/0/1 | 1/0/0 | 1.901 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.104 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.137 |
| 34 | no_crash | 1.534 | - | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.071 |
| 35 | crash | 0.0 | A-C | 2 | 1/1 | 1/0/1 | 1/0/2 | 0.373 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.100 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.103 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.123 |
| 39 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.095 |
