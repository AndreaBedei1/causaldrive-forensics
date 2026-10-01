# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 12.814889293164015 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 15; edges: 21 (PRECEDES 14, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 0.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 1.25 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e06 | 1.55 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 2.45 | BRAKE_START | A | - | controls |  |
| A:e08 | 2.70 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e09 | 3.20 | BRAKE_END | A | - | controls |  |
| A:e10 | 3.40 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e11 | 3.70 | TRACK_LOST | A | track_001 | radar |  |
| A:e12 | 3.85 | COLLISION | A | - | collision_sensor | peak_impulse=241.17 |
| A:e13 | 3.90 | BRAKE_START | A | - | controls |  |
| A:e14 | 4.45 | MOVING_END | A | - | ego |  |
| A:e15 | 4.45 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
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
    A:e13 --PRECEDES--> A:e15
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 0.75 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 0.70 |
| 1.25 | A:e05 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 1.20 |
| 1.55 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 1.50 |
| 2.45 | A:e07 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 2.40 |
| 2.70 | A:e08 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC | 2.60 |
| 3.20 | A:e09 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.10 |
| 3.40 | A:e10 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.30 |
| 3.70 | A:e11 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 3.60 |
| 3.85 | A:e12 COLLISION | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 3.80 |
| 3.90 | A:e13 BRAKE_START | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 3.80 |
| 4.45 | A:e14 MOVING_END<br>A:e15 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 | 4.40 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 3.70 s
- CRITICAL_TTC of track_001, since A:e06 (t = 1.55 s); the track was lost at 3.70 s
- CUT_IN_FROM_LEFT of track_001, since A:e08 (t = 2.70 s); the track was lost at 3.70 s
- EGO_PATH of track_001, since A:e10 (t = 3.40 s); the track was lost at 3.70 s
- BRAKE, since A:e13 (t = 3.90 s)
- STOP, since A:e15 (t = 4.45 s)

## Tracks lost

- track_001 at 3.70 s (A:e11): CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 1.55 <= CUT_IN_FROM_LEFT_START 2.70 (+1.15 s); EGO_PATH_ENTRY 3.40 after critical TTC (+1.85 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 3.70 | 72 | 24.1 m / -8 deg | 0.92 m (3.70) | 0.9 m / -74 deg | 7.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.75 s: A's time-to-contact with track_001 became critical.
- t = 1.25 s: A's time-to-contact with track_001 stopped being critical.
- t = 1.55 s: A's time-to-contact with track_001 became critical.
- t = 2.45 s: A started braking.
- t = 2.70 s: A observed track_001 cutting in from the left.
- t = 3.20 s: A released the brake.
- t = 3.40 s: A observed track_001 enter its forward path corridor.
- t = 3.70 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.85 s: A's collision sensor recorded a contact (peak impulse 241 N*s).
- t = 3.90 s: A started braking.
- t = 4.45 s: A stopped moving.
- t = 4.45 s: A came to a stop.
