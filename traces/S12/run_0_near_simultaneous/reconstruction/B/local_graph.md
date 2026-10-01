# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 411.87760305032134 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 151 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (14.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 32; edges: 64 (PRECEDES 55, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=True |
| B:e05 | 2.55 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e06 | 2.55 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 2.60 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e08 | 2.75 | BRAKE_START | B | - | controls |  |
| B:e09 | 2.75 | HARD_BRAKE_START | B | - | controls |  |
| B:e10 | 3.50 | CLOSING_END | B | track_001 | radar |  |
| B:e11 | 3.50 | MOVING_END | B | - | ego |  |
| B:e12 | 3.50 | STOP_START | B | - | ego |  |
| B:e13 | 6.95 | HARD_BRAKE_END | B | - | controls |  |
| B:e14 | 6.95 | BRAKE_END | B | - | controls |  |
| B:e15 | 6.95 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e16 | 7.30 | CLOSING_START | B | track_001 | radar |  |
| B:e17 | 7.35 | STOP_END | B | - | ego |  |
| B:e18 | 7.35 | MOVING_START | B | - | ego |  |
| B:e19 | 8.25 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e20 | 8.65 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e21 | 8.95 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e22 | 9.45 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e23 | 9.45 | CLOSING_END | B | track_001 | radar |  |
| B:e24 | 9.50 | COLLISION | B | - | collision_sensor | peak_impulse=4032.49 |
| B:e25 | 9.50 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e26 | 9.50 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e27 | 9.55 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e28 | 9.55 | BRAKE_START | B | - | controls |  |
| B:e29 | 9.55 | HARD_BRAKE_START | B | - | controls |  |
| B:e30 | 9.60 | TRACK_LOST | B | track_001 | radar |  |
| B:e31 | 9.95 | MOVING_END | B | - | ego |  |
| B:e32 | 9.95 | STOP_START | B | - | ego |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e08 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e14
    B:e10 --PRECEDES--> B:e15
    B:e11 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e11 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e22 --PRECEDES--> B:e25
    B:e22 --PRECEDES--> B:e26
    B:e23 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e23 --PRECEDES--> B:e26
    B:e24 --PRECEDES--> B:e27
    B:e24 --PRECEDES--> B:e28
    B:e24 --PRECEDES--> B:e29
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e25 --PRECEDES--> B:e29
    B:e26 --PRECEDES--> B:e27
    B:e26 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e30
    B:e30 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e10
    B:e05 --SAME_TRACK--> B:e16
    B:e05 --SAME_TRACK--> B:e19
    B:e05 --SAME_TRACK--> B:e21
    B:e05 --SAME_TRACK--> B:e22
    B:e05 --SAME_TRACK--> B:e23
    B:e05 --SAME_TRACK--> B:e25
    B:e05 --SAME_TRACK--> B:e30
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 2.10 | B:e04 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 2.00 |
| 2.55 | B:e05 TRACK_APPEARED_RIGHT track_001<br>B:e06 CLOSING_START track_001 | ego: MOVING<br>sign-1: STOP sign known, relevant to the path | 2.50 |
| 2.60 | B:e07 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 2.50 |
| 2.75 | B:e08 BRAKE_START<br>B:e09 HARD_BRAKE_START | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 2.70 |
| 3.50 | B:e10 CLOSING_END track_001<br>B:e11 MOVING_END<br>B:e12 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 3.40 |
| 6.95 | B:e13 HARD_BRAKE_END<br>B:e14 BRAKE_END<br>B:e15 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 6.90 |
| 7.30 | B:e16 CLOSING_START track_001 | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 7.20 |
| 7.35 | B:e17 STOP_END<br>B:e18 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 7.30 |
| 8.25 | B:e19 CRITICAL_TTC_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 8.20 |
| 8.65 | B:e20 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 8.60 |
| 8.95 | B:e21 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known, relevant to the path | 8.90 |
| 9.45 | B:e22 CRITICAL_TTC_END track_001<br>B:e23 CLOSING_END track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known, relevant to the path | 9.40 |
| 9.50 | B:e24 COLLISION<br>B:e25 EGO_PATH_EXIT track_001<br>B:e26 STRONG_THROTTLE_START | ego: MOVING<br>track_001: IN_EGO_PATH<br>sign-1: STOP sign known, relevant to the path | 9.40 |
| 9.55 | B:e27 STRONG_THROTTLE_END<br>B:e28 BRAKE_START<br>B:e29 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 9.50 |
| 9.60 | B:e30 TRACK_LOST track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 9.50 |
| 9.95 | B:e31 MOVING_END<br>B:e32 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known, relevant to the path | 9.90 |

## States still active when observation ended

- BRAKE, since B:e28 (t = 9.55 s)
- HARD_BRAKE, since B:e29 (t = 9.55 s)
- STOP, since B:e32 (t = 9.95 s)

## Tracks lost

- lost with no state active: track_001

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.55 | 9.60 | 142 | 27.5 m / +35 deg | 0.70 m (9.40) | 2.0 m / -144 deg | 8.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1).
- t = 2.55 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.55 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.60 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.75 s: B started braking.
- t = 2.75 s: B started braking hard.
- t = 3.50 s: B observed track_001 stop closing in.
- t = 3.50 s: B stopped moving.
- t = 3.50 s: B came to a stop.
- t = 6.95 s: B stopped braking hard.
- t = 6.95 s: B released the brake.
- t = 6.95 s: B started applying strong throttle.
- t = 7.30 s: B observed track_001 start closing in.
- t = 7.35 s: B left its stop.
- t = 7.35 s: B started moving.
- t = 8.25 s: B's time-to-contact with track_001 became critical.
- t = 8.65 s: B stopped applying strong throttle.
- t = 8.95 s: B observed track_001 enter its forward path corridor.
- t = 9.45 s: B's time-to-contact with track_001 stopped being critical.
- t = 9.45 s: B observed track_001 stop closing in.
- t = 9.50 s: B's collision sensor recorded a contact (peak impulse 4032 N*s).
- t = 9.50 s: B observed track_001 leave its forward path corridor.
- t = 9.50 s: B started applying strong throttle.
- t = 9.55 s: B stopped applying strong throttle.
- t = 9.55 s: B started braking.
- t = 9.55 s: B started braking hard.
- t = 9.60 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.95 s: B stopped moving.
- t = 9.95 s: B came to a stop.
