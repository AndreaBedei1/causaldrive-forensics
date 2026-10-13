"""Global graph: no new CRITICAL_TTC episode of a colliding pair while the pair is still in contact
(fusion.post_contact_episodes)."""

import json
import unittest
from pathlib import Path
from types import SimpleNamespace as NS

from src.cdf.reconstruction.fusion import post_contact_episodes

ROOT = Path(__file__).resolve().parents[1]


def local(nodes, tracks):
    return NS(owner="A", graph=NS(nodes=[NS(node_id=i, event_type=e, subject_id=s, t_local=t) for i, e, s, t in nodes]),
              tracks=[NS(track_id=k, samples=[NS(t_local=t, clearance_m=c) for t, c in v]) for k, v in tracks.items()])


ALIGNMENT = NS(graphs={"A": NS(status="ALIGNED"), "B": NS(status="ALIGNED")})
CONTACT = [{"graphs": ["A", "B"], "t_local": {"A": 5.0, "B": 5.0}}]
NODES = [("e1", "CRITICAL_TTC_START", "t2", 5.45), ("e2", "CRITICAL_TTC_END", "t2", 6.0)]


class PostContactTests(unittest.TestCase):
    def test_a_second_track_of_the_partner_starts_no_episode_while_touching(self):
        a = local(NODES, {"t1": [(5.45, 0.0)], "t2": [(5.45, 1.6)]})  # t1 (the partner track) still at A's skin
        drop = post_contact_episodes([a], ALIGNMENT, {("A", "t1"): "B", ("A", "t2"): "B"}, CONTACT, 1.0)
        self.assertEqual(drop, {("A", "e1"), ("A", "e2")})

    def test_once_separated_a_new_episode_is_kept(self):
        a = local(NODES, {"t1": [(5.45, 3.0)], "t2": [(5.45, 4.0)]})
        self.assertEqual(post_contact_episodes([a], ALIGNMENT, {("A", "t1"): "B", ("A", "t2"): "B"}, CONTACT, 1.0), set())

    def test_another_road_user_is_unaffected(self):
        a = local(NODES, {"t1": [(5.45, 0.0)], "t2": [(5.45, 1.6)]})
        self.assertEqual(post_contact_episodes([a], ALIGNMENT, {("A", "t1"): "B", ("A", "t2"): "U3"}, CONTACT, 1.0), set())

    def test_canonical_runs_have_no_same_pair_episode_after_contact(self):
        for run in sorted((ROOT / "traces").glob("S*/run_*")):
            path = run / "reconstruction/global/global_graph.json"
            if not path.exists():
                continue
            nodes = json.loads(path.read_text())["nodes"]
            for c in (n for n in nodes if n["event_type"] == "COLLISION" and n.get("participants")):
                pair = set(c["participants"])
                late = [n for n in nodes if n["event_type"] == "CRITICAL_TTC_START" and n["t_global"] is not None
                        and n["t_global"] > c["t_global"] and {n["actor_id"], n["subject_id"]} == pair]
                self.assertEqual(late, [], run.name)


if __name__ == "__main__":
    unittest.main()
