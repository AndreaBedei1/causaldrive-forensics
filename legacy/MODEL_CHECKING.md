> **Superseded by [FORMAL_METHODS.md](../docs/FORMAL_METHODS.md).**
>
> This describes the V1 property layer, whose properties were hand-written
> Python evaluators carrying an MTL-looking string beside them. Nothing
> checked that the string and the code agreed, and the string appeared in
> reports as though it had been evaluated.
> 
> V2 replaces it with an AST that is evaluated directly, so the rendering and
> the verdict are the same object. Read
> [FORMAL_METHODS.md](../docs/FORMAL_METHODS.md).

---

# Finite-trace property monitoring

> **This is finite-trace property monitoring over recorded traces. It is NOT
> formal verification of CARLA.**
>
> Nothing here proves a property of the simulator, of its physics, or of any
> vehicle model. Each property is *evaluated* over the finite, irregularly
> sampled sequence one participant actually recorded, and the verdict is a
> statement about **that trace** -- not about the system that produced it. There
> is no state-space exploration, no abstraction and no model of the environment;
> a `PASS` on one run says nothing about the next.

---

## 1. Why a three-valued monitor

A classical model checker answers a question we cannot honestly ask here: it
assumes the model is *complete*. A participant's onboard recording is not. Radar
tracks drop out, the log window is finite (20 s before the trigger, 5 s after),
and a participant can be involved in a collision it never saw coming. Feeding such
a trace to a two-valued checker would turn *"I had no evidence"* into *"the
property holds"* -- precisely the failure mode this project exists to avoid.

So every verdict is one of three (`CheckStatus`):

| Verdict | Meaning |
|---|---|
| `PASS` | the property is **witnessed** to hold on this trace |
| `FAIL` | a concrete violating interval exists and can be shown |
| `UNKNOWN` | the local evidence cannot decide it |

### Why `UNKNOWN` is a first-class verdict

It is not an error code, not a default and not a soft failure. It is the honest
answer to a question the evidence does not settle, and it is the verdict the whole
architecture is designed to be able to produce. Four distinct situations yield it,
and all four are distinguished in `PropertyResult.reason`:

1. **The stream the property needs was never recorded** -- no radar tracks, no
   controls, no telemetry. *"no range-rate evidence: this participant recorded no
   radar tracks, so the closing-rate antecedent cannot be evaluated."*
2. **The antecedent never held**, so the implication is only *vacuously* true. A
   vacuous `PASS` is indistinguishable from a real one once aggregated, and would
   silently inflate every summary; it is reported as `UNKNOWN` instead.
3. **The trace ends before the deadline** the property talks about -- the required
   response might still have occurred off-record.
4. **An evidence gap sits exactly where the verdict would be decided.**
   `_max_evidence_gap` measures the longest stretch of the deadline window
   carrying no usable sample (leading and trailing gaps count: evidence that
   starts halfway through the window says nothing about the first half). A gap
   wider than `max_gap_s` forbids `FAIL`, because a blackout leaves room for an
   unobserved response and asserting a violation there would be an over-claim.

An implementation bug is emphatically **not** `UNKNOWN`: a property that raises
aborts the run with the participant and property named
(`TraceChecker._evaluate`), because a bug and a genuine lack of evidence must not
look alike.

*From the committed S01 run* (`TraceChecker(cfg).check_run(run)` → `{'PASS': 4,
'FAIL': 0, 'UNKNOWN': 4}`): A passes P1, P2 and P3 and is `UNKNOWN` on P4 (it
detected no path conflict -- vacuous); B, the lead vehicle with no radar tracks at
all, is `UNKNOWN` on P1, P2 and P4 and passes P3. Four `UNKNOWN`s out of eight
verdicts on a perfectly healthy run is the expected, correct behaviour.

---

## 2. How a trace is built

`build_state_trace(ev, cfg)` flattens one participant's telemetry, controls and
radar tracks onto **one sample grid** -- its own telemetry timeline (falling back
to controls, then tracks), because that is the highest-rate stream a vehicle
records about itself. Streams are joined by nearest-neighbour lookup within
`match_tolerance_s`; a stream with no sample near a grid point leaves **`None`**
there instead of being interpolated, so a genuine drop-out stays visible to the
monitor. `None` is never silently coerced to a number -- that distinction is the
entire basis of the `UNKNOWN` verdict.

Per sample, a `TraceSample` carries `t`, `speed`, `throttle`, `brake`, `steer`,
`min_range`, `min_ttc` (smallest *defined* TTC over the active tracks),
`closing_rate` (largest closing speed, positive = closing) and `active_track_ids`.

Two sampling tolerances are recorded in **every** result's `parameters`, because
they can change a verdict and reproducing one requires knowing them:

