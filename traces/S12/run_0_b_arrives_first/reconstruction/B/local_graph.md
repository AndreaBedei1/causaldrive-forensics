# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 370.09269582107663 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 20; edges: 33 (PRECEDES 29, SAME_TRACK 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=True |
| B:e05 | 2.60 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e06 | 2.65 | BRAKE_START | B | - | controls |  |
| B:e07 | 2.65 | HARD_BRAKE_START | B | - | controls |  |
| B:e08 | 3.00 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e09 | 3.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e10 | 3.40 | MOVING_END | B | - | ego |  |
| B:e11 | 3.40 | STOP_START | B | - | ego |  |
| B:e12 | 4.70 | CLOSING_END | B | track_001 | radar |  |
| B:e13 | 6.45 | HARD_BRAKE_END | B | - | controls |  |
| B:e14 | 6.45 | BRAKE_END | B | - | controls |  |
| B:e15 | 6.45 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e16 | 6.85 | STOP_END | B | - | ego |  |
| B:e17 | 6.85 | MOVING_START | B | - | ego |  |
| B:e18 | 7.00 | CLOSING_START | B | track_001 | radar |  |
| B:e19 | 7.90 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e20 | 8.75 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

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
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e13 --PRECEDES--> B:e17
    B:e14 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e16 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e08 --SAME_TRACK--> B:e09
    B:e08 --SAME_TRACK--> B:e12
    B:e08 --SAME_TRACK--> B:e18
    B:e08 --SAME_TRACK--> B:e20
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 2.10 | B:e04 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING | 2.00 |
| 2.60 | B:e05 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>sign-1: STOP sign known, relevant to the path | 2.50 |
| 2.65 | B:e06 BRAKE_START<br>B:e07 HARD_BRAKE_START | ego: MOVING<br>sign-1: STOP sign known, relevant to the path | 2.60 |
| 3.00 | B:e08 TRACK_APPEARED_RIGHT track_001<br>B:e09 CLOSING_START track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>sign-1: STOP sign known, relevant to the path | 2.90 |
| 3.40 | B:e10 MOVING_END<br>B:e11 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 3.30 |
| 4.70 | B:e12 CLOSING_END track_001 | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 4.60 |
| 6.45 | B:e13 HARD_BRAKE_END<br>B:e14 BRAKE_END<br>B:e15 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 6.40 |
| 6.85 | B:e16 STOP_END<br>B:e17 MOVING_START | ego: STOP, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 6.80 |
| 7.00 | B:e18 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE<br>track_001: no active state<br>sign-1: STOP sign known, relevant to the path | 6.90 |
| 7.90 | B:e19 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 7.80 |
| 8.75 | B:e20 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-1: STOP sign known, relevant to the path | 8.70 |

## States still active when observation ended

- MOVING, since B:e17 (t = 6.85 s)
- CLOSING of track_001, since B:e18 (t = 7.00 s); the track was lost at 8.75 s

## Tracks lost

- track_001 at 8.75 s (B:e20): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-1: detected 2.10 s -> 2.60 s; relevant to the path: True; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 3.00 | 8.75 | 115 | 28.7 m / +48 deg | 14.09 m (8.75) | 14.1 m / +60 deg | 5.3 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 2.10 s: B's camera established a STOP sign detection (sign-1).
- t = 2.60 s: B's camera stopped detecting STOP sign sign-1.
- t = 2.65 s: B started braking.
- t = 2.65 s: B started braking hard.
- t = 3.00 s: B's radar started tracking track_001, which appeared on its right.
- t = 3.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 3.40 s: B stopped moving.
- t = 3.40 s: B came to a stop.
- t = 4.70 s: B observed track_001 stop closing in.
- t = 6.45 s: B stopped braking hard.
- t = 6.45 s: B released the brake.
- t = 6.45 s: B started applying strong throttle.
- t = 6.85 s: B left its stop.
- t = 6.85 s: B started moving.
- t = 7.00 s: B observed track_001 start closing in.
- t = 7.90 s: B stopped applying strong throttle.
- t = 8.75 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
