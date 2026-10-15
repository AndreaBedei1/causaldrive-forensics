# Road-user fusion against ground truth - S14/run_0_surrounded

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| A:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_003 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_004 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_005 | U9 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_006 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_007 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_008 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_009 | U11 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_001 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_002 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| B:track_003 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| B:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_005 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_006 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_007 | U6 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_008 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_009 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_010 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_011 | U8 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_012 | U10 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_013 | U11 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_014 | U12 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |

Counts: anonymous: 21, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | P | no | 1.000 |
| U2 | A:track_002, B:track_005 | C | no | 1.000 |
| U3 | B:track_001, A:track_004 | D | no | 1.000 |
| U4 | B:track_004, B:track_010, A:track_008 | F | no | 1.000 |
| U5 | B:track_006, A:track_007 | E | no | 1.000 |
| U6 | B:track_007 | H | no | 1.000 |
| U7 | B:track_008, B:track_009, A:track_006 | G | no | 1.000 |
| U8 | B:track_011 | H | no | 1.000 |
| U9 | A:track_005 | J | no | 1.000 |
| U10 | B:track_012 | H | no | 1.000 |
| U11 | B:track_013, A:track_009 | J | no | 1.000 |
| U12 | B:track_014 | H | no | 1.000 |

Merges over pairs of anonymous tracks: correct 11, false 0, missed 8.
Fragmentation (true road user -> entities): C -> U2, D -> U3, E -> U5, F -> U4, G -> U7, H -> U10/U12/U6/U8, J -> U11/U9, P -> U1

## Fused state errors (against the majority identity, 744 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 744 | 0.147 | 0.093 | 0.399 | 0.307 | 0.668 | 0.751 | 2.164 |
| coverage_s | 12 | 7.525 | 0.662 | 11.950 | 11.287 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 744 | 0.343 | 0.140 | 0.926 | 0.787 | 2.394 | 3.358 | 14.504 |
| length_error_m | 12 | 0.192 | 0.166 | 0.249 | 0.083 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 744 | 1.769 | 1.164 | 3.366 | 2.202 | 5.035 | 5.819 | 8.563 |
| single_track_nominal_centre_error_m | 725 | 0.324 | 0.215 | 0.532 | 0.317 | 0.726 | 0.824 | 1.809 |
| speed_error_mps | 744 | 0.025 | 0.011 | 0.057 | 0.046 | 0.091 | 0.124 | 0.334 |
| velocity_error_mps | 744 | 0.074 | 0.038 | 0.206 | 0.168 | 0.425 | 0.650 | 3.141 |
| width_error_m | 12 | 0.185 | 0.104 | 0.263 | 0.159 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 514 | 0.111 | 0.077 | 0.169 | 0.092 | 0.261 | 0.347 | 0.658 |
| heading_error_deg | 514 | 0.231 | 0.099 | 0.436 | 0.337 | 1.078 | 1.803 | 4.065 |
| speed_error_mps | 514 | 0.019 | 0.009 | 0.041 | 0.031 | 0.068 | 0.090 | 0.234 |
| velocity_error_mps | 514 | 0.056 | 0.027 | 0.099 | 0.072 | 0.232 | 0.340 | 0.844 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 230 | 0.504 | 0.392 | 0.702 | 0.310 | 0.807 | 0.905 | 2.164 |
| heading_error_deg | 230 | 1.107 | 0.539 | 2.421 | 1.882 | 4.509 | 5.899 | 14.504 |
| speed_error_mps | 230 | 0.051 | 0.022 | 0.089 | 0.068 | 0.174 | 0.232 | 0.334 |
| velocity_error_mps | 230 | 0.220 | 0.118 | 0.445 | 0.327 | 1.004 | 1.241 | 3.141 |

Calibration of pos_std_m over 744 states: within 1/2/3 sigma 0.183/0.550/0.684 (Gaussian: 0.393/0.865/0.989).
