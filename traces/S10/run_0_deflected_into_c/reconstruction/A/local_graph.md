# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 204.24685563519597 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 41; edges: 86 (PRECEDES 56, SAME_TRACK 30)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.10 | TRACK_APPEARED_FRONT | A | track_001 | radar | initial_in_ego_path=False |
| A:e04 | 0.10 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.15 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e06 | 0.20 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e07 | 0.70 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e08 | 0.75 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e09 | 1.05 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e10 | 1.10 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e11 | 1.60 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e12 | 1.65 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e13 | 1.95 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e14 | 2.00 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e15 | 2.05 | TRACK_APPEARED_RIGHT | A | track_002 | radar | initial_in_ego_path=False |
| A:e16 | 2.05 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e17 | 2.15 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e18 | 2.20 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e19 | 2.50 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e20 | 2.55 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e21 | 2.55 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e22 | 3.05 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e23 | 3.10 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e24 | 3.60 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e25 | 3.65 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e26 | 3.65 | EGO_PATH_ENTRY | A | track_002 | radar | geometry=estimated_body |
| A:e27 | 3.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e28 | 3.80 | COLLISION | A | - | collision_sensor | peak_impulse=10358.22 |
| A:e29 | 3.80 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e30 | 3.80 | CLOSING_END | A | track_002 | radar |  |
| A:e31 | 3.85 | THROTTLE_END | A | - | controls |  |
| A:e32 | 3.85 | TURN_LEFT_START | A | - | ego |  |
| A:e33 | 4.05 | EGO_PATH_EXIT | A | track_002 | radar | geometry=estimated_body |
| A:e34 | 4.05 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e35 | 4.70 | COLLISION | A | - | collision_sensor | peak_impulse=1880.32 |
| A:e36 | 4.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e37 | 5.00 | CLOSING_END | A | track_001 | radar |  |
| A:e38 | 5.00 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e39 | 5.05 | TURN_LEFT_END | A | - | ego |  |
| A:e40 | 5.10 | MOVING_END | A | - | ego |  |
| A:e41 | 5.10 | STOP_START | A | - | ego |  |

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
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e17
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e19 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e27
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e27 --PRECEDES--> A:e29
    A:e27 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e28 --PRECEDES--> A:e32
    A:e29 --PRECEDES--> A:e31
    A:e29 --PRECEDES--> A:e32
    A:e30 --PRECEDES--> A:e31
    A:e30 --PRECEDES--> A:e32
    A:e31 --PRECEDES--> A:e33
    A:e31 --PRECEDES--> A:e34
    A:e32 --PRECEDES--> A:e33
    A:e32 --PRECEDES--> A:e34
    A:e33 --PRECEDES--> A:e35
    A:e33 --PRECEDES--> A:e36
    A:e34 --PRECEDES--> A:e35
    A:e34 --PRECEDES--> A:e36
    A:e35 --PRECEDES--> A:e37
    A:e35 --PRECEDES--> A:e38
    A:e36 --PRECEDES--> A:e37
    A:e36 --PRECEDES--> A:e38
    A:e37 --PRECEDES--> A:e39
    A:e38 --PRECEDES--> A:e39
    A:e39 --PRECEDES--> A:e40
    A:e39 --PRECEDES--> A:e41
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e08
    A:e03 --SAME_TRACK--> A:e09
    A:e03 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e15 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e17
    A:e03 --SAME_TRACK--> A:e18
    A:e03 --SAME_TRACK--> A:e19
    A:e03 --SAME_TRACK--> A:e20
    A:e15 --SAME_TRACK--> A:e21
    A:e03 --SAME_TRACK--> A:e22
    A:e03 --SAME_TRACK--> A:e23
    A:e03 --SAME_TRACK--> A:e24
    A:e03 --SAME_TRACK--> A:e25
    A:e15 --SAME_TRACK--> A:e26
    A:e03 --SAME_TRACK--> A:e27
    A:e15 --SAME_TRACK--> A:e29
    A:e15 --SAME_TRACK--> A:e30
    A:e15 --SAME_TRACK--> A:e33
    A:e03 --SAME_TRACK--> A:e34
    A:e03 --SAME_TRACK--> A:e36
    A:e03 --SAME_TRACK--> A:e37
    A:e03 --SAME_TRACK--> A:e38
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 0.10 | A:e03 TRACK_APPEARED_FRONT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 0.00 |
| 0.15 | A:e05 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? | 0.10 |
| 0.20 | A:e06 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CRITICAL_TTC? | 0.10 |
| 0.70 | A:e07 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 0.60 |
| 0.75 | A:e08 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH | 0.70 |
| 1.05 | A:e09 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 1.00 |
| 1.10 | A:e10 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH | 1.00 |
| 1.60 | A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 1.50 |
| 1.65 | A:e12 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH | 1.60 |
| 1.95 | A:e13 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 1.90 |
| 2.00 | A:e14 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH | 1.90 |
| 2.05 | A:e15 TRACK_APPEARED_RIGHT track_002<br>A:e16 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 2.00 |
| 2.15 | A:e17 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? | 2.10 |
| 2.20 | A:e18 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC? | 2.10 |
| 2.50 | A:e19 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? | 2.40 |
| 2.55 | A:e20 EGO_PATH_EXIT track_001<br>A:e21 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC? | 2.50 |
| 3.05 | A:e22 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 3.00 |
| 3.10 | A:e23 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC | 3.00 |
| 3.60 | A:e24 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 3.50 |
| 3.65 | A:e25 EGO_PATH_EXIT track_001<br>A:e26 EGO_PATH_ENTRY track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC | 3.60 |
| 3.75 | A:e27 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 3.70 |
| 3.80 | A:e28 COLLISION<br>A:e29 CRITICAL_TTC_END track_002<br>A:e30 CLOSING_END track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 3.70 |
| 3.85 | A:e31 THROTTLE_END<br>A:e32 TURN_LEFT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: IN_EGO_PATH | 3.80 |
| 4.05 | A:e33 EGO_PATH_EXIT track_002<br>A:e34 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: IN_EGO_PATH | 4.00 |
| 4.70 | A:e35 COLLISION<br>A:e36 CRITICAL_TTC_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state | 4.60 |
| 5.00 | A:e37 CLOSING_END track_001<br>A:e38 EGO_PATH_EXIT track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: no active state | 4.90 |
| 5.05 | A:e39 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: no active state<br>track_002: no active state | 5.00 |
| 5.10 | A:e40 MOVING_END<br>A:e41 STOP_START | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 5.00 |

