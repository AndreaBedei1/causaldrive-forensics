# Road-user fusion against ground truth - S16/run_0_overtaking

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_002 | U2 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_003#segment_1 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_003#segment_2 | U8 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_003#segment_3 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_004 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_005 | U5 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_006 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_007 | U9 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_008 | U10 | ANONYMOUS | - | G | 0.659 | anonymous (non-recording road user G) |
| A:track_009 | U13 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_010 | U15 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_011 | U14 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_001 | U1 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_002 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_003 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_004 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_005 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_006 | U9 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_007 | U11 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_008 | U12 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_009 | U14 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_010 | U15 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

Counts: anonymous: 21, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_001 | H | no | 1.000 |
| U2 | A:track_002 | I | no | 1.000 |
| U3 | A:track_003#segment_1, B:track_003, A:track_003#segment_3 | F | no | 1.000 |
| U4 | A:track_004 | D | no | 1.000 |
| U5 | A:track_005 | E | no | 1.000 |
| U6 | B:track_004 | E | no | 1.000 |
| U7 | B:track_005 | G | no | 1.000 |
| U8 | A:track_003#segment_2 | F | no | 1.000 |
| U9 | A:track_007, B:track_006 | D | no | 1.000 |
| U10 | A:track_008 | G | no | 0.659 |
| U11 | B:track_007 | G | no | 1.000 |
| U12 | B:track_008 | C | no | 1.000 |
| U13 | A:track_009 | C | no | 1.000 |
| U14 | B:track_009, A:track_011 | I | no | 1.000 |
| U15 | A:track_010, B:track_010 | E | no | 1.000 |

Merges over pairs of anonymous tracks: correct 7, false 0, missed 16.
Fragmentation (true road user -> entities): C -> U12/U13, D -> U4/U9, E -> U15/U5/U6, F -> U3/U8, G -> U10/U11/U7, H -> U1, I -> U14/U2

## Fused state errors (against the majority identity, 681 pure states; 17 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 681 | 0.410 | 0.164 | 0.620 | 0.456 | 1.077 | 2.284 | 3.370 |
| coverage_s | 15 | 3.650 | 2.300 | 5.800 | 3.500 | 9.380 | 11.425 | 11.950 |
| heading_error_deg | 681 | 0.850 | 0.365 | 1.869 | 1.504 | 4.146 | 6.308 | 9.912 |
| length_error_m | 15 | 0.192 | 0.086 | 0.305 | 0.220 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 681 | 0.794 | 0.390 | 1.180 | 0.789 | 1.809 | 3.088 | 6.150 |
| single_track_nominal_centre_error_m | 672 | 0.539 | 0.399 | 0.786 | 0.387 | 1.386 | 1.612 | 3.454 |
| speed_error_mps | 681 | 0.068 | 0.031 | 0.161 | 0.131 | 0.432 | 0.793 | 3.630 |
| velocity_error_mps | 681 | 0.227 | 0.105 | 0.488 | 0.384 | 1.095 | 1.462 | 3.644 |
| width_error_m | 15 | 0.107 | 0.101 | 0.263 | 0.163 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 349 | 0.181 | 0.122 | 0.371 | 0.249 | 0.589 | 0.781 | 1.529 |
| heading_error_deg | 349 | 0.826 | 0.346 | 1.650 | 1.304 | 4.246 | 6.631 | 9.912 |
| speed_error_mps | 349 | 0.070 | 0.037 | 0.146 | 0.109 | 0.374 | 0.738 | 3.587 |
| velocity_error_mps | 349 | 0.188 | 0.098 | 0.439 | 0.341 | 0.882 | 1.447 | 3.593 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 332 | 0.583 | 0.424 | 0.902 | 0.478 | 2.302 | 2.707 | 3.370 |
| heading_error_deg | 332 | 0.890 | 0.397 | 1.966 | 1.570 | 3.650 | 5.726 | 8.618 |
| speed_error_mps | 332 | 0.064 | 0.024 | 0.202 | 0.178 | 0.542 | 0.808 | 3.630 |
| velocity_error_mps | 332 | 0.251 | 0.121 | 0.540 | 0.419 | 1.154 | 1.464 | 3.644 |

Calibration of pos_std_m over 681 states: within 1/2/3 sigma 0.624/0.912/0.949 (Gaussian: 0.393/0.865/0.989).
