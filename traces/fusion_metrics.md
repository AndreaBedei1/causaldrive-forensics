# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, 2026-10-12T12:32:30Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 23, correct link: 46, missed link: 1

Merges over pairs of anonymous tracks: correct 17, false 0, missed 10. Anonymous entities: 12 (purity median 1.000, min 0.795); entities per true road user: median 1.000, max 3.000.

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
| S12/run_0_near_simultaneous | 4 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S15/run_0_deflected_into_c | 6 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S16/run_0_consequential | 6 correct link, 1 missed link | 0/0/0 | 1 | 1 | C->U1 | 3.303 | 3.307 |
| S17/run_0_crash | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.106 | 1.032 |
| S18/run_0_abreast | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2, D->U1/U3/U4 | 0.402 | 0.724 |
| S18/run_0_passing | 6 anonymous, 2 correct link | 6/0/0 | 2 | 0 | C->U2, D->U1 | 0.303 | 0.474 |
| S18/run_0_platoon | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.623 | 0.679 |

## Pooled fused-state errors

Against the entity's majority identity, at the 721 instants every source track was on it; 12 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 721 | 0.348 | 0.219 | 0.719 | 0.500 | 1.051 | 1.237 | 3.542 |
| coverage_s | 12 | 6.025 | 3.125 | 10.200 | 7.075 | 10.425 | 10.473 | 10.500 |
| heading_error_deg | 721 | 0.551 | 0.258 | 1.066 | 0.808 | 1.864 | 2.736 | 16.274 |
| length_error_m | 12 | 0.139 | 0.086 | 0.192 | 0.106 | 0.192 | 0.697 | 1.315 |
| normalised_centre_error | 721 | 0.838 | 0.520 | 1.407 | 0.887 | 1.962 | 2.252 | 6.464 |
| single_track_nominal_centre_error_m | 720 | 0.613 | 0.404 | 0.916 | 0.512 | 1.383 | 1.556 | 3.563 |
| speed_error_mps | 721 | 0.051 | 0.019 | 0.097 | 0.078 | 0.159 | 0.243 | 0.974 |
| velocity_error_mps | 721 | 0.143 | 0.076 | 0.253 | 0.177 | 0.426 | 0.639 | 3.558 |
| width_error_m | 12 | 0.107 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 451 | 0.263 | 0.167 | 0.364 | 0.197 | 0.594 | 0.763 | 1.903 |
| heading_error_deg | 451 | 0.511 | 0.253 | 0.961 | 0.708 | 1.423 | 1.897 | 14.764 |
| speed_error_mps | 451 | 0.043 | 0.017 | 0.082 | 0.065 | 0.134 | 0.176 | 0.974 |
| velocity_error_mps | 451 | 0.118 | 0.066 | 0.222 | 0.157 | 0.313 | 0.405 | 3.260 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 270 | 0.770 | 0.511 | 0.986 | 0.475 | 1.243 | 3.471 | 3.542 |
| heading_error_deg | 270 | 0.622 | 0.280 | 1.326 | 1.046 | 2.507 | 3.944 | 16.274 |
| speed_error_mps | 270 | 0.066 | 0.030 | 0.118 | 0.089 | 0.196 | 0.275 | 0.958 |
| velocity_error_mps | 270 | 0.193 | 0.100 | 0.338 | 0.238 | 0.547 | 0.934 | 3.558 |

Calibration of the declared position uncertainty over 721 states: within 1/2/3 sigma 0.609/0.908/0.960 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S07/run_0_crash | C | True | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
| S08/run_0_crash | C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
