# Reconstruction report - S13/run_0_accelerates_into_gap

Inputs: `vehicles/A/`, `vehicles/B/` (vehicle-local files) and the supplied `incident_context.json`. `ground_truth/` and the run's `metadata.json` were not read; the privileged comparison, if run, is in `evaluation/`.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

Pipeline: raw log -> local trace -> local graph (each recorder alone, own clock, own frame) -> graph-level alignment -> identity association -> global graph.

## Local reconstructions

| Recorder | Duration (local) | Trace frames | Graph nodes | Graph edges | Radar tracks | Collision reports (local time) |
|----------|-----------------:|-------------:|------------:|------------:|-------------:|-------------------------------|
| A | 9.95 s | 101 | 25 | 53 | 2 | A:e12 @ 5.65 s |
| B | 9.95 s | 101 | 62 | 226 | 16 | B:e03 @ 5.65 s |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e12 | 5.65 | -5.65 | reported the reference collision collision_001 |
| B | ALIGNED | B:e03 | 5.65 | -5.65 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 5215.85 vs 5215.85 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 5.65 s before the matched collision<br>not at the contact: last seen 4.65 s before the matched collision (window 0.50 s)<br>speed not comparable with B's own speed before the collision |
| A:track_002 | B | ASSOCIATED | 0.93 | A and B both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked for 2.30 s before the matched collision<br>at the contact: minimum range 1.35 m in the last 0.50 s before the collision<br>the only track of A at the contact<br>track speed agrees with B's own speed: RMSE 0.58 m/s over 2.3 s |
| B:track_001 | B:track_001 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_002 | B:track_002 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.30 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_003 | B:track_003 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.35 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_004 | B:track_004 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.35 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_005 | B:track_005 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.55 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_006 | B:track_006 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.60 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_007 | B:track_007 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.65 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_008 | B:track_008 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.65 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_009 | B:track_009 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.70 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_010 | B:track_010 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.75 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_011 | B:track_011 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.80 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_012 | B:track_012 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.85 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_013 | B:track_013 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.90 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_014 | B:track_014 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.90 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_015 | B:track_015 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.95 s after the matched collision<br>speed not comparable with A's own speed before the collision |
| B:track_016 | B:track_016 | ANONYMOUS | - | B and A both reported collision_001 (peak impulse 5215.85 vs 5215.85 N*s)<br>tracked only 0.00 s before the matched collision (needs 1.00 s)<br>not at the contact: first seen 0.95 s after the matched collision<br>speed not comparable with A's own speed before the collision |

## Global graph

86 nodes, 307 edges; 1 merged node(s): g14 COLLISION(A,B) from A:e12 + B:e03.

### Event sequence (global time)

- `-5.65` MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- `-4.85` BRAKE_START(B)
- `-4.65` TRACK_LOST(A,A:track_001)
- `-3.70` STRONG_THROTTLE_START(A)
- `-2.90` STRONG_THROTTLE_END(A); SPEED_LIMIT_EXCEEDED_START(A)
- `-2.30` TRACK_APPEARED(A,B); CLOSING_START(A,B)
- `-1.85` CRITICAL_TTC_START(A,B)
- `-0.40` EGO_PATH_ENTRY(A,B)
- `+0.00` COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A); STRONG_THROTTLE_START(A); HARD_BRAKE_START(B)
- `+0.05` CRITICAL_TTC_END(A,B); STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
- `+0.15` CLOSING_END(A,B)
- `+0.30` TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001); CRITICAL_TTC_START(B,B:track_002)
- `+0.35` TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004)
- `+0.55` TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_005)
- `+0.60` TRACK_APPEARED(B,B:track_006); CLOSING_START(B,B:track_006)
- `+0.65` TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
- `+0.70` TRACK_APPEARED(B,B:track_009); CLOSING_START(B,B:track_009)
- `+0.75` TRACK_APPEARED(B,B:track_010); CLOSING_START(A,B); CLOSING_START(B,B:track_010); CRITICAL_TTC_START(A,B)
- `+0.80` TRACK_APPEARED(B,B:track_011); CLOSING_START(B,B:track_011); TRACK_LOST(B,B:track_006)
- `+0.85` TRACK_APPEARED(B,B:track_012); CLOSING_START(B,B:track_012)
- `+0.90` TRACK_APPEARED(B,B:track_013); TRACK_APPEARED(B,B:track_014); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); TRACK_LOST(B,B:track_008)
- `+0.95` TRACK_APPEARED(B,B:track_015); TRACK_APPEARED(B,B:track_016); EGO_PATH_ENTRY(B,B:track_001); EGO_PATH_ENTRY(B,B:track_004); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_016); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_009)
- `+1.00` TRACK_LOST(B,B:track_010)
- `+1.05` EGO_PATH_EXIT(B,B:track_004); TRACK_LOST(B,B:track_011)
- `+1.10` CRITICAL_TTC_END(B,B:track_002); TRACK_LOST(B,B:track_012)
- `+1.15` CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,B:track_003); TRACK_LOST(B,B:track_013)
- `+1.25` CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B)
- `+1.30` CLOSING_END(B,B:track_016); MOVING_END(A); STOP_START(A)
- `+1.35` CLOSING_END(B,B:track_002)

