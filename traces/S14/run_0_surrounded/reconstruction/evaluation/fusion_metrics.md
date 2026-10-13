# Road-user fusion against ground truth - S14/run_0_surrounded

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| A:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_003 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_004 | U9 | ANONYMOUS | - | K | 1.000 | anonymous (non-recording road user K) |
| A:track_005 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_006 | U13 | ANONYMOUS | - | L | 1.000 | anonymous (non-recording road user L) |
| A:track_007 | U14 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_008 | U10 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_009 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_011 | U15 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_001 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_002 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| B:track_003 | U1 | ANONYMOUS | - | P | 1.000 | anonymous (non-recording road user P) |
| B:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_005 | U5 | ANONYMOUS | - | K | 1.000 | anonymous (non-recording road user K) |
| B:track_006 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_007 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_008 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_009 | U8 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_010 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_011 | U10 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_012 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_013 | U12 | ANONYMOUS | - | J | 0.816 | anonymous (non-recording road user J) |
| B:track_014 | U5 | ANONYMOUS | - | K | 1.000 | anonymous (non-recording road user K) |
| B:track_015 | U16 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_016 | U17 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |

Counts: anonymous: 25, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | P | no | 1.000 |
| U2 | A:track_002, B:track_008 | C | no | 1.000 |
| U3 | B:track_001, A:track_005 | D | no | 1.000 |
| U4 | B:track_004 | F | no | 1.000 |
| U5 | B:track_005, B:track_014 | K | no | 1.000 |
| U6 | B:track_006, B:track_010 | G | no | 1.000 |
| U7 | B:track_007, A:track_009 | E | no | 1.000 |
| U8 | B:track_009 | H | no | 1.000 |
| U9 | A:track_004 | K | no | 1.000 |
| U10 | B:track_011, A:track_008 | G | no | 1.000 |
| U11 | B:track_012, A:track_010 | F | no | 1.000 |
| U12 | B:track_013 | J | no | 0.816 |
| U13 | A:track_006 | L | no | 1.000 |
| U14 | A:track_007 | J | no | 1.000 |
| U15 | A:track_011 | J | no | 1.000 |
| U16 | B:track_015 | H | no | 1.000 |
| U17 | B:track_016 | G | no | 1.000 |

Merges over pairs of anonymous tracks: correct 8, false 0, missed 16.
Fragmentation (true road user -> entities): C -> U2, D -> U3, E -> U7, F -> U11/U4, G -> U10/U17/U6, H -> U16/U8, J -> U12/U14/U15, K -> U5/U9, L -> U13, P -> U1

## Fused state errors (against the majority identity, 870 pure states; 13 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 870 | 0.251 | 0.118 | 0.641 | 0.523 | 1.541 | 2.358 | 3.163 |
| coverage_s | 17 | 3.800 | 1.650 | 8.050 | 6.400 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 870 | 0.503 | 0.210 | 1.249 | 1.039 | 2.468 | 3.255 | 14.496 |
| length_error_m | 17 | 0.192 | 0.086 | 0.419 | 0.333 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 870 | 0.516 | 0.297 | 1.116 | 0.818 | 1.752 | 1.912 | 5.773 |
| single_track_nominal_centre_error_m | 847 | 0.353 | 0.231 | 0.757 | 0.526 | 1.504 | 1.716 | 3.235 |
| speed_error_mps | 870 | 0.036 | 0.013 | 0.084 | 0.071 | 0.167 | 0.235 | 0.572 |
| velocity_error_mps | 870 | 0.119 | 0.059 | 0.301 | 0.242 | 0.559 | 0.739 | 3.119 |
| width_error_m | 17 | 0.107 | 0.094 | 0.263 | 0.169 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 435 | 0.123 | 0.087 | 0.193 | 0.105 | 0.264 | 0.412 | 1.757 |
| heading_error_deg | 435 | 0.361 | 0.175 | 0.858 | 0.683 | 1.422 | 2.058 | 4.485 |
| speed_error_mps | 435 | 0.032 | 0.012 | 0.071 | 0.059 | 0.126 | 0.162 | 0.313 |
| velocity_error_mps | 435 | 0.098 | 0.053 | 0.230 | 0.177 | 0.349 | 0.492 | 0.945 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 435 | 0.618 | 0.324 | 1.074 | 0.750 | 2.358 | 2.434 | 3.163 |
| heading_error_deg | 435 | 0.653 | 0.273 | 1.843 | 1.570 | 3.132 | 4.696 | 14.496 |
| speed_error_mps | 435 | 0.042 | 0.015 | 0.093 | 0.078 | 0.210 | 0.266 | 0.572 |
| velocity_error_mps | 435 | 0.149 | 0.071 | 0.454 | 0.382 | 0.713 | 1.008 | 3.119 |

Calibration of pos_std_m over 870 states: within 1/2/3 sigma 0.707/0.966/0.990 (Gaussian: 0.393/0.865/0.989).
