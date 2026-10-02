# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 14.006294470280409 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 235 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (23.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 27 (PRECEDES 21, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TURN_LEFT_START | A | - | ego | active_at_first_observation=True |
| A:e04 | 2.75 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e05 | 2.75 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 5.30 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e07 | 5.55 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e08 | 6.90 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e09 | 9.45 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e10 | 10.25 | COLLISION | A | - | collision_sensor | peak_impulse=1904.84; merged_bursts=[[10.35, 116.28], [10.85, 7.95]] |
| A:e11 | 10.25 | CLOSING_END | A | track_001 | radar |  |
| A:e12 | 10.30 | THROTTLE_END | A | - | controls |  |
| A:e13 | 10.30 | BRAKE_START | A | - | controls |  |
| A:e14 | 10.55 | TURN_LEFT_END | A | - | ego |  |
| A:e15 | 11.05 | MOVING_END | A | - | ego |  |
| A:e16 | 11.05 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e01 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TURN_LEFT_START | ego: not yet observed | - |
| 2.75 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING, THROTTLE, TURN_LEFT | 2.70 |
| 5.30 | A:e06 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING | 5.20 |
| 5.55 | A:e07 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH | 5.50 |
| 6.90 | A:e08 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING | 6.80 |
| 9.45 | A:e09 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 9.40 |
| 10.25 | A:e10 COLLISION<br>A:e11 CLOSING_END track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING | 10.20 |
| 10.30 | A:e12 THROTTLE_END<br>A:e13 BRAKE_START | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: no active state | 10.20 |
| 10.55 | A:e14 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 10.50 |
| 11.05 | A:e15 MOVING_END<br>A:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 11.00 |

## States still active when observation ended

- BRAKE, since A:e13 (t = 10.30 s)
- STOP, since A:e16 (t = 11.05 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 6.90, COLLISION 10.25 (+3.35 s); EGO_PATH_ENTRY 5.30 before critical TTC (-1.60 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.75 | 23.35 | 401 | 87.4 m / -43 deg | 0.99 m (10.55) | 1.6 m / +101 deg | 10.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A started turning left (already the case when first observed).
- t = 2.75 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.75 s: A observed track_001 start closing in (already the case when first observed).
- t = 5.30 s: A observed track_001 enter its forward path corridor.
- t = 5.55 s: A observed track_001 leave its forward path corridor.
- t = 6.90 s: A's time-to-contact with track_001 became critical.
- t = 9.45 s: A's time-to-contact with track_001 stopped being critical.
- t = 10.25 s: A's collision sensor recorded a contact (peak impulse 1905 N*s).
- t = 10.25 s: A observed track_001 stop closing in.
- t = 10.30 s: A released the accelerator.
- t = 10.30 s: A started braking.
- t = 10.55 s: A stopped turning left.
- t = 11.05 s: A stopped moving.
- t = 11.05 s: A came to a stop.
