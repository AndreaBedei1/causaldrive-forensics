# Road-user fusion against ground truth - S18/run_0_passing

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 0.649 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_004 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_005 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |

Counts: anonymous: 7, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001 | C | no | 0.649 |
| U2 | B:track_002, B:track_004, A:track_003 | C | no | 1.000 |
| U3 | B:track_003, A:track_004, B:track_005 | D | no | 1.000 |

Merges over pairs of anonymous tracks: correct 6, false 0, missed 3.
Fragmentation (true road user -> entities): C -> U1/U2, D -> U3

## Fused state errors (against the majority identity, 257 pure states; 34 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 257 | 0.411 | 0.237 | 0.615 | 0.378 | 0.846 | 0.970 | 2.077 |
| coverage_s | 3 | 9.700 | 9.325 | 9.950 | 0.625 | 10.100 | 10.150 | 10.200 |
| heading_error_deg | 257 | 0.415 | 0.214 | 0.865 | 0.651 | 1.295 | 1.744 | 14.540 |
| length_error_m | 3 | 0.192 | 0.139 | 0.192 | 0.053 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 257 | 0.827 | 0.533 | 1.133 | 0.600 | 1.515 | 1.738 | 3.888 |
| single_track_nominal_centre_error_m | 377 | 0.525 | 0.322 | 0.697 | 0.375 | 3.460 | 3.564 | 3.673 |
| speed_error_mps | 257 | 0.048 | 0.027 | 0.085 | 0.058 | 0.146 | 0.174 | 1.089 |
| velocity_error_mps | 257 | 0.114 | 0.073 | 0.218 | 0.146 | 0.320 | 0.406 | 3.185 |
| width_error_m | 3 | 0.263 | 0.185 | 0.263 | 0.078 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 94 | 0.269 | 0.188 | 0.392 | 0.204 | 0.548 | 0.724 | 1.735 |
| heading_error_deg | 94 | 0.396 | 0.201 | 0.686 | 0.485 | 1.541 | 4.726 | 14.540 |
| speed_error_mps | 94 | 0.042 | 0.027 | 0.087 | 0.060 | 0.140 | 0.172 | 1.089 |
| velocity_error_mps | 94 | 0.105 | 0.063 | 0.184 | 0.121 | 0.344 | 0.982 | 3.185 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 163 | 0.498 | 0.330 | 0.709 | 0.378 | 0.940 | 0.993 | 2.077 |
| heading_error_deg | 163 | 0.436 | 0.222 | 0.885 | 0.663 | 1.151 | 1.557 | 9.600 |
| speed_error_mps | 163 | 0.054 | 0.027 | 0.084 | 0.057 | 0.147 | 0.172 | 0.324 |
| velocity_error_mps | 163 | 0.132 | 0.079 | 0.221 | 0.142 | 0.317 | 0.400 | 2.002 |

Calibration of pos_std_m over 257 states: within 1/2/3 sigma 0.634/0.981/0.996 (Gaussian: 0.393/0.865/0.989).
