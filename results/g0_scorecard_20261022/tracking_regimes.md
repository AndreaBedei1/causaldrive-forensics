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
