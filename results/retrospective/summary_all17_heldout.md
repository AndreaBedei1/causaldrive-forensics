# Three-method identity study (_all17_heldout)

Privileged evaluation of `scripts/retrospective_study.py`; provenance at the end.  Counts per draw (summed over runs, averaged over seeds); shares over all measured samples.

| condition | method | seeds | merges_correct | merges_false | merges_missed | links_wrong | links_missed | duplicate_entities | correct_share | wrong_share | unresolved_share | early_correct_share | early_wrong_share | retrospective_resolved | retrospective_correct |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| consumer | current | 5 | 17.0 | 20.4 | 11.0 | 0.2 | 4.8 | 3.4 | 0.8426 | 0.0656 | 0.0917 | 0.8295 | 0.1344 | 0 | 0 |
| consumer | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8682 | 0.0017 | 0.1301 | 0.9056 | 0.0062 | 0 | 0 |
| consumer | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8682 | 0.0017 | 0.1301 | 0.9056 | 0.0062 | 0 | 0 |
| consumer_common_0.5 | current | 5 | 17.0 | 20.4 | 10.8 | 0.4 | 3.8 | 3.2 | 0.8617 | 0.0697 | 0.0687 | 0.8387 | 0.1342 | 0 | 0 |
| consumer_common_0.5 | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8677 | 0.0017 | 0.1306 | 0.903 | 0.0062 | 0 | 0 |
| consumer_common_0.5 | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8677 | 0.0017 | 0.1306 | 0.903 | 0.0062 | 0 | 0 |
| consumer_common_0.9 | current | 5 | 17.0 | 20.4 | 10.6 | 0.2 | 3.2 | 3.0 | 0.8805 | 0.0642 | 0.0553 | 0.8482 | 0.1285 | 0 | 0 |
| consumer_common_0.9 | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.8 | 7.0 | 0.86 | 0.0017 | 0.1383 | 0.9007 | 0.0062 | 0 | 0 |
| consumer_common_0.9 | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.8 | 7.0 | 0.86 | 0.0017 | 0.1383 | 0.9007 | 0.0062 | 0 | 0 |
| consumer_common_0.9_impulse10 | current | 5 | 17.0 | 20.4 | 10.6 | 0.0 | 3.2 | 3.0 | 0.8854 | 0.0596 | 0.0551 | 0.8495 | 0.1274 | 0 | 0 |
| consumer_common_0.9_impulse10 | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.8 | 7.0 | 0.86 | 0.0017 | 0.1383 | 0.9007 | 0.0062 | 0 | 0 |
| consumer_common_0.9_impulse10 | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.8 | 7.0 | 0.86 | 0.0017 | 0.1383 | 0.9007 | 0.0062 | 0 | 0 |
| consumer_common_1.0 | current | 5 | 17.0 | 21.0 | 10.2 | 0.0 | 2.4 | 2.2 | 0.9115 | 0.0576 | 0.0309 | 0.8662 | 0.1267 | 0 | 0 |
| consumer_common_1.0 | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 8.6 | 7.0 | 0.845 | 0.0017 | 0.1533 | 0.8962 | 0.0061 | 0 | 0 |
| consumer_common_1.0 | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 8.6 | 7.0 | 0.845 | 0.0017 | 0.1533 | 0.8962 | 0.0061 | 0 | 0 |
| consumer_impulse10 | current | 5 | 17.0 | 20.4 | 11.0 | 0.0 | 4.4 | 3.4 | 0.8579 | 0.0604 | 0.0818 | 0.834 | 0.1309 | 0 | 0 |
| consumer_impulse10 | corrected | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8682 | 0.0017 | 0.1301 | 0.9056 | 0.0062 | 0 | 0 |
| consumer_impulse10 | retrospective | 5 | 17.0 | 0.0 | 14.0 | 0.0 | 7.4 | 7.0 | 0.8682 | 0.0017 | 0.1301 | 0.9056 | 0.0062 | 0 | 0 |
| degraded | current | 5 | 17.0 | 20.8 | 10.6 | 1.6 | 7.8 | 4.0 | 0.7902 | 0.074 | 0.1358 | 0.7662 | 0.1276 | 0 | 0 |
| degraded | corrected | 5 | 6.4 | 0.0 | 28.0 | 0.0 | 13.0 | 14.8 | 0.7281 | 0.0017 | 0.2702 | 0.7176 | 0.0059 | 0 | 0 |
| degraded | retrospective | 5 | 6.4 | 0.0 | 28.0 | 0.0 | 13.0 | 14.8 | 0.7281 | 0.0017 | 0.2702 | 0.7176 | 0.0059 | 0 | 0 |
| exact | current | 1 | 17.0 | 0.0 | 10.0 | 0.0 | 1.0 | 4.0 | 0.9874 | 0.0016 | 0.0109 | 0.9708 | 0.0061 | 0 | 0 |
| exact | corrected | 1 | 17.0 | 0.0 | 10.0 | 0.0 | 2.0 | 4.0 | 0.9675 | 0.0016 | 0.0309 | 0.9706 | 0.0061 | 0 | 0 |
| exact | retrospective | 1 | 19.0 | 0.0 | 8.0 | 0.0 | 2.0 | 3.0 | 0.9723 | 0.0016 | 0.0261 | 0.9706 | 0.0061 | 1 | 1 |
| exact_impulse10 | current | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 1.0 | 4.0 | 0.9874 | 0.0016 | 0.0109 | 0.9708 | 0.0061 | 0 | 0 |
| exact_impulse10 | corrected | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 2.0 | 4.0 | 0.9675 | 0.0016 | 0.0309 | 0.9706 | 0.0061 | 0 | 0 |
| exact_impulse10 | retrospective | 5 | 19.0 | 0.0 | 8.0 | 0.0 | 2.0 | 3.0 | 0.9723 | 0.0016 | 0.0261 | 0.9706 | 0.0061 | 5 | 5 |
| rtk | current | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 1.0 | 4.0 | 0.9874 | 0.0016 | 0.0109 | 0.9708 | 0.0061 | 0 | 0 |
| rtk | corrected | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 2.0 | 4.0 | 0.9675 | 0.0016 | 0.0309 | 0.9706 | 0.0061 | 0 | 0 |
| rtk | retrospective | 5 | 19.0 | 0.0 | 8.0 | 0.0 | 2.0 | 3.0 | 0.9723 | 0.0016 | 0.0261 | 0.9706 | 0.0061 | 5 | 5 |
| rtk_impulse10 | current | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 1.0 | 4.0 | 0.9874 | 0.0016 | 0.0109 | 0.9708 | 0.0061 | 0 | 0 |
| rtk_impulse10 | corrected | 5 | 17.0 | 0.0 | 10.0 | 0.0 | 2.0 | 4.0 | 0.9675 | 0.0016 | 0.0309 | 0.9706 | 0.0061 | 0 | 0 |
| rtk_impulse10 | retrospective | 5 | 19.0 | 0.0 | 8.0 | 0.0 | 2.0 | 3.0 | 0.9723 | 0.0016 | 0.0261 | 0.9706 | 0.0061 | 5 | 5 |

