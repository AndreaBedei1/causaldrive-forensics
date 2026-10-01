# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 234.8135948292911 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 166 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (16.45 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 16; edges: 26 (PRECEDES 20, SAME_TRACK 6)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 2.10 | STOP_SIGN_DETECTED_START | B | sign-0 | camera | relevant_to_ego_path=False |
| B:e03 | 4.00 | STOP_SIGN_DETECTED_END | B | sign-0 | camera |  |
| B:e04 | 4.35 | BRAKE_START | B | - | controls |  |
| B:e05 | 4.70 | MOVING_END | B | - | ego |  |
| B:e06 | 4.70 | STOP_START | B | - | ego |  |
| B:e07 | 6.90 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e08 | 6.90 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e09 | 8.50 | EGO_PATH_ENTRY | B | track_001 | radar |  |
| B:e10 | 9.05 | EGO_PATH_EXIT | B | track_001 | radar |  |
| B:e11 | 10.45 | BRAKE_END | B | - | controls |  |
| B:e12 | 10.55 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e13 | 10.85 | CRITICAL_TTC_END | B | track_001 | radar |  |
| B:e14 | 10.85 | STOP_END | B | - | ego |  |
| B:e15 | 10.85 | MOVING_START | B | - | ego |  |
| B:e16 | 11.15 | TRACK_LOST | B | track_001 | radar |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
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
    B:e12 --PRECEDES--> B:e13
    B:e12 --PRECEDES--> B:e14
    B:e12 --PRECEDES--> B:e15
    B:e13 --PRECEDES--> B:e16
    B:e14 --PRECEDES--> B:e16
    B:e15 --PRECEDES--> B:e16
    B:e07 --SAME_TRACK--> B:e08
    B:e07 --SAME_TRACK--> B:e09
    B:e07 --SAME_TRACK--> B:e10
    B:e07 --SAME_TRACK--> B:e12
    B:e07 --SAME_TRACK--> B:e13
    B:e07 --SAME_TRACK--> B:e16
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 2.10 | B:e02 STOP_SIGN_DETECTED_START sign-0 | ego: MOVING | 2.00 |
| 4.00 | B:e03 STOP_SIGN_DETECTED_END sign-0 | ego: MOVING<br>sign-0: STOP sign known | 3.90 |
| 4.35 | B:e04 BRAKE_START | ego: MOVING<br>sign-0: STOP sign known | 4.30 |
| 4.70 | B:e05 MOVING_END<br>B:e06 STOP_START | ego: MOVING, BRAKE<br>sign-0: STOP sign known | 4.60 |
| 6.90 | B:e07 TRACK_APPEARED_RIGHT track_001<br>B:e08 CLOSING_START track_001 | ego: STOP, BRAKE<br>sign-0: STOP sign known | 6.80 |
| 8.50 | B:e09 EGO_PATH_ENTRY track_001 | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 8.40 |
| 9.05 | B:e10 EGO_PATH_EXIT track_001 | ego: STOP, BRAKE<br>track_001: CLOSING, IN_EGO_PATH<br>sign-0: STOP sign known | 9.00 |
| 10.45 | B:e11 BRAKE_END | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known | 10.40 |
| 10.55 | B:e12 CRITICAL_TTC_START track_001 | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known | 10.50 |
| 10.85 | B:e13 CRITICAL_TTC_END track_001<br>B:e14 STOP_END<br>B:e15 MOVING_START | ego: STOP<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known | 10.80 |
| 11.15 | B:e16 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known | 11.10 |

## States still active when observation ended

- CLOSING of track_001, since B:e08 (t = 6.90 s); the track was lost at 11.15 s
- MOVING, since B:e15 (t = 10.85 s)

## Tracks lost

- track_001 at 11.15 s (B:e16): CLOSING were true; they are UNKNOWN afterwards (no END recorded)

## Temporal safety relations

Order of each track's cut-in, critical TTC and path entry and of the collision report, in local time. Temporal properties only, not causes.

- track_001: CRITICAL_TTC_START 10.55; EGO_PATH_ENTRY 8.50 before critical TTC (-2.05 s)

## Sign detection windows

- STOP sign sign-0: detected 2.10 s -> 4.00 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 6.90 | 11.15 | 86 | 21.8 m / +33 deg | 5.18 m (11.15) | 5.2 m / -87 deg | 8.4 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 2.10 s: B's camera established a STOP sign detection (sign-0) (the detector judged it not relevant to its path).
- t = 4.00 s: B's camera stopped detecting STOP sign sign-0.
- t = 4.35 s: B started braking.
- t = 4.70 s: B stopped moving.
- t = 4.70 s: B came to a stop.
- t = 6.90 s: B's radar started tracking track_001, which appeared on its right.
- t = 6.90 s: B observed track_001 start closing in (already the case when first observed).
- t = 8.50 s: B observed track_001 enter its forward path corridor.
- t = 9.05 s: B observed track_001 leave its forward path corridor.
- t = 10.45 s: B released the brake.
- t = 10.55 s: B's time-to-contact with track_001 became critical.
- t = 10.85 s: B's time-to-contact with track_001 stopped being critical.
- t = 10.85 s: B left its stop.
- t = 10.85 s: B started moving.
- t = 11.15 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
