# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 324.2700144685805 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 12 (PRECEDES 9, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 2.95 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e03 | 2.95 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 3.75 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e05 | 5.45 | TRACK_LOST | A | track_001 | radar |  |
| A:e06 | 5.50 | COLLISION | A | - | collision_sensor | peak_impulse=8859.58 |
| A:e07 | 5.55 | BRAKE_START | A | - | controls |  |
| A:e08 | 6.05 | MOVING_END | A | - | ego |  |
| A:e09 | 6.05 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e04
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e02 --SAME_TRACK--> A:e03
    A:e02 --SAME_TRACK--> A:e04
    A:e02 --SAME_TRACK--> A:e05
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 2.95 | A:e02 TRACK_APPEARED_RIGHT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 2.90 |
| 3.75 | A:e04 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 3.70 |
| 5.45 | A:e05 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 5.40 |
| 5.50 | A:e06 COLLISION | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 5.40 |
| 5.55 | A:e07 BRAKE_START | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 5.50 |
| 6.05 | A:e08 MOVING_END<br>A:e09 STOP_START | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001 | 6.00 |

## States still active when observation ended

- CLOSING of track_001, since A:e03 (t = 2.95 s); the track was lost at 5.45 s
- CRITICAL_TTC of track_001, since A:e04 (t = 3.75 s); the track was lost at 5.45 s
- BRAKE, since A:e07 (t = 5.55 s)
- STOP, since A:e09 (t = 6.05 s)

## Tracks lost

- track_001 at 5.45 s (A:e05): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 3.75, COLLISION 5.50 (+1.75 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.95 | 5.45 | 48 | 32.7 m / +23 deg | 3.15 m (5.45) | 3.1 m / +40 deg | 5.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 2.95 s: A's radar started tracking track_001, which appeared on its right.
- t = 2.95 s: A observed track_001 start closing in (already the case when first observed).
- t = 3.75 s: A's time-to-contact with track_001 became critical.
- t = 5.45 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 5.50 s: A's collision sensor recorded a contact (peak impulse 8860 N*s).
- t = 5.55 s: A started braking.
- t = 6.05 s: A stopped moving.
- t = 6.05 s: A came to a stop.
