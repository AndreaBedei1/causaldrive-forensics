# Limitations

Read this before the results. Everything below constrains what the numbers in
[RESULTS.md](RESULTS.md) — and the generated tables they come from — can
support.

## 1. Simulation-to-reality gap

### Recorder clock synchronization

Independent clock offsets/drift/jitter are configurable experimental
perturbations, not empirically measured automotive clock distributions. Only a
reference-recorder time gauge is observable, not absolute simulator time. Radar
surface centroids differ from self-reported vehicle origins; robust fitting and
supplementary compatible collision triggers reduce, but cannot eliminate, bias.
Constant motion, short tracks, fragmented tracks, dropout or ambiguous identities
can make time alignment unresolved. Those local graphs remain valid but are not
included in common-time cross-vehicle fusion.

Drift needs sufficiently long, informative evidence. A short CARLA crash usually
produces an offset-only estimate; this is not proof that its clock has no drift.
Confidence and Jacobian uncertainty are heuristic diagnostics, not calibrated
coverage guarantees. Large jitter may activate monotonic clamping and distort
elapsed local time. The A/B/C driver uses a restamped time-only synchronized
control on the same recording, not a separate online-recorder/physics experiment.
The old campaign remains a synchronized-clock baseline; independent-clock smoke
tests do not replace a full newly generated campaign or establish real-world
clock robustness.

The A/B/C ablation has since been run over the whole campaign rather than a
seed-0 smoke test, and the conclusion is sharper than the smoke test suggested:
estimated alignment improves offset accuracy substantially and leaves the graph
metrics flat, for the reason given in §16. The causal and temporal rules were not
adjusted to make either half of that look better. The measured table is in
[RESULTS.md](RESULTS.md) and regenerates from the artifacts.

Every result comes from CARLA 0.9.15. The vehicle dynamics, tyre model, impact
response and — especially — the radar model are simulator approximations. A
conclusion of the form "fusion recovered the initiating cause" is a statement
about this simulator, not about road vehicles.

Nothing here has been validated against real vehicle data, real radar returns or
a real crash.

## 2. Radar simplifications

The CARLA radar is a ray-cast range/azimuth/elevation/range-rate sensor. It has
no radar cross-section model, no multipath, no interference, no angular
side-lobes, no separate detection-probability model, and its returns are
noise-free unless we add noise ourselves.

Consequences that matter for the conclusions:

* **Object extent is unrealistically clean.** Clustering separates vehicles more
  easily than a real radar would.
* **Our degradation profiles are injected, not physical.** `radar_noisy`,
  `radar_dropout` and `radar_degraded` apply Gaussian noise and Bernoulli
  dropout *after* acquisition. That makes them reproducible from a seed, but
  they are a model of degradation, not measured degradation.
* **The stationary-target discriminator is unusually effective here.** It rejects
  world-fixed clutter by comparing measured range rate against
  `-(v_forward·cos az + v_lateral·sin az)`. With noise-free simulated range
  rates this separates cleanly; with real radar noise the tolerance would have to
  be wider and the rejection correspondingly worse.
* **TTC is referenced to the vehicle origin, not the bumper.** `range_m` is the
  range of the body-frame cluster centroid while `range_rate` is measured along
  the sensor line of sight, and the radar is mounted 2.2 m forward of the
  vehicle origin. TTC is therefore optimistic by roughly
  `2.2 / closing_speed` seconds. This is documented in
  `cdf.local.radar` rather than silently corrected.

## 3. Post-impact tracking degrades

Radar tracking is reliable *before* an impact and demonstrably poor after one.
During the post-crash spin the sensor's own motion is large and rapidly
changing, and although the discriminator compensates for body-frame velocity and
for lever-arm rotation (`omega x r`), spurious tracks still appear in the frames
around the impact.

This is mitigated (tracks sustained only by world-fixed returns are dropped after
a bounded number of frames) but not eliminated. Pre-impact evidence — which is
what carries causal weight — is clean; post-impact node counts are noisy and the
graph-structure metrics inherit that noise.

## 4. Scripted scenarios

