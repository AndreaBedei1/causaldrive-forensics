# The causal model

## 1. Two documents, on purpose

Each participant produces **two** graphs over the same node set, and the
separation is load-bearing.

| | Event graph (`cdf.local.event_graph`) | Causal DAG (`cdf.local.causal_graph`) |
|---|---|---|
| What an edge means | a relation readable straight off the evidence | a *hypothesis* about why something happened |
| Edge types | `PRECEDES`, `OBSERVED_FROM`, `SAME_TRACK`, `INTERACTS_WITH` (plus `ALIGNS_WITH` / `ASSOCIATED_WITH`, fusion only) | `CONTRIBUTES_TO`, `TRIGGERS`, `INCREASES_RISK_OF`, `PREVENTS`, `CAUSES_OUTCOME` |
| Needs a theory? | no | yes -- one named rule per edge |
| Acyclic? | not required | **guaranteed** |
| Artifact | `vehicle_<id>/event_graph.json` | `vehicle_<id>/causal_graph.json` |

Why they are separate documents rather than one annotated graph:

1. **A reviewer must be able to tell an observation from a hypothesis.** "A
   braked, then the range fell" and "A's braking caused the range to fall" are
   different claims with different evidential status.
2. **An error in the causal rule table must not corrupt the observational
   record.** The event graph is reproducible from the raw streams alone; retuning
   the rule table cannot change it.
3. **The two have different edge budgets and different failure modes.**
   `PRECEDES` is dense and nearly free; a causal edge is expensive and must be
   defended.

The event graph's edges are additionally bounded so the document says something:
`PRECEDES` fans out only to the next `event_graph.precedes_fanout` (3) events,
`SAME_TRACK` chains a track's events with fan-out `event_graph.same_track_fanout`
(1), `INTERACTS_WITH` links an ego event to at most
`event_graph.interacts_max_per_event` (4) temporally overlapping track events with
the intervals padded by `event_graph.interacts_tolerance_s` (0.5 s), and the whole
document is capped at `event_graph.max_edges` (5000). When the cap bites, whole
relation classes are given up in priority order (`PRECEDES` first, because it
merely restates the timestamps) and, within a class, the *longest* temporal spans
go first -- keeping the immediate-successor chain, which transitivity cannot
recover. The limits actually used are recorded in the document's `meta`.

> None of the five `event_graph.*` keys is present in `configs/default.yaml`; the
> code defaults quoted above are in force. See `docs/IMPLEMENTATION_CHECKLIST.md`.

---

## 2. The causal rule table

Every causal hypothesis the pipeline is *capable* of stating is declared in
`src/cdf/local/causal_rules.py` as a frozen `CausalRule`. A reviewer can read that
one module and know exactly which edges can ever be drawn, before looking at a
single run. Two invariants keep the table honest, both enforced by
`validate_rules()` at import time and again on every configured table:

1. **Rules are generic over event types.** Nothing may be keyed on a scenario id,
   a participant id or a track id. Scenario-specific behaviour would make the
   evaluation circular.
2. **An observation is not a cause.** `RADAR_TRACK_APPEARED` and
   `RADAR_TRACK_LOST` may never appear on either side of a causal edge: they are
   facts about the observer's sensing process, not about the world.

`validate_rules()` additionally rejects a duplicate rule name, an empty
cause/effect set, an edge type that is not a `CausalEdgeType` value, a `prior`
outside `(0, 1]`, a non-positive `max_lag_s`, an empty description, an event type
appearing as both cause and effect of one rule, a `require_self_effect` rule whose
effects are track-scoped, a `require_same_subject` rule whose types are not all
interaction types, and the combination of both flags (an own-behaviour effect has
no track subject to match).

### 2.1 The table

`prior` is the rule's strength before any evidence -- a **modelling assumption,
not a measured probability**. `lag` is the longest accepted cause→effect delay.
"same subj." means both events must concern the same local radar track; "self
eff." means the effect must be an own-behaviour (subject-free) event.

#### How a conflict develops around one tracked object

