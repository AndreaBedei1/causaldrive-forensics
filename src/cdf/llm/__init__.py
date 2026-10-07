"""LLM abductive forensics on admissible facts, verified against the semantic trace.

Three bodies of information are kept apart:

* admissible facts (``facts``): measured ego motion and controls, radar tracks
  (identified only where the reconstruction associated them), sign detections,
  collision reports, the supplied context.  This is the only thing a model sees;
* the reconstructed semantic trace (events and perceived states): read only by
  the deterministic verifier (``formal.verifier``), after the model's answers
  are saved; never sent to a model and never changed by this package;
* privileged simulator ground truth: never read here except by ``oracle``
  (evaluation infrastructure, ``--oracle-identities``).
"""
