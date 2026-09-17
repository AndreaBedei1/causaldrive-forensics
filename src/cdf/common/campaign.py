"""Campaign identity: which experiment a tree of artifacts belongs to.

A run directory records how *it* was produced. It does not record which
experiment it belongs to, and without that a report can silently average two
campaigns together -- a synchronized-clock baseline and an independent-clock
campaign, say -- and produce a number that answers no question anyone asked.

This module adds the missing identity. ``campaign.json`` sits at the root of an
artifacts tree and names the campaign, the clock protocol its runs were recorded
under, and the commit they were recorded from. Aggregation reads it and refuses
to mix: a run whose ``clock_protocol`` disagrees with the campaign it is sitting
in is reported as foreign rather than averaged in.

A tree with no ``campaign.json`` is treated as an unnamed campaign, so older
artifact trees keep working; the check then degrades to "every run agrees with
every other run", which is still worth having.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence

from .io import read_json, write_json

__all__ = [
    "CAMPAIGN_FILE",
    "campaign_path",
    "load_campaign",
    "write_campaign",
    "classify_runs",
]

CAMPAIGN_FILE = "campaign.json"


def campaign_path(artifacts_root: Any) -> Path:
    return Path(artifacts_root) / CAMPAIGN_FILE


def load_campaign(artifacts_root: Any) -> Optional[Dict[str, Any]]:
    """The campaign identity of an artifacts tree, or None when it has none."""
    path = campaign_path(artifacts_root)
    if not path.exists():
        return None
    try:
        return read_json(path)
    except (OSError, ValueError):
        return None


def write_campaign(
    artifacts_root: Any,
    campaign_id: str,
    clock_protocol: str,
    description: str = "",
    extra: Optional[Mapping[str, Any]] = None,
) -> Path:
    """Stamp an artifacts tree with the experiment it holds."""
    if not campaign_id:
        raise ValueError("a campaign needs an id")
    payload: Dict[str, Any] = {
        "schema_version": "1.0.0",
        "campaign_id": str(campaign_id),
        "clock_protocol": str(clock_protocol),
        "description": str(description),
    }
    if extra:
        payload.update({str(k): v for k, v in extra.items()})
    root = Path(artifacts_root)
    root.mkdir(parents=True, exist_ok=True)
    return write_json(campaign_path(root), payload)


def classify_runs(
    artifacts_root: Any,
    manifests: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    """Split runs into those belonging to this campaign and those that do not.

    ``manifests`` maps a run path to its ``manifest.json`` contents. A run is
    *foreign* when the campaign declares a clock protocol and the run was
    recorded under a different one -- the one difference that makes two runs
    incomparable no matter how carefully everything else was held equal.
    """
    campaign = load_campaign(artifacts_root)
    declared = str((campaign or {}).get("clock_protocol") or "") or None

    belonging: List[str] = []
    foreign: List[Dict[str, Any]] = []
    protocols: Dict[str, int] = {}
    for run_path in sorted(manifests):
        manifest = manifests[run_path] or {}
        protocol = str(
            manifest.get("clock_protocol") or "synchronized_clock_baseline"
        )
        protocols[protocol] = protocols.get(protocol, 0) + 1
        if declared is not None and protocol != declared:
            foreign.append(
                {
                    "run_path": run_path,
                    "clock_protocol": protocol,
                    "reason": (
                        "recorded under {0!r}; this campaign is {1!r}".format(
                            protocol, declared
                        )
                    ),
                }
            )
            continue
        belonging.append(run_path)

    mixed = declared is None and len(protocols) > 1
    return {
        "campaign": campaign,
        "campaign_id": (campaign or {}).get("campaign_id"),
        "declared_clock_protocol": declared,
        "runs": belonging,
        "foreign_runs": foreign,
        "clock_protocols": dict(sorted(protocols.items())),
        "mixed_unnamed_campaign": mixed,
        "note": (
            "artifacts tree carries no campaign.json; runs recorded under "
            "different clock protocols are present and must not be averaged "
            "together" if mixed else ""
        ),
    }
