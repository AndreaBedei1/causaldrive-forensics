# Fused road users: errors by motion regime (diagnostic)

All pure fused road users of the runs; thresholds: braking >= 2.0 m/s2 along the velocity, turning >= 5.0 deg/s, after contact split at 3.0 s (`scripts/tracking_regimes.py`).

| regime | samples | centre median [m] | centre P95 [m] | centre RMSE [m] | speed median [m/s] | speed P95 [m/s] |
|---|---:|---:|---:|---:|---:|---:|
| steady | 3259 | 0.205 | 0.734 | 0.416 | 0.032 | 0.308 |
| braking | 1 | 0.484 | 0.484 | 0.484 | 0.004 | 0.004 |
| turning | 1127 | 0.325 | 1.023 | 0.514 | 0.055 | 0.314 |
| after contact (0-3 s) | 0 | - | - | - | - | - |
| after contact (> 3 s) | 0 | - | - | - | - | - |
| one recorder | 641 | 0.465 | 1.650 | 0.804 | 0.110 | 0.394 |
| several recorders | 3746 | 0.220 | 0.671 | 0.346 | 0.032 | 0.246 |

## Radar tracks of the recorders, seen by another recorder

Distance from the track point (the tracker's estimate, on the near side of the body) to the true body outline of the tracked recorder (0 on or inside it), and speed error, by the tracked recorder's motion.

| regime | samples | measured | body distance median [m] | body distance P95 [m] | speed median [m/s] | speed P95 [m/s] |
|---|---:|---:|---:|---:|---:|---:|
| steady | 2250 | 0.991 | 0.000 | 0.000 | 0.060 | 0.549 |
| braking | 134 | 0.993 | 0.000 | 0.000 | 0.105 | 1.248 |
| turning | 354 | 0.994 | 0.000 | 0.106 | 0.125 | 0.667 |
| after contact (0-3 s) | 1303 | 0.994 | 0.000 | 0.000 | 0.072 | 0.435 |
| after contact (> 3 s) | 1927 | 1.000 | 0.000 | 0.000 | 0.007 | 0.076 |
