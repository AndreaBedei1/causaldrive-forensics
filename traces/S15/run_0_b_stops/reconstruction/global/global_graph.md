# Global graph - S15/run_0_b_stops

Global time `t_global` is 0 at the matched reference collision. The local graphs were not modified: every node lists the local node(s) and local time(s) it comes from.

Speed limit 50 km/h, supplied as incident context: known a priori, not perceived and not ground truth.

## Entities

| Entity | Kind | Details |
|--------|------|---------|
| A | recorder | clock UNALIGNED; observed by others as: - |
| B | recorder | clock UNALIGNED; observed by others as: - |
| C | recorder | clock UNALIGNED; observed by others as: - |
| A:track_001 | anonymous_track | seen only by A; candidate: - |
| A:track_002 | anonymous_track | seen only by A; candidate: - |
| B:track_001 | anonymous_track | seen only by B; candidate: - |
| B:track_002 | anonymous_track | seen only by B; candidate: - |
| B:track_003 | anonymous_track | seen only by B; candidate: - |
| C:track_001 | anonymous_track | seen only by C; candidate: - |
| C:track_002 | anonymous_track | seen only by C; candidate: - |

## Graph alignment

No collision was matched across recorders, so no local graph could be aligned; every event keeps only its local time (radar-only alignment is not implemented).

| Graph | Status | Anchor node | Anchor local time | Offset to global | Note |
|-------|--------|-------------|------------------:|-----------------:|------|
| A | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| B | UNALIGNED | - | - | - | it recorded no collision to anchor on |
| C | UNALIGNED | - | - | - | it recorded no collision to anchor on |

## Identity associations

| Local track | Global entity | Status | Confidence | Evidence |
|-------------|---------------|--------|-----------:|----------|
| A:track_001 | A:track_001 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| A:track_002 | A:track_002 | ANONYMOUS | - | graph A is not aligned: it recorded no collision to anchor on |
| B:track_001 | B:track_001 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_002 | B:track_002 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| B:track_003 | B:track_003 | ANONYMOUS | - | graph B is not aligned: it recorded no collision to anchor on |
| C:track_001 | C:track_001 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |
| C:track_002 | C:track_002 | ANONYMOUS | - | graph C is not aligned: it recorded no collision to anchor on |

## Nodes

