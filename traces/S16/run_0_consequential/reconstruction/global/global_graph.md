# Global graph - S16/run_0_consequential

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: B |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| A:track_004 | anonymous_track | seen only by A; candidate: B |
| A:track_005 | anonymous_track | seen only by A; candidate: B |
| A:track_006 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e03 | 5.15 | -5.15 | reported the reference collision collision_001 |
| B | ALIGNED | B:e10 | 5.15 | -5.15 | reported the reference collision collision_001 |
| C | UNALIGNED | - | - | - | shares only a non-reference collision (multi-hop alignment not implemented) |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 6073.81 vs 6073.81 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

Matched `collision_002`: A and C both recorded a collision; peak impulses 2695.68 vs 2695.68 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 4.65 m (beyond 3.50 m: confidence factor 0.93) |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 15.89 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 13.50 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 21.69 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.35 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.35 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.94 | B and A both reported collision_001 (peak impulse 6073.81 vs 6073.81 N*s)<br>tracked for 5.15 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 4.0 m -> 0.6 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 0.51 m/s over 3.0 s<br>range at the contact 0.59 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.15 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.15 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.15 | TRACK_APPEARED_FRONT | B | A | B:e02 @ 0.00 |  |
| g04 | -4.45 | CLOSING_START | B | A | B:e03 @ 0.70 |  |
| g05 | -4.40 | CRITICAL_TTC_START | B | A | B:e04 @ 0.75 |  |
| g06 | -3.75 | CRITICAL_TTC_END | B | A | B:e05 @ 1.40 |  |
| g07 | -3.75 | CLOSING_END | B | A | B:e06 @ 1.40 |  |
| g08 | -1.20 | BRAKE_START | A | - | A:e02 @ 3.95 |  |
| g09 | -0.90 | CLOSING_START | B | A | B:e07 @ 4.25 |  |
| g10 | -0.70 | CRITICAL_TTC_START | B | A | B:e08 @ 4.45 |  |
| g11 | -0.40 | BRAKE_START | B | - | B:e09 @ 4.75 |  |
| g12 | 0.00 | COLLISION | - | A, B | A:e03 @ 5.15, B:e10 @ 5.15 | matched_event=collision_001; reference_event=True; peak_impulse=A 6073.81, B 6073.81 |
| g13 | 0.00 | TRACK_APPEARED_LEFT | A | A:track_001 | A:e04 @ 5.15 |  |
| g14 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_002 | A:e05 @ 5.15 |  |
| g15 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_003 | A:e06 @ 5.15 |  |
| g16 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_004 | A:e07 @ 5.15 |  |
| g17 | 0.00 | CLOSING_START | A | A:track_001 | A:e08 @ 5.15 | active_at_first_observation=True |
| g18 | 0.00 | CLOSING_START | A | A:track_002 | A:e09 @ 5.15 | active_at_first_observation=True |
| g19 | 0.00 | CLOSING_START | A | A:track_003 | A:e10 @ 5.15 | active_at_first_observation=True |
| g20 | 0.00 | CLOSING_START | A | A:track_004 | A:e11 @ 5.15 | active_at_first_observation=True |
| g21 | 0.00 | CRITICAL_TTC_START | A | A:track_001 | A:e12 @ 5.15 | active_at_first_observation=True |
| g22 | 0.05 | CRITICAL_TTC_END | B | A | B:e11 @ 5.20 |  |
| g23 | 0.05 | CLOSING_END | B | A | B:e12 @ 5.20 |  |
| g24 | 0.05 | BRAKE_END | A | - | A:e13 @ 5.20 |  |
| g25 | 0.25 | TURN_LEFT_START | A | - | A:e14 @ 5.40 |  |
| g26 | 0.30 | CLOSING_END | A | A:track_002 | A:e15 @ 5.45 |  |
| g27 | 0.30 | CLOSING_END | A | A:track_003 | A:e16 @ 5.45 |  |
| g28 | 0.35 | TRACK_APPEARED_RIGHT | A | A:track_005 | A:e17 @ 5.50 |  |
| g29 | 0.35 | TRACK_APPEARED_RIGHT | A | A:track_006 | A:e18 @ 5.50 |  |
| g30 | 0.45 | MOVING_END | B | - | B:e13 @ 5.60 |  |
| g31 | 0.45 | STOP_START | B | - | B:e14 @ 5.60 |  |
| g32 | 0.55 | CLOSING_END | A | A:track_004 | A:e19 @ 5.70 |  |
| g33 | 0.55 | EGO_PATH_ENTRY | A | A:track_001 | A:e20 @ 5.70 |  |
| g34 | 0.75 | COLLISION | A | - | A:e21 @ 5.90 | peak_impulse=2695.68 |
| g35 | 0.80 | TRACK_LOST | A | A:track_005 | A:e22 @ 5.95 |  |
| g36 | 0.85 | CRITICAL_TTC_END | A | A:track_001 | A:e23 @ 6.00 |  |
| g37 | 0.85 | TURN_LEFT_END | A | - | A:e24 @ 6.00 |  |
| g38 | 0.90 | CLOSING_END | A | A:track_001 | A:e25 @ 6.05 |  |
| g39 | 0.90 | MOVING_END | A | - | A:e26 @ 6.05 |  |
| g40 | 0.90 | STOP_START | A | - | A:e27 @ 6.05 |  |
| g41 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g42 | - | MOVING_END | C | - | C:e02 @ 0.30 |  |
| g43 | - | STOP_START | C | - | C:e03 @ 0.30 |  |
| g44 | - | COLLISION | C | - | C:e04 @ 5.90 | peak_impulse=2695.68 |
| g45 | - | STOP_END | C | - | C:e05 @ 5.90 |  |
| g46 | - | MOVING_START | C | - | C:e06 @ 5.90 |  |
| g47 | - | BRAKE_START | C | - | C:e07 @ 5.95 |  |
| g48 | - | MOVING_END | C | - | C:e08 @ 6.05 |  |
| g49 | - | STOP_START | C | - | C:e09 @ 6.05 |  |

