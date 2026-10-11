# Road-user fusion against ground truth - S18/run_0_abreast

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_001#segment_2 | U4 | ANONYMOUS | - | D | 0.719 | anonymous (non-recording road user D) |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U3 | ANONYMOUS | - | D | 0.976 | anonymous (non-recording road user D) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 7, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001#segment_1 | D | no | 1.000 |
| U2 | B:track_002, B:track_004, A:track_001#segment_3 | C | no | 1.000 |
| U3 | B:track_003, A:track_003 | D | no | 0.988 |
| U4 | A:track_001#segment_2 | D | no | 0.719 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 5.
Fragmentation (true road user -> entities): C -> U2, D -> U1/U3/U4

## Fused state errors (against the majority identity, 230 pure states; 13 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 230 | 0.402 | 0.247 | 0.729 | 0.482 | 0.928 | 1.506 | 3.631 |
| coverage_s | 4 | 6.650 | 2.388 | 10.262 | 7.875 | 10.375 | 10.412 | 10.450 |
| heading_error_deg | 230 | 0.546 | 0.261 | 1.090 | 0.829 | 1.946 | 3.466 | 13.884 |
| length_error_m | 4 | 0.086 | 0.086 | 0.113 | 0.026 | 0.160 | 0.176 | 0.192 |
| normalised_centre_error | 230 | 0.920 | 0.575 | 1.448 | 0.874 | 1.825 | 2.769 | 6.627 |
| single_track_nominal_centre_error_m | 414 | 0.605 | 0.347 | 0.858 | 0.511 | 3.375 | 3.524 | 3.651 |
| speed_error_mps | 230 | 0.067 | 0.034 | 0.122 | 0.089 | 0.242 | 0.281 | 0.833 |
| velocity_error_mps | 230 | 0.154 | 0.084 | 0.276 | 0.191 | 0.454 | 0.803 | 2.990 |
| width_error_m | 4 | 0.107 | 0.107 | 0.146 | 0.039 | 0.216 | 0.240 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 137 | 0.315 | 0.189 | 0.484 | 0.295 | 0.709 | 0.843 | 1.980 |
| heading_error_deg | 137 | 0.551 | 0.291 | 1.034 | 0.743 | 1.655 | 2.935 | 13.867 |
| speed_error_mps | 137 | 0.055 | 0.033 | 0.121 | 0.088 | 0.244 | 0.272 | 0.674 |
| velocity_error_mps | 137 | 0.143 | 0.084 | 0.267 | 0.182 | 0.423 | 0.737 | 2.829 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 93 | 0.677 | 0.459 | 0.909 | 0.450 | 1.429 | 2.196 | 3.631 |
| heading_error_deg | 93 | 0.465 | 0.219 | 1.161 | 0.942 | 2.310 | 3.707 | 13.884 |
| speed_error_mps | 93 | 0.082 | 0.035 | 0.126 | 0.091 | 0.228 | 0.288 | 0.833 |
| velocity_error_mps | 93 | 0.161 | 0.086 | 0.294 | 0.208 | 0.520 | 0.873 | 2.990 |

Calibration of pos_std_m over 230 states: within 1/2/3 sigma 0.552/0.930/0.957 (Gaussian: 0.393/0.865/0.989).
