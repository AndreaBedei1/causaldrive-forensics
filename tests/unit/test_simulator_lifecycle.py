"""Unit tests for simulator process management.

No CARLA here: the subprocess calls and the process listing are replaced with
doubles, because what has to be right is the *bookkeeping* -- which engine
processes this session owns, which it must leave alone, and whether it noticed
that a kill did not work.

This matters more than it looks. ``CarlaUE4.exe`` is a launcher that spawns
``CarlaUE4-Win64-Shipping.exe`` and exits, so terminating the handle returned by
``Popen`` leaves the engine alive holding the RPC port. Every later "fresh"
server then fails to bind and the client silently reconnects to the first one --
so runs meant to be independent quietly share accumulated state, which is
exactly the condition a counterfactual comparison must not be run under
(``docs/ENVIRONMENT.md``).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

import pytest

from cdf.simulation import carla_client


class FakeLauncher:
    """A ``Popen``-shaped double for the launcher process, already exited."""

    def __init__(self, pid: int = 4242) -> None:
        self.pid = pid
        self.terminated = False
        self.killed = False

    def poll(self) -> Optional[int]:
        return 0  # the launcher exits immediately, as the real one does

    def terminate(self) -> None:
        self.terminated = True

    def kill(self) -> None:
        self.killed = True


@pytest.fixture
def server(monkeypatch: pytest.MonkeyPatch) -> carla_client.CarlaServer:
    """A server object with no installation behind it and no sleeping."""
    monkeypatch.setattr(carla_client, "find_carla_root", lambda root=None: None)
    monkeypatch.setattr(carla_client.time, "sleep", lambda _s: None)
    return carla_client.CarlaServer(root=None, port=2000)


def _record_kills(monkeypatch: pytest.MonkeyPatch) -> List[List[str]]:
    calls: List[List[str]] = []

    def fake_call(cmd: Sequence[str], **_kwargs: Any) -> int:
        calls.append(list(cmd))
        return 0

    monkeypatch.setattr(carla_client.subprocess, "call", fake_call)
    return calls


def test_stop_kills_only_the_engines_this_session_started(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An engine a user was already running must survive our teardown."""
    calls = _record_kills(monkeypatch)
    server._process = FakeLauncher()
    server._pre_existing_pids = {111}
    server._owned_pids = {222}
    monkeypatch.setattr(server, "_server_pids", lambda: [111])

    server.stop(grace_s=0.1)

    assert [c for c in calls if "/PID" in c] == [["taskkill", "/F", "/PID", "222"]]
    assert server._owned_pids == set()


