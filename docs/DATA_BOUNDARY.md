# The data boundary

The central methodological claim of this project is that each reconstruction is
built from evidence a real vehicle could plausibly have retained. That claim is
worthless unless the boundary is enforced by construction rather than by
discipline. This document states the allowed and forbidden inputs per layer, how
the boundary is enforced structurally, and exactly what the anti-leakage test
suite must assert.

---

## 1. Allowed and forbidden inputs, per layer

### `cdf.local` -- per-participant inference

**Allowed** (all of it produced by, and about, one participant):

* its own `TelemetrySample` stream -- pose `(x, y, z, yaw, pitch, roll)`,
  velocity, acceleration, `speed`, `accel_long`, `accel_lat`, `yaw_rate`;
* its own `ControlSample` stream -- throttle, brake, steer, hand brake, reverse,
  gear;
* its own `RadarFrame` stream -- `(depth, azimuth, altitude, velocity)` returns
  plus that participant's own sensor extrinsics (`sensor_id`, `sensor_yaw`,
  `sensor_x/y/z`);
* its own `TrackSample` stream -- tracks produced by *its own* tracker, labelled
  with *its own* anonymous ids (`make_track_id("A", 3)` → `"A::T003"`);
* its own `LocalTriggerRecord`s -- that an impact occurred, when, and how hard;
* the resolved `Config` thresholds.

**Forbidden:**

* any other actor's true pose, velocity, controls or intent;
* any CARLA actor id, including the identity of a collision partner;
* map data of any kind -- lane id, road id, section id, junction id, waypoints,
  lane topology;
* traffic-light state, phase or id;
* scenario labels -- roles, expected outcomes, causal templates, fault
  assignments;
* anything under `oracle/`.

### `cdf.fusion` -- post-event merge

**Allowed:** every participant's *exported local logs and graphs*, i.e. exactly
what the participants could have handed over after an incident -- their own
telemetry (the trajectory each one self-reports), their own track streams, their
own events and their own graph documents, plus the `Config`.

**Forbidden:** everything forbidden to `cdf.local`. In particular, cross-vehicle
identity may **only** be established from observable trajectory evidence
(`cdf.fusion.track_association`), never from a simulator id. `cdf.fusion` may not
import `cdf.oracle`, `cdf.simulation` or `carla`.

### `cdf.graph`, `cdf.checking` -- inference support

**Allowed:** whatever their caller hands them from the two layers above.
`cdf.checking` additionally evaluates *privileged* properties, but does so over a
**plain dictionary trace** supplied by the caller (see §2.5), so it never imports
`cdf.oracle` either.

**Forbidden:** importing `cdf.oracle`, `cdf.simulation` or `carla`.

### `cdf.oracle`, `cdf.simulation` -- privileged

**Allowed:** everything. `cdf.simulation` is *test-generation* code: it
legitimately reads the map, places vehicles on lane waypoints, scripts their
behaviour and knows the intended outcome, because it creates all of it.
`cdf.oracle` reads exact global state.

**Obligation:** their output must never re-enter inference. Oracle artifacts live
under `oracle/`, carry `Provenance.ORACLE`, and are refused at every inference
boundary.

### `cdf.evaluation` -- the comparison layer

**Allowed:** both sides. It is the one layer permitted to read a reconstruction
and the ground truth in the same process, because comparing them is its purpose.

**Forbidden:** writing anything back into a local or fused artifact. Evaluation
output belongs under `evaluation/`. A pipeline in which an evaluation stage could
edit `vehicle_*/causal_graph.json` or `fusion/fused_causal_graph.json` would make
every published metric circular.

### `cdf.causal` -- the counterfactual layer (privileged)

**Allowed:** both sides, like `cdf.evaluation`, and additionally the simulator.
It imports `cdf.simulation.runner` because a counterfactual claim in this project
is not a graph operation: it is an actual re-run of the scenario with one
scripted action changed. It reads the oracle summary to decide whether a replay
collided, because "did this replay collide, and with whom" is ground truth.

It is therefore **not** an inference layer and is deliberately outside the set
the anti-leakage suite scans for privileged imports
(`INFERENCE_PACKAGES = ("local", "fusion", "graph", "checking")`).

**Forbidden:** writing into a local or fused artifact. Its output belongs under
`counterfactual/`, and each replay is written into its own subdirectory so the
factual run is never overwritten.

