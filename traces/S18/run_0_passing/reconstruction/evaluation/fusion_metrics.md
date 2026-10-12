# Road-user fusion against ground truth - S18/run_0_passing

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_005 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |

Counts: anonymous: 6, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003, B:track_005 | D | no | 1.000 |
| U2 | B:track_002, B:track_004, A:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 6, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 201 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 201 | 0.303 | 0.223 | 0.531 | 0.308 | 0.770 | 0.888 | 1.631 |
| coverage_s | 2 | 9.950 | 9.825 | 10.075 | 0.250 | 10.150 | 10.175 | 10.200 |
| heading_error_deg | 201 | 0.359 | 0.180 | 0.732 | 0.552 | 1.173 | 1.355 | 5.183 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 201 | 0.752 | 0.563 | 1.155 | 0.591 | 1.599 | 1.748 | 4.099 |
| single_track_nominal_centre_error_m | 201 | 0.474 | 0.371 | 0.544 | 0.173 | 0.671 | 0.744 | 1.705 |
| speed_error_mps | 201 | 0.034 | 0.016 | 0.079 | 0.064 | 0.141 | 0.184 | 0.350 |
| velocity_error_mps | 201 | 0.102 | 0.052 | 0.198 | 0.146 | 0.284 | 0.335 | 1.200 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 142 | 0.261 | 0.191 | 0.336 | 0.145 | 0.574 | 0.723 | 1.631 |
| heading_error_deg | 142 | 0.369 | 0.187 | 0.732 | 0.544 | 1.272 | 1.421 | 5.183 |
| speed_error_mps | 142 | 0.027 | 0.014 | 0.060 | 0.047 | 0.112 | 0.155 | 0.350 |
| velocity_error_mps | 142 | 0.095 | 0.050 | 0.173 | 0.123 | 0.281 | 0.318 | 1.200 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 59 | 0.611 | 0.441 | 0.766 | 0.325 | 0.903 | 0.940 | 0.958 |
| heading_error_deg | 59 | 0.307 | 0.145 | 0.700 | 0.555 | 1.095 | 1.276 | 1.806 |
| speed_error_mps | 59 | 0.059 | 0.033 | 0.130 | 0.098 | 0.190 | 0.222 | 0.330 |
| velocity_error_mps | 59 | 0.133 | 0.063 | 0.215 | 0.152 | 0.294 | 0.367 | 0.518 |

Calibration of pos_std_m over 201 states: within 1/2/3 sigma 0.697/0.965/0.990 (Gaussian: 0.393/0.865/0.989).
