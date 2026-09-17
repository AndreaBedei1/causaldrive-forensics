#!/usr/bin/env python
"""Record one scenario run and analyse it end to end.

::

    python scripts/run_scenario.py --scenario S01 [--seed 0] [--variant crash]
                                   [--no-analyse] [--no-fuse]

Runs the scenario and then, by default, local analysis, fusion, the oracle graph
build, model checking and the viewer bundle, printing a concise summary of what
was produced and whether the scenario's own validation passed.

The map is selected through :class:`cdf.simulation.carla_client.SimulatorSession`
before the run starts, because the tested 0.9.15 build only tolerates one
dependable map switch per server process and the session is what knows when a
restart is needed.

Exits non-zero when scenario validation fails.

Thin wrapper around ``cdf run``.
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
    """Run ``cdf run`` and return its exit code."""
    return delegate("run", argv)


if __name__ == "__main__":
    raise SystemExit(main())
