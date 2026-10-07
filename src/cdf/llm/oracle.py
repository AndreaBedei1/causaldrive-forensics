"""Oracle identities: PRIVILEGED - NOT ADMISSIBLE INPUT.

Evaluation infrastructure only, for measuring what partial observability costs:
the same analysis with every anonymous radar track renamed to the simulator
participant it really was (from the privileged evaluation, which compared the
tracks with ``ground_truth/``).  Everything it produces lives under
``reconstruction/evaluation/llm_oracle/``; the main pipeline never imports this
module unless ``--oracle-identities`` is given, and never reads that directory.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Optional

NOTICE = "PRIVILEGED - NOT ADMISSIBLE INPUT: identities from simulator ground truth, evaluation only"


def oracle_dir(run_dir: Path) -> Path:
    return Path(run_dir) / "reconstruction" / "evaluation" / "llm_oracle"


def oracle_identity_map(run_dir: Path) -> Dict[str, str]:
    """{"A:track_001": "C", ...} for anonymous tracks whose true identity the privileged evaluation found."""
    path = Path(run_dir) / "reconstruction" / "evaluation" / "evaluation.json"
    if not path.exists():
        raise FileNotFoundError("no privileged evaluation at {0}; run scripts/reconstruct_run.py --evaluate".format(path))
    evaluation = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for row in evaluation.get("tracks", []):
        if row.get("status") != "ASSOCIATED" and row.get("true_identity"):
            out[row["track"]] = row["true_identity"]
    return dict(sorted(out.items()))


def write_oracle_identities(run_dir: Path) -> Path:
    mapping = oracle_identity_map(run_dir)
    target = oracle_dir(run_dir) / "oracle_identities.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"_notice": NOTICE, "identities": mapping}, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8")
    return target


def oracle_packet(packet: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
    """The packet with anonymous tracks renamed to their true identities (nothing else changes)."""
    out = copy.deepcopy(packet)
    added = []
    for entity in out["entities"]:
        if entity.get("kind") == "RADAR_TRACK" and entity["entity_id"] in mapping:
            entity["observed_subject"] = mapping[entity["entity_id"]]
            entity["identity_status"] = "ASSOCIATED"
    known = {entity["entity_id"] for entity in out["entities"]}
    for name in sorted(set(mapping.values()) - known):
        added.append({"entity_id": name, "kind": "ROAD_USER", "recorder": False})
    out["entities"] = out["entities"][:len(out["known_recorders"])] + added + out["entities"][len(out["known_recorders"]):]
    block = out["facts"]["TRACK_STATE"]
    subject, local, status = (block["columns"].index(k) for k in ("observed_subject", "local_track_id", "identity_status"))
    for row in block["rows"]:
        if row[local] in mapping:
            row[subject] = mapping[row[local]]
            row[status] = "ASSOCIATED"
    out["run_id"] = packet["run_id"] + "-id"
    return out


def save_oracle_packet(run_dir: Path, packet: Dict[str, Any]) -> Path:
    target = oracle_dir(run_dir) / "forensic_packet_oracle.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"_notice": NOTICE, "packet": packet}, indent=1, ensure_ascii=False) + "\n",
                      encoding="utf-8")
    return target


def load_identity_map_for(analysis_dir: Path) -> Optional[Dict[str, str]]:
    """The oracle map recorded with an oracle analysis, or None for an ordinary one."""
    path = Path(analysis_dir) / "oracle_identities.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))["identities"]
