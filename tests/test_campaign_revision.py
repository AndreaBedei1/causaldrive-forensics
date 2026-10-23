"""Campaign revision v2: a collision without global time does not crash the closure audit, a further evaluation
that raises is recorded without losing the job, run paths pair whatever their spelling, and the controller's
adaptive concurrency rule keeps its headroom."""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def _script(name):
    for path in (str(ROOT / "scripts"), str(ROOT / "src")):
        if path not in sys.path:
            sys.path.insert(0, path)
    spec = importlib.util.spec_from_file_location(name, str(ROOT / "scripts" / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClosureTests(unittest.TestCase):
    def test_a_collision_without_global_time_is_skipped(self):
        audit = _script("stability_audit")
        nodes = [{"event_type": "COLLISION", "participants": ["A", "B"], "t_global": None},
                 {"event_type": "COLLISION", "participants": ["A", "C"], "t_global": 1.0},
                 {"event_type": "CRITICAL_TTC_START", "actor_id": "A", "subject_id": "C", "t_global": 2.0},
                 {"event_type": "CRITICAL_TTC_START", "actor_id": "A", "subject_id": "B", "t_global": 2.0}]
        with tempfile.TemporaryDirectory() as tmp:
            graph = Path(tmp) / "reconstruction" / "global"
            graph.mkdir(parents=True)
            (graph / "global_graph.json").write_text(json.dumps({"nodes": nodes}), encoding="utf-8")
            self.assertEqual(audit.closure_violations(Path(tmp)), 1)  # only the A-C pair has a defined closure


class IsolationTests(unittest.TestCase):
    def test_a_failing_further_evaluation_keeps_the_others(self):
        rob = _script("robustness")
        import stability_audit
        fusion = {"state_errors": {}, "calibration": None, "track_decisions": [], "entities": []}
        with mock.patch.object(stability_audit, "audit_run", side_effect=TypeError("boom")), \
                mock.patch("cdf.evaluation.event_oracle.compare_run", return_value={"comparison": {}}), \
                mock.patch("cdf.evaluation.campaign_metrics.campaign_metrics", return_value={"collisions": {}}):
            out = rob.extra_evaluation(Path("."), {"collisions": []}, fusion)
        self.assertIn("stability_audit", out["evaluation_errors"])
        self.assertNotIn("stability", out)
        self.assertEqual(out["campaign"], {"collisions": {}})
        self.assertEqual(out["event_oracle"], {})


class ReportKeyTests(unittest.TestCase):
    def test_run_paths_pair_whatever_their_spelling(self):
        rep = _script("campaign_report")
        self.assertEqual(rep.run_key("C:\\x\\CarlaGraph\\traces\\S04\\run_0_a_front_pushed"), "S04/run_0_a_front_pushed")
        self.assertEqual(rep.run_key("traces/S04/run_0_a_front_pushed"), "S04/run_0_a_front_pushed")


class ConcurrencyTests(unittest.TestCase):
    def sample(self, **kw):
        s = {"ram_available_gb": 60.0, "other_cores": 4.0, "own_cores": 13.5, "pagefile_growth_gb": 0.0,
             "disk_free_gb": 70.0, "own_rss_gb": 5.0}
        s.update(kw)
        return s

    def test_rules(self):
        ctl = _script("campaign_controller")
        steady = [self.sample() for _ in range(5)]
        self.assertEqual(ctl.decide(14, steady, 14, 22)[0], 15)  # 22 - 3 headroom - 4 other = 15 cores
        busy = [self.sample(other_cores=10.0) for _ in range(5)]
        self.assertEqual(ctl.decide(14, busy, 14, 22)[0], 12)  # other users' load: at most 2 fewer per decision
        short = [self.sample(ram_available_gb=8.0) for _ in range(5)]
        self.assertEqual(ctl.decide(14, short, 14, 22)[0], 12)
        swapping = [self.sample(pagefile_growth_gb=0.0)] * 4 + [self.sample(pagefile_growth_gb=2.0)]
        self.assertEqual(ctl.decide(14, swapping, 14, 22)[0], 12)
        contended = [self.sample(own_cores=8.0, cpu_percent=95.0) for _ in range(5)]
        self.assertEqual(ctl.decide(14, contended, 14, 22)[0], 12)  # saturated machine, workers starved
        io_bound = [self.sample(own_cores=8.0, cpu_percent=60.0) for _ in range(5)]
        self.assertEqual(ctl.decide(14, io_bound, 14, 22)[0], 15)  # not saturated: low CPU per job is I/O, not contention
        idle = [self.sample(other_cores=1.0) for _ in range(5)]
        self.assertEqual(ctl.decide(14, idle, 14, 22)[0], 16)  # +2 at most
        self.assertEqual(ctl.decide(20, [self.sample(other_cores=0.0, own_cores=19.5)] * 5, 20, 22)[0], 19)
        self.assertGreaterEqual(ctl.decide(4, [self.sample(other_cores=20.0)] * 5, 4, 22)[0], ctl.MIN_WORKERS)

    def test_fixed_setting(self):
        ctl = _script("campaign_controller")
        fixed = {"workers": 20, "cpu_rules": False}
        busy = [self.sample(other_cores=12.0, own_cores=6.0, cpu_percent=99.0) for _ in range(5)]
        self.assertEqual(ctl.decide(10, busy, 10, 22, fixed)[0], 20)  # CPU rules off: other users' load ignored
        tight = [self.sample(ram_available_gb=12.0) for _ in range(5)]
        self.assertEqual(ctl.decide(10, tight, 10, 22, fixed)[0], 12)  # RAM allows a step only
        short = [self.sample(ram_available_gb=8.0) for _ in range(5)]
        self.assertEqual(ctl.decide(20, short, 20, 22, fixed)[0], 18)  # safety rules still apply
        self.assertEqual(ctl.decide(10, [], 10, 22, {"workers": 40})[0], ctl.HARD_MAX_WORKERS)


class DetachedStartTests(unittest.TestCase):
    def test_the_controller_gets_a_hidden_console_that_its_jobs_share(self):
        """Campaign v3 (2026-10-23): with DETACHED_PROCESS the controller had no console, so Windows opened a visible
        console window for every job it started.  A hidden console of its own (CREATE_NO_WINDOW) is shared by the
        jobs, and a new process group keeps it independent of the terminal that started it."""
        ctl = _script("campaign_controller")
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(ctl, "CONTROL", Path(tmp)), \
                mock.patch.object(ctl.subprocess, "Popen") as popen:
            popen.return_value.pid = 1234
            ctl.start_detached([])
            for handle in popen.call_args[1]["stdout"], popen.call_args[1]["stderr"]:
                handle.close()
        flags = popen.call_args[1]["creationflags"]
        self.assertTrue(flags & 0x08000000)  # CREATE_NO_WINDOW
        self.assertTrue(flags & 0x00000200)  # CREATE_NEW_PROCESS_GROUP
        self.assertFalse(flags & 0x00000008)  # not DETACHED_PROCESS, which leaves every job its own window


if __name__ == "__main__":
    unittest.main()