| Rule | Cause → Effect | Edge | prior | lag | same subj. | Why this relation is physically plausible |
|---|---|---|---|---|---|---|
| `target_deceleration_closes_gap` | `TARGET_DECELERATION` → `RANGE_DECREASING`, `RAPID_CLOSING` | `TRIGGERS` | 0.80 | 2.5 s | yes | A tracked object slowing while we hold speed mechanically shortens the gap: observed range falls and range-rate turns strongly negative. |
| `closing_range_increases_ttc_risk` | `RANGE_DECREASING` → `LOW_TTC` | `INCREASES_RISK_OF` | 0.50 | 4.0 s | yes | A shrinking range does not by itself imply an imminent impact -- the closure may be slow -- but it is the precondition under which a low TTC can arise. Risk-raising, not triggering. |
| `rapid_closing_shortens_ttc` | `RAPID_CLOSING` → `LOW_TTC` | `CONTRIBUTES_TO` | 0.75 | 3.0 s | yes | TTC is range divided by closing speed, so a high closing speed is a direct numerical contributor to that same track's TTC falling below the warning threshold. |
| `ttc_escalates_to_critical` | `LOW_TTC`, `RAPID_CLOSING` → `CRITICAL_TTC` | `CONTRIBUTES_TO` | 0.80 | 3.0 s | yes | Without an intervening correction an already-low TTC keeps decreasing into the critical band; the earlier crossing is the same physical process one stage earlier. |
| `cut_in_closes_gap` | `CUT_IN_LIKE_MOTION` → `RANGE_DECREASING`, `RAPID_CLOSING`, `LOW_TTC` | `TRIGGERS` | 0.75 | 2.5 s | yes | An object moving laterally into our path takes over the headway reserved for empty road, abruptly converting lateral separation into longitudinal closure. |
| `lateral_crossing_predicts_conflict` | `LATERAL_CROSSING` → `PREDICTED_PATH_CONFLICT` | `CONTRIBUTES_TO` | 0.60 | 3.0 s | yes | Sustained lateral motion across our heading is what makes the constant-velocity extrapolation of the two paths intersect; the predicted conflict is that observation carried forward in time. |
| `predicted_conflict_becomes_region_entry` | `PREDICTED_PATH_CONFLICT`, `LATERAL_CROSSING` → `CONFLICT_REGION_ENTRY` | `TRIGGERS` | 0.70 | 4.0 s | yes | A predicted crossing point that neither party alters is reached: entry into the inferred region is the prediction coming true. |
| `conflict_region_entry_shortens_ttc` | `CONFLICT_REGION_ENTRY` → `LOW_TTC`, `CRITICAL_TTC` | `CONTRIBUTES_TO` | 0.70 | 3.0 s | yes | Once both parties occupy the same small region the remaining separation is metres rather than tens of metres -- exactly the condition under which TTC collapses. |
| `predicted_conflict_increases_ttc_risk` | `PREDICTED_PATH_CONFLICT` → `LOW_TTC` | `INCREASES_RISK_OF` | 0.55 | 4.0 s | yes | A predicted path conflict raises the probability of a low-TTC encounter, but either party can falsify the prediction, so the claim is risk-raising rather than deterministic. |

#### How the ego vehicle reacts to what it perceives

| Rule | Cause → Effect | Edge | prior | lag | self eff. | Why |
|---|---|---|---|---|---|---|
| `critical_ttc_triggers_hard_braking` | `CRITICAL_TTC` → `HARD_BRAKE`, `HARD_DECELERATION` | `TRIGGERS` | 0.85 | 2.0 s | yes | A critical TTC is the canonical stimulus for an emergency stop, whether from a driver model or an AEB function. Subjects need not match: the ego brakes once, for whichever threat is worst. |
| `low_ttc_triggers_braking` | `LOW_TTC` → `BRAKE_ONSET`, `DECELERATION` | `TRIGGERS` | 0.60 | 2.5 s | yes | A TTC below the comfort threshold typically produces ordinary service braking; the weaker prior reflects that the driver may instead simply lift off. |
| `rapid_closing_triggers_braking` | `RAPID_CLOSING` → `BRAKE_ONSET`, `HARD_BRAKE` | `TRIGGERS` | 0.55 | 2.5 s | yes | Fast closure is perceptible (looming) before any TTC threshold is crossed, so it can explain a brake application that *precedes* the TTC events. |
| `lateral_threat_triggers_evasive_steering` | `CUT_IN_LIKE_MOTION`, `LATERAL_CROSSING`, `PREDICTED_PATH_CONFLICT`, `CONFLICT_REGION_ENTRY` → `STEER_ONSET`, `SIGNIFICANT_HEADING_CHANGE`, `LANE_CHANGE_LIKE_MANEUVER` | `TRIGGERS` | 0.50 | 3.0 s | yes | A threat that is lateral rather than straight ahead is commonly answered by steering away; the modest prior reflects that braking is the more frequent response. |

