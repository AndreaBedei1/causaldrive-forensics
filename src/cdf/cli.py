"""One-command entry points for the whole experiment stack.

Every stage of this project is usable as a library, but a research artifact also
has to be runnable by somebody who has just cloned it. This module is that
surface: ``cdf run``, ``cdf evaluate``, ``cdf report`` and friends, each of which
wires the already-tested stages together and does nothing clever of its own.

Three decisions are worth stating, because they are what keep the CLI honest:

* **The configuration of a recorded run comes from that run.** A command that
  operates on an existing run directory rebuilds its :class:`~cdf.common.config.Config`
  from the ``config`` block stamped into ``manifest.json``, then applies
  ``--config-overrides`` on top. Re-analysing a run therefore uses the thresholds
  the run was recorded with rather than whatever ``configs/default.yaml`` happens
  to say today, and the resulting artifacts carry a config hash that matches.
* **Simulator access is lazy and map-aware.** Nothing under :mod:`cdf.simulation`
  is imported until a command actually needs the simulator, so ``cdf evaluate``
  and ``cdf report`` work on a machine with no CARLA installed. When a run *is*
  needed, the map is selected through
  :class:`~cdf.simulation.carla_client.SimulatorSession`, which owns the one
  dependable map switch per server process; ``cdf suite`` therefore groups its
  work by map instead of paying a server restart per scenario.
* **Optional stages are delegated, never faked.** The oracle graph builder, the
  counterfactual replay engine, the viewer bundle writer and a dedicated
  evaluation module are separate deliverables. Where one of them is installed the
  CLI calls it (contract: ``f(run_dir: Path, cfg: Config)``); where it is not,
  the command either says exactly what is missing and exits non-zero, or -- for
  ``evaluate`` -- falls back to the reduced, clearly-labelled comparison that the
  artifacts on disk actually support. No number printed by this module is ever
  invented: every one of them is read from, or computed from, a real artifact.

Exit codes: ``0`` success, ``1`` the command ran but its subject failed (a
scenario that did not produce its declared encounter, a missing required
dependency), ``2`` the command could not run at all (bad usage, missing input,
missing optional stage).
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import inspect
import logging
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from .common.config import (
    Config,
    available_scenarios,
    load_run_config,
    parse_override,
    repo_root,
)
from .common.io import read_json, read_jsonl_gz, write_csv, write_json
from .common.layout import RunLayout
from .common.schemas import EventType, OutcomeClass, Provenance, SCHEMA_VERSIONS

LOGGER = logging.getLogger("cdf.cli")

__all__ = [
    "main",
    "build_parser",
    "resolve_config",
    "CliError",
    "EXIT_OK",
    "EXIT_FAILED",
    "EXIT_USAGE",
]

EXIT_OK = 0
"""The command did what it was asked to do."""

EXIT_FAILED = 1
"""The command ran, but its subject failed (validation, missing dependency)."""

EXIT_USAGE = 2
"""The command could not run: bad arguments, missing input, missing stage."""


class CliError(RuntimeError):
    """An operational failure that should be reported without a traceback.

    Carries the exit code the CLI must return, so that "the run directory does
    not exist" (usage) and "the scenario did not collide" (failure) stay
    distinguishable to a shell script.
    """

    def __init__(self, message: str, exit_code: int = EXIT_USAGE) -> None:
        super(CliError, self).__init__(message)
        self.exit_code = int(exit_code)


# ---------------------------------------------------------------------------
# Optional downstream stages
# ---------------------------------------------------------------------------
#
# Each entry is ``(module, attribute)``. The first one that exists and accepts
# the ``(run_dir, cfg)`` contract wins. Probing by name rather than importing a
# fixed module is what lets this CLI ship before -- and keep working after -- the
# oracle/counterfactual/evaluation modules land.

_EVALUATION_HOOKS: Tuple[Tuple[str, str], ...] = (
    ("cdf.evaluation.suite", "evaluate_run"),
    ("cdf.evaluation.pipeline", "evaluate_run"),
    ("cdf.evaluation", "evaluate_run"),
)

_VIEWER_BUNDLE_HOOKS: Tuple[Tuple[str, str], ...] = (
    ("cdf.viewer.bundle", "write_bundle"),
    ("cdf.evaluation.viewer", "build_viewer_bundle"),
    ("cdf.evaluation", "build_viewer_bundle"),
)

_AGGREGATE_HOOKS: Tuple[Tuple[str, str], ...] = (
    ("cdf.evaluation.suite", "aggregate_runs"),
    ("cdf.evaluation.report", "aggregate_runs"),
    ("cdf.evaluation", "aggregate_runs"),
)

#: Modules whose entry points take more than ``(run_dir, cfg)`` and are therefore
#: wired explicitly rather than through :func:`_load_hook`.
_ORACLE_GRAPH_MODULE = "cdf.oracle.graph"
_COUNTERFACTUAL_MODULE = "cdf.causal.counterfactuals"
_INTERVENTION_MODULE = "cdf.causal.interventions"

#: Files the browser viewer needs next to a run's ``viewer/run_data.json``.
VIEWER_ASSETS: Tuple[str, ...] = ("index.html", "app.js", "styles.css")

#: Third-party packages the non-simulator stack cannot work without, mapped to
#: the import name (``pyyaml`` is imported as ``yaml``).
REQUIRED_PACKAGES: Tuple[Tuple[str, str], ...] = (
    ("numpy", "numpy"),
    ("scipy", "scipy"),
    ("networkx", "networkx"),
    ("pandas", "pandas"),
    ("pyyaml", "yaml"),
    ("matplotlib", "matplotlib"),
)

#: Packages that improve the experience but whose absence is not fatal.
OPTIONAL_PACKAGES: Tuple[Tuple[str, str], ...] = (("pytest", "pytest"),)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

_HANDLER_MARK = "_cdf_cli_handler"


def _configure_logging(verbosity: int) -> None:
    """Install exactly one stderr handler, whatever how often ``main`` is called.

    Stdout is reserved for the command's own report so that ``cdf report | ...``
    stays pipeable; diagnostics go to stderr. The handler is tagged and replaced
    on re-entry, because the test-suite calls :func:`main` many times in one
    process and stacked handlers would duplicate every line.
    """
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, _HANDLER_MARK, False):
            root.removeHandler(handler)
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)-7s %(name)s: %(message)s"))
    setattr(handler, _HANDLER_MARK, True)
    root.addHandler(handler)
    root.setLevel(level)


# ---------------------------------------------------------------------------
# Small shared helpers
# ---------------------------------------------------------------------------


def _maybe_import(module_name: str) -> Optional[Any]:
    """Import ``module_name`` if it exists, else ``None``.

    Absence is detected with :func:`importlib.util.find_spec` rather than by
    catching :class:`ImportError` around the import, so that an ``ImportError``
    raised *inside* an installed module surfaces as the bug it is instead of
    being mistaken for "the optional stage is not installed".
    """
    try:
        spec = importlib.util.find_spec(module_name)
    except (ImportError, ValueError):
        return None
    if spec is None:
        return None
    return importlib.import_module(module_name)


def _load_hook(
    candidates: Sequence[Tuple[str, str]], n_positional: int = 2
) -> Optional[Callable[..., Any]]:
    """First installed ``(module, attribute)`` callable accepting the contract.

    A module that is simply absent is skipped silently -- that is the expected
    state before the optional stage is written. A module that *exists* but whose
    entry point has an incompatible signature is reported loudly, because that is
    a wiring bug the user needs to know about rather than a missing feature.
    """
    for module_name, attr in candidates:
        module = _maybe_import(module_name)
        if module is None:
            continue
        fn = getattr(module, attr, None)
        if fn is None or not callable(fn):
            continue
        if not _accepts_positional(fn, n_positional):
            LOGGER.warning(
                "%s.%s exists but does not accept %d positional argument(s) "
                "(expected the f(run_dir, cfg) contract); ignoring it",
                module_name,
                attr,
                n_positional,
            )
            continue
        LOGGER.info("using %s.%s", module_name, attr)
        return fn
    return None


def _accepts_positional(fn: Callable[..., Any], n: int) -> bool:
    """Whether ``fn`` can be called with exactly ``n`` positional arguments."""
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):  # builtins without introspectable signatures
        return True
    required = 0
    allowed = 0
    unlimited = False
    for param in sig.parameters.values():
        if param.kind in (param.POSITIONAL_ONLY, param.POSITIONAL_OR_KEYWORD):
            allowed += 1
            if param.default is param.empty:
                required += 1
        elif param.kind is param.VAR_POSITIONAL:
            unlimited = True
    return required <= n and (unlimited or n <= allowed)


def resolve_config(
    scenario_id: Optional[str] = None,
    overrides: Optional[Sequence[str]] = None,
    run_dir: Optional[Path] = None,
) -> Config:
    """Resolve the configuration a command should use.

    When ``run_dir`` names a recorded run, its manifest's ``config`` block is the
    base: re-analysing an old run must not silently pick up today's thresholds.
    ``overrides`` (``dotted.key=value``) are applied last in either case, so a
    caller can always steer one parameter without editing a file.
    """
    items = list(overrides or [])
    if run_dir is not None:
        layout = RunLayout.from_run_dir(run_dir)
        if layout.manifest.exists():
            manifest = read_json(layout.manifest)
            block = manifest.get("config")
            if isinstance(block, dict) and block:
                cfg = Config(block, sources=[str(layout.manifest)])
                for item in items:
                    cfg = cfg.with_overrides(parse_override(item))
                return cfg
            scenario_id = scenario_id or str(manifest.get("scenario_id") or "") or None
    return load_run_config(scenario_id=scenario_id, overrides=items)


def _require_run_dir(raw: str) -> RunLayout:
    """Validate that ``raw`` looks like a recorded run and wrap it in a layout."""
    path = Path(raw).expanduser()
    if not path.exists():
        raise CliError("run directory does not exist: {0}".format(path))
    if not path.is_dir():
        raise CliError("--run must be a directory, got a file: {0}".format(path))
    layout = RunLayout.from_run_dir(path)
    if not layout.participant_ids():
        raise CliError(
            "no vehicle_*/ evidence under {0}; is this a run directory? "
            "(expected e.g. {0}/vehicle_A/telemetry.jsonl.gz)".format(path)
        )
    return layout


def _artifacts_root(args: argparse.Namespace, cfg: Config) -> Path:
    """Artifacts root from ``--artifacts``, else ``output.artifacts_root``."""
    if getattr(args, "artifacts", None):
        return Path(args.artifacts).expanduser()
    return Path(str(cfg.get("output.artifacts_root", "artifacts")))


def _fmt(value: Any, width: int) -> str:
    """Left-aligned fixed-width cell; over-long content is marked, not hidden."""
    text = "-" if value is None else str(value)
    if len(text) > width:
        return text[: max(1, width - 2)] + ".."
    return text.ljust(width)


def _outcome_text(manifest: Any) -> str:
    """Outcome label of a run manifest, whether it holds an enum or a string."""
    outcome = getattr(manifest, "outcome", None)
    if outcome is None:
        return "unknown"
    return str(getattr(outcome, "value", outcome))


def _print_table(columns: Sequence[Tuple[str, int]], rows: Sequence[Mapping[str, Any]]) -> None:
    """Print a fixed-width table; ``columns`` is ``(key, width)`` pairs."""
    header = "  ".join(_fmt(key, width) for key, width in columns)
    print(header)
    print("  ".join("-" * width for _key, width in columns))
    for row in rows:
        print("  ".join(_fmt(row.get(key), width) for key, width in columns))


def _rel(path: Path) -> str:
    """Path relative to the working directory when possible, else absolute."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# cdf env
