# Responsibility

Nothing in this layer is a finding of legal fault. What it produces is a
normative violation against a stated benchmark rule, plus evidence of causal
relevance, reported as **supported**, **partial** or **insufficient**. What a
court would make of any of it is a question this project cannot answer and does
not.

## Why it is a separate graph

The physical DAG says a hard brake closed a gap and the closing gap produced an
impact. It cannot say anyone *should* have acted differently — "should" is not a
physical relation — and putting norms in the same graph makes it impossible to
accept the physics while disputing the rule. A reader must be able to do exactly
that, so `fusion/responsibility_graph.json` is a second graph, built from the
first.

## The claim needs both halves

```
STOP_SIGN_DETECTED(B)              a sign was seen
    → STOP_REQUIRED(B)             so an obligation existed
+ NO_STOP_AFTER_STOP_SIGN(B)       and the vehicle did not discharge it
    → STOP_RULE_VIOLATION(B)       so the rule was broken
+ a physical path to the collision
    → RESPONSIBILITY_CONTRIBUTION(B)
```

Neither half alone is enough:

- a vehicle that ran a stop sign a hundred metres from an unrelated collision
  broke a rule without contributing to the outcome → **partial**;
- a vehicle that braked lawfully and was rear-ended contributed physically
  without breaking anything → **partial**, and the report says "A vehicle that
  brakes lawfully and is struck from behind is causally involved and has done
  nothing wrong".

## The pushed vehicle

C hits B, B is shunted into A. B's collision sensor fires with B's mass behind it
and B genuinely strikes A — so a naive ancestry check makes B a contributor to an
impact it could not have avoided.

A blanket rule of "paths may not pass through any impact this vehicle was in"
fails the other way: C also reaches the second impact only through the first, so
C stops being a contributor too. The asymmetry has to come from somewhere, and it
cannot come from asking who struck whom — the collision record deliberately does
not say, and asking the simulator is the privileged shortcut this project exists
to avoid.

What works: **a path may traverse an impact only if the vehicle's own behaviour
independently reaches that impact.** C accelerated into B, so C reaches the first
impact by its own doing and may follow it onward. Nothing B did reaches it, so
for B the route is closed. Striker and struck fall out of the graph.

And if B *had* done something that contributed to being hit — braking hard for no
reason — B would reach the first impact and could follow it onward. Correctly:
B's braking really would be in the chain that ends at A. Whether that counts
against B is the other half of the claim, and a vehicle that braked lawfully
broke no rule however involved it was.

Relevance is computed **per outcome**, not pooled. In a chain a vehicle is usually
a contributor to one impact and not the other, which is precisely what the chain
scenarios test.

## The right-of-way benchmark

Right of way is where a forensic reconstruction is most tempted to overreach. The
rule used here is written out in full, attached to every verdict it produces, and
labelled a benchmark — a convention adopted for this experiment so results are
comparable across runs, not a claim about any jurisdiction.

1. Where one approach is controlled by a stop sign and the other is not, the
   uncontrolled approach has priority.
2. Where both are controlled, priority goes to the vehicle that completed its
   stop first **by a clear margin**.
3. Where neither holds, priority is ambiguous and is reported as such.

**The part that matters most is clause 3.** Two vehicles that stopped a tenth of a
second apart were not clearly anything, and `AMBIGUOUS_PRIORITY` is a result
rather than a failure of the method. S12's `near_simultaneous` variant is designed
to produce it: a method tuned to always return a verdict scores better on a naive
metric there while being wrong.

A right-side tie-break is applied only where a scenario explicitly configures one.
It is a local convention, and applying it silently would put a jurisdiction's rule
into results that name none.

| Verdict | When |
|---|---|
| `PRIORITY_TO_UNCONTROLLED` | one approach faced a sign, the other did not |
| `PRIORITY_BY_ARRIVAL` | both faced signs; one stopped clearly first |
| `PRIORITY_BY_CONFIGURED_TIE_BREAK` | close arrival, and the scenario declares a tie-break |
| `AMBIGUOUS_PRIORITY` | close arrival with no tie-break, or a stop never completed |
| `NO_CONTROL_OBSERVED` | no vehicle saw a sign — which is not the same as no rule applying |

## Eight findings, never a number

`fusion/responsibility_report.json` reports, per participant:

| Finding | Values |
|---|---|
| physical causal contributor | yes / no / uncertain |
| but-for contribution | yes / no / **not tested** |
| traffic-control violations | the rules broken, with what showed it |
| temporal-property failures | which properties failed, and where |
| non-action evidence | what was not done, and over what interval |
| mitigating actions | what reduced the outcome |
| prevention opportunities | what would have helped |
| responsibility evidence | supported / partial / insufficient |

"Not tested" is the common case for but-for, and it is a real third value: a
counterfactual replay needs the simulator, and a run analysed offline has no
evidence either way. Reporting that as "no" would turn an absence of experiment
into a finding.

**Prevention opportunities are kept out of the but-for column.** Advancing or
strengthening a safety action can avert an outcome without the original action
having caused it — see `docs/COUNTERFACTUALS.md`. Folding them in would make
every vehicle that could have braked sooner a cause of what happened.

### Why there is no percentage

A number invites arithmetic: 70 and 30, summing to a whole, apportioning
something. Nothing here sums. Two vehicles can both be supported contributors, or
neither can be, and a share of an incident is not a quantity this method measures
— or that any method could measure from telemetry.

A test walks every string of real output and permits *fault*, *guilt*,
*liability* and *blame* to appear only inside the disclaimers that say what this
layer is not.

## Node types

`STOP_REQUIRED` `YIELD_REQUIRED` `PRIORITY_GRANTED` `PRIORITY_AMBIGUOUS`
`STOP_RULE_VIOLATION` `YIELD_RULE_VIOLATION` `SOLID_LINE_VIOLATION`
`UNSAFE_CONFLICT_ENTRY` `RESPONSIBILITY_CONTRIBUTION` `MITIGATING_RESPONSE`

These are deliberately **not** in `EventType`. An obligation is not an observable
event, and the event ontology exists to say what a reconstruction and a
privileged trace can both assert about the world.

## Where this is written down

| Concern | File |
|---|---|
| Obligations, violations, contribution | `src/cdf/responsibility/graph.py` |
| The benchmark rule | `src/cdf/responsibility/priority.py` |
| The eight findings | `src/cdf/responsibility/report.py` |
| Tests, including the five §37 cases | `tests/unit/test_responsibility.py` |
| But-for versus prevention | `src/cdf/causal/attribution.py` |
