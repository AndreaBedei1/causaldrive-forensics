> **Superseded by [EVENTS.md](../docs/EVENTS.md).**
>
> This describes the V1 event vocabulary: own-behaviour, radar and outcome
> events, before the road, traffic-control and non-action families were
> added and before the comparable/sensor-relative/design-reference split
> that makes the graph comparison fair in both directions.
> 
> It is kept because many code docstrings still point here. For what the
> vocabulary is now, and why it is divided the way it is, read
> [EVENTS.md](../docs/EVENTS.md).

---

# Event taxonomy

`EventType` (`src/cdf/common/schemas.py`) is the complete, versioned vocabulary in
which a reconstruction may speak. It has **27 members**: 24 producible by the
local participant pipeline (`LOCAL_EVENT_TYPES`) and 3 reserved for the
privileged layer (`ORACLE_ONLY_EVENT_TYPES`).

## The naming rule

**No event name may imply an unobservable fact.** Nothing in the local vocabulary
names a traffic light, a lane, a road, a junction, a right of way, a map feature,
another actor's identity or a fault. The types are deliberately phrased as what a
vehicle's own sensors can witness -- a brake *command*, a *closing* range, a
*lateral* drift, an *inferred* path conflict -- and the "-`LIKE`" suffixes
(`CUT_IN_LIKE_MOTION`, `LANE_CHANGE_LIKE_MANEUVER`) exist precisely because the
underlying manoeuvre cannot be confirmed without a map. A lane change is inferred
from the vehicle's own pose history alone: a *lateral displacement relative to its
own earlier heading*, not a change of `lane_id`.

Where a genuinely unobservable fact must be stated, the taxonomy makes it
unmistakable by prefixing it `ORACLE_`, and `validated_local_nodes()` raises if
such a type ever reaches a local graph.

---

## The three global rules

Every threshold in the local extractor is an *episode*, not an instant.

| Rule | Key | Value | Effect |
|---|---|---|---|
| Hysteresis (Schmitt trigger) | `events.hysteresis_ratio` | `0.75` | an episode opens at the enter threshold and closes only once the signal has retreated past the release threshold |
| Minimum duration | `events.min_duration_s` | `0.10` s | shorter episodes are chatter and are dropped |
| Debounce / merge | `events.min_separation_s` | `0.75` s | two episodes of the same `(type, subject)` whose peaks are closer than this -- or whose end-to-start gap is -- merge into one wider event |

**Hysteresis direction.** `events.hysteresis_ratio` scales the enter threshold
*towards the non-event region*, which is asymmetric by necessity
(`_release_threshold`):

* threshold crossed from below, positive (`accel_long >= 1.5`): release at
  `enter * ratio` = 1.125;
* threshold crossed from above, negative (`accel_long <= -1.8`): release at
  `enter * ratio` = -1.35;
* threshold crossed from above, positive (`ttc <= 3.0`): the non-event region
  lies at *larger* values, so release at `enter / ratio` = 4.0.

An `enter` of exactly 0.0 releases at 0.0.

**Undefined samples.** A `None` in a signal (an undefined TTC, a conflict point
that could not be computed) is treated as "condition not met" and **closes** an
open episode rather than silently bridging it.

**Episode geometry.** `t_start` and `t_end` are the first and last in-episode
sample; `t_peak` is the *extreme* sample (maximum for an `"above"` test, minimum
for a `"below"` one), and its value is recorded in `values`. A merge keeps the
more extreme peak and the wider `[t_start, t_end]` span, the union of the
evidence pointers and sensors, and the higher confidence.

**Confidence.** Events derived from own telemetry or own controls carry
confidence 1.0 -- a recorded brake command is not an estimate. Radar-derived
events inherit the **mean tracker confidence over the episode**, so a claim resting
on a weak track cannot look as solid as a recorded command. `PREDICTED_PATH_CONFLICT`
is the exception: its conflict score *is* its confidence.

---

## Own-behaviour events

Derived from one participant's own telemetry and own actuator commands. These
never carry a radar-track subject.