**Consequence for reading the results:** a counterfactual conclusion is
privileged-assisted. It says "re-running this scenario without action X produced
no collision", which is a statement about the simulator, not something the local
layers derived from onboard evidence. `docs/CAUSAL_MODEL.md` states the
interventional semantics; `docs/LIMITATIONS.md` §9 states what the claim does and
does not support.

---

## 2. How the boundary is enforced structurally

### Independent recorder clocks

CARLA physics and scripted controls use one hidden simulator clock. Every local
stream, trigger and derived local graph instead uses the participant's recorder
clock; exported frame numbers are unrelated local sequences. True offsets,
scales and drift exist only in `oracle/clock_ground_truth.json`, read exclusively
by evaluation. They must not be copied into local/fused evidence or diagnostics.

The inference-facing `load_run` manifest keeps only run identity and protocol,
not simulator timings, participant scripts, true collision pairs or the resolved
generation configuration. Inference may use configurable estimator bounds but
must not import the clock-profile generator or reconstruct profiles from seeds.
Anti-leakage tests enforce forbidden imports, field names and direct clock-truth
access. An independent-clock synthetic recording exercises the complete pipeline.

Synchronization uses local own poses and anonymous radar trajectory/range/rate
evidence, not frame equality or sampling cadence. Final cross-vehicle APIs reject
unconverted independent clocks. Evaluation's clock-truth inverse transform is a
detached scoring copy and never an input to normal inference.

### 2.1 Record schemas with no field for privileged data

`src/cdf/common/schemas.py` is the single definition of the on-disk evidence
format, and the local record types simply **have no field** in which a privileged
quantity could be stored:

* `TelemetrySample` -- only the participant's own kinematics. No neighbour block.
* `ControlSample` -- only its own actuator channels.
* `RadarDetection` -- `depth`, `azimuth`, `altitude`, `velocity`. Nothing
  identifies the reflecting object.
* `RadarFrame` -- `sensor_id` is a *logical* name (`"front"`), documented as "not
  a CARLA actor id".
* `TrackSample` -- `track_id` is locally generated and documented as having "no
  relation to any CARLA actor id". Its global-frame fields are *estimates*
  obtained by composing the observer's own pose with its own measurement.
* `LocalTriggerRecord` -- for a collision it holds `collision_detected` and
  `impulse`. "The identity of the other party is deliberately absent."
* `ParticipantEvidence` -- "deliberately has no field capable of holding another
  actor's ground truth".

The privileged counterpart is a *different* dataclass in a *different* package:
`cdf.oracle.logger.OracleActorState` carries `actor_id`, `lane_id`, `road_id`,
`section_id`, `junction_id`, `traffic_light_state`, `traffic_light_id`. A local
record cannot be silently upgraded into one.

### 2.2 `Provenance` scope on every graph, checked on load

`GraphDocument.scope` is a `Provenance` (`LOCAL` / `FUSED` / `ORACLE`), and every
`Event` and `GraphEdge` carries its own `provenance`. Two guards use it:

```python
# cdf.graph.export
load_graph(path, expect_scope=Provenance.LOCAL)   # raises on a scope mismatch

# cdf.common.schemas
assert_non_oracle(doc, context)                   # raises on an ORACLE document
```

`cdf.fusion.pipeline.fuse_run` loads **every** local graph with
`expect_scope=Provenance.LOCAL`, and `cdf.fusion.graph_fusion.fuse_graphs` calls
`assert_non_oracle()` on each input and additionally refuses a document whose
scope is not `LOCAL` or whose `graph_kind` is not the one requested. A mis-wired
path therefore fails loudly instead of leaking ground truth.

### 2.3 Node-level validation inside the local builders

`cdf.local.event_graph.validated_local_nodes(events, participant_id)` -- shared by
the event graph and the causal DAG so both refuse the same inputs -- raises when:

* an event's type is in `ORACLE_ONLY_EVENT_TYPES`
  (`ORACLE_SIGNAL_VIOLATION`, `ORACLE_RIGHT_OF_WAY_CONFLICT`,
  `ORACLE_SCRIPTED_INTERVENTION`);
* an event carries `Provenance.ORACLE`;
* an event's `participant_id` differs from the graph owner's -- "every vehicle
  builds its graph from its own evidence only".

