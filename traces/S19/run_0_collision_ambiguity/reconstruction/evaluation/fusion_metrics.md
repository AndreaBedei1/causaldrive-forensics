# Road-user fusion against ground truth - S19/run_0_collision_ambiguity

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_001#segment_2 | U7 | ANONYMOUS | - | D | 0.963 | anonymous (non-recording road user D) |
| A:track_002 | U2 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_003 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_004 | U4 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_005#segment_1 | U8 | ANONYMOUS | - | B | 0.889 | missed link (true identity B) |
| A:track_005#segment_2 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_005#segment_3 | U9 | ANONYMOUS | - | B | 1.000 | missed link (true identity B) |
| A:track_005#segment_4 | B | ASSOCIATED | common_frame | B | 1.000 | correct link |
| A:track_006 | U6 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_007 | U5 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_008 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_009 | U10 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_010 | U11 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_011 | U12 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_001 | U5 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_002 | U6 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U7 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_005 | U13 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_006 | U14 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |

Counts: anonymous: 17, correct link: 2, missed link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001#segment_1 | D | no | 1.000 |
| U2 | A:track_002 | E | no | 1.000 |
| U3 | A:track_003, B:track_004, A:track_008 | H | no | 1.000 |
| U4 | A:track_004 | F | no | 1.000 |
| U5 | B:track_001, A:track_007 | G | no | 1.000 |
| U6 | B:track_002, A:track_006 | C | no | 1.000 |
| U7 | B:track_003, A:track_001#segment_2 | D | no | 0.985 |
| U8 | A:track_005#segment_1 | B | yes | 0.889 |
| U9 | A:track_005#segment_3 | B | yes | 1.000 |
| U10 | A:track_009 | D | no | 1.000 |
| U11 | A:track_010 | E | no | 1.000 |
| U12 | A:track_011 | F | no | 1.000 |
| U13 | B:track_005 | E | no | 1.000 |
| U14 | B:track_006 | F | no | 1.000 |

Merges over pairs of anonymous tracks: correct 6, false 0, missed 12.
Fragmentation (true road user -> entities): B -> U8/U9, C -> U6, D -> U1/U10/U7, E -> U11/U13/U2, F -> U12/U14/U4, G -> U5, H -> U3

## Fused state errors (against the majority identity, 706 pure states; 4 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 706 | 0.278 | 0.128 | 0.744 | 0.616 | 1.898 | 2.329 | 3.429 |
| coverage_s | 14 | 2.500 | 1.525 | 9.175 | 7.650 | 11.950 | 11.950 | 11.950 |
| heading_error_deg | 702 | 0.862 | 0.220 | 2.289 | 2.068 | 6.910 | 13.305 | 20.355 |
| length_error_m | 14 | 0.192 | 0.113 | 0.419 | 0.306 | 0.419 | 0.700 | 1.223 |
| normalised_centre_error | 706 | 0.533 | 0.276 | 1.239 | 0.962 | 1.774 | 2.003 | 8.383 |
| single_track_nominal_centre_error_m | 690 | 0.497 | 0.345 | 0.696 | 0.350 | 1.193 | 1.456 | 2.230 |
| speed_error_mps | 706 | 0.085 | 0.028 | 0.324 | 0.295 | 1.024 | 1.473 | 4.180 |
| velocity_error_mps | 706 | 0.220 | 0.067 | 0.630 | 0.563 | 1.742 | 3.144 | 4.214 |
| width_error_m | 14 | 0.107 | 0.097 | 0.263 | 0.166 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 364 | 0.153 | 0.084 | 0.315 | 0.231 | 0.741 | 1.332 | 3.429 |
| heading_error_deg | 363 | 0.706 | 0.179 | 2.091 | 1.912 | 7.950 | 14.992 | 20.355 |
| speed_error_mps | 364 | 0.069 | 0.029 | 0.294 | 0.265 | 1.006 | 1.456 | 3.118 |
| velocity_error_mps | 364 | 0.163 | 0.055 | 0.585 | 0.529 | 2.018 | 3.179 | 4.214 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 342 | 0.569 | 0.274 | 1.624 | 1.351 | 2.331 | 2.498 | 2.829 |
| heading_error_deg | 339 | 1.159 | 0.273 | 2.296 | 2.023 | 6.132 | 8.408 | 19.604 |
| speed_error_mps | 342 | 0.125 | 0.028 | 0.349 | 0.321 | 1.151 | 1.552 | 4.180 |
| velocity_error_mps | 342 | 0.360 | 0.080 | 0.744 | 0.664 | 1.500 | 2.978 | 4.180 |

Calibration of pos_std_m over 706 states: within 1/2/3 sigma 0.704/0.948/0.984 (Gaussian: 0.393/0.865/0.989).
