"""End-to-end smoke test against a live CARLA server.

Marked ``carla`` and skipped when no server answers on the configured host and
port, so `make test` passes on a machine without a simulator. Run it on its own
with `make test-carla`.

What it is for: everything else in the suite runs on synthetic evidence, which
proves the analysis code is right about data it was handed but says nothing
about whether this project can still *talk to* a simulator. The pieces checked
here are exactly the ones that broke during development and that no synthetic
test can cover -- the handshake, synchronous stepping at a fixed step, spawning
from a lane waypoint (spawning at a settled actor's transform fails on this
build), and a radar actually delivering frames.

It deliberately uses the project's own `ScenarioWorld` rather than raw CARLA
calls, because that context manager is what restores the world settings and
destroys the actors; a smoke test that left a server in synchronous mode would
be worse than no smoke test. It also stays on whatever map the server already
has loaded: reloading the current map kills this build (`docs/ENVIRONMENT.md`,
finding 1), and a smoke test must not be the thing that takes the server down.
"""

from __future__ import annotations

from typing import Any, List

import pytest

from cdf.common.config import load_run_config

pytestmark = pytest.mark.carla

TICKS = 20


@pytest.fixture(scope="module")
def cfg():
    return load_run_config(scenario_id="S01")


@pytest.fixture(scope="module")
def client(cfg):
    """A connected CARLA client, or a skip when none is reachable."""
    carla_client = pytest.importorskip(
        "cdf.simulation.carla_client", reason="the simulation layer is not importable")
    host = cfg.get("simulation.host", "127.0.0.1")
    port = int(cfg.get("simulation.port", 2000))
    try:
        return carla_client.connect_with_retry(
            host=host, port=port, attempts=2, retry_delay_s=1.0, probe_timeout_s=5.0)
    except Exception as exc:  # noqa: BLE001 - any failure here means "no server"
        pytest.skip("no CARLA server reachable at {0}:{1} ({2})".format(host, port, exc))


def test_client_and_server_versions_match(client) -> None:
    """A client/server version mismatch produces failures far from their cause."""
    assert client.get_client_version() == client.get_server_version()


def test_world_steps_synchronously_at_the_configured_rate(client, cfg) -> None:
    """Fixed-step synchronous mode is the premise of every recorded timestamp."""
    from cdf.simulation.world import ScenarioWorld

    current_map = client.get_world().get_map().name
    dt = float(cfg.get("simulation.fixed_delta_seconds", 0.05))

    with ScenarioWorld(client, cfg, current_map, seed=0) as world:
        assert world.delta_seconds == pytest.approx(dt, abs=1e-9)
        start_frame = world.frame
        start_t = world.elapsed_seconds
        for _ in range(TICKS):
            world.tick()
        assert world.frame - start_frame == TICKS, "a tick did not advance one frame"
        assert world.elapsed_seconds - start_t == pytest.approx(TICKS * dt, abs=1e-6)

    # The world must be handed back as it was found, or the next process
    # inherits synchronous mode from us and hangs waiting for ticks nobody sends.
    assert client.get_world().get_settings().synchronous_mode is False


def test_a_vehicle_and_its_radar_produce_evidence(client, cfg) -> None:
    """Spawn from a lane waypoint, step, and require real radar frames."""
    from cdf.simulation.carla_client import import_carla
    from cdf.simulation.world import ScenarioWorld

    current_map = client.get_world().get_map().name
    frames: List[Any] = []

    with ScenarioWorld(client, cfg, current_map, seed=0) as world:
        spawn_points = world.spawn_points()
        assert spawn_points, "the loaded map exposes no spawn points"

        vehicle = world.spawn_vehicle("vehicle.tesla.model3", spawn_points[0])
        assert vehicle is not None, "the vehicle could not be spawned"

        carla = import_carla()
        radar = world.spawn_sensor(
            "sensor.other.radar",
            carla.Transform(carla.Location(x=2.2, z=0.8)),
            vehicle,
            attributes={"horizontal_fov": "30", "vertical_fov": "10", "range": "80"},
        )
        radar.listen(frames.append)

        world.warmup()
        for _ in range(TICKS):
            world.tick()
        radar.stop()

    assert frames, "the radar delivered no frames over {0} ticks".format(TICKS)
    # One frame per tick is the property synchronous mode is supposed to give.
    assert len(frames) >= TICKS // 2, "only {0} radar frame(s) over {1} ticks".format(
        len(frames), TICKS)


def test_the_smoke_test_leaves_no_actors_behind(client) -> None:
    """A leaked vehicle changes the next run's scene, silently."""
    remaining = [a for a in client.get_world().get_actors()
                 if a.type_id.startswith(("vehicle.", "sensor."))]
    assert not remaining, "actors left in the world: {0}".format(
        [a.type_id for a in remaining])
