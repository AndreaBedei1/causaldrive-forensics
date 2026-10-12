**T6_sensitivity_sweeps.**  One-at-a-time sensitivity of the core events to their thresholds before the first contact (240 runs, sweeps).

| setting | CTTC start: recall / precision | CTTC start: oracle events | path entry: recall / precision | path entry: oracle events | cut-in R: recall / precision | cut-in R: oracle events |
|---|---|---|---|---|---|---|
| nominal | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_reaction_time_s = 0.7 | 0.96 / 0.94 | 522/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_reaction_time_s = 1.5 | 0.94 / 0.95 | 571/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_deceleration_mps2 = 5.0 | 0.94 / 0.94 | 554/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_deceleration_mps2 = 8.0 | 0.95 / 0.94 | 535/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_release_ratio = 0.6 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_release_ratio = 0.9 | 0.95 / 0.94 | 545/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_min_following_distance_m = 1.0 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_min_following_distance_m = 3.0 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_time_gap_table = x0.8 | 0.93 / 0.94 | 504/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| critical_time_gap_table = x1.2 | 0.95 / 0.94 | 548/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| path_half_width_m = 1.25 | 0.94 / 0.94 | 547/549 | 0.62 / 0.87 | 258/267 | 0.73 / 0.99 | 153/153 |
| path_half_width_m = 1.75 | 0.91 / 0.94 | 576/549 | 0.68 / 0.83 | 279/267 | 0.45 / 1.00 | 190/153 |
| cut_in_lateral_speed_mps = 0.2 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| cut_in_lateral_speed_mps = 0.5 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.71 / 0.97 | 150/153 |
| cut_in_persistence_s = 0.3 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.75 / 0.96 | 155/153 |
| cut_in_persistence_s = 0.8 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.66 / 0.95 | 140/153 |
| cut_in_outside_margin_m = 0.3 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| cut_in_outside_margin_m = 0.8 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.44 / 0.85 | 145/153 |
| cut_in_horizon_s = 2.0 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.97 | 153/153 |
| cut_in_horizon_s = 4.0 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| target_length_m = 4.2 | 0.94 / 0.94 | 549/549 | 0.63 / 0.90 | 267/267 | 0.71 / 0.96 | 153/153 |
| target_length_m = 5.0 | 0.94 / 0.94 | 549/549 | 0.66 / 0.80 | 267/267 | 0.73 / 0.96 | 153/153 |
| max_position_std_m = 0.5 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |
| max_position_std_m = 1.5 | 0.94 / 0.94 | 549/549 | 0.66 / 0.86 | 267/267 | 0.73 / 0.96 | 153/153 |

Recall / precision: the reconstruction against the COVERAGE oracle under the same definition.  Oracle events: COVERAGE oracle events under the varied value / nominal value (what the threshold alone does to the reference).  Full table: results/semantics/sensitivity_sweeps.md.
