# Road-user fusion against ground truth - S18/run_0_platoon

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004 | U4 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U3 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_004 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_005 | U4 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 7, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_002, B:track_004 | D | no | 1.000 |
| U2 | A:track_003 | D | no | 1.000 |
| U3 | B:track_003 | C | no | 1.000 |
| U4 | A:track_004, B:track_005 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 5.
Fragmentation (true road user -> entities): C -> U3/U4, D -> U1/U2

## Fused state errors (against the majority identity, 204 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 204 | 0.623 | 0.305 | 1.057 | 0.752 | 1.248 | 3.482 | 3.542 |
| coverage_s | 4 | 4.150 | 3.125 | 6.075 | 2.950 | 8.730 | 9.615 | 10.500 |
| heading_error_deg | 204 | 0.635 | 0.324 | 1.190 | 0.866 | 2.156 | 3.110 | 5.936 |
| length_error_m | 4 | 0.139 | 0.086 | 0.192 | 0.106 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 204 | 1.172 | 0.792 | 1.971 | 1.179 | 2.288 | 6.353 | 6.464 |
| single_track_nominal_centre_error_m | 204 | 0.679 | 0.373 | 0.934 | 0.561 | 1.172 | 3.479 | 3.563 |
| speed_error_mps | 204 | 0.048 | 0.015 | 0.075 | 0.060 | 0.143 | 0.173 | 0.535 |
| velocity_error_mps | 204 | 0.154 | 0.089 | 0.282 | 0.193 | 0.502 | 0.803 | 1.524 |
| width_error_m | 4 | 0.185 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 97 | 0.304 | 0.245 | 0.358 | 0.113 | 0.504 | 0.712 | 0.985 |
| heading_error_deg | 97 | 0.499 | 0.259 | 0.729 | 0.471 | 1.191 | 1.305 | 1.481 |
| speed_error_mps | 97 | 0.041 | 0.015 | 0.057 | 0.043 | 0.070 | 0.101 | 0.164 |
| velocity_error_mps | 97 | 0.109 | 0.070 | 0.158 | 0.088 | 0.257 | 0.288 | 0.332 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 107 | 1.051 | 0.809 | 1.210 | 0.402 | 3.479 | 3.499 | 3.542 |
| heading_error_deg | 107 | 0.925 | 0.451 | 1.982 | 1.531 | 3.066 | 4.003 | 5.936 |
| speed_error_mps | 107 | 0.058 | 0.020 | 0.104 | 0.084 | 0.170 | 0.199 | 0.535 |
| velocity_error_mps | 107 | 0.235 | 0.145 | 0.445 | 0.300 | 0.792 | 1.016 | 1.524 |

Calibration of pos_std_m over 204 states: within 1/2/3 sigma 0.422/0.770/0.912 (Gaussian: 0.393/0.865/0.989).