#### Own actuation → own motion (mechanical, short lag)

| Rule | Cause → Effect | Edge | prior | lag | self eff. | Why |
|---|---|---|---|---|---|---|
| `brake_command_decelerates_vehicle` | `BRAKE_ONSET`, `HARD_BRAKE` → `DECELERATION`, `HARD_DECELERATION` | `CONTRIBUTES_TO` | 0.85 | 1.5 s | yes | The brake command is the actuation and the measured longitudinal deceleration is its mechanical consequence, delayed only by hydraulic build-up and tyre response. |
| `throttle_command_accelerates_vehicle` | `THROTTLE_ONSET` → `ACCELERATION`, `VEHICLE_STARTED` | `CONTRIBUTES_TO` | 0.85 | 2.0 s | yes | Symmetrically to braking: applying throttle is what makes our own speed rise, and what moves a standing vehicle off. |

#### Own behaviour raising the risk we then observe

| Rule | Cause → Effect | Edge | prior | lag | Why |
|---|---|---|---|---|---|
| `own_acceleration_closes_gap` | `ACCELERATION`, `VEHICLE_STARTED` → `RANGE_DECREASING`, `RAPID_CLOSING`, `LOW_TTC` | `INCREASES_RISK_OF` | 0.40 | 3.0 s | Closure is relative: our own acceleration shortens the gap to anything ahead just as the target's braking does. Stating it keeps the reconstruction symmetric instead of always blaming the other party. |
| `own_lateral_manoeuvre_creates_conflict` | `STEER_ONSET`, `SIGNIFICANT_HEADING_CHANGE`, `LANE_CHANGE_LIKE_MANEUVER` → `PREDICTED_PATH_CONFLICT`, `CONFLICT_REGION_ENTRY`, `LATERAL_CROSSING` | `INCREASES_RISK_OF` | 0.40 | 3.0 s | Our own steering changes our predicted path, so a conflict appearing just afterwards may have been created by us. The deliberate mirror image of `lateral_threat_triggers_evasive_steering`; which survives is decided by the observed ordering, and by cycle rejection when the ordering is ambiguous. |

#### Outcomes

| Rule | Cause → Effect | Edge | prior | lag | Why |
|---|---|---|---|---|---|
| `critical_ttc_causes_collision` | `CRITICAL_TTC` → `COLLISION` | `CAUSES_OUTCOME` | 0.90 | 3.0 s | A TTC inside the critical band followed by an impact is the strongest onboard explanation of that impact: the collision is the TTC running out. |
| `unmitigated_conflict_causes_collision` | `RAPID_CLOSING`, `CONFLICT_REGION_ENTRY`, `CUT_IN_LIKE_MOTION` → `COLLISION` | `CAUSES_OUTCOME` | 0.50 | 4.0 s | Fallback for impacts the TTC estimator never flagged -- a short-range cut-in or an intersection conflict can collide before any TTC sample is confirmed. |
| `conflict_causes_near_miss` | `CRITICAL_TTC`, `LOW_TTC`, `CONFLICT_REGION_ENTRY` → `NEAR_MISS` | `CAUSES_OUTCOME` | 0.65 | 3.0 s | A near miss is a conflict that materialised without contact; the conflict indicators are what make the encounter a near miss rather than ordinary traffic. |
| `braking_prevents_collision` | `HARD_BRAKE`, `HARD_DECELERATION`, `BRAKE_ONSET` → `NEAR_MISS` | `PREVENTS` | 0.70 | 3.0 s | A near miss is a collision that did not happen. When our own braking precedes it, the braking is the averting action -- hence `PREVENTS`: the edge claims the cause *removed a worse outcome*, not that it produced this one. |
| `steering_prevents_collision` | `STEER_ONSET`, `SIGNIFICANT_HEADING_CHANGE`, `LANE_CHANGE_LIKE_MANEUVER` → `NEAR_MISS` | `PREVENTS` | 0.45 | 3.0 s | The evasive-steering counterpart; weaker because a steering input near an encounter is also consistent with ordinary path following. |
| `collision_forces_stop` | `COLLISION` → `POST_IMPACT_STOP`, `HARD_DECELERATION` | `TRIGGERS` | 0.85 | 4.0 s | The impact, plus the post-impact braking it provokes, is what brings the vehicle to rest. `TRIGGERS` rather than `CAUSES_OUTCOME`, because the standstill is a consequence of the outcome, not the forensic outcome under investigation. |

