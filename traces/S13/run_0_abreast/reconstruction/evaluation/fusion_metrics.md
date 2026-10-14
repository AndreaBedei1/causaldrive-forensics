# Road-user fusion against ground truth - S13/run_0_abreast

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

Counts: anonymous: 4, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | D | no | 1.000 |
| U2 | A:track_003, B:track_002 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 2, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 207 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 207 | 0.323 | 0.207 | 0.535 | 0.328 | 0.768 | 0.856 | 1.780 |
| coverage_s | 2 | 10.300 | 10.225 | 10.375 | 0.150 | 10.420 | 10.435 | 10.450 |
| heading_error_deg | 207 | 0.414 | 0.163 | 0.823 | 0.660 | 1.287 | 2.053 | 4.540 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 207 | 0.817 | 0.514 | 1.240 | 0.727 | 1.564 | 1.661 | 2.506 |
| single_track_nominal_centre_error_m | 207 | 0.442 | 0.310 | 0.595 | 0.284 | 0.682 | 0.745 | 0.867 |
| speed_error_mps | 207 | 0.034 | 0.017 | 0.067 | 0.050 | 0.119 | 0.164 | 0.264 |
| velocity_error_mps | 207 | 0.114 | 0.055 | 0.199 | 0.144 | 0.288 | 0.482 | 1.003 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 157 | 0.269 | 0.176 | 0.375 | 0.200 | 0.557 | 0.719 | 1.780 |
| heading_error_deg | 157 | 0.426 | 0.160 | 0.754 | 0.594 | 1.212 | 1.782 | 4.540 |
| speed_error_mps | 157 | 0.028 | 0.013 | 0.049 | 0.036 | 0.086 | 0.126 | 0.199 |
| velocity_error_mps | 157 | 0.103 | 0.043 | 0.174 | 0.131 | 0.265 | 0.361 | 0.931 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 50 | 0.680 | 0.485 | 0.796 | 0.311 | 0.882 | 0.893 | 0.911 |
| heading_error_deg | 50 | 0.409 | 0.224 | 0.929 | 0.705 | 1.941 | 2.551 | 3.783 |
| speed_error_mps | 50 | 0.068 | 0.037 | 0.114 | 0.076 | 0.171 | 0.203 | 0.264 |
| velocity_error_mps | 50 | 0.163 | 0.085 | 0.273 | 0.187 | 0.496 | 0.668 | 1.003 |

Calibration of pos_std_m over 207 states: within 1/2/3 sigma 0.662/0.976/1.000 (Gaussian: 0.393/0.865/0.989).
