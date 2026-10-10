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
| centre_error_m | 204 | 0.616 | 0.321 | 1.051 | 0.730 | 1.233 | 3.482 | 3.542 |
| coverage_s | 4 | 4.150 | 3.125 | 6.075 | 2.950 | 8.730 | 9.615 | 10.500 |
| heading_error_deg | 204 | 0.728 | 0.350 | 1.193 | 0.843 | 2.156 | 3.110 | 5.936 |
| length_error_m | 4 | 0.139 | 0.086 | 0.192 | 0.106 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 204 | 1.199 | 0.789 | 1.946 | 1.157 | 2.264 | 6.353 | 6.464 |
| single_track_nominal_centre_error_m | 370 | 0.522 | 0.294 | 1.059 | 0.765 | 3.502 | 3.537 | 3.563 |
| speed_error_mps | 204 | 0.040 | 0.014 | 0.087 | 0.073 | 0.152 | 0.178 | 0.535 |
| velocity_error_mps | 204 | 0.172 | 0.100 | 0.295 | 0.196 | 0.502 | 0.803 | 1.524 |
| width_error_m | 4 | 0.185 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 91 | 0.317 | 0.245 | 0.380 | 0.135 | 0.539 | 0.685 | 0.985 |
| heading_error_deg | 91 | 0.511 | 0.284 | 0.855 | 0.571 | 1.189 | 1.296 | 1.670 |
| speed_error_mps | 91 | 0.026 | 0.013 | 0.056 | 0.043 | 0.097 | 0.152 | 0.179 |
| velocity_error_mps | 91 | 0.111 | 0.070 | 0.183 | 0.113 | 0.279 | 0.299 | 0.346 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 113 | 0.986 | 0.685 | 1.176 | 0.491 | 3.476 | 3.498 | 3.542 |
| heading_error_deg | 113 | 0.948 | 0.465 | 1.837 | 1.372 | 2.974 | 3.885 | 5.936 |
| speed_error_mps | 113 | 0.058 | 0.022 | 0.106 | 0.084 | 0.166 | 0.198 | 0.535 |
| velocity_error_mps | 113 | 0.235 | 0.149 | 0.440 | 0.291 | 0.763 | 0.993 | 1.524 |

Calibration of pos_std_m over 204 states: within 1/2/3 sigma 0.402/0.784/0.926 (Gaussian: 0.393/0.865/0.989).
