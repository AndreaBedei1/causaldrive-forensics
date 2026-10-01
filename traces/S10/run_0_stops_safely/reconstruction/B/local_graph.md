# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 265.36246832087636 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 97 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (9.55 s)
- Anonymous radar tracks: 1 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 9; edges: 12 (PRECEDES 9, SAME_TRACK 3)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 1.20 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.80 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 2.55 | TRACK_APPEARED_RIGHT | B | track_001 | radar |  |
| B:e05 | 2.55 | CLOSING_START | B | track_001 | radar | active_at_first_observation=True |
| B:e06 | 4.30 | CRITICAL_TTC_START | B | track_001 | radar |  |
| B:e07 | 5.50 | TRACK_LOST | B | track_001 | radar |  |
| B:e08 | 7.55 | STOP_SIGN_DETECTED_START | B | sign-1 | camera | relevant_to_ego_path=False |
| B:e09 | 7.75 | STOP_SIGN_DETECTED_END | B | sign-1 | camera |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e03 --PRECEDES--> B:e05
    B:e04 --PRECEDES--> B:e06
    B:e05 --PRECEDES--> B:e06
    B:e06 --PRECEDES--> B:e07
    B:e07 --PRECEDES--> B:e08
    B:e08 --PRECEDES--> B:e09
    B:e04 --SAME_TRACK--> B:e05
    B:e04 --SAME_TRACK--> B:e06
    B:e04 --SAME_TRACK--> B:e07
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 1.20 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 1.10 |
| 1.80 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.70 |
| 2.55 | B:e04 TRACK_APPEARED_RIGHT track_001<br>B:e05 CLOSING_START track_001 | ego: MOVING | 2.50 |
| 4.30 | B:e06 CRITICAL_TTC_START track_001 | ego: MOVING<br>track_001: CLOSING | 4.20 |
| 5.50 | B:e07 TRACK_LOST track_001 | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC | 5.40 |
| 7.55 | B:e08 STOP_SIGN_DETECTED_START sign-1 | ego: MOVING<br>track lost, states UNKNOWN: track_001 | 7.50 |
| 7.75 | B:e09 STOP_SIGN_DETECTED_END sign-1 | ego: MOVING<br>track lost, states UNKNOWN: track_001<br>sign-1: STOP sign known | 7.70 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)
- CLOSING of track_001, since B:e05 (t = 2.55 s); the track was lost at 5.50 s
- CRITICAL_TTC of track_001, since B:e06 (t = 4.30 s); the track was lost at 5.50 s

## Tracks lost

- track_001 at 5.50 s (B:e07): CLOSING, CRITICAL_TTC were true; they are UNKNOWN afterwards (no END recorded)

## Sign detection windows

- STOP sign sign-1: detected 7.55 s -> 7.75 s; relevant to the path: False; STOP_START inside: none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

| Track | First seen | Last seen | Measured sweeps | First range / bearing | Min range (at) | Last range / bearing | Max speed |
|-------|-----------:|----------:|----------------:|----------------------|----------------|---------------------|----------:|
| track_001 | 2.55 | 5.50 | 59 | 35.4 m / +20 deg | 8.35 m (5.50) | 8.3 m / +60 deg | 5.1 m/s |

Bearing: positive = to B's right. Ranges are measured from the radar to the visible surface of the object.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 1.20 s: B started applying strong throttle.
- t = 1.80 s: B stopped applying strong throttle.
- t = 2.55 s: B's radar started tracking track_001, which appeared on its right.
- t = 2.55 s: B observed track_001 start closing in (already the case when first observed).
- t = 4.30 s: B's time-to-contact with track_001 became critical.
- t = 5.50 s: B's radar lost track_001 (its states are UNKNOWN from then on, not ended).
- t = 7.55 s: B's camera established a STOP sign detection (sign-1) (the detector judged it not relevant to its path).
- t = 7.75 s: B's camera stopped detecting STOP sign sign-1.
