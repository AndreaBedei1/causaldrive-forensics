# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 23.313608441501856 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 12; edges: 16 (PRECEDES 12, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TURN_LEFT_START | A | - | ego | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e04 | 0.00 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.00 | CRITICAL_TTC_START | A | track_001 | radar | active_at_first_observation=True |
| A:e06 | 1.65 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e07 | 1.80 | COLLISION | A | - | collision_sensor | peak_impulse=1247.19 |
| A:e08 | 1.80 | CLOSING_END | A | track_001 | radar |  |
| A:e09 | 1.85 | BRAKE_START | A | - | controls |  |
| A:e10 | 2.45 | TURN_LEFT_END | A | - | ego |  |
| A:e11 | 2.50 | MOVING_END | A | - | ego |  |
| A:e12 | 2.50 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e06
    A:e02 --PRECEDES--> A:e06
    A:e03 --PRECEDES--> A:e06
    A:e04 --PRECEDES--> A:e06
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e06 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e09
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e12
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e05
    A:e03 --SAME_TRACK--> A:e06
    A:e03 --SAME_TRACK--> A:e08
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TURN_LEFT_START<br>A:e03 TRACK_APPEARED_RIGHT track_001<br>A:e04 CLOSING_START track_001<br>A:e05 CRITICAL_TTC_START track_001 | ego: not yet observed | - |
| 1.65 | A:e06 CRITICAL_TTC_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC | 1.60 |
| 1.80 | A:e07 COLLISION<br>A:e08 CLOSING_END track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING | 1.70 |
| 1.85 | A:e09 BRAKE_START | ego: MOVING, TURN_LEFT<br>track_001: no active state | 1.80 |
| 2.45 | A:e10 TURN_LEFT_END | ego: MOVING, BRAKE, TURN_LEFT<br>track_001: no active state | 2.40 |
| 2.50 | A:e11 MOVING_END<br>A:e12 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state | 2.40 |

## States still active when observation ended

- BRAKE, since A:e09 (t = 1.85 s)
- STOP, since A:e12 (t = 2.50 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 0.00, COLLISION 1.80 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.95 | 300 | 10.5 m / +30 deg | 2.23 m (2.35) | 2.5 m / +50 deg | 7.8 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A started turning left (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.00 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.00 s: A's time-to-contact with track_001 became critical (already the case when first observed).
- t = 1.65 s: A's time-to-contact with track_001 stopped being critical.
- t = 1.80 s: A's collision sensor recorded a contact (peak impulse 1247 N*s).
- t = 1.80 s: A observed track_001 stop closing in.
- t = 1.85 s: A started braking.
- t = 2.45 s: A stopped turning left.
- t = 2.50 s: A stopped moving.
- t = 2.50 s: A came to a stop.
