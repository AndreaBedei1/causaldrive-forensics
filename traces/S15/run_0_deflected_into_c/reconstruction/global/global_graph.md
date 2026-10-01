# Global graph - S15/run_0_deflected_into_c

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_002, C:track_002 |
| B | recorder | clock ALIGNED; observed by others as: A:track_002 |
| C | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |
| B:track_005 | anonymous_track | seen only by B; candidate: A |
| B:track_006 | anonymous_track | seen only by B; candidate: A |
| B:track_007 | anonymous_track | seen only by B; candidate: A |
| B:track_008 | anonymous_track | seen only by B; candidate: A |
| C:track_001 | anonymous_track | seen only by C; candidate: A |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e09 | 3.80 | -3.80 | reported the reference collision collision_001 |
| B | ALIGNED | B:e29 | 3.80 | -3.80 | reported the reference collision collision_001 |
| C | ALIGNED | C:e08 | 4.75 | -3.80 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 9797.5 vs 9797.5 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 1637.56 vs 1637.56 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | C | ASSOCIATED | 0.94 | A and C both reported collision_002 at 4.75 s (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.6 m -> 1.1 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.53 m/s over 3.0 s<br>range at the contact 1.13 m<br>the only track of A compatible with the contact<br>collision_001 with B at 3.80 s: not compatible (track speed disagrees with B's own speed: RMSE 3.64 m/s over 3.0 s (> 1.50)) |
| A:track_002 | B | ASSOCIATED | 0.85 | A and B both reported collision_001 at 3.80 s (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.80 s before the matched collision<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.1 m -> 1.9 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.85 m/s over 1.8 s<br>range at the contact 1.89 m<br>the only track of A compatible with the contact<br>collision_002 with C at 4.75 s: not compatible (lost 1.00 s before the matched collision (window 0.50 s); track speed disagrees with C's own speed: RMSE 3.29 m/s over 1.8 s (> 1.50)) |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 2.35 s before the matched collision<br>lost 0.65 s before the matched collision (window 0.50 s)<br>approaching before the contact: range 22.2 m -> 14.7 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 5.69 m/s over 1.7 s (> 1.50) |
| B:track_002 | A | ASSOCIATED | 0.88 | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 1.85 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 16.9 m -> 1.1 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.77 m/s over 1.8 s<br>range at the contact 0.99 m<br>the only track of B compatible with the contact |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 33.3 m -> 30.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.67 m/s over 0.7 s (> 1.50)<br>range at the contact 30.02 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 22.0 m -> 19.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.16 m/s over 0.7 s (> 1.50)<br>range at the contact 19.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 30.4 m -> 27.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 8.37 m/s over 0.7 s (> 1.50)<br>range at the contact 26.97 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 27.3 m -> 24.1 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.37 m/s over 0.7 s (> 1.50)<br>range at the contact 24.12 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.05 s before it (window 0.50 s)<br>approaching before the contact: range 17.3 m -> 15.0 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 9.73 m/s over 0.6 s (> 1.50)<br>range at the contact 15.03 m (beyond 3.50 m: confidence factor 0.00) |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 9797.5 vs 9797.5 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| C:track_001 | C:track_001 | ANONYMOUS | - | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.75 s before the matched collision<br>continuous up to the contact: last observed 0.30 s before it (window 0.50 s)<br>approaching before the contact: range 11.6 m -> 7.6 m over the last 1.0 s<br>track speed disagrees with A's own speed: RMSE 3.88 m/s over 2.7 s (> 1.50)<br>range at the contact 7.64 m (beyond 3.50 m: confidence factor 0.39) |
| C:track_002 | A | ASSOCIATED | 0.92 | C and A both reported collision_002 (peak impulse 1637.56 vs 1637.56 N*s)<br>tracked for 4.70 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 11.5 m -> 1.9 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.59 m/s over 3.0 s<br>range at the contact 1.89 m<br>the only track of C compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -3.80 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -3.80 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -3.80 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -3.80 | TRACK_APPEARED_LEFT | C | C:track_001 | C:e02 @ 0.00 |  |
| g05 | -3.80 | CLOSING_START | C | C:track_001 | C:e03 @ 0.00 | active_at_first_observation=True |
| g06 | -3.75 | TRACK_APPEARED_FRONT | A | C | A:e02 @ 0.05 |  |
| g07 | -3.75 | TRACK_APPEARED_FRONT | C | A | C:e04 @ 0.05 |  |
| g08 | -3.75 | CLOSING_START | A | C | A:e03 @ 0.05 | active_at_first_observation=True |
| g09 | -3.75 | CLOSING_START | C | A | C:e05 @ 0.05 | active_at_first_observation=True |
| g10 | -2.35 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e02 @ 1.45 |  |
| g11 | -2.35 | CLOSING_START | B | B:track_001 | B:e03 @ 1.45 | active_at_first_observation=True |
| g12 | -2.30 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e04 @ 1.50 | relevant_to_ego_path=False |
| g13 | -1.85 | TRACK_APPEARED_LEFT | B | A | B:e05 @ 1.95 |  |
| g14 | -1.85 | CLOSING_START | B | A | B:e06 @ 1.95 | active_at_first_observation=True |
| g15 | -1.80 | TRACK_APPEARED_RIGHT | A | B | A:e04 @ 2.00 |  |
| g16 | -1.80 | CLOSING_START | A | B | A:e05 @ 2.00 | active_at_first_observation=True |
| g17 | -1.80 | CRITICAL_TTC_START | A | B | A:e06 @ 2.00 | active_at_first_observation=True |
| g18 | -1.70 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e07 @ 2.10 |  |
| g19 | -1.65 | CRITICAL_TTC_START | B | A | B:e08 @ 2.15 |  |
| g20 | -1.55 | TURN_LEFT_START | B | - | B:e09 @ 2.25 |  |
| g21 | -1.25 | CRITICAL_TTC_START | A | C | A:e07 @ 2.55 |  |
| g22 | -0.90 | CRITICAL_TTC_START | C | A | C:e06 @ 2.90 |  |
| g23 | -0.85 | BRAKE_START | B | - | B:e10 @ 2.95 |  |
| g24 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_003 | B:e11 @ 3.05 |  |
| g25 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_004 | B:e12 @ 3.05 |  |
| g26 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_005 | B:e13 @ 3.05 |  |
| g27 | -0.75 | TRACK_APPEARED_LEFT | B | B:track_006 | B:e14 @ 3.05 |  |
| g28 | -0.75 | CLOSING_START | B | B:track_003 | B:e15 @ 3.05 | active_at_first_observation=True |
| g29 | -0.75 | CLOSING_START | B | B:track_004 | B:e16 @ 3.05 | active_at_first_observation=True |
| g30 | -0.75 | CLOSING_START | B | B:track_005 | B:e17 @ 3.05 | active_at_first_observation=True |
| g31 | -0.75 | CLOSING_START | B | B:track_006 | B:e18 @ 3.05 | active_at_first_observation=True |
| g32 | -0.70 | TRACK_APPEARED_LEFT | B | B:track_007 | B:e19 @ 3.10 |  |
| g33 | -0.70 | CLOSING_START | B | B:track_007 | B:e20 @ 3.10 | active_at_first_observation=True |
| g34 | -0.65 | TRACK_LOST | B | B:track_001 | B:e21 @ 3.15 |  |
| g35 | -0.30 | BRAKE_END | B | - | B:e22 @ 3.50 |  |
| g36 | -0.10 | EGO_PATH_ENTRY | B | A | B:e23 @ 3.70 |  |
| g37 | -0.05 | TRACK_LOST | A | B | A:e08 @ 3.75 |  |
| g38 | -0.05 | TRACK_LOST | B | B:track_003 | B:e24 @ 3.75 |  |
| g39 | -0.05 | TRACK_LOST | B | B:track_004 | B:e25 @ 3.75 |  |
| g40 | -0.05 | TRACK_LOST | B | B:track_005 | B:e26 @ 3.75 |  |
| g41 | -0.05 | TRACK_LOST | B | B:track_006 | B:e27 @ 3.75 |  |
| g42 | -0.05 | TRACK_LOST | B | B:track_007 | B:e28 @ 3.75 |  |
| g43 | 0.00 | COLLISION | - | A, B | A:e09 @ 3.80, B:e29 @ 3.80 | matched_event=collision_001; reference_event=True; peak_impulse=A 9797.50, B 9797.50 |
| g44 | 0.00 | TURN_LEFT_END | B | - | B:e30 @ 3.80 |  |
| g45 | 0.00 | TURN_LEFT_START | A | - | A:e10 @ 3.80 |  |
| g46 | 0.05 | BRAKE_START | B | - | B:e31 @ 3.85 |  |
| g47 | 0.05 | TRACK_APPEARED_RIGHT | B | B:track_008 | B:e32 @ 3.85 |  |
| g48 | 0.05 | CLOSING_START | B | B:track_008 | B:e33 @ 3.85 | active_at_first_observation=True |
| g49 | 0.05 | CRITICAL_TTC_START | B | B:track_008 | B:e34 @ 3.85 | active_at_first_observation=True |
| g50 | 0.20 | MOVING_END | B | - | B:e35 @ 4.00 |  |
| g51 | 0.20 | STOP_START | B | - | B:e36 @ 4.00 |  |
| g52 | 0.30 | CRITICAL_TTC_END | B | A | B:e37 @ 4.10 |  |
| g53 | 0.35 | TRACK_LOST | B | B:track_008 | B:e38 @ 4.15 |  |
| g54 | 0.50 | CLOSING_END | B | A | B:e39 @ 4.30 |  |
| g55 | 0.65 | TRACK_LOST | C | C:track_001 | C:e07 @ 4.45 |  |
| g56 | 0.70 | EGO_PATH_ENTRY | A | C | A:e11 @ 4.50 |  |
| g57 | 0.80 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e12 @ 4.60 | relevant_to_ego_path=False |
| g58 | 0.80 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e13 @ 4.60 |  |
| g59 | 0.95 | COLLISION | - | A, C | A:e14 @ 4.75, C:e08 @ 4.75 | matched_event=collision_002; reference_event=False; peak_impulse=A 1637.56, C 1637.56 |
| g60 | 1.00 | CRITICAL_TTC_END | A | C | A:e15 @ 4.80 |  |
| g61 | 1.00 | CLOSING_END | A | C | A:e16 @ 4.80 |  |
| g62 | 1.00 | EGO_PATH_EXIT | B | A | B:e40 @ 4.80 |  |
| g63 | 1.00 | BRAKE_START | C | - | C:e09 @ 4.80 |  |
| g64 | 1.15 | TURN_LEFT_END | A | - | A:e17 @ 4.95 |  |
| g65 | 1.15 | EGO_PATH_ENTRY | C | A | C:e10 @ 4.95 |  |
| g66 | 1.20 | CRITICAL_TTC_END | C | A | C:e11 @ 5.00 |  |
| g67 | 1.25 | CLOSING_END | C | A | C:e12 @ 5.05 |  |
| g68 | 1.25 | MOVING_END | A | - | A:e18 @ 5.05 |  |
| g69 | 1.25 | MOVING_END | C | - | C:e13 @ 5.05 |  |
| g70 | 1.25 | STOP_START | A | - | A:e19 @ 5.05 |  |
| g71 | 1.25 | STOP_START | C | - | C:e14 @ 5.05 |  |
| g72 | 1.50 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e20 @ 5.30 | relevant_to_ego_path=False |
| g73 | 4.00 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e21 @ 7.80 |  |
| g74 | 4.90 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e22 @ 8.70 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| g75 | 4.90 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e23 @ 8.70 | sign_track=sign-3 |
| g76 | 5.80 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e24 @ 9.60 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| g77 | 6.10 | STOP_SIGN_DETECTED_END | A | A:sign-2 | A:e25 @ 9.90 | sign_track=sign-4 |
| g78 | 7.10 | STOP_SIGN_DETECTED_START | A | A:sign-2 | A:e26 @ 10.90 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-5 |

## Edges

```
    g01 --PRECEDES--> g06
    g01 --PRECEDES--> g07
    g01 --PRECEDES--> g08
    g01 --PRECEDES--> g09
    g02 --PRECEDES--> g06
    g02 --PRECEDES--> g07
    g02 --PRECEDES--> g08
    g02 --PRECEDES--> g09
    g03 --PRECEDES--> g06
    g03 --PRECEDES--> g07
    g03 --PRECEDES--> g08
    g03 --PRECEDES--> g09
    g04 --PRECEDES--> g06
    g04 --PRECEDES--> g07
    g04 --PRECEDES--> g08
    g04 --PRECEDES--> g09
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g05 --PRECEDES--> g08
    g05 --PRECEDES--> g09
    g06 --PRECEDES--> g10
    g06 --PRECEDES--> g11
    g07 --PRECEDES--> g10
    g07 --PRECEDES--> g11
    g08 --PRECEDES--> g10
    g08 --PRECEDES--> g11
    g09 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g15 --PRECEDES--> g18
    g16 --PRECEDES--> g18
    g17 --PRECEDES--> g18
    g18 --PRECEDES--> g19
    g19 --PRECEDES--> g20
    g20 --PRECEDES--> g21
    g21 --PRECEDES--> g22
    g22 --PRECEDES--> g23
    g23 --PRECEDES--> g24
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g23 --PRECEDES--> g28
    g23 --PRECEDES--> g29
    g23 --PRECEDES--> g30
    g23 --PRECEDES--> g31
    g24 --PRECEDES--> g32
    g24 --PRECEDES--> g33
    g25 --PRECEDES--> g32
    g25 --PRECEDES--> g33
    g26 --PRECEDES--> g32
    g26 --PRECEDES--> g33
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g36 --PRECEDES--> g41
    g36 --PRECEDES--> g42
    g37 --PRECEDES--> g43
    g37 --PRECEDES--> g44
    g37 --PRECEDES--> g45
    g38 --PRECEDES--> g43
    g38 --PRECEDES--> g44
    g38 --PRECEDES--> g45
    g39 --PRECEDES--> g43
    g39 --PRECEDES--> g44
    g39 --PRECEDES--> g45
    g40 --PRECEDES--> g43
    g40 --PRECEDES--> g44
    g40 --PRECEDES--> g45
    g41 --PRECEDES--> g43
    g41 --PRECEDES--> g44
    g41 --PRECEDES--> g45
    g42 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g44 --PRECEDES--> g46
    g44 --PRECEDES--> g47
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g45 --PRECEDES--> g46
    g45 --PRECEDES--> g47
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g46 --PRECEDES--> g50
    g46 --PRECEDES--> g51
    g47 --PRECEDES--> g50
    g47 --PRECEDES--> g51
    g48 --PRECEDES--> g50
    g48 --PRECEDES--> g51
    g49 --PRECEDES--> g50
    g49 --PRECEDES--> g51
    g50 --PRECEDES--> g52
    g51 --PRECEDES--> g52
    g52 --PRECEDES--> g53
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g55 --PRECEDES--> g56
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g57 --PRECEDES--> g59
    g58 --PRECEDES--> g59
    g59 --PRECEDES--> g60
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g60 --PRECEDES--> g64
    g60 --PRECEDES--> g65
    g61 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g62 --PRECEDES--> g64
    g62 --PRECEDES--> g65
    g63 --PRECEDES--> g64
    g63 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g65 --PRECEDES--> g66
    g66 --PRECEDES--> g67
    g66 --PRECEDES--> g68
    g66 --PRECEDES--> g69
    g66 --PRECEDES--> g70
    g66 --PRECEDES--> g71
    g67 --PRECEDES--> g72
    g68 --PRECEDES--> g72
    g69 --PRECEDES--> g72
    g70 --PRECEDES--> g72
    g71 --PRECEDES--> g72
    g72 --PRECEDES--> g73
    g73 --PRECEDES--> g74
    g73 --PRECEDES--> g75
    g74 --PRECEDES--> g76
    g75 --PRECEDES--> g76
    g76 --PRECEDES--> g77
    g77 --PRECEDES--> g78
    g06 --SAME_TRACK--> g08
    g15 --SAME_TRACK--> g16
    g15 --SAME_TRACK--> g17
    g06 --SAME_TRACK--> g21
    g15 --SAME_TRACK--> g37
    g06 --SAME_TRACK--> g56
    g06 --SAME_TRACK--> g60
    g06 --SAME_TRACK--> g61
    g10 --SAME_TRACK--> g11
    g13 --SAME_TRACK--> g14
    g13 --SAME_TRACK--> g19
    g24 --SAME_TRACK--> g28
    g25 --SAME_TRACK--> g29
    g26 --SAME_TRACK--> g30
    g27 --SAME_TRACK--> g31
    g32 --SAME_TRACK--> g33
    g10 --SAME_TRACK--> g34
    g13 --SAME_TRACK--> g36
    g24 --SAME_TRACK--> g38
    g25 --SAME_TRACK--> g39
    g26 --SAME_TRACK--> g40
    g27 --SAME_TRACK--> g41
    g32 --SAME_TRACK--> g42
    g47 --SAME_TRACK--> g48
    g47 --SAME_TRACK--> g49
    g13 --SAME_TRACK--> g52
    g47 --SAME_TRACK--> g53
    g13 --SAME_TRACK--> g54
    g13 --SAME_TRACK--> g62
    g04 --SAME_TRACK--> g05
    g07 --SAME_TRACK--> g09
    g07 --SAME_TRACK--> g22
    g04 --SAME_TRACK--> g55
    g07 --SAME_TRACK--> g65
    g07 --SAME_TRACK--> g66
    g07 --SAME_TRACK--> g67
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -3.80 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_LEFT(C,C:track_001); CLOSING_START(C,C:track_001) |
| -3.75 | TRACK_APPEARED_FRONT(A,C); TRACK_APPEARED_FRONT(C,A); CLOSING_START(A,C); CLOSING_START(C,A) |
| -2.35 | TRACK_APPEARED_RIGHT(B,B:track_001); CLOSING_START(B,B:track_001) |
| -2.30 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -1.85 | TRACK_APPEARED_LEFT(B,A); CLOSING_START(B,A) |
| -1.80 | TRACK_APPEARED_RIGHT(A,B); CLOSING_START(A,B); CRITICAL_TTC_START(A,B) |
| -1.70 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -1.65 | CRITICAL_TTC_START(B,A) |
| -1.55 | TURN_LEFT_START(B) |
| -1.25 | CRITICAL_TTC_START(A,C) |
| -0.90 | CRITICAL_TTC_START(C,A) |
| -0.85 | BRAKE_START(B) |
| -0.75 | TRACK_APPEARED_LEFT(B,B:track_003); TRACK_APPEARED_LEFT(B,B:track_004); TRACK_APPEARED_LEFT(B,B:track_005); TRACK_APPEARED_LEFT(B,B:track_006); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005); CLOSING_START(B,B:track_006) |
| -0.70 | TRACK_APPEARED_LEFT(B,B:track_007); CLOSING_START(B,B:track_007) |
| -0.65 | TRACK_LOST(B,B:track_001) |
| -0.30 | BRAKE_END(B) |
| -0.10 | EGO_PATH_ENTRY(B,A) |
| -0.05 | TRACK_LOST(A,B); TRACK_LOST(B,B:track_003); TRACK_LOST(B,B:track_004); TRACK_LOST(B,B:track_005); TRACK_LOST(B,B:track_006); TRACK_LOST(B,B:track_007) |
| +0.00 | COLLISION(A,B); TURN_LEFT_END(B); TURN_LEFT_START(A) |
| +0.05 | BRAKE_START(B); TRACK_APPEARED_RIGHT(B,B:track_008); CLOSING_START(B,B:track_008); CRITICAL_TTC_START(B,B:track_008) |
| +0.20 | MOVING_END(B); STOP_START(B) |
| +0.30 | CRITICAL_TTC_END(B,A) |
| +0.35 | TRACK_LOST(B,B:track_008) |
| +0.50 | CLOSING_END(B,A) |
| +0.65 | TRACK_LOST(C,C:track_001) |
| +0.70 | EGO_PATH_ENTRY(A,C) |
| +0.80 | STOP_SIGN_DETECTED_START(A,A:sign-0); STOP_SIGN_DETECTED_END(A,A:sign-0) |
| +0.95 | COLLISION(A,C) |
| +1.00 | CRITICAL_TTC_END(A,C); CLOSING_END(A,C); EGO_PATH_EXIT(B,A); BRAKE_START(C) |
| +1.15 | TURN_LEFT_END(A); EGO_PATH_ENTRY(C,A) |
| +1.20 | CRITICAL_TTC_END(C,A) |
| +1.25 | CLOSING_END(C,A); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |
| +1.50 | STOP_SIGN_DETECTED_START(A,A:sign-2) |
| +4.00 | STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +4.90 | STOP_SIGN_DETECTED_START(A,A:sign-2); STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +5.80 | STOP_SIGN_DETECTED_START(A,A:sign-2) |
| +6.10 | STOP_SIGN_DETECTED_END(A,A:sign-2) |
| +7.10 | STOP_SIGN_DETECTED_START(A,A:sign-2) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (C): CRITICAL_TTC_START 2.55, COLLISION with C 4.75 (+2.20 s); EGO_PATH_ENTRY 4.50 after critical TTC (+1.95 s) [local times; t_global: critical_ttc_start -1.25, ego_path_entry +0.70, collision +0.95]
- A's track_002 (B): CRITICAL_TTC_START 2.00, COLLISION with B 3.80 (+1.80 s) [local times; t_global: critical_ttc_start -1.80, collision +0.00]
- B's track_002 (A): CRITICAL_TTC_START 2.15, COLLISION with A 3.80 (+1.65 s); EGO_PATH_ENTRY 3.70 after critical TTC (+1.55 s) [local times; t_global: critical_ttc_start -1.65, ego_path_entry -0.10, collision +0.00]
- B's track_008 (unidentified B:track_008): CRITICAL_TTC_START 3.85 [local times; t_global: critical_ttc_start +0.05]
- C's track_002 (A): CRITICAL_TTC_START 2.90, COLLISION with A 4.75 (+1.85 s); EGO_PATH_ENTRY 4.95 after critical TTC (+2.05 s) [local times; t_global: critical_ttc_start -0.90, ego_path_entry +1.15, collision +0.95]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -3.80 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -3.80 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -3.80 | C | g03 MOVING_START(C) (C:e01)<br>g04 TRACK_APPEARED_LEFT(C,C:track_001) (C:e02)<br>g05 CLOSING_START(C,C:track_001) (C:e03) | ego: not yet observed |
| -3.75 | A | g06 TRACK_APPEARED_FRONT(A,C) (A:e02)<br>g08 CLOSING_START(A,C) (A:e03) | ego: MOVING |
| -3.75 | C | g07 TRACK_APPEARED_FRONT(C,A) (C:e04)<br>g09 CLOSING_START(C,A) (C:e05) | ego: MOVING<br>track_001: CLOSING |
| -2.35 | B | g10 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e02)<br>g11 CLOSING_START(B,B:track_001) (B:e03) | ego: MOVING |
| -2.30 | B | g12 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.85 | B | g13 TRACK_APPEARED_LEFT(B,A) (B:e05)<br>g14 CLOSING_START(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known |
| -1.80 | A | g15 TRACK_APPEARED_RIGHT(A,B) (A:e04)<br>g16 CLOSING_START(A,B) (A:e05)<br>g17 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING<br>track_001: CLOSING |
| -1.70 | B | g18 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |
| -1.65 | B | g19 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING<br>sign-0: STOP sign known |
| -1.55 | B | g20 TURN_LEFT_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -1.25 | A | g21 CRITICAL_TTC_START(A,C) (A:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| -0.90 | C | g22 CRITICAL_TTC_START(C,A) (C:e06) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING |
| -0.85 | B | g23 BRAKE_START(B) (B:e10) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.75 | B | g24 TRACK_APPEARED_LEFT(B,B:track_003) (B:e11)<br>g25 TRACK_APPEARED_LEFT(B,B:track_004) (B:e12)<br>g26 TRACK_APPEARED_LEFT(B,B:track_005) (B:e13)<br>g27 TRACK_APPEARED_LEFT(B,B:track_006) (B:e14)<br>g28 CLOSING_START(B,B:track_003) (B:e15)<br>g29 CLOSING_START(B,B:track_004) (B:e16)<br>g30 CLOSING_START(B,B:track_005) (B:e17)<br>g31 CLOSING_START(B,B:track_006) (B:e18) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known |
| -0.70 | B | g32 TRACK_APPEARED_LEFT(B,B:track_007) (B:e19)<br>g33 CLOSING_START(B,B:track_007) (B:e20) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>sign-0: STOP sign known |
| -0.65 | B | g34 TRACK_LOST(B,B:track_001) (B:e21) | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>sign-0: STOP sign known |
| -0.30 | B | g35 BRAKE_END(B) (B:e22) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| -0.10 | B | g36 EGO_PATH_ENTRY(B,A) (B:e23) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| -0.05 | A | g37 TRACK_LOST(A,B) (A:e08) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC |
| -0.05 | B | g38 TRACK_LOST(B,B:track_003) (B:e24)<br>g39 TRACK_LOST(B,B:track_004) (B:e25)<br>g40 TRACK_LOST(B,B:track_005) (B:e26)<br>g41 TRACK_LOST(B,B:track_006) (B:e27)<br>g42 TRACK_LOST(B,B:track_007) (B:e28) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known |
| +0.00 | A | g43 COLLISION(A,B) (A:e09)<br>g45 TURN_LEFT_START(A) (A:e10) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.00 | B | g43 COLLISION(A,B) (B:e29)<br>g44 TURN_LEFT_END(B) (B:e30) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known |
| +0.05 | B | g46 BRAKE_START(B) (B:e31)<br>g47 TRACK_APPEARED_RIGHT(B,B:track_008) (B:e32)<br>g48 CLOSING_START(B,B:track_008) (B:e33)<br>g49 CRITICAL_TTC_START(B,B:track_008) (B:e34) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known |
| +0.20 | B | g50 MOVING_END(B) (B:e35)<br>g51 STOP_START(B) (B:e36) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known |
| +0.30 | B | g52 CRITICAL_TTC_END(B,A) (B:e37) | ego: STOP, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known |
| +0.35 | B | g53 TRACK_LOST(B,B:track_008) (B:e38) | ego: STOP, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track_008: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007<br>sign-0: STOP sign known |
| +0.50 | B | g54 CLOSING_END(B,A) (B:e39) | ego: STOP, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008<br>sign-0: STOP sign known |
| +0.65 | C | g55 TRACK_LOST(C,C:track_001) (C:e07) | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC |
| +0.70 | A | g56 EGO_PATH_ENTRY(A,C) (A:e11) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 |
| +0.80 | A | g57 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e12)<br>g58 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e13) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 |
| +0.95 | A | g59 COLLISION(A,C) (A:e14) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +0.95 | C | g59 COLLISION(A,C) (C:e08) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| +1.00 | A | g60 CRITICAL_TTC_END(A,C) (A:e15)<br>g61 CLOSING_END(A,C) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.00 | B | g62 EGO_PATH_EXIT(B,A) (B:e40) | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001, track_003, track_004, track_005, track_006, track_007, track_008<br>sign-0: STOP sign known |
| +1.00 | C | g63 BRAKE_START(C) (C:e09) | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| +1.15 | A | g64 TURN_LEFT_END(A) (A:e17) | ego: MOVING, TURN_LEFT<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.15 | C | g65 EGO_PATH_ENTRY(C,A) (C:e10) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 |
| +1.20 | C | g66 CRITICAL_TTC_END(C,A) (C:e11) | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +1.25 | C | g67 CLOSING_END(C,A) (C:e12)<br>g69 MOVING_END(C) (C:e13)<br>g71 STOP_START(C) (C:e14) | ego: MOVING, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 |
| +1.25 | A | g68 MOVING_END(A) (A:e18)<br>g70 STOP_START(A) (A:e19) | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +1.50 | A | g72 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e20) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known |
| +4.00 | A | g73 STOP_SIGN_DETECTED_END(A,A:sign-2) (A:e21) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +4.90 | A | g74 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e22)<br>g75 STOP_SIGN_DETECTED_END(A,A:sign-2) (A:e23) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +5.80 | A | g76 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e24) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +6.10 | A | g77 STOP_SIGN_DETECTED_END(A,A:sign-2) (A:e25) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |
| +7.10 | A | g78 STOP_SIGN_DETECTED_START(A,A:sign-2) (A:e26) | ego: STOP<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002<br>sign-0: STOP sign known<br>sign-2: STOP sign known |

## Plain-language reading

- 3.80 s before the reference collision, A started moving (already the case when first observed).
- 3.80 s before the reference collision, B started moving (already the case when first observed).
- 3.80 s before the reference collision, C started moving (already the case when first observed).
- 3.80 s before the reference collision, C's radar started tracking unidentified object C:track_001, which appeared on its left.
- 3.80 s before the reference collision, C observed unidentified object C:track_001 start closing in (already the case when first observed).
- 3.75 s before the reference collision, A's radar started tracking C, which appeared in front of it.
- 3.75 s before the reference collision, C's radar started tracking A, which appeared in front of it.
- 3.75 s before the reference collision, A observed C start closing in (already the case when first observed).
- 3.75 s before the reference collision, C observed A start closing in (already the case when first observed).
- 2.35 s before the reference collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 2.35 s before the reference collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 2.30 s before the reference collision, B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- 1.85 s before the reference collision, B's radar started tracking A, which appeared on its left.
- 1.85 s before the reference collision, B observed A start closing in (already the case when first observed).
- 1.80 s before the reference collision, A's radar started tracking B, which appeared on its right.
- 1.80 s before the reference collision, A observed B start closing in (already the case when first observed).
- 1.80 s before the reference collision, A's time-to-contact with B became critical (already the case when first observed).
- 1.70 s before the reference collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 1.65 s before the reference collision, B's time-to-contact with A became critical.
- 1.55 s before the reference collision, B started turning left.
- 1.25 s before the reference collision, A's time-to-contact with C became critical.
- 0.90 s before the reference collision, C's time-to-contact with A became critical.
- 0.85 s before the reference collision, B started braking.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_003, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_004, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_005, which appeared on its left.
- 0.75 s before the reference collision, B's radar started tracking unidentified object B:track_006, which appeared on its left.
- 0.75 s before the reference collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.75 s before the reference collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.70 s before the reference collision, B's radar started tracking unidentified object B:track_007, which appeared on its left.
- 0.70 s before the reference collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.65 s before the reference collision, B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- 0.30 s before the reference collision, B released the brake.
- 0.10 s before the reference collision, B observed A enter its forward path corridor.
- 0.05 s before the reference collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_003 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_004 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_005 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_006 (its states are UNKNOWN from then on, not ended).
- 0.05 s before the reference collision, B's radar lost unidentified object B:track_007 (its states are UNKNOWN from then on, not ended).
- At the reference collision, A and B both recorded this same collision (peak impulses A: 9798, B: 9798 N*s).
- At the reference collision, B stopped turning left.
- At the reference collision, A started turning left.
- 0.05 s after the reference collision, B started braking.
- 0.05 s after the reference collision, B's radar started tracking unidentified object B:track_008, which appeared on its right.
- 0.05 s after the reference collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.05 s after the reference collision, B's time-to-contact with unidentified object B:track_008 became critical (already the case when first observed).
- 0.20 s after the reference collision, B stopped moving.
- 0.20 s after the reference collision, B came to a stop.
- 0.30 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.35 s after the reference collision, B's radar lost unidentified object B:track_008 (its states are UNKNOWN from then on, not ended).
- 0.50 s after the reference collision, B observed A stop closing in.
- 0.65 s after the reference collision, C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
- 0.70 s after the reference collision, A observed C enter its forward path corridor.
- 0.80 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- 0.80 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 0.95 s after the reference collision, A and C both recorded this same collision (peak impulses A: 1638, C: 1638 N*s).
- 1.00 s after the reference collision, A's time-to-contact with C stopped being critical.
- 1.00 s after the reference collision, A observed C stop closing in.
- 1.00 s after the reference collision, B observed A leave its forward path corridor.
- 1.00 s after the reference collision, C started braking.
- 1.15 s after the reference collision, A stopped turning left.
- 1.15 s after the reference collision, C observed A enter its forward path corridor.
- 1.20 s after the reference collision, C's time-to-contact with A stopped being critical.
- 1.25 s after the reference collision, C observed A stop closing in.
- 1.25 s after the reference collision, A stopped moving.
- 1.25 s after the reference collision, C stopped moving.
- 1.25 s after the reference collision, A came to a stop.
- 1.25 s after the reference collision, C came to a stop.
- 1.50 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path).
- 4.00 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 4.90 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- 4.90 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 5.80 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- 6.10 s after the reference collision, A's camera stopped detecting STOP sign unidentified object A:sign-2.
- 7.10 s after the reference collision, A's camera established a STOP sign detection (unidentified object A:sign-2) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-5).
