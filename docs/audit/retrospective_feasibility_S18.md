# Retrospective feasibility on S18 (before any implementation)

Privileged evaluation of METHOD 1 (`current`, the algorithm of `main`) on `traces/S18/run_0_{abreast,passing,platoon}` with consumer GNSS and its correlated variants, development seeds 0-3 (`scripts/retrospective_feasibility.py`, rows in `retrospective_feasibility_S18.json`).
Ground truth only labels a link as wrong (its two tracks on different true vehicles); the evidence is searched in the reconstruction's own data: two simultaneous tracks of ONE recorder whose returns cannot be faces of one body (one-box test of `anonymous.pair_evidence` WITHOUT the observer's pose error, which is common to both tracks and cancels in their difference; chi-square beyond the 0.99 gate).

Verdicts: RECOVERABLE = such distinctness on >= 10 instants before the recorder's first contact; POSSIBLY_RECOVERABLE = fewer instants, or only after the contact; NOT_RECOVERABLE = no instant distinguishes the two vehicles (backward association cannot solve this case).

## Summary

| condition | link kind | verdict | wrong links (4 seeds x 3 runs) |
|---|---|---|--:|
| consumer | cross_observer | NOT_RECOVERABLE | 1 |
| consumer | cross_observer | RECOVERABLE | 2 |
| consumer | same_observer | POSSIBLY_RECOVERABLE | 3 |
| consumer | same_observer | RECOVERABLE | 12 |
| consumer_common_0.5 | cross_observer | RECOVERABLE | 1 |
| consumer_common_0.5 | same_observer | POSSIBLY_RECOVERABLE | 3 |
| consumer_common_0.5 | same_observer | RECOVERABLE | 11 |
| consumer_common_0.9 | cross_observer | RECOVERABLE | 1 |
| consumer_common_0.9 | same_observer | POSSIBLY_RECOVERABLE | 3 |
| consumer_common_0.9 | same_observer | RECOVERABLE | 11 |
| consumer_common_1.0 | same_observer | POSSIBLY_RECOVERABLE | 4 |
| consumer_common_1.0 | same_observer | RECOVERABLE | 12 |

## Every wrong link

