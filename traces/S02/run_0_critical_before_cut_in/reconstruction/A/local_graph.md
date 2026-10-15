# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 13.522847969084978 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 21; edges: 37 (PRECEDES 30, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.15 | TRACK_APPEARED_LEFT | A | track_001 | radar | initial_in_ego_path=False |
| A:e04 | 0.15 | CLOSING_START | A | track_001 | radar | active_at_first_observation=True |
| A:e05 | 0.25 | INDICATOR_LEFT_START | A | - | lights |  |
| A:e06 | 1.45 | INDICATOR_LEFT_END | A | - | lights |  |
| A:e07 | 1.95 | CUT_IN_FROM_LEFT_START | A | track_001 | radar | geometry=estimated_body |
| A:e08 | 2.30 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e09 | 2.45 | THROTTLE_END | A | - | controls |  |
| A:e10 | 2.45 | BRAKE_START | A | - | controls |  |
| A:e11 | 2.90 | EGO_PATH_ENTRY | A | track_001 | radar | occupancy_evidence=box; occupancy_margin_m=0.46; occupancy_sigma_m=0.27; cause=TARGET_LATERAL; geometry=estimated_body |
| A:e12 | 3.25 | BRAKE_END | A | - | controls |  |
| A:e13 | 3.35 | THROTTLE_START | A | - | controls |  |
| A:e14 | 4.10 | COLLISION | A | - | collision_sensor | peak_impulse=937.49 |
| A:e15 | 4.10 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e16 | 4.10 | CLOSING_END | A | track_001 | radar |  |
| A:e17 | 4.15 | THROTTLE_END | A | - | controls |  |
| A:e18 | 4.15 | BRAKE_START | A | - | controls |  |
| A:e19 | 4.65 | CUT_IN_FROM_LEFT_END | A | track_001 | radar | geometry=estimated_body |
| A:e20 | 4.65 | MOVING_END | A | - | ego |  |
| A:e21 | 4.65 | STOP_START | A | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e03
    A:e01 --PRECEDES--> A:e04
    A:e02 --PRECEDES--> A:e03
    A:e02 --PRECEDES--> A:e04
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e08 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e11
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e13 --PRECEDES--> A:e15
    A:e13 --PRECEDES--> A:e16
    A:e14 --PRECEDES--> A:e17
    A:e14 --PRECEDES--> A:e18
    A:e15 --PRECEDES--> A:e17
    A:e15 --PRECEDES--> A:e18
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e17 --PRECEDES--> A:e21
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e21
    A:e03 --SAME_TRACK--> A:e04
    A:e03 --SAME_TRACK--> A:e07
    A:e03 --SAME_TRACK--> A:e08
    A:e03 --SAME_TRACK--> A:e11
    A:e03 --SAME_TRACK--> A:e15
    A:e03 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e19
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START | ego: not yet observed | - |
| 0.15 | A:e03 TRACK_APPEARED_LEFT track_001<br>A:e04 CLOSING_START track_001 | ego: MOVING, THROTTLE | 0.10 |
| 0.25 | A:e05 INDICATOR_LEFT_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC? | 0.20 |
| 1.45 | A:e06 INDICATOR_LEFT_END | ego: MOVING, THROTTLE, INDICATOR_LEFT<br>track_001: CLOSING | 1.40 |
| 1.95 | A:e07 CUT_IN_FROM_LEFT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING | 1.90 |
| 2.30 | A:e08 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CUT_IN_FROM_LEFT | 2.20 |
| 2.45 | A:e09 THROTTLE_END<br>A:e10 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 2.40 |
| 2.90 | A:e11 EGO_PATH_ENTRY track_001 | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, CUT_IN_FROM_LEFT | 2.80 |
| 3.25 | A:e12 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 3.20 |
| 3.35 | A:e13 THROTTLE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 3.30 |
| 4.10 | A:e14 COLLISION<br>A:e15 CRITICAL_TTC_END track_001<br>A:e16 CLOSING_END track_001 | ego: MOVING, THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.00 |
| 4.15 | A:e17 THROTTLE_END<br>A:e18 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.10 |
| 4.65 | A:e19 CUT_IN_FROM_LEFT_END track_001<br>A:e20 MOVING_END<br>A:e21 STOP_START | ego: MOVING, BRAKE<br>track_001: IN_EGO_PATH, CUT_IN_FROM_LEFT | 4.60 |

## States still active when observation ended

- EGO_PATH of track_001, since A:e11 (t = 2.90 s)
- BRAKE, since A:e18 (t = 4.15 s)
- STOP, since A:e21 (t = 4.65 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: cut-in started before critical TTC: CUT_IN_FROM_LEFT_START 1.95 < CRITICAL_TTC_START 2.30 (+0.35 s) < COLLISION 4.10 (+1.80 s); EGO_PATH_ENTRY 2.90 after critical TTC (+0.60 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.15 | 11.45 | 227 | 24.1 m / -6 deg | 0.69 m (5.65) | 0.7 m / -13 deg | 7.2 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.15 s: A's radar started tracking track_001, which appeared on its left.
- t = 0.15 s: A observed track_001 start closing in (already the case when first observed).
- t = 0.25 s: A switched on its left turn indicator.
- t = 1.45 s: A switched off its left turn indicator.
- t = 1.95 s: A observed track_001 cutting in from the left.
- t = 2.30 s: A's time-to-contact with track_001 became critical.
- t = 2.45 s: A released the accelerator.
- t = 2.45 s: A started braking.
- t = 2.90 s: A observed track_001 enter its forward path corridor.
- t = 3.25 s: A released the brake.
- t = 3.35 s: A pressed the accelerator.
- t = 4.10 s: A's collision sensor recorded a contact (peak impulse 937 N*s).
- t = 4.10 s: A's time-to-contact with track_001 stopped being critical.
- t = 4.10 s: A observed track_001 stop closing in.
- t = 4.15 s: A released the accelerator.
- t = 4.15 s: A started braking.
- t = 4.65 s: A observed track_001's cut-in from the left settle.
- t = 4.65 s: A stopped moving.
- t = 4.65 s: A came to a stop.
