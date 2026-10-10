#!/usr/bin/env python3
"""Interactive slow-motion replay of a recorded run in CARLA (visualization only).

    python scripts/replay_run.py traces/S01/run_0_crash [--speed 0.25]

Every rendered frame, the recorded ego.jsonl pose of each vehicle is
interpolated at the playback time and applied directly to a physics-less CARLA
actor.  No scenario controller runs and CARLA simulates no vehicle physics, so
every playback speed shows exactly the recorded trajectories.  Reconstructed
events (local graphs, global collisions, track associations) and each
recorder's perceived state (``local_trace.jsonl``: its tracks with CLOSING,
CRITICAL_TTC, CUT_IN, ..., lost tracks, known signs) are only read and
displayed, never derived here; nothing is written anywhere.

The viewer shows what the reconstruction knows, not the simulator's ground
truth: only the recorders (vehicles with their own ego.jsonl) are replayed as
vehicles, and the map is recognised from their recorded positions and the
public OpenDRIVE files (``--map`` overrides it).  What each recorder's radar
tracks is drawn in its colour: an ANONYMOUS track (no recorder identified with
it) as a ghost, a wireframe box of the reconstruction's nominal target size
(not a measured body) with an arrow along its estimated motion, solid while
measured, dashed while only PREDICTED, gone at its TRACK_LOST; a track
associated with a recorder as a radar dot, a line from its observer and
``A:track_002 → B``, never a second body.  Tracks of different recorders are
never merged.

Controls: SPACE play/pause, R restart, LEFT/RIGHT seek 0.5 s (with SHIFT
0.05 s), N/P next/previous reconstructed event, 1-4 speed 0.25/0.5/1/2x,
C camera mode, TAB next recorder, T tracks, G ghost boxes or dots, H help, ESC
exit.  In the free camera: W/A/S/D/Q/E move (SHIFT faster); drag with the
mouse to look or orbit, wheel to zoom.
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import math
import queue
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.common.config import load_run_config  # noqa: E402
from cdf.replay.model import (BOX_EDGES, HEADING_HELD, HEADING_UNKNOWN, MAP_MIN_FIT, SPEEDS,  # noqa: E402
                              FreeCamera, PlaybackClock, Pose, ReplayRun, TrackPath, TrackPoint, Vector,
                              box_corners, choose_map, follow_camera, overview_camera, project, project_segment,
                              rotate)
from cdf.simulation.carla_client import (find_carla_root, import_carla, map_basename,  # noqa: E402
                                         session_from_config)

LOGGER = logging.getLogger("replay")
ROLE_PREFIX = "replay_"
PALETTE = [(230, 57, 70), (52, 120, 246), (46, 184, 92), (245, 158, 11), (168, 85, 247),
           (20, 184, 166), (236, 72, 153), (140, 140, 140)]
CAMERA_MODES = ("overview", "follow", "free")
SEEK_S, FINE_SEEK_S = 0.5, 0.05
EVENT_WINDOW_S = 1.0  # replay seconds an event stays next to its vehicle
COLLISION_WINDOW_S = 1.5
LABEL_CLEARANCE_M = 0.6  # label anchor above the roof
TRACK_DOT_HEIGHT_M = 0.8  # radar dots above the road (tracks are planar)
OPENDRIVE_DIR = Path("CarlaUE4") / "Content" / "Carla" / "Maps" / "OpenDrive"
HELP = ("SPACE play/pause   R restart   ←/→ ±0.5 s (SHIFT ±0.05 s)   N/P next/prev event   "
        "1-4 speed   C camera   TAB recorder   T tracks   G ghost boxes/dots   H help   ESC exit")
LEGEND = ("ghost box = ANONYMOUS radar track (nominal {0:.1f} x {1:.1f} x {2:.1f} m, not a measured body): "
          "solid measured, dashed PREDICTED   dot + line = track associated with a recorder")
FREE_HELP = "free camera: W/A/S/D/Q/E move (SHIFT faster), drag to look, wheel to move"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay a recorded run in CARLA (visualization only)")
    parser.add_argument("run_dir", help="run directory, e.g. traces/S01/run_0_crash")
    parser.add_argument("--speed", type=float, default=0.5, help="playback speed (default 0.5x)")
    parser.add_argument("--start", type=float, default=0.0, help="start at this replay time [s]")
    parser.add_argument("--paused", action="store_true", help="start paused")
    parser.add_argument("--camera", choices=CAMERA_MODES, default="overview")
    parser.add_argument("--follow", default=None, help="recorder selected for the follow camera")
    parser.add_argument("--hide-tracks", action="store_true",
                        help="start with the radar-track overlay hidden (toggle with T)")
    parser.add_argument("--show-tracks", action="store_true", help=argparse.SUPPRESS)  # markers are on by default
    parser.add_argument("--track-dots", action="store_true",
                        help="start with anonymous tracks as dots instead of ghost boxes (toggle with G)")
    parser.add_argument("--res", default="1280x720", help="window size WxH")
    parser.add_argument("--fov", type=float, default=90.0)
    parser.add_argument("--fps", type=float, default=30.0, help="render rate (CARLA ticks per wall second)")
    parser.add_argument("--map", default=None,
                        help="CARLA map; default: recognised from the recorders' recorded positions")
    parser.add_argument("--no-autostart", action="store_true", help="do not start a local CARLA process")
    parser.add_argument("--keep-server", action="store_true", help="leave a CARLA server this viewer started running")
    parser.add_argument("--exit-after", type=float, default=None, help=argparse.SUPPRESS)  # smoke tests
    args = parser.parse_args(argv)
    width, _, height = args.res.lower().partition("x")
    args.res = (int(width), int(height))
    if args.speed <= 0:
        parser.error("--speed must be positive")
    return args


def opendrive_sources(carla_root: Optional[Path]) -> Dict[str, str]:
    """Map name -> OpenDRIVE text of the maps shipped with a local CARLA installation (public files)."""
    if carla_root is None:
        return {}
    return {path.stem: path.read_text(encoding="utf-8", errors="replace")
            for path in sorted((Path(carla_root) / OPENDRIVE_DIR).glob("*.xodr"))}


def lane_share(lane_map: Any, samples: Sequence[Vector]) -> float:
    """Share of the positions inside a driving lane of ``lane_map`` (a carla.Map)."""
    carla = import_carla()
    inside = sum(1 for x, y, z in samples
                 if lane_map.get_waypoint(carla.Location(x=x, y=y, z=z), project_to_road=False,
                                          lane_type=carla.LaneType.Driving) is not None)
    return inside / float(len(samples)) if samples else 0.0


def resolve_map(run: ReplayRun, carla_root: Optional[Path], current: Optional[str],
                current_map: Any = None) -> Optional[str]:
    """The map the recorders drove on, from their own recorded positions only.

    Every OpenDRIVE map of the local CARLA installation is parsed client-side
    and scored by the share of recorded ego positions inside its driving lanes
    (``choose_map``).  Without a local installation only the server's current
    map (``current_map``) can be checked.  No scenario configuration, run
    metadata or ground truth is read.
    """
    carla = import_carla()
    samples = run.map_samples()
    sources = opendrive_sources(carla_root)
    if not sources:
        if current_map is None:
            return None
        share = lane_share(current_map, samples)
        LOGGER.warning("no local OpenDRIVE files: only the server's map %s was checked (%.0f%% of the recorded "
                       "positions in its driving lanes)", current, 100.0 * share)
        return current if share >= MAP_MIN_FIT else None
    fits: Dict[str, float] = {}
    networks: Dict[str, str] = {}
    scored: Dict[str, float] = {}
    for name, text in sources.items():
        network = hashlib.sha1(text.encode("utf-8")).hexdigest()  # Town05 and Town05_Opt share one
        if network not in scored:
            scored[network] = lane_share(carla.Map(name, text), samples)
        fits[name], networks[name] = scored[network], network
    ranked = sorted(fits.items(), key=lambda item: (-item[1], item[0]))
    LOGGER.info("recorded positions in the driving lanes of: %s",
                ", ".join("{0} {1:.0%}".format(name, fit) for name, fit in ranked[:4]))
    return choose_map(fits, networks, current)


class ReplayApp:
    """CARLA actors, a camera and the pygame window for one replay."""

    def __init__(self, run: ReplayRun, map_name: str, client: Any, world: Any, args: argparse.Namespace):
        self.carla = import_carla()
        self.run, self.map_name, self.client, self.world, self.args = run, map_name, client, world, args
        self.width, self.height = args.res
        self.ids = [p.participant_id for p in run.participants]  # the recorders: TAB cycles these only
        self.colors = {pid: PALETTE[i % len(PALETTE)] for i, pid in enumerate(self.ids)}
        self.clock = PlaybackClock(run.duration, speed=args.speed, start=args.start, playing=not args.paused)
        self.events = run.all_events()
        self.selected = args.follow if args.follow in self.ids else self.ids[0]
        self.camera_mode = args.camera
        self.heading = run.participants[0].trajectory.pose_at(run.start).yaw
        self.elevation = 30.0
        self.zoom = 1.0
        self.follow_orbit, self.follow_distance = 0.0, 9.0
        self.free: Optional[FreeCamera] = None
        self.show_tracks = not args.hide_tracks
        self.show_ghosts = not args.track_dots
        self.show_help = True
        self.running = True
        self.dragging = False
        self.actors: Dict[str, Any] = {}
        self.roof: Dict[str, float] = {}
        self.camera: Any = None
        self.camera_pose: Optional[Pose] = None
        self.images: "queue.Queue[Any]" = queue.Queue()
        self.last_image: Any = None
        self.original_settings: Any = None
        self.map: Any = None
        self.screen: Any = None
        self.overlay: Any = None
        self.pygame: Any = None
        self.occupied: List[Any] = []  # per frame: screen rectangles a track label must not cover

    # -- setup / teardown -------------------------------------------------------

    def setup(self) -> None:
        import pygame

        self.pygame = pygame
        self._destroy_leftovers()
        self.map = self.world.get_map()  # client-side; only for the height of drawn track markers
        self.original_settings = self.world.get_settings()
        settings = self.world.get_settings()
        settings.synchronous_mode = True  # every frame: place actors, then render exactly that state
        settings.fixed_delta_seconds = 1.0 / float(self.args.fps)
        settings.no_rendering_mode = False
        self.world.apply_settings(settings)
        self._spawn_vehicles()
        self._spawn_camera()
        pygame.init()
        pygame.display.set_caption("CARLA replay - " + self.run.name)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # translucent ghost footprints
        pygame.key.set_repeat(300, 80)
        mono = "consolas,dejavusansmono,couriernew,monospace"
        self.font = pygame.font.SysFont(mono, 15)
        self.font_small = pygame.font.SysFont(mono, 13)
        self.font_bold = pygame.font.SysFont(mono, 15, bold=True)
        self.font_id = pygame.font.SysFont("arial,dejavusans", 26, bold=True)
        self.font_banner = pygame.font.SysFont("arial,dejavusans", 34, bold=True)

    def _destroy_leftovers(self) -> None:
        stale = [a for a in self.world.get_actors() if a.attributes.get("role_name", "").startswith(ROLE_PREFIX)]
        if stale:
            LOGGER.info("destroying %d replay actor(s) left by an earlier viewer", len(stale))
            self.client.apply_batch_sync([self.carla.command.DestroyActor(a.id) for a in stale], False)

    def _blueprint(self, name: str) -> Any:
        library = self.world.get_blueprint_library()
        try:
            return library.find(name)
        except (IndexError, RuntimeError):
            LOGGER.warning("blueprint %s not available; using vehicle.tesla.model3", name)
            return library.find("vehicle.tesla.model3")

    def _spawn_vehicles(self) -> None:
        carla = self.carla
        for index, participant in enumerate(self.run.participants):
            pid = participant.participant_id
            bp = self._blueprint(participant.blueprint)
            bp.set_attribute("role_name", ROLE_PREFIX + pid)
            if bp.has_attribute("color"):
                try:
                    bp.set_attribute("color", "{0},{1},{2}".format(*self.colors[pid]))
                except RuntimeError:
                    pass
            pose = participant.trajectory.pose_at(self.run.start)
            # Spawn well above the first pose (nothing to collide with), then
            # switch physics off and place it by transform only.
            spawn = carla.Transform(carla.Location(x=pose.x, y=pose.y, z=pose.z + 200.0 + 10.0 * index),
                                    carla.Rotation(yaw=pose.yaw))
            actor = self.world.try_spawn_actor(bp, spawn)
            if actor is None:
                raise RuntimeError("could not spawn a replay actor for " + pid)
            actor.set_simulate_physics(False)
            self.actors[pid] = actor
            box = actor.bounding_box
            self.roof[pid] = float(box.location.z + box.extent.z)
            LOGGER.info("%s: %s (%s blueprint)", pid, participant.blueprint, participant.blueprint_source)

    def _spawn_camera(self) -> None:
        bp = self.world.get_blueprint_library().find("sensor.camera.rgb")
        bp.set_attribute("image_size_x", str(self.width))
        bp.set_attribute("image_size_y", str(self.height))
        bp.set_attribute("fov", str(self.args.fov))
        bp.set_attribute("sensor_tick", "0.0")
        if bp.has_attribute("role_name"):
            bp.set_attribute("role_name", ROLE_PREFIX + "camera")
        pose = self._camera_pose(self._poses(self.clock.time))
        if self.camera_mode == "free":
            self.free = FreeCamera(pose)
        self.camera = self.world.spawn_actor(bp, self._transform(pose))
        self.camera.listen(self.images.put)

    def close(self) -> None:
        """Destroy every replay actor, restore the world settings, close pygame."""
        carla = self.carla
        if self.camera is not None:
            try:
                self.camera.stop()
            except RuntimeError as exc:
                LOGGER.warning("could not stop the replay camera: %s", exc)
        actors = list(self.actors.values()) + ([self.camera] if self.camera is not None else [])
        try:
            if actors:
                self.client.apply_batch_sync([carla.command.DestroyActor(a.id) for a in actors], False)
            if self.world.get_settings().synchronous_mode:
                self.world.tick()  # a destroy only takes effect on the next synchronous tick
        except RuntimeError as exc:
            LOGGER.warning("could not destroy the replay actors: %s", exc)
        if self.original_settings is not None:
            try:
                self.world.apply_settings(self.original_settings)
            except RuntimeError as exc:
                LOGGER.warning("could not restore the world settings: %s", exc)
        try:
            left = [a.id for a in self.world.get_actors() if a.attributes.get("role_name", "").startswith(ROLE_PREFIX)]
            if left:
                LOGGER.warning("replay actor(s) %s still in the world", left)
            else:
                LOGGER.info("replay actors destroyed")
        except RuntimeError:
            pass
        self.actors, self.camera = {}, None
        if self.pygame is not None:
            self.pygame.quit()

    # -- geometry -----------------------------------------------------------------

    def _transform(self, pose: Pose) -> Any:
        carla = self.carla
        return carla.Transform(carla.Location(x=pose.x, y=pose.y, z=pose.z),
                               carla.Rotation(pitch=pose.pitch, yaw=pose.yaw, roll=pose.roll))

    def _poses(self, t: float) -> Dict[str, Pose]:
        return {p.participant_id: p.trajectory.pose_at(self.run.start + t) for p in self.run.participants}

    def _camera_pose(self, poses: Dict[str, Pose]) -> Pose:
        if self.camera_mode == "follow":
            return follow_camera(poses[self.selected], orbit=self.follow_orbit, distance=self.follow_distance,
                                 height=0.4 * self.follow_distance)
        if self.camera_mode == "free" and self.free is not None:
            return self.free.pose
        points = [(p.x, p.y, p.z) for p in poses.values()]
        return overview_camera(points, self.heading, zoom=self.zoom, elevation=self.elevation)

    def _project(self, point: Tuple[float, float, float]) -> Optional[Tuple[int, int]]:
        uv = project(point, self.camera_pose, self.args.fov, self.width, self.height)
        if uv is None or not (-200 < uv[0] < self.width + 200 and -200 < uv[1] < self.height + 200):
            return None
        return int(uv[0]), int(uv[1])

    # -- input ----------------------------------------------------------------------

    def handle(self, event: Any) -> None:
        pg = self.pygame
        if event.type == pg.QUIT:
            self.running = False
        elif event.type == pg.KEYDOWN:
            self._on_key(event.key, event.mod)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button in (1, 3):
            if event.button == 1 and self._timeline_hit(event.pos):
                self._seek_to_pixel(event.pos[0])
            else:
                self.dragging = True
        elif event.type == pg.MOUSEBUTTONUP and event.button in (1, 3):
            self.dragging = False
        elif event.type == pg.MOUSEMOTION and self.dragging:
            dx, dy = event.rel
            if self.camera_mode == "free" and self.free is not None:
                self.free.turn(0.2 * dx, -0.2 * dy)
            elif self.camera_mode == "follow":
                self.follow_orbit += 0.3 * dx
            else:
                self.heading += 0.3 * dx
                self.elevation = max(10.0, min(85.0, self.elevation + 0.2 * dy))
        elif event.type == pg.MOUSEWHEEL:
            if self.camera_mode == "free" and self.free is not None:
                self.free.move(2.0 * event.y, 0.0, 0.0)
            elif self.camera_mode == "follow":
                self.follow_distance = max(3.0, min(60.0, self.follow_distance * (0.9 ** event.y)))
            else:
                self.zoom = max(0.2, min(8.0, self.zoom * (0.9 ** event.y)))

    def _on_key(self, key: int, mod: int) -> None:
        pg = self.pygame
        speed_keys = {pg.K_1: 0, pg.K_2: 1, pg.K_3: 2, pg.K_4: 3, pg.K_KP1: 0, pg.K_KP2: 1, pg.K_KP3: 2, pg.K_KP4: 3}
        if key == pg.K_ESCAPE:
            self.running = False
        elif key == pg.K_SPACE:
            self.clock.toggle()
        elif key == pg.K_r:
            self.clock.restart()
        elif key in (pg.K_LEFT, pg.K_RIGHT):
            step = FINE_SEEK_S if mod & pg.KMOD_SHIFT else SEEK_S
            self.clock.seek(step if key == pg.K_RIGHT else -step)
        elif key in speed_keys:
            self.clock.set_speed(SPEEDS[speed_keys[key]])
        elif key == pg.K_c:
            self.camera_mode = CAMERA_MODES[(CAMERA_MODES.index(self.camera_mode) + 1) % len(CAMERA_MODES)]
            if self.camera_mode == "free" and self.camera_pose is not None:
                self.free = FreeCamera(self.camera_pose)
        elif key == pg.K_TAB:
            step = -1 if mod & pg.KMOD_SHIFT else 1
            self.selected = self.ids[(self.ids.index(self.selected) + step) % len(self.ids)]
        elif key in (pg.K_n, pg.K_p):
            target = (self.run.next_event_time if key == pg.K_n else self.run.previous_event_time)(self.clock.time)
            if target is not None:
                self.clock.seek_to(target)
                self.clock.pause()
        elif key == pg.K_t:
            self.show_tracks = not self.show_tracks
        elif key == pg.K_g:
            self.show_ghosts = not self.show_ghosts
        elif key == pg.K_h:
            self.show_help = not self.show_help

    def _move_free_camera(self, wall_dt: float) -> None:
        if self.camera_mode != "free" or self.free is None:
            return
        pg = self.pygame
        keys = pg.key.get_pressed()
        rate = (30.0 if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT] else 10.0) * wall_dt
        forward = (keys[pg.K_w] - keys[pg.K_s]) * rate
        right = (keys[pg.K_d] - keys[pg.K_a]) * rate
        up = (keys[pg.K_e] - keys[pg.K_q]) * rate
        if forward or right or up:
            self.free.move(forward, right, up)

    # -- frame --------------------------------------------------------------------

    def run_loop(self) -> None:
        ticker = self.pygame.time.Clock()
        last = started = time.perf_counter()
        while self.running:
            now = time.perf_counter()
            wall_dt, last = min(now - last, 0.25), now
            for event in self.pygame.event.get():
                self.handle(event)
            self._move_free_camera(wall_dt)
            self.clock.advance(wall_dt)
            self.render_frame()
            ticker.tick(self.args.fps)
            if self.args.exit_after is not None and now - started >= self.args.exit_after:
                self.running = False

    def render_frame(self) -> None:
        """Place every actor at the recorded pose for the current time, render, draw overlays."""
        carla = self.carla
        t = self.clock.time
        poses = self._poses(t)
        self.camera_pose = self._camera_pose(poses)
        commands = [carla.command.ApplyTransform(self.actors[pid].id, self._transform(pose)) for pid, pose in poses.items()]
        commands.append(carla.command.ApplyTransform(self.camera.id, self._transform(self.camera_pose)))
        self.client.apply_batch_sync(commands, False)
        self.world.get_spectator().set_transform(self._transform(self.camera_pose))
        frame = self.world.tick()
        image = self._image_for(frame)
        self._draw(image, poses, t)

    def _image_for(self, frame: int) -> Any:
        deadline = time.time() + 2.0
        while time.time() < deadline:
            try:
                image = self.images.get(timeout=max(0.0, deadline - time.time()))
            except queue.Empty:
                break
            if image.frame >= frame:
                self.last_image = image
                return image
        return self.last_image

    # -- drawing ------------------------------------------------------------------

    def _draw(self, image: Any, poses: Dict[str, Pose], t: float) -> None:
        pg, screen = self.pygame, self.screen
        if image is not None:
            import numpy as np

            array = np.frombuffer(image.raw_data, dtype=np.uint8).reshape((image.height, image.width, 4))
            screen.blit(pg.surfarray.make_surface(array[:, :, 2::-1].swapaxes(0, 1)), (0, 0))
        else:
            screen.fill((20, 20, 20))
        self.occupied = []  # screen rectangles a track label must not cover
        labels = self._draw_tracks(poses, t) if self.show_tracks else []
        badges = {pid: self._draw_badge(pid, pose) for pid, pose in poses.items()}
        self._draw_side_panels(t, badges)
        self._draw_collision_banner(t)
        self._draw_hud(t)
        self._draw_timeline(t)
        for label in labels:  # last, each in free space: off the panels, the badges and each other
            label()
        pg.display.flip()

    def _panel(self, rect: Tuple[int, int, int, int], alpha: int = 170) -> None:
        panel = self.pygame.Surface((rect[2], rect[3]), self.pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))
        self.screen.blit(panel, (rect[0], rect[1]))
        self.occupied.append(self.pygame.Rect(rect))

    def _draw_badge(self, pid: str, pose: Pose) -> Any:
        """The vehicle's letter just above its roof; returns the badge rectangle (None if not visible)."""
        pg = self.pygame
        anchor = self._project((pose.x, pose.y, pose.z + self.roof.get(pid, 1.5) + LABEL_CLEARANCE_M))
        if anchor is None:
            return None
        u, v = anchor
        color = self.colors[pid]
        text = self.font_id.render(pid, True, (255, 255, 255))
        box = pg.Rect(0, 0, text.get_width() + 16, text.get_height() + 4)
        box.midbottom = (u, v - 8)
        pg.draw.polygon(self.screen, color, [(u - 7, v - 9), (u + 7, v - 9), (u, v)])
        pg.draw.rect(self.screen, color, box, border_radius=6)
        pg.draw.rect(self.screen, (255, 255, 255), box, width=2, border_radius=6)
        self.screen.blit(text, (box.x + 8, box.y + 2))
        self.occupied.append(box.inflate(4, 14))
        return box

    def _vehicle_lines(self, pid: str, t: float) -> List[Tuple[str, Tuple[int, int, int], Any]]:
        """The recorder's perceived state as the reconstruction wrote it (else its open
        START/END pairs), then the events of the last EVENT_WINDOW_S (newest first)."""
        lines = []
        perceived = self.run.perceived_lines(pid, t)
        if perceived is not None:
            for text in perceived:
                lost = text.startswith("track lost")
                alert = any(name in text for name in ("CUT_IN", "CRITICAL_TTC"))
                rgb = (150, 150, 150) if lost else (255, 150, 90) if alert else (255, 255, 255)
                lines.append((text, rgb, self.font_small))
        else:
            for state in self.run.active_states(pid, t):
                subject = self.run.subject_name(pid, state.subject)
                lines.append((state.state + (" → " + subject if subject else ""), (255, 255, 255), self.font_small))
        anonymous = self.run.anonymous_at(pid, t)
        if anonymous:
            names = ", ".join(track.name + ("" if state.measured else " (PREDICTED)") for track, state in anonymous)
            lines.append(("anonymous tracks: " + names, (200, 200, 255), self.font_small))
        for event in reversed(self.run.recent_events(pid, t, EVENT_WINDOW_S)):
            subject = self.run.subject_name(pid, event.subject)
            lines.append(("» " + event.event_type + (" → " + subject if subject else ""),
                          (255, 214, 10), self.font_bold))
        return lines

    def _draw_side_panels(self, t: float, badges: Dict[str, Any]) -> None:
        """One details panel per vehicle in a right-hand column, linked to its badge.

        A fixed column cannot overlap however close the vehicles are.
        """
        pg = self.pygame
        panels = []
        for pid in self.ids:
            speed = self.run.participant(pid).trajectory.speed_at(self.run.start + t)
            header = self.font_bold.render("{0}   {1:5.1f} m/s  {2:3.0f} km/h".format(pid, speed, speed * 3.6),
                                           True, (255, 255, 255))
            body = [font.render(text, True, rgb) for text, rgb, font in self._vehicle_lines(pid, t)]
            panels.append((pid, header, body))
        width = max(240, max(max([h.get_width()] + [b.get_width() for b in body]) for _, h, body in panels) + 18)
        x, y = self.width - width - 8, 8
        bottom = self._bottom_bar_top() - 4  # keep clear of the help lines and the timeline
        for pid, header, body in panels:
            room = max(0, (bottom - y - header.get_height() - 12) // max(1, self.font_small.get_linesize()))
            if len(body) > room:
                body = body[:max(0, room - 1)] + [self.font_small.render("...", True, (200, 200, 200))]
            height = header.get_height() + 6 + sum(b.get_height() for b in body) + (4 if body else 0)
            if y + height > bottom:
                break
            color = self.colors[pid]
            self._panel((x, y, width, height), 165)
            pg.draw.rect(self.screen, color, (x, y, width, header.get_height() + 6))
            self.screen.blit(header, (x + 8, y + 3))
            line_y = y + header.get_height() + 8
            for surface in body:
                self.screen.blit(surface, (x + 8, line_y))
                line_y += surface.get_height()
            badge = badges.get(pid)
            if badge is not None:
                start = (x, y + (header.get_height() + 6) // 2)
                pg.draw.line(self.screen, color, start, badge.midright, 2)
                pg.draw.circle(self.screen, color, start, 4)
            y += height + 6

    def _ground_z(self, x: float, y: float, near_z: float) -> float:
        """Road height under a 2-D track position, for drawing only (the tracks are planar)."""
        try:
            waypoint = self.map.get_waypoint(self.carla.Location(x=x, y=y, z=near_z), project_to_road=True)
            if waypoint is not None:
                return float(waypoint.transform.location.z)
        except RuntimeError:
            pass
        return near_z

    def _draw_tracks(self, poses: Dict[str, Pose], t: float) -> List[Any]:
        """What each recorder's radar knows at ``t``, in the recorder's colour, as the reconstruction wrote it.

        Each track is drawn from its own samples through its own observer's
        frame; tracks of different recorders are never merged, even when they
        overlap.  A track is shown only between its first and last sample (it
        disappears at its TRACK_LOST).  Returns the deferred label drawings.
        """
        ghosts, dots = [], []
        for index, recorder in enumerate(self.ids):
            observer = poses.get(recorder)
            if observer is None:
                continue
            for track in self.run.tracks.get(recorder, []):
                state = track.state_at(t)
                if state is None:
                    continue
                (ghosts if track.ghost and self.show_ghosts else dots).append((track, state, observer, index))
        size = self.run.geometry
        boxes = []
        if ghosts:
            self.overlay.fill((0, 0, 0, 0))
            for track, state, observer, index in ghosts:
                z = self._ground_z(state.centre[0], state.centre[1], observer.z)
                corners = box_corners(state.centre, state.yaw, size.length, size.width, z, size.height)
                footprint = [self._project(corner) for corner in corners[:4]]
                if all(point is not None for point in footprint):  # translucent, under every line
                    alpha = 70 if state.measured else 35
                    self.pygame.draw.polygon(self.overlay, self.colors[track.recorder] + (alpha,), footprint)
                boxes.append((track, state, corners, index))
            self.screen.blit(self.overlay, (0, 0))
        labels = [self._draw_ghost(track, state, corners, index) for track, state, corners, index in boxes]
        labels += [self._draw_track_dot(track, state, observer, index) for track, state, observer, index in dots]
        return [label for label in labels if label is not None]

    def _track_lines(self, track: TrackPath, state: TrackPoint) -> List[str]:
        """``A:track_001 / ANONYMOUS`` and ``[seen by A]`` with what the sample is (PREDICTED, heading)."""
        detail = ["[seen by {0}]".format(track.recorder)]
        if not state.measured:
            detail.append("PREDICTED")
        if state.heading == HEADING_HELD:
            detail.append("heading held")
        elif state.heading == HEADING_UNKNOWN:
            detail.append("heading unknown")
        return [track.label, "  ".join(detail)]

    def _draw_ghost(self, track: TrackPath, state: TrackPoint, corners: List[Vector], index: int) -> Any:
        """An anonymous track as a ghost: the reconstruction's nominal box where its CRITICAL_TTC model
        places the target, an arrow along the estimated motion (none while the heading is unknown),
        solid while measured, dashed while only predicted.  Returns the deferred label drawing."""
        color = self.colors[track.recorder]
        size = self.run.geometry
        dashed = not state.measured
        for i, j in BOX_EDGES:
            self._line3d(corners[i], corners[j], color, 2, dashed)
        roof = corners[4][2]
        if state.heading != HEADING_UNKNOWN:
            reach = size.length / 2.0 + 1.5
            fx, fy = rotate(reach, 0.0, state.yaw)
            tip = (state.centre[0] + fx, state.centre[1] + fy, roof)
            self._line3d((state.centre[0], state.centre[1], roof), tip, color, 3, dashed)
            for side in (-1.0, 1.0):
                bx, by = rotate(-1.0, 0.6 * side, state.yaw)
                self._line3d(tip, (tip[0] + bx, tip[1] + by, roof), color, 3, dashed)
        anchor = self._project((state.centre[0], state.centre[1], roof + 0.3))
        if anchor is None:
            return None
        lines = self._track_lines(track, state)
        return lambda: self._label(anchor, lines, color, index, above=True)

    def _draw_track_dot(self, track: TrackPath, state: TrackPoint, observer: Pose, index: int) -> Any:
        """A radar dot at the track estimate.  For a track associated with a recorder (that recorder's
        replayed vehicle: no second body), a line from the observer and ``A:track_002 → B``.
        Returns the deferred label drawing."""
        pg = self.pygame
        color = self.colors[track.recorder]
        x, y = state.position
        point = (x, y, self._ground_z(x, y, observer.z) + TRACK_DOT_HEIGHT_M)
        uv = self._project(point)
        if not track.ghost:
            self._line3d((observer.x, observer.y, observer.z + 1.0), point, color, 1)
        if uv is None:
            return None
        if state.measured:
            pg.draw.circle(self.screen, color, uv, 6)
            pg.draw.circle(self.screen, (255, 255, 255), uv, 6, width=2)
        else:
            pg.draw.circle(self.screen, color, uv, 6, width=2)  # hollow: predicted
        lines = self._track_lines(track, state) if track.ghost else [
            track.label + ("  PREDICTED" if not state.measured else "")]
        return lambda: self._label(uv, lines, color, index, above=False)

    def _free_rect(self, rect: Any) -> Any:
        """``rect`` or the nearest shift of it (rows up and down, or slid left of what it hits) that is
        inside the window and covers nothing in ``self.occupied``; ``rect`` itself when none is free."""
        window = self.pygame.Rect(0, 0, self.width, self.height)
        for rows in (0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6):
            moved = rect.move(0, rows * (rect.height + 3))
            candidates = [moved] + [moved.move(other.left - 4 - moved.right, 0)
                                    for other in self.occupied if moved.colliderect(other)]
            for candidate in candidates:
                if window.contains(candidate) and candidate.collidelist(self.occupied) < 0:
                    return candidate
        return rect

    def _label(self, anchor: Tuple[int, int], lines: List[str], color: Tuple[int, int, int], index: int,
               above: bool) -> None:
        """A small panel with a bar in the recorder's colour and a leader line to what it names: above
        a ghost box (one row per recorder, so the labels of overlapping ghosts of two recorders do not
        cover each other) or left of a dot (vehicle panels sit to the right), moved to free space."""
        pg = self.pygame
        surfaces = [self.font_small.render(text, True, (255, 255, 255)) for text in lines]
        width = max(surface.get_width() for surface in surfaces) + 13
        height = sum(surface.get_height() for surface in surfaces) + 2
        u, v = anchor
        if above:
            rect = pg.Rect(u - width // 2, v - height - 6 - index * (height + 4), width, height)
        else:
            row = index - (len(self.ids) - 1) / 2.0
            rect = pg.Rect(u - 14 - width, int(round(v - height / 2.0 + (height + 2) * row)), width, height)
        rect = self._free_rect(rect)
        end = (min(max(u, rect.left), rect.right), rect.bottom) if above \
            else (rect.right, min(max(v, rect.top), rect.bottom))
        pg.draw.line(self.screen, color, (u, v), end, 1)
        self._panel(tuple(rect), 165)
        pg.draw.rect(self.screen, color, (rect.left, rect.top, 4, rect.height))
        y = rect.top + 1
        for surface in surfaces:
            self.screen.blit(surface, (rect.left + 9, y))
            y += surface.get_height()

    def _line3d(self, a: Vector, b: Vector, color: Tuple[int, int, int], width: int = 2, dashed: bool = False) -> None:
        """A world segment, clipped at the camera's near plane and at the window."""
        segment = project_segment(a, b, self.camera_pose, self.args.fov, self.width, self.height)
        if segment is None:
            return
        clipped = self.pygame.Rect(-4, -4, self.width + 8, self.height + 8).clipline(segment[0], segment[1])
        if not clipped:
            return
        p0, p1 = clipped
        if not dashed:
            self.pygame.draw.line(self.screen, color, p0, p1, width)
            return
        length = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        if length < 1.0:
            return
        ux, uy = (p1[0] - p0[0]) / length, (p1[1] - p0[1]) / length
        start = 0.0
        while start < length:  # 9 px dashes, 7 px gaps
            end = min(start + 9.0, length)
            self.pygame.draw.line(self.screen, color, (p0[0] + ux * start, p0[1] + uy * start),
                                  (p0[0] + ux * end, p0[1] + uy * end), width)
            start += 16.0

    def _draw_collision_banner(self, t: float) -> None:
        marks = self.run.collisions_near(t, COLLISION_WINDOW_S)
        if not marks:
            return
        text = "COLLISION  " + "  ".join("–".join(mark.participants) or "?" for mark in marks)
        surface = self.font_banner.render(text, True, (255, 255, 255))
        rect = surface.get_rect(midtop=(self.width // 2, 16))
        self.pygame.draw.rect(self.screen, (200, 20, 30), rect.inflate(28, 12), border_radius=8)
        self.occupied.append(rect.inflate(28, 12))
        self.screen.blit(surface, rect)

    def _draw_hud(self, t: float) -> None:
        state = "END" if self.clock.at_end and not self.clock.playing else ("PLAYING" if self.clock.playing else "PAUSED")
        camera = self.camera_mode + ("" if self.camera_mode == "overview" else " " + self.selected)
        tracks = ("tracks: ghost boxes + dots" if self.show_ghosts else "tracks: dots") if self.show_tracks \
            else "tracks hidden"
        lines = [(self.run.name + "  (" + self.map_name + ")", self.font_bold, (255, 255, 255)),
                 (("t_global {0:+6.2f} s   replay {1:5.2f} / {2:.2f} s" if self.run.clock == "t_global" else
                   "Time  {1:6.2f} / {2:.2f} s (recorded source clock)").format(self.run.display_time(t), t,
                                                                               self.run.duration),
                  self.font, (255, 255, 255)),
                 ("Speed {0:.2f}x   {1}".format(self.clock.speed, state), self.font,
                  (120, 230, 120) if state == "PLAYING" else (255, 170, 60)),
                 ("Camera {0}   selected {1}   {2}".format(camera, self.selected, tracks),
                  self.font_small, (200, 200, 200))]
        passed = [e for e in self.events if e.time <= t + 1e-6]
        upcoming = [e for e in self.events if e.time > t + 1e-6]
        if passed:
            e = passed[-1]
            lines.append(("last {0:+6.2f} {1} {2} {3}".format(self.run.display_time(e.time), e.actor, e.event_type,
                                                          self.run.subject_name(e.actor, e.subject)).rstrip(),
                          self.font_small, (255, 214, 10)))
        if upcoming:
            e = upcoming[0]
            lines.append(("next {0:+6.2f} {1} {2} {3}".format(self.run.display_time(e.time), e.actor, e.event_type,
                                                          self.run.subject_name(e.actor, e.subject)).rstrip(),
                          self.font_small, (200, 200, 200)))
        rendered = [font.render(text, True, rgb) for text, font, rgb in lines]
        width = max(r.get_width() for r in rendered) + 16
        height = sum(r.get_height() for r in rendered) + 10
        self._panel((8, 8, width, height))
        y = 13
        for surface in rendered:
            self.screen.blit(surface, (16, y))
            y += surface.get_height()

    def _timeline_rect(self) -> Tuple[int, int, int, int]:
        return 12, self.height - 26, self.width - 24, 14

    def _timeline_hit(self, pos: Tuple[int, int]) -> bool:
        x, y, w, h = self._timeline_rect()
        return x <= pos[0] <= x + w and y - 8 <= pos[1] <= y + h + 8

    def _seek_to_pixel(self, px: int) -> None:
        x, _, w, _ = self._timeline_rect()
        self.clock.seek_to((px - x) / float(w) * self.run.duration)

    def _help_lines(self) -> List[str]:
        if not self.show_help:
            return []
        size = self.run.geometry
        return [HELP, LEGEND.format(size.length, size.width, size.height)] + (
            [FREE_HELP] if self.camera_mode == "free" else [])

    def _bottom_bar_top(self) -> int:
        """Top of the help lines and timeline at the bottom of the window."""
        return self._timeline_rect()[1] - 14 - 16 * len(self._help_lines())

    def _draw_timeline(self, t: float) -> None:
        pg = self.pygame
        x, y, w, h = self._timeline_rect()
        help_lines = self._help_lines()
        top = self._bottom_bar_top() + 4
        self._panel((0, top - 4, self.width, self.height - top + 4), 140)
        for index, text in enumerate(help_lines):
            self.screen.blit(self.font_small.render(text, True, (220, 220, 220)), (x, top + 16 * index))
        duration = max(self.run.duration, 1e-6)
        pg.draw.rect(self.screen, (70, 70, 70), (x, y, w, h), border_radius=4)
        pg.draw.rect(self.screen, (150, 150, 150), (x, y, int(w * t / duration), h), border_radius=4)
        for event in self.events:
            ex = x + int(w * event.time / duration)
            pg.draw.line(self.screen, self.colors.get(event.actor, (255, 255, 255)), (ex, y + 2), (ex, y + h - 2), 2)
        for mark in self.run.collisions:
            mx = x + int(w * mark.time / duration)
            pg.draw.line(self.screen, (230, 20, 30), (mx, y - 5), (mx, y + h + 5), 3)
        cx = x + int(w * t / duration)
        pg.draw.line(self.screen, (255, 255, 255), (cx, y - 7), (cx, y + h + 7), 2)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    run_dir = Path(args.run_dir)
    run = ReplayRun.load(run_dir)
    for note in run.notes:
        LOGGER.info("note: %s", note)
    LOGGER.info("%s: recorders %s, %.2f s, %d reconstructed event(s), anonymous tracks: %s", run.name,
                ", ".join(p.participant_id for p in run.participants), run.duration, len(run.all_events()),
                ", ".join(track.name for track in run.ghost_tracks()) or "none")

    cfg = load_run_config()  # configs/default.yaml: only the simulator connection (no scenario)
    session = session_from_config(cfg, autostart=not args.no_autostart)
    app = None
    try:
        map_name = args.map
        if not map_name:
            server_map = session.client().get_world().get_map()
            map_name = resolve_map(run, find_carla_root(cfg.get("simulation.carla_root")),
                                   map_basename(server_map.name), server_map)
            if not map_name:
                LOGGER.error("cannot recognise the map of %s from the recorded positions; pass --map", run_dir)
                return 2
        LOGGER.info("map %s (%s)", map_name, "--map" if args.map else "recognised from the recorded positions")
        world = session.world_for_map(map_name)
        app = ReplayApp(run, map_name, session.client(), world, args)
        app.setup()
        app.run_loop()
    except KeyboardInterrupt:
        LOGGER.info("interrupted")
    finally:
        if app is not None:
            app.close()
        if not args.keep_server:
            session.close()  # stops only a server this viewer started
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
