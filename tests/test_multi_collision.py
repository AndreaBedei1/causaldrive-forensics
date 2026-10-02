"""Close multiple collisions: callback segmentation, time-consistent matching, multi-hop
alignment and identity association with every collision partner.

The real-trace tests run in memory (nothing is written to traces/) and use
``ground_truth/`` only to validate the result offline, as the evaluation does.
"""

import copy
import dataclasses
import json
import tempfile
import unittest
from pathlib import Path

from src.cdf.evaluation.reconstruction import _truth_contacts
from src.cdf.reconstruction.alignment import align_graphs
from src.cdf.reconstruction.config import CollisionConfig, FusionConfig, ReconstructionConfig
from src.cdf.reconstruction.fusion import associate_tracks, fuse_graphs, global_temporal_relations
from src.cdf.reconstruction.local import collision_events, number_events, read_jsonl, reconstruct_vehicle
from src.cdf.reconstruction.models import Alignment, GraphEdge, GraphNode, LocalGraph
from src.cdf.reconstruction.pipeline import read_incident_context, reconstruct_run
from src.cdf.reconstruction.tracking import EgoState, EgoTrajectory, ego_trajectory

from synthetic_run import make_run

ROOT = Path(__file__).resolve().parents[1]
CFG = CollisionConfig()
STEP = 0.05


def ego_with_jumps(jumps, duration=4.0):
    """A recorder driving along x at 10 m/s whose velocity jumps by (dvx, dvy) at the given local times."""
    states = []
    for k in range(int(round(duration / STEP)) + 1):
        t = round(k * STEP, 4)
        vx = 10.0 + sum(dv[0] for at, dv in jumps if t >= at - 1e-9)
        vy = sum(dv[1] for at, dv in jumps if t >= at - 1e-9)
        states.append(EgoState(t, 0.0, 0.0, 0.0, vx, vy))
    return EgoTrajectory(states)


def callbacks(*bursts):
    """Raw collision callbacks: (start time, impulses at consecutive samples) per burst."""
    return [{"timestamp": round(start + STEP * k, 4), "impulse": impulse}
            for start, impulses in bursts for k, impulse in enumerate(impulses)]


def contacts(records, ego, cfg=CFG):
    return [(event.t_local, event.attributes) for event in collision_events("B", records, 0.0, cfg, ego)]


