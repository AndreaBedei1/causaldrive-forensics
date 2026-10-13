# Road-user fusion against ground truth - S17/run_0_occlusion_reappearance

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| A:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_003 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_005 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| A:track_006 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_007 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_008 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_009 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_010 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_001 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_004 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| B:track_005 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_006 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_007 | U1 | ANONYMOUS | - | V | 0.872 | anonymous (non-recording road user V) |
| B:track_008 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_009 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_010 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |

Counts: anonymous: 18, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_004, A:track_005, B:track_007 | V | no | 0.985 |
| U2 | A:track_002, B:track_002, A:track_008, B:track_009 | D | no | 1.000 |
| U3 | A:track_003, B:track_003, B:track_005 | E | no | 1.000 |
| U4 | A:track_004 | F | no | 1.000 |
| U5 | A:track_006, B:track_001, A:track_009 | C | no | 1.000 |
| U6 | B:track_008, B:track_010 | G | no | 1.000 |
| U7 | A:track_010 | E | no | 1.000 |

Merges over pairs of anonymous tracks: correct 19, false 0, missed 3.
Fragmentation (true road user -> entities): C -> U5, D -> U2, E -> U3/U7, F -> U4, G -> U6, V -> U1

## Fused state errors (against the majority identity, 552 pure states; 5 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 552 | 0.386 | 0.154 | 0.646 | 0.492 | 0.913 | 1.224 | 2.713 |
| coverage_s | 7 | 7.150 | 5.275 | 11.950 | 6.675 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 526 | 0.824 | 0.355 | 1.750 | 1.394 | 3.213 | 5.903 | 20.386 |
| length_error_m | 7 | 0.192 | 0.139 | 0.305 | 0.167 | 0.465 | 0.499 | 0.534 |
| normalised_centre_error | 552 | 0.743 | 0.296 | 1.316 | 1.020 | 2.071 | 2.267 | 4.952 |
| single_track_nominal_centre_error_m | 550 | 0.553 | 0.359 | 1.157 | 0.798 | 1.664 | 2.273 | 2.658 |
| speed_error_mps | 552 | 0.047 | 0.020 | 0.131 | 0.111 | 0.305 | 0.457 | 1.711 |
| velocity_error_mps | 552 | 0.181 | 0.077 | 0.390 | 0.314 | 0.695 | 1.296 | 3.347 |
| width_error_m | 7 | 0.107 | 0.101 | 0.263 | 0.163 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 312 | 0.276 | 0.104 | 0.585 | 0.482 | 0.757 | 0.875 | 1.827 |
| heading_error_deg | 312 | 0.639 | 0.262 | 1.263 | 1.001 | 2.441 | 2.754 | 20.386 |
| speed_error_mps | 312 | 0.047 | 0.019 | 0.120 | 0.101 | 0.226 | 0.293 | 1.711 |
| velocity_error_mps | 312 | 0.146 | 0.068 | 0.291 | 0.223 | 0.482 | 0.559 | 2.867 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 240 | 0.487 | 0.295 | 0.720 | 0.425 | 1.247 | 1.626 | 2.713 |
| heading_error_deg | 214 | 1.111 | 0.508 | 2.475 | 1.967 | 5.600 | 6.516 | 17.526 |
| speed_error_mps | 240 | 0.047 | 0.021 | 0.175 | 0.154 | 0.418 | 0.500 | 1.491 |
| velocity_error_mps | 240 | 0.214 | 0.089 | 0.500 | 0.411 | 1.146 | 1.387 | 3.347 |

Calibration of pos_std_m over 552 states: within 1/2/3 sigma 0.596/0.880/0.982 (Gaussian: 0.393/0.865/0.989).
