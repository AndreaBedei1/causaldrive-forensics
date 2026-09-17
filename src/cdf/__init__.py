"""carla-distributed-causal-forensics.

A multi-vehicle forensic reconstruction system in which every participant
vehicle is its own ego vehicle: it records only its own onboard evidence
(telemetry, controls, radar), builds a local event graph and a local causal DAG,
and only afterwards are the independent local reconstructions fused into a
single multi-vehicle causal DAG.

The package is organised around a strict, structurally enforced data boundary:

``cdf.local``
    Per-participant inference. May use only onboard evidence.
``cdf.fusion``
    Post-event fusion of exchanged local logs and graphs. May not use CARLA
    actor identities, map data or oracle labels.
``cdf.oracle``
    Privileged ground truth. Used exclusively for evaluation and never fed back
    into local or fused inference.

See ``docs/DATA_BOUNDARY.md`` for the full specification and
``tests/test_no_privileged_leakage.py`` for the automated enforcement.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
