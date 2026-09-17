"""Atomic, provenance-carrying persistence helpers.

All evidence is written through this module so that every artifact gets the same
guarantees:

* **Atomicity** -- files are written to a temporary sibling and then replaced, so
  an interrupted run never leaves a half-written evidence file behind.
* **Determinism** -- JSON is emitted with sorted keys and a fixed float
  repr, so two runs of the same seed produce byte-identical artifacts and can be
  diffed or hashed.
* **Integrity** -- :func:`write_evidence_manifest` records a SHA-256 digest of
  every persisted evidence file.
"""

from __future__ import annotations

import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Union

from .schemas import to_jsonable

__all__ = [
    "PathLike",
    "ensure_dir",
    "write_json",
    "read_json",
    "write_jsonl_gz",
    "append_jsonl_gz",
    "read_jsonl_gz",
    "JsonlGzWriter",
    "sha256_file",
    "write_evidence_manifest",
    "verify_evidence_manifest",
    "git_commit",
    "environment_block",
    "write_csv",
]

PathLike = Union[str, "os.PathLike[str]", Path]


def ensure_dir(path: PathLike) -> Path:
    """Create ``path`` (and parents) if needed and return it as a :class:`Path`."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------------------
# JSON
# ---------------------------------------------------------------------------


def write_json(path: PathLike, payload: Any, indent: int = 2) -> Path:
    """Atomically write ``payload`` as deterministic JSON.

    Dataclasses and enums are converted via
    :func:`cdf.common.schemas.to_jsonable`, so callers can hand over records
    directly.
    """
    p = Path(path)
    ensure_dir(p.parent)
    data = json.dumps(to_jsonable(payload), indent=indent, sort_keys=True, allow_nan=False)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(data)
            fh.write("\n")
        os.replace(tmp, str(p))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return p


def read_json(path: PathLike) -> Any:
    """Read a JSON document."""
    with open(str(path), "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Gzipped JSON lines
# ---------------------------------------------------------------------------


def _dumps_line(record: Any) -> str:
    return json.dumps(
        to_jsonable(record), sort_keys=True, separators=(",", ":"), allow_nan=False
    )


def write_jsonl_gz(path: PathLike, records: Iterable[Any]) -> Path:
    """Atomically write ``records`` as a gzipped JSON-lines file."""
    p = Path(path)
    ensure_dir(p.parent)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    os.close(fd)
    try:
        # mtime=0 keeps the gzip header deterministic across runs.
        with gzip.GzipFile(filename="", mode="wb", fileobj=open(tmp, "wb"), mtime=0) as gz:
            for rec in records:
                gz.write((_dumps_line(rec) + "\n").encode("utf-8"))
        os.replace(tmp, str(p))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return p


def append_jsonl_gz(path: PathLike, records: Iterable[Any]) -> Path:
    """Append ``records`` to an existing gzipped JSON-lines file (or create it).

    Gzip supports member concatenation, so this stays readable by
    :func:`read_jsonl_gz`. Used by the recorder when streaming long runs.
    """
    p = Path(path)
    ensure_dir(p.parent)
    with open(str(p), "ab") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            for rec in records:
                gz.write((_dumps_line(rec) + "\n").encode("utf-8"))
    return p


def read_jsonl_gz(path: PathLike) -> List[Dict[str, Any]]:
    """Read a gzipped JSON-lines file into a list of dicts."""
    return list(iter_jsonl_gz(path))


def iter_jsonl_gz(path: PathLike) -> Iterator[Dict[str, Any]]:
    """Stream a gzipped JSON-lines file record by record."""
    with gzip.open(str(path), "rt", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


class JsonlGzWriter:
    """Context-managed streaming writer for gzipped JSON lines.

    Keeps memory bounded for long runs: records are compressed and flushed as
    they arrive rather than accumulated. Writes to a temporary file and only
    replaces the destination on clean exit, preserving atomicity.
    """

    def __init__(self, path: PathLike) -> None:
        self.path = Path(path)
        ensure_dir(self.path.parent)
        self._tmp: Optional[str] = None
        self._raw = None  # type: Any
        self._gz = None  # type: Any
        self.count = 0

    def __enter__(self) -> "JsonlGzWriter":
        fd, self._tmp = tempfile.mkstemp(dir=str(self.path.parent), suffix=".tmp")
        os.close(fd)
        self._raw = open(self._tmp, "wb")
        self._gz = gzip.GzipFile(filename="", mode="wb", fileobj=self._raw, mtime=0)
        return self

    def write(self, record: Any) -> None:
        """Write one record."""
        if self._gz is None:
            raise RuntimeError("JsonlGzWriter used outside its context manager")
        self._gz.write((_dumps_line(record) + "\n").encode("utf-8"))
        self.count += 1

    def write_many(self, records: Iterable[Any]) -> None:
        """Write a batch of records."""
        for rec in records:
            self.write(rec)

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if self._gz is not None:
                self._gz.close()
            if self._raw is not None:
                self._raw.close()
        finally:
            if self._tmp is not None and os.path.exists(self._tmp):
                if exc_type is None:
                    os.replace(self._tmp, str(self.path))
                else:
                    os.unlink(self._tmp)
            self._gz = None
            self._raw = None
            self._tmp = None


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------


def write_csv(
    path: PathLike, rows: Sequence[Dict[str, Any]], columns: Optional[Sequence[str]] = None
) -> Path:
    """Atomically write ``rows`` as CSV with a stable column order.

    When ``columns`` is omitted the union of all keys is used, ordered by first
    appearance, so the output remains deterministic.
    """
    import csv

    p = Path(path)
    ensure_dir(p.parent)

    if columns is None:
        seen: List[str] = []
        for row in rows:
            for k in row.keys():
                if k not in seen:
                    seen.append(k)
        columns = seen

    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(columns), extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({k: _csv_cell(row.get(k)) for k in columns})
        os.replace(tmp, str(p))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
    return p


def _csv_cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(to_jsonable(value), sort_keys=True, separators=(",", ":"))
    from enum import Enum

    if isinstance(value, Enum):
        return value.value
    return value


# ---------------------------------------------------------------------------
# Integrity / provenance
# ---------------------------------------------------------------------------


def sha256_file(path: PathLike, chunk: int = 1 << 20) -> str:
    """SHA-256 hex digest of a file's contents."""
    import hashlib

    h = hashlib.sha256()
    with open(str(path), "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def verify_evidence_manifest(run_dir: PathLike) -> Dict[str, Any]:
    """Re-hash a run directory and compare it against its evidence manifest.

    A manifest nobody checks is decorative, so this is the other half of
    :func:`write_evidence_manifest`. It reports three kinds of disagreement
    separately, because they mean different things:

    ``missing``
        a file the manifest lists that is no longer on disk;
    ``changed``
        a file whose bytes differ from the recorded digest;
    ``unlisted``
        a file on disk that the manifest does not mention -- expected when
        later stages (analysis, fusion, evaluation) have added artifacts since
        the manifest was written, which is why the manifest records the stage
        it was written at.
    """
    root = Path(run_dir)
    path = root / "evidence_manifest.json"
    if not path.exists():
        return {"ok": False, "reason": "no evidence_manifest.json at {0}".format(root),
                "n_files": 0, "missing": [], "changed": [], "unlisted": []}
    manifest = read_json(path)
    listed = {e["path"]: e for e in manifest.get("files", [])}

    missing: List[str] = []
    changed: List[str] = []
    for rel, entry in sorted(listed.items()):
        target = root / rel
        if not target.is_file():
            missing.append(rel)
            continue
        if sha256_file(target) != entry.get("sha256"):
            changed.append(rel)

    on_disk = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and p.name != "evidence_manifest.json"
    }
    unlisted = sorted(on_disk - set(listed))

    return {
        "ok": not missing and not changed,
        "n_files": len(listed),
        "stage": manifest.get("stage"),
        "missing": missing,
        "changed": changed,
        "unlisted": unlisted,
    }


