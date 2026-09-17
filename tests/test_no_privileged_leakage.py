"""Automated enforcement of the data boundary.

This is the most important test module in the project. Every scientific claim the
pipeline makes rests on one premise: a participant's local reconstruction, and
the fusion of several of them, were produced *without* privileged knowledge --
no CARLA actor ids, no true pose of another vehicle, no map topology, no signal
phase, no scenario role label, no oracle artifact. A reader has to be able to
verify that premise mechanically rather than take it on trust.

The module therefore attacks the premise from six independent directions, so that
a leak has to defeat all of them at once:

1. **Static import isolation.** Every module under ``cdf.local``, ``cdf.fusion``,
   ``cdf.graph`` and ``cdf.checking`` is parsed with :mod:`ast` and its imports
   are *resolved*, relative ones included. A grep for ``"cdf.oracle"`` would be
   fooled by ``from ..oracle import x``; resolving the level against the module's
   own package is not.
2. **Runtime import isolation.** The same claim is re-checked in a fresh
   interpreter, because a dynamic ``importlib`` call has no import statement for
   the AST pass to find.
3. **Forbidden simulator calls.** The privileged CARLA queries
   (``get_map``, ``get_waypoint``, ``get_traffic_light`` ...) may not appear in
   those packages in any form -- attribute access, bare name, or a string handed
   to :func:`getattr`.
4. **Structural impossibility.** No dataclass a participant persists has a field
   in which a privileged quantity could be stored.
5. **Artifact scanning.** A complete run is built, analysed and fused, and every
   persisted key -- at any nesting depth, in JSON, gzipped JSON-lines and GraphML
   alike -- is checked against the registries in
   :mod:`cdf.common.schemas`. The recorded CARLA run under ``artifacts/`` is
   scanned the same way when it is present.
6. **Discrimination.** The same scanner is pointed at the ``oracle/`` subtree,
   which *must* fail it. A scan that passes everywhere proves nothing; this test
   is what shows the scan can actually see a leak.

A failure here is never cosmetic. It means a published number may have been
computed with information the vehicle did not have.
"""

from __future__ import annotations

import ast
import dataclasses
import gzip
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator, List, Optional, Sequence, Set, Tuple

import pytest

from cdf.common.layout import RunLayout
from cdf.common.schemas import (
    FORBIDDEN_LOCAL_FIELD_NAMES,
    FORBIDDEN_LOCAL_FIELD_SUBSTRINGS,
    ORACLE_ONLY_EVENT_TYPES,
    ControlSample,
    Event,
    EventType,
    GraphDocument,
    LocalTriggerRecord,
    Provenance,
    RadarDetection,
    RadarFrame,
    TelemetrySample,
    TrackSample,
)
from cdf.fusion.pipeline import fuse_run
from cdf.graph.export import load_graph, save_graph
from cdf.local.pipeline import analyse_run

from fixtures.synthetic import synthetic_partial_view

# ---------------------------------------------------------------------------
# What may never appear where
# ---------------------------------------------------------------------------

#: Packages that perform inference and therefore live on the unprivileged side.
INFERENCE_PACKAGES: Tuple[str, ...] = ("local", "fusion", "graph", "checking")

#: Module roots those packages may not reach, directly or relatively.
FORBIDDEN_IMPORT_ROOTS: Tuple[str, ...] = ("carla", "cdf.oracle", "cdf.simulation")

#: Privileged simulator queries. Each one answers a question an onboard sensor
#: cannot: who else exists, what the road looks like, what the signal says.
FORBIDDEN_CALL_NAMES: Tuple[str, ...] = (
    "get_actors",
    "get_map",
    "get_waypoint",
    "get_traffic_light",
    "get_spectator",
    "generate_waypoints",
    "get_snapshot",
)

#: Camera sensing is out of scope for the whole project: the evidence model is
#: radar plus own telemetry, and a camera would quietly reintroduce the ability
#: to identify another vehicle.
CAMERA_PATTERNS: Tuple[str, ...] = (
    r"sensor\.camera",
    r"semantic_segmentation",
    r"depth_camera",
    r"optical_flow",
    r"\brgb\b",
)

