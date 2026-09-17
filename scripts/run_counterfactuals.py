#!/usr/bin/env python
"""Replay one recorded run under each candidate intervention.

::

    python scripts/run_counterfactuals.py --run <run_dir>

Every replay holds the map, the spawn state, the seed and the controller
parameters identical and changes exactly one scripted action, which is what
makes the comparison a controlled counterfactual rather than a different
experiment. The intervention set comes from the scenario's
``intervention_candidates``.

Thin wrapper around ``cdf counterfactuals``.
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
    """Run ``cdf counterfactuals`` and return its exit code."""
    return delegate("counterfactuals", argv)


if __name__ == "__main__":
    raise SystemExit(main())
