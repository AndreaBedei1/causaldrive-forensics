# Road-user fusion against ground truth - S08/run_0_crash

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| C:track_001#segment_1 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| C:track_001#segment_2 | U2 | ANONYMOUS | - | B | 0.643 | missed link (true identity B) |
| C:track_001#segment_3 | U3 | ANONYMOUS | - | A | 0.921 | missed link (true identity A) |
| C:track_002 | U1 | ANONYMOUS | - | B | 0.632 | missed link (true identity B) |

Counts: correct link: 5, missed link: 3

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | C:track_002 | B | yes | 0.632 |
| U2 | C:track_001#segment_2 | B | yes | 0.643 |
| U3 | C:track_001#segment_3 | A | yes | 0.921 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 1.
Fragmentation (true road user -> entities): A -> U3, B -> U1/U2

## Fused state errors (against the majority identity, 126 pure states; 27 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 126 | 1.122 | 1.027 | 1.192 | 0.165 | 1.276 | 1.538 | 2.305 |
| coverage_s | 3 | 3.700 | 2.525 | 6.875 | 4.350 | 8.780 | 9.415 | 10.050 |
| heading_error_deg | 28 | 2.332 | 0.926 | 3.996 | 3.069 | 74.612 | 80.874 | 89.859 |
| length_error_m | 3 | 0.419 | 0.305 | 0.419 | 0.114 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 126 | 0.860 | 0.799 | 0.906 | 0.107 | 1.178 | 3.186 | 5.636 |
| single_track_nominal_centre_error_m | 126 | 1.345 | 1.220 | 1.387 | 0.167 | 1.419 | 1.451 | 2.192 |
| speed_error_mps | 126 | 0.169 | 0.092 | 0.313 | 0.221 | 0.806 | 1.716 | 4.472 |
| velocity_error_mps | 126 | 0.180 | 0.097 | 0.446 | 0.349 | 1.425 | 3.383 | 8.197 |
| width_error_m | 3 | 0.094 | 0.094 | 0.178 | 0.085 | 0.229 | 0.246 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 25 | 0.338 | 0.290 | 1.315 | 1.025 | 1.956 | 2.179 | 2.305 |
| heading_error_deg | 20 | 1.335 | 0.734 | 2.798 | 2.063 | 75.309 | 84.217 | 89.859 |
| speed_error_mps | 25 | 0.278 | 0.088 | 0.408 | 0.321 | 0.978 | 1.139 | 4.472 |
| velocity_error_mps | 25 | 0.382 | 0.225 | 0.820 | 0.595 | 3.999 | 7.301 | 8.197 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 101 | 1.138 | 1.069 | 1.191 | 0.122 | 1.254 | 1.279 | 1.887 |
| heading_error_deg | 8 | 4.380 | 3.496 | 6.227 | 2.731 | 29.089 | 52.153 | 75.218 |
| speed_error_mps | 101 | 0.166 | 0.095 | 0.268 | 0.173 | 0.611 | 1.738 | 3.479 |
| velocity_error_mps | 101 | 0.166 | 0.095 | 0.284 | 0.189 | 0.900 | 2.015 | 6.667 |

Calibration of pos_std_m over 126 states: within 1/2/3 sigma 0.865/0.921/0.937 (Gaussian: 0.393/0.865/0.989).

## Observed-trajectory alignment

| Recorder | Accepted | Estimated offset | True offset | Error | Interval |
|----------|----------|-----------------:|------------:|------:|----------|
| C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
