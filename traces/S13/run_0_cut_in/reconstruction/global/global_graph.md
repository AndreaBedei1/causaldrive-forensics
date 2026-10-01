# Global graph - S13/run_0_cut_in

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: - |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| B:track_001 | anonymous_track | seen only by B; candidate: A |
| B:track_002 | anonymous_track | seen only by B; candidate: A |
| B:track_003 | anonymous_track | seen only by B; candidate: A |
| B:track_004 | anonymous_track | seen only by B; candidate: A |
| B:track_005 | anonymous_track | seen only by B; candidate: A |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e08 | 5.25 | -5.25 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.25 | -5.25 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 3184.37 vs 3184.37 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.98 | A and B both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 5.25 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 5.6 m -> 1.3 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.33 m/s over 3.0 s<br>range at the contact 1.28 m<br>the only track of A compatible with the contact |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 3184.37 vs 3184.37 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.70 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with A's own speed before the collision |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -5.25 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -5.25 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -5.25 | TRACK_APPEARED_LEFT | A | B | A:e02 @ 0.00 |  |
| g04 | -5.25 | CLOSING_START | A | B | A:e03 @ 0.00 | active_at_first_observation=True |
| g05 | -4.45 | BRAKE_START | B | - | B:e02 @ 0.80 |  |
| g06 | -2.40 | BRAKE_START | A | - | A:e04 @ 2.85 |  |
| g07 | -1.70 | CUT_IN_FROM_LEFT_START | A | B | A:e05 @ 3.55 |  |
| g08 | -1.30 | CRITICAL_TTC_START | A | B | A:e06 @ 3.95 |  |
| g09 | -0.35 | EGO_PATH_ENTRY | A | B | A:e07 @ 4.90 |  |
| g10 | 0.00 | COLLISION | - | A, B | A:e08 @ 5.25, B:e03 @ 5.25 | matched_event=collision_001; reference_event=True; peak_impulse=A 3184.37, B 3184.37 |
| g11 | 0.05 | CRITICAL_TTC_END | A | B | A:e09 @ 5.30 |  |
| g12 | 0.05 | CLOSING_END | A | B | A:e10 @ 5.30 |  |
| g13 | 0.20 | TURN_RIGHT_START | B | - | B:e04 @ 5.45 |  |
| g14 | 0.70 | TRACK_APPEARED_RIGHT | B | B:track_001 | B:e05 @ 5.95 |  |
| g15 | 0.70 | TRACK_APPEARED_RIGHT | B | B:track_002 | B:e06 @ 5.95 |  |
| g16 | 0.70 | TRACK_APPEARED_RIGHT | B | B:track_003 | B:e07 @ 5.95 |  |
| g17 | 0.70 | TRACK_APPEARED_RIGHT | B | B:track_004 | B:e08 @ 5.95 |  |
| g18 | 0.70 | TRACK_APPEARED_RIGHT | B | B:track_005 | B:e09 @ 5.95 |  |
| g19 | 0.70 | CLOSING_START | B | B:track_001 | B:e10 @ 5.95 | active_at_first_observation=True |
| g20 | 0.70 | CLOSING_START | B | B:track_002 | B:e11 @ 5.95 | active_at_first_observation=True |
| g21 | 0.70 | CLOSING_START | B | B:track_003 | B:e12 @ 5.95 | active_at_first_observation=True |
| g22 | 0.70 | CLOSING_START | B | B:track_004 | B:e13 @ 5.95 | active_at_first_observation=True |
| g23 | 0.70 | CLOSING_START | B | B:track_005 | B:e14 @ 5.95 | active_at_first_observation=True |
| g24 | 1.15 | CLOSING_END | B | B:track_001 | B:e15 @ 6.40 |  |
| g25 | 1.15 | CLOSING_END | B | B:track_002 | B:e16 @ 6.40 |  |
| g26 | 1.15 | CLOSING_END | B | B:track_003 | B:e17 @ 6.40 |  |
| g27 | 1.15 | CLOSING_END | B | B:track_004 | B:e18 @ 6.40 |  |
| g28 | 1.15 | CLOSING_END | B | B:track_005 | B:e19 @ 6.40 |  |
| g29 | 1.15 | TURN_RIGHT_END | B | - | B:e20 @ 6.40 |  |
| g30 | 1.15 | MOVING_END | A | - | A:e11 @ 6.40 |  |
| g31 | 1.15 | STOP_START | A | - | A:e12 @ 6.40 |  |
| g32 | 1.20 | MOVING_END | B | - | B:e21 @ 6.45 |  |
| g33 | 1.20 | STOP_START | B | - | B:e22 @ 6.45 |  |
| g34 | 1.40 | CUT_IN_FROM_LEFT_END | A | B | A:e13 @ 6.65 |  |

## Edges

