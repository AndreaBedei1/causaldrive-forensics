# Formal methods

Metric temporal logic over a finite, partially observed trace, evaluated with
three-valued semantics.

## The formula is the thing that runs

The previous layer carried a `formal` field beside each property: an MTL-looking
string, written by hand, sitting next to separate Python that computed the
verdict. Nothing checked that the two agreed, and the string appeared in reports
as though it had been evaluated.

`src/cdf/formal/` replaces that with an AST that is evaluated directly. The
rendering in a report and the object that produced the verdict are the same
thing, so they cannot drift apart. A test asserts that every property's published
formula is `render(prop.formula)`.

## The fragment

Occurrence atoms, the Boolean connectives, and five metric operators:

| Operator | Meaning |
|---|---|
| `F[a,b] φ` | eventually: φ holds somewhere in the future interval |
| `G[a,b] φ` | always: φ holds throughout it |
| `O[a,b] φ` | once: φ held somewhere in the past interval |
| `H[a,b] φ` | historically: φ held throughout it |
| `φ S[a,b] ψ` | since: ψ held in the past window, and φ at every instant after |

Intervals are closed and relative to the instant of evaluation.

Atoms bind to participants through three placeholders. A property fires at a
trigger event, and that event supplies `SELF` — the vehicle the obligation falls
on — and `SUBJECT`, the vehicle it is about. `ANY` matches whatever is there.

### Why `Since` had to exist

"A full stop between seeing the sign and crossing the line" is not expressible
with `Once`. `O[0,12] FULL_STOP` asks whether a stop happened in the last twelve
seconds, which is not the obligation — a stop made at a previous junction, before
the sign was ever seen, would satisfy it.

What the rule requires is that nothing violated it *in the stretch between* the
sign and now, and that stretch has a length the formula cannot know in advance.
`Since` finds the most recent marker and then checks from wherever it turned out
to be. It is the only operator whose window is set by an event rather than by a
constant, and both the stop and yield properties need it.

## Three-valued, and why

**Missing evidence never becomes PASS, and never becomes FAIL either.** Both
would be assertions about time nobody watched.

Two situations produce `UNKNOWN`, and they are the same situation seen twice. A
window running past the end of a 25 s recording contains time that was not
observed. A window inside the recording but across a sensor dropout contains time
that was not observed either. In both, an `Eventually` that found nothing has not
established absence — only that it did not see anything.

So the temporal operators check three things in order:

1. is there a witness (or a counterexample) in the part that *was* observed? That
   settles it — a thing seen to happen happened regardless of what else was
   missed;
2. if not, was the whole interval observed and covered? If not, `UNKNOWN`;
3. only then, the negative verdict.

Connectives are Kleene's: `FAIL & UNKNOWN` is `FAIL`, because one false conjunct
is enough whatever the other turns out to be, and symmetrically `PASS | UNKNOWN`
is `PASS`.

## Aggregating over instances

A property fires once per trigger, and the rule for combining is asymmetric on
purpose. One instance failing means the property failed however many others
passed — a vehicle that stopped at four signs and ran the fifth ran a sign. One
instance undecidable and none failing means the property is undecided, because a
pass claimed while an instance is unknown is a pass over unwatched time.

**Vacuity is reported apart from all three.** A property whose trigger never fired
has not passed; there was nothing to pass. Folding those into PASS would make the
pass rate a measure of how few obligations a scenario contained, and the
negative-control runs — where almost nothing triggers — would score best of all.
`n_vacuous` is excluded from `n_checked`, and the unknown rate is over checked
properties only.

## Two vehicles need one clock

A property relating one vehicle's braking to another's conflict entry is
meaningless unless the two recorders share an axis. The trace carries which clock
it is on and which participants are aligned, and a property declared
`needs_two_vehicles` returns `UNKNOWN` on an unaligned trace with that as its
stated reason — rather than quietly comparing timestamps from two different
clocks.

## The properties