### What happened, in plain language

- 5.65 s before the matched collision, A started moving (already the case when first observed).
- 5.65 s before the matched collision, B started moving (already the case when first observed).
- 5.65 s before the matched collision, A's radar started tracking unidentified object A:track_001.
- 5.65 s before the matched collision, A observed unidentified object A:track_001 start closing in (already the case when first observed).
- 4.85 s before the matched collision, B started braking.
- 4.65 s before the matched collision, A's radar lost unidentified object A:track_001.
- 3.70 s before the matched collision, A started applying strong throttle.
- 2.90 s before the matched collision, A stopped applying strong throttle.
- 2.90 s before the matched collision, A began exceeding the speed limit.
- 2.30 s before the matched collision, A's radar started tracking B.
- 2.30 s before the matched collision, A observed B start closing in (already the case when first observed).
- 1.85 s before the matched collision, A's time-to-contact with B became critical.
- 0.40 s before the matched collision, A observed B enter its forward path corridor.
- At the matched collision, A and B both recorded this same collision (peak impulses A: 5216, B: 5216 N*s).
- At the matched collision, A returned within the speed limit.
- At the matched collision, A started applying strong throttle.
- At the matched collision, B started braking hard.
- 0.05 s after the matched collision, A's time-to-contact with B stopped being critical.
- 0.05 s after the matched collision, A stopped applying strong throttle.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, A started braking hard.
- 0.15 s after the matched collision, A observed B stop closing in.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_001.
- 0.30 s after the matched collision, B's radar started tracking unidentified object B:track_002.
- 0.30 s after the matched collision, B observed unidentified object B:track_001 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B observed unidentified object B:track_002 start closing in (already the case when first observed).
- 0.30 s after the matched collision, B's time-to-contact with unidentified object B:track_001 became critical (already the case when first observed).
- 0.30 s after the matched collision, B's time-to-contact with unidentified object B:track_002 became critical (already the case when first observed).
- 0.35 s after the matched collision, B's radar started tracking unidentified object B:track_003.
- 0.35 s after the matched collision, B's radar started tracking unidentified object B:track_004.
- 0.35 s after the matched collision, B observed unidentified object B:track_003 start closing in (already the case when first observed).
- 0.35 s after the matched collision, B observed unidentified object B:track_004 start closing in (already the case when first observed).
- 0.55 s after the matched collision, B's radar started tracking unidentified object B:track_005.
- 0.55 s after the matched collision, B observed unidentified object B:track_005 start closing in (already the case when first observed).
- 0.60 s after the matched collision, B's radar started tracking unidentified object B:track_006.
- 0.60 s after the matched collision, B observed unidentified object B:track_006 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_007.
- 0.65 s after the matched collision, B's radar started tracking unidentified object B:track_008.
- 0.65 s after the matched collision, B observed unidentified object B:track_007 start closing in (already the case when first observed).
- 0.65 s after the matched collision, B observed unidentified object B:track_008 start closing in (already the case when first observed).
- 0.70 s after the matched collision, B's radar started tracking unidentified object B:track_009.
- 0.70 s after the matched collision, B observed unidentified object B:track_009 start closing in (already the case when first observed).
- 0.75 s after the matched collision, B's radar started tracking unidentified object B:track_010.
- 0.75 s after the matched collision, A observed B start closing in.
- 0.75 s after the matched collision, B observed unidentified object B:track_010 start closing in (already the case when first observed).
- 0.75 s after the matched collision, A's time-to-contact with B became critical.
- 0.80 s after the matched collision, B's radar started tracking unidentified object B:track_011.
- 0.80 s after the matched collision, B observed unidentified object B:track_011 start closing in (already the case when first observed).
- 0.80 s after the matched collision, B's radar lost unidentified object B:track_006.
- 0.85 s after the matched collision, B's radar started tracking unidentified object B:track_012.
- 0.85 s after the matched collision, B observed unidentified object B:track_012 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B's radar started tracking unidentified object B:track_013.
- 0.90 s after the matched collision, B's radar started tracking unidentified object B:track_014.
- 0.90 s after the matched collision, B observed unidentified object B:track_013 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B observed unidentified object B:track_014 start closing in (already the case when first observed).
- 0.90 s after the matched collision, B's radar lost unidentified object B:track_008.
- 0.95 s after the matched collision, B's radar started tracking unidentified object B:track_015.
- 0.95 s after the matched collision, B's radar started tracking unidentified object B:track_016.
- 0.95 s after the matched collision, B observed unidentified object B:track_001 enter its forward path corridor.
- 0.95 s after the matched collision, B observed unidentified object B:track_004 enter its forward path corridor.
- 0.95 s after the matched collision, B observed unidentified object B:track_015 start closing in (already the case when first observed).
- 0.95 s after the matched collision, B observed unidentified object B:track_016 start closing in (already the case when first observed).
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_007.
- 0.95 s after the matched collision, B's radar lost unidentified object B:track_009.
- 1.00 s after the matched collision, B's radar lost unidentified object B:track_010.
- 1.05 s after the matched collision, B observed unidentified object B:track_004 leave its forward path corridor.
- 1.05 s after the matched collision, B's radar lost unidentified object B:track_011.
- 1.10 s after the matched collision, B's time-to-contact with unidentified object B:track_002 stopped being critical.
- 1.10 s after the matched collision, B's radar lost unidentified object B:track_012.
- 1.15 s after the matched collision, B's time-to-contact with unidentified object B:track_001 stopped being critical.
- 1.15 s after the matched collision, B observed unidentified object B:track_003 enter its forward path corridor.
- 1.15 s after the matched collision, B's radar lost unidentified object B:track_013.
- 1.25 s after the matched collision, A's time-to-contact with B stopped being critical.
- 1.25 s after the matched collision, A observed B stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_001 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_003 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_004 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_005 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_014 stop closing in.
- 1.25 s after the matched collision, B observed unidentified object B:track_015 stop closing in.
- 1.25 s after the matched collision, B stopped moving.
- 1.25 s after the matched collision, B came to a stop.
- 1.30 s after the matched collision, B observed unidentified object B:track_016 stop closing in.
- 1.30 s after the matched collision, A stopped moving.
- 1.30 s after the matched collision, A came to a stop.
- 1.35 s after the matched collision, B observed unidentified object B:track_002 stop closing in.

