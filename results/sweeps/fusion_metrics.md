# Road-user fusion against ground truth (campaign)

Privileged evaluation: ground truth is read only here, after the reconstruction was written. Provenance: commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, 2026-10-12T12:33:32Z.

## Identity decisions (tracks of aligned recorders)

anonymous: 549, correct link: 405, missed link: 70

Merges over pairs of anonymous tracks: correct 329, false 0, missed 194. Anonymous entities: 356 (purity median 1.000, min 0.500); entities per true road user: median 1.000, max 4.000.

## Per run

| Run | Decisions | Merges c/f/m | Entities | Of recorders | Fragmentation | Fused centre err. median | Single-track centre err. median |
|-----|-----------|--------------|---------:|-------------:|---------------|-------------------------:|--------------------------------:|
| S18/run_0_anonymous_pair_adjacent_000 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.212 | 0.473 |
| S18/run_10_anonymous_pair_adjacent_010 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.313 | 0.464 |
| S18/run_11_anonymous_pair_adjacent_011 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.311 | 0.471 |
| S18/run_12_anonymous_pair_adjacent_012 | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2, D->U1/U3/U4 | 0.345 | 0.512 |
| S18/run_13_anonymous_pair_adjacent_013 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.269 | 0.528 |
| S18/run_14_anonymous_pair_adjacent_014 | 7 anonymous, 2 correct link | 3/0/8 | 4 | 0 | C->U1, D->U2/U3/U4 | 0.383 | 0.398 |
| S18/run_15_anonymous_pair_adjacent_015 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.333 | 0.444 |
| S18/run_16_anonymous_pair_adjacent_016 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U2, D->U1 | 0.376 | 0.472 |
| S18/run_17_anonymous_pair_adjacent_017 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.293 | 0.446 |
| S18/run_18_anonymous_pair_adjacent_018 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.259 | 0.487 |
| S18/run_19_anonymous_pair_adjacent_019 | 8 anonymous, 2 correct link | 16/0/0 | 2 | 0 | C->U1, D->U2 | 0.383 | 0.471 |
| S18/run_1_anonymous_pair_adjacent_001 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.251 | 0.394 |
| S18/run_20_anonymous_pair_adjacent_020 | 8 anonymous, 2 correct link | 7/0/9 | 4 | 0 | C->U2, D->U1/U3/U4 | 0.396 | 0.571 |
| S18/run_21_anonymous_pair_adjacent_021 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.273 | 0.440 |
| S18/run_22_anonymous_pair_adjacent_022 | 6 anonymous, 2 correct link | 6/0/0 | 2 | 0 | C->U1, D->U2 | 0.396 | 0.497 |
| S18/run_23_anonymous_pair_adjacent_023 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.297 | 0.406 |
| S18/run_24_anonymous_pair_adjacent_024 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U2, D->U1 | 0.271 | 0.410 |
| S18/run_25_anonymous_pair_adjacent_025 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.247 | 0.499 |
| S18/run_26_anonymous_pair_adjacent_026 | 6 anonymous, 2 correct link | 4/0/3 | 3 | 0 | C->U1, D->U2/U3 | 0.378 | 0.549 |
| S18/run_27_anonymous_pair_adjacent_027 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.232 | 0.471 |
| S18/run_28_anonymous_pair_adjacent_028 | 8 anonymous, 2 correct link | 4/0/9 | 5 | 0 | C->U2/U3, D->U1/U4/U5 | 0.404 | 0.754 |
| S18/run_29_anonymous_pair_adjacent_029 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U2, D->U1 | 0.284 | 0.412 |
| S18/run_2_anonymous_pair_adjacent_002 | 6 anonymous, 2 correct link | 7/0/0 | 2 | 0 | C->U2, D->U1 | 0.419 | 0.502 |
| S18/run_30_anonymous_pair_adjacent_030 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.314 | 0.422 |
| S18/run_31_anonymous_pair_adjacent_031 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.418 | 0.498 |
| S18/run_32_anonymous_pair_adjacent_032 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.367 | 0.438 |
| S18/run_33_anonymous_pair_adjacent_033 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.231 | 0.370 |
| S18/run_34_anonymous_pair_adjacent_034 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.319 | 0.482 |
| S18/run_35_anonymous_pair_adjacent_035 | 8 anonymous, 2 correct link | 5/0/11 | 4 | 0 | C->U1, D->U2/U3/U4 | 0.377 | 0.565 |
| S18/run_36_anonymous_pair_adjacent_036 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2, D->U1/U3 | 0.281 | 0.420 |
| S18/run_37_anonymous_pair_adjacent_037 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.279 | 0.411 |
| S18/run_38_anonymous_pair_adjacent_038 | 7 anonymous, 2 correct link | 5/0/4 | 3 | 0 | C->U1, D->U2/U3 | 0.388 | 0.478 |
| S18/run_39_anonymous_pair_adjacent_039 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.321 | 0.455 |
| S18/run_3_anonymous_pair_adjacent_003 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U1/U3, D->U2 | 0.442 | 0.694 |
| S18/run_4_anonymous_pair_adjacent_004 | 6 anonymous, 2 correct link | 1/0/6 | 5 | 0 | C->U2/U3, D->U1/U4/U5 | 0.366 | 0.446 |
| S18/run_5_anonymous_pair_adjacent_005 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.268 | 0.407 |
| S18/run_6_anonymous_pair_adjacent_006 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U1, D->U2 | 0.321 | 0.659 |
| S18/run_7_anonymous_pair_adjacent_007 | 6 anonymous, 2 correct link | 7/0/0 | 2 | 0 | C->U1, D->U2 | 0.386 | 0.469 |
| S18/run_8_anonymous_pair_adjacent_008 | 5 anonymous, 2 correct link | 4/0/0 | 2 | 0 | C->U2, D->U1 | 0.296 | 0.514 |
| S18/run_9_anonymous_pair_adjacent_009 | 4 anonymous, 2 correct link | 2/0/0 | 2 | 0 | C->U1, D->U2 | 0.209 | 0.370 |
| S18/run_0_anonymous_pair_platoon_000 | 7 anonymous, 2 correct link | 2/0/7 | 5 | 0 | C->U3/U4/U5, D->U1/U2 | 0.291 | 0.346 |
| S18/run_10_anonymous_pair_platoon_010 | 6 anonymous, 2 correct link | 2/0/5 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.396 | 0.418 |
| S18/run_11_anonymous_pair_platoon_011 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.324 | 0.356 |
| S18/run_12_anonymous_pair_platoon_012 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.468 | 0.511 |
| S18/run_13_anonymous_pair_platoon_013 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.341 | 0.432 |
| S18/run_14_anonymous_pair_platoon_014 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.442 | 0.426 |
| S18/run_15_anonymous_pair_platoon_015 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.510 | 0.461 |
| S18/run_16_anonymous_pair_platoon_016 | 5 anonymous, 2 correct link | 1/0/3 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.465 | 0.575 |
| S18/run_17_anonymous_pair_platoon_017 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.460 | 0.486 |
| S18/run_18_anonymous_pair_platoon_018 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.476 | 0.522 |
| S18/run_19_anonymous_pair_platoon_019 | 7 anonymous, 2 correct link | 2/0/7 | 5 | 0 | C->U3/U4/U5, D->U1/U2 | 0.276 | 0.380 |
| S18/run_1_anonymous_pair_platoon_001 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.284 | 0.345 |
| S18/run_20_anonymous_pair_platoon_020 | 7 anonymous, 2 correct link | 3/0/6 | 5 | 0 | C->U2/U3/U4/U5, D->U1 | 0.647 | 0.597 |
| S18/run_21_anonymous_pair_platoon_021 | 6 anonymous, 2 correct link | 3/0/3 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.418 | 0.477 |
| S18/run_22_anonymous_pair_platoon_022 | 6 anonymous, 2 correct link | 1/0/5 | 5 | 0 | C->U3/U4/U5, D->U1/U2 | 0.764 | 0.835 |
| S18/run_23_anonymous_pair_platoon_023 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.303 | 0.352 |
| S18/run_24_anonymous_pair_platoon_024 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.383 | 0.481 |
| S18/run_25_anonymous_pair_platoon_025 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.314 | 0.362 |
| S18/run_26_anonymous_pair_platoon_026 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.681 | 0.655 |
| S18/run_27_anonymous_pair_platoon_027 | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.359 | 0.515 |
| S18/run_28_anonymous_pair_platoon_028 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.558 | 0.525 |
| S18/run_29_anonymous_pair_platoon_029 | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.479 | 0.560 |
| S18/run_2_anonymous_pair_platoon_002 | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.547 | 0.758 |
| S18/run_30_anonymous_pair_platoon_030 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.432 | 0.445 |
| S18/run_31_anonymous_pair_platoon_031 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.559 | 0.501 |
| S18/run_32_anonymous_pair_platoon_032 | 6 anonymous, 2 correct link | 2/0/4 | 4 | 0 | C->U3/U4, D->U1/U2 | 0.412 | 0.481 |
| S18/run_33_anonymous_pair_platoon_033 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.364 | 0.378 |
| S18/run_34_anonymous_pair_platoon_034 | 5 anonymous, 2 correct link | 1/0/3 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.612 | 0.633 |
| S18/run_35_anonymous_pair_platoon_035 | 6 anonymous, 2 correct link | 2/0/5 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.286 | 0.380 |
| S18/run_36_anonymous_pair_platoon_036 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.349 | 0.425 |
| S18/run_37_anonymous_pair_platoon_037 | 7 anonymous, 2 correct link | 4/0/5 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.383 | 0.495 |
| S18/run_38_anonymous_pair_platoon_038 | 6 anonymous, 2 correct link | 3/0/3 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.813 | 0.548 |
| S18/run_39_anonymous_pair_platoon_039 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.543 | 0.475 |
| S18/run_3_anonymous_pair_platoon_003 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.346 | 0.345 |
| S18/run_4_anonymous_pair_platoon_004 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.425 | 0.570 |
| S18/run_5_anonymous_pair_platoon_005 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.273 | 0.329 |
| S18/run_6_anonymous_pair_platoon_006 | 6 anonymous, 2 correct link | 4/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.498 | 0.475 |
| S18/run_7_anonymous_pair_platoon_007 | 5 anonymous, 2 correct link | 1/0/3 | 4 | 0 | C->U2/U3/U4, D->U1 | 0.906 | 0.817 |
| S18/run_8_anonymous_pair_platoon_008 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.482 | 0.432 |
| S18/run_9_anonymous_pair_platoon_009 | 5 anonymous, 2 correct link | 2/0/2 | 3 | 0 | C->U2/U3, D->U1 | 0.298 | 0.382 |
| S03/run_0_crossing_000 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.623 | 0.793 |
| S03/run_10_crossing_010 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_11_crossing_011 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_12_crossing_012 | 3 missed link | 0/0/1 | 3 | 3 | A->U2/U3, B->U1 | 0.401 | 0.692 |
| S03/run_13_crossing_013 | 2 missed link | 0/0/0 | 2 | 2 | A->U2, B->U1 | 0.540 | 0.904 |
| S03/run_14_crossing_014 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_15_crossing_015 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_16_crossing_016 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_17_crossing_017 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_18_crossing_018 | 2 missed link | 0/0/0 | 2 | 2 | A->U1, B->U2 | 0.379 | 0.592 |
| S03/run_19_crossing_019 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.637 | 0.859 |
| S03/run_1_crossing_001 | 2 missed link | 0/0/0 | 2 | 2 | A->U2, B->U1 | 0.608 | 0.934 |
| S03/run_20_crossing_020 | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | A->U1 | 0.567 | 0.412 |
| S03/run_21_crossing_021 | 2 missed link | 0/0/0 | 2 | 2 | A->U2, B->U1 | 0.659 | 0.907 |
| S03/run_22_crossing_022 | 2 missed link | 0/0/0 | 2 | 2 | A->U1, B->U2 | 0.487 | 0.563 |
| S03/run_23_crossing_023 | 3 missed link | 1/0/0 | 2 | 2 | A->U1, B->U2 | 0.494 | 0.794 |
| S03/run_24_crossing_024 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_25_crossing_025 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_26_crossing_026 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.560 | 0.757 |
| S03/run_27_crossing_027 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_28_crossing_028 | 3 missed link | 1/0/0 | 2 | 2 | A->U1, B->U2 | 0.435 | 0.922 |
| S03/run_29_crossing_029 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.656 | 0.863 |
| S03/run_2_crossing_002 | 3 missed link | 1/0/0 | 2 | 2 | A->U1, B->U2 | 0.508 | 0.714 |
| S03/run_30_crossing_030 | 4 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_31_crossing_031 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_32_crossing_032 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_33_crossing_033 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_34_crossing_034 | 3 missed link | 1/0/0 | 2 | 2 | A->U1, B->U2 | 0.507 | 0.654 |
| S03/run_35_crossing_035 | 3 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_36_crossing_036 | 2 missed link | 0/0/0 | 2 | 2 | A->U1, B->U2 | 0.410 | 0.600 |
| S03/run_37_crossing_037 | 2 missed link | 0/0/0 | 2 | 2 | A->U1, B->U2 | 0.610 | 0.832 |
| S03/run_38_crossing_038 | 2 missed link | 0/0/0 | 2 | 2 | A->U1, B->U2 | 0.471 | 0.563 |
| S03/run_39_crossing_039 | 4 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_3_crossing_003 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_4_crossing_004 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_5_crossing_005 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.646 | 0.912 |
| S03/run_6_crossing_006 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S03/run_7_crossing_007 | 3 missed link | 1/0/0 | 2 | 2 | A->U1, B->U2 | 0.520 | 0.683 |
| S03/run_8_crossing_008 | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | A->U1 | 0.290 | 0.423 |
| S03/run_9_crossing_009 | 3 missed link | 1/0/0 | 2 | 2 | A->U2, B->U1 | 0.604 | 0.843 |
| S02/run_0_cut_in_000 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_10_cut_in_010 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_11_cut_in_011 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_12_cut_in_012 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_13_cut_in_013 | 3 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_14_cut_in_014 | 1 anonymous, 3 correct link, 1 missed link | 0/0/0 | 2 | 1 | B->U1 | 0.670 | 0.609 |
| S02/run_15_cut_in_015 | 2 anonymous, 3 correct link, 1 missed link | 0/0/0 | 3 | 1 | B->U1 | 0.807 | 0.637 |
| S02/run_16_cut_in_016 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_17_cut_in_017 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_18_cut_in_018 | 1 anonymous, 3 correct link, 1 missed link | 0/0/0 | 2 | 1 | B->U1 | 0.597 | 0.483 |
| S02/run_19_cut_in_019 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_1_cut_in_001 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_20_cut_in_020 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_21_cut_in_021 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_22_cut_in_022 | 2 anonymous, 3 correct link, 1 missed link | 0/0/0 | 3 | 1 | B->U1 | 0.536 | 0.739 |
| S02/run_23_cut_in_023 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_24_cut_in_024 | 2 correct link, 2 missed link | 0/0/1 | 2 | 2 | B->U1/U2 | 1.563 | 1.191 |
| S02/run_25_cut_in_025 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_26_cut_in_026 | 1 anonymous, 1 correct link, 1 missed link | 0/0/0 | 2 | 1 | A->U2 | 2.817 | 2.034 |
| S02/run_27_cut_in_027 | 3 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_28_cut_in_028 | 3 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_29_cut_in_029 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_2_cut_in_002 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_30_cut_in_030 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_31_cut_in_031 | 1 anonymous, 2 correct link, 1 missed link | 0/0/0 | 2 | 1 | B->U1 | 0.409 | 0.427 |
| S02/run_32_cut_in_032 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_33_cut_in_033 | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | B->U1 | 0.285 | 0.594 |
| S02/run_34_cut_in_034 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_35_cut_in_035 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_36_cut_in_036 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_37_cut_in_037 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_38_cut_in_038 | 2 anonymous, 2 correct link, 1 missed link | 0/0/0 | 3 | 1 | B->U1 | 0.506 | 0.699 |
| S02/run_39_cut_in_039 | 2 anonymous, 1 correct link, 2 missed link | 0/0/0 | 4 | 2 | A->U4, B->U1 | 0.906 | 1.505 |
| S02/run_3_cut_in_003 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_4_cut_in_004 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_5_cut_in_005 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_6_cut_in_006 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_7_cut_in_007 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_8_cut_in_008 | 3 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S02/run_9_cut_in_009 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_0_rear_end_000 | 2 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_10_rear_end_010 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_11_rear_end_011 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_12_rear_end_012 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_13_rear_end_013 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_14_rear_end_014 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_15_rear_end_015 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_16_rear_end_016 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_17_rear_end_017 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_18_rear_end_018 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_19_rear_end_019 | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | B->U1 | 0.616 | 0.586 |
| S01/run_1_rear_end_001 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_20_rear_end_020 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_21_rear_end_021 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_22_rear_end_022 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_23_rear_end_023 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_24_rear_end_024 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_25_rear_end_025 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_26_rear_end_026 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_27_rear_end_027 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_28_rear_end_028 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_29_rear_end_029 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_2_rear_end_002 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_30_rear_end_030 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_31_rear_end_031 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_32_rear_end_032 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_33_rear_end_033 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_34_rear_end_034 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_35_rear_end_035 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_36_rear_end_036 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_37_rear_end_037 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_38_rear_end_038 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_39_rear_end_039 | 1 correct link, 1 missed link | 0/0/0 | 1 | 1 | B->U1 | 0.463 | 0.468 |
| S01/run_3_rear_end_003 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_4_rear_end_004 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_5_rear_end_005 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_6_rear_end_006 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_7_rear_end_007 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_8_rear_end_008 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S01/run_9_rear_end_009 | 1 correct link | 0/0/0 | 0 | 0 | - | - | - |
| S17/run_0_unobserved_cut_in_000 | 4 anonymous, 2 correct link | 3/0/3 | 2 | 0 | C->U1/U2 | 0.136 | 0.557 |
| S17/run_10_unobserved_cut_in_010 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.093 | 0.246 |
| S17/run_11_unobserved_cut_in_011 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.135 | 1.400 |
| S17/run_12_unobserved_cut_in_012 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.169 | 0.296 |
| S17/run_13_unobserved_cut_in_013 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.092 | 0.293 |
| S17/run_14_unobserved_cut_in_014 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.122 | 0.705 |
| S17/run_15_unobserved_cut_in_015 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.129 | 0.488 |
| S17/run_16_unobserved_cut_in_016 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.085 | 0.247 |
| S17/run_17_unobserved_cut_in_017 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.134 | 1.030 |
| S17/run_18_unobserved_cut_in_018 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.159 | 0.296 |
| S17/run_19_unobserved_cut_in_019 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.131 | 0.527 |
| S17/run_1_unobserved_cut_in_001 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.089 | 0.651 |
| S17/run_20_unobserved_cut_in_020 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.144 | 0.368 |
| S17/run_21_unobserved_cut_in_021 | 3 anonymous, 2 correct link | 1/0/2 | 2 | 0 | C->U1/U2 | 0.113 | 0.615 |
| S17/run_22_unobserved_cut_in_022 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.091 | 0.259 |
| S17/run_23_unobserved_cut_in_023 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.117 | 0.534 |
| S17/run_24_unobserved_cut_in_024 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.100 | 0.340 |
| S17/run_25_unobserved_cut_in_025 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.087 | 0.339 |
| S17/run_26_unobserved_cut_in_026 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.098 | 0.435 |
| S17/run_27_unobserved_cut_in_027 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.122 | 0.932 |
| S17/run_28_unobserved_cut_in_028 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.073 | 0.286 |
| S17/run_29_unobserved_cut_in_029 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.114 | 0.559 |
| S17/run_2_unobserved_cut_in_002 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.101 | 1.020 |
| S17/run_30_unobserved_cut_in_030 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.147 | 0.552 |
| S17/run_31_unobserved_cut_in_031 | 4 anonymous, 2 correct link | 1/0/0 | 3 | 0 | C->U1 | 0.158 | 0.571 |
| S17/run_32_unobserved_cut_in_032 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.104 | 0.905 |
| S17/run_33_unobserved_cut_in_033 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.137 | 0.557 |
| S17/run_34_unobserved_cut_in_034 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.113 | 0.529 |
| S17/run_35_unobserved_cut_in_035 | 3 anonymous, 1 correct link, 1 missed link | 1/0/2 | 3 | 1 | B->U2, C->U1/U3 | 0.373 | 0.847 |
| S17/run_36_unobserved_cut_in_036 | 3 anonymous, 2 correct link | 1/0/2 | 2 | 0 | C->U1/U2 | 0.106 | 0.689 |
| S17/run_37_unobserved_cut_in_037 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.103 | 0.329 |
| S17/run_38_unobserved_cut_in_038 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.123 | 0.545 |
| S17/run_39_unobserved_cut_in_039 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.089 | 1.296 |
| S17/run_3_unobserved_cut_in_003 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.141 | 0.619 |
| S17/run_4_unobserved_cut_in_004 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.088 | 0.275 |
| S17/run_5_unobserved_cut_in_005 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.114 | 1.008 |
| S17/run_6_unobserved_cut_in_006 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.117 | 0.291 |
| S17/run_7_unobserved_cut_in_007 | 3 anonymous, 2 correct link | 3/0/0 | 1 | 0 | C->U1 | 0.108 | 0.587 |
| S17/run_8_unobserved_cut_in_008 | 3 anonymous, 1 correct link, 1 missed link | 1/0/2 | 3 | 1 | B->U2, C->U1/U3 | 0.248 | 0.601 |
| S17/run_9_unobserved_cut_in_009 | 2 anonymous, 2 correct link | 1/0/0 | 1 | 0 | C->U1 | 0.119 | 0.824 |

