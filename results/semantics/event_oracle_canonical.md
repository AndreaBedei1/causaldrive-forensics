# Core events against the ground-truth event oracle (canonical)

Privileged evaluation (`cdf.evaluation.event_oracle`).  PERFECT: the reconstruction's own event definitions applied to an ideal track of every other vehicle built from ground truth (true near surface, velocity, acceleration and size; an all-seeing sensor).  COVERAGE: the same ideal track only where the vehicle was inside one of the recorder's radar fields of view and range with a clear line of sight.  RECONSTRUCTION: the recorder's own local events, the subject being the true identity of its track.  Events of one type, recorder and true subject matched one to one, nearest first, within 2.0 s; time difference = found - expected (positive: later).  Recorder clocks: local (the alignment plays no part here).

Runs: 17 (0 failed).  Provenance: code `c76d72a3965907b6`, configuration `50f7dc9e35556156`, commit `fd8d2baed644db4a32c2eb502a2eeb9b32f70887` (uncommitted changes), 2026-10-11T09:35:15Z.

## RECONSTRUCTION vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 32 | 6 | 4 | 0.125 | 0.667 | +0.17 | +0.10 / +0.29 | 0.17 |
| ego-path entry | 11 | 16 | 8 | 0.727 | 0.500 | +0.10 | +0.00 / +0.33 | 0.10 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.40 | -0.45 / +0.05 | 0.40 |
| cut-in from right | 1 | 5 | 1 | 1.000 | 0.200 | -0.25 | -0.25 / -0.25 | 0.25 |
| CRITICAL_TTC start | 40 | 41 | 38 | 0.950 | 0.927 | +0.05 | -0.07 / +0.65 | 0.10 |
| CRITICAL_TTC end | 4 | 6 | 4 | 1.000 | 0.667 | +0.00 | -0.09 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 32 | 6 | 4 | 0.125 | 0.667 | +0.17 | +0.10 / +0.29 | 0.17 |
| ego-path entry | 11 | 9 | 8 | 0.727 | 0.889 | +0.05 | -0.05 / +0.38 | 0.05 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.25 | -0.29 / +0.15 | 0.25 |
| cut-in from right | 1 | 2 | 1 | 1.000 | 0.500 | -0.15 | -0.15 / -0.15 | 0.15 |
| CRITICAL_TTC start | 40 | 45 | 38 | 0.950 | 0.844 | +0.07 | -0.05 / +0.65 | 0.10 |
| CRITICAL_TTC end | 4 | 6 | 4 | 1.000 | 0.667 | -0.15 | -0.15 / -0.11 | 0.15 |

## RECONSTRUCTION vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 11 | 16 | 8 | 0.727 | 0.500 | +0.10 | +0.00 / +0.33 | 0.10 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.40 | -0.45 / +0.05 | 0.40 |
| cut-in from right | 1 | 5 | 1 | 1.000 | 0.200 | -0.25 | -0.25 / -0.25 | 0.25 |
| CRITICAL_TTC start | 40 | 55 | 38 | 0.950 | 0.691 | +0.05 | -0.07 / +0.66 | 0.10 |
| CRITICAL_TTC end | 4 | 9 | 4 | 1.000 | 0.444 | +0.00 | -0.09 / +0.00 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 6 | 6 | 6 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 9 | 16 | 8 | 0.889 | 0.500 | +0.03 | -0.10 / +0.23 | 0.10 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.15 | -0.15 / -0.10 | 0.15 |
| cut-in from right | 2 | 5 | 1 | 0.500 | 0.200 | -0.10 | -0.10 / -0.10 | 0.10 |
| CRITICAL_TTC start | 45 | 41 | 41 | 0.911 | 1.000 | +0.00 | -0.10 / +0.00 | 0.00 |
| CRITICAL_TTC end | 6 | 6 | 6 | 1.000 | 1.000 | +0.10 | +0.00 / +0.15 | 0.10 |

## COVERAGE vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 16 | 16 | 16 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 41 | 55 | 41 | 1.000 | 0.746 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 6 | 9 | 6 | 1.000 | 0.667 | +0.00 | +0.00 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 39 | 8 | 6 | 0.154 | 0.750 | +0.17 | -0.28 / +0.41 | 0.28 |
| ego-path entry | 15 | 25 | 12 | 0.800 | 0.480 | +0.15 | +0.00 / +0.99 | 0.15 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.40 | -0.45 / +0.05 | 0.40 |
| cut-in from right | 3 | 15 | 3 | 1.000 | 0.200 | -0.25 | -0.25 / -0.20 | 0.25 |
| CRITICAL_TTC start | 41 | 44 | 39 | 0.951 | 0.886 | +0.05 | -0.15 / +0.65 | 0.10 |
| CRITICAL_TTC end | 37 | 44 | 37 | 1.000 | 0.841 | +0.00 | -0.02 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 39 | 8 | 6 | 0.154 | 0.750 | +0.17 | -0.28 / +0.41 | 0.28 |
| ego-path entry | 15 | 17 | 10 | 0.667 | 0.588 | +0.05 | -0.05 / +0.48 | 0.05 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.25 | -0.29 / +0.15 | 0.25 |
| cut-in from right | 3 | 12 | 3 | 1.000 | 0.250 | -0.15 | -0.15 / -0.15 | 0.15 |
| CRITICAL_TTC start | 41 | 48 | 39 | 0.951 | 0.812 | +0.05 | -0.06 / +0.65 | 0.10 |
| CRITICAL_TTC end | 37 | 47 | 37 | 1.000 | 0.787 | +0.00 | -0.15 / +0.00 | 0.00 |

## RECONSTRUCTION vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 15 | 25 | 12 | 0.800 | 0.480 | +0.15 | +0.00 / +0.99 | 0.15 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.40 | -0.45 / +0.05 | 0.40 |
| cut-in from right | 3 | 15 | 3 | 1.000 | 0.200 | -0.25 | -0.25 / -0.20 | 0.25 |
| CRITICAL_TTC start | 41 | 59 | 39 | 0.951 | 0.661 | +0.05 | -0.15 / +0.66 | 0.10 |
| CRITICAL_TTC end | 37 | 59 | 37 | 1.000 | 0.627 | +0.00 | -0.02 / +0.00 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 8 | 8 | 8 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 17 | 25 | 16 | 0.941 | 0.640 | -0.05 | -0.11 / +0.21 | 0.10 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | -0.15 | -0.15 / -0.10 | 0.15 |
| cut-in from right | 12 | 15 | 11 | 0.917 | 0.733 | -0.10 | -0.10 / -0.07 | 0.10 |
| CRITICAL_TTC start | 48 | 44 | 44 | 0.917 | 1.000 | +0.00 | -0.10 / +0.00 | 0.00 |
| CRITICAL_TTC end | 47 | 44 | 44 | 0.936 | 1.000 | +0.00 | +0.00 / +0.15 | 0.00 |

## COVERAGE vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 25 | 25 | 25 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 3 | 3 | 3 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 15 | 15 | 15 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 44 | 59 | 44 | 1.000 | 0.746 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 44 | 59 | 44 | 1.000 | 0.746 | +0.00 | +0.00 / +0.00 | 0.00 |