class SegmentationTests(unittest.TestCase):
    def test_a_strong_peak_after_a_short_break_opens_a_new_collision(self):
        # The S06 pattern: an impact, 0.25 s without contact, a second impact, then
        # persistent contact (small callbacks after a one-sample break).
        records = callbacks((1.0, [11622.0]), (1.25, [9832.0]), (1.35, [508.0, 1157.0] + [300.0] * 40))
        found = contacts(records, ego_with_jumps([]))
        self.assertEqual([t for t, _ in found], [1.0, 1.25])
        self.assertEqual(found[0][1], {"peak_impulse": 11622.0})
        # The second contact lists the burst it absorbed (persistent contact after a one-sample break).
        self.assertEqual(found[1][1], {"peak_impulse": 9832.0, "new_contact": {"break_s": 0.25, "peak_ratio": 0.85,
                                                                               "evidence": "peak"},
                                       "merged_bursts": [[1.35, 1157.0]]})

    def test_rebounds_and_persistent_contact_stay_one_collision(self):
        # The S16 pattern: a rebound at 43 % of the first impulse, then weaker bursts.
        records = callbacks((1.0, [9096.0]), (1.35, [3883.0]), (1.45, [1407.0] * 4), (1.75, [204.0] * 60))
        jumps = [(1.05, (-6.6, 0.0)), (1.4, (-2.0, 0.0))]  # both push the recorder backwards
        self.assertEqual(contacts(records, ego_with_jumps(jumps)),
                         [(1.0, {"peak_impulse": 9096.0,
                                 "merged_bursts": [[1.35, 3883.0], [1.45, 1407.0], [1.75, 204.0]]})])

    def test_a_scrape_of_weak_bursts_stays_one_collision(self):
        # The S16 A-C pattern: two bodies scraping along each other for 2 s, bursts of 140-320 N*s
        # after one-sample breaks.  Peaks above new_impact_ratio of the contact's peak, but each
        # weaker than min_new_impact_impulse: one collision.
        records = callbacks((1.0, [141.0]), (1.25, [322.0, 158.0, 92.0]), (1.55, [235.0, 173.0]), (2.0, [240.0] * 20))
        found = contacts(records, ego_with_jumps([]))
        self.assertEqual([t for t, _ in found], [1.0])
        self.assertEqual(found[0][1]["peak_impulse"], 322.0)
        self.assertEqual(len(found[0][1]["merged_bursts"]), 3)

    def test_a_strong_rebound_pushing_the_same_way_stays_one_collision(self):
        # The 360-degree S06 A pattern: struck again 0.2 s later with 52 % of the first impulse, and
        # pushed backwards both times: a rebound, although above undirected_impact_ratio.
        records = callbacks((1.0, [11622.0]), (1.2, [6043.0]))
        backwards = ego_with_jumps([(1.05, (-6.4, 0.0)), (1.25, (-5.5, 0.0))])
        self.assertEqual(len(contacts(records, backwards)), 1)
        # Without impact-like jumps to compare (a recorder that barely moves), the peak decides.
        self.assertEqual([t for t, _ in contacts(records, ego_with_jumps([]))], [1.0, 1.2])

    def test_continuous_callbacks_are_never_split(self):
        # No sample without a callback: no real break, whatever the impulses.
        records = callbacks((1.0, [500.0, 600.0, 9000.0, 700.0, 650.0]))
        self.assertEqual(len(contacts(records, ego_with_jumps([]))), 1)

    def test_a_long_pause_always_separates_contacts(self):
        records = callbacks((1.0, [9000.0]), (1.6, [100.0]))
        self.assertEqual([t for t, _ in contacts(records, ego_with_jumps([]))], [1.0, 1.6])

    def test_the_velocity_jumps_decide_between_the_impulse_bands(self):
        # A burst at 30 % of the peak: between min_impact_ratio and new_impact_ratio.
        records = callbacks((1.0, [10000.0]), (1.3, [3000.0]))
        forward_then_back = ego_with_jumps([(1.05, (6.0, 0.0)), (1.35, (-5.0, 0.0))])
        found = contacts(records, forward_then_back)
        self.assertEqual([t for t, _ in found], [1.0, 1.3])
        self.assertEqual(found[1][1]["new_contact"], {"break_s": 0.3, "peak_ratio": 0.3, "reversal_deg": 180,
                                                      "evidence": "reversed velocity jump"})
        # The same jumps in one direction: a rebound, one collision.
        self.assertEqual(len(contacts(records, ego_with_jumps([(1.05, (6.0, 0.0)), (1.35, (5.0, 0.0))]))), 1)
        # Reversed but braking-sized (0.9 m/s over two samples = 9 m/s^2): no direction evidence, and
        # 0.3 is below undirected_impact_ratio: one collision.
        self.assertEqual(len(contacts(records, ego_with_jumps([(1.05, (6.0, 0.0)), (1.35, (-0.9, 0.0))]))), 1)
        # Below min_impact_ratio the velocity evidence is not even considered.
        weak = callbacks((1.0, [10000.0]), (1.3, [2000.0]))
        self.assertEqual(len(contacts(weak, forward_then_back)), 1)
        # From new_impact_ratio a burst is a new impact whatever the direction.
        strong = callbacks((1.0, [10000.0]), (1.3, [8000.0]))
        self.assertEqual(len(contacts(strong, ego_with_jumps([(1.05, (6.0, 0.0)), (1.35, (5.0, 0.0))]))), 2)


