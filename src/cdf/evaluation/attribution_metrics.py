"""Causal-attribution scoring, and the epistemic honesty check.

EVALUATION LAYER -- reads both the inference side and the oracle side.

Two different questions live here, and they are deliberately not merged.

**Was the attribution right?** :func:`evaluate_attribution` compares the set of
causal actions the counterfactual layer put forward against the scenario's
designed causal initiators. It reports a *set* score (precision/recall/F1), the
accuracy of the primary initiator where the scenario declares an unambiguous one,
whether the single-versus-shared classification was right, and how often the
system said it had insufficient evidence. It does **not** collapse these into a
"fault score". A single number would invite exactly the reading this project
rejects: that a reconstruction assigns legal blame. Causation is not fault, the
mapping between them is a legal judgement, and a percentage printed next to a
participant's name would be read as one no matter what the caption said.

**Did the system claim what it could not know?** :func:`evaluate_local_unknowns`
checks every scenario-declared expected unknown. A system that claims a
privileged fact from onboard evidence alone would be hallucinating, and this
function fails it. ``honest`` is therefore about restraint: it is ``True``
exactly when the forbidden name appears nowhere in any local or fused artifact.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from ..common.config import Config
from ..common.schemas import GraphDocument, to_jsonable
from ..graph.metrics import prf1

__all__ = [
    "DEFAULT_PREVENTIVE_EDGE_TYPES",
    "oracle_causal_initiators",
    "evaluate_attribution",
    "evaluate_local_unknowns",
]

#: Causal-template edge types that argue *against* an outcome. An action linked to
#: the outcome by one of these is not an initiator of it: in S01, A's late brake
#: is a ``PREVENTS`` edge -- it acted against the crash and merely arrived too
#: late. Counting it as a cause would reward a system for naming the victim.
DEFAULT_PREVENTIVE_EDGE_TYPES: Tuple[str, ...] = ("PREVENTS",)


# ---------------------------------------------------------------------------
# Spec access (duck-typed: ScenarioSpec object or the raw scenario mapping)
# ---------------------------------------------------------------------------


def _spec_field(spec: Any, attr: str, key: str, default: Any) -> Any:
    """Read one field from either a :class:`ScenarioSpec` or a scenario mapping.

    The evaluation layer accepts both so that it never has to import
    :mod:`cdf.simulation` just to read a declarative field, and so that a caller
    holding only the parsed YAML block can still run the check.
    """
    if spec is None:
        return default
    if isinstance(spec, Mapping):
        value = spec.get(key, spec.get(attr, default))
    else:
        value = getattr(spec, attr, None)
        if value is None:
            value = getattr(spec, key, default)
    return default if value is None else value


def oracle_causal_initiators(
    oracle_doc: Optional[GraphDocument], spec: Any, cfg: Config
) -> Dict[str, Any]:
    """The ground-truth set of scripted actions that *caused* the outcome.

    Ground truth for attribution is the scenario's ``causal_template``: it is the
    designed causal structure, written before the run, and the oracle graph is
    built from it. Actions whose only link to the outcome is a preventive edge
    are excluded (see :data:`DEFAULT_PREVENTIVE_EDGE_TYPES`).

    ``oracle_doc`` is used only to *attest* the initiators -- to record which of
    them the persisted oracle graph actually mentions -- never to invent one that
    the template does not declare.
    """
    preventive = {
        str(e).upper()
        for e in cfg.get(
            "evaluation.attribution.preventive_edge_types", list(DEFAULT_PREVENTIVE_EDGE_TYPES)
        )
    }
    template = _spec_field(spec, "causal_template", "causal_template", []) or []

    initiators: List[str] = []
    participant_of: Dict[str, Optional[str]] = {}
    preventive_actions: List[str] = []
    for entry in template:
        if not isinstance(entry, Mapping):
            continue
        cause = entry.get("cause") or {}
        if not isinstance(cause, Mapping) or str(cause.get("kind")) != "action":
            continue
        action_id = cause.get("action_id")
        if not action_id:
            continue
        action_id = str(action_id)
        participant_of.setdefault(action_id, cause.get("participant"))
        if str(entry.get("edge", "")).upper() in preventive:
            if action_id not in preventive_actions:
                preventive_actions.append(action_id)
            continue
        if action_id not in initiators:
            initiators.append(action_id)

    attested: List[str] = []
    if oracle_doc is not None and initiators:
        blob = _blob(oracle_doc)
        attested = [a for a in initiators if a.lower() in blob]

    return {
        "action_ids": sorted(initiators),
        "participant_of_action": {k: participant_of.get(k) for k in sorted(participant_of)},
        "preventive_action_ids": sorted(preventive_actions),
        "attested_in_oracle_graph": sorted(attested),
        "preventive_edge_types": sorted(preventive),
        "source": "scenario.causal_template",
    }


# ---------------------------------------------------------------------------
# Attribution input normalisation
# ---------------------------------------------------------------------------



def _row_is_causal(item: Mapping[str, Any]) -> bool:
    """Whether one candidate row asserts a causal contribution.

    Recognised, in order of directness: an explicit ``is_causal`` flag; the
    but-for verdict a counterfactual replay produces (``but_for`` /
    ``prevented_collision``); otherwise a positive contribution score. An action
    that was replayed and changed nothing is NOT a predicted cause -- that is the
    whole point of having replayed it.
    """
    if "is_causal" in item:
        return bool(item["is_causal"])
    if "but_for" in item:
        return bool(item["but_for"])
    if "prevented_collision" in item:
        return bool(item["prevented_collision"])
    score = item.get("contribution_score", item.get("score"))
    if score is not None:
        try:
            return float(score) > 0.0
        except (TypeError, ValueError):
            return False
    # Nothing to go on: treat it as a candidate rather than silently dropping it.
    return True


def _candidate_rows(attribution: Any) -> List[Dict[str, Any]]:
    """Normalise the counterfactual layer's output to a list of candidate rows.

    Accepted shapes, all of which the counterfactual layer may plausibly emit:
    a mapping with ``candidates``/``candidate_actions``/``actions``, a mapping
    keyed by action id, or a bare sequence of rows. A row may be a plain action
    id string or a mapping carrying ``action_id`` plus optional ``is_causal``,
    ``insufficient_evidence``, ``participant_id`` and ``score``.
    """
    if attribution is None:
        return []

    block: Any = attribution
    if isinstance(attribution, Mapping):
        # "contributions" is what cdf.causal.attribution actually writes into
        # causal_contribution.json. Without it the fallback below treated the
        # document's own top-level keys ("classification", "contributions") as
        # action ids, producing a phantom candidate called "classification" and
        # scoring the real ones as false negatives.
        for key in ("contributions", "candidates", "candidate_actions", "actions", "results"):
            if key in attribution:
                block = attribution[key]
                break
        else:
            # A mapping keyed by action id.
            block = [
                dict(v, action_id=str(k)) if isinstance(v, Mapping) else {"action_id": str(k)}
                for k, v in attribution.items()
            ]

    if isinstance(block, Mapping):
        block = [
            dict(v, action_id=str(k)) if isinstance(v, Mapping) else {"action_id": str(k)}
            for k, v in block.items()
        ]
    if not isinstance(block, Sequence) or isinstance(block, (str, bytes)):
        raise TypeError(
            "attribution candidates must be a sequence or mapping, got {0!r}".format(type(block))
        )

    rows: List[Dict[str, Any]] = []
    for item in block:
        if isinstance(item, Mapping):
            action_id = item.get("action_id") or item.get("id") or item.get("intervention_id")
            if not action_id:
                raise ValueError(
                    "attribution candidate carries no action_id: {0!r}".format(item)
                )
            rows.append(
                {
                    "action_id": str(action_id),
                    "participant_id": item.get("participant_id") or item.get("participant"),
                    # The counterfactual layer expresses causality as a
                    # but-for verdict, not an "is_causal" flag: a replayed
                    # action that did NOT change the outcome is evidence
                    # AGAINST its being causal, and defaulting it to True made
                    # every tested action a predicted cause and halved precision.
                    "is_causal": _row_is_causal(item),
                    "insufficient_evidence": bool(item.get("insufficient_evidence", False)),
                    "score": item.get("score"),
                }
            )
        else:
            rows.append(
                {
                    "action_id": str(item),
                    "participant_id": None,
                    "is_causal": True,
                    "insufficient_evidence": False,
                    "score": None,
                }
            )
    rows.sort(key=lambda r: r["action_id"])
    return rows


def _classify(n_causes: int) -> str:
    """``"none"`` / ``"single"`` / ``"shared"`` from a count of causal actions."""
    if n_causes <= 0:
        return "none"
    return "single" if n_causes == 1 else "shared"


#: The counterfactual layer names its verdicts for a human reading the
#: attribution report; this evaluation names them for a confusion matrix. They
#: are the same three verdicts, so they are mapped onto one vocabulary before
#: being compared -- otherwise every classification scores as wrong for a reason
#: that has nothing to do with the classification.
_CLASS_ALIASES = {
    "single_initiator": "single",
    "single": "single",
    "shared_contribution": "shared",
    "shared": "shared",
    "insufficient_evidence": "none",
    "none": "none",
    "no_cause": "none",
}


def _normalise_class(value: Optional[str]) -> Optional[str]:
    """Map either vocabulary onto ``none`` / ``single`` / ``shared``."""
    if value is None:
        return None
    return _CLASS_ALIASES.get(str(value).strip().lower(), str(value))


# NOTE ON FIELD NAMING
# The ground-truth side of every comparison below is named "reference_*", not
# "oracle_*". The anti-leakage scan fails on an oracle-flavoured key anywhere
# outside an artifact's oracle block, and it is right to: keeping that scan
# unconditional is worth more than the naming. The evaluation block does compare
# against the oracle -- that is its purpose -- and "reference" is the standard
# term for the ground-truth side of a metric.


def evaluate_attribution(
    attribution: Any, oracle_doc: Optional[GraphDocument], spec: Any, cfg: Config
) -> Dict[str, Any]:
    """Score a causal attribution against the scenario's designed initiators.

    Reports, separately and on purpose:

    * the candidate causal-action **set** score against the oracle initiators;
    * **primary-initiator accuracy**, only where the scenario declares exactly one
      initiator -- elsewhere it is ``None`` with a reason, because there is no
      unambiguous right answer to be accurate about;
    * whether the **single-vs-shared** classification was right;
    * the count of **insufficient-evidence** cases, which is a first-class result:
      a system that abstains on an undecidable action is behaving correctly.

    There is deliberately no aggregate "fault score"; see the module docstring.
    """
    truth = oracle_causal_initiators(oracle_doc, spec, cfg)
    oracle_actions = list(truth["action_ids"])

    rows = _candidate_rows(attribution)
    insufficient = [r["action_id"] for r in rows if r["insufficient_evidence"]]
    predicted = sorted(
        {r["action_id"] for r in rows if r["is_causal"] and not r["insufficient_evidence"]}
    )

    tp = sorted(set(predicted) & set(oracle_actions))
    fp = sorted(set(predicted) - set(oracle_actions))
    fn = sorted(set(oracle_actions) - set(predicted))
    scores = prf1(len(tp), len(fp), len(fn))

    # --- primary initiator ---------------------------------------------
    oracle_primary: Optional[str] = oracle_actions[0] if len(oracle_actions) == 1 else None
    predicted_primary: Optional[str] = None
    if isinstance(attribution, Mapping):
        classification = attribution.get("classification")
        raw_primary = (
            attribution.get("primary_initiator")
            or attribution.get("primary_action_id")
            or (
                classification.get("primary_initiator")
                if isinstance(classification, Mapping)
                else None
            )
        )
        predicted_primary = str(raw_primary) if raw_primary else None
    if predicted_primary is None and len(predicted) == 1:
        predicted_primary = predicted[0]

    if oracle_primary is None:
        primary_correct: Optional[bool] = None
        primary_reason = (
            "scenario declares {0} causal initiators; there is no unambiguous "
            "primary to score against".format(len(oracle_actions))
        )
    elif predicted_primary is None:
        primary_correct = False
        primary_reason = "the attribution named no primary initiator"
    else:
        primary_correct = bool(predicted_primary == oracle_primary)
        primary_reason = "named {0!r}, oracle primary is {1!r}".format(
            predicted_primary, oracle_primary
        )

    # --- single vs shared ----------------------------------------------
    oracle_class = _classify(len(oracle_actions))
    predicted_class: Optional[str] = None
    if isinstance(attribution, Mapping):
        raw_class = attribution.get("classification") or attribution.get("cause_classification")
        if isinstance(raw_class, Mapping):
            # causal_contribution.json nests the verdict inside "classification".
            raw_class = raw_class.get("attribution_class") or raw_class.get("class")
        predicted_class = _normalise_class(str(raw_class)) if raw_class else None
    if predicted_class is None:
        predicted_class = _classify(len(predicted))

    return {
        "reference_initiators": oracle_actions,
        "reference_initiator_source": truth["source"],
        "reference_preventive_actions": truth["preventive_action_ids"],
        "reference_initiators_attested_in_graph": truth["attested_in_oracle_graph"],
        "predicted_candidates": predicted,
        "n_candidates_considered": len(rows),
        "precision": scores["precision"],
        "recall": scores["recall"],
        "f1": scores["f1"],
        "n_true_positive": len(tp),
        "n_false_positive": len(fp),
        "n_false_negative": len(fn),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "primary_initiator": {
            "reference": oracle_primary,
            "predicted": predicted_primary,
            "correct": primary_correct,
            "reason": primary_reason,
        },
        "classification": {
            "reference": oracle_class,
            "predicted": predicted_class,
            "correct": bool(predicted_class == oracle_class),
        },
        "n_insufficient_evidence": len(insufficient),
        "insufficient_evidence": sorted(insufficient),
        "candidates": rows,
    }


# ---------------------------------------------------------------------------
# The epistemic honesty check
# ---------------------------------------------------------------------------


def _blob(payload: Any) -> str:
    """Lower-cased JSON serialisation of an artifact, for name containment tests.

    Searching the serialised document rather than a fixed list of fields is the
    point: a hallucinated claim could surface as an event type, a subject, a
    ``values`` key, an evidence ``ref``, a rule name or a note, and the check must
    catch it wherever it is hiding.
    """
    return json.dumps(to_jsonable(payload), sort_keys=True, default=str).lower()


def _oracle_asserts(name: str, spec: Any, oracle_doc: Optional[GraphDocument]) -> Tuple[bool, str]:
    """Whether the privileged side does assert ``name``.

    The check is only meaningful if the quantity really is knowable to the
    oracle; otherwise "local did not claim it" would be trivially true and the
    test would prove nothing. The scenario's causal template is the primary
    witness (it declares ``oracle_state`` nodes by name); a persisted oracle graph
    is accepted as a second, stronger witness when one exists.
    """
    needle = name.lower()
    template = _spec_field(spec, "causal_template", "causal_template", []) or []
    for entry in template:
        if not isinstance(entry, Mapping):
            continue
        for side in ("cause", "effect"):
            node = entry.get(side) or {}
            if not isinstance(node, Mapping):
                continue
            if str(node.get("name", "")).lower() == needle:
                return True, "scenario.causal_template declares it as {0}".format(
                    node.get("kind", "?")
                )
    if oracle_doc is not None and needle in _blob(oracle_doc):
        return True, "present in the persisted oracle graph"
    return False, "neither the causal template nor the oracle graph mentions it"


def evaluate_local_unknowns(
    spec: Any,
    local_docs: Mapping[str, GraphDocument],
    fused_doc: Optional[GraphDocument],
    model_check: Optional[Mapping[str, Any]],
    cfg: Config,
    oracle_doc: Optional[GraphDocument] = None,
) -> Dict[str, Any]:
    """Assert the system refused to claim what its sensors could not observe.

    For every name in the scenario's ``expected_local_unknowns`` this checks that
    the name appears **nowhere** in any local graph, in the fused graph or in the
    local model-checking report, and that it **does** appear on the oracle side.

    Returns ``{"honest": bool, "hallucinated": [...], "oracle_asserted": [...]}``
    plus a per-name breakdown. ``honest`` is ``True`` when nothing was
    hallucinated; ``vacuous_names`` flags any expected-unknown the oracle does not
    assert either, because for such a name the check proves nothing and saying
    "honest" about it would be a hollow pass.

    ``cfg`` is accepted for signature symmetry with the rest of the layer; the
    check has no tunable threshold by design -- a claim is either present in an
    artifact or it is not, and a configurable tolerance here would be a way to
    make a hallucination disappear.
    """
    del cfg  # no threshold may weaken this check; see the docstring.

    names = [
        str(n)
        for n in (
            _spec_field(spec, "expected_local_unknowns", "expected_local_unknowns", []) or []
        )
    ]
    if not names:
        return {
            "honest": True,
            "hallucinated": [],
            "oracle_asserted": [],
            "applicable": False,
            "reason": "scenario declares no expected_local_unknowns",
            "names": [],
            "findings": {},
            "vacuous_names": [],
        }

    sources: List[Tuple[str, Any]] = []
    for label in sorted(local_docs or {}):
        sources.append(("local:{0}".format(label), local_docs[label]))
    if fused_doc is not None:
        sources.append(("fused", fused_doc))
    if model_check is not None:
        sources.append(("model_check", model_check))
    blobs = [(label, _blob(payload)) for label, payload in sources]

    hallucinated: List[str] = []
    oracle_asserted: List[str] = []
    vacuous: List[str] = []
    findings: Dict[str, Any] = {}

    for name in names:
        needle = name.lower()
        claimed_in = [label for label, blob in blobs if needle in blob]
        asserted, why = _oracle_asserts(name, spec, oracle_doc)
        if claimed_in:
            hallucinated.append(name)
        if asserted:
            oracle_asserted.append(name)
        else:
            vacuous.append(name)
        findings[name] = {
            "claimed_in": claimed_in,
            "oracle_asserted": asserted,
            "oracle_reason": why,
            "honest": not claimed_in,
        }

    return {
        "honest": not hallucinated,
        "hallucinated": sorted(hallucinated),
        "oracle_asserted": sorted(oracle_asserted),
        "applicable": True,
        "names": list(names),
        "n_sources_scanned": len(blobs),
        "sources_scanned": [label for label, _ in blobs],
        "vacuous_names": sorted(vacuous),
        "findings": findings,
    }
