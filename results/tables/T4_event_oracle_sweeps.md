**T4_event_oracle_sweeps.**  Core perception events before each recorder's first contact against the ground-truth event oracle (240 runs, sweeps).

| comparison | event | expected | found | matched | precision | recall | dt median [s] | dt p5 / p95 [s] |
|---|---|---|---|---|---|---|---|---|
| reconstruction vs. COVERAGE | track appeared | 96 | 271 | 42 | 0.155 | 0.438 | 0.15 | -0.54 / +0.45 |
| reconstruction vs. COVERAGE | ego-path entry | 267 | 203 | 175 | 0.862 | 0.655 | 0.10 | -0.20 / +0.25 |
| reconstruction vs. COVERAGE | cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | -0.07 | -0.21 / +0.20 |
| reconstruction vs. COVERAGE | cut-in from right | 153 | 116 | 111 | 0.957 | 0.726 | 0.00 | -0.25 / +0.25 |
| reconstruction vs. COVERAGE | CRITICAL_TTC start | 549 | 550 | 517 | 0.940 | 0.942 | 0.05 | -0.10 / +0.55 |
| reconstruction vs. COVERAGE | CRITICAL_TTC end | 155 | 157 | 132 | 0.841 | 0.852 | 0.00 | -0.05 / +0.14 |
| reconstruction vs. COVERAGE_TRACKED | track appeared | 96 | 271 | 42 | 0.155 | 0.438 | 0.15 | -0.54 / +0.45 |
| reconstruction vs. COVERAGE_TRACKED | ego-path entry | 267 | 203 | 175 | 0.862 | 0.655 | 0.10 | -0.20 / +0.25 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | -0.07 | -0.21 / +0.20 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from right | 153 | 116 | 111 | 0.957 | 0.726 | 0.00 | -0.25 / +0.25 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC start | 549 | 550 | 517 | 0.940 | 0.942 | 0.05 | -0.10 / +0.55 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC end | 155 | 157 | 132 | 0.841 | 0.852 | 0.00 | -0.05 / +0.14 |
| COVERAGE_TRACKED vs. COVERAGE | track appeared | 96 | 96 | 96 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | ego-path entry | 267 | 267 | 267 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from right | 153 | 153 | 153 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC start | 549 | 549 | 549 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC end | 155 | 155 | 155 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | ego-path entry | 267 | 267 | 267 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from right | 153 | 153 | 153 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC start | 621 | 549 | 548 | 0.998 | 0.882 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC end | 189 | 155 | 155 | 1.000 | 0.820 | 0.00 | +0.00 / +0.00 |

COVERAGE: the reconstruction's definitions applied to ideal tracks from ground truth within the radar coverage (true nearest point); COVERAGE_TRACKED: the same with the point a radar track reports (median of the visible faces); PERFECT: an all-seeing sensor.  dt = found - expected (positive: later), matched within 2.0 s per recorder, event type and true subject.
