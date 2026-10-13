# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 1771.4966107942164 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 25 (PRECEDES 18, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.25 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e04 | 0.25 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 1.45 | CUT_IN_FROM_LEFT_START | A | track_001 | radar | geometry=estimated_body |
| A:e06 | 1.80 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e07 | 1.90 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 4.45 | THROTTLE_END | A | - | controls |  |
| A:e09 | 4.45 | BRAKE_START | A | - | controls |  |
| A:e10 | 5.15 | CUT_IN_FROM_LEFT_END | A | track_001 | radar | geometry=estimated_body |
| A:e11 | 5.30 | COLLISION | A | - | collision_sensor | peak_impulse=2460.67 |
| A:e12 | 5.30 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e13 | 5.45 | CLOSING_END | A | track_001 | radar |  |
| A:e14 | 5.65 | MOVING_END | A | - | ego |  |
| A:e15 | 5.65 | STOP_START | A | - | ego |  |

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
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e10
    A:e03 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 0.25 | A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 0.20 |
| 1.45 | A:e05 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 1.40 |
| 1.80 | A:e06 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 1.70 |
| 1.90 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, IN_EGO_PATH, CUT_IN_FROM_LEFT | 1.80 |
| 4.45 | A:e08 THROTTLE_END<br>A:e09 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.40 |
| 5.15 | A:e10 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 5.10 |
| 5.30 | A:e11 COLLISION<br>A:e12 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.20 |
| 5.45 | A:e13 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, IN_EGO_PATH | 5.40 |
| 5.65 | A:e14 MOVING_END<br>A:e15 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 5.60 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e06 (t = 1.80 s)
- BRAKE, since A:e09 (t = 4.45 s)
- STOP, since A:e15 (t = 5.65 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 1.45 < CRITICAL_TTC_START 1.90 (+0.45 s) < COLLISION 5.30 (+3.40 s); EGO_PATH_ENTRY 1.80 before critical TTC (-0.10 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.25 | 15.15 | 294 | 28.9 m / -6 deg | 0.02 m (5.40) | 1.2 m / -1 deg | 9.0 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.25 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.25 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.45 s: A observed track_001 cutting in from the left.
- t = 1.80 s: A observed track_001 enter its forward path corridor.
- t = 1.90 s: A's time-to-contact with track_001 became critical.
- t = 4.45 s: A released the accelerator.
- t = 4.45 s: A started braking.
- t = 5.15 s: A observed track_001's cut-in from the left settle.
- t = 5.30 s: A's collision sensor recorded a contact (peak impulse 2461 N*s).
- t = 5.30 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.45 s: A observed track_001 stop closing in.
- t = 5.65 s: A stopped moving.
- t = 5.65 s: A came to a stop.