**23 rules in total** (9 conflict-development, 4 perception→reaction, 2
actuation→motion, 2 own-behaviour-raises-risk, 6 outcome). The `PREVENTS` type is what lets the model say "this action
acted *against* the outcome" -- essential for not mistaking a victim's late
braking for a cause.

### 2.2 Tuning without editing code

`load_rules(cfg)` applies two configuration mechanisms:

* `causal_rules.default_max_lag_s` (4.0 s) is a **global ceiling**: a rule whose
  declared window is longer is clipped, so one value can tighten the whole table,
  while rules with shorter, mechanically motivated windows keep them.
* `causal_rules.overrides.<rule name>.<field>` adjusts one rule. Only
  `OVERRIDABLE_FIELDS` may be set -- `enabled`, `prior`, `max_lag_s`, `edge_type`,
  `require_same_subject`, `require_self_effect`; `enabled: false` removes the rule
  entirely. An explicit `max_lag_s` override is honoured as given and *not*
  clipped, otherwise asking for a longer window would silently do nothing.

Cause/effect type lists are deliberately **not** overridable: changing which event
types a rule relates changes the scientific claim and belongs in code review.
Unknown rule names and unknown field names raise, because a silently ignored
override would make a published configuration a lie about what was run. Disabling
every rule raises too. The table actually used is written into the graph's
`meta["rules"]`.

---

## 3. Edge confidence

For a rule `r` firing on cause `c` and effect `e` separated by
`lag = e.t_peak - c.t_peak`:

```
node_factor     = w * mean(c.confidence, e.confidence) + (1 - w)
temporal_factor = exp(-|lag| / tau)
confidence      = clamp( r.prior * node_factor * temporal_factor , 0, 1 )
```

with `w = causal_rules.confidence.node_weight` (0.6) and
`tau = causal_rules.confidence.temporal_decay_s` (3.0 s).

The three terms answer three different questions -- *how plausible is the rule at
all*, *how solid is the underlying detection*, *how tightly did the two events
actually follow each other* -- and **each term is stored on the edge**
(`detail["rule_prior"]`, `["node_factor"]`, `["temporal_factor"]`, `["lag_s"]`,
`["max_lag_s"]`) so a surprising number can be traced to the term that produced
it without recomputing anything. `w` interpolates between "trust the rule" and
"trust the detector": at `w = 0` node confidence is ignored entirely.

**Why the absolute value.** `|lag|` is the one documented refinement of the
literal `exp(-lag / tau)`, and it matters only inside the small negative band that
`causal_rules.min_lag_s` (-0.15 s) tolerates for sampling jitter. For the ordinary
`lag >= 0` the two formulas are identical. For a negative lag the literal formula
would return a factor *greater than one* and inflate the edge above its rule
prior; merely clamping the lag at zero fixes that but introduces a subtler error,
because every time-reversed pair would then score a flat 1.0 -- strictly better
than any correctly ordered pair, however tight. Two mirror-image rules
(`own_lateral_manoeuvre_creates_conflict` and
`lateral_threat_triggers_evasive_steering`) compete for exactly such pairs, and
the observed ordering is the only evidence that can separate them.

An edge is kept only when its confidence reaches
`causal_rules.min_edge_confidence` (0.25); the rejection count goes into
`meta["rule_statistics"]["n_below_min_confidence"]`.

**Guardrail.** `causal_rules.min_lag_s` may not be more negative than
`MAX_JITTER_TOLERANCE_S = 0.5 s`. The negative minimum exists to absorb two
extractors ordering their peaks a few milliseconds either way at a 20 Hz tick; it
is *not* a backwards-causation switch, and a generously negative configuration
value would quietly repeal the project's stated contract for every rule at once.
`build_causal_graph` also validates `min_edge_confidence`, `node_weight` and
`temporal_decay_s` **before** any pair is examined, so a trace that happens to
produce no candidates cannot silently accept a nonsensical configuration and
stamp it into `meta`.

**At most one edge per ordered node pair.** When several rules explain the same
pair, the strongest becomes the edge and the others are listed in its
`detail["alternatives"]` (rule, edge type, confidence, sorted). Parallel edges
would make the document ambiguous about which claim it asserts; dropping the
losers silently would hide competing explanations.

---