# ---------------------------------------------------------------------------


def _package_version(import_name: str) -> Optional[str]:
    """Version string of an installed package, or ``None`` when not importable."""
    try:
        module = importlib.import_module(import_name)
    except ImportError:
        return None
    for attr in ("__version__", "version", "VERSION"):
        value = getattr(module, attr, None)
        if isinstance(value, str) and value:
            return value
    return "installed (version unknown)"


def _probe_server(cfg: Config) -> Dict[str, Any]:
    """Try one short handshake with a CARLA server.

    A single probe with a short timeout, not :func:`connect_with_retry`'s full
    schedule: ``cdf env`` is a diagnostic and must answer in seconds whether a
    server is there, not wait two minutes for one that is not.
    """
    from .simulation.carla_client import CarlaUnavailable, connect_with_retry, map_basename

    host = str(cfg.get("simulation.host", "127.0.0.1"))
    port = int(cfg.get("simulation.port", 2000))
    probe_s = float(cfg.get("simulation.env_probe_timeout_s", 4.0))
    out: Dict[str, Any] = {"host": host, "port": port, "reachable": False}
    try:
        client = connect_with_retry(
            host=host,
            port=port,
            timeout_s=float(cfg.get("simulation.timeout_s", 60.0)),
            attempts=1,
            retry_delay_s=0.0,
            probe_timeout_s=probe_s,
        )
        out["reachable"] = True
        out["server_version"] = str(client.get_server_version())
        out["map"] = map_basename(client.get_world().get_map().name)
    except CarlaUnavailable as exc:
        out["error"] = str(exc).splitlines()[0]
    except RuntimeError as exc:  # server answered the handshake then timed out
        out["error"] = str(exc)
    return out


def cmd_env(args: argparse.Namespace) -> int:
    """Report the environment and whether it can run the stack."""
    cfg = resolve_config(overrides=args.config_overrides)
    problems: List[str] = []
    warnings: List[str] = []

    print("interpreter")
    print("  python           {0}".format(sys.version.split()[0]))
    print("  executable       {0}".format(sys.executable))
    if sys.version_info < (3, 8):
        problems.append(
            "Python {0} is too old; this project requires 3.8 or newer".format(
                ".".join(str(p) for p in sys.version_info[:3])
            )
        )

    try:
        from . import __version__ as package_version
    except ImportError:  # pragma: no cover - the package is what we are running
        package_version = "unknown"
    print("  cdf package      {0}".format(package_version))
    print("  config hash      {0}".format(cfg.hash))

    print("required packages")
    for dist_name, import_name in REQUIRED_PACKAGES:
        version = _package_version(import_name)
        print("  {0:<16} {1}".format(dist_name, version or "MISSING"))
        if version is None:
            problems.append(
                "required package {0!r} is not importable; install it with "
                "`pip install -e .`".format(dist_name)
            )

    print("optional packages")
    for dist_name, import_name in OPTIONAL_PACKAGES:
        version = _package_version(import_name)
        print("  {0:<16} {1}".format(dist_name, version or "not installed"))

    carla_version = _package_version("carla")
    print("simulator")
    print("  carla module     {0}".format(carla_version or "not importable"))
    if carla_version is None:
        warnings.append(
            "the carla Python API is not importable: recording new runs is "
            "unavailable, but analysis, fusion, checking, evaluation and "
            "reporting all work on already-recorded artifacts"
        )

    from .simulation.carla_client import CarlaServer, CarlaUnavailable, find_carla_root

    root = find_carla_root(cfg.get("simulation.carla_root"))
    print("  carla root       {0}".format(root if root is not None else "not found"))
    if root is None:
        warnings.append(
            "no packaged CARLA installation found; set $CARLA_ROOT or "
            "simulation.carla_root to start a server automatically"
        )

    if args.start_server:
        if root is None:
            problems.append("--start-server was requested but no CARLA installation was found")
        else:
            server = CarlaServer(
                root=cfg.get("simulation.carla_root"),
                port=int(cfg.get("simulation.port", 2000)),
                quality=str(cfg.get("simulation.quality_level", "Low")),
            )
            print("  starting server  {0}".format(" ".join(server.command())))
            try:
                server.start(wait_s=float(cfg.get("simulation.server_start_wait_s", 180.0)))
            except CarlaUnavailable as exc:
                problems.append("could not start a CARLA server: {0}".format(exc))

    if carla_version is not None:
        probe = _probe_server(cfg)
        target = "{0}:{1}".format(probe["host"], probe["port"])
        if probe["reachable"]:
            print("  server           reachable at {0}".format(target))
            print("  server version   {0}".format(probe.get("server_version", "unknown")))
            print("  current map      {0}".format(probe.get("map", "unknown")))
        else:
            print("  server           not reachable at {0}".format(target))
            warnings.append(
                "no CARLA server answered at {0} ({1})".format(target, probe.get("error", ""))
            )
    else:
        print("  server           not probed (carla module missing)")

    print("host")
    print("  cpu count        {0}".format(os.cpu_count() or "unknown"))
    usage = shutil.disk_usage(str(Path.cwd()))
    print("  free disk        {0:.1f} GiB of {1:.1f} GiB".format(
        usage.free / float(1 << 30), usage.total / float(1 << 30)
    ))
    print("  artifacts root   {0}".format(_artifacts_root(args, cfg)))
    print("  scenarios        {0}".format(", ".join(available_scenarios())))

    for text in warnings:
        print("warning: {0}".format(text), file=sys.stderr)
    for text in problems:
        print("error: {0}".format(text), file=sys.stderr)

    if problems:
        print("environment NOT usable ({0} problem(s))".format(len(problems)))
        return EXIT_FAILED
    print("environment usable{0}".format(
        " (with {0} warning(s))".format(len(warnings)) if warnings else ""
    ))
    return EXIT_OK


# ---------------------------------------------------------------------------
# Post-run stages shared by `cdf run` and `cdf suite`
# ---------------------------------------------------------------------------


def _stage_analyse(layout: RunLayout, cfg: Config) -> Dict[str, Any]:
    """Local per-participant analysis; returns a printable summary."""
    from .local.pipeline import analyse_run

    analyses = analyse_run(layout.root, cfg, persist=True)
    return {pid: analysis.summary() for pid, analysis in sorted(analyses.items())}


def _stage_fuse(layout: RunLayout, cfg: Config) -> Dict[str, Any]:
    """Post-event fusion; returns a printable summary."""
    from .fusion.pipeline import fuse_run

    result = fuse_run(layout.root, cfg, persist=True)
    return result.summary()


def _spec_for_run(layout: RunLayout, cfg: Config) -> Any:
    """Rebuild the :class:`ScenarioSpec` a recorded run was produced from.

    The variant is taken from the run's manifest rather than from the scenario's
    default, because a run of the ``avoided`` variant must not be re-described as
    the ``crash`` one when its artifacts are revisited.
    """
    from .simulation.scenario_base import ScenarioSpec

    variant = None
    if layout.manifest.exists():
        variant = read_json(layout.manifest).get("variant") or None
    return ScenarioSpec.from_config(cfg, variant=variant)


def _stage_oracle_graph(layout: RunLayout, cfg: Config, spec: Any) -> Optional[Tuple[int, int]]:
    """Build and persist the privileged reference graphs for a run.

    Returns the ``(n_events, n_causal_edges)`` actually produced, or ``None``
    when the oracle graph builder is not installed. The scenario specification is
    required (it carries the designed causal template), which is why this stage
    is wired explicitly instead of through the ``(run_dir, cfg)`` hook contract.
    """
    module = _maybe_import(_ORACLE_GRAPH_MODULE)
    if module is None or not hasattr(module, "build_and_persist"):
        return None
    events, _event_graph, causal_graph = module.build_and_persist(layout.root, spec, cfg)
    return (len(events), len(causal_graph.edges))


def _stage_check(layout: RunLayout, cfg: Config) -> Dict[str, Any]:
    """Finite-trace model checking over the recorded local evidence."""
    from .checking.trace_checker import TraceChecker
    from .common.evidence import load_run

    run = load_run(layout.root, with_radar=False)
    # Persists the results AND the counterexamples they reference.
    report = TraceChecker(cfg).check_and_persist(layout, run)
    return report.get("summary", {})


def _post_run_stages(
    layout: RunLayout,
    cfg: Config,
    spec: Any = None,
    do_analyse: bool = True,
    do_fuse: bool = True,
    do_check: bool = True,
    do_viewer: bool = True,
) -> List[str]:
    """Run the offline stages over a freshly recorded run, reporting each.

    Returns human-readable lines rather than printing directly so that
    ``cdf suite`` can decide how verbose to be. A stage that fails for a
    structural reason (fusion with a single participant, for instance) is
    reported and the remaining stages still run: a partially analysed run is far
    more useful than a discarded one.
    """
    lines: List[str] = []

    if do_analyse:
        summaries = _stage_analyse(layout, cfg)
        for pid, summary in summaries.items():
            lines.append(
                "  local {0}: {1} events, causal {2} nodes / {3} edges".format(
                    pid,
                    summary["n_events"],
                    summary["n_causal_nodes"],
                    summary["n_causal_edges"],
                )
            )
    else:
        lines.append("  local analysis skipped (--no-analyse)")

    if do_fuse:
        have_graphs = any(layout.causal_graph(pid).exists() for pid in layout.participant_ids())
        if not have_graphs:
            lines.append("  fusion skipped: no local causal graphs (run without --no-analyse)")
        else:
            try:
                summary = _stage_fuse(layout, cfg)
                lines.append(
                    "  fusion: {0}/{1} track(s) resolved, fused causal {2} nodes / {3} edges".format(
                        summary["n_resolved"],
                        summary["n_tracks"],
                        summary["fused_causal"]["n_nodes"],
                        summary["fused_causal"]["n_edges"],
                    )
                )
            except (ValueError, FileNotFoundError) as exc:
                lines.append("  fusion skipped: {0}".format(exc))
    else:
        lines.append("  fusion skipped (--no-fuse)")

    built = _stage_oracle_graph(layout, cfg, spec if spec is not None else _spec_for_run(layout, cfg))
    if built is not None:
        lines.append(
            "  oracle graph: {0} event(s), {1} causal edge(s) -> {2}".format(
                built[0], built[1], _rel(layout.oracle_causal_graph)
            )
        )
    else:
        lines.append(
            "  oracle graph skipped: {0} is not installed".format(_ORACLE_GRAPH_MODULE)
        )

    if do_check:
        summary = _stage_check(layout, cfg)
        lines.append(
            "  model checking: {0} PASS / {1} FAIL / {2} UNKNOWN".format(
                summary.get("PASS", 0), summary.get("FAIL", 0), summary.get("UNKNOWN", 0)
            )
        )
    else:
        lines.append("  model checking skipped (--no-check)")

    if do_viewer and bool(cfg.get("output.write_viewer_bundle", True)):
        viewer_hook = _load_hook(_VIEWER_BUNDLE_HOOKS)
        if viewer_hook is not None:
            viewer_hook(layout.root, cfg)
            lines.append("  viewer bundle: {0}".format(_rel(layout.viewer_bundle)))
        else:
            lines.append("  viewer bundle skipped: no bundle writer installed")
    return lines


