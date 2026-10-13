# Road-user fusion against ground truth - S13/run_0_abreast

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001#segment_1 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_001#segment_2 | U4 | ANONYMOUS | - | D | 0.795 | anonymous (non-recording road user D) |
| A:track_001#segment_3 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U3 | ANONYMOUS | - | D | 0.978 | anonymous (non-recording road user D) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_003 | U3 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_004 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 7, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001#segment_1 | D | no | 1.000 |
| U2 | B:track_002, B:track_004, A:track_001#segment_3 | C | no | 1.000 |
| U3 | B:track_003, A:track_003 | D | no | 0.988 |
| U4 | A:track_001#segment_2 | D | no | 0.795 |

Merges over pairs of anonymous tracks: correct 4, false 0, missed 5.
Fragmentation (true road user -> entities): C -> U2, D -> U1/U3/U4

## Fused state errors (against the majority identity, 238 pure states; 12 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 238 | 0.402 | 0.240 | 0.707 | 0.466 | 0.883 | 0.946 | 3.249 |
| coverage_s | 4 | 7.000 | 2.913 | 10.262 | 7.350 | 10.375 | 10.412 | 10.450 |
| heading_error_deg | 238 | 0.575 | 0.267 | 1.104 | 0.837 | 1.969 | 3.182 | 16.274 |
| length_error_m | 4 | 0.086 | 0.086 | 0.113 | 0.026 | 0.160 | 0.176 | 0.192 |
| normalised_centre_error | 238 | 0.874 | 0.561 | 1.374 | 0.813 | 1.675 | 1.878 | 5.928 |
| single_track_nominal_centre_error_m | 238 | 0.724 | 0.475 | 1.171 | 0.696 | 1.478 | 1.568 | 1.685 |
| speed_error_mps | 238 | 0.072 | 0.030 | 0.118 | 0.088 | 0.244 | 0.296 | 0.974 |
| velocity_error_mps | 238 | 0.160 | 0.085 | 0.275 | 0.190 | 0.457 | 0.715 | 3.558 |
| width_error_m | 4 | 0.107 | 0.107 | 0.146 | 0.039 | 0.216 | 0.240 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 142 | 0.314 | 0.192 | 0.487 | 0.295 | 0.734 | 0.993 | 1.903 |
| heading_error_deg | 142 | 0.598 | 0.281 | 1.003 | 0.722 | 1.839 | 2.887 | 14.764 |
| speed_error_mps | 142 | 0.066 | 0.025 | 0.117 | 0.092 | 0.240 | 0.271 | 0.974 |
| velocity_error_mps | 142 | 0.159 | 0.080 | 0.260 | 0.180 | 0.401 | 0.662 | 3.260 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 96 | 0.651 | 0.416 | 0.827 | 0.411 | 0.926 | 0.941 | 3.249 |
| heading_error_deg | 96 | 0.539 | 0.227 | 1.229 | 1.002 | 2.436 | 4.391 | 16.274 |
| speed_error_mps | 96 | 0.079 | 0.032 | 0.122 | 0.089 | 0.239 | 0.326 | 0.958 |
| velocity_error_mps | 96 | 0.181 | 0.090 | 0.309 | 0.219 | 0.528 | 1.051 | 3.558 |

Calibration of pos_std_m over 238 states: within 1/2/3 sigma 0.592/0.966/0.979 (Gaussian: 0.393/0.865/0.989).