## 4. DAG enforcement and cycle rejection

The rule table is intentionally **not** a DAG over event *types*: a steering input
can create a conflict and a conflict can provoke a steering input, and deciding
which happened is exactly what a reconstruction is for. On concrete events the
observed ordering usually settles it, but jitter tolerance and repeated events can
still close a loop.

`enforce_dag(doc)` resolves this by considering edges in **descending confidence**
(ties broken deterministically by source, target, edge type) and adding them one
at a time. An edge is rejected when:

| Reason recorded | Condition |
|---|---|
| `self loop: an event cannot cause itself` | `source == target` |
| `a stronger edge already connects this ordered pair` | the pair is already occupied |
| `would close a cycle: <target> already reaches <source> through accepted, more strongly supported edges` | `nx.has_path(graph, target, source)` |

Greedy insertion in confidence order is the standard approximation to the maximum
acyclic subgraph problem, and it has the property that matters forensically: **the
claim that survives a contradiction is the best-supported one**. Every rejection is
recorded in `meta["rejected_edges"]` as
`{source, target, edge_type, rule, confidence, reason}`, so a suppressed
hypothesis stays visible instead of vanishing. An edge referencing a node that is
not in the document raises rather than being dropped.

The result is verified, not assumed: `build_causal_graph` runs
`nx.is_directed_acyclic_graph(to_networkx(acyclic))` and raises an `AssertionError`
if it fails, because a regression here would silently poison every downstream
analysis. Fusion imposes the same guarantee by **delegating to this same
function** (`docs/GRAPH_FUSION.md` §6).

Nodes are always kept, even when no rule fires on them: "this was observed and
explains nothing" is itself a finding.

---

## 5. Counterfactuals: interventional semantics

### 5.1 What `do(·)` means here

`cdf.causal.scm.StructuralCausalModel` abstracts a reconstructed DAG into named
variables with functional dependences, and `intervene(name, value)` means exactly
what Pearl's `do(X = x)` means: the mechanism that normally sets `X` is replaced
by an external assignment, so edges *into* `X` are cut while edges *out of* `X`
remain.

What the SCM deliberately does **not** do is predict the consequences. It has no
structural equations, no fitted parameters and no distribution over exogenous
noise; propagating a value through it would amount to inventing physics.

### 5.2 Interventions are realised physically

In this project an intervention is a **re-execution**: the identical scenario is
replayed in the simulator -- same map, same spawn state, same seed, same
controller gains, same sensor configuration -- with one named scripted action
modified. The outcome is then *measured*, not inferred.

`cdf.simulation.runner._apply_intervention` supports five operations on exactly
one `action_id` (`RUNNER_OPS` in `cdf.causal.interventions`):

| op | Effect |
|---|---|
| `disable` | `action.enabled = False` -- the action never fires |
| `delay` | `t_start += seconds` |
| `advance` | `t_start = max(0, t_start - seconds)` |
| `scale` | `params[param] *= factor` |
| `set` | `params[param] = value` |

The modification is applied **before the world is created**, so it changes
behaviour from the first tick and never has to be injected mid-run. Targeting
exactly one action is what isolates a single candidate cause. Unknown action ids
raise, listing the declared actions.

### 5.3 Which interventions are worth replaying

`cdf.causal.interventions.enumerate_interventions` merges two independent sources:

* **the scenario author** -- `intervention_candidates` in the YAML, always
  enumerated even when the reconstruction never noticed them, otherwise a
  reconstruction that missed a cause could quietly remove that cause from the
  experiment;
* **the reconstruction itself** -- `GraphAnalyzer.candidate_intervention_nodes()`
  ranks nodes whose removal destroys causal explanations of the outcome; being
  *events*, they are mapped back onto actions by participant and time proximity.

An action that is both declared and graph-ranked outranks one that is only
declared. The list is capped at `counterfactual.max_interventions` (8) and dropped
candidates are **logged, never silently discarded**.

`GraphAnalyzer` is the structural half, run before any replay: `remove_node()` and
`remove_edge()` report `outcome_still_reachable`, `lost_paths`, `lost_ancestors`
and `outcomes_disconnected`. Two conventions matter there:

* *causal paths start at root causes* -- a path is a complete chain from an
  in-degree-0 node down to the outcome, so path-cut rankings depend on structure
  rather than on chain length;
* *removal is measured against the **original** root set* -- after a deletion the
  graph re-roots itself and the deleted node's children would look like fresh root
  causes, hiding that an explanation was destroyed.