## Collisions

| condition | method | recall | wrong pairings | unmatched true contacts | ambiguous refusals | recorders aligned |
|---|---|---|--:|--:|--:|---|
| consumer | current | 89/110 | 0 | 21 | 35 | 192/200 |
| consumer | corrected | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer | retrospective | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_common_0.5 | current | 88/110 | 0 | 22 | 34 | 192/200 |
| consumer_common_0.5 | corrected | 105/110 | 0 | 5 | 0 | 191/200 |
| consumer_common_0.5 | retrospective | 105/110 | 0 | 5 | 0 | 191/200 |
| consumer_common_0.9 | current | 93/110 | 0 | 17 | 30 | 195/200 |
| consumer_common_0.9 | corrected | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_common_0.9 | retrospective | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_common_0.9_impulse10 | current | 95/110 | 0 | 15 | 25 | 196/200 |
| consumer_common_0.9_impulse10 | corrected | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_common_0.9_impulse10 | retrospective | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_common_1.0 | current | 95/110 | 0 | 15 | 25 | 199/200 |
| consumer_common_1.0 | corrected | 105/110 | 0 | 5 | 0 | 194/200 |
| consumer_common_1.0 | retrospective | 105/110 | 0 | 5 | 0 | 194/200 |
| consumer_impulse10 | current | 95/110 | 0 | 15 | 20 | 195/200 |
| consumer_impulse10 | corrected | 105/110 | 0 | 5 | 0 | 192/200 |
| consumer_impulse10 | retrospective | 105/110 | 0 | 5 | 0 | 192/200 |
| degraded | current | 85/110 | 1 | 25 | 44 | 188/200 |
| degraded | corrected | 105/110 | 0 | 5 | 0 | 193/200 |
| degraded | retrospective | 105/110 | 0 | 5 | 0 | 193/200 |
| exact | current | 22/22 | 0 | 0 | 0 | 40/40 |
| exact | corrected | 21/22 | 0 | 1 | 0 | 40/40 |
| exact | retrospective | 21/22 | 0 | 1 | 0 | 40/40 |
| exact_impulse10 | current | 110/110 | 0 | 0 | 0 | 200/200 |
| exact_impulse10 | corrected | 105/110 | 0 | 5 | 0 | 200/200 |
| exact_impulse10 | retrospective | 105/110 | 0 | 5 | 0 | 200/200 |
| rtk | current | 110/110 | 0 | 0 | 0 | 200/200 |
| rtk | corrected | 105/110 | 0 | 5 | 0 | 200/200 |
| rtk | retrospective | 105/110 | 0 | 5 | 0 | 200/200 |
| rtk_impulse10 | current | 110/110 | 0 | 0 | 0 | 200/200 |
| rtk_impulse10 | corrected | 105/110 | 0 | 5 | 0 | 200/200 |
| rtk_impulse10 | retrospective | 105/110 | 0 | 5 | 0 | 200/200 |

