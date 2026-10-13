# Road-user fusion against ground truth - S23/run_0

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_004 | U6 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_005 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_006 | U7 | ANONYMOUS | - | D | 0.500 | anonymous (non-recording road user D) |
| A:track_007 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_008 | U8 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_009 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_001 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_003 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_004 | U4 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_005 | U5 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_006 | U6 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_007 | U1 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_008 | U8 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_009 | U9 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_010 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_011 | U3 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

Counts: anonymous: 18, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_001, B:track_007 | F | no | 1.000 |
| U2 | A:track_003 | G | no | 1.000 |
| U3 | B:track_003, A:track_005, B:track_010, B:track_011, A:track_009 | E | no | 1.000 |
| U4 | B:track_004 | G | no | 1.000 |
| U5 | B:track_005 | D | no | 1.000 |
| U6 | B:track_006, A:track_004 | C | no | 1.000 |
| U7 | A:track_006 | D | no | 0.500 |
| U8 | B:track_008, A:track_008 | D | no | 1.000 |
| U9 | A:track_007, B:track_009 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 16, false 0, missed 10.
Fragmentation (true road user -> entities): C -> U6/U9, D -> U5/U7/U8, E -> U3, F -> U1, G -> U2/U4

## Fused state errors (against the majority identity, 371 pure states; 8 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 371 | 0.312 | 0.187 | 0.917 | 0.730 | 1.880 | 2.185 | 2.692 |
| coverage_s | 9 | 2.950 | 2.150 | 5.400 | 3.250 | 6.680 | 9.240 | 11.800 |
| heading_error_deg | 371 | 4.333 | 1.563 | 9.165 | 7.602 | 11.973 | 12.820 | 40.899 |
| length_error_m | 9 | 0.192 | 0.086 | 0.192 | 0.106 | 0.237 | 0.328 | 0.419 |
| normalised_centre_error | 371 | 0.699 | 0.480 | 1.390 | 0.909 | 1.815 | 2.039 | 3.431 |
| single_track_nominal_centre_error_m | 370 | 0.710 | 0.427 | 1.137 | 0.710 | 1.466 | 1.762 | 4.355 |
| speed_error_mps | 371 | 0.223 | 0.051 | 0.767 | 0.716 | 1.498 | 1.951 | 3.985 |
| velocity_error_mps | 371 | 0.538 | 0.203 | 1.356 | 1.153 | 1.918 | 2.513 | 5.042 |
| width_error_m | 9 | 0.263 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 227 | 0.215 | 0.155 | 0.289 | 0.134 | 0.527 | 0.810 | 2.128 |
| heading_error_deg | 227 | 3.369 | 1.373 | 6.531 | 5.158 | 10.186 | 11.744 | 13.210 |
| speed_error_mps | 227 | 0.187 | 0.056 | 0.506 | 0.449 | 1.016 | 1.215 | 1.726 |
| velocity_error_mps | 227 | 0.389 | 0.182 | 0.889 | 0.706 | 1.524 | 1.730 | 2.071 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 144 | 0.965 | 0.639 | 1.878 | 1.239 | 2.290 | 2.415 | 2.692 |
| heading_error_deg | 144 | 7.414 | 1.897 | 11.455 | 9.557 | 13.005 | 13.569 | 40.899 |
| speed_error_mps | 144 | 0.543 | 0.048 | 1.338 | 1.290 | 2.265 | 3.231 | 3.985 |
| velocity_error_mps | 144 | 1.235 | 0.278 | 1.884 | 1.606 | 2.882 | 3.527 | 5.042 |

Calibration of pos_std_m over 371 states: within 1/2/3 sigma 0.639/0.946/0.981 (Gaussian: 0.393/0.865/0.989).
