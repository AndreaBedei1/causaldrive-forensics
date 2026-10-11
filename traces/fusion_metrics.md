# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `fd8d2baed644db4a32c2eb502a2eeb9b32f70887` (uncommitted changes), code `c76d72a3965907b6`, configuration `50f7dc9e35556156`, 2026-10-11T09:29:44Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 26, correct link: 44, missed link: 7

Merges over pairs of anonymous tracks: correct 23, false 0, missed 16. Anonymous entities: 19 (purity median 1.000, min 0.609); entities per true road user: median 1.500, max 3.000.

## Per run

| Run | Decisions | Merges c/f/m | Entities | Of recorders | Fragmentation | Fused centre err. median | Single-track centre err. median |
|-----|-----------|--------------|---------:|-------------:|---------------|-------------------------:|--------------------------------:|
| S01/run_0_crash | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_0_crash | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_0_critical_before_cut_in | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_0_crash | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S06/run_0_a_front_pushed | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S06/run_0_b_rear_first | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S07/run_0_crash | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S08/run_0_crash | 5 correct link, 3 missed link | 0/0/1 | 3 | 3 | A->U3, B->U1/U2 | 1.122 | 1.345 |
| S09/run_0_merge_conflict | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S10/run_0_rolls_through | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S12/run_0_near_simultaneous | 3 correct link, 1 missed link | 0/0/0 | 1 | 1 | A->U1 | 0.827 | 0.964 |
| S15/run_0_deflected_into_c | 6 correct link, 2 missed link | 0/0/1 | 2 | 2 | A->U1/U2 | 0.983 | 1.921 |
| S16/run_0_consequential | 6 correct link, 1 missed link | 0/0/0 | 1 | 1 | C->U1 | 3.303 | 3.307 |
| S17/run_0_crash | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.106 | 0.690 |
| S18/run_0_abreast | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2, D->U1/U3/U4 | 0.402 | 0.605 |
| S18/run_0_passing | 9 anonymous, 2 correct link | 12/0/4 | 3 | 0 | C->U2, D->U1/U3 | 0.378 | 0.492 |
| S18/run_0_platoon | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.616 | 0.522 |

## Pooled fused-state errors

Against the entity's majority identity, at the 958 instants every source track was on it; 49 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 958 | 0.530 | 0.267 | 0.983 | 0.716 | 1.176 | 1.429 | 3.777 |
| coverage_s | 19 | 3.700 | 1.375 | 9.875 | 8.500 | 10.250 | 10.455 | 10.500 |
| heading_error_deg | 766 | 0.589 | 0.291 | 1.181 | 0.890 | 2.407 | 4.597 | 164.969 |
| length_error_m | 19 | 0.192 | 0.086 | 0.192 | 0.106 | 0.419 | 0.509 | 1.315 |
| normalised_centre_error | 958 | 0.838 | 0.462 | 1.332 | 0.870 | 1.999 | 2.735 | 6.893 |
| single_track_nominal_centre_error_m | 1557 | 0.637 | 0.348 | 1.353 | 1.005 | 3.311 | 3.526 | 3.674 |
| speed_error_mps | 958 | 0.062 | 0.022 | 0.127 | 0.105 | 0.253 | 0.457 | 4.472 |
| velocity_error_mps | 958 | 0.140 | 0.073 | 0.268 | 0.195 | 0.545 | 1.190 | 8.197 |
| width_error_m | 19 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 477 | 0.286 | 0.171 | 0.425 | 0.255 | 0.721 | 0.920 | 2.305 |
| heading_error_deg | 460 | 0.563 | 0.281 | 1.058 | 0.776 | 1.791 | 3.599 | 89.859 |
| speed_error_mps | 477 | 0.058 | 0.025 | 0.113 | 0.088 | 0.232 | 0.378 | 4.472 |
| velocity_error_mps | 477 | 0.138 | 0.081 | 0.253 | 0.172 | 0.447 | 1.070 | 8.197 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 481 | 0.973 | 0.639 | 1.109 | 0.469 | 1.250 | 2.447 | 3.777 |
| heading_error_deg | 306 | 0.667 | 0.310 | 1.450 | 1.139 | 3.299 | 6.505 | 164.969 |
| speed_error_mps | 481 | 0.069 | 0.015 | 0.141 | 0.127 | 0.264 | 0.494 | 3.510 |
| velocity_error_mps | 481 | 0.146 | 0.060 | 0.291 | 0.231 | 0.637 | 1.336 | 7.825 |

Calibration of the declared position uncertainty over 958 states: within 1/2/3 sigma 0.636/0.900/0.955 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S07/run_0_crash | C | True | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
| S08/run_0_crash | C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
