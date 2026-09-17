"""Shared bootstrap for the ``scripts/`` wrappers.

Every script in this directory is a two-line alias for one ``cdf`` subcommand.
They exist so the README can document a command that works immediately after a
clone -- before ``pip install -e .`` has been run -- which is also why this
module puts the repository's ``src/`` on ``sys.path`` when (and only when) the
package is not already importable. An installed package always wins, so a script
never shadows the environment the user deliberately set up.

The scripts import this module by path rather than as ``cdf.*`` for the obvious
reason: at that point ``cdf`` may not be importable yet.
"""

from __future__ import annotations

import os
import sys
from typing import List, Optional, Sequence

__all__ = ["ensure_package_importable", "delegate"]


def ensure_package_importable() -> None:
    """Make ``import cdf`` work, falling back to the repository's ``src/``."""
    try:
        # A probe, not a use: if the package is already importable there is
        # nothing to do. pyflakes reports it as an unused import; it is not.
        import cdf  # noqa: F401  (import for effect)

        return
    except ImportError:
        pass
    src = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "src")
    )
    if not os.path.isdir(src):
        raise SystemExit(
            "cannot import the cdf package and no src/ directory next to "
            "scripts/ ({0}); install the package with `pip install -e .`".format(src)
        )
    sys.path.insert(0, src)


def delegate(command: str, argv: Optional[Sequence[str]] = None) -> int:
    """Run ``cdf <command>`` with ``argv`` and return its exit code."""
    ensure_package_importable()
    from cdf.cli import main as cli_main

    args: List[str] = list(sys.argv[1:] if argv is None else argv)
    return int(cli_main([command] + args))