| Id | Global time | Type | Actor | Subject / participants | Observed by (local node @ local time) | Details |
|----|------------:|------|-------|------------------------|----------------------------------------|---------|
| g01 | - | MOVING_START | A | - | A:e01 @ 0.00 | active_at_first_observation=True |
| g02 | - | TRACK_APPEARED | A | A:track_001 | A:e02 @ 0.00 |  |
| g03 | - | CLOSING_START | A | A:track_001 | A:e03 @ 0.00 | active_at_first_observation=True |
| g04 | - | TRACK_APPEARED | A | A:track_002 | A:e04 @ 2.00 |  |
| g05 | - | CLOSING_START | A | A:track_002 | A:e05 @ 2.00 | active_at_first_observation=True |
| g06 | - | CRITICAL_TTC_START | A | A:track_002 | A:e06 @ 2.00 | active_at_first_observation=True |
| g07 | - | CRITICAL_TTC_START | A | A:track_001 | A:e07 @ 2.45 |  |
| g08 | - | PREDICTED_PATH_CONFLICT_START | A | A:track_002 | A:e08 @ 2.55 |  |
| g09 | - | PREDICTED_PATH_CONFLICT_END | A | A:track_002 | A:e09 @ 3.20 |  |
| g10 | - | TRACK_LOST | A | A:track_002 | A:e10 @ 3.80 |  |
| g11 | - | TRACK_LOST | A | A:track_001 | A:e11 @ 4.45 |  |
| g12 | - | MOVING_START | B | - | B:e01 @ 0.00 | active_at_first_observation=True |
| g13 | - | STRONG_THROTTLE_START | B | - | B:e02 @ 1.20 |  |
| g14 | - | TRACK_APPEARED | B | B:track_001 | B:e03 @ 1.45 |  |
| g15 | - | CLOSING_START | B | B:track_001 | B:e04 @ 1.45 | active_at_first_observation=True |
| g16 | - | STRONG_THROTTLE_END | B | - | B:e05 @ 1.80 |  |
| g17 | - | STOP_SIGN_DETECTED_START | B | B:sign-0 | B:e06 @ 1.80 | relevant_to_ego_path=False |
| g18 | - | TRACK_APPEARED | B | B:track_002 | B:e07 @ 1.95 |  |
| g19 | - | CLOSING_START | B | B:track_002 | B:e08 @ 1.95 | active_at_first_observation=True |
| g20 | - | CRITICAL_TTC_START | B | B:track_002 | B:e09 @ 2.00 |  |
| g21 | - | STOP_SIGN_DETECTED_END | B | B:sign-0 | B:e10 @ 2.10 |  |
| g22 | - | CRITICAL_TTC_START | B | B:track_001 | B:e11 @ 2.35 |  |
| g23 | - | BRAKE_START | B | - | B:e12 @ 2.55 |  |
| g24 | - | HARD_BRAKE_START | B | - | B:e13 @ 2.55 |  |
| g25 | - | CRITICAL_TTC_END | B | B:track_001 | B:e14 @ 2.70 |  |
| g26 | - | TRACK_LOST | B | B:track_001 | B:e15 @ 2.85 |  |
| g27 | - | PREDICTED_PATH_CONFLICT_START | B | B:track_002 | B:e16 @ 2.95 |  |
| g28 | - | PREDICTED_PATH_CONFLICT_END | B | B:track_002 | B:e17 @ 3.30 |  |
| g29 | - | MOVING_END | B | - | B:e18 @ 3.40 |  |
| g30 | - | STOP_START | B | - | B:e19 @ 3.40 |  |
| g31 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e20 @ 3.40 | relevant_to_ego_path=False |
| g32 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e21 @ 3.70 |  |
| g33 | - | EGO_PATH_ENTRY | B | B:track_002 | B:e22 @ 3.90 |  |
| g34 | - | TRACK_APPEARED | B | B:track_003 | B:e23 @ 3.95 |  |
| g35 | - | CLOSING_START | B | B:track_003 | B:e24 @ 3.95 | active_at_first_observation=True |
| g36 | - | CRITICAL_TTC_END | B | B:track_002 | B:e25 @ 4.20 |  |
| g37 | - | CLOSING_END | B | B:track_002 | B:e26 @ 4.25 |  |
| g38 | - | EGO_PATH_EXIT | B | B:track_002 | B:e27 @ 4.40 |  |
| g39 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e28 @ 4.80 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-2 |
| g40 | - | TRACK_LOST | B | B:track_002 | B:e29 @ 4.80 |  |
| g41 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e30 @ 4.80 | sign_track=sign-2 |
| g42 | - | CLOSING_END | B | B:track_003 | B:e31 @ 5.35 |  |
| g43 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e32 @ 5.60 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-3 |
| g44 | - | STOP_SIGN_DETECTED_END | B | B:sign-1 | B:e33 @ 5.60 | sign_track=sign-3 |
| g45 | - | EGO_PATH_ENTRY | B | B:track_003 | B:e34 @ 5.65 |  |
| g46 | - | EGO_PATH_EXIT | B | B:track_003 | B:e35 @ 6.45 |  |
| g47 | - | STOP_SIGN_DETECTED_START | B | B:sign-1 | B:e36 @ 6.70 | relevant_to_ego_path=False; reacquired=True; sign_track=sign-4 |
| g48 | - | STRONG_THROTTLE_START | B | - | B:e37 @ 10.55 |  |
| g49 | - | MOVING_START | C | - | C:e01 @ 0.00 | active_at_first_observation=True |
| g50 | - | TRACK_APPEARED | C | C:track_001 | C:e02 @ 0.00 |  |
| g51 | - | TRACK_APPEARED | C | C:track_002 | C:e03 @ 0.00 |  |
| g52 | - | CLOSING_START | C | C:track_001 | C:e04 @ 0.00 | active_at_first_observation=True |
| g53 | - | CLOSING_START | C | C:track_002 | C:e05 @ 0.00 | active_at_first_observation=True |
| g54 | - | PREDICTED_PATH_CONFLICT_START | C | C:track_002 | C:e06 @ 0.45 |  |
| g55 | - | PREDICTED_PATH_CONFLICT_END | C | C:track_002 | C:e07 @ 1.65 |  |
| g56 | - | STRONG_THROTTLE_START | C | - | C:e08 @ 1.65 |  |
| g57 | - | STRONG_THROTTLE_END | C | - | C:e09 @ 2.10 |  |
| g58 | - | CRITICAL_TTC_START | C | C:track_002 | C:e10 @ 2.25 |  |
| g59 | - | CRITICAL_TTC_START | C | C:track_001 | C:e11 @ 2.45 |  |
| g60 | - | CRITICAL_TTC_END | C | C:track_002 | C:e12 @ 2.95 |  |
| g61 | - | PREDICTED_PATH_CONFLICT_START | C | C:track_002 | C:e13 @ 3.00 |  |
| g62 | - | PREDICTED_PATH_CONFLICT_END | C | C:track_002 | C:e14 @ 3.35 |  |
| g63 | - | TRACK_LOST | C | C:track_002 | C:e15 @ 4.00 |  |
| g64 | - | CRITICAL_TTC_END | C | C:track_001 | C:e16 @ 4.50 |  |
| g65 | - | CLOSING_END | C | C:track_001 | C:e17 @ 4.50 |  |
| g66 | - | TRACK_LOST | C | C:track_001 | C:e18 @ 4.50 |  |