| | Title | Trigger | Notes |
|---|---|---|---|
| P1 | a stop sign seen means a full stop before the line | `STOP_LINE_CROSSED` or `LANE_MARKING_CROSSED` | needs `Since` |
| P2 | a yield sign seen means yielding before conflict entry | `CONFLICT_REGION_ENTRY` | needs `Since` |
| P3 | a critical time-to-collision gets a response | `CRITICAL_TTC` | braking or swerving both count |
| P4 | no acceleration into a critical conflict | `CRITICAL_TTC` | distinct from P3 by design |
| P5 | a collision is followed by coming to rest | `COLLISION` | most often `UNKNOWN`, correctly |
| P6 | a solid line is not crossed | `SOLID_LINE_CROSSED` | the trigger is the violation |
| P7 | one impact per pair on the merged timeline | `COLLISION` | two vehicles |
| P8 | a claimed missing braking response really had none | `NO_BRAKING_RESPONSE` | anchors at `t_start` |

### Why P1 has two triggers

The stop obligation's natural boundary is the painted stop line, and Town05
paints no stop bar at any junction where it renders a stop sign
(`docs/LIMITATIONS.md` §24). `STOP_LINE_CROSSED` therefore never fires on a real
run, and the property was permanently vacuous -- not passing, not failing, simply
never asked. The stop-line detector was behaving correctly throughout: it tracked
a bright band, saw it leave the frame upward rather than pass beneath the
vehicle, and refused to claim a crossing. Missing a crossing costs recall;
inventing one would corrupt every non-action built on it.

Crossing into the junction is the same boundary observed another way, and the
vehicle's own lane sensor records it. So P1 accepts either.

This does not weaken the property. Its formula is an implication whose antecedent
is *a stop sign was seen in the last twelve seconds*, so a trigger firing where
no sign was seen -- an ordinary lane change -- is vacuously satisfied rather than
violated. The checker also deduplicates triggers landing on the same instant for
the same vehicle, because a lane sensor reports the marking and the solid line
together and one violation must not be counted twice.

A measured witness, from `S10/rolls_through` on the development seed:

```
P1 = FAIL
  STOP_SIGN_DETECTED    t = 0.570   (camera, confidence 0.90)
  LANE_MARKING_CROSSED  t = 2.770   (lane sensor)
  FULL_STOP             absent in [0.570, 2.770]
```


Three of these are worth a note.

**P3 and P4 are separate on purpose.** A vehicle can brake and then accelerate
again, which satisfies "responded" while still making things worse. A layer with
only one of the two would miss that, and a recorded chain exercises exactly it.

**P5 is the property most often UNKNOWN rather than decided**, because a collision
near the end of a 25 s window leaves the eight seconds after it unrecorded. That
is the correct answer there, not a failure.

**P7 is not what §18 first asked for.** Whether a chain's two impacts are in the
right *order* cannot be checked from the trace at all: a consistently wrong order
is still self-consistent, so that is a question for the reconstruction metrics
against ground truth. What the trace *can* say is that each impact appears once —
two recorders reporting the same contact under a bad alignment show up as one
pair colliding twice a fraction of a second apart. P7 checks that, and its
rationale says what it is not checking.

**P8 anchors at `t_start`.** A non-action node spans the window it monitored and
its `t_peak` is the *end* of that window; evaluating at the peak searched the
1.5 s after the window and found nothing, so every non-action confirmed itself.

## Artifacts

```
formal/
    properties.json   the formulae as written, and what each verdict means
    results.json      one verdict per property, with witness or reason
```

`properties.json` is published separately from the results so a reader can see
what was checked without having to read a result to infer it.

## Where this is written down

| Concern | File |
|---|---|
| The formulae | `src/cdf/formal/syntax.py` |
| Trace, horizon and coverage | `src/cdf/formal/trace.py` |
| Three-valued evaluation | `src/cdf/formal/evaluator.py` |
| The eight properties | `src/cdf/formal/properties.py` |
| Running them, and vacuity | `src/cdf/formal/report.py` |
| Tests | `tests/unit/test_formal_logic.py` |

Historical note: [`legacy/MODEL_CHECKING.md`](../legacy/MODEL_CHECKING.md) describes the V1 layer, whose properties
were hand-written evaluators rather than executable formulae.