def _graph(owner, collisions):
    """A local graph with only COLLISION nodes: (t_local, peak impulse) per report."""
    nodes = [GraphNode("{0}:e{1:02d}".format(owner, index), "COLLISION", "OUTCOME", owner, None, t,
                       {"peak_impulse": impulse}, "collision_sensor", 1.0)
             for index, (t, impulse) in enumerate(collisions, 1)]
    edges = [GraphEdge(a.node_id, b.node_id, "PRECEDES") for a, b in zip(nodes, nodes[1:])]
    return LocalGraph(owner=owner, nodes=nodes, edges=edges)


class MultiHopAlignmentTests(unittest.TestCase):
    def test_a_third_graph_is_aligned_through_a_shared_recorder(self):
        # A-B collide at physical time 0, B-C 0.25 s later; three unrelated local clocks.
        graphs = [_graph("A", [(17.32, 11600.0)]), _graph("B", [(18.04, 11600.0), (18.29, 9800.0)]),
                  _graph("C", [(3.0, 9800.0)])]
        alignment = align_graphs(graphs, FusionConfig())
        clocks = alignment.graphs
        self.assertEqual({name: clock.status for name, clock in clocks.items()},
                         {"A": "ALIGNED", "B": "ALIGNED", "C": "ALIGNED"})
        reference = alignment.reference_event
        self.assertEqual(clocks["A"].chain, [reference])
        self.assertEqual(len(clocks["C"].chain), 2)
        self.assertEqual(clocks["C"].chain[0], reference)
        self.assertAlmostEqual(clocks["C"].to_global(3.0), 0.25)
        self.assertAlmostEqual(clocks["B"].to_global(18.29), 0.25)
        # Relative offsets come from the offsets, not from anchors (C's anchor is another contact).
        self.assertAlmostEqual(alignment.to_dict()["relative_clock_offsets_s"]["C - A"], 3.0 - 17.57)

    def test_matches_must_agree_on_the_clock_offset(self):
        # Two contacts of A and B with equal impulses: 2.0 s apart for A, 1.0 s apart for B.
        # Only one pairing can be the same pair of contacts: the second one is rejected.
        graphs = [_graph("A", [(10.0, 1000.0), (12.0, 1000.0)]), _graph("B", [(20.0, 1000.0), (21.0, 1000.0)])]
        alignment = align_graphs(graphs, FusionConfig())
        self.assertEqual(len(alignment.matched_events), 1)
        self.assertEqual(len(alignment.rejected_matches), 1)
        self.assertIn("clock offset", alignment.rejected_matches[0]["reason"])
        # Consistent offsets (2.0 s apart in both clocks): both contacts match.
        graphs = [_graph("A", [(10.0, 1000.0), (12.0, 1000.0)]), _graph("B", [(20.0, 1000.0), (22.0, 1000.0)])]
        alignment = align_graphs(graphs, FusionConfig())
        self.assertEqual([sorted(event["t_local"].values()) for event in alignment.matched_events],
                         [[10.0, 20.0], [12.0, 22.0]])
        self.assertEqual(alignment.rejected_matches, [])
        self.assertTrue(any("consistent with the clock offset" in line
                            for event in alignment.matched_events for line in event["evidence"]))

    def test_graphs_linked_to_no_aligned_graph_stay_unaligned(self):
        graphs = [_graph("A", [(5.0, 900.0)]), _graph("B", [(6.0, 900.0)]),
                  _graph("C", [(2.0, 4000.0)]), _graph("D", [(9.0, 4000.0)])]
        alignment = align_graphs(graphs, FusionConfig())
        self.assertEqual(alignment.graphs["C"].status, "ALIGNED")  # the strongest contact is the reference
        for name in ("A", "B"):
            self.assertEqual(alignment.graphs[name].status, "UNALIGNED")
            self.assertIn("no graph aligned with the reference", alignment.graphs[name].reason)


