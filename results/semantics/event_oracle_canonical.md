# Core events against the ground-truth event oracle (canonical)

Privileged evaluation (`cdf.evaluation.event_oracle`).  PERFECT: the reconstruction's own event definitions applied to an ideal track of every other vehicle built from ground truth (true near surface, velocity, acceleration and size; an all-seeing sensor).  COVERAGE: the same ideal track only where the vehicle was inside one of the recorder's radar fields of view and range with a clear line of sight.  RECONSTRUCTION: the recorder's own local events, the subject being the true identity of its track.  Events of one type, recorder and true subject matched one to one, nearest first, within 2.0 s; time difference = found - expected (positive: later).  Recorder clocks: local (the alignment plays no part here).

Runs: 17 (0 failed).  Provenance: code `b6bc47487dabcc94`, configuration `0b5c899acef9146c`, commit `8d7343d36cf3f3ebfc2baecb2fcb302273c698f5`, 2026-10-12T12:32:10Z.

## RECONSTRUCTION vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 26 | 5 | 4 | 0.154 | 0.800 | +0.17 | +0.10 / +0.29 | 0.17 |
| ego-path entry | 17 | 21 | 14 | 0.824 | 0.667 | +0.05 | -0.17 / +0.27 | 0.12 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 2 | 5 | 2 | 1.000 | 0.400 | -0.03 | -0.05 / -0.00 | 0.03 |
| CRITICAL_TTC start | 39 | 40 | 38 | 0.974 | 0.950 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 4 | 5 | 4 | 1.000 | 0.800 | -0.05 | -0.09 / -0.01 | 0.05 |

## RECONSTRUCTION vs COVERAGE_TRACKED (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 26 | 5 | 4 | 0.154 | 0.800 | +0.17 | +0.10 / +0.29 | 0.17 |
| ego-path entry | 17 | 21 | 14 | 0.824 | 0.667 | +0.05 | -0.17 / +0.27 | 0.12 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 2 | 5 | 2 | 1.000 | 0.400 | -0.03 | -0.05 / -0.00 | 0.03 |
| CRITICAL_TTC start | 39 | 40 | 38 | 0.974 | 0.950 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 4 | 5 | 4 | 1.000 | 0.800 | -0.05 | -0.09 / -0.01 | 0.05 |

## RECONSTRUCTION vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 17 | 21 | 14 | 0.824 | 0.667 | +0.05 | -0.17 / +0.27 | 0.12 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 2 | 5 | 2 | 1.000 | 0.400 | -0.03 | -0.05 / -0.00 | 0.03 |
| CRITICAL_TTC start | 39 | 53 | 38 | 0.974 | 0.717 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 4 | 7 | 4 | 1.000 | 0.571 | -0.05 | -0.09 / -0.01 | 0.05 |

## COVERAGE_TRACKED vs COVERAGE (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 5 | 5 | 5 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 21 | 21 | 21 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 40 | 40 | 40 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 5 | 5 | 5 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |

## COVERAGE vs PERFECT (before each recorder's first contact)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 21 | 21 | 21 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 5 | 5 | 5 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 40 | 53 | 40 | 1.000 | 0.755 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 5 | 7 | 5 | 1.000 | 0.714 | +0.00 | +0.00 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 32 | 7 | 6 | 0.188 | 0.857 | +0.17 | -0.28 / +0.41 | 0.28 |
| ego-path entry | 34 | 31 | 23 | 0.676 | 0.742 | +0.10 | -0.15 / +1.50 | 0.15 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 4 | 13 | 4 | 1.000 | 0.308 | +0.00 | -0.04 / +0.09 | 0.03 |
| CRITICAL_TTC start | 40 | 40 | 38 | 0.950 | 0.950 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 37 | 40 | 37 | 1.000 | 0.925 | +0.00 | -0.06 / +0.00 | 0.00 |

## RECONSTRUCTION vs COVERAGE_TRACKED (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 32 | 7 | 6 | 0.188 | 0.857 | +0.17 | -0.28 / +0.41 | 0.28 |
| ego-path entry | 34 | 31 | 23 | 0.676 | 0.742 | +0.10 | -0.15 / +1.50 | 0.15 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 4 | 13 | 4 | 1.000 | 0.308 | +0.00 | -0.04 / +0.09 | 0.03 |
| CRITICAL_TTC start | 40 | 40 | 38 | 0.950 | 0.950 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 37 | 40 | 37 | 1.000 | 0.925 | +0.00 | -0.06 / +0.00 | 0.00 |

## RECONSTRUCTION vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 34 | 31 | 23 | 0.676 | 0.742 | +0.10 | -0.15 / +1.50 | 0.15 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.05 | +0.01 / +0.10 | 0.05 |
| cut-in from right | 4 | 14 | 4 | 1.000 | 0.286 | +0.00 | -0.04 / +0.09 | 0.03 |
| CRITICAL_TTC start | 40 | 54 | 38 | 0.950 | 0.704 | +0.05 | -0.10 / +0.65 | 0.10 |
| CRITICAL_TTC end | 37 | 54 | 37 | 1.000 | 0.685 | +0.00 | -0.06 / +0.00 | 0.00 |

## COVERAGE_TRACKED vs COVERAGE (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| track appeared | 7 | 7 | 7 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| ego-path entry | 31 | 31 | 31 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 13 | 13 | 13 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 40 | 40 | 40 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 40 | 40 | 40 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |

## COVERAGE vs PERFECT (whole recording)

| event | found | expected | matched | precision | recall | dt median [s] | dt p5 / p95 [s] | |dt| median [s] |
|---|--:|--:|--:|--:|--:|--:|--:|--:|
| ego-path entry | 31 | 31 | 31 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from left | 2 | 2 | 2 | 1.000 | 1.000 | +0.00 | +0.00 / +0.00 | 0.00 |
| cut-in from right | 13 | 14 | 13 | 1.000 | 0.929 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC start | 40 | 54 | 40 | 1.000 | 0.741 | +0.00 | +0.00 / +0.00 | 0.00 |
| CRITICAL_TTC end | 40 | 54 | 40 | 1.000 | 0.741 | +0.00 | +0.00 / +0.00 | 0.00 |