## Edges

```
    g02 --SAME_TRACK--> g03
    g04 --SAME_TRACK--> g05
    g04 --SAME_TRACK--> g06
    g02 --SAME_TRACK--> g07
    g04 --SAME_TRACK--> g08
    g04 --SAME_TRACK--> g09
    g04 --SAME_TRACK--> g10
    g02 --SAME_TRACK--> g11
    g14 --SAME_TRACK--> g15
    g18 --SAME_TRACK--> g19
    g18 --SAME_TRACK--> g20
    g14 --SAME_TRACK--> g22
    g14 --SAME_TRACK--> g25
    g14 --SAME_TRACK--> g26
    g18 --SAME_TRACK--> g27
    g18 --SAME_TRACK--> g28
    g18 --SAME_TRACK--> g33
    g34 --SAME_TRACK--> g35
    g18 --SAME_TRACK--> g36
    g18 --SAME_TRACK--> g37
    g18 --SAME_TRACK--> g38
    g18 --SAME_TRACK--> g40
    g34 --SAME_TRACK--> g42
    g34 --SAME_TRACK--> g45
    g34 --SAME_TRACK--> g46
    g50 --SAME_TRACK--> g52
    g51 --SAME_TRACK--> g53
    g51 --SAME_TRACK--> g54
    g51 --SAME_TRACK--> g55
    g51 --SAME_TRACK--> g58
    g50 --SAME_TRACK--> g59
    g51 --SAME_TRACK--> g60
    g51 --SAME_TRACK--> g61
    g51 --SAME_TRACK--> g62
    g51 --SAME_TRACK--> g63
    g50 --SAME_TRACK--> g64
    g50 --SAME_TRACK--> g65
    g50 --SAME_TRACK--> g66
```

## Global trace

Events in one row are simultaneous at 0.05 s resolution: their order is unresolved.

| t_global | Events |
|---------:|--------|

## Perceived state before each event, per observing recorder

Each recorder's own belief just before its events, in its own local names (track_001, ...): fusion does not rewrite it. True states are named, unknown ones end with `?`.