### Simultaneous events (order unresolved at 0.05 s)

- MOVING_START(A); MOVING_START(B); TRACK_APPEARED(A,A:track_001); CLOSING_START(A,A:track_001)
- STRONG_THROTTLE_END(A); SPEED_LIMIT_EXCEEDED_START(A)
- TRACK_APPEARED(A,B); CLOSING_START(A,B)
- COLLISION(A,B); SPEED_LIMIT_EXCEEDED_END(A); STRONG_THROTTLE_START(A); HARD_BRAKE_START(B)
- CRITICAL_TTC_END(A,B); STRONG_THROTTLE_END(A); BRAKE_START(A); HARD_BRAKE_START(A)
- TRACK_APPEARED(B,B:track_001); TRACK_APPEARED(B,B:track_002); CLOSING_START(B,B:track_001); CLOSING_START(B,B:track_002); CRITICAL_TTC_START(B,B:track_001); CRITICAL_TTC_START(B,B:track_002)
- TRACK_APPEARED(B,B:track_003); TRACK_APPEARED(B,B:track_004); CLOSING_START(B,B:track_003); CLOSING_START(B,B:track_004)
- TRACK_APPEARED(B,B:track_005); CLOSING_START(B,B:track_005)
- TRACK_APPEARED(B,B:track_006); CLOSING_START(B,B:track_006)
- TRACK_APPEARED(B,B:track_007); TRACK_APPEARED(B,B:track_008); CLOSING_START(B,B:track_007); CLOSING_START(B,B:track_008)
- TRACK_APPEARED(B,B:track_009); CLOSING_START(B,B:track_009)
- TRACK_APPEARED(B,B:track_010); CLOSING_START(A,B); CLOSING_START(B,B:track_010); CRITICAL_TTC_START(A,B)
- TRACK_APPEARED(B,B:track_011); CLOSING_START(B,B:track_011); TRACK_LOST(B,B:track_006)
- TRACK_APPEARED(B,B:track_012); CLOSING_START(B,B:track_012)
- TRACK_APPEARED(B,B:track_013); TRACK_APPEARED(B,B:track_014); CLOSING_START(B,B:track_013); CLOSING_START(B,B:track_014); TRACK_LOST(B,B:track_008)
- TRACK_APPEARED(B,B:track_015); TRACK_APPEARED(B,B:track_016); EGO_PATH_ENTRY(B,B:track_001); EGO_PATH_ENTRY(B,B:track_004); CLOSING_START(B,B:track_015); CLOSING_START(B,B:track_016); TRACK_LOST(B,B:track_007); TRACK_LOST(B,B:track_009)
- EGO_PATH_EXIT(B,B:track_004); TRACK_LOST(B,B:track_011)
- CRITICAL_TTC_END(B,B:track_002); TRACK_LOST(B,B:track_012)
- CRITICAL_TTC_END(B,B:track_001); EGO_PATH_ENTRY(B,B:track_003); TRACK_LOST(B,B:track_013)
- CRITICAL_TTC_END(A,B); CLOSING_END(A,B); CLOSING_END(B,B:track_001); CLOSING_END(B,B:track_003); CLOSING_END(B,B:track_004); CLOSING_END(B,B:track_005); CLOSING_END(B,B:track_014); CLOSING_END(B,B:track_015); MOVING_END(B); STOP_START(B)
- CLOSING_END(B,B:track_016); MOVING_END(A); STOP_START(A)

