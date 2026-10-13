# Road-user fusion against ground truth - S19/run_0

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_001#segment_2 | U8 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | U2 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_003 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| A:track_004 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_005#segment_1 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_005#segment_2 | U9 | ANONYMOUS | - | E | 0.600 | anonymous (non-recording road user E) |
| A:track_005#segment_3 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_006 | U12 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| A:track_007 | U10 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| A:track_008 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| A:track_009 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| A:track_010 | U14 | ANONYMOUS | - | J | 1.000 | anonymous (non-recording road user J) |
| B:track_001 | U4 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_002 | A | ASSOCIATED | common_frame | A | 1.000 | correct link |
| B:track_003 | U5 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_004 | U6 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_005 | U7 | ANONYMOUS | - | E | 1.000 | anonymous (non-recording road user E) |
| B:track_006 | U8 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_007 | U3 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |
| B:track_008 | U10 | ANONYMOUS | - | G | 1.000 | anonymous (non-recording road user G) |
| B:track_009 | U11 | ANONYMOUS | - | F | 1.000 | anonymous (non-recording road user F) |
| B:track_010 | U13 | ANONYMOUS | - | J | 0.816 | anonymous (non-recording road user J) |
| B:track_011 | U15 | ANONYMOUS | - | H | 1.000 | anonymous (non-recording road user H) |

Counts: anonymous: 22, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001#segment_1 | C | no | 1.000 |
| U2 | A:track_002 | J | no | 1.000 |
| U3 | A:track_003, B:track_007 | H | no | 1.000 |
| U4 | B:track_001, A:track_005#segment_3 | D | no | 1.000 |
| U5 | B:track_003 | F | no | 1.000 |
| U6 | B:track_004 | G | no | 1.000 |
| U7 | A:track_005#segment_1, B:track_005, A:track_008 | E | no | 1.000 |
| U8 | B:track_006, A:track_001#segment_2 | C | no | 1.000 |
| U9 | A:track_005#segment_2 | E | no | 0.600 |
| U10 | B:track_008, A:track_007 | G | no | 1.000 |
| U11 | B:track_009, A:track_009 | F | no | 1.000 |
| U12 | A:track_006 | J | no | 1.000 |
| U13 | B:track_010 | J | no | 0.816 |
| U14 | A:track_010 | J | no | 1.000 |
| U15 | B:track_011 | H | no | 1.000 |

Merges over pairs of anonymous tracks: correct 8, false 0, missed 17.
Fragmentation (true road user -> entities): C -> U1/U8, D -> U4, E -> U7/U9, F -> U11/U5, G -> U10/U6, H -> U15/U3, J -> U12/U13/U14/U2

## Fused state errors (against the majority identity, 689 pure states; 21 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 689 | 0.256 | 0.141 | 0.551 | 0.409 | 0.798 | 0.945 | 2.131 |
| coverage_s | 15 | 3.650 | 1.800 | 5.575 | 3.775 | 11.900 | 11.915 | 11.950 |
| heading_error_deg | 689 | 0.654 | 0.256 | 1.502 | 1.246 | 2.703 | 3.606 | 15.299 |
| length_error_m | 15 | 0.192 | 0.192 | 0.419 | 0.227 | 0.419 | 0.419 | 0.419 |
| normalised_centre_error | 689 | 0.548 | 0.335 | 1.016 | 0.680 | 1.577 | 1.790 | 4.861 |
| single_track_nominal_centre_error_m | 674 | 0.304 | 0.205 | 0.633 | 0.429 | 0.854 | 1.036 | 2.162 |
| speed_error_mps | 689 | 0.035 | 0.013 | 0.073 | 0.060 | 0.130 | 0.182 | 0.531 |
| velocity_error_mps | 689 | 0.153 | 0.068 | 0.353 | 0.285 | 0.637 | 0.829 | 3.204 |
| width_error_m | 15 | 0.107 | 0.094 | 0.263 | 0.169 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 334 | 0.150 | 0.099 | 0.225 | 0.126 | 0.347 | 0.684 | 1.988 |
| heading_error_deg | 334 | 0.553 | 0.260 | 1.050 | 0.791 | 2.337 | 3.572 | 15.299 |
| speed_error_mps | 334 | 0.035 | 0.013 | 0.074 | 0.061 | 0.133 | 0.176 | 0.531 |
| velocity_error_mps | 334 | 0.134 | 0.071 | 0.280 | 0.209 | 0.565 | 0.808 | 3.204 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 355 | 0.489 | 0.276 | 0.706 | 0.429 | 0.929 | 1.078 | 2.131 |
| heading_error_deg | 355 | 0.833 | 0.246 | 1.841 | 1.595 | 2.964 | 3.605 | 12.814 |
| speed_error_mps | 355 | 0.035 | 0.013 | 0.073 | 0.060 | 0.129 | 0.184 | 0.295 |
| velocity_error_mps | 355 | 0.190 | 0.065 | 0.440 | 0.374 | 0.661 | 0.833 | 2.759 |

Calibration of pos_std_m over 689 states: within 1/2/3 sigma 0.742/0.971/0.993 (Gaussian: 0.393/0.865/0.989).