## Range from the observing radar (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 0.9998 / 0.0002 / 0.0 (66128) | 0.9727 / 0.0002 / 0.0271 (66128) | 0.9727 / 0.0002 / 0.0271 (66128) |
| 10-20 | 0.9665 / 0.0066 / 0.0269 (24368) | 0.9619 / 0.0066 / 0.0315 (24368) | 0.9619 / 0.0066 / 0.0315 (24368) |
| 20-30 | 0.9725 / 0.0 / 0.0275 (11056) | 0.9595 / 0.0 / 0.0405 (11056) | 0.987 / 0.0 / 0.013 (11056) |
| 30-40 | 0.9493 / 0.0 / 0.0507 (2208) | 0.913 / 0.0 / 0.087 (2208) | 0.9638 / 0.0 / 0.0362 (2208) |
| 40-50 | 0.9324 / 0.0 / 0.0676 (1184) | 0.9324 / 0.0 / 0.0676 (1184) | 1.0 / 0.0 / 0.0 (1184) |
| 50-60 | 0.9778 / 0.0 / 0.0222 (720) | 0.9778 / 0.0 / 0.0222 (720) | 1.0 / 0.0 / 0.0 (720) |
| 60+ | 1.0 / 0.0 / 0.0 (1136) | 1.0 / 0.0 / 0.0 (1136) | 1.0 / 0.0 / 0.0 (1136) |

## Range from the observing radar (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 0.9476 / 0.0031 / 0.0492 (120051) | 0.9236 / 0.0003 / 0.0762 (118138) | 0.9236 / 0.0003 / 0.0762 (118138) |
| 10-20 | 0.7678 / 0.1171 / 0.1151 (43272) | 0.7084 / 0.0069 / 0.2847 (43450) | 0.7084 / 0.0069 / 0.2847 (43450) |
| 20-30 | 0.7029 / 0.2665 / 0.0306 (20373) | 0.8491 / 0.0 / 0.1509 (20139) | 0.8491 / 0.0 / 0.1509 (20139) |
| 30-40 | 0.7346 / 0.1951 / 0.0702 (3972) | 0.8043 / 0.0 / 0.1957 (3842) | 0.8043 / 0.0 / 0.1957 (3842) |
| 40-50 | 0.7872 / 0.1442 / 0.0686 (2115) | 0.8369 / 0.0 / 0.1631 (2115) | 0.8369 / 0.0 / 0.1631 (2115) |
| 50-60 | 0.7711 / 0.1285 / 0.1004 (1245) | 0.8193 / 0.0 / 0.1807 (1245) | 0.8193 / 0.0 / 0.1807 (1245) |
| 60+ | 0.8906 / 0.0 / 0.1094 (1920) | 0.7969 / 0.0 / 0.2031 (1920) | 0.7969 / 0.0 / 0.2031 (1920) |

