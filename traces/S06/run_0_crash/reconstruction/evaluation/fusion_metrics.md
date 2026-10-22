# Road-user fusion against ground truth - S06/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_001 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| C:track_002#segment_1 | B | ASSOCIATED | common_frame | B | 0.935 | correct link |
| C:track_002#segment_2 | U1 | ANONYMOUS | - | A | 1.000 | missed link (true identity A) |

Counts: correct link: 6, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | C:track_002#segment_2 | A | yes | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): A -> U1

## Fused state errors (against the majority identity, 99 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 99 | 1.745 | 1.656 | 1.769 | 0.113 | 1.784 | 1.799 | 1.832 |
| coverage_s | 1 | 9.850 | 9.850 | 9.850 | 0.000 | 9.850 | 9.850 | 9.850 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 99 | 10.369 | 9.390 | 10.907 | 1.516 | 11.212 | 11.240 | 11.285 |
| single_track_nominal_centre_error_m | 98 | 1.205 | 1.176 | 1.223 | 0.047 | 1.234 | 1.247 | 1.256 |
| speed_error_mps | 99 | 0.066 | 0.043 | 0.100 | 0.057 | 0.562 | 0.578 | 0.870 |
| velocity_error_mps | 99 | 0.066 | 0.043 | 0.100 | 0.057 | 0.562 | 0.578 | 0.870 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 1 | 1.089 | 1.089 | 1.089 | 0.000 | 1.089 | 1.089 | 1.089 |
| speed_error_mps | 1 | 0.526 | 0.526 | 0.526 | 0.000 | 0.526 | 0.526 | 0.526 |
| velocity_error_mps | 1 | 0.526 | 0.526 | 0.526 | 0.000 | 0.526 | 0.526 | 0.526 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 98 | 1.746 | 1.659 | 1.769 | 0.110 | 1.785 | 1.799 | 1.832 |
| speed_error_mps | 98 | 0.066 | 0.042 | 0.095 | 0.052 | 0.562 | 0.579 | 0.870 |
| velocity_error_mps | 98 | 0.066 | 0.042 | 0.095 | 0.052 | 0.562 | 0.579 | 0.870 |

Calibration of pos_std_m over 99 states: within 1/2/3 sigma 0.010/0.030/0.051 (Gaussian: 0.393/0.865/0.989).

## Observed-trajectory alignment

| Recorder | Accepted | Estimated offset | True offset | Error | Interval |
|----------|----------|-----------------:|------------:|------:|----------|
| C | True | -4.150 | -4.100 | -0.050 | [-4.2, -4.0] |
