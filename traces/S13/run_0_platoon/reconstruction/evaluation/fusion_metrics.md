# Road-user fusion against ground truth - S13/run_0_platoon

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_002 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 5, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_002, A:track_002 | D | no | 1.000 |
| U2 | B:track_003, A:track_003, B:track_004 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 188 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 188 | 0.435 | 0.253 | 0.828 | 0.575 | 0.965 | 1.038 | 1.160 |
| coverage_s | 2 | 10.025 | 9.787 | 10.262 | 0.475 | 10.405 | 10.453 | 10.500 |
| heading_error_deg | 188 | 0.449 | 0.233 | 1.032 | 0.799 | 1.856 | 3.154 | 6.126 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 188 | 3.394 | 2.948 | 6.951 | 4.003 | 8.033 | 8.267 | 8.657 |
| single_track_nominal_centre_error_m | 186 | 0.507 | 0.317 | 0.878 | 0.561 | 1.005 | 1.097 | 1.241 |
| speed_error_mps | 188 | 0.047 | 0.020 | 0.117 | 0.097 | 0.145 | 0.164 | 0.650 |
| velocity_error_mps | 188 | 0.137 | 0.075 | 0.228 | 0.152 | 0.442 | 0.755 | 1.518 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 85 | 0.253 | 0.244 | 0.269 | 0.025 | 0.815 | 0.905 | 0.968 |
| heading_error_deg | 85 | 0.278 | 0.128 | 0.498 | 0.371 | 1.072 | 1.318 | 1.690 |
| speed_error_mps | 85 | 0.025 | 0.014 | 0.051 | 0.036 | 0.117 | 0.145 | 0.184 |
| velocity_error_mps | 85 | 0.081 | 0.054 | 0.137 | 0.083 | 0.215 | 0.283 | 0.317 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 103 | 0.803 | 0.509 | 0.932 | 0.423 | 1.022 | 1.099 | 1.160 |
| heading_error_deg | 103 | 0.752 | 0.324 | 1.339 | 1.015 | 2.854 | 4.489 | 6.126 |
| speed_error_mps | 103 | 0.082 | 0.041 | 0.127 | 0.086 | 0.152 | 0.213 | 0.650 |
| velocity_error_mps | 103 | 0.193 | 0.123 | 0.360 | 0.236 | 0.713 | 1.067 | 1.518 |

Calibration of pos_std_m over 188 states: within 1/2/3 sigma 0.021/0.080/0.261 (Gaussian: 0.393/0.865/0.989).
