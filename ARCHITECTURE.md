# Architecture

## Semantic primitives

The kernel uses five durable primitives.

Object
A stable identified thing with type, state, authority, and evidence references.

Relation
A typed claim between objects with provenance and authority.

Event
An immutable record that something material occurred.

Transition
The ordinary path for consequential state change. A transition binds baseline, target,
authority, evidence, protected behavior, validators, and outcome.

Observation
Structured evidence about what was seen or executed.

## Controller

Let J be the protected job, K the admissibility/authority basis, Z semantic controller
state, M learning memory, D typed terminal dispositions, and A+ admissible actions.

The current transferable controller abstraction is:

C+_(J,K) = <Z x M, D, A+_(J,K), pi+_(J,K), T+_(J,K), Tau+_(J,K)>.

The policy is recomputed after admitted material state change.

Recursive child-controller work is one typed action family inside A+.
A child return never becomes authoritative until the parent admits/reconciles it.

Learning memory blocks unchanged NO_GAIN / REJECTED / FAILED routes relative to the basis
that produced them. Relevant dependency change can reopen them.

## Inquiry before capability selection

Question/discriminator generation and work generation occur before capability selection.

A capability is treated as a probe over live distinctions, not as a name that defines the
problem.

## Supervisor

The Supervisor carries continuity:

target
job
basis/currentness
protected behavior
OPEN coordinates
capability gaps
evidence/recovery references.

Missing continuity coordinates remain OPEN.

The Supervisor does not own the controller's substantive action choice.

## Reality closure

Semantic intent
-> bound action
-> execution
-> observation
-> evidence
-> admission
-> persistence
-> semantic/state update
-> consumer/reentry.

These states are not interchangeable.

## Sparse architecture

A new durable subsystem is admitted only after a view/composition fails to preserve a
result-sensitive requirement.

This is the Take-Two discipline retained in the stronger system.
