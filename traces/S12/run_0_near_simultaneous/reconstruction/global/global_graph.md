# Global graph - S12/run_0_near_simultaneous

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock ALIGNED; observed by others as: B:track_001 |
| B | recorder | clock ALIGNED; observed by others as: A:track_001 |
| A:track_002 | anonymous_track | seen only by A; candidate: B |
| A:track_003 | anonymous_track | seen only by A; candidate: B |
| A:track_004 | anonymous_track | seen only by A; candidate: B |
| A:track_005 | anonymous_track | seen only by A; candidate: B |
| A:track_006 | anonymous_track | seen only by A; candidate: B |
| A:track_007 | anonymous_track | seen only by A; candidate: B |
| A:track_008 | anonymous_track | seen only by A; candidate: B |
| A:track_009 | anonymous_track | seen only by A; candidate: B |
| A:track_010 | anonymous_track | seen only by A; candidate: B |
| A:track_011 | anonymous_track | seen only by A; candidate: B |
| A:track_012 | anonymous_track | seen only by A; candidate: B |
| A:track_013 | anonymous_track | seen only by A; candidate: B |
| A:track_014 | anonymous_track | seen only by A; candidate: B |
| A:track_015 | anonymous_track | seen only by A; candidate: B |
| A:track_016 | anonymous_track | seen only by A; candidate: B |
| A:track_017 | anonymous_track | seen only by A; candidate: B |
| A:track_018 | anonymous_track | seen only by A; candidate: B |
| A:track_019 | anonymous_track | seen only by A; candidate: B |

## Graph alignment

Reference event: `collision_001`; `t_global = t_local + offset_to_global`.

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | ALIGNED | A:e44 | 9.50 | -9.50 | reported the reference collision collision_001 |
| B | ALIGNED | B:e18 | 9.50 | -9.50 | reported the reference collision collision_001 |

Estimated relative clock offsets: B - A = +0.000 s