#: Dataclasses a participant persists. None of them may be able to *hold* a
#: privileged quantity, whatever the code around them does.
LOCAL_RECORD_TYPES = (
    TelemetrySample,
    ControlSample,
    RadarDetection,
    RadarFrame,
    TrackSample,
    LocalTriggerRecord,
    Event,
)

#: Key names that would identify the other party to a collision. The local
#: collision record is allowed to say "something hit me this hard at this time"
#: and nothing more.
COUNTERPARTY_KEY_PATTERN = re.compile(
    r"other|partner|counterpart|opponent|collided_with|struck_by", re.IGNORECASE
)

#: Keys whose value names a participant. Inside ``vehicle_X/`` every one of them
#: must say ``X``: a local artifact that names another participant has, by
#: definition, resolved an identity the vehicle could not resolve alone.
PARTICIPANT_VALUED_KEYS: Tuple[str, ...] = ("participant_id", "owner", "owners")


# ---------------------------------------------------------------------------
# Static analysis helpers
# ---------------------------------------------------------------------------


def _iter_modules(src_root: Path, packages: Sequence[str]) -> Iterator[Tuple[Path, str, bool]]:
    """Yield ``(path, dotted_module_name, is_package)`` for the given packages."""
    for package in packages:
        pkg_dir = src_root / package
        if not pkg_dir.is_dir():
            raise AssertionError(
                "expected an inference package at {0}; the boundary test cannot "
                "vouch for code it cannot find".format(pkg_dir)
            )
        for path in sorted(pkg_dir.rglob("*.py")):
            rel = path.relative_to(src_root.parent)
            parts = list(rel.with_suffix("").parts)
            is_package = parts[-1] == "__init__"
            if is_package:
                parts = parts[:-1]
            yield (path, ".".join(parts), is_package)


def _resolve_relative(module_name: str, is_package: bool, level: int, module: Optional[str]) -> str:
    """Resolve a relative import to its absolute dotted name.

    ``level`` is the number of leading dots. Level 1 is relative to the module's
    own package; each further dot strips one more component. This mirrors
    :pep:`328` and is the reason the test cannot be fooled by ``from ..oracle
    import x``.
    """
    package = module_name if is_package else module_name.rsplit(".", 1)[0]
    parts = package.split(".") if package else []
    keep = len(parts) - (level - 1)
    if keep < 0:
        raise AssertionError(
            "relative import of level {0} escapes the package tree in {1}".format(
                level, module_name
            )
        )
    base = parts[:keep]
    if module:
        base = base + module.split(".")
    return ".".join(base)


def _imported_targets(tree: ast.AST, module_name: str, is_package: bool) -> Set[str]:
    """Every absolute module name a source file imports.

    Both the module and the individual names imported from it are reported
    (``from cdf import oracle`` imports ``cdf.oracle``), so a leak cannot hide in
    the ``from`` clause.
    """
    out: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = _resolve_relative(module_name, is_package, node.level, node.module)
            else:
                base = node.module or ""
            if base:
                out.add(base)
                for alias in node.names:
                    out.add("{0}.{1}".format(base, alias.name))
    return out


def _is_forbidden_import(target: str) -> bool:
    return any(
        target == root or target.startswith(root + ".") for root in FORBIDDEN_IMPORT_ROOTS
    )


