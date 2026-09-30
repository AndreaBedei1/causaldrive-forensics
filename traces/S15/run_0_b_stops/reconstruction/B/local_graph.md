# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 478.86066130176187 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 35; edges: 61 (PRECEDES 46, SAME_TRACK 15)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.20 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.45 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e04 | 1.45 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e05 | 1.80 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e06 | 1.80 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e07 | 1.95 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e08 | 1.95 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e09 | 2.00 | CRITICAL_TTC_START | B | track_002 | radar |  |
| B:e10 | 2.10 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e11 | 2.35 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e12 | 2.55 | BRAKE_START | B | - | controls |  |
| B:e13 | 2.55 | HARD_BRAKE_START | B | - | controls |  |
| B:e14 | 2.70 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e15 | 2.85 | TRACK_LOST | B | track_001 | radar |  |
| B:e16 | 3.40 | MOVING_END | B | - | ego |  |
| B:e17 | 3.40 | STOP_START | B | - | ego |  |
| B:e18 | 3.40 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e19 | 3.70 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e20 | 3.90 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e21 | 3.95 | TRACK_APPEARED | B | track_003 | radar |  |
| B:e22 | 3.95 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e23 | 4.20 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e24 | 4.25 | CLOSING_END | B | track_002 | radar |  |
| B:e25 | 4.40 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e26 | 4.80 | STOP_SIGN_DETECTED_START | B | sign-2 | camera | relevant_to_ego_path=False |
| B:e27 | 4.80 | TRACK_LOST | B | track_002 | radar |  |
| B:e28 | 4.80 | STOP_SIGN_DETECTED_END | B | sign-2 | camera |  |
| B:e29 | 5.35 | CLOSING_END | B | track_003 | radar |  |
| B:e30 | 5.60 | STOP_SIGN_DETECTED_START | B | sign-3 | camera | relevant_to_ego_path=False |
| B:e31 | 5.60 | STOP_SIGN_DETECTED_END | B | sign-3 | camera |  |
| B:e32 | 5.65 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e33 | 6.45 | EGO_PATH_EXIT | B | track_003 | radar |  |
| B:e34 | 6.70 | STOP_SIGN_DETECTED_START | B | sign-4 | camera | relevant_to_ego_path=False |
| B:e35 | 10.55 | STRONG_THROTTLE_START | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times.

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
    B:e05 --PRECEDES--> B:e08
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e09
    B:e09 --PRECEDES--> B:e10
    B:e10 --PRECEDES--> B:e11
    B:e11 --PRECEDES--> B:e12
    B:e11 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e17
    B:e15 --PRECEDES--> B:e18
    B:e16 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e19
    B:e19 --PRECEDES--> B:e20
    B:e20 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e23
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e25 --PRECEDES--> B:e27
    B:e25 --PRECEDES--> B:e28
    B:e26 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e29
    B:e28 --PRECEDES--> B:e29
    B:e29 --PRECEDES--> B:e30
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e32
    B:e32 --PRECEDES--> B:e33
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e03 --SAME_TRACK--> B:e04
    B:e07 --SAME_TRACK--> B:e08
    B:e07 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e11
    B:e03 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e07 --SAME_TRACK--> B:e20
    B:e21 --SAME_TRACK--> B:e22
    B:e07 --SAME_TRACK--> B:e23
    B:e07 --SAME_TRACK--> B:e24
    B:e07 --SAME_TRACK--> B:e25
    B:e07 --SAME_TRACK--> B:e27
    B:e21 --SAME_TRACK--> B:e29
    B:e21 --SAME_TRACK--> B:e32
    B:e21 --SAME_TRACK--> B:e33
```

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 1.45 s); the track was lost at 2.85 s
- BRAKE, since B:e12 (t = 2.55 s)
- HARD_BRAKE, since B:e13 (t = 2.55 s)
- STOP, since B:e17 (t = 3.40 s)
- STOP_SIGN_DETECTED of sign-4, since B:e34 (t = 6.70 s)
- STRONG_THROTTLE, since B:e35 (t = 10.55 s)

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 3.40 s -> 3.70 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-2: detected 4.80 s -> 4.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-3: detected 5.60 s -> 5.60 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-4: detected 6.70 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 1.45 | 2.85 | 27 | 28.6 m / +37 deg | 15.73 m (2.85) | 15.7 m / +61 deg | 6.2 m/s |
| track_002 | 1.95 | 4.80 | 58 | 29.3 m / -57 deg | 3.28 m (4.25) | 5.7 m / +63 deg | 10.8 m/s |
| track_003 | 3.95 | 10.55 | 130 | 10.4 m / +59 deg | 7.10 m (5.45) | 29.5 m / -55 deg | 5.9 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.20 s: B started applying strong throttle.
- t = 1.45 s: B's radar started tracking track_001.
- t = 1.45 s: B observed track_001 start closing in (already the case when first observed).
- t = 1.80 s: B stopped applying strong throttle.
- t = 1.80 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 1.95 s: B's radar started tracking track_002.
- t = 1.95 s: B observed track_002 start closing in (already the case when first observed).
- t = 2.00 s: B's time-to-contact with track_002 became critical.
- t = 2.10 s: B's camera stopped detecting STOP sign sign-0.
- t = 2.35 s: B's time-to-contact with track_001 became critical.
- t = 2.55 s: B started braking.
- t = 2.55 s: B started braking hard.
- t = 2.70 s: B's time-to-contact with track_001 stopped being critical.
- t = 2.85 s: B's radar lost track_001.
- t = 3.40 s: B stopped moving.
- t = 3.40 s: B came to a stop.
- t = 3.40 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 3.70 s: B's camera stopped detecting STOP sign sign-1.
- t = 3.90 s: B observed track_002 enter its forward path corridor.
- t = 3.95 s: B's radar started tracking track_003.
- t = 3.95 s: B observed track_003 start closing in (already the case when first observed).
- t = 4.20 s: B's time-to-contact with track_002 stopped being critical.
- t = 4.25 s: B observed track_002 stop closing in.
- t = 4.40 s: B observed track_002 leave its forward path corridor.
- t = 4.80 s: B's camera established a STOP sign detection (sign-2) (the detector judged it not relevant to its path).
- t = 4.80 s: B's radar lost track_002.
- t = 4.80 s: B's camera stopped detecting STOP sign sign-2.
- t = 5.35 s: B observed track_003 stop closing in.
- t = 5.60 s: B's camera established a STOP sign detection (sign-3) (the detector judged it not relevant to its path).
- t = 5.60 s: B's camera stopped detecting STOP sign sign-3.
- t = 5.65 s: B observed track_003 enter its forward path corridor.
- t = 6.45 s: B observed track_003 leave its forward path corridor.
- t = 6.70 s: B's camera established a STOP sign detection (sign-4) (the detector judged it not relevant to its path).
- t = 10.55 s: B started applying strong throttle.
