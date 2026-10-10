"""Section 10 of CAMPAIGN_REPORT.md: the global event sequence of every run, from global_graph.json.

    python scripts/report_sequences.py [--show] [--write]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def label(node):
    if node["event_type"] == "COLLISION":
        return "COLLISION({0})".format(",".join(node.get("participants") or [node["actor_id"]]))
    if node.get("subject_id"):
        return "{0}({1},{2})".format(node["event_type"], node["actor_id"], node["subject_id"])
    return "{0}({1})".format(node["event_type"], node["actor_id"])


def sequence(run):
    graph = json.loads((ROOT / "traces" / run / "reconstruction" / "global" / "global_graph.json").read_text(encoding="utf-8"))
    lines, current, items = [], None, []
    for node in graph["nodes"]:
        t = node.get("t_global")
        if t is None:
            continue
        if current is not None and abs(t - current) > 1e-9:
            lines.append("{0:+.2f} {1}".format(current, "; ".join(items)).replace("+-", "-"))
            items = []
        current = t
        items.append(label(node))
    if items:
        lines.append("{0:+.2f} {1}".format(current, "; ".join(items)))
    return "\n".join(line if not line.startswith("+-") else line[1:] for line in lines)


def blocks(text):
    return {m.group(1): m.group(2) for m in re.finditer(r"### (S\d\d/run_[^\n]+)\n\n```\n(.*?)\n```", text, re.S)}


if __name__ == "__main__":
    report = (ROOT / "CAMPAIGN_REPORT.md").read_text(encoding="utf-8")
    current = blocks(report)
    for run, text in current.items():
        new = sequence(run)
        print(run, "SAME" if new == text else "DIFFERENT")
        if new != text and "--show" in sys.argv:
            print("--- old\n" + text + "\n--- new\n" + new)
    if "--write" in sys.argv:
        for run in current:
            old_block = "### {0}\n\n```\n{1}\n```".format(run, current[run])
            new_block = "### {0}\n\n```\n{1}\n```".format(run, sequence(run))
            report = report.replace(old_block, new_block)
        (ROOT / "CAMPAIGN_REPORT.md").write_text(report, encoding="utf-8")
        print("written")
