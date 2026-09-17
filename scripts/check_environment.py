#!/usr/bin/env python
"""Inspect the Python and CARLA environment.

::

    python scripts/check_environment.py [--start-server]

Reports the interpreter, the package version, every dependency and its version,
whether the ``carla`` module imports, whether a server is reachable and on which
map, the detected CARLA root, the CPU count and the free disk space.

Exits non-zero when a *required* piece is missing. A missing simulator is a
warning rather than a failure on purpose: recording new runs needs CARLA, but
analysis, fusion, model checking, evaluation and reporting all work on
already-recorded artifacts, and a machine that can only do the second half is a
perfectly useful machine.

Thin wrapper around ``cdf env``.
"""

from __future__ import annotations

import os
import sys
from typing import Optional, Sequence

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from _bootstrap import delegate  # noqa: E402  (needs the sys.path entry above)

__all__ = ["main"]


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run ``cdf env`` and return its exit code."""
    return delegate("env", argv)


if __name__ == "__main__":
    raise SystemExit(main())
