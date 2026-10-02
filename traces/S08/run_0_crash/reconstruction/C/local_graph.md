# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 248.77736597135663 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 34 (PRECEDES 24, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | TRACK_APPEARED_FRONT | C | track_001 | radar |  |
| C:e03 | 0.00 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e04 | 2.25 | TRACK_APPEARED_LEFT | C | track_002 | radar |  |
| C:e05 | 2.25 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e06 | 2.25 | CRITICAL_TTC_START | C | track_001 | radar |  |
| C:e07 | 2.35 | BRAKE_START | C | - | controls |  |
| C:e08 | 2.80 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e09 | 2.85 | MOVING_END | C | - | ego |  |
| C:e10 | 2.85 | STOP_START | C | - | ego |  |
| C:e11 | 3.20 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e12 | 3.55 | CRITICAL_TTC_START | C | track_002 | radar |  |
| C:e13 | 3.85 | CRITICAL_TTC_END | C | track_001 | radar |  |
| C:e14 | 3.85 | CRITICAL_TTC_END | C | track_002 | radar |  |
| C:e15 | 4.55 | CLOSING_END | C | track_002 | radar |  |
| C:e16 | 4.90 | CLOSING_END | C | track_001 | radar |  |
| C:e17 | 14.35 | BRAKE_END | C | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e04
    C:e01 --PRECEDES--> C:e05
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e07
    C:e07 --PRECEDES--> C:e08
    C:e08 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e12 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e15
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e16 --PRECEDES--> C:e17
    C:e02 --SAME_TRACK--> C:e03
    C:e04 --SAME_TRACK--> C:e05
    C:e02 --SAME_TRACK--> C:e06
    C:e04 --SAME_TRACK--> C:e08
    C:e04 --SAME_TRACK--> C:e11
    C:e04 --SAME_TRACK--> C:e12
    C:e02 --SAME_TRACK--> C:e13
    C:e04 --SAME_TRACK--> C:e14
    C:e04 --SAME_TRACK--> C:e15
    C:e02 --SAME_TRACK--> C:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 TRACK_APPEARED_FRONT track_001<br>C:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 2.25 | C:e04 TRACK_APPEARED_LEFT track_002<br>C:e05 CLOSING_START track_002<br>C:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 2.20 |
| 2.35 | C:e07 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 2.30 |
| 2.80 | C:e08 CRITICAL_TTC_START track_002 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 2.70 |
| 2.85 | C:e09 MOVING_END<br>C:e10 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 2.80 |
| 3.20 | C:e11 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 3.10 |
| 3.55 | C:e12 CRITICAL_TTC_START track_002 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 3.50 |
| 3.85 | C:e13 CRITICAL_TTC_END track_001<br>C:e14 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 3.80 |
| 4.55 | C:e15 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING | 4.50 |
| 4.90 | C:e16 CLOSING_END track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>track_002: no active state | 4.80 |
| 14.35 | C:e17 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state | 14.30 |

## States still active when observation ended

- STOP, since C:e10 (t = 2.85 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.25
- track_002: CRITICAL_TTC_START 2.80

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 15.15 | 278 | 76.9 m / -3 deg | 10.13 m (5.00) | 10.2 m / -15 deg | 9.8 m/s |
| track_002 | 2.25 | 15.15 | 258 | 35.1 m / -61 deg | 13.46 m (4.65) | 13.6 m / -26 deg | 12.7 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001, which appeared in front of it.
- t = 0.00 s: C observed track_001 start closing in (already the case when first observed).
- t = 2.25 s: C's radar started tracking track_002, which appeared on its left.
- t = 2.25 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.25 s: C's time-to-contact with track_001 became critical.
- t = 2.35 s: C started braking.
- t = 2.80 s: C's time-to-contact with track_002 became critical.
- t = 2.85 s: C stopped moving.
- t = 2.85 s: C came to a stop.
- t = 3.20 s: C's time-to-contact with track_002 stopped being critical.
- t = 3.55 s: C's time-to-contact with track_002 became critical.
- t = 3.85 s: C's time-to-contact with track_001 stopped being critical.
- t = 3.85 s: C's time-to-contact with track_002 stopped being critical.
- t = 4.55 s: C observed track_002 stop closing in.
- t = 4.90 s: C observed track_001 stop closing in.
- t = 14.35 s: C released the brake.
