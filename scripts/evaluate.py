#!/usr/bin/env python
"""Score one recorded run against the privileged ground truth.

::

    python scripts/evaluate.py --run <run_dir>

Writes ``evaluation/metrics.json`` inside the run directory (plus the match
tables when an oracle causal graph is available to compare against) and prints
the headline numbers. Nothing is ever written back into the local or fused
artifacts: evaluation reads both sides of the boundary and owns only its own
subdirectory.

Thin wrapper around ``cdf evaluate``.
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
    """Run ``cdf evaluate`` and return its exit code."""
    return delegate("evaluate", argv)


if __name__ == "__main__":
    raise SystemExit(main())
