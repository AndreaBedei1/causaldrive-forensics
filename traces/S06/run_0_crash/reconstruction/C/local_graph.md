# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 144.63758319616318 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 33 (PRECEDES 26, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | THROTTLE_START | C | - | controls | active_at_first_observation=True |
| C:e03 | 0.10 | TRACK_APPEARED_LEFT | C | track_001 | radar | initial_in_ego_path=False |
| C:e04 | 0.10 | CLOSING_START | C | track_001 | radar | active_at_first_observation=True |
| C:e05 | 0.30 | TRACK_LOST | C | track_001 | radar |  |
| C:e06 | 0.40 | TRACK_APPEARED_LEFT | C | track_002 | radar | initial_in_ego_path=False |
| C:e07 | 0.40 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e08 | 2.10 | TRACK_APPEARED_LEFT | C | track_003 | radar | initial_in_ego_path=False |
| C:e09 | 2.10 | CLOSING_START | C | track_003 | radar | active_at_first_observation=True |
| C:e10 | 2.35 | THROTTLE_END | C | - | controls |  |
| C:e11 | 2.35 | BRAKE_START | C | - | controls |  |
| C:e12 | 2.90 | MOVING_END | C | - | ego |  |
| C:e13 | 2.90 | STOP_START | C | - | ego |  |
| C:e14 | 4.60 | CLOSING_END | C | track_003 | radar |  |
| C:e15 | 4.60 | EGO_PATH_ENTRY | C | track_003 | radar | geometry=estimated_body |
| C:e16 | 4.60 | TRACK_LOST | C | track_002 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e03
    C:e01 --PRECEDES--> C:e04
    C:e02 --PRECEDES--> C:e03
    C:e02 --PRECEDES--> C:e04
    C:e03 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e05
    C:e05 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e06 --PRECEDES--> C:e09
    C:e07 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e08 --PRECEDES--> C:e11
    C:e09 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e12
    C:e10 --PRECEDES--> C:e13
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e12 --PRECEDES--> C:e15
    C:e12 --PRECEDES--> C:e16
    C:e13 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e15
    C:e13 --PRECEDES--> C:e16
    C:e03 --SAME_TRACK--> C:e04
    C:e03 --SAME_TRACK--> C:e05
    C:e06 --SAME_TRACK--> C:e07
    C:e08 --SAME_TRACK--> C:e09
    C:e08 --SAME_TRACK--> C:e14
    C:e08 --SAME_TRACK--> C:e15
    C:e06 --SAME_TRACK--> C:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 THROTTLE_START | ego: not yet observed | - |
| 0.10 | C:e03 TRACK_APPEARED_LEFT track_001<br>C:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 0.00 |
| 0.30 | C:e05 TRACK_LOST track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 0.20 |
| 0.40 | C:e06 TRACK_APPEARED_LEFT track_002<br>C:e07 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track lost, states UNKNOWN: track_001 | 0.30 |
| 2.10 | C:e08 TRACK_APPEARED_LEFT track_003<br>C:e09 CLOSING_START track_003 | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001 | 2.00 |
| 2.35 | C:e10 THROTTLE_END<br>C:e11 BRAKE_START | ego: MOVING, THROTTLE<br>track_002: CLOSING<br>track_003: CLOSING, CRITICAL_TTC?<br>track lost, states UNKNOWN: track_001 | 2.30 |
| 2.90 | C:e12 MOVING_END<br>C:e13 STOP_START | ego: MOVING, BRAKE<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001 | 2.80 |
| 4.60 | C:e14 CLOSING_END track_003<br>C:e15 EGO_PATH_ENTRY track_003<br>C:e16 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_002: CLOSING<br>track_003: CLOSING<br>track lost, states UNKNOWN: track_001 | 4.50 |

## States still active when observation ended

- CLOSING of track_001, since C:e04 (t = 0.10 s); the track was lost at 0.30 s
- CLOSING of track_002, since C:e07 (t = 0.40 s); the track was lost at 4.60 s
- BRAKE, since C:e11 (t = 2.35 s)
- STOP, since C:e13 (t = 2.90 s)
- EGO_PATH of track_003, since C:e15 (t = 4.60 s)

## Tracks lost

- track_001 at 0.30 s (C:e05): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 4.60 s (C:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_003: EGO_PATH_ENTRY 4.60, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.10 | 0.30 | 5 | 75.6 m / -5 deg | 71.82 m (0.30) | 71.8 m / -7 deg | 10.2 m/s |
| track_002 | 0.40 | 4.60 | 80 | 70.0 m / -7 deg | 9.95 m (4.60) | 9.9 m / -27 deg | 10.7 m/s |
| track_003 | 2.10 | 15.15 | 262 | 34.3 m / -59 deg | 9.19 m (15.15) | 9.2 m / -13 deg | 12.5 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C pressed the accelerator (already the case when first observed).
- t = 0.10 s: C's radar started tracking track_001, which appeared on its left.
- t = 0.10 s: C observed track_001 start closing in (already the case when first observed).
- t = 0.30 s: C's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 0.40 s: C's radar started tracking track_002, which appeared on its left.
- t = 0.40 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.10 s: C's radar started tracking track_003, which appeared on its left.
- t = 2.10 s: C observed track_003 start closing in (already the case when first observed).
- t = 2.35 s: C released the accelerator.
- t = 2.35 s: C started braking.
- t = 2.90 s: C stopped moving.
- t = 2.90 s: C came to a stop.
- t = 4.60 s: C observed track_003 stop closing in.
- t = 4.60 s: C observed track_003 enter its forward path corridor.
- t = 4.60 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
