# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `c79b1e627cbfaa5c042749291876597e922509f7` (uncommitted changes), code `1c410466c184df92`, configuration `87109d249a009c15`, 2026-10-10T21:47:54Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 22, correct link: 41, missed link: 4

Merges over pairs of anonymous tracks: correct 15, false 0, missed 10. Anonymous entities: 15 (purity median 1.000, min 0.632); entities per true road user: median 1.000, max 2.000.

## Per run

| Run | Decisions | Merges c/f/m | Entities | Of recorders | Fragmentation | Fused centre err. median | Single-track centre err. median |
|-----|-----------|--------------|---------:|-------------:|---------------|-------------------------:|--------------------------------:|
| S01/run_0_crash | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_0_crash | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_0_critical_before_cut_in | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_0_crash | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S06/run_0_a_front_pushed | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S06/run_0_b_rear_first | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S07/run_0_crash | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | C->U1 | 0.278 | 0.214 |
| S08/run_0_crash | 5 correct link, 1 missed link | 0/0/0 | 1 | 1 | B->U1 | 0.337 | 0.897 |
| S09/run_0_merge_conflict | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S10/run_0_rolls_through | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S12/run_0_near_simultaneous | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S15/run_0_deflected_into_c | 5 correct link, 1 missed link | 0/0/0 | 1 | 1 | A->U1 | 1.468 | 1.409 |
| S16/run_0_consequential | 6 correct link, 1 missed link | 0/0/0 | 1 | 1 | C->U1 | 3.303 | 3.307 |
| S17/run_0_crash | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.106 | 0.690 |
| S18/run_0_abreast | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U1/U2, D->U3 | 0.401 | 0.616 |
| S18/run_0_passing | 7 anonymous, 2 correct link | 6/0/3 | 3 | 0 | C->U1/U2, D->U3 | 0.411 | 0.525 |
| S18/run_0_platoon | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.616 | 0.522 |

## Pooled fused-state errors

Against the entity's majority identity, at the 1062 instants every source track was on it; 107 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 1062 | 0.392 | 0.240 | 0.781 | 0.541 | 1.417 | 1.514 | 6.588 |
| coverage_s | 15 | 8.950 | 4.150 | 10.325 | 6.175 | 11.550 | 12.670 | 13.650 |
| heading_error_deg | 878 | 0.534 | 0.253 | 1.046 | 0.793 | 1.798 | 2.799 | 176.769 |
| length_error_m | 15 | 0.192 | 0.139 | 0.192 | 0.053 | 0.328 | 0.688 | 1.315 |
| normalised_centre_error | 1062 | 0.829 | 0.479 | 1.228 | 0.749 | 1.846 | 2.282 | 16.108 |
| single_track_nominal_centre_error_m | 1539 | 0.571 | 0.306 | 1.082 | 0.776 | 3.372 | 3.528 | 5.283 |
| speed_error_mps | 1062 | 0.049 | 0.023 | 0.097 | 0.074 | 0.166 | 0.270 | 4.472 |
| velocity_error_mps | 1062 | 0.119 | 0.064 | 0.233 | 0.169 | 0.400 | 0.685 | 10.357 |
| width_error_m | 15 | 0.263 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 393 | 0.272 | 0.142 | 0.385 | 0.244 | 0.667 | 1.038 | 6.588 |
| heading_error_deg | 375 | 0.591 | 0.288 | 1.068 | 0.780 | 1.678 | 2.454 | 158.576 |
| speed_error_mps | 393 | 0.052 | 0.023 | 0.113 | 0.090 | 0.246 | 0.393 | 4.472 |
| velocity_error_mps | 393 | 0.146 | 0.080 | 0.258 | 0.178 | 0.389 | 1.056 | 10.357 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 669 | 0.567 | 0.297 | 0.972 | 0.675 | 1.487 | 1.558 | 4.036 |
| heading_error_deg | 503 | 0.483 | 0.230 | 1.034 | 0.803 | 1.880 | 3.104 | 176.769 |
| speed_error_mps | 669 | 0.048 | 0.022 | 0.091 | 0.069 | 0.154 | 0.210 | 3.828 |
| velocity_error_mps | 669 | 0.109 | 0.058 | 0.220 | 0.162 | 0.403 | 0.554 | 8.736 |

Calibration of the declared position uncertainty over 1062 states: within 1/2/3 sigma 0.595/0.919/0.968 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S07/run_0_crash | C | False | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
| S08/run_0_crash | C | True | -4.100 | -4.100 | 0.000 | [-4.2, -3.75] |
