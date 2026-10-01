# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock ALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: C |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| A:track_004 | anonymous_track | seen only by A; candidate: C |
| A:track_005 | anonymous_track | seen only by A; candidate: C |
| A:track_006 | anonymous_track | seen only by A; candidate: C |

## Graph alignment

Reference event: `collision_001` (t_global = 0); `t_global = t_local + offset_to_global`. A graph that did not report it is aligned through the chain of matched collisions linking it to the reference (multi-hop); its anchor is its own report of the last collision of that chain.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e03 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | ALIGNED | C:e04 | 5.90 | -5.15 | shares collision_002 with A, aligned through collision_001 -> collision_002 |

Estimated relative clock offsets: B - A = +0.000 s, C - A = +0.000 s, C - B = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 4.7 m -> 0.6 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 1.66 m/s over 0.8 s (> 1.50)<br>range at the contact 0.56 m<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 15.89 m (beyond 3.50 m: confidence factor 0.00)<br>collision_002 with C at 5.90 s: not compatible (tracked for 0.75 s before the matched collision (needs 1.00 s); not approaching before the contact: range 15.9 m -> 16.6 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 7.92 m/s over 0.8 s (> 1.50)) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 at 5.15 s (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 13.50 m (beyond 3.50 m: confidence factor 0.00)<br>collision_002 with C at 5.90 s: not compatible (tracked for 0.75 s before the matched collision (needs 1.00 s); not approaching before the contact: range 13.5 m -> 14.4 m over the last 1.0 s; track speed disagrees with C's own speed: RMSE 6.03 m/s over 0.8 s (> 1.50)) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.75 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 21.7 m -> 19.7 m over the last 1.0 s<br>track speed agrees with C's own speed: RMSE 0.45 m/s over 0.8 s<br>range at the contact 19.42 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 14.2 m -> 15.1 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 5.31 m/s over 0.4 s (> 1.50)<br>range at the contact 14.23 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.35 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and C both reported collision_002 at 5.90 s (peak impulse 2695.68 vs 2695.68 N*s)<br>tracked for 0.40 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 19.0 m -> 19.9 m over the last 1.0 s<br>track speed disagrees with C's own speed: RMSE 2.83 m/s over 0.4 s (> 1.50)<br>range at the contact 19.02 m (beyond 3.50 m: confidence factor 0.00)<br>collision_001 with B at 5.15 s: not compatible (tracked for 0.00 s before the matched collision (needs 1.00 s); first seen 0.35 s after the matched collision; range trend before the contact not measurable; speed not comparable with B's own speed before the collision) |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 4.0 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.51 m/s over 3.0 s<br>range at the contact 0.59 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g04 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g05 | -4.85 | MOVING_END | C | - | C:e02 @ 0.30 |  |
| g06 | -4.85 | STOP_START | C | - | C:e03 @ 0.30 |  |
| g07 | -4.45 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g08 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g09 | -3.75 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g10 | -3.75 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g11 | -1.20 | BRAKE_START | A | - | A:e02 @ 3.95 |  |
| g12 | -0.90 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g13 | -0.70 | CRITICAL_TTC_START | B | A | B:e08 @ 4.45 |  |
| g14 | -0.40 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g15 | 0.00 | COLLISION | - | A, B | A:e03 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g16 | 0.00 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e04 @ 5.15 |  |
| g17 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_002 | A:e05 @ 5.15 |  |
| g18 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_003 | A:e06 @ 5.15 |  |
| g19 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_004 | A:e07 @ 5.15 |  |
| g20 | 0.00 | CLOSING_START | A | A:track_001 | A:e08 @ 5.15 | active_at_first_observation=True |
| g21 | 0.00 | CLOSING_START | A | A:track_002 | A:e09 @ 5.15 | active_at_first_observation=True |
| g22 | 0.00 | CLOSING_START | A | A:track_003 | A:e10 @ 5.15 | active_at_first_observation=True |
| g23 | 0.00 | CLOSING_START | A | A:track_004 | A:e11 @ 5.15 | active_at_first_observation=True |
| g24 | 0.00 | CRITICAL_TTC_START | A | A:track_001 | A:e12 @ 5.15 | active_at_first_observation=True |
| g25 | 0.05 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g26 | 0.05 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g27 | 0.05 | BRAKE_END | A | - | A:e13 @ 5.20 |  |
| g28 | 0.25 | TURN_LEFT_START | A | - | A:e14 @ 5.40 |  |
| g29 | 0.30 | CLOSING_END | A | A:track_002 | A:e15 @ 5.45 |  |
| g30 | 0.30 | CLOSING_END | A | A:track_003 | A:e16 @ 5.45 |  |
| g31 | 0.35 | TRACK_APPEARED_RIGHT | A | A:track_005 | A:e17 @ 5.50 |  |
| g32 | 0.35 | TRACK_APPEARED_RIGHT | A | A:track_006 | A:e18 @ 5.50 |  |
| g33 | 0.45 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g34 | 0.45 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g35 | 0.55 | CLOSING_END | A | A:track_004 | A:e19 @ 5.70 |  |
| g36 | 0.55 | EGO_PATH_ENTRY | A | A:track_001 | A:e20 @ 5.70 |  |
| g37 | 0.75 | COLLISION | - | A, C | A:e21 @ 5.90, C:e04 @ 5.90 | matched_event=collision_002; reference_event=False; peak_impulse=A 2695.68, C 2695.68 |
| g38 | 0.75 | STOP_END | C | - | C:e05 @ 5.90 |  |
| g39 | 0.75 | MOVING_START | C | - | C:e06 @ 5.90 |  |
| g40 | 0.80 | BRAKE_START | C | - | C:e07 @ 5.95 |  |
| g41 | 0.80 | TRACK_LOST | A | A:track_005 | A:e22 @ 5.95 |  |
| g42 | 0.85 | CRITICAL_TTC_END | A | A:track_001 | A:e23 @ 6.00 |  |
| g43 | 0.85 | TURN_LEFT_END | A | - | A:e24 @ 6.00 |  |
| g44 | 0.90 | CLOSING_END | A | A:track_001 | A:e25 @ 6.05 |  |
| g45 | 0.90 | MOVING_END | A | - | A:e26 @ 6.05 |  |
| g46 | 0.90 | MOVING_END | C | - | C:e08 @ 6.05 |  |
| g47 | 0.90 | STOP_START | A | - | A:e27 @ 6.05 |  |
| g48 | 0.90 | STOP_START | C | - | C:e09 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g01 --PRECEDES--> g06
    g02 --PRECEDES--> g05
    g02 --PRECEDES--> g06
    g03 --PRECEDES--> g05
    g03 --PRECEDES--> g06
    g04 --PRECEDES--> g05
    g04 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g11
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g14 --PRECEDES--> g19
    g14 --PRECEDES--> g20
    g14 --PRECEDES--> g21
    g14 --PRECEDES--> g22
    g14 --PRECEDES--> g23
    g14 --PRECEDES--> g24
    g15 --PRECEDES--> g25
    g15 --PRECEDES--> g26
    g15 --PRECEDES--> g27
    g16 --PRECEDES--> g25
    g16 --PRECEDES--> g26
    g16 --PRECEDES--> g27
    g17 --PRECEDES--> g25
    g17 --PRECEDES--> g26
    g17 --PRECEDES--> g27
    g18 --PRECEDES--> g25
    g18 --PRECEDES--> g26
    g18 --PRECEDES--> g27
    g19 --PRECEDES--> g25
    g19 --PRECEDES--> g26
    g19 --PRECEDES--> g27
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g23 --PRECEDES--> g27
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g24 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g26 --PRECEDES--> g28
    g27 --PRECEDES--> g28
    g28 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g30 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g31 --PRECEDES--> g34
    g32 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g35
    g33 --PRECEDES--> g36
    g34 --PRECEDES--> g35
    g34 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g36 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g37 --PRECEDES--> g41
    g38 --PRECEDES--> g40
    g38 --PRECEDES--> g41
    g39 --PRECEDES--> g40
    g39 --PRECEDES--> g41
    g40 --PRECEDES--> g42
    g40 --PRECEDES--> g43
    g41 --PRECEDES--> g42
    g41 --PRECEDES--> g43
    g42 --PRECEDES--> g44
    g42 --PRECEDES--> g45
    g42 --PRECEDES--> g46
    g42 --PRECEDES--> g47
    g42 --PRECEDES--> g48
    g43 --PRECEDES--> g44
    g43 --PRECEDES--> g45
    g43 --PRECEDES--> g46
    g43 --PRECEDES--> g47
    g43 --PRECEDES--> g48
    g16 --SAME_TRACK--> g20
    g17 --SAME_TRACK--> g21
    g18 --SAME_TRACK--> g22
    g19 --SAME_TRACK--> g23
    g16 --SAME_TRACK--> g24
    g17 --SAME_TRACK--> g29
    g18 --SAME_TRACK--> g30
    g19 --SAME_TRACK--> g35
    g16 --SAME_TRACK--> g36
    g31 --SAME_TRACK--> g41
    g16 --SAME_TRACK--> g42
    g16 --SAME_TRACK--> g44
    g04 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g10
    g04 --SAME_TRACK--> g12
    g04 --SAME_TRACK--> g13
    g04 --SAME_TRACK--> g25
    g04 --SAME_TRACK--> g26
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); MOVING_START(C); TRACK_APPEARED_FRONT(B,A) |
| -4.85 | MOVING_END(C); STOP_START(C) |
| -4.45 | CLOSING_START(B,A) |
| -4.40 | CRITICAL_TTC_START(B,A) |
| -3.75 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A) |
| -1.20 | BRAKE_START(A) |
| -0.90 | CLOSING_START(B,A) |
| -0.70 | CRITICAL_TTC_START(B,A) |
| -0.40 | BRAKE_START(B) |
| +0.00 | COLLISION(A,B); TRACK_APPEARED_LEFT(A,A:track_001); TRACK_APPEARED_RIGHT(A,A:track_002); TRACK_APPEARED_RIGHT(A,A:track_003); TRACK_APPEARED_RIGHT(A,A:track_004); CLOSING_START(A,A:track_001); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CRITICAL_TTC_START(A,A:track_001) |
| +0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); BRAKE_END(A) |
| +0.25 | TURN_LEFT_START(A) |
| +0.30 | CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_003) |
| +0.35 | TRACK_APPEARED_RIGHT(A,A:track_005); TRACK_APPEARED_RIGHT(A,A:track_006) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.55 | CLOSING_END(A,A:track_004); EGO_PATH_ENTRY(A,A:track_001) |
| +0.75 | COLLISION(A,C); STOP_END(C); MOVING_START(C) |
| +0.80 | BRAKE_START(C); TRACK_LOST(A,A:track_005) |
| +0.85 | CRITICAL_TTC_END(A,A:track_001); TURN_LEFT_END(A) |
| +0.90 | CLOSING_END(A,A:track_001); MOVING_END(A); MOVING_END(C); STOP_START(A); STOP_START(C) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 5.15, COLLISION 5.15 (+0.00 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.55 s) [local times; t_global: critical_ttc_start +0.00, ego_path_entry +0.55, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION with A 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g04 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -5.15 | C | g03 MOVING_START(C) (C:e01) | ego: not yet observed |
| -4.85 | C | g05 MOVING_END(C) (C:e02)<br>g06 STOP_START(C) (C:e03) | ego: MOVING |
| -4.45 | B | g07 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.40 | B | g08 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.75 | B | g09 CRITICAL_TTC_END(B,A) (B:e05)<br>g10 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.20 | A | g11 BRAKE_START(A) (A:e02) | ego: MOVING |
| -0.90 | B | g12 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.70 | B | g13 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g14 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g15 COLLISION(A,B) (A:e03)<br>g16 TRACK_APPEARED_LEFT(A,A:track_001) (A:e04)<br>g17 TRACK_APPEARED_RIGHT(A,A:track_002) (A:e05)<br>g18 TRACK_APPEARED_RIGHT(A,A:track_003) (A:e06)<br>g19 TRACK_APPEARED_RIGHT(A,A:track_004) (A:e07)<br>g20 CLOSING_START(A,A:track_001) (A:e08)<br>g21 CLOSING_START(A,A:track_002) (A:e09)<br>g22 CLOSING_START(A,A:track_003) (A:e10)<br>g23 CLOSING_START(A,A:track_004) (A:e11)<br>g24 CRITICAL_TTC_START(A,A:track_001) (A:e12) | ego: MOVING, BRAKE |
| +0.00 | B | g15 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g25 CRITICAL_TTC_END(B,A) (B:e11)<br>g26 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g27 BRAKE_END(A) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.25 | A | g28 TURN_LEFT_START(A) (A:e14) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.30 | A | g29 CLOSING_END(A,A:track_002) (A:e15)<br>g30 CLOSING_END(A,A:track_003) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.35 | A | g31 TRACK_APPEARED_RIGHT(A,A:track_005) (A:e17)<br>g32 TRACK_APPEARED_RIGHT(A,A:track_006) (A:e18) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING |
| +0.45 | B | g33 MOVING_END(B) (B:e13)<br>g34 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.55 | A | g35 CLOSING_END(A,A:track_004) (A:e19)<br>g36 EGO_PATH_ENTRY(A,A:track_001) (A:e20) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING<br>track_005: no active state<br>track_006: no active state |
| +0.75 | A | g37 COLLISION(A,C) (A:e21) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state |
| +0.75 | C | g37 COLLISION(A,C) (C:e04)<br>g38 STOP_END(C) (C:e05)<br>g39 MOVING_START(C) (C:e06) | ego: STOP |
| +0.80 | C | g40 BRAKE_START(C) (C:e07) | ego: MOVING |
| +0.80 | A | g41 TRACK_LOST(A,A:track_005) (A:e22) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state |
| +0.85 | A | g42 CRITICAL_TTC_END(A,A:track_001) (A:e23)<br>g43 TURN_LEFT_END(A) (A:e24) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 |
| +0.90 | A | g44 CLOSING_END(A,A:track_001) (A:e25)<br>g45 MOVING_END(A) (A:e26)<br>g47 STOP_START(A) (A:e27) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 |
| +0.90 | C | g46 MOVING_END(C) (C:e08)<br>g48 STOP_START(C) (C:e09) | ego: MOVING, BRAKE |

## Plain-language reading

- 5.15 s before the reference collision, A started moving (already the case when first observed).
- 5.15 s before the reference collision, B started moving (already the case when first observed).
- 5.15 s before the reference collision, C started moving (already the case when first observed).
- 5.15 s before the reference collision, B's radar started tracking A, which appeared in front of it.
- 4.85 s before the reference collision, C stopped moving.
- 4.85 s before the reference collision, C came to a stop.
- 4.45 s before the reference collision, B observed A start closing in.
- 4.40 s before the reference collision, B's time-to-contact with A became critical.
- 3.75 s before the reference collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the reference collision, B observed A stop closing in.
- 1.20 s before the reference collision, A started braking.
- 0.90 s before the reference collision, B observed A start closing in.
- 0.70 s before the reference collision, B's time-to-contact with A became critical.
- 0.40 s before the reference collision, B started braking.
- At the reference collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the reference collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- At the reference collision, A's radar started tracking unidentified object A:track_002, which appeared on its right.
- At the reference collision, A's radar started tracking unidentified object A:track_003, which appeared on its right.
- At the reference collision, A's radar started tracking unidentified object A:track_004, which appeared on its right.
- At the reference collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- At the reference collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- At the reference collision, A's time-to-contact with unidentified object A:track_001 became critical (already the case when first observed).
- 0.05 s after the reference collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the reference collision, B observed A stop closing in.
- 0.05 s after the reference collision, A released the brake.
- 0.25 s after the reference collision, A started turning left.
- 0.30 s after the reference collision, A observed unidentified object A:track_002 stop closing in.
- 0.30 s after the reference collision, A observed unidentified object A:track_003 stop closing in.
- 0.35 s after the reference collision, A's radar started tracking unidentified object A:track_005, which appeared on its right.
- 0.35 s after the reference collision, A's radar started tracking unidentified object A:track_006, which appeared on its right.
- 0.45 s after the reference collision, B stopped moving.
- 0.45 s after the reference collision, B came to a stop.
- 0.55 s after the reference collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the reference collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.75 s after the reference collision, A and C both recorded this same collision (peak impulses A: 2696, C: 2696 N*s).
- 0.75 s after the reference collision, C left its stop.
- 0.75 s after the reference collision, C started moving.
- 0.80 s after the reference collision, C started braking.
- 0.80 s after the reference collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the reference collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s after the reference collision, A stopped turning left.
- 0.90 s after the reference collision, A observed unidentified object A:track_001 stop closing in.
- 0.90 s after the reference collision, A stopped moving.
- 0.90 s after the reference collision, C stopped moving.
- 0.90 s after the reference collision, A came to a stop.
- 0.90 s after the reference collision, C came to a stop.
