# Core events against the ground-truth event oracle (sweeps)

Privileged evaluation (`cdf.evaluation.event_oracle`).  PERFECT: the reconstruction's own event definitions applied to an ideal track of every other vehicle built from ground truth (true near surface, velocity, acceleration and size; an all-seeing sensor).  COVERAGE: the same ideal track only where the vehicle was inside one of the recorder's radar fields of view and range with a clear line of sight.  RECONSTRUCTION: the recorder's own local events, the subject being the true identity of its track.  Events of one type, recorder and true subject matched one to one, nearest first, within 2.0 s; time difference = found - expected (positive: later).  Recorder clocks: local (the alignment plays no part here).

Runs: 240 (0 failed).  Provenance: code `c76d72a3965907b6`, configuration `50f7dc9e35556156`, commit `fd8d2baed644db4a32c2eb502a2eeb9b32f70887` (uncommitted changes), 2026-10-11T09:35:33Z.

## RECONSTRUCTION vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 281 | 96 | 42 | 0.149 | 0.438 | +0.15 | -0.54 / +0.45 | 0.15 |
| ego-path entry | 129 | 246 | 124 | 0.961 | 0.504 | +0.20 | -0.14 / +0.35 | 0.20 |
| cut-in from left | 41 | 57 | 41 | 1.000 | 0.719 | -0.30 | -0.45 / -0.05 | 0.30 |
| cut-in from right | 65 | 136 | 60 | 0.923 | 0.441 | -0.25 | -0.30 / -0.10 | 0.25 |
| CRITICAL_TTC start | 551 | 552 | 515 | 0.935 | 0.933 | +0.05 | -0.10 / +0.45 | 0.10 |
| CRITICAL_TTC end | 156 | 145 | 122 | 0.782 | 0.841 | +0.00 | -0.05 / +0.05 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 281 | 96 | 42 | 0.149 | 0.438 | +0.15 | -0.54 / +0.45 | 0.15 |
| ego-path entry | 129 | 139 | 119 | 0.922 | 0.856 | +0.20 | -0.05 / +0.50 | 0.20 |
| cut-in from left | 41 | 40 | 39 | 0.951 | 0.975 | -0.20 | -0.35 / +0.05 | 0.20 |
| cut-in from right | 65 | 89 | 59 | 0.908 | 0.663 | -0.15 | -0.30 / +1.31 | 0.15 |
| CRITICAL_TTC start | 551 | 620 | 517 | 0.938 | 0.834 | +0.05 | -0.10 / +0.51 | 0.10 |
| CRITICAL_TTC end | 156 | 150 | 123 | 0.788 | 0.820 | -0.10 | -0.20 / +0.05 | 0.15 |

## RECONSTRUCTION vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 129 | 246 | 124 | 0.961 | 0.504 | +0.20 | -0.14 / +0.35 | 0.20 |
| cut-in from left | 41 | 57 | 41 | 1.000 | 0.719 | -0.30 | -0.45 / -0.05 | 0.30 |
| cut-in from right | 65 | 136 | 60 | 0.923 | 0.441 | -0.25 | -0.30 / -0.10 | 0.25 |
| CRITICAL_TTC start | 551 | 631 | 515 | 0.935 | 0.816 | +0.05 | -0.10 / +0.60 | 0.10 |
| CRITICAL_TTC end | 156 | 186 | 124 | 0.795 | 0.667 | +0.00 | -0.09 / +0.05 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 96 | 96 | 96 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 139 | 246 | 137 | 0.986 | 0.557 | -0.10 | -0.20 / +0.15 | 0.10 |
| cut-in from left | 40 | 57 | 40 | 1.000 | 0.702 | -0.10 | -0.15 / -0.05 | 0.10 |
| cut-in from right | 89 | 136 | 58 | 0.652 | 0.426 | -0.10 | -0.35 / +0.00 | 0.10 |
| CRITICAL_TTC start | 620 | 552 | 537 | 0.866 | 0.973 | +0.00 | -0.10 / +0.00 | 0.00 |
| CRITICAL_TTC end | 150 | 145 | 129 | 0.860 | 0.890 | +0.00 | +0.00 / +0.15 | 0.00 |

