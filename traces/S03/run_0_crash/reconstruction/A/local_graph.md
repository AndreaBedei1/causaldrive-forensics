# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 68.5934028364718 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 28 (PRECEDES 22, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 2.05 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e04 | 2.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 2.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e06 | 4.10 | COLLISION | A | - | collision_sensor | peak_impulse=12137.59; merged_bursts=[[4.35, 2340.23]] |
| A:e07 | 4.10 | CLOSING_END | A | track_001 | radar |  |
| A:e08 | 4.10 | TURN_LEFT_START | A | - | ego |  |
| A:e09 | 4.15 | THROTTLE_END | A | - | controls |  |
| A:e10 | 4.15 | BRAKE_START | A | - | controls |  |
| A:e11 | 4.25 | CLOSING_START | A | track_001 | radar |  |
| A:e12 | 4.55 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e13 | 4.65 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 4.70 | TURN_LEFT_END | A | - | ego |  |
| A:e15 | 4.75 | MOVING_END | A | - | ego |  |
| A:e16 | 4.75 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e06 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 2.05 | A:e03 TRACK_APPEARED_RIGHT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 2.00 |
| 2.55 | A:e05 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? | 2.50 |
| 4.10 | A:e06 COLLISION<br>A:e07 CLOSING_END track_001<br>A:e08 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC | 4.00 |
| 4.15 | A:e09 THROTTLE_END<br>A:e10 BRAKE_START | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CRITICAL_TTC | 4.10 |
| 4.25 | A:e11 CLOSING_START track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CRITICAL_TTC | 4.20 |
| 4.55 | A:e12 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 4.50 |
| 4.65 | A:e13 CLOSING_END track_001 | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: CLOSING | 4.60 |
| 4.70 | A:e14 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 4.60 |
| 4.75 | A:e15 MOVING_END<br>A:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.70 |

## States still active when observation ended

- BRAKE, since A:e10 (t = 4.15 s)
- STOP, since A:e16 (t = 4.75 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.55, COLLISION 4.10 (+1.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.05 | 15.15 | 263 | 33.2 m / +49 deg | 0.10 m (15.15) | 0.1 m / +88 deg | 12.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 2.05 s: A's radar started tracking track_001, which appeared on its right.
- t = 2.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.55 s: A's time-to-contact with track_001 became critical.
- t = 4.10 s: A's collision sensor recorded a contact (peak impulse 12138 N*s).
- t = 4.10 s: A observed track_001 stop closing in.
- t = 4.10 s: A started turning left.
- t = 4.15 s: A released the accelerator.
- t = 4.15 s: A started braking.
- t = 4.25 s: A observed track_001 start closing in.
- t = 4.55 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.65 s: A observed track_001 stop closing in.
- t = 4.70 s: A stopped turning left.
- t = 4.75 s: A stopped moving.
- t = 4.75 s: A came to a stop.