# ---------------------------------------------------------------------------
# cdf run
# ---------------------------------------------------------------------------


def cmd_run(args: argparse.Namespace) -> int:
    """Record one scenario run and analyse it end to end."""
    cfg = resolve_config(scenario_id=args.scenario, overrides=args.config_overrides)

    from .simulation.carla_client import session_from_config
    from .simulation.runner import run_scenario
    from .simulation.scenario_base import ScenarioSpec

    spec = ScenarioSpec.from_config(cfg, variant=args.variant)
    if args.follow_vehicle.upper() not in spec.participant_ids:
        raise CliError(
            "follow vehicle {0!r} is not present in {1}; available vehicles: {2}".format(
                args.follow_vehicle,
                spec.scenario_id,
                ", ".join(spec.participant_ids),
            )
        )
    if args.realtime and not args.live:
        raise CliError("--realtime requires --live")
    if not args.realtime and abs(float(args.playback_speed) - 1.0) > 1e-12:
        raise CliError("--playback-speed other than 1.0 requires --realtime")
    artifacts = _artifacts_root(args, cfg)
    print("running {0} ({1}) variant={2} seed={3} on {4}".format(
        spec.scenario_id, spec.name, spec.variant, args.seed, spec.map_name
    ))

    with session_from_config(cfg) as session:
        # The map must be selected through the session: the tested 0.9.15 build
        # only tolerates one dependable map switch per server process, and the
        # session is what knows whether this process has already spent it.
        session.world_for_map(spec.map_name)
        result = run_scenario(
            session.client(),
            cfg,
            spec,
            seed=int(args.seed),
            artifacts_root=str(artifacts),
            persist=True,
            live=bool(args.live),
            realtime=bool(args.realtime),
            playback_speed=float(args.playback_speed),
            spectator_mode=args.spectator,
            follow_vehicle=args.follow_vehicle.upper(),
            spectator_height=float(args.spectator_height),
            show_labels=not bool(args.no_labels),
        )

    layout = result.layout
    print("run dir: {0}".format(_rel(layout.root)))
    print("  outcome: {0}  (expected {1})".format(
        _outcome_text(result.manifest), spec.expected_outcome
    ))
    for line in _post_run_stages(
        layout,
        cfg,
        spec=spec,
        do_analyse=not args.no_analyse,
        do_fuse=not args.no_fuse,
        do_check=not args.no_check,
        do_viewer=not args.no_viewer,
    ):
        print(line)

    if not result.ok:
        problems = result.validation.get("problems", [])
        print("scenario validation FAILED:", file=sys.stderr)
        for problem in problems:
            print("  - {0}".format(problem), file=sys.stderr)
        return EXIT_FAILED
    print("scenario validation passed")
    return EXIT_OK


# ---------------------------------------------------------------------------
# cdf suite
# ---------------------------------------------------------------------------


def declared_variants(scenario_id: str, overrides: Sequence[str] = ()) -> List[str]:
    """Every variant a scenario declares, in declaration order.

    The campaign is defined as "every scenario, every variant it declares, every
    seed", so the list has to come from the scenario files rather than from a
    number written down somewhere. ``--variants crash avoided`` applies the same
    names to every scenario and fails on one that has no such variant, which is
    why this exists alongside it.
    """
    cfg = resolve_config(scenario_id=scenario_id, overrides=list(overrides))
    block = cfg.get("scenario", None)
    if not isinstance(block, Mapping):
        return []
    variants = block.get("variants")
    if isinstance(variants, Mapping):
        return [str(name) for name in variants.keys()]
    if isinstance(variants, (list, tuple)):
        return [str((v or {}).get("name", "")) for v in variants if (v or {}).get("name")]
    return []


def suite_combinations(
    scenario_ids: Sequence[str], overrides: Sequence[str] = ()
) -> List[Tuple[str, str]]:
    """``(scenario_id, variant)`` for every declared variant of every scenario."""
    out: List[Tuple[str, str]] = []
    for scenario_id in scenario_ids:
        for variant in declared_variants(scenario_id, overrides):
            out.append((str(scenario_id), variant))
    return out


def _suite_plan(
    scenario_ids: Sequence[str],
    seeds: Sequence[int],
    variants: Optional[Sequence[str]],
    overrides: Sequence[str],
    all_variants: bool = False,
) -> List[Dict[str, Any]]:
    """Build the ordered work plan, grouped so that map switches are minimal.

    Sorting by map first is the whole point: a suite that alternates between two
    towns pays a full server restart on every alternation (see
    :class:`~cdf.simulation.carla_client.SimulatorSession`), while one that runs
    every Town05 scenario before the first Town03 one pays exactly one.

    With ``all_variants`` every variant each scenario declares is run, which is
    what the experimental campaign is defined as; ``variants`` applies one fixed
    list to every scenario and is for running a slice of it.
    """
    from .simulation.scenario_base import ScenarioSpec

    entries: List[Dict[str, Any]] = []
    for scenario_id in scenario_ids:
        cfg = resolve_config(scenario_id=scenario_id, overrides=overrides)
        if all_variants:
            wanted = declared_variants(scenario_id, overrides) or [None]
        else:
            wanted = list(variants) if variants else [None]
        for variant in wanted:
            spec = ScenarioSpec.from_config(cfg, variant=variant)
            for seed in seeds:
                entries.append(
                    {
                        "scenario_id": spec.scenario_id,
                        "variant": spec.variant,
                        "seed": int(seed),
                        "map": spec.map_name,
                        "cfg": cfg,
                        "spec": spec,
                    }
                )
    entries.sort(key=lambda e: (e["map"], e["scenario_id"], e["variant"], e["seed"]))
    return entries


def cmd_suite(args: argparse.Namespace) -> int:
    """Run many scenarios and seeds in one process, reusing one session."""
    if not args.all and not args.scenarios:
        raise CliError("pass --all or --scenarios S01 S02 ...")
    scenario_ids = list(args.scenarios) if args.scenarios else available_scenarios()
    seeds = [int(s) for s in args.seeds]

    from .simulation.carla_client import session_from_config
    from .simulation.runner import run_scenario

    plan = _suite_plan(
        scenario_ids,
        seeds,
        args.variants,
        args.config_overrides,
        all_variants=bool(getattr(args, "all_variants", False)),
    )
    if not plan:
        raise CliError("the suite plan is empty; check --scenarios and --seeds")
    maps = sorted({entry["map"] for entry in plan})
    print("suite: {0} run(s) over {1} scenario(s), {2} seed(s), map(s) {3}".format(
        len(plan), len(scenario_ids), len(seeds), ", ".join(maps)
    ))

    rows: List[Dict[str, Any]] = []
    failures = 0
    # One session for the whole suite; `world_for_map` is a no-op when the map is
    # already loaded, so grouping by map means one switch per map at most.
    with session_from_config(plan[0]["cfg"]) as session:
        for entry in plan:
            cfg: Config = entry["cfg"]
            spec = entry["spec"]
            label = "{0}/{1}/seed{2:03d}".format(
                entry["scenario_id"], entry["variant"], entry["seed"]
            )
            print("--- {0} on {1}".format(label, entry["map"]))
            row: Dict[str, Any] = {
                "scenario": entry["scenario_id"],
                "variant": entry["variant"],
                "seed": entry["seed"],
                "outcome": None,
                "validation": None,
                "run_dir": None,
            }
            try:
                session.world_for_map(spec.map_name)
                result = run_scenario(
                    session.client(),
                    cfg,
                    spec,
                    seed=entry["seed"],
                    artifacts_root=str(_artifacts_root(args, cfg)),
                    persist=True,
                )
                row["run_dir"] = _rel(result.layout.root)
                row["outcome"] = _outcome_text(result.manifest)
                row["validation"] = "passed" if result.ok else "FAILED"
                for line in _post_run_stages(
                    result.layout,
                    cfg,
                    spec=spec,
                    do_analyse=not args.no_analyse,
                    do_fuse=not args.no_fuse,
                    do_check=not args.no_check,
                    do_viewer=not args.no_viewer,
                ):
                    print(line)
                if not result.ok:
                    failures += 1
                    for problem in result.validation.get("problems", []):
                        print("  problem: {0}".format(problem), file=sys.stderr)
            except Exception as exc:  # noqa: BLE001 - recorded, then re-raised below
                failures += 1
                row["validation"] = "ERROR"
                row["outcome"] = type(exc).__name__
                print("error: {0} failed: {1}".format(label, exc), file=sys.stderr)
                LOGGER.exception("run %s raised", label)
                if not args.continue_on_error:
                    rows.append(row)
                    _print_suite_table(rows)
                    return EXIT_FAILED
            rows.append(row)
            if row["validation"] == "FAILED" and not args.continue_on_error:
                _print_suite_table(rows)
                return EXIT_FAILED

    _print_suite_table(rows)
    if failures and not args.continue_on_error:
        return EXIT_FAILED
    if failures:
        print("{0} of {1} run(s) failed; --continue-on-error kept the suite going".format(
            failures, len(rows)
        ), file=sys.stderr)
    return EXIT_OK


def _print_suite_table(rows: Sequence[Mapping[str, Any]]) -> None:
    print("")
    _print_table(
        (("scenario", 10), ("variant", 12), ("seed", 5), ("outcome", 12),
         ("validation", 10), ("run_dir", 52)),
        rows,
    )


# ---------------------------------------------------------------------------
# cdf analyse / cdf fuse
# ---------------------------------------------------------------------------


