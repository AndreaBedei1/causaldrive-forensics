# Road-user fusion against ground truth - S18/run_0_passing

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_001#segment_2 | U3 | ANONYMOUS | - | D | 0.609 | anonymous (non-recording road user D) |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_004 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_005 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |

Counts: anonymous: 9, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001#segment_1, B:track_003, A:track_004, B:track_005 | D | no | 1.000 |
| U2 | B:track_002, B:track_004, A:track_003, A:track_001#segment_3 | C | no | 1.000 |
| U3 | A:track_001#segment_2 | D | no | 0.609 |

Merges over pairs of anonymous tracks: correct 12, false 0, missed 4.
Fragmentation (true road user -> entities): C -> U2, D -> U1/U3

## Fused state errors (against the majority identity, 215 pure states; 9 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 215 | 0.378 | 0.236 | 0.588 | 0.352 | 0.879 | 0.986 | 3.355 |
| coverage_s | 3 | 9.700 | 6.000 | 9.950 | 3.950 | 10.100 | 10.150 | 10.200 |
| heading_error_deg | 215 | 0.419 | 0.217 | 0.841 | 0.624 | 1.516 | 3.127 | 13.178 |
| length_error_m | 3 | 0.086 | 0.086 | 0.139 | 0.053 | 0.171 | 0.181 | 0.192 |
| normalised_centre_error | 215 | 0.837 | 0.570 | 1.282 | 0.712 | 1.731 | 1.950 | 6.122 |
| single_track_nominal_centre_error_m | 402 | 0.492 | 0.319 | 0.671 | 0.352 | 3.414 | 3.556 | 3.674 |
| speed_error_mps | 215 | 0.063 | 0.029 | 0.106 | 0.077 | 0.165 | 0.213 | 0.455 |
| velocity_error_mps | 215 | 0.114 | 0.077 | 0.213 | 0.137 | 0.366 | 0.703 | 2.914 |
| width_error_m | 3 | 0.107 | 0.107 | 0.185 | 0.078 | 0.232 | 0.247 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 136 | 0.284 | 0.200 | 0.435 | 0.235 | 0.627 | 0.844 | 1.757 |
| heading_error_deg | 136 | 0.422 | 0.223 | 0.871 | 0.648 | 1.656 | 4.224 | 11.718 |
| speed_error_mps | 136 | 0.061 | 0.027 | 0.101 | 0.074 | 0.147 | 0.200 | 0.443 |
| velocity_error_mps | 136 | 0.110 | 0.072 | 0.215 | 0.143 | 0.365 | 0.949 | 2.653 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 79 | 0.585 | 0.412 | 0.814 | 0.402 | 0.971 | 1.103 | 3.355 |
| heading_error_deg | 79 | 0.392 | 0.189 | 0.793 | 0.604 | 1.342 | 1.804 | 13.178 |
| speed_error_mps | 79 | 0.066 | 0.034 | 0.120 | 0.086 | 0.174 | 0.218 | 0.455 |
| velocity_error_mps | 79 | 0.129 | 0.082 | 0.213 | 0.131 | 0.366 | 0.438 | 2.914 |

Calibration of pos_std_m over 215 states: within 1/2/3 sigma 0.614/0.949/0.981 (Gaussian: 0.393/0.865/0.989).
