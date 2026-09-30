# Global graph - S10/run_0_stops_safely

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |

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
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 1.90 | relevant_to_ego_path=False |
| g03 | - | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.15 |  |
| g04 | - | BRAKE_START | A | - | A:e04 @ 2.55 |  |
| g05 | - | HARD_BRAKE_START | A | - | A:e05 @ 2.55 |  |
| g06 | - | MOVING_END | A | - | A:e06 @ 3.35 |  |
| g07 | - | STOP_START | A | - | A:e07 @ 3.35 |  |
| g08 | - | TRACK_APPEARED | A | A:track_001 | A:e08 @ 3.70 |  |
| g09 | - | CLOSING_START | A | A:track_001 | A:e09 @ 3.70 | active_at_first_observation=True |
| g10 | - | CRITICAL_TTC_START | A | A:track_001 | A:e10 @ 4.25 |  |
| g11 | - | EGO_PATH_ENTRY | A | A:track_001 | A:e11 @ 5.80 |  |
| g12 | - | CRITICAL_TTC_END | A | A:track_001 | A:e12 @ 5.95 |  |
| g13 | - | CLOSING_END | A | A:track_001 | A:e13 @ 6.10 |  |
| g14 | - | EGO_PATH_EXIT | A | A:track_001 | A:e14 @ 6.25 |  |
| g15 | - | TRACK_LOST | A | A:track_001 | A:e15 @ 7.00 |  |
| g16 | - | STRONG_THROTTLE_START | A | - | A:e16 @ 9.55 |  |
| g17 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g18 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g19 | - | STRONG_THROTTLE_END | B | - | B:e03 @ 1.80 |  |
| g20 | - | TRACK_APPEARED | B | B:track_001 | B:e04 @ 2.55 |  |
| g21 | - | CLOSING_START | B | B:track_001 | B:e05 @ 2.55 | active_at_first_observation=True |
| g22 | - | CRITICAL_TTC_START | B | B:track_001 | B:e06 @ 4.30 |  |
| g23 | - | TRACK_LOST | B | B:track_001 | B:e07 @ 5.50 |  |
| g24 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e08 @ 7.55 | relevant_to_ego_path=False |
| g25 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e09 @ 7.75 |  |

## Edges

```
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g10
    g08 --SAME_TRACK--> g11
    g08 --SAME_TRACK--> g12
    g08 --SAME_TRACK--> g13
    g08 --SAME_TRACK--> g14
    g08 --SAME_TRACK--> g15
    g20 --SAME_TRACK--> g21
    g20 --SAME_TRACK--> g22
    g20 --SAME_TRACK--> g23
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 1.90 s) A's camera established a STOP sign detection (unidentified object A:sign-0) (the detector judged it not relevant to its path).
- (unaligned, A local time 2.15 s) A's camera stopped detecting STOP sign unidentified object A:sign-0.
- (unaligned, A local time 2.55 s) A started braking.
- (unaligned, A local time 2.55 s) A started braking hard.
- (unaligned, A local time 3.35 s) A stopped moving.
- (unaligned, A local time 3.35 s) A came to a stop.
- (unaligned, A local time 3.70 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 3.70 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 4.25 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 5.80 s) A observed unidentified object A:track_001 enter its forward path corridor.
- (unaligned, A local time 5.95 s) A's time-to-contact with unidentified object A:track_001 stopped being critical.
- (unaligned, A local time 6.10 s) A observed unidentified object A:track_001 stop closing in.
- (unaligned, A local time 6.25 s) A observed unidentified object A:track_001 leave its forward path corridor.
- (unaligned, A local time 7.00 s) A's radar lost unidentified object A:track_001.
- (unaligned, A local time 9.55 s) A started applying strong throttle.
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 2.55 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 2.55 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 4.30 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 5.50 s) B's radar lost unidentified object B:track_001.
- (unaligned, B local time 7.55 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 7.75 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