| t_global | Recorder | Events (local node) | Perceived state just before |
|---------:|----------|---------------------|-----------------------------|
| - | A | g01 MOVING_START(A) (A:e01)<br>g02 TRACK_APPEARED(A,A:track_001) (A:e02)<br>g03 CLOSING_START(A,A:track_001) (A:e03) | ego: not yet observed |
| - | A | g04 TRACK_APPEARED(A,A:track_002) (A:e04)<br>g05 CLOSING_START(A,A:track_002) (A:e05)<br>g06 CRITICAL_TTC_START(A,A:track_002) (A:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING |
| - | A | g07 CRITICAL_TTC_START(A,A:track_001) (A:e07) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g08 PREDICTED_PATH_CONFLICT_START(A,A:track_002) (A:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g09 PREDICTED_PATH_CONFLICT_END(A,A:track_002) (A:e09) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT |
| - | A | g10 TRACK_LOST(A,A:track_002) (A:e10) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC |
| - | A | g11 TRACK_LOST(A,A:track_001) (A:e11) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 |
| - | B | g12 MOVING_START(B) (B:e01) | ego: not yet observed |
| - | B | g13 STRONG_THROTTLE_START(B) (B:e02) | ego: MOVING |
| - | B | g14 TRACK_APPEARED(B,B:track_001) (B:e03)<br>g15 CLOSING_START(B,B:track_001) (B:e04) | ego: MOVING, STRONG_THROTTLE |
| - | B | g16 STRONG_THROTTLE_END(B) (B:e05)<br>g17 STOP_SIGN_DETECTED_START(B,B:sign-0) (B:e06) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING |
| - | B | g18 TRACK_APPEARED(B,B:track_002) (B:e07)<br>g19 CLOSING_START(B,B:track_002) (B:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>sign-0: STOP sign VISIBLE, known |
| - | B | g20 CRITICAL_TTC_START(B,B:track_002) (B:e09) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING<br>sign-0: STOP sign VISIBLE, known |
| - | B | g21 STOP_SIGN_DETECTED_END(B,B:sign-0) (B:e10) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign VISIBLE, known |
| - | B | g22 CRITICAL_TTC_START(B,B:track_001) (B:e11) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g23 BRAKE_START(B) (B:e12)<br>g24 HARD_BRAKE_START(B) (B:e13) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g25 CRITICAL_TTC_END(B,B:track_001) (B:e14) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g26 TRACK_LOST(B,B:track_001) (B:e15) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>sign-0: STOP sign not visible, known |
| - | B | g27 PREDICTED_PATH_CONFLICT_START(B,B:track_002) (B:e16) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | B | g28 PREDICTED_PATH_CONFLICT_END(B,B:track_002) (B:e17) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, PATH_CONFLICT<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | B | g29 MOVING_END(B) (B:e18)<br>g30 STOP_START(B) (B:e19)<br>g31 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e20) | ego: MOVING, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known |
| - | B | g32 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e21) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign VISIBLE, known |
| - | B | g33 EGO_PATH_ENTRY(B,B:track_002) (B:e22) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g34 TRACK_APPEARED(B,B:track_003) (B:e23)<br>g35 CLOSING_START(B,B:track_003) (B:e24) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g36 CRITICAL_TTC_END(B,B:track_002) (B:e25) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g37 CLOSING_END(B,B:track_002) (B:e26) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, CLOSING, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g38 EGO_PATH_EXIT(B,B:track_002) (B:e27) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE, IN_EGO_PATH<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g39 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e28)<br>g40 TRACK_LOST(B,B:track_002) (B:e29)<br>g41 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e30) | ego: STOP, BRAKE, HARD_BRAKE<br>track_002: VISIBLE<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g42 CLOSING_END(B,B:track_003) (B:e31) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, CLOSING<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g43 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e32)<br>g44 STOP_SIGN_DETECTED_END(B,B:sign-1) (B:e33) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g45 EGO_PATH_ENTRY(B,B:track_003) (B:e34) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g46 EGO_PATH_EXIT(B,B:track_003) (B:e35) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE, IN_EGO_PATH<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g47 STOP_SIGN_DETECTED_START(B,B:sign-1) (B:e36) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign not visible, known |
| - | B | g48 STRONG_THROTTLE_START(B) (B:e37) | ego: STOP, BRAKE, HARD_BRAKE<br>track_003: VISIBLE<br>lost (states UNKNOWN): track_001, track_002<br>sign-0: STOP sign not visible, known<br>sign-1: STOP sign VISIBLE, known |
| - | C | g49 MOVING_START(C) (C:e01)<br>g50 TRACK_APPEARED(C,C:track_001) (C:e02)<br>g51 TRACK_APPEARED(C,C:track_002) (C:e03)<br>g52 CLOSING_START(C,C:track_001) (C:e04)<br>g53 CLOSING_START(C,C:track_002) (C:e05) | ego: not yet observed |
| - | C | g54 PREDICTED_PATH_CONFLICT_START(C,C:track_002) (C:e06) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING |
| - | C | g55 PREDICTED_PATH_CONFLICT_END(C,C:track_002) (C:e07)<br>g56 STRONG_THROTTLE_START(C) (C:e08) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT |
| - | C | g57 STRONG_THROTTLE_END(C) (C:e09) | ego: MOVING, STRONG_THROTTLE<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING |
| - | C | g58 CRITICAL_TTC_START(C,C:track_002) (C:e10) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING |
| - | C | g59 CRITICAL_TTC_START(C,C:track_001) (C:e11) | ego: MOVING<br>track_001: VISIBLE, CLOSING<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC |
| - | C | g60 CRITICAL_TTC_END(C,C:track_002) (C:e12) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, CRITICAL_TTC |
| - | C | g61 PREDICTED_PATH_CONFLICT_START(C,C:track_002) (C:e13) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING |
| - | C | g62 PREDICTED_PATH_CONFLICT_END(C,C:track_002) (C:e14) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING, PATH_CONFLICT |
| - | C | g63 TRACK_LOST(C,C:track_002) (C:e15) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>track_002: VISIBLE, CLOSING |
| - | C | g64 CRITICAL_TTC_END(C,C:track_001) (C:e16)<br>g65 CLOSING_END(C,C:track_001) (C:e17)<br>g66 TRACK_LOST(C,C:track_001) (C:e18) | ego: MOVING<br>track_001: VISIBLE, CLOSING, CRITICAL_TTC<br>lost (states UNKNOWN): track_002 |

