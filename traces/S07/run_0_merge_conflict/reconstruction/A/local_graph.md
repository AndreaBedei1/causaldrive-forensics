# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 15.514892023056746 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 235 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (23.35 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 25 (PRECEDES 21, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TURN_LEFT_START | A | - | ego | active_at_first_observation=True |
| A:e04 | 2.75 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e05 | 2.75 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 6.95 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 10.25 | COLLISION | A | - | collision_sensor | peak_impulse=1904.84; merged_bursts=[[10.35, 116.28], [10.85, 7.95]] |
| A:e08 | 10.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e09 | 10.25 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 10.30 | THROTTLE_END | A | - | controls |  |
| A:e11 | 10.30 | BRAKE_START | A | - | controls |  |
| A:e12 | 10.55 | TURN_LEFT_END | A | - | ego |  |
| A:e13 | 11.05 | MOVING_END | A | - | ego |  |
| A:e14 | 11.05 | STOP_START | A | - | ego |  |

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
    A:e06 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e07 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TURN_LEFT_START | ego: not yet observed | - |
| 2.75 | A:e04 TRACK_APPEARED_LEFT track_001<br>A:e05 CLOSING_START track_001 | ego: MOVING, THROTTLE, TURN_LEFT | 2.70 |
| 6.95 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING | 6.90 |
| 10.25 | A:e07 COLLISION<br>A:e08 CRITICAL_TTC_END track_001<br>A:e09 CLOSING_END track_001 | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 10.20 |
| 10.30 | A:e10 THROTTLE_END<br>A:e11 BRAKE_START | ego: MOVING, THROTTLE, TURN_LEFT<br>track_001: no active state | 10.20 |
| 10.55 | A:e12 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 10.50 |
| 11.05 | A:e13 MOVING_END<br>A:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 11.00 |

## States still active when observation ended

- BRAKE, since A:e11 (t = 10.30 s)
- STOP, since A:e14 (t = 11.05 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 6.95, COLLISION 10.25 (+3.30 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.75 | 23.35 | 402 | 87.4 m / -43 deg | 0.97 m (10.25) | 1.6 m / +101 deg | 9.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A started turning left (already the case when first observed).
- t = 2.75 s: A's radar started tracking track_001, which appeared on its left.
- t = 2.75 s: A observed track_001 start closing in (already the case when first observed).
- t = 6.95 s: A's time-to-contact with track_001 became critical.
- t = 10.25 s: A's collision sensor recorded a contact (peak impulse 1905 N*s).
- t = 10.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 10.25 s: A observed track_001 stop closing in.
- t = 10.30 s: A released the accelerator.
- t = 10.30 s: A started braking.
- t = 10.55 s: A stopped turning left.
- t = 11.05 s: A stopped moving.
- t = 11.05 s: A came to a stop.