`cdf.fusion.event_alignment.align_event_records` performs the same oracle-type
check at the fusion boundary.

Single-owner enforcement runs one level lower, too:
`RollingRecorder._check_owner`, `RadarFrontEnd.process`, `RadarTracker.update` and
`score_candidate` all raise on a record belonging to another participant (the last
refuses the degenerate "a participant observes itself" hypothesis).

### 2.4 `CollisionSensor`: two drains, two audiences

`cdf.simulation.sensors.CollisionSensor` holds each raw CARLA event as a private
`_RawCollision` carrying `other_actor_id` and `other_type_id`, and exposes it
through exactly two methods with **independent cursors**:

| Method | Returns | Caller |
|---|---|---|
| `drain_local(min_impulse)` | `LocalTriggerRecord(t, frame, participant_id, kind=COLLISION, collision_detected=True, impulse, detail={"source": "onboard_collision_sensor"})` -- **`other_actor` stripped** | `ParticipantAgent._handle_triggers` |
| `drain_privileged()` | a dict **including** `other_actor_id` and `other_type_id` | `OracleLogger._drain_collisions` only |

This is the single point at which the identity of a collision partner could enter
the local layer, and it is where the identity is deleted. The consequence is
visible in the committed example run: A's local `COLLISION` event names no
partner, and fusion has to *infer* the counterpart from A's own resolved radar
tracks -- `"counterpart B inferred from own track at 3.64m at t=6.550s"` -- while
B's own `COLLISION` event stays unmerged with `counterpart_unknown`, because B (the
lead vehicle) held no tracks at all.

### 2.5 Privileged properties without a privileged import

`cdf.checking.properties` defines `ORACLE_PROPERTIES` (`O1_signal_compliance`,
`O2_right_of_way`), which need facts no onboard sensor produces. To keep the layer
boundary structural rather than conventional, they operate on a **plain mapping**
with a documented shape, so `cdf.checking` never imports `cdf.oracle`.
`TraceChecker` keeps the two families in separate methods
(`check_participant` / `check_oracle`) producing separate reports, and
`check_run()` "contains **no** oracle verdicts".

### 2.6 Privileged accessors are labelled and quarantined

`ScenarioWorld.all_vehicles()` and `ScenarioWorld.traffic_lights()` carry explicit
`PRIVILEGED -- oracle use only` docstrings; `spawn_points()` and `waypoint()` are
labelled scenario-construction only. `OracleLogger.participant_of_actor()` is the
only actor-id → participant resolution in the codebase.

### 2.7 The artifact tree mirrors the boundary

`RunLayout` puts per-participant evidence under `vehicle_<id>/`, fused output
under `fusion/`, and quarantines ground truth under `oracle/`. The local stage
`analyse_run` reads "only `vehicle_*/` artifacts. The `oracle/` subtree is never
opened", and `fuse_run` likewise.

---

## 3. The anti-leakage registries

`src/cdf/common/schemas.py` names what must never appear in a `local` or `fused`
artifact.

`FORBIDDEN_LOCAL_FIELD_NAMES` (exact field names, 40 entries):

```
other_actor_id, carla_actor_id_other, other_actor, actor_id, carla_id,
true_other_x, true_other_y, true_other_z, true_other_yaw, true_other_velocity,
true_other_speed, lane_id, road_id, junction_id, section_id, waypoint,
map_waypoint, traffic_light_state, traffic_light_id, signal_state,
ground_truth_role, gt_role, role, oracle_label, oracle_id, expected_cause,
expected_culprit, culprit, causes, scenario_role, is_at_fault,
true_sim_time, sim_time, simulation_timestamp, carla_timestamp,
true_offset_s, true_scale, true_drift_ppm, true_clock_offset, true_clock_drift
```

`FORBIDDEN_LOCAL_FIELD_SUBSTRINGS` (flag a leak regardless of the exact name, 18
entries):

```
ground_truth, groundtruth, privileged, oracle, true_other, gt_other,
actor_id, traffic_light, waypoint, lane_id, road_id, junction,
true_clock, true_offset, true_drift, true_scale, sim_time, carla_timestamp
```

`ORACLE_ONLY_EVENT_TYPES` names the three event types the oracle alone may emit;
`LOCAL_EVENT_TYPES` is its complement over `EventType`.

---

