# Road-user fusion against ground truth - S13/run_0_abreast

Privileged evaluation (ground truth used here only). Assumptions: recorder raw clocks are CARLA simulator time; a vehicle box is centred on its origin in the horizontal plane.

## Track identity decisions (aligned recorders)

| Track | Decision | Status | By | True identity | Purity | Verdict |
|-------|----------|--------|----|---------------|-------:|---------|
| A:track_001 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| A:track_002 | B | ASSOCIATED | collision | B | 1.000 | correct link |
| A:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |
| B:track_001 | A | ASSOCIATED | collision | A | 1.000 | correct link |
| B:track_002 | U1 | ANONYMOUS | - | D | 1.000 | anonymous (non-recording road user D) |
| B:track_003 | U2 | ANONYMOUS | - | C | 1.000 | anonymous (non-recording road user C) |

Counts: anonymous: 4, correct link: 2

## Anonymous entities

| Entity | Source tracks | True identity | Recorder? | Purity |
|--------|---------------|---------------|-----------|-------:|
| U1 | A:track_001, B:track_002 | D | no | 1.000 |
| U2 | B:track_003, A:track_003 | C | no | 1.000 |

Merges over pairs of anonymous tracks: correct 2, false 0, missed 0.
Fragmentation (true road user -> entities): C -> U2, D -> U1

## Fused state errors (against the majority identity, 208 pure states; 0 impure states where a source track was on another body, excluded)

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 208 | 0.273 | 0.231 | 0.377 | 0.146 | 0.576 | 0.660 | 0.736 |
| coverage_s | 2 | 10.325 | 10.262 | 10.387 | 0.125 | 10.425 | 10.438 | 10.450 |
| heading_error_deg | 208 | 0.355 | 0.127 | 0.688 | 0.560 | 1.103 | 1.702 | 3.783 |
| length_error_m | 2 | 0.139 | 0.113 | 0.166 | 0.053 | 0.181 | 0.187 | 0.192 |
| normalised_centre_error | 208 | 3.182 | 2.563 | 3.743 | 1.180 | 4.196 | 5.093 | 5.601 |
| single_track_nominal_centre_error_m | 208 | 0.445 | 0.317 | 0.595 | 0.278 | 0.680 | 0.745 | 0.868 |
| speed_error_mps | 208 | 0.040 | 0.019 | 0.094 | 0.074 | 0.168 | 0.219 | 0.322 |
| velocity_error_mps | 208 | 0.108 | 0.056 | 0.174 | 0.117 | 0.309 | 0.431 | 1.053 |
| width_error_m | 2 | 0.185 | 0.146 | 0.224 | 0.078 | 0.247 | 0.255 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 154 | 0.259 | 0.214 | 0.294 | 0.080 | 0.369 | 0.399 | 0.600 |
| heading_error_deg | 154 | 0.339 | 0.101 | 0.644 | 0.543 | 0.981 | 1.093 | 2.571 |
| speed_error_mps | 154 | 0.032 | 0.018 | 0.067 | 0.050 | 0.159 | 0.200 | 0.322 |
| velocity_error_mps | 154 | 0.077 | 0.043 | 0.149 | 0.107 | 0.224 | 0.284 | 0.508 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 54 | 0.524 | 0.377 | 0.607 | 0.231 | 0.710 | 0.727 | 0.736 |
| heading_error_deg | 54 | 0.441 | 0.238 | 1.174 | 0.936 | 2.292 | 2.559 | 3.783 |
| speed_error_mps | 54 | 0.076 | 0.028 | 0.122 | 0.093 | 0.206 | 0.231 | 0.261 |
| velocity_error_mps | 54 | 0.176 | 0.116 | 0.307 | 0.191 | 0.490 | 0.647 | 1.053 |

Calibration of pos_std_m over 208 states: within 1/2/3 sigma 0.000/0.077/0.389 (Gaussian: 0.393/0.865/0.989).
