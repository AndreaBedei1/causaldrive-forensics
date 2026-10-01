# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 130.43641052767634 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 146 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 13; edges: 22 (PRECEDES 15, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 1.20 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e03 | 1.20 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.65 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 3.45 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e06 | 3.70 | COLLISION | A | - | collision_sensor | peak_impulse=6116.26 |
| A:e07 | 3.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e08 | 3.70 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 3.75 | BRAKE_START | A | - | controls |  |
| A:e10 | 3.90 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e11 | 4.05 | TRACK_LOST | A | track_001 | radar |  |
| A:e12 | 4.55 | MOVING_END | A | - | ego |  |
| A:e13 | 4.55 | STOP_START | A | - | ego |  |

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
    A:e05 --PRECEDES--> A:e08
    A:e06 --PRECEDES--> A:e09
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e11 --PRECEDES--> A:e13
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 1.20 | A:e02 TRACK_APPEARED_RIGHT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 1.10 |
| 1.65 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 1.60 |
| 3.45 | A:e05 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 3.40 |
| 3.70 | A:e06 COLLISION<br>A:e07 CRITICAL_TTC_END track_001<br>A:e08 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH | 3.60 |
| 3.75 | A:e09 BRAKE_START | ego: MOVING<br>track_001: IN_EGO_PATH | 3.70 |
| 3.90 | A:e10 EGO_PATH_EXIT track_001 | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH | 3.80 |
| 4.05 | A:e11 TRACK_LOST track_001 | ego: MOVING, BRAKE<br>track_001: no active state | 4.00 |
| 4.55 | A:e12 MOVING_END<br>A:e13 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 | 4.50 |

## States still active when observation ended

- BRAKE, since A:e09 (t = 3.75 s)
- STOP, since A:e13 (t = 4.55 s)

## Tracks lost

- lost with no state active: track_001

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 1.65, COLLISION 3.70 (+2.05 s); EGO_PATH_ENTRY 3.45 after critical TTC (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.20 | 4.05 | 57 | 37.1 m / +42 deg | 0.90 m (3.65) | 3.0 m / -107 deg | 11.5 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 1.20 s: A's radar started tracking track_001, which appeared on its right.
- t = 1.20 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.65 s: A's time-to-contact with track_001 became critical.
- t = 3.45 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A's collision sensor recorded a contact (peak impulse 6116 N*s).
- t = 3.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.70 s: A observed track_001 stop closing in.
- t = 3.75 s: A started braking.
- t = 3.90 s: A observed track_001 leave its forward path corridor.
- t = 4.05 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 4.55 s: A stopped moving.
- t = 4.55 s: A came to a stop.
