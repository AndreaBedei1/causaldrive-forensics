# Road-user fusion against ground truth - S08/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_001 | A | ASSOCIATED | common_frame | A | 0.882 | correct link |
| C:track_002 | U1 | ANONYMOUS | - | B | 0.632 | missed link (true identity B) |

Counts: correct link: 5, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | C:track_002 | B | yes | 0.632 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): B -> U1

## Fused state errors (against the majority identity, 24 pure states; 14 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 24 | 0.337 | 0.263 | 0.481 | 0.218 | 1.042 | 1.761 | 1.937 |
| coverage_s | 1 | 3.700 | 3.700 | 3.700 | 0.000 | 3.700 | 3.700 | 3.700 |
| heading_error_deg | 24 | 1.772 | 0.774 | 3.372 | 2.598 | 4.688 | 5.189 | 9.319 |
| length_error_m | 1 | 0.419 | 0.419 | 0.419 | 0.000 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 24 | 0.766 | 0.562 | 0.886 | 0.324 | 1.358 | 1.803 | 4.736 |
| single_track_nominal_centre_error_m | 24 | 0.897 | 0.708 | 1.138 | 0.429 | 1.229 | 1.317 | 1.345 |
| speed_error_mps | 24 | 0.310 | 0.093 | 0.699 | 0.606 | 2.900 | 3.408 | 4.472 |
| velocity_error_mps | 24 | 0.596 | 0.232 | 0.982 | 0.750 | 3.851 | 4.515 | 6.667 |
| width_error_m | 1 | 0.094 | 0.094 | 0.094 | 0.000 | 0.094 | 0.094 | 0.094 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 17 | 0.303 | 0.242 | 0.338 | 0.096 | 0.408 | 0.737 | 1.937 |
| heading_error_deg | 17 | 1.100 | 0.710 | 2.124 | 1.414 | 2.841 | 3.103 | 3.458 |
| speed_error_mps | 17 | 0.143 | 0.083 | 0.341 | 0.258 | 0.776 | 1.762 | 4.472 |
| velocity_error_mps | 17 | 0.269 | 0.169 | 0.652 | 0.483 | 0.942 | 1.902 | 4.604 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 7 | 0.665 | 0.481 | 1.037 | 0.556 | 1.384 | 1.635 | 1.887 |
| heading_error_deg | 7 | 3.611 | 3.445 | 5.173 | 1.728 | 6.845 | 8.082 | 9.319 |
| speed_error_mps | 7 | 1.650 | 0.416 | 2.827 | 2.410 | 3.198 | 3.338 | 3.479 |
| velocity_error_mps | 7 | 1.964 | 0.894 | 3.745 | 2.851 | 5.073 | 5.870 | 6.667 |

Calibration of pos_std_m over 24 states: within 1/2/3 sigma 0.792/0.958/0.958 (Gaussian: 0.393/0.865/0.989).

## Observed-trajectory alignment

| Recorder | Accepted | Estimated offset | True offset | Error | Interval |
|----------|----------|-----------------:|------------:|------:|----------|
| C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