| condition | seed | run | link | kind | true (eval.) | verdict | evidence pair (same recorder) | distinct instants before contact / simultaneous | first distinct, s before contact | longest interval [s] | range [m] | separation [m] | velocity diff. [m/s] |
|---|--:|---|---|---|---|---|---|---|---|---|---|---|---|
| consumer | 0 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer | 0 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer | 0 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer | 0 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer | 1 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer | 1 | run_0_abreast | A:track_001#segment_3 - A:track_003 | same_observer | C/D | RECOVERABLE | A:track_001#segment_3 / A:track_003 | 35 / 103 | 2.05 | 2.6 | 15.4-37.9 | 3.4-3.6 | 0.158 |
| consumer | 1 | run_0_abreast | A:track_003 - B:track_002 | cross_observer | D/C | NOT_RECOVERABLE | - | - | - | - | - | - | - |
| consumer | 1 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer | 1 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer | 1 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer | 2 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer | 2 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer | 2 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer | 2 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer | 3 | run_0_abreast | A:track_001#segment_3 - B:track_003 | cross_observer | C/D | RECOVERABLE | B:track_002 / B:track_003 | 91 / 150 | 6.2 | 2.8 | 18.8-21.4 | 3.2-3.4 | 0.283 |
| consumer | 3 | run_0_abreast | A:track_001#segment_3 - A:track_003 | same_observer | C/D | RECOVERABLE | A:track_001#segment_3 / A:track_003 | 35 / 103 | 2.05 | 2.6 | 15.4-37.9 | 3.4-3.6 | 0.158 |
| consumer | 3 | run_0_passing | A:track_003 - B:track_003 | cross_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer | 3 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.5 | 0 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.5 | 0 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.5 | 0 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.5 | 0 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.5 | 1 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.5 | 1 | run_0_abreast | A:track_003 - B:track_002 | cross_observer | D/C | RECOVERABLE | A:track_003 / A:track_001#segment_3 | 35 / 103 | 2.05 | 2.6 | 15.7-37.4 | 3.4-3.6 | 0.158 |
| consumer_common_0.5 | 1 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.5 | 1 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.5 | 1 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.5 | 2 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.5 | 2 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.5 | 2 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.5 | 2 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.5 | 3 | run_0_abreast | A:track_001#segment_3 - A:track_003 | same_observer | C/D | RECOVERABLE | A:track_001#segment_3 / A:track_003 | 35 / 103 | 2.05 | 2.6 | 15.4-37.9 | 3.4-3.6 | 0.158 |
| consumer_common_0.5 | 3 | run_0_passing | A:track_001 - A:track_003 | same_observer | D/C | RECOVERABLE | A:track_001 / A:track_003 | 111 / 171 | 6.05 | 5.15 | 12.9-17.3 | 3.1-3.9 | 0.804 |
| consumer_common_0.9 | 0 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.9 | 0 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.9 | 0 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.9 | 0 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.9 | 1 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.9 | 1 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.9 | 1 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.9 | 1 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.9 | 2 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.9 | 2 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.9 | 2 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_0.9 | 2 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_0.9 | 3 | run_0_abreast | A:track_001#segment_3 - B:track_003 | cross_observer | C/D | RECOVERABLE | B:track_002 / B:track_003 | 91 / 150 | 6.2 | 2.8 | 18.8-21.4 | 3.2-3.4 | 0.283 |
| consumer_common_0.9 | 3 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_0.9 | 3 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_1.0 | 0 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_1.0 | 0 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_1.0 | 0 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_1.0 | 0 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_1.0 | 1 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_1.0 | 1 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_1.0 | 1 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_1.0 | 1 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_1.0 | 2 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_1.0 | 2 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_1.0 | 2 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_1.0 | 2 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |
| consumer_common_1.0 | 3 | run_0_abreast | B:track_003 - B:track_004 | same_observer | D/C | RECOVERABLE | B:track_003 / B:track_002 | 91 / 150 | 6.2 | 2.8 | 19.2-22.4 | 3.2-3.4 | 0.283 |
| consumer_common_1.0 | 3 | run_0_passing | B:track_002 - B:track_003 | same_observer | C/D | RECOVERABLE | A:track_003 / A:track_001 | 111 / 171 | 6.05 | 5.15 | 15.1-15.4 | 3.1-3.9 | 0.804 |
| consumer_common_1.0 | 3 | run_0_platoon | B:track_003 - B:track_004 | same_observer | C/D | RECOVERABLE | B:track_003 / B:track_002 | 72 / 81 | 6.15 | 3.95 | 24.4-28.2 | 8.5-9.2 | 0.283 |
| consumer_common_1.0 | 3 | run_0_platoon | B:track_004 - B:track_005 | same_observer | D/C | POSSIBLY_RECOVERABLE | B:track_002 / B:track_005 | 0 / 25 | None | 0.6 | 13.8-16.0 | 9.1-9.1 | 0.265 |

## Reading

* Almost every wrong link is a SAME_OBSERVER link: two tracks of B (or A), simultaneous and 4-7 m apart, one on C and one on D, accepted as one body because the full absolute pose variance of the observer (consumer GNSS, 1.66 m per axis) was added to the faces of both.  The same recorder's own data distinguish C and D from its first sweeps: about 6 s before the contact (the start of the recording), at 15-29 m, 3-8 m apart, for up to 5 s at a time.  The evidence is simultaneous with the wrong link, not later: these merges are recovered by treating the observer's pose error as common to its two tracks (METHOD 2), not by backward association.
* The POSSIBLY_RECOVERABLE links (platoon, B's tracks of D and C one behind the other) are distinguishable only after the contact in this test (before it the pair has no heading or no failing instant).
* The NOT_RECOVERABLE cross-observer link (abreast, seed 1: A's track of D with B's track of C) has no recorder that sees both vehicles at once before the impact: no interval of the recorded data tells them apart, so backward association cannot solve it.  Only a smaller relative pose uncertainty (or not linking) can.
* With exact poses (METHOD 1, same seeds) there are no false merges; the remaining errors are missed merges: tracks too short to share 10 instants, a cross-observer pair just below the 80 % pass fraction, and the same car tracked again by B after a 1.85 s gap while both recorders identify it strongly.  These are the cases later evidence can address.
