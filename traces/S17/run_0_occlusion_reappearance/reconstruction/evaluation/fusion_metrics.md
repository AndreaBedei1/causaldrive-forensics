# Road-user fusion against ground truth - S17/run_0_occlusion_reappearance

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| A:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_003 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_005 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_006 | B | ASSOCIATED | collision | B | 0.676 | correct link |
| A:track_007 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_008 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_009 | U8 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_001 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| B:track_004 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_005 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_006 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_007 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_008 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |

Counts: anonymous: 15, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | V | no | 1.000 |
| U2 | A:track_002, B:track_002, A:track_008, B:track_007 | D | no | 1.000 |
| U3 | A:track_003, B:track_004 | E | no | 1.000 |
| U4 | A:track_004 | F | no | 1.000 |
| U5 | B:track_001, A:track_005, A:track_007 | C | no | 1.000 |
| U6 | B:track_006 | G | no | 1.000 |
| U7 | B:track_008 | G | no | 1.000 |
| U8 | A:track_009 | E | no | 1.000 |

Merges over pairs of anonymous tracks: correct 11, false 0, missed 3.
Fragmentation (true road user -> entities): C -> U5, D -> U2, E -> U3/U8, F -> U4, G -> U6/U7, V -> U1

## Fused state errors (against the majority identity, 546 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 546 | 0.419 | 0.174 | 0.650 | 0.476 | 0.887 | 1.129 | 2.531 |
| coverage_s | 8 | 5.200 | 3.438 | 11.950 | 8.512 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 520 | 0.676 | 0.320 | 1.478 | 1.157 | 2.694 | 4.696 | 16.956 |
| length_error_m | 8 | 0.192 | 0.166 | 0.419 | 0.254 | 0.585 | 0.778 | 0.971 |
| normalised_centre_error | 546 | 0.801 | 0.332 | 1.376 | 1.044 | 1.851 | 2.011 | 4.473 |
| single_track_nominal_centre_error_m | 544 | 0.538 | 0.364 | 0.818 | 0.454 | 1.265 | 2.039 | 2.651 |
| speed_error_mps | 546 | 0.047 | 0.019 | 0.114 | 0.095 | 0.321 | 0.456 | 1.472 |
| velocity_error_mps | 546 | 0.157 | 0.074 | 0.352 | 0.278 | 0.581 | 1.013 | 3.255 |
| width_error_m | 8 | 0.107 | 0.094 | 0.263 | 0.169 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 307 | 0.268 | 0.115 | 0.591 | 0.476 | 0.698 | 0.809 | 1.829 |
| heading_error_deg | 307 | 0.580 | 0.260 | 1.284 | 1.024 | 2.440 | 2.736 | 15.886 |
| speed_error_mps | 307 | 0.046 | 0.015 | 0.101 | 0.086 | 0.224 | 0.303 | 1.452 |
| velocity_error_mps | 307 | 0.134 | 0.062 | 0.269 | 0.207 | 0.502 | 0.686 | 2.075 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 239 | 0.568 | 0.337 | 0.757 | 0.420 | 1.132 | 1.524 | 2.531 |
| heading_error_deg | 213 | 0.892 | 0.463 | 1.766 | 1.303 | 4.330 | 6.963 | 16.956 |
| speed_error_mps | 239 | 0.049 | 0.026 | 0.150 | 0.124 | 0.413 | 0.511 | 1.472 |
| velocity_error_mps | 239 | 0.179 | 0.095 | 0.411 | 0.316 | 0.864 | 1.447 | 3.255 |

Calibration of pos_std_m over 546 states: within 1/2/3 sigma 0.575/0.947/0.993 (Gaussian: 0.393/0.865/0.989).
