# Limitations

Read this before the results. Everything below constrains what the numbers in
`docs/EXPERIMENTAL_FINDINGS.md` can support.

## 1. Simulation-to-reality gap

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
