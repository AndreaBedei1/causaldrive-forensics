"""Unit tests for the counterfactual campaign driver.

No CARLA and no subprocesses: what has to be right is the driver's judgement --
whether a suite on disk is finished, and which processes it is entitled to kill.
Both matter more than they look.

*Completeness* decides whether a suite is retried or quoted. A suite whose
interpreter aborted leaves a partial contribution report behind, and treating
that as a result would publish an attribution derived from half the replays.

*Killing engines* is not tidiness. When the interpreter aborts, the teardown
never runs and the orphaned engine keeps holding the RPC port; the next
attempt's "fresh" server fails to bind and the client silently reconnects to the
orphan, so the replays share exactly the accumulated state that restarting the
simulator exists to prevent (``docs/ENVIRONMENT.md``, findings 8 and 9). The
driver must kill the *engine* image and never the launcher, which exits on its
own and whose death stops nothing.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, List, Sequence

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "run_counterfactual_campaign.py"


def _load_driver() -> Any:
    spec = importlib.util.spec_from_file_location("cdf_cf_campaign", str(SCRIPT))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


driver = _load_driver()


def _write_report(run_dir: Path, n_contributions: int) -> None:
    out = run_dir / "counterfactual"
    out.mkdir(parents=True, exist_ok=True)
    (out / "causal_contribution.json").write_text(
        json.dumps({
            "contributions": [{"action_id": "a{0}".format(i)} for i in range(n_contributions)],
            "classification": {"attribution_class": "single_initiator", "failures": []},
        }),
        encoding="utf-8",
    )


def test_a_suite_with_every_replay_is_complete(tmp_path: Path) -> None:
    _write_report(tmp_path, 4)

    state = driver.contribution_state(tmp_path, 4)

    assert state["complete"] is True
    assert state["n_contributions"] == 4
    assert state["attribution_class"] == "single_initiator"


def test_a_half_finished_suite_is_not_complete(tmp_path: Path) -> None:
    """The failure mode this guards: quoting an attribution from half the replays."""
    _write_report(tmp_path, 2)

    state = driver.contribution_state(tmp_path, 4)

    assert state["complete"] is False
    assert "expected 4" in state["reason"]


def test_a_suite_that_never_ran_is_not_complete(tmp_path: Path) -> None:
    state = driver.contribution_state(tmp_path, 4)

    assert state["complete"] is False
    assert state["n_contributions"] == 0


def test_an_unreadable_report_is_not_complete(tmp_path: Path) -> None:
    out = tmp_path / "counterfactual"
    out.mkdir(parents=True)
    (out / "causal_contribution.json").write_text("{ truncated", encoding="utf-8")

    state = driver.contribution_state(tmp_path, 4)

    assert state["complete"] is False
    assert "unreadable" in state["reason"]


def test_without_an_expected_count_any_outcome_counts(tmp_path: Path) -> None:
    """With no budget override there is no number to compare against."""
    _write_report(tmp_path, 1)

    assert driver.contribution_state(tmp_path, None)["complete"] is True
    assert driver.contribution_state(tmp_path.parent / "absent", None)["complete"] is False


def test_kill_stray_engines_targets_engines_not_the_launcher(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    listings = {
        "CarlaUE4-Win64-Shipping.exe": (
            b'"CarlaUE4-Win64-Shipping.exe","1234","Console","1","2.512.736 K"\r\n'
            b'"CarlaUE4-Win64-Shipping.exe","5678","Console","1","2.412.736 K"\r\n'
        ),
        "CarlaUE4-Linux-Shipping": (
            b"INFO: No tasks are running which match the specified criteria.\r\n"
        ),
    }
    calls: List[List[str]] = []

    def fake_check_output(cmd: Sequence[str], **_kwargs: Any) -> bytes:
        return listings[cmd[2].split("eq ", 1)[1]]

    def fake_call(cmd: Sequence[str], **_kwargs: Any) -> int:
        calls.append(list(cmd))
        return 0

    monkeypatch.setattr(driver.subprocess, "check_output", fake_check_output)
    monkeypatch.setattr(driver.subprocess, "call", fake_call)
    monkeypatch.setattr(driver.time, "sleep", lambda _s: None)

    killed = driver.kill_stray_engines()

    assert killed == 2
    assert calls == [
        ["taskkill", "/F", "/PID", "1234"],
        ["taskkill", "/F", "/PID", "5678"],
    ]
    assert "CarlaUE4.exe" not in driver.ENGINE_IMAGES


def test_kill_stray_engines_is_quiet_when_none_are_running(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        driver.subprocess, "check_output",
        lambda *a, **k: b"INFO: No tasks are running which match the specified criteria.\r\n",
    )
    calls: List[List[str]] = []
    monkeypatch.setattr(driver.subprocess, "call",
                        lambda cmd, **k: calls.append(list(cmd)) or 0)

    assert driver.kill_stray_engines() == 0
    assert calls == []
