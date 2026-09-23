#!/usr/bin/env python3
"""Privileged validation-site search; never imported by online perception."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cdf.simulation.carla_client import connect_with_retry, import_carla  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="List CARLA OpenDRIVE YieldSign landmarks (evaluation only)")
    parser.add_argument("--host", default="127.0.0.1"); parser.add_argument("--port", type=int, default=2000)
    parser.add_argument("--map", default=None, help="optional map to load for site inspection")
    args = parser.parse_args(); carla = import_carla(); client = connect_with_retry(args.host, args.port)
    if args.map:
        world = client.load_world(args.map)
    else:
        world = client.get_world()
    landmarks = world.get_map().get_all_landmarks_of_type("205")
    print(json.dumps({"map": world.get_map().name, "yield_landmarks": [
        {"id": int(landmark.id), "x": landmark.transform.location.x,
         "y": landmark.transform.location.y, "z": landmark.transform.location.z,
         "yaw_deg": landmark.transform.rotation.yaw}
        for landmark in landmarks]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
