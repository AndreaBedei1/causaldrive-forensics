# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 103.39315643906593 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 101 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.95 s)
- Anonymous radar tracks: 2 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 26; edges: 47 (PRECEDES 38, SAME_TRACK 9)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.25 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.85 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.00 | TRACK_APPEARED | B | track_001 | radar |  |
| B:e05 | 2.00 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 2.35 | TRACK_LOST | B | track_001 | radar |  |
| B:e07 | 3.15 | BRAKE_START | B | - | controls |  |
| B:e08 | 3.15 | HARD_BRAKE_START | B | - | controls |  |
| B:e09 | 3.90 | MOVING_END | B | - | ego |  |
| B:e10 | 3.90 | STOP_START | B | - | ego |  |
| B:e11 | 4.35 | TRACK_APPEARED | B | track_002 | radar |  |
| B:e12 | 4.35 | CLOSING_START | B | track_002 | radar | active_at_first_observation=True |
| B:e13 | 4.35 | CRITICAL_TTC_START | B | track_002 | radar | active_at_first_observation=True |
| B:e14 | 5.40 | EGO_PATH_ENTRY | B | track_002 | radar |  |
| B:e15 | 5.45 | CRITICAL_TTC_END | B | track_002 | radar |  |
| B:e16 | 5.55 | CLOSING_END | B | track_002 | radar |  |
| B:e17 | 5.90 | EGO_PATH_EXIT | B | track_002 | radar |  |
| B:e18 | 6.90 | TRACK_LOST | B | track_002 | radar |  |
| B:e19 | 7.15 | HARD_BRAKE_END | B | - | controls |  |
| B:e20 | 7.15 | BRAKE_END | B | - | controls |  |
| B:e21 | 7.15 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e22 | 7.55 | STOP_END | B | - | ego |  |
| B:e23 | 7.55 | MOVING_START | B | - | ego |  |
| B:e24 | 8.55 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e25 | 8.75 | BRAKE_START | B | - | controls |  |
| B:e26 | 9.00 | BRAKE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e06 --PRECEDES--> B:e08
    B:e07 --PRECEDES--> B:e09
    B:e07 --PRECEDES--> B:e10
    B:e08 --PRECEDES--> B:e09
    B:e08 --PRECEDES--> B:e10
    B:e09 --PRECEDES--> B:e11
    B:e09 --PRECEDES--> B:e12
    B:e09 --PRECEDES--> B:e13
    B:e10 --PRECEDES--> B:e11
    B:e10 --PRECEDES--> B:e12
    B:e10 --PRECEDES--> B:e13
    B:e11 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e14
    B:e13 --PRECEDES--> B:e14
    B:e14 --PRECEDES--> B:e15
    B:e15 --PRECEDES--> B:e16
    B:e16 --PRECEDES--> B:e17
    B:e17 --PRECEDES--> B:e18
    B:e18 --PRECEDES--> B:e19
    B:e18 --PRECEDES--> B:e20
    B:e18 --PRECEDES--> B:e21
    B:e19 --PRECEDES--> B:e22
    B:e19 --PRECEDES--> B:e23
    B:e20 --PRECEDES--> B:e22
    B:e20 --PRECEDES--> B:e23
    B:e21 --PRECEDES--> B:e22
    B:e21 --PRECEDES--> B:e23
    B:e22 --PRECEDES--> B:e24
    B:e23 --PRECEDES--> B:e24
    B:e24 --PRECEDES--> B:e25
    B:e25 --PRECEDES--> B:e26
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e11 --SAME_TRACK--> B:e12
    B:e11 --SAME_TRACK--> B:e13
    B:e11 --SAME_TRACK--> B:e14
    B:e11 --SAME_TRACK--> B:e15
    B:e11 --SAME_TRACK--> B:e16
    B:e11 --SAME_TRACK--> B:e17
    B:e11 --SAME_TRACK--> B:e18
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.25 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.20 |
| 1.85 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.80 |
| 2.00 | B:e04 TRACK_APPEARED track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING | 1.90 |
| 2.35 | B:e06 TRACK_LOST track_001 | ego: MOVING<br>track_001: VISIBLE, CLOSING, PATH_CONFLICT?, CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT? | 2.30 |
| 3.15 | B:e07 BRAKE_START<br>B:e08 HARD_BRAKE_START | ego: MOVING<br>lost (states UNKNOWN): track_001 | 3.10 |
| 3.90 | B:e09 MOVING_END<br>B:e10 STOP_START | ego: MOVING, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 | 3.80 |
| 4.35 | B:e11 TRACK_APPEARED track_002<br>B:e12 CLOSING_START track_002<br>B:e13 CRITICAL_TTC_START track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001 | 4.30 |
| 5.40 | B:e14 EGO_PATH_ENTRY track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001 | 5.30 |
| 5.45 | B:e15 CRITICAL_TTC_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 | 5.40 |
| 5.55 | B:e16 CLOSING_END track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 | 5.50 |
| 5.90 | B:e17 EGO_PATH_EXIT track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_001 | 5.80 |
| 6.90 | B:e18 TRACK_LOST track_002 | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>lost (states UNKNOWN): track_001 | 6.80 |
| 7.15 | B:e19 HARD_BRAKE_END<br>B:e20 BRAKE_END<br>B:e21 STRONG_THROTTLE_START | ego: STOP, BRAKE, HARD_BRAKE<br>lost (states UNKNOWN): track_001, track_002 | 7.10 |
| 7.55 | B:e22 STOP_END<br>B:e23 MOVING_START | ego: STOP, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 | 7.50 |
| 8.55 | B:e24 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE<br>lost (states UNKNOWN): track_001, track_002 | 8.50 |
| 8.75 | B:e25 BRAKE_START | ego: MOVING<br>lost (states UNKNOWN): track_001, track_002 | 8.70 |
| 9.00 | B:e26 BRAKE_END | ego: MOVING, BRAKE<br>lost (states UNKNOWN): track_001, track_002 | 8.90 |

