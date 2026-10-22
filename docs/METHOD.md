# Reconstruction method

There is one reconstruction method.  Its parameters are in `configs/reconstruction.yaml`; no option selects another
algorithm.  Every parameter, its category and its evidence: [FINAL_PARAMETER_AUDIT.md](FINAL_PARAMETER_AUDIT.md).
Event definitions and thresholds: [event_definitions.md](event_definitions.md).

## Pipeline

| stage | module | output |
|---|---|---|
| Local reconstruction | `reconstruction/tracking.py`, `local.py` | radar tracks, ego motion and local semantic events of each recorder, on its own clock |
| Temporal alignment | `reconstruction/alignment.py`, `fusion.py` | one global clock, from the collisions the recorders share (else from what they observed of each other) |
| Identity association | `reconstruction/identity.py` | which local track is which recorder |
| Anonymous road users | `reconstruction/anonymous.py` | road users that recorded nothing, fused from the recorders' radar views (`U1`, `U2`, ...) |
| Global semantic graph | `reconstruction/pipeline.py`, `render.py` | one event trace on the global clock (`reconstruction/global/global_graph.json`, `.md`, `.dot`) |

Principles: ground truth is never read by the reconstruction (only by the evaluation); no scenario-specific rules;
ambiguity stays unresolved, because a false merge is worse than an unresolved identity.

## Radar tracking

- A return joins a track when its Mahalanobis distance is inside the 99 % gate of S = the track's predicted
  covariance + the spread of a vehicle body + the radar's polar noise at the return's range (lateral uncertainty
  grows with range).
- Doppler speed is tested along the return's own line of sight only; the tangential velocity, which Doppler does
  not measure, is never tested.
- A return that two tracks explain within a likelihood ratio of 20 is ambiguous and updates neither.
- A track survives while its prediction can still tell two bodies a car width apart (2 s cap), and is confirmed
  after 0.2 s of support and 3 updates.  A recorder's own impact widens the covariance of the tracks touching it.
- A part of a known body seen apart is never a second vehicle; a target that crashes ahead keeps its track through
  the abrupt slowdown or rebound.

## Alignment

Recorders are aligned on the collisions they report.  A pairing is refused when the pose streams put the bodies
apart, or when a recorder's own radar view of the contact contradicts the partner's speed in the observed direction.
Without a shared collision, observed trajectories can fix a clock offset; otherwise the recorder stays unaligned.
A contact of the same pair at most 2 s after the previous one, with the two bodies never more than 1 m apart in
between (their own pose streams, less 3 sigma of their declared accuracy), is a recontact of that collision, not a
new one: the global COLLISION node lists it under `recontacts` (S04 `a_front_pushed`: a rebound of 0.15 m, then A
pushes B again 0.65 s later).

## Identity and anonymous road users

- Recorder links use the relative pose uncertainty and the line-of-sight velocity and are conservative: one
  recorder per observer and instant, unless same-body evidence joins two fragments.
- Anonymous road users come from one-box evidence across observers, cannot-link constraints, one-to-one assignment
  and a stitch posterior against a new road user.
- Two observers seeing one body at the same instants are tested on every shared instant: a brief overlap must pass
  at every instant, a long one by majority.  After an observer's own collision its velocity estimates are not
  compared (geometry decides).
- A track that is the same body as another observer's track of recorder X inherits X, and no other recorder.
- A retrospective resolution may name an earlier observation from later evidence by several observers; no sample,
  event or timestamp moves.

## Semantics

- The recorder's path corridor follows the lane it drives in (OpenDRIVE map of the CARLA installation named by the
  supplied incident context, as an investigation knows where the incident happened; without one, the map the
  recorder's own poses fit); at a junction, the branch it takes later.  Cars following one bend are not in its path.
- CUT_IN needs a lateral manoeuvre of the target toward that path, leaving its own lane, confirmed by its
  EGO_PATH_ENTRY; none starts after the recorder's own collision.
- CRITICAL_TTC is PREDICTED_OVERLAP (a collision course braking cannot avoid: crossings, merges) or
  UNSAFE_FORWARD_GAP, which only a leader can cause (a target in the recorder's path or in a confirmed cut-in, never
  a car abreast).  A pair's episode ends at their collision and does not restart while they touch.
- Turn indicators come from the recorder's own light log only; they are never inferred from motion.
- In the global graph, a CRITICAL_TTC between a pair that has already touched is suppressed; the raw local evidence
  stays in the local graphs.
