"""Driver that evaluates the property registry over recorded evidence.

The checker is deliberately thin: all semantics live in
:mod:`cdf.checking.properties`. What this module adds is the discipline around
them.

* **Layer separation is enforced, not assumed.** :meth:`TraceChecker.check_participant`
  refuses to run a property whose scope is not ``LOCAL``, and
  :meth:`TraceChecker.check_oracle` refuses anything that is not ``ORACLE``. The
  two produce separate reports, so a privileged verdict can never be merged into
  the local evidence a downstream stage reads.
* **Failures are loud.** A property that raises aborts the run with the
  participant and property named, instead of being silently recorded as
  ``UNKNOWN`` -- an implementation bug and a genuine lack of evidence are very
  different things and must not look alike.
* **Reports are self-describing.** Each report carries the configuration hash and
  the formal statement of every property evaluated, so a verdict read months
  later is interpretable without the code that produced it.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.io import write_json
from ..common.evidence import ParticipantEvidence, RunEvidence
from ..common.schemas import CheckStatus, Provenance, SCHEMA_VERSIONS
from .properties import (
    LOCAL_PROPERTIES,
    ORACLE_PROPERTIES,
    Property,
    PropertyResult,
    oracle_participant_ids,
)

__all__ = ["TraceChecker", "summarise_results"]


#: Verdict keys reported in every summary block, in a fixed order so that two
#: reports can be diffed line by line.
_STATUS_KEYS = (CheckStatus.PASS.value, CheckStatus.FAIL.value, CheckStatus.UNKNOWN.value)


def summarise_results(results: Sequence[PropertyResult]) -> Dict[str, int]:
    """Count verdicts by status, always reporting all three keys.

    All three are emitted even when zero so that downstream consumers (plots,
    tables, the viewer) never have to guess whether a missing key means zero or
    means the checker did not run.
    """
    counts = {k: 0 for k in _STATUS_KEYS}
    for res in results:
        counts[res.status.value] = counts.get(res.status.value, 0) + 1
    return counts


class TraceChecker:
    """Evaluates finite-trace properties over one run's recorded evidence.

    Parameters
    ----------
    cfg:
        The resolved run configuration. Every threshold a property uses is read
        from it, and its hash is stamped into the report.
    properties:
        Optional explicit local property list. Defaults to
        :data:`~cdf.checking.properties.LOCAL_PROPERTIES`, optionally filtered by
        the ``checking.enabled_properties`` configuration key.
    """

    def __init__(
        self, cfg: Config, properties: Optional[Sequence[Property]] = None
    ) -> None:
        self.cfg = cfg
        selected = list(properties) if properties is not None else list(LOCAL_PROPERTIES)
        enabled = cfg.get("checking.enabled_properties", None)
        if enabled:
            wanted = set(str(x) for x in enabled)
            unknown = wanted - set(p.property_id for p in selected)
            if unknown:
                raise KeyError(
                    "checking.enabled_properties names unknown properties: {0}".format(
                        ", ".join(sorted(unknown))
                    )
                )
            selected = [p for p in selected if p.property_id in wanted]
        for prop in selected:
            if prop.scope is not Provenance.LOCAL:
                raise ValueError(
                    "property {0!r} has scope {1} and cannot be used as a local "
                    "property".format(prop.property_id, prop.scope.value)
                )
        self.properties: List[Property] = selected

    # -- local ------------------------------------------------------------

    def check_participant(self, ev: ParticipantEvidence) -> List[PropertyResult]:
        """Evaluate every local property on one participant's own evidence.

        Results come back in registry order so that reports for different
        participants line up.
        """
        context: Dict[str, Any] = {
            "participant_id": ev.participant_id,
            "config_hash": self.cfg.hash,
        }
        out: List[PropertyResult] = []
        for prop in self.properties:
            out.append(self._evaluate(prop, ev, context, Provenance.LOCAL))
        return out

    def check_run(self, run: RunEvidence) -> Dict[str, Any]:
        """Evaluate every local property on every participant of a run.

        The returned mapping is the on-disk shape of
        ``checking/model_check_results.json``. It contains **no** oracle verdicts:
        those are produced by :meth:`check_oracle` and persisted separately, which
        is what keeps the privileged layer out of the local artifact tree.
        """
        return self.check_run_with_results(run)[0]

    def check_run_with_results(
        self, run: RunEvidence
    ) -> Tuple[Dict[str, Any], List[PropertyResult]]:
        """:meth:`check_run`, also returning the results the report was built from.

        The counterexample report needs the :class:`PropertyResult` objects, not
        their serialised form, and evaluating every property twice to get them
        would be both wasteful and a way for the two artifacts to disagree.
        """
        results: List[PropertyResult] = []
        by_participant: Dict[str, Any] = {}
        for pid in run.participant_ids:
            per = self.check_participant(run.get(pid))
            results.extend(per)
            by_participant[pid] = {
                "summary": summarise_results(per),
                "statuses": {r.property_id: r.status.value for r in per},
            }

        by_property: Dict[str, Any] = {}
        for prop in self.properties:
            subset = [r for r in results if r.property_id == prop.property_id]
            by_property[prop.property_id] = {
                "summary": summarise_results(subset),
                "statuses": {r.participant_id: r.status.value for r in subset},
                "formal": prop.formal,
            }

        report = {
            "schema_version": SCHEMA_VERSIONS["model_check"],
            "scope": Provenance.LOCAL.value,
            "run_id": run.run_id,
            "scenario_id": run.scenario_id,
            "seed": run.seed,
            "config_hash": self.cfg.hash,
            "properties": [p.describe() for p in self.properties],
            "results": [r.to_dict() for r in results],
            "summary": summarise_results(results),
            "by_participant": by_participant,
            "by_property": by_property,
        }
        return report, results

    def check_and_persist(self, layout: Any, run: RunEvidence) -> Dict[str, Any]:
        """Check a run and write **both** checking artifacts.

        Every ``FAIL`` result carries a ``counterexample_ref``, so writing
        ``model_check_results.json`` without ``counterexamples.json`` leaves
        those references pointing at a file that does not exist -- and the
        viewer, which resolves them, shows "counterexample report missing"
        instead of the trace. Persisting both from one call is what stops the
        two from drifting apart again.
        """
        from .counterexamples import build_counterexample_report

        report, results = self.check_run_with_results(run)
        layout.checking_dir.mkdir(parents=True, exist_ok=True)
        write_json(layout.model_check_results, report)
        write_json(layout.counterexamples,
                   build_counterexample_report(results, run, self.cfg))
        return report

    # -- oracle (privileged, kept separate) -------------------------------

    def check_oracle(self, oracle_trace: Dict[str, Any]) -> List[PropertyResult]:
        """Evaluate the privileged properties on a plain oracle trace mapping.

        Kept as a separate entry point returning a separate list: nothing here
        touches :class:`~cdf.common.evidence.ParticipantEvidence`, and the caller
        must persist the outcome under the run's ``oracle``/evaluation artifacts
        rather than mixing it into the local checking report.
        """
        pids = oracle_participant_ids(oracle_trace)
        targets: List[Optional[str]] = list(pids) if pids else [None]
        out: List[PropertyResult] = []
        for prop in ORACLE_PROPERTIES:
            if prop.scope is not Provenance.ORACLE:
                raise ValueError(
                    "property {0!r} is registered as an oracle property but has "
                    "scope {1}".format(prop.property_id, prop.scope.value)
                )
            for pid in targets:
                context: Dict[str, Any] = {"config_hash": self.cfg.hash}
                if pid is not None:
                    context["participant_id"] = pid
                out.append(
                    self._evaluate(prop, oracle_trace, context, Provenance.ORACLE)
                )
        return out

    # -- internals --------------------------------------------------------

    def _evaluate(
        self,
        prop: Property,
        subject: Any,
        context: Dict[str, Any],
        expected_scope: Provenance,
    ) -> PropertyResult:
        """Run one evaluator and validate what it returned.

        The validation is not paranoia: a property that silently reports the
        wrong scope or the wrong id would corrupt the layer separation the whole
        design rests on, and that must surface here rather than in a report.
        """
        if prop.scope is not expected_scope:
            raise ValueError(
                "property {0!r} has scope {1} but was evaluated in the {2} "
                "pipeline".format(
                    prop.property_id, prop.scope.value, expected_scope.value
                )
            )
        try:
            result = prop.evaluate(subject, self.cfg, context)
        except Exception as exc:  # re-raised with the missing context attached
            raise RuntimeError(
                "property {0!r} raised while checking {1!r}: {2}".format(
                    prop.property_id, context.get("participant_id", "<all>"), exc
                )
            ) from exc

        if not isinstance(result, PropertyResult):
            raise TypeError(
                "property {0!r} returned {1}, expected a PropertyResult".format(
                    prop.property_id, type(result).__name__
                )
            )
        if result.property_id != prop.property_id:
            raise ValueError(
                "property {0!r} returned a result labelled {1!r}".format(
                    prop.property_id, result.property_id
                )
            )
        if result.scope is not expected_scope:
            raise ValueError(
                "property {0!r} returned scope {1}, expected {2}".format(
                    prop.property_id, result.scope.value, expected_scope.value
                )
            )
        if not result.parameters:
            raise ValueError(
                "property {0!r} returned no parameters; a verdict must record the "
                "thresholds that produced it".format(prop.property_id)
            )
        if result.status is CheckStatus.FAIL and not result.violating_intervals:
            raise ValueError(
                "property {0!r} reported FAIL without a violating interval".format(
                    prop.property_id
                )
            )
        return result