def recorded_runs():
    return sorted(run for run in (ROOT / "traces").glob("S*/run_*")
                  if (run / "vehicles").exists() and (run / "ground_truth" / "collisions.jsonl").exists())


def truth_contacts(run):
    """Ground-truth contacts (offline validation only): recorded participants by name."""
    recorded = {path.name for path in (run / "vehicles").iterdir() if path.is_dir()}
    actors = {}
    with (run / "ground_truth" / "states.jsonl").open(encoding="utf-8") as handle:
        for line in handle:
            if '"participant_id"' in line:
                state = json.loads(line)
                actors[state["actor_id"]] = state["participant_id"]
                if set(actors.values()) >= recorded:
                    break
    return _truth_contacts(read_jsonl(run / "ground_truth" / "collisions.jsonl"), actors)


def collision_graphs(run, cfg):
    """Local graphs with only the COLLISION nodes of the raw callbacks (no radar needed)."""
    graphs, origins = [], {}
    for vehicle in sorted(path for path in (run / "vehicles").iterdir() if path.is_dir()):
        ego_records = read_jsonl(vehicle / "ego.jsonl")
        origin = float(ego_records[0]["timestamp"])
        events = collision_events(vehicle.name, read_jsonl(vehicle / "collisions.jsonl"), origin, cfg.collision,
                                  ego_trajectory(ego_records, origin))
        nodes = [GraphNode.from_event(event) for event in number_events(vehicle.name, events)]
        graphs.append(LocalGraph(owner=vehicle.name, nodes=nodes, edges=[]))
        origins[vehicle.name] = origin
    return graphs, origins


class CampaignCollisionTests(unittest.TestCase):
    """Every recorded run of the campaign, against the ground-truth contacts."""

    def test_one_collision_per_true_contact_and_vehicle_contacts_matched_across_recorders(self):
        runs = recorded_runs()
        if not runs:
            self.skipTest("canonical traces not present")
        cfg = ReconstructionConfig()
        for run in runs:
            with self.subTest(run=run.parent.name + "/" + run.name):
                graphs, origins = collision_graphs(run, cfg)
                truth = truth_contacts(run)
                # Per recorder: every COLLISION is a true contact at its true time; every true contact is a
                # COLLISION or a burst that the recorder's sensor merged into one (struck again within it).
                for graph in graphs:
                    reported = [round(node.t_local + origins[graph.owner], 3) for node in graph.nodes]
                    merged = [round(t + origins[graph.owner], 3) for node in graph.nodes
                              for t, _ in node.attributes.get("merged_bursts", [])]
                    expected = sorted(round(contact["sim_time"], 3) for contact in truth
                                      if graph.owner in contact["participants"])
                    self.assertTrue(set(reported) <= set(expected), (graph.owner, reported, expected))
                    self.assertTrue(set(expected) <= set(reported) | set(merged), (graph.owner, reported, expected))
                # Every vehicle-vehicle contact is one matched event of the right pair, nothing else is.
                alignment = align_graphs(graphs, cfg.fusion)
                matched = sorted((sorted(event["graphs"]), round(event["t_local"][event["graphs"][0]]
                                                                  + origins[event["graphs"][0]], 3))
                                 for event in alignment.matched_events)
                between = sorted((contact["participants"], round(contact["sim_time"], 3)) for contact in truth
                                 if "static/unrecorded" not in contact["participants"])
                self.assertEqual(matched, between)
                # Every recorder in a vehicle contact shares the global clock (multi-hop where needed).
                for participants, _ in between:
                    for name in participants:
                        self.assertEqual(alignment.graphs[name].status, "ALIGNED", name)


