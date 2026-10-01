# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 513.3408981114626 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 141 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (13.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 22; edges: 41 (PRECEDES 34, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.20 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.80 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e05 | 1.95 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e06 | 1.95 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 2.00 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e08 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e09 | 2.95 | BRAKE_START | B | - | controls |  |
| B:e10 | 3.50 | BRAKE_END | B | - | controls |  |
| B:e11 | 3.60 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e12 | 3.80 | COLLISION | B | - | collision_sensor | peak_impulse=9797.50 |
| B:e13 | 3.80 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e14 | 3.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e15 | 3.85 | BRAKE_START | B | - | controls |  |
| B:e16 | 3.85 | HARD_BRAKE_START | B | - | controls |  |
| B:e17 | 4.00 | MOVING_END | B | - | ego |  |
| B:e18 | 4.00 | STOP_START | B | - | ego |  |
| B:e19 | 4.05 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e20 | 4.05 | CLOSING_END | B | track_001 | radar |  |
| B:e21 | 4.85 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e22 | 5.50 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e02 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e03 --PRECEDES--> B:e06
    B:e04 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e12 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e18
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e07
    B:e05 --SAME_TRACK--> B:e11
    B:e05 --SAME_TRACK--> B:e19
    B:e05 --SAME_TRACK--> B:e20
    B:e05 --SAME_TRACK--> B:e21
    B:e05 --SAME_TRACK--> B:e22
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.20 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.10 |
| 1.80 | B:e03 STRONG_THROTTLE_END<br>B:e04 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING, STRONG_THROTTLE | 1.70 |
| 1.95 | B:e05 TRACK_APPEARED_LEFT track_001<br>B:e06 CLOSING_START track_001 | ego: MOVING<br>sign-0: STOP sign known | 1.90 |
| 2.00 | B:e07 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 1.90 |
| 2.10 | B:e08 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.00 |
| 2.95 | B:e09 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 2.90 |
| 3.50 | B:e10 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.40 |
| 3.60 | B:e11 EGO_PATH_ENTRY track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 3.50 |
| 3.80 | B:e12 COLLISION<br>B:e13 STRONG_THROTTLE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known | 3.70 |
| 3.85 | B:e14 STRONG_THROTTLE_END<br>B:e15 BRAKE_START<br>B:e16 HARD_BRAKE_START | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known | 3.80 |
| 4.00 | B:e17 MOVING_END<br>B:e18 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known | 3.90 |
| 4.05 | B:e19 CRITICAL_TTC_END track_001<br>B:e20 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known | 4.00 |
| 4.85 | B:e21 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known | 4.80 |
| 5.50 | B:e22 TRACK_LOST track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-0: STOP sign known | 5.40 |

## States still active when observation ended

- BRAKE, since B:e15 (t = 3.85 s)
- HARD_BRAKE, since B:e16 (t = 3.85 s)
- STOP, since B:e18 (t = 4.00 s)

## Tracks lost

- lost with no state active: track_001

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.95 | 5.50 | 72 | 29.3 m / -57 deg | 0.21 m (4.05) | 5.3 m / +58 deg | 11.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.20 s: B started applying strong throttle.
- t = 1.80 s: B stopped applying strong throttle.
- t = 1.80 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_001, which appeared on its left.
- t = 1.95 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.00 s: B's time-to-contact with track_001 became critical.
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.95 s: B started braking.
- t = 3.50 s: B released the brake.
- t = 3.60 s: B observed track_001 enter its forward path corridor.
- t = 3.80 s: B's collision sensor recorded a contact (peak impulse 9798 N*s).
- t = 3.80 s: B started applying strong throttle.
- t = 3.85 s: B stopped applying strong throttle.
- t = 3.85 s: B started braking.
- t = 3.85 s: B started braking hard.
- t = 4.00 s: B stopped moving.
- t = 4.00 s: B came to a stop.
- t = 4.05 s: B's time-to-contact with track_001 stopped being critical.
- t = 4.05 s: B observed track_001 stop closing in.
- t = 4.85 s: B observed track_001 leave its forward path corridor.
- t = 5.50 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
