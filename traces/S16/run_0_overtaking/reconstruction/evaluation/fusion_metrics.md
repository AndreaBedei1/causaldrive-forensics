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
| A:track_008 | U9 | ANONYMOUS | - | G | 0.673 | anonymous (non-recording road user G) |
| A:track_009 | U10 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_010 | U11 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_011 | U12 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| A:track_012 | U12 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_001 | A | ASSOCIATED | collision | A | 0.633 | correct link |
| B:track_002 | U3 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_003 | U6 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_004 | U1 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_005 | U7 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_006 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_007 | U8 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_008 | U12 | ANONYMOUS | - | I | 1.000 | anonymous (non-recording road user I) |
| B:track_009 | U11 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |

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
| U8 | B:track_007 | G | no | 1.000 |
| U9 | A:track_008 | G | no | 0.673 |
| U10 | A:track_009 | C | no | 1.000 |
| U11 | A:track_010, B:track_009 | E | no | 1.000 |
| U12 | A:track_011, B:track_008, A:track_012 | I | no | 1.000 |

Merges over pairs of anonymous tracks: correct 9, false 0, missed 11.
Fragmentation (true road user -> entities): C -> U10, D -> U4, E -> U11/U5/U6, F -> U3, G -> U7/U8/U9, H -> U1, I -> U12/U2

## Fused state errors (against the majority identity, 628 pure states; 18 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 628 | 0.363 | 0.159 | 0.558 | 0.399 | 0.842 | 1.312 | 3.330 |
| coverage_s | 12 | 4.425 | 2.600 | 7.188 | 4.588 | 11.875 | 11.950 | 11.950 |
| heading_error_deg | 628 | 0.831 | 0.297 | 1.764 | 1.468 | 4.363 | 6.494 | 17.390 |
| length_error_m | 12 | 0.192 | 0.086 | 0.249 | 0.163 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 628 | 0.724 | 0.367 | 1.140 | 0.773 | 1.590 | 2.023 | 6.077 |
| single_track_nominal_centre_error_m | 617 | 0.536 | 0.399 | 0.722 | 0.322 | 1.174 | 1.345 | 3.558 |
| speed_error_mps | 628 | 0.063 | 0.029 | 0.178 | 0.149 | 0.395 | 0.716 | 4.123 |
| velocity_error_mps | 628 | 0.212 | 0.086 | 0.473 | 0.387 | 1.112 | 1.506 | 5.030 |
| width_error_m | 12 | 0.107 | 0.104 | 0.263 | 0.159 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 361 | 0.183 | 0.116 | 0.383 | 0.266 | 0.593 | 0.814 | 1.726 |
| heading_error_deg | 361 | 0.784 | 0.247 | 1.584 | 1.337 | 4.006 | 5.988 | 9.422 |
| speed_error_mps | 361 | 0.063 | 0.032 | 0.142 | 0.110 | 0.361 | 0.696 | 3.366 |
| velocity_error_mps | 361 | 0.191 | 0.072 | 0.404 | 0.332 | 0.840 | 1.413 | 3.369 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 267 | 0.538 | 0.398 | 0.698 | 0.300 | 1.372 | 2.134 | 3.330 |
| heading_error_deg | 267 | 0.899 | 0.385 | 2.155 | 1.770 | 4.942 | 6.828 | 17.390 |
| speed_error_mps | 267 | 0.062 | 0.022 | 0.229 | 0.208 | 0.434 | 0.745 | 4.123 |
| velocity_error_mps | 267 | 0.256 | 0.114 | 0.568 | 0.454 | 1.244 | 1.618 | 5.030 |

Calibration of pos_std_m over 628 states: within 1/2/3 sigma 0.672/0.947/0.989 (Gaussian: 0.393/0.865/0.989).
