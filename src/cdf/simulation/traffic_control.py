"""Putting signs where a scenario says they are, and recording what is true.

Two jobs that must not be confused, and this module does both because they share
one source: the scenario's ``traffic_control`` block.

**At construction time** it places what the map may not provide. CARLA does not
put a physical stop sign on every approach a scenario might want, and an approach
with no sign on it cannot be perceived — a camera that finds nothing where the
scenario says there is a sign has not failed, it has been asked an unanswerable
question. Where a real sign already stands at the declared place, that one is
used and nothing is spawned.

**At evaluation time** the same block is the privileged traffic-control ground
truth: the true class of each sign, where it stands, where its stop line is, and
which approach it governs. That is what perception is scored against.

What must never happen is the second leaking into the first. Local inference sees
signs only through the camera; this module writes to ``oracle/`` and to the world,
never to a vehicle. The anti-leakage suite checks that local code cannot reach the
CARLA sign API at all.

## Placing a sign so it can be read

A sign the camera cannot resolve is a sign the scenario did not really place. The
placement therefore has to put it where an approaching vehicle will see it grow
in the centre of frame: to the right of the lane, at windscreen height, facing
back down the approach. Those are the three things that decide whether the
detector has a chance, and each is derived from the approach waypoint rather than
guessed.
"""

from __future__ import annotations

import logging
import math
from typing import Any, Dict, List, Mapping, Optional, Sequence

from ..common.config import Config
from ..common.schemas import SCHEMA_VERSIONS, Provenance

LOGGER = logging.getLogger(__name__)

__all__ = [
    "SIGN_BLUEPRINTS",
    "place_traffic_control",
    "traffic_control_truth",
    "stop_lines_truth",
]

#: What to spawn for each declared sign kind. CARLA ships both as static props,
#: which is what makes the camera route possible at all: the vehicle sees the
#: same geometry and texture a real approach would show it.
SIGN_BLUEPRINTS: Dict[str, str] = {
    "stop": "static.prop.streetsign",
    "yield": "static.prop.streetsign",
}

#: Blueprints that actually depict the sign they are named for, tried in order.
#:
#: This list used to fall back to ``static.prop.streetsign`` -- a blank
#: rectangular street sign -- when no stop-sign prop was found, and the packaged
#: CARLA 0.9.15 build ships **no** stop or yield prop at all, so every run took
#: that fallback. A generic street sign was spawned, the record said a stop sign
#: was physically present, and the perception ground truth then asserted a red
#: octagon that had never existed. The camera scored a false negative against a
#: sign that was not there.
#:
#: A substitute that does not look like the sign is worse than no sign: it makes
#: the reference wrong rather than merely incomplete. So the fallbacks are gone,
#: and an absent blueprint is reported as an absent sign.
_BLUEPRINT_CANDIDATES: Dict[str, Sequence[str]] = {
    "stop": ("static.prop.trafficsign_stop",),
    "yield": ("static.prop.trafficsign_yield",),
}

#: How close a rendered sign mesh has to be to the declared position to count as
#: the sign the scenario means. Generous: the scenario anchors on a lane and the
#: map's sign stands on the verge beside it.
_MAP_SIGN_RADIUS_M = 12.0

#: Substrings identifying a rendered mesh as the sign kind. CARLA names the stop
#: meshes ``BP_Stop*``.
_MESH_NAME_HINTS: Dict[str, Sequence[str]] = {
    "stop": ("stop",),
    "yield": ("yield", "giveway"),
}

#: Lateral offset from the lane centre, in metres. A sign in the middle of the
#: road would be seen perfectly and would be nothing like a road.
_LATERAL_OFFSET_M = 2.6
#: Height of the sign face. Roughly where a real one sits, and within the
#: camera's vertical field of view at the mounting height used.
_SIGN_HEIGHT_M = 2.2


