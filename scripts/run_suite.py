#!/usr/bin/env python
"""Run many scenarios and seeds in one process.

::

    python scripts/run_suite.py --all --seeds 0 1 2 [--scenarios S01 S02]
                                [--continue-on-error]

All runs share a single :class:`cdf.simulation.carla_client.SimulatorSession`,
and the work plan is ordered by map so that the session performs as few map
switches as possible -- a suite that alternates towns pays a server restart on
every alternation, while one that finishes a town first pays exactly one.

Prints a final table of scenario, variant, seed, outcome, validation and run
directory. Exits non-zero if any run failed, unless ``--continue-on-error`` was
given.

Thin wrapper around ``cdf suite``.
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
    """Run ``cdf suite`` and return its exit code."""
    return delegate("suite", argv)


if __name__ == "__main__":
    raise SystemExit(main())
