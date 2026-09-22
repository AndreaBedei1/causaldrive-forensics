#!/usr/bin/env python3
"""Acquire one raw CARLA scenario run."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.common.config import available_scenarios, load_run_config
from cdf.simulation.carla_client import client_from_config
from cdf.simulation.runner import run_scenario
from cdf.simulation.scenario_base import ScenarioSpec


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire raw CARLA data for one scenario")
    parser.add_argument("--scenario", required=True, help="scenario id, for example S01")
    parser.add_argument("--variant", default=None, help="configured scenario variant")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--output", default="traces")
    parser.add_argument("--sensor-profile", default=None)
    parser.add_argument("--override", action="append", default=[])
    parser.add_argument("--no-autostart", action="store_true", help="do not start a local CARLA process")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    cfg = load_run_config(args.scenario, sensor_profile=args.sensor_profile, overrides=args.override)
    spec = ScenarioSpec.from_config(cfg, variant=args.variant)
    client = client_from_config(cfg, autostart=not args.no_autostart)
    path = run_scenario(client, cfg, spec, args.seed, output_root=args.output)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