| Parameter | Key | Default |
|---|---|---|
| `match_tolerance_s` | `checking.trace.match_tolerance_s` | `0.75 x` the participant's median sample period (0.06 s at 20 Hz), or 0.06 s when the period is unknown |
| `max_gap_s` | `checking.trace.max_gap_s` | `max(3 x period, 0.25)`, or 0.25 s |

The match tolerance is deliberately **strictly below one sampling period**: a
nearest-neighbour join must absorb timestamp jitter (which can never exceed half a
period) but must never bridge a whole missing sample, or the monitor would reason
over evidence that was never recorded.

Neither key is present in `configs/default.yaml`; the derived defaults above are
in force.

---

## 3. The local properties

All four are decidable from a **single participant's own onboard evidence** and
carry `scope = Provenance.LOCAL`.

---

### P1 -- `P1_brake_response`

**Semi-formal (finite-trace MTL):**

```
G( critical_ttc  ->  F[0, response_window_s] (brake >= brake_cmd) )
```

**Parameters**

| Parameter | Key | Value |
|---|---|---|
| `ttc_critical_s` | `checking.P1_brake_response.ttc_critical_s` | **1.6** s |
| `response_window_s` | `checking.P1_brake_response.response_window_s` | **1.2** s |
| `brake_cmd` | `checking.P1_brake_response.brake_cmd` | **0.25** |

**Semantics.** The antecedent is an *episode*: a maximal stretch during which the
smallest TTC over the participant's own tracks stays at or below the threshold,
split wherever an evidence gap exceeds `max_gap_s`. The deadline is measured from
the episode **onset**, because that is the first instant at which a driver or an
ADAS could have known. Braking already in progress at the onset counts as a
response -- reacting early is not a violation.

When no TTC was ever *sampled* but `CRITICAL_TTC` **events** exist, the episodes
are taken from those events instead (`evidence_source` records which was used).

**Verdicts.** `FAIL` when at least one episode had control evidence throughout the
window, the trace extended past the deadline, no evidence gap sat inside it, and
the brake never reached the threshold; the violating interval is
`[onset, onset + response_window_s]`. `UNKNOWN` when: no samples at all; no radar
track *and* no `CRITICAL_TTC` event; tracks but no TTC ever defined (nothing was
closing); no episode reached the threshold (vacuous); or any episode was
undecidable. `PASS` only when every episode was answered in time -- the witness
carries `max_response_latency_s`.

*Example:* on the committed S01 run A passes with *"every one of the 1
critical-TTC episode(s) was answered by brake >= 0.25 within 1.20 s (worst latency
0.45 s)"*.

---

### P2 -- `P2_no_throttle_while_closing`

**Semi-formal:**

```
G( closing_rate >= closing_rate_mps  ->  !G[0, grace_s] (throttle > throttle_cmd) )
```

**Parameters**

| Parameter | Key | Value |
|---|---|---|
| `closing_rate_mps` | `checking.P2_no_throttle_while_closing.closing_rate_mps` | **5.0** m/s |
| `grace_s` | `checking.P2_no_throttle_while_closing.grace_s` | **1.0** s |
| `throttle_cmd` | `checking.P2_no_throttle_while_closing.throttle_cmd` | **0.20** |

**Semantics.** A brief overlap of throttle and closing is normal -- the pedal takes
time to release -- so only a *sustained* stretch longer than `grace_s` violates.

**Verdicts.** `FAIL` with the offending interval when such a stretch exists.
`UNKNOWN` when there are no samples; no radar tracks at all; no closing episode
reached the rate (vacuous); no throttle evidence inside any closing episode; or a
throttle-while-closing stretch was **still active when the trace ended**, or was
immediately followed by an evidence gap -- because in both cases the run stopped,
not necessarily the condition, and only the latter is compliance. `PASS`
otherwise.

---

### P3 -- `P3_post_collision_stop`

**Semi-formal:**

```
G( collision  ->  ( G[0, window_s] (throttle <= max_throttle)
                  & F[0, window_s] (speed < stop_speed_mps) ) )
```

**Parameters**

| Parameter | Key | Value |
|---|---|---|
| `window_s` | `checking.P3_post_collision_stop.window_s` | **3.0** s |
| `max_throttle` | `checking.P3_post_collision_stop.max_throttle` | **0.05** |
| `stop_speed_mps` | `checking.P3_post_collision_stop.stop_speed_mps` | **1.0** m/s |

**Semantics.** The collision instant comes from the participant's **own** onboard
trigger (or, failing that, its own `COLLISION` event) -- nothing about the other
party is needed. The two conjuncts are treated asymmetrically **on purpose**:

* throttle above the threshold anywhere in the window is a violation that can be
  *shown* immediately, even on a truncated trace → `FAIL`;
