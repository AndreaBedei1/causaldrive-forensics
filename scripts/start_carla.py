#!/usr/bin/env python3
"""Start CARLA with deterministic NVIDIA adapter selection and keep it alive."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cdf.simulation.carla_client import CarlaServer, query_nvidia_gpus


def main() -> int:
    parser = argparse.ArgumentParser(description="Start a local CARLA 0.9.15 server")
    parser.add_argument("--carla-root", default=None)
    parser.add_argument("--port", type=int, default=2000)
    parser.add_argument("--quality", default="Low")
    parser.add_argument("--gpu", default="auto", help="auto, adapter index, or none")
    parser.add_argument("--no-offscreen", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    gpu = None if str(args.gpu).lower() in {"none", "null", "off"} else args.gpu
    server = CarlaServer(root=args.carla_root, port=args.port, quality=args.quality,
                         offscreen=not args.no_offscreen, gpu=gpu)
    client = server.start()
    print("CARLA client/server:", client.get_server_version())
    print("CARLA PID(s):", server._server_pids())
    print("GPU query:", query_nvidia_gpus())
    print("Launch command:", " ".join(server.command()))
    try:
        while server._server_pids() or server.is_running():
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