Matched `collision_001`: A and B both recorded a collision; peak impulses 4032.49 vs 4032.49 N*s (similarity 1.000, tolerance 0.10); no competing report within tolerance

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | B | ASSOCIATED | 0.90 | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 7.05 s before the matched collision<br>continuous up to the contact: last observed 0.35 s before it (window 0.50 s)<br>approaching before the contact: range 16.8 m -> 4.6 m over the last 1.0 s<br>track speed agrees with B's own speed: RMSE 0.43 m/s over 2.7 s<br>range at the contact 4.63 m (beyond 3.50 m: confidence factor 0.93)<br>the only track of A compatible with the contact |
| A:track_002 | A:track_002 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 68.5 m -> 64.7 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.09 m/s over 0.7 s (> 1.50)<br>range at the contact 64.74 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_003 | A:track_003 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 45.3 m -> 41.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.35 m/s over 0.7 s (> 1.50)<br>range at the contact 41.89 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_004 | A:track_004 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 40.8 m -> 37.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.25 m/s over 0.7 s (> 1.50)<br>range at the contact 37.45 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_005 | A:track_005 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 96.6 m -> 93.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.61 m/s over 0.7 s (> 1.50)<br>range at the contact 93.37 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_006 | A:track_006 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 57.8 m -> 54.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50)<br>range at the contact 54.52 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_007 | A:track_007 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 50.0 m -> 46.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.81 m/s over 0.7 s (> 1.50)<br>range at the contact 46.85 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_008 | A:track_008 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 53.6 m -> 50.4 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.77 m/s over 0.7 s (> 1.50)<br>range at the contact 50.36 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_009 | A:track_009 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.60 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 35.9 m -> 32.9 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 7.67 m/s over 0.6 s (> 1.50)<br>range at the contact 32.92 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_010 | A:track_010 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.70 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 93.2 m -> 88.8 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 5.58 m/s over 0.7 s (> 1.50)<br>range at the contact 88.83 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_011 | A:track_011 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.20 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 25.8 m -> 24.5 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 6.33 m/s over 0.2 s (> 1.50)<br>range at the contact 24.51 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_012 | A:track_012 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.15 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>not approaching before the contact: range 12.9 m -> 13.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 12.91 m (beyond 3.50 m: confidence factor 0.01) |
| A:track_013 | A:track_013 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.65 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 87.1 m -> 83.0 m over the last 1.0 s<br>track speed disagrees with B's own speed: RMSE 8.61 m/s over 0.7 s (> 1.50)<br>range at the contact 82.97 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_014 | A:track_014 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.10 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 87.4 m -> 86.5 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 86.50 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_015 | A:track_015 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 9.78 m (beyond 3.50 m: confidence factor 0.11) |
| A:track_016 | A:track_016 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.05 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 18.6 m -> 18.2 m over the last 1.0 s<br>speed not comparable with B's own speed before the collision<br>range at the contact 18.17 m (beyond 3.50 m: confidence factor 0.00) |
| A:track_017 | A:track_017 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision<br>range at the contact 12.72 m (beyond 3.50 m: confidence factor 0.01) |
| A:track_018 | A:track_018 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| A:track_019 | A:track_019 | ANONYMOUS | - | A and B both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 0.00 s before the matched collision (needs 1.00 s)<br>first seen 0.05 s after the matched collision<br>range trend before the contact not measurable<br>speed not comparable with B's own speed before the collision |
| B:track_001 | A | ASSOCIATED | 0.69 | B and A both reported collision_001 (peak impulse 4032.49 vs 4032.49 N*s)<br>tracked for 6.95 s before the matched collision<br>continuous up to the contact: last observed 0.00 s before it (window 0.50 s)<br>approaching before the contact: range 12.5 m -> 1.2 m over the last 1.0 s<br>track speed agrees with A's own speed: RMSE 1.30 m/s over 3.0 s<br>range at the contact 1.09 m<br>the only track of B compatible with the contact |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | -9.50 | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | -9.50 | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g03 | -8.80 | STOP_SIGN_DETECTED_START | A | A:sign-0 | A:e02 @ 0.70 | relevant_to_ego_path=True |
| g04 | -7.70 | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e02 @ 1.80 | relevant_to_ego_path=True |
| g05 | -7.20 | STOP_SIGN_DETECTED_END | A | A:sign-0 | A:e03 @ 2.30 |  |
| g06 | -7.05 | TRACK_APPEARED_LEFT | A | B | A:e04 @ 2.45 |  |
| g07 | -7.05 | CLOSING_START | A | B | A:e05 @ 2.45 | active_at_first_observation=True |
| g08 | -6.95 | TRACK_APPEARED_RIGHT | B | A | B:e03 @ 2.55 |  |
| g09 | -6.95 | CLOSING_START | B | A | B:e04 @ 2.55 | active_at_first_observation=True |
| g10 | -6.90 | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e05 @ 2.60 |  |
| g11 | -6.85 | BRAKE_START | A | - | A:e06 @ 2.65 |  |
| g12 | -6.75 | BRAKE_START | B | - | B:e06 @ 2.75 |  |
| g13 | -6.10 | MOVING_END | A | - | A:e07 @ 3.40 |  |
| g14 | -6.10 | STOP_START | A | - | A:e08 @ 3.40 |  |
| g15 | -6.00 | CLOSING_END | A | B | A:e09 @ 3.50 |  |
| g16 | -6.00 | CLOSING_END | B | A | B:e07 @ 3.50 |  |
| g17 | -6.00 | MOVING_END | B | - | B:e08 @ 3.50 |  |
| g18 | -6.00 | STOP_START | B | - | B:e09 @ 3.50 |  |
| g19 | -2.55 | BRAKE_END | A | - | A:e10 @ 6.95 |  |
| g20 | -2.55 | BRAKE_END | B | - | B:e10 @ 6.95 |  |
| g21 | -2.20 | STOP_END | A | - | A:e11 @ 7.30 |  |
| g22 | -2.20 | MOVING_START | A | - | A:e12 @ 7.30 |  |
| g23 | -2.20 | CLOSING_START | A | B | A:e13 @ 7.30 |  |
| g24 | -2.20 | CLOSING_START | B | A | B:e11 @ 7.30 |  |
| g25 | -2.15 | STOP_END | B | - | B:e12 @ 7.35 |  |
| g26 | -2.15 | MOVING_START | B | - | B:e13 @ 7.35 |  |
| g27 | -1.20 | TURN_LEFT_START | A | - | A:e14 @ 8.30 |  |
| g28 | -1.20 | CRITICAL_TTC_START | A | B | A:e15 @ 8.30 |  |
| g29 | -1.20 | CRITICAL_TTC_START | B | A | B:e14 @ 8.30 |  |
| g30 | -0.70 | TRACK_APPEARED_LEFT | A | A:track_002 | A:e16 @ 8.80 |  |
| g31 | -0.70 | TRACK_APPEARED_LEFT | A | A:track_005 | A:e17 @ 8.80 |  |
| g32 | -0.70 | TRACK_APPEARED_LEFT | A | A:track_010 | A:e18 @ 8.80 |  |
| g33 | -0.70 | CLOSING_START | A | A:track_002 | A:e19 @ 8.80 | active_at_first_observation=True |
| g34 | -0.70 | CLOSING_START | A | A:track_005 | A:e20 @ 8.80 | active_at_first_observation=True |
| g35 | -0.70 | CLOSING_START | A | A:track_010 | A:e21 @ 8.80 | active_at_first_observation=True |
| g36 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_003 | A:e22 @ 8.85 |  |
| g37 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_004 | A:e23 @ 8.85 |  |
| g38 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_006 | A:e24 @ 8.85 |  |
| g39 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_007 | A:e25 @ 8.85 |  |
| g40 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_008 | A:e26 @ 8.85 |  |
| g41 | -0.65 | TRACK_APPEARED_LEFT | A | A:track_013 | A:e27 @ 8.85 |  |
| g42 | -0.65 | CLOSING_START | A | A:track_003 | A:e28 @ 8.85 | active_at_first_observation=True |
| g43 | -0.65 | CLOSING_START | A | A:track_004 | A:e29 @ 8.85 | active_at_first_observation=True |
| g44 | -0.65 | CLOSING_START | A | A:track_006 | A:e30 @ 8.85 | active_at_first_observation=True |
| g45 | -0.65 | CLOSING_START | A | A:track_007 | A:e31 @ 8.85 | active_at_first_observation=True |
| g46 | -0.65 | CLOSING_START | A | A:track_008 | A:e32 @ 8.85 | active_at_first_observation=True |
| g47 | -0.65 | CLOSING_START | A | A:track_013 | A:e33 @ 8.85 | active_at_first_observation=True |
| g48 | -0.60 | TRACK_APPEARED_LEFT | A | A:track_009 | A:e34 @ 8.90 |  |
| g49 | -0.60 | CLOSING_START | A | A:track_009 | A:e35 @ 8.90 | active_at_first_observation=True |
| g50 | -0.55 | EGO_PATH_ENTRY | B | A | B:e15 @ 8.95 |  |
| g51 | -0.35 | TRACK_LOST | A | B | A:e36 @ 9.15 |  |
| g52 | -0.20 | TRACK_APPEARED_LEFT | A | A:track_011 | A:e37 @ 9.30 |  |
| g53 | -0.20 | CLOSING_START | A | A:track_011 | A:e38 @ 9.30 | active_at_first_observation=True |
| g54 | -0.15 | TRACK_APPEARED_RIGHT | A | A:track_012 | A:e39 @ 9.35 |  |
| g55 | -0.10 | TRACK_APPEARED_LEFT | A | A:track_014 | A:e40 @ 9.40 |  |
| g56 | -0.10 | CLOSING_START | A | A:track_014 | A:e41 @ 9.40 | active_at_first_observation=True |
| g57 | -0.05 | CRITICAL_TTC_END | B | A | B:e16 @ 9.45 |  |
| g58 | -0.05 | CLOSING_END | B | A | B:e17 @ 9.45 |  |
| g59 | -0.05 | TRACK_APPEARED_LEFT | A | A:track_016 | A:e42 @ 9.45 |  |
| g60 | -0.05 | CLOSING_START | A | A:track_016 | A:e43 @ 9.45 | active_at_first_observation=True |
| g61 | 0.00 | COLLISION | - | A, B | A:e44 @ 9.50, B:e18 @ 9.50 | matched_event=collision_001; reference_event=True; peak_impulse=A 4032.49, B 4032.49 |
| g62 | 0.00 | TRACK_APPEARED_FRONT | A | A:track_017 | A:e45 @ 9.50 |  |
| g63 | 0.00 | TRACK_APPEARED_RIGHT | A | A:track_015 | A:e46 @ 9.50 |  |
| g64 | 0.00 | CLOSING_START | A | A:track_017 | A:e47 @ 9.50 | active_at_first_observation=True |
| g65 | 0.05 | EGO_PATH_EXIT | A | A:track_017 | A:e48 @ 9.55 |  |
| g66 | 0.05 | EGO_PATH_EXIT | B | A | B:e19 @ 9.55 |  |
| g67 | 0.05 | BRAKE_START | A | - | A:e49 @ 9.55 |  |
| g68 | 0.05 | BRAKE_START | B | - | B:e20 @ 9.55 |  |
| g69 | 0.05 | TRACK_APPEARED_LEFT | A | A:track_018 | A:e50 @ 9.55 |  |
| g70 | 0.05 | TRACK_APPEARED_RIGHT | A | A:track_019 | A:e51 @ 9.55 |  |
| g71 | 0.05 | CLOSING_START | A | A:track_018 | A:e52 @ 9.55 | active_at_first_observation=True |
| g72 | 0.05 | CLOSING_START | A | A:track_019 | A:e53 @ 9.55 | active_at_first_observation=True |
| g73 | 0.05 | TRACK_LOST | A | A:track_012 | A:e54 @ 9.55 |  |
| g74 | 0.20 | CLOSING_START | A | A:track_015 | A:e55 @ 9.70 |  |
| g75 | 0.25 | TRACK_LOST | B | A | B:e21 @ 9.75 |  |
| g76 | 0.45 | MOVING_END | B | - | B:e22 @ 9.95 |  |
| g77 | 0.45 | STOP_START | B | - | B:e23 @ 9.95 |  |
| g78 | 0.50 | CLOSING_END | A | A:track_002 | A:e56 @ 10.00 |  |
| g79 | 0.50 | CLOSING_END | A | A:track_005 | A:e57 @ 10.00 |  |
| g80 | 0.50 | CLOSING_END | A | A:track_008 | A:e58 @ 10.00 |  |
| g81 | 0.50 | CLOSING_END | A | A:track_015 | A:e59 @ 10.00 |  |
| g82 | 0.50 | CLOSING_END | A | A:track_017 | A:e60 @ 10.00 |  |
| g83 | 0.50 | CLOSING_END | A | A:track_018 | A:e61 @ 10.00 |  |
| g84 | 0.50 | CLOSING_END | A | A:track_019 | A:e62 @ 10.00 |  |
| g85 | 0.50 | TURN_LEFT_END | A | - | A:e63 @ 10.00 |  |
| g86 | 0.50 | MOVING_END | A | - | A:e64 @ 10.00 |  |
| g87 | 0.50 | STOP_START | A | - | A:e65 @ 10.00 |  |
| g88 | 0.50 | TRACK_LOST | A | A:track_019 | A:e66 @ 10.00 |  |
| g89 | 0.55 | CLOSING_END | A | A:track_003 | A:e67 @ 10.05 |  |
| g90 | 0.55 | CLOSING_END | A | A:track_004 | A:e68 @ 10.05 |  |
| g91 | 0.55 | CLOSING_END | A | A:track_007 | A:e69 @ 10.05 |  |
| g92 | 0.55 | CLOSING_END | A | A:track_009 | A:e70 @ 10.05 |  |
| g93 | 0.55 | CLOSING_END | A | A:track_010 | A:e71 @ 10.05 |  |
| g94 | 0.55 | CLOSING_END | A | A:track_011 | A:e72 @ 10.05 |  |
| g95 | 0.55 | CLOSING_END | A | A:track_013 | A:e73 @ 10.05 |  |
| g96 | 0.55 | CLOSING_END | A | A:track_014 | A:e74 @ 10.05 |  |
| g97 | 0.55 | CLOSING_END | A | A:track_016 | A:e75 @ 10.05 |  |
| g98 | 0.60 | CLOSING_END | A | A:track_006 | A:e76 @ 10.10 |  |
| g99 | 1.50 | STOP_SIGN_DETECTED_START | A | A:sign-1 | A:e77 @ 11.00 | relevant_to_ego_path=False |
| g100 | 3.10 | TRACK_LOST | A | A:track_006 | A:e78 @ 12.60 |  |
| g101 | 4.85 | TRACK_LOST | A | A:track_018 | A:e79 @ 14.35 |  |
| g102 | 5.35 | TRACK_LOST | A | A:track_005 | A:e80 @ 14.85 |  |
| g103 | 5.40 | TRACK_LOST | A | A:track_008 | A:e81 @ 14.90 |  |

