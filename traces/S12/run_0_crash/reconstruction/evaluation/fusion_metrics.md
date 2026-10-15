# Road-user fusion against ground truth - S12/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
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
| centre_error_m | 75 | 0.046 | 0.035 | 0.056 | 0.021 | 0.096 | 0.197 | 0.317 |
| coverage_s | 1 | 7.450 | 7.450 | 7.450 | 0.000 | 7.450 | 7.450 | 7.450 |
| heading_error_deg | 75 | 0.388 | 0.158 | 0.673 | 0.515 | 1.403 | 1.676 | 2.715 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 75 | 0.482 | 0.383 | 0.700 | 0.317 | 0.956 | 1.689 | 1.957 |
| single_track_nominal_centre_error_m | 74 | 1.003 | 0.836 | 1.210 | 0.374 | 1.300 | 1.340 | 1.660 |
| speed_error_mps | 75 | 0.018 | 0.010 | 0.034 | 0.023 | 0.050 | 0.092 | 0.630 |
| velocity_error_mps | 75 | 0.046 | 0.029 | 0.098 | 0.069 | 0.220 | 0.350 | 0.816 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 69 | 0.044 | 0.035 | 0.054 | 0.019 | 0.069 | 0.082 | 0.152 |
| heading_error_deg | 69 | 0.275 | 0.146 | 0.583 | 0.437 | 0.985 | 1.230 | 1.493 |
| speed_error_mps | 69 | 0.016 | 0.009 | 0.030 | 0.022 | 0.041 | 0.043 | 0.091 |
| velocity_error_mps | 69 | 0.045 | 0.026 | 0.072 | 0.046 | 0.119 | 0.145 | 0.296 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 6 | 0.237 | 0.195 | 0.274 | 0.079 | 0.299 | 0.308 | 0.317 |
| heading_error_deg | 6 | 2.044 | 1.664 | 2.452 | 0.788 | 2.619 | 2.667 | 2.715 |
| speed_error_mps | 6 | 0.125 | 0.088 | 0.291 | 0.203 | 0.483 | 0.557 | 0.630 |
| velocity_error_mps | 6 | 0.373 | 0.349 | 0.506 | 0.157 | 0.681 | 0.749 | 0.816 |

Calibration of pos_std_m over 75 states: within 1/2/3 sigma 0.893/1.000/1.000 (Gaussian: 0.393/0.865/0.989).
