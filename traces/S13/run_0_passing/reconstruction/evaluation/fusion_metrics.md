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
| U2 | B:track_003, A:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 201 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 201 | 0.311 | 0.241 | 0.406 | 0.165 | 0.551 | 0.586 | 0.797 |
| coverage_s | 2 | 9.950 | 9.825 | 10.075 | 0.250 | 10.150 | 10.175 | 10.200 |
| heading_error_deg | 201 | 0.289 | 0.100 | 0.749 | 0.649 | 1.179 | 1.364 | 15.673 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 201 | 3.436 | 2.711 | 4.107 | 1.396 | 4.385 | 4.562 | 7.591 |
| single_track_nominal_centre_error_m | 201 | 0.434 | 0.292 | 0.591 | 0.298 | 0.711 | 0.737 | 0.993 |
| speed_error_mps | 201 | 0.043 | 0.018 | 0.088 | 0.070 | 0.160 | 0.198 | 0.431 |
| velocity_error_mps | 201 | 0.108 | 0.060 | 0.179 | 0.120 | 0.281 | 0.386 | 3.307 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 141 | 0.282 | 0.213 | 0.337 | 0.124 | 0.385 | 0.412 | 0.797 |
| heading_error_deg | 141 | 0.253 | 0.100 | 0.627 | 0.527 | 1.117 | 1.325 | 15.673 |
| speed_error_mps | 141 | 0.035 | 0.015 | 0.071 | 0.056 | 0.160 | 0.176 | 0.431 |
| velocity_error_mps | 141 | 0.089 | 0.047 | 0.159 | 0.113 | 0.240 | 0.333 | 3.307 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 60 | 0.499 | 0.388 | 0.573 | 0.185 | 0.638 | 0.674 | 0.688 |
| heading_error_deg | 60 | 0.514 | 0.096 | 0.876 | 0.780 | 1.251 | 1.701 | 2.466 |
| speed_error_mps | 60 | 0.070 | 0.024 | 0.123 | 0.099 | 0.149 | 0.218 | 0.283 |
| velocity_error_mps | 60 | 0.162 | 0.106 | 0.213 | 0.106 | 0.332 | 0.410 | 0.635 |

Calibration of pos_std_m over 201 states: within 1/2/3 sigma 0.000/0.109/0.308 (Gaussian: 0.393/0.865/0.989).