### 5.4 The measured outcome of a replay

`cdf.causal.counterfactuals.CounterfactualOutcome` records, per replay:
`collision`, `collision_pairs`, `t_collision`, `impact_speed`,
`relative_impact_speed` (the delta-v proxy), `min_ttc`, `min_distance`,
`near_miss`, `validation_passed`, `notes`. **`None` means undefined and is never
turned into a zero** -- attribution has to be able to tell "no severity" from
"severity unknown".

Replays run into their own artifact directories (`replay_layout`), so the factual
run is never touched. A replay that fails (dropped connection, occupied spawn,
tripped assertion) is recorded with its error and the suite continues: a missing
replay is reported as missing, never replaced by an assumption.

---

## 6. The contribution score, written out

`cdf.causal.attribution.contribution_score(factual, cf, cfg)`:

```
but_for            = 1 if (factual.collision and not cf.collision) else 0

severity_reduction = (S_factual - S_cf) / S_factual        # None when undefined
                     where S = getattr(outcome, counterfactual.severity_metric)
                     and   counterfactual.severity_metric = "relative_impact_speed"

severity_term      = 1.0                       if severity_reduction is None and but_for == 1
                   = 0.0                       if severity_reduction is None and but_for == 0
                   = clamp(severity_reduction, 0, 1)   otherwise

score = (w_prevent * but_for + w_severity * severity_term) / (w_prevent + w_severity)
```

with

* `w_prevent = counterfactual.contribution.prevention_weight` = **1.0**
* `w_severity = counterfactual.contribution.severity_weight` = **0.5**
* `counterfactual.severity_metric` = **`"relative_impact_speed"`** (the
  alternative is `"impact_speed"`)

so `score ∈ [0, 1]` and prevention dominates: a replay that only made the impact
softer still scores above one that changed nothing. Prevention implies the maximum
severity term by definition -- there was no impact left to be severe -- while an
*unmeasured* reduction contributes `0.0`, because an unmeasured reduction is not
evidence of a reduction. `severity_reduction` returns `None` when either run has
no measured value or when the factual severity is zero and the ratio would be
meaningless; it is negative when the replay was *worse*.

The verdict over a whole intervention set is
`classify_attribution`, which reaches exactly three classes
(`ATTRIBUTION_CLASSES`):

| Class | When | Reported |
|---|---|---|
| `single_initiator` | exactly one action passed the but-for test | that action as `primary_initiator` |
| `shared_contribution` | two or more actions independently passed it | **no** primary initiator; the contribution is shared |
| `insufficient_evidence` | no replay produced a usable outcome, or the collision survived every intervention available | no initiator attributed |

Actions that scored above `counterfactual.contribution.min_reportable_score`
without passing the but-for test are listed separately as *contributing actions*.

> ### This is not a legal fault percentage
>
> The score is a **monotone summary of two measurements from controlled replays,
> on an arbitrary but fixed scale, and it is meaningless outside the intervention
> set that produced it.** `but_for` is a causal contribution *under the stated
> intervention semantics* -- "had this scripted action not been performed as it
> was, no collision would have occurred in this replay". Duty of care, right of
> way and foreseeability are outside this model and cannot be derived from
> onboard evidence. The report carries the disclaimer *"Causal contribution under
> controlled replay semantics. NOT legal fault and NOT a fault percentage."*
> inline, and `cdf.evaluation.attribution_metrics` deliberately refuses to
> collapse its scores into a single "fault score".
>
> **The raw counterfactual outcomes are kept.** `CausalContribution` stores the
> full `CounterfactualOutcome` next to the score; `attribution_report` carries the
> factual outcome, every replay's raw outcome, the verdict *and* the replays that
> failed with their error messages -- so a reader can always ask "what actually
> happened in that replay?", and can tell a hypothesis that was tested and
> rejected from one that was never tested at all. `intervention_results.csv`
> carries the same raw columns (`collision`, `t_collision`, `impact_speed`,
> `relative_impact_speed`, `min_ttc`, `min_distance`, `near_miss`,
> `validation_passed`) alongside `but_for`, `severity_reduction` and
> `contribution_score`. The score never has to be trusted on its own.

`shared_contribution` is the designed result of **S05**, where either
participant's yielding would have prevented the collision;
`insufficient_evidence` is a real result, not a failure to try, and must never be
rewritten into a culprit.
