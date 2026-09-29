"""A tiny deterministic two-vehicle rear-end run in the raw recording format.

A drives along +x at 10 m/s; B starts 20 m ahead at 6 m/s; A's front meets
B's rear at physical time 3.9 s and both stop.  Each recorder has its OWN raw
clock (A reads 100 + t, B reads 250 + t) and B starts recording ``b_late_start_s``
later, so the two local clocks disagree.  A's forward radar sees B's rear face
(until ``a_sees_b_until``) plus static poles; B's radar sees only poles.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import List, Optional

import numpy as np

V_A, V_B, GAP_M = 10.0, 6.0, 20.0
CONTACT_T = (GAP_M - 2.0 - 2.4) / (V_A - V_B)  # B's rear at x-2.0, A's front at x+2.4
DURATION_S = 6.0
IMPULSE = 5000.0
RADAR_MOUNT = {"x": 2.2, "y": 0.0, "z": 1.0, "yaw_deg": 0.0, "pitch_deg": 0.0}


def _x_a(t: float) -> float:
    return V_A * min(t, CONTACT_T)


def _x_b(t: float) -> float:
    return GAP_M + V_B * min(t, CONTACT_T)


def _speed(t: float, v: float) -> float:
    return v if t < CONTACT_T else 0.0


def _detection(sensor, point, sensor_velocity, point_velocity):
    dx, dy, dz = (point[i] - sensor[i] for i in range(3))
    depth = math.sqrt(dx * dx + dy * dy + dz * dz)
    unit = (dx / depth, dy / depth, dz / depth)
    range_rate = sum((point_velocity[i] - sensor_velocity[i]) * unit[i] for i in range(3))
    return [depth, math.atan2(dy, dx), math.atan2(dz, math.hypot(dx, dy)), range_rate]


def _poles() -> List[tuple]:
    return [(10.0 * k, side * 7.0, height) for k in range(1, 12) for side in (-1, 1) for height in (0.6, 1.4)]


def _write_jsonl(path: Path, rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def _write_radar(folder: Path, times, detections) -> None:
    offsets = np.cumsum([0] + [len(rows) for rows in detections]).astype(np.int64)
    rows = np.asarray([row for frame in detections for row in frame], dtype=np.float32).reshape(-1, 4)
    folder.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(folder / "observations.npz", frames=np.arange(len(times), dtype=np.int64),
                        timestamps=np.asarray(times, dtype=np.float64), offsets=offsets, detections=rows)
    (folder / "metadata.json").write_text(json.dumps({"source": "radar", "sensor_transform": RADAR_MOUNT}),
                                          encoding="utf-8")


def make_run(root: Path, b_late_start_s: float = 0.5, a_sees_b_until: Optional[float] = None,
             with_ground_truth: bool = True) -> Path:
    """Write ``root/vehicles/{A,B}`` (and a poisoned ``ground_truth/``); return root."""
    rng = np.random.RandomState(7)
    for owner, clock_zero, start in (("A", 100.0, 0.0), ("B", 250.0, b_late_start_s)):
        # Each recorder samples every 50 ms on its own grid from its own start.
        times = [round(start + 0.05 * k, 4) for k in range(int((DURATION_S - start) / 0.05) + 1)]
        folder = root / "vehicles" / owner
        ego, controls, radar_times, radar_rows = [], [], [], []
        for t in times:
            x = _x_a(t) if owner == "A" else _x_b(t)
            v = _speed(t, V_A if owner == "A" else V_B)
            stamp = clock_zero + t
            ego.append({"frame": 0, "timestamp": stamp, "x": x, "y": 0.0, "z": 0.0, "roll_deg": 0.0,
                        "pitch_deg": 0.0, "yaw_deg": 0.0, "velocity": {"x": v, "y": 0.0, "z": 0.0},
                        "acceleration": {"x": 0.0, "y": 0.0, "z": 0.0},
                        "angular_velocity": {"x": 0.0, "y": 0.0, "z": 0.0}})
            braking = owner == "A" and t >= 3.0
            controls.append({"frame": 0, "timestamp": stamp, "throttle": 0.0 if braking else 0.4,
                             "brake": 0.8 if braking else 0.0, "steer": 0.0, "hand_brake": False, "reverse": False})
            sensor = (x + 2.2, 0.0, 1.0)
            own_velocity = (v, 0.0, 0.0)
            frame = []
            for pole in _poles():
                if pole[0] > sensor[0] + 1.0 and pole[0] - sensor[0] < 90.0:
                    frame.append(_detection(sensor, pole, own_velocity, (0.0, 0.0, 0.0)))
            visible = a_sees_b_until is None or t <= a_sees_b_until
            if owner == "A" and visible:
                rear = _x_b(t) - 2.0
                for lateral in (-0.7, -0.2, 0.3, 0.8):
                    for height in (0.6, 1.1):
                        point = (rear + rng.normal(0, 0.05), lateral + rng.normal(0, 0.05), height)
                        frame.append(_detection(sensor, point, own_velocity, (_speed(t, V_B), 0.0, 0.0)))
            radar_times.append(stamp)
            radar_rows.append(frame)
        _write_jsonl(folder / "ego.jsonl", ego)
        _write_jsonl(folder / "controls.jsonl", controls)
        _write_jsonl(folder / "collisions.jsonl", [{"frame": 0, "timestamp": clock_zero + CONTACT_T, "impulse": IMPULSE}])
        _write_jsonl(folder / "traffic_signs.jsonl", [])
        _write_radar(folder / "radar", radar_times, radar_rows)
    if with_ground_truth:
        truth = root / "ground_truth"
        truth.mkdir(parents=True, exist_ok=True)
        for name in ("states.jsonl", "collisions.jsonl", "controls.jsonl"):
            # Poison: any attempt to parse privileged files fails loudly.
            (truth / name).write_text("POISON: reconstruction must never read ground_truth\n", encoding="utf-8")
    return root