class S06FrontPushedTests(unittest.TestCase):
    """traces/S06/run_0_a_front_pushed: A, following too closely, strikes B while B is still slowing
    behind C (4.80 s), pushes it into C (5.30 s) and strikes it again 0.15 s later (5.45 s)."""

    RUN = ROOT / "traces" / "S06" / "run_0_a_front_pushed"

    @classmethod
    def setUpClass(cls):
        if not (cls.RUN / "vehicles").exists():
            raise unittest.SkipTest("canonical trace not present")
        cls.cfg = ReconstructionConfig()
        context = read_incident_context(cls.RUN)
        cls.vehicle_dirs = sorted(path for path in (cls.RUN / "vehicles").iterdir() if path.is_dir())
        cls.locals = {path.name: reconstruct_vehicle(path, cls.cfg, context=context) for path in cls.vehicle_dirs}
        locals_ = list(cls.locals.values())
        cls.alignment = align_graphs([local.graph for local in locals_], cls.cfg.fusion)
        cls.associations = associate_tracks(locals_, cls.alignment, cls.cfg.fusion)
        cls.graph = fuse_graphs(locals_, cls.alignment, cls.associations)
        cls.relations = global_temporal_relations(locals_, cls.alignment, cls.associations)

    def collisions(self, owner):
        return [node for node in self.locals[owner].graph.nodes if node.event_type == "COLLISION"]

    def test_each_recorder_reports_its_own_contacts(self):
        b = self.collisions("B")
        self.assertEqual([node.t_local for node in b], [4.8, 5.3])
        self.assertEqual([node.attributes["peak_impulse"] for node in b], [10281.41, 8788.05])
        self.assertEqual(b[1].attributes["new_contact"], {"break_s": 0.5, "peak_ratio": 0.85, "evidence": "peak"})
        # A's second strike reaches B 0.15 s after B's own impact on C, at 0.17 of its peak: B's
        # sensor (magnitudes only) cannot tell it from that contact and merges it.
        self.assertEqual(b[1].attributes["merged_bursts"], [[5.45, 1509.76]])
        self.assertEqual([node.t_local for node in self.collisions("A")], [4.8, 5.45])
        self.assertEqual([node.t_local for node in self.collisions("C")], [5.3])

    def test_pushing_contact_adds_no_collision(self):
        raw = {name: len(read_jsonl(self.RUN / "vehicles" / name / "collisions.jsonl")) for name in "ABC"}
        self.assertGreater(raw["A"], 5)  # A stays on B after its second strike
        self.assertEqual([len(self.collisions(name)) for name in "ABC"], [2, 2, 1])
        types = {node.event_type for local in self.locals.values() for node in local.graph.nodes}
        self.assertFalse(types & {"IMPACT", "CONTACT", "CONTINUED_CONTACT"})

    def test_global_graph_has_ab_bc_then_ab_again(self):
        collisions = [node for node in self.graph.nodes if node.event_type == "COLLISION"]
        self.assertEqual([(node.participants, node.t_global) for node in collisions],
                         [(["A", "B"], 0.0), (["B", "C"], 0.5), (["A", "B"], 0.65)])
        self.assertTrue(collisions[0].attributes["reference_event"])
        self.assertEqual({obs.graph for obs in collisions[1].observations}, {"B", "C"})
        # The second A-B contact: A's own report, matched to the burst B merged into its B-C contact.
        merged = next(event for event in self.alignment.matched_events if event.get("merged_burst_of") == "B")
        self.assertEqual(merged["t_local"], {"A": 5.45, "B": 5.45})
        self.assertEqual({obs.graph for obs in collisions[2].observations}, {"A", "B"})

    def test_c_is_aligned_through_b(self):
        clocks = self.alignment.graphs
        self.assertEqual({name: clock.status for name, clock in clocks.items()},
                         {"A": "ALIGNED", "B": "ALIGNED", "C": "ALIGNED"})
        self.assertEqual(len(clocks["C"].chain), 2)
        self.assertIn("aligned through", clocks["C"].reason)
        # In CARLA every raw clock is simulator time, so the true relative offsets are the
        # differences of the clock origins (privileged knowledge, used only to check).
        offsets = self.alignment.to_dict()["relative_clock_offsets_s"]
        origins = {name: local.clock_origin for name, local in self.locals.items()}
        for pair, estimated in offsets.items():
            second, first = pair.split(" - ")
            self.assertAlmostEqual(estimated, origins[first] - origins[second], places=3)

    def test_partners_identified_and_no_rear_view(self):
        decisions = {(item.local_graph, item.local_track): item for item in self.associations}
        a_b = next(event for event in self.alignment.matched_events if event["event_id"] == "collision_001")
        b_c = next(event for event in self.alignment.matched_events if sorted(event["graphs"]) == ["B", "C"])
        item = decisions[("B", "track_001")]  # ahead of B
        self.assertEqual((item.status, item.global_entity, item.collision_event), ("ASSOCIATED", "C", b_c["event_id"]))
        item = decisions[("A", "track_001")]
        self.assertEqual((item.status, item.global_entity, item.collision_event), ("ASSOCIATED", "B", a_b["event_id"]))
        # A strikes B from directly behind: in B's rear blind zone, B never tracks it.
        self.assertEqual([track.track_id for track in self.locals["B"].tracks], ["track_001"])
        relation = next(item for item in self.relations if item["recorder"] == "B" and item["track"] == "track_001")
        self.assertEqual((relation["collision"], relation["collision_with"]), (5.3, "C"))

    def test_the_global_graph_does_not_depend_on_cs_clock_origin(self):
        context = read_incident_context(self.RUN)
        locals_ = []
        for path in self.vehicle_dirs:
            origin = None if path.name != "C" else self.locals["C"].clock_origin - 0.73
            locals_.append(reconstruct_vehicle(path, self.cfg, clock_origin=origin, context=context))
        alignment = align_graphs([local.graph for local in locals_], self.cfg.fusion)
        graph = fuse_graphs(locals_, alignment, associate_tracks(locals_, alignment, self.cfg.fusion))
        signature = [[(node.event_type, node.actor_id, node.subject_id, node.t_global) for node in g.nodes]
                     for g in (self.graph, graph)]
        self.assertEqual(signature[0], signature[1])
        self.assertAlmostEqual(alignment.graphs["C"].offset_to_global - self.alignment.graphs["C"].offset_to_global,
                               -0.73, places=3)


