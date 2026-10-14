# Road-user fusion against ground truth - S18/run_0_far_to_near

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_004 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_005#segment_1 | U4 | ANONYMOUS | - | C | 0.857 | anonymous (non-recording road user C) |
| A:track_005#segment_2 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_006 | U6 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_007#segment_1 | U8 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_007#segment_2 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_008 | U10 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_009 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_002 | A | ASSOCIATED | collision | A | 0.808 | correct link |
| B:track_003 | U2 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_004 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_005 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_006 | U5 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_007 | U7 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_008 | U6 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_009 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_010 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_011 | U10 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_012 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_013 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

Counts: anonymous: 22, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_001, B:track_009 | F | no | 1.000 |
| U2 | A:track_003, B:track_003 | G | no | 1.000 |
| U3 | B:track_004, A:track_004, B:track_005, B:track_012, B:track_013, A:track_009 | E | no | 1.000 |
| U4 | A:track_005#segment_1 | C | no | 0.857 |
| U5 | B:track_006, A:track_005#segment_2 | C | no | 1.000 |
| U6 | A:track_006, B:track_008 | D | no | 1.000 |
| U7 | B:track_007 | D | no | 1.000 |
| U8 | A:track_007#segment_1 | C | no | 1.000 |
| U9 | B:track_010, A:track_007#segment_2 | C | no | 1.000 |
| U10 | B:track_011, A:track_008 | D | no | 1.000 |

Merges over pairs of anonymous tracks: correct 23, false 0, missed 21.
Fragmentation (true road user -> entities): C -> U4/U5/U8/U9, D -> U10/U6/U7, E -> U3, F -> U1, G -> U2

## Fused state errors (against the majority identity, 372 pure states; 2 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 372 | 0.276 | 0.172 | 0.763 | 0.591 | 1.614 | 2.095 | 2.774 |
| coverage_s | 10 | 2.700 | 1.488 | 5.287 | 3.800 | 6.005 | 8.727 | 11.450 |
| heading_error_deg | 372 | 5.209 | 2.067 | 10.367 | 8.300 | 13.454 | 16.056 | 27.949 |
| length_error_m | 10 | 0.192 | 0.192 | 0.192 | 0.000 | 0.215 | 0.317 | 0.419 |
| normalised_centre_error | 372 | 0.643 | 0.435 | 1.348 | 0.913 | 1.738 | 2.008 | 4.957 |
| single_track_nominal_centre_error_m | 370 | 0.726 | 0.373 | 1.145 | 0.772 | 1.435 | 1.657 | 2.706 |
| speed_error_mps | 372 | 0.217 | 0.083 | 0.698 | 0.615 | 1.185 | 1.994 | 3.992 |
| velocity_error_mps | 372 | 0.678 | 0.252 | 1.475 | 1.223 | 2.038 | 2.595 | 4.003 |
| width_error_m | 10 | 0.263 | 0.146 | 0.263 | 0.117 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 247 | 0.198 | 0.135 | 0.306 | 0.170 | 0.619 | 0.875 | 2.070 |
| heading_error_deg | 247 | 3.809 | 1.603 | 7.144 | 5.542 | 12.167 | 13.235 | 16.642 |
| speed_error_mps | 247 | 0.200 | 0.088 | 0.570 | 0.482 | 0.971 | 1.129 | 2.283 |
| velocity_error_mps | 247 | 0.468 | 0.205 | 1.097 | 0.892 | 1.608 | 1.756 | 2.609 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 125 | 0.835 | 0.667 | 1.700 | 1.033 | 2.297 | 2.428 | 2.774 |
| heading_error_deg | 125 | 9.638 | 3.421 | 12.509 | 9.088 | 17.608 | 22.861 | 27.949 |
| speed_error_mps | 125 | 0.391 | 0.075 | 1.036 | 0.961 | 2.592 | 3.379 | 3.992 |
| velocity_error_mps | 125 | 1.373 | 0.658 | 2.065 | 1.407 | 3.080 | 3.423 | 4.003 |

Calibration of pos_std_m over 372 states: within 1/2/3 sigma 0.659/0.946/0.995 (Gaussian: 0.393/0.865/0.989).
