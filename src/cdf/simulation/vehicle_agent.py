"""One participant vehicle: its actuation, its sensors and its local pipeline.

Every participant in a scenario is an ego vehicle from its own point of view.
:class:`ParticipantAgent` is where that principle becomes concrete: the agent
owns a CARLA vehicle and *only* reads that vehicle's own pose, velocity and
control, plus the returns of radars bolted to it. Those measurements flow
straight into the participant's private radar front-end, tracker and rolling
recorder. Nothing about any other actor is ever queried.

The class is deliberately the narrow waist between the simulator and the local
pipeline: if a privileged quantity were ever to reach local inference, it would
have to pass through here, which makes the boundary auditable in one file.
"""

from __future__ import annotations

import logging
import math
import random
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config, deep_merge, load_yaml
from ..common.clocks import LocalClock
from ..common.evidence import ParticipantEvidence
from ..common.io import write_json
from ..common.layout import RunLayout
from ..common.schemas import (
    ControlSample,
    Event,
    EventType,
    Provenance,
    LocalTriggerRecord,
    RadarFrame,
    TelemetrySample,
    TrackSample,
    TriggerKind,
)
from ..local.own_state import make_telemetry
from ..local.radar import RadarCluster, RadarFrontEnd
from ..local.recorder import RollingRecorder
from ..local.video_buffer import VideoBuffer
from ..local.tracking import RadarTracker
from .carla_client import import_carla
from .controllers import ControlCommand, ScriptedController, VehicleState
from .scenario_base import ParticipantSpec
from .sensors import (
    CameraSensor, CollisionSensor, LaneInvasionSensor, RadarSensor,
    camera_spec_from_config, radar_specs_from_config,
)

LOGGER = logging.getLogger(__name__)

__all__ = ["ParticipantAgent", "participant_config"]


def participant_config(cfg: Config, spec: ParticipantSpec) -> Config:
    """Resolve a participant-specific configuration.

    A participant may override the radar profile (scenario S07 gives one vehicle
    a narrow-FOV sensor so that its partial view arises from *sensing*, not from
    deleting data afterwards). Everything else is inherited from the run
    configuration.
    """
    if not spec.sensor_profile:
        return cfg
    from ..common.config import configs_dir

    path = configs_dir() / "sensors" / "{0}.yaml".format(spec.sensor_profile)
    if not path.exists():
        raise FileNotFoundError(
            "participant {0} requests unknown sensor profile {1!r} ({2})".format(
                spec.participant_id, spec.sensor_profile, path
            )
        )
    profile = load_yaml(path)
    merged = deep_merge(
        cfg.data, {"radar": profile.get("radar", {}), "sensors": {"profile": spec.sensor_profile}}
    )
    return Config(merged, cfg.sources + [str(path)])


