# Three-method identity study (_S18_heldout)

Privileged evaluation of `scripts/retrospective_study.py`; provenance at the end.  Counts per draw (summed over runs, averaged over seeds); shares over all measured samples.

| condition | method | seeds | merges_correct | merges_false | merges_missed | links_wrong | links_missed | duplicate_entities | correct_share | wrong_share | unresolved_share | early_correct_share | early_wrong_share | retrospective_resolved | retrospective_correct |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| consumer | current | 10 | 14.0 | 20.1 | 10.0 | 0.0 | 0.0 | 2.5 | 0.7532 | 0.2158 | 0.0311 | 0.7064 | 0.2577 | 0 | 0 |
| consumer | corrected | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer | retrospective | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.5 | current | 10 | 14.0 | 20.4 | 10.0 | 0.0 | 0.0 | 2.6 | 0.7459 | 0.2176 | 0.0365 | 0.701 | 0.2577 | 0 | 0 |
| consumer_common_0.5 | corrected | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.5 | retrospective | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.9 | current | 10 | 14.0 | 20.4 | 10.0 | 0.0 | 0.0 | 2.6 | 0.7459 | 0.2176 | 0.0365 | 0.701 | 0.2577 | 0 | 0 |
| consumer_common_0.9 | corrected | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.9 | retrospective | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_1.0 | current | 10 | 14.0 | 20.7 | 10.0 | 0.0 | 0.0 | 2.0 | 0.7842 | 0.2119 | 0.0039 | 0.7333 | 0.2577 | 0 | 0 |
| consumer_common_1.0 | corrected | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_1.0 | retrospective | 10 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | current | 1 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | corrected | 1 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | retrospective | 1 | 16.0 | 0.0 | 8.0 | 0.0 | 0.0 | 3.0 | 0.9731 | 0.0056 | 0.0213 | 0.9385 | 0.0128 | 1 | 1 |
| rtk | current | 10 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| rtk | corrected | 10 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| rtk | retrospective | 10 | 16.0 | 0.0 | 8.0 | 0.0 | 0.0 | 3.0 | 0.9731 | 0.0056 | 0.0213 | 0.9385 | 0.0128 | 10 | 10 |

## Collisions

| condition | method | recall | wrong pairings | unmatched true contacts | ambiguous refusals | recorders aligned |
|---|---|---|--:|--:|--:|---|
| consumer | current | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer | corrected | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer | retrospective | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.5 | current | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.5 | corrected | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.5 | retrospective | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.9 | current | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.9 | corrected | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_0.9 | retrospective | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_1.0 | current | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_1.0 | corrected | 30/30 | 0 | 0 | 0 | 60/60 |
| consumer_common_1.0 | retrospective | 30/30 | 0 | 0 | 0 | 60/60 |
| exact | current | 3/3 | 0 | 0 | 0 | 6/6 |
| exact | corrected | 3/3 | 0 | 0 | 0 | 6/6 |
| exact | retrospective | 3/3 | 0 | 0 | 0 | 6/6 |
| rtk | current | 30/30 | 0 | 0 | 0 | 60/60 |
| rtk | corrected | 30/30 | 0 | 0 | 0 | 60/60 |
| rtk | retrospective | 30/30 | 0 | 0 | 0 | 60/60 |

## Range from the observing radar (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 1.0 / 0.0 / 0.0 (7590) | 1.0 / 0.0 / 0.0 (7590) | 1.0 / 0.0 / 0.0 (7590) |
| 10-20 | 0.9212 / 0.0164 / 0.0624 (6699) | 0.9212 / 0.0164 / 0.0624 (6699) | 0.9212 / 0.0164 / 0.0624 (6699) |
| 20-30 | 0.9499 / 0.0 / 0.0501 (4169) | 0.9499 / 0.0 / 0.0501 (4169) | 1.0 / 0.0 / 0.0 (4169) |
| 30-40 | 0.8923 / 0.0 / 0.1077 (715) | 0.8923 / 0.0 / 0.1077 (715) | 1.0 / 0.0 / 0.0 (715) |
| 40-50 | 0.8438 / 0.0 / 0.1562 (352) | 0.8438 / 0.0 / 0.1562 (352) | 1.0 / 0.0 / 0.0 (352) |
| 50-60 | 0.9167 / 0.0 / 0.0833 (132) | 0.9167 / 0.0 / 0.0833 (132) | 1.0 / 0.0 / 0.0 (132) |
| 60+ | - | - | - |

