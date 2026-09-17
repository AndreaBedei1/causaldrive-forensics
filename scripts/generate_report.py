#!/usr/bin/env python
"""Aggregate every recorded run into one summary.

::

    python scripts/generate_report.py --artifacts artifacts

Walks the artifacts root, reads each run's manifest, validation, fusion,
checking and evaluation artifacts, and writes ``summary.json``, ``summary.csv``
and ``report.md`` under ``<artifacts>/report`` (or ``--out``). Every number in
the report is read from an artifact on disk; a quantity that no run produced is
reported as missing rather than filled in.

Thin wrapper around ``cdf report``.
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
    """Run ``cdf report`` and return its exit code."""
    return delegate("report", argv)


if __name__ == "__main__":
    raise SystemExit(main())
