# Global graph - S04/run_0_yield

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 2.10 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 2.10 | active_at_first_observation=True |
| g04 | - | CRITICAL_TTC_START | A | A:track_001 | A:e04 @ 3.00 |  |
| g05 | - | TRACK_LOST | A | A:track_001 | A:e05 @ 4.95 |  |
| g06 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e06 @ 8.15 | relevant_to_ego_path=False |
| g07 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e07 @ 8.45 |  |
| g08 | - | TRACK_APPEARED | A | A:track_002 | A:e08 @ 9.70 |  |
| g09 | - | CLOSING_START | A | A:track_002 | A:e09 @ 9.70 | active_at_first_observation=True |
| g10 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g11 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.25 |  |
| g12 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.85 |  |
| g13 | - | TRACK_APPEARED | B | B:track_001 | B:e04 @ 2.00 |  |
| g14 | - | CLOSING_START | B | B:track_001 | B:e05 @ 2.00 | active_at_first_observation=True |
| g15 | - | TRACK_LOST | B | B:track_001 | B:e06 @ 2.35 |  |
| g16 | - | BRAKE_START | B | - | B:e07 @ 3.15 |  |
| g17 | - | HARD_BRAKE_START | B | - | B:e08 @ 3.15 |  |
| g18 | - | MOVING_END | B | - | B:e09 @ 3.90 |  |
| g19 | - | STOP_START | B | - | B:e10 @ 3.90 |  |
| g20 | - | TRACK_APPEARED | B | B:track_002 | B:e11 @ 4.35 |  |
| g21 | - | CLOSING_START | B | B:track_002 | B:e12 @ 4.35 | active_at_first_observation=True |
| g22 | - | CRITICAL_TTC_START | B | B:track_002 | B:e13 @ 4.35 | active_at_first_observation=True |
| g23 | - | EGO_PATH_ENTRY | B | B:track_002 | B:e14 @ 5.40 |  |
| g24 | - | CRITICAL_TTC_END | B | B:track_002 | B:e15 @ 5.45 |  |
| g25 | - | CLOSING_END | B | B:track_002 | B:e16 @ 5.55 |  |
| g26 | - | EGO_PATH_EXIT | B | B:track_002 | B:e17 @ 5.90 |  |
| g27 | - | TRACK_LOST | B | B:track_002 | B:e18 @ 6.90 |  |
| g28 | - | HARD_BRAKE_END | B | - | B:e19 @ 7.15 |  |
| g29 | - | BRAKE_END | B | - | B:e20 @ 7.15 |  |
| g30 | - | STRONG_THROTTLE_START | B | - | B:e21 @ 7.15 |  |
| g31 | - | STOP_END | B | - | B:e22 @ 7.55 |  |
| g32 | - | MOVING_START | B | - | B:e23 @ 7.55 |  |
| g33 | - | STRONG_THROTTLE_END | B | - | B:e24 @ 8.55 |  |
| g34 | - | BRAKE_START | B | - | B:e25 @ 8.75 |  |
| g35 | - | BRAKE_END | B | - | B:e26 @ 9.00 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g02 --SAME_TRACK--> g04
    g02 --SAME_TRACK--> g05
    g08 --SAME_TRACK--> g09
    g13 --SAME_TRACK--> g14
    g13 --SAME_TRACK--> g15
    g20 --SAME_TRACK--> g21
    g20 --SAME_TRACK--> g22
    g20 --SAME_TRACK--> g23
    g20 --SAME_TRACK--> g24
    g20 --SAME_TRACK--> g25
    g20 --SAME_TRACK--> g26
    g20 --SAME_TRACK--> g27
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 2.10 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 2.10 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 3.00 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 4.95 s) A's radar lost unidentified object A:track_001.
- (unaligned, A local time 8.15 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 8.45 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 9.70 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 9.70 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.25 s) B started applying strong throttle.
- (unaligned, B local time 1.85 s) B stopped applying strong throttle.
- (unaligned, B local time 2.00 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 2.00 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 2.35 s) B's radar lost unidentified object B:track_001.
- (unaligned, B local time 3.15 s) B started braking.
- (unaligned, B local time 3.15 s) B started braking hard.
- (unaligned, B local time 3.90 s) B stopped moving.
- (unaligned, B local time 3.90 s) B came to a stop.
- (unaligned, B local time 4.35 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 4.35 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 4.35 s) B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- (unaligned, B local time 5.40 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 5.45 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 5.55 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 5.90 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 6.90 s) B's radar lost unidentified object B:track_002.
- (unaligned, B local time 7.15 s) B stopped braking hard.
- (unaligned, B local time 7.15 s) B released the brake.
- (unaligned, B local time 7.15 s) B started applying strong throttle.
- (unaligned, B local time 7.55 s) B left its stop.
- (unaligned, B local time 7.55 s) B started moving.
- (unaligned, B local time 8.55 s) B stopped applying strong throttle.
- (unaligned, B local time 8.75 s) B started braking.
- (unaligned, B local time 9.00 s) B released the brake.
