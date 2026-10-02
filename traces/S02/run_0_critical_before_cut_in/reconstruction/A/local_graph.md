# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 93.72970312461257 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 14; edges: 26 (PRECEDES 20, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_LEFT | A | track_001 | radar |  |
| A:e03 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 0.80 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 2.45 | BRAKE_START | A | - | controls |  |
| A:e06 | 2.60 | CUT_IN_FROM_LEFT_START | A | track_001 | radar |  |
| A:e07 | 3.20 | BRAKE_END | A | - | controls |  |
| A:e08 | 3.90 | COLLISION | A | - | collision_sensor | peak_impulse=406.35 |
| A:e09 | 3.90 | CUT_IN_FROM_LEFT_END | A | track_001 | radar |  |
| A:e10 | 3.95 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e11 | 3.95 | CLOSING_END | A | track_001 | radar |  |
| A:e12 | 3.95 | BRAKE_START | A | - | controls |  |
| A:e13 | 4.45 | MOVING_END | A | - | ego |  |
| A:e14 | 4.45 | STOP_START | A | - | ego |  |

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
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e08 --PRECEDES--> A:e11
    A:e08 --PRECEDES--> A:e12
    A:e09 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e09 --PRECEDES--> A:e12
    A:e10 --PRECEDES--> A:e13
    A:e10 --PRECEDES--> A:e14
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e13
    A:e12 --PRECEDES--> A:e14
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e06
    A:e02 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_LEFT track_001<br>A:e03 CLOSING_START track_001 | ego: not yet observed | - |
| 0.80 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 0.70 |
| 2.45 | A:e05 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 2.40 |
| 2.60 | A:e06 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC | 2.50 |
| 3.20 | A:e07 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.10 |
| 3.90 | A:e08 COLLISION<br>A:e09 CUT_IN_FROM_LEFT_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 3.80 |
| 3.95 | A:e10 CRITICAL_TTC_END track_001<br>A:e11 CLOSING_END track_001<br>A:e12 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 3.90 |
| 4.45 | A:e13 MOVING_END<br>A:e14 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 4.40 |

## States still active when observation ended

- BRAKE, since A:e12 (t = 3.95 s)
- STOP, since A:e14 (t = 4.45 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 0.80 <= CUT_IN_FROM_LEFT_START 2.60 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 11.45 | 229 | 27.2 m / -6 deg | 1.72 m (4.50) | 2.0 m / -70 deg | 6.4 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.80 s: A's time-to-contact with track_001 became critical.
- t = 2.45 s: A started braking.
- t = 2.60 s: A observed track_001 cutting in from the left.
- t = 3.20 s: A released the brake.
- t = 3.90 s: A's collision sensor recorded a contact (peak impulse 406 N*s).
- t = 3.90 s: A observed track_001's cut-in from the left settle.
- t = 3.95 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.95 s: A observed track_001 stop closing in.
- t = 3.95 s: A started braking.
- t = 4.45 s: A stopped moving.
- t = 4.45 s: A came to a stop.
