# Campaign v3: reconstruction quality per condition

Per seed the jobs are pooled: rates are ratios of sums; counts and paired changes from the G0 baseline of the same run are means per job.  Then the mean over seeds +- SD.  Represented: observable road users that record nothing.  Definitions: `cdf.evaluation.scorecard`.

| family | level | degraded | recorders | seeds | jobs | failed | collisions identified | invented | observable represented | duplicates | recorder ghosts | phantoms | median of the per-job position medians [m] | paired d identified | paired d represented | paired d phantoms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | none | all | 2 | 1 | 16 | 0 | 1.000 | 0.0 | 1.000 | 1.2 | 0.0 | 0.0 | 0.274 | 0.00 | 0.00 | 0.0 |
| baseline | none | all | 3 | 1 | 6 | 0 | 1.000 | 0.0 | - | 0.0 | 0.2 | 0.0 | - | 0.00 | 0.00 | 0.0 |
| gnss | rtk | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 1.2 | 0.0 | 0.0 | 0.269 +- 0.004 | 0.00 | 0.00 | 0.0 |
| gnss | degraded | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 1.3 +- 0.1 | 0.0 | 0.0 | 0.269 +- 0.044 | 0.00 | 0.00 | 0.0 |
| gnss | rtk | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.2 | 0.0 | - | 0.00 | 0.00 | 0.0 |
| gnss | degraded | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.1 | 0.0 | - | 0.00 | 0.00 | 0.0 |
| radar_v3 | nominal | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 1.6 +- 0.3 | 0.0 +- 0.1 | 0.6 +- 0.2 | 0.308 +- 0.022 | 0.00 | 0.00 | 0.6 +- 0.2 |
| radar_v3 | severe | all | 2 | 3 | 48 | 0 | 0.979 +- 0.036 | 0.0 +- 0.0 | 1.000 | 2.5 +- 0.1 | 0.5 +- 0.1 | 64.6 +- 1.1 | 0.342 +- 0.021 | -0.02 +- 0.04 | 0.00 | 64.6 +- 1.1 |
| radar_v3 | extreme | all | 2 | 5 | 80 | 0 | 0.975 +- 0.056 | 0.0 +- 0.1 | 1.000 | 3.4 +- 0.4 | 1.6 +- 0.4 | 98.3 +- 1.2 | 0.342 +- 0.012 | -0.03 +- 0.06 | 0.00 | 98.3 +- 1.2 |
| radar_v3 | nominal | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.1 | 0.4 +- 0.1 | - | 0.00 | 0.00 | 0.4 +- 0.1 |
| radar_v3 | severe | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.4 +- 0.1 | 79.8 +- 4.5 | - | 0.00 | 0.00 | 79.8 +- 4.5 |
| radar_v3 | extreme | all | 3 | 5 | 30 | 0 | 0.920 +- 0.110 | 0.1 +- 0.2 | - | 0.0 | 2.2 +- 0.7 | 113.3 +- 6.4 | - | -0.13 +- 0.18 | 0.00 | 113.3 +- 6.4 |
| radar_asym | nominal | alone | 2 | 3 | 96 | 0 | 1.000 | 0.0 | 1.000 | 1.4 +- 0.2 | 0.0 +- 0.0 | 0.3 +- 0.1 | 0.284 +- 0.008 | 0.00 | 0.00 | 0.3 +- 0.1 |
| radar_asym | extreme | alone | 2 | 5 | 160 | 0 | 0.988 +- 0.028 | 0.0 +- 0.0 | 1.000 | 2.4 +- 0.2 | 0.8 +- 0.2 | 49.4 +- 0.6 | 0.295 +- 0.011 | -0.01 +- 0.03 | 0.00 | 49.4 +- 0.6 |
| radar_asym | severe | alone | 2 | 3 | 96 | 0 | 0.990 +- 0.018 | 0.0 +- 0.0 | 1.000 | 1.9 +- 0.1 | 0.3 +- 0.0 | 32.5 +- 0.6 | 0.291 +- 0.020 | -0.01 +- 0.02 | 0.00 | 32.5 +- 0.6 |
| radar_asym | severe | alone | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.3 +- 0.0 | 27.0 +- 1.5 | - | 0.00 | 0.00 | 27.0 +- 1.5 |
| radar_asym | nominal | alone | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.0 | 0.1 +- 0.0 | - | 0.00 | 0.00 | 0.1 +- 0.0 |
| radar_asym | nominal | all but one | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.1 | 0.3 +- 0.1 | - | 0.00 | 0.00 | 0.3 +- 0.1 |
| radar_asym | severe | all but one | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.4 +- 0.1 | 53.6 +- 3.0 | - | 0.00 | 0.00 | 53.6 +- 3.0 |
| radar_asym | extreme | alone | 3 | 5 | 90 | 0 | 0.973 +- 0.036 | 0.0 +- 0.1 | - | 0.0 | 0.9 +- 0.2 | 38.8 +- 1.5 | - | -0.04 +- 0.06 | 0.00 | 38.8 +- 1.5 |
| radar_asym | extreme | all but one | 3 | 5 | 90 | 0 | 0.947 +- 0.073 | 0.1 +- 0.1 | - | 0.0 | 1.5 +- 0.5 | 76.6 +- 3.6 | - | -0.09 +- 0.12 | 0.00 | 76.6 +- 3.6 |
| radar_gnss_v3 | gnss rtk + radar severe | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 2.5 +- 0.2 | 0.3 +- 0.1 | 63.6 +- 1.8 | 0.335 +- 0.017 | 0.00 | 0.00 | 63.6 +- 1.8 |
| radar_gnss_v3 | gnss rtk + radar nominal | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 1.6 +- 0.3 | 0.1 +- 0.1 | 0.6 +- 0.2 | 0.303 +- 0.025 | 0.00 | 0.00 | 0.6 +- 0.2 |
| radar_gnss_v3 | gnss degraded + radar nominal | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 1.7 +- 0.3 | 0.0 +- 0.1 | 0.7 +- 0.1 | 0.292 +- 0.052 | 0.00 | 0.00 | 0.7 +- 0.1 |
| radar_gnss_v3 | gnss degraded + radar severe | all | 2 | 3 | 48 | 0 | 1.000 | 0.0 | 1.000 | 2.6 +- 0.2 | 0.4 +- 0.1 | 65.0 +- 1.5 | 0.340 +- 0.061 | 0.00 | 0.00 | 65.0 +- 1.5 |
| radar_gnss_v3 | gnss rtk + radar nominal | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.1 | 0.4 +- 0.1 | - | 0.00 | 0.00 | 0.4 +- 0.1 |
| radar_gnss_v3 | gnss degraded + radar nominal | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.2 +- 0.2 | 0.3 +- 0.2 | - | 0.00 | 0.00 | 0.3 +- 0.2 |
| radar_gnss_v3 | gnss degraded + radar severe | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.9 +- 0.1 | 81.9 +- 4.2 | - | 0.00 | 0.00 | 81.9 +- 4.2 |
| radar_gnss_v3 | gnss rtk + radar severe | all | 3 | 3 | 18 | 0 | 1.000 | 0.0 | - | 0.0 | 0.4 +- 0.3 | 80.5 +- 6.1 | - | 0.00 | 0.00 | 80.5 +- 6.1 |
| radar_asym_gnss | gnss degraded + radar severe | alone | 2 | 3 | 96 | 0 | 1.000 | 0.0 | 1.000 | 2.0 +- 0.1 | 0.2 +- 0.0 | 32.8 +- 0.8 | 0.305 +- 0.050 | 0.00 | 0.00 | 32.8 +- 0.8 |
| radar_asym_gnss | gnss degraded + radar nominal | alone | 2 | 3 | 96 | 0 | 1.000 | 0.0 | 1.000 | 1.5 +- 0.2 | 0.0 +- 0.0 | 0.3 +- 0.1 | 0.280 +- 0.044 | 0.00 | 0.00 | 0.3 +- 0.1 |
| radar_asym_gnss | gnss degraded + radar nominal | alone | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.1 +- 0.1 | 0.1 +- 0.1 | - | 0.00 | 0.00 | 0.1 +- 0.1 |
| radar_asym_gnss | gnss degraded + radar severe | alone | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.3 +- 0.1 | 28.1 +- 0.6 | - | 0.00 | 0.00 | 28.1 +- 0.6 |
| radar_asym_gnss | gnss degraded + radar severe | all but one | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.6 +- 0.1 | 55.4 +- 2.0 | - | 0.00 | 0.00 | 55.4 +- 2.0 |
| radar_asym_gnss | gnss degraded + radar nominal | all but one | 3 | 3 | 54 | 0 | 1.000 | 0.0 | - | 0.0 | 0.2 +- 0.1 | 0.2 +- 0.1 | - | 0.00 | 0.00 | 0.2 +- 0.1 |
