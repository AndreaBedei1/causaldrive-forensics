# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 181.6859812811017 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 161 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.95 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 17; edges: 23 (PRECEDES 18, SAME_TRACK 5)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.95 | BRAKE_START | B | - | controls |  |
| B:e03 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e04 | 2.50 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e05 | 2.60 | TRACK_APPEARED_LEFT | B | track_001 | radar |  |
| B:e06 | 2.60 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e07 | 2.65 | BRAKE_END | B | - | controls |  |
| B:e08 | 3.80 | TURN_LEFT_START | B | - | ego |  |
| B:e09 | 4.10 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e10 | 5.35 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e11 | 5.50 | COLLISION | B | - | collision_sensor | peak_impulse=8859.58 |
| B:e12 | 5.50 | TURN_LEFT_END | B | - | ego |  |
| B:e13 | 5.55 | BRAKE_START | B | - | controls |  |
| B:e14 | 5.70 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e15 | 5.70 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 5.70 | MOVING_END | B | - | ego |  |
| B:e17 | 5.70 | STOP_START | B | - | ego |  |

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
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e05 --SAME_TRACK--> B:e06
    B:e05 --SAME_TRACK--> B:e09
    B:e05 --SAME_TRACK--> B:e10
    B:e05 --SAME_TRACK--> B:e14
    B:e05 --SAME_TRACK--> B:e15
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.95 | B:e02 BRAKE_START | ego: MOVING | 1.90 |
| 2.10 | B:e03 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING, BRAKE | 2.00 |
| 2.50 | B:e04 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING, BRAKE<br>sign-1: STOP sign known | 2.40 |
| 2.60 | B:e05 TRACK_APPEARED_LEFT track_001<br>B:e06 CLOSING_START track_001 | ego: MOVING, BRAKE<br>sign-1: STOP sign known | 2.50 |
| 2.65 | B:e07 BRAKE_END | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known | 2.60 |
| 3.80 | B:e08 TURN_LEFT_START | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known | 3.70 |
| 4.10 | B:e09 CRITICAL_TTC_START track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING<br>sign-1: STOP sign known | 4.00 |
| 5.35 | B:e10 EGO_PATH_ENTRY track_001 | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-1: STOP sign known | 5.30 |
| 5.50 | B:e11 COLLISION<br>B:e12 TURN_LEFT_END | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known | 5.40 |
| 5.55 | B:e13 BRAKE_START | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known | 5.50 |
| 5.70 | B:e14 CRITICAL_TTC_END track_001<br>B:e15 CLOSING_END track_001<br>B:e16 MOVING_END<br>B:e17 STOP_START | ego: MOVING, BRAKE<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-1: STOP sign known | 5.60 |

## States still active when observation ended

- EGO_PATH of track_001, since B:e10 (t = 5.35 s)
- BRAKE, since B:e13 (t = 5.55 s)
- STOP, since B:e17 (t = 5.70 s)

## Tracks lost

- no track was lost

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 4.10, COLLISION 5.50 (+1.40 s); EGO_PATH_ENTRY 5.35 after critical TTC (+1.25 s)

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.50 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.60 | 15.95 | 268 | 35.3 m / -69 deg | 0.13 m (5.70) | 0.3 m / +17 deg | 10.0 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.95 s: B started braking.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.50 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.60 s: B's radar started tracking track_001, which appeared on its left.
- t = 2.60 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.65 s: B released the brake.
- t = 3.80 s: B started turning left.
- t = 4.10 s: B's time-to-contact with track_001 became critical.
- t = 5.35 s: B observed track_001 enter its forward path corridor.
- t = 5.50 s: B's collision sensor recorded a contact (peak impulse 8860 N*s).
- t = 5.50 s: B stopped turning left.
- t = 5.55 s: B started braking.
- t = 5.70 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.70 s: B observed track_001 stop closing in.
- t = 5.70 s: B stopped moving.
- t = 5.70 s: B came to a stop.
