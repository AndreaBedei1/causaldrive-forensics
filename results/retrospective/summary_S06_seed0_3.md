# Three-method identity study (_S06_seed0_3)

Privileged evaluation of `scripts/retrospective_study.py`; provenance at the end.  Counts per draw (summed over runs, averaged over seeds); shares over all measured samples.

| condition | method | seeds | merges_correct | merges_false | merges_missed | links_wrong | links_missed | duplicate_entities | correct_share | wrong_share | unresolved_share | early_correct_share | early_wrong_share | retrospective_resolved | retrospective_correct |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| consumer_impulse10 | current | 2 | 0.0 | 0.0 | 0.0 | 0.5 | 1.0 | 0.0 | 0.5729 | 0.1437 | 0.2834 | 0.7742 | 0.0 | 0 | 0 |
| consumer_impulse10 | corrected | 2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.8589 | 0.0 | 0.1411 | 1.0 | 0.0 | 0 | 0 |
| consumer_impulse10 | retrospective | 2 | 0.0 | 0.0 | 0.0 | 0.0 | 0.5 | 0.0 | 0.8589 | 0.0 | 0.1411 | 1.0 | 0.0 | 0 | 0 |

## Collisions

| condition | method | recall | wrong pairings | unmatched true contacts | ambiguous refusals | recorders aligned |
|---|---|---|--:|--:|--:|---|
| consumer_impulse10 | current | 3/10 | 1 | 7 | 10 | 11/12 |
| consumer_impulse10 | corrected | 7/10 | 0 | 3 | 2 | 11/12 |
| consumer_impulse10 | retrospective | 7/10 | 0 | 3 | 2 | 11/12 |

## Range from the observing radar (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | - | - | - |
| 10-20 | - | - | - |
| 20-30 | - | - | - |
| 30-40 | - | - | - |
| 40-50 | - | - | - |
| 50-60 | - | - | - |
| 60+ | - | - | - |

## Range from the observing radar (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-10 | 0.5682 / 0.1163 / 0.3155 (748) | 0.8165 / 0.0 / 0.1835 (752) | 0.8165 / 0.0 / 0.1835 (752) |
| 10-20 | 0.6493 / 0.0522 / 0.2985 (134) | 1.0 / 0.0 / 0.0 (134) | 1.0 / 0.0 / 0.0 (134) |
| 20-30 | 0.5 / 0.5 / 0.0 (92) | 1.0 / 0.0 / 0.0 (92) | 1.0 / 0.0 / 0.0 (92) |
| 30-40 | - | - | - |
| 40-50 | - | - | - |
| 50-60 | - | - | - |
| 60+ | - | - | - |

## Time before the observer's first contact (exact and RTK)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | - | - | - |
| 0.5-1 | - | - | - |
| 1-2 | - | - | - |
| 2-4 | - | - | - |
| 4+ | - | - | - |
| after contact | - | - | - |

## Time before the observer's first contact (consumer and correlated consumer)

| bin [m or s] | current correct / wrong / unresolved (samples) | corrected correct / wrong / unresolved (samples) | retrospective correct / wrong / unresolved (samples) |
|---|---|---|---|
| 0-0.5 | 0.6957 / 0.0435 / 0.2609 (23, few) | 0.9677 / 0.0 / 0.0323 (31, few) | 0.9677 / 0.0 / 0.0323 (31, few) |
| 0.5-1 | 0.75 / 0.0 / 0.25 (20, few) | 1.0 / 0.0 / 0.0 (30, few) | 1.0 / 0.0 / 0.0 (30, few) |
| 1-2 | 0.75 / 0.0 / 0.25 (40, few) | 1.0 / 0.0 / 0.0 (60) | 1.0 / 0.0 / 0.0 (60) |
| 2-4 | 0.75 / 0.0 / 0.25 (80) | 1.0 / 0.0 / 0.0 (120) | 1.0 / 0.0 / 0.0 (120) |
| 4+ | 0.8085 / 0.0 / 0.1915 (47, few) | 1.0 / 0.0 / 0.0 (76) | 1.0 / 0.0 / 0.0 (76) |
| after contact | 0.5223 / 0.1819 / 0.2958 (764) | 0.7927 / 0.0 / 0.2073 (661) | 0.7927 / 0.0 / 0.2073 (661) |

## Confidence calibration (tracks with an association score)

| method | score bin | tracks | empirical accuracy |
|---|---|--:|--:|
| current | 0.5-0.8 | 2 | 1.0 |
| current | 0.8-0.9 | 1 | 0.0 |
| current | 0.9-0.95 | 1 | 1.0 |
| current | 0.95-0.99 | 1 | 1.0 |
| corrected | 0.5-0.8 | 3 | 1.0 |
| corrected | 0.8-0.9 | 1 | 1.0 |
| corrected | 0.9-0.95 | 1 | 1.0 |
| corrected | 0.95-0.99 | 1 | 1.0 |
| retrospective | 0.5-0.8 | 3 | 1.0 |
| retrospective | 0.8-0.9 | 1 | 1.0 |
| retrospective | 0.9-0.95 | 1 | 1.0 |
| retrospective | 0.95-0.99 | 1 | 1.0 |

## Backward decisions by gap (retrospective)

| gap [s] | outcome counts |
|---|---|

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
  3
 ],
 "conditions": [
  "consumer_impulse10"
 ],
 "runs": [
  "S06/run_0_a_front_pushed",
  "S06/run_0_b_rear_first"
 ],
 "generated_utc": "2026-10-13T10:33:33Z"
}
```
