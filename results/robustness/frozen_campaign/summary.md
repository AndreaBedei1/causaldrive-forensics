# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `ac2cb70ad595af1c`, configuration `af2b7dc72208533f`, commit `143667f7b1d830ba497295ff213fb3a70b5154fc`, 2026-10-15T22:24:09Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | none | 1 | 22 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/22 |
| radar | low | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.993 +- 0.006 | 0.0 | 0.050 | 0.283 +- 0.010 | 0.0 | 0.7 +- 0.6 | 0.0 | 1.3 +- 1.5 | 3/66 |
| radar | nominal | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.971 +- 0.019 | 5.7 +- 1.5 | 0.150 | 0.302 +- 0.006 | 0.0 | 1.3 +- 0.6 | 0.7 +- 1.2 | 14.0 +- 1.7 | 1/66 |
| radar | high | 4 | 88 | 0 | 0.950 +- 0.031 | 0.991 +- 0.018 | 0.966 +- 0.023 | 0.854 +- 0.015 | 206.2 +- 9.5 | 0.312 +- 0.063 | 0.517 +- 0.089 | 1.5 +- 1.3 | 39.2 +- 5.1 | 16.5 +- 5.4 | 2251.8 +- 26.9 | 0/88 |
| gnss | rtk | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.295 +- 0.019 | 0.0 | 1.0 | 0.0 | 0.0 | 21/66 |
| gnss | consumer | 8 | 176 | 0 | 1.000 | 1.000 | 0.972 +- 0.024 | 0.974 +- 0.004 | 3.0 +- 0.9 | 0.000 | 1.781 +- 0.787 | 0.0 | 6.2 +- 1.6 | 0.0 | 0.0 | 12/176 |
| gnss | degraded | 8 | 176 | 0 | 1.000 | 1.000 | 0.960 +- 0.016 | 0.967 +- 0.003 | 3.8 +- 1.5 | 0.000 | 4.902 +- 1.721 | 0.0 | 7.9 +- 1.7 | 0.0 | 0.0 | 8/176 |
| gnss_refined | rtk | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.295 +- 0.019 | 0.0 | 1.0 | 0.0 | 0.0 | 21/66 |
| gnss_refined | consumer | 8 | 176 | 0 | 1.000 | 1.000 | 0.972 +- 0.024 | 0.974 +- 0.004 | 3.0 +- 0.9 | 0.000 | 1.781 +- 0.787 | 0.0 | 6.2 +- 1.6 | 0.0 | 0.0 | 12/176 |
| gnss_refined | degraded | 8 | 176 | 0 | 1.000 | 1.000 | 0.960 +- 0.016 | 0.967 +- 0.003 | 3.8 +- 1.5 | 0.000 | 4.902 +- 1.721 | 0.0 | 7.9 +- 1.7 | 0.0 | 0.0 | 8/176 |
| gnss_correlated | consumer common 0.5 | 8 | 176 | 0 | 1.000 | 1.000 | 0.972 +- 0.024 | 0.975 +- 0.004 | 2.9 +- 1.0 | 0.000 | 1.626 +- 0.416 | 0.0 | 6.2 +- 1.5 | 0.0 | 0.0 | 12/176 |
| gnss_correlated | consumer common 0.9 | 8 | 176 | 0 | 1.000 | 1.000 | 0.966 +- 0.021 | 0.974 +- 0.003 | 2.6 +- 0.9 | 0.000 | 2.050 +- 0.667 | 0.0 | 5.9 +- 1.4 | 0.0 | 0.0 | 12/176 |
| gnss_correlated | consumer common 1.0 | 8 | 176 | 0 | 1.000 | 1.000 | 0.989 +- 0.021 | 0.977 +- 0.003 | 3.5 +- 0.9 | 0.000 | 2.236 +- 1.093 | 0.0 | 7.2 +- 1.4 | 0.0 | 0.0 | 12/176 |
| combined | exact + 10% | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/66 |
| combined | RTK + 10% | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.295 +- 0.019 | 0.0 | 1.0 | 0.0 | 0.0 | 21/66 |
| combined | consumer independent + 10% | 8 | 176 | 0 | 1.000 | 0.903 +- 0.275 | 0.926 +- 0.137 | 0.911 +- 0.177 | 12.8 +- 27.2 | 0.019 +- 0.053 | 1.881 +- 0.765 | 0.0 | 9.5 +- 8.8 | 0.0 | 0.0 | 10/176 |
| combined | consumer common 0.9 + 10% | 8 | 176 | 0 | 1.000 | 0.903 +- 0.275 | 0.920 +- 0.135 | 0.914 +- 0.172 | 12.2 +- 27.4 | 0.019 +- 0.053 | 2.095 +- 0.681 | 0.0 | 9.1 +- 9.3 | 0.0 | 0.0 | 10/176 |
| radar_gnss_combined | gnss rtk + radar low | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.993 +- 0.006 | 0.0 | 0.050 | 0.298 +- 0.002 | 0.0 | 0.7 +- 0.6 | 0.0 | 1.3 +- 1.5 | 3/66 |
| radar_gnss_combined | gnss rtk + radar nominal | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.971 +- 0.019 | 5.7 +- 1.5 | 0.150 | 0.302 +- 0.009 | 0.0 | 1.3 +- 0.6 | 0.0 | 14.0 +- 1.7 | 1/66 |
| radar_gnss_combined | gnss rtk + radar high | 3 | 66 | 0 | 0.939 +- 0.028 | 0.988 +- 0.021 | 0.970 +- 0.026 | 0.860 +- 0.009 | 206.7 +- 11.6 | 0.283 +- 0.029 | 0.529 +- 0.081 | 2.0 +- 1.0 | 37.3 +- 4.2 | 14.3 +- 3.2 | 2263.7 +- 12.2 | 0/66 |
| radar_gnss_combined | gnss consumer + radar low | 8 | 176 | 0 | 1.000 | 1.000 | 0.972 +- 0.024 | 0.964 +- 0.011 | 3.8 +- 1.3 | 0.050 | 1.801 +- 0.762 | 0.0 | 6.9 +- 1.6 | 0.0 | 1.1 +- 0.8 | 4/176 |
| radar_gnss_combined | gnss consumer + radar nominal | 8 | 176 | 0 | 1.000 | 1.000 | 0.972 +- 0.024 | 0.940 +- 0.011 | 10.2 +- 1.9 | 0.175 +- 0.027 | 1.780 +- 0.816 | 0.0 | 9.8 +- 2.1 | 0.0 | 14.5 +- 3.4 | 1/176 |
| radar_gnss_combined | gnss consumer + radar high | 8 | 176 | 0 | 0.942 +- 0.047 | 0.986 +- 0.019 | 0.909 +- 0.024 | 0.778 +- 0.036 | 219.2 +- 10.7 | 0.319 +- 0.046 | 2.137 +- 0.453 | 1.1 +- 1.2 | 55.4 +- 6.5 | 10.4 +- 4.0 | 2242.9 +- 20.2 | 0/176 |
| radar_gnss_combined | gnss degraded + radar low | 8 | 176 | 0 | 1.000 | 1.000 | 0.960 +- 0.016 | 0.958 +- 0.009 | 4.6 +- 1.7 | 0.050 | 4.934 +- 1.696 | 0.0 | 8.2 +- 1.3 | 0.0 | 1.1 +- 0.8 | 4/176 |
| radar_gnss_combined | gnss degraded + radar nominal | 8 | 176 | 0 | 1.000 | 1.000 | 0.955 +- 0.034 | 0.934 +- 0.009 | 11.0 +- 2.6 | 0.169 +- 0.037 | 4.944 +- 1.535 | 0.0 | 10.8 +- 2.5 | 0.0 | 14.5 +- 3.4 | 1/176 |
| radar_gnss_combined | gnss degraded + radar high | 8 | 176 | 0 | 0.908 +- 0.057 | 0.986 +- 0.019 | 0.938 +- 0.034 | 0.754 +- 0.033 | 228.5 +- 12.7 | 0.312 +- 0.052 | 5.353 +- 1.036 | 1.6 +- 1.2 | 62.6 +- 9.4 | 2.2 +- 1.7 | 2268.0 +- 24.9 | 0/176 |
| impulse | 2% | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/66 |
| impulse | 5% | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/66 |
| impulse | 10% | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/66 |
| impulse | 20% | 3 | 66 | 0 | 1.000 | 0.988 +- 0.021 | 1.000 | 0.998 +- 0.003 | 0.3 +- 0.6 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 21/66 |
| latency | 0.05 s | 1 | 22 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.050 | 0.469 | 0.0 | 1.0 | 0.0 | 0.0 | 0/22 |
| latency | 0.10 s | 1 | 22 | 0 | 1.000 | 0.926 | 1.000 | 0.989 | 4.0 | 0.100 | 0.629 | 0.0 | 1.0 | 0.0 | 0.0 | 0/22 |
| latency | 0.25 s | 1 | 22 | 0 | 1.000 | 0.815 | 1.000 | 0.968 | 9.0 | 0.250 | 0.654 | 0.0 | 1.0 | 0.0 | 0.0 | 0/22 |
| latency | 0.50 s | 1 | 22 | 0 | 1.000 | 0.518 | 0.818 | 0.839 | 28.0 | 0.500 | 0.412 | 0.0 | 5.0 | 1.0 | 0.0 | 0/22 |
| clock | offsets | 1 | 22 | 0 | - | - | - | 1.000 | 0.0 | 0.000 | - | - | - | - | - | 19/22 |
| downsample | 10 Hz | 1 | 22 | 0 | 0.980 | 1.000 | 1.000 | 0.930 | 3.0 | 0.050 | 0.258 | 1.0 | 2.0 | 0.0 | 0.0 | 0/22 |
| downsample | 5 Hz | 1 | 22 | 0 | 0.980 | 0.889 | 1.000 | 0.855 | 15.0 | 0.250 | 0.245 | 1.0 | 3.0 | 0.0 | 18.0 | 0/22 |
| dropout | one recorder | 1 | 50 | 0 | 1.000 | 0.909 | 0.980 | 0.959 | 7.0 | 0.000 | 0.359 | 0.0 | 2.0 | 0.0 | 0.0 | 0/50 |
| outage | 1 s radar outage | 1 | 50 | 0 | 0.984 | 1.000 | 1.000 | 0.941 | 20.0 | 0.200 | 0.289 | 2.0 | 9.0 | 2.0 | 10.0 | 6/50 |