def _resolve_blueprint(scenario_world: Any, kind: str) -> Optional[str]:
    """The first candidate blueprint this CARLA build actually has."""
    try:
        library = scenario_world.world.get_blueprint_library()
    except AttributeError:  # pragma: no cover - defensive
        return None
    for candidate in _BLUEPRINT_CANDIDATES.get(kind, ()):
        if library.filter(candidate):
            return candidate
    return None


def _rendered_sign_nearby(
    scenario_world: Any, kind: str, location: Any,
) -> Optional[Dict[str, Any]]:
    """The map's own rendered sign of this kind near ``location``, if there is one.

    ``traffic.stop`` *actors* are trigger volumes, and they are not the same
    thing as a sign a camera can see: Town05 carries 33 of those actors and
    renders only 5 sign meshes. Asking for the meshes is the only way to know
    whether there is anything to detect, and it is what makes
    ``physically_present`` a measured claim rather than an assumption.
    """
    try:
        from .carla_client import import_carla

        carla = import_carla()
        objects = scenario_world.world.get_environment_objects(
            carla.CityObjectLabel.TrafficSigns
        )
    except Exception:  # pragma: no cover - build-dependent
        return None

    hints = tuple(h.lower() for h in _MESH_NAME_HINTS.get(kind, ()))
    if not hints:
        return None
    best = None
    for obj in objects:
        name = str(getattr(obj, "name", "")).lower()
        if not any(h in name for h in hints):
            continue
        where = obj.transform.location
        distance = math.sqrt(
            (where.x - location.x) ** 2 + (where.y - location.y) ** 2
        )
        if distance > _MAP_SIGN_RADIUS_M:
            continue
        if best is None or distance < best["distance_m"]:
            best = {
                "mesh_name": str(obj.name),
                "distance_m": round(float(distance), 3),
                "location": {
                    "x": round(float(where.x), 3),
                    "y": round(float(where.y), 3),
                    "z": round(float(where.z), 3),
                },
            }
    return best


def _approach_waypoint(scenario_world: Any, anchor: Mapping[str, Any]) -> Any:
    """Where the sign stands, expressed the way a scenario spawn is.

    Reusing the spawn resolver means a sign and the vehicle it governs are
    positioned by the same code against the same geometry, so "12 m back from the
    junction" means the same thing for both.
    """
    from .scenario_base import SpawnSpec, resolve_spawn_waypoint

    spec = SpawnSpec.from_dict(dict(anchor))
    return resolve_spawn_waypoint(
        scenario_world.map, scenario_world.spawn_points(), spec
    )


