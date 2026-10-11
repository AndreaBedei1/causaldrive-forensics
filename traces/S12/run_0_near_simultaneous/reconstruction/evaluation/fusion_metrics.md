# Road-user fusion against ground truth - S12/run_0_near_simultaneous

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| B:track_001#segment_1 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_001#segment_2 | U1 | ANONYMOUS | - | A | 1.000 | missed link (true identity A) |
| B:track_001#segment_3 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |

Counts: correct link: 3, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_001#segment_2 | A | yes | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): A -> U1

## Fused state errors (against the majority identity, 12 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 12 | 0.827 | 0.725 | 0.839 | 0.115 | 0.850 | 1.113 | 1.436 |
| coverage_s | 1 | 1.200 | 1.200 | 1.200 | 0.000 | 1.200 | 1.200 | 1.200 |
| heading_error_deg | 8 | 41.894 | 15.686 | 61.580 | 45.894 | 63.318 | 64.352 | 65.386 |
| length_error_m | 1 | 0.192 | 0.192 | 0.192 | 0.000 | 0.192 | 0.192 | 0.192 |
| normalised_centre_error | 12 | 1.915 | 1.303 | 2.041 | 0.738 | 2.072 | 2.119 | 2.173 |
| single_track_nominal_centre_error_m | 12 | 0.964 | 0.914 | 1.178 | 0.264 | 1.763 | 2.024 | 2.298 |
| speed_error_mps | 12 | 1.524 | 0.247 | 2.252 | 2.005 | 3.478 | 3.580 | 3.666 |
| velocity_error_mps | 12 | 2.070 | 0.252 | 2.816 | 2.564 | 3.631 | 3.647 | 3.666 |
| width_error_m | 1 | 0.263 | 0.263 | 0.263 | 0.000 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 10 | 0.827 | 0.686 | 0.835 | 0.149 | 0.849 | 0.849 | 0.850 |
| heading_error_deg | 6 | 56.365 | 26.107 | 62.148 | 36.041 | 63.909 | 64.647 | 65.386 |
| speed_error_mps | 10 | 1.398 | 0.181 | 1.606 | 1.425 | 3.229 | 3.447 | 3.666 |
| velocity_error_mps | 10 | 1.861 | 0.188 | 2.496 | 2.308 | 3.635 | 3.651 | 3.666 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 2 | 1.127 | 0.972 | 1.281 | 0.309 | 1.374 | 1.405 | 1.436 |
| heading_error_deg | 2 | 21.054 | 15.404 | 26.704 | 11.300 | 30.094 | 31.224 | 32.354 |
| speed_error_mps | 2 | 2.726 | 2.334 | 3.119 | 0.784 | 3.354 | 3.432 | 3.510 |
| velocity_error_mps | 2 | 2.787 | 2.368 | 3.206 | 0.838 | 3.457 | 3.541 | 3.625 |

Calibration of pos_std_m over 12 states: within 1/2/3 sigma 0.167/0.500/1.000 (Gaussian: 0.393/0.865/0.989).
