**T4_event_oracle_canonical.**  Core perception events before each recorder's first contact against the ground-truth event oracle (17 runs, canonical).

| comparison | event | expected | found | matched | precision | recall | dt median [s] | dt p5 / p95 [s] |
|---|---|---|---|---|---|---|---|---|
| reconstruction vs. COVERAGE | track appeared | 5 | 26 | 4 | 0.154 | 0.800 | 0.17 | +0.10 / +0.29 |
| reconstruction vs. COVERAGE | ego-path entry | 21 | 17 | 14 | 0.824 | 0.667 | 0.05 | -0.17 / +0.27 |
| reconstruction vs. COVERAGE | cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | 0.05 | +0.01 / +0.10 |
| reconstruction vs. COVERAGE | cut-in from right | 5 | 2 | 2 | 1.000 | 0.400 | -0.03 | -0.05 / -0.00 |
| reconstruction vs. COVERAGE | CRITICAL_TTC start | 40 | 39 | 38 | 0.974 | 0.950 | 0.05 | -0.10 / +0.65 |
| reconstruction vs. COVERAGE | CRITICAL_TTC end | 5 | 4 | 4 | 1.000 | 0.800 | -0.05 | -0.09 / -0.01 |
| reconstruction vs. COVERAGE_TRACKED | track appeared | 5 | 26 | 4 | 0.154 | 0.800 | 0.17 | +0.10 / +0.29 |
| reconstruction vs. COVERAGE_TRACKED | ego-path entry | 21 | 17 | 14 | 0.824 | 0.667 | 0.05 | -0.17 / +0.27 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | 0.05 | +0.01 / +0.10 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from right | 5 | 2 | 2 | 1.000 | 0.400 | -0.03 | -0.05 / -0.00 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC start | 40 | 39 | 38 | 0.974 | 0.950 | 0.05 | -0.10 / +0.65 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC end | 5 | 4 | 4 | 1.000 | 0.800 | -0.05 | -0.09 / -0.01 |
| COVERAGE_TRACKED vs. COVERAGE | track appeared | 5 | 5 | 5 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | ego-path entry | 21 | 21 | 21 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC start | 40 | 40 | 40 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC end | 5 | 5 | 5 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | ego-path entry | 21 | 21 | 21 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC start | 53 | 40 | 40 | 1.000 | 0.755 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC end | 7 | 5 | 5 | 1.000 | 0.714 | 0.00 | +0.00 / +0.00 |

COVERAGE: the reconstruction's definitions applied to ideal tracks from ground truth within the radar coverage (true nearest point); COVERAGE_TRACKED: the same with the point a radar track reports (median of the visible faces); PERFECT: an all-seeing sensor.  dt = found - expected (positive: later), matched within 2.0 s per recorder, event type and true subject.
