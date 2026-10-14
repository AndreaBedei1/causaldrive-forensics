# Road-user fusion against ground truth - S11/run_0_consequential

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | collision | C | 1.000 | correct link |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002#segment_1 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_002#segment_2 | U1 | ANONYMOUS | - | - | 1.000 | anonymous (clutter: no true vehicle) |
| B:track_002#segment_3 | U3 | ANONYMOUS | - | - | 1.000 | anonymous (clutter: no true vehicle) |
| B:track_003 | U2 | ANONYMOUS | - | C | 1.000 | missed link (true identity C) |
| C:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |

Counts: anonymous: 2, correct link: 4, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_002#segment_2 | - | no | 1.000 |
| U2 | B:track_003 | C | yes | 1.000 |
| U3 | B:track_002#segment_3 | - | no | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2

## Fused state errors (against the majority identity, 8 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 8 | 0.504 | 0.432 | 0.722 | 0.290 | 0.906 | 1.014 | 1.122 |
| coverage_s | 1 | 0.750 | 0.750 | 0.750 | 0.000 | 0.750 | 0.750 | 0.750 |
| heading_error_deg | 8 | 3.810 | 1.933 | 4.560 | 2.627 | 4.759 | 4.910 | 5.060 |
| length_error_m | 1 | 1.315 | 1.315 | 1.315 | 0.000 | 1.315 | 1.315 | 1.315 |
| normalised_centre_error | 8 | 0.920 | 0.789 | 1.318 | 0.529 | 1.653 | 1.850 | 2.047 |
| single_track_nominal_centre_error_m | 7 | 0.958 | 0.933 | 0.983 | 0.050 | 0.991 | 0.994 | 0.998 |
| speed_error_mps | 8 | 0.257 | 0.199 | 0.365 | 0.166 | 0.471 | 0.577 | 0.683 |
| velocity_error_mps | 8 | 0.587 | 0.375 | 0.791 | 0.417 | 0.893 | 0.919 | 0.944 |
| width_error_m | 1 | 0.088 | 0.088 | 0.088 | 0.000 | 0.088 | 0.088 | 0.088 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 8 | 0.504 | 0.432 | 0.722 | 0.290 | 0.906 | 1.014 | 1.122 |
| heading_error_deg | 8 | 3.810 | 1.933 | 4.560 | 2.627 | 4.759 | 4.910 | 5.060 |
| speed_error_mps | 8 | 0.257 | 0.199 | 0.365 | 0.166 | 0.471 | 0.577 | 0.683 |
| velocity_error_mps | 8 | 0.587 | 0.375 | 0.791 | 0.417 | 0.893 | 0.919 | 0.944 |

Calibration of pos_std_m over 8 states: within 1/2/3 sigma 0.625/0.875/1.000 (Gaussian: 0.393/0.865/0.989).
