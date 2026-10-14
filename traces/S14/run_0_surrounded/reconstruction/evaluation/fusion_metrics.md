# Road-user fusion against ground truth - S14/run_0_surrounded

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| A:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_003 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_004#segment_1 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004#segment_2 | U13 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004#segment_3 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_005 | U9 | ANONYMOUS | - | K | 1.000 | anonymous (non-recording road user K) |
| A:track_006 | U14 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_007 | U15 | ANONYMOUS | - | L | 1.000 | anonymous (non-recording road user L) |
| A:track_008 | U11 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_009 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U10 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_011 | U17 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_001 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_002 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| B:track_003 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| B:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_005 | U5 | ANONYMOUS | - | K | 1.000 | anonymous (non-recording road user K) |
| B:track_006 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_007 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_008 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_009 | U8 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_010 | U10 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_011 | U11 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_012 | U12 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_013 | U16 | ANONYMOUS | - | - | 0.833 | anonymous (clutter: no true vehicle) |
| B:track_014 | U17 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |

Counts: anonymous: 25, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | P | no | 1.000 |
| U2 | A:track_002, B:track_006 | C | no | 1.000 |
| U3 | B:track_001, A:track_004#segment_1, A:track_004#segment_3 | D | no | 1.000 |
| U4 | B:track_004 | F | no | 1.000 |
| U5 | B:track_005 | K | no | 1.000 |
| U6 | B:track_007, A:track_009 | E | no | 1.000 |
| U7 | B:track_008 | G | no | 1.000 |
| U8 | B:track_009 | H | no | 1.000 |
| U9 | A:track_005 | K | no | 1.000 |
| U10 | B:track_010, A:track_010 | F | no | 1.000 |
| U11 | B:track_011, A:track_008 | G | no | 1.000 |
| U12 | B:track_012 | H | no | 1.000 |
| U13 | A:track_004#segment_2 | D | no | 1.000 |
| U14 | A:track_006 | J | no | 1.000 |
| U15 | A:track_007 | L | no | 1.000 |
| U16 | B:track_013 | - | no | 0.833 |
| U17 | B:track_014, A:track_011 | J | no | 1.000 |

Merges over pairs of anonymous tracks: correct 9, false 0, missed 11.
Fragmentation (true road user -> entities): C -> U2, D -> U13/U3, E -> U6, F -> U10/U4, G -> U11/U7, H -> U12/U8, J -> U14/U17, K -> U5/U9, L -> U15, P -> U1

## Fused state errors (against the majority identity, 849 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 849 | 0.213 | 0.105 | 0.549 | 0.444 | 1.008 | 2.307 | 2.582 |
| coverage_s | 16 | 3.725 | 1.900 | 8.000 | 6.100 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 849 | 0.541 | 0.259 | 1.117 | 0.857 | 2.212 | 2.965 | 15.946 |
| length_error_m | 16 | 0.192 | 0.086 | 0.419 | 0.333 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 849 | 0.481 | 0.254 | 0.995 | 0.741 | 1.604 | 1.787 | 4.299 |
| single_track_nominal_centre_error_m | 832 | 0.382 | 0.227 | 0.639 | 0.412 | 1.079 | 1.517 | 2.976 |
| speed_error_mps | 849 | 0.034 | 0.013 | 0.074 | 0.061 | 0.127 | 0.194 | 0.725 |
| velocity_error_mps | 849 | 0.124 | 0.066 | 0.267 | 0.201 | 0.520 | 0.691 | 3.433 |
| width_error_m | 16 | 0.107 | 0.094 | 0.263 | 0.169 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 511 | 0.121 | 0.080 | 0.203 | 0.123 | 0.280 | 0.378 | 1.923 |
| heading_error_deg | 511 | 0.420 | 0.170 | 0.835 | 0.666 | 1.557 | 2.185 | 4.156 |
| speed_error_mps | 511 | 0.034 | 0.014 | 0.068 | 0.054 | 0.104 | 0.155 | 0.725 |
| velocity_error_mps | 511 | 0.099 | 0.055 | 0.218 | 0.163 | 0.393 | 0.534 | 0.968 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 338 | 0.613 | 0.389 | 0.897 | 0.508 | 2.362 | 2.427 | 2.582 |
| heading_error_deg | 338 | 0.752 | 0.443 | 1.799 | 1.356 | 2.950 | 3.751 | 15.946 |
| speed_error_mps | 338 | 0.036 | 0.012 | 0.087 | 0.076 | 0.155 | 0.233 | 0.392 |
| velocity_error_mps | 338 | 0.161 | 0.100 | 0.417 | 0.317 | 0.688 | 0.853 | 3.433 |

Calibration of pos_std_m over 849 states: within 1/2/3 sigma 0.751/0.992/0.996 (Gaussian: 0.393/0.865/0.989).