## Time before the observer's first contact (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 1.0 / 0.0 / 0.0 (4448) | 1.0 / 0.0 / 0.0 (4288) | 1.0 / 0.0 / 0.0 (4288) |
| 0.5-1 | 1.0 / 0.0 / 0.0 (4432) | 1.0 / 0.0 / 0.0 (4272) | 1.0 / 0.0 / 0.0 (4272) |
| 1-2 | 1.0 / 0.0 / 0.0 (9120) | 1.0 / 0.0 / 0.0 (8800) | 1.0 / 0.0 / 0.0 (8800) |
| 2-4 | 0.98 / 0.0084 / 0.0116 (15216) | 0.9797 / 0.0086 / 0.0118 (14944) | 0.9797 / 0.0086 / 0.0118 (14944) |
| 4+ | 0.9606 / 0.0027 / 0.0367 (11776) | 0.9606 / 0.0027 / 0.0367 (11776) | 0.9606 / 0.0027 / 0.0367 (11776) |
| after contact | 0.9907 / 0.0003 / 0.0091 (61808) | 0.9569 / 0.0003 / 0.0429 (62720) | 0.9651 / 0.0003 / 0.0347 (62720) |

## Time before the observer's first contact (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 0.9051 / 0.0547 / 0.0402 (7757) | 0.908 / 0.0 / 0.092 (7830) | 0.908 / 0.0 / 0.092 (7830) |
| 0.5-1 | 0.9164 / 0.047 / 0.0366 (7660) | 0.8923 / 0.0 / 0.1077 (7800) | 0.8923 / 0.0 / 0.1077 (7800) |
| 1-2 | 0.8886 / 0.0759 / 0.0354 (15800) | 0.8955 / 0.0 / 0.1045 (16080) | 0.8955 / 0.0 / 0.1045 (16080) |
| 2-4 | 0.8532 / 0.1205 / 0.0263 (26396) | 0.8974 / 0.0087 / 0.0939 (27580) | 0.8974 / 0.0087 / 0.0939 (27580) |
| 4+ | 0.8323 / 0.1428 / 0.0249 (21006) | 0.9093 / 0.0027 / 0.088 (22039) | 0.9093 / 0.0027 / 0.088 (22039) |
| after contact | 0.8788 / 0.0346 / 0.0866 (114329) | 0.8322 / 0.0003 / 0.1675 (109520) | 0.8322 / 0.0003 / 0.1675 (109520) |

## Confidence calibration (tracks with an association score)

| method | score bin | tracks | empirical accuracy |
|---|---|--:|--:|
| current | 0.5-0.8 | 90 | 1.0 |
| current | 0.8-0.9 | 548 | 0.9836 |
| current | 0.9-0.95 | 491 | 1.0 |
| current | 0.95-0.99 | 538 | 1.0 |
| current | 0.99-1.0001 | 507 | 0.9941 |
| corrected | 0.5-0.8 | 96 | 1.0 |
| corrected | 0.8-0.9 | 517 | 1.0 |
| corrected | 0.9-0.95 | 481 | 1.0 |
| corrected | 0.95-0.99 | 1438 | 0.9221 |
| corrected | 0.99-1.0001 | 391 | 0.9949 |
| retrospective | 0.5-0.8 | 96 | 1.0 |
| retrospective | 0.8-0.9 | 517 | 1.0 |
| retrospective | 0.9-0.95 | 481 | 1.0 |
| retrospective | 0.95-0.99 | 1454 | 0.945 |
| retrospective | 0.99-1.0001 | 391 | 0.9949 |

## Backward decisions by gap (retrospective)

| gap [s] | outcome counts |
|---|---|
| 1-2 | resolved_correct 16 |
| 4+ | unresolved_other_vehicle 16 |

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
  104
 ],
 "conditions": [
  "consumer",
  "consumer_common_0.5",
  "consumer_common_0.9",
  "consumer_common_0.9_impulse10",
  "consumer_common_1.0",
  "consumer_impulse10",
  "degraded",
  "exact",
  "exact_impulse10",
  "rtk",
  "rtk_impulse10"
 ],
 "runs": [
  "S01/run_0_crash",
  "S02/run_0_crash",
  "S02/run_0_critical_before_cut_in",
  "S03/run_0_crash",
  "S06/run_0_a_front_pushed",
  "S06/run_0_b_rear_first",
  "S07/run_0_crash",
  "S08/run_0_crash",
  "S09/run_0_merge_conflict",
  "S10/run_0_rolls_through",
  "S12/run_0_near_simultaneous",
  "S15/run_0_deflected_into_c",
  "S16/run_0_consequential",
  "S17/run_0_crash",
  "S18/run_0_abreast",
  "S18/run_0_passing",
  "S18/run_0_platoon"
 ],
 "generated_utc": "2026-10-13T10:33:32Z"
}
```
