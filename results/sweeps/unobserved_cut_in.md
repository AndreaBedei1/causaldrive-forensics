# Sweep unobserved_cut_in (S17, base variant crash)

The non-recording C cuts into A's lane ahead of A; A swerves (privileged corridor trigger) when C is close, into B catching up in the left lane.  C's distance, speed and cut-in moment and B's distance vary: A-B crashes, swerves without contact, no swerve.

Runs complete: 40; failed: none.  Outcomes: crash 32, borderline 0, no crash 8.
Provenance: code `c76d72a3965907b6`, configuration `50f7dc9e35556156`, commit `fd8d2baed644db4a32c2eb502a2eeb9b32f70887` (uncommitted changes), 2026-10-11T09:35:37Z.

Totals: collisions_reconstructed 23, associations_correct 78, associations_decided 78, anonymous_tracks 107, links_correct 78, links_wrong 0, links_missed 4, merges_correct 62, merges_false 0, merges_missed 28, entities 57

| quantity | n | median | q25 | q75 | p95 | max |
|---|--:|--:|--:|--:|--:|--:|
| min_gap_m | 40 | 0.000 | 0.000 | 0.000 | 1.516 | 1.534 |
| max_abs_t_global_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 |
| max_abs_relative_offset_error_s | 40 | 0.000 | 0.000 | 0.000 | 0.000 | 0.050 |
| fused_centre_error_median_m | 40 | 0.117 | 0.099 | 0.138 | 0.254 | 0.705 |
| single_track_centre_error_median_m | 40 | 0.494 | 0.344 | 0.582 | 0.979 | 1.224 |
| record_wall_s | 40 | 30.060 | 27.913 | 33.195 | 38.562 | 44.940 |
| reconstruct_wall_s | 40 | 4.705 | 3.728 | 5.798 | 7.077 | 8.540 |
| evaluate_wall_s | 40 | 3.515 | 3.087 | 3.833 | 4.822 | 5.430 |

| k | outcome | min gap [m] | contacts | aligned | assoc. | links c/w/m | merges c/f/m | fused centre [m] |
|--:|---|--:|---|--:|--:|---|---|--:|
| 0 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.138 |
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
| 11 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 3/0/3 | 0.138 |
| 12 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.169 |
| 13 | no_crash | 1.534 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.092 |
| 14 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.122 |
| 15 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.129 |
| 16 | no_crash | 1.513 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.085 |
| 17 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 6/0/4 | 0.140 |
| 18 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.159 |
| 19 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.131 |
| 20 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.133 |
| 21 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/2 | 0.113 |
| 22 | no_crash | 1.512 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.091 |
| 23 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 0/0/1 | 0.134 |
| 24 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.100 |
| 25 | no_crash | 1.515 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.087 |
| 26 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.098 |
| 27 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/2 | 3/0/4 | 0.705 |
| 28 | no_crash | 1.514 | - | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.073 |
| 29 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.114 |
| 30 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.147 |
| 31 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.158 |
| 32 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.104 |
| 33 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.137 |
| 34 | no_crash | 1.534 | - | 2 | 2/2 | 2/0/0 | 3/0/0 | 0.071 |
| 35 | crash | 0.0 | A-C | 2 | 1/1 | 1/0/1 | 1/0/2 | 0.373 |
| 36 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/2 | 0.106 |
| 37 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.103 |
| 38 | crash | 0.0 | A-B | 2 | 2/2 | 2/0/0 | 1/0/0 | 0.123 |
| 39 | crash | 0.0 | A-C | 2 | 2/2 | 2/0/0 | 1/0/5 | 0.116 |