Participants follow scripted routes and scripted actions. They do not perceive
each other and do not react to each other: a "reaction" is a scripted brake at a
chosen time, not a controller responding to a detected threat.

This is deliberate — it makes the ground-truth causal structure known and the
counterfactuals controlled — but it means:

* the scenarios contain no naturalistic driver behaviour or behavioural variety;
* the *timing* of every response is a design parameter rather than a measurement;
* results do not generalise to a fleet of independently behaving agents.

## 5. Scenario tuning is empirical

Several scenarios needed their approach distances and entry speeds tuned by
measurement to produce the intended encounter (S09's entry timing was found by a
parameter sweep after two hand-picked values missed). The collision margins are
consequently small — typically 3–5 m minimum separation — which is why the
per-seed parameter variation had to be kept to ±5% common speed scaling and
±0.12 s action jitter. A larger perturbation flips the outcome class, and
scenario validation correctly rejects it.

So the scenarios are reproducible but **not robust to large parameter change**,
and the reported robustness is over a correspondingly narrow band.

## 6. Limited vehicle count and no vulnerable road users

At most three vehicles, vehicle-to-vehicle only. No pedestrians, cyclists or
motorcycles. Multi-agent effects that only appear with denser traffic are out of
scope, and nothing here addresses the perception problems specific to vulnerable
road users.

## 7. No camera, no local semantic map

By design, local inference sees only telemetry, controls and radar. It therefore
cannot observe traffic-light state, lane markings, signage, road geometry or
right-of-way rules. Those privileged facts remain outside the local and fused
evidence boundary; the oracle and model-checking layers retain explicit support
for them.

That is an honest epistemic result, not a capability. A production forensic
system would fuse camera and map data and would not face this particular limit.

## 8. Causal assumptions

* **The event vocabulary bounds what can be found.** The causal graph is built by
  explicit rules over a fixed event taxonomy. A cause with no corresponding event
  type cannot be represented at all.
* **Local causal edges are hypotheses, not discoveries.** They come from an
  interpretable rule table with temporal constraints. This is not causal
  discovery from observational data, and no claim is made that the rules are
  complete or that the data alone identifies them.
* **Confidence values are not calibrated probabilities.** Rule priors, node
  confidences and the noisy-OR fusion rule are evidence-accumulation heuristics.
  They order claims sensibly; they do not carry frequentist or Bayesian meaning,
  and they have not been validated against observed frequencies.
* **The oracle graph is itself a model.** Ground truth here is the scenario's
  designed causal template instantiated with measured kinematics. It is a
  defensible reference because the scenarios were *constructed* to have that
  structure, but it is a designer's account of causation, not an independent one.

## 9. Counterfactual intervention semantics

A but-for claim here means exactly: *re-running the identical scenario — same
map, same spawn state, same seed, same everything — with one named scripted
action disabled, delayed or weakened changes the outcome.*

It does **not** mean:

* that the action was necessary in any broader sense;
* that a real driver could have taken the alternative;
* that the counterfactual world is the nearest possible world in any formal
  sense — it is the nearest world *reachable by editing one scripted action*;
* anything about other interventions that were not tried. Only the declared
  `intervention_candidates` are tested, and the number tested is capped.

Interventions are also tested one at a time, so joint effects and interaction
between two contributing actions are not measured.

## 10. Not legal liability

The system reports causal contribution, contributing actions, a causal initiator
where one exists, shared causal contribution, and insufficient evidence. It does
**not** determine fault, blame, negligence or legal liability, and the normalised
contribution score is **not** a fault percentage. The raw counterfactual outcomes
are always retained alongside it precisely so the score cannot be read as a
verdict.

## 11. Not formal verification

The checking layer is a finite-trace property monitor over recorded traces. It
evaluates a small set of parameterised properties on the traces that were
actually produced. It does not explore the state space, does not prove anything
about traces that were not recorded, and verifies nothing about CARLA.

`UNKNOWN` is returned whenever the evidence cannot decide a property, and it
should be read as "this run did not contain the situation the property is about,
or the evidence to judge it", never as a pass.

