# Road-user fusion against ground truth - S15/run_0_deflected_into_c

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | collision | C | 1.000 | correct link |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001#segment_1 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_001#segment_2 | U1 | ANONYMOUS | - | A | 1.000 | missed link (true identity A) |
| B:track_001#segment_3 | U2 | ANONYMOUS | - | A | 1.000 | missed link (true identity A) |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_002 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |

Counts: correct link: 6, missed link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_001#segment_2 | A | yes | 1.000 |
| U2 | B:track_001#segment_3 | A | yes | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 1.
Fragmentation (true road user -> entities): A -> U1/U2

## Fused state errors (against the majority identity, 93 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 93 | 0.983 | 0.972 | 0.991 | 0.018 | 1.000 | 1.043 | 3.777 |
| coverage_s | 2 | 4.625 | 2.962 | 6.287 | 3.325 | 7.285 | 7.617 | 7.950 |
| heading_error_deg | 3 | 160.035 | 153.673 | 162.502 | 8.829 | 163.982 | 164.475 | 164.969 |
| length_error_m | 2 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 93 | 0.428 | 0.425 | 0.432 | 0.008 | 0.778 | 1.828 | 6.893 |
| single_track_nominal_centre_error_m | 93 | 1.921 | 1.918 | 1.926 | 0.008 | 1.933 | 2.294 | 3.648 |
| speed_error_mps | 93 | 0.004 | 0.002 | 0.005 | 0.004 | 0.655 | 1.174 | 2.237 |
| velocity_error_mps | 93 | 0.007 | 0.004 | 0.014 | 0.009 | 0.700 | 2.333 | 7.825 |
| width_error_m | 2 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 8 | 0.518 | 0.467 | 1.083 | 0.616 | 1.136 | 1.163 | 1.189 |
| speed_error_mps | 8 | 0.966 | 0.426 | 1.762 | 1.336 | 2.056 | 2.126 | 2.196 |
| velocity_error_mps | 8 | 0.990 | 0.445 | 1.798 | 1.353 | 2.103 | 2.177 | 2.250 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 85 | 0.984 | 0.973 | 0.990 | 0.017 | 0.998 | 1.015 | 3.777 |
| heading_error_deg | 3 | 160.035 | 153.673 | 162.502 | 8.829 | 163.982 | 164.475 | 164.969 |
| speed_error_mps | 85 | 0.004 | 0.002 | 0.004 | 0.003 | 0.008 | 0.565 | 2.237 |
| velocity_error_mps | 85 | 0.006 | 0.004 | 0.012 | 0.007 | 0.022 | 1.972 | 7.825 |

Calibration of pos_std_m over 93 states: within 1/2/3 sigma 0.903/0.946/0.978 (Gaussian: 0.393/0.865/0.989).
