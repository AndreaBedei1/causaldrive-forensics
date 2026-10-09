# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 224.2758263722062 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 121 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 31; edges: 59 (PRECEDES 44, SAME_TRACK 15)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e04 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.05 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e06 | 0.05 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e07 | 3.95 | THROTTLE_END | A | - | controls |  |
| A:e08 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e09 | 4.45 | CLOSING_END | A | track_001 | radar |  |
| A:e10 | 4.45 | CLOSING_END | A | track_002 | radar |  |
| A:e11 | 4.55 | BRAKE_END | A | - | controls |  |
| A:e12 | 4.65 | THROTTLE_START | A | - | controls |  |
| A:e13 | 5.20 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e14 | 5.40 | EGO_PATH_ENTRY | A | track_002 | radar |  |
| A:e15 | 5.45 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e16 | 5.55 | COLLISION | A | - | collision_sensor | peak_impulse=4243.51 |
| A:e17 | 5.55 | THROTTLE_END | A | - | controls |  |
| A:e18 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e19 | 5.55 | CLOSING_START | A | track_001 | radar |  |
| A:e20 | 5.55 | CLOSING_START | A | track_002 | radar |  |
| A:e21 | 5.60 | BRAKE_END | A | - | controls |  |
| A:e22 | 5.75 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e23 | 6.60 | COLLISION | A | - | collision_sensor | peak_impulse=322.10; merged_bursts=[[6.85, 322.1], [7.6, 239.84]] |
| A:e24 | 6.60 | CLOSING_END | A | track_001 | radar |  |
| A:e25 | 6.60 | CLOSING_END | A | track_002 | radar |  |
| A:e26 | 6.75 | TRACK_LOST | A | track_002 | radar |  |
| A:e27 | 6.85 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |
| A:e28 | 7.00 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e29 | 7.45 | MOVING_END | A | - | ego |  |
| A:e30 | 7.45 | STOP_START | A | - | ego |  |
| A:e31 | 7.45 | BRAKE_START | A | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e01 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e05 --PRECEDES--> A:e08
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
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e19
    A:e15 --PRECEDES--> A:e20
    A:e16 --PRECEDES--> A:e21
    A:e17 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e21
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e22 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e22 --PRECEDES--> A:e25
    A:e23 --PRECEDES--> A:e26
    A:e24 --PRECEDES--> A:e26
    A:e25 --PRECEDES--> A:e26
    A:e26 --PRECEDES--> A:e27
    A:e27 --PRECEDES--> A:e28
    A:e28 --PRECEDES--> A:e29
    A:e28 --PRECEDES--> A:e30
    A:e28 --PRECEDES--> A:e31
    A:e03 --SAME_TRACK--> A:e04
    A:e05 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e09
    A:e05 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e13
    A:e05 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e15
    A:e03 --SAME_TRACK--> A:e19
    A:e05 --SAME_TRACK--> A:e20
    A:e03 --SAME_TRACK--> A:e22
    A:e03 --SAME_TRACK--> A:e24
    A:e05 --SAME_TRACK--> A:e25
    A:e05 --SAME_TRACK--> A:e26
    A:e03 --SAME_TRACK--> A:e27
    A:e03 --SAME_TRACK--> A:e28
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: not yet observed | - |
| 0.05 | A:e05 TRACK_APPEARED_LEFT track_002<br>A:e06 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? | 0.00 |
| 3.95 | A:e07 THROTTLE_END<br>A:e08 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING<br>track_002: CLOSING | 3.90 |
| 4.45 | A:e09 CLOSING_END track_001<br>A:e10 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track_002: CLOSING | 4.40 |
| 4.55 | A:e11 BRAKE_END | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state | 4.50 |
| 4.65 | A:e12 THROTTLE_START | ego: MOVING<br>track_001: no active state<br>track_002: no active state | 4.60 |
| 5.20 | A:e13 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state | 5.10 |
| 5.40 | A:e14 EGO_PATH_ENTRY track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: no active state | 5.30 |
| 5.45 | A:e15 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: IN_EGO_PATH | 5.40 |
| 5.55 | A:e16 COLLISION<br>A:e17 THROTTLE_END<br>A:e18 BRAKE_START<br>A:e19 CLOSING_START track_001<br>A:e20 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: IN_EGO_PATH | 5.50 |
| 5.60 | A:e21 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH | 5.50 |
| 5.75 | A:e22 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH | 5.70 |
| 6.60 | A:e23 COLLISION<br>A:e24 CLOSING_END track_001<br>A:e25 CLOSING_END track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: CLOSING, IN_EGO_PATH | 6.50 |
| 6.75 | A:e26 TRACK_LOST track_002 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track_002: IN_EGO_PATH | 6.70 |
| 6.85 | A:e27 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT<br>track lost, states UNKNOWN: track_002 | 6.80 |
| 7.00 | A:e28 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 6.90 |
| 7.45 | A:e29 MOVING_END<br>A:e30 STOP_START<br>A:e31 BRAKE_START | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 7.40 |

## States still active when observation ended

- EGO_PATH of track_002, since A:e14 (t = 5.40 s); the track was lost at 6.75 s
- EGO_PATH of track_001, since A:e22 (t = 5.75 s)
- STOP, since A:e30 (t = 7.45 s)
- BRAKE, since A:e31 (t = 7.45 s)

## Tracks lost

- track_002 at 6.75 s (A:e26): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 5.20 <= CUT_IN_FROM_LEFT_START 5.45 (+0.25 s); EGO_PATH_ENTRY 5.75 after critical TTC (+0.55 s)
- track_002: EGO_PATH_ENTRY 5.40, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.95 | 240 | 14.0 m / -10 deg | 0.05 m (11.95) | 0.1 m / -1 deg | 9.2 m/s |
| track_002 | 0.05 | 6.75 | 134 | 17.5 m / -8 deg | 3.49 m (6.60) | 3.5 m / +4 deg | 9.4 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.05 s: A observed track_002 start closing in (already the case when first observed).
- t = 3.95 s: A released the accelerator.
- t = 3.95 s: A started braking.
- t = 4.45 s: A observed track_001 stop closing in.
- t = 4.45 s: A observed track_002 stop closing in.
- t = 4.55 s: A released the brake.
- t = 4.65 s: A pressed the accelerator.
- t = 5.20 s: A's time-to-contact with track_001 became critical.
- t = 5.40 s: A observed track_002 enter its forward path corridor.
- t = 5.45 s: A observed track_001 cutting in from the left.
- t = 5.55 s: A's collision sensor recorded a contact (peak impulse 4244 N*s).
- t = 5.55 s: A released the accelerator.
- t = 5.55 s: A started braking.
- t = 5.55 s: A observed track_001 start closing in.
- t = 5.55 s: A observed track_002 start closing in.
- t = 5.60 s: A released the brake.
- t = 5.75 s: A observed track_001 enter its forward path corridor.
- t = 6.60 s: A's collision sensor recorded a contact (peak impulse 322 N*s).
- t = 6.60 s: A observed track_001 stop closing in.
- t = 6.60 s: A observed track_002 stop closing in.
- t = 6.75 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.85 s: A observed track_001's cut-in from the left settle.
- t = 7.00 s: A's time-to-contact with track_001 stopped being critical.
- t = 7.45 s: A stopped moving.
- t = 7.45 s: A came to a stop.
- t = 7.45 s: A started braking.
