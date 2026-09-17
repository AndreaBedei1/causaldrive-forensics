"""Multi-frame radar tracking: per-frame clusters -> persistent anonymous tracks.

A cluster (:class:`cdf.local.radar.RadarCluster`) is a measurement with no
identity. This module is the one place that *invents* identity, and it does so
from observable motion alone: a track id such as ``"A::T003"`` records only that
participant ``A``'s own tracker opened its third hypothesis. It is deliberately
not a CARLA actor id, and the same physical vehicle re-acquired after a long
occlusion gets a *new* id -- because that is genuinely all an onboard unit knows.
Re-establishing cross-vehicle identity is the fusion layer's job, from evidence.

Design rationale
----------------
* **Global-frame association.** Gating happens on the global-frame position
  estimate rather than in the body frame, because the observer's own motion
  (especially yaw rate during a turn) otherwise dominates the frame-to-frame
  displacement of a stationary object and blows the gate.
* **One-to-one assignment.** Nearest-neighbour-per-track can assign two tracks to
  the same cluster and swap identities whenever two objects pass close to each
  other. Solving the gated assignment problem optimally
  (:func:`scipy.optimize.linear_sum_assignment`) removes that failure mode, which
  matters here: a swapped identity silently corrupts every causal claim built on
  the track.
* **Alpha-beta smoothing.** A constant-velocity alpha-beta filter is the right
  complexity level for radar clusters at 20 Hz: it is stateless in its tuning,
  has no covariance to mis-initialise and degrades gracefully under the
  intermittent dropouts the degraded sensor profiles inject.
* **Coasting.** On a miss the track is propagated with its estimated velocity and
  its confidence decays. It is dropped after ``max_misses`` consecutive misses
  rather than at the first one, so a single dropped frame does not shred a track.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Set, Tuple

import numpy as np
from scipy.optimize import linear_sum_assignment

from ..common.config import Config
from ..common.geometry import global_to_body, rotate2d, time_to_collision_1d
from ..common.schemas import TelemetrySample, TrackSample, make_track_id
from .radar import RadarCluster

__all__ = ["TrackState", "RadarTracker"]


#: Cost used for a track/cluster pair that is outside the association gate. It is
#: a numerical sentinel, not a tunable threshold: it only has to dominate every
#: admissible pairing so that the optimal assignment never prefers a gated pair.
#: Rejected pairs are discarded again after the solve.
_GATE_REJECT_COST = 1.0e9


@dataclass
class TrackState:
    """Live estimate of one tracked object, in the observer's own reference.

    The global-frame fields are the filter state; the body-frame and polar fields
    are re-derived from it against the observer's current pose on every update,
    so a consumer can never observe a body/global pair that disagree.
    """

    track_id: str

    # Body frame of the observer (x forward, y right), metres.
    rel_x: float = 0.0
    rel_y: float = 0.0
    # Global (map) frame filter state, metres and m/s.
    gx: float = 0.0
    gy: float = 0.0
    gvx: float = 0.0
    gvy: float = 0.0

    range_m: float = 0.0
    azimuth_rad: float = 0.0
    range_rate: float = 0.0
    """Radial rate, m/s, negative means closing (radar convention)."""

    rel_vx: float = 0.0
    """Target velocity relative to the observer, observer body frame, m/s."""
    rel_vy: float = 0.0

    stationary_streak: int = 0
    """Consecutive frames whose associated cluster read as world-fixed."""
    hits: int = 0
    misses: int = 0
    """Consecutive updates without an associated cluster."""
    age: int = 0
    """Number of updates (hit or miss) the track has survived."""
    confidence: float = 0.0
    confirmed: bool = False

    first_t: float = 0.0
    last_t: float = 0.0
    """Time of the most recent update, whether it was a hit or a coast."""

    n_points: int = 0
    extent_x: float = 0.0
    extent_y: float = 0.0


class RadarTracker:
    """Alpha-beta multi-target tracker over one participant's radar clusters.

    One instance belongs to one participant and owns that participant's track-id
    counter. The counter is monotone and ids are never reused, so a track id is a
    stable key for evidence pointers for the whole run.
    """

    def __init__(self, cfg: Config, participant_id: str) -> None:
        self._cfg = cfg
        self._participant_id = str(participant_id)

        self._gate_m = float(cfg.get("radar_processing.tracking.gate_m", 4.5))
        self._max_misses = int(cfg.get("radar_processing.tracking.max_misses", 6))
        self._min_hits = int(
            cfg.get("radar_processing.tracking.min_hits_to_confirm", 3)
        )
        self._pos_alpha = float(
            cfg.get("radar_processing.tracking.position_alpha", 0.55)
        )
        self._vel_alpha = float(
            cfg.get("radar_processing.tracking.velocity_alpha", 0.35)
        )
        self._max_tracks = int(cfg.get("radar_processing.tracking.max_tracks", 16))
        self._hit_gain = float(
            cfg.get("radar_processing.tracking.confidence.hit_gain", 0.16)
        )
        self._miss_decay = float(
            cfg.get("radar_processing.tracking.confidence.miss_decay", 0.22)
        )
        self._min_confirm = float(
            cfg.get("radar_processing.tracking.confidence.min_confirm", 0.35)
        )

        if self._gate_m <= 0.0:
            raise ValueError("radar_processing.tracking.gate_m must be positive")
        if self._max_tracks < 1:
            raise ValueError("radar_processing.tracking.max_tracks must be >= 1")

        self._reject_stationary = bool(
            cfg.get("radar_processing.stationary.reject_new_tracks", True)
        )
        self._max_stationary_frames = int(
            cfg.get("radar_processing.stationary.max_stationary_frames", 40)
        )
        self._stationary_rejected = 0

        self._tracks: List[TrackState] = []
        self._next_index = 1
        # Monotonicity is an invariant of the *tracker*, not of any individual
        # track: it must keep holding across an interval in which every
        # hypothesis has been dropped, otherwise an out-of-order frame would be
        # silently accepted whenever the track list happened to be empty and
        # would stamp fabricated evidence with an earlier time.
        self._last_t: Optional[float] = None

    # -- accessors --------------------------------------------------------

    @property
    def participant_id(self) -> str:
        """The participant this tracker belongs to."""
        return self._participant_id

    @property
    def active_tracks(self) -> List[TrackState]:
        """The live track states, in creation order (oldest first)."""
        return list(self._tracks)

    # -- main entry point -------------------------------------------------

    def update(
        self,
        t: float,
        frame: int,
        clusters: Sequence[RadarCluster],
        telemetry: TelemetrySample,
    ) -> List[TrackSample]:
        """Advance every track to time ``t`` and fold in this frame's clusters.

        Returns one :class:`~cdf.common.schemas.TrackSample` per *confirmed*
        track that was associated with a cluster in this frame, in track creation
        order. Coasting tracks deliberately emit nothing: a sample is a claim that
        the object was observed, and downstream event extraction must not mistake
        an extrapolation for an observation.

        ``t`` must not move backwards. The check is held against the tracker's
        own clock rather than against the live tracks, so it keeps biting across
        an interval in which every hypothesis has been dropped.
        """
        t = float(t)
        if telemetry.participant_id != self._participant_id:
            raise ValueError(
                "telemetry belongs to participant {0!r} but this tracker serves {1!r}".format(
                    telemetry.participant_id, self._participant_id
                )
            )
        for cluster in clusters:
            if cluster.participant_id != self._participant_id:
                raise ValueError(
                    "cluster belongs to participant {0!r} but this tracker serves {1!r}".format(
                        cluster.participant_id, self._participant_id
                    )
                )
        if self._last_t is not None and t < self._last_t - 1e-9:
            raise ValueError(
                "tracker received t={0!r} after already having advanced to {1!r}".format(
                    t, self._last_t
                )
            )
        self._last_t = t

        predictions = self._predict(t)
        pairs = self._associate(predictions, clusters)

        hit_ids: Set[str] = set()
        matched_clusters: Set[int] = set()
        for track_index, cluster_index in sorted(pairs.items()):
            track = self._tracks[track_index]
            self._apply_hit(
                track, clusters[cluster_index], t, predictions[track_index], telemetry
            )
            hit_ids.add(track.track_id)
            matched_clusters.add(cluster_index)

        for track_index, track in enumerate(self._tracks):
            if track_index in pairs:
                continue
            self._apply_miss(track, t, predictions[track_index], telemetry)

        self._tracks = [
            tr
            for tr in self._tracks
            if tr.misses < self._max_misses
            and not (
                self._max_stationary_frames > 0
                and tr.stationary_streak >= self._max_stationary_frames
            )
        ]

        for cluster_index, cluster in enumerate(clusters):
            if cluster_index in matched_clusters:
                continue
            if self._reject_stationary and cluster.is_stationary:
                # Road surface, kerbs, walls, signs and parked objects all read
                # as world-fixed. Opening a track for each of them buries the
                # handful of genuinely moving objects that matter and shatters
                # identity across frames.
                #
                # The test gates track BIRTH only. An already-established track
                # that later stops -- a vehicle braking to a halt, which is
                # precisely the situation this project studies -- still
                # associates normally above, so it is never lost.
                self._stationary_rejected += 1
                continue
            self._spawn(cluster, t, telemetry)

        self._enforce_capacity()

        out: List[TrackSample] = []
        for track in self._tracks:
            if track.confirmed and track.track_id in hit_ids:
                out.append(self._to_sample(track, t, frame))
        return out

    # -- prediction / association ----------------------------------------

    def _predict(self, t: float) -> List[Tuple[float, float, float]]:
        """Constant-velocity prediction of each track to time ``t``.

        Returns ``(gx, gy, dt)`` per track, in track order. ``dt`` is measured
        from each track's own last update, so a track that coasted through a
        dropout is extrapolated over the whole gap rather than over one frame.
        """
        out: List[Tuple[float, float, float]] = []
        for track in self._tracks:
            dt = t - track.last_t
            if dt < -1e-9:
                raise ValueError(
                    "tracker received t={0!r} before track {1} was last updated at {2!r}".format(
                        t, track.track_id, track.last_t
                    )
                )
            dt = max(0.0, dt)
            out.append((track.gx + track.gvx * dt, track.gy + track.gvy * dt, dt))
        return out

    def _associate(
        self,
        predictions: Sequence[Tuple[float, float, float]],
        clusters: Sequence[RadarCluster],
    ) -> Dict[int, int]:
        """Optimal gated one-to-one assignment of clusters to tracks.

        Pairs farther apart than ``gate_m`` are priced out *before* the solve and
        dropped again afterwards, so the optimiser can never be forced into an
        implausible pairing merely because the matrix had to be square.
        """
        n_tracks = len(predictions)
        n_clusters = len(clusters)
        if n_tracks == 0 or n_clusters == 0:
            return {}

        cost = np.full((n_tracks, n_clusters), _GATE_REJECT_COST, dtype=float)
        for i in range(n_tracks):
            px, py, _dt = predictions[i]
            for j, cluster in enumerate(clusters):
                d = math.hypot(cluster.gx - px, cluster.gy - py)
                if d <= self._gate_m:
                    cost[i, j] = d

        rows, cols = linear_sum_assignment(cost)
        pairs: Dict[int, int] = {}
        for i, j in zip(rows.tolist(), cols.tolist()):
            if cost[i, j] <= self._gate_m:
                pairs[int(i)] = int(j)
        return pairs

    # -- state transitions ------------------------------------------------

    def _apply_hit(
        self,
        track: TrackState,
        cluster: RadarCluster,
        t: float,
        prediction: Tuple[float, float, float],
        telemetry: TelemetrySample,
    ) -> None:
        """Fold one associated cluster into a track (alpha-beta correction)."""
        # A track sustained only by world-fixed returns is, on the evidence,
        # world-fixed. Tracks born in the chaotic frame of an impact otherwise
        # live forever by latching onto roadside structure. The streak is reset
        # by any moving return, so a vehicle that merely stops is not dropped
        # until it has read as static for max_stationary_frames.
        if cluster.is_stationary:
            track.stationary_streak += 1
        else:
            track.stationary_streak = 0
        px, py, dt = prediction
        res_x = cluster.gx - px
        res_y = cluster.gy - py

        track.gx = px + self._pos_alpha * res_x
        track.gy = py + self._pos_alpha * res_y
        if dt > 1e-6:
            track.gvx += self._vel_alpha * res_x / dt
            track.gvy += self._vel_alpha * res_y / dt

        track.hits += 1
        track.misses = 0
        track.age += 1
        track.confidence = min(1.0, track.confidence + self._hit_gain)
        track.last_t = t
        track.n_points = int(cluster.n_points)
        track.extent_x = float(cluster.extent_x)
        track.extent_y = float(cluster.extent_y)

        self._refresh_relative(track, telemetry)
        # The measured radial rate is a direct, unbiased observation; it beats the
        # line-of-sight projection of a still-converging velocity estimate.
        track.range_rate = float(cluster.range_rate)

        if (
            not track.confirmed
            and track.hits >= self._min_hits
            and track.confidence >= self._min_confirm
        ):
            # Confirmation latches: a confirmed track that later fades is dropped
            # by the miss logic, and flickering confirmation would otherwise
            # fragment the event stream built on top of it.
            track.confirmed = True

    def _apply_miss(
        self,
        track: TrackState,
        t: float,
        prediction: Tuple[float, float, float],
        telemetry: TelemetrySample,
    ) -> None:
        """Coast a track that received no cluster this frame."""
        px, py, _dt = prediction
        track.gx = px
        track.gy = py
        track.misses += 1
        track.age += 1
        track.confidence = max(0.0, track.confidence - self._miss_decay)
        track.last_t = t

        self._refresh_relative(track, telemetry)
        # No measurement this frame: fall back to the line-of-sight projection of
        # the estimated relative velocity so that range_rate stays defined.
        if track.range_m > 1e-6:
            track.range_rate = (
                track.rel_x * track.rel_vx + track.rel_y * track.rel_vy
            ) / track.range_m
        else:
            track.range_rate = 0.0

    def _spawn(
        self, cluster: RadarCluster, t: float, telemetry: TelemetrySample
    ) -> None:
        """Open a new hypothesis for an unassociated cluster."""
        track = TrackState(
            track_id=make_track_id(self._participant_id, self._next_index),
            gx=float(cluster.gx),
            gy=float(cluster.gy),
            gvx=0.0,
            gvy=0.0,
            hits=1,
            misses=0,
            age=1,
            confidence=min(1.0, self._hit_gain),
            confirmed=False,
            first_t=t,
            last_t=t,
            n_points=int(cluster.n_points),
            extent_x=float(cluster.extent_x),
            extent_y=float(cluster.extent_y),
        )
        self._next_index += 1
        self._refresh_relative(track, telemetry)
        track.range_rate = float(cluster.range_rate)
        self._tracks.append(track)

    def _enforce_capacity(self) -> None:
        """Keep at most ``max_tracks`` hypotheses, dropping the least credible.

        Ties are broken by creation order, so an established track is never
        evicted by a freshly opened one of equal confidence.
        """
        if len(self._tracks) <= self._max_tracks:
            return
        ranked = sorted(
            range(len(self._tracks)),
            key=lambda i: (-self._tracks[i].confidence, i),
        )
        keep = sorted(ranked[: self._max_tracks])
        self._tracks = [self._tracks[i] for i in keep]

    # -- derived quantities ----------------------------------------------

    def _refresh_relative(
        self, track: TrackState, telemetry: TelemetrySample
    ) -> None:
        """Re-derive body-frame and polar quantities from the global estimate.

        Uses only the observer's own pose and own velocity, which is what keeps a
        track sample admissible local evidence.
        """
        bx, by = global_to_body(
            track.gx, track.gy, telemetry.x, telemetry.y, telemetry.yaw
        )
        track.rel_x = float(bx)
        track.rel_y = float(by)
        track.range_m = float(math.hypot(bx, by))
        track.azimuth_rad = float(math.atan2(by, bx))

        dvx = float(track.gvx) - float(telemetry.vx)
        dvy = float(track.gvy) - float(telemetry.vy)
        rel_vx, rel_vy = rotate2d(dvx, dvy, -float(telemetry.yaw))
        track.rel_vx = float(rel_vx)
        track.rel_vy = float(rel_vy)

    def _to_sample(self, track: TrackState, t: float, frame: int) -> TrackSample:
        """Serialise one track's current estimate as a persisted record."""
        return TrackSample(
            t=float(t),
            frame=int(frame),
            participant_id=self._participant_id,
            track_id=track.track_id,
            rel_x=track.rel_x,
            rel_y=track.rel_y,
            gx=track.gx,
            gy=track.gy,
            gvx=track.gvx,
            gvy=track.gvy,
            range_m=track.range_m,
            azimuth_rad=track.azimuth_rad,
            range_rate=track.range_rate,
            rel_vx=track.rel_vx,
            rel_vy=track.rel_vy,
            n_points=track.n_points,
            extent_x=track.extent_x,
            extent_y=track.extent_y,
            confidence=track.confidence,
            age=track.age,
            misses=track.misses,
            ttc=time_to_collision_1d(track.range_m, track.range_rate),
        )
