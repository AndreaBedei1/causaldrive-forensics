#!/usr/bin/env python3
"""Automatic checks of the paper's tables and figures (``results/``).

    python scripts/results_qa.py [--results results]

Tables (``tables/<name>.{csv,md,tex}``): all three formats present, with the same header and the same cells
row by row (the TeX cells after undoing its escapes), no empty cell, no "nan".
Figures (every ``*.pdf`` under ``results``, with its ``.svg``): one page, at most the IEEE double-column width
(7.16 in, warning up to 7.5 in), fonts embedded as TrueType (``/FontFile2``) and no Type 3 font (rejected by IEEE
PDF eXpress), text kept as text in the SVG with every font size >= 6 pt.
Every study record (``*.json`` under ``results`` with a ``provenance``) names its code and configuration hashes,
and the index ``results/README.md`` exists and names every table and figure.
Exit status 1 on any failure; warnings do not fail.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]
MAX_WIDTH_IN, WARN_WIDTH_IN, MIN_FONT_PT = 7.5, 7.16, 6.0


def _untex(cell: str) -> str:
    for a, b in (("$\\pm$", "+-"), ("$\\le$", "<="), ("$\\ge$", ">="), ("\\textbackslash{}", "\\"), ("\\&", "&"),
                 ("\\%", "%"), ("\\#", "#"), ("\\_", "_")):
        cell = cell.replace(a, b)
    return cell.strip()


def check_table(stem: Path, errors: List[str]) -> None:
    paths = {suffix: stem.with_suffix("." + suffix) for suffix in ("csv", "md", "tex")}
    missing = [s for s, p in paths.items() if not p.exists()]
    if missing:
        errors.append("{0}: missing {1}".format(stem.name, ", ".join(missing)))
        return
    with paths["csv"].open(encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    md = [line for line in paths["md"].read_text(encoding="utf-8").splitlines() if line.startswith("| ")]
    md_rows = [[c.strip() for c in line.strip()[1:-1].split(" | ")] for line in md]
    tex_lines = paths["tex"].read_text(encoding="utf-8").splitlines()
    body = tex_lines[tex_lines.index("\\toprule") + 1:tex_lines.index("\\bottomrule")]
    tex_rows = [[_untex(c) for c in line[:-len(" \\\\")].split(" & ")] for line in body if line != "\\midrule"]
    if not (len(rows) == len(md_rows) == len(tex_rows)):
        errors.append("{0}: {1} CSV, {2} MD, {3} TeX rows".format(stem.name, len(rows), len(md_rows), len(tex_rows)))
        return
    for i, (a, b, c) in enumerate(zip(rows, md_rows, tex_rows)):
        if not (a == b == c):
            errors.append("{0}: row {1} differs between formats: {2} / {3} / {4}".format(stem.name, i, a, b, c))
            return
        if any(cell.strip() == "" or cell.lower() == "nan" for cell in a):
            errors.append("{0}: row {1} has an empty or NaN cell: {2}".format(stem.name, i, a))


def check_figure(pdf: Path, errors: List[str], warnings: List[str]) -> None:
    data = pdf.read_bytes()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    if pages != 1:
        errors.append("{0}: {1} pages".format(pdf, pages))
    box = re.search(rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]", data)
    if box:
        width = (float(box.group(3)) - float(box.group(1))) / 72.0
        if width > MAX_WIDTH_IN:
            errors.append("{0}: {1:.2f} in wide (max {2})".format(pdf, width, MAX_WIDTH_IN))
        elif width > WARN_WIDTH_IN:
            warnings.append("{0}: {1:.2f} in wide (IEEE text width {2})".format(pdf, width, WARN_WIDTH_IN))
    if b"/Type3" in data or b"/Subtype /Type3" in data:
        errors.append("{0}: Type 3 font".format(pdf))
    if b"/Font" in data and b"/FontFile2" not in data:
        errors.append("{0}: fonts not embedded as TrueType".format(pdf))
    svg = pdf.with_suffix(".svg")
    if not svg.exists():
        errors.append("{0}: no SVG".format(pdf))
        return
    text = svg.read_text(encoding="utf-8")
    if "<text" not in text:
        errors.append("{0}: text drawn as paths (set svg.fonttype none)".format(svg))
        return
    sizes = [float(v) for v in re.findall(r"font(?:-size)?:\s*(?:[a-z]+\s+)*([\d.]+)px", text)]
    sizes += [float(v) for v in re.findall(r'font-size="([\d.]+)', text)]
    if sizes and min(sizes) < MIN_FONT_PT:
        errors.append("{0}: font size {1} pt < {2}".format(svg, min(sizes), MIN_FONT_PT))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--results", type=Path, default=ROOT / "results")
    args = parser.parse_args(argv)
    errors: List[str] = []
    warnings: List[str] = []
    tables = sorted({p.with_suffix("") for p in (args.results / "tables").glob("*.*")})
    for stem in tables:
        check_table(stem, errors)
    figures = sorted(args.results.rglob("*.pdf"))
    for pdf in figures:
        check_figure(pdf, errors, warnings)
    studies = 0
    for path in args.results.rglob("*.json"):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except ValueError:
            errors.append("{0}: not JSON".format(path))
            continue
        if isinstance(record, dict) and "provenance" in record:
            studies += 1
            prov = record["provenance"]
            if not prov.get("code_sha256") or "git_commit" not in prov:
                errors.append("{0}: incomplete provenance".format(path))
    index = args.results / "README.md"
    if not index.exists():
        errors.append("results/README.md missing")
    else:
        text = index.read_text(encoding="utf-8")
        for stem in tables:
            if "`{0}`".format(stem.name) not in text:
                errors.append("README does not name table {0}".format(stem.name))
        for pdf in (args.results / "figures").glob("*.pdf"):
            if "`{0}`".format(pdf.stem) not in text:
                errors.append("README does not name figure {0}".format(pdf.stem))
    print("{0} tables, {1} figures, {2} study records checked".format(len(tables), len(figures), studies))
    for warning in warnings:
        print("WARN", warning)
    for error in errors:
        print("FAIL", error)
    print("PASS" if not errors else "FAIL ({0})".format(len(errors)))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
