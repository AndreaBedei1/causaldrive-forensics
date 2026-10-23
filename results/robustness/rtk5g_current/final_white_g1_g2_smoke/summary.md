# Robustness of the reconstruction

Every condition applied to every canonical run (`scripts/robustness.py`, `cdf.robustness.perturb`); stochastic conditions over seeds (3 at least, more until the standard error of every pooled metric is below its tolerance, 8 at most).  Per seed the metrics are pooled over the runs (counts: sums over the runs of one draw); the table gives the mean over seeds +- their standard deviation.  Ground truth is used only here, for the evaluation; the reconstruction under test never sees it.

Columns: identity association accuracy over the decided tracks; true vehicle-vehicle collisions reconstructed; share of runs with every recorder on the global clock; core instant events of the unperturbed reconstruction found again (same type, actor and subject class within 1 s, after removing a shift of the clock origin) and those added; 95th percentile of their time differences; median fused centre error of the anonymous road users (map frame of the pose streams: a GNSS error common to all recorders stays in it); recorder links wrong or missed; false merges of anonymous tracks; anonymous entities that are no vehicle (clutter).

Provenance: code `396e559665c905a1`, configuration `af2b7dc72208533f`, commit `40a8d485588af9e4399e2f923b7f16cbaeb8d454` (uncommitted changes), 2026-10-21T20:02:55Z.

| family | level | seeds | runs | failed | assoc. acc. | coll. recall | runs aligned | event recall | extra events | event dt p95 [s] | centre err. [m] | wrong links | missed links | false merges | spurious U | identical graphs |
|---|---|--:|--:|--:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gnss | rtk | 1 | 4 | 0 | 1.000 | 1.000 | 1.000 | 0.853 | 11.0 | 0.450 | 0.209 | 0.0 | 0.0 | 0.0 | 0.0 | 1/4 |
| gnss | degraded | 1 | 4 | 0 | 1.000 | 1.000 | 1.000 | 0.853 | 11.0 | 0.450 | 0.247 | 0.0 | 0.0 | 0.0 | 0.0 | 1/4 |
| radar_gnss_combined | gnss rtk + radar low | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0/1 |
| radar_gnss_combined | gnss rtk + radar nominal | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0/1 |
| radar_gnss_combined | gnss rtk + radar high | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 8.0 | 0.000 | 2.685 | 0.0 | 1.0 | 0.0 | 122.0 | 0/1 |
| radar_gnss_combined | gnss degraded + radar low | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0/1 |
| radar_gnss_combined | gnss degraded + radar nominal | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 0.0 | 0.000 | - | 0.0 | 0.0 | 0.0 | 0.0 | 0/1 |
| radar_gnss_combined | gnss degraded + radar high | 1 | 1 | 0 | 1.000 | 1.000 | 1.000 | 1.000 | 8.0 | 0.000 | 2.285 | 0.0 | 1.0 | 0.0 | 122.0 | 0/1 |