## 12. Statistical weight

Each scenario was run at a small number of seeds with narrow parameter variation.
That is enough to show the pipeline is deterministic and to detect gross
sensitivity; it is **not** enough for statistical claims about effect sizes.
Differences between conditions should be read as observations from a handful of
controlled runs, not as estimates with confidence intervals.

## 13. Single environment

Everything was run on one machine, one OS, one simulator build. Several
workarounds encoded in the code are specific to that build's behaviour (map
reload crashes, unreliable second map switch, Town03 unusable). Results on
another build may differ, and the map-handling code may be unnecessary there.

## 14. The counterfactual campaign runs behind a workaround

A counterfactual suite restarts the simulator before every replay, and on this
build the native CARLA client aborts the whole interpreter -- `Fatal Python
error: Aborted`, inside `world.apply_settings()` -- on the third simulator
process of a run. It is reproducible, it produces no Python traceback and no
Windows error report, and the cause is not established (finding 10 in
`docs/ENVIRONMENT.md` records what was tried and what it did not fix).

The campaign gets through it by structure rather than by repair:
`counterfactual.resume` reuses replays already on disk, and the driver retries
each suite, so successive attempts need fewer restarts until one completes. The
S01 suite needed four attempts for four replays.

Two consequences for reading §9 of the findings. The replays in one suite were
recorded across several processes and, for the retried ones, across several
attempts -- each still on its own freshly started engine, which is the property
the comparison actually depends on, but not in one uninterrupted session. And a
suite that exhausts its retries would leave a partial contribution report; the
driver reports such a run as `INCOMPLETE` rather than scoring it, and no
incomplete suite is quoted.

**A second, worse failure was found in this area and is now checked rather than
trusted.** A simulator engine left running by an interrupted run keeps RPC port
2000; every later "fresh" engine fails to bind it and the client silently
reconnects to the old one. The restart appears to succeed, the log says so, and
every replay of every later sweep shares one drifting session. It happened here
and produced a verdict that did not reproduce.

The restart is now verified against the connected world's clock, the result is
written into every attribution report, the sweep driver exits non-zero when any
run was degraded, and the viewer refuses to show such a verdict without a
banner. What this limits is older artifacts: any counterfactual report that
carries no `replay_protocol` block predates the check, and nothing in it
establishes which protocol it ran under.

## 15. Self-localisation is exact, so one reported error is not a measurement

This simulator models no localisation noise. Each recorder's exported position is
the true pose, byte for byte, which means the self-localisation RMSE reported by
the evaluation is exactly zero on every run.

That number verifies the recorder copies the pose faithfully. It says nothing
whatever about reconstruction quality, and quoting it as a trajectory accuracy
result would be badly misleading. It is labelled as such in every artifact and
kept out of the headline; the reported trajectory error is the **cross-view** one
instead, which does carry radar error, identity resolution and clock error.

The consequence for the collision *location* error is subtler and worth stating.
Because the positions are exact, the location error is the distance the vehicles
travelled during the reconstruction's time error — it measures the clock, not the
sensors. In scenarios where the impact happens at near-zero closing speed it is
sub-millimetre, which looks like an extraordinary result and is really a
statement about how slowly the vehicles were moving.

A real deployment would have GNSS and odometry error on every self-reported
position, and every figure that currently depends on exact self-localisation
would degrade. Nothing here establishes by how much.

## 16. The structural metrics are insensitive to the clock at these magnitudes

The clock ablation shows the estimated alignment cutting mean absolute offset
error roughly fourfold, and it shows node F1, edge F1 and edge recall completely
flat across all three protocols.

Both are true and they are not in tension: the event matcher's tolerance is
1.5 s, the uncorrected offset is an order of magnitude smaller, and a
misalignment that never moves an event across the matching threshold cannot
change the match. So this campaign does **not** demonstrate that clock alignment
improves graph reconstruction. It demonstrates that alignment is necessary for
the quantities measured in seconds and metres, and that at these offset
magnitudes the structural metrics cannot see it either way.

