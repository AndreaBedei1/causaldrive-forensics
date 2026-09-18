"""Normative reasoning, kept in its own layer.

``graph``
    obligations, violations, and the contribution claim that needs both a rule
    broken and a physical path to the outcome.
``priority``
    the right-of-way benchmark, which is allowed to return "ambiguous".
``report``
    eight findings per participant, none of them a number.

Nothing here decides legal fault, and the vocabulary is chosen so that it
cannot be mistaken for doing so.
"""

from .graph import RESPONSIBILITY_NODE_TYPES, build_responsibility_graph
from .priority import BENCHMARK_RULE, PRIORITY_VERDICTS, benchmark_priority
from .report import EVIDENCE_LEVELS, build_responsibility_report

__all__ = [
    "RESPONSIBILITY_NODE_TYPES",
    "build_responsibility_graph",
    "BENCHMARK_RULE",
    "PRIORITY_VERDICTS",
    "benchmark_priority",
    "EVIDENCE_LEVELS",
    "build_responsibility_report",
]