| Type | Semantics | Signal | Enter threshold (config key) |
|---|---|---|---|
| `VEHICLE_STARTED` | the vehicle was **witnessed** pulling away from standstill | own `speed` | `events.vehicle_started.speed_mps` = `0.8` m/s, above |
| `ACCELERATION` | sustained speeding up | own `accel_long` | `events.acceleration.enter_mps2` = `1.5` m/s², above |
| `DECELERATION` | sustained slowing | own `accel_long` | `events.deceleration.enter_mps2` = `-1.8` m/s², below |
| `HARD_DECELERATION` | emergency-level slowing | own `accel_long` | `events.hard_deceleration.enter_mps2` = `-4.5` m/s², below |
| `BRAKE_ONSET` | the brake was applied | own `brake` command | `events.brake_onset.brake_cmd` = `0.12`, above |
| `HARD_BRAKE` | the brake was applied hard | own `brake` command | `events.hard_brake.brake_cmd` = `0.65`, above |
| `THROTTLE_ONSET` | the throttle was applied | own `throttle` command | `events.throttle_onset.throttle_cmd` = `0.25`, above |
| `STEER_ONSET` | a steering input was made | `abs(steer)` command | `events.steer_onset.steer_cmd` = `0.14`, above |
| `SIGNIFICANT_HEADING_CHANGE` | the vehicle turned appreciably | cumulative \|heading change\| over a trailing window | `events.heading_change.total_deg` = `12.0`°, above, window `events.heading_change.window_s` = `1.5` s |
| `LANE_CHANGE_LIKE_MANEUVER` | an out-and-back lateral displacement consistent with changing lane -- **inferred, never a map lane** | gated \|lateral path offset\| | `events.lane_change_like.lateral_offset_m` = `1.8` m, above |

Two entries need their extra machinery spelled out.

**`VEHICLE_STARTED` may only be asserted when the standstill was recorded.** The
recorder is a rolling buffer, so a trace routinely opens with the vehicle already
in motion. An episode that is already open on the very first sample is evidence
that *the recording* started, not that the vehicle did, so only episodes with
`i_start > 0` count and only the first such departure is reported. Without this,
a manufactured departure would be handed to the causal rules, which would then
blame it for the closing range.

**`LANE_CHANGE_LIKE_MANEUVER` needs three further gates**, all from own pose and
own controls, evaluated over `events.lane_change_like.window_s` = `3.0` s. The
lateral signal is zeroed wherever any of them fails:

1. *not a turn*: cumulative heading change over the window
   `<= events.lane_change_like.max_heading_change_deg` = `45.0`°;
2. *out-and-back*: `net_heading_change <= max_net_heading_ratio *
   cumulative_heading_change`, with
   `events.lane_change_like.max_net_heading_ratio` defaulting to `0.5`. A turn
   spends all of its cumulative heading change on a *net* change; a lane change
   spends it on an excursion that nets out. Without this gate, a window catching
   the tail of a turn plus the straight run after it looks exactly like a lane
   change;
3. *the driver actually steered*: the rolling maximum of `abs(steer)` over the
   window `>= events.steer_onset.steer_cmd`, which rules out sideways displacement
   caused by road curvature alone.

> `events.lane_change_like.max_net_heading_ratio` is **not** present in
> `configs/default.yaml`; the code default `0.5` is in force. See
> `legacy/IMPLEMENTATION_CHECKLIST.md`.

---

## Radar / interaction events

Derived from one participant's own radar tracks. Each carries a `subject` -- the
observer's **own anonymous track id** (`"A::T001"`), never an actor id.

