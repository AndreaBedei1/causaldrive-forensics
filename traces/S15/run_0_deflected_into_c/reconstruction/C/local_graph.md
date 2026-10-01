# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 142.30000706017017 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 23 (PRECEDES 16, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED_LEFT | C | track_001 | radar |  |
| C:e03 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 0.05 | TRACK_APPEARED_FRONT | C | track_002 | radar |  |
| C:e05 | 0.05 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.90 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e07 | 4.45 | TRACK_LOST | C | track_001 | radar |  |
| C:e08 | 4.75 | COLLISION | C | - | collision_sensor | peak_impulse=1637.56 |
| C:e09 | 4.80 | BRAKE_START | C | - | controls |  |
| C:e10 | 4.95 | EGO_PATH_ENTRY | C | track_002 | radar |  |
| C:e11 | 5.00 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e12 | 5.05 | CLOSING_END | C | track_002 | radar |  |
| C:e13 | 5.05 | MOVING_END | C | - | ego |  |
| C:e14 | 5.05 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e04
    C:e01 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e11 --PRECEDES--> C:e14
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e04 --SAME_TRACK--> C:e06
    C:e02 --SAME_TRACK--> C:e07
    C:e04 --SAME_TRACK--> C:e10
    C:e04 --SAME_TRACK--> C:e11
    C:e04 --SAME_TRACK--> C:e12
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED_LEFT track_001<br>C:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 0.05 | C:e04 TRACK_APPEARED_FRONT track_002<br>C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 0.00 |
| 2.90 | C:e06 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.80 |
| 4.45 | C:e07 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 4.40 |
| 4.75 | C:e08 COLLISION | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 | 4.70 |
| 4.80 | C:e09 BRAKE_START | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 | 4.70 |
| 4.95 | C:e10 EGO_PATH_ENTRY track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_001 | 4.90 |
| 5.00 | C:e11 CRITICAL_TTC_END track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 4.90 |
| 5.05 | C:e12 CLOSING_END track_002<br>C:e13 MOVING_END<br>C:e14 STOP_START | ego: MOVING, BRAKE<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 5.00 |

## States still active when observation ended

- CLOSING of track_001, since C:e03 (t = 0.00 s); the track was lost at 4.45 s
- BRAKE, since C:e09 (t = 4.80 s)
- EGO_PATH of track_002, since C:e10 (t = 4.95 s)
- STOP, since C:e14 (t = 5.05 s)

## Tracks lost

- track_001 at 4.45 s (C:e07): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 2.90, COLLISION 4.75 (+1.85 s); EGO_PATH_ENTRY 4.95 after critical TTC (+2.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 4.45 | 84 | 45.3 m / -57 deg | 7.64 m (4.45) | 7.6 m / -54 deg | 9.6 m/s |
| track_002 | 0.05 | 13.95 | 271 | 69.9 m / -3 deg | 1.32 m (5.30) | 1.6 m / -67 deg | 10.8 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.05 s: C's radar started tracking track_002, which appeared in front of it.
- t = 0.05 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.90 s: C's time-to-contact with track_002 became critical.
- t = 4.45 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.75 s: C's collision sensor recorded a contact (peak impulse 1638 N*s).
- t = 4.80 s: C started braking.
- t = 4.95 s: C observed track_002 enter its forward path corridor.
- t = 5.00 s: C's time-to-contact with track_002 stopped being critical.
- t = 5.05 s: C observed track_002 stop closing in.
- t = 5.05 s: C stopped moving.
- t = 5.05 s: C came to a stop.