## Edges

```
    g01 --PRECEDES--> g03
    g02 --PRECEDES--> g03
    g03 --PRECEDES--> g04
    g04 --PRECEDES--> g05
    g05 --PRECEDES--> g06
    g05 --PRECEDES--> g07
    g06 --PRECEDES--> g08
    g06 --PRECEDES--> g09
    g07 --PRECEDES--> g08
    g07 --PRECEDES--> g09
    g08 --PRECEDES--> g10
    g09 --PRECEDES--> g10
    g10 --PRECEDES--> g11
    g11 --PRECEDES--> g12
    g12 --PRECEDES--> g13
    g12 --PRECEDES--> g14
    g13 --PRECEDES--> g15
    g13 --PRECEDES--> g16
    g13 --PRECEDES--> g17
    g13 --PRECEDES--> g18
    g14 --PRECEDES--> g15
    g14 --PRECEDES--> g16
    g14 --PRECEDES--> g17
    g14 --PRECEDES--> g18
    g15 --PRECEDES--> g19
    g15 --PRECEDES--> g20
    g16 --PRECEDES--> g19
    g16 --PRECEDES--> g20
    g17 --PRECEDES--> g19
    g17 --PRECEDES--> g20
    g18 --PRECEDES--> g19
    g18 --PRECEDES--> g20
    g19 --PRECEDES--> g21
    g19 --PRECEDES--> g22
    g19 --PRECEDES--> g23
    g19 --PRECEDES--> g24
    g20 --PRECEDES--> g21
    g20 --PRECEDES--> g22
    g20 --PRECEDES--> g23
    g20 --PRECEDES--> g24
    g21 --PRECEDES--> g25
    g21 --PRECEDES--> g26
    g22 --PRECEDES--> g25
    g22 --PRECEDES--> g26
    g23 --PRECEDES--> g25
    g23 --PRECEDES--> g26
    g24 --PRECEDES--> g25
    g24 --PRECEDES--> g26
    g25 --PRECEDES--> g27
    g25 --PRECEDES--> g28
    g25 --PRECEDES--> g29
    g26 --PRECEDES--> g27
    g26 --PRECEDES--> g28
    g26 --PRECEDES--> g29
    g27 --PRECEDES--> g30
    g27 --PRECEDES--> g31
    g27 --PRECEDES--> g32
    g27 --PRECEDES--> g33
    g27 --PRECEDES--> g34
    g27 --PRECEDES--> g35
    g28 --PRECEDES--> g30
    g28 --PRECEDES--> g31
    g28 --PRECEDES--> g32
    g28 --PRECEDES--> g33
    g28 --PRECEDES--> g34
    g28 --PRECEDES--> g35
    g29 --PRECEDES--> g30
    g29 --PRECEDES--> g31
    g29 --PRECEDES--> g32
    g29 --PRECEDES--> g33
    g29 --PRECEDES--> g34
    g29 --PRECEDES--> g35
    g30 --PRECEDES--> g36
    g30 --PRECEDES--> g37
    g30 --PRECEDES--> g38
    g30 --PRECEDES--> g39
    g30 --PRECEDES--> g40
    g30 --PRECEDES--> g41
    g30 --PRECEDES--> g42
    g30 --PRECEDES--> g43
    g30 --PRECEDES--> g44
    g30 --PRECEDES--> g45
    g30 --PRECEDES--> g46
    g30 --PRECEDES--> g47
    g31 --PRECEDES--> g36
    g31 --PRECEDES--> g37
    g31 --PRECEDES--> g38
    g31 --PRECEDES--> g39
    g31 --PRECEDES--> g40
    g31 --PRECEDES--> g41
    g31 --PRECEDES--> g42
    g31 --PRECEDES--> g43
    g31 --PRECEDES--> g44
    g31 --PRECEDES--> g45
    g31 --PRECEDES--> g46
    g31 --PRECEDES--> g47
    g32 --PRECEDES--> g36
    g32 --PRECEDES--> g37
    g32 --PRECEDES--> g38
    g32 --PRECEDES--> g39
    g32 --PRECEDES--> g40
    g32 --PRECEDES--> g41
    g32 --PRECEDES--> g42
    g32 --PRECEDES--> g43
    g32 --PRECEDES--> g44
    g32 --PRECEDES--> g45
    g32 --PRECEDES--> g46
    g32 --PRECEDES--> g47
    g33 --PRECEDES--> g36
    g33 --PRECEDES--> g37
    g33 --PRECEDES--> g38
    g33 --PRECEDES--> g39
    g33 --PRECEDES--> g40
    g33 --PRECEDES--> g41
    g33 --PRECEDES--> g42
    g33 --PRECEDES--> g43
    g33 --PRECEDES--> g44
    g33 --PRECEDES--> g45
    g33 --PRECEDES--> g46
    g33 --PRECEDES--> g47
    g34 --PRECEDES--> g36
    g34 --PRECEDES--> g37
    g34 --PRECEDES--> g38
    g34 --PRECEDES--> g39
    g34 --PRECEDES--> g40
    g34 --PRECEDES--> g41
    g34 --PRECEDES--> g42
    g34 --PRECEDES--> g43
    g34 --PRECEDES--> g44
    g34 --PRECEDES--> g45
    g34 --PRECEDES--> g46
    g34 --PRECEDES--> g47
    g35 --PRECEDES--> g36
    g35 --PRECEDES--> g37
    g35 --PRECEDES--> g38
    g35 --PRECEDES--> g39
    g35 --PRECEDES--> g40
    g35 --PRECEDES--> g41
    g35 --PRECEDES--> g42
    g35 --PRECEDES--> g43
    g35 --PRECEDES--> g44
    g35 --PRECEDES--> g45
    g35 --PRECEDES--> g46
    g35 --PRECEDES--> g47
    g36 --PRECEDES--> g48
    g36 --PRECEDES--> g49
    g37 --PRECEDES--> g48
    g37 --PRECEDES--> g49
    g38 --PRECEDES--> g48
    g38 --PRECEDES--> g49
    g39 --PRECEDES--> g48
    g39 --PRECEDES--> g49
    g40 --PRECEDES--> g48
    g40 --PRECEDES--> g49
    g41 --PRECEDES--> g48
    g41 --PRECEDES--> g49
    g42 --PRECEDES--> g48
    g42 --PRECEDES--> g49
    g43 --PRECEDES--> g48
    g43 --PRECEDES--> g49
    g44 --PRECEDES--> g48
    g44 --PRECEDES--> g49
    g45 --PRECEDES--> g48
    g45 --PRECEDES--> g49
    g46 --PRECEDES--> g48
    g46 --PRECEDES--> g49
    g47 --PRECEDES--> g48
    g47 --PRECEDES--> g49
    g48 --PRECEDES--> g50
    g49 --PRECEDES--> g50
    g50 --PRECEDES--> g51
    g51 --PRECEDES--> g52
    g51 --PRECEDES--> g53
    g52 --PRECEDES--> g54
    g53 --PRECEDES--> g54
    g54 --PRECEDES--> g55
    g54 --PRECEDES--> g56
    g55 --PRECEDES--> g57
    g55 --PRECEDES--> g58
    g55 --PRECEDES--> g59
    g55 --PRECEDES--> g60
    g56 --PRECEDES--> g57
    g56 --PRECEDES--> g58
    g56 --PRECEDES--> g59
    g56 --PRECEDES--> g60
    g57 --PRECEDES--> g61
    g57 --PRECEDES--> g62
    g57 --PRECEDES--> g63
    g57 --PRECEDES--> g64
    g58 --PRECEDES--> g61
    g58 --PRECEDES--> g62
    g58 --PRECEDES--> g63
    g58 --PRECEDES--> g64
    g59 --PRECEDES--> g61
    g59 --PRECEDES--> g62
    g59 --PRECEDES--> g63
    g59 --PRECEDES--> g64
    g60 --PRECEDES--> g61
    g60 --PRECEDES--> g62
    g60 --PRECEDES--> g63
    g60 --PRECEDES--> g64
    g61 --PRECEDES--> g65
    g61 --PRECEDES--> g66
    g61 --PRECEDES--> g67
    g61 --PRECEDES--> g68
    g61 --PRECEDES--> g69
    g61 --PRECEDES--> g70
    g61 --PRECEDES--> g71
    g61 --PRECEDES--> g72
    g61 --PRECEDES--> g73
    g62 --PRECEDES--> g65
    g62 --PRECEDES--> g66
    g62 --PRECEDES--> g67
    g62 --PRECEDES--> g68
    g62 --PRECEDES--> g69
    g62 --PRECEDES--> g70
    g62 --PRECEDES--> g71
    g62 --PRECEDES--> g72
    g62 --PRECEDES--> g73
    g63 --PRECEDES--> g65
    g63 --PRECEDES--> g66
    g63 --PRECEDES--> g67
    g63 --PRECEDES--> g68
    g63 --PRECEDES--> g69
    g63 --PRECEDES--> g70
    g63 --PRECEDES--> g71
    g63 --PRECEDES--> g72
    g63 --PRECEDES--> g73
    g64 --PRECEDES--> g65
    g64 --PRECEDES--> g66
    g64 --PRECEDES--> g67
    g64 --PRECEDES--> g68
    g64 --PRECEDES--> g69
    g64 --PRECEDES--> g70
    g64 --PRECEDES--> g71
    g64 --PRECEDES--> g72
    g64 --PRECEDES--> g73
    g65 --PRECEDES--> g74
    g66 --PRECEDES--> g74
    g67 --PRECEDES--> g74
    g68 --PRECEDES--> g74
    g69 --PRECEDES--> g74
    g70 --PRECEDES--> g74
    g71 --PRECEDES--> g74
    g72 --PRECEDES--> g74
    g73 --PRECEDES--> g74
    g74 --PRECEDES--> g75
    g75 --PRECEDES--> g76
    g75 --PRECEDES--> g77
    g76 --PRECEDES--> g78
    g76 --PRECEDES--> g79
    g76 --PRECEDES--> g80
    g76 --PRECEDES--> g81
    g76 --PRECEDES--> g82
    g76 --PRECEDES--> g83
    g76 --PRECEDES--> g84
    g76 --PRECEDES--> g85
    g76 --PRECEDES--> g86
    g76 --PRECEDES--> g87
    g76 --PRECEDES--> g88
    g77 --PRECEDES--> g78
    g77 --PRECEDES--> g79
    g77 --PRECEDES--> g80
    g77 --PRECEDES--> g81
    g77 --PRECEDES--> g82
    g77 --PRECEDES--> g83
    g77 --PRECEDES--> g84
    g77 --PRECEDES--> g85
    g77 --PRECEDES--> g86
    g77 --PRECEDES--> g87
    g77 --PRECEDES--> g88
    g78 --PRECEDES--> g89
    g78 --PRECEDES--> g90
    g78 --PRECEDES--> g91
    g78 --PRECEDES--> g92
    g78 --PRECEDES--> g93
    g78 --PRECEDES--> g94
    g78 --PRECEDES--> g95
    g78 --PRECEDES--> g96
    g78 --PRECEDES--> g97
    g79 --PRECEDES--> g89
    g79 --PRECEDES--> g90
    g79 --PRECEDES--> g91
    g79 --PRECEDES--> g92
    g79 --PRECEDES--> g93
    g79 --PRECEDES--> g94
    g79 --PRECEDES--> g95
    g79 --PRECEDES--> g96
    g79 --PRECEDES--> g97
    g80 --PRECEDES--> g89
    g80 --PRECEDES--> g90
    g80 --PRECEDES--> g91
    g80 --PRECEDES--> g92
    g80 --PRECEDES--> g93
    g80 --PRECEDES--> g94
    g80 --PRECEDES--> g95
    g80 --PRECEDES--> g96
    g80 --PRECEDES--> g97
    g81 --PRECEDES--> g89
    g81 --PRECEDES--> g90
    g81 --PRECEDES--> g91
    g81 --PRECEDES--> g92
    g81 --PRECEDES--> g93
    g81 --PRECEDES--> g94
    g81 --PRECEDES--> g95
    g81 --PRECEDES--> g96
    g81 --PRECEDES--> g97
    g82 --PRECEDES--> g89
    g82 --PRECEDES--> g90
    g82 --PRECEDES--> g91
    g82 --PRECEDES--> g92
    g82 --PRECEDES--> g93
    g82 --PRECEDES--> g94
    g82 --PRECEDES--> g95
    g82 --PRECEDES--> g96
    g82 --PRECEDES--> g97
    g83 --PRECEDES--> g89
    g83 --PRECEDES--> g90
    g83 --PRECEDES--> g91
    g83 --PRECEDES--> g92
    g83 --PRECEDES--> g93
    g83 --PRECEDES--> g94
    g83 --PRECEDES--> g95
    g83 --PRECEDES--> g96
    g83 --PRECEDES--> g97
    g84 --PRECEDES--> g89
    g84 --PRECEDES--> g90
    g84 --PRECEDES--> g91
    g84 --PRECEDES--> g92
    g84 --PRECEDES--> g93
    g84 --PRECEDES--> g94
    g84 --PRECEDES--> g95
    g84 --PRECEDES--> g96
    g84 --PRECEDES--> g97
    g85 --PRECEDES--> g89
    g85 --PRECEDES--> g90
    g85 --PRECEDES--> g91
    g85 --PRECEDES--> g92
    g85 --PRECEDES--> g93
    g85 --PRECEDES--> g94
    g85 --PRECEDES--> g95
    g85 --PRECEDES--> g96
    g85 --PRECEDES--> g97
    g86 --PRECEDES--> g89
    g86 --PRECEDES--> g90
    g86 --PRECEDES--> g91
    g86 --PRECEDES--> g92
    g86 --PRECEDES--> g93
    g86 --PRECEDES--> g94
    g86 --PRECEDES--> g95
    g86 --PRECEDES--> g96
    g86 --PRECEDES--> g97
    g87 --PRECEDES--> g89
    g87 --PRECEDES--> g90
    g87 --PRECEDES--> g91
    g87 --PRECEDES--> g92
    g87 --PRECEDES--> g93
    g87 --PRECEDES--> g94
    g87 --PRECEDES--> g95
    g87 --PRECEDES--> g96
    g87 --PRECEDES--> g97
    g88 --PRECEDES--> g89
    g88 --PRECEDES--> g90
    g88 --PRECEDES--> g91
    g88 --PRECEDES--> g92
    g88 --PRECEDES--> g93
    g88 --PRECEDES--> g94
    g88 --PRECEDES--> g95
    g88 --PRECEDES--> g96
    g88 --PRECEDES--> g97
    g89 --PRECEDES--> g98
    g90 --PRECEDES--> g98
    g91 --PRECEDES--> g98
    g92 --PRECEDES--> g98
    g93 --PRECEDES--> g98
    g94 --PRECEDES--> g98
    g95 --PRECEDES--> g98
    g96 --PRECEDES--> g98
    g97 --PRECEDES--> g98
    g98 --PRECEDES--> g99
    g99 --PRECEDES--> g100
    g100 --PRECEDES--> g101
    g101 --PRECEDES--> g102
    g102 --PRECEDES--> g103
    g06 --SAME_TRACK--> g07
    g06 --SAME_TRACK--> g15
    g06 --SAME_TRACK--> g23
    g06 --SAME_TRACK--> g28
    g30 --SAME_TRACK--> g33
    g31 --SAME_TRACK--> g34
    g32 --SAME_TRACK--> g35
    g36 --SAME_TRACK--> g42
    g37 --SAME_TRACK--> g43
    g38 --SAME_TRACK--> g44
    g39 --SAME_TRACK--> g45
    g40 --SAME_TRACK--> g46
    g41 --SAME_TRACK--> g47
    g48 --SAME_TRACK--> g49
    g06 --SAME_TRACK--> g51
    g52 --SAME_TRACK--> g53
    g55 --SAME_TRACK--> g56
    g59 --SAME_TRACK--> g60
    g62 --SAME_TRACK--> g64
    g62 --SAME_TRACK--> g65
    g69 --SAME_TRACK--> g71
    g70 --SAME_TRACK--> g72
    g54 --SAME_TRACK--> g73
    g63 --SAME_TRACK--> g74
    g30 --SAME_TRACK--> g78
    g31 --SAME_TRACK--> g79
    g40 --SAME_TRACK--> g80
    g63 --SAME_TRACK--> g81
    g62 --SAME_TRACK--> g82
    g69 --SAME_TRACK--> g83
    g70 --SAME_TRACK--> g84
    g70 --SAME_TRACK--> g88
    g36 --SAME_TRACK--> g89
    g37 --SAME_TRACK--> g90
    g39 --SAME_TRACK--> g91
    g48 --SAME_TRACK--> g92
    g32 --SAME_TRACK--> g93
    g52 --SAME_TRACK--> g94
    g41 --SAME_TRACK--> g95
    g55 --SAME_TRACK--> g96
    g59 --SAME_TRACK--> g97
    g38 --SAME_TRACK--> g98
    g38 --SAME_TRACK--> g100
    g69 --SAME_TRACK--> g101
    g31 --SAME_TRACK--> g102
    g40 --SAME_TRACK--> g103
    g08 --SAME_TRACK--> g09
    g08 --SAME_TRACK--> g16
    g08 --SAME_TRACK--> g24
    g08 --SAME_TRACK--> g29
    g08 --SAME_TRACK--> g50
    g08 --SAME_TRACK--> g57
    g08 --SAME_TRACK--> g58
    g08 --SAME_TRACK--> g66
    g08 --SAME_TRACK--> g75
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|
| -9.50 | MOVING_START(A); MOVING_START(B) |
| -8.80 | STOP_SIGN_DETECTED_START(A,A:sign-0) |
| -7.70 | STOP_SIGN_DETECTED_START(B,B:sign-0) |
| -7.20 | STOP_SIGN_DETECTED_END(A,A:sign-0) |
| -7.05 | TRACK_APPEARED_LEFT(A,B); CLOSING_START(A,B) |
| -6.95 | TRACK_APPEARED_RIGHT(B,A); CLOSING_START(B,A) |
| -6.90 | STOP_SIGN_DETECTED_END(B,B:sign-0) |
| -6.85 | BRAKE_START(A) |
| -6.75 | BRAKE_START(B) |
| -6.10 | MOVING_END(A); STOP_START(A) |
| -6.00 | CLOSING_END(A,B); CLOSING_END(B,A); MOVING_END(B); STOP_START(B) |
| -2.55 | BRAKE_END(A); BRAKE_END(B) |
| -2.20 | STOP_END(A); MOVING_START(A); CLOSING_START(A,B); CLOSING_START(B,A) |
| -2.15 | STOP_END(B); MOVING_START(B) |
| -1.20 | TURN_LEFT_START(A); CRITICAL_TTC_START(A,B); CRITICAL_TTC_START(B,A) |
| -0.70 | TRACK_APPEARED_LEFT(A,A:track_002); TRACK_APPEARED_LEFT(A,A:track_005); TRACK_APPEARED_LEFT(A,A:track_010); CLOSING_START(A,A:track_002); CLOSING_START(A,A:track_005); CLOSING_START(A,A:track_010) |
| -0.65 | TRACK_APPEARED_LEFT(A,A:track_003); TRACK_APPEARED_LEFT(A,A:track_004); TRACK_APPEARED_LEFT(A,A:track_006); TRACK_APPEARED_LEFT(A,A:track_007); TRACK_APPEARED_LEFT(A,A:track_008); TRACK_APPEARED_LEFT(A,A:track_013); CLOSING_START(A,A:track_003); CLOSING_START(A,A:track_004); CLOSING_START(A,A:track_006); CLOSING_START(A,A:track_007); CLOSING_START(A,A:track_008); CLOSING_START(A,A:track_013) |
| -0.60 | TRACK_APPEARED_LEFT(A,A:track_009); CLOSING_START(A,A:track_009) |
| -0.55 | EGO_PATH_ENTRY(B,A) |
| -0.35 | TRACK_LOST(A,B) |
| -0.20 | TRACK_APPEARED_LEFT(A,A:track_011); CLOSING_START(A,A:track_011) |
| -0.15 | TRACK_APPEARED_RIGHT(A,A:track_012) |
| -0.10 | TRACK_APPEARED_LEFT(A,A:track_014); CLOSING_START(A,A:track_014) |
| -0.05 | CRITICAL_TTC_END(B,A); CLOSING_END(B,A); TRACK_APPEARED_LEFT(A,A:track_016); CLOSING_START(A,A:track_016) |
| +0.00 | COLLISION(A,B); TRACK_APPEARED_FRONT(A,A:track_017); TRACK_APPEARED_RIGHT(A,A:track_015); CLOSING_START(A,A:track_017) |
| +0.05 | EGO_PATH_EXIT(A,A:track_017); EGO_PATH_EXIT(B,A); BRAKE_START(A); BRAKE_START(B); TRACK_APPEARED_LEFT(A,A:track_018); TRACK_APPEARED_RIGHT(A,A:track_019); CLOSING_START(A,A:track_018); CLOSING_START(A,A:track_019); TRACK_LOST(A,A:track_012) |
| +0.20 | CLOSING_START(A,A:track_015) |
| +0.25 | TRACK_LOST(B,A) |
| +0.45 | MOVING_END(B); STOP_START(B) |
| +0.50 | CLOSING_END(A,A:track_002); CLOSING_END(A,A:track_005); CLOSING_END(A,A:track_008); CLOSING_END(A,A:track_015); CLOSING_END(A,A:track_017); CLOSING_END(A,A:track_018); CLOSING_END(A,A:track_019); TURN_LEFT_END(A); MOVING_END(A); STOP_START(A); TRACK_LOST(A,A:track_019) |
| +0.55 | CLOSING_END(A,A:track_003); CLOSING_END(A,A:track_004); CLOSING_END(A,A:track_007); CLOSING_END(A,A:track_009); CLOSING_END(A,A:track_010); CLOSING_END(A,A:track_011); CLOSING_END(A,A:track_013); CLOSING_END(A,A:track_014); CLOSING_END(A,A:track_016) |
| +0.60 | CLOSING_END(A,A:track_006) |
| +1.50 | STOP_SIGN_DETECTED_START(A,A:sign-1) |
| +3.10 | TRACK_LOST(A,A:track_006) |
| +4.85 | TRACK_LOST(A,A:track_018) |
| +5.35 | TRACK_LOST(A,A:track_005) |
| +5.40 | TRACK_LOST(A,A:track_008) |

## Temporal safety relations

Per track: does the cut-in start before the critical TTC, or was the critical TTC already active? Is the path entry before or after it? Temporal properties only, not causes.

- A's track_001 (B): CRITICAL_TTC_START 8.30, COLLISION 9.50 (+1.20 s) [local times; t_global: critical_ttc_start -1.20, collision +0.00]
- B's track_001 (A): CRITICAL_TTC_START 8.30, COLLISION 9.50 (+1.20 s); EGO_PATH_ENTRY 8.95 after critical TTC (+0.65 s) [local times; t_global: critical_ttc_start -1.20, ego_path_entry -0.55, collision +0.00]

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| -9.50 | A | g01 MOVING_START(A) (A:e01) | ego: not yet observed |
| -9.50 | B | g02 MOVING_START(B) (B:e01) | ego: not yet observed |
| -8.80 | A | g03 STOP_SIGN_DETECTED_START(A,A:sign-0) (A:e02) | ego: MOVING |
| -7.70 | B | g04 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e02) | ego: MOVING |
| -7.20 | A | g05 STOP_SIGN_DETECTED_END(A,A:sign-0) (A:e03) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -7.05 | A | g06 TRACK_APPEARED_LEFT(A,B) (A:e04)<br>g07 CLOSING_START(A,B) (A:e05) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.95 | B | g08 TRACK_APPEARED_RIGHT(B,A) (B:e03)<br>g09 CLOSING_START(B,A) (B:e04) | ego: MOVING<br>sign-0: STOP sign known, relevant to the path |
| -6.90 | B | g10 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e05) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.85 | A | g11 BRAKE_START(A) (A:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.75 | B | g12 BRAKE_START(B) (B:e06) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.10 | A | g13 MOVING_END(A) (A:e07)<br>g14 STOP_START(A) (A:e08) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.00 | A | g15 CLOSING_END(A,B) (A:e09) | ego: STOP, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -6.00 | B | g16 CLOSING_END(B,A) (B:e07)<br>g17 MOVING_END(B) (B:e08)<br>g18 STOP_START(B) (B:e09) | ego: MOVING, BRAKE<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -2.55 | A | g19 BRAKE_END(A) (A:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.55 | B | g20 BRAKE_END(B) (B:e10) | ego: STOP, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.20 | A | g21 STOP_END(A) (A:e11)<br>g22 MOVING_START(A) (A:e12)<br>g23 CLOSING_START(A,B) (A:e13) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.20 | B | g24 CLOSING_START(B,A) (B:e11) | ego: STOP<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| -2.15 | B | g25 STOP_END(B) (B:e12)<br>g26 MOVING_START(B) (B:e13) | ego: STOP<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.20 | A | g27 TURN_LEFT_START(A) (A:e14)<br>g28 CRITICAL_TTC_START(A,B) (A:e15) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -1.20 | B | g29 CRITICAL_TTC_START(B,A) (B:e14) | ego: MOVING<br>track_001: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -0.70 | A | g30 TRACK_APPEARED_LEFT(A,A:track_002) (A:e16)<br>g31 TRACK_APPEARED_LEFT(A,A:track_005) (A:e17)<br>g32 TRACK_APPEARED_LEFT(A,A:track_010) (A:e18)<br>g33 CLOSING_START(A,A:track_002) (A:e19)<br>g34 CLOSING_START(A,A:track_005) (A:e20)<br>g35 CLOSING_START(A,A:track_010) (A:e21) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.65 | A | g36 TRACK_APPEARED_LEFT(A,A:track_003) (A:e22)<br>g37 TRACK_APPEARED_LEFT(A,A:track_004) (A:e23)<br>g38 TRACK_APPEARED_LEFT(A,A:track_006) (A:e24)<br>g39 TRACK_APPEARED_LEFT(A,A:track_007) (A:e25)<br>g40 TRACK_APPEARED_LEFT(A,A:track_008) (A:e26)<br>g41 TRACK_APPEARED_LEFT(A,A:track_013) (A:e27)<br>g42 CLOSING_START(A,A:track_003) (A:e28)<br>g43 CLOSING_START(A,A:track_004) (A:e29)<br>g44 CLOSING_START(A,A:track_006) (A:e30)<br>g45 CLOSING_START(A,A:track_007) (A:e31)<br>g46 CLOSING_START(A,A:track_008) (A:e32)<br>g47 CLOSING_START(A,A:track_013) (A:e33) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_005: CLOSING<br>track_010: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -0.60 | A | g48 TRACK_APPEARED_LEFT(A,A:track_009) (A:e34)<br>g49 CLOSING_START(A,A:track_009) (A:e35) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -0.55 | B | g50 EGO_PATH_ENTRY(B,A) (B:e15) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC<br>sign-0: STOP sign known, relevant to the path |
| -0.35 | A | g51 TRACK_LOST(A,B) (A:e36) | ego: MOVING, TURN_LEFT<br>track_001: CLOSING, CRITICAL_TTC<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>sign-0: STOP sign known, relevant to the path |
| -0.20 | A | g52 TRACK_APPEARED_LEFT(A,A:track_011) (A:e37)<br>g53 CLOSING_START(A,A:track_011) (A:e38) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -0.15 | A | g54 TRACK_APPEARED_RIGHT(A,A:track_012) (A:e39) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -0.10 | A | g55 TRACK_APPEARED_LEFT(A,A:track_014) (A:e40)<br>g56 CLOSING_START(A,A:track_014) (A:e41) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| -0.05 | B | g57 CRITICAL_TTC_END(B,A) (B:e16)<br>g58 CLOSING_END(B,A) (B:e17) | ego: MOVING<br>track_001: CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| -0.05 | A | g59 TRACK_APPEARED_LEFT(A,A:track_016) (A:e42)<br>g60 CLOSING_START(A,A:track_016) (A:e43) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | A | g61 COLLISION(A,B) (A:e44)<br>g62 TRACK_APPEARED_FRONT(A,A:track_017) (A:e45)<br>g63 TRACK_APPEARED_RIGHT(A,A:track_015) (A:e46)<br>g64 CLOSING_START(A,A:track_017) (A:e47) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track_016: CLOSING<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.00 | B | g61 COLLISION(A,B) (B:e18) | ego: MOVING<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | A | g65 EGO_PATH_EXIT(A,A:track_017) (A:e48)<br>g67 BRAKE_START(A) (A:e49)<br>g69 TRACK_APPEARED_LEFT(A,A:track_018) (A:e50)<br>g70 TRACK_APPEARED_RIGHT(A,A:track_019) (A:e51)<br>g71 CLOSING_START(A,A:track_018) (A:e52)<br>g72 CLOSING_START(A,A:track_019) (A:e53)<br>g73 TRACK_LOST(A,A:track_012) (A:e54) | ego: MOVING, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_012: CUT_IN_FROM_LEFT?, CUT_IN_FROM_RIGHT?<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING, IN_EGO_PATH<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.05 | B | g66 EGO_PATH_EXIT(B,A) (B:e19)<br>g68 BRAKE_START(B) (B:e20) | ego: MOVING<br>track_001: IN_EGO_PATH<br>sign-0: STOP sign known, relevant to the path |
| +0.20 | A | g74 CLOSING_START(A,A:track_015) (A:e55) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_012<br>sign-0: STOP sign known, relevant to the path |
| +0.25 | B | g75 TRACK_LOST(B,A) (B:e21) | ego: MOVING, BRAKE<br>track_001: no active state<br>sign-0: STOP sign known, relevant to the path |
| +0.45 | B | g76 MOVING_END(B) (B:e22)<br>g77 STOP_START(B) (B:e23) | ego: MOVING, BRAKE<br>track lost, states UNKNOWN: track_001<br>sign-0: STOP sign known, relevant to the path |
| +0.50 | A | g78 CLOSING_END(A,A:track_002) (A:e56)<br>g79 CLOSING_END(A,A:track_005) (A:e57)<br>g80 CLOSING_END(A,A:track_008) (A:e58)<br>g81 CLOSING_END(A,A:track_015) (A:e59)<br>g82 CLOSING_END(A,A:track_017) (A:e60)<br>g83 CLOSING_END(A,A:track_018) (A:e61)<br>g84 CLOSING_END(A,A:track_019) (A:e62)<br>g85 TURN_LEFT_END(A) (A:e63)<br>g86 MOVING_END(A) (A:e64)<br>g87 STOP_START(A) (A:e65)<br>g88 TRACK_LOST(A,A:track_019) (A:e66) | ego: MOVING, BRAKE, TURN_LEFT<br>track_002: CLOSING<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: CLOSING<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: CLOSING<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: CLOSING<br>track_016: CLOSING<br>track_017: CLOSING<br>track_018: CLOSING<br>track_019: CLOSING<br>track lost, states UNKNOWN: track_001, track_012<br>sign-0: STOP sign known, relevant to the path |
| +0.55 | A | g89 CLOSING_END(A,A:track_003) (A:e67)<br>g90 CLOSING_END(A,A:track_004) (A:e68)<br>g91 CLOSING_END(A,A:track_007) (A:e69)<br>g92 CLOSING_END(A,A:track_009) (A:e70)<br>g93 CLOSING_END(A,A:track_010) (A:e71)<br>g94 CLOSING_END(A,A:track_011) (A:e72)<br>g95 CLOSING_END(A,A:track_013) (A:e73)<br>g96 CLOSING_END(A,A:track_014) (A:e74)<br>g97 CLOSING_END(A,A:track_016) (A:e75) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: CLOSING<br>track_004: CLOSING<br>track_005: no active state<br>track_006: CLOSING<br>track_007: CLOSING<br>track_008: no active state<br>track_009: CLOSING<br>track_010: CLOSING<br>track_011: CLOSING<br>track_013: CLOSING<br>track_014: CLOSING<br>track_015: no active state<br>track_016: CLOSING<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path |
| +0.60 | A | g98 CLOSING_END(A,A:track_006) (A:e76) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: CLOSING<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path |
| +1.50 | A | g99 STOP_SIGN_DETECTED_START(A,A:sign-1) (A:e77) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path |
| +3.10 | A | g100 TRACK_LOST(A,A:track_006) (A:e78) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_006: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_012, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known |
| +4.85 | A | g101 TRACK_LOST(A,A:track_018) (A:e79) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track_018: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_012, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known |
| +5.35 | A | g102 TRACK_LOST(A,A:track_005) (A:e80) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_005: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track lost, states UNKNOWN: track_001, track_006, track_012, track_018, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known |
| +5.40 | A | g103 TRACK_LOST(A,A:track_008) (A:e81) | ego: STOP, BRAKE<br>track_002: no active state<br>track_003: no active state<br>track_004: no active state<br>track_007: no active state<br>track_008: no active state<br>track_009: no active state<br>track_010: no active state<br>track_011: no active state<br>track_013: no active state<br>track_014: no active state<br>track_015: no active state<br>track_016: no active state<br>track_017: no active state<br>track lost, states UNKNOWN: track_001, track_005, track_006, track_012, track_018, track_019<br>sign-0: STOP sign known, relevant to the path<br>sign-1: STOP sign known |

## Plain-language reading

- 9.50 s before the matched collision, A started moving (already the case when first observed).
- 9.50 s before the matched collision, B started moving (already the case when first observed).
- 8.80 s before the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-0).
- 7.70 s before the matched collision, B's camera established a STOP sign detection (unidentified object B:sign-0).
- 7.20 s before the matched collision, A's camera stopped detecting STOP sign unidentified object A:sign-0.
- 7.05 s before the matched collision, A's radar started tracking B, which appeared on its left.
- 7.05 s before the matched collision, A observed B start closing in (already the case when first observed).
- 6.95 s before the matched collision, B's radar started tracking A, which appeared on its right.
- 6.95 s before the matched collision, B observed A start closing in (already the case when first observed).
- 6.90 s before the matched collision, B's camera stopped detecting STOP sign unidentified object B:sign-0.
- 6.85 s before the matched collision, A started braking.
- 6.75 s before the matched collision, B started braking.
- 6.10 s before the matched collision, A stopped moving.
- 6.10 s before the matched collision, A came to a stop.
- 6.00 s before the matched collision, A observed B stop closing in.
- 6.00 s before the matched collision, B observed A stop closing in.
- 6.00 s before the matched collision, B stopped moving.
- 6.00 s before the matched collision, B came to a stop.
- 2.55 s before the matched collision, A released the brake.
- 2.55 s before the matched collision, B released the brake.
- 2.20 s before the matched collision, A left its stop.
- 2.20 s before the matched collision, A started moving.
- 2.20 s before the matched collision, A observed B start closing in.
- 2.20 s before the matched collision, B observed A start closing in.
- 2.15 s before the matched collision, B left its stop.
- 2.15 s before the matched collision, B started moving.
- 1.20 s before the matched collision, A started turning left.
- 1.20 s before the matched collision, A's time-to-contact with B became critical.
- 1.20 s before the matched collision, B's time-to-contact with A became critical.
- 0.70 s before the matched collision, A's radar started tracking unidentified object A:track_002, which appeared on its left.
- 0.70 s before the matched collision, A's radar started tracking unidentified object A:track_005, which appeared on its left.
- 0.70 s before the matched collision, A's radar started tracking unidentified object A:track_010, which appeared on its left.
- 0.70 s before the matched collision, A observed unidentified object A:track_002 start closing in (already the case when first observed).
- 0.70 s before the matched collision, A observed unidentified object A:track_005 start closing in (already the case when first observed).
- 0.70 s before the matched collision, A observed unidentified object A:track_010 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_003, which appeared on its left.
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_004, which appeared on its left.
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_006, which appeared on its left.
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_007, which appeared on its left.
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_008, which appeared on its left.
- 0.65 s before the matched collision, A's radar started tracking unidentified object A:track_013, which appeared on its left.
- 0.65 s before the matched collision, A observed unidentified object A:track_003 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A observed unidentified object A:track_004 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A observed unidentified object A:track_006 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A observed unidentified object A:track_007 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A observed unidentified object A:track_008 start closing in (already the case when first observed).
- 0.65 s before the matched collision, A observed unidentified object A:track_013 start closing in (already the case when first observed).
- 0.60 s before the matched collision, A's radar started tracking unidentified object A:track_009, which appeared on its left.
- 0.60 s before the matched collision, A observed unidentified object A:track_009 start closing in (already the case when first observed).
- 0.55 s before the matched collision, B observed A enter its forward path corridor.
- 0.35 s before the matched collision, A's radar lost B (its states are UNKNOWN from then on, not ended).
- 0.20 s before the matched collision, A's radar started tracking unidentified object A:track_011, which appeared on its left.
- 0.20 s before the matched collision, A observed unidentified object A:track_011 start closing in (already the case when first observed).
- 0.15 s before the matched collision, A's radar started tracking unidentified object A:track_012, which appeared on its right.
- 0.10 s before the matched collision, A's radar started tracking unidentified object A:track_014, which appeared on its left.
- 0.10 s before the matched collision, A observed unidentified object A:track_014 start closing in (already the case when first observed).
- 0.05 s before the matched collision, B's time-to-contact with A stopped being critical.
- 0.05 s before the matched collision, B observed A stop closing in.
- 0.05 s before the matched collision, A's radar started tracking unidentified object A:track_016, which appeared on its left.
- 0.05 s before the matched collision, A observed unidentified object A:track_016 start closing in (already the case when first observed).
- At the matched collision, A and B both recorded this same collision (peak impulses A: 4032, B: 4032 N*s).
- At the matched collision, A's radar started tracking unidentified object A:track_017, which appeared in front of it.
- At the matched collision, A's radar started tracking unidentified object A:track_015, which appeared on its right.
- At the matched collision, A observed unidentified object A:track_017 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_017 leave its forward path corridor.
- 0.05 s after the matched collision, B observed A leave its forward path corridor.
- 0.05 s after the matched collision, A started braking.
- 0.05 s after the matched collision, B started braking.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_018, which appeared on its left.
- 0.05 s after the matched collision, A's radar started tracking unidentified object A:track_019, which appeared on its right.
- 0.05 s after the matched collision, A observed unidentified object A:track_018 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A observed unidentified object A:track_019 start closing in (already the case when first observed).
- 0.05 s after the matched collision, A's radar lost unidentified object A:track_012 (its states are UNKNOWN from then on, not ended).
- 0.20 s after the matched collision, A observed unidentified object A:track_015 start closing in.
- 0.25 s after the matched collision, B's radar lost A (its states are UNKNOWN from then on, not ended).
- 0.45 s after the matched collision, B stopped moving.
- 0.45 s after the matched collision, B came to a stop.
- 0.50 s after the matched collision, A observed unidentified object A:track_002 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_005 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_008 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_015 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_017 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_018 stop closing in.
- 0.50 s after the matched collision, A observed unidentified object A:track_019 stop closing in.
- 0.50 s after the matched collision, A stopped turning left.
- 0.50 s after the matched collision, A stopped moving.
- 0.50 s after the matched collision, A came to a stop.
- 0.50 s after the matched collision, A's radar lost unidentified object A:track_019 (its states are UNKNOWN from then on, not ended).
- 0.55 s after the matched collision, A observed unidentified object A:track_003 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_004 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_007 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_009 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_010 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_011 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_013 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_014 stop closing in.
- 0.55 s after the matched collision, A observed unidentified object A:track_016 stop closing in.
- 0.60 s after the matched collision, A observed unidentified object A:track_006 stop closing in.
- 1.50 s after the matched collision, A's camera established a STOP sign detection (unidentified object A:sign-1) (the detector judged it not relevant to its path).
- 3.10 s after the matched collision, A's radar lost unidentified object A:track_006 (its states are UNKNOWN from then on, not ended).
- 4.85 s after the matched collision, A's radar lost unidentified object A:track_018 (its states are UNKNOWN from then on, not ended).
- 5.35 s after the matched collision, A's radar lost unidentified object A:track_005 (its states are UNKNOWN from then on, not ended).
- 5.40 s after the matched collision, A's radar lost unidentified object A:track_008 (its states are UNKNOWN from then on, not ended).
