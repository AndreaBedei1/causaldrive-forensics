# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 77.64883407205343 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 35 (PRECEDES 24, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.15 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 0.75 | TRACK_LOST | A | track_001 | radar |  |
| A:e05 | 2.75 | SPEED_LIMIT_EXCEEDED_START | A | - | ego |  |
| A:e06 | 3.35 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e07 | 3.35 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e08 | 3.85 | CUT_IN_FROM_LEFT_START | A | track_002 | radar |  |
| A:e09 | 4.00 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e10 | 5.45 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e11 | 5.65 | COLLISION | A | - | collision_sensor | peak_impulse=5215.85 |
| A:e12 | 5.65 | SPEED_LIMIT_EXCEEDED_END | A | - | ego |  |
| A:e13 | 5.70 | BRAKE_START | A | - | controls |  |
| A:e14 | 5.85 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e15 | 6.40 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e16 | 6.80 | CUT_IN_FROM_LEFT_END | A | track_002 | radar |  |
| A:e17 | 6.85 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e18 | 6.85 | CLOSING_END | A | track_002 | radar |  |
| A:e19 | 6.95 | MOVING_END | A | - | ego |  |
| A:e20 | 6.95 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e06 --SAME_TRACK--> A:e07
    A:e06 --SAME_TRACK--> A:e08
    A:e06 --SAME_TRACK--> A:e09
    A:e06 --SAME_TRACK--> A:e10
    A:e06 --SAME_TRACK--> A:e14
    A:e06 --SAME_TRACK--> A:e15
    A:e06 --SAME_TRACK--> A:e16
    A:e06 --SAME_TRACK--> A:e17
    A:e06 --SAME_TRACK--> A:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.15 | A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.10 |
| 0.75 | A:e04 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING | 0.70 |
| 2.75 | A:e05 SPEED_LIMIT_EXCEEDED_START | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 2.70 |
| 3.35 | A:e06 TRACK_APPEARED_LEFT track_002<br>A:e07 CLOSING_START track_002 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track lost, states UNKNOWN: track_001 | 3.30 |
| 3.85 | A:e08 CUT_IN_FROM_LEFT_START track_002 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 | 3.80 |
| 4.00 | A:e09 CRITICAL_TTC_START track_002 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 3.90 |
| 5.45 | A:e10 EGO_PATH_ENTRY track_002 | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 5.40 |
| 5.65 | A:e11 COLLISION<br>A:e12 SPEED_LIMIT_EXCEEDED_END | ego: MOVING, SPEED_LIMIT_EXCEEDED<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 5.60 |
| 5.70 | A:e13 BRAKE_START | ego: MOVING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 5.60 |
| 5.85 | A:e14 CRITICAL_TTC_END track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 5.80 |
| 6.40 | A:e15 CRITICAL_TTC_START track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 6.30 |
| 6.80 | A:e16 CUT_IN_FROM_LEFT_END track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_001 | 6.70 |
| 6.85 | A:e17 CRITICAL_TTC_END track_002<br>A:e18 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 6.80 |
| 6.95 | A:e19 MOVING_END<br>A:e20 STOP_START | ego: MOVING, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001 | 6.90 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 0.15 s); the track was lost at 0.75 s
- EGO_PATH of track_002, since A:e10 (t = 5.45 s)
- BRAKE, since A:e13 (t = 5.70 s)
- STOP, since A:e20 (t = 6.95 s)

## Tracks lost

- track_001 at 0.75 s (A:e04): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_002: cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 3.85 < CRITICAL_TTC_START 4.00 (+0.15 s) < COLLISION 5.65 (+1.65 s); EGO_PATH_ENTRY 5.45 after critical TTC (+1.45 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.15 | 0.75 | 7 | 32.7 m / -6 deg | 30.50 m (0.75) | 30.5 m / -7 deg | 7.1 m/s |
| track_002 | 3.35 | 9.95 | 128 | 18.3 m / -11 deg | 0.25 m (7.35) | 0.4 m / -0 deg | 11.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.15 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.75 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.75 s: A began exceeding the speed limit.
- t = 3.35 s: A's radar started tracking track_002, which appeared on its left.
- t = 3.35 s: A observed track_002 start closing in (already the case when first observed).
- t = 3.85 s: A observed track_002 cutting in from the left.
- t = 4.00 s: A's time-to-contact with track_002 became critical.
- t = 5.45 s: A observed track_002 enter its forward path corridor.
- t = 5.65 s: A's collision sensor recorded a contact (peak impulse 5216 N*s).
- t = 5.65 s: A returned within the speed limit.
- t = 5.70 s: A started braking.
- t = 5.85 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.40 s: A's time-to-contact with track_002 became critical.
- t = 6.80 s: A observed track_002's cut-in from the left settle.
- t = 6.85 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.85 s: A observed track_002 stop closing in.
- t = 6.95 s: A stopped moving.
- t = 6.95 s: A came to a stop.