## States still active when observation ended

- CLOSING of track_001, since B:e05 (t = 2.00 s); the track was lost at 2.35 s
- MOVING, since B:e23 (t = 7.55 s)

## Tracks lost

- track_001 at 2.35 s (B:e06): CLOSING were true; they are UNKNOWN afterwards (no END recorded)
- lost with no state active: track_002

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.00 | 2.35 | 6 | 37.5 m / -58 deg | 33.02 m (2.35) | 33.0 m / -60 deg | 9.7 m/s |
| track_002 | 4.35 | 6.90 | 51 | 11.6 m / -59 deg | 4.65 m (5.60) | 12.6 m / +59 deg | 8.8 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.25 s: B started applying strong throttle.
- t = 1.85 s: B stopped applying strong throttle.
- t = 2.00 s: B's radar started tracking track_001.
- t = 2.00 s: B observed track_001 start closing in (already the case when first observed).
- t = 2.35 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 3.15 s: B started braking.
- t = 3.15 s: B started braking hard.
- t = 3.90 s: B stopped moving.
- t = 3.90 s: B came to a stop.
- t = 4.35 s: B's radar started tracking track_002.
- t = 4.35 s: B observed track_002 start closing in (already the case when first observed).
- t = 4.35 s: B's time-to-contact with track_002 became critical (already the case when first observed).
- t = 5.40 s: B observed track_002 enter its forward path corridor.
- t = 5.45 s: B's time-to-contact with track_002 stopped being critical.
- t = 5.55 s: B observed track_002 stop closing in.
- t = 5.90 s: B observed track_002 leave its forward path corridor.
- t = 6.90 s: B's radar lost track_002 (its states are UNKNOWN from then on, not ended).
- t = 7.15 s: B stopped braking hard.
- t = 7.15 s: B released the brake.
- t = 7.15 s: B started applying strong throttle.
- t = 7.55 s: B left its stop.
- t = 7.55 s: B started moving.
- t = 8.55 s: B stopped applying strong throttle.
- t = 8.75 s: B started braking.
- t = 9.00 s: B released the brake.