* failing to *see* the stop on a truncated trace is not a violation → `UNKNOWN`.

**Verdicts.** `FAIL` on the throttle conjunct; or when the speed never fell below
the threshold, the window was **not** truncated, and the speed was sampled densely
enough across it. `UNKNOWN` when no collision was recorded (vacuous); no samples
fall inside the window; control or telemetry evidence is missing inside it; the
trace ends before the window elapses; or a speed-evidence gap wider than
`max_gap_s` sits inside it. `PASS` when the stop is witnessed and the throttle
stayed low.

---

### P4 -- `P4_conflict_without_response`

**Semi-formal:**

```
G( (predicted_path_conflict | conflict_region_entry)
     ->  F[0, lookahead_s] (brake >= min_evasive_brake | |steer| >= min_evasive_steer) )
```

**Parameters**

| Parameter | Key | Value |
|---|---|---|
| `lookahead_s` | `checking.P4_conflict_without_response.lookahead_s` | **3.0** s |
| `min_evasive_brake` | `checking.P4_conflict_without_response.min_evasive_brake` | **0.2** |
| `min_evasive_steer` | `checking.P4_conflict_without_response.min_evasive_steer` | **0.15** |

**Semantics.** This is the property that turns *"it saw the conflict coming"* into
a checkable statement. The antecedent is the participant's **own** detection -- a
`PREDICTED_PATH_CONFLICT` or a `CONFLICT_REGION_ENTRY` event -- and the response
window starts at that event's `t_start`.

The window is **clipped at the outcome** (its own collision trigger, or its
earliest `COLLISION` / `NEAR_MISS` event) when one occurred sooner: after the
outcome there is no longer an opportunity to avoid it, and counting that time
would be unfair to the participant. A clipped window that leaves no time at all is
`UNKNOWN`, not `FAIL`.

**Verdicts.** `FAIL` with one interval per unanswered conflict. `UNKNOWN` when no
conflict was detected (vacuous); no control evidence sits inside a window; the
outcome left no time; the trace ends before an unclipped lookahead elapses; or an
evidence gap sits inside a window. `PASS` when every detected conflict was
answered.

---

## 4. The oracle properties -- privileged, evaluation only

These are kept **strictly separate**. They answer questions no onboard sensor in
this project observes, they carry `scope = Provenance.ORACLE`, and their verdicts
are evaluation-only and must never re-enter local or fused inference.

The separation is structural, not conventional:

* they operate on a **plain dictionary trace** with a documented shape, so
  `cdf.checking` never imports `cdf.oracle`;
* `TraceChecker` exposes them only through `check_oracle()`, a different method
  returning a different list, and `check_run()` -- the producer of
  `checking/model_check_results.json` -- **contains no oracle verdicts at all**;
* `_evaluate()` refuses to run a property whose scope does not match the pipeline
  it was invoked from, in either direction.

The expected trace shape:

```json
{"run_id": "...", "scenario_id": "...",
 "samples": [{"t": 0.05,
              "actors": {"A": {"x": .., "y": .., "speed": ..,
                               "signal_state": "red",
                               "in_junction": false,
                               "has_right_of_way": true}}}]}
```

Any field may be missing; a property that needs an absent field returns
**`UNKNOWN`** rather than guessing -- *the oracle is privileged, not omniscient*.

---

### O1 -- `O1_signal_compliance`

```
G( junction_entry  ->  signal_at_entry != red )
```

| Parameter | Key | Default |
|---|---|---|
| `min_entry_speed_mps` | `checking.O1_signal_compliance.min_entry_speed_mps` | 0.5 m/s |
| `red_states` | `checking.O1_signal_compliance.red_states` | `["red"]` |
| required fields | -- | `in_junction`, `signal_state`, `speed` |

A junction *entry* is a rising edge of `in_junction`; the signal facing the actor
at that instant is read from `signal_state`. A stationary actor (below
`min_entry_speed_mps`) creeping over a boundary is not a violation. `UNKNOWN` when
the trace has no samples, names no actors, lacks the two privileged fields, or the
actor never entered a signalised junction. A malformed, empty `red_states` raises.

Per-actor verdicts are combined conjunctively by `combine_statuses`: **`FAIL`
dominates** (one witnessed violation refutes the conjunction), then `UNKNOWN` (an
undecided conjunct makes the whole undecided), and `PASS` only when every conjunct
passed. An empty sequence is `UNKNOWN`: nothing was checked, so nothing is known.

---

### O2 -- `O2_right_of_way`

```
G( in_junction & !has_right_of_way  ->  !(exists q != self: in_junction(q) & has_right_of_way(q)) )
```

