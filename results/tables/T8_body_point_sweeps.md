**T8_body_point_sweeps.**  Body-vs-point geometry on identical tracks, target-motion frame and body reference (sweeps).

| geometry | event | found | expected | matched | precision | recall | onset dt median [s] |
|---|---|---|---|---|---|---|---|
| point | EGO_PATH_ENTRY | 131 | 267 | 124 | 0.947 | 0.464 | 0.500 |
| point | CUT_IN_FROM_LEFT_START | 40 | 40 | 40 | 1.000 | 1.000 | 0.150 |
| point | CUT_IN_FROM_RIGHT_START | 73 | 153 | 71 | 0.973 | 0.464 | 0.050 |
| point | CRITICAL_TTC_START | 550 | 549 | 517 | 0.940 | 0.942 | 0.050 |
| body | EGO_PATH_ENTRY | 203 | 267 | 175 | 0.862 | 0.655 | 0.100 |
| body | CUT_IN_FROM_LEFT_START | 40 | 40 | 40 | 1.000 | 1.000 | -0.075 |
| body | CUT_IN_FROM_RIGHT_START | 116 | 153 | 111 | 0.957 | 0.726 | 0.000 |
| body | CRITICAL_TTC_START | 550 | 549 | 517 | 0.940 | 0.942 | 0.050 |

Pre-contact window. This isolates geometry; historical recalls under different definitions are not paired ablations.
