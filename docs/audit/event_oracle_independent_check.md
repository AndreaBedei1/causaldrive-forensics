# Independent event-oracle check

Privileged evaluation only. Direct GT body geometry/control kinematics; no reconstruction event generator.
Comparison: PERFECT oracle, before each observer's first contact, first onset per pair/type.

| run | pair | event | main [s] | independent [s] | delta [s] |
|---|---|---|---|---|---|
| traces/S01/run_0_crash | A→B | CRITICAL_TTC_START | 4.35 | 4.35 | 0.0 |
| traces/S01/run_0_crash | B→A | CRITICAL_TTC_START | 5.0 | 4.5 | -0.5 |
| traces/S02/run_0_crash | A→B | CUT_IN_FROM_LEFT_START | 2.55 | 2.55 | 0.0 |
| traces/S02/run_0_crash | A→B | EGO_PATH_ENTRY | 2.9 | 2.9 | 0.0 |
| traces/S02/run_0_crash | A→B | CRITICAL_TTC_START | 1.65 | 1.65 | 0.0 |
| traces/S02/run_0_crash | B→A | CRITICAL_TTC_START | 1.25 | 1.75 | 0.5 |
| traces/S03/run_0_crash | A→B | CRITICAL_TTC_START | 2.15 | 2.15 | 0.0 |
| traces/S03/run_0_crash | B→A | EGO_PATH_ENTRY | 4.0 | 4.0 | 0.0 |
| traces/S03/run_0_crash | B→A | CRITICAL_TTC_START | 1.95 | 1.95 | 0.0 |
| traces/S17/run_0_crash | A→B | CRITICAL_TTC_START | 3.85 | 4.05 | 0.2 |
| traces/S17/run_0_crash | A→C | CUT_IN_FROM_RIGHT_START | 3.0 | 3.0 | 0.0 |
| traces/S17/run_0_crash | A→C | EGO_PATH_ENTRY | 3.2 | 3.2 | 0.0 |
| traces/S17/run_0_crash | A→C | CRITICAL_TTC_START | 2.3 | 2.3 | 0.0 |
| traces/S17/run_0_crash | B→A | CUT_IN_FROM_RIGHT_START | 4.45 | 4.45 | 0.0 |
| traces/S17/run_0_crash | B→A | EGO_PATH_ENTRY | 4.65 | 4.65 | 0.0 |
| traces/S17/run_0_crash | B→A | CRITICAL_TTC_START | 4.05 | 3.95 | -0.1 |
| traces/S18/run_0_passing | A→B | CRITICAL_TTC_START | 5.2 | 5.3 | 0.1 |
| traces/S18/run_0_passing | A→C | CRITICAL_TTC_START | 0.5 | 0.5 | 0.0 |
| traces/S18/run_0_passing | B→A | CUT_IN_FROM_RIGHT_START | 5.8 | 5.8 | 0.0 |
| traces/S18/run_0_passing | B→A | EGO_PATH_ENTRY | 5.9 | 5.9 | 0.0 |
| traces/S18/run_0_passing | B→A | CRITICAL_TTC_START | 5.4 | 5.3 | -0.1 |
| sweeps/crossing/S03/run_0_crossing_000 | A→B | EGO_PATH_ENTRY | 9.95 | 9.95 | 0.0 |
| sweeps/crossing/S03/run_0_crossing_000 | B→A | EGO_PATH_ENTRY | 3.4 | 3.35 | -0.05 |

Checker differences are diagnostic: true oriented body vs oracle surface-based placement, explicit SAT/braking test,
straight forecasts instead of yaw-rate arcs, first onsets only. No definitions are changed to force agreement.
