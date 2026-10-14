# Road-user fusion against ground truth - S16/run_0_overtaking

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_002 | U2 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_003 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_004 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_005 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_006 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_007 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_008 | U8 | ANONYMOUS | - | G | 0.673 | anonymous (non-recording road user G) |
| A:track_009 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_010 | U10 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_011 | U11 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_012 | U11 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_001 | A | ASSOCIATED | collision | A | 0.633 | correct link |
| B:track_002 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_003 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_004 | U1 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_005 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_006 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_007 | U8 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_008 | U11 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_009 | U10 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

Counts: anonymous: 19, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_004 | H | no | 1.000 |
| U2 | A:track_002 | I | no | 1.000 |
| U3 | A:track_003, B:track_002 | F | no | 1.000 |
| U4 | A:track_004, A:track_007, B:track_006 | D | no | 1.000 |
| U5 | A:track_005 | E | no | 1.000 |
| U6 | B:track_003 | E | no | 1.000 |
| U7 | B:track_005 | G | no | 1.000 |
| U8 | B:track_007, A:track_008 | G | no | 0.843 |
| U9 | A:track_009 | C | no | 1.000 |
| U10 | A:track_010, B:track_009 | E | no | 1.000 |
| U11 | A:track_011, B:track_008, A:track_012 | I | no | 1.000 |

Merges over pairs of anonymous tracks: correct 10, false 0, missed 10.
Fragmentation (true road user -> entities): C -> U9, D -> U4, E -> U10/U5/U6, F -> U3, G -> U7/U8, H -> U1, I -> U11/U2

## Fused state errors (against the majority identity, 571 pure states; 19 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 571 | 0.347 | 0.152 | 0.564 | 0.411 | 0.785 | 1.141 | 2.714 |
| coverage_s | 11 | 3.650 | 2.500 | 8.575 | 6.075 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 571 | 0.834 | 0.290 | 1.682 | 1.392 | 3.896 | 5.948 | 9.422 |
| length_error_m | 11 | 0.192 | 0.086 | 0.305 | 0.220 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 571 | 0.725 | 0.373 | 1.166 | 0.792 | 1.606 | 2.039 | 3.423 |
| single_track_nominal_centre_error_m | 561 | 0.537 | 0.402 | 0.724 | 0.322 | 1.069 | 1.325 | 2.047 |
| speed_error_mps | 571 | 0.061 | 0.028 | 0.142 | 0.114 | 0.355 | 0.697 | 3.384 |
| velocity_error_mps | 571 | 0.201 | 0.081 | 0.456 | 0.375 | 0.954 | 1.435 | 3.411 |
| width_error_m | 11 | 0.107 | 0.101 | 0.263 | 0.163 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 381 | 0.192 | 0.123 | 0.453 | 0.330 | 0.734 | 1.021 | 2.319 |
| heading_error_deg | 381 | 0.809 | 0.264 | 1.627 | 1.363 | 3.896 | 5.908 | 9.422 |
| speed_error_mps | 381 | 0.063 | 0.032 | 0.144 | 0.112 | 0.355 | 0.638 | 3.366 |
| velocity_error_mps | 381 | 0.195 | 0.077 | 0.419 | 0.343 | 0.832 | 1.409 | 3.369 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 190 | 0.549 | 0.410 | 0.649 | 0.239 | 0.920 | 1.811 | 2.714 |
| heading_error_deg | 190 | 0.884 | 0.359 | 1.851 | 1.493 | 3.875 | 6.150 | 8.612 |
| speed_error_mps | 190 | 0.050 | 0.019 | 0.131 | 0.112 | 0.338 | 0.738 | 3.384 |
| velocity_error_mps | 190 | 0.222 | 0.098 | 0.538 | 0.440 | 1.140 | 1.494 | 3.411 |

Calibration of pos_std_m over 571 states: within 1/2/3 sigma 0.655/0.940/0.996 (Gaussian: 0.393/0.865/0.989).
