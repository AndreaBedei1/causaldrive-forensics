# Local graph - vehicle B

All times are B's own local clock: `t_local` = seconds since B's first ego sample (raw clock reading 56.33916341140866 at `t_local` = 0). Only files under `vehicles/B/` were read; external objects are anonymous radar tracks.

- Local frame: origin = first ego position; x = first heading; y = to the right of the first heading (CARLA convention)
- Trace: 153 frames at 10 Hz in `local_trace.jsonl`, the last one at the recording end (15.15 s)
- Anonymous radar tracks: 0 (10 Hz samples in `local_tracks.jsonl`)
- Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.
- Nodes: 5; edges: 4 (PRECEDES 4)

## Nodes

| Id | Local time | Type | Actor | Subject | Source | Details |
|----|-----------:|------|-------|---------|--------|---------|
| B:e01 | 0.00 | MOVING_START | B | - | ego | active_at_first_observation=True |
| B:e02 | 0.35 | STRONG_THROTTLE_START | B | - | controls |  |
| B:e03 | 1.30 | STRONG_THROTTLE_END | B | - | controls |  |
| B:e04 | 3.15 | BRAKE_START | B | - | controls |  |
| B:e05 | 3.60 | BRAKE_END | B | - | controls |  |

Events are state transitions; the quantities behind them (speed, pedals, ranges, TTC, relative motion, closest approach) are facts in `local_trace.jsonl`. Events with equal times are simultaneous at the recorder's resolution: PRECEDES links only different times. SAME_TRACK links a track's TRACK_APPEARED_* to every other event about the same local track (grouping only, no order).

## Edges

```
    B:e01 --PRECEDES--> B:e02
    B:e02 --PRECEDES--> B:e03
    B:e03 --PRECEDES--> B:e04
    B:e04 --PRECEDES--> B:e05
```

## Perceived state before each event

Each row is the state just BEFORE its events (none of them applied): events at one time are simultaneous and share it. True states are named, unknown ones end with `?`, false ones are omitted; a lost track's states are UNKNOWN, never ended. Facts: the trace frame at the time shown.

| Local time | Events | Perceived state just before | Facts at |
|-----------:|--------|-----------------------------|---------:|
| 0.00 | B:e01 MOVING_START | ego: not yet observed | - |
| 0.35 | B:e02 STRONG_THROTTLE_START | ego: MOVING | 0.30 |
| 1.30 | B:e03 STRONG_THROTTLE_END | ego: MOVING, STRONG_THROTTLE | 1.20 |
| 3.15 | B:e04 BRAKE_START | ego: MOVING | 3.10 |
| 3.60 | B:e05 BRAKE_END | ego: MOVING, BRAKE | 3.50 |

## States still active when observation ended

- MOVING, since B:e01 (t = 0.00 s)

## Tracks lost

- no track was lost

## Sign detection windows

- none

An END means this recorder stopped detecting the sign, not that its obligation ended.

## Anonymous radar tracks

No radar track: nothing moving stayed in B's forward radar view long enough.

## Plain-language reading

- t = 0.00 s: B started moving (already the case when first observed).
- t = 0.35 s: B started applying strong throttle.
- t = 1.30 s: B stopped applying strong throttle.
- t = 3.15 s: B started braking.
- t = 3.60 s: B released the brake.