## COVERAGE vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 246 | 246 | 246 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 57 | 57 | 57 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 136 | 136 | 136 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 552 | 631 | 551 | 0.998 | 0.873 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 145 | 186 | 145 | 1.000 | 0.780 | +0.00 | +0.00 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 399 | 127 | 92 | 0.231 | 0.724 | +0.20 | -0.72 / +0.62 | 0.40 |
| ego-path entry | 212 | 450 | 194 | 0.915 | 0.431 | +0.25 | -0.15 / +1.52 | 0.25 |
| cut-in from left | 43 | 59 | 43 | 1.000 | 0.729 | -0.30 | -0.45 / +0.14 | 0.35 |
| cut-in from right | 107 | 312 | 90 | 0.841 | 0.288 | -0.20 | -0.30 / +0.20 | 0.25 |
| CRITICAL_TTC start | 565 | 600 | 526 | 0.931 | 0.877 | +0.05 | -0.10 / +0.45 | 0.10 |
| CRITICAL_TTC end | 486 | 527 | 461 | 0.949 | 0.875 | +0.00 | -0.05 / +0.25 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 399 | 127 | 92 | 0.231 | 0.724 | +0.20 | -0.72 / +0.62 | 0.40 |
| ego-path entry | 212 | 353 | 180 | 0.849 | 0.510 | +0.25 | -0.10 / +0.95 | 0.25 |
| cut-in from left | 43 | 40 | 39 | 0.907 | 0.975 | -0.20 | -0.35 / +0.05 | 0.20 |
| cut-in from right | 107 | 270 | 89 | 0.832 | 0.330 | -0.10 | -0.25 / +0.63 | 0.10 |
| CRITICAL_TTC start | 565 | 660 | 523 | 0.926 | 0.792 | +0.05 | -0.10 / +0.50 | 0.10 |
| CRITICAL_TTC end | 486 | 580 | 466 | 0.959 | 0.803 | +0.00 | -0.19 / +0.19 | 0.00 |

## RECONSTRUCTION vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 212 | 450 | 194 | 0.915 | 0.431 | +0.25 | -0.15 / +1.52 | 0.25 |
| cut-in from left | 43 | 59 | 43 | 1.000 | 0.729 | -0.30 | -0.45 / +0.14 | 0.35 |
| cut-in from right | 107 | 312 | 90 | 0.841 | 0.288 | -0.20 | -0.30 / +0.20 | 0.25 |
| CRITICAL_TTC start | 565 | 679 | 526 | 0.931 | 0.775 | +0.05 | -0.10 / +0.60 | 0.10 |
| CRITICAL_TTC end | 486 | 582 | 463 | 0.953 | 0.795 | +0.00 | -0.10 / +0.25 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 127 | 127 | 127 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 353 | 450 | 338 | 0.958 | 0.751 | -0.10 | -0.15 / +0.15 | 0.10 |
| cut-in from left | 40 | 59 | 40 | 1.000 | 0.678 | -0.10 | -0.15 / -0.05 | 0.10 |
| cut-in from right | 270 | 312 | 234 | 0.867 | 0.750 | -0.10 | -0.15 / -0.05 | 0.10 |
| CRITICAL_TTC start | 660 | 600 | 578 | 0.876 | 0.963 | +0.00 | -0.10 / +0.00 | 0.00 |
| CRITICAL_TTC end | 580 | 527 | 510 | 0.879 | 0.968 | +0.00 | +0.00 / +0.15 | 0.00 |

## COVERAGE vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 450 | 450 | 450 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 59 | 59 | 59 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 312 | 312 | 312 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 600 | 679 | 599 | 0.998 | 0.882 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 527 | 582 | 527 | 1.000 | 0.905 | +0.00 | +0.00 / +0.00 | 0.00 |

