# Clocks

Every vehicle timestamps with its own clock. Nothing in the recordings says what
any other clock read, so before the logs can be merged something physical has to
link them.

## The method

If A and B were in the same collision, both felt it, and both recorded *when* on
their own clocks. The difference between those two timestamps is the offset
between the clocks:

```
offset(B → A) = t_contact_A − t_contact_B
t_common      = t_local + offset
```

One equation, one unknown, no fitting. `scale` is fixed at exactly **1.0** and
drift is reported as **unestimated** — not as zero, and not as a fitted ppm
figure. A single impact constrains an offset and carries no information whatever
about rate.

## What this replaced, and why

V1 fitted the range and range-rate one vehicle measured against the trajectory
another recorded of itself, and read both an offset and a drift rate off that
fit. It worked. But a drift rate fitted over a 25 s window from noisy radar is a
number with more decimal places than evidence behind it, and the method took a
page to explain.

The radar estimator is still run, as a diagnostic, so the clock ablation can
compare the two. It no longer decides the timeline the results are computed on.

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

The alignment says which anchor is doing double duty and bounds the error it
leaves: no larger than the spread between the times the two counterparties
reported. On the recorded chain the bound is **13 ms**, so the result stands. In
a chain with a longer interval between impacts the bound would be larger, and a
reader of that merged timeline would know.

## Statuses

| Status | Meaning |
|---|---|
| `CONTACT_ALIGNED` | one shared impact tied the recorders together |
| `MULTI_CONTACT_ALIGNED` | more than one |
| `PARTIALLY_ALIGNED` | some recorders aligned, at least one not |
| `AMBIGUOUS_CONTACT_MATCH` | contacts were felt; which is which cannot be decided |
| `UNALIGNED_NO_SHARED_CONTACT` | nothing physical links the clocks |
| `ACQUISITION_START_ALIGNED` | the harness marker below, never a contact result |

The first three are `CONTACT_DERIVED_STATUSES` — the ones whose results say
something about what the method can do.

## No collision, no offset

A contact-anchored method cannot align recordings with no contact in them, and
this is exactly where a silent fallback would do the most damage: the negative
controls *are* those runs, and every one of them would appear perfectly aligned
while resting on knowledge no vehicle has.

So the fallback is explicit, separately named and separately reported. The
experiment harness starts every recorder in one simulator tick, which makes the
first sample of each log a common instant. That is a declared property of the
harness — a clapperboard — not a reconstruction result, and the artifact carries
the caveat in words.

It is **not** simulator time. Simulator time would hand every recorder the engine
clock, erasing the offsets and the jitter the experiment exists to work against.
Here each recorder keeps its own clock and its own jitter; only the single
constant relating them comes from outside.

## What contact alignment costs

It aligns fewer recorders than radar alignment did, and that is asserted in the
test suite rather than glossed. In the partial-view scene A and B collide and C
never touches anything, so C stays on its own clock and is named as unaligned.

A recorder with no common time usually contributes no fused events at all, so the
merged log takes its unaligned set from the alignment as well as from the rows —
otherwise it would report a clean single timeline while silently omitting a whole
vehicle. An unaligned row renders as a dash, never as 0.00.

Measured on that scene, the cost has two parts. C appears nowhere in the fused
graph — not as a participant, an owner or a subject. And B's radar track of C is
never resolved to C, because association needs both ends on one clock, so it stays
`B::T001`.

What survives is weaker and worth stating precisely: the initiating event still
reaches the vehicle that was blind to it, as B's observation of a decelerating
target rather than as C's own record of braking. A reader of the merged graph
learns that something ahead of B slowed down, not that C did. The strong form of
the claim holds on the recorded `S07/occluded` run, where C is in contact.
`docs/LIMITATIONS.md` §22 carries the full statement, including why the harness
marker is not applied to one participant of an otherwise contact-aligned run.

## Where this is written down

| Concern | File |
|---|---|
| Contact alignment and the harness marker | `src/cdf/fusion/contact_alignment.py` |
| The merged log and its honesty about axes | `src/cdf/common/event_log.py` |
| The superseded radar estimator | `src/cdf/fusion/time_alignment.py` |
| Per-recorder clock models | `src/cdf/common/clocks.py` |
| Tests, including the four cases the brief names | `tests/unit/test_contact_alignment.py` |

Historical note: `docs/CLOCK_SYNCHRONIZATION.md` describes the V1 radar-based
method, which is retained for the ablation. This document describes the method
the V2 results are computed from.
