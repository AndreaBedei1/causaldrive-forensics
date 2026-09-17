"""Shared, dependency-light foundations: schemas, geometry, time, IO, config."""

from .config import Config, load_run_config
from .schemas import (
    CausalEdgeType,
    Event,
    EventEdgeType,
    EventType,
    GraphDocument,
    GraphEdge,
    Provenance,
    SCHEMA_VERSIONS,
)

__all__ = [
    "Config",
    "load_run_config",
    "CausalEdgeType",
    "Event",
    "EventEdgeType",
    "EventType",
    "GraphDocument",
    "GraphEdge",
    "Provenance",
    "SCHEMA_VERSIONS",
]
