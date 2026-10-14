# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 126.25217776373029 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 138 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.65 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 24 (PRECEDES 18, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.10 | TRACK_APPEARED_FRONT | A | track_001 | radar | initial_in_ego_path=True |
| A:e04 | 0.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 3.75 | EGO_PATH_EXIT | A | track_001 | radar | geometry=estimated_body |
| A:e06 | 3.85 | CLOSING_START | A | track_001 | radar |  |
| A:e07 | 5.25 | THROTTLE_END | A | - | controls |  |
| A:e08 | 5.25 | BRAKE_START | A | - | controls |  |
| A:e09 | 5.75 | EGO_PATH_ENTRY | A | track_001 | radar | geometry=estimated_body |
| A:e10 | 5.90 | COLLISION | A | - | collision_sensor | peak_impulse=22183.35 |
| A:e11 | 5.90 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e12 | 5.90 | CLOSING_END | A | track_001 | radar |  |
| A:e13 | 6.00 | MOVING_END | A | - | ego |  |
| A:e14 | 6.00 | STOP_START | A | - | ego |  |

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
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e09
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e12
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 0.10 | A:e03 TRACK_APPEARED_FRONT track_001 | ego: MOVING, THROTTLE | 0.00 |
| 0.60 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CRITICAL_TTC? | 0.50 |
| 3.75 | A:e05 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH | 3.70 |
| 3.85 | A:e06 CLOSING_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC | 3.80 |
| 5.25 | A:e07 THROTTLE_END<br>A:e08 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC | 5.20 |
| 5.75 | A:e09 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC | 5.70 |
| 5.90 | A:e10 COLLISION<br>A:e11 CRITICAL_TTC_END track_001<br>A:e12 CLOSING_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 5.80 |
| 6.00 | A:e13 MOVING_END<br>A:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 5.90 |

## States still active when observation ended

- BRAKE, since A:e08 (t = 5.25 s)
- EGO_PATH of track_001, since A:e09 (t = 5.75 s)
- STOP, since A:e14 (t = 6.00 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.60, COLLISION 5.90 (+5.30 s); EGO_PATH_ENTRY 5.75 after critical TTC (+5.15 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.10 | 13.65 | 271 | 19.4 m / +0 deg | 0.06 m (5.90) | 0.1 m / +0 deg | 13.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.10 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.60 s: A's time-to-contact with track_001 became critical.
- t = 3.75 s: A observed track_001 leave its forward path corridor.
- t = 3.85 s: A observed track_001 start closing in.
- t = 5.25 s: A released the accelerator.
- t = 5.25 s: A started braking.
- t = 5.75 s: A observed track_001 enter its forward path corridor.
- t = 5.90 s: A's collision sensor recorded a contact (peak impulse 22183 N*s).
- t = 5.90 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.90 s: A observed track_001 stop closing in.
- t = 6.00 s: A stopped moving.
- t = 6.00 s: A came to a stop.