Showing a structural effect would need larger offsets, a tighter matching
tolerance, or both — and a tighter tolerance would change every other number in
the campaign, so it is not a change that can be made for one ablation alone.

## 17. Drift is declined rather than estimated

Over a ten-to-fifteen-second encounter a realistic crystal deviation of tens of
parts per million moves a timestamp by well under a millisecond, far below the
radar noise the alignment is fitted from. The solver therefore pins `scale` to
1.0 and fits the offset only, recording `OFFSET_ONLY_UNOBSERVABLE_DRIFT`.

This is the right refusal — fitting a two-parameter model to data that constrains
one parameter produces a number that looks like a measurement and is noise — but
it means the drift error the evaluation reports is the error of a parameter that
was never estimated. It should not be read as a drift-estimation result.

## 18. One variant is not reconstructed at all, and some clocks do not align

In `S02/avoided` the two recorders share too few observations for the alignment
to place one of them on the common timeline. The run reports
`UNRESOLVED_TIME_ALIGNMENT` and produces no reconstruction rather than a guessed
one, which is correct behaviour and also a gap in coverage: a variant that
cannot be reconstructed contributes nothing to any claim about reconstruction
quality, and the campaign is one variant smaller than it looks.

The same applies within a run to the cross-view figure, which is reported as
unscored with the unaligned recorders named, never as zero error.

## 19. Attribution is right on a minority of scenarios

The campaign names exactly the designed contributors on a small number of the
scenario variants designed to collide. On most it names a subset or a superset,
and on one it names the wrong vehicle entirely.

Restraint on the negative controls is complete — nobody is ever named where
nobody contributed — and ancestry recall is near-total, meaning the behaviours
the template blames are almost always somewhere in the reconstructed ancestry of
the impact. What the method is weaker at is selecting *which* of the behaviours
in that ancestry to name, which is the harder half of the problem and is not
solved here.

## 20. A cause that consists of *not acting* leaves no node to root a chain at

This is the sharpest limitation of the graph-only attribution, and S08 shows it
cleanly.

The scenario's designed cause is `B_fail_to_yield`: B enters the junction
without slowing. That is an **absence** — no braking command, no deceleration,
no manoeuvre — and the event taxonomy has nothing to represent it, because every
event type in it describes something that happened. A's reaction, by contrast,
is full of events: A moves laterally, A brakes, A's time-to-collision goes
critical.

So the reconstruction roots its causal chains at A, and the graph-derived
hypothesis names A — the vehicle that *responded* to the hazard rather than the
one that created it. It is exactly wrong, and it is wrong for a structural
reason rather than a tuning one: you cannot put a non-event at the root of a
chain of events.

The counterfactual replay gets it right, because removing `B_fail_to_yield` is
something the simulator can do even though the local recorders could not observe
it, and the collision then does not happen. This is the clearest case in the
campaign for why the replay-backed verdict and the graph-only hypothesis are
both reported: on S08 they disagree, and the replay is the one to believe.

Fixing this properly would need the taxonomy to carry *expected-but-absent*
behaviour — "approached a conflict at constant speed where a response was due" —
which is a normative judgement about what was due, and that is right of way
again (§7). `conflict_entry_without_deceleration` is the closest the current
vocabulary comes, and it describes the kinematics without asserting the duty.

## 21. Post-crash behaviour is not modelled, and the property monitor says so

The scenario scripts drive each vehicle through the encounter; they do not model
what a driver does after an impact. Vehicles therefore keep applying throttle
after a collision, which the `P3_post_collision_stop` property correctly reports
as a violation on many runs.

The monitor is right and the scenarios are unrealistic in this specific respect.
The failure counts in the results should be read as a statement about the
scripted behaviour, not as a finding about driver conduct.

## 22. Contact alone cannot place a vehicle that never collides

**Superseded as a limitation of the final method; retained because it is what the
radar fallback exists for, and because the contact-only ablation still shows it.**