## Range from the observing radar (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 1.0 / 0.0 / 0.0 (27600) | 1.0 / 0.0 / 0.0 (27600) | 1.0 / 0.0 / 0.0 (27600) |
| 10-20 | 0.6596 / 0.2759 / 0.0645 (24360) | 0.9212 / 0.0164 / 0.0624 (24360) | 0.9212 / 0.0164 / 0.0624 (24360) |
| 20-30 | 0.5281 / 0.4629 / 0.009 (15160) | 0.9499 / 0.0 / 0.0501 (15160) | 0.9499 / 0.0 / 0.0501 (15160) |
| 30-40 | 0.5527 / 0.4015 / 0.0458 (2600) | 0.8923 / 0.0 / 0.1077 (2600) | 0.8923 / 0.0 / 0.1077 (2600) |
| 40-50 | 0.6188 / 0.3281 / 0.0531 (1280) | 0.8438 / 0.0 / 0.1562 (1280) | 0.8438 / 0.0 / 0.1562 (1280) |
| 50-60 | 0.4771 / 0.4521 / 0.0708 (480) | 0.9167 / 0.0 / 0.0833 (480) | 0.9167 / 0.0 / 0.0833 (480) |
| 60+ | - | - | - |

## Time before the observer's first contact (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 1.0 / 0.0 / 0.0 (935) | 1.0 / 0.0 / 0.0 (935) | 1.0 / 0.0 / 0.0 (935) |
| 0.5-1 | 1.0 / 0.0 / 0.0 (847) | 1.0 / 0.0 / 0.0 (847) | 1.0 / 0.0 / 0.0 (847) |
| 1-2 | 1.0 / 0.0 / 0.0 (1903) | 1.0 / 0.0 / 0.0 (1903) | 1.0 / 0.0 / 0.0 (1903) |
| 2-4 | 0.9499 / 0.0211 / 0.029 (4169) | 0.9499 / 0.0211 / 0.029 (4169) | 0.9499 / 0.0211 / 0.029 (4169) |
| 4+ | 0.9311 / 0.0048 / 0.0641 (4631) | 0.9311 / 0.0048 / 0.0641 (4631) | 0.9311 / 0.0048 / 0.0641 (4631) |
| after contact | 0.9509 / 0.0 / 0.0491 (7172) | 0.9509 / 0.0 / 0.0491 (7172) | 1.0 / 0.0 / 0.0 (7172) |

## Time before the observer's first contact (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 0.8103 / 0.1647 / 0.025 (3400) | 1.0 / 0.0 / 0.0 (3400) | 1.0 / 0.0 / 0.0 (3400) |
| 0.5-1 | 0.8166 / 0.1558 / 0.0276 (3080) | 1.0 / 0.0 / 0.0 (3080) | 1.0 / 0.0 / 0.0 (3080) |
| 1-2 | 0.7442 / 0.2312 / 0.0246 (6920) | 1.0 / 0.0 / 0.0 (6920) | 1.0 / 0.0 / 0.0 (6920) |
| 2-4 | 0.6979 / 0.2797 / 0.0224 (15160) | 0.9499 / 0.0211 / 0.029 (15160) | 0.9499 / 0.0211 / 0.029 (15160) |
| 4+ | 0.7226 / 0.2375 / 0.0398 (16840) | 0.9311 / 0.0048 / 0.0641 (16840) | 0.9311 / 0.0048 / 0.0641 (16840) |
| after contact | 0.8038 / 0.174 / 0.0222 (26080) | 0.9509 / 0.0 / 0.0491 (26080) | 0.9509 / 0.0 / 0.0491 (26080) |

## Confidence calibration (tracks with an association score)

| method | score bin | tracks | empirical accuracy |
|---|---|--:|--:|
| current | 0.9-0.95 | 51 | 1.0 |
| current | 0.95-0.99 | 255 | 1.0 |
| corrected | 0.9-0.95 | 55 | 1.0 |
| corrected | 0.95-0.99 | 987 | 0.9777 |
| retrospective | 0.9-0.95 | 55 | 1.0 |
| retrospective | 0.95-0.99 | 998 | 1.0 |

## Backward decisions by gap (retrospective)

| gap [s] | outcome counts |
|---|---|
| 1-2 | resolved_correct 11 |
| 4+ | unresolved_other_vehicle 11 |

## Provenance

```
{
 "commits": [
  [
   "e7819cd4d517efaa1a16ea96b1f33a7bfcf1f8cc",
   false,
   "485155bb3b78b5256fe2cb374a45da285613be2c135b884d3d82045762f2a33b"
  ]
 ],
 "config_sha256": [
  "33ca8db532f3b52883cc85518386f38b2185799fd07a931682d31f5e51f64361",
  "efbafa2cccc349dfd7c6206529ee7eecfa0ba56984246941c8cb63f0eab67db3",
  "f749393d966d22fb2f653fb21397a948b2fc3f243a43a4fe83f8122289d51278"
 ],
 "seeds": [
  100,
  101,
  102,
  103,
  104,
  105,
  106,
  107,
  108,
  109
 ],
 "conditions": [
  "consumer",
  "consumer_common_0.5",
  "consumer_common_0.9",
  "consumer_common_1.0",
  "exact",
  "rtk"
 ],
 "runs": [
  "S18/run_0_abreast",
  "S18/run_0_passing",
  "S18/run_0_platoon"
 ],
 "generated_utc": "2026-10-13T10:33:32Z"
}
```