def cmd_analyse(args: argparse.Namespace) -> int:
    """Re-run local per-participant inference over a recorded run."""
    layout = _require_run_dir(args.run)
    cfg = resolve_config(overrides=args.config_overrides, run_dir=layout.root)
    summaries = _stage_analyse(layout, cfg)
    print("local analysis of {0} (config {1})".format(_rel(layout.root), cfg.hash))
    for pid, summary in summaries.items():
        print("  {0}: {1} events, event graph {2} edges, causal {3} nodes / {4} edges".format(
            pid,
            summary["n_events"],
            summary["n_event_graph_edges"],
            summary["n_causal_nodes"],
            summary["n_causal_edges"],
        ))
    return EXIT_OK


def cmd_fuse(args: argparse.Namespace) -> int:
    """Re-run post-event fusion over a recorded run."""
    layout = _require_run_dir(args.run)
    cfg = resolve_config(overrides=args.config_overrides, run_dir=layout.root)
    try:
        summary = _stage_fuse(layout, cfg)
    except (ValueError, FileNotFoundError) as exc:
        raise CliError(str(exc))
    print("fusion of {0} (config {1})".format(_rel(layout.root), cfg.hash))
    print("  tracks: {0} resolved / {1} ambiguous / {2} unresolved of {3}".format(
        summary["n_resolved"], summary["n_ambiguous"], summary["n_unresolved"], summary["n_tracks"]
    ))
    print("  fused causal graph: {0} nodes / {1} edges -> {2}".format(
        summary["fused_causal"]["n_nodes"],
        summary["fused_causal"]["n_edges"],
        _rel(layout.fused_causal_graph),
    ))
    return EXIT_OK


# ---------------------------------------------------------------------------
# cdf counterfactuals
# ---------------------------------------------------------------------------


def cmd_counterfactuals(args: argparse.Namespace) -> int:
    """Replay a recorded run under each candidate scripted intervention."""
    layout = _require_run_dir(args.run)
    cfg = resolve_config(overrides=args.config_overrides, run_dir=layout.root)

    engine = _maybe_import(_COUNTERFACTUAL_MODULE)
    planner = _maybe_import(_INTERVENTION_MODULE)
    if engine is None or planner is None:
        raise CliError(
            "the counterfactual replay engine is not installed (expected {0} and "
            "{1})".format(_COUNTERFACTUAL_MODULE, _INTERVENTION_MODULE)
        )

    from .simulation.carla_client import session_from_config

    spec = _spec_for_run(layout, cfg)
    seed = int(read_json(layout.manifest).get("seed", 0)) if layout.manifest.exists() else 0
    # The replay engine re-creates the factual layout from the artifacts root, so
    # it must be given the root this run actually lives under rather than the
    # default: <artifacts_root>/<scenario dir>/<seed dir>.
    artifacts_root = layout.root.parent.parent

    fused = _load_graph_if(layout.fused_causal_graph, Provenance.FUSED)
    interventions = list(planner.enumerate_interventions(spec, fused, cfg))

    # Omission repairs come last and come from the *reconstruction*: a
    # non-action node exists only where an obligation was observed and the
    # interval was covered, so proposing to supply the missing behaviour is
    # proposing to test something the data already supports. Enumerated from the
    # scenario instead, they would be testing the experiment's intent.
    repairs = list(planner.omission_repairs(spec, fused, cfg))
    if repairs:
        print("  {0} omission repair(s) proposed from the reconstruction".format(
            len(repairs)
        ))
    interventions.extend(repairs)

    if not interventions:
        raise CliError(
            "scenario {0} declares no intervention candidates and the "
            "reconstruction supports no omission repair, so there is nothing "
            "to replay".format(spec.scenario_id)
        )
    print("counterfactual replays for {0} (config {1})".format(_rel(layout.root), cfg.hash))
    print("  {0} intervention(s): {1}".format(
        len(interventions),
        ", ".join(str(getattr(i, "intervention_id", i)) for i in interventions),
    ))

    with session_from_config(cfg) as session:
        result = engine.run_counterfactual_suite(
            session,
            cfg,
            spec,
            seed,
            interventions,
            artifacts_root=str(artifacts_root),
        )

    if layout.counterfactual_manifest.exists():
        print("  manifest:      {0}".format(_rel(layout.counterfactual_manifest)))
    if layout.intervention_results.exists():
        print("  results table: {0}".format(_rel(layout.intervention_results)))
    if layout.causal_contribution.exists():
        print("  contribution:  {0}".format(_rel(layout.causal_contribution)))
    failures = result.get("failures", []) if isinstance(result, Mapping) else []
    for failure in failures:
        print("  replay failed: {0}".format(failure), file=sys.stderr)
    return EXIT_FAILED if failures else EXIT_OK