```
    g01 --PRECEDES--> g05
    g02 --PRECEDES--> g05
    g03 --PRECEDES--> g05
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g06 --PRECEDES--> g07
    g07 --PRECEDES--> g08
    g08 --PRECEDES--> g09
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g10 --PRECEDES--> g12
    g11 --PRECEDES--> g13
    g12 --PRECEDES--> g13
    g13 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g13 --PRECEDES--> g19
    g13 --PRECEDES--> g20
    g13 --PRECEDES--> g21
    g13 --PRECEDES--> g22
    g13 --PRECEDES--> g23
    g14 --PRECEDES--> g24
    g14 --PRECEDES--> g25
    g14 --PRECEDES--> g26
    g14 --PRECEDES--> g27
    g14 --PRECEDES--> g28
    g14 --PRECEDES--> g29
    g14 --PRECEDES--> g30
    g14 --PRECEDES--> g31
    g15 --PRECEDES--> g24
    g15 --PRECEDES--> g25
    g15 --PRECEDES--> g26
    g15 --PRECEDES--> g27
    g15 --PRECEDES--> g28
    g15 --PRECEDES--> g29
    g15 --PRECEDES--> g30
    g15 --PRECEDES--> g31
    g16 --PRECEDES--> g24
    g16 --PRECEDES--> g25
    g16 --PRECEDES--> g26
    g16 --PRECEDES--> g27
    g16 --PRECEDES--> g28
    g16 --PRECEDES--> g29
    g16 --PRECEDES--> g30
    g16 --PRECEDES--> g31
    g17 --PRECEDES--> g24
    g17 --PRECEDES--> g25
    g17 --PRECEDES--> g26
    g17 --PRECEDES--> g27
    g17 --PRECEDES--> g28
    g17 --PRECEDES--> g29
    g17 --PRECEDES--> g30
    g17 --PRECEDES--> g31
    g18 --PRECEDES--> g24
    g18 --PRECEDES--> g25
    g18 --PRECEDES--> g26
    g18 --PRECEDES--> g27
    g18 --PRECEDES--> g28
    g18 --PRECEDES--> g29
    g18 --PRECEDES--> g30
    g18 --PRECEDES--> g31
    g19 --PRECEDES--> g24
    g19 --PRECEDES--> g25
    g19 --PRECEDES--> g26
    g19 --PRECEDES--> g27
    g19 --PRECEDES--> g28
    g19 --PRECEDES--> g29
    g19 --PRECEDES--> g30
    g19 --PRECEDES--> g31
    g20 --PRECEDES--> g24
    g20 --PRECEDES--> g25
    g20 --PRECEDES--> g26
    g20 --PRECEDES--> g27
    g20 --PRECEDES--> g28
    g20 --PRECEDES--> g29
    g20 --PRECEDES--> g30
    g20 --PRECEDES--> g31
    g21 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g21 --PRECEDES--> g27
    g21 --PRECEDES--> g28
    g21 --PRECEDES--> g29
    g21 --PRECEDES--> g30
    g21 --PRECEDES--> g31
    g22 --PRECEDES--> g24
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g22 --PRECEDES--> g27
    g22 --PRECEDES--> g28
    g22 --PRECEDES--> g29
    g22 --PRECEDES--> g30
    g22 --PRECEDES--> g31
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
    g03 --SAME_TRACK--> g04
    g03 --SAME_TRACK--> g07
    g03 --SAME_TRACK--> g08
    g03 --SAME_TRACK--> g09
    g03 --SAME_TRACK--> g11
    g03 --SAME_TRACK--> g12
    g03 --SAME_TRACK--> g34
    g14 --SAME_TRACK--> g19
    g15 --SAME_TRACK--> g20
    g16 --SAME_TRACK--> g21
    g17 --SAME_TRACK--> g22
    g18 --SAME_TRACK--> g23
    g14 --SAME_TRACK--> g24
    g15 --SAME_TRACK--> g25
    g16 --SAME_TRACK--> g26
    g17 --SAME_TRACK--> g27
    g18 --SAME_TRACK--> g28
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -5.25 | MOVING_START(A); MOVING_START(B); TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -4.45 | BRAKE_START(B) |
| -2.40 | BRAKE_START(A) |
| -1.70 | CUT_IN_FROM_LEFT_START(A,B) |
| -1.30 | CRITICAL_TTC_START(A,B) |
| -0.35 | EGO_PATH_ENTRY(A,B) |
| +0.00 | COLLISION(A,B) |
| +0.05 | CRITICAL_TTC_END(A,B); CLOSING_END(A,B) |
| +0.20 | TURN_RIGHT_START(B) |
| +0.70 | TRACK_APPEARED_RIGHT(B,B:track_001); TRACK_APPEARED_RIGHT(B,B:track_002); TRACK_APPEARED_RIGHT(B,B:track_003); TRACK_APPEARED_RIGHT(B,B:track_004); TRACK_APPEARED_RIGHT(B,B:track_005); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004); CLOSING_START(B,B:track_005) |
| +1.15 | CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_002); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); TURN_RIGHT_END(B); MOVING_END(A); STOP_START(A) |
| +1.20 | MOVING_END(B); STOP_START(B) |
| +1.40 | CUT_IN_FROM_LEFT_END(A,B) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 3.55 < CRITICAL_TTC_START 3.95 (+0.40 s) < COLLISION 5.25 (+1.30 s); EGO_PATH_ENTRY 4.90 after critical TTC (+0.95 s) [local times; t_global: cut_in -1.70, critical_ttc_start -1.30, ego_path_entry -0.35, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -5.25 | A | g01 MOVING_START(A) (A:e01)<br>g03 TRACK_APPEARED_LEFT(A,B) (A:e02)<br>g04 CLOSING_START(A,B) (A:e03) | ego: not yet observed |
| -5.25 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -4.45 | B | g05 BRAKE_START(B) (B:e02) | ego: MOVING |
| -2.40 | A | g06 BRAKE_START(A) (A:e04) | ego: MOVING<br>track_001: CLOSING |
| -1.70 | A | g07 CUT_IN_FROM_LEFT_START(A,B) (A:e05) | ego: MOVING, BRAKE<br>track_001: CLOSING |
| -1.30 | A | g08 CRITICAL_TTC_START(A,B) (A:e06) | ego: MOVING, BRAKE<br>track_001: CLOSING, CUT_IN_FROM_LEFT |
| -0.35 | A | g09 EGO_PATH_ENTRY(A,B) (A:e07) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT |
| +0.00 | A | g10 COLLISION(A,B) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.00 | B | g10 COLLISION(A,B) (B:e03) | ego: MOVING, BRAKE |
| +0.05 | A | g11 CRITICAL_TTC_END(A,B) (A:e09)<br>g12 CLOSING_END(A,B) (A:e10) | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +0.20 | B | g13 TURN_RIGHT_START(B) (B:e04) | ego: MOVING, BRAKE |
| +0.70 | B | g14 TRACK_APPEARED_RIGHT(B,B:track_001) (B:e05)<br>g15 TRACK_APPEARED_RIGHT(B,B:track_002) (B:e06)<br>g16 TRACK_APPEARED_RIGHT(B,B:track_003) (B:e07)<br>g17 TRACK_APPEARED_RIGHT(B,B:track_004) (B:e08)<br>g18 TRACK_APPEARED_RIGHT(B,B:track_005) (B:e09)<br>g19 CLOSING_START(B,B:track_001) (B:e10)<br>g20 CLOSING_START(B,B:track_002) (B:e11)<br>g21 CLOSING_START(B,B:track_003) (B:e12)<br>g22 CLOSING_START(B,B:track_004) (B:e13)<br>g23 CLOSING_START(B,B:track_005) (B:e14) | ego: MOVING, BRAKE, TURN_RIGHT |
| +1.15 | B | g24 CLOSING_END(B,B:track_001) (B:e15)<br>g25 CLOSING_END(B,B:track_002) (B:e16)<br>g26 CLOSING_END(B,B:track_003) (B:e17)<br>g27 CLOSING_END(B,B:track_004) (B:e18)<br>g28 CLOSING_END(B,B:track_005) (B:e19)<br>g29 TURN_RIGHT_END(B) (B:e20) | ego: MOVING, BRAKE, TURN_RIGHT<br>track_001: CLOSING<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING |
| +1.15 | A | g30 MOVING_END(A) (A:e11)<br>g31 STOP_START(A) (A:e12) | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |
| +1.20 | B | g32 MOVING_END(B) (B:e21)<br>g33 STOP_START(B) (B:e22) | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state |
| +1.40 | A | g34 CUT_IN_FROM_LEFT_END(A,B) (A:e13) | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT |

## Plain-language reading

- 5.25 s before the matched collision, A started moving (already the case when first observed).
- 5.25 s before the matched collision, B started moving (already the case when first observed).
- 5.25 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 5.25 s before the matched collision, A observed B start closing in (already the case when first observed).
- 4.45 s before the matched collision, B started braking.
- 2.40 s before the matched collision, A started braking.
- 1.70 s before the matched collision, A observed B cutting in from the left.
- 1.30 s before the matched collision, A's time-to-contact with B became critical.
- 0.35 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 3184, B: 3184 N*s).
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A observed B stop closing in.
- 0.20 s after the matched collision, B started turning right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_001, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_002, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_003, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_004, which appeared on its right.
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_005, which appeared on its right.
- 0.70 s after the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 1.15 s after the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_002 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 1.15 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 1.15 s after the matched collision, B stopped turning right.
- 1.15 s after the matched collision, A stopped moving.
- 1.15 s after the matched collision, A came to a stop.
- 1.20 s after the matched collision, B stopped moving.
- 1.20 s after the matched collision, B came to a stop.
- 1.40 s after the matched collision, A observed B's cut-in from the left settle.