## 4. What `tests/test_no_privileged_leakage.py` must check

The implemented suite checks static/runtime imports, privileged API calls,
schemas, graph scopes and serialized artifacts. It additionally forbids direct
clock-truth access and importing the clock-profile generator in inference,
and exercises an independently clocked synthetic three-vehicle pipeline.

**A. Import-graph checks.** No module under `cdf.local`, `cdf.fusion`, `cdf.graph`
or `cdf.checking` may import `cdf.oracle`, `cdf.simulation` or `carla`, directly
or transitively. Asserted by static inspection of the module sources (an
`import`/`from` scan over `src/cdf/{local,fusion,graph,checking}/**/*.py`) rather
than by importing them, so a conditional or lazily-guarded import is caught too.

**B. Field-name checks over serialised artifacts.** Recursively walk every JSON
object under `vehicle_*/`, `fusion/` and `checking/` of a run directory and fail
if any key equals an entry of `FORBIDDEN_LOCAL_FIELD_NAMES` or contains an entry
of `FORBIDDEN_LOCAL_FIELD_SUBSTRINGS`. The same walk applies to the decompressed
`*.jsonl.gz` streams.

`checking/` is on this side of the line because finite-trace monitoring consumes
local evidence only; the privileged properties go through
`TraceChecker.check_oracle` and are persisted under `oracle/`. Three subtrees are
deliberately *not* scanned and their exclusion is not an oversight: `oracle/` is
the privileged layer itself, `evaluation/` is the scoring layer and is allowed to
consult the oracle, and `viewer/` carries the badged oracle view for human
inspection.

The walk runs over a synthetic run built in-process **and** over every recorded
run under `artifacts/` -- all 39 of the campaign plus their counterfactual
replays and the separate independent-clock smoke recordings are included --
marked `slow` because the recursive scan takes substantial time. Scanning one run proves the
pipeline *can* produce clean artifacts; scanning the campaign proves it *did*.

**C. Event-type checks.** No event in a `local` or `fused` artifact may have a
type in `ORACLE_ONLY_EVENT_TYPES`; every event in `vehicle_<pid>/events.json`
must have `provenance == "local"` and `participant_id == pid`; every node of a
fused graph must have `provenance == "fused"`.

**D. Scope checks.** `vehicle_*/event_graph.json` and `vehicle_*/causal_graph.json`
must load under `expect_scope=Provenance.LOCAL`; `fusion/fused_*_graph.json` under
`Provenance.FUSED`; any `oracle/*_graph.json` under `Provenance.ORACLE`, and must
be *rejected* when loaded with either other scope.

**E. Schema checks.** The dataclass field sets of `TelemetrySample`,
`ControlSample`, `RadarDetection`, `RadarFrame`, `TrackSample`,
`LocalTriggerRecord`, `Evidence`, `Event`, `GraphEdge` and `GraphDocument` (via
`schemas.field_names`) must contain no forbidden name or substring -- the
structural guarantee of §2.1, asserted rather than assumed.

**F. Collision-sensor split.** A `CollisionSensor` fed a synthetic event must
yield a `drain_local()` record whose serialised form contains neither the actor
id nor any forbidden key, while `drain_privileged()` on the same event yields
`other_actor_id`. The two cursors must be independent: draining one must not
consume the other's events.

**G. Track-id opacity.** Every `track_id` in a local or fused artifact must match
the `"<participant>::T<nnn>"` shape produced by `make_track_id`, and must never
equal a CARLA actor id recorded in the oracle trace for that run.

---

## 5. What the boundary costs, and why that is the point

The boundary is not free, and the committed S01 run shows the bill:

* B, the lead vehicle, holds **zero** radar tracks -- its forward radar sees empty
  road. Its local causal DAG has 10 nodes and 6 edges against A's 20 and 22.
* B's own `COLLISION` event cannot name A. Fusion records
  `counterpart_unknown` for it rather than guessing.
* `P1_brake_response` and `P2_no_throttle_while_closing` are **`UNKNOWN`** for B:
  "no radar track and no CRITICAL_TTC event evidence", "no range-rate evidence".

An omniscient recorder would have answered all three. Reporting *insufficient
evidence* instead is the behaviour under test, not a defect -- and it is what
makes the fusion benefit measured in S07 and the remaining epistemic limits
meaningful rather than circular.
