# Road-user fusion against ground truth - S17/run_0_crash

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
| centre_error_m | 75 | 0.106 | 0.067 | 0.140 | 0.073 | 0.232 | 0.363 | 1.368 |
| coverage_s | 1 | 7.450 | 7.450 | 7.450 | 0.000 | 7.450 | 7.450 | 7.450 |
| heading_error_deg | 75 | 0.941 | 0.523 | 1.369 | 0.846 | 1.859 | 2.007 | 2.417 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 75 | 0.271 | 0.176 | 0.348 | 0.172 | 0.523 | 0.803 | 3.489 |
| single_track_nominal_centre_error_m | 137 | 0.690 | 0.280 | 1.804 | 1.524 | 2.155 | 2.260 | 2.966 |
| speed_error_mps | 75 | 0.067 | 0.022 | 0.105 | 0.083 | 0.130 | 0.134 | 0.245 |
| velocity_error_mps | 75 | 0.176 | 0.104 | 0.245 | 0.140 | 0.374 | 0.417 | 0.531 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 70 | 0.103 | 0.066 | 0.134 | 0.068 | 0.192 | 0.332 | 1.368 |
| heading_error_deg | 70 | 0.897 | 0.515 | 1.279 | 0.764 | 1.808 | 1.971 | 2.417 |
| speed_error_mps | 70 | 0.066 | 0.022 | 0.104 | 0.082 | 0.128 | 0.132 | 0.144 |
| velocity_error_mps | 70 | 0.168 | 0.099 | 0.235 | 0.136 | 0.355 | 0.392 | 0.466 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 5 | 0.197 | 0.173 | 0.232 | 0.059 | 0.310 | 0.337 | 0.363 |
| heading_error_deg | 5 | 1.550 | 1.117 | 1.852 | 0.736 | 1.974 | 2.014 | 2.055 |
| speed_error_mps | 5 | 0.093 | 0.054 | 0.182 | 0.128 | 0.220 | 0.233 | 0.245 |
| velocity_error_mps | 5 | 0.374 | 0.242 | 0.413 | 0.171 | 0.484 | 0.508 | 0.531 |

Calibration of pos_std_m over 75 states: within 1/2/3 sigma 0.973/0.987/0.987 (Gaussian: 0.393/0.865/0.989).
