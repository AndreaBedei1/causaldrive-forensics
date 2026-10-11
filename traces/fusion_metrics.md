# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, 2026-10-11T03:24:28Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 22, correct link: 42, missed link: 3

Merges over pairs of anonymous tracks: correct 15, false 0, missed 10. Anonymous entities: 14 (purity median 1.000, min 0.632); entities per true road user: median 1.000, max 2.000.

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

Against the entity's majority identity, at the 925 instants every source track was on it; 107 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 925 | 0.447 | 0.236 | 0.846 | 0.609 | 1.456 | 1.525 | 6.588 |
| coverage_s | 14 | 8.950 | 3.925 | 10.200 | 6.275 | 10.485 | 11.113 | 12.250 |
| heading_error_deg | 835 | 0.572 | 0.287 | 1.068 | 0.780 | 1.830 | 3.053 | 176.769 |
| length_error_m | 14 | 0.192 | 0.113 | 0.192 | 0.080 | 0.351 | 0.733 | 1.315 |
| normalised_centre_error | 925 | 0.925 | 0.506 | 1.303 | 0.797 | 1.953 | 2.591 | 16.108 |
| single_track_nominal_centre_error_m | 1402 | 0.618 | 0.337 | 1.216 | 0.880 | 3.434 | 3.535 | 5.283 |
| speed_error_mps | 925 | 0.051 | 0.022 | 0.103 | 0.081 | 0.182 | 0.281 | 4.472 |
| velocity_error_mps | 925 | 0.142 | 0.078 | 0.250 | 0.172 | 0.430 | 0.826 | 10.357 |
| width_error_m | 14 | 0.263 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 390 | 0.271 | 0.142 | 0.380 | 0.238 | 0.665 | 1.007 | 6.588 |
| heading_error_deg | 374 | 0.599 | 0.289 | 1.069 | 0.779 | 1.680 | 2.460 | 158.576 |
| speed_error_mps | 390 | 0.052 | 0.023 | 0.113 | 0.090 | 0.248 | 0.402 | 4.472 |
| velocity_error_mps | 390 | 0.147 | 0.081 | 0.258 | 0.177 | 0.390 | 1.077 | 10.357 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 535 | 0.675 | 0.417 | 1.135 | 0.718 | 1.505 | 2.118 | 4.036 |
| heading_error_deg | 461 | 0.551 | 0.281 | 1.065 | 0.784 | 2.013 | 3.253 | 176.769 |
| speed_error_mps | 535 | 0.050 | 0.021 | 0.097 | 0.076 | 0.165 | 0.244 | 3.828 |
| velocity_error_mps | 535 | 0.136 | 0.075 | 0.241 | 0.167 | 0.441 | 0.790 | 8.736 |

Calibration of the declared position uncertainty over 925 states: within 1/2/3 sigma 0.547/0.908/0.963 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S07/run_0_crash | C | True | -5.950 | -5.900 | -0.050 | [-5.95, -5.9] |
| S08/run_0_crash | C | True | -4.100 | -4.100 | 0.000 | [-4.2, -4.0] |
