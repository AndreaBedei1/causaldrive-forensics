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
| U2 | B:track_003, B:track_004, A:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 168 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 168 | 0.433 | 0.299 | 0.785 | 0.486 | 0.987 | 1.074 | 1.329 |
| coverage_s | 2 | 9.200 | 8.550 | 9.850 | 1.300 | 10.240 | 10.370 | 10.500 |
| heading_error_deg | 168 | 0.495 | 0.191 | 1.123 | 0.933 | 2.173 | 3.382 | 6.136 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 168 | 0.952 | 0.707 | 1.442 | 0.735 | 1.925 | 2.136 | 2.572 |
| single_track_nominal_centre_error_m | 167 | 0.436 | 0.346 | 0.826 | 0.480 | 0.973 | 1.042 | 1.207 |
| speed_error_mps | 168 | 0.046 | 0.013 | 0.090 | 0.077 | 0.165 | 0.187 | 0.221 |
| velocity_error_mps | 168 | 0.118 | 0.060 | 0.263 | 0.203 | 0.492 | 0.820 | 1.572 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 91 | 0.311 | 0.223 | 0.372 | 0.150 | 0.523 | 0.803 | 1.008 |
| heading_error_deg | 91 | 0.278 | 0.125 | 0.538 | 0.413 | 1.231 | 2.242 | 5.829 |
| speed_error_mps | 91 | 0.026 | 0.006 | 0.061 | 0.055 | 0.099 | 0.156 | 0.196 |
| velocity_error_mps | 91 | 0.075 | 0.046 | 0.118 | 0.072 | 0.264 | 0.473 | 1.191 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 77 | 0.758 | 0.611 | 0.940 | 0.328 | 1.075 | 1.203 | 1.329 |
| heading_error_deg | 77 | 0.990 | 0.558 | 1.594 | 1.035 | 2.496 | 4.022 | 6.136 |
| speed_error_mps | 77 | 0.067 | 0.037 | 0.125 | 0.089 | 0.177 | 0.200 | 0.221 |
| velocity_error_mps | 77 | 0.239 | 0.139 | 0.390 | 0.251 | 0.612 | 1.031 | 1.572 |

Calibration of pos_std_m over 168 states: within 1/2/3 sigma 0.530/0.929/1.000 (Gaussian: 0.393/0.865/0.989).
