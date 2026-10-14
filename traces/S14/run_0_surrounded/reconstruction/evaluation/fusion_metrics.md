# Road-user fusion against ground truth - S14/run_0_surrounded

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| A:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_003 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_004#segment_1 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004#segment_2 | U11 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004#segment_3 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_005 | U12 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_006 | U9 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_007 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_008 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_009 | U13 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_001 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_002 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| B:track_003 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| B:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_005 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_006 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_007 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_008 | U7 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_009 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_010 | U9 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_011 | U10 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_012 | U13 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |

Counts: anonymous: 21, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | P | no | 1.000 |
| U2 | A:track_002, B:track_005 | C | no | 1.000 |
| U3 | B:track_001, A:track_004#segment_1, A:track_004#segment_3 | D | no | 1.000 |
| U4 | B:track_004 | F | no | 1.000 |
| U5 | B:track_006, A:track_007 | E | no | 1.000 |
| U6 | B:track_007 | G | no | 1.000 |
| U7 | B:track_008 | H | no | 1.000 |
| U8 | B:track_009, A:track_008 | F | no | 1.000 |
| U9 | B:track_010, A:track_006 | G | no | 1.000 |
| U10 | B:track_011 | H | no | 1.000 |
| U11 | A:track_004#segment_2 | D | no | 1.000 |
| U12 | A:track_005 | J | no | 1.000 |
| U13 | B:track_012, A:track_009 | J | no | 1.000 |

Merges over pairs of anonymous tracks: correct 9, false 0, missed 10.
Fragmentation (true road user -> entities): C -> U2, D -> U11/U3, E -> U5, F -> U4/U8, G -> U6/U9, H -> U10/U7, J -> U12/U13, P -> U1

## Fused state errors (against the majority identity, 754 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 754 | 0.181 | 0.099 | 0.397 | 0.298 | 0.661 | 0.774 | 2.129 |
| coverage_s | 13 | 3.800 | 2.000 | 11.900 | 9.900 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 754 | 0.548 | 0.241 | 1.160 | 0.919 | 2.273 | 3.008 | 15.014 |
| length_error_m | 13 | 0.192 | 0.086 | 0.419 | 0.333 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 754 | 0.428 | 0.243 | 0.831 | 0.588 | 1.286 | 1.426 | 2.627 |
| single_track_nominal_centre_error_m | 741 | 0.323 | 0.213 | 0.530 | 0.317 | 0.719 | 0.822 | 1.177 |
| speed_error_mps | 754 | 0.037 | 0.014 | 0.075 | 0.061 | 0.117 | 0.160 | 0.925 |
| velocity_error_mps | 754 | 0.131 | 0.063 | 0.278 | 0.215 | 0.545 | 0.715 | 3.249 |
| width_error_m | 13 | 0.107 | 0.094 | 0.263 | 0.169 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 508 | 0.119 | 0.079 | 0.210 | 0.131 | 0.288 | 0.346 | 0.801 |
| heading_error_deg | 508 | 0.405 | 0.184 | 0.825 | 0.641 | 1.575 | 2.186 | 3.965 |
| speed_error_mps | 508 | 0.034 | 0.014 | 0.068 | 0.054 | 0.105 | 0.142 | 0.925 |
| velocity_error_mps | 508 | 0.095 | 0.054 | 0.215 | 0.161 | 0.392 | 0.545 | 1.038 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 246 | 0.546 | 0.348 | 0.734 | 0.386 | 0.819 | 0.893 | 2.129 |
| heading_error_deg | 246 | 1.068 | 0.498 | 2.115 | 1.617 | 3.333 | 5.009 | 15.014 |
| speed_error_mps | 246 | 0.043 | 0.013 | 0.084 | 0.071 | 0.145 | 0.186 | 0.340 |
| velocity_error_mps | 246 | 0.222 | 0.112 | 0.446 | 0.334 | 0.772 | 1.120 | 3.249 |

Calibration of pos_std_m over 754 states: within 1/2/3 sigma 0.816/0.996/1.000 (Gaussian: 0.393/0.865/0.989).
