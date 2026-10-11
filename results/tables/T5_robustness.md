**T5_robustness.**  Robustness of the reconstruction on the canonical runs (docs/robustness_profiles.md): mean +- SD over seeds of the metrics pooled over the runs. Baseline/impulse refreshed in final hardening; other families retain the historical implementation and its baseline (see family_provenance in summary.json).

| family | level | seeds | identity acc. | collisions | runs aligned | core events | event dt p95 [s] | centre err. [m] | wrong links + false merges | identical graphs |
|---|---|---|---|---|---|---|---|---|---|---|
| baseline | none | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.72 | 0.0 | - |
| baseline historical | none | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.41 | 0.0 | - |
| radar | low | 3 | 1.000 | 1.000 | 1.000 | 0.966 +- 0.011 | 0.05 | 0.41 +- 0.02 | 0.0 | - |
| radar | nominal | 3 | 1.000 | 1.000 | 1.000 | 0.973 +- 0.022 | 0.13 +- 0.08 | 0.51 +- 0.06 | 0.0 | - |
| radar | high | 3 | 0.987 +- 0.011 | 1.000 | 0.980 +- 0.034 | 0.939 +- 0.004 | 0.27 +- 0.08 | 1.27 +- 0.05 | 15.3 | - |
| gnss | rtk | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.43 +- 0.02 | 0.0 | - |
| gnss | consumer | 8 | 1.000 | 1.000 | 0.963 +- 0.030 | 0.977 +- 0.014 | 0.00 | 2.99 +- 0.42 | 19.1 | - |
| gnss | degraded | 8 | 0.950 +- 0.045 | 1.000 | 0.949 +- 0.038 | 0.963 +- 0.009 | 0.00 | 6.58 +- 1.14 | 21.6 | - |
| gnss refined | rtk | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.43 +- 0.02 | 0.0 | - |
| gnss refined | consumer | 8 | 1.000 | 1.000 | 0.963 +- 0.030 | 0.979 +- 0.011 | 0.00 | 2.00 +- 0.64 | 8.6 | - |
| gnss refined | degraded | 8 | 0.964 +- 0.039 | 1.000 | 0.949 +- 0.038 | 0.966 +- 0.007 | 0.00 | 5.24 +- 1.04 | 23.0 | - |
| impulse | 2% | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.72 | 0.0 | - |
| impulse | 5% | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.72 | 0.0 | - |
| impulse | 10% | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.00 | 0.72 | 0.0 | - |
| impulse | 20% | 3 | 1.000 | 0.985 +- 0.026 | 1.000 | 0.998 +- 0.004 | 0.00 | 0.72 | 0.0 | - |
| latency | 0.05 s | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.05 | 0.76 | 0.0 | - |
| latency | 0.10 s | 1 | 1.000 | 1.000 | 1.000 | 1.000 | 0.10 | 1.09 | 0.0 | - |
| latency | 0.25 s | 1 | 1.000 | 0.864 | 0.882 | 0.890 | 0.25 | 0.73 | 0.0 | - |
| latency | 0.50 s | 1 | 1.000 | 0.818 | 0.941 | 0.816 | 0.50 | 1.09 | 2.0 | - |
| clock | offsets | 1 | - | - | - | 1.000 | 0.00 | - | - | 17/17 |
| downsample | 10 Hz | 1 | 1.000 | 1.000 | 1.000 | 0.993 | 0.25 | 0.40 | 2.0 | - |
| downsample | 5 Hz | 1 | 0.976 | 0.955 | 1.000 | 0.912 | 0.25 | 0.45 | 1.0 | - |
| dropout | one recorder | 1 | 1.000 | 1.000 | 0.975 | 0.953 | 0.00 | 0.75 | 0.0 | - |
| outage | 1 s radar outage | 1 | 1.000 | 1.000 | 1.000 | 0.988 | 0.05 | 0.41 | 0.0 | - |

Core events: the unperturbed reconstruction's instant core events found again (same type, actor, subject class, within 1 s).  Centre error in the map frame of the pose streams (a GNSS error common to all recorders stays in it).  Wrong links and false merges: counts per draw over the 17 runs.
