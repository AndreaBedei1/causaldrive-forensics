"""Executable metric temporal logic over a finite, partially observed trace.

Four modules, in the order they depend on each other:

``syntax``
    the formulae -- occurrence atoms, the Boolean connectives, and four metric
    operators. The object that is rendered into a report is the object that is
    evaluated, which is the difference between this and what it replaced.
``trace``
    what a formula is evaluated against: the events, the horizon of the
    recording, and how much of any interval the evidence actually covers.
``evaluator``
    three-valued evaluation. Time nobody watched yields ``UNKNOWN``, never
    ``PASS`` and never ``FAIL``.
``properties``
    the eight obligations from the brief, written as formulae.
``report``
    running them, and keeping vacuity separate from success.
"""

from .properties import PROPERTIES, TemporalProperty, property_by_id
from .report import check_all, check_property, describe_properties
from .trace import EventTrace

__all__ = [
    "PROPERTIES",
    "TemporalProperty",
    "property_by_id",
    "check_all",
    "check_property",
    "describe_properties",
    "EventTrace",
]
