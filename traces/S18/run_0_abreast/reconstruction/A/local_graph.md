# Local graph - vehicle A

All times are A's own local clock: `t_local` = seconds since A's first ego sample (raw clock reading 482.42503720521927 at `t_local` = 0). Only files under `vehicles/A/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 116 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (11.45 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 46 (PRECEDES 30, SAME_TRACK 16)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| A:e01 | 0.00 | MOVING_START | A | - | ego | active_at_first_observation=True |
| A:e02 | 0.00 | THROTTLE_START | A | - | controls | active_at_first_observation=True |
| A:e03 | 0.00 | TRACK_APPEARED_LEFT | A | track_002 | radar |  |
| A:e04 | 0.00 | TRACK_APPEARED_RIGHT | A | track_001 | radar |  |
| A:e05 | 0.25 | TRACK_APPEARED_FRONT | A | track_003 | radar |  |
| A:e06 | 0.75 | EGO_PATH_EXIT | A | track_003 | radar |  |
| A:e07 | 2.05 | CRITICAL_TTC_START | A | track_001 | radar |  |
| A:e08 | 2.40 | CLOSING_START | A | track_003 | radar |  |
| A:e09 | 2.40 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar |  |
| A:e10 | 2.65 | EGO_PATH_ENTRY | A | track_001 | radar |  |
| A:e11 | 3.55 | CUT_IN_FROM_RIGHT_END | A | track_001 | radar |  |
| A:e12 | 4.20 | CLOSING_END | A | track_003 | radar |  |
| A:e13 | 5.15 | CRITICAL_TTC_START | A | track_002 | radar |  |
| A:e14 | 5.60 | CLOSING_START | A | track_002 | radar |  |
| A:e15 | 5.65 | EGO_PATH_EXIT | A | track_001 | radar |  |
| A:e16 | 5.75 | CRITICAL_TTC_END | A | track_001 | radar |  |
| A:e17 | 6.20 | COLLISION | A | - | collision_sensor | peak_impulse=1079.56; merged_bursts=[[6.3, 49.9]] |
| A:e18 | 6.20 | CRITICAL_TTC_END | A | track_002 | radar |  |
| A:e19 | 6.25 | THROTTLE_END | A | - | controls |  |
| A:e20 | 6.25 | BRAKE_START | A | - | controls |  |
| A:e21 | 6.40 | CLOSING_END | A | track_002 | radar |  |
| A:e22 | 7.35 | MOVING_END | A | - | ego |  |
| A:e23 | 7.35 | STOP_START | A | - | ego |  |
| A:e24 | 9.90 | CUT_IN_FROM_RIGHT_START | A | track_001 | radar |  |
| A:e25 | 10.20 | TRACK_LOST | A | track_001 | radar |  |
| A:e26 | 10.45 | TRACK_LOST | A | track_003 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    A:e01 --PRECEDES--> A:e05
    A:e02 --PRECEDES--> A:e05
    A:e03 --PRECEDES--> A:e05
    A:e04 --PRECEDES--> A:e05
    A:e05 --PRECEDES--> A:e06
    A:e06 --PRECEDES--> A:e07
    A:e07 --PRECEDES--> A:e08
    A:e07 --PRECEDES--> A:e09
    A:e08 --PRECEDES--> A:e10
    A:e09 --PRECEDES--> A:e10
    A:e10 --PRECEDES--> A:e11
    A:e11 --PRECEDES--> A:e12
    A:e12 --PRECEDES--> A:e13
    A:e13 --PRECEDES--> A:e14
    A:e14 --PRECEDES--> A:e15
    A:e15 --PRECEDES--> A:e16
    A:e16 --PRECEDES--> A:e17
    A:e16 --PRECEDES--> A:e18
    A:e17 --PRECEDES--> A:e19
    A:e17 --PRECEDES--> A:e20
    A:e18 --PRECEDES--> A:e19
    A:e18 --PRECEDES--> A:e20
    A:e19 --PRECEDES--> A:e21
    A:e20 --PRECEDES--> A:e21
    A:e21 --PRECEDES--> A:e22
    A:e21 --PRECEDES--> A:e23
    A:e22 --PRECEDES--> A:e24
    A:e23 --PRECEDES--> A:e24
    A:e24 --PRECEDES--> A:e25
    A:e25 --PRECEDES--> A:e26
    A:e05 --SAME_TRACK--> A:e06
    A:e04 --SAME_TRACK--> A:e07
    A:e05 --SAME_TRACK--> A:e08
    A:e04 --SAME_TRACK--> A:e09
    A:e04 --SAME_TRACK--> A:e10
    A:e04 --SAME_TRACK--> A:e11
    A:e05 --SAME_TRACK--> A:e12
    A:e03 --SAME_TRACK--> A:e13
    A:e03 --SAME_TRACK--> A:e14
    A:e04 --SAME_TRACK--> A:e15
    A:e04 --SAME_TRACK--> A:e16
    A:e03 --SAME_TRACK--> A:e18
    A:e03 --SAME_TRACK--> A:e21
    A:e04 --SAME_TRACK--> A:e24
    A:e04 --SAME_TRACK--> A:e25
    A:e05 --SAME_TRACK--> A:e26
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | A:e01 MOVING_START<br>A:e02 THROTTLE_START<br>A:e03 TRACK_APPEARED_LEFT track_002<br>A:e04 TRACK_APPEARED_RIGHT track_001 | ego: not yet observed | - |
| 0.25 | A:e05 TRACK_APPEARED_FRONT track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC?<br>track_002: CRITICAL_TTC? | 0.20 |
| 0.75 | A:e06 EGO_PATH_EXIT track_003 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: IN_EGO_PATH, CRITICAL_TTC? | 0.70 |
| 2.05 | A:e07 CRITICAL_TTC_START track_001 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state | 2.00 |
| 2.40 | A:e08 CLOSING_START track_003<br>A:e09 CUT_IN_FROM_RIGHT_START track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: no active state<br>track_003: no active state | 2.30 |
| 2.65 | A:e10 EGO_PATH_ENTRY track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: CLOSING | 2.60 |
| 3.55 | A:e11 CUT_IN_FROM_RIGHT_END track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH, CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: CLOSING | 3.50 |
| 4.20 | A:e12 CLOSING_END track_003 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: CLOSING | 4.10 |
| 5.15 | A:e13 CRITICAL_TTC_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: no active state<br>track_003: no active state | 5.10 |
| 5.60 | A:e14 CLOSING_START track_002 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CRITICAL_TTC<br>track_003: no active state | 5.50 |
| 5.65 | A:e15 EGO_PATH_EXIT track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC, IN_EGO_PATH<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state | 5.60 |
| 5.75 | A:e16 CRITICAL_TTC_END track_001 | ego: MOVING, THROTTLE<br>track_001: CRITICAL_TTC<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state | 5.70 |
| 6.20 | A:e17 COLLISION<br>A:e18 CRITICAL_TTC_END track_002 | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING, CRITICAL_TTC<br>track_003: no active state | 6.10 |
| 6.25 | A:e19 THROTTLE_END<br>A:e20 BRAKE_START | ego: MOVING, THROTTLE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state | 6.20 |
| 6.40 | A:e21 CLOSING_END track_002 | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: CLOSING<br>track_003: no active state | 6.30 |
| 7.35 | A:e22 MOVING_END<br>A:e23 STOP_START | ego: MOVING, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state | 7.30 |
| 9.90 | A:e24 CUT_IN_FROM_RIGHT_START track_001 | ego: STOP, BRAKE<br>track_001: no active state<br>track_002: no active state<br>track_003: no active state | 9.80 |
| 10.20 | A:e25 TRACK_LOST track_001 | ego: STOP, BRAKE<br>track_001: CUT_IN_FROM_RIGHT<br>track_002: no active state<br>track_003: no active state | 10.10 |
| 10.45 | A:e26 TRACK_LOST track_003 | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track lost, states UNKNOWN: track_001 | 10.40 |

## States still active when observation ended

- BRAKE, since A:e20 (t = 6.25 s)
- STOP, since A:e23 (t = 7.35 s)
- CUT_IN_FROM_RIGHT of track_001, since A:e24 (t = 9.90 s); the track was lost at 10.20 s

## Tracks lost

- track_001 at 10.20 s (A:e25): CUT_IN_FROM_RIGHT were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_003

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: critical TTC already active before the cut-in: CRITICAL_TTC_START 2.05 <= CUT_IN_FROM_RIGHT_START 2.40 (+0.35 s); EGO_PATH_ENTRY 2.65 after critical TTC (+0.60 s)
- track_002: CRITICAL_TTC_START 5.15, COLLISION 6.20 (+1.05 s)

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 0.00 | 10.20 | 192 | 15.8 m / +10 deg | 15.33 m (3.20) | 58.3 m / +3 deg | 14.4 m/s |
| track_002 | 0.00 | 11.45 | 230 | 5.5 m / -144 deg | 0.02 m (6.50) | 0.3 m / -90 deg | 12.9 m/s |
| track_003 | 0.25 | 10.45 | 171 | 18.1 m / +2 deg | 15.73 m (5.25) | 61.4 m / +6 deg | 14.3 m/s |

Bearing: positive = to A's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: A started moving (already the case when first observed).
- t = 0.00 s: A pressed the accelerator (already the case when first observed).
- t = 0.00 s: A's radar started tracking track_002, which appeared on its left.
- t = 0.00 s: A's radar started tracking track_001, which appeared on its right.
- t = 0.25 s: A's radar started tracking track_003, which appeared in front of it.
- t = 0.75 s: A observed track_003 leave its forward path corridor.
- t = 2.05 s: A's time-to-contact with track_001 became critical.
- t = 2.40 s: A observed track_003 start closing in.
- t = 2.40 s: A observed track_001 cutting in from the right.
- t = 2.65 s: A observed track_001 enter its forward path corridor.
- t = 3.55 s: A observed track_001's cut-in from the right settle.
- t = 4.20 s: A observed track_003 stop closing in.
- t = 5.15 s: A's time-to-contact with track_002 became critical.
- t = 5.60 s: A observed track_002 start closing in.
- t = 5.65 s: A observed track_001 leave its forward path corridor.
- t = 5.75 s: A's time-to-contact with track_001 stopped being critical.
- t = 6.20 s: A's collision sensor recorded a contact (peak impulse 1080 N*s).
- t = 6.20 s: A's time-to-contact with track_002 stopped being critical.
- t = 6.25 s: A released the accelerator.
- t = 6.25 s: A started braking.
- t = 6.40 s: A observed track_002 stop closing in.
- t = 7.35 s: A stopped moving.
- t = 7.35 s: A came to a stop.
- t = 9.90 s: A observed track_001 cutting in from the right.
- t = 10.20 s: A's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 10.45 s: A's radar lost track_003 (its states are UNKNOWN from then on, not ended).