# ---------------------------------------------------------------------------
# cdf evaluate
# ---------------------------------------------------------------------------


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Score a recorded run against the privileged ground truth."""
    layout = _require_run_dir(args.run)
    cfg = resolve_config(overrides=args.config_overrides, run_dir=layout.root)

    hook = _load_hook(_EVALUATION_HOOKS)
    delegation_error = None  # type: Optional[str]
    metrics = None  # type: Optional[Any]
    if hook is not None:
        try:
            metrics = hook(layout.root, cfg)
        except Exception as exc:  # noqa: BLE001 - reported, then degraded deliberately
            # The dedicated evaluator is the richer of the two; when it breaks,
            # the command's guarantee (a metrics.json built from real artifacts)
            # is still met by the built-in comparison. The failure is shouted on
            # stderr and recorded inside metrics.json so it cannot pass unnoticed.
            delegation_error = "{0}: {1}".format(type(exc).__name__, exc)
            LOGGER.exception("the installed evaluator failed")
            print(
                "error: the installed evaluator failed ({0}); falling back to the "
                "built-in comparison".format(delegation_error),
                file=sys.stderr,
            )
            metrics = None
        else:
            if not layout.metrics.exists():
                if not isinstance(metrics, Mapping):
                    raise CliError(
                        "the installed evaluator returned {0} and wrote no {1}; it "
                        "must either persist the metrics itself or return a "
                        "mapping".format(type(metrics).__name__, _rel(layout.metrics))
                    )
                layout.evaluation_dir.mkdir(parents=True, exist_ok=True)
                write_json(layout.metrics, metrics)

    if metrics is None:
        metrics = _builtin_evaluate(layout, cfg)
        if delegation_error is not None:
            metrics["delegation_error"] = delegation_error
            metrics["notes"].append(
                "the installed evaluator raised {0}; these numbers come from the "
                "built-in comparison".format(delegation_error)
            )
        layout.evaluation_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.metrics, metrics)

    _print_evaluation(layout, metrics if isinstance(metrics, Mapping) else read_json(layout.metrics))
    print("  metrics: {0}".format(_rel(layout.metrics)))
    return EXIT_OK


def _print_evaluation(layout: RunLayout, metrics: Mapping[str, Any]) -> None:
    """Print the headline numbers of an evaluation, whoever computed them.

    Written against what a metrics document *contains* rather than against one
    producer's schema: the dedicated evaluation suite and the built-in fallback
    describe the same run with different block names, and a reader should not
    have to care which one ran.
    """
    print("evaluation of {0}".format(_rel(layout.root)))

    outcome = metrics.get("outcome")
    if isinstance(outcome, Mapping):
        print("  outcome: predicted {0}, truth {1} -> {2}".format(
            outcome.get("predicted"),
            outcome.get("truth"),
            "correct" if outcome.get("correct") else "WRONG",
        ))
    elif outcome:
        print("  outcome: {0}".format(outcome))

    timing = metrics.get("collision_timing")
    if isinstance(timing, Mapping) and timing.get("abs_error_s") is not None:
        print("  collision time: predicted {0:.2f}s, truth {1:.2f}s, error {2:.3f}s".format(
            float(timing["predicted_t"]), float(timing["truth_t"]), float(timing["abs_error_s"])
        ))

    assoc = metrics.get("association")
    if isinstance(assoc, Mapping):
        total = assoc.get("n_assignments", assoc.get("n_scorable", assoc.get("n_tracks")))
        if total is not None and assoc.get("n_correct") is not None:
            print("  track association: {0}/{1} correct (precision {2:.2f}, recall {3:.2f})".format(
                assoc.get("n_correct", 0),
                total,
                float(assoc.get("precision", 0.0)),
                float(assoc.get("recall", 0.0)),
            ))

    benefit = metrics.get("fusion_benefit")
    if isinstance(benefit, Mapping) and benefit.get("fused"):
        print("  causal graph vs oracle: fused edge F1 {0:.3f}, best local ({1}) {2:.3f}, "
              "delta {3:+.3f}".format(
                  float(benefit["fused"].get("edge_f1", 0.0)),
                  benefit.get("best_local_participant_id", "?"),
                  float((benefit.get("best_local") or {}).get("edge_f1", 0.0)),
                  float(benefit.get("delta_edge_f1", 0.0)),
              ))
    versus = metrics.get("causal_graph_vs_oracle")
    if isinstance(versus, Mapping) and versus.get("fused"):
        best = versus.get("best_single_local", {})
        print("  causal graph vs oracle: fused edge F1 {0:.3f}, best local ({1}) {2:.3f}, "
              "delta {3:+.3f}".format(
                  float(versus["fused"].get("edge_f1", 0.0)),
                  best.get("participant_id", "?"),
                  float(best.get("metrics", {}).get("edge_f1", 0.0)),
                  float(versus.get("delta_edge_f1", 0.0)),
              ))

    checks = metrics.get("model_check") or metrics.get("model_checking")
    if isinstance(checks, Mapping):
        summary = checks.get("summary", checks)
        if isinstance(summary, Mapping) and "PASS" in summary:
            print("  model checking: {0} PASS / {1} FAIL / {2} UNKNOWN".format(
                summary.get("PASS", 0), summary.get("FAIL", 0), summary.get("UNKNOWN", 0)
            ))

    for note in metrics.get("notes", []) or []:
        print("  note: {0}".format(note))
    reasons = metrics.get("reasons") or {}
    if isinstance(reasons, Mapping):
        for block in sorted(reasons):
            print("  no {0} block: {1}".format(block, reasons[block]))


# ---------------------------------------------------------------------------
# Built-in evaluation (used when no dedicated evaluator is installed)
# ---------------------------------------------------------------------------


def _load_graph_if(path: Path, scope: Provenance) -> Optional[Any]:
    """Load a graph document if it exists, asserting which layer produced it."""
    from .graph.export import load_graph

    if not path.exists():
        return None
    return load_graph(path, expect_scope=scope)


def _oracle_positions(frames: Sequence[Mapping[str, Any]]) -> Dict[str, List[Tuple[float, float, float]]]:
    """``participant -> [(t, x, y)]`` from the privileged trace, sorted by time."""
    out: Dict[str, List[Tuple[float, float, float]]] = {}
    for frame in frames:
        t = float(frame.get("t", 0.0))
        for actor in frame.get("actors", []) or []:
            pid = actor.get("participant_id")
            if pid is None:
                continue
            out.setdefault(str(pid), []).append((t, float(actor["x"]), float(actor["y"])))
    for samples in out.values():
        samples.sort(key=lambda s: s[0])
    return out


def _position_at(
    samples: Sequence[Tuple[float, float, float]], t: float, max_gap_s: float
) -> Optional[Tuple[float, float]]:
    """Nearest recorded position to ``t``, or ``None`` beyond ``max_gap_s``."""
    import bisect

    if not samples:
        return None
    times = [s[0] for s in samples]
    i = bisect.bisect_left(times, t)
    best = None
    best_d = float("inf")
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(samples):
            d = abs(times[j] - t)
            if d < best_d:
                best, best_d = samples[j], d
    if best is None or best_d > max_gap_s:
        return None
    return (best[1], best[2])


def _true_track_subject(
    track_xy: Sequence[Tuple[float, float, float]],
    oracle_pos: Mapping[str, List[Tuple[float, float, float]]],
    observer_id: str,
    max_distance_m: float,
    max_time_gap_s: float,
    min_vote_ratio: float,
) -> Dict[str, Any]:
    """Which participant a radar track was *really* following, per the oracle.

    Decided by majority vote over the track's samples rather than by a single
    frame: a radar track wanders, and one bad frame near two vehicles must not be
    able to relabel the whole track. A track that matches nobody within
    ``max_distance_m`` (clutter, a non-participant object) correctly yields
    ``None`` -- that is a real answer, not a failure.
    """
    votes: Dict[str, int] = {}
    distances: Dict[str, List[float]] = {}
    n_comparable = 0
    for t, gx, gy in track_xy:
        best_pid = None
        best_d = float("inf")
        for pid, samples in oracle_pos.items():
            if pid == observer_id:
                continue
            pos = _position_at(samples, t, max_time_gap_s)
            if pos is None:
                continue
            d = ((pos[0] - gx) ** 2 + (pos[1] - gy) ** 2) ** 0.5
            if d < best_d:
                best_pid, best_d = pid, d
        if best_pid is None:
            continue
        n_comparable += 1
        if best_d <= max_distance_m:
            votes[best_pid] = votes.get(best_pid, 0) + 1
            distances.setdefault(best_pid, []).append(best_d)

    if not votes or n_comparable == 0:
        return {
            "true_participant": None,
            "n_samples": len(track_xy),
            "n_comparable": n_comparable,
            "vote_ratio": 0.0,
            "mean_distance_m": None,
        }
    winner = sorted(votes.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
    ratio = float(votes[winner]) / float(n_comparable)
    mean_d = sum(distances[winner]) / float(len(distances[winner]))
    return {
        "true_participant": winner if ratio >= min_vote_ratio else None,
        "n_samples": len(track_xy),
        "n_comparable": n_comparable,
        "vote_ratio": ratio,
        "mean_distance_m": mean_d,
        "votes": dict(sorted(votes.items())),
    }


def _evaluate_association(
    layout: RunLayout, cfg: Config, run: Any, frames: Sequence[Mapping[str, Any]]
) -> Dict[str, Any]:
    """Score the fusion layer's track-to-participant decisions against truth."""
    from .graph.metrics import prf1

    if not layout.association_report.exists():
        return {"available": False, "reason": "no fusion/association_report.json; run `cdf fuse`"}
    if not frames:
        return {"available": False, "reason": "no oracle trace; ground truth unavailable"}

    report = read_json(layout.association_report)
    assignments = report.get("assignments", []) or []
    oracle_pos = _oracle_positions(frames)

    max_distance_m = float(
        cfg.get(
            "evaluation.association.max_match_distance_m",
            cfg.get("fusion.track_association.max_rmse_m", 6.0),
        )
    )
    max_time_gap_s = float(
        cfg.get(
            "evaluation.association.max_time_gap_s",
            2.0 * float(cfg.get("simulation.fixed_delta_seconds", 0.05)),
        )
    )
    min_vote_ratio = float(cfg.get("evaluation.association.min_vote_ratio", 0.5))
    count_unresolved_as_miss = bool(cfg.get("evaluation.association.count_unresolved_as_miss", True))

    rows: List[Dict[str, Any]] = []
    tp = fp = fn = 0
    n_correct = 0
    for item in assignments:
        observer = str(item.get("observer_id", ""))
        track_id = str(item.get("track_id", ""))
        status = str(item.get("status", "UNRESOLVED"))
        assigned = item.get("assigned_participant")
        if observer not in run.participants:
            raise CliError(
                "association report names observer {0!r}, which has no evidence "
                "under {1}".format(observer, layout.root)
            )
        t, gx, gy = run.get(observer).track_trajectory(track_id)
        truth = _true_track_subject(
            list(zip(t, gx, gy)),
            oracle_pos,
            observer,
            max_distance_m=max_distance_m,
            max_time_gap_s=max_time_gap_s,
            min_vote_ratio=min_vote_ratio,
        )
        true_pid = truth["true_participant"]
        correct = bool(assigned is not None and assigned == true_pid)
        if correct:
            tp += 1
            n_correct += 1
        elif assigned is not None:
            # An assignment that names the wrong participant (or names one for a
            # track that followed nobody) is both a wrong claim and a miss.
            fp += 1
            if true_pid is not None:
                fn += 1
        elif true_pid is not None and count_unresolved_as_miss:
            fn += 1
        rows.append(
            {
                "track_id": track_id,
                "observer_id": observer,
                "status": status,
                "assigned_participant": assigned,
                "true_participant": true_pid,
                "correct": correct,
                "confidence": item.get("confidence"),
                "rmse_m": item.get("rmse_m"),
                "n_track_samples": truth["n_samples"],
                "vote_ratio": truth["vote_ratio"],
                "mean_distance_m": truth["mean_distance_m"],
            }
        )

    scores = prf1(tp, fp, fn)
    n_tracks_on_disk = sum(len(run.get(pid).track_ids()) for pid in run.participant_ids)
    out: Dict[str, Any] = {
        "available": True,
        "n_assignments": len(rows),
        "n_tracks_recorded": n_tracks_on_disk,
        "n_correct": n_correct,
        "n_true_positive": tp,
        "n_false_positive": fp,
        "n_false_negative": fn,
        "n_without_ground_truth": sum(1 for r in rows if r["true_participant"] is None),
        "accuracy": float(n_correct) / float(len(rows)) if rows else 0.0,
        "assignments": rows,
        "thresholds": {
            "max_match_distance_m": max_distance_m,
            "max_time_gap_s": max_time_gap_s,
            "min_vote_ratio": min_vote_ratio,
            "count_unresolved_as_miss": count_unresolved_as_miss,
        },
    }
    out.update(scores)
    return out


def _collision_events(events: Sequence[Any]) -> List[Any]:
    return [e for e in events if e.event_type == EventType.COLLISION]


def _predicted_outcome(fused: Optional[Any], run: Any) -> Dict[str, Any]:
    """Outcome class implied by the non-privileged reconstruction.

    The fused graph is preferred when it exists because it is the system's final
    claim; otherwise the union of the local event lists is used. Either way the
    decision uses only onboard-derived evidence.
    """
    if fused is not None:
        events = list(fused.nodes)
        source = "fused_causal_graph"
    else:
        events = [e for pid in run.participant_ids for e in run.get(pid).events]
        source = "local_events"
    collisions = _collision_events(events)
    if collisions:
        predicted = OutcomeClass.COLLISION.value
    elif any(e.event_type == EventType.NEAR_MISS for e in events):
        predicted = OutcomeClass.NEAR_MISS.value
    else:
        predicted = OutcomeClass.NO_EVENT.value
    t_pred = min((float(e.t_peak) for e in collisions), default=None)
    return {"predicted": predicted, "source": source, "predicted_collision_t": t_pred}


