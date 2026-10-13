"""pytest: this checkout's ``src`` comes first, whatever other checkout of the project is pip-installed (an
editable install of another worktree would otherwise answer ``import cdf``)."""
import sys
from pathlib import Path

SRC = str(Path(__file__).resolve().parent / "src")
if SRC in sys.path:
    sys.path.remove(SRC)
sys.path.insert(0, SRC)
