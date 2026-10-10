# Road-user fusion against ground truth - S18/run_0_abreast

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 0.732 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U3 | ANONYMOUS | - | D | 0.976 | anonymous (non-recording road user D) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 5, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001 | C | no | 0.732 |
| U2 | B:track_002, B:track_004 | C | no | 1.000 |
| U3 | B:track_003, A:track_003 | D | no | 0.988 |

Merges over pairs of anonymous tracks: correct 2, false 0, missed 2.
Fragmentation (true road user -> entities): C -> U1/U2, D -> U3

## Fused state errors (against the majority identity, 268 pure states; 30 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 268 | 0.401 | 0.228 | 0.660 | 0.432 | 0.926 | 1.349 | 3.631 |
| coverage_s | 3 | 10.200 | 9.575 | 10.325 | 0.750 | 10.400 | 10.425 | 10.450 |
| heading_error_deg | 268 | 0.506 | 0.268 | 0.992 | 0.724 | 1.403 | 2.248 | 15.630 |
| length_error_m | 3 | 0.192 | 0.139 | 0.192 | 0.053 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 268 | 0.829 | 0.462 | 1.283 | 0.821 | 1.692 | 2.113 | 6.627 |
| single_track_nominal_centre_error_m | 397 | 0.616 | 0.347 | 0.866 | 0.519 | 3.394 | 3.528 | 3.650 |
| speed_error_mps | 268 | 0.051 | 0.024 | 0.105 | 0.081 | 0.191 | 0.267 | 0.757 |
| velocity_error_mps | 268 | 0.144 | 0.085 | 0.254 | 0.169 | 0.374 | 0.515 | 3.336 |
| width_error_m | 3 | 0.263 | 0.185 | 0.263 | 0.078 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 101 | 0.315 | 0.175 | 0.403 | 0.228 | 0.747 | 0.900 | 1.980 |
| heading_error_deg | 101 | 0.725 | 0.390 | 1.166 | 0.777 | 1.945 | 7.720 | 15.630 |
| speed_error_mps | 101 | 0.062 | 0.034 | 0.142 | 0.109 | 0.269 | 0.427 | 0.757 |
| velocity_error_mps | 101 | 0.201 | 0.092 | 0.294 | 0.202 | 0.486 | 1.599 | 3.336 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 167 | 0.499 | 0.283 | 0.771 | 0.488 | 0.941 | 1.553 | 3.631 |
| heading_error_deg | 167 | 0.429 | 0.239 | 0.844 | 0.604 | 1.293 | 1.706 | 3.113 |
| speed_error_mps | 167 | 0.045 | 0.019 | 0.092 | 0.073 | 0.149 | 0.192 | 0.410 |
| velocity_error_mps | 167 | 0.127 | 0.080 | 0.221 | 0.141 | 0.303 | 0.417 | 0.839 |

Calibration of pos_std_m over 268 states: within 1/2/3 sigma 0.623/0.944/0.966 (Gaussian: 0.393/0.865/0.989).