| Parameter | Key | Default |
|---|---|---|
| `min_overlap_s` | `checking.O2_right_of_way.min_overlap_s` | 0.1 s |
| required fields | -- | `in_junction`, `has_right_of_way` |

A yielding actor sharing the junction with a priority actor is a right-of-way
violation. The overlap must last at least `min_overlap_s` so that a single sample
of geometric coincidence at the boundary is not reported as a breach. `UNKNOWN`
when the trace has no samples, names fewer than two actors, lacks the privileged
fields, or the actor never had to yield inside a junction.

Neither `checking.O1_signal_compliance.*` nor `checking.O2_right_of_way.*` is
present in `configs/default.yaml`; the code defaults above are in force.

---

## 5. The checker and its reports

`TraceChecker(cfg, properties=None)` selects `LOCAL_PROPERTIES` by default,
optionally filtered by `checking.enabled_properties` (an unknown id raises), and
refuses any property whose scope is not `LOCAL`.

`_evaluate()` validates what a property returned -- not paranoia, but the thing
that keeps the layer separation real:

* right scope, right `property_id`;
* **non-empty `parameters`** -- a verdict must record the thresholds that produced
  it;
* **no `FAIL` without a violating interval**;
* an exception is re-raised as a `RuntimeError` naming the property and the
  participant.

`check_run(run)` is the on-disk shape of `checking/model_check_results.json`:
the schema version, `scope: "local"`, run identity, the **config hash**, every
property's `describe()` block (id, description, semi-formal `formal` string,
scope), every `PropertyResult`, and three summaries -- overall, `by_participant`
and `by_property`. All three verdict keys are always emitted, even when zero, so a
consumer never has to guess whether a missing key means zero or means the checker
did not run.

Keeping the `formal` string in the same object as the evaluator is deliberate:
that string is what appears in reports and in the paper, and co-locating them makes
a drift between the two visible.

---

## 6. Counterexamples

For every `FAIL`, `build_counterexample_report(results, run, cfg)` extracts the
short stretch of trace around the hull of that result's violating intervals, so a
human can see what happened rather than reading a pair of numbers.

* **Padding.** The window is widened by `checking.counterexample.pad_s` (1.0 s) on
  both sides -- the interesting part is usually the approach to the violation.
* **Bounded size.** At most `checking.counterexample.max_samples` (240) rows,
  decimated by a fixed stride that always keeps the first and last sample and
  never widens the window. A fixed stride rather than an adaptive scheme, because
  counterexamples are artifacts and must be byte-reproducible.
* **Own evidence only.** Extracted from one participant's own
  `ParticipantEvidence`: exactly what that vehicle could have shown an
  investigator.

Each payload carries the sample table (`t`, `speed`, `throttle`, `brake`, `steer`,
`min_range`, `min_ttc`, `active_track_ids` -- with `None` preserved to mark missing
evidence), the thresholds used, a **condition-span map** (`critical_ttc`,
`closing_fast`, `braking`, `throttle_applied`, `steering`, `stopped`,
`missing_control_evidence`, `no_track_evidence`, `inside_violating_interval`) so a
reader can see at a glance that the critical-TTC condition started at 2.40 s while
braking only began at 4.10 s, a numeric summary, and the `trace_parameters` the
monitor ran under.

A `FAIL` that cannot be explained -- no interval, or a participant missing from the
run bundle -- is recorded in `skipped` with the reason. A counterexample that
quietly disappears is worse than one reported as unavailable.

Both reports are joinable after the fact through the deterministic
`counterexample_ref` = `"CE:<property_id>:<participant_id>:<t0>-<t1>"`.

They are written together by `TraceChecker.check_and_persist(layout, run)`, and
that is not a convenience. Writing `model_check_results.json` on its own leaves
every `FAIL` naming a counterexample that does not exist, which is exactly what
happened for the whole first campaign: 171 references resolving to nothing, and
a viewer showing "counterexample report missing" for all of them.
`tests/integration/test_recorded_graph_invariants.py` now fails if any recorded
`FAIL` carries a dangling reference or no violating interval.

Across the 39 recorded runs: 147 `FAIL` verdicts, 147 counterexamples, 0 skipped.

---

## 7. What these verdicts do and do not mean

* A `FAIL` is a **safety-property violation on a recorded trace**, evaluated
  against explicitly stated thresholds -- not a finding of fault, and not a claim
  about the vehicle's design.
* A `PASS` is witnessed on *that* trace only.
* An `UNKNOWN` means **insufficient evidence**, and is the intended verdict
whenever the onboard recording genuinely cannot settle the question. Scenarios
may deliberately exercise this boundary, while `O1` -- reading privileged state
-- can decide questions that onboard evidence cannot.
* The property set is small, hand-written and auditable by design. It is a monitor
  over evidence, not a proof about a system.