def _builtin_evaluate(layout: RunLayout, cfg: Config) -> Dict[str, Any]:
    """Score a run from the artifacts that are actually on disk.

    This is the fallback used when no dedicated evaluation module is installed.
    It deliberately reports *which* comparisons were possible: without an oracle
    causal graph there is no reference to score graph structure against, and
    saying so is the honest alternative to inventing a baseline. Everything it
    does report -- outcome class, collision timing, track-association accuracy,
    fusion knowledge gain -- is computed from the run's own artifacts and the
    privileged oracle trace.
    """
    from .common.evidence import load_run
    from .graph.analysis import GraphAnalyzer

    manifest: Dict[str, Any] = read_json(layout.manifest) if layout.manifest.exists() else {}
    run = load_run(layout.root, with_radar=False)
    notes: List[str] = []

    oracle_summary_path = layout.oracle_dir / "oracle_summary.json"
    oracle_summary: Dict[str, Any] = (
        read_json(oracle_summary_path) if oracle_summary_path.exists() else {}
    )
    frames: List[Dict[str, Any]] = (
        read_jsonl_gz(layout.oracle_trace) if layout.oracle_trace.exists() else []
    )
    if not oracle_summary:
        notes.append("no oracle/oracle_summary.json: outcome truth falls back to the manifest")
    if not frames:
        notes.append("no oracle/oracle_trace.jsonl.gz: association accuracy unavailable")

    fused = _load_graph_if(layout.fused_causal_graph, Provenance.FUSED)
    if fused is None:
        notes.append("no fused causal graph: reporting the local reconstructions only")
    local_graphs: Dict[str, Any] = {}
    for pid in run.participant_ids:
        doc = _load_graph_if(layout.causal_graph(pid), Provenance.LOCAL)
        if doc is not None:
            local_graphs[pid] = doc
    oracle_graph = _load_graph_if(layout.oracle_causal_graph, Provenance.ORACLE)

    subject_map: Dict[str, str] = {}
    if layout.fusion_diagnostics.exists():
        diagnostics = read_json(layout.fusion_diagnostics)
        subject_map = dict(diagnostics.get("subject_map", {}) or {})

    # -- outcome ----------------------------------------------------------
    predicted = _predicted_outcome(fused, run)
    collision_pairs = oracle_summary.get("collision_pairs", []) or []
    if collision_pairs:
        truth_outcome = OutcomeClass.COLLISION.value
    elif manifest.get("outcome"):
        truth_outcome = str(manifest["outcome"])
    else:
        truth_outcome = OutcomeClass.NO_EVENT.value
    truth_t = min((float(p["t"]) for p in collision_pairs), default=None)

    outcome_block = {
        "predicted": predicted["predicted"],
        "truth": truth_outcome,
        "correct": predicted["predicted"] == truth_outcome,
        "source": predicted["source"],
        "truth_source": "oracle_summary" if collision_pairs else "manifest",
    }
    t_pred = predicted["predicted_collision_t"]
    timing_block: Dict[str, Any] = {
        "predicted_t": t_pred,
        "truth_t": truth_t,
        "abs_error_s": (abs(t_pred - truth_t) if (t_pred is not None and truth_t is not None) else None),
        "signed_error_s": ((t_pred - truth_t) if (t_pred is not None and truth_t is not None) else None),
    }

    # -- graphs -----------------------------------------------------------
    graphs_block: Dict[str, Any] = {
        "local": {
            pid: {
                "n_nodes": len(doc.nodes),
                "n_edges": len(doc.edges),
                "n_outcome_nodes": len(GraphAnalyzer(doc, cfg).outcome_nodes()),
            }
            for pid, doc in sorted(local_graphs.items())
        },
        "fused": (
            {
                "n_nodes": len(fused.nodes),
                "n_edges": len(fused.edges),
                "n_outcome_nodes": len(GraphAnalyzer(fused, cfg).outcome_nodes()),
            }
            if fused is not None
            else None
        ),
    }

    fusion_gain: Dict[str, Any] = {}
    if fused is not None and local_graphs:
        analyzer = GraphAnalyzer(fused, cfg)
        for pid, doc in sorted(local_graphs.items()):
            diff = analyzer.compare_to(doc, subject_map_other=subject_map)
            fusion_gain[pid] = {
                "n_nodes_only_fused": diff["n_nodes_only_self"],
                "n_nodes_only_local": diff["n_nodes_only_other"],
                "n_nodes_shared": diff["n_nodes_both"],
                "n_edges_only_fused": diff["n_edges_only_self"],
                "n_edges_only_local": diff["n_edges_only_other"],
                "n_edges_shared": diff["n_edges_both"],
                "time_bucket_s": diff["time_bucket_s"],
            }

    metrics: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSIONS["evaluation"],
        "evaluator": "cdf.cli builtin",
        "run_dir": layout.root.name,
        "run_id": str(manifest.get("run_id", "")),
        "scenario_id": str(manifest.get("scenario_id", "")),
        "seed": int(manifest.get("seed", 0)),
        "variant": str(manifest.get("variant", "")),
        "config_hash": cfg.hash,
        "participants": run.participant_ids,
        "reference": {
            "oracle_summary": bool(oracle_summary),
            "oracle_trace": bool(frames),
            "oracle_causal_graph": oracle_graph is not None,
            "oracle_events": layout.oracle_events.exists(),
            "fused_causal_graph": fused is not None,
        },
        "outcome": outcome_block,
        "collision_timing": timing_block,
        "association": _evaluate_association(layout, cfg, run, frames),
        "graphs": graphs_block,
        "fusion_knowledge_gain": fusion_gain,
        "notes": notes,
    }

    tolerance_s = float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5))
    require_same_type = bool(cfg.get("evaluation.event_match.require_same_type", True))
    metrics["event_match"] = {
        "time_tolerance_s": tolerance_s,
        "require_same_type": require_same_type,
        "use_matched_nodes_only": bool(cfg.get("evaluation.graph_match.use_matched_nodes_only", False)),
    }

    if oracle_graph is not None and local_graphs and fused is not None:
        metrics["causal_graph_vs_oracle"] = _evaluate_against_oracle_graph(
            layout, cfg, local_graphs, fused, oracle_graph, subject_map
        )
    else:
        notes.append(
            "no oracle causal graph under {0}: graph-structure accuracy was not "
            "computed (install the oracle graph builder and re-run)".format(_rel(layout.oracle_dir))
        )

    if layout.oracle_events.exists():
        metrics["event_detection_vs_oracle"] = _evaluate_events_against_oracle(
            layout, cfg, run, fused, subject_map, tolerance_s, require_same_type
        )

    if layout.model_check_results.exists():
        report = read_json(layout.model_check_results)
        metrics["model_checking"] = {
            "summary": report.get("summary", {}),
            "by_property": {
                pid: block.get("summary", {})
                for pid, block in sorted((report.get("by_property", {}) or {}).items())
            },
        }
    return metrics


def _evaluate_against_oracle_graph(
    layout: RunLayout,
    cfg: Config,
    local_graphs: Mapping[str, Any],
    fused: Any,
    oracle_graph: Any,
    subject_map: Mapping[str, str],
) -> Dict[str, Any]:
    """Score every local graph and the fused graph against the oracle DAG."""
    from .graph.metrics import compare_local_vs_fused

    tolerance_s = float(cfg.get("evaluation.event_match.time_tolerance_s", 1.5))
    comparison = compare_local_vs_fused(
        local_graphs,
        fused,
        oracle_graph,
        tolerance_s=tolerance_s,
        require_same_type=bool(cfg.get("evaluation.event_match.require_same_type", True)),
        subject_maps={pid: subject_map for pid in local_graphs},
        restrict_to_matched_nodes=bool(
            cfg.get("evaluation.graph_match.use_matched_nodes_only", False)
        ),
    )

    fused_metrics = comparison["fused"]
    layout.evaluation_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        layout.event_matches,
        [
            {"pred_event_id": a, "truth_event_id": b, "dt_s": dt}
            for a, b, dt in fused_metrics["node_matches"]
        ],
        columns=("pred_event_id", "truth_event_id", "dt_s"),
    )
    edge_rows: List[Dict[str, Any]] = []
    for kind in ("matched_edges", "missing_edges", "extra_edges", "reversed_edges"):
        for edge in fused_metrics[kind]:
            edge_rows.append({"kind": kind[: -len("_edges")], "edge": edge})
    write_csv(layout.edge_matches, edge_rows, columns=("kind", "edge"))
    return comparison


def _evaluate_events_against_oracle(
    layout: RunLayout,
    cfg: Config,
    run: Any,
    fused: Optional[Any],
    subject_map: Mapping[str, str],
    tolerance_s: float,
    require_same_type: bool,
) -> Dict[str, Any]:
    """Event-detection quality of the local and fused event lists."""
    from .common.schemas import _event_from_dict  # local import: private decoder
    from .graph.metrics import event_metrics

    payload = read_json(layout.oracle_events)
    truth = [_event_from_dict(d) for d in payload.get("events", [])]
    out: Dict[str, Any] = {"n_truth": len(truth), "per_participant": {}}
    for pid in run.participant_ids:
        out["per_participant"][pid] = event_metrics(
            run.get(pid).events,
            truth,
            tolerance_s=tolerance_s,
            require_same_type=require_same_type,
            subject_map_pred=subject_map,
        )
    if fused is not None:
        out["fused"] = event_metrics(
            list(fused.nodes),
            truth,
            tolerance_s=tolerance_s,
            require_same_type=require_same_type,
        )
    return out


# ---------------------------------------------------------------------------
# cdf report
# ---------------------------------------------------------------------------


def _run_kind(run_root: Path, artifacts_root: Path) -> Dict[str, str]:
    """Where a run sits in the artifacts tree, which is what it means.

    A counterfactual replay lives under ``<run>/counterfactual/replays/<id>``
    and an ablation run under ``<artifacts>/ablation/<profile>``. Both carry a
    ``manifest.json`` and are genuine runs, but neither belongs in the campaign
    table: a replay is deliberately a different experiment from the factual run,
    and its scenario validation is checked against the factual expectation, so a
    replay that prevented the collision reports ``FAILED`` when in fact it did
    the one thing the intervention was asked to test.
    """
    try:
        parts = run_root.resolve().relative_to(artifacts_root.resolve()).parts
    except ValueError:
        return {"kind": "primary", "context": "", "intervention": ""}
    if "counterfactual" in parts:
        index = parts.index("counterfactual")
        return {
            "kind": "replay",
            "context": "/".join(parts[:index]),
            "intervention": parts[-1] if len(parts) > index + 2 else "",
        }
    if parts and parts[0] == "ablation":
        return {
            "kind": "ablation",
            "context": parts[1] if len(parts) > 1 else "",
            "intervention": "",
        }
    return {"kind": "primary", "context": "", "intervention": ""}


def _discover_runs(artifacts_root: Path) -> List[RunLayout]:
    """Every run directory under ``artifacts_root``, identified by its manifest."""
    if not artifacts_root.exists():
        raise CliError("artifacts directory does not exist: {0}".format(artifacts_root))
    return [
        RunLayout.from_run_dir(p.parent)
        for p in sorted(artifacts_root.rglob("manifest.json"))
        if p.is_file()
    ]


def _run_row(layout: RunLayout, artifacts_root: Optional[Path] = None) -> Dict[str, Any]:
    """One aggregate row, built only from artifacts that exist on disk."""
    manifest = read_json(layout.manifest)
    placement = _run_kind(layout.root, artifacts_root or layout.root)
    row: Dict[str, Any] = {
        "kind": placement["kind"],
        "context": placement["context"],
        "intervention": placement["intervention"],
        "scenario": str(manifest.get("scenario_id", "")),
        "variant": str(manifest.get("variant", "")),
        "seed": int(manifest.get("seed", 0)),
        "run_id": str(manifest.get("run_id", "")),
        "config_hash": str(manifest.get("config_hash", "")),
        "map": str(manifest.get("map_name", "")),
        "outcome": str(manifest.get("outcome", "")),
        "n_frames": manifest.get("n_frames"),
        "duration_sim_s": manifest.get("duration_sim_s"),
        "n_participants": len(layout.participant_ids()),
        "run_dir": _rel(layout.root),
        "validation": None,
        "n_events": None,
        "n_fused_nodes": None,
        "n_fused_edges": None,
        "tracks_resolved": None,
        "tracks_total": None,
        "checks_pass": None,
        "checks_fail": None,
        "checks_unknown": None,
        "fused_edge_f1": None,
        "best_local_edge_f1": None,
        "delta_edge_f1": None,
        "association_accuracy": None,
    }
    if layout.scenario_validation.exists():
        validation = read_json(layout.scenario_validation)
        row["validation"] = "passed" if validation.get("passed") else "FAILED"

    n_events = 0
    have_events = False
    for pid in layout.participant_ids():
        path = layout.events(pid)
        if path.exists():
            have_events = True
            n_events += len(read_json(path).get("events", []))
    row["n_events"] = n_events if have_events else None

    if layout.fused_causal_graph.exists():
        fused = read_json(layout.fused_causal_graph)
        row["n_fused_nodes"] = len(fused.get("nodes", []))
        row["n_fused_edges"] = len(fused.get("edges", []))
    if layout.association_report.exists():
        report = read_json(layout.association_report)
        counts = report.get("counts", {}) or {}
        row["tracks_resolved"] = counts.get("RESOLVED", 0)
        row["tracks_total"] = sum(int(v) for v in counts.values())
    if layout.model_check_results.exists():
        summary = read_json(layout.model_check_results).get("summary", {}) or {}
        row["checks_pass"] = summary.get("PASS")
        row["checks_fail"] = summary.get("FAIL")
        row["checks_unknown"] = summary.get("UNKNOWN")
    if layout.metrics.exists():
        metrics = read_json(layout.metrics)
        # `graphs` is the current key; `causal_graph_vs_oracle` was its name in
        # earlier artifacts and is still read so that an old run stays legible.
        versus = metrics.get("graphs") or metrics.get("causal_graph_vs_oracle") or {}
        if versus:
            row["fused_edge_f1"] = versus.get("fused", {}).get("edge_f1")
            row["best_local_edge_f1"] = (
                versus.get("best_single_local", {}).get("metrics", {}).get("edge_f1")
            )
            row["delta_edge_f1"] = versus.get("delta_edge_f1")
        association = metrics.get("association") or {}
        if association.get("available"):
            row["association_accuracy"] = association.get("accuracy")
    return row


