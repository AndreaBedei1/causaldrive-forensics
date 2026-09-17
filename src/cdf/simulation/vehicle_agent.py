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
from ..common.evidence import ParticipantEvidence
from ..common.layout import RunLayout
from ..common.schemas import (
    ControlSample,
    LocalTriggerRecord,
    RadarFrame,
    TelemetrySample,
    TrackSample,
    TriggerKind,
)
from ..local.own_state import make_telemetry
from ..local.radar import RadarCluster, RadarFrontEnd
from ..local.recorder import RollingRecorder
from ..local.tracking import RadarTracker
from .carla_client import import_carla
from .controllers import ControlCommand, ScriptedController, VehicleState
from .scenario_base import ParticipantSpec
from .sensors import CollisionSensor, RadarSensor, radar_specs_from_config

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
    ) -> None:
        self.world = scenario_world
        self.spec = spec
        self.participant_id = spec.participant_id
        self.controller = controller
        self.spawn_transform = spawn_transform

        self.cfg = participant_config(cfg, spec)
        self.seed = int(seed)
        # Each participant gets its own deterministic stream so that adding a
        # third vehicle cannot perturb the first two's degraded-radar draws.
        self._rng = random.Random(
            (self.seed * 1000003) ^ (abs(hash(self.participant_id)) & 0xFFFF)
        )

        self.vehicle: Any = None
        self.radars: List[RadarSensor] = []
        self.collision_sensor: Optional[CollisionSensor] = None

        # Simulator time at which the scenario proper begins. Every timestamp the
        # participant records is expressed relative to it, so scripted action
        # times ("brake at t=6.0") and recorded evidence share one clock and
        # artifacts stay comparable across runs and across server sessions.
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
        LOGGER.info(
            "participant %s spawned: %s with %d radar(s), profile=%s",
            self.participant_id,
            self.spec.blueprint,
            len(self.radars),
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
        telemetry, control = self.read_own_state(t, frame)

        radar_frames = self._poll_radars(frame)
        clusters: List[RadarCluster] = []
        for rframe in radar_frames:
            clusters.extend(self.front_end.process(rframe, telemetry))

        track_samples = self.tracker.update(t, frame, clusters, telemetry)
        self._latest_tracks = list(track_samples)

        self.recorder.record_telemetry(telemetry)
        self.recorder.record_control(control)
        for rframe in radar_frames:
            self.recorder.record_radar(rframe)
        self.recorder.record_tracks(track_samples)

        self._handle_triggers(t, frame, telemetry, control, track_samples)

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
            rframe.t = float(rframe.t) - self.time_offset
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
                rec.t = float(rec.t) - self.time_offset
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
                self.recorder.trigger(rec)
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

    # -- results ----------------------------------------------------------

    @property
    def triggered(self) -> bool:
        return self.recorder.triggered

    @property
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
        return self.recorder.persist(layout)

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
        }