class ParticipantAgent:
    """A participant vehicle and its complete onboard forensic stack."""

    def __init__(
        self,
        scenario_world: Any,
        cfg: Config,
        spec: ParticipantSpec,
        controller: ScriptedController,
        spawn_transform: Any,
        seed: int = 0,
        clock_context: str = "",
    ) -> None:
        self.world = scenario_world
        self.spec = spec
        self.participant_id = spec.participant_id
        self.controller = controller
        self.spawn_transform = spawn_transform

        self.cfg = participant_config(cfg, spec)
        self.seed = int(seed)
        self.clock = LocalClock.for_participant(self.cfg, seed, self.participant_id, clock_context)
        self.latest_trigger_sim_time: Optional[float] = None
        # Each participant gets its own deterministic stream so that adding a
        # third vehicle cannot perturb the first two's degraded-radar draws.
        self._rng = random.Random(
            (self.seed * 1000003) ^ (abs(hash(self.participant_id)) & 0xFFFF)
        )

        self.vehicle: Any = None
        self.radars: List[RadarSensor] = []
        self.collision_sensor: Optional[CollisionSensor] = None
        self.camera: Optional[CameraSensor] = None
        self.lane_sensor: Optional[LaneInvasionSensor] = None

        # The camera buffer is bounded by construction: it holds the configured
        # pre-event window until a contact latches it, then five seconds more.
        # Nothing here can grow with run length, which is the whole premise of a
        # vehicle that keeps a short rolling window rather than a full recording.
        camera_spec = camera_spec_from_config(self.cfg)
        self.video: Optional[VideoBuffer] = VideoBuffer(
            pre_event_s=float(self.cfg.get("sensors.camera.pre_event_s", 20.0)),
            post_event_s=float(self.cfg.get("sensors.camera.post_event_s", 5.0)),
            max_frames=int(self.cfg.get("sensors.camera.max_frames", 1200)),
            participant_id=self.participant_id,
            sensor_id=camera_spec.sensor_id if camera_spec else "front",
        ) if camera_spec is not None else None
        self._camera_spec = camera_spec
        #: ``(t_local, frame, array)`` for perception, kept only while the frame
        #: is inside the retained window -- the same bound as the video buffer,
        #: because holding full-resolution arrays for the whole run would cost
        #: more than the encoded clip it is meant to accompany.
        self._perception_frames: List[Any] = []
        self._camera_frames_missed = 0

        # Simulator time at which the scenario proper begins. Every timestamp the
        # participant samples is first rebased onto scenario time. The recorder
        # clock then perturbs that time; scripted controllers remain on sim time.
        self.time_offset: float = 0.0

        self.front_end = RadarFrontEnd(self.cfg, self.participant_id, rng=self._rng)
        self.tracker = RadarTracker(self.cfg, self.participant_id)
        self.recorder = RollingRecorder(self.cfg, self.participant_id)

        self._prev_telemetry: Optional[TelemetrySample] = None
        self._last_command = ControlCommand()
        self._near_miss_armed = True
        self._brake_trigger_armed = True
        self._radar_frames_seen = 0
        self._radar_frames_missed = 0
        self._latest_tracks: List[TrackSample] = []
        self._last_collision_t: Optional[float] = None
        self._collisions_debounced = 0

    # -- construction -----------------------------------------------------

    def spawn(self) -> Any:
        """Spawn the vehicle and attach its radars and collision sensor."""
        self.vehicle = self.world.spawn_vehicle(self.spec.blueprint, self.spawn_transform)
        for rspec in radar_specs_from_config(self.cfg):
            self.radars.append(
                RadarSensor(self.world, self.vehicle, rspec, self.participant_id)
            )
        self.collision_sensor = CollisionSensor(self.world, self.vehicle, self.participant_id)
        if self._camera_spec is not None:
            self.camera = CameraSensor(
                self.world, self.vehicle, self._camera_spec, self.participant_id
            )
        if bool(self.cfg.get("sensors.lane_invasion.enabled", True)):
            self.lane_sensor = LaneInvasionSensor(
                self.world, self.vehicle, self.participant_id
            )
        LOGGER.info(
            "participant %s spawned: %s with %d radar(s), camera=%s, lane=%s, "
            "profile=%s",
            self.participant_id,
            self.spec.blueprint,
            len(self.radars),
            "on" if self.camera else "off",
            "on" if self.lane_sensor else "off",
            self.cfg.get("sensors.profile", "?"),
        )
        return self.vehicle

    def apply_initial_speed(self) -> None:
        """Impart the specified initial velocity along the vehicle's heading.

        Scenarios start mid-manoeuvre so the encounter is reached quickly and
        deterministically, instead of depending on a long acceleration run-up
        whose timing drifts with vehicle dynamics.
        """
        if self.vehicle is None or self.spec.initial_speed <= 0.0:
            return
        carla = import_carla()
        yaw = math.radians(self.vehicle.get_transform().rotation.yaw)
        speed = float(self.spec.initial_speed)
        self.vehicle.set_target_velocity(
            carla.Vector3D(x=math.cos(yaw) * speed, y=math.sin(yaw) * speed, z=0.0)
        )

    # -- per-tick ---------------------------------------------------------

    def read_own_state(self, t: float, frame: int) -> Tuple[TelemetrySample, ControlSample]:
        """Sample this vehicle's own pose, motion and actuation.

        Only ``self.vehicle`` is touched. This is the onboard localisation/IMU
        proxy plus the vehicle's own actuator feedback.
        """
        tf = self.vehicle.get_transform()
        vel = self.vehicle.get_velocity()
        acc = self.vehicle.get_acceleration()
        ang = self.vehicle.get_angular_velocity()
        ctrl = self.vehicle.get_control()

        telemetry = make_telemetry(
            participant_id=self.participant_id,
            t=float(t),
            frame=int(frame),
            x=float(tf.location.x),
            y=float(tf.location.y),
            z=float(tf.location.z),
            yaw=float(tf.rotation.yaw),
            pitch=float(tf.rotation.pitch),
            roll=float(tf.rotation.roll),
            vx=float(vel.x),
            vy=float(vel.y),
            vz=float(vel.z),
            ax=float(acc.x),
            ay=float(acc.y),
            az=float(acc.z),
            yaw_rate=float(ang.z),
        )
        control = ControlSample(
            t=float(t),
            frame=int(frame),
            participant_id=self.participant_id,
            throttle=float(ctrl.throttle),
            brake=float(ctrl.brake),
            steer=float(ctrl.steer),
            hand_brake=bool(ctrl.hand_brake),
            reverse=bool(ctrl.reverse),
            gear=int(getattr(ctrl, "gear", 0)),
        )
        return telemetry, control

    def step(self, t: float, frame: int, dt: float) -> None:
        """Advance this participant's onboard stack by one simulation step."""
        local_t, local_frame = self.clock.stamp(t, frame)
        telemetry, control = self.read_own_state(local_t, local_frame)

        radar_frames = self._poll_radars(frame)
        clusters: List[RadarCluster] = []
        for rframe in radar_frames:
            clusters.extend(self.front_end.process(rframe, telemetry))

        track_samples = self.tracker.update(local_t, local_frame, clusters, telemetry)
        self._latest_tracks = list(track_samples)

        self.recorder.record_telemetry(telemetry)
        self.recorder.record_control(control)
        for rframe in radar_frames:
            self.recorder.record_radar(rframe)
        self.recorder.record_tracks(track_samples)

        self._poll_camera(frame, local_t)

        self._handle_triggers(local_t, local_frame, telemetry, control, track_samples, sim_t=t)

        command = self.controller.step(
            VehicleState(
                t=float(t),
                x=telemetry.x,
                y=telemetry.y,
                yaw=telemetry.yaw,
                speed=telemetry.speed,
                vx=telemetry.vx,
                vy=telemetry.vy,
            ),
            dt,
        )
        self._apply_command(command)
        self._prev_telemetry = telemetry

    def _poll_camera(self, frame: int, local_t: float) -> None:
        """Take this tick's image, compress it into the buffer, keep it for perception.

        A missed frame is counted and skipped rather than waited on: blocking the
        tick to wait for a camera would change the physics being recorded, which
        is a far worse outcome than a gap in the video.
        """
        if self.camera is None or self.video is None:
            return
        image = self.camera.poll(frame, timeout_s=0.5)
        if image is None:
            self._camera_frames_missed += 1
            return
        kept = self.video.add(
            local_t, frame, image["jpeg"], encoding="jpeg",
            width=image["width"], height=image["height"],
        )
        if not kept:
            return
        self._perception_frames.append((local_t, frame, image["array"]))
        # Keep the perception frames in step with the buffer. The buffer evicts
        # by time; matching that here means the arrays cannot outlive the clip
        # they belong to.
        span = self.video.span()
        if span is not None:
            self._perception_frames = [
                f for f in self._perception_frames if f[0] >= span[0]
            ]

    def _poll_radars(self, frame: int) -> List[RadarFrame]:
        """Collect this tick's radar frames, tolerating an occasional miss.

        Radar timestamps arrive on the simulator's absolute clock and are rebased
        onto scenario time here, so a radar frame and the telemetry sample of the
        same tick carry the same ``t``.
        """
        out: List[RadarFrame] = []
        for radar in self.radars:
            rframe = radar.poll(frame)
            if rframe is None:
                self._radar_frames_missed += 1
                continue
            self._radar_frames_seen += 1
            rframe.t, rframe.frame = self.clock.stamp(float(rframe.t) - self.time_offset, rframe.frame)
            out.append(rframe)
        return out

    def drain_radar_queues(self, frame: int) -> None:
        """Discard radar output produced during warm-up.

        The first frames after spawn are unreliable (a spurious ~100 m/s return
        was measured on this build) and would otherwise sit in the queue and be
        attributed to the first recorded tick.
        """
        for radar in self.radars:
            radar.poll(frame, timeout_s=0.5)

    def _apply_command(self, command: ControlCommand) -> None:
        carla = import_carla()
        self._last_command = command
        self.vehicle.apply_control(
            carla.VehicleControl(
                throttle=float(command.throttle),
                brake=float(command.brake),
                steer=float(command.steer),
                hand_brake=bool(command.hand_brake),
                reverse=bool(command.reverse),
            )
        )

    # -- triggers ---------------------------------------------------------

    def _handle_triggers(
        self,
        t: float,
        frame: int,
        telemetry: TelemetrySample,
        control: ControlSample,
        tracks: Sequence[TrackSample],
        sim_t: float,
    ) -> None:
        """Evaluate every recorder trigger from ONBOARD evidence only."""
        # --- collision: reported by the onboard sensor, identity stripped ---
        if self.collision_sensor is not None:
            min_impulse = float(self.cfg.get("recorder.triggers.collision.min_impulse", 1.0))
            debounce_s = float(self.cfg.get("recorder.triggers.collision.debounce_s", 0.5))
            for rec in self.collision_sensor.drain_local(min_impulse=min_impulse):
                # CARLA stamps collision events with the absolute simulator
                # clock; rebase onto scenario time so the trigger lines up with
                # the telemetry and radar samples recorded for the same tick.
                collision_sim_t = float(rec.t) - self.time_offset
                rec.t, rec.frame = self.clock.stamp(collision_sim_t, rec.frame)
                # Vehicles that stay in contact emit an event every frame. They
                # describe ONE impact, so collapse them: otherwise the event
                # extractor would report a dozen COLLISION events for one crash.
                if (
                    self._last_collision_t is not None
                    and rec.t - self._last_collision_t < debounce_s
                ):
                    self._collisions_debounced += 1
                    continue
                self._last_collision_t = rec.t
                self.latest_trigger_sim_time = collision_sim_t
                self.recorder.trigger(rec)
                # Stop the camera's pre-event window rolling. Only the first
                # contact counts: a chain fires several and re-arming on each
                # would turn a bounded tail into an unbounded one.
                self.latch_video(rec.t)
                self.controller.notify_impact()
                LOGGER.info(
                    "participant %s: collision trigger at t=%.2f (impulse %.1f)",
                    self.participant_id,
                    rec.t,
                    rec.impulse,
                )

        # --- near miss: derived from our own tracks' TTC ---
        if self._near_miss_armed and bool(
            self.cfg.get("recorder.triggers.near_miss.enabled", True)
        ):
            ttc_thr = float(self.cfg.get("recorder.triggers.near_miss.ttc_s", 0.9))
            range_thr = float(self.cfg.get("recorder.triggers.near_miss.min_range_m", 12.0))
            for s in tracks:
                if s.ttc is not None and s.ttc <= ttc_thr and s.range_m <= range_thr:
                    self.recorder.trigger(
                        LocalTriggerRecord(
                            t=float(t),
                            frame=int(frame),
                            participant_id=self.participant_id,
                            kind=TriggerKind.NEAR_MISS,
                            collision_detected=False,
                            impulse=0.0,
                            detail={
                                "ttc": float(s.ttc),
                                "range_m": float(s.range_m),
                                "track_id": s.track_id,
                                "source": "local_ttc",
                            },
                        )
                    )
                    self._near_miss_armed = False
                    self.latest_trigger_sim_time = float(sim_t)
                    LOGGER.info(
                        "participant %s: near-miss trigger at t=%.2f (ttc %.2f s)",
                        self.participant_id,
                        t,
                        s.ttc,
                    )
                    break

        # --- emergency braking: our own control and deceleration ---
        if self._brake_trigger_armed and bool(
            self.cfg.get("recorder.triggers.emergency_brake.enabled", True)
        ):
            brake_thr = float(self.cfg.get("recorder.triggers.emergency_brake.brake_cmd", 0.85))
            decel_thr = float(self.cfg.get("recorder.triggers.emergency_brake.decel_mps2", 5.5))
            if control.brake >= brake_thr and telemetry.accel_long <= -decel_thr:
                self.recorder.trigger(
                    LocalTriggerRecord(
                        t=float(t),
                        frame=int(frame),
                        participant_id=self.participant_id,
                        kind=TriggerKind.EMERGENCY_BRAKE,
                        collision_detected=False,
                        impulse=0.0,
                        detail={
                            "brake": float(control.brake),
                            "accel_long": float(telemetry.accel_long),
                            "source": "local_control",
                        },
                    )
                )
                self._brake_trigger_armed = False
                self.latest_trigger_sim_time = float(sim_t)

    # -- results ----------------------------------------------------------

    @property
    def triggered(self) -> bool:
        return self.recorder.triggered

    @property
    def latch_video(self, local_t: float) -> None:
        """Stop the pre-event window rolling: the event has happened.

        Called on the first contact. Only the first counts -- a chain fires
        several triggers, and re-arming on each would turn a bounded tail into an
        unbounded one.
        """
        if self.video is not None:
            self.video.mark_event(local_t)

    def finished(self) -> bool:
        return self.recorder.finished

    @property
    def collided(self) -> bool:
        return self.collision_sensor is not None and self.collision_sensor.any_collision

    @property
    def latest_tracks(self) -> List[TrackSample]:
        """Track samples emitted on the most recent step."""
        return list(self._latest_tracks)

    def sensor_health(self) -> Dict[str, Any]:
        """Radar delivery statistics, surfaced in the run manifest.

        A high miss count means the run loop and the sensor stream drifted apart,
        which would silently degrade every downstream estimate -- so it is
        reported rather than hidden.
        """
        return {
            "radar_frames_seen": self._radar_frames_seen,
            "radar_frames_missed": self._radar_frames_missed,
            "radar_queue_dropped": sum(r.dropped for r in self.radars),
            "sensor_profile": self.cfg.get("sensors.profile", "?"),
            "n_radars": len(self.radars),
            "collisions_debounced": self._collisions_debounced,
        }

    def finalize(self) -> ParticipantEvidence:
        """Stop the sensors and return the retained evidence window."""
        for radar in self.radars:
            radar.stop()
        if self.collision_sensor is not None:
            self.collision_sensor.stop()
        return self.recorder.to_evidence()

    def persist(self, layout: RunLayout) -> ParticipantEvidence:
        """Persist the retained evidence window under ``vehicle_<id>/``."""
        evidence = self.recorder.persist(layout)
        self._persist_camera(layout)
        self._persist_lane_events(layout)
        return evidence

    def _persist_camera(self, layout: RunLayout) -> None:
        """Write the clip, its index, and what perception made of the frames.

        Perception runs here rather than during the tick because it needs the
        whole sequence: a sign is one perception across tens of frames, and a
        stop line is only known to have been crossed once it has left the frame.
        Running it per tick could not see either.
        """
        if self.video is None or not len(self.video):
            return
        from ..local.sign_perception import detect_signs
        from ..local.stop_line_perception import detect_stop_lines
        from ..common.schemas import to_jsonable

        layout.video_dir(self.participant_id).mkdir(parents=True, exist_ok=True)
        layout.perception_dir(self.participant_id).mkdir(parents=True, exist_ok=True)
        index = self.video.index()
        index["n_frames_missed"] = self._camera_frames_missed
        write_json(layout.frame_index(self.participant_id), index)
        _encode_clip(self.video, layout.front_video(self.participant_id))

        frames = list(self._perception_frames)
        signs = detect_signs(frames, cfg=self.cfg, image_width=index.get("width", 0))
        # One event per confirmed sign track, at the moment the evidence first
        # became good enough -- not one per frame, which would put dozens of
        # nodes in the graph for one physical sign.
        signs["events"] = [
            to_jsonable(e) for e in _sign_events(signs, self.participant_id)
        ]
        write_json(layout.traffic_sign_detections(self.participant_id), signs)

        speeds = {
            float(t.t): float(t.speed) for t in self.recorder.to_evidence().telemetry
        }
        stop_lines = detect_stop_lines(
            frames, speed_at=_nearest_speed(speeds), cfg=self.cfg,
            participant_id=self.participant_id,
        )
        stop_lines["events"] = [to_jsonable(e) for e in stop_lines["events"]]
        write_json(
            layout.perception_dir(self.participant_id) / "stop_lines.json", stop_lines
        )

    def _persist_lane_events(self, layout: RunLayout) -> None:
        """Collapse the lane sensor's reports into the crossings they were."""
        if self.lane_sensor is None:
            return
        from ..local.lane_events import build_lane_events
        from ..common.schemas import to_jsonable

        records = self.lane_sensor.drain()
        for record in records:
            # The sensor stamps simulator time; every other local record is on
            # this recorder's own clock, and mixing the two inside one vehicle
            # would be a worse error than any this project is studying.
            local_t, local_frame = self.clock.stamp(
                float(record["t"]) - self.time_offset, int(record["frame"])
            )
            record["t"], record["frame"] = local_t, local_frame
        result = build_lane_events(self.participant_id, records, cfg=self.cfg)
        layout.perception_dir(self.participant_id).mkdir(parents=True, exist_ok=True)
        result["events"] = [to_jsonable(e) for e in result["events"]]
        write_json(layout.lane_events(self.participant_id), result)

    def manifest_block(self) -> Dict[str, Any]:
        """Per-participant provenance for the run manifest."""
        tf = self.spawn_transform
        return {
            "participant_id": self.participant_id,
            "blueprint": self.spec.blueprint,
            "spawn": {
                "x": float(tf.location.x),
                "y": float(tf.location.y),
                "z": float(tf.location.z),
                "yaw": float(tf.rotation.yaw),
            },
            "controller": "ScriptedController",
            "controller_params": self.controller.describe(),
            "sensor_profile": self.cfg.get("sensors.profile", "?"),
            "radar_sensors": self.cfg.get("radar.sensors", []),
            "initial_speed": self.spec.initial_speed,
            "target_speed": self.spec.target_speed,
            "sensor_health": self.sensor_health(),
            "camera": (
                {
                    "width": self._camera_spec.width,
                    "height": self._camera_spec.height,
                    "fov_deg": self._camera_spec.fov_deg,
                    "pre_event_s": self.video.pre_event_s if self.video else None,
                    "post_event_s": self.video.post_event_s if self.video else None,
                    "frames_missed": self._camera_frames_missed,
                }
                if self._camera_spec is not None else None
            ),
            "lane_sensor": self.lane_sensor is not None,
        }