def place_traffic_control(
    scenario_world: Any,
    traffic_control: Optional[Mapping[str, Any]],
    cfg: Optional[Config] = None,
) -> Dict[str, Any]:
    """Place the declared signs, and report exactly what was done.

    Returns a record per sign: where it ended up, whether a prop was spawned or a
    map sign was already there, and — when neither worked — why. A scenario whose
    sign could not be placed is not silently a scenario without a sign: the
    record says so, and the run gate can refuse it.
    """
    cfg = cfg if cfg is not None else Config({})
    carla = None
    placed: List[Dict[str, Any]] = []

    for sign in (traffic_control or {}).get("signs", []) or []:
        kind = str(sign.get("kind", "")).lower()
        record: Dict[str, Any] = {
            "sign_id": str(sign.get("sign_id", "")),
            "kind": kind,
            "governs": str(sign.get("governs", "")),
            "spawned": False,
            "blueprint": None,
            "location": None,
            "yaw_deg": None,
            "problem": None,
        }
        try:
            waypoint = _approach_waypoint(scenario_world, sign.get("anchor") or {})
        except Exception as exc:  # pragma: no cover - map-dependent
            record["problem"] = "could not resolve the anchor: {0}".format(exc)
            placed.append(record)
            LOGGER.warning("sign %s: %s", record["sign_id"], record["problem"])
            continue

        if carla is None:
            from .carla_client import import_carla

            carla = import_carla()

        transform = _sign_transform(carla, waypoint)
        record["location"] = {
            "x": round(float(transform.location.x), 3),
            "y": round(float(transform.location.y), 3),
            "z": round(float(transform.location.z), 3),
        }
        record["yaw_deg"] = round(float(transform.rotation.yaw), 2)

        if not bool(sign.get("spawn_prop", True)):
            # The scenario says the map already carries this sign. Check, rather
            # than take its word: a reference asserting an unseeable sign scores
            # the camera against something that was never there.
            found = _rendered_sign_nearby(scenario_world, kind, transform.location)
            if found is None:
                record["problem"] = (
                    "the scenario expects the map's own {0} sign here, but no "
                    "rendered {0}-sign mesh lies within {1:.0f} m. There is "
                    "nothing for a camera to read".format(kind, _MAP_SIGN_RADIUS_M)
                )
                LOGGER.warning("sign %s: %s", record["sign_id"], record["problem"])
            else:
                record["spawned"] = True
                record["source"] = "map"
                record["mesh"] = found
                # Report where the sign actually is, not where the lane anchor
                # put it: the perception metric measures against the real thing.
                record["location"] = found["location"]
            placed.append(record)
            continue

        blueprint = _resolve_blueprint(scenario_world, kind)
        if blueprint is None:
            record["problem"] = (
                "this CARLA build ships no {0}-sign prop, so the approach "
                "carries no sign a camera could read. No substitute is spawned: "
                "a blank street sign standing in for a stop sign would make the "
                "perception reference wrong rather than merely incomplete"
                .format(kind)
            )
            placed.append(record)
            LOGGER.warning("sign %s: %s", record["sign_id"], record["problem"])
            continue

        try:
            actor = scenario_world.spawn_prop(blueprint, transform)
        except Exception as exc:
            record["problem"] = "spawn failed: {0}".format(exc)
            placed.append(record)
            LOGGER.warning("sign %s: %s", record["sign_id"], record["problem"])
            continue

        record["spawned"] = actor is not None
        record["blueprint"] = blueprint
        record["source"] = "prop" if actor is not None else None
        if actor is None:
            record["problem"] = "the spawn point is blocked"
        placed.append(record)

    n_ok = sum(1 for r in placed if r["spawned"])
    if placed:
        LOGGER.info(
            "traffic control: %d of %d declared sign(s) placed", n_ok, len(placed)
        )
    return {
        "n_declared": len(placed),
        "n_placed": n_ok,
        "all_placed": n_ok == len(placed),
        "signs": placed,
        "note": (
            "a sign the camera cannot see is a scenario that did not really "
            "place it, so what was and was not placed is recorded rather than "
            "assumed"
        ),
    }


def _sign_transform(carla: Any, waypoint: Any) -> Any:
    """Put the sign beside the lane, at head height, facing oncoming traffic.

    All three matter for whether the detector has a chance, and all three come
    from the approach waypoint rather than from a guess: a sign facing the wrong
    way is invisible, one in the lane centre is unlike any road, and one at
    ground level leaves the camera's field of view as the vehicle nears it.
    """
    transform = waypoint.transform
    yaw = math.radians(float(transform.rotation.yaw))
    # Right of the lane, in the direction of travel.
    right_x = math.cos(yaw + math.pi / 2.0)
    right_y = math.sin(yaw + math.pi / 2.0)
    location = carla.Location(
        x=float(transform.location.x) + right_x * _LATERAL_OFFSET_M,
        y=float(transform.location.y) + right_y * _LATERAL_OFFSET_M,
        z=float(transform.location.z) + _SIGN_HEIGHT_M,
    )
    # Facing back down the approach, so a vehicle driving towards it sees the
    # face rather than the back.
    rotation = carla.Rotation(
        pitch=0.0, yaw=float(transform.rotation.yaw) + 180.0, roll=0.0
    )
    return carla.Transform(location, rotation)


