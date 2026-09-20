"""Every relative link and inline path in the documentation has to resolve.

A forensics project's documentation makes one promise above the others: that
every number can be traced to the file it was read from. A link that no longer
resolves breaks that promise quietly, and it happens most often exactly when the
underlying evidence has been regenerated, renamed or archived -- the moment when
the reader is most likely to follow it.

Paths written as inline code are navigational too, and go stale in the same way,
so they are checked as well.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
#: Paths written as `docs/FOO.md` rather than as a link. The prefixes are the
#: directories the documentation actually navigates to.
INLINE_PATH = re.compile(
    r"`((?:docs|legacy|results|scripts|configs|src|tests)/[\w./-]+\.\w+)`"
)


def _markdown_files():
    out = subprocess.check_output(
        ["git", "ls-files", "*.md"], cwd=str(REPO_ROOT), universal_newlines=True
    )
    return sorted(line for line in out.split() if line)


MARKDOWN = _markdown_files()


@pytest.mark.parametrize("relative", MARKDOWN)
def test_every_documentation_reference_resolves(relative: str) -> None:
    path = REPO_ROOT / relative
    text = path.read_text(encoding="utf-8")
    base = path.parent
    broken = []

    for target in LINK.findall(text):
        target = target.split()[0].strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#")[0]
        if not target:
            continue
        if not (base / target).resolve().exists():
            broken.append(("link", target))

    for target in INLINE_PATH.findall(text):
        if not (REPO_ROOT / target).exists():
            broken.append(("inline path", target))

    assert broken == [], "{0} refers to {1}".format(
        relative, ", ".join("{0} {1}".format(kind, t) for kind, t in broken)
    )


def test_the_documentation_is_actually_being_checked() -> None:
    """A glob that matched nothing would make every case above vacuous."""
    assert len(MARKDOWN) > 20, MARKDOWN
    assert "README.md" in MARKDOWN
