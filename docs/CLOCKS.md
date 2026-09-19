# Clocks

## The problem

Two vehicles collide. A writes the impact down at **5.2 s**. B writes the same
impact down at **5.7 s**.

Neither is wrong. It is one physical event, and their clocks simply start from
different places. Nothing in either recording says what the other clock read, so
half a second of disagreement sits between two accounts of the same moment. Merge
them as they stand and the reconstruction will report a vehicle braking after the
crash it was braking for.

Something physical has to link the two clocks, and it has to be something the
vehicles recorded themselves.

## The hierarchy

Three levels, chosen **per participant**, and every participant records which one
placed it.

**Primary: contact.** If two vehicles were in the same collision, both felt it
and both wrote down when, each on its own clock. The difference between those two
timestamps is the offset between the clocks. One subtraction, no fitting, nothing
modelled in between. This is preferred wherever it is available.

**Secondary: radar.** A vehicle that never collides has no impact to anchor on,
and a chain can produce one recorded impact where two happened. Where contact
cannot reach a participant, or the anchor it would rest on is impeached, the
method fits an **offset only** from radar and trajectory consistency against a
vehicle already placed.

**Last: unresolved.** If neither works, the recorder keeps its own clock and the
artifact says so. It is never placed on a guess.

The result, in both cases:

```
t_common = t_local + offset
scale    = 1
```

**Drift is not estimated.** The method fits one number per recorder, not two.
*Scale and drift* below says why, and [RESULTS.md](RESULTS.md) measures what the
choice costs.

## The method in detail

### Contact, where there is one

The subtraction, written out:

```
offset(B -> A) = t_contact_A - t_contact_B
t_common       = t_local + offset
```

One equation, one unknown, no fitting. This is the preferred source because it is
direct and interpretable, and because nothing is modelled in between.

### Radar, where contact cannot reach

Contact alone is not enough, and two recorded cases show why. A vehicle that
never collides has no anchor at all: in the partial-view scene the leader only
brakes, and contact-only leaves its whole account off the merged timeline. And a
chain can yield one anchor where two impacts happened. On the recorded three-car
case the middle vehicle registered a single contact, and the third vehicle's
timeline moved by exactly the 0.200 s between the two impacts.

So where a participant has no contact, or the contact matching was ambiguous, or
its offset is impeached by the shared-anchor caveat, an **offset-only** radar and
trajectory fit is tried. It estimates one number. If it does not clear its
confidence floor, or two independent pairings disagree, the recorder stays
unresolved rather than being placed on a guess.

### Never both

Contact and radar are not averaged. Averaging a good estimate with a bad one
produces a value neither supports, and this project measured that happening: on
the chain, a true impact implied +0.267 s, a spurious pairing -0.083 s, and the
median +0.092 s. The chosen source, the estimate each source gave, and the reason
for the choice are all recorded.

### Scale and drift

`scale` is fixed at exactly **1.0** on both paths and drift is reported as
**unestimated**, not as zero and not as a fitted ppm figure. A single impact
constrains an offset and carries no information about rate; a rate fitted over a
twenty-second window from trajectory residuals is a number with more decimal
places than evidence behind it. `offset_only` is an argument to the estimator
rather than a configuration key, so it cannot be switched back on by a file the
results then rest on.

| source | meaning |
|---|---|
| `REFERENCE` | the gauge the common timeline is expressed in |
| `CONTACT` | tied in by a shared physical impact |
| `RADAR` | placed by an offset-only trajectory fit |
| `UNRESOLVED` | neither source sufficed; the recorder stays on its own clock |
| `ACQUISITION_START` | no impact and no usable radar geometry anywhere in the run, so the harness marker described below placed every recorder. Never a result of the method |

## What this replaced, and why

V1 fitted range and range-rate against another vehicle's recorded trajectory and
read **both** an offset and a drift rate off that fit. V2 keeps the estimator and
drops the drift.

It also fixed a defect that fit had carried all along. A radar return comes off
the target's nearest surface, not the trajectory point its own telemetry reports,
and on the partial-view geometry that is a -2.35 m bias. Unmodelled, the fit paid
for it in *time*: +0.150 s against a true offset of zero, because position and
time are exchangeable for a target at constant speed. They stop being
exchangeable when the target changes speed, and a vehicle braking from 14 m/s to
rest separates them decisively. The bias is now a fitted nuisance parameter,
reported and never mistaken for a clock. That took the fallback from 0.150 s of
error to 0.0011 s on the same geometry.

The whole-run V1 estimator is still run unchanged, as a diagnostic, so the clock
ablation can compare the two. It does not decide the timeline the results are
computed on.

## Matching the anchors

The collision sensor does not report *who* it hit — deliberately, since knowing
that would be privileged. So which of A's impacts corresponds to which of B's has
to be inferred. Each candidate pairing is scored on two things a recorder can
know about itself:

- **impulse** — by Newton's third law the two parties to one impact feel equal
  and opposite impulses, so their magnitudes should agree. On a recorded
  three-car chain the two parties reported 11 569 N·s each, to the unit;
- **place** — each vehicle knows where *it* was, from its own localisation. Two
  vehicles in one collision are within a car length of each other.

Three things about the matching only became apparent on real recordings.

**Resting contact is not an impact.** After a pile-up the vehicles stay touching
and the sensor goes on reporting roughly twice a second for the rest of the run:
43 such reports at 30–290 N·s beside the one real impact at 11 569. They are too
far apart in time for a burst merge to reach and they look, to the matcher,
exactly like impacts. Left in they do active harm — two recorders both rubbing
produce a high-scoring pairing at an arbitrary time. An anchor must therefore
carry a real share of the momentum that recorder felt, tested relative to its own
peak so the threshold needs no knowledge of the scenario's scale.

**Greedy matching cannot use the evidence that separates similar impacts.** When
each recorder felt two, the impulses are useless but the times are decisive,
because only one pairing implies a consistent offset for both — and that is a
property of the assignment as a whole, invisible to any rule that commits to the
best single pairing first. Matching is an assignment search scored on joint
consistency. Only *maximal* assignments compete: comparing a two-pairing
assignment against a subset of itself on mean score is unfair to the larger one,
and made every two-impact run look ambiguous.

**Disagreeing pairings must not be averaged.** On one recording a true impact
implied +0.267 s and a spurious pairing implied −0.083 s; their median was
+0.092, a value neither piece of evidence supported. Offsets that agree within
tolerance are still averaged; offsets that disagree resolve to the
better-evidenced pairing.

## Three cars

Alignment is transitive but not direct: A and C may never touch. A–B from impact
one and B–C from impact two put all three on one axis through B.

This is where position evidence stops being enough on its own. In a chain all
three vehicles are within a car length of each other at impact, so pairing the
two outer cars looks perfectly plausible on position even though they never
touched. The timeline is therefore grown from the **best-supported links** — a
maximum spanning tree on match score — and the links the tree did not need are
checked against it.

A contradicting link needs a judgement, and the first version got it wrong by
calling the whole run ambiguous, which would make every three-car run ambiguous.
The spurious link is not a tie: its impulses disagree, so it scores distinctly
lower. A contradicting link that is *clearly weaker* is rejected in favour of the
alignment and recorded as rejected; one the evidence does not separate leaves the
run `AMBIGUOUS_CONTACT_MATCH`. Two config knobs, because "are these two pairings
too close to call" and "is this link clearly the weaker hypothesis" are different
questions.

### One impact doing duty for two

In a chain the middle vehicle often registers *one* impact rather than two — its
collision sensor reported a single event — so its single anchor relates both
neighbours. That may be a genuine three-way impact or a missed second contact,
and the recordings cannot distinguish them.

The alignment says which anchor is doing double duty, which pairing through it
the impulse evidence favours, and which recorders therefore carry a suspect
offset. It does **not** put a number on the error, and an earlier version did.

That version took the two counterparties' local timestamps and subtracted them —
two readings from two different clocks, which is the error this whole document
exists to correct, committed inside the code that corrects it. On the recorded
chain it reported a bound of **13 ms**. The offset was in fact out by **200 ms**,
and the reassuring small number was worse than no number at all.

The honest position: if the middle vehicle never registered its second impact, it
has no measurement of when that impact happened, so nothing in the recordings
bounds how far the derived offset is out. The interval between the two impacts
*is* the error, and it is unobserved. The artifact therefore carries
`offset_error_bound_s: null` and `error_bound_determinable: false`.

What that cost on the recorded chain, measured against the privileged record: on
`S06/a_front_pushed` seed 2 the A to B offset was out by 0.000625 s and C's by
0.199960 s, which is the interval between the two impacts. Two impacts 0.200 s
apart were reconstructed onto the same instant, so their order was not recovered.
The supervisor table's `collision_order` column reports that as not established
rather than printing the order a timestamp sort happens to produce.

The caveat travels with the participant only for as long as it applies. Being
named in it is exactly what sends a recorder to the radar fallback, so once radar
has placed that recorder it is no longer resting on the impeached anchor, and the
column stops withholding an order on its account. That is why seed 0 of the same
variant, where radar did engage, reports its order and reports it correctly.

## Statuses

Run level:

| Status | Meaning |
|---|---|
| `CONTACT_ALIGNED` | one shared impact tied the recorders together |
| `MULTI_CONTACT_ALIGNED` | more than one |
| `RADAR_ALIGNED` | every non-reference recorder was placed by the fallback |
| `HYBRID_ALIGNED` | some on contact, some on radar |
| `PARTIALLY_ALIGNED` | at least one recorder could not be placed at all |
| `UNRESOLVED_TIME_ALIGNMENT` | none could |
| `AMBIGUOUS_CONTACT_MATCH` | contacts were felt; which is which cannot be decided |
| `UNALIGNED_NO_SHARED_CONTACT` | nothing physical links the clocks |
| `ACQUISITION_START_ALIGNED` | the harness marker below, never a reconstruction result |

