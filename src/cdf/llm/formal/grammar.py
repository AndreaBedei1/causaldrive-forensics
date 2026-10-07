"""The restricted temporal logic in which an LLM formalises its own claims.

A small bounded fragment of MTL/STL over the reconstructed semantic trace,
deliberately not a general theorem prover:

* propositional: AND, OR, NOT;
* bounded temporal: F[a,b] (EVENTUALLY) and G[a,b] (ALWAYS), with bounds in
  seconds relative to the evaluation instant, possibly negative or infinite;
* ordering: BEFORE(p, q), sugar for ``F[-inf,inf](p AND F(0,inf] q)``;
* predicates: ``event(TYPE, actor[, subject])`` and
  ``state(STATE, actor[, subject])`` over the vocabulary.

Formulas are evaluated once, at t_global = 0 (the time-origin collision), on a
finite trace sampled every ``time_step_s``; the values are three-valued
(Kleene): TRUE, FALSE, UNKNOWN.
"""

from __future__ import annotations

OPS = ("AND", "OR", "NOT", "EVENTUALLY", "ALWAYS", "BEFORE", "EVENT", "STATE")
UNARY_TEMPORAL = {"F": "EVENTUALLY", "EVENTUALLY": "EVENTUALLY", "G": "ALWAYS", "ALWAYS": "ALWAYS"}
KEYWORDS = ("AND", "OR", "NOT", "F", "G", "EVENTUALLY", "ALWAYS", "BEFORE", "event", "state")

GRAMMAR_VERSION = "cdf.formal/1"

GRAMMAR_TEXT = """\
formula  := disj
disj     := conj { "OR" conj }
conj     := unary { "AND" unary }
unary    := "NOT" unary
          | "F" "[" bound "," bound "]" unary          eventually: true at t if the operand is true at some
                                                        instant in [t+a, t+b]
          | "G" "[" bound "," bound "]" unary          always: true at t if the operand is true at every
                                                        instant in [t+a, t+b]
          | "BEFORE" "(" formula "," formula ")"       some instant where the first operand is true lies
                                                        strictly before some instant where the second is true
                                                        (anywhere in the recording)
          | "(" formula ")"
          | atom
atom     := "event" "(" EVENT_TYPE "," ACTOR [ "," SUBJECT ] ")"
          | "state" "(" STATE "," ACTOR [ "," SUBJECT ] ")"
bound    := number | "-inf" | "inf"                    seconds; a <= b

Meaning:
- Time is t_global in seconds.  A formula is evaluated once, at t = 0 (the time-origin collision), so
  bounds are offsets from that instant: F[-3,0] event(...) = "within the 3 s before the collision".
- event(TYPE, ACTOR, SUBJECT) is true at the instants where recorder ACTOR reports an event of TYPE about
  SUBJECT (SUBJECT omitted for event types without a subject; for COLLISION, ACTOR and SUBJECT are the two
  parties in either order).
- state(STATE, ACTOR, SUBJECT) is true while that state is active: opened by its START (or ENTRY) event and
  closed by its END (or EXIT) event.
- ACTOR must be a recorder id; SUBJECT an entity id of the packet (a recorder id, a track id such as
  A:track_001, or a sign id such as A:sign-0).
- Values are three-valued: TRUE, FALSE or UNKNOWN.  UNKNOWN when the recordings cannot decide (the subject
  was not observed then, the state was not established, the identity is not available, the instant lies
  outside the recorded interval).  Infinite bounds are limited to the recorded interval.
- Shape of a formula (placeholders in angle brackets):
  F[-5,0] (event(<EVENT_TYPE>, <ACTOR>, <SUBJECT>) AND F[0,2] state(<STATE>, <ACTOR>))

formula_ast is the same formula as a table of nodes {id, op, children, lo, hi, event_type, state,
actor_id, subject_id} with op one of AND, OR, NOT, EVENTUALLY, ALWAYS, BEFORE, EVENT, STATE:
- AND / OR: two or more children; NOT: one child; EVENTUALLY / ALWAYS: one child and the bounds lo / hi
  (null for -inf / +inf); BEFORE: two children (first, then second);
- EVENT: event_type, actor_id, subject_id (null when absent), no children;
- STATE: state, actor_id, subject_id (null when absent), no children;
- unused fields are null; root is the id of the top node; every other node is the child of exactly one node.
"""
