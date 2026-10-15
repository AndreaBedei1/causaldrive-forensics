# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `ac2cb70ad595af1c`, configuration `af2b7dc72208533f`, commit `5d7adf764f1b8c3d82e58d91f8bba309da79b7b8`, 2026-10-15T10:50:28Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline | none | 1 | 22 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.273 | 0.0 | 1.0 | 0.0 | 0.0 | 22/22 |
| radar | low | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.098 | 0.0 | 0.0 | 0.0 | 0.0 | 0/3 |
| radar | nominal | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.938 | 0.0 | 0.150 | 0.118 | 0.0 | 1.0 | 0.0 | 0.0 | 0/3 |
| radar | high | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.812 | 27.0 | 0.250 | 0.290 | 0.0 | 5.0 | 6.0 | 354.0 | 0/3 |
| gnss | rtk | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.115 | 0.0 | 0.0 | 0.0 | 0.0 | 3/3 |
| gnss | consumer | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 2.217 | 0.0 | 0.0 | 0.0 | 0.0 | 2/3 |
| gnss | degraded | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.969 | 1.0 | 0.000 | 5.616 | 0.0 | 1.0 | 0.0 | 0.0 | 1/3 |
| combined | exact + 10% | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.097 | 0.0 | 0.0 | 0.0 | 0.0 | 3/3 |
| combined | RTK + 10% | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.115 | 0.0 | 0.0 | 0.0 | 0.0 | 3/3 |
| combined | consumer independent + 10% | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 2.217 | 0.0 | 0.0 | 0.0 | 0.0 | 2/3 |
| combined | consumer common 0.9 + 10% | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.797 | 0.0 | 0.0 | 0.0 | 0.0 | 2/3 |
| radar_gnss_combined | gnss rtk + radar low | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 0.118 | 0.0 | 0.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss rtk + radar nominal | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.938 | 0.0 | 0.150 | 0.132 | 0.0 | 1.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss rtk + radar high | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.812 | 27.0 | 0.250 | 0.292 | 0.0 | 5.0 | 5.0 | 355.0 | 0/3 |
| radar_gnss_combined | gnss consumer + radar low | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | 2.217 | 0.0 | 0.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss consumer + radar nominal | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.875 | 2.0 | 0.150 | 2.283 | 0.0 | 3.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss consumer + radar high | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.781 | 28.0 | 0.250 | 0.968 | 0.0 | 9.0 | 1.0 | 359.0 | 0/3 |
| radar_gnss_combined | gnss degraded + radar low | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.969 | 1.0 | 0.000 | 5.620 | 0.0 | 1.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss degraded + radar nominal | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.875 | 2.0 | 0.150 | 7.310 | 0.0 | 3.0 | 0.0 | 0.0 | 0/3 |
| radar_gnss_combined | gnss degraded + radar high | 1 | 3 | 0 | 1.000 | 1.000 | 1.000 | 0.688 | 31.0 | 0.250 | 6.590 | 0.0 | 10.0 | 0.0 | 360.0 | 0/3 |
| dropout | one recorder | 1 | 7 | 0 | 1.000 | 1.000 | 1.000 | 0.913 | 2.0 | 0.000 | 0.263 | 0.0 | 0.0 | 0.0 | 0.0 | 0/7 |