def _forbidden_call_sites(tree: ast.AST) -> List[str]:
    """Occurrences of a privileged simulator query in a parsed source file."""
    found: List[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_CALL_NAMES:
            found.append("attribute {0} at line {1}".format(node.attr, node.lineno))
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_CALL_NAMES:
            found.append("name {0} at line {1}".format(node.id, node.lineno))
        elif isinstance(node, ast.Call):
            func = node.func
            is_getattr = isinstance(func, ast.Name) and func.id == "getattr"
            if not is_getattr:
                continue
            for arg in node.args[1:2]:
                value = getattr(arg, "value", None)
                if isinstance(value, str) and value in FORBIDDEN_CALL_NAMES:
                    found.append(
                        "getattr({0!r}) at line {1}".format(value, node.lineno)
                    )
    return found


# ---------------------------------------------------------------------------
# Artifact scanning helpers
# ---------------------------------------------------------------------------


def _load_artifact(path: Path) -> Any:
    """Read a JSON or gzipped JSON-lines artifact into plain Python data."""
    if path.name.endswith(".jsonl.gz"):
        with gzip.open(str(path), "rt", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]
    with open(str(path), "r", encoding="utf-8") as handle:
        return json.load(handle)


def _walk_keys(node: Any, path: str = "$") -> Iterator[Tuple[str, str]]:
    """Yield ``(key, json_path)`` for every mapping key at any depth."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield (str(key), path)
            for item in _walk_keys(value, "{0}.{1}".format(path, key)):
                yield item
    elif isinstance(node, list):
        for index, value in enumerate(node):
            for item in _walk_keys(value, "{0}[{1}]".format(path, index)):
                yield item


def _walk_strings(node: Any) -> Iterator[str]:
    """Yield every string value at any depth."""
    if isinstance(node, dict):
        for value in node.values():
            for item in _walk_strings(value):
                yield item
    elif isinstance(node, list):
        for value in node:
            for item in _walk_strings(value):
                yield item
    elif isinstance(node, str):
        yield node


def _key_violations(key: str, where: str) -> List[str]:
    """Registry violations for one key name."""
    low = key.lower()
    out: List[str] = []
    if low in FORBIDDEN_LOCAL_FIELD_NAMES:
        out.append("forbidden field name {0!r} at {1}".format(key, where))
    for substring in FORBIDDEN_LOCAL_FIELD_SUBSTRINGS:
        if substring in low:
            out.append(
                "key {0!r} contains forbidden substring {1!r} at {2}".format(
                    key, substring, where
                )
            )
    return out


def scan_tree_for_privileged_keys(root: Path) -> List[str]:
    """Every privileged key found under ``root``.

    Covers ``*.json``, ``*.jsonl.gz`` and the attribute names of ``*.graphml``,
    recursively. Returns the violations rather than asserting, because the same
    scanner has to be *expected to pass* on a local subtree and *expected to
    fail* on the oracle one.
    """
    violations: List[str] = []
    graphml_attr = re.compile(r'attr\.name="([^"]+)"')

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".json") or path.name.endswith(".jsonl.gz"):
            data = _load_artifact(path)
            for key, where in _walk_keys(data):
                violations.extend(_key_violations(key, "{0}:{1}".format(path.name, where)))
        elif path.suffix == ".graphml":
            text = path.read_text(encoding="utf-8")
            for key in sorted(set(graphml_attr.findall(text))):
                violations.extend(
                    _key_violations(key, "{0}:<graphml attribute>".format(path.name))
                )
    return violations


def scan_tree_for_oracle_event_types(root: Path) -> List[str]:
    """Occurrences of an oracle-only event type in any artifact under ``root``."""
    forbidden = tuple(t.value for t in ORACLE_ONLY_EVENT_TYPES)
    violations: List[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name.endswith(".json") or path.name.endswith(".jsonl.gz"):
            for text in _walk_strings(_load_artifact(path)):
                for value in forbidden:
                    if value in text:
                        violations.append(
                            "oracle-only event type {0!r} in {1}".format(value, path.name)
                        )
        elif path.suffix == ".graphml":
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                if value in text:
                    violations.append(
                        "oracle-only event type {0!r} in {1}".format(value, path.name)
                    )
    return violations


def local_and_fused_dirs(run_dir: Path) -> List[Path]:
    """The subtrees that must contain no privileged data.

    ``vehicle_*`` (each ego's own reconstruction), ``fusion`` (the merge of
    those reconstructions) and ``checking`` (finite-trace monitoring, which runs
    on local evidence only -- the privileged properties are evaluated by
    ``TraceChecker.check_oracle`` and persisted under ``oracle/``).

    Deliberately excluded: ``oracle/`` is the privileged layer itself,
    ``evaluation/`` is the scoring layer and is *allowed* to consult the oracle,
    and ``viewer/`` carries the badged oracle view for human inspection. Those
    three are not oversights; the oracle subtree is separately asserted to
    *contain* the privileged fields, so this scan cannot pass by scanning
    nothing.
    """
    out = [p for p in sorted(run_dir.glob("vehicle_*")) if p.is_dir()]
    for name in ("fusion", "checking"):
        subtree = run_dir / name
        if subtree.is_dir():
            out.append(subtree)
    if not out:
        raise AssertionError(
            "no local or fused artifacts under {0}; the scan would pass "
            "vacuously".format(run_dir)
        )
    return out


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def analysed_run(tmp_path_factory, default_config) -> RunLayout:
    """A synthetic three-vehicle run, analysed and fused for real.

    The partial-view scene is used deliberately: it is the one with three
    participants, two observers holding tracks and a resolved identity chain
    (A sees B, B sees C), so the fusion artifacts it produces are the richest the
    scan can be pointed at.
    """
    root = tmp_path_factory.mktemp("leakage_artifacts")
    layout = synthetic_partial_view(root, seed=0, cfg=default_config)
    analyse_run(layout.root, default_config)
    fuse_run(layout.root, default_config)
    return layout


# ---------------------------------------------------------------------------
# 1. Static import isolation
# ---------------------------------------------------------------------------


def test_inference_packages_never_import_privileged_modules(src_root: Path) -> None:
    """No inference module may import carla, cdf.oracle or cdf.simulation."""
    offences: List[str] = []
    n_modules = 0
    for path, module_name, is_package in _iter_modules(src_root, INFERENCE_PACKAGES):
        n_modules += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for target in sorted(_imported_targets(tree, module_name, is_package)):
            if _is_forbidden_import(target):
                offences.append("{0} imports {1}".format(module_name, target))

    assert n_modules >= len(INFERENCE_PACKAGES), (
        "only {0} inference modules were scanned; the scan is not covering the "
        "package tree".format(n_modules)
    )
    assert not offences, "privileged imports in inference code:\n  " + "\n  ".join(offences)


def test_relative_import_resolution_is_not_fooled_by_dots() -> None:
    """The resolver itself must handle the form a grep would miss.

    If this ever regressed, test 1 above would keep passing while no longer
    checking anything -- so the resolver gets its own assertions.
    """
    # 'from ..oracle import logger' inside cdf.local.pipeline
    tree = ast.parse("from ..oracle import logger\n")
    targets = _imported_targets(tree, "cdf.local.pipeline", is_package=False)
    assert "cdf.oracle" in targets
    assert any(_is_forbidden_import(t) for t in targets)

    # 'from . import simulation' inside the cdf package __init__
    tree = ast.parse("from . import simulation\n")
    targets = _imported_targets(tree, "cdf", is_package=True)
    assert "cdf.simulation" in targets
    assert any(_is_forbidden_import(t) for t in targets)

    # A sibling relative import must stay allowed.
    tree = ast.parse("from ..common.geometry import distance\n")
    targets = _imported_targets(tree, "cdf.fusion.pipeline", is_package=False)
    assert "cdf.common.geometry" in targets
    assert not any(_is_forbidden_import(t) for t in targets)


def test_inference_packages_stay_clean_at_runtime() -> None:
    """Importing the inference entry points must not pull in privileged code.

    The AST pass cannot see an ``importlib.import_module`` call, so the same
    claim is verified by observing ``sys.modules`` in a fresh interpreter.
    """
    program = (
        "import sys\n"
        "import cdf.local.pipeline\n"
        "import cdf.fusion.pipeline\n"
        "import cdf.graph.analysis\n"
        "import cdf.graph.export\n"
        "import cdf.checking.trace_checker\n"
        "leaked = sorted(m for m in sys.modules\n"
        "                if m == 'carla' or m.startswith('carla.')\n"
        "                or m.startswith('cdf.oracle') or m.startswith('cdf.simulation'))\n"
        "print('LEAKED=' + ','.join(leaked))\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", program],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    assert proc.returncode == 0, "probe interpreter failed:\n{0}".format(proc.stderr)
    line = [l for l in proc.stdout.splitlines() if l.startswith("LEAKED=")]
    assert line, "probe interpreter produced no verdict:\n{0}".format(proc.stdout)
    leaked = [m for m in line[-1][len("LEAKED=") :].split(",") if m]
    assert not leaked, "privileged modules reachable from inference imports: {0}".format(
        leaked
    )


# ---------------------------------------------------------------------------
# 2. Forbidden simulator calls
# ---------------------------------------------------------------------------


def test_inference_packages_never_call_privileged_simulator_api(src_root: Path) -> None:
    """No privileged world query may appear anywhere in inference code."""
    offences: List[str] = []
    for path, module_name, _is_package in _iter_modules(src_root, INFERENCE_PACKAGES):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for site in _forbidden_call_sites(tree):
            offences.append("{0}: {1}".format(module_name, site))
    assert not offences, "privileged simulator calls in inference code:\n  " + "\n  ".join(
        offences
    )


def test_forbidden_call_detector_actually_detects() -> None:
    """The call detector must see all three evasion shapes it claims to see."""
    tree = ast.parse(
        "def f(world):\n"
        "    a = world.get_map()\n"
        "    b = getattr(world, 'get_waypoint')(1)\n"
        "    return a, b\n"
    )
    sites = _forbidden_call_sites(tree)
    assert any("get_map" in s for s in sites)
    assert any("get_waypoint" in s for s in sites)
    assert not _forbidden_call_sites(ast.parse("x = obj.get_range()\n"))


# ---------------------------------------------------------------------------
# 3. No camera sensing anywhere in the package
# ---------------------------------------------------------------------------


def test_no_camera_sensor_anywhere_in_the_package(src_root: Path) -> None:
    """The evidence model is radar plus own telemetry -- no camera, at all."""
    patterns = [re.compile(p, re.IGNORECASE) for p in CAMERA_PATTERNS]
    offences: List[str] = []
    n_files = 0
    for path in sorted(src_root.rglob("*.py")):
        n_files += 1
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern in patterns:
                if pattern.search(line):
                    offences.append(
                        "{0}:{1} matches {2}".format(
                            path.relative_to(src_root), lineno, pattern.pattern
                        )
                    )
    assert n_files > 0, "no sources found under {0}".format(src_root)
    assert not offences, "camera sensing referenced in the package:\n  " + "\n  ".join(
        offences
    )


# ---------------------------------------------------------------------------
# 4. Structural impossibility: the records have nowhere to put it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("record_type", LOCAL_RECORD_TYPES, ids=lambda t: t.__name__)
def test_local_records_cannot_hold_privileged_fields(record_type: type) -> None:
    """No persisted local record type has a privileged field."""
    names = [f.name for f in dataclasses.fields(record_type)]
    assert names, "{0} has no dataclass fields".format(record_type.__name__)

    exact = sorted(set(names) & set(FORBIDDEN_LOCAL_FIELD_NAMES))
    assert not exact, "{0} declares privileged field(s) {1}".format(
        record_type.__name__, exact
    )

    fuzzy = sorted(
        "{0} (contains {1!r})".format(n, s)
        for n in names
        for s in FORBIDDEN_LOCAL_FIELD_SUBSTRINGS
        if s in n.lower()
    )
    assert not fuzzy, "{0} declares privileged-looking field(s): {1}".format(
        record_type.__name__, fuzzy
    )


# ---------------------------------------------------------------------------
# 5. Artifact scanning: synthetic run and, when present, the recorded run
# ---------------------------------------------------------------------------


def test_synthetic_run_artifacts_carry_no_privileged_keys(analysed_run: RunLayout) -> None:
    """Every local and fused artifact of a fully analysed run is clean."""
    subtrees = local_and_fused_dirs(analysed_run.root)
    assert len(subtrees) >= 4, (
        "expected three vehicle subtrees and a fusion subtree, found {0}".format(
            [p.name for p in subtrees]
        )
    )
    violations: List[str] = []
    for subtree in subtrees:
        violations.extend(scan_tree_for_privileged_keys(subtree))
    assert not violations, "privileged keys in local/fused artifacts:\n  " + "\n  ".join(
        violations
    )


def test_synthetic_run_artifacts_are_actually_populated(analysed_run: RunLayout) -> None:
    """Guard against the scan passing because there was nothing to scan."""
    n_files = 0
    for subtree in local_and_fused_dirs(analysed_run.root):
        for path in subtree.rglob("*"):
            if path.is_file() and (
                path.name.endswith(".json")
                or path.name.endswith(".jsonl.gz")
                or path.suffix == ".graphml"
            ):
                n_files += 1
    assert n_files >= 20, "only {0} local/fused artifacts were scanned".format(n_files)

    causal = load_graph(analysed_run.causal_graph("A"), expect_scope=Provenance.LOCAL)
    assert causal.nodes, "participant A's causal graph is empty; the scan is vacuous"
    fused = load_graph(analysed_run.fused_causal_graph, expect_scope=Provenance.FUSED)
    assert fused.nodes, "the fused causal graph is empty; the scan is vacuous"


def test_recorded_run_artifacts_carry_no_privileged_keys(real_run: Path) -> None:
    """The same scan over genuine CARLA output, when a recorded run exists."""
    violations: List[str] = []
    for subtree in local_and_fused_dirs(real_run):
        violations.extend(scan_tree_for_privileged_keys(subtree))
    assert not violations, "privileged keys in recorded run artifacts:\n  " + "\n  ".join(
        violations
    )


# ---------------------------------------------------------------------------
# 6. Oracle-only event types never reach the unprivileged side
# ---------------------------------------------------------------------------


def test_oracle_only_event_types_absent_from_local_and_fused(
    analysed_run: RunLayout,
) -> None:
    """``ORACLE_*`` event types may not appear in a local or fused artifact."""
    assert ORACLE_ONLY_EVENT_TYPES, "the oracle-only registry is empty"
    violations: List[str] = []
    for subtree in local_and_fused_dirs(analysed_run.root):
        violations.extend(scan_tree_for_oracle_event_types(subtree))
    assert not violations, "oracle event types in local/fused artifacts:\n  " + "\n  ".join(
        violations
    )


def test_oracle_only_event_types_absent_from_recorded_run(real_run: Path) -> None:
    """The same check over the recorded run."""
    violations: List[str] = []
    for subtree in local_and_fused_dirs(real_run):
        violations.extend(scan_tree_for_oracle_event_types(subtree))
    assert not violations, "oracle event types in recorded artifacts:\n  " + "\n  ".join(
        violations
    )


def _recorded_campaign_runs() -> List[Path]:
    """Every recorded run under `artifacts/`, replays and ablation included.

    Replays and ablation runs ARE scanned here, unlike in the campaign
    aggregates: they are not part of the experiment, but they are artifacts this
    code wrote, and the boundary has to hold in everything it writes.
    """
    root = Path(__file__).resolve().parents[1] / "artifacts"
    if not root.is_dir():
        return []
    return [m.parent for m in sorted(root.rglob("manifest.json"))
            if (m.parent / "fusion").is_dir() or list(m.parent.glob("vehicle_*"))]


@pytest.mark.slow
def test_whole_recorded_campaign_carries_no_privileged_keys() -> None:
    """The scan of record: every local and fused artifact of every run.

    `test_recorded_run_artifacts_carry_no_privileged_keys` checks one run, which
    proves the pipeline can produce clean artifacts. This proves that it did --
    across every scenario, every seed, every variant and every counterfactual
    replay actually on disk. It is the single strongest statement the project
    makes about its data boundary, so it is worth the ~55 s it costs.
    """
    runs = _recorded_campaign_runs()
    if not runs:
        pytest.skip("no recorded runs under artifacts/")
    violations: List[str] = []
    scanned = 0
    for run_dir in runs:
        for subtree in local_and_fused_dirs(run_dir):
            scanned += 1
            violations.extend(scan_tree_for_privileged_keys(subtree))
    assert scanned, "the scan found no local or fused subtree; it would be vacuous"
    assert not violations, "privileged keys in {0} recorded run(s): {1}".format(
        len(runs), violations
    )


@pytest.mark.slow
def test_whole_recorded_campaign_carries_no_oracle_event_types() -> None:
    """No `ORACLE_*` event type anywhere on the unprivileged side of any run."""
    runs = _recorded_campaign_runs()
    if not runs:
        pytest.skip("no recorded runs under artifacts/")
    violations: List[str] = []
    for run_dir in runs:
        for subtree in local_and_fused_dirs(run_dir):
            violations.extend(scan_tree_for_oracle_event_types(subtree))
    assert not violations, "oracle event types in {0} recorded run(s): {1}".format(
        len(runs), violations
    )


def test_oracle_event_type_scanner_detects_a_planted_value(tmp_path: Path) -> None:
    """The oracle-type scanner must fail on an artifact that really carries one."""
    planted = tmp_path / "events.json"
    planted.write_text(
        json.dumps(
            {"events": [{"event_type": EventType.ORACLE_SIGNAL_VIOLATION.value}]}
        ),
        encoding="utf-8",
    )
    assert scan_tree_for_oracle_event_types(tmp_path)


# ---------------------------------------------------------------------------
# 7. The loader refuses to hand an oracle graph to an inference stage
# ---------------------------------------------------------------------------


def test_load_graph_refuses_an_oracle_graph_for_a_local_consumer(
    analysed_run: RunLayout,
) -> None:
    """``load_graph(..., expect_scope=LOCAL)`` must raise on an oracle document."""
    oracle_doc = GraphDocument(
        graph_kind="causal",
        scope=Provenance.ORACLE,
        owner=None,
        run_id="synthetic",
        scenario_id="SYN07",
        seed=0,
        nodes=[
            Event(
                event_id="oracle:ground-truth:1",
                event_type=EventType.ORACLE_SCRIPTED_INTERVENTION,
                participant_id="C",
                t_start=3.0,
                t_peak=3.0,
                provenance=Provenance.ORACLE,
            )
        ],
    )
    path = analysed_run.oracle_causal_graph
    save_graph(oracle_doc, path)

    with pytest.raises(ValueError) as excinfo:
        load_graph(path, expect_scope=Provenance.LOCAL)
    assert "oracle" in str(excinfo.value)

    with pytest.raises(ValueError):
        load_graph(path, expect_scope=Provenance.FUSED)

    # ... and the converse: a local graph may not masquerade as an oracle one.
    with pytest.raises(ValueError):
        load_graph(analysed_run.causal_graph("A"), expect_scope=Provenance.ORACLE)

    # The loader must still work when the scopes agree, or the guard would be
    # indistinguishable from a loader that always raises.
    assert load_graph(path, expect_scope=Provenance.ORACLE).scope is Provenance.ORACLE


# ---------------------------------------------------------------------------
# 8. A collision is recorded without the identity of the other party
# ---------------------------------------------------------------------------


def test_local_collision_record_knows_the_impact_but_not_the_counterparty(
    analysed_run: RunLayout,
) -> None:
    """The onboard collision record carries impulse and time -- and nothing else.

    In the partial-view scene A strikes B. A's own log must show that an impact
    happened and how hard, while remaining unable to say *who* it hit; the oracle
    is the only artifact that knows the pair.
    """
    payload = json.loads(analysed_run.triggers("A").read_text(encoding="utf-8"))
    collisions = [t for t in payload["triggers"] if t.get("collision_detected")]
    assert collisions, "participant A recorded no collision trigger"

    record = collisions[0]
    assert record["impulse"] > 0.0, "a collision trigger with no impulse is not evidence"
    assert record["kind"] == "collision"
    assert record["participant_id"] == "A"

    for key, where in _walk_keys(record):
        assert not COUNTERPARTY_KEY_PATTERN.search(key), (
            "the local collision record names the other party via key {0!r} "
            "at {1}".format(key, where)
        )
        assert not _key_violations(key, where)

    # No value anywhere in the record may name another participant either.
    others = {"B", "C"}
    for text in _walk_strings(record):
        assert text not in others, (
            "the local collision record contains the bare participant id {0!r}".format(
                text
            )
        )

    # Discrimination: the privileged side *does* know, which is what makes the
    # absence above meaningful rather than an accident of the scene.
    summary = json.loads(
        (analysed_run.oracle_dir / "oracle_summary.json").read_text(encoding="utf-8")
    )
    pairs = summary["collision_pairs"]
    assert pairs, "the oracle recorded no collision pair for a run that collided"
    assert {pairs[0]["a"], pairs[0]["b"]} == {"A", "B"}
    assert any(c.get("other_participant_id") for c in summary["collisions"])


def test_vehicle_subtree_never_names_another_participant(
    analysed_run: RunLayout,
) -> None:
    """Inside ``vehicle_X/`` every participant-valued field must say ``X``.

    This is the strongest form of the identity claim: not merely that no field is
    *called* something privileged, but that no participant-naming field in one
    vehicle's own log ever resolves to a different vehicle.
    """
    pids = analysed_run.participant_ids()
    assert len(pids) >= 2, "a single-participant run cannot test cross-naming"

    for pid in pids:
        subtree = analysed_run.vehicle_dir(pid)
        for path in sorted(subtree.rglob("*")):
            if not (path.name.endswith(".json") or path.name.endswith(".jsonl.gz")):
                continue
            data = _load_artifact(path)
            for key, value, where in _walk_key_values(data):
                if key not in PARTICIPANT_VALUED_KEYS:
                    continue
                names = value if isinstance(value, list) else [value]
                for name in names:
                    if not isinstance(name, str) or name not in pids:
                        continue
                    assert name == pid, (
                        "{0}/{1} at {2} names participant {3!r} in {4}'s own "
                        "log".format(pid, path.name, where, name, pid)
                    )


def _walk_key_values(node: Any, path: str = "$") -> Iterator[Tuple[str, Any, str]]:
    """Yield ``(key, value, json_path)`` for every mapping entry at any depth."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield (str(key), value, path)
            for item in _walk_key_values(value, "{0}.{1}".format(path, key)):
                yield item
    elif isinstance(node, list):
        for index, value in enumerate(node):
            for item in _walk_key_values(value, "{0}[{1}]".format(path, index)):
                yield item


# ---------------------------------------------------------------------------
# 9. Discrimination: the scan must fail on the oracle subtree
# ---------------------------------------------------------------------------


def test_oracle_subtree_is_expected_to_carry_privileged_fields(
    analysed_run: RunLayout,
) -> None:
    """The oracle subtree *must* fail the scan, or the scan proves nothing.

    Every assertion above is an assertion of absence, and an absence is only
    evidence if the instrument can detect a presence. The privileged trace is
    that positive control: it is supposed to contain actor ids, lane ids and
    signal state, and the same scanner that clears the local artifacts has to
    light up here.
    """
    oracle_dir = analysed_run.oracle_dir
    assert (oracle_dir / "oracle_summary.json").is_file()
    assert analysed_run.oracle_trace.is_file()

    violations = scan_tree_for_privileged_keys(oracle_dir)
    assert violations, (
        "the oracle subtree passed the privileged-field scan; either the trace is "
        "not being written or the scanner is blind"
    )

    flagged = " ".join(violations)
    for expected in ("actor_id", "lane_id", "traffic_light_state"):
        assert expected in flagged, (
            "the scanner did not flag {0!r} in the oracle trace; it is not "
            "discriminating on the registry it claims to use".format(expected)
        )


def test_recorded_oracle_subtree_is_also_flagged(real_run: Path) -> None:
    """The same positive control against genuine simulator ground truth."""
    oracle_dir = real_run / "oracle"
    if not oracle_dir.is_dir():
        pytest.skip("the recorded run has no oracle subtree")
    assert scan_tree_for_privileged_keys(oracle_dir), (
        "the recorded oracle trace carries no privileged field; it cannot be "
        "ground truth"
    )
