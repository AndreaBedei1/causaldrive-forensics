# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `83713ba55cc1bdf5`, configuration `830087c6640c709c`, commit `df12f75995d2ca7a78882a2ef17a2f677d023eab`, 2026-10-23T12:28:25Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | none | 1 | 22 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.277 | 0.0 | 1.0 | 0.0 | 0.0 | 22/22 |
| gnss | rtk | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.998 +- 0.003 | 2.7 +- 0.6 | 0.017 +- 0.029 | 0.282 +- 0.011 | 0.0 | 1.0 | 0.0 | 0.0 | 9/66 |
| gnss | degraded | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.989 +- 0.009 | 4.3 +- 0.6 | 0.050 | 0.272 +- 0.044 | 0.0 | 0.3 +- 0.6 | 0.0 | 0.0 | 2/66 |
| radar_v3 | nominal | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.976 +- 0.006 | 7.0 +- 2.6 | 0.150 | 0.305 +- 0.005 | 0.0 | 1.3 +- 1.5 | 0.0 | 12.3 +- 2.5 | 1/66 |
| radar_v3 | severe | 3 | 66 | 0 | 0.988 +- 0.011 | 0.987 +- 0.022 | 1.000 | 0.951 +- 0.016 | 27.7 +- 7.0 | 0.283 +- 0.029 | 0.375 +- 0.031 | 0.7 +- 0.6 | 11.0 +- 2.0 | 15.0 +- 3.5 | 1512.3 +- 26.5 | 0/66 |
| radar_v3 | extreme | 5 | 110 | 0 | 0.948 +- 0.029 | 0.954 +- 0.042 | 0.964 +- 0.038 | 0.857 +- 0.040 | 223.8 +- 11.5 | 0.340 +- 0.022 | 0.478 +- 0.074 | 2.6 +- 1.3 | 39.8 +- 9.4 | 20.0 +- 6.2 | 2252.8 +- 51.2 | 0/110 |
| radar_asym | nominal | 3 | 204 | 0 | 1.000 | 1.000 | 1.000 | 0.988 | 11.7 +- 2.1 | 0.050 | 0.298 +- 0.006 | 0.0 | 5.7 +- 2.5 | 0.0 | 17.0 +- 2.6 | 14/204 |
| radar_asym | severe | 3 | 204 | 0 | 0.990 +- 0.009 | 0.996 +- 0.006 | 1.000 | 0.979 +- 0.007 | 43.7 +- 9.9 | 0.150 +- 0.050 | 0.358 +- 0.011 | 2.0 +- 1.7 | 19.3 +- 3.1 | 9.7 +- 3.2 | 2490.0 +- 76.3 | 0/204 |
| radar_asym | extreme | 5 | 340 | 0 | 0.972 +- 0.015 | 0.970 +- 0.033 | 0.965 +- 0.037 | 0.926 +- 0.029 | 370.6 +- 28.2 | 0.150 | 0.511 +- 0.116 | 4.6 +- 2.6 | 70.4 +- 17.4 | 11.4 +- 5.7 | 3657.4 +- 104.2 | 0/340 |
| radar_gnss_v3 | gnss rtk + radar nominal | 3 | 66 | 0 | 1.000 | 1.000 | 1.000 | 0.978 +- 0.005 | 7.0 +- 2.6 | 0.150 | 0.309 +- 0.014 | 0.0 | 2.0 +- 2.6 | 0.0 | 12.7 +- 3.1 | 2/66 |
| radar_gnss_v3 | gnss rtk + radar severe | 3 | 66 | 0 | 0.994 +- 0.011 | 1.000 | 0.985 +- 0.026 | 0.945 +- 0.009 | 30.0 +- 4.4 | 0.283 +- 0.029 | 0.360 +- 0.027 | 0.0 | 7.7 +- 1.2 | 15.0 +- 2.6 | 1501.0 +- 64.8 | 0/66 |
| radar_gnss_v3 | gnss degraded + radar nominal | 3 | 66 | 0 | 0.993 +- 0.011 | 1.000 | 1.000 | 0.969 +- 0.003 | 8.0 +- 1.7 | 0.150 | 0.301 +- 0.045 | 0.3 +- 0.6 | 2.0 +- 2.0 | 0.0 | 12.7 +- 1.2 | 1/66 |
| radar_gnss_v3 | gnss degraded + radar severe | 3 | 66 | 0 | 0.988 +- 0.021 | 1.000 | 0.985 +- 0.026 | 0.933 +- 0.025 | 27.0 +- 3.6 | 0.283 +- 0.029 | 0.378 +- 0.078 | 0.7 +- 1.2 | 11.3 +- 1.5 | 16.0 +- 2.6 | 1531.3 +- 31.1 | 0/66 |
| radar_asym_gnss | gnss degraded + radar nominal | 3 | 204 | 0 | 0.995 +- 0.009 | 1.000 | 1.000 | 0.979 +- 0.006 | 18.7 +- 3.8 | 0.050 | 0.305 +- 0.030 | 1.0 +- 1.7 | 5.7 +- 5.5 | 0.7 +- 1.2 | 16.7 +- 1.2 | 5/204 |
| radar_asym_gnss | gnss degraded + radar severe | 3 | 204 | 0 | 0.990 +- 0.018 | 1.000 | 0.985 +- 0.025 | 0.960 +- 0.019 | 47.3 +- 5.8 | 0.150 +- 0.050 | 0.350 +- 0.055 | 2.0 +- 3.5 | 22.7 +- 2.1 | 7.7 +- 1.2 | 2552.7 +- 45.0 | 0/204 |
