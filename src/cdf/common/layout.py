"""Canonical on-disk layout of a run directory.

Every producer and consumer of artifacts resolves paths through :class:`RunLayout`
so that the directory structure is defined exactly once. The layout mirrors the
three-layer boundary: per-participant evidence lives under ``vehicle_<id>/``,
fusion output under ``fusion/``, and privileged ground truth is quarantined under
``oracle/``.

::

    artifacts/S01_rear_end/seed_000/
        manifest.json
        evidence_manifest.json
        vehicle_A/   telemetry.jsonl.gz controls.jsonl.gz radar.jsonl.gz
                     tracks.jsonl.gz triggers.json events.json
                     event_graph.json|.graphml causal_graph.json|.graphml
        vehicle_B/   ...
        fusion/      association_report.json fused_events.json
                     fused_event_graph.json|.graphml
                     fused_causal_graph.json|.graphml fusion_diagnostics.json
        oracle/      oracle_events.json oracle_event_graph.json
                     oracle_causal_graph.json|.graphml
        checking/    model_check_results.json counterexamples.json
        counterfactual/ counterfactual_manifest.json intervention_results.csv
                        causal_contribution.json
        evaluation/  metrics.json event_matches.csv edge_matches.csv
                     attribution_metrics.json
        figures/     *.png
        viewer/      run_data.json
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

__all__ = ["RunLayout", "run_dir_name", "seed_dir_name"]


def run_dir_name(scenario_id: str, scenario_name: str) -> str:
    """Directory name for a scenario, e.g. ``"S01_rear_end"``."""
    return "{0}_{1}".format(scenario_id.upper(), scenario_name)


def seed_dir_name(seed: int, variant: Optional[str] = None) -> str:
    """Directory name for one run, e.g. ``"seed_000"`` or ``"seed_001_crash"``."""
    base = "seed_{0:03d}".format(int(seed))
    if variant and variant != "default":
        return "{0}_{1}".format(base, variant)
    return base


@dataclass(frozen=True)
class RunLayout:
    """Resolved paths for a single run directory.

    Construct with :meth:`create` (which makes the directories) or directly from
    an existing run directory with :meth:`from_run_dir` when only reading.
    """

    root: Path
    """The ``seed_xxx`` directory holding this run."""

    # -- construction -----------------------------------------------------

    @staticmethod
    def from_run_dir(run_dir: Union[str, Path]) -> "RunLayout":
        """Wrap an existing run directory without creating anything."""
        return RunLayout(root=Path(run_dir).resolve())

    @staticmethod
    def create(
        artifacts_root: Union[str, Path],
        scenario_id: str,
        scenario_name: str,
        seed: int,
        variant: Optional[str] = None,
    ) -> "RunLayout":
        """Create (or reuse) the directory tree for a run and return its layout."""
        root = (
            Path(artifacts_root)
            / run_dir_name(scenario_id, scenario_name)
            / seed_dir_name(seed, variant)
        )
        layout = RunLayout(root=root.resolve())
        layout.ensure()
        return layout

    def ensure(self) -> "RunLayout":
        """Create every standard subdirectory."""
        for d in (
            self.root,
            self.fusion_dir,
            self.oracle_dir,
            self.checking_dir,
            self.counterfactual_dir,
            self.evaluation_dir,
            self.figures_dir,
            self.viewer_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)
        return self

    # -- top level --------------------------------------------------------

    @property
    def manifest(self) -> Path:
        return self.root / "manifest.json"

    @property
    def evidence_manifest(self) -> Path:
        return self.root / "evidence_manifest.json"

    @property
    def scenario_validation(self) -> Path:
        return self.root / "scenario_validation.json"

    # -- per participant --------------------------------------------------

    def vehicle_dir(self, participant_id: str) -> Path:
        """Directory holding one participant's local evidence."""
        return self.root / "vehicle_{0}".format(participant_id)

    def telemetry(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "telemetry.jsonl.gz"

    def controls(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "controls.jsonl.gz"

    def radar(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "radar.jsonl.gz"

    def tracks(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "tracks.jsonl.gz"

    def triggers(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "triggers.json"

    def events(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "events.json"

    def event_graph(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "event_graph.json"

    def event_graphml(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "event_graph.graphml"

    def causal_graph(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "causal_graph.json"

    def causal_graphml(self, participant_id: str) -> Path:
        return self.vehicle_dir(participant_id) / "causal_graph.graphml"

    def participant_ids(self) -> List[str]:
        """Participant ids discovered on disk, sorted (``["A", "B", ...]``)."""
        out = []
        for p in sorted(self.root.glob("vehicle_*")):
            if p.is_dir():
                out.append(p.name[len("vehicle_") :])
        return out

    # -- fusion -----------------------------------------------------------

    @property
    def fusion_dir(self) -> Path:
        return self.root / "fusion"

    @property
    def association_report(self) -> Path:
        return self.fusion_dir / "association_report.json"

    @property
    def fused_events(self) -> Path:
        return self.fusion_dir / "fused_events.json"

    @property
    def fused_event_graph(self) -> Path:
        return self.fusion_dir / "fused_event_graph.json"

    @property
    def fused_event_graphml(self) -> Path:
        return self.fusion_dir / "fused_event_graph.graphml"

    @property
    def fused_causal_graph(self) -> Path:
        return self.fusion_dir / "fused_causal_graph.json"

    @property
    def fused_causal_graphml(self) -> Path:
        return self.fusion_dir / "fused_causal_graph.graphml"

    @property
    def fusion_diagnostics(self) -> Path:
        return self.fusion_dir / "fusion_diagnostics.json"

    @property
    def simple_fused_causal_graph(self) -> Path:
        """The union baseline: local graphs merged, nothing inferred.

        Kept beside the global inferred graph rather than derived from it, so
        the ablation between the two compares two things that were each built
        the way they claim to have been built.
        """
        return self.fusion_dir / "simple_fused_causal_graph.json"

    @property
    def simple_fused_causal_graphml(self) -> Path:
        return self.fusion_dir / "simple_fused_causal_graph.graphml"

    @property
    def observable_events(self) -> Path:
        """Privileged ground truth in the vocabulary a reconstruction shares."""
        return self.oracle_dir / "oracle_observable_events.json"

    @property
    def observable_causal_graph(self) -> Path:
        return self.oracle_dir / "oracle_observable_causal_graph.json"

    @property
    def observable_causal_graphml(self) -> Path:
        return self.oracle_dir / "oracle_observable_causal_graph.graphml"

    @property
    def radar_truth(self) -> Path:
        """Exact radar-equivalent geometry for every ordered pair."""
        return self.oracle_dir / "radar_truth.jsonl.gz"

    @property
    def map_context(self) -> Path:
        """Privileged map facts, kept out of the comparable claim."""
        return self.oracle_dir / "map_context.json"

    @property
    def scenario_design_graph(self) -> Path:
        """What the scenario intended, for checking the mechanism executed."""
        return self.oracle_dir / "scenario_design_graph.json"

    @property
    def graph_diff(self) -> Path:
        """Row-by-row comparison of each account with the ground truth."""
        return self.evaluation_dir / "graph_diff.json"

    @property
    def node_matches(self) -> Path:
        return self.evaluation_dir / "node_matches.csv"

    @property
    def knowledge_gain(self) -> Path:
        """Which account first recovered each ground-truth node and edge."""
        return self.evaluation_dir / "knowledge_gain.json"

    @property
    def incident_reconstruction(self) -> Path:
        """What happened, reconstructed from the exchanged logs alone."""
        return self.fusion_dir / "incident_reconstruction.json"

    @property
    def causal_attribution(self) -> Path:
        """Which behaviours contributed, as a hypothesis read off the graph."""
        return self.fusion_dir / "causal_attribution.json"

    # -- oracle (privileged) ----------------------------------------------

    @property
    def oracle_dir(self) -> Path:
        return self.root / "oracle"

    @property
    def oracle_trace(self) -> Path:
        """Privileged full-state trace; never read by local or fused inference."""
        return self.oracle_dir / "oracle_trace.jsonl.gz"

    @property
    def oracle_events(self) -> Path:
        return self.oracle_dir / "oracle_events.json"

    @property
    def oracle_event_graph(self) -> Path:
        return self.oracle_dir / "oracle_event_graph.json"

    @property
    def oracle_causal_graph(self) -> Path:
        return self.oracle_dir / "oracle_causal_graph.json"

    @property
    def oracle_causal_graphml(self) -> Path:
        return self.oracle_dir / "oracle_causal_graph.graphml"

    # -- checking ---------------------------------------------------------

    @property
    def checking_dir(self) -> Path:
        return self.root / "checking"

    @property
    def model_check_results(self) -> Path:
        return self.checking_dir / "model_check_results.json"

    @property
    def counterexamples(self) -> Path:
        return self.checking_dir / "counterexamples.json"

    # -- counterfactual ---------------------------------------------------

    @property
    def counterfactual_dir(self) -> Path:
        return self.root / "counterfactual"

    @property
    def counterfactual_manifest(self) -> Path:
        return self.counterfactual_dir / "counterfactual_manifest.json"

    @property
    def intervention_results(self) -> Path:
        return self.counterfactual_dir / "intervention_results.csv"

    @property
    def causal_contribution(self) -> Path:
        return self.counterfactual_dir / "causal_contribution.json"

    # -- evaluation -------------------------------------------------------

    @property
    def evaluation_dir(self) -> Path:
        return self.root / "evaluation"

    @property
    def metrics(self) -> Path:
        return self.evaluation_dir / "metrics.json"

    @property
    def event_matches(self) -> Path:
        return self.evaluation_dir / "event_matches.csv"

    @property
    def edge_matches(self) -> Path:
        """Edge-by-edge comparison with the observable ground truth.

        This is the primary comparison. The template-based one it replaced is
        retained beside it under :attr:`legacy_template_edge_matches`, because
        the historical numbers should stay readable rather than be overwritten
        by numbers that mean something different.
        """
        return self.evaluation_dir / "edge_matches.csv"

    @property
    def legacy_template_edge_matches(self) -> Path:
        """The superseded comparison against the scenario causal template."""
        return self.evaluation_dir / "legacy_template_edge_matches.csv"

    @property
    def attribution_metrics(self) -> Path:
        return self.evaluation_dir / "attribution_metrics.json"

    # -- presentation -----------------------------------------------------

    @property
    def figures_dir(self) -> Path:
        return self.root / "figures"

    @property
    def viewer_dir(self) -> Path:
        return self.root / "viewer"

    @property
    def viewer_bundle(self) -> Path:
        return self.viewer_dir / "run_data.json"

    def __str__(self) -> str:
        return str(self.root)