Per participant, the `source` field carries `REFERENCE`, `CONTACT`, `RADAR` or
`UNRESOLVED`. Reading the run status alone would hide that one vehicle on a
timeline rests on a fitted trajectory while the others rest on a physical impact.

## No collision, and no radar either

A contact-anchored method cannot align recordings with no contact in them, and
the radar fallback needs a tracked target with enough varying geometry to
separate an offset from a spatial bias. Where **neither** is available, and the
negative controls are the clearest case, a silent fallback would do the most
damage: every one of those runs would appear perfectly aligned while resting on
knowledge no vehicle has.

So that last fallback is explicit, separately named and separately reported. The
experiment harness starts every recorder in one simulator tick, which makes the
first sample of each log a common instant. That is a declared property of the
harness, a clapperboard rather than a reconstruction result, and the artifact
carries the caveat in words. It is used only when no recorder could be placed by contact
or radar, and it is **never** applied to one participant of a run whose others
rest on physics: that would put offsets of two provenances on one timeline and
report them identically.

It is **not** simulator time. Simulator time would hand every recorder the engine
clock, erasing the offsets and the jitter the experiment exists to work against.
Here each recorder keeps its own clock and its own jitter; only the single
constant relating them comes from outside.

## What contact alone costs, and what the fallback buys

This is measured rather than argued, and it is why the hierarchy exists.

In the partial-view scene A and B collide and C never touches anything. With the
fallback disabled, which is how the ablation runs, C stays on its own clock and
is named unaligned, and the cost has two parts: C appears nowhere in the fused
graph, not as a participant, an owner or a subject; and B's radar track of C is
never resolved to C, because association needs both ends on one clock, so it
stays `B::T001`.

With the fallback, on the recorded `S07/occluded` seed 0:

| id | source | offset | true (relative) | error |
|---|---|---|---|---|
| A | `REFERENCE` | +0.000000 | +0.000000 | +0.000000 |
| B | `CONTACT` | +0.233566 | +0.234189 | −0.000623 |
| C | `RADAR` | +0.005173 | +0.007568 | **−0.002395** |

C enters the merged log, B's track resolves to C, and C appears in the fused
graph by name.

All six S07 runs behave this way: A reference, B contact, C radar, every run
`HYBRID_ALIGNED`. Across those six, C's offset error averages **0.0021 s** and
reaches **0.0032 s** at worst. A recorder with no physical anchor is placed on
the common timeline to within a fifteenth of a simulator tick, from trajectory
consistency alone.

On the recorded three-car chain the picture is mixed, and that is the result
rather than a caveat on it. `S06/a_front_pushed` runs on three seeds, and the
middle vehicle registers one contact for two impacts in all of them:

| Seed | Status | C placed by | C offset error | Collision order |
|---|---|---|---|---|
| 0 | `HYBRID_ALIGNED` | `RADAR` | −0.001958 s | **correct** |
| 1 | `MULTI_CONTACT_ALIGNED` | `CONTACT` | −0.249685 s | single impact reconstructed |
| 2 | `MULTI_CONTACT_ALIGNED` | `CONTACT` | −0.199960 s | **not established** |

On seed 0 the radar fallback engaged, replaced C's impeached contact offset, and
the two impacts came apart far enough to be ordered correctly. On seeds 1 and 2
it did not engage, C kept a contact offset out by a quarter and a fifth of a
second, and the method declined to order the impacts rather than sorting two
timestamps that had been collapsed onto one instant.

**The fallback fixes this chain on one seed of three.** What it needs is a
tracked target whose geometry varies enough to separate an offset from a spatial
bias, and the other two seeds do not give it one. The ambiguous cases stay
flagged; none of them is forced.

A recorder with no common time contributes no fused events, so the merged log
takes its unaligned set from the alignment as well as from the rows. Otherwise it
would report a clean single timeline while silently omitting a whole vehicle.
An unaligned row renders as a dash, never as 0.00.

`docs/LIMITATIONS.md` §22 carries the full statement of what contact alone costs.

## Where this is written down

| Concern | File |
|---|---|
| Contact alignment and the harness marker | `src/cdf/fusion/contact_alignment.py` |
| The merged log and its honesty about axes | `src/cdf/common/event_log.py` |
| The superseded radar estimator | `src/cdf/fusion/time_alignment.py` |
| Per-recorder clock models | `src/cdf/common/clocks.py` |
| Tests, including the four cases the brief names | `tests/unit/test_contact_alignment.py` |

Historical note: [`legacy/CLOCK_SYNCHRONIZATION.md`](../legacy/CLOCK_SYNCHRONIZATION.md) describes the V1 radar-based
method, which is retained for the ablation. This document describes the method
the V2 results are computed from.
