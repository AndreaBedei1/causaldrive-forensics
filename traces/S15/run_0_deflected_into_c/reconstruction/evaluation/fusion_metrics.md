# Road-user fusion against ground truth - S15/run_0_deflected_into_c

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | collision | C | 1.000 | correct link |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | U1 | ANONYMOUS | - | A | 0.760 | missed link (true identity A) |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_002 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |

Counts: correct link: 5, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_001 | A | yes | 0.760 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): A -> U1

## Fused state errors (against the majority identity, 94 pure states; 29 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 94 | 1.468 | 1.405 | 1.506 | 0.101 | 1.526 | 1.558 | 6.588 |
| coverage_s | 1 | 12.250 | 12.250 | 12.250 | 0.000 | 12.250 | 12.250 | 12.250 |
| heading_error_deg | 4 | 164.708 | 161.978 | 168.921 | 6.944 | 173.630 | 175.199 | 176.769 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 94 | 1.128 | 1.100 | 1.154 | 0.055 | 2.681 | 2.796 | 16.108 |
| single_track_nominal_centre_error_m | 94 | 1.409 | 1.342 | 1.435 | 0.093 | 1.475 | 2.490 | 5.283 |
| speed_error_mps | 94 | 0.052 | 0.008 | 0.174 | 0.166 | 0.699 | 2.558 | 3.828 |
| velocity_error_mps | 94 | 0.072 | 0.025 | 0.194 | 0.170 | 1.495 | 3.747 | 10.357 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 17 | 1.069 | 0.899 | 1.129 | 0.231 | 1.144 | 2.237 | 6.588 |
| heading_error_deg | 1 | 158.576 | 158.576 | 158.576 | 0.000 | 158.576 | 158.576 | 158.576 |
| speed_error_mps | 17 | 0.433 | 0.247 | 1.680 | 1.433 | 2.893 | 2.995 | 3.026 |
| velocity_error_mps | 17 | 0.458 | 0.268 | 2.446 | 2.178 | 3.139 | 4.650 | 10.357 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 77 | 1.481 | 1.454 | 1.510 | 0.056 | 1.528 | 1.556 | 4.036 |
| heading_error_deg | 3 | 166.305 | 164.708 | 171.537 | 6.829 | 174.676 | 175.722 | 176.769 |
| speed_error_mps | 77 | 0.030 | 0.007 | 0.092 | 0.085 | 0.165 | 0.231 | 3.828 |
| velocity_error_mps | 77 | 0.050 | 0.020 | 0.113 | 0.093 | 0.185 | 1.123 | 8.736 |

Calibration of pos_std_m over 94 states: within 1/2/3 sigma 0.021/0.830/0.957 (Gaussian: 0.393/0.865/0.989).
