# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 267.8788150437176 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 47 (PRECEDES 38, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_REAR | A | track_001 | radar |  |
| A:e03 | 0.70 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.40 | CLOSING_END | A | track_001 | radar |  |
| A:e05 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e06 | 4.20 | CLOSING_START | A | track_001 | radar |  |
| A:e07 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e08 | 5.15 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 5.80 | MOVING_END | A | - | ego |  |
| A:e10 | 5.80 | STOP_START | A | - | ego |  |
| A:e11 | 10.95 | BRAKE_END | A | - | controls |  |
| A:e12 | 11.40 | STOP_END | A | - | ego |  |
| A:e13 | 11.40 | MOVING_START | A | - | ego |  |
| A:e14 | 13.15 | TRACK_APPEARED_FRONT | A | track_002 | radar |  |
| A:e15 | 13.15 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e16 | 13.15 | CRITICAL_TTC_START | A | track_002 | radar | active_at_first_observation=True |
| A:e17 | 14.10 | COLLISION | A | - | collision_sensor | peak_impulse=9089.81 |
| A:e18 | 14.10 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e19 | 14.10 | CLOSING_END | A | track_002 | radar |  |
| A:e20 | 14.65 | MOVING_END | A | - | ego |  |
| A:e21 | 14.65 | STOP_START | A | - | ego |  |
| A:e22 | 17.80 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e12 --PRECEDES--> A:e16
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e14 --PRECEDES--> A:e19
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e08
    A:e14 --SAME_TRACK--> A:e15
    A:e14 --SAME_TRACK--> A:e16
    A:e14 --SAME_TRACK--> A:e18
    A:e14 --SAME_TRACK--> A:e19
    A:e02 --SAME_TRACK--> A:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_REAR track_001 | ego: not yet observed | - |
| 0.70 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state | 0.60 |
| 1.40 | A:e04 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING | 1.30 |
| 3.95 | A:e05 BRAKE_START | ego: MOVING<br>track_001: no active state | 3.90 |
| 4.20 | A:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>track_001: no active state | 4.10 |
| 5.15 | A:e07 COLLISION<br>A:e08 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING | 5.10 |
| 5.80 | A:e09 MOVING_END<br>A:e10 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 5.70 |
| 10.95 | A:e11 BRAKE_END | ego: STOP, BRAKE<br>track_001: no active state | 10.90 |
| 11.40 | A:e12 STOP_END<br>A:e13 MOVING_START | ego: STOP<br>track_001: no active state | 11.30 |
| 13.15 | A:e14 TRACK_APPEARED_FRONT track_002<br>A:e15 CLOSING_START track_002<br>A:e16 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: no active state | 13.10 |
| 14.10 | A:e17 COLLISION<br>A:e18 CRITICAL_TTC_END track_002<br>A:e19 CLOSING_END track_002 | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 14.00 |
| 14.65 | A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING<br>track_001: no active state<br>track_002: IN_EGO_PATH | 14.60 |
| 17.80 | A:e22 TRACK_LOST track_001 | ego: STOP<br>track_001: no active state<br>track_002: IN_EGO_PATH | 17.70 |

## States still active when observation ended

- STOP, since A:e21 (t = 14.65 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 13.15, COLLISION 14.10 (+0.95 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 17.80 | 339 | 6.2 m / -180 deg | 3.73 m (5.15) | 24.2 m / +178 deg | 13.3 m/s |
| track_002 | 13.15 | 17.95 | 93 | 9.5 m / +1 deg | 2.12 m (14.55) | 2.1 m / -1 deg | 3.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared behind it.
- t = 0.70 s: A observed track_001 start closing in.
- t = 1.40 s: A observed track_001 stop closing in.
- t = 3.95 s: A started braking.
- t = 4.20 s: A observed track_001 start closing in.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.15 s: A observed track_001 stop closing in.
- t = 5.80 s: A stopped moving.
- t = 5.80 s: A came to a stop.
- t = 10.95 s: A released the brake.
- t = 11.40 s: A left its stop.
- t = 11.40 s: A started moving.
- t = 13.15 s: A's radar started tracking track_002, which appeared in front of it.
- t = 13.15 s: A observed track_002 start closing in (already the case when first observed).
- t = 13.15 s: A's time-to-contact with track_002 became critical (already the case when first observed).
- t = 14.10 s: A's collision sensor recorded a contact (peak impulse 9090 N*s).
- t = 14.10 s: A's time-to-contact with track_002 stopped being critical.
- t = 14.10 s: A observed track_002 stop closing in.
- t = 14.65 s: A stopped moving.
- t = 14.65 s: A came to a stop.
- t = 17.80 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