## Pooled fused-state errors

Against the entity's majority identity, at the 22874 instants every source track was on it; 102 impure instants (a source track on another body: an association error) are excluded.

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 22874 | 0.317 | 0.174 | 0.640 | 0.465 | 0.978 | 1.267 | 4.148 |
| coverage_s | 342 | 4.825 | 3.900 | 10.650 | 6.750 | 11.595 | 11.950 | 13.250 |
| heading_error_deg | 22871 | 0.595 | 0.260 | 1.217 | 0.957 | 2.502 | 4.450 | 83.087 |
| length_error_m | 342 | 0.192 | 0.086 | 0.192 | 0.106 | 0.343 | 0.419 | 0.605 |
| normalised_centre_error | 22874 | 0.719 | 0.420 | 1.241 | 0.821 | 1.732 | 2.067 | 8.048 |
| single_track_nominal_centre_error_m | 22751 | 0.480 | 0.323 | 0.741 | 0.418 | 1.124 | 1.394 | 4.660 |
| speed_error_mps | 22874 | 0.056 | 0.024 | 0.129 | 0.105 | 0.300 | 0.623 | 12.617 |
| velocity_error_mps | 22874 | 0.158 | 0.080 | 0.313 | 0.233 | 0.715 | 1.229 | 12.873 |
| width_error_m | 342 | 0.263 | 0.107 | 0.263 | 0.156 | 0.263 | 0.263 | 0.263 |

