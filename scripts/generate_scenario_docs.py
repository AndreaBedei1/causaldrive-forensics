#!/usr/bin/env python
"""Regenerate the scenario parameter tables in ``docs/SCENARIOS.md``.

The prose in that document is written by hand; the *numbers* are not. Scenario
geometry is tuned empirically against the simulator, so any table typed by hand
goes stale the moment an approach distance or a brake timing is retuned -- and a
stale parameter table in a forensics project is worse than no table.

This script reads ``configs/scenarios/*.yaml`` and rewrites everything between
the ``<!-- BEGIN GENERATED ... -->`` and ``<!-- END GENERATED ... -->`` markers,
leaving the surrounding prose untouched.

    python scripts/generate_scenario_docs.py [--check]

``--check`` exits non-zero if the file is out of date instead of rewriting it,
so it can be used as a documentation regression test.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cdf.common.config import configs_dir, deep_merge, load_yaml  # noqa: E402

BEGIN = "<!-- BEGIN GENERATED SCENARIO TABLE -->"
END = "<!-- END GENERATED SCENARIO TABLE -->"


def _variant_block(block: Dict[str, Any], variant: str) -> Dict[str, Any]:
    """Merge one variant's overrides over the base scenario block."""
    merged = dict(block)
    variants = block.get("variants", {}) or {}
    if variant in variants:
        merged = deep_merge(merged, variants[variant] or {})
    overrides = merged.pop("participant_overrides", {}) or {}
    participants = []
    for p in merged.get("participants", []) or []:
        pid = str(p["id"])
        if pid in overrides:
            p = deep_merge(p, overrides[pid] or {})
        participants.append(p)
    merged["participants"] = participants
    return merged


def _spawn_text(spawn: Dict[str, Any]) -> str:
    anchor = spawn.get("anchor", "spawn_index")
    if anchor == "spawn_index":
        bits = ["spawn {0}".format(spawn.get("index", 0))]
        if float(spawn.get("forward_m", 0.0)):
            bits.append("fwd {0:g} m".format(float(spawn["forward_m"])))
        if int(spawn.get("lane_offset", 0)):
            bits.append("lane {0:+d}".format(int(spawn["lane_offset"])))
        return ", ".join(bits)
    if anchor == "junction_approach":
        return "junction ({0:g}, {1:g}), bearing {2:g}deg, back {3:g} m".format(
            float(spawn.get("junction_x", 0.0)),
            float(spawn.get("junction_y", 0.0)),
            float(spawn.get("bearing_deg", 0.0)),
            float(spawn.get("back_m", 0.0)),
        )
    return "location ({0:g}, {1:g})".format(
        float(spawn.get("x", 0.0)), float(spawn.get("y", 0.0))
    )


def _action_text(action: Dict[str, Any]) -> str:
    params = action.get("params", {}) or {}
    ptxt = ", ".join("{0} {1:g}".format(k, float(v)) for k, v in sorted(params.items()))
    return "`{0}` -- {1} at t={2:g}s for {3:g}s{4}".format(
        action["action_id"],
        action["kind"],
        float(action.get("t_start", 0.0)),
        float(action.get("duration", 0.0)),
        " ({0})".format(ptxt) if ptxt else "",
    )


