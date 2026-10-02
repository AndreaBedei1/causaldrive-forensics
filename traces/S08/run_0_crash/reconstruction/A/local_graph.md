# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 248.77736597135663 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 27 (PRECEDES 18, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.05 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.05 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e04 | 1.25 | TRACK_APPEARED_RIGHT | A | track_002 | radar |  |
| A:e05 | 1.25 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 2.20 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e07 | 2.45 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e08 | 2.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e09 | 3.50 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e10 | 4.20 | TRACK_LOST | A | track_002 | radar |  |
| A:e11 | 4.25 | COLLISION | A | - | collision_sensor | peak_impulse=12077.22 |
| A:e12 | 4.30 | BRAKE_START | A | - | controls |  |
| A:e13 | 4.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e14 | 4.90 | CLOSING_END | A | track_001 | radar |  |
| A:e15 | 4.90 | MOVING_END | A | - | ego |  |
| A:e16 | 4.90 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e02
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e06
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
    A:e13 --PRECEDES--> A:e16
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e02 --SAME_TRACK--> A:e08
    A:e02 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e14
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START | ego: not yet observed | - |
| 0.05 | A:e02 TRACK_APPEARED_FRONT track_001<br>A:e03 CLOSING_START track_001 | ego: MOVING | 0.00 |
| 1.25 | A:e04 TRACK_APPEARED_RIGHT track_002<br>A:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING | 1.20 |
| 2.20 | A:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING | 2.10 |
| 2.45 | A:e07 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING | 2.40 |
| 2.75 | A:e08 CRITICAL_TTC_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 2.70 |
| 3.50 | A:e09 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>track_002: CLOSING, CRITICAL_TTC | 3.40 |
| 4.20 | A:e10 TRACK_LOST track_002 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC | 4.10 |
| 4.25 | A:e11 COLLISION | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 | 4.20 |
| 4.30 | A:e12 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 | 4.20 |
| 4.75 | A:e13 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>track lost, states UNKNOWN: track_002 | 4.70 |
| 4.90 | A:e14 CLOSING_END track_001<br>A:e15 MOVING_END<br>A:e16 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING<br>track lost, states UNKNOWN: track_002 | 4.80 |

## States still active when observation ended

- CLOSING of track_002, since A:e05 (t = 1.25 s); the track was lost at 4.20 s
- CRITICAL_TTC of track_002, since A:e07 (t = 2.45 s); the track was lost at 4.20 s
- BRAKE, since A:e12 (t = 4.30 s)
- STOP, since A:e16 (t = 4.90 s)

## Tracks lost

- track_002 at 4.20 s (A:e10): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 2.20, COLLISION 4.25 (+2.05 s)
- track_002: CRITICAL_TTC_START 2.45, COLLISION 4.25 (+1.80 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.05 | 15.15 | 284 | 76.3 m / -3 deg | 9.91 m (12.50) | 10.0 m / -18 deg | 8.9 m/s |
| track_002 | 1.25 | 4.20 | 50 | 45.7 m / +52 deg | 3.05 m (4.20) | 3.0 m / +69 deg | 12.9 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.05 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.05 s: A observed track_001 start closing in (already the case when first observed).
- t = 1.25 s: A's radar started tracking track_002, which appeared on its right.
- t = 1.25 s: A observed track_002 start closing in (already the case when first observed).
- t = 2.20 s: A's time-to-contact with track_001 became critical.
- t = 2.45 s: A's time-to-contact with track_002 became critical.
- t = 2.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 3.50 s: A's time-to-contact with track_001 became critical.
- t = 4.20 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.25 s: A's collision sensor recorded a contact (peak impulse 12077 N*s).
- t = 4.30 s: A started braking.
- t = 4.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.90 s: A observed track_001 stop closing in.
- t = 4.90 s: A stopped moving.
- t = 4.90 s: A came to a stop.