## States still active when observation ended

- STOP, since A:e41 (t = 5.10 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 3.80 (+0.05 s); EGO_PATH_ENTRY 0.15 before critical TTC (-3.60 s)
- track_002: CRITICAL_TTC_START 2.55, COLLISION 3.80 (+1.25 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.10 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.10 | 13.95 | 277 | 72.4 m / -3 deg | 0.26 m (13.95) | 0.3 m / -81 deg | 6.2 m/s |
| track_002 | 2.05 | 13.95 | 239 | 28.5 m / +31 deg | 1.14 m (4.15) | 4.7 m / +140 deg | 9.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.10 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.10 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.15 s: A observed track_001 enter its forward path corridor.
- t = 0.20 s: A observed track_001 leave its forward path corridor.
- t = 0.70 s: A observed track_001 enter its forward path corridor.
- t = 0.75 s: A observed track_001 leave its forward path corridor.
- t = 1.05 s: A observed track_001 enter its forward path corridor.
- t = 1.10 s: A observed track_001 leave its forward path corridor.
- t = 1.60 s: A observed track_001 enter its forward path corridor.
- t = 1.65 s: A observed track_001 leave its forward path corridor.
- t = 1.95 s: A observed track_001 enter its forward path corridor.
- t = 2.00 s: A observed track_001 leave its forward path corridor.
- t = 2.05 s: A's radar started tracking track_002, which appeared on its right.
- t = 2.05 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.15 s: A observed track_001 enter its forward path corridor.
- t = 2.20 s: A observed track_001 leave its forward path corridor.
- t = 2.50 s: A observed track_001 enter its forward path corridor.
- t = 2.55 s: A observed track_001 leave its forward path corridor.
- t = 2.55 s: A's time-to-contact with track_002 became critical.
- t = 3.05 s: A observed track_001 enter its forward path corridor.
- t = 3.10 s: A observed track_001 leave its forward path corridor.
- t = 3.60 s: A observed track_001 enter its forward path corridor.
- t = 3.65 s: A observed track_001 leave its forward path corridor.
- t = 3.65 s: A observed track_002 enter its forward path corridor.
- t = 3.75 s: A's time-to-contact with track_001 became critical.
- t = 3.80 s: A's collision sensor recorded a contact (peak impulse 10358 N*s).
- t = 3.80 s: A's time-to-contact with track_002 stopped being critical.
- t = 3.80 s: A observed track_002 stop closing in.
- t = 3.85 s: A released the accelerator.
- t = 3.85 s: A started turning left.
- t = 4.05 s: A observed track_002 leave its forward path corridor.
- t = 4.05 s: A observed track_001 enter its forward path corridor.
- t = 4.70 s: A's collision sensor recorded a contact (peak impulse 1880 N*s).
- t = 4.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.00 s: A observed track_001 stop closing in.
- t = 5.00 s: A observed track_001 leave its forward path corridor.
- t = 5.05 s: A stopped turning left.
- t = 5.10 s: A stopped moving.
- t = 5.10 s: A came to a stop.
