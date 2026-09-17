"""Shared pytest fixtures for the whole test-suite.

Three things live here because every layer of the suite needs them and because
duplicating any of them would let two tests silently disagree about what they are
testing:

* ``default_config`` -- the resolved default configuration. Loaded once per
  session: it is immutable (:class:`~cdf.common.config.Config` copies on every
  read) and parsing the YAML tree for each of a few hundred tests is pure waste.
* ``tmp_artifacts_root`` -- a per-test artifacts root, so a synthetic run is
  written to a real directory tree with the real layout and is thrown away
  afterwards.
* ``real_run`` -- the recorded CARLA run under ``artifacts/``. It is *optional*
  evidence: a fresh clone has no ``artifacts/`` directory, so tests that use it
  skip cleanly rather than fail. Nothing in the suite may *depend* on it for its
  core assertions; it is there so the anti-leakage scan can also be pointed at
  genuine simulator output.

This file also puts ``tests/`` on ``sys.path`` so that the synthetic-run builders
can be imported as ``fixtures.synthetic`` from any test module, regardless of the
directory pytest was invoked from.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent

if str(TESTS_DIR) not in sys.path:
    # Implicit namespace packages (PEP 420) make ``fixtures.synthetic``
    # importable without an ``__init__.py``; the explicit insert keeps that true
    # no matter which rootdir pytest chose.
    sys.path.insert(0, str(TESTS_DIR))

#: Path of the recorded run the suite may cross-check against, when present.
REAL_RUN_DIR = REPO_ROOT / "artifacts" / "S01_rear_end" / "seed_000_crash"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """Repository root, derived from this file's location."""
    return REPO_ROOT


@pytest.fixture(scope="session")
def src_root(repo_root: Path) -> Path:
    """The installed package source tree (``src/cdf``)."""
    path = repo_root / "src" / "cdf"
    if not path.is_dir():
        raise RuntimeError(
            "expected the package sources at {0}; the anti-leakage scan cannot "
            "run without them".format(path)
        )
    return path


@pytest.fixture(scope="session")
def default_config():
    """The resolved default configuration (``configs/default.yaml`` + profile)."""
    from cdf.common.config import load_run_config

    return load_run_config()


@pytest.fixture
def tmp_artifacts_root(tmp_path: Path) -> Path:
    """A throw-away artifacts root for one test."""
    root = tmp_path / "artifacts"
    root.mkdir(parents=True, exist_ok=True)
    return root


@pytest.fixture(scope="session")
def real_run() -> Path:
    """The recorded S01 run directory, skipping the test when it is absent."""
    if not REAL_RUN_DIR.is_dir():
        pytest.skip(
            "no recorded run at {0}; record one with "
            "scripts/run_scenario.py --scenario S01 --seed 0".format(REAL_RUN_DIR)
        )
    return REAL_RUN_DIR
