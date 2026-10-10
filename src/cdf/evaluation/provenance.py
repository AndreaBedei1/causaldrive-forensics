"""Provenance of evaluation aggregates: code version, configuration hash, inputs, time.

Every aggregate written for the paper carries one ``provenance`` record so that a number can be traced
back to the code, the configuration, the raw runs, the perturbation profile and the seed it came from.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence

ROOT = Path(__file__).resolve().parents[3]


def _git(*args: str) -> Optional[str]:
    try:
        out = subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def config_hash(config: Mapping[str, Any]) -> str:
    """SHA-256 of the configuration as canonical JSON (sorted keys)."""
    return hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def code_hash() -> str:
    """SHA-256 over the source code (``src/cdf/**/*.py``) and ``configs/*.yaml``, path and content: identifies
    the code version even before it is committed (an output committed with its code cannot name that
    commit)."""
    digest = hashlib.sha256()
    files = sorted(list((ROOT / "src" / "cdf").rglob("*.py")) + list((ROOT / "configs").glob("*.yaml")))
    for path in files:
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return digest.hexdigest()


def provenance(config: Optional[Mapping[str, Any]] = None, runs: Sequence[str] = (),
               perturbation: Optional[str] = None, seed: Optional[int] = None,
               extra: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    """The provenance record of an aggregate."""
    status = _git("status", "--porcelain", "--untracked-files=no")
    record: Dict[str, Any] = {
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else bool(status),
        "code_sha256": code_hash(),
        "config_sha256": None if config is None else config_hash(config),
        "runs": list(runs),
        "perturbation_profile": perturbation,
        "seed": seed,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": sys.version.split()[0],
    }
    if extra:
        record.update(extra)
    return record
