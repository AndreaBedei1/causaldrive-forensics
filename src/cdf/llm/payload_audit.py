"""Pre-send payload audit (``--audit-payload``; privileged, for manual integration runs).

Before every HTTP request of an analysis, the exact request body is searched for things that must
never reach a model:

* instances of the run's reconstructed semantic trace: the node ids of its local and global graphs;
* names of the semantic, privileged and scenario-construction files and fields (ground_truth,
  perceived_state, global_graph, triggers.jsonl, counterfactuals.json, true_identity, oracle, ...)
  and the ids of the scripted actions recorded in ground truth;
* the ids of physical participants that recorded nothing (``record: false`` in ground truth, e.g.
  "C"), as an identity.

The blocks the pipeline renders itself (vocabulary, grammar, supplied context) and the model's own
previous answer are exempt, as in the leak guard (a hallucinated "C" in a Stage-1 answer is the
model's output, measured by the evaluation, not a leak).  The body must also carry the checked
forensic packet verbatim; its SHA-256 is recorded for every request.

The audit reads those files only to look for them in the outgoing body: nothing from them is added
to any request, and the verifier still loads the semantic trace only after both answers are saved.
A finding raises :class:`PayloadAuditError` before anything is sent.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence

STATIC_MARKERS = (
    "ground_truth", "ground truth", "counterfactuals.json", "swerve_disabled", "without_c\"",
    "--without-participant", "--disable-action", "triggers.jsonl", "corridor_clearance", "envelope_entry",
    "front_clearance_m", "perceived_state", "semantic_trace", "semantic trace", "global_graph", "local_graph",
    "local_trace", "global_trace", "true_identity", "oracle", "evaluation.json", "culprit",
    "unobserved_causal_vehicle", "\"record\": false",
)


class PayloadAuditError(RuntimeError):
    """Something privileged was about to be sent; nothing was sent."""

    def __init__(self, stage: str, findings: Sequence[str]) -> None:
        self.findings = list(findings)
        super().__init__("payload audit ({0}): {1} finding(s): {2}".format(stage, len(self.findings),
                                                                         "; ".join(self.findings[:6])))


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            for text in _strings(item):
                yield text
    elif isinstance(value, list):
        for item in value:
            for text in _strings(item):
                yield text


def _read_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


class PayloadAuditor:
    """Checks request bodies of one run's analysis before they are sent (see the module docstring)."""

    def __init__(self, run_dir: Path) -> None:
        run_dir = Path(run_dir)
        rec = run_dir / "reconstruction"
        node_ids = set()
        for graph in sorted(rec.glob("*/local_graph.json")) + [rec / "global" / "global_graph.json"]:
            if graph.exists():
                node_ids |= {str(node["node_id"]) for node in _read_json(graph).get("nodes", [])}
        truth = run_dir / "ground_truth"
        hidden = []
        if (truth / "metadata.json").exists():
            hidden = [str(p["participant_id"]) for p in _read_json(truth / "metadata.json").get("participants", [])
                      if isinstance(p, dict) and not p.get("record", True)]
        actions = set()
        if (truth / "triggers.jsonl").exists():
            actions = {str(row.get("action_id")) for row in _read_jsonl(truth / "triggers.jsonl") if row.get("action_id")}
        self._node_patterns = [re.compile(r"(?<![\w:]){0}(?!\w)".format(re.escape(node))) for node in sorted(node_ids)]
        self._identity_patterns = [re.compile(r"\"{0}\"|(?<![\w:]){0}:track_\d+".format(re.escape(pid)))
                                   for pid in hidden]
        self._static = tuple(STATIC_MARKERS) + tuple(sorted(actions))
        self.marker_counts = {"semantic_node_ids": len(node_ids), "unrecorded_participants": len(hidden),
                              "scripted_actions": len(actions), "static": len(STATIC_MARKERS)}
        self.records: List[Dict[str, Any]] = []

    def check(self, stage: str, url: str, body: Dict[str, Any], packet_json: str, exempt: Sequence[str]) -> None:
        """Raise PayloadAuditError if ``body`` carries anything privileged; record what was checked."""
        texts = list(_strings(body))
        findings = []
        packet_hits = sum(text.count(packet_json) for text in texts)
        if packet_hits != 1:
            findings.append("the checked forensic packet appears {0} time(s) in the body (expected 1)".format(
                packet_hits))
        scanned = "\n".join(texts).replace(packet_json, "\n<packet>\n")
        for block in sorted((block for block in exempt if block), key=len, reverse=True):
            scanned = scanned.replace(block, "\n<exempt>\n")
        lowered = scanned.lower()
        findings += ["marker {0!r}".format(marker) for marker in self._static if marker.lower() in lowered]
        findings += ["semantic graph node id {0}".format(p.pattern) for p in self._node_patterns if p.search(scanned)]
        findings += ["unrecorded participant id ({0})".format(p.pattern) for p in self._identity_patterns
                     if p.search(scanned) or p.search(packet_json)]
        body_text = json.dumps(body, ensure_ascii=False, sort_keys=True)
        record = {"stage": stage, "url": url, "body_sha256": hashlib.sha256(body_text.encode("utf-8")).hexdigest(),
                  "body_characters": len(body_text),
                  "embedded_packet_sha256": hashlib.sha256(packet_json.encode("utf-8")).hexdigest(),
                  "markers_checked": dict(self.marker_counts), "result": "BLOCKED" if findings else "PASS"}
        if findings:
            record["findings"] = findings
        self.records.append(record)
        if findings:
            raise PayloadAuditError(stage, findings)

    def report(self) -> Dict[str, Any]:
        return {"note": "pre-send payload audit (privileged files were read only to search the outgoing bodies)",
                "requests": self.records}
