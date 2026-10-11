# Independent event-oracle check

Privileged evaluation only. Direct GT body geometry/control kinematics; no reconstruction event generator.
Comparison: PERFECT oracle, before each observer's first contact, first onset per pair/type.

| run | pair | event | main [s] | independent [s] | delta [s] |
|---|---|---|---|---|---|
| traces/S01/run_0_crash | A→B | CRITICAL_TTC_START | 4.35 | 4.35 | 0.0 |
| traces/S01/run_0_crash | B→A | CRITICAL_TTC_START | 5.0 | 5.0 | 0.0 |
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

## Discrepancy diagnosis

Six stratified runs: rear-end S01, cut-in S02, crossing S03, S17, difficult S18
passing, and non-crash crossing sweep seed 0. There are 23 first onsets:
17 exact, one path entry differing 0.05 s, and five critical onsets differing
0.10–0.50 s. All expected first onsets were found. No definition was changed.

The largest difference is S02 B→A (+0.50 s). Evaluation-only diagnostic ablations
of the main predictor give 1.25 s normally, 1.60 s with zero ego curvature,
1.40 s with actual GT body placement, and 1.90 s with both; the independent
checker gives 1.75 s. Thus yaw-rate extrapolation and surface-to-body placement
explain substantial movement of this threshold crossing. The remaining difference
includes straight GT velocity vs projected ego speed and the checker stopping
the ego instantly for its alternative-braking test vs the main finite maximum
deceleration. These conventions are deliberately independent approximations.

S17 A→B changes from 3.85 to 4.10 s under straight main prediction (independent
4.05); S18 A→B from 5.20 to 5.45 (independent 5.30). The two B→A -0.10 s
differences persist under the geometry ablations, consistent with different
braking/velocity conventions. Crossing's 0.05 s difference is one sample and
uses the same path hysteresis with independently sampled oriented outlines.
See [diagnostic values](event_oracle_discrepancy_diagnosis.json).

This small subset finds no obvious event-generator implementation error. It
does not independently validate all definitions, post-impact releases, end
debouncing, all GT coverage, or a real-world avoidability conclusion.