class ConflictTests(unittest.TestCase):
    def test_a_track_compatible_with_two_partners_stays_anonymous(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = reconstruct_run(make_run(Path(tmp)), ReconstructionConfig())
        a, b = (next(local for local in result.locals if local.owner == name) for name in ("A", "B"))
        # A third recorder C moving exactly like B, in contact with A at the same instant.
        c = dataclasses.replace(b, owner="C")
        event = copy.deepcopy(result.alignment.matched_events[0])
        twin = {"event_id": "collision_002", "graphs": ["A", "C"],
                "nodes": {"A": event["nodes"]["A"], "C": "C:e99"},
                "t_local": {"A": event["t_local"]["A"], "C": event["t_local"]["B"]},
                "peak_impulse": {"A": event["peak_impulse"]["A"], "C": event["peak_impulse"]["B"]},
                "impulse_similarity": 1.0, "confidence": 1.0, "evidence": []}
        graphs = dict(result.alignment.graphs)
        graphs["C"] = dataclasses.replace(graphs["B"], graph="C")
        alignment = Alignment(result.alignment.reference_event, graphs, [event, twin])
        decisions = {(item.local_graph, item.local_track): item
                     for item in associate_tracks([a, b, c], alignment, FusionConfig())}
        item = decisions[("A", "track_001")]
        self.assertEqual(item.status, "ANONYMOUS")
        self.assertTrue(item.blocking[0].startswith("conflict: compatible with the contacts with B"))


if __name__ == "__main__":
    unittest.main()