| Type | Semantics | Signal | Threshold (config key) |
|---|---|---|---|
| `RADAR_TRACK_APPEARED` | our radar acquired a track | first sample of the track | instantaneous; no threshold |
| `RADAR_TRACK_LOST` | our radar stopped holding a track **before the recording ended** | last sample of the track | emitted only when `run_end - t_last >= gap` |
| `RANGE_DECREASING` | the gap to a tracked object is shrinking steadily | closing rate `= -range_rate` | `events.radar.range_decreasing.min_rate_mps` = `1.0` m/s, above, for at least `events.radar.range_decreasing.min_duration_s` = `0.6` s |
| `RAPID_CLOSING` | the gap is shrinking fast (looming) | closing rate | `events.radar.rapid_closing.min_rate_mps` = `6.0` m/s, above |
| `LOW_TTC` | time-to-collision below the comfort threshold | range-rate TTC | `events.radar.low_ttc.ttc_s` = `3.0` s, below |
| `CRITICAL_TTC` | time-to-collision in the critical band | range-rate TTC | `events.radar.critical_ttc.ttc_s` = `1.6` s, below |
| `LATERAL_CROSSING` | a tracked object is moving across our heading | \|lateral rate\| = \|d(rel_y)/dt\| | `events.radar.lateral_crossing.min_lateral_rate_mps` = `1.8` m/s, above, gated on `range_m <= events.radar.lateral_crossing.max_range_m` = `45.0` m |
| `CUT_IN_LIKE_MOTION` | a tracked object ahead is moving *towards our own path centre-line* | mean reduction of \|rel_y\| over the window | `events.radar.cut_in_like.lateral_closing_mps` = `1.2` m/s, above |
| `PREDICTED_PATH_CONFLICT` | our extrapolated path and the target's cross, and both would arrive together | conflict score in `[0, 1]` | `events.radar.path_conflict.min_confidence` = `0.35`, above |
| `CONFLICT_REGION_ENTRY` | we drove into the region we had ourselves predicted we would contest | distance from own position to the inferred conflict point | `indicators.conflict.region_radius_m` = `6.0` m, below |
| `TARGET_DECELERATION` | a tracked object is slowing down | target acceleration inferred along the line of sight | `-events.radar.target_deceleration.min_decel_mps2` = `-2.5` m/s², below |

**`RADAR_TRACK_LOST` -- the "lost" gate.** A track whose last sample sits at the
end of the recording was not lost; the recording stopped. The required gap is
`events.radar.track_lost.min_gap_to_end_s` when configured, otherwise
`radar_processing.tracking.max_misses` (`6`) x the participant's median sample
period -- exactly how long the tracker itself waits before deciding a track is
gone.

**`CUT_IN_LIKE_MOTION` -- the signal.** A cut-in is not merely lateral motion; it
is lateral motion *towards* the observer's longitudinal axis by a target that is
ahead and already near it. The signal at sample `i` is
`(|rel_y[j]| - |rel_y[i]|) / (t_i - t_j)` over
`events.radar.cut_in_like.window_s` = `2.5` s, and is zeroed unless
`|rel_y| <= events.radar.cut_in_like.max_lateral_offset_m` = `4.5` m and
`rel_x >= events.radar.cut_in_like.min_longitudinal_m` = `4.0` m. A sample whose
window is less than half covered reports `0.0`, because its denominator would be
dominated by noise.

**`PREDICTED_PATH_CONFLICT` -- map-free by construction.** `infer_conflict()`
(`cdf.local.indicators`) extrapolates both parties' currently observed constant
velocity over `indicators.conflict.prediction_horizon_s` = `4.0` s in steps of
`indicators.conflict.prediction_step_s` = `0.2` s and intersects the two predicted
polylines. A crossing alone is not a conflict, so the score is driven by the
**arrival-time gap**: `1.0` for simultaneous arrival, decaying linearly to `0` at
`indicators.conflict.max_arrival_gap_s` = `2.5` s. A party slower than
`indicators.conflict.min_own_speed_mps` / `min_target_speed_mps` = `1.5` m/s has no
meaningful predicted path and yields a zero score.

**`CONFLICT_REGION_ENTRY` -- self-checkable.** The distance signal is defined only
while the conflict hypothesis is itself credible (`conflict_score >=
events.radar.path_conflict.min_confidence`) and own telemetry exists within
`indicators.max_sync_gap_s` (code default `0.15` s). The event therefore states
"I drove into the area I had predicted we would contest" -- checkable against the
same recorded evidence.

**`TARGET_DECELERATION` -- inferred, not measured.** Differentiating the range
rate yields `(a_target - a_own) · los`; adding the observer's own acceleration
projected on the line of sight recovers the target's own longitudinal
acceleration. The approximation neglects rotation of the line of sight (second
order over the short episodes concerned) and uses only quantities the observer
measured itself.

