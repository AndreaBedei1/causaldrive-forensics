"""The graph invariants, checked against every graph actually on disk.

The unit tests prove the builders *maintain* these invariants. This proves the
artifacts *have* them -- every local, fused and oracle causal graph of every
recorded run, replays included. Two properties are asserted, and they are the
two the rest of the project rests on:

**Acyclicity.** A causal DAG with a cycle is not a causal explanation; every
query built on it (ancestors, root causes, all causal paths, the minimal outcome
subgraph, the SCM) either loops or returns nonsense.

**Provenance scope.** `load_graph(path, expect_scope=...)` refuses a graph whose
recorded scope is not the one the caller expects, so loading each artifact under
the scope its location implies is a direct check that no oracle graph is sitting
where a local or fused one belongs -- the failure mode the whole data boundary
exists to prevent.

Skipped when no artifacts are present, so a fresh clone still passes.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import networkx as nx
import pytest

from cdf.common.schemas import Provenance
from cdf.graph.export import load_graph, to_networkx

ARTIFACTS = Path(__file__).resolve().parents[2] / "artifacts"

pytestmark = pytest.mark.skipif(
    not any(ARTIFACTS.glob("*/*/manifest.json")),
    reason="no recorded runs under artifacts/",
)


def _causal_graphs() -> List[Tuple[Path, Provenance]]:
    """Every persisted causal graph, paired with the scope its location implies."""
    found: List[Tuple[Path, Provenance]] = []
    for manifest in sorted(ARTIFACTS.rglob("manifest.json")):
        run = manifest.parent
        for path in sorted(run.glob("vehicle_*/causal_graph.json")):
            found.append((path, Provenance.LOCAL))
        fused = run / "fusion" / "fused_causal_graph.json"
        if fused.exists():
            found.append((fused, Provenance.FUSED))
        oracle = run / "oracle" / "oracle_causal_graph.json"
        if oracle.exists():
            found.append((oracle, Provenance.ORACLE))
    return found


def test_every_recorded_causal_graph_is_a_dag() -> None:
    cyclic: List[str] = []
    checked = 0
    for path, scope in _causal_graphs():
        doc = load_graph(path, expect_scope=scope)
        checked += 1
        graph = to_networkx(doc)
        if not nx.is_directed_acyclic_graph(graph):
            cycle = nx.find_cycle(graph)
            cyclic.append("{0}: {1}".format(path, cycle))
    assert checked, "no causal graphs found; the check would be vacuous"
    assert not cyclic, "causal graphs with cycles: {0}".format(cyclic)


def test_every_recorded_causal_graph_carries_the_scope_its_location_implies() -> None:
    """A graph in the wrong place is the leak the scope guard exists to catch."""
    checked = 0
    for path, scope in _causal_graphs():
        doc = load_graph(path, expect_scope=scope)  # raises on a scope mismatch
        assert doc.scope is scope, "{0} claims scope {1}".format(path, doc.scope)
        assert doc.graph_kind == "causal", "{0} is a {1} graph".format(
            path, doc.graph_kind)
        if scope is Provenance.LOCAL:
            assert doc.owner == path.parent.name.replace("vehicle_", ""), (
                "{0} is owned by {1}".format(path, doc.owner))
        else:
            assert doc.owner is None, "{0} names an owner: {1}".format(path, doc.owner)
        checked += 1
    assert checked, "no causal graphs found; the check would be vacuous"


def test_local_graphs_are_owned_by_exactly_one_participant() -> None:
    """A local graph is one ego's reconstruction; two owners means fusion leaked."""
    offenders: List[str] = []
    for path, scope in _causal_graphs():
        if scope is not Provenance.LOCAL:
            continue
        doc = load_graph(path, expect_scope=scope)
        expected = path.parent.name.replace("vehicle_", "")
        for node in doc.nodes:
            owners = getattr(node, "owner_participant_ids", None) or []
            if owners and sorted(set(owners)) != [expected]:
                offenders.append("{0}: node {1} owned by {2}".format(
                    path, getattr(node, "node_id", "?"), sorted(set(owners))))
    assert not offenders, "local graph nodes with foreign owners: {0}".format(
        offenders[:10])


# ---------------------------------------------------------------------------
# Model-checking artifacts
# ---------------------------------------------------------------------------


def test_no_recorded_fail_has_a_dangling_counterexample() -> None:
    """Every FAIL names a counterexample; that name has to resolve.

    It did not, for the whole first campaign: the results file referenced
    counterexamples that no pipeline ever wrote, so the viewer -- which resolves
    the refs -- showed "counterexample report missing" for all 171 of them.
    """
    import json

    refs = 0
    dangling: List[str] = []
    runs = 0
    for results_path in sorted(ARTIFACTS.rglob("checking/model_check_results.json")):
        runs += 1
        with open(str(results_path), encoding="utf-8") as handle:
            results = json.load(handle)
        cex_path = results_path.parent / "counterexamples.json"
        available = set()
        if cex_path.exists():
            with open(str(cex_path), encoding="utf-8") as handle:
                available = set(json.load(handle).get("counterexamples") or {})
        for result in results.get("results") or []:
            ref = result.get("counterexample_ref")
            if not ref:
                continue
            refs += 1
            if ref not in available:
                dangling.append("{0}: {1}".format(results_path, ref))

    assert runs, "no checking artifacts found; the check would be vacuous"
    assert refs, "no FAIL verdict names a counterexample; the check would be vacuous"
    assert not dangling, "counterexample refs resolving to nothing: {0}".format(
        dangling[:10])


def test_every_recorded_fail_verdict_carries_a_violating_interval() -> None:
    """A FAIL with no interval is a verdict nobody can check."""
    import json

    offenders: List[str] = []
    for results_path in sorted(ARTIFACTS.rglob("checking/model_check_results.json")):
        with open(str(results_path), encoding="utf-8") as handle:
            results = json.load(handle)
        for result in results.get("results") or []:
            if result.get("status") != "FAIL":
                continue
            if not result.get("violating_intervals"):
                offenders.append("{0}: {1}/{2}".format(
                    results_path, result.get("property_id"),
                    result.get("participant_id")))
    assert not offenders, "FAIL verdicts without an interval: {0}".format(offenders[:10])

