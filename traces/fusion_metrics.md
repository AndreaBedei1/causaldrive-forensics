# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `a095b4c3b8cc2e3d1fb0dd0abcdb53b3e859aa8e` (uncommitted changes), code `1667dea2979183ef`, configuration `0b5c899acef9146c`, 2026-10-11T13:06:17Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 23, correct link: 45, missed link: 2

Merges over pairs of anonymous tracks: correct 17, false 0, missed 10. Anonymous entities: 13 (purity median 1.000, min 0.795); entities per true road user: median 1.000, max 3.000.

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
| S08/run_0_crash | 6 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S09/run_0_merge_conflict | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S10/run_0_rolls_through | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S12/run_0_near_simultaneous | 3 correct link, 1 missed link | 0/0/0 | 1 | 1 | A->U1 | 0.827 | 0.964 |
| S15/run_0_deflected_into_c | 6 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S16/run_0_consequential | 6 correct link, 1 missed link | 0/0/0 | 1 | 1 | C->U1 | 3.303 | 3.307 |
| S17/run_0_crash | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.106 | 0.690 |
| S18/run_0_abreast | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2, D->U1/U3/U4 | 0.402 | 0.633 |
| S18/run_0_passing | 6 anonymous, 2 correct link | 6/0/0 | 2 | 0 | C->U2, D->U1 | 0.303 | 0.469 |
| S18/run_0_platoon | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.623 | 0.647 |

## Pooled fused-state errors

Against the entity's majority identity, at the 733 instants every source track was on it; 12 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 733 | 0.356 | 0.220 | 0.734 | 0.514 | 1.045 | 1.239 | 3.542 |
| coverage_s | 13 | 4.600 | 1.400 | 10.200 | 8.800 | 10.400 | 10.470 | 10.500 |
| heading_error_deg | 729 | 0.561 | 0.259 | 1.092 | 0.833 | 1.954 | 3.204 | 65.386 |
| length_error_m | 13 | 0.192 | 0.086 | 0.192 | 0.106 | 0.192 | 0.641 | 1.315 |
| normalised_centre_error | 733 | 0.842 | 0.527 | 1.415 | 0.888 | 1.989 | 2.247 | 6.464 |
| single_track_nominal_centre_error_m | 1462 | 0.578 | 0.329 | 1.363 | 1.035 | 2.399 | 2.831 | 3.563 |
| speed_error_mps | 733 | 0.052 | 0.020 | 0.099 | 0.079 | 0.165 | 0.260 | 3.666 |
| velocity_error_mps | 733 | 0.145 | 0.077 | 0.257 | 0.180 | 0.442 | 0.747 | 3.666 |
| width_error_m | 13 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 461 | 0.267 | 0.170 | 0.370 | 0.200 | 0.644 | 0.822 | 1.903 |
| heading_error_deg | 457 | 0.513 | 0.254 | 0.979 | 0.725 | 1.455 | 2.236 | 65.386 |
| speed_error_mps | 461 | 0.044 | 0.018 | 0.083 | 0.066 | 0.137 | 0.246 | 3.666 |
| velocity_error_mps | 461 | 0.120 | 0.066 | 0.226 | 0.160 | 0.324 | 0.466 | 3.666 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 272 | 0.772 | 0.513 | 0.989 | 0.476 | 1.249 | 3.471 | 3.542 |
| heading_error_deg | 272 | 0.625 | 0.283 | 1.367 | 1.084 | 2.578 | 4.489 | 32.354 |
| speed_error_mps | 272 | 0.067 | 0.030 | 0.122 | 0.092 | 0.205 | 0.293 | 3.510 |
| velocity_error_mps | 272 | 0.194 | 0.100 | 0.341 | 0.241 | 0.619 | 0.981 | 3.625 |

Calibration of the declared position uncertainty over 733 states: within 1/2/3 sigma 0.602/0.902/0.961 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S07/run_0_crash | C | True | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
| S08/run_0_crash | C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
