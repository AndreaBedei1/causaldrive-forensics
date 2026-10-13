# Three-method identity study (_S18_dev)

Privileged evaluation of `scripts/retrospective_study.py`; provenance at the end.  Counts per draw (summed over runs, averaged over seeds); shares over all measured samples.

| condition | method | seeds | merges_correct | merges_false | merges_missed | links_wrong | links_missed | duplicate_entities | correct_share | wrong_share | unresolved_share | early_correct_share | early_wrong_share | retrospective_resolved | retrospective_correct |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| consumer | current | 4 | 14.0 | 20.25 | 10.0 | 0.0 | 0.0 | 2.5 | 0.7528 | 0.2161 | 0.0311 | 0.7064 | 0.2577 | 0 | 0 |
| consumer | corrected | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer | retrospective | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.5 | current | 4 | 10.5 | 16.25 | 8.5 | 0.0 | 0.75 | 2.75 | 0.6888 | 0.2147 | 0.0965 | 0.6974 | 0.2577 | 0 | 0 |
| consumer_common_0.5 | corrected | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.5 | retrospective | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.9 | current | 4 | 14.0 | 20.25 | 10.0 | 0.0 | 0.0 | 2.5 | 0.7528 | 0.2161 | 0.0311 | 0.7064 | 0.2577 | 0 | 0 |
| consumer_common_0.9 | corrected | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_0.9 | retrospective | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_1.0 | current | 4 | 14.0 | 21.0 | 10.0 | 0.0 | 0.0 | 2.0 | 0.7834 | 0.2126 | 0.0039 | 0.7333 | 0.2577 | 0 | 0 |
| consumer_common_1.0 | corrected | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| consumer_common_1.0 | retrospective | 4 | 13.0 | 0.0 | 11.0 | 0.0 | 0.0 | 5.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | current | 1 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | corrected | 1 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| exact | retrospective | 1 | 16.0 | 0.0 | 8.0 | 0.0 | 0.0 | 3.0 | 0.9731 | 0.0056 | 0.0213 | 0.9385 | 0.0128 | 1 | 1 |
| rtk | current | 4 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| rtk | corrected | 4 | 14.0 | 0.0 | 10.0 | 0.0 | 0.0 | 4.0 | 0.9552 | 0.0056 | 0.0392 | 0.9385 | 0.0128 | 0 | 0 |
| rtk | retrospective | 4 | 16.0 | 0.0 | 8.0 | 0.0 | 0.0 | 3.0 | 0.9731 | 0.0056 | 0.0213 | 0.9385 | 0.0128 | 4 | 4 |

## Collisions

| condition | method | recall | wrong pairings | unmatched true contacts | ambiguous refusals | recorders aligned |
|---|---|---|--:|--:|--:|---|
| consumer | current | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer | corrected | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer | retrospective | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_0.5 | current | 9/12 | 0 | 3 | 0 | 21/24 |
| consumer_common_0.5 | corrected | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_0.5 | retrospective | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_0.9 | current | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_0.9 | corrected | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_0.9 | retrospective | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_1.0 | current | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_1.0 | corrected | 12/12 | 0 | 0 | 0 | 24/24 |
| consumer_common_1.0 | retrospective | 12/12 | 0 | 0 | 0 | 24/24 |
| exact | current | 3/3 | 0 | 0 | 0 | 6/6 |
| exact | corrected | 3/3 | 0 | 0 | 0 | 6/6 |
| exact | retrospective | 3/3 | 0 | 0 | 0 | 6/6 |
| rtk | current | 12/12 | 0 | 0 | 0 | 24/24 |
| rtk | corrected | 12/12 | 0 | 0 | 0 | 24/24 |
| rtk | retrospective | 12/12 | 0 | 0 | 0 | 24/24 |

## Range from the observing radar (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 1.0 / 0.0 / 0.0 (3450) | 1.0 / 0.0 / 0.0 (3450) | 1.0 / 0.0 / 0.0 (3450) |
| 10-20 | 0.9212 / 0.0164 / 0.0624 (3045) | 0.9212 / 0.0164 / 0.0624 (3045) | 0.9212 / 0.0164 / 0.0624 (3045) |
| 20-30 | 0.9499 / 0.0 / 0.0501 (1895) | 0.9499 / 0.0 / 0.0501 (1895) | 1.0 / 0.0 / 0.0 (1895) |
| 30-40 | 0.8923 / 0.0 / 0.1077 (325) | 0.8923 / 0.0 / 0.1077 (325) | 1.0 / 0.0 / 0.0 (325) |
| 40-50 | 0.8438 / 0.0 / 0.1562 (160) | 0.8438 / 0.0 / 0.1562 (160) | 1.0 / 0.0 / 0.0 (160) |
| 50-60 | 0.9167 / 0.0 / 0.0833 (60) | 0.9167 / 0.0 / 0.0833 (60) | 1.0 / 0.0 / 0.0 (60) |
| 60+ | - | - | - |