def _markdown_report(rows: Sequence[Mapping[str, Any]], artifacts_root: Path) -> str:
    """A self-contained Markdown summary of every run found."""
    lines: List[str] = []
    lines.append("# carla-distributed-causal-forensics -- run summary")
    lines.append("")
    lines.append("Artifacts root: `{0}`".format(artifacts_root))
    lines.append("")
    primary = [r for r in rows if r.get("kind", "primary") == "primary"]
    replays = [r for r in rows if r.get("kind") == "replay"]
    ablation = [r for r in rows if r.get("kind") == "ablation"]
    lines.append("{0} recorded run(s), {1} scenario(s).".format(
        len(primary), len({r["scenario"] for r in primary})
    ))
    if replays:
        lines.append("")
        lines.append(
            "{0} counterfactual replay(s) and {1} ablation run(s) are listed "
            "separately below; they are deliberately different experiments and "
            "are not part of the campaign table.".format(len(replays), len(ablation))
        )
    lines.append("")
    header = (
        "| scenario | variant | seed | outcome | validation | events | fused nodes/edges "
        "| tracks resolved | checks P/F/U |"
    )
    lines.append(header)
    lines.append("|---" * 9 + "|")
    for row in primary:
        lines.append(
            "| {0} | {1} | {2} | {3} | {4} | {5} | {6}/{7} | {8}/{9} | {10}/{11}/{12} |".format(
                row["scenario"],
                row["variant"],
                row["seed"],
                row["outcome"] or "-",
                row["validation"] or "-",
                row["n_events"] if row["n_events"] is not None else "-",
                row["n_fused_nodes"] if row["n_fused_nodes"] is not None else "-",
                row["n_fused_edges"] if row["n_fused_edges"] is not None else "-",
                row["tracks_resolved"] if row["tracks_resolved"] is not None else "-",
                row["tracks_total"] if row["tracks_total"] is not None else "-",
                row["checks_pass"] if row["checks_pass"] is not None else "-",
                row["checks_fail"] if row["checks_fail"] is not None else "-",
                row["checks_unknown"] if row["checks_unknown"] is not None else "-",
            )
        )
    lines.append("")
    scored = [r for r in primary if r["delta_edge_f1"] is not None]
    if scored:
        lines.append("## Fused versus best single local reconstruction")
        lines.append("")
        lines.append("| scenario | variant | seed | best local edge F1 | fused edge F1 | delta |")
        lines.append("|---|---|---|---|---|---|")
        for row in scored:
            lines.append("| {0} | {1} | {2} | {3:.3f} | {4:.3f} | {5:+.3f} |".format(
                row["scenario"],
                row["variant"],
                row["seed"],
                float(row["best_local_edge_f1"] or 0.0),
                float(row["fused_edge_f1"] or 0.0),
                float(row["delta_edge_f1"]),
            ))
        lines.append("")
        mean_delta = sum(float(r["delta_edge_f1"]) for r in scored) / float(len(scored))
        lines.append("Mean delta over {0} scored run(s): {1:+.3f}.".format(len(scored), mean_delta))
    else:
        lines.append(
            "No run carries `evaluation/metrics.json` with an oracle graph comparison yet; "
            "run `cdf evaluate --run <run_dir>` after building the oracle graphs."
        )
    lines.append("")

    if replays:
        lines.append("## Counterfactual replays")
        lines.append("")
        lines.append(
            "Each replay re-runs one factual run with exactly one scripted "
            "action changed. `outcome` is the replay's own outcome; a value "
            "differing from the factual run is the finding, not an error. "
            "Scenario validation is intentionally omitted here, because it "
            "checks the *factual* scenario's expected outcome and an effective "
            "intervention is expected to violate it."
        )
        lines.append("")
        lines.append("| factual run | intervention | outcome |")
        lines.append("|---|---|---|")
        for row in sorted(replays, key=lambda r: (r["context"], r["intervention"])):
            lines.append("| {0} | `{1}` | {2} |".format(
                row["context"] or "-", row["intervention"] or "-",
                row["outcome"] or "-"))
        lines.append("")

    if ablation:
        lines.append("## Radar-degradation ablation")
        lines.append("")
        lines.append(
            "The same encounter recorded through a different sensor profile; "
            "the physics is held identical and only what the vehicles could "
            "see differs."
        )
        lines.append("")
        lines.append("| profile | scenario | variant | outcome | validation | events |")
        lines.append("|---|---|---|---|---|---|")
        for row in sorted(ablation, key=lambda r: r["context"]):
            lines.append("| {0} | {1} | {2} | {3} | {4} | {5} |".format(
                row["context"] or "-", row["scenario"], row["variant"],
                row["outcome"] or "-", row["validation"] or "-",
                row["n_events"] if row["n_events"] is not None else "-"))
        lines.append("")

    return "\n".join(lines)


