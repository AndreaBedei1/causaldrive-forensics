# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 207.26394240558147 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 23 (PRECEDES 17, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED_REAR | C | track_001 | radar |  |
| C:e03 | 0.00 | TRACK_APPEARED_REAR | C | track_002 | radar |  |
| C:e04 | 0.80 | CLOSING_START | C | track_001 | radar |  |
| C:e05 | 1.05 | CLOSING_START | C | track_002 | radar |  |
| C:e06 | 2.00 | CLOSING_END | C | track_001 | radar |  |
| C:e07 | 2.10 | CLOSING_END | C | track_002 | radar |  |
| C:e08 | 2.40 | SPEED_LIMIT_EXCEEDED_START | C | - | ego |  |
| C:e09 | 2.50 | TRACK_LOST | C | track_001 | radar |  |
| C:e10 | 2.85 | TRACK_LOST | C | track_002 | radar |  |
| C:e11 | 2.95 | BRAKE_START | C | - | controls |  |
| C:e12 | 3.10 | SPEED_LIMIT_EXCEEDED_END | C | - | ego |  |
| C:e13 | 4.05 | MOVING_END | C | - | ego |  |
| C:e14 | 4.05 | STOP_START | C | - | ego |  |
| C:e15 | 12.95 | BRAKE_END | C | - | controls |  |
| C:e16 | 13.75 | STOP_END | C | - | ego |  |
| C:e17 | 13.75 | MOVING_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e04
    C:e04 --PRECEDES--> C:e05
    C:e05 --PRECEDES--> C:e06
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e09 --PRECEDES--> C:e10
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e12 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e15
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e15 --PRECEDES--> C:e17
    C:e02 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e02 --SAME_TRACK--> C:e06
    C:e03 --SAME_TRACK--> C:e07
    C:e02 --SAME_TRACK--> C:e09
    C:e03 --SAME_TRACK--> C:e10
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED_REAR track_001<br>C:e03 TRACK_APPEARED_REAR track_002 | ego: not yet observed | - |
| 0.80 | C:e04 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 0.70 |
| 1.05 | C:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING<br>track_002: no active state | 1.00 |
| 2.00 | C:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 1.90 |
| 2.10 | C:e07 CLOSING_END track_002 | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING | 2.00 |
| 2.40 | C:e08 SPEED_LIMIT_EXCEEDED_START | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 2.30 |
| 2.50 | C:e09 TRACK_LOST track_001 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_001: no active state<br>track_002: no active state | 2.40 |
| 2.85 | C:e10 TRACK_LOST track_002 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: no active state<br>track lost, states UNKNOWN: track_001 | 2.80 |
| 2.95 | C:e11 BRAKE_START | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001, track_002 | 2.90 |
| 3.10 | C:e12 SPEED_LIMIT_EXCEEDED_END | ego: MOVING, BRAKE, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001, track_002 | 3.00 |
| 4.05 | C:e13 MOVING_END<br>C:e14 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 | 4.00 |
| 12.95 | C:e15 BRAKE_END | ego: STOP, BRAKE<br>track lost, states UNKNOWN: track_001, track_002 | 12.90 |
| 13.75 | C:e16 STOP_END<br>C:e17 MOVING_START | ego: STOP<br>track lost, states UNKNOWN: track_001, track_002 | 13.70 |

## States still active when observation ended

- MOVING, since C:e17 (t = 13.75 s)

## Tracks lost

- lost with no state active: track_001, track_002

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- none

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 2.50 | 40 | 48.6 m / +180 deg | 44.36 m (2.00) | 44.7 m / -180 deg | 13.4 m/s |
| track_002 | 0.00 | 2.85 | 46 | 25.1 m / -180 deg | 23.63 m (2.15) | 23.8 m / +180 deg | 13.9 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared behind it.
- t = 0.00 s: C's radar started tracking track_002, which appeared behind it.
- t = 0.80 s: C observed track_001 start closing in.
- t = 1.05 s: C observed track_002 start closing in.
- t = 2.00 s: C observed track_001 stop closing in.
- t = 2.10 s: C observed track_002 stop closing in.
- t = 2.40 s: C began exceeding the speed limit.
- t = 2.50 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.85 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 2.95 s: C started braking.
- t = 3.10 s: C returned within the speed limit.
- t = 4.05 s: C stopped moving.
- t = 4.05 s: C came to a stop.
- t = 12.95 s: C released the brake.
- t = 13.75 s: C left its stop.
- t = 13.75 s: C started moving.