## Range from the observing radar (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 0.9677 / 0.0 / 0.0323 (10695) | 1.0 / 0.0 / 0.0 (11040) | 1.0 / 0.0 / 0.0 (11040) |
| 10-20 | 0.6605 / 0.2764 / 0.0631 (9491) | 0.9212 / 0.0164 / 0.0624 (9744) | 0.9212 / 0.0164 / 0.0624 (9744) |
| 20-30 | 0.5286 / 0.4631 / 0.0084 (5740) | 0.9499 / 0.0 / 0.0501 (6064) | 0.9499 / 0.0 / 0.0501 (6064) |
| 30-40 | 0.5572 / 0.4014 / 0.0414 (1014) | 0.8923 / 0.0 / 0.1077 (1040) | 0.8923 / 0.0 / 0.1077 (1040) |
| 40-50 | 0.6235 / 0.3294 / 0.0471 (510) | 0.8438 / 0.0 / 0.1562 (512) | 0.8438 / 0.0 / 0.1562 (512) |
| 50-60 | 0.4948 / 0.4427 / 0.0625 (192) | 0.9167 / 0.0 / 0.0833 (192) | 0.9167 / 0.0 / 0.0833 (192) |
| 60+ | - | - | - |

## Time before the observer's first contact (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 1.0 / 0.0 / 0.0 (425) | 1.0 / 0.0 / 0.0 (425) | 1.0 / 0.0 / 0.0 (425) |
| 0.5-1 | 1.0 / 0.0 / 0.0 (385) | 1.0 / 0.0 / 0.0 (385) | 1.0 / 0.0 / 0.0 (385) |
| 1-2 | 1.0 / 0.0 / 0.0 (865) | 1.0 / 0.0 / 0.0 (865) | 1.0 / 0.0 / 0.0 (865) |
| 2-4 | 0.9499 / 0.0211 / 0.029 (1895) | 0.9499 / 0.0211 / 0.029 (1895) | 0.9499 / 0.0211 / 0.029 (1895) |
| 4+ | 0.9311 / 0.0048 / 0.0641 (2105) | 0.9311 / 0.0048 / 0.0641 (2105) | 0.9311 / 0.0048 / 0.0641 (2105) |
| after contact | 0.9509 / 0.0 / 0.0491 (3260) | 0.9509 / 0.0 / 0.0491 (3260) | 1.0 / 0.0 / 0.0 (3260) |

## Time before the observer's first contact (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 0.8081 / 0.1646 / 0.0273 (1282) | 1.0 / 0.0 / 0.0 (1360) | 1.0 / 0.0 / 0.0 (1360) |
| 0.5-1 | 0.8182 / 0.1558 / 0.026 (1155) | 1.0 / 0.0 / 0.0 (1232) | 1.0 / 0.0 / 0.0 (1232) |
| 1-2 | 0.7457 / 0.2312 / 0.0231 (2595) | 1.0 / 0.0 / 0.0 (2768) | 1.0 / 0.0 / 0.0 (2768) |
| 2-4 | 0.6992 / 0.2797 / 0.0211 (5685) | 0.9499 / 0.0211 / 0.029 (6064) | 0.9499 / 0.0211 / 0.029 (6064) |
| 4+ | 0.724 / 0.2375 / 0.0385 (6315) | 0.9311 / 0.0048 / 0.0641 (6736) | 0.9311 / 0.0048 / 0.0641 (6736) |
| after contact | 0.7698 / 0.1753 / 0.0549 (10610) | 0.9509 / 0.0 / 0.0491 (10432) | 0.9509 / 0.0 / 0.0491 (10432) |

## Confidence calibration (tracks with an association score)

| method | score bin | tracks | empirical accuracy |
|---|---|--:|--:|
| current | 0.9-0.95 | 20 | 1.0 |
| current | 0.95-0.99 | 100 | 1.0 |
| corrected | 0.9-0.95 | 21 | 1.0 |
| corrected | 0.95-0.99 | 409 | 0.9756 |
| retrospective | 0.9-0.95 | 21 | 1.0 |
| retrospective | 0.95-0.99 | 414 | 1.0 |

## Backward decisions by gap (retrospective)

| gap [s] | outcome counts |
|---|---|
| 1-2 | resolved_correct 5 |
| 4+ | unresolved_other_vehicle 5 |

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
  0,
  1,
  2,
  3
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
