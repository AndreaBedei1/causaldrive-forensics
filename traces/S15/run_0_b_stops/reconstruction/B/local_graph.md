# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 478.86066130176187 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 107 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (10.55 s)
- Anonymous radar tracks: 3 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 37; edges: 65 (PRECEDES 48, SAME_TRACK 17)

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
| B:e16 | 2.95 | PREDICTED_PATH_CONFLICT_START | B | track_002 | radar |  |
| B:e17 | 3.30 | PREDICTED_PATH_CONFLICT_END | B | track_002 | radar |  |
| B:e18 | 3.40 | MOVING_END | B | - | ego |  |
| B:e19 | 3.40 | STOP_START | B | - | ego |  |
| B:e20 | 3.40 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e21 | 3.70 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |
| B:e22 | 3.90 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e23 | 3.95 | TRACK_APPEARED | B | track_003 | radar |  |
| B:e24 | 3.95 | CLOSING_START | B | track_003 | radar | active_at_first_observation=True |
| B:e25 | 4.20 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e26 | 4.25 | CLOSING_END | B | track_002 | radar |  |
| B:e27 | 4.40 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e28 | 4.80 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-2 |
| B:e29 | 4.80 | TRACK_LOST | B | track_002 | radar |  |
| B:e30 | 4.80 | STOP_SIGN_DETECTED_END | B | sign-1 | camera | sign_track=sign-2 |
| B:e31 | 5.35 | CLOSING_END | B | track_003 | radar |  |
| B:e32 | 5.60 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| B:e33 | 5.60 | STOP_SIGN_DETECTED_END | B | sign-1 | camera | sign_track=sign-3 |
| B:e34 | 5.65 | EGO_PATH_ENTRY | B | track_003 | radar |  |
| B:e35 | 6.45 | EGO_PATH_EXIT | B | track_003 | radar |  |
| B:e36 | 6.70 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| B:e37 | 10.55 | STRONG_THROTTLE_START | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

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
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e17 --PRECEDES--> B:e19
    B:e17 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e21
    B:e20 --PRECEDES--> B:e21
    B:e21 --PRECEDES--> B:e22
    B:e22 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e25
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e26 --PRECEDES--> B:e27
    B:e27 --PRECEDES--> B:e28
    B:e27 --PRECEDES--> B:e29
    B:e27 --PRECEDES--> B:e30
    B:e28 --PRECEDES--> B:e31
    B:e29 --PRECEDES--> B:e31
    B:e30 --PRECEDES--> B:e31
    B:e31 --PRECEDES--> B:e32
    B:e31 --PRECEDES--> B:e33
    B:e32 --PRECEDES--> B:e34
    B:e33 --PRECEDES--> B:e34
    B:e34 --PRECEDES--> B:e35
    B:e35 --PRECEDES--> B:e36
    B:e36 --PRECEDES--> B:e37
    B:e03 --SAME_TRACK--> B:e04
    B:e07 --SAME_TRACK--> B:e08
    B:e07 --SAME_TRACK--> B:e09
    B:e03 --SAME_TRACK--> B:e11
    B:e03 --SAME_TRACK--> B:e14
    B:e03 --SAME_TRACK--> B:e15
    B:e07 --SAME_TRACK--> B:e16
    B:e07 --SAME_TRACK--> B:e17
    B:e07 --SAME_TRACK--> B:e22
    B:e23 --SAME_TRACK--> B:e24
    B:e07 --SAME_TRACK--> B:e25
    B:e07 --SAME_TRACK--> B:e26
    B:e07 --SAME_TRACK--> B:e27
    B:e07 --SAME_TRACK--> B:e29
    B:e23 --SAME_TRACK--> B:e31
    B:e23 --SAME_TRACK--> B:e34
    B:e23 --SAME_TRACK--> B:e35
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.20 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.10 |
| 1.45 | B:e03 TRACK_APPEARED track_001<br>B:e04 CLOSING_START track_001 | ego: MOVING, STRONG_THROTTLE | 1.40 |
| 1.80 | B:e05 STRONG_THROTTLE_END<br>B:e06 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING | 1.70 |
| 1.95 | B:e07 TRACK_APPEARED track_002<br>B:e08 CLOSING_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign VISIBLE, known | 1.90 |
| 2.00 | B:e09 CRITICAL_TTC_START track_002 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>sign-0: STOP sign VISIBLE, known | 1.90 |
| 2.10 | B:e10 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign VISIBLE, known | 2.00 |
| 2.35 | B:e11 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known | 2.30 |
| 2.55 | B:e12 BRAKE_START<br>B:e13 HARD_BRAKE_START | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known | 2.50 |
| 2.70 | B:e14 CRITICAL_TTC_END track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known | 2.60 |
| 2.85 | B:e15 TRACK_LOST track_001 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known | 2.80 |
| 2.95 | B:e16 PREDICTED_PATH_CONFLICT_START track_002 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 2.90 |
| 3.30 | B:e17 PREDICTED_PATH_CONFLICT_END track_002 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 3.20 |
| 3.40 | B:e18 MOVING_END<br>B:e19 STOP_START<br>B:e20 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known | 3.30 |
| 3.70 | B:e21 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign VISIBLE, known | 3.60 |
| 3.90 | B:e22 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 3.80 |
| 3.95 | B:e23 TRACK_APPEARED track_003<br>B:e24 CLOSING_START track_003 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 3.90 |
| 4.20 | B:e25 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 4.10 |
| 4.25 | B:e26 CLOSING_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 4.20 |
| 4.40 | B:e27 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 4.30 |
| 4.80 | B:e28 STOP_SIGN_DETECTED_START sign-1<br>B:e29 TRACK_LOST track_002<br>B:e30 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 4.70 |
| 5.35 | B:e31 CLOSING_END track_003 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 5.30 |
| 5.60 | B:e32 STOP_SIGN_DETECTED_START sign-1<br>B:e33 STOP_SIGN_DETECTED_END sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 5.50 |
| 5.65 | B:e34 EGO_PATH_ENTRY track_003 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 5.60 |
| 6.45 | B:e35 EGO_PATH_EXIT track_003 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 6.40 |
| 6.70 | B:e36 STOP_SIGN_DETECTED_START sign-1 | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known | 6.60 |
| 10.55 | B:e37 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign VISIBLE, known | 10.50 |

