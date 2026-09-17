"""Unit tests for the external-only CARLA spectator view."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, List, Optional, Tuple

import pytest

from cdf import cli
from cdf.simulation import live_view
from cdf.simulation import runner


class FakeLocation:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x, self.y, self.z = x, y, z


class FakeRotation:
    def __init__(self, pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0) -> None:
        self.pitch, self.yaw, self.roll = pitch, yaw, roll


class FakeTransform:
    def __init__(self, location: FakeLocation, rotation: FakeRotation) -> None:
        self.location, self.rotation = location, rotation


class FakeColor:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.r, self.g, self.b = red, green, blue


class FakeCarla:
    Location = FakeLocation
    Rotation = FakeRotation
    Transform = FakeTransform
    Color = FakeColor


class FakeVehicle:
    def __init__(self, x: float, y: float, z: float = 0.0, yaw: float = 0.0) -> None:
        self.transform = FakeTransform(FakeLocation(x, y, z), FakeRotation(yaw=yaw))

    def get_transform(self) -> FakeTransform:
        return self.transform

    def get_forward_vector(self) -> SimpleNamespace:
        import math

        yaw = self.transform.rotation.yaw * math.pi / 180.0
        return SimpleNamespace(x=math.cos(yaw), y=math.sin(yaw), z=0.0)


class FakeSpectator:
    def __init__(self) -> None:
        self.transform: Any = None

    def set_transform(self, transform: FakeTransform) -> None:
        self.transform = transform


class FakeDebug:
    def __init__(self) -> None:
        self.calls: List[Any] = []

    def draw_string(self, location: FakeLocation, text: str, **kwargs: Any) -> None:
        self.calls.append((location, text, kwargs))


class FakeWorld:
    def __init__(self, no_rendering_mode: bool = False) -> None:
        self.spectator = FakeSpectator()
        self.debug = FakeDebug()
        self.settings = SimpleNamespace(no_rendering_mode=no_rendering_mode)
        self.get_spectator_calls = 0

    def get_settings(self) -> Any:
        return self.settings

    def get_spectator(self) -> FakeSpectator:
        self.get_spectator_calls += 1
        return self.spectator


def make_view(
    monkeypatch: pytest.MonkeyPatch,
    vehicles: Dict[str, FakeVehicle],
    options: Optional[live_view.LiveViewOptions] = None,
    world: Optional[FakeWorld] = None,
) -> Tuple[live_view.LiveScenarioView, FakeWorld]:
    monkeypatch.setattr(live_view, "import_carla", lambda: FakeCarla)
    fake_world = world or FakeWorld()
    return live_view.LiveScenarioView(fake_world, vehicles, options), fake_world


def test_vehicle_center_supports_two_and_three_vehicles() -> None:
    assert live_view.vehicle_center([(0.0, 2.0, 1.0), (4.0, 4.0, 3.0)]) == (2.0, 3.0, 2.0)
    assert live_view.vehicle_center(
        [(0.0, 0.0, 0.0), (3.0, 6.0, 3.0), (6.0, 3.0, 6.0)]
    ) == (3.0, 3.0, 3.0)


def test_overhead_view_centers_all_participants_and_smooths(monkeypatch: pytest.MonkeyPatch) -> None:
    vehicles = {"A": FakeVehicle(0.0, 0.0), "B": FakeVehicle(10.0, 0.0)}
    view, world = make_view(
        monkeypatch,
        vehicles,
        live_view.LiveViewOptions(smoothing=0.5),
    )
    assert view.update(0.05)
    first = world.spectator.transform
    assert first.location.x < 5.0
    assert first.location.z > 0.0
    assert first.rotation.pitch < 0.0

    vehicles["A"].transform.location.x = 20.0
    assert view.update(0.10)
    second = world.spectator.transform
    assert first.location.x < second.location.x < 20.0


def test_follow_view_uses_chase_transform(monkeypatch: pytest.MonkeyPatch) -> None:
    view, world = make_view(
        monkeypatch,
        {"A": FakeVehicle(10.0, 4.0, yaw=0.0)},
        live_view.LiveViewOptions(mode="follow", follow_vehicle="A"),
    )
    assert view.update(0.05)
    transform = world.spectator.transform
    assert transform.location.x < 10.0
    assert transform.location.z > 0.0
    assert transform.rotation.pitch < 0.0


def test_labels_use_ids_short_lifetime_and_optional_colors(monkeypatch: pytest.MonkeyPatch) -> None:
    view, world = make_view(
        monkeypatch,
        {"A": FakeVehicle(0.0, 0.0), "B": FakeVehicle(2.0, 0.0), "C": FakeVehicle(4.0, 0.0)},
    )
    assert view.update(0.05)
    assert [call[1] for call in world.debug.calls] == ["A", "B", "C"]
    assert all(call[2]["persistent_lines"] is False for call in world.debug.calls)
    assert all(call[2]["life_time"] == pytest.approx(0.15) for call in world.debug.calls)
    assert world.debug.calls[0][2]["color"].r == 255

    world.debug.calls.clear()
    view, world = make_view(
        monkeypatch,
        {"A": FakeVehicle(0.0, 0.0)},
        live_view.LiveViewOptions(show_labels=False),
    )
    assert view.update(0.05)
    assert world.debug.calls == []


def test_no_rendering_mode_does_not_access_or_fail_on_spectator(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    world = FakeWorld(no_rendering_mode=True)
    view, _ = make_view(monkeypatch, {"A": FakeVehicle(0.0, 0.0)}, world=world)
    assert not view.available
    assert not view.update(0.05)
    assert world.get_spectator_calls == 0


def test_realtime_pacer_sleeps_only_when_ahead_of_schedule() -> None:
    now = [100.0]
    slept: List[float] = []

    def clock() -> float:
        return now[0]

    def sleep(seconds: float) -> None:
        slept.append(seconds)
        now[0] += seconds

    pacer = live_view.RealtimePacer(0.5, clock=clock, sleep=sleep)
    pacer.start(0.0)
    now[0] = 100.1
    assert pacer.pace(0.1) == pytest.approx(0.1)
    assert slept == [pytest.approx(0.1)]

    now[0] = 100.5
    assert pacer.pace(0.2) == 0.0
    assert len(slept) == 1


def test_cli_parses_live_options() -> None:
    args = cli.build_parser().parse_args(
        [
            "run",
            "--scenario",
            "S02",
            "--live",
            "--realtime",
            "--playback-speed",
            "0.5",
            "--spectator",
            "follow",
            "--follow-vehicle",
            "A",
            "--spectator-height",
            "24",
            "--no-labels",
        ]
    )
    assert args.live is True
    assert args.realtime is True
    assert args.playback_speed == pytest.approx(0.5)
    assert args.spectator == "follow"
    assert args.follow_vehicle == "A"
    assert args.spectator_height == pytest.approx(24.0)
    assert args.no_labels is True


def test_cli_rejects_non_positive_playback_speed() -> None:
    assert cli.main(["run", "--scenario", "S01", "--playback-speed", "0"]) == cli.EXIT_USAGE


def test_disabled_live_view_does_not_touch_spectator() -> None:
    assert (
        runner._maybe_live_view(
            SimpleNamespace(world=SimpleNamespace(get_spectator=lambda: (_ for _ in ()).throw(AssertionError()))),
            [],
            live=False,
            realtime=False,
            playback_speed=1.0,
            spectator_mode="overhead",
            follow_vehicle="A",
            spectator_height=35.0,
            show_labels=True,
        )
        is None
    )


def test_live_options_reject_non_positive_values() -> None:
    with pytest.raises(ValueError, match="playback speed"):
        live_view.LiveViewOptions(playback_speed=0.0)
    with pytest.raises(ValueError, match="spectator height"):
        live_view.LiveViewOptions(spectator_height=0.0)