## Edges

```
    g01 --PRECEDES--> g04
    g02 --PRECEDES--> g04
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g11 --PRECEDES--> g14
    g11 --PRECEDES--> g15
    g11 --PRECEDES--> g16
    g11 --PRECEDES--> g17
    g11 --PRECEDES--> g18
    g11 --PRECEDES--> g19
    g11 --PRECEDES--> g20
    g11 --PRECEDES--> g21
    g12 --PRECEDES--> g22
    g12 --PRECEDES--> g23
    g12 --PRECEDES--> g24
    g13 --PRECEDES--> g22
    g13 --PRECEDES--> g23
    g13 --PRECEDES--> g24
    g14 --PRECEDES--> g22
    g14 --PRECEDES--> g23
    g14 --PRECEDES--> g24
    g15 --PRECEDES--> g22
    g15 --PRECEDES--> g23
    g15 --PRECEDES--> g24
    g16 --PRECEDES--> g22
    g16 --PRECEDES--> g23
    g16 --PRECEDES--> g24
    g17 --PRECEDES--> g22
    g17 --PRECEDES--> g23
    g17 --PRECEDES--> g24
    g18 --PRECEDES--> g22
    g18 --PRECEDES--> g23
    g18 --PRECEDES--> g24
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g22
    g21 --PRECEDES--> g23
    g21 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g23 --PRECEDES--> g25
    g24 --PRECEDES--> g25
    g25 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g28
    g27 --PRECEDES--> g29
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g30 --PRECEDES--> g32
    g30 --PRECEDES--> g33
    g31 --PRECEDES--> g32
    g31 --PRECEDES--> g33
    g32 --PRECEDES--> g34
    g33 --PRECEDES--> g34
    g34 --PRECEDES--> g35
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g36 --PRECEDES--> g38
    g36 --PRECEDES--> g39
    g36 --PRECEDES--> g40
    g37 --PRECEDES--> g38
    g37 --PRECEDES--> g39
    g37 --PRECEDES--> g40
    g13 --SAME_TRACK--> g17
    g14 --SAME_TRACK--> g18
    g15 --SAME_TRACK--> g19
    g16 --SAME_TRACK--> g20
    g13 --SAME_TRACK--> g21
    g14 --SAME_TRACK--> g26
    g15 --SAME_TRACK--> g27
    g16 --SAME_TRACK--> g32
    g13 --SAME_TRACK--> g33
    g28 --SAME_TRACK--> g35
    g13 --SAME_TRACK--> g36
    g13 --SAME_TRACK--> g38
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g05
    g03 --SAME_TRACK--> g06
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g10
    g03 --SAME_TRACK--> g22
    g03 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.15 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_FRONT(B,A) |
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
| +0.75 | COLLISION(A) |
| +0.80 | TRACK_LOST(A,A:track_005) |
| +0.85 | CRITICAL_TTC_END(A,A:track_001); TURN_LEFT_END(A) |
| +0.90 | CLOSING_END(A,A:track_001); MOVING_END(A); STOP_START(A) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (unidentified A:track_001): CRITICAL_TTC_START 5.15, COLLISION 5.15 (+0.00 s); EGO_PATH_ENTRY 5.70 after critical TTC (+0.55 s) [local times; t_global: critical_ttc_start +0.00, ego_path_entry +0.55, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 0.75, COLLISION 5.15 (+4.40 s) [local times; t_global: critical_ttc_start -4.40, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.15 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -5.15 | B | g02 MOVING_START(B) (B:e01)<br>g03 TRACK_APPEARED_FRONT(B,A) (B:e02) | ego: not yet observed |
| -4.45 | B | g04 CLOSING_START(B,A) (B:e03) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -4.40 | B | g05 CRITICAL_TTC_START(B,A) (B:e04) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -3.75 | B | g06 CRITICAL_TTC_END(B,A) (B:e05)<br>g07 CLOSING_END(B,A) (B:e06) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| -1.20 | A | g08 BRAKE_START(A) (A:e02) | ego: MOVING |
| -0.90 | B | g09 CLOSING_START(B,A) (B:e07) | ego: MOVING<br>track_001: IN_EGO_PATH |
| -0.70 | B | g10 CRITICAL_TTC_START(B,A) (B:e08) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH |
| -0.40 | B | g11 BRAKE_START(B) (B:e09) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.00 | A | g12 COLLISION(A,B) (A:e03)<br>g13 TRACK_APPEARED_LEFT(A,A:track_001) (A:e04)<br>g14 TRACK_APPEARED_RIGHT(A,A:track_002) (A:e05)<br>g15 TRACK_APPEARED_RIGHT(A,A:track_003) (A:e06)<br>g16 TRACK_APPEARED_RIGHT(A,A:track_004) (A:e07)<br>g17 CLOSING_START(A,A:track_001) (A:e08)<br>g18 CLOSING_START(A,A:track_002) (A:e09)<br>g19 CLOSING_START(A,A:track_003) (A:e10)<br>g20 CLOSING_START(A,A:track_004) (A:e11)<br>g21 CRITICAL_TTC_START(A,A:track_001) (A:e12) | ego: MOVING, BRAKE |
| +0.00 | B | g12 COLLISION(A,B) (B:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | B | g22 CRITICAL_TTC_END(B,A) (B:e11)<br>g23 CLOSING_END(B,A) (B:e12) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH |
| +0.05 | A | g24 BRAKE_END(A) (A:e13) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.25 | A | g25 TURN_LEFT_START(A) (A:e14) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.30 | A | g26 CLOSING_END(A,A:track_002) (A:e15)<br>g27 CLOSING_END(A,A:track_003) (A:e16) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING |
| +0.35 | A | g28 TRACK_APPEARED_RIGHT(A,A:track_005) (A:e17)<br>g29 TRACK_APPEARED_RIGHT(A,A:track_006) (A:e18) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING |
| +0.45 | B | g30 MOVING_END(B) (B:e13)<br>g31 STOP_START(B) (B:e14) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH |
| +0.55 | A | g32 CLOSING_END(A,A:track_004) (A:e19)<br>g33 EGO_PATH_ENTRY(A,A:track_001) (A:e20) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state<br>track_004: CLOSING<br>track_005: no active state<br>track_006: no active state |
| +0.75 | A | g34 COLLISION(A) (A:e21) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state |
| +0.80 | A | g35 TRACK_LOST(A,A:track_005) (A:e22) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state |
| +0.85 | A | g36 CRITICAL_TTC_END(A,A:track_001) (A:e23)<br>g37 TURN_LEFT_END(A) (A:e24) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 |
| +0.90 | A | g38 CLOSING_END(A,A:track_001) (A:e25)<br>g39 MOVING_END(A) (A:e26)<br>g40 STOP_START(A) (A:e27) | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_006: no active state<br>track lost, states UNKNOWN: track_005 |
| - | C | g41 MOVING_START(C) (C:e01) | ego: not yet observed |
| - | C | g42 MOVING_END(C) (C:e02)<br>g43 STOP_START(C) (C:e03) | ego: MOVING |
| - | C | g44 COLLISION(C) (C:e04)<br>g45 STOP_END(C) (C:e05)<br>g46 MOVING_START(C) (C:e06) | ego: STOP |
| - | C | g47 BRAKE_START(C) (C:e07) | ego: MOVING |
| - | C | g48 MOVING_END(C) (C:e08)<br>g49 STOP_START(C) (C:e09) | ego: MOVING, BRAKE |

## Plain-language reading

- 5.15 s before the matched collision, A started moving (already the case when first observed).
- 5.15 s before the matched collision, B started moving (already the case when first observed).
- 5.15 s before the matched collision, B's radar started tracking A, which appeared in front of it.
- 4.45 s before the matched collision, B observed A start closing in.
- 4.40 s before the matched collision, B's time-to-contact with A became critical.
- 3.75 s before the matched collision, B's time-to-contact with A stopped being critical.
- 3.75 s before the matched collision, B observed A stop closing in.
- 1.20 s before the matched collision, A started braking.
- 0.90 s before the matched collision, B observed A start closing in.
- 0.70 s before the matched collision, B's time-to-contact with A became critical.
- 0.40 s before the matched collision, B started braking.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 6074, B: 6074 N*s).
- At the matched collision, A's radar started tracking unidentified object A:track_001, which appeared on its left.
- At the matched collision, A's radar started tracking unidentified object A:track_002, which appeared on its right.
- At the matched collision, A's radar started tracking unidentified object A:track_003, which appeared on its right.
- At the matched collision, A's radar started tracking unidentified object A:track_004, which appeared on its right.
- At the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- At the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- At the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- At the matched collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- At the matched collision, A's time-to-contact with unidentified object A:track_001 became critical (already the case when first observed).
- 0.05 s after the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s after the matched collision, B observed A stop closing in.
- 0.05 s after the matched collision, A released the brake.
- 0.25 s after the matched collision, A started turning left.
- 0.30 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.30 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.35 s after the matched collision, A's radar started tracking unidentified object A:track_005, which appeared on its right.
- 0.35 s after the matched collision, A's radar started tracking unidentified object A:track_006, which appeared on its right.
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.55 s after the matched collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_001 enter its forward path corridor.
- 0.75 s after the matched collision, A's collision sensor recorded a contact (peak impulse 2696 N*s).
- 0.80 s after the matched collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 0.85 s after the matched collision, A's time-to-contact with unidentified object A:track_001 stopped being critical.
- 0.85 s after the matched collision, A stopped turning left.
- 0.90 s after the matched collision, A observed unidentified object A:track_001 stop closing in.
- 0.90 s after the matched collision, A stopped moving.
- 0.90 s after the matched collision, A came to a stop.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.30 s) C stopped moving.
- (unaligned, C local time 0.30 s) C came to a stop.
- (unaligned, C local time 5.90 s) C's collision sensor recorded a contact (peak impulse 2696 N*s).
- (unaligned, C local time 5.90 s) C left its stop.
- (unaligned, C local time 5.90 s) C started moving.
- (unaligned, C local time 5.95 s) C started braking.
- (unaligned, C local time 6.05 s) C stopped moving.
- (unaligned, C local time 6.05 s) C came to a stop.
