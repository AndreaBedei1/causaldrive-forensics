# Road-user fusion against ground truth - S07/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | U1 | ANONYMOUS | - | C | 1.000 | missed link (true identity C) |

Counts: correct link: 1, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_001 | C | yes | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U1

## Fused state errors (against the majority identity, 137 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 137 | 0.278 | 0.246 | 0.351 | 0.105 | 0.526 | 0.694 | 1.484 |
| coverage_s | 1 | 13.650 | 13.650 | 13.650 | 0.000 | 13.650 | 13.650 | 13.650 |
| heading_error_deg | 43 | 0.127 | 0.072 | 0.272 | 0.200 | 0.387 | 0.528 | 0.747 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 137 | 0.507 | 0.448 | 0.639 | 0.192 | 0.905 | 1.380 | 2.756 |
| single_track_nominal_centre_error_m | 137 | 0.214 | 0.170 | 0.282 | 0.112 | 0.314 | 0.343 | 0.380 |
| speed_error_mps | 137 | 0.044 | 0.026 | 0.061 | 0.035 | 0.100 | 0.125 | 0.406 |
| velocity_error_mps | 137 | 0.053 | 0.032 | 0.070 | 0.038 | 0.110 | 0.128 | 0.410 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 3 | 0.647 | 0.601 | 0.887 | 0.286 | 1.031 | 1.079 | 1.127 |
| heading_error_deg | 1 | 0.114 | 0.114 | 0.114 | 0.000 | 0.114 | 0.114 | 0.114 |
| speed_error_mps | 3 | 0.032 | 0.029 | 0.036 | 0.006 | 0.038 | 0.039 | 0.039 |
| velocity_error_mps | 3 | 0.033 | 0.033 | 0.036 | 0.004 | 0.038 | 0.039 | 0.039 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 134 | 0.278 | 0.245 | 0.345 | 0.100 | 0.467 | 0.597 | 1.484 |
| heading_error_deg | 42 | 0.130 | 0.072 | 0.273 | 0.202 | 0.390 | 0.528 | 0.747 |
| speed_error_mps | 134 | 0.044 | 0.026 | 0.061 | 0.035 | 0.101 | 0.126 | 0.406 |
| velocity_error_mps | 134 | 0.055 | 0.030 | 0.070 | 0.040 | 0.110 | 0.128 | 0.410 |

Calibration of pos_std_m over 137 states: within 1/2/3 sigma 0.920/0.993/1.000 (Gaussian: 0.393/0.865/0.989).

## Observed-trajectory alignment

| Recorder | Accepted | Estimated offset | True offset | Error | Interval |
|----------|----------|-----------------:|------------:|------:|----------|
| C | False | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