## States still active when observation ended

- CLOSING of track_001, since B:e04 (t = 1.45 s); the track was lost at 2.85 s
- BRAKE, since B:e12 (t = 2.55 s)
- HARD_BRAKE, since B:e13 (t = 2.55 s)
- STOP, since B:e19 (t = 3.40 s)
- STOP_SIGN_DETECTED of sign-1, since B:e36 (t = 6.70 s)
- STRONG_THROTTLE, since B:e37 (t = 10.55 s)

## Tracks lost

- track_001 at 2.85 s (B:e15): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_002

## Sign detection windows

- STOP sign sign-0: detected 1.80 s -> 2.10 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 3.40 s -> 3.70 s; relevant to the path: False; STOP_START inside: none
- STOP sign sign-1: detected 4.80 s -> 4.80 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 5.60 s -> 5.60 s; relevant to the path: False; STOP_START inside: none; already stopped when the window opened
- STOP sign sign-1: detected 6.70 s -> the end of the recording (still in view); relevant to the path: False; STOP_START inside: none; already stopped when the window opened

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
- t = 2.85 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 2.95 s: B predicted a path conflict with track_002 (close approach ahead if both keep their motion).
- t = 3.30 s: B stopped predicting a path conflict with track_002.
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
- t = 4.80 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- t = 4.80 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 4.80 s: B's camera stopped detecting STOP sign sign-1.
- t = 5.35 s: B observed track_003 stop closing in.
- t = 5.60 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- t = 5.60 s: B's camera stopped detecting STOP sign sign-1.
- t = 5.65 s: B observed track_003 enter its forward path corridor.
- t = 6.45 s: B observed track_003 leave its forward path corridor.
- t = 6.70 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- t = 10.55 s: B started applying strong throttle.
