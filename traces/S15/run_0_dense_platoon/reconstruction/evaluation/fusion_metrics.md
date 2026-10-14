# Road-user fusion against ground truth - S15/run_0_dense_platoon

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_003 | U3 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_004 | U4 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_005 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_006 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_007 | U7 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_008 | U8 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_009 | U10 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001#segment_1 | U6 | ANONYMOUS | - | G | 0.880 | anonymous (non-recording road user G) |
| B:track_001#segment_2 | U9 | ANONYMOUS | - | - | 1.000 | anonymous (clutter: no true vehicle) |
| B:track_001#segment_3 | U12 | ANONYMOUS | - | - | 1.000 | anonymous (clutter: no true vehicle) |
| B:track_002 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_003 | U7 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_004 | U3 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_005 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_006 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_007 | U4 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_008 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

Counts: anonymous: 19, correct link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_005 | F | no | 1.000 |
| U2 | A:track_002 | D | no | 1.000 |
| U3 | A:track_003, B:track_004 | I | no | 1.000 |
| U4 | A:track_004, B:track_007 | H | no | 1.000 |
| U5 | A:track_005, B:track_002, B:track_008 | E | no | 1.000 |
| U6 | A:track_006, B:track_001#segment_1 | G | no | 0.951 |
| U7 | A:track_007, B:track_003 | J | no | 1.000 |
| U8 | A:track_008 | C | no | 1.000 |
| U9 | B:track_001#segment_2 | - | no | 1.000 |
| U10 | A:track_009 | E | no | 1.000 |
| U11 | A:track_010 | F | no | 1.000 |
| U12 | B:track_001#segment_3 | - | no | 1.000 |

Merges over pairs of anonymous tracks: correct 8, false 0, missed 5.
Fragmentation (true road user -> entities): C -> U8, D -> U2, E -> U10/U5, F -> U1/U11, G -> U6, H -> U4, I -> U3, J -> U7

## Fused state errors (against the majority identity, 812 pure states; 10 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 812 | 0.190 | 0.080 | 0.341 | 0.261 | 0.595 | 0.836 | 1.893 |
| coverage_s | 10 | 10.700 | 4.000 | 11.938 | 7.938 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 812 | 0.307 | 0.110 | 1.109 | 0.999 | 2.674 | 4.057 | 22.409 |
| length_error_m | 10 | 0.192 | 0.096 | 0.192 | 0.096 | 0.216 | 0.318 | 0.419 |
| normalised_centre_error | 812 | 0.399 | 0.219 | 0.699 | 0.480 | 1.089 | 1.413 | 4.841 |
| single_track_nominal_centre_error_m | 802 | 0.337 | 0.224 | 0.517 | 0.293 | 0.757 | 0.912 | 1.866 |
| speed_error_mps | 812 | 0.036 | 0.016 | 0.071 | 0.055 | 0.159 | 0.227 | 4.428 |
| velocity_error_mps | 812 | 0.087 | 0.041 | 0.260 | 0.219 | 0.655 | 0.973 | 4.858 |
| width_error_m | 10 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 481 | 0.109 | 0.045 | 0.217 | 0.172 | 0.312 | 0.385 | 1.893 |
| heading_error_deg | 481 | 0.220 | 0.096 | 0.679 | 0.583 | 1.440 | 2.755 | 22.409 |
| speed_error_mps | 481 | 0.035 | 0.017 | 0.065 | 0.048 | 0.138 | 0.298 | 4.428 |
| velocity_error_mps | 481 | 0.068 | 0.036 | 0.160 | 0.124 | 0.342 | 0.676 | 4.858 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 331 | 0.348 | 0.199 | 0.579 | 0.380 | 0.881 | 1.082 | 1.772 |
| heading_error_deg | 331 | 0.604 | 0.144 | 2.117 | 1.973 | 3.510 | 4.824 | 21.236 |
| speed_error_mps | 331 | 0.037 | 0.013 | 0.090 | 0.077 | 0.195 | 0.222 | 0.339 |
| velocity_error_mps | 331 | 0.145 | 0.051 | 0.521 | 0.470 | 0.820 | 1.077 | 4.476 |

Calibration of pos_std_m over 812 states: within 1/2/3 sigma 0.868/0.988/0.999 (Gaussian: 0.393/0.865/0.989).
