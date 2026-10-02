# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 204.24685563519597 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 31 (PRECEDES 25, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | THROTTLE_START | C | - | controls | active_at_first_observation=True |
| C:e03 | 0.00 | TRACK_APPEARED_FRONT | C | track_001 | radar |  |
| C:e04 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.20 | TRACK_APPEARED_LEFT | C | track_002 | radar |  |
| C:e06 | 0.20 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e07 | 3.75 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e08 | 4.70 | COLLISION | C | - | collision_sensor | peak_impulse=1880.32 |
| C:e09 | 4.70 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e10 | 4.70 | CLOSING_END | C | track_001 | radar |  |
| C:e11 | 4.75 | THROTTLE_END | C | - | controls |  |
| C:e12 | 4.75 | BRAKE_START | C | - | controls |  |
| C:e13 | 5.00 | CLOSING_END | C | track_002 | radar |  |
| C:e14 | 5.00 | MOVING_END | C | - | ego |  |
| C:e15 | 5.00 | STOP_START | C | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e05
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e07 --PRECEDES--> C:e10
    C:e08 --PRECEDES--> C:e11
    C:e08 --PRECEDES--> C:e12
    C:e09 --PRECEDES--> C:e11
    C:e09 --PRECEDES--> C:e12
    C:e10 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e11 --PRECEDES--> C:e14
    C:e11 --PRECEDES--> C:e15
    C:e12 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e12 --PRECEDES--> C:e15
    C:e03 --SAME_TRACK--> C:e04
    C:e05 --SAME_TRACK--> C:e06
    C:e03 --SAME_TRACK--> C:e07
    C:e03 --SAME_TRACK--> C:e09
    C:e03 --SAME_TRACK--> C:e10
    C:e05 --SAME_TRACK--> C:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 THROTTLE_START<br>C:e03 TRACK_APPEARED_FRONT track_001<br>C:e04 CLOSING_START track_001 | ego: not yet observed | - |
| 0.20 | C:e05 TRACK_APPEARED_LEFT track_002<br>C:e06 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? | 0.10 |
| 3.75 | C:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING | 3.70 |
| 4.70 | C:e08 COLLISION<br>C:e09 CRITICAL_TTC_END track_001<br>C:e10 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 4.60 |
| 4.75 | C:e11 THROTTLE_END<br>C:e12 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING | 4.70 |
| 5.00 | C:e13 CLOSING_END track_002<br>C:e14 MOVING_END<br>C:e15 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING | 4.90 |

## States still active when observation ended

- BRAKE, since C:e12 (t = 4.75 s)
- STOP, since C:e15 (t = 5.00 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 4.70 (+0.95 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 13.95 | 278 | 74.1 m / -3 deg | 0.23 m (13.95) | 0.2 m / -90 deg | 11.1 m/s |
| track_002 | 0.20 | 13.95 | 268 | 45.8 m / -54 deg | 5.59 m (13.95) | 5.6 m / -34 deg | 10.3 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C pressed the accelerator (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.20 s: C's radar started tracking track_002, which appeared on its left.
- t = 0.20 s: C observed track_002 start closing in (already the case when first observed).
- t = 3.75 s: C's time-to-contact with track_001 became critical.
- t = 4.70 s: C's collision sensor recorded a contact (peak impulse 1880 N*s).
- t = 4.70 s: C's time-to-contact with track_001 stopped being critical.
- t = 4.70 s: C observed track_001 stop closing in.
- t = 4.75 s: C released the accelerator.
- t = 4.75 s: C started braking.
- t = 5.00 s: C observed track_002 stop closing in.
- t = 5.00 s: C stopped moving.
- t = 5.00 s: C came to a stop.