### States still active when observation ended

A:
- CLOSING of track_001, since A:e03 (t = 0.00 s); the track was lost at 1.00 s
- EGO_PATH of track_002, since A:e11 (t = 5.25 s)
- BRAKE, since A:e17 (t = 5.70 s)
- HARD_BRAKE, since A:e18 (t = 5.70 s)
- STOP, since A:e25 (t = 6.95 s)
B:
- BRAKE, since B:e02 (t = 0.80 s)
- HARD_BRAKE, since B:e04 (t = 5.65 s)
- CLOSING of track_006, since B:e18 (t = 6.25 s); the track was lost at 6.45 s
- CLOSING of track_007, since B:e21 (t = 6.30 s); the track was lost at 6.60 s
- CLOSING of track_008, since B:e22 (t = 6.30 s); the track was lost at 6.55 s
- CLOSING of track_009, since B:e24 (t = 6.35 s); the track was lost at 6.60 s
- CLOSING of track_010, since B:e26 (t = 6.40 s); the track was lost at 6.65 s
- CLOSING of track_011, since B:e28 (t = 6.45 s); the track was lost at 6.70 s
- CLOSING of track_012, since B:e31 (t = 6.50 s); the track was lost at 6.75 s
- CLOSING of track_013, since B:e34 (t = 6.55 s); the track was lost at 6.80 s
- EGO_PATH of track_001, since B:e39 (t = 6.60 s)
- EGO_PATH of track_003, since B:e51 (t = 6.80 s)
- STOP, since B:e60 (t = 6.90 s)

### Sign detection windows

A:
- none
B:
- none

## Uncertainty and limitations

- A:track_001 stays anonymous: not at the contact: last seen 4.65 s before the matched collision (window 0.50 s); speed not comparable with B's own speed before the collision.
- B:track_001 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.30 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_002 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.30 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_003 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.35 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_004 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.35 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_005 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.55 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_006 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.60 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_007 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.65 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_008 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.65 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_009 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.70 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_010 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.75 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_011 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.80 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_012 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.85 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_013 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.90 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_014 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.90 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_015 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.95 s after the matched collision; speed not comparable with A's own speed before the collision.
- B:track_016 stays anonymous: tracked only 0.00 s before the matched collision (needs 1.00 s); not at the contact: first seen 0.95 s after the matched collision; speed not comparable with A's own speed before the collision.
- Global time rests on one collision anchor and a constant offset per recorder; clock drift is not modelled, so timing uncertainty grows away from t_global = 0.
- Radar tracks follow the visible surface of an object, not its centre, and a straight-ahead corridor is used for 'in path'.

## Files

- Local: `<recorder>/local_trace.jsonl`, `local_tracks.jsonl`, `local_graph.json|md|dot`
- Global: `global/alignment.json`, `associations.json`, `global_trace.jsonl`, `global_graph.json|md|dot`

## Parameters

```
{
  "trace_hz": 10.0,
  "collision": {
    "merge_gap_s": 0.5
  },
  "tracking": {
    "min_height_m": 0.3,
    "max_height_m": 2.5,
    "moving_speed_mps": 1.0,
    "cluster_distance_m": 2.0,
    "max_association_distance_m": 2.5,
    "max_velocity_mismatch_mps": 4.0,
    "max_track_gap_s": 0.5,
    "min_track_frames": 5,
    "measurement_std_m": 0.5,
    "radial_speed_std_mps": 0.3,
    "acceleration_std_mps2": 6.0
  },
  "semantics": {
    "brake_onset_threshold": 0.1,
    "hard_brake_threshold": 0.9,
    "strong_throttle_threshold": 0.8,
    "full_stop_speed_mps": 0.3,
    "speed_limit_hysteresis_kmh": 1.0,
    "closing_speed_threshold_mps": 1.0,
    "critical_ttc_s": 2.0,
    "path_half_width_m": 1.5
  },
  "fusion": {
    "impulse_tolerance": 0.1,
    "contact_window_s": 0.5,
    "contact_range_m": 3.5,
    "min_track_persistence_s": 1.0,
    "speed_consistency_mps": 1.5
  }
}
```
