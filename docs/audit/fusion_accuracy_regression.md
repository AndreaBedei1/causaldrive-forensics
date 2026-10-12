# Fusion accuracy regression decomposition

Diagnostic re-evaluation of stored historical fused states on the same recorder raw data,
physical timestamps and majority-identity truth, using one evaluator. This is a historical
comparison, not a claim that old algorithms were executed at the final analysis freeze.
Snapshots: pre-hardening (11dbc6d-equivalent saved baseline), pre-tracker (a095 snapshot),
pre-final (c706e025). Canonical S02 was replaced between these histories; it contributes no
anonymous fused states, so it does not affect this comparison. All other fusion raw recordings agree.
The paired-state CSV records every evaluated state, sources, method and fragmentation.

| snapshot | pure states | excluded impure | entities | pooled median [m] | median run medians [m] | box fit n / median [m] | CI n / median [m] |
|---|--:|--:|--:|--:|--:|---|---|
| pre_hardening | 925 | 107 | 14 | 0.446716 | 0.411482 | 390 / 0.271037 | 535 / 0.675488 |
| pre_tracker | 958 | 49 | 19 | 0.530348 | 0.721579 | 477 / 0.286264 | 481 / 0.972879 |
| pre_final | 733 | 12 | 13 | 0.355698 | 0.512451 | 461 / 0.266700 | 272 / 0.771747 |

The quoted 0.45 -> 0.53 m is reproduced (0.446716 -> 0.530348) by pooling
different pure-state populations. After segmentation, entities grow 14 -> 19,
and the impure states excluded from geometric evaluation fall 107 -> 49.
On the 789 shared physical instants the median instead changes 0.480391 -> 0.466442 m;
the median paired change is exactly zero. All 407 comparisons with the same sources
and method have identical geometry (maximum absolute error change zero).

CI 0.68 -> 0.97 m is also reproduced (0.675488 -> 0.972879), but CI states
decrease 535 -> 481 while box-fit states increase 390 -> 477. Thus the remaining
CI subset is a different, harder conditional population, not more CI fallback.
Box-fit median changes only 0.271037 -> 0.286264 m. There is no common-source
geometric degradation attributable to this segmentation change.

Robustness 0.41 -> 0.72 m reproduces 0.411482 -> 0.721579 **as median of run
medians**; it is not the pooled state median. Fragmented/new recorder ghosts
change the run populations and weighting. These statistics must not be interchanged.
The subsequent tracker fix reduces the pooled median to 0.355698 m and CI to
0.771747 m: 688 shared instants improve 0.388499 -> 0.359386 m, with median paired
change zero. Here geometry does change on some equal-source/method states (max
1.947710 m), consistent with changed track estimates rather than an evaluation relabel.

Metric correction: the single-track comparator is now the median source error
once per entity/physical instant, paired with one fused error. Previously, a state
with several sources contributed several single-track errors but one fused error.
The primary fused metric and identity-purity exclusions are unchanged. The CSV
allows comparison by method, source count and fragmented vs nonfragmented identity.
No threshold was adjusted to improve these medians or reopen unsafe merges.

Final frozen-state accuracy is reported separately in `traces/fusion_metrics.json`
and `docs/FINAL_VALIDATION_REPORT.md`; final result tables contain only that run.

## Conditional source and fragmentation populations

| snapshot | subset | states | paired states | paired fused median [m] | paired single-source median [m] |
|---|---|--:|--:|--:|--:|
| pre_hardening | one source | 328 | 328 | 0.762443034705392 | 0.8351648159074156 |
| pre_hardening | multiple sources | 597 | 596 | 0.36363937336421576 | 0.639619655822739 |
| pre_hardening | fragmented identity | 530 | 530 | 0.41666732371578535 | 0.451140860039008 |
| pre_hardening | one entity per identity | 395 | 394 | 0.5040962996559666 | 0.8703488946813853 |
| pre_hardening | true non-recorder | 804 | 803 | 0.3887007119047798 | 0.6168231444508773 |
| pre_tracker | one source | 335 | 335 | 0.9885992858272288 | 1.3523563530929805 |
| pre_tracker | multiple sources | 623 | 622 | 0.35647182505126573 | 0.6147475479383682 |
| pre_tracker | fragmented identity | 569 | 569 | 0.6197279210205907 | 0.7311312349239597 |
| pre_tracker | one entity per identity | 389 | 388 | 0.4217873116860984 | 0.911844540119154 |
| pre_tracker | true non-recorder | 724 | 723 | 0.3781924534850511 | 0.6389724098167837 |
| pre_final | one source | 110 | 110 | 0.8356625539169438 | 0.871134773902986 |
| pre_final | multiple sources | 623 | 622 | 0.3142447168482635 | 0.5712506787376482 |
| pre_final | fragmented identity | 339 | 339 | 0.5022277396489787 | 0.724738103051342 |
| pre_final | one entity per identity | 394 | 393 | 0.28605994480476704 | 0.5270309457761988 |
| pre_final | true non-recorder | 718 | 717 | 0.34721202068929125 | 0.6089743552873453 |

### Same physical instant and method

| comparison | method | shared instants | before [m] | after [m] | median paired change [m] |
|---|---|--:|--:|--:|--:|
| pre_hardening → pre_tracker | box_fit | 367 | 0.271238 | 0.270429 | 0.000000 |
| pre_hardening → pre_tracker | covariance_intersection | 362 | 0.918131 | 0.919970 | 0.000000 |
| pre_tracker → pre_final | box_fit | 423 | 0.277577 | 0.259733 | 0.000000 |
| pre_tracker → pre_final | covariance_intersection | 250 | 0.813546 | 0.805948 | 0.000000 |