def write_evidence_manifest(run_dir: PathLike, extra: Optional[Dict[str, Any]] = None) -> Path:
    """Hash every artifact under ``run_dir`` and write ``evidence_manifest.json``.

    This gives the run a tamper-evident inventory, which is the forensic
    reproducibility property we want -- without inventing a distributed ledger.
    """
    root = Path(run_dir)
    entries: List[Dict[str, Any]] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.name == "evidence_manifest.json":
            continue
        entries.append(
            {
                "path": p.relative_to(root).as_posix(),
                "bytes": p.stat().st_size,
                "sha256": sha256_file(p),
            }
        )
    payload: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "run_dir": root.name,
        "n_files": len(entries),
        "files": entries,
    }
    if extra:
        payload.update(extra)
    return write_json(root / "evidence_manifest.json", payload)


def git_commit(repo_root: Optional[PathLike] = None) -> Optional[str]:
    """Current git commit SHA, or ``None`` when unavailable.

    Never raises: provenance capture must not be able to fail a run.
    """
    root = str(repo_root) if repo_root is not None else str(Path(__file__).resolve().parents[3])
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, stderr=subprocess.DEVNULL
        )
        return out.decode("utf-8").strip() or None
    except Exception:
        return None


def environment_block() -> Dict[str, Any]:
    """Versions and platform identification stamped into every run manifest."""
    import platform

    try:
        import carla  # type: ignore

        carla_version = getattr(carla, "__version__", "unknown")
    except Exception:
        carla_version = "not-installed"

    try:
        from .. import __version__ as pkg_version
    except Exception:
        pkg_version = "unknown"

    return {
        "python_version": sys.version.split()[0],
        "carla_version": carla_version,
        "platform": "{0} {1} ({2})".format(
            platform.system(), platform.release(), platform.machine()
        ),
        "package_version": pkg_version,
        "git_commit": git_commit(),
    }


def copy_tree(src: PathLike, dst: PathLike) -> Path:
    """Copy a directory tree, replacing the destination if present."""
    s, d = Path(src), Path(dst)
    if d.exists():
        shutil.rmtree(str(d))
    shutil.copytree(str(s), str(d))
    return d
