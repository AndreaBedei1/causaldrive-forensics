# Road-user fusion against ground truth - S18/run_0_collision_ambiguity

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_004 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_005 | U5 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_006 | U6 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_007 | U6 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_008 | U4 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_009 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_010 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001 | U4 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_002 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U5 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U6 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_005 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_006 | U9 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |

Counts: anonymous: 15, correct link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_002 | C | no | 1.000 |
| U2 | A:track_003 | E | no | 1.000 |
| U3 | A:track_004 | F | no | 1.000 |
| U4 | B:track_001, A:track_008 | G | no | 1.000 |
| U5 | B:track_003, A:track_005 | D | no | 1.000 |
| U6 | A:track_006, B:track_004, A:track_007 | H | no | 1.000 |
| U7 | A:track_009, B:track_005 | E | no | 1.000 |
| U8 | A:track_010 | F | no | 1.000 |
| U9 | B:track_006 | F | no | 1.000 |

Merges over pairs of anonymous tracks: correct 7, false 0, missed 5.
Fragmentation (true road user -> entities): C -> U1, D -> U5, E -> U2/U7, F -> U3/U8/U9, G -> U4, H -> U6

## Fused state errors (against the majority identity, 677 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 677 | 0.161 | 0.115 | 0.289 | 0.174 | 0.450 | 0.748 | 1.836 |
| coverage_s | 9 | 6.350 | 3.250 | 11.950 | 8.700 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 677 | 0.298 | 0.092 | 0.784 | 0.692 | 2.118 | 3.090 | 9.766 |
| length_error_m | 9 | 0.261 | 0.192 | 0.419 | 0.227 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 677 | 1.729 | 1.161 | 3.191 | 2.030 | 4.139 | 6.385 | 11.114 |
| single_track_nominal_centre_error_m | 666 | 0.443 | 0.321 | 0.764 | 0.443 | 1.371 | 1.554 | 2.390 |
| speed_error_mps | 677 | 0.032 | 0.011 | 0.172 | 0.161 | 0.305 | 0.401 | 0.560 |
| velocity_error_mps | 677 | 0.090 | 0.030 | 0.252 | 0.222 | 0.458 | 0.690 | 1.787 |
| width_error_m | 9 | 0.107 | 0.094 | 0.107 | 0.013 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 400 | 0.159 | 0.109 | 0.264 | 0.154 | 0.336 | 0.384 | 0.722 |
| heading_error_deg | 400 | 0.225 | 0.058 | 0.754 | 0.696 | 1.552 | 2.244 | 3.186 |
| speed_error_mps | 400 | 0.032 | 0.013 | 0.139 | 0.127 | 0.258 | 0.344 | 0.560 |
| velocity_error_mps | 400 | 0.077 | 0.021 | 0.203 | 0.182 | 0.387 | 0.461 | 0.785 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 277 | 0.166 | 0.121 | 0.396 | 0.275 | 0.972 | 1.503 | 1.836 |
| heading_error_deg | 277 | 0.387 | 0.143 | 1.018 | 0.875 | 3.266 | 3.832 | 9.766 |
| speed_error_mps | 277 | 0.033 | 0.010 | 0.240 | 0.230 | 0.360 | 0.428 | 0.495 |
| velocity_error_mps | 277 | 0.111 | 0.050 | 0.302 | 0.252 | 0.750 | 0.863 | 1.787 |

Calibration of pos_std_m over 677 states: within 1/2/3 sigma 0.171/0.569/0.712 (Gaussian: 0.393/0.865/0.989).
