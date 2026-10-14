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
| B:track_006 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |

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
| U8 | A:track_010, B:track_006 | F | no | 1.000 |

Merges over pairs of anonymous tracks: correct 8, false 0, missed 4.
Fragmentation (true road user -> entities): C -> U1, D -> U5, E -> U2/U7, F -> U3/U8, G -> U4, H -> U6

## Fused state errors (against the majority identity, 665 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 665 | 0.189 | 0.112 | 0.408 | 0.296 | 1.875 | 2.306 | 2.825 |
| coverage_s | 8 | 9.100 | 5.050 | 11.950 | 6.900 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 665 | 0.611 | 0.164 | 1.559 | 1.395 | 2.604 | 6.290 | 15.806 |
| length_error_m | 8 | 0.192 | 0.161 | 0.351 | 0.191 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 665 | 0.405 | 0.229 | 0.789 | 0.561 | 1.595 | 1.853 | 3.865 |
| single_track_nominal_centre_error_m | 656 | 0.412 | 0.227 | 0.607 | 0.381 | 1.076 | 1.407 | 2.120 |
| speed_error_mps | 665 | 0.049 | 0.010 | 0.246 | 0.237 | 0.809 | 1.301 | 3.769 |
| velocity_error_mps | 665 | 0.150 | 0.045 | 0.473 | 0.428 | 1.102 | 1.866 | 3.771 |
| width_error_m | 8 | 0.107 | 0.094 | 0.146 | 0.052 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 378 | 0.142 | 0.075 | 0.231 | 0.156 | 0.359 | 0.496 | 1.607 |
| heading_error_deg | 378 | 0.602 | 0.105 | 1.474 | 1.370 | 4.647 | 8.024 | 15.806 |
| speed_error_mps | 378 | 0.052 | 0.018 | 0.219 | 0.201 | 0.911 | 1.510 | 3.769 |
| velocity_error_mps | 378 | 0.144 | 0.040 | 0.367 | 0.327 | 1.249 | 2.819 | 3.771 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 287 | 0.382 | 0.149 | 1.618 | 1.469 | 2.366 | 2.517 | 2.825 |
| heading_error_deg | 287 | 0.633 | 0.229 | 1.641 | 1.412 | 2.285 | 2.482 | 14.559 |
| speed_error_mps | 287 | 0.035 | 0.009 | 0.267 | 0.259 | 0.688 | 1.224 | 1.447 |
| velocity_error_mps | 287 | 0.196 | 0.051 | 0.502 | 0.451 | 0.850 | 1.304 | 2.822 |

Calibration of pos_std_m over 665 states: within 1/2/3 sigma 0.806/0.977/0.994 (Gaussian: 0.393/0.865/0.989).
