# Road-user fusion against ground truth - S13/run_0_passing

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_004 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |

Counts: anonymous: 5, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_002, B:track_004 | D | no | 1.000 |
| U2 | A:track_003, B:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 200 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 200 | 0.332 | 0.223 | 0.543 | 0.320 | 0.757 | 0.844 | 1.774 |
| coverage_s | 2 | 9.900 | 9.800 | 10.000 | 0.200 | 10.060 | 10.080 | 10.100 |
| heading_error_deg | 200 | 0.321 | 0.113 | 0.812 | 0.699 | 1.298 | 2.062 | 4.283 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 200 | 0.807 | 0.536 | 1.193 | 0.656 | 1.481 | 1.587 | 4.176 |
| single_track_nominal_centre_error_m | 200 | 0.434 | 0.299 | 0.561 | 0.262 | 0.694 | 0.714 | 0.768 |
| speed_error_mps | 200 | 0.029 | 0.012 | 0.068 | 0.056 | 0.117 | 0.142 | 0.348 |
| velocity_error_mps | 200 | 0.102 | 0.043 | 0.205 | 0.162 | 0.330 | 0.468 | 1.014 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 142 | 0.276 | 0.176 | 0.366 | 0.190 | 0.542 | 0.620 | 1.774 |
| heading_error_deg | 142 | 0.305 | 0.129 | 0.815 | 0.686 | 1.384 | 2.190 | 4.283 |
| speed_error_mps | 142 | 0.026 | 0.012 | 0.056 | 0.044 | 0.093 | 0.128 | 0.348 |
| velocity_error_mps | 142 | 0.078 | 0.042 | 0.188 | 0.146 | 0.309 | 0.466 | 1.014 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 58 | 0.654 | 0.466 | 0.772 | 0.306 | 0.854 | 0.872 | 1.044 |
| heading_error_deg | 58 | 0.411 | 0.092 | 0.791 | 0.699 | 1.263 | 1.708 | 2.466 |
| speed_error_mps | 58 | 0.043 | 0.022 | 0.097 | 0.075 | 0.145 | 0.176 | 0.289 |
| velocity_error_mps | 58 | 0.144 | 0.057 | 0.225 | 0.168 | 0.339 | 0.450 | 0.682 |

Calibration of pos_std_m over 200 states: within 1/2/3 sigma 0.670/0.990/0.995 (Gaussian: 0.393/0.865/0.989).
