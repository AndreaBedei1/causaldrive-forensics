# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 207.26394240558147 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 143 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.15 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 19; edges: 33 (PRECEDES 22, SAME_TRACK 11)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | TRACK_APPEARED_FRONT | A | track_001 | radar |  |
| A:e03 | 0.45 | CLOSING_START | A | track_001 | radar |  |
| A:e04 | 1.05 | TRACK_APPEARED_FRONT | A | track_002 | radar |  |
| A:e05 | 1.05 | CLOSING_START | A | track_002 | radar | active_at_first_observation=True |
| A:e06 | 1.65 | CLOSING_END | A | track_001 | radar |  |
| A:e07 | 2.00 | CLOSING_END | A | track_002 | radar |  |
| A:e08 | 3.25 | CLOSING_START | A | track_002 | radar |  |
| A:e09 | 3.55 | TRACK_LOST | A | track_002 | radar |  |
| A:e10 | 3.90 | CLOSING_START | A | track_001 | radar |  |
| A:e11 | 4.60 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e12 | 5.70 | COLLISION | A | - | collision_sensor | peak_impulse=31406.82 |
| A:e13 | 5.70 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e14 | 5.70 | CLOSING_END | A | track_001 | radar |  |
| A:e15 | 5.75 | BRAKE_START | A | - | controls |  |
| A:e16 | 5.85 | MOVING_END | A | - | ego |  |
| A:e17 | 5.85 | STOP_START | A | - | ego |  |
| A:e18 | 13.75 | TRACK_APPEARED_FRONT | A | track_003 | radar |  |
| A:e19 | 14.10 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e03
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
    A:e11 --PRECEDES--> A:e13
    A:e11 --PRECEDES--> A:e14
    A:e12 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e15
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e15 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e18
    A:e18 --PRECEDES--> A:e19
    A:e02 --SAME_TRACK--> A:e03
    A:e04 --SAME_TRACK--> A:e05
    A:e02 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e04 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e02 --SAME_TRACK--> A:e10
    A:e02 --SAME_TRACK--> A:e11
    A:e02 --SAME_TRACK--> A:e13
    A:e02 --SAME_TRACK--> A:e14
    A:e18 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 TRACK_APPEARED_FRONT track_001 | ego: not yet observed | - |
| 0.45 | A:e03 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH | 0.40 |
| 1.05 | A:e04 TRACK_APPEARED_FRONT track_002<br>A:e05 CLOSING_START track_002 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH | 1.00 |
| 1.65 | A:e06 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 1.60 |
| 2.00 | A:e07 CLOSING_END track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 1.90 |
| 3.25 | A:e08 CLOSING_START track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: IN_EGO_PATH | 3.20 |
| 3.55 | A:e09 TRACK_LOST track_002 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track_002: CLOSING, IN_EGO_PATH | 3.50 |
| 3.90 | A:e10 CLOSING_START track_001 | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 3.80 |
| 4.60 | A:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 4.50 |
| 5.70 | A:e12 COLLISION<br>A:e13 CRITICAL_TTC_END track_001<br>A:e14 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 5.60 |
| 5.75 | A:e15 BRAKE_START | ego: MOVING<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 5.70 |
| 5.85 | A:e16 MOVING_END<br>A:e17 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 5.80 |
| 13.75 | A:e18 TRACK_APPEARED_FRONT track_003 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track lost, states UNKNOWN: track_002 | 13.70 |
| 14.10 | A:e19 TRACK_LOST track_003 | ego: STOP, BRAKE<br>track_001: IN_EGO_PATH<br>track_003: IN_EGO_PATH, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track lost, states UNKNOWN: track_002 | 14.00 |

## States still active when observation ended

- CLOSING of track_002, since A:e08 (t = 3.25 s); the track was lost at 3.55 s
- BRAKE, since A:e15 (t = 5.75 s)
- STOP, since A:e17 (t = 5.85 s)

## Tracks lost

- track_002 at 3.55 s (A:e09): CLOSING, IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- track_003 at 14.10 s (A:e19): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.60, COLLISION 5.70 (+1.10 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 14.15 | 284 | 21.9 m / +0 deg | 3.08 m (5.65) | 3.7 m / +1 deg | 13.9 m/s |
| track_002 | 1.05 | 3.55 | 43 | 46.4 m / +0 deg | 43.45 m (2.00) | 43.5 m / +0 deg | 14.3 m/s |
| track_003 | 13.75 | 14.10 | 8 | 17.8 m / +0 deg | 17.81 m (13.75) | 18.6 m / +1 deg | 3.7 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_001, which appeared in front of it.
- t = 0.45 s: A observed track_001 start closing in.
- t = 1.05 s: A's radar started tracking track_002, which appeared in front of it.
- t = 1.05 s: A observed track_002 start closing in (already the case when first observed).
- t = 1.65 s: A observed track_001 stop closing in.
- t = 2.00 s: A observed track_002 stop closing in.
- t = 3.25 s: A observed track_002 start closing in.
- t = 3.55 s: A's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 3.90 s: A observed track_001 start closing in.
- t = 4.60 s: A's time-to-contact with track_001 became critical.
- t = 5.70 s: A's collision sensor recorded a contact (peak impulse 31407 N*s).
- t = 5.70 s: A's time-to-contact with track_001 stopped being critical.
- t = 5.70 s: A observed track_001 stop closing in.
- t = 5.75 s: A started braking.
- t = 5.85 s: A stopped moving.
- t = 5.85 s: A came to a stop.
- t = 13.75 s: A's radar started tracking track_003, which appeared in front of it.
- t = 14.10 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
