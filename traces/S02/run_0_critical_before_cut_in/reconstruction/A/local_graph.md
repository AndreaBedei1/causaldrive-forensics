# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 50.8344409391284 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 37 (PRECEDES 30, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.15 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e04 | 0.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 2.45 | THROTTLE_END | A | - | controls |  |
| A:e06 | 2.45 | BRAKE_START | A | - | controls |  |
| A:e07 | 2.65 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 2.95 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e09 | 3.25 | BRAKE_END | A | - | controls |  |
| A:e10 | 3.35 | THROTTLE_START | A | - | controls |  |
| A:e11 | 3.65 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e12 | 4.10 | COLLISION | A | - | collision_sensor | peak_impulse=604.48 |
| A:e13 | 4.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e14 | 4.15 | CLOSING_END | A | track_001 | radar |  |
| A:e15 | 4.15 | THROTTLE_END | A | - | controls |  |
| A:e16 | 4.15 | BRAKE_START | A | - | controls |  |
| A:e17 | 4.65 | MOVING_END | A | - | ego |  |
| A:e18 | 4.65 | STOP_START | A | - | ego |  |
| A:e19 | 4.90 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
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
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e19
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e08
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e03 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 0.15 | A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 0.10 |
| 2.45 | A:e05 THROTTLE_END<br>A:e06 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING | 2.40 |
| 2.65 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING | 2.60 |
| 2.95 | A:e08 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC | 2.90 |
| 3.25 | A:e09 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.20 |
| 3.35 | A:e10 THROTTLE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.30 |
| 3.65 | A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.60 |
| 4.10 | A:e12 COLLISION<br>A:e13 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 4.15 | A:e14 CLOSING_END track_001<br>A:e15 THROTTLE_END<br>A:e16 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.10 |
| 4.65 | A:e17 MOVING_END<br>A:e18 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.60 |
| 4.90 | A:e19 CUT_IN_FROM_LEFT_END track_001 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.80 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e11 (t = 3.65 s)
- BRAKE, since A:e16 (t = 4.15 s)
- STOP, since A:e18 (t = 4.65 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 2.65 <= CUT_IN_FROM_LEFT_START 2.95 (+0.30 s); EGO_PATH_ENTRY 3.65 after critical TTC (+1.00 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.15 | 11.45 | 227 | 23.9 m / -6 deg | 0.53 m (4.95) | 0.7 m / -12 deg | 7.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.15 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 2.45 s: A released the accelerator.
- t = 2.45 s: A started braking.
- t = 2.65 s: A's time-to-contact with track_001 became critical.
- t = 2.95 s: A observed track_001 cutting in from the left.
- t = 3.25 s: A released the brake.
- t = 3.35 s: A pressed the accelerator.
- t = 3.65 s: A observed track_001 enter its forward path corridor.
- t = 4.10 s: A's collision sensor recorded a contact (peak impulse 604 N*s).
- t = 4.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.15 s: A observed track_001 stop closing in.
- t = 4.15 s: A released the accelerator.
- t = 4.15 s: A started braking.
- t = 4.65 s: A stopped moving.
- t = 4.65 s: A came to a stop.
- t = 4.90 s: A observed track_001's cut-in from the left settle.
