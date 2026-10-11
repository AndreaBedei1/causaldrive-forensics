**T4_event_oracle_canonical.**  Core perception events before each recorder's first contact against the ground-truth event oracle (17 runs, canonical).

| comparison | event | expected | found | matched | precision | recall | dt median [s] | dt p5 / p95 [s] |
|---|---|---|---|---|---|---|---|---|
| reconstruction vs. COVERAGE | track appeared | 6 | 32 | 4 | 0.125 | 0.667 | 0.17 | +0.10 / +0.29 |
| reconstruction vs. COVERAGE | ego-path entry | 16 | 11 | 8 | 0.727 | 0.500 | 0.10 | +0.00 / +0.33 |
| reconstruction vs. COVERAGE | cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.40 | -0.45 / +0.05 |
| reconstruction vs. COVERAGE | cut-in from right | 5 | 1 | 1 | 1.000 | 0.200 | -0.25 | -0.25 / -0.25 |
| reconstruction vs. COVERAGE | CRITICAL_TTC start | 41 | 40 | 38 | 0.950 | 0.927 | 0.05 | -0.07 / +0.65 |
| reconstruction vs. COVERAGE | CRITICAL_TTC end | 6 | 4 | 4 | 1.000 | 0.667 | 0.00 | -0.09 / +0.00 |
| reconstruction vs. COVERAGE_TRACKED | track appeared | 6 | 32 | 4 | 0.125 | 0.667 | 0.17 | +0.10 / +0.29 |
| reconstruction vs. COVERAGE_TRACKED | ego-path entry | 9 | 11 | 8 | 0.727 | 0.889 | 0.05 | -0.05 / +0.38 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.25 | -0.29 / +0.15 |
| reconstruction vs. COVERAGE_TRACKED | cut-in from right | 2 | 1 | 1 | 1.000 | 0.500 | -0.15 | -0.15 / -0.15 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC start | 45 | 40 | 38 | 0.950 | 0.844 | 0.07 | -0.05 / +0.65 |
| reconstruction vs. COVERAGE_TRACKED | CRITICAL_TTC end | 6 | 4 | 4 | 1.000 | 0.667 | -0.15 | -0.15 / -0.11 |
| COVERAGE_TRACKED vs. COVERAGE | track appeared | 6 | 6 | 6 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | ego-path entry | 16 | 9 | 8 | 0.889 | 0.500 | 0.03 | -0.10 / +0.23 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.15 | -0.15 / -0.10 |
| COVERAGE_TRACKED vs. COVERAGE | cut-in from right | 5 | 2 | 1 | 0.500 | 0.200 | -0.10 | -0.10 / -0.10 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC start | 41 | 45 | 41 | 0.911 | 1.000 | 0.00 | -0.10 / +0.00 |
| COVERAGE_TRACKED vs. COVERAGE | CRITICAL_TTC end | 6 | 6 | 6 | 1.000 | 1.000 | 0.10 | +0.00 / +0.15 |
| COVERAGE vs. PERFECT | ego-path entry | 16 | 16 | 16 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC start | 55 | 41 | 41 | 1.000 | 0.746 | 0.00 | +0.00 / +0.00 |
| COVERAGE vs. PERFECT | CRITICAL_TTC end | 9 | 6 | 6 | 1.000 | 0.667 | 0.00 | +0.00 / +0.00 |

COVERAGE: the reconstruction's definitions applied to ideal tracks from ground truth within the radar coverage (true nearest point); COVERAGE_TRACKED: the same with the point a radar track reports (median of the visible faces); PERFECT: an all-seeing sensor.  dt = found - expected (positive: later), matched within 2.0 s per recorder, event type and true subject.