## Plain-language reading

- (unaligned, A local time 0.00 s) A started moving (already the case when first observed).
- (unaligned, A local time 0.00 s) A's radar started tracking unidentified object A:track_001.
- (unaligned, A local time 0.00 s) A observed unidentified object A:track_001 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's radar started tracking unidentified object A:track_002.
- (unaligned, A local time 2.00 s) A observed unidentified object A:track_002 start closing in (already the case when first observed).
- (unaligned, A local time 2.00 s) A's time-to-contact with unidentified object A:track_002 became critical (already the case when first observed).
- (unaligned, A local time 2.45 s) A's time-to-contact with unidentified object A:track_001 became critical.
- (unaligned, A local time 2.55 s) A predicted a path conflict with unidentified object A:track_002 (close approach ahead if both keep their motion).
- (unaligned, A local time 3.20 s) A stopped predicting a path conflict with unidentified object A:track_002.
- (unaligned, A local time 3.80 s) A's radar lost unidentified object A:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, A local time 4.45 s) A's radar lost unidentified object A:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 0.00 s) B started moving (already the case when first observed).
- (unaligned, B local time 1.20 s) B started applying strong throttle.
- (unaligned, B local time 1.45 s) B's radar started tracking unidentified object B:track_001.
- (unaligned, B local time 1.45 s) B observed unidentified object B:track_001 start closing in (already the case when first observed).
- (unaligned, B local time 1.80 s) B stopped applying strong throttle.
- (unaligned, B local time 1.80 s) B's camera established a STOP sign detection (unidentified object B:sign-0) (the detector judged it not relevant to its path).
- (unaligned, B local time 1.95 s) B's radar started tracking unidentified object B:track_002.
- (unaligned, B local time 1.95 s) B observed unidentified object B:track_002 start closing in (already the case when first observed).
- (unaligned, B local time 2.00 s) B's time-to-contact with unidentified object B:track_002 became critical.
- (unaligned, B local time 2.10 s) B's camera stopped detecting STOP sign unidentified object B:sign-0.
- (unaligned, B local time 2.35 s) B's time-to-contact with unidentified object B:track_001 became critical.
- (unaligned, B local time 2.55 s) B started braking.
- (unaligned, B local time 2.55 s) B started braking hard.
- (unaligned, B local time 2.70 s) B's time-to-contact with unidentified object B:track_001 stopped being critical.
- (unaligned, B local time 2.85 s) B's radar lost unidentified object B:track_001 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 2.95 s) B predicted a path conflict with unidentified object B:track_002 (close approach ahead if both keep their motion).
- (unaligned, B local time 3.30 s) B stopped predicting a path conflict with unidentified object B:track_002.
- (unaligned, B local time 3.40 s) B stopped moving.
- (unaligned, B local time 3.40 s) B came to a stop.
- (unaligned, B local time 3.40 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path).
- (unaligned, B local time 3.70 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 3.90 s) B observed unidentified object B:track_002 enter its forward path corridor.
- (unaligned, B local time 3.95 s) B's radar started tracking unidentified object B:track_003.
- (unaligned, B local time 3.95 s) B observed unidentified object B:track_003 start closing in (already the case when first observed).
- (unaligned, B local time 4.20 s) B's time-to-contact with unidentified object B:track_002 stopped being critical.
- (unaligned, B local time 4.25 s) B observed unidentified object B:track_002 stop closing in.
- (unaligned, B local time 4.40 s) B observed unidentified object B:track_002 leave its forward path corridor.
- (unaligned, B local time 4.80 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-2).
- (unaligned, B local time 4.80 s) B's radar lost unidentified object B:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, B local time 4.80 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.35 s) B observed unidentified object B:track_003 stop closing in.
- (unaligned, B local time 5.60 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-3).
- (unaligned, B local time 5.60 s) B's camera stopped detecting STOP sign unidentified object B:sign-1.
- (unaligned, B local time 5.65 s) B observed unidentified object B:track_003 enter its forward path corridor.
- (unaligned, B local time 6.45 s) B observed unidentified object B:track_003 leave its forward path corridor.
- (unaligned, B local time 6.70 s) B's camera established a STOP sign detection (unidentified object B:sign-1) (the detector judged it not relevant to its path) (the same sign reacquired, as camera track sign-4).
- (unaligned, B local time 10.55 s) B started applying strong throttle.
- (unaligned, C local time 0.00 s) C started moving (already the case when first observed).
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_001.
- (unaligned, C local time 0.00 s) C's radar started tracking unidentified object C:track_002.
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_001 start closing in (already the case when first observed).
- (unaligned, C local time 0.00 s) C observed unidentified object C:track_002 start closing in (already the case when first observed).
- (unaligned, C local time 0.45 s) C predicted a path conflict with unidentified object C:track_002 (close approach ahead if both keep their motion).
- (unaligned, C local time 1.65 s) C stopped predicting a path conflict with unidentified object C:track_002.
- (unaligned, C local time 1.65 s) C started applying strong throttle.
- (unaligned, C local time 2.10 s) C stopped applying strong throttle.
- (unaligned, C local time 2.25 s) C's time-to-contact with unidentified object C:track_002 became critical.
- (unaligned, C local time 2.45 s) C's time-to-contact with unidentified object C:track_001 became critical.
- (unaligned, C local time 2.95 s) C's time-to-contact with unidentified object C:track_002 stopped being critical.
- (unaligned, C local time 3.00 s) C predicted a path conflict with unidentified object C:track_002 (close approach ahead if both keep their motion).
- (unaligned, C local time 3.35 s) C stopped predicting a path conflict with unidentified object C:track_002.
- (unaligned, C local time 4.00 s) C's radar lost unidentified object C:track_002 (its states are UNKNOWN from then on, not ended).
- (unaligned, C local time 4.50 s) C's time-to-contact with unidentified object C:track_001 stopped being critical.
- (unaligned, C local time 4.50 s) C observed unidentified object C:track_001 stop closing in.
- (unaligned, C local time 4.50 s) C's radar lost unidentified object C:track_001 (its states are UNKNOWN from then on, not ended).