def render_scenario(path: Path) -> List[str]:
    """Markdown for one scenario file, covering every declared variant."""
    block = load_yaml(path).get("scenario", {})
    out: List[str] = []
    sid = block.get("scenario_id", path.stem.upper())
    name = block.get("name", "")
    out.append("### {0} -- {1}".format(sid, name.replace("_", " ")))
    out.append("")
    out.append(
        "*Map:* **{0}** &nbsp;&nbsp; *Config:* `configs/scenarios/{1}`".format(
            block.get("map", "?"), path.name
        )
    )
    out.append("")
    desc = " ".join(str(block.get("description", "")).split())
    if desc:
        out.append(desc)
        out.append("")

    variants = list((block.get("variants", {}) or {}).keys()) or ["default"]
    default_variant = block.get("default_variant", "default")

    for variant in variants:
        merged = _variant_block(block, variant)
        marker = " *(default)*" if variant == default_variant else ""
        out.append("**Variant `{0}`**{1}".format(variant, marker))
        out.append("")
        out.append("| Participant | Blueprint | Spawn | Initial / target speed | Radar profile |")
        out.append("|---|---|---|---|---|")
        for p in merged["participants"]:
            out.append(
                "| {0} | `{1}` | {2} | {3:g} / {4:g} m/s | {5} |".format(
                    p["id"],
                    p.get("blueprint", "?"),
                    _spawn_text(p.get("spawn", {}) or {}),
                    float(p.get("initial_speed", 0.0)),
                    float(p.get("target_speed", 0.0)),
                    p.get("sensor_profile") or "baseline",
                )
            )
        out.append("")

        actions = [
            (p["id"], a)
            for p in merged["participants"]
            for a in (p.get("actions", []) or [])
        ]
        if actions:
            out.append("Scripted actions (these are the intervention handles):")
            out.append("")
            for pid, a in actions:
                out.append("* **{0}** &mdash; {1}".format(pid, _action_text(a)))
            out.append("")
        else:
            out.append("No scripted actions: every participant holds its target speed.")
            out.append("")

        expected = merged.get("expected_outcome", "?")
        pairs = merged.get("expected_collision_pairs", []) or []
        order = merged.get("expected_collision_order", []) or []
        validation = merged.get("validation", {}) or {}
        bits = ["expected outcome **{0}**".format(expected)]
        if pairs:
            bits.append(
                "collision pairs " + ", ".join("({0})".format("-".join(p)) for p in pairs)
            )
        if order:
            bits.append(
                "in order " + " then ".join("({0})".format("-".join(p)) for p in order)
            )
        if validation.get("min_separation_below_m") is not None:
            bits.append(
                "{0} must close to under {1:g} m".format(
                    "-".join(validation.get("encounter_pair", [])) or "the pair",
                    float(validation["min_separation_below_m"]),
                )
            )
        out.append("*Validation:* " + "; ".join(bits) + ".")
        out.append("")

        cands = merged.get("intervention_candidates", []) or []
        if cands:
            out.append(
                "*Counterfactual candidates:* "
                + ", ".join("`{0}`".format(c) for c in cands)
                + "."
            )
            out.append("")

        unknowns = merged.get("expected_local_unknowns", []) or []
        if unknowns:
            out.append(
                "*Expected local UNKNOWNs:* "
                + ", ".join("`{0}`".format(u) for u in unknowns)
                + " -- the oracle may assert these; local and fused inference must not."
            )
            out.append("")

        template = merged.get("causal_template", []) or []
        if template:
            out.append("*Ground-truth causal template (oracle only):*")
            out.append("")
            for edge in template:
                cause = edge.get("cause", {})
                effect = edge.get("effect", {})
                out.append(
                    "* `{0}` --{1}--> `{2}`{3}".format(
                        _endpoint(cause),
                        edge.get("edge", "?"),
                        _endpoint(effect),
                        "  \n  _{0}_".format(edge["rationale"])
                        if edge.get("rationale")
                        else "",
                    )
                )
            out.append("")

        for note in merged.get("notes", []) or []:
            out.append("> {0}".format(note))
        out.append("")

    out.append("---")
    out.append("")
    return out


def _endpoint(node: Dict[str, Any]) -> str:
    kind = node.get("kind", "?")
    if kind == "action":
        return "{0}.{1}".format(node.get("participant", "?"), node.get("action_id", "?"))
    if kind in ("state", "oracle_state"):
        return "{0}.{1}{2}".format(
            node.get("participant", "?"),
            node.get("name", "?"),
            " (oracle only)" if kind == "oracle_state" else "",
        )
    if kind == "outcome":
        return "{0}({1})".format(
            node.get("name", "?"), "-".join(node.get("participants", []) or [])
        )
    return str(node)


def build_section() -> str:
    paths = sorted((configs_dir() / "scenarios").glob("*.yaml"))
    lines: List[str] = [BEGIN, ""]
    lines.append(
        "_Generated from `configs/scenarios/*.yaml` by "
        "`scripts/generate_scenario_docs.py`. Do not edit by hand._"
    )
    lines.append("")
    for path in paths:
        lines.extend(render_scenario(path))
    lines.append(END)
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if the document is out of date instead of rewriting it",
    )
    parser.add_argument(
        "--doc",
        default=str(Path(__file__).resolve().parents[1] / "docs" / "SCENARIOS.md"),
    )
    args = parser.parse_args(argv)

    doc = Path(args.doc)
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""
    section = build_section()

    if BEGIN in text and END in text:
        head = text.split(BEGIN)[0]
        tail = text.split(END, 1)[1]
        updated = head + section + tail
    else:
        updated = text.rstrip() + "\n\n" + section + "\n"

    if args.check:
        if updated != text:
            print(
                "docs/SCENARIOS.md is out of date; run "
                "python scripts/generate_scenario_docs.py",
                file=sys.stderr,
            )
            return 1
        print("docs/SCENARIOS.md is up to date")
        return 0

    doc.write_text(updated, encoding="utf-8")
    print("wrote {0} ({1} scenarios)".format(doc, len(list((configs_dir() / 'scenarios').glob('*.yaml')))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