def _nearest_speed(speeds):
    """A speed lookup by nearest recorded sample.

    The stop-line inference needs to know the vehicle was moving when the
    marking left the frame. Nearest-sample rather than interpolation: at 20 Hz
    the difference is far below the threshold being tested, and interpolating
    would invent a value between two real ones.
    """
    if not speeds:
        return None
    ordered = sorted(speeds)

    def at(t: float) -> float:
        best = min(ordered, key=lambda s: abs(s - float(t)))
        return speeds[best]

    return at


def _sign_events(detection: Dict[str, Any], participant_id: str) -> List[Event]:
    """One event per confirmed sign track, at its first confident sighting."""
    from ..common.schemas import Evidence

    kinds = {
        "STOP": EventType.STOP_SIGN_DETECTED,
        "YIELD": EventType.YIELD_SIGN_DETECTED,
    }
    out: List[Event] = []
    for track in detection.get("tracks", []) or []:
        event_type = kinds.get(str(track.get("class")))
        if event_type is None:
            continue
        relevance = track.get("relevance") or {}
        out.append(Event(
            event_id="sign-{0}-{1}".format(participant_id, track["sign_track_id"]),
            event_type=event_type,
            participant_id=str(participant_id),
            t_start=float(track["t_first"]),
            t_peak=float(track["t_first"]),
            t_end=float(track["t_last"]),
            subject=None,
            values={"centredness": float(relevance.get("centredness", 0.0))},
            detail={
                "sign_track_id": track["sign_track_id"],
                "n_detections": track["n_detections"],
                "best_bbox": track.get("best_bbox"),
                "relevant_to_ego_path": relevance.get("relevant_to_ego_path"),
                "method": "camera only; no privileged sign label consulted",
            },
            confidence=float(track.get("best_confidence", 0.0)),
            evidence=[Evidence(
                kind="camera", ref=str(track["sign_track_id"]),
                t_start=float(track["t_first"]), t_end=float(track["t_last"]),
                detail={"n_detections": track["n_detections"]},
            )],
            provenance=Provenance.LOCAL,
            source_sensors=["camera"],
        ))
    return sorted(out, key=lambda e: (e.t_peak, e.event_id))