def test_stop_does_not_use_a_tree_kill(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`/T` walks the tree by parent pid, and the parent pid is recycled.

    The engine's recorded parent is the launcher, which exited long ago; Windows
    is free to give that pid to an unrelated process, and a tree kill would then
    reach whatever inherited it.
    """
    calls = _record_kills(monkeypatch)
    server._process = None
    server._owned_pids = {777}
    monkeypatch.setattr(server, "_server_pids", lambda: [])

    server.stop(grace_s=0.1)

    assert calls, "the owned engine must be killed"
    assert all("/T" not in cmd for cmd in calls)


def test_stop_reports_an_engine_that_survived(
    server: carla_client.CarlaServer,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A surviving engine is the failure this teardown exists to prevent."""
    _record_kills(monkeypatch)
    server._process = None
    server._owned_pids = {333}
    monkeypatch.setattr(server, "_server_pids", lambda: [333])  # never dies

    with caplog.at_level("ERROR", logger="cdf.simulation.carla_client"):
        server.stop(grace_s=0.1)

    assert any("survived the kill" in rec.getMessage() for rec in caplog.records), \
        caplog.text


def test_stop_without_owned_pids_touches_nothing(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A session that never started a server must not kill anybody's."""
    calls = _record_kills(monkeypatch)
    server._process = None
    server._owned_pids = set()
    monkeypatch.setattr(server, "_server_pids", lambda: [999])

    server.stop(grace_s=0.1)

    assert calls == []


def test_start_owns_only_the_engine_it_started(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The pid set is the difference between before and after, nothing else."""
    listings = [[555], [555, 666]]  # one engine already running, then ours

    def fake_pids() -> List[int]:
        return listings.pop(0) if listings else [555, 666]

    monkeypatch.setattr(server, "_server_pids", fake_pids)
    monkeypatch.setattr(carla_client.CarlaServer, "available", property(lambda _s: True))
    monkeypatch.setattr(server, "command", lambda: ["carla"])
    monkeypatch.setattr(carla_client.subprocess, "Popen",
                        lambda *a, **k: FakeLauncher())
    monkeypatch.setattr(carla_client, "connect_with_retry",
                        lambda **_k: object())

    server.start(wait_s=1.0)

    assert server._owned_pids == {666}
    assert 555 not in server._owned_pids


def test_server_pids_ignores_the_launcher_image() -> None:
    """The launcher is not the server; killing it leaves the engine running."""
    assert "CarlaUE4.exe" not in carla_client.CarlaServer._SERVER_IMAGE_NAMES
    assert "CarlaUE4-Win64-Shipping.exe" in carla_client.CarlaServer._SERVER_IMAGE_NAMES


def test_server_pids_parses_tasklist_csv(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Including the `no tasks are running` line, which is not a pid."""
    outputs: Dict[str, bytes] = {
        "CarlaUE4-Win64-Shipping.exe": (
            b'"CarlaUE4-Win64-Shipping.exe","10536","Console","1","2.512.736 K"\r\n'
        ),
        "CarlaUE4-Linux-Shipping": (
            b"INFO: No tasks are running which match the specified criteria.\r\n"
        ),
    }

    def fake_check_output(cmd: Sequence[str], **_kwargs: Any) -> bytes:
        name = cmd[2].split("eq ", 1)[1]
        return outputs[name]

    monkeypatch.setattr(carla_client.subprocess, "check_output", fake_check_output)

    assert server._server_pids() == [10536]


# ---------------------------------------------------------------------------
# Releasing the client bound to a server that is about to be replaced
# ---------------------------------------------------------------------------


class FakeServer:
    """A CarlaServer-shaped double that records its lifecycle calls."""

    available = True

    def __init__(self, events: List[str]) -> None:
        self.events = events

    def restart(self, wait_s: float = 180.0) -> object:
        self.events.append("restart")
        return object()

    def stop(self, grace_s: float = 10.0) -> None:
        self.events.append("stop")


def _session(monkeypatch: pytest.MonkeyPatch) -> carla_client.SimulatorSession:
    monkeypatch.setattr(carla_client, "find_carla_root", lambda root=None: None)
    return carla_client.SimulatorSession(autostart=False)


def test_release_client_drops_the_reference(monkeypatch: pytest.MonkeyPatch) -> None:
    session = _session(monkeypatch)
    session._client = object()

    session.release_client()

    assert session._client is None


def test_release_client_on_no_client_is_a_no_op(monkeypatch: pytest.MonkeyPatch) -> None:
    session = _session(monkeypatch)
    session._client = None

    session.release_client()  # must not raise

    assert session._client is None


def test_fresh_world_releases_before_restarting(monkeypatch: pytest.MonkeyPatch) -> None:
    """The dead server's client must be gone BEFORE the next one comes up.

    Otherwise its streaming thread keeps retrying inside this process, and
    enough of those accumulating aborts the interpreter outright.
    """
    events: List[str] = []
    session = _session(monkeypatch)
    session.server = FakeServer(events)  # type: ignore[assignment]
    session._client = object()

    seen_at_restart: Dict[str, Any] = {}

    def fake_restart(wait_s: float = 180.0) -> object:
        seen_at_restart["client"] = session._client
        events.append("restart")
        return object()

    monkeypatch.setattr(session.server, "restart", fake_restart)
    monkeypatch.setattr(session, "world_for_map", lambda name: events.append("world"))

    session.fresh_world_for_map("Town05")

    assert seen_at_restart["client"] is None, "client released before the restart"
    assert events == ["restart", "world"]
    assert session.restarts == 1


def test_close_releases_the_client_then_stops_the_server(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: List[str] = []
    session = _session(monkeypatch)
    session.server = FakeServer(events)  # type: ignore[assignment]
    session._client = object()

    session.close()

    assert session._client is None
    assert events == ["stop"]



# ---------------------------------------------------------------------------
# Was the restart real?
#
# `stop` deliberately leaves engines that were already running when this session
# started -- killing a server somebody else is using would be indefensible. That
# creates the failure this group guards: the pre-existing engine keeps the RPC
# port, the new one cannot bind it, and the client reconnects to the old one
# while every log line says the restart succeeded. A counterfactual comparison
# run under that condition is measuring accumulated state, not the intervention.
# ---------------------------------------------------------------------------


class FakeWorld:
    def __init__(self, elapsed: float) -> None:
        self._elapsed = elapsed

    def get_snapshot(self) -> Any:
        elapsed = self._elapsed

        class _Snapshot:
            timestamp = type("_T", (), {"elapsed_seconds": elapsed})()

        return _Snapshot()


class FakeClient:
    def __init__(self, elapsed: float) -> None:
        self._world = FakeWorld(elapsed)

    def get_world(self) -> FakeWorld:
        return self._world


def test_a_freshly_booted_engine_verifies(
    server: carla_client.CarlaServer,
) -> None:
    assert server._verify_fresh(FakeClient(elapsed=1.3)) is True
    assert server._verify_fresh(FakeClient(elapsed=0.0)) is True


def test_an_engine_that_has_been_running_for_hours_does_not(
    server: carla_client.CarlaServer, caplog: pytest.LogCaptureFixture
) -> None:
    """The exact failure: a stale server still holding the port."""
    with caplog.at_level("WARNING"):
        assert server._verify_fresh(FakeClient(elapsed=16_500.0)) is False
    assert "restart did not take effect" in caplog.text
    assert "pre-existing server" in caplog.text


def test_a_probe_that_cannot_read_the_clock_does_not_claim_freshness(
    server: carla_client.CarlaServer,
) -> None:
    """Unable to tell is not the same as verified, and must not be reported as it."""

    class Broken:
        def get_world(self) -> Any:
            raise RuntimeError("no connection")

    assert server._verify_fresh(Broken()) is False


def test_restart_records_whether_it_worked(
    server: carla_client.CarlaServer, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert server.last_restart_verified is None, "unknown until one is attempted"

    monkeypatch.setattr(server, "stop", lambda grace_s=10.0: None)
    monkeypatch.setattr(server, "start", lambda wait_s=180.0: FakeClient(elapsed=2.0))
    server.restart()
    assert server.last_restart_verified is True

    monkeypatch.setattr(server, "start", lambda wait_s=180.0: FakeClient(elapsed=9_000.0))
    server.restart()
    assert server.last_restart_verified is False, (
        "a restart that reconnected to a stale engine must not be recorded as fresh"
    )