**TTC is undefined, not safe.** `time_to_collision_1d` returns `None` when
`range_rate >= -1e-3` (not closing), and `compute_track_indicators` discards a TTC
above `indicators.ttc.max_reportable_s` = `12.0` s. Both mean *no evidence*, and
the extractor treats them as such.

---

## Outcome events

| Type | Semantics | Source | Threshold |
|---|---|---|---|
| `COLLISION` | this vehicle was involved in an impact | its **own** recorder trigger (`TriggerKind.COLLISION` or `collision_detected`); `values = {"impulse": …}` | `recorder.triggers.collision.min_impulse` = `1.0` N·s |
| `NEAR_MISS` | a conflict that materialised without contact | (a) the recorder's own near-miss trigger, or (b) derived from a `CRITICAL_TTC` episode that no collision resolved | (a) `recorder.triggers.near_miss.ttc_s` = `0.9` s and `min_range_m` = `12.0` m; (b) resolve window `events.outcome.near_miss.resolve_window_s`, code default `3.0` s |
| `POST_IMPACT_STOP` | the vehicle came to rest after its own impact | own `speed` after a `COLLISION` candidate | `events.outcome.post_impact_stop.speed_mps` = `0.6` m/s within `events.outcome.post_impact_stop.within_s` = `4.0` s |

A local `COLLISION` event **cannot name the other party**: the onboard collision
sensor's `drain_local()` strips it (see `../docs/DATA_BOUNDARY.md` §2.4). Its
`subject` is set only when the originating trigger carried a `track_id` -- which
near-miss triggers do and collision triggers do not.

The derived `NEAR_MISS` (case b) is built in a **second pass over already
debounced events**, so it can cite a stable event id for the `CRITICAL_TTC` it was
inferred from. The absence of a collision is itself the evidence.

---

## Oracle-only events

Producible only by `cdf.oracle`; their presence in a `local` or `fused` artifact
is a leakage bug.

| Type | Semantics | Why it is unobservable onboard |
|---|---|---|
| `ORACLE_SIGNAL_VIOLATION` | an actor was inside a junction while the signal facing it was red | needs ground-truth junction geometry *and* signal phase; neither appears anywhere in a participant's own recording. This remains an oracle-only reference event |
| `ORACLE_RIGHT_OF_WAY_CONFLICT` | two actors occupied the same junction simultaneously | needs the map's junction identity for both actors |
| `ORACLE_SCRIPTED_INTERVENTION` | a scripted action fired: "this was a commanded 8 s emergency brake" | declared intent; no amount of onboard evidence recovers a *command* as opposed to its effect |

`cdf.oracle.events.build_oracle_events()` measures these from the privileged
trace. It deliberately shares **no code** with the local extractor -- scoring a
reconstruction against a reference produced by the same code would measure
nothing but numerical noise -- and in particular it uses **no hysteresis**,
because its signals are exact and a plain minimum-duration gate reports the
interval during which the condition genuinely held.

---

## Event-graph and causal-DAG relation types

These are relations over events, not events. They are listed here because they
share the taxonomy's discipline.

`EventEdgeType` -- explicitly **not** causal claims:
`PRECEDES`, `OBSERVED_FROM`, `SAME_TRACK`, `INTERACTS_WITH`, `ALIGNS_WITH`,
`ASSOCIATED_WITH`. The last two express agreement *between* participants and are
emitted only by the fusion layer.

`CausalEdgeType` -- every instance is a hypothesis with evidence attached:
`CONTRIBUTES_TO`, `TRIGGERS`, `INCREASES_RISK_OF`, `PREVENTS`, `CAUSES_OUTCOME`.

`RADAR_TRACK_APPEARED` and `RADAR_TRACK_LOST` are banned from *both* sides of
every causal edge (enforced by `validate_rules()`): they are facts about the
observer's sensing process, not about the world. Their place is the
`OBSERVED_FROM` relation in the event graph. See `../docs/CAUSAL_MODEL.md`.
