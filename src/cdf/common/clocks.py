"""Deterministic recorder clocks. Profile generation belongs to producers only.

The simulator continues to use physical time. Neither inference nor the aligned
view calls this generator: true parameters are persisted only under oracle/.
The configured perturbations are experimental settings, not measured hardware.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from .config import Config


@dataclass(frozen=True)
class ClockModel:
    offset_s: float = 0.0
    scale: float = 1.0

    def __post_init__(self) -> None:
        if (
            not math.isfinite(self.offset_s)
            or not math.isfinite(self.scale)
            or self.scale <= 0
        ):
            raise ValueError("clock parameters must be finite with positive scale")

    def to_local(self, t: float) -> float:
        return self.scale * float(t) + self.offset_s

    @property
    def drift_ppm(self) -> float:
        return (self.scale - 1.0) * 1e6


class LocalClock:
    """One affine clock with seeded jitter, shared by this recorder's streams.

    A timestamp is drawn once per tick and cached, including for delayed sensor
    callbacks. New ticks advance strictly even with excessive configured jitter.
    Local sequence numbers have an independent origin; CARLA frame identifiers
    are not exported as a cross-recorder synchronization channel.
    """

    def __init__(
        self,
        model: ClockModel,
        seed: int = 0,
        jitter_std_s: float = 0.0,
        independent: bool = True,
    ) -> None:
        if jitter_std_s < 0 or not math.isfinite(jitter_std_s):
            raise ValueError("clock jitter must be finite and nonnegative")
        self.model = model
        self.independent = bool(independent)
        self.jitter_std_s = float(jitter_std_s)
        self._rng = random.Random(seed)
        self._sequence_origin = self._rng.randrange(10000, 1000000000)
        self._first_frame: Optional[int] = None
        self._last_sim: Optional[float] = None
        self._last_local: Optional[float] = None
        self._cache: Dict[int, Tuple[float, int]] = {}

    @classmethod
    def for_participant(
        cls, cfg: Config, seed: int, participant: str, context: str = ""
    ) -> "LocalClock":
        settings = cfg.get("clocks", {}) or {}
        payload = json.dumps(
            [int(seed), str(participant), context, settings], sort_keys=True
        )
        clock_seed = int(hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16], 16)
        rng = random.Random(clock_seed)
        independent = bool(settings.get("independent", False))

        def draw(name: str, bound: str) -> float:
            block = settings.get(name, {}) or {}
            value = float(block.get(bound, 0.0))
            if value < 0 or not math.isfinite(value):
                raise ValueError("invalid clocks.{0}.{1}".format(name, bound))
            return (
                rng.uniform(-value, value)
                if independent and block.get("enabled", False)
                else 0.0
            )

        offset = draw("offset", "max_abs_s")
        drift = draw("drift", "max_abs_ppm")
        jitter = settings.get("jitter", {}) or {}
        std = (
            float(jitter.get("std_s", 0.0))
            if independent and jitter.get("enabled", False)
            else 0.0
        )
        return cls(ClockModel(offset, 1.0 + drift * 1e-6), clock_seed, std, independent)

    def stamp(self, t_sim: float, frame: int) -> Tuple[float, int]:
        if not self.independent:
            return float(t_sim), int(frame)
        if frame in self._cache:
            return self._cache[frame]
        if not math.isfinite(t_sim):
            raise ValueError("non-finite recorder time")
        if self._last_sim is not None and t_sim < self._last_sim - 1e-8:
            raise ValueError("uncached sensor tick predates recorder history")
        if self._first_frame is None:
            self._first_frame = int(frame)
        local = self.model.to_local(t_sim) + self._rng.gauss(0.0, self.jitter_std_s)
        if self._last_local is not None:
            local = max(local, self._last_local + 1e-9)
        result = (float(local), self._sequence_origin + int(frame) - self._first_frame)
        self._last_sim, self._last_local = float(t_sim), float(local)
        self._cache[int(frame)] = result
        # Bounded history comfortably covers a rolling window and callback lag.
        if len(self._cache) > 4096:
            del self._cache[min(self._cache)]
        return result

    def ground_truth(self) -> Dict[str, Any]:
        """Producer/evaluation-only description; never a local artifact."""
        return {
            "true_offset_s": self.model.offset_s,
            "true_scale": self.model.scale,
            "true_drift_ppm": self.model.drift_ppm,
            "jitter_std_s": self.jitter_std_s,
            "independent": self.independent,
        }
