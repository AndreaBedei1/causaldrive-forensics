# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 188.80934267118573 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 31 (PRECEDES 21, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.00 | TRACK_APPEARED_FRONT | B | track_001 | radar |  |
| B:e03 | 0.00 | TRACK_APPEARED_REAR | B | track_002 | radar |  |
| B:e04 | 0.50 | CLOSING_START | B | track_002 | radar |  |
| B:e05 | 1.10 | CLOSING_START | B | track_001 | radar |  |
| B:e06 | 1.65 | CLOSING_END | B | track_002 | radar |  |
| B:e07 | 2.10 | CLOSING_END | B | track_001 | radar |  |
| B:e08 | 3.20 | CLOSING_START | B | track_001 | radar |  |
| B:e09 | 3.75 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e10 | 4.60 | COLLISION | B | - | collision_sensor | peak_impulse=21812.15 |
| B:e11 | 4.60 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e12 | 4.60 | CLOSING_END | B | track_001 | radar |  |
| B:e13 | 4.60 | CLOSING_START | B | track_002 | radar |  |
| B:e14 | 4.65 | BRAKE_START | B | - | controls |  |
| B:e15 | 4.75 | MOVING_END | B | - | ego |  |
| B:e16 | 4.75 | STOP_START | B | - | ego |  |
| B:e17 | 5.95 | TRACK_LOST | B | track_002 | radar |  |
| B:e18 | 6.00 | COLLISION | B | - | collision_sensor | peak_impulse=31488.29 |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e04
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e03 --SAME_TRACK--> B:e04
    B:e02 --SAME_TRACK--> B:e05
    B:e03 --SAME_TRACK--> B:e06
    B:e02 --SAME_TRACK--> B:e07
    B:e02 --SAME_TRACK--> B:e08
    B:e02 --SAME_TRACK--> B:e09
    B:e02 --SAME_TRACK--> B:e11
    B:e02 --SAME_TRACK--> B:e12
    B:e03 --SAME_TRACK--> B:e13
    B:e03 --SAME_TRACK--> B:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START<br>B:e02 TRACK_APPEARED_FRONT track_001<br>B:e03 TRACK_APPEARED_REAR track_002 | ego: not yet observed | - |
| 0.50 | B:e04 CLOSING_START track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state | 0.40 |
| 1.10 | B:e05 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING | 1.00 |
| 1.65 | B:e06 CLOSING_END track_002 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING | 1.60 |
| 2.10 | B:e07 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state | 2.00 |
| 3.20 | B:e08 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: no active state | 3.10 |
| 3.75 | B:e09 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state | 3.70 |
| 4.60 | B:e10 COLLISION<br>B:e11 CRITICAL_TTC_END track_001<br>B:e12 CLOSING_END track_001<br>B:e13 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state | 4.50 |
| 4.65 | B:e14 BRAKE_START | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING | 4.60 |
| 4.75 | B:e15 MOVING_END<br>B:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING | 4.70 |
| 5.95 | B:e17 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING | 5.90 |
| 6.00 | B:e18 COLLISION | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 5.90 |

## States still active when observation ended

- CLOSING of track_002, since B:e13 (t = 4.60 s); the track was lost at 5.95 s
- BRAKE, since B:e14 (t = 4.65 s)
- STOP, since B:e16 (t = 4.75 s)

## Tracks lost

- track_002 at 5.95 s (B:e17): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 4.60 (+0.85 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.15 | 284 | 16.3 m / -0 deg | 2.46 m (4.60) | 2.7 m / +0 deg | 14.3 m/s |
| track_002 | 0.00 | 5.95 | 116 | 24.2 m / +180 deg | 3.24 m (5.95) | 3.2 m / -179 deg | 13.7 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.00 s: B's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: B's radar started tracking track_002, which appeared behind it.
- t = 0.50 s: B observed track_002 start closing in.
- t = 1.10 s: B observed track_001 start closing in.
- t = 1.65 s: B observed track_002 stop closing in.
- t = 2.10 s: B observed track_001 stop closing in.
- t = 3.20 s: B observed track_001 start closing in.
- t = 3.75 s: B's time-to-contact with track_001 became critical.
- t = 4.60 s: B's collision sensor recorded a contact (peak impulse 21812 N*s).
- t = 4.60 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.60 s: B observed track_001 stop closing in.
- t = 4.60 s: B observed track_002 start closing in.
- t = 4.65 s: B started braking.
- t = 4.75 s: B stopped moving.
- t = 4.75 s: B came to a stop.
- t = 5.95 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.00 s: B's collision sensor recorded a contact (peak impulse 31488 N*s).
