# Local graph - vehicle C

All times are C's own local clock: `t_local` = seconds since C's first ego sample (raw clock reading 144.63758319616318 at `t_local` = 0). Only files under `vehicles/C/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 4 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 38 (PRECEDES 28, SAME_TRACK 10)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| C:e01 | 0.00 | MOVING_START | C | - | ego | active_at_first_observation=True |
| C:e02 | 0.00 | THROTTLE_START | C | - | controls | active_at_first_observation=True |
| C:e03 | 0.00 | TRACK_APPEARED_FRONT | C | track_001#segment_1 | radar |  |
| C:e04 | 0.00 | CLOSING_START | C | track_001#segment_1 | radar | active_at_first_observation=True |
| C:e05 | 2.10 | TRACK_APPEARED_LEFT | C | track_002 | radar |  |
| C:e06 | 2.10 | CLOSING_START | C | track_002 | radar | active_at_first_observation=True |
| C:e07 | 2.35 | THROTTLE_END | C | - | controls |  |
| C:e08 | 2.35 | BRAKE_START | C | - | controls |  |
| C:e09 | 2.90 | MOVING_END | C | - | ego |  |
| C:e10 | 2.90 | STOP_START | C | - | ego |  |
| C:e11 | 3.65 | TRACK_LOST | C | track_001#segment_1 | radar |  |
| C:e12 | 3.70 | TRACK_APPEARED_LEFT | C | track_001#segment_2 | radar |  |
| C:e13 | 3.70 | CLOSING_START | C | track_001#segment_2 | radar | active_at_first_observation=True |
| C:e14 | 4.60 | CLOSING_END | C | track_001#segment_2 | radar |  |
| C:e15 | 4.65 | EGO_PATH_ENTRY | C | track_002 | radar |  |
| C:e16 | 4.75 | CLOSING_END | C | track_002 | radar |  |
| C:e17 | 5.05 | TRACK_LOST | C | track_001#segment_2 | radar |  |
| C:e18 | 5.10 | TRACK_APPEARED_LEFT | C | track_001#segment_3 | radar |  |
| C:e19 | 5.80 | TRACK_LOST | C | track_002 | radar |  |
| C:e20 | 6.25 | EGO_PATH_ENTRY | C | track_001#segment_3 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    C:e01 --PRECEDES--> C:e05
    C:e01 --PRECEDES--> C:e06
    C:e02 --PRECEDES--> C:e05
    C:e02 --PRECEDES--> C:e06
    C:e03 --PRECEDES--> C:e05
    C:e03 --PRECEDES--> C:e06
    C:e04 --PRECEDES--> C:e05
    C:e04 --PRECEDES--> C:e06
    C:e05 --PRECEDES--> C:e07
    C:e05 --PRECEDES--> C:e08
    C:e06 --PRECEDES--> C:e07
    C:e06 --PRECEDES--> C:e08
    C:e07 --PRECEDES--> C:e09
    C:e07 --PRECEDES--> C:e10
    C:e08 --PRECEDES--> C:e09
    C:e08 --PRECEDES--> C:e10
    C:e09 --PRECEDES--> C:e11
    C:e10 --PRECEDES--> C:e11
    C:e11 --PRECEDES--> C:e12
    C:e11 --PRECEDES--> C:e13
    C:e12 --PRECEDES--> C:e14
    C:e13 --PRECEDES--> C:e14
    C:e14 --PRECEDES--> C:e15
    C:e15 --PRECEDES--> C:e16
    C:e16 --PRECEDES--> C:e17
    C:e17 --PRECEDES--> C:e18
    C:e18 --PRECEDES--> C:e19
    C:e19 --PRECEDES--> C:e20
    C:e03 --SAME_TRACK--> C:e04
    C:e05 --SAME_TRACK--> C:e06
    C:e03 --SAME_TRACK--> C:e11
    C:e12 --SAME_TRACK--> C:e13
    C:e12 --SAME_TRACK--> C:e14
    C:e05 --SAME_TRACK--> C:e15
    C:e05 --SAME_TRACK--> C:e16
    C:e12 --SAME_TRACK--> C:e17
    C:e05 --SAME_TRACK--> C:e19
    C:e18 --SAME_TRACK--> C:e20
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | C:e01 MOVING_START<br>C:e02 THROTTLE_START<br>C:e03 TRACK_APPEARED_FRONT track_001#segment_1<br>C:e04 CLOSING_START track_001#segment_1 | ego: not yet observed | - |
| 2.10 | C:e05 TRACK_APPEARED_LEFT track_002<br>C:e06 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING | 2.00 |
| 2.35 | C:e07 THROTTLE_END<br>C:e08 BRAKE_START | ego: MOVING, THROTTLE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING, CRITICAL_TTC? | 2.30 |
| 2.90 | C:e09 MOVING_END<br>C:e10 STOP_START | ego: MOVING, BRAKE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING | 2.80 |
| 3.65 | C:e11 TRACK_LOST track_001#segment_1 | ego: STOP, BRAKE<br>track_001#segment_1: CLOSING<br>track_002: CLOSING | 3.60 |
| 3.70 | C:e12 TRACK_APPEARED_LEFT track_001#segment_2<br>C:e13 CLOSING_START track_001#segment_2 | ego: STOP, BRAKE<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 | 3.60 |
| 4.60 | C:e14 CLOSING_END track_001#segment_2 | ego: STOP, BRAKE<br>track_001#segment_2: CLOSING, CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 | 4.50 |
| 4.65 | C:e15 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING<br>track lost, states UNKNOWN: track_001#segment_1 | 4.60 |
| 4.75 | C:e16 CLOSING_END track_002 | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 4.70 |
| 5.05 | C:e17 TRACK_LOST track_001#segment_2 | ego: STOP, BRAKE<br>track_001#segment_2: CRITICAL_TTC?, IN_EGO_PATH?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1 | 5.00 |
| 5.10 | C:e18 TRACK_APPEARED_LEFT track_001#segment_3 | ego: STOP, BRAKE<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 | 5.00 |
| 5.80 | C:e19 TRACK_LOST track_002 | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track_002: IN_EGO_PATH<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2 | 5.70 |
| 6.25 | C:e20 EGO_PATH_ENTRY track_001#segment_3 | ego: STOP, BRAKE<br>track_001#segment_3: no active state<br>track lost, states UNKNOWN: track_001#segment_1, track_001#segment_2, track_002 | 6.20 |

## States still active when observation ended

- CLOSING of track_001#segment_1, since C:e04 (t = 0.00 s); the track was lost at 3.65 s
- BRAKE, since C:e08 (t = 2.35 s)
- STOP, since C:e10 (t = 2.90 s)
- EGO_PATH of track_002, since C:e15 (t = 4.65 s); the track was lost at 5.80 s
- EGO_PATH of track_001#segment_3, since C:e20 (t = 6.25 s)

## Tracks lost

- track_001#segment_1 at 3.65 s (C:e11): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- track_002 at 5.80 s (C:e19): IN_EGO_PATH were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_001#segment_2

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001#segment_3: EGO_PATH_ENTRY 6.25, no critical TTC
- track_002: EGO_PATH_ENTRY 4.65, no critical TTC

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001#segment_1 | 0.00 | 3.65 | 69 | 77.6 m / -3 deg | 16.70 m (3.65) | 16.7 m / -11 deg | 10.2 m/s |
| track_001#segment_2 | 3.70 | 5.05 | 28 | 16.2 m / -12 deg | 10.34 m (4.65) | 10.4 m / -25 deg | 10.7 m/s |
| track_001#segment_3 | 5.10 | 15.15 | 202 | 9.1 m / -21 deg | 8.84 m (15.15) | 8.8 m / -8 deg | 2.6 m/s |
| track_002 | 2.10 | 5.80 | 75 | 34.4 m / -59 deg | 8.48 m (4.85) | 8.5 m / -2 deg | 12.7 m/s |

Bearing: positive = to C's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: C started moving (already the case when first observed).
- t = 0.00 s: C pressed the accelerator (already the case when first observed).
- t = 0.00 s: C's radar started tracking track_001#segment_1, which appeared in front of it.
- t = 0.00 s: C observed track_001#segment_1 start closing in (already the case when first observed).
- t = 2.10 s: C's radar started tracking track_002, which appeared on its left.
- t = 2.10 s: C observed track_002 start closing in (already the case when first observed).
- t = 2.35 s: C released the accelerator.
- t = 2.35 s: C started braking.
- t = 2.90 s: C stopped moving.
- t = 2.90 s: C came to a stop.
- t = 3.65 s: C's radar lost track_001#segment_1 (its states are UNKNOWN from then on, not ended).
- t = 3.70 s: C's radar started tracking track_001#segment_2, which appeared on its left.
- t = 3.70 s: C observed track_001#segment_2 start closing in (already the case when first observed).
- t = 4.60 s: C observed track_001#segment_2 stop closing in.
- t = 4.65 s: C observed track_002 enter its forward path corridor.
- t = 4.75 s: C observed track_002 stop closing in.
- t = 5.05 s: C's radar lost track_001#segment_2 (its states are UNKNOWN from then on, not ended).
- t = 5.10 s: C's radar started tracking track_001#segment_3, which appeared on its left.
- t = 5.80 s: C's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 6.25 s: C observed track_001#segment_3 enter its forward path corridor.
