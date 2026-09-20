#!/usr/bin/env python
"""Rebuild the hero image: three recorded dashcams at one reconstructed instant.

Every frame is decoded from a video the campaign actually recorded, and every
number in the caption is read from that run's own artifacts. Nothing is drawn
that was not measured, and there is no hand-placed annotation anywhere in it --
which is the point, because a figure in a forensics project that cannot be
regenerated from the evidence is a drawing.

The default run is the second of the two impacts in `S14/c_pushes_b`, where C
has already pushed B and B is now in contact with A. It was chosen because it
makes the point the project exists for: B and C both feel the contact, and A,
the vehicle being struck from behind, sees nothing at all. No single recorder
holds the account.

Usage::

    python scripts/make_hero_figure.py
    python scripts/make_hero_figure.py --run artifacts_v2/S16_.../seed_000_consequential \\
        --impact-index 1 --out docs/assets/causaldrive_hero.png

This script lives in the repository rather than in a scratch directory because
the figure has to be rebuilt whenever the campaign behind it is re-recorded, and
an image whose provenance is a script nobody kept is an image nobody can check.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from typing import Tuple

import cv2
from PIL import Image, ImageDraw, ImageFont

DEFAULT_RUN = "artifacts_v2/S14_three_car_chain/seed_000_c_pushes_b"
DEFAULT_OUT = "docs/assets/causaldrive_hero.png"

INK, PAPER, RULE, DIM = (18, 20, 24), (247, 247, 245), (196, 198, 200), (104, 108, 114)
PANEL_W, PANEL_H, GAP, MARGIN = 480, 270, 18, 40
HEAD, LABEL, FOOT = 128, 74, 150


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    for name in (("segoeuib.ttf", "arialbd.ttf") if bold else ("segoeui.ttf", "arial.ttf")):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _read(run: str, *parts: str) -> dict:
    with io.open(os.path.join(run, *parts), encoding="utf-8") as handle:
        return json.load(handle)


def _frame_at(run: str, pid: str, t_local: float) -> Tuple[Image.Image, float]:
    """The recorded frame nearest ``t_local``, decoded from that vehicle's video."""
    vdir = os.path.join(run, "vehicle_%s" % pid, "video")
    index = _read(vdir, "frame_index.json")
    best = min(index["frames"], key=lambda f: abs(float(f["t_local"]) - t_local))
    cap = cv2.VideoCapture(os.path.join(vdir, "front.mp4"))
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(best["i"]))
    ok, bgr = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError("could not decode frame %d for %s" % (best["i"], pid))
    return Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)), float(best["t_local"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--run", default=DEFAULT_RUN, help="recorded run to draw from")
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--impact-index", type=int, default=1,
                        help="which reconstructed impact to show, in time order")
    args = parser.parse_args(argv)
    run = args.run

    align = _read(run, "fusion", "clock_alignment.json")
    recon = _read(run, "fusion", "incident_reconstruction.json")
    metrics = _read(run, "evaluation", "metrics.json")
    manifest = _read(run, "manifest.json")

    reference = align["reference"]
    offsets = {p: m.get("offset_s") for p, m in align["offsets"].items()}
    sources = {p: m.get("source") for p, m in align["offsets"].items()}
    clock = metrics["clock_alignment"]
    true_offset = {p["participant"]: p["true_relative_offset_s"]
                   for p in clock["participants"]}

    order = sorted(recon["collision_order"], key=lambda c: float(c["t_common"]))
    if not order:
        raise SystemExit("%s reconstructed no collisions; nothing to show" % run)
    shown = order[min(args.impact_index, len(order) - 1)]
    t_common = float(shown["t_common"])
    struck = set(shown["participants"])
    pids = sorted(offsets)

    width = MARGIN * 2 + PANEL_W * len(pids) + GAP * (len(pids) - 1)
    height = MARGIN + HEAD + PANEL_H + LABEL + FOOT
    canvas = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(canvas)
    f_title, f_lede = _font(40, bold=True), _font(19)
    f_pid, f_meta, f_small, f_foot = _font(21, bold=True), _font(15), _font(14), _font(15)

    x, y = MARGIN, MARGIN
    draw.text((x, y), "CausalDrive Forensics", font=f_title, fill=INK)
    y += 50
    draw.text((x, y),
              "Three vehicles record the same chain collision on three unsynchronised "
              "clocks. Each keeps only what its own sensors saw.",
              font=f_lede, fill=DIM)
    y += 26
    draw.text((x, y),
              "The common timeline below was estimated from the shared observations "
              "alone, with no simulator state and no map.",
              font=f_lede, fill=DIM)

    top = MARGIN + HEAD
    for i, pid in enumerate(pids):
        off = float(offsets[pid])
        img, actual = _frame_at(run, pid, t_common - off)
        px = MARGIN + i * (PANEL_W + GAP)
        canvas.paste(img.resize((PANEL_W, PANEL_H), Image.LANCZOS), (px, top))
        draw.rectangle([px, top, px + PANEL_W - 1, top + PANEL_H - 1], outline=RULE)

        ly = top + PANEL_H + 10
        role = ("reference recorder" if pid == reference
                else "placed by %s" % str(sources[pid]).lower())
        draw.text((px, ly), "Vehicle %s" % pid, font=f_pid, fill=INK)
        draw.text((px + draw.textlength("Vehicle %s  " % pid, font=f_pid), ly + 4),
                  role, font=f_small, fill=DIM)
        ly += 26
        draw.text((px, ly), "own clock  t = %.3f s" % actual, font=f_meta, fill=INK)
        ly += 20
        draw.text((px, ly),
                  ("offset 0 by definition; a common timeline is fixed up to a constant"
                   if pid == reference else
                   "offset %+.3f s estimated, %+.3f s true" % (off, true_offset[pid])),
                  font=f_small, fill=DIM)

    fy = top + PANEL_H + LABEL + 8
    draw.line([MARGIN, fy, width - MARGIN, fy], fill=RULE, width=1)
    fy += 14
    draw.text((MARGIN, fy),
              "One instant on the estimated common clock: t = %.3f s, %s in contact."
              % (t_common, " and ".join(sorted(struck))),
              font=f_pid, fill=INK)
    fy += 28
    spread = sorted(float(v) for v in offsets.values())
    draw.text((MARGIN, fy),
              "Their clocks sat %.2f s and %.2f s apart. Aligned from shared "
              "observations alone, the three land on one timeline to %.0f microseconds "
              "mean absolute error in this run."
              % (spread[0], spread[-1], clock["mean_abs_offset_error_s"] * 1e6),
              font=f_foot, fill=INK)
    fy += 24
    draw.text((MARGIN, fy),
              "The reconstruction orders both impacts: %s."
              % ", then ".join("%s at %.3f s" % ("".join(c["participants"]),
                                                 float(c["t_common"])) for c in order),
              font=f_foot, fill=DIM)
    fy += 24
    draw.text((MARGIN, fy),
              "%s   %s / %s   seed %d   %s   CARLA 0.9.15, %s"
              % (manifest["run_id"], manifest["scenario_id"], manifest["variant"],
                 manifest["seed"], align["status"], manifest["map_name"]),
              font=f_small, fill=DIM)

    canvas.save(args.out, "PNG", optimize=True)
    unsighted = sorted(set(pids) - struck)
    print("wrote %s  %dx%d  %.1f KB  (unsighted at this instant: %s)"
          % (args.out, width, height, os.path.getsize(args.out) / 1024.0,
             ", ".join(unsighted) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