### Method: box_fit

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 14372 | 0.215 | 0.128 | 0.332 | 0.204 | 0.547 | 0.688 | 3.147 |
| heading_error_deg | 14372 | 0.524 | 0.230 | 1.063 | 0.833 | 1.996 | 3.508 | 26.711 |
| speed_error_mps | 14372 | 0.045 | 0.020 | 0.106 | 0.086 | 0.248 | 0.461 | 11.588 |
| velocity_error_mps | 14372 | 0.129 | 0.066 | 0.249 | 0.183 | 0.516 | 0.871 | 11.658 |

### Method: covariance_intersection

| Quantity | n | median | q25 | q75 | IQR | p90 | p95 | max |
|----------|--:|-------:|----:|----:|----:|----:|----:|----:|
| centre_error_m | 8502 | 0.700 | 0.460 | 0.959 | 0.500 | 1.353 | 2.015 | 4.148 |
| heading_error_deg | 8499 | 0.739 | 0.330 | 1.583 | 1.253 | 3.435 | 5.729 | 83.087 |
| speed_error_mps | 8502 | 0.082 | 0.034 | 0.163 | 0.129 | 0.429 | 1.326 | 12.617 |
| velocity_error_mps | 8502 | 0.222 | 0.123 | 0.458 | 0.335 | 1.038 | 1.845 | 12.873 |