def _encode_clip(video, path) -> None:
    """Mux the buffered frames into a playable file, or leave the frames alone.

    Encoding happens after the run, never during it: an encoder on the critical
    path of a synchronous tick changes the physics being recorded. If no encoder
    is available the clip is simply absent and the frame index stands on its own
    -- the viewer copes, and a missing video is a degraded artifact rather than a
    lost run.
    """
    frames = video.frames
    if not frames:
        return
    try:
        import cv2
        import numpy as np
    except ImportError:  # pragma: no cover - environment-dependent
        LOGGER.warning("no encoder available; %s not written", path.name)
        return

    spans = [frames[i + 1].t - frames[i].t for i in range(len(frames) - 1)]
    period = sorted(spans)[len(spans) // 2] if spans else 0.05
    fps = max(1.0, 1.0 / max(period, 1e-3))
    writer = None
    try:
        for frame in frames:
            image = cv2.imdecode(
                np.frombuffer(frame.payload, dtype=np.uint8), cv2.IMREAD_COLOR
            )
            if image is None:
                continue
            if writer is None:
                height, width = image.shape[:2]
                writer = cv2.VideoWriter(
                    str(path), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
                )
                if not writer.isOpened():
                    LOGGER.warning("could not open %s for writing", path.name)
                    return
            writer.write(image)
    finally:
        if writer is not None:
            writer.release()
