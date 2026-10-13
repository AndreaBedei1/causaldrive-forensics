# Road-user fusion against ground truth - S19/run_0_collision_ambiguity

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_002 | U2 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_003 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_005#segment_1 | U8 | ANONYMOUS | - | B | 0.923 | missed link (true identity B) |
| A:track_005#segment_2 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_006 | U7 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_007 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_008 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_009 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_010 | U9 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_011 | U10 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001 | U5 | ANONYMOUS | - | H | 0.918 | anonymous (non-recording road user H) |
| B:track_002 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_003 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_004 | U7 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_005 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_006 | U11 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_007 | U12 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |

Counts: anonymous: 16, correct link: 2, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_005 | D | no | 1.000 |
| U2 | A:track_002 | E | no | 1.000 |
| U3 | A:track_003, B:track_003, A:track_009 | H | no | 1.000 |
| U4 | A:track_004 | F | no | 1.000 |
| U5 | B:track_001 | H | no | 0.918 |
| U6 | B:track_002, A:track_007 | G | no | 1.000 |
| U7 | B:track_004, A:track_006 | C | no | 1.000 |
| U8 | A:track_005#segment_1 | B | yes | 0.923 |
| U9 | A:track_010 | E | no | 1.000 |
| U10 | A:track_011 | F | no | 1.000 |
| U11 | B:track_006 | E | no | 1.000 |
| U12 | B:track_007 | F | no | 1.000 |

Merges over pairs of anonymous tracks: correct 6, false 0, missed 9.
Fragmentation (true road user -> entities): B -> U8, C -> U7, D -> U1, E -> U11/U2/U9, F -> U10/U12/U4, G -> U6, H -> U3/U5

## Fused state errors (against the majority identity, 774 pure states; 23 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 774 | 0.310 | 0.137 | 1.073 | 0.936 | 2.038 | 2.264 | 2.796 |
| coverage_s | 12 | 5.800 | 2.312 | 11.425 | 9.113 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 774 | 1.025 | 0.268 | 2.353 | 2.085 | 6.217 | 10.294 | 19.675 |
| length_error_m | 12 | 0.192 | 0.086 | 0.419 | 0.333 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 774 | 0.550 | 0.306 | 1.515 | 1.209 | 2.572 | 3.472 | 4.801 |
| single_track_nominal_centre_error_m | 762 | 0.549 | 0.392 | 0.928 | 0.537 | 1.742 | 1.929 | 2.296 |
| speed_error_mps | 774 | 0.104 | 0.029 | 0.311 | 0.282 | 0.915 | 1.403 | 4.228 |
| velocity_error_mps | 774 | 0.284 | 0.071 | 0.623 | 0.552 | 1.481 | 3.052 | 4.233 |
| width_error_m | 12 | 0.107 | 0.094 | 0.146 | 0.052 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 345 | 0.140 | 0.085 | 0.267 | 0.182 | 0.657 | 1.164 | 1.811 |
| heading_error_deg | 345 | 0.764 | 0.182 | 2.334 | 2.152 | 7.619 | 14.869 | 19.616 |
| speed_error_mps | 345 | 0.092 | 0.033 | 0.352 | 0.319 | 1.020 | 1.532 | 3.181 |
| velocity_error_mps | 345 | 0.193 | 0.059 | 0.599 | 0.540 | 1.931 | 3.267 | 4.107 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 429 | 0.753 | 0.295 | 1.813 | 1.517 | 2.238 | 2.380 | 2.796 |
| heading_error_deg | 429 | 1.228 | 0.360 | 2.382 | 2.023 | 5.655 | 7.312 | 19.675 |
| speed_error_mps | 429 | 0.114 | 0.027 | 0.288 | 0.261 | 0.767 | 1.233 | 4.228 |
| velocity_error_mps | 429 | 0.373 | 0.090 | 0.641 | 0.551 | 1.349 | 2.779 | 4.233 |

Calibration of pos_std_m over 774 states: within 1/2/3 sigma 0.652/0.884/0.917 (Gaussian: 0.393/0.865/0.989).
