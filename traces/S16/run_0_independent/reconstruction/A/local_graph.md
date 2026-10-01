# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 13.179586462676525 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 181 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (17.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 30 (PRECEDES 23, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e03 | 5.15 | COLLISION | A | - | collision_sensor | peak_impulse=6073.81 |
| A:e04 | 5.80 | MOVING_END | A | - | ego |  |
| A:e05 | 5.80 | STOP_START | A | - | ego |  |
| A:e06 | 10.95 | BRAKE_END | A | - | controls |  |
| A:e07 | 11.15 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e08 | 11.15 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e09 | 11.40 | STOP_END | A | - | ego |  |
| A:e10 | 11.40 | MOVING_START | A | - | ego |  |
| A:e11 | 11.75 | CLOSING_START | A | track_002 | radar |  |
| A:e12 | 11.80 | CLOSING_START | A | track_001 | radar |  |
| A:e13 | 11.90 | TRACK_LOST | A | track_001 | radar |  |
| A:e14 | 12.10 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e15 | 12.65 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e16 | 14.10 | COLLISION | A | - | collision_sensor | peak_impulse=9095.53 |
| A:e17 | 14.30 | CLOSING_END | A | track_002 | radar |  |
| A:e18 | 14.35 | TRACK_LOST | A | track_002 | radar |  |
| A:e19 | 14.65 | MOVING_END | A | - | ego |  |
| A:e20 | 14.65 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e02 --PRECEDES--> A:e03
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
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
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e08 --SAME_TRACK--> A:e11
    A:e07 --SAME_TRACK--> A:e12
    A:e07 --SAME_TRACK--> A:e13
    A:e08 --SAME_TRACK--> A:e14
    A:e08 --SAME_TRACK--> A:e15
    A:e08 --SAME_TRACK--> A:e17
    A:e08 --SAME_TRACK--> A:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 3.95 | A:e02 BRAKE_START | ego: MOVING | 3.90 |
| 5.15 | A:e03 COLLISION | ego: MOVING, BRAKE | 5.10 |
| 5.80 | A:e04 MOVING_END<br>A:e05 STOP_START | ego: MOVING, BRAKE | 5.70 |
| 10.95 | A:e06 BRAKE_END | ego: STOP, BRAKE | 10.90 |
| 11.15 | A:e07 TRACK_APPEARED_LEFT track_001<br>A:e08 TRACK_APPEARED_LEFT track_002 | ego: STOP | 11.10 |
| 11.40 | A:e09 STOP_END<br>A:e10 MOVING_START | ego: STOP<br>track_001: no active state<br>track_002: no active state | 11.30 |
| 11.75 | A:e11 CLOSING_START track_002 | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 11.70 |
| 11.80 | A:e12 CLOSING_START track_001 | ego: MOVING<br>track_001: no active state<br>track_002: CLOSING | 11.70 |
| 11.90 | A:e13 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 11.80 |
| 12.10 | A:e14 EGO_PATH_ENTRY track_002 | ego: MOVING<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 | 12.00 |
| 12.65 | A:e15 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 12.60 |
| 14.10 | A:e16 COLLISION | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 14.00 |
| 14.30 | A:e17 CLOSING_END track_002 | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 14.20 |
| 14.35 | A:e18 TRACK_LOST track_002 | ego: MOVING<br>track_002: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 14.30 |
| 14.65 | A:e19 MOVING_END<br>A:e20 STOP_START | ego: MOVING<br>track lost, states UNKNOWN: track_001, track_002 | 14.60 |

## States still active when observation ended

- CLOSING of track_001, since A:e12 (t = 11.80 s); the track was lost at 11.90 s
- EGO_PATH of track_002, since A:e14 (t = 12.10 s); the track was lost at 14.35 s
- CRITICAL_TTC of track_002, since A:e15 (t = 12.65 s); the track was lost at 14.35 s
- STOP, since A:e20 (t = 14.65 s)

## Tracks lost

- track_001 at 11.90 s (A:e13): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 14.35 s (A:e18): CRITICAL_TTC, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: CRITICAL_TTC_START 12.65, COLLISION 14.10 (+1.45 s); EGO_PATH_ENTRY 12.10 before critical TTC (-0.55 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 11.15 | 11.90 | 15 | 14.9 m / -12 deg | 14.70 m (11.90) | 14.7 m / -12 deg | 1.3 m/s |
| track_002 | 11.15 | 14.35 | 59 | 15.5 m / -8 deg | 0.05 m (14.30) | 0.1 m / +132 deg | 2.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 3.95 s: A started braking.
- t = 5.15 s: A's collision sensor recorded a contact (peak impulse 6074 N*s).
- t = 5.80 s: A stopped moving.
- t = 5.80 s: A came to a stop.
- t = 10.95 s: A released the brake.
- t = 11.15 s: A's radar started tracking track_001, which appeared on its left.
- t = 11.15 s: A's radar started tracking track_002, which appeared on its left.
- t = 11.40 s: A left its stop.
- t = 11.40 s: A started moving.
- t = 11.75 s: A observed track_002 start closing in.
- t = 11.80 s: A observed track_001 start closing in.
- t = 11.90 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 12.10 s: A observed track_002 enter its forward path corridor.
- t = 12.65 s: A's time-to-contact with track_002 became critical.
- t = 14.10 s: A's collision sensor recorded a contact (peak impulse 9096 N*s).
- t = 14.30 s: A observed track_002 stop closing in.
- t = 14.35 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 14.65 s: A stopped moving.
- t = 14.65 s: A came to a stop.