Calibration of the declared position uncertainty over 22874 states: within 1/2/3 sigma 0.658/0.943/0.988 (a Gaussian would give 0.393/0.865/0.989).

## Observed-trajectory alignment

| Run | Recorder | Accepted | Estimated | True | Error | Interval |
|-----|----------|----------|----------:|-----:|------:|----------|
| S03/run_0_crossing_000 | B | True | 0.050 | -0.000 | 0.050 | [-0.15, 0.1] |
| S03/run_12_crossing_012 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S03/run_13_crossing_013 | B | True | 0.050 | -0.000 | 0.050 | [-0.15, 0.1] |
| S03/run_18_crossing_018 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S03/run_19_crossing_019 | B | True | 0.050 | -0.000 | 0.050 | [-0.2, 0.1] |
| S03/run_1_crossing_001 | B | True | 0.050 | -0.000 | 0.050 | [-0.2, 0.1] |
| S03/run_20_crossing_020 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.15] |
| S03/run_21_crossing_021 | B | True | 0.050 | -0.000 | 0.050 | [-0.2, 0.1] |
| S03/run_22_crossing_022 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.15] |
| S03/run_23_crossing_023 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S03/run_26_crossing_026 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.15] |
| S03/run_28_crossing_028 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.15] |
| S03/run_29_crossing_029 | B | True | 0.050 | -0.000 | 0.050 | [-0.15, 0.15] |
| S03/run_2_crossing_002 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S03/run_34_crossing_034 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.2] |
| S03/run_36_crossing_036 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.15] |
| S03/run_37_crossing_037 | B | True | 0.050 | -0.000 | 0.050 | [-0.2, 0.1] |
| S03/run_38_crossing_038 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.1] |
| S03/run_5_crossing_005 | B | True | 0.050 | -0.000 | 0.050 | [-0.15, 0.15] |
| S03/run_7_crossing_007 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.15] |
| S03/run_8_crossing_008 | B | True | 0.000 | -0.000 | 0.000 | [-0.15, 0.1] |
| S03/run_9_crossing_009 | B | True | 0.050 | -0.000 | 0.050 | [-0.15, 0.15] |
| S02/run_0_cut_in_000 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_11_cut_in_011 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S02/run_13_cut_in_013 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_14_cut_in_014 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_15_cut_in_015 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_18_cut_in_018 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_20_cut_in_020 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_22_cut_in_022 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_23_cut_in_023 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_27_cut_in_027 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_28_cut_in_028 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_29_cut_in_029 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_2_cut_in_002 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_30_cut_in_030 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_31_cut_in_031 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_34_cut_in_034 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_35_cut_in_035 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_36_cut_in_036 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_38_cut_in_038 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S02/run_3_cut_in_003 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_7_cut_in_007 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.05] |
| S02/run_8_cut_in_008 | B | True | -0.050 | -0.000 | -0.050 | [-0.15, 0.1] |
| S02/run_9_cut_in_009 | B | True | -0.050 | -0.000 | -0.050 | [-0.2, 0.1] |
| S01/run_10_rear_end_010 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_11_rear_end_011 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.05] |
| S01/run_12_rear_end_012 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_13_rear_end_013 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_15_rear_end_015 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_16_rear_end_016 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.0] |
| S01/run_17_rear_end_017 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.05] |
| S01/run_18_rear_end_018 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_19_rear_end_019 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_1_rear_end_001 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_20_rear_end_020 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_21_rear_end_021 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_22_rear_end_022 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S01/run_23_rear_end_023 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.05] |
| S01/run_24_rear_end_024 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_26_rear_end_026 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S01/run_27_rear_end_027 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_28_rear_end_028 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_2_rear_end_002 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S01/run_30_rear_end_030 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S01/run_31_rear_end_031 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_32_rear_end_032 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_33_rear_end_033 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_35_rear_end_035 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.05] |
| S01/run_36_rear_end_036 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_37_rear_end_037 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_38_rear_end_038 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S01/run_3_rear_end_003 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_4_rear_end_004 | B | True | -0.050 | -0.000 | -0.050 | [-0.05, 0.0] |
| S01/run_5_rear_end_005 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.0] |
| S01/run_6_rear_end_006 | B | True | -0.050 | -0.000 | -0.050 | [-0.1, 0.05] |
| S01/run_7_rear_end_007 | B | True | 0.000 | -0.000 | 0.000 | [-0.05, 0.05] |
| S17/run_10_unobserved_cut_in_010 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.15] |
| S17/run_11_unobserved_cut_in_011 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_13_unobserved_cut_in_013 | B | True | 0.000 | -0.000 | 0.000 | [-0.25, 0.25] |
| S17/run_16_unobserved_cut_in_016 | B | True | 0.000 | -0.000 | 0.000 | [-0.2, 0.05] |
| S17/run_17_unobserved_cut_in_017 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_22_unobserved_cut_in_022 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.1] |
| S17/run_23_unobserved_cut_in_023 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_25_unobserved_cut_in_025 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.2] |
| S17/run_27_unobserved_cut_in_027 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.1] |
| S17/run_28_unobserved_cut_in_028 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.1] |
| S17/run_29_unobserved_cut_in_029 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_30_unobserved_cut_in_030 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_34_unobserved_cut_in_034 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.2] |
| S17/run_35_unobserved_cut_in_035 | B | True | 0.000 | -0.000 | 0.000 | [-0.1, 0.05] |
| S17/run_39_unobserved_cut_in_039 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.1] |
| S17/run_3_unobserved_cut_in_003 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_4_unobserved_cut_in_004 | B | True | 0.000 | -0.000 | 0.000 | [-0.3, 0.2] |
| S17/run_8_unobserved_cut_in_008 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
| S17/run_9_unobserved_cut_in_009 | B | True | 0.000 | -0.000 | 0.000 | [-0.35, 0.05] |
