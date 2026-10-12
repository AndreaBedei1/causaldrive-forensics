# Core events against the ground-truth event oracle (sweeps)

Privileged evaluation (`cdf.evaluation.event_oracle`).  PERFECT: the reconstruction's own event definitions applied to an ideal track of every other vehicle built from ground truth (true near surface, velocity, acceleration and size; an all-seeing sensor).  COVERAGE: the same ideal track only where the vehicle was inside one of the recorder's radar fields of view and range with a clear line of sight.  RECONSTRUCTION: the recorder's own local events, the subject being the true identity of its track.  Events of one type, recorder and true subject matched one to one, nearest first, within 2.0 s; time difference = found - expected (positive: later).  Recorder clocks: local (the alignment plays no part here).

Runs: 240 (0 failed).  Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:15Z.

## RECONSTRUCTION vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 271 | 96 | 42 | 0.155 | 0.438 | +0.15 | -0.54 / +0.45 | 0.15 |
| ego-path entry | 203 | 267 | 175 | 0.862 | 0.655 | +0.10 | -0.20 / +0.25 | 0.10 |
| cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 116 | 153 | 111 | 0.957 | 0.726 | +0.00 | -0.25 / +0.25 | 0.05 |
| CRITICAL_TTC start | 550 | 549 | 517 | 0.940 | 0.942 | +0.05 | -0.10 / +0.55 | 0.10 |
| CRITICAL_TTC end | 157 | 155 | 132 | 0.841 | 0.852 | +0.00 | -0.05 / +0.14 | 0.05 |

## RECONSTRUCTION vs COVERAGE_TRACKED (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 271 | 96 | 42 | 0.155 | 0.438 | +0.15 | -0.54 / +0.45 | 0.15 |
| ego-path entry | 203 | 267 | 175 | 0.862 | 0.655 | +0.10 | -0.20 / +0.25 | 0.10 |
| cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 116 | 153 | 111 | 0.957 | 0.726 | +0.00 | -0.25 / +0.25 | 0.05 |
| CRITICAL_TTC start | 550 | 549 | 517 | 0.940 | 0.942 | +0.05 | -0.10 / +0.55 | 0.10 |
| CRITICAL_TTC end | 157 | 155 | 132 | 0.841 | 0.852 | +0.00 | -0.05 / +0.14 | 0.05 |

## RECONSTRUCTION vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 203 | 267 | 175 | 0.862 | 0.655 | +0.10 | -0.20 / +0.25 | 0.10 |
| cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 116 | 153 | 111 | 0.957 | 0.726 | +0.00 | -0.25 / +0.25 | 0.05 |
| CRITICAL_TTC start | 550 | 621 | 517 | 0.940 | 0.833 | +0.05 | -0.10 / +0.66 | 0.10 |
| CRITICAL_TTC end | 157 | 189 | 134 | 0.854 | 0.709 | +0.00 | -0.05 / +0.12 | 0.05 |

## COVERAGE_TRACKED vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 96 | 96 | 96 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 267 | 267 | 267 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 153 | 153 | 153 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 549 | 549 | 549 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 155 | 155 | 155 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |

## COVERAGE vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 267 | 267 | 267 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 40 | 40 | 40 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 153 | 153 | 153 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 549 | 621 | 548 | 0.998 | 0.882 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 155 | 189 | 155 | 1.000 | 0.820 | +0.00 | +0.00 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 375 | 127 | 92 | 0.245 | 0.724 | +0.20 | -0.72 / +0.62 | 0.40 |
| ego-path entry | 489 | 485 | 330 | 0.675 | 0.680 | +0.10 | -0.15 / +1.45 | 0.15 |
| cut-in from left | 40 | 41 | 40 | 1.000 | 0.976 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 160 | 339 | 154 | 0.963 | 0.454 | +0.00 | -0.25 / +0.30 | 0.05 |
| CRITICAL_TTC start | 571 | 576 | 531 | 0.930 | 0.922 | +0.05 | -0.10 / +0.53 | 0.10 |
| CRITICAL_TTC end | 493 | 504 | 463 | 0.939 | 0.919 | +0.00 | -0.05 / +0.25 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 375 | 127 | 92 | 0.245 | 0.724 | +0.20 | -0.72 / +0.62 | 0.40 |
| ego-path entry | 489 | 485 | 330 | 0.675 | 0.680 | +0.10 | -0.15 / +1.45 | 0.15 |
| cut-in from left | 40 | 41 | 40 | 1.000 | 0.976 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 160 | 339 | 154 | 0.963 | 0.454 | +0.00 | -0.25 / +0.30 | 0.05 |
| CRITICAL_TTC start | 571 | 576 | 531 | 0.930 | 0.922 | +0.05 | -0.10 / +0.53 | 0.10 |
| CRITICAL_TTC end | 493 | 504 | 463 | 0.939 | 0.919 | +0.00 | -0.05 / +0.25 | 0.00 |

## RECONSTRUCTION vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 489 | 485 | 330 | 0.675 | 0.680 | +0.10 | -0.15 / +1.45 | 0.15 |
| cut-in from left | 40 | 41 | 40 | 1.000 | 0.976 | -0.07 | -0.21 / +0.20 | 0.10 |
| cut-in from right | 160 | 373 | 154 | 0.963 | 0.413 | +0.00 | -0.25 / +0.30 | 0.05 |
| CRITICAL_TTC start | 571 | 648 | 531 | 0.930 | 0.819 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 493 | 552 | 465 | 0.943 | 0.842 | +0.00 | -0.05 / +0.25 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 127 | 127 | 127 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 485 | 485 | 485 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 41 | 41 | 41 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 339 | 339 | 339 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 576 | 576 | 576 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 504 | 504 | 504 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |

## COVERAGE vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 485 | 485 | 485 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 41 | 41 | 41 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 339 | 373 | 339 | 1.000 | 0.909 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 576 | 648 | 575 | 0.998 | 0.887 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 504 | 552 | 504 | 1.000 | 0.913 | +0.00 | +0.00 / +0.00 | 0.00 |

