# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 317.08158706873655 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 18; edges: 29 (PRECEDES 22, SAME_TRACK 7)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e05 | 2.35 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e06 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e07 | 2.55 | HARD_BRAKE_START | B | - | controls |  |
| B:e08 | 3.25 | MOVING_END | B | - | ego |  |
| B:e09 | 3.25 | STOP_START | B | - | ego |  |
| B:e10 | 3.50 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e11 | 3.50 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e12 | 4.40 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e13 | 5.75 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e14 | 5.80 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e15 | 6.10 | CLOSING_END | B | track_001 | radar |  |
| B:e16 | 6.20 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e17 | 7.30 | TRACK_LOST | B | track_001 | radar |  |
| B:e18 | 9.55 | STRONG_THROTTLE_START | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
    B:e05 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e12
    B:e12 --PRECEDES--> B:e13
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e10 --SAME_TRACK--> B:e11
    B:e10 --SAME_TRACK--> B:e12
    B:e10 --SAME_TRACK--> B:e13
    B:e10 --SAME_TRACK--> B:e14
    B:e10 --SAME_TRACK--> B:e15
    B:e10 --SAME_TRACK--> B:e16
    B:e10 --SAME_TRACK--> B:e17
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 2.10 | B:e04 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 2.00 |
| 2.35 | B:e05 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign VISIBLE, known | 2.30 |
| 2.55 | B:e06 BRAKE_START<br>B:e07 HARD_BRAKE_START | ego: MOVING<br>sign-1: STOP sign not visible, known | 2.50 |
| 3.25 | B:e08 MOVING_END<br>B:e09 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign not visible, known | 3.20 |
| 3.50 | B:e10 TRACK_APPEARED track_001<br>B:e11 CLOSING_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>sign-1: STOP sign not visible, known | 3.40 |
| 4.40 | B:e12 CRITICAL_TTC_START track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known | 4.30 |
| 5.75 | B:e13 CRITICAL_TTC_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-1: STOP sign not visible, known | 5.70 |
| 5.80 | B:e14 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>sign-1: STOP sign not visible, known | 5.70 |
| 6.10 | B:e15 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, IN_EGO_PATH<br>sign-1: STOP sign not visible, known | 6.00 |
| 6.20 | B:e16 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, IN_EGO_PATH<br>sign-1: STOP sign not visible, known | 6.10 |
| 7.30 | B:e17 TRACK_LOST track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: VISIBLE<br>sign-1: STOP sign not visible, known | 7.20 |
| 9.55 | B:e18 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001<br>sign-1: STOP sign not visible, known | 9.50 |

## States still active when observation ended

- BRAKE, since B:e06 (t = 2.55 s)
- HARD_BRAKE, since B:e07 (t = 2.55 s)
- STOP, since B:e09 (t = 3.25 s)
- STRONG_THROTTLE, since B:e18 (t = 9.55 s)

## Tracks lost

- lost with no state active: track_001

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.35 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.50 | 7.30 | 75 | 24.6 m / -60 deg | 6.91 m (6.10) | 12.8 m / +59 deg | 9.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 2.35 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.55 s: B started braking.
- t = 2.55 s: B started braking hard.
- t = 3.25 s: B stopped moving.
- t = 3.25 s: B came to a stop.
- t = 3.50 s: B's radar started tracking track_001.
- t = 3.50 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.40 s: B's time-to-contact with track_001 became critical.
- t = 5.75 s: B's time-to-contact with track_001 stopped being critical.
- t = 5.80 s: B observed track_001 enter its forward path corridor.
- t = 6.10 s: B observed track_001 stop closing in.
- t = 6.20 s: B observed track_001 leave its forward path corridor.
- t = 7.30 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 9.55 s: B started applying strong throttle.
