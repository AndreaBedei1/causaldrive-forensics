# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `b5cbbff6ceb04c12`, configuration `767c7dbb12167da9`, commit `c80eab47ec83dcc66909751b0514f1bcb4d5066e` (uncommitted changes), 2026-10-11T04:07:37Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | none | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.722 | 0.0 | 7.0 | 0.0 | 0.0 | - |
| radar | low | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 0.966 +- 0.011 | 4.7 +- 1.5 | 0.050 | 0.414 +- 0.024 | 0.0 | 3.3 +- 0.6 | 0.0 | 0.3 +- 0.6 | - |
| radar | nominal | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 0.973 +- 0.022 | 9.3 +- 2.1 | 0.133 +- 0.076 | 0.505 +- 0.060 | 0.0 | 3.7 +- 1.2 | 0.0 | 0.0 | - |
| radar | high | 3 | 51 | 0 | 0.987 +- 0.011 | 1.000 | 0.980 +- 0.034 | 0.939 +- 0.004 | 236.0 +- 16.1 | 0.267 +- 0.076 | 1.268 +- 0.047 | 0.3 +- 0.6 | 19.0 +- 3.5 | 15.0 +- 1.7 | 798.0 +- 15.1 | - |
| gnss | rtk | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.428 +- 0.023 | 0.0 | 3.0 | 0.0 | 0.0 | - |
| gnss | consumer | 8 | 136 | 0 | 1.000 | 1.000 | 0.963 +- 0.030 | 0.977 +- 0.014 | 1.2 +- 0.7 | 0.000 | 2.987 +- 0.422 | 0.0 | 3.4 +- 1.2 | 19.1 +- 1.6 | 0.0 | - |
| gnss | degraded | 8 | 136 | 0 | 0.950 +- 0.045 | 1.000 | 0.949 +- 0.038 | 0.963 +- 0.009 | 2.6 +- 1.8 | 0.000 | 6.583 +- 1.138 | 2.1 +- 2.0 | 4.6 +- 1.3 | 19.5 +- 6.2 | 0.0 | - |
| gnss_refined | rtk | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.428 +- 0.025 | 0.0 | 3.0 | 0.0 | 0.0 | - |
| gnss_refined | consumer | 8 | 136 | 0 | 1.000 | 1.000 | 0.963 +- 0.030 | 0.979 +- 0.011 | 1.0 | 0.000 | 2.001 +- 0.642 | 0.0 | 3.2 +- 1.0 | 8.6 +- 3.0 | 0.0 | - |
| gnss_refined | degraded | 8 | 136 | 0 | 0.964 +- 0.039 | 1.000 | 0.949 +- 0.038 | 0.966 +- 0.007 | 2.2 +- 1.3 | 0.000 | 5.243 +- 1.041 | 1.5 +- 1.7 | 4.1 +- 1.0 | 21.5 +- 3.1 | 0.0 | - |
| impulse | 2% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.722 | 0.0 | 7.0 | 0.0 | 0.0 | - |
| impulse | 5% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.722 | 0.0 | 7.0 | 0.0 | 0.0 | - |
| impulse | 10% | 3 | 51 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.722 | 0.0 | 7.0 | 0.0 | 0.0 | - |
| impulse | 20% | 3 | 51 | 0 | 1.000 | 0.985 +- 0.026 | 1.000 | 0.998 +- 0.004 | 0.3 +- 0.6 | 0.000 | 0.722 | 0.0 | 7.0 | 0.0 | 0.0 | - |
| latency | 0.05 s | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.0 | 0.050 | 0.757 | 0.0 | 3.0 | 0.0 | 0.0 | - |
| latency | 0.10 s | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 1.0 | 0.100 | 1.093 | 0.0 | 3.0 | 0.0 | 0.0 | - |
| latency | 0.25 s | 1 | 17 | 0 | 1.000 | 0.864 | 0.882 | 0.890 | 13.0 | 0.250 | 0.732 | 0.0 | 11.0 | 0.0 | 0.0 | - |
| latency | 0.50 s | 1 | 17 | 0 | 1.000 | 0.818 | 0.941 | 0.816 | 25.0 | 0.500 | 1.085 | 0.0 | 20.0 | 2.0 | 0.0 | - |
| clock | offsets | 1 | 17 | 0 | - | - | - | 1.000 | 0.0 | 0.000 | - | - | - | - | - | 17/17 |
| downsample | 10 Hz | 1 | 17 | 0 | 1.000 | 1.000 | 1.000 | 0.993 | 0.0 | 0.250 | 0.399 | 0.0 | 2.0 | 2.0 | 0.0 | - |
| downsample | 5 Hz | 1 | 17 | 0 | 0.976 | 0.955 | 1.000 | 0.912 | 9.0 | 0.250 | 0.450 | 1.0 | 2.0 | 0.0 | 0.0 | - |
| dropout | one recorder | 1 | 40 | 0 | 1.000 | 1.000 | 0.975 | 0.953 | 5.0 | 0.000 | 0.753 | 0.0 | 3.0 | 0.0 | 0.0 | - |
| outage | 1 s radar outage | 1 | 40 | 0 | 1.000 | 1.000 | 1.000 | 0.988 | 2.0 | 0.050 | 0.413 | 0.0 | 10.0 | 0.0 | 1.0 | - |

Baseline/impulse refreshed; all other families historical. Use family_provenance, not a single current-code claim.
