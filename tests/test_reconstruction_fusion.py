"""Graph-level alignment, identity association and the global graph."""

import copy
import tempfile
import unittest
from pathlib import Path

from src.cdf.reconstruction.alignment import align_graphs
from src.cdf.reconstruction.config import FusionConfig, ReconstructionConfig
from src.cdf.reconstruction.models import GraphEdge, GraphNode, LocalGraph
from src.cdf.reconstruction.pipeline import reconstruct_run

from synthetic_run import CONTACT_T, make_run


def _graph(owner, collision_t, impulse):
    brake = GraphNode(owner + ":e01", "BRAKE_START", "ACTION", owner, None, round(collision_t - 2.4, 4),
                      {}, "controls", None)
    collision = GraphNode(owner + ":e02", "COLLISION", "OUTCOME", owner, None, collision_t,
                          {"peak_impulse": impulse}, "collision_sensor", 1.0)
    return LocalGraph(owner=owner, nodes=[brake, collision],
                      edges=[GraphEdge(brake.node_id, collision.node_id, "PRECEDES")])


class AlignmentTests(unittest.TestCase):
    def test_collision_anchor_estimates_an_artificial_clock_offset(self):
        graphs = [_graph("A", 17.32, 900.0), _graph("B", 18.04, 905.0), _graph("C", 3.0, 4000.0)]
        alignment = align_graphs(graphs, FusionConfig())

        self.assertEqual(alignment.reference_event, "collision_001")
        self.assertEqual(alignment.graphs["A"].offset_to_global, -17.32)
        self.assertEqual(alignment.graphs["B"].offset_to_global, -18.04)
        self.assertAlmostEqual(alignment.to_dict()["relative_clock_offsets_s"]["B - A"], 0.72)
        # A's brake 2.4 s before its collision lands 2.4 s before the global anchor.
        self.assertAlmostEqual(alignment.graphs["A"].to_global(14.92), -2.4)
        # C's contact has a different impulse: not the same collision, so no anchor.
        self.assertEqual(alignment.graphs["C"].status, "UNALIGNED")

    def test_alignment_and_fusion_do_not_modify_local_graphs(self):
        graphs = [_graph("A", 17.32, 900.0), _graph("B", 18.04, 900.0)]
        before = copy.deepcopy([graph.to_dict() for graph in graphs])
        align_graphs(graphs, FusionConfig())
        self.assertEqual([graph.to_dict() for graph in graphs], before)

        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp), b_late_start_s=0.72)
            result = reconstruct_run(run, ReconstructionConfig())
            b = next(local for local in result.locals if local.owner == "B")
            b_collision = next(node for node in b.graph.nodes if node.event_type == "COLLISION")
        # B's local graph still reads B's own clock after alignment and fusion.
        self.assertAlmostEqual(b_collision.t_local, CONTACT_T - 0.72, places=3)
        self.assertAlmostEqual(result.alignment.to_dict()["relative_clock_offsets_s"]["B - A"], -0.72, places=3)


class FusionTests(unittest.TestCase):
    def test_matched_collision_becomes_one_global_node_with_provenance(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = reconstruct_run(make_run(Path(tmp), b_late_start_s=0.5), ReconstructionConfig())
        collisions = [node for node in result.graph.nodes if node.event_type == "COLLISION"]
        self.assertEqual(len(collisions), 1)
        node = collisions[0]
        self.assertEqual(node.participants, ["A", "B"])
        self.assertEqual(node.t_global, 0.0)
        provenance = {obs.graph: (obs.local_node, obs.t_local) for obs in node.observations}
        self.assertEqual(set(provenance), {"A", "B"})
        self.assertAlmostEqual(provenance["A"][1], CONTACT_T, places=3)
        self.assertAlmostEqual(provenance["B"][1], CONTACT_T - 0.5, places=3)
        # The anonymous radar track of A is named B only here, at fusion.
        association = result.associations[0]
        self.assertEqual((association.local_graph, association.local_track, association.global_entity,
                          association.status), ("A", "track_001", "B", "ASSOCIATED"))
        self.assertGreater(association.confidence, 0.5)

    def test_track_stays_anonymous_when_evidence_is_weak(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = make_run(Path(tmp), a_sees_b_until=CONTACT_T - 2.0)
            result = reconstruct_run(run, ReconstructionConfig())
        association = result.associations[0]
        self.assertEqual(association.status, "ANONYMOUS")
        self.assertEqual(association.global_entity, "A:track_001")
        self.assertIsNone(association.confidence)
        self.assertTrue(any("lost 2.00 s before the matched collision" in reason for reason in association.blocking))
        subjects = {node.subject_id for node in result.graph.nodes if node.actor_id == "A" and node.subject_id}
        self.assertEqual(subjects, {"A:track_001"})


if __name__ == "__main__":
    unittest.main()