def traffic_control_truth(
    scenario_world: Any,
    traffic_control: Optional[Mapping[str, Any]],
    placement: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """The privileged truth about the traffic control in this run.

    What perception is scored against: the true class of each sign, where it
    really is, and which approach it really governs. Written to ``oracle/`` and
    read by evaluation only — deleting the oracle directory must not change a
    single inference artifact, which the anti-leakage suite verifies.
    """
    records = list((placement or {}).get("signs", []) or [])
    by_id = {r["sign_id"]: r for r in records}

    signs: List[Dict[str, Any]] = []
    for sign in (traffic_control or {}).get("signs", []) or []:
        sign_id = str(sign.get("sign_id", ""))
        record = by_id.get(sign_id, {})
        signs.append({
            "sign_id": sign_id,
            "kind": str(sign.get("kind", "")).lower(),
            "governs": str(sign.get("governs", "")),
            "location": record.get("location"),
            "yaw_deg": record.get("yaw_deg"),
            "physically_present": bool(record.get("spawned")),
            "placement_problem": record.get("problem"),
            "source": record.get("source"),
            "mesh": record.get("mesh"),
            "stop_line_forward_m": float(sign.get("stop_line_forward_m", 0.0)),
        })

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "provenance": Provenance.ORACLE.value,
        "reference_kind": "traffic_control",
        "signs": signs,
        "tie_break": (traffic_control or {}).get("tie_break"),
        "n_signs": len(signs),
        "n_physically_present": sum(1 for s in signs if s["physically_present"]),
        "note": (
            "privileged. The true class and position of each sign, and which "
            "approach it governs. Used to score what the camera made of them; "
            "never available to inference, which sees signs only as pixels"
        ),
    }


def stop_lines_truth(
    scenario_world: Any,
    traffic_control: Optional[Mapping[str, Any]],
) -> Dict[str, Any]:
    """Where each stop line really is, from the map.

    A stop line is a position along the lane rather than an object, so unlike a
    sign there is nothing to spawn: the scenario says how far forward of the sign
    it lies and the map supplies the geometry. Inference has no access to either
    and infers the crossing from the camera.
    """
    lines: List[Dict[str, Any]] = []
    for sign in (traffic_control or {}).get("signs", []) or []:
        forward = float(sign.get("stop_line_forward_m", 0.0))
        if forward <= 0.0:
            continue
        try:
            waypoint = _approach_waypoint(scenario_world, sign.get("anchor") or {})
            ahead = waypoint.next(forward)
            target = ahead[0] if ahead else waypoint
        except Exception as exc:  # pragma: no cover - map-dependent
            lines.append({
                "sign_id": str(sign.get("sign_id", "")),
                "governs": str(sign.get("governs", "")),
                "problem": "could not resolve the stop line: {0}".format(exc),
            })
            continue
        transform = target.transform
        lines.append({
            "sign_id": str(sign.get("sign_id", "")),
            "governs": str(sign.get("governs", "")),
            "forward_of_sign_m": forward,
            "location": {
                "x": round(float(transform.location.x), 3),
                "y": round(float(transform.location.y), 3),
                "z": round(float(transform.location.z), 3),
            },
            "yaw_deg": round(float(transform.rotation.yaw), 2),
            "map_context": {
                "road_id": int(getattr(target, "road_id", -1)),
                "lane_id": int(getattr(target, "lane_id", 0)),
            },
        })

    return {
        "schema_version": SCHEMA_VERSIONS["graph"],
        "provenance": Provenance.ORACLE.value,
        "reference_kind": "stop_lines",
        "stop_lines": lines,
        "n_stop_lines": len(lines),
        "note": (
            "privileged map geometry. Map identity is kept under map_context so "
            "it reads as context for interpreting a claim rather than as the "
            "claim itself"
        ),
    }