def cmd_report(args: argparse.Namespace) -> int:
    """Aggregate every run under the artifacts root into one summary."""
    cfg = resolve_config(overrides=args.config_overrides)
    artifacts_root = _artifacts_root(args, cfg)
    layouts = _discover_runs(artifacts_root)
    if not layouts:
        raise CliError(
            "no runs found under {0} (a run directory is one containing "
            "manifest.json)".format(artifacts_root)
        )

    rows = [_run_row(layout, artifacts_root) for layout in layouts]
    rows.sort(key=lambda r: (r["scenario"], r["variant"], r["seed"]))

    # The campaign tables belong to the evaluation layer when it is installed;
    # this command then only adds the human-readable Markdown on top, so that
    # there is exactly one authoritative summary directory per artifacts root.
    hook = _load_hook(_AGGREGATE_HOOKS)
    aggregated: Optional[Mapping[str, Any]] = None
    out_dir: Optional[Path] = Path(args.out).expanduser() if args.out else None
    if hook is not None:
        result = hook(artifacts_root, cfg)
        aggregated = result if isinstance(result, Mapping) else None
        if out_dir is None:
            out_dir = _summary_dir(artifacts_root)
    if out_dir is None:
        out_dir = artifacts_root / "report"
    out_dir.mkdir(parents=True, exist_ok=True)

    written: List[str] = []
    if aggregated is None:
        write_json(
            out_dir / "summary.json",
            {
                "schema_version": SCHEMA_VERSIONS["evaluation"],
                "artifacts_root": str(artifacts_root),
                "n_runs": len(rows),
                "scenarios": sorted({r["scenario"] for r in rows}),
                "runs": rows,
            },
        )
        write_csv(
            out_dir / "summary.csv",
            rows,
            columns=(
                "kind", "context", "intervention",
                "scenario", "variant", "seed", "map", "outcome", "validation",
                "n_participants", "n_events", "n_fused_nodes", "n_fused_edges",
                "tracks_resolved", "tracks_total", "checks_pass", "checks_fail",
                "checks_unknown", "best_local_edge_f1", "fused_edge_f1", "delta_edge_f1",
                "association_accuracy", "config_hash", "run_dir",
            ),
        )
        written.extend(["summary.json", "summary.csv"])
    # Campaign figures. They read only the aggregate artifacts just written, so a
    # figure can always be re-derived from the summary directory alone.
    figures_module = _maybe_import("cdf.evaluation.figures")
    if figures_module is not None and hasattr(figures_module, "render_summary_figures"):
        try:
            made = figures_module.render_summary_figures(artifacts_root, cfg)
            written.extend(sorted(str(Path(p).name) for p in made))
        except Exception as exc:  # noqa: BLE001 - reported, never silently skipped
            LOGGER.warning("campaign figures could not be rendered: %s", exc)

    # Explicit newline so the report is byte-identical on every platform.
    with open(str(out_dir / "report.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(_markdown_report(rows, artifacts_root))
    written.append("report.md")

    n_primary = sum(1 for r in rows if r.get("kind", "primary") == "primary")
    print("aggregated {0} recorded run(s) ({1} replay/ablation run(s) kept "
          "separate) under {2}".format(
              n_primary, len(rows) - n_primary, _rel(artifacts_root)))
    _print_table(
        (("scenario", 10), ("variant", 12), ("seed", 5), ("outcome", 11),
         ("validation", 10), ("n_events", 8), ("n_fused_edges", 13)),
        [r for r in rows if r.get("kind", "primary") == "primary"],
    )
    print("")
    if aggregated is not None:
        missing = aggregated.get("runs_without_metrics", []) or []
        if missing:
            print("  {0} run(s) carry no evaluation/metrics.json yet".format(len(missing)))
        for name in sorted(str(f) for f in aggregated.get("files", []) or []):
            print("  {0}".format(name))
    for name in written:
        print("  {0}".format(_rel(out_dir / name)))
    return EXIT_OK


def _summary_dir(artifacts_root: Path) -> Path:
    """Campaign-level output directory, as the evaluation layer defines it."""
    module = _maybe_import("cdf.evaluation.suite")
    if module is not None and hasattr(module, "summary_dir"):
        return Path(module.summary_dir(artifacts_root))
    return artifacts_root / "summary"


# ---------------------------------------------------------------------------
# cdf viewer
# ---------------------------------------------------------------------------


def _viewer_source_dir() -> Path:
    """Repository directory holding the static viewer assets."""
    module = _maybe_import("cdf.viewer.bundle")
    if module is not None and hasattr(module, "viewer_assets_dir"):
        return Path(module.viewer_assets_dir())
    return repo_root() / "viewer"


def _stage_viewer_assets(layout: RunLayout, cfg: Config) -> Path:
    """Put the page next to the data and return the directory to serve.

    The page fetches ``run_data.json`` relative to itself, so the two have to sit
    together; serving the run's own ``viewer/`` directory (rather than the
    repository's) also means the served tree is exactly what an archived run
    contains. A missing bundle is built here when the writer is installed,
    because "serve the viewer for this run" should not fail on a step the tool
    can perform itself.
    """
    module = _maybe_import("cdf.viewer.bundle")
    assets = getattr(module, "VIEWER_ASSETS", VIEWER_ASSETS) if module else VIEWER_ASSETS
    source = _viewer_source_dir()
    missing = [name for name in assets if not (source / name).exists()]
    if missing:
        raise CliError(
            "the static viewer is incomplete: {0} missing from {1}".format(
                ", ".join(missing), source
            )
        )

    if not layout.viewer_bundle.exists():
        if module is None or not hasattr(module, "write_bundle"):
            raise CliError(
                "no viewer bundle at {0} and no bundle writer installed; produce "
                "one with `cdf run`".format(layout.viewer_bundle)
            )
        module.write_bundle(layout.root, cfg)
        print("built the missing bundle {0}".format(_rel(layout.viewer_bundle)))

    layout.viewer_dir.mkdir(parents=True, exist_ok=True)
    if module is not None and hasattr(module, "install_viewer_assets"):
        module.install_viewer_assets(layout.viewer_dir)
    else:
        for name in assets:
            shutil.copyfile(str(source / name), str(layout.viewer_dir / name))
    return layout.viewer_dir


def cmd_viewer(args: argparse.Namespace) -> int:
    """Serve one run's forensic viewer on the loopback interface."""
    import webbrowser
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

    layout = _require_run_dir(args.run)
    cfg = resolve_config(overrides=args.config_overrides, run_dir=layout.root)
    directory = _stage_viewer_assets(layout, cfg)

    class _Handler(SimpleHTTPRequestHandler):
        """Serves the run's viewer directory and logs through the CLI logger."""

        def __init__(self, *handler_args: Any, **handler_kwargs: Any) -> None:
            handler_kwargs["directory"] = str(directory)
            super(_Handler, self).__init__(*handler_args, **handler_kwargs)

        def log_message(self, fmt: str, *fmt_args: Any) -> None:
            LOGGER.debug("viewer %s - %s", self.address_string(), fmt % fmt_args)

    # Loopback only, always: a run directory contains a complete reconstruction
    # of an incident and has no business being reachable from the network.
    host = "127.0.0.1"
    try:
        server = ThreadingHTTPServer((host, int(args.port)), _Handler)
    except OSError as exc:
        raise CliError(
            "cannot bind {0}:{1} ({2}); pass --port with a free port "
            "(--port 0 picks one)".format(host, args.port, exc)
        )
    port = server.server_address[1]
    url = "http://{0}:{1}/index.html".format(host, port)
    print("serving {0}".format(_rel(directory)))
    print("  {0}".format(url))
    print("  press Ctrl+C to stop")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("viewer stopped")
    finally:
        server.server_close()
    return EXIT_OK


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def _positive_float(value: str) -> float:
    """Parse a strictly positive floating-point CLI value."""
    try:
        parsed = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a number greater than zero") from exc
    if parsed <= 0.0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def _common_parser() -> argparse.ArgumentParser:
    """Options every subcommand shares."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--config-overrides",
        dest="config_overrides",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="override one configuration value, e.g. "
        "--config-overrides events.radar.critical_ttc.ttc_s=2.0 (repeatable)",
    )
    common.add_argument(
        "--artifacts",
        default=None,
        metavar="DIR",
        help="artifacts root (default: output.artifacts_root from the configuration)",
    )
    common.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="-v for INFO logging on stderr, -vv for DEBUG",
    )
    return common


def build_parser() -> argparse.ArgumentParser:
    """The full argument parser, including every subcommand."""
    common = _common_parser()
    parser = argparse.ArgumentParser(
        prog="cdf",
        description=(
            "Distributed multi-vehicle causal forensics for CARLA: record runs, "
            "build local and fused causal graphs, check, evaluate and report."
        ),
        parents=[common],
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    env = subparsers.add_parser(
        "env",
        parents=[common],
        help="inspect the Python and CARLA environment",
        description="Report interpreter, dependencies, simulator and host resources.",
    )
    env.add_argument(
        "--start-server",
        action="store_true",
        help="start a CARLA server from the detected installation and wait for it",
    )
    env.set_defaults(func=cmd_env)

    run = subparsers.add_parser(
        "run",
        parents=[common],
        help="record one scenario run and analyse it",
        description=(
            "Record one scenario run, then (unless disabled) run local analysis, "
            "fusion, the oracle graph build, model checking and the viewer bundle."
        ),
    )
    run.add_argument("--scenario", required=True, help="scenario id, e.g. S01")
    run.add_argument("--seed", type=int, default=0, help="random seed (default: 0)")
    run.add_argument(
        "--variant", default=None, help="scenario variant (default: the scenario's own default)"
    )
    run.add_argument(
        "--live",
        action="store_true",
        help="show the running scenario through CARLA's native spectator",
    )
    run.add_argument(
        "--realtime",
        action="store_true",
        help="pace a live run to simulated wall-clock time",
    )
    run.add_argument(
        "--playback-speed",
        type=_positive_float,
        default=1.0,
        metavar="FLOAT",
        help="live playback multiplier (default: 1.0; requires --realtime)",
    )
    run.add_argument(
        "--spectator",
        choices=("overhead", "follow"),
        default="overhead",
        help="live spectator mode (default: overhead)",
    )
    run.add_argument(
        "--follow-vehicle",
        choices=("A", "B", "C"),
        default="A",
        help="participant for --spectator follow (default: A)",
    )
    run.add_argument(
        "--spectator-height",
        type=_positive_float,
        default=35.0,
        metavar="FLOAT",
        help="spectator height in metres (default: 35)",
    )
    run.add_argument(
        "--no-labels",
        action="store_true",
        help="do not draw A/B/C labels above participant vehicles",
    )
    run.add_argument("--no-analyse", action="store_true", help="skip local analysis")
    run.add_argument("--no-fuse", action="store_true", help="skip fusion")
    run.add_argument("--no-check", action="store_true", help="skip model checking")
    run.add_argument("--no-viewer", action="store_true", help="skip the viewer bundle")
    run.set_defaults(func=cmd_run)

    suite = subparsers.add_parser(
        "suite",
        parents=[common],
        help="run many scenarios and seeds in one process",
        description=(
            "Run several scenarios and seeds reusing a single simulator session. "
            "Runs are grouped by map so the server performs as few map switches "
            "as possible."
        ),
    )
    suite.add_argument("--all", action="store_true", help="run every scenario in configs/scenarios")
    suite.add_argument(
        "--all-variants",
        action="store_true",
        help="run every variant each scenario declares (the experimental campaign)",
    )
    suite.add_argument(
        "--scenarios", nargs="+", default=None, metavar="ID", help="explicit scenario ids"
    )
    suite.add_argument(
        "--seeds", nargs="+", type=int, default=[0], metavar="N", help="seeds (default: 0)"
    )
    suite.add_argument(
        "--variants",
        nargs="+",
        default=None,
        metavar="NAME",
        help="variants to run for every scenario (default: each scenario's own default)",
    )
    suite.add_argument(
        "--continue-on-error",
        action="store_true",
        help="keep going after a failing run and report success if the suite completed",
    )
    suite.add_argument("--no-analyse", action="store_true", help="skip local analysis")
    suite.add_argument("--no-fuse", action="store_true", help="skip fusion")
    suite.add_argument("--no-check", action="store_true", help="skip model checking")
    suite.add_argument("--no-viewer", action="store_true", help="skip the viewer bundle")
    suite.set_defaults(func=cmd_suite)

    counterfactuals = subparsers.add_parser(
        "counterfactuals",
        parents=[common],
        help="replay a run under scripted interventions",
        description="Replay one recorded run under each candidate intervention.",
    )
    counterfactuals.add_argument("--run", required=True, metavar="DIR", help="run directory")
    counterfactuals.set_defaults(func=cmd_counterfactuals)

    evaluate = subparsers.add_parser(
        "evaluate",
        parents=[common],
        help="score a run against the privileged ground truth",
        description=(
            "Compare the local and fused reconstructions of one run against the "
            "oracle and write evaluation/metrics.json."
        ),
    )
    evaluate.add_argument("--run", required=True, metavar="DIR", help="run directory")
    evaluate.set_defaults(func=cmd_evaluate)

    report = subparsers.add_parser(
        "report",
        parents=[common],
        help="aggregate every run under the artifacts root",
        description="Aggregate all runs into summary.json, summary.csv and report.md.",
    )
    report.add_argument(
        "--out", default=None, metavar="DIR", help="output directory (default: <artifacts>/report)"
    )
    report.set_defaults(func=cmd_report)

    viewer = subparsers.add_parser(
        "viewer",
        parents=[common],
        help="serve one run's forensic viewer",
        description="Serve the viewer for one run on 127.0.0.1 and print its URL.",
    )
    viewer.add_argument("--run", required=True, metavar="DIR", help="run directory")
    viewer.add_argument("--port", type=int, default=8000, help="TCP port (default: 8000, 0 picks one)")
    viewer.add_argument("--no-browser", action="store_true", help="do not open a browser")
    viewer.set_defaults(func=cmd_viewer)

    analyse = subparsers.add_parser(
        "analyse",
        parents=[common],
        help="re-run local inference over a recorded run",
        description="Rebuild every participant's events, event graph and causal DAG.",
    )
    analyse.add_argument("--run", required=True, metavar="DIR", help="run directory")
    analyse.set_defaults(func=cmd_analyse)

    fuse = subparsers.add_parser(
        "fuse",
        parents=[common],
        help="re-run fusion over a recorded run",
        description="Rebuild the association report and the fused graphs.",
    )
    fuse.add_argument("--run", required=True, metavar="DIR", help="run directory")
    fuse.set_defaults(func=cmd_fuse)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

#: Errors that mean "the job could not be done", as opposed to a bug in the
#: pipeline. They are reported as one actionable line instead of a traceback.
_OPERATIONAL_ERRORS: Tuple[type, ...] = (
    CliError,
    FileNotFoundError,
    NotADirectoryError,
    PermissionError,
    KeyError,
    ValueError,
)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run one CLI command and return its exit code.

    ``argv`` excludes the program name. :class:`SystemExit` from argparse (bad
    usage, ``--help``) is converted into a return code so that callers -- the
    thin scripts in ``scripts/``, and the test-suite -- always deal with an int.
    """
    parser = build_parser()
    try:
        args = parser.parse_args(list(argv) if argv is not None else None)
    except SystemExit as exc:  # argparse already printed the reason
        return int(exc.code or 0)

    _configure_logging(int(getattr(args, "verbose", 0)))

    if getattr(args, "command", None) is None:
        parser.print_help(sys.stderr)
        print("error: a COMMAND is required", file=sys.stderr)
        return EXIT_USAGE

    try:
        return int(args.func(args))
    except _OPERATIONAL_ERRORS as exc:
        code = getattr(exc, "exit_code", EXIT_USAGE)
        print("error: {0}".format(exc), file=sys.stderr)
        LOGGER.debug("command %s failed", args.command, exc_info=True)
        return int(code)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return EXIT_FAILED


if __name__ == "__main__":  # pragma: no cover - module entry point
    raise SystemExit(main())
