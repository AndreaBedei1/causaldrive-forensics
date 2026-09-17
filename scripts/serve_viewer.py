#!/usr/bin/env python
"""Serve one run's forensic viewer locally.

::

    python scripts/serve_viewer.py --run <run_dir> [--port 8000] [--no-browser]

Copies ``viewer/index.html``, ``viewer/app.js`` and ``viewer/styles.css`` next to
the run's ``viewer/run_data.json`` and serves that directory with
:mod:`http.server`, printing the exact URL.

The server binds ``127.0.0.1`` only, never ``0.0.0.0``: a run directory holds a
complete reconstruction of an incident, including every participant's own
telemetry, and it has no business being reachable from the network.

Thin wrapper around ``cdf viewer``.
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
    """Run ``cdf viewer`` and return its exit code."""
    return delegate("viewer", argv)


if __name__ == "__main__":
    raise SystemExit(main())
