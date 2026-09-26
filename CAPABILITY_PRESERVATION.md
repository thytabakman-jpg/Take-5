# Capability Preservation

A capability is not preserved merely because its name, documentation, or source code remains.

For operational capability c:

Pres(c)
=
Identity
and Semantics
and Reachability
and Selection
and Execution
and Effect
and Consumer
and RecoveryWitness.

Identity
The object and lineage are recoverable.

Semantics
Its job, inputs, outputs, failures, and protected distinctions are recoverable.

Reachability
The normal system can still reach it.

Selection
There is a state-relative basis for selecting it.

Execution
A real binding exists.

Effect
Its result has typed admission/state semantics.

Consumer
Something consumes, propagates, or reenters from its result.

RecoveryWitness
A future system can prove how to reconstruct the chain.

For every protected predecessor capability, a successor must provide one of:

PRESERVED with witness
STRICT_GAIN replacement with reconstruction witness
authorized SUPERSEDED
OPEN with missing coordinates exposed.

Silent disappearance is regression.
