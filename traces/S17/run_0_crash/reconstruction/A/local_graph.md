# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 12.853837836533785 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 43 (PRECEDES 30, SAME_TRACK 13)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e04 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e05 | 2.80 | CLOSING_START | A | track_001 | radar |  |
| A:e06 | 3.45 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar |  |
| A:e07 | 4.15 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 4.25 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e09 | 4.40 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e10 | 4.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e11 | 4.90 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar |  |
| A:e12 | 5.00 | CLOSING_END | A | track_001 | radar |  |
| A:e13 | 5.00 | CLOSING_START | A | track_002 | radar |  |
| A:e14 | 5.45 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e15 | 5.75 | COLLISION | A | - | collision_sensor | peak_impulse=915.98 |
| A:e16 | 5.75 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e17 | 5.80 | CLOSING_END | A | track_002 | radar |  |
| A:e18 | 5.80 | THROTTLE_END | A | - | controls |  |
| A:e19 | 5.80 | BRAKE_START | A | - | controls |  |
| A:e20 | 6.85 | MOVING_END | A | - | ego |  |
| A:e21 | 6.85 | STOP_START | A | - | ego |  |
| A:e22 | 7.65 | TRACK_LOST | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
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
    A:e04 --SAME_TRACK--> A:e05
    A:e04 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e03 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e04 --SAME_TRACK--> A:e11
    A:e04 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e04 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e17
    A:e04 --SAME_TRACK--> A:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_002<br>A:e04 TRACK_APPEARED_RIGHT track_001 | ego: not yet observed | - |
| 2.80 | A:e05 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state | 2.70 |
| 3.45 | A:e06 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: no active state | 3.40 |
| 4.15 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_RIGHT<br>track_002: no active state | 4.10 |
| 4.25 | A:e08 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state | 4.20 |
| 4.40 | A:e09 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state | 4.30 |
| 4.70 | A:e10 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC | 4.60 |
| 4.90 | A:e11 CUT_IN_FROM_RIGHT_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: CRITICAL_TTC | 4.80 |
| 5.00 | A:e12 CLOSING_END track_001<br>A:e13 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CRITICAL_TTC | 4.90 |
| 5.45 | A:e14 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC | 5.40 |
| 5.75 | A:e15 COLLISION<br>A:e16 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC | 5.70 |
| 5.80 | A:e17 CLOSING_END track_002<br>A:e18 THROTTLE_END<br>A:e19 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING | 5.70 |
| 6.85 | A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state | 6.80 |
| 7.65 | A:e22 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state | 7.60 |

## States still active when observation ended

- BRAKE, since A:e19 (t = 5.80 s)
- STOP, since A:e21 (t = 6.85 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: cut-in started before critical TTC: CUT_IN_FROM_RIGHT_START 3.45 < CRITICAL_TTC_START 4.15 (+0.70 s) < COLLISION 5.75 (+1.60 s); EGO_PATH_ENTRY 4.25 after critical TTC (+0.10 s)
- track_002: CRITICAL_TTC_START 4.40, COLLISION 5.75 (+1.35 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 7.65 | 152 | 8.0 m / +17 deg | 3.16 m (4.95) | 26.0 m / +12 deg | 16.2 m/s |
| track_002 | 0.00 | 11.50 | 231 | 3.2 m / -132 deg | 0.02 m (6.15) | 0.5 m / -104 deg | 12.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 2.80 s: A observed track_001 start closing in.
- t = 3.45 s: A observed track_001 cutting in from the right.
- t = 4.15 s: A's time-to-contact with track_001 became critical.
- t = 4.25 s: A observed track_001 enter its forward path corridor.
- t = 4.40 s: A's time-to-contact with track_002 became critical.
- t = 4.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: A observed track_001's cut-in from the right settle.
- t = 5.00 s: A observed track_001 stop closing in.
- t = 5.00 s: A observed track_002 start closing in.
- t = 5.45 s: A observed track_001 leave its forward path corridor.
- t = 5.75 s: A's collision sensor recorded a contact (peak impulse 916 N*s).
- t = 5.75 s: A's time-to-contact with track_002 stopped being critical.
- t = 5.80 s: A observed track_002 stop closing in.
- t = 5.80 s: A released the accelerator.
- t = 5.80 s: A started braking.
- t = 6.85 s: A stopped moving.
- t = 6.85 s: A came to a stop.
- t = 7.65 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
