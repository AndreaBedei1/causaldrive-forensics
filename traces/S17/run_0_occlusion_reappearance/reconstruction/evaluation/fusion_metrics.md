# Road-user fusion against ground truth - S17/run_0_occlusion_reappearance

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| A:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_003 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_004 | U4 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_005 | B | ASSOCIATED | collision | B | 0.676 | correct link |
| A:track_006 | U4 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_007 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_008 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_001 | U4 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_002 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U1 | ANONYMOUS | - | V | 1.000 | anonymous (non-recording road user V) |
| B:track_004 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_005 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_006 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |

Counts: anonymous: 12, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | V | no | 1.000 |
| U2 | A:track_002, B:track_002, A:track_007, B:track_006 | D | no | 1.000 |
| U3 | A:track_003, B:track_004 | E | no | 1.000 |
| U4 | B:track_001, A:track_004, A:track_006 | C | no | 1.000 |
| U5 | A:track_008 | E | no | 1.000 |

Merges over pairs of anonymous tracks: correct 11, false 0, missed 2.
Fragmentation (true road user -> entities): C -> U4, D -> U2, E -> U3/U5, V -> U1

## Fused state errors (against the majority identity, 418 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 418 | 0.422 | 0.179 | 0.625 | 0.446 | 0.727 | 0.784 | 2.551 |
| coverage_s | 5 | 11.950 | 3.450 | 11.950 | 8.500 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 418 | 0.579 | 0.259 | 1.089 | 0.829 | 1.706 | 2.167 | 7.612 |
| length_error_m | 5 | 0.192 | 0.086 | 0.192 | 0.106 | 0.659 | 0.815 | 0.971 |
| normalised_centre_error | 418 | 0.900 | 0.383 | 1.363 | 0.981 | 1.773 | 1.911 | 3.599 |
| single_track_nominal_centre_error_m | 416 | 0.462 | 0.331 | 0.599 | 0.269 | 0.844 | 1.076 | 1.450 |
| speed_error_mps | 418 | 0.039 | 0.013 | 0.075 | 0.062 | 0.150 | 0.248 | 0.677 |
| velocity_error_mps | 418 | 0.134 | 0.063 | 0.237 | 0.174 | 0.408 | 0.558 | 1.735 |
| width_error_m | 5 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 245 | 0.300 | 0.134 | 0.570 | 0.436 | 0.671 | 0.697 | 0.778 |
| heading_error_deg | 245 | 0.487 | 0.200 | 0.930 | 0.730 | 1.472 | 1.873 | 2.448 |
| speed_error_mps | 245 | 0.036 | 0.013 | 0.074 | 0.061 | 0.121 | 0.216 | 0.677 |
| velocity_error_mps | 245 | 0.111 | 0.054 | 0.223 | 0.169 | 0.335 | 0.441 | 0.854 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 173 | 0.548 | 0.333 | 0.681 | 0.349 | 0.873 | 1.089 | 2.551 |
| heading_error_deg | 173 | 0.726 | 0.394 | 1.250 | 0.856 | 2.047 | 3.490 | 7.612 |
| speed_error_mps | 173 | 0.042 | 0.015 | 0.079 | 0.064 | 0.182 | 0.355 | 0.521 |
| velocity_error_mps | 173 | 0.150 | 0.092 | 0.312 | 0.220 | 0.476 | 0.840 | 1.735 |

Calibration of pos_std_m over 418 states: within 1/2/3 sigma 0.553/0.974/0.995 (Gaussian: 0.393/0.865/0.989).
