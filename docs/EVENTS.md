# Events

Everything this project says about an incident is said in events. There are 38
types and they fall into six families, and which family a type belongs to decides
what it means, who may assert it, and whether it takes part in scoring.

The families are declared once, in `src/cdf/graph/ontology.py`, and every type
belongs to exactly one. A test asserts that.

## Why the families exist

A structural metric compares two graphs, and it is only meaningful if both graphs
are *allowed to say the same things*. For most of this project's life they were
not. The privileged reference emitted `ORACLE_SCRIPTED_INTERVENTION` — a record
that the scenario script had fired — and no reconstruction built from telemetry,
controls and radar has any node of that kind. Every edge touching one was
unmatchable however well the incident had been reconstructed, and **53.4% of
reference edges touched one**. Meanwhile the reconstruction asserted fourteen
types the reference never produced, so each was counted a false positive.

The comparison was unfair in both directions at once, and the resulting F1 was
largely measuring the vocabulary gap. The ontology is the fix: it states the
vocabulary the two sides share, and classifies every type that is *not* shared
into the reason it is not.

## The comparable families

These are what the primary graph comparison is computed over. Both an exact
simulator trace and an onboard reconstruction may assert them; they reach them by
different routes, which is what makes the comparison a measurement rather than a
tautology.

### Own vehicle — 11 types

`VEHICLE_STARTED` `ACCELERATION` `DECELERATION` `HARD_DECELERATION`
`BRAKE_ONSET` `HARD_BRAKE` `THROTTLE_ONSET` `STEER_ONSET`
`SIGNIFICANT_HEADING_CHANGE` `LANE_CHANGE_LIKE_MANEUVER` `FULL_STOP`

**Produced by** a vehicle's own controls and its own accelerometer, needing
nothing outside itself. **Why it matters:** these are what a vehicle did, and
every causal chain in the project has one of them somewhere near its root. One
vehicle, no subject. The reference reads the same facts from exact controls and
exact velocity, so the comparison is between two instruments, not two
vocabularies.

### Interaction — 8 types

`RANGE_DECREASING` `RAPID_CLOSING` `LOW_TTC` `CRITICAL_TTC` `LATERAL_CROSSING`
`CUT_IN_LIKE_MOTION` `PREDICTED_PATH_CONFLICT` `CONFLICT_REGION_ENTRY`

**Produced by** radar returns a vehicle has resolved into a track, and the
geometry it computes from them. **Why it matters:** this is where one vehicle's
account first mentions another, and it is what turns a set of separate logs into
an encounter. `participant_id` observes, `subject` is observed. The reference
computes the same relations from exact relative geometry.

### Road and camera — 7 types

`STOP_SIGN_DETECTED` `YIELD_SIGN_DETECTED` `STOP_LINE_DETECTED`
`STOP_LINE_CROSSED` `LANE_MARKING_CROSSED` `SOLID_LINE_CROSSED`
`ROAD_BOUNDARY_CROSSED`

**Produced by** the forward camera, for the signs and the stop line, and by the
onboard lane sensor, for the crossings. **Why it matters:** an obligation has to
come from somewhere, and this is the only family that supplies one. No sign, no
stop rule to violate. The other party is the road, so there is no subject.

The routes differ most sharply here: a vehicle reads a sign off its own frames
while the reference reads it off the exact map, and that gap **is** the
perception measurement. See [DATA_BOUNDARY.md](DATA_BOUNDARY.md) for what the
vehicle may not consult, and [RESULTS.md](RESULTS.md) §4 for what the detector
was worth.

### Non-actions — 6 types

`NO_STOP_AFTER_STOP_SIGN` `NO_BRAKING_RESPONSE` `NO_YIELD_RESPONSE`
`NO_EVASIVE_RESPONSE` `CONFLICT_ENTRY_WITHOUT_DECELERATION`
`CONTINUED_ACCELERATION_DURING_CONFLICT`

**Produced by** a rule that watches an interval opened by an observed obligation
and finds no qualifying response in it. **Why it matters:** most of what a
responsibility analysis wants to say is about something that did not happen, and
without these there is no node for a causal chain to start at. They are also the
only types whose claim is the *absence* of a signal, which makes them the only
ones assertable without evidence, so they need four conditions rather than one.
Their own section is below.

### Outcomes — 3 types

`NEAR_MISS` `COLLISION` `POST_IMPACT_STOP`

**Produced by** the onboard contact trigger, for a collision, and by the
closest-approach geometry for a near miss. **Why it matters:** this is the thing
to be explained, and every causal chain terminates in one. A collision and a near miss are facts about a *pair*,
and which vehicle a graph files the event under is an artifact of who recorded it
first — so the matcher normalises the pair and treats `COLLISION(A,B)` and
`COLLISION(B,A)` as the same event. `POST_IMPACT_STOP` is deliberately left
alone: it is about one vehicle coming to rest.

