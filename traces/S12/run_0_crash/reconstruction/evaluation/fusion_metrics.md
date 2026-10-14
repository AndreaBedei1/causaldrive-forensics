# Road-user fusion against ground truth - S12/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 0.582 | correct link |
| B:track_001 | A | ASSOCIATED | collision | A | 0.555 | correct link |
| B:track_002 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 3, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_002, B:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 3, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U1

## Fused state errors (against the majority identity, 75 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 75 | 0.103 | 0.068 | 0.137 | 0.069 | 0.213 | 0.344 | 0.987 |
| coverage_s | 1 | 7.450 | 7.450 | 7.450 | 0.000 | 7.450 | 7.450 | 7.450 |
| heading_error_deg | 75 | 0.972 | 0.619 | 1.375 | 0.756 | 1.835 | 1.920 | 2.245 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 75 | 0.262 | 0.173 | 0.351 | 0.178 | 0.459 | 0.779 | 1.802 |
| single_track_nominal_centre_error_m | 74 | 1.016 | 0.683 | 1.225 | 0.542 | 1.340 | 1.371 | 1.631 |
| speed_error_mps | 75 | 0.065 | 0.029 | 0.102 | 0.073 | 0.127 | 0.132 | 0.261 |
| velocity_error_mps | 75 | 0.186 | 0.090 | 0.264 | 0.174 | 0.360 | 0.372 | 0.577 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 70 | 0.092 | 0.065 | 0.128 | 0.063 | 0.164 | 0.267 | 0.381 |
| heading_error_deg | 70 | 0.947 | 0.596 | 1.266 | 0.670 | 1.794 | 1.911 | 1.946 |
| speed_error_mps | 70 | 0.064 | 0.029 | 0.102 | 0.073 | 0.122 | 0.129 | 0.144 |
| velocity_error_mps | 70 | 0.180 | 0.079 | 0.238 | 0.159 | 0.339 | 0.361 | 0.374 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 5 | 0.227 | 0.167 | 0.369 | 0.202 | 0.740 | 0.864 | 0.987 |
| heading_error_deg | 5 | 1.750 | 1.347 | 2.042 | 0.696 | 2.164 | 2.204 | 2.245 |
| speed_error_mps | 5 | 0.065 | 0.050 | 0.131 | 0.082 | 0.209 | 0.235 | 0.261 |
| velocity_error_mps | 5 | 0.390 | 0.277 | 0.450 | 0.173 | 0.526 | 0.552 | 0.577 |

Calibration of pos_std_m over 75 states: within 1/2/3 sigma 0.987/1.000/1.000 (Gaussian: 0.393/0.865/0.989).
