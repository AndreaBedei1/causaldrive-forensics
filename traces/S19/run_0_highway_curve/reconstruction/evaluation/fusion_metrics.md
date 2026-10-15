# Road-user fusion against ground truth - S19/run_0_highway_curve

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_004 | U3 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_005 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_006 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_007 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_008 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_009 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_011 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001 | U3 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_002 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_003 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_004 | U2 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_005 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_006 | U9 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_007 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |

Counts: anonymous: 16, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_003 | C | no | 1.000 |
| U2 | A:track_003, B:track_004 | D | no | 1.000 |
| U3 | A:track_004, B:track_001 | G | no | 1.000 |
| U4 | A:track_005 | F | no | 1.000 |
| U5 | B:track_002, A:track_007, A:track_008, A:track_009 | E | no | 1.000 |
| U6 | A:track_006 | E | no | 1.000 |
| U7 | A:track_010 | G | no | 1.000 |
| U8 | A:track_011, B:track_007 | F | no | 1.000 |
| U9 | B:track_006 | G | no | 1.000 |

Merges over pairs of anonymous tracks: correct 10, false 0, missed 11.
Fragmentation (true road user -> entities): C -> U1, D -> U2, E -> U5/U6, F -> U4/U8, G -> U3/U7/U9

## Fused state errors (against the majority identity, 460 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 460 | 0.273 | 0.151 | 0.498 | 0.348 | 0.647 | 0.708 | 1.675 |
| coverage_s | 9 | 3.250 | 0.700 | 7.700 | 7.000 | 11.310 | 11.630 | 11.950 |
| heading_error_deg | 460 | 0.796 | 0.397 | 1.417 | 1.020 | 2.354 | 3.074 | 10.460 |
| length_error_m | 9 | 0.192 | 0.086 | 0.319 | 0.233 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 460 | 2.437 | 1.588 | 3.802 | 2.214 | 4.929 | 5.379 | 12.590 |
| single_track_nominal_centre_error_m | 460 | 0.765 | 0.559 | 0.925 | 0.366 | 1.180 | 1.504 | 2.387 |
| speed_error_mps | 460 | 0.047 | 0.019 | 0.115 | 0.096 | 0.318 | 0.436 | 0.639 |
| velocity_error_mps | 460 | 0.137 | 0.059 | 0.323 | 0.265 | 0.747 | 0.918 | 3.231 |
| width_error_m | 9 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 292 | 0.182 | 0.091 | 0.300 | 0.210 | 0.386 | 0.550 | 0.875 |
| heading_error_deg | 292 | 0.517 | 0.290 | 1.114 | 0.824 | 1.928 | 2.505 | 5.352 |
| speed_error_mps | 292 | 0.041 | 0.018 | 0.114 | 0.096 | 0.296 | 0.399 | 0.639 |
| velocity_error_mps | 292 | 0.111 | 0.049 | 0.226 | 0.177 | 0.547 | 0.771 | 1.755 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 168 | 0.550 | 0.339 | 0.639 | 0.300 | 0.794 | 1.050 | 1.675 |
| heading_error_deg | 168 | 1.111 | 0.773 | 1.943 | 1.170 | 2.955 | 4.817 | 10.460 |
| speed_error_mps | 168 | 0.057 | 0.023 | 0.116 | 0.093 | 0.327 | 0.436 | 0.579 |
| velocity_error_mps | 168 | 0.225 | 0.100 | 0.630 | 0.530 | 0.954 | 1.748 | 3.231 |

Calibration of pos_std_m over 460 states: within 1/2/3 sigma 0.100/0.378/0.604 (Gaussian: 0.393/0.865/0.989).