V1 aligned the clocks by fitting radar tracks, so it could place a vehicle that
never touched anything. Contact-only V2 could not. In the partial-view scene A
strikes B and C only brakes, so C has no anchor: the alignment reports
`PARTIALLY_ALIGNED`, names C unaligned, and two things follow -- C appears nowhere
in the fused graph, and B's radar track of C is never resolved to C, because
association needs both ends on one clock.

The final method keeps an **offset-only radar fit behind contact** for exactly
this case, and on the recorded `S07/occluded` run it places C to 0.000101 s while
A and B keep their contact anchors. The loss above is now reproduced only by
disabling the fallback, which is how the ablation runs and how the tests assert
it (`tests/integration/test_fusion_improvement.py`).

What remains a limitation is the residue: the fallback needs a tracked target
whose geometry varies enough to separate an offset from a spatial bias. Where it
does not, the recorder stays `UNRESOLVED` rather than being placed on a guess,
and a whole account is still lost. The harness marker is **not** used to patch
one participant of an otherwise physically aligned run: mixing provenances on one
timeline and reporting them identically would be worse than an honest gap.

## 23. One all-way-stop variant does not produce its designed encounter

`S12/near_simultaneous` declares a collision and does not achieve one. Its
closest approach is 11.08 m against the 6 m the variant requires.

The cause is geometry, not timing luck. The junction is the only one in Town05
that renders stop signs on more than one approach, and it is a large T: the
vehicle turning in has a merge point about 8 m beyond its stop line while the
vehicle going straight has about 23 m. Six timing attempts on the development
seed did not bring the two together, and the ones that came closest did so by
making the two arrivals *not* near-simultaneous -- which is the one thing the
variant is for.

It is left as declared and recorded by the campaign as a scenario validation
failure. The priority-ambiguity question it was written to ask is therefore not
answered by this campaign. The other three S12 variants do run, and the
clear-priority cases are covered by them.

## 24. Town05 renders five stop signs, and none of them has a painted stop line

The map carries 33 `traffic.stop` trigger actors and renders **5** sign meshes;
a trigger volume is not something a camera can read. The packaged CARLA 0.9.15
build also ships no stop-sign prop at all, so a scenario cannot place one.

Both facts bound what the traffic-control scenarios can be. They must sit at one
of five junctions, only one of which renders signs on more than one approach.
And none of those junctions paints a stop bar, so `STOP_LINE_CROSSED` never fires
on a real run -- which is why the stop property also accepts the lane sensor's
record of crossing into the junction as its boundary (`docs/FORMAL_METHODS.md`).
The stop-line detector still runs and still reports honestly; it simply has
nothing to find at these junctions.

## 25. The pushed-vehicle case does not come out the way it was designed

`S14/c_pushes_b` puts C into B and B into A, and the question it exists to ask is
whether the middle vehicle is spared: B is in the second impact only because it
was struck, so it should not be named an initiating contributor. The campaign
records the collision order correctly — (B,C) at 6.50 s then (A,B) at 7.70 s —
and then names **B supported and C partial**, which is not the designed answer.

Neither finding is arbitrary, and both are worth stating precisely.

B is named because it has `CONTINUED_ACCELERATION_DURING_CONFLICT` at 5.76 s,
*before* the first impact, together with an independent physical path. That is
B's own behaviour and not a consequence of the push, so on the evidence recorded
the finding is defensible — it is simply not the thing the variant was written to
test, and a reader comparing it against the design would take it for the failure
the design was guarding against.

C is the striker and is reported with no physical path to the outcome. Its own
rule violation is stamped at 6.66 s, *after* the impact at 6.50 s that it caused,
so the physical requirement finds nothing of C's that independently reaches the
collision. A violation recorded after the event it should explain cannot support
a contribution, and the layer is right to refuse — but the result is that the
vehicle which initiated the chain is the one the account does not name.

What this bounds: the pushed-vehicle discrimination is not demonstrated by this
campaign. The mechanism it depends on — a physical path that traverses an impact
only where the vehicle's own behaviour independently reaches it — is implemented
and unit-tested, and the recorded run does not exercise it as intended because
the pre-impact evidence falls the wrong side of the two vehicles.
