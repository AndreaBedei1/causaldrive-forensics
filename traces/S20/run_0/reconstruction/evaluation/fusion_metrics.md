# Road-user fusion against ground truth - S20/run_0

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_002 | U2 | ANONYMOUS | - | D | 0.983 | anonymous (non-recording road user D) |
| A:track_003 | U3 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_004 | U4 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_005 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_006 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_007 | U7 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_008 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_009 | U10 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_002 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_003 | U7 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_004 | U3 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_005 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_006 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_007 | U4 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_008 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_009 | U8 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |

Counts: anonymous: 18, correct link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_005 | F | no | 1.000 |
| U2 | A:track_002 | D | no | 0.983 |
| U3 | A:track_003, B:track_004 | I | no | 1.000 |
| U4 | A:track_004, B:track_007 | H | no | 1.000 |
| U5 | A:track_005, B:track_002, B:track_008 | E | no | 1.000 |
| U6 | A:track_006, B:track_001 | G | no | 1.000 |
| U7 | A:track_007, B:track_003 | J | no | 1.000 |
| U8 | B:track_009 | H | no | 1.000 |
| U9 | A:track_008 | C | no | 1.000 |
| U10 | A:track_009 | E | no | 1.000 |
| U11 | A:track_010 | F | no | 1.000 |

Merges over pairs of anonymous tracks: correct 8, false 0, missed 7.
Fragmentation (true road user -> entities): C -> U9, D -> U2, E -> U10/U5, F -> U1/U11, G -> U6, H -> U4/U8, I -> U3, J -> U7

## Fused state errors (against the majority identity, 838 pure states; 3 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 838 | 0.192 | 0.091 | 0.369 | 0.278 | 0.680 | 1.129 | 2.091 |
| coverage_s | 11 | 9.550 | 1.950 | 11.925 | 9.975 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 838 | 0.312 | 0.121 | 1.087 | 0.965 | 3.154 | 5.244 | 11.287 |
| length_error_m | 11 | 0.192 | 0.105 | 0.192 | 0.087 | 0.194 | 0.306 | 0.419 |
| normalised_centre_error | 838 | 0.412 | 0.238 | 0.725 | 0.486 | 1.216 | 1.908 | 3.394 |
| single_track_nominal_centre_error_m | 828 | 0.360 | 0.213 | 0.539 | 0.325 | 0.832 | 1.131 | 2.222 |
| speed_error_mps | 838 | 0.036 | 0.017 | 0.071 | 0.054 | 0.223 | 0.359 | 4.539 |
| velocity_error_mps | 838 | 0.089 | 0.040 | 0.268 | 0.228 | 0.769 | 1.306 | 4.551 |
| width_error_m | 11 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 472 | 0.116 | 0.049 | 0.206 | 0.157 | 0.296 | 0.394 | 0.893 |
| heading_error_deg | 472 | 0.239 | 0.100 | 0.524 | 0.423 | 1.441 | 2.651 | 10.549 |
| speed_error_mps | 472 | 0.035 | 0.017 | 0.058 | 0.041 | 0.129 | 0.328 | 4.539 |
| velocity_error_mps | 472 | 0.066 | 0.034 | 0.132 | 0.097 | 0.331 | 0.771 | 4.551 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 366 | 0.364 | 0.205 | 0.639 | 0.434 | 1.221 | 1.568 | 2.091 |
| heading_error_deg | 366 | 0.738 | 0.164 | 2.331 | 2.167 | 4.167 | 6.569 | 11.287 |
| speed_error_mps | 366 | 0.041 | 0.018 | 0.104 | 0.086 | 0.278 | 0.367 | 0.424 |
| velocity_error_mps | 366 | 0.174 | 0.059 | 0.559 | 0.499 | 0.942 | 1.476 | 2.414 |

Calibration of pos_std_m over 838 states: within 1/2/3 sigma 0.844/0.955/0.988 (Gaussian: 0.393/0.865/0.989).
