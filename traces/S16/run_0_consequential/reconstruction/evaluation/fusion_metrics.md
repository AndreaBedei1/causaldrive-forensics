# Road-user fusion against ground truth - S16/run_0_consequential

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | C | ASSOCIATED | collision | C | 1.000 | correct link |
| A:track_002 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_003 | C | ASSOCIATED | common_frame | C | 1.000 | correct link |
| B:track_004 | U1 | ANONYMOUS | - | C | 1.000 | missed link (true identity C) |
| C:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |

Counts: correct link: 6, missed link: 1

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | B:track_004 | C | yes | 1.000 |

Merges over pairs of anonymous tracks: correct 0, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U1

## Fused state errors (against the majority identity, 3 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 3 | 3.303 | 3.291 | 3.330 | 0.039 | 3.346 | 3.352 | 3.357 |
| coverage_s | 1 | 0.300 | 0.300 | 0.300 | 0.000 | 0.300 | 0.300 | 0.300 |
| heading_error_deg | 3 | 7.606 | 7.404 | 7.670 | 0.266 | 7.709 | 7.721 | 7.734 |
| length_error_m | 1 | 1.315 | 1.315 | 1.315 | 0.000 | 1.315 | 1.315 | 1.315 |
| normalised_centre_error | 3 | 6.026 | 6.006 | 6.077 | 0.071 | 6.106 | 6.117 | 6.127 |
| single_track_nominal_centre_error_m | 3 | 3.307 | 3.291 | 3.340 | 0.049 | 3.360 | 3.366 | 3.373 |
| speed_error_mps | 3 | 0.361 | 0.197 | 0.400 | 0.204 | 0.424 | 0.432 | 0.440 |
| velocity_error_mps | 3 | 0.916 | 0.776 | 0.959 | 0.183 | 0.985 | 0.994 | 1.002 |
| width_error_m | 1 | 0.088 | 0.088 | 0.088 | 0.000 | 0.088 | 0.088 | 0.088 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 3 | 3.303 | 3.291 | 3.330 | 0.039 | 3.346 | 3.352 | 3.357 |
| heading_error_deg | 3 | 7.606 | 7.404 | 7.670 | 0.266 | 7.709 | 7.721 | 7.734 |
| speed_error_mps | 3 | 0.361 | 0.197 | 0.400 | 0.204 | 0.424 | 0.432 | 0.440 |
| velocity_error_mps | 3 | 0.916 | 0.776 | 0.959 | 0.183 | 0.985 | 0.994 | 1.002 |

Calibration of pos_std_m over 3 states: within 1/2/3 sigma 0.000/0.000/0.000 (Gaussian: 0.393/0.865/0.989).