## The excluded families, and why

### Sensor-relative — 3 types

`RADAR_TRACK_APPEARED` `RADAR_TRACK_LOST` `TARGET_DECELERATION`

Facts about an instrument rather than about the world. A radar track appearing is
real and worth recording, but the simulator has no radar tracks — it has
vehicles — so there is nothing privileged to compare against. Excluded from the
primary comparison rather than counted as errors.

### Design reference — 3 types

`ORACLE_SCRIPTED_INTERVENTION` `ORACLE_RIGHT_OF_WAY_CONFLICT`
`ORACLE_SIGNAL_VIOLATION`

Privileged knowledge of what the scenario *intended*. Retained, because "did the
designed mechanism actually execute?" is a real question — it is answered against
the scenario design reference, never against a reconstruction.

Every exclusion carries a stated reason, and the reason travels into the diff
artifact. A metric that silently dropped nodes could be gamed by emitting more of
whatever it drops.

## Non-actions need four things

A non-action is the claim that a required response was absent, and the evidence
for it is the absence of a signal — which is worth nothing unless you were
actually looking. `src/cdf/graph/non_actions.py` will not emit one without all
four of:

1. **A real observed obligation.** A stop sign the camera saw; a critical
   time-to-collision the radar measured. Never "the scenario configured a brake
   here" — a non-action derived from the scenario's intent would make the design
   reference and the reconstruction agree by construction.
2. **A bounded interval.** "B never yielded" is not checkable; "B did not
   decelerate between first seeing the sign and crossing the line" is.
3. **Evidence covering that interval.** If the recorder dropped samples across
   the window, the response may simply not have been recorded.
4. **No qualifying response inside it.**

The third is the one that keeps the metric honest. A detector that skipped it
would produce its most confident failures on exactly the runs where the sensors
worked worst.

A window that opens but is not covered well enough becomes an `UNKNOWN`, recorded
in its own list and kept out of the graph. Those entries are published rather
than dropped, because a detector that stayed silent invisibly cannot be told
apart from one that found nothing. Coverage is also the node's confidence: a
window watched 82% of the time supports a weaker assertion than one watched
throughout.

Two shapes beyond the obvious one. The stop and yield rules run to the event that
*closes* them rather than for a fixed horizon, which is how "did not stop before
the line" becomes expressible. And the conflict rule looks backwards: entering a
junction without having slowed is a claim about the approach.

The privileged reference runs these same rules over its own events. If it used a
laxer definition the comparison would stop measuring whether the vehicle noticed
and start measuring whose rule was looser.

## Two graphs, two vocabularies of relation

The project builds two graphs per vehicle and keeps their edge types strictly
apart, because they make different kinds of claim.

**Event-graph relations** are structural and assert nothing causal:

| Relation | What it says |
|---|---|
| `PRECEDES` | this event happened before that one |
| `OBSERVED_FROM` | this event was derived from that observation |
| `SAME_TRACK` | these observations are of one radar track |
| `INTERACTS_WITH` | these two events involve the same pair of vehicles |
| `ALIGNS_WITH` | these two events, from different recorders, are the same event |
| `ASSOCIATED_WITH` | this track was resolved to that participant |

**Causal-DAG relations** are hypotheses, and every instance carries evidence and
a confidence:

| Relation | What it says |
|---|---|
| `CONTRIBUTES_TO` | this made that more likely or more severe |
| `TRIGGERS` | this is what set that off |
| `INCREASES_RISK_OF` | this raised the risk of that without determining it |
| `PREVENTS` | this acted against that outcome |
| `CAUSES_OUTCOME` | this reaches the outcome being explained |

The separation is the point. `PRECEDES` is cheap and nearly always true;
`CONTRIBUTES_TO` has to be argued for. Collapsing the two would let temporal
order masquerade as causation, which is the specific mistake this project exists
to avoid. The two graphs are written to separate artifacts, scored separately,
and a relation from one is never read as a relation from the other.

## Matching

Node correspondence is a globally optimal assignment over events of the same
type, participant and subject, within a time tolerance. **Event ids are never
compared** — two graphs describing the same incident have no reason to agree
about identifiers. Edges are then compared *through* that correspondence: an
inferred edge counts only when both endpoints matched a reference node and the
reference has the same relation between those two nodes.

## Where this is written down

| Concern | File |
|---|---|
| The families and their exclusions | `src/cdf/graph/ontology.py` |
| The enum itself | `src/cdf/common/schemas.py` |
| Non-action derivation | `src/cdf/graph/non_actions.py` |
| Matching and scoring | `src/cdf/evaluation/graph_comparison.py` |
| The privileged side | `src/cdf/oracle/observable.py` |

Historical note: [`legacy/EVENT_TAXONOMY.md`](../legacy/EVENT_TAXONOMY.md) described the V1 vocabulary, before the
road, non-action and outcome-pair work. It is superseded by this document.
