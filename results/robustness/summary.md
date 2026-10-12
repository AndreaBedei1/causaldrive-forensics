# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T14:25:03Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | none | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| radar | low | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 0.991 +- 0.004 | 1.0 +- 1.7 | 0.050 | 0.382 +- 0.034 | 0.0 | 1.3 +- 0.6 | 0.0 | 0.0 | - |
| radar | nominal | 5 | 85 | 0 | 1.000 | 1.000 | 1.000 | 0.972 +- 0.009 | 9.8 +- 2.7 | 0.080 +- 0.045 | 0.479 +- 0.108 | 0.0 | 2.0 +- 1.2 | 0.0 | 0.0 | - |
| radar | high | 3 | 51 | 0 | 0.994 +- 0.010 | 1.000 | 0.980 +- 0.034 | 0.894 +- 0.010 | 141.0 +- 7.2 | 0.367 +- 0.029 | 0.873 +- 0.054 | 0.0 | 15.3 +- 3.8 | 9.7 +- 4.6 | 938.0 +- 28.4 | - |
| gnss | rtk | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.434 +- 0.040 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| gnss | consumer | 8 | 136 | 0 | 0.985 +- 0.013 | 0.807 +- 0.047 | 0.890 +- 0.049 | 0.905 +- 0.031 | 9.2 +- 2.8 | 0.000 | 2.835 +- 0.491 | 0.6 +- 0.5 | 3.5 +- 1.3 | 19.9 +- 1.6 | 0.0 | - |
| gnss | degraded | 8 | 136 | 0 | 0.945 +- 0.024 | 0.778 +- 0.038 | 0.860 +- 0.054 | 0.872 +- 0.013 | 14.0 +- 4.6 | 0.000 | 6.961 +- 1.959 | 2.1 +- 1.0 | 5.5 +- 2.1 | 22.5 +- 2.3 | 0.0 | - |
| gnss_refined | rtk | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.434 +- 0.040 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| gnss_refined | consumer | 8 | 136 | 0 | 0.985 +- 0.013 | 0.807 +- 0.047 | 0.890 +- 0.049 | 0.906 +- 0.028 | 9.0 +- 2.6 | 0.000 | 1.944 +- 0.448 | 0.6 +- 0.5 | 3.4 +- 1.2 | 6.0 | 0.0 | - |
| gnss_refined | degraded | 8 | 136 | 0 | 0.955 +- 0.022 | 0.778 +- 0.038 | 0.860 +- 0.054 | 0.874 +- 0.013 | 13.4 +- 4.3 | 0.000 | 5.854 +- 1.360 | 1.8 +- 0.9 | 5.0 +- 1.8 | 23.6 +- 1.1 | 0.0 | - |
| gnss_correlated | consumer common 0.5 | 8 | 136 | 0 | 0.990 +- 0.014 | 0.784 +- 0.126 | 0.868 +- 0.112 | 0.888 +- 0.084 | 11.2 +- 7.7 | 0.013 +- 0.035 | 2.390 +- 0.771 | 0.4 +- 0.5 | 4.4 +- 2.2 | 18.2 +- 6.6 | 0.0 | - |
| gnss_correlated | consumer common 0.9 | 8 | 136 | 0 | 0.997 +- 0.009 | 0.847 +- 0.034 | 0.934 +- 0.038 | 0.928 +- 0.025 | 8.4 +- 2.2 | 0.000 | 2.495 +- 0.846 | 0.1 +- 0.4 | 3.6 +- 1.1 | 20.6 +- 1.1 | 0.0 | - |
| gnss_correlated | consumer common 1.0 | 8 | 136 | 0 | 1.000 | 0.864 | 0.985 +- 0.027 | 0.958 +- 0.016 | 7.2 +- 0.5 | 0.000 | 2.485 +- 0.906 | 0.0 | 2.5 +- 0.9 | 20.6 +- 1.1 | 0.0 | - |
| combined | exact + 10% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| combined | RTK + 10% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.434 +- 0.040 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| combined | consumer independent + 10% | 8 | 136 | 0 | 0.994 +- 0.011 | 0.767 +- 0.204 | 0.875 +- 0.123 | 0.878 +- 0.123 | 12.9 +- 14.0 | 0.037 +- 0.106 | 2.704 +- 0.711 | 0.2 +- 0.5 | 5.2 +- 5.3 | 17.9 +- 6.6 | 0.0 | - |
| combined | consumer common 0.9 + 10% | 8 | 136 | 0 | 1.000 | 0.784 +- 0.207 | 0.897 +- 0.129 | 0.896 +- 0.107 | 11.9 +- 11.5 | 0.025 +- 0.071 | 2.521 +- 0.845 | 0.0 | 4.6 +- 3.2 | 18.6 +- 6.7 | 0.0 | - |
| impulse | 2% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| impulse | 5% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| impulse | 10% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| impulse | 20% | 3 | 51 | 0 | 1.000 | 0.985 +- 0.026 | 1.000 | 0.998 +- 0.004 | 0.3 +- 0.6 | 0.000 | 0.402 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| latency | 0.05 s | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.0 | 0.050 | 0.758 | 0.0 | 1.0 | 0.0 | 0.0 | - |
| latency | 0.10 s | 1 | 17 | 0 | 1.000 | 0.909 | 0.941 | 0.960 | 5.0 | 0.100 | 0.925 | 0.0 | 2.0 | 0.0 | 0.0 | - |
| latency | 0.25 s | 1 | 17 | 0 | 1.000 | 0.773 | 0.824 | 0.878 | 14.0 | 0.250 | 0.763 | 0.0 | 8.0 | 0.0 | 0.0 | - |
| latency | 0.50 s | 1 | 17 | 0 | 1.000 | 0.545 | 0.882 | 0.797 | 34.0 | 0.500 | 0.732 | 0.0 | 14.0 | 2.0 | 0.0 | - |
| clock | offsets | 1 | 17 | 0 | - | - | - | 1.000 | 0.0 | 0.000 | - | - | - | - | - | 17/17 |
| downsample | 10 Hz | 1 | 17 | 0 | 0.977 | 1.000 | 1.000 | 0.966 | 0.0 | 0.100 | 0.396 | 1.0 | 1.0 | 0.0 | 0.0 | - |
| downsample | 5 Hz | 1 | 17 | 0 | 0.975 | 0.864 | 0.941 | 0.899 | 9.0 | 0.250 | 0.354 | 1.0 | 2.0 | 0.0 | 0.0 | - |
| dropout | one recorder | 1 | 40 | 0 | 1.000 | 0.909 | 0.975 | 0.948 | 7.0 | 0.000 | 0.728 | 0.0 | 2.0 | 0.0 | 0.0 | - |
| outage | 1 s radar outage | 1 | 40 | 0 | 0.991 | 0.964 | 0.975 | 0.966 | 7.0 | 0.050 | 0.410 | 1.0 | 5.0 | 0.0 | 0.0 | - |
