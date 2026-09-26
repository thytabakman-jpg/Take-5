# Capability Preservation Invariant 097

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / FAIL-CLOSED

## Problem

The system has repeatedly rediscovered valuable behavior because capability presence was
confused with capability preservation.

A capability can remain:

- named in a Markdown file;
- present in a historical registry;
- implemented in code;
- described by a current assistant reply;

and still be functionally lost when the normal controller can no longer recover, select,
execute, consume, or reenter through it.

That is the lost-capabilities defect.

## Preservation predicate

For an operational capability c define

Pres(c)
=
I(c)
and S(c)
and R(c)
and Q(c)
and X(c)
and E(c)
and C(c)
and V(c).

Coordinates:

I identity and lineage are recoverable.

S semantic job/input/output/failure contract is recoverable.

R the capability is reachable from the normal operating system.

Q the state-relative selection or routing basis is recoverable.

X a real execution binding exists.

E its result has typed effect/admission semantics.

C a consumer, propagation, or reentry path exists.

V a recovery/verification witness proves the chain can be reconstructed.

A name, file, registry row, or implementation alone satisfies none of the conjunction by itself.

## Semantic-only objects

A genuinely non-operational semantic object may waive X only when non-operational status is
explicitly typed. Unknown execution status remains OPEN.

## Successor rule

For every protected capability c in predecessor S and successor S':

Pres_S(c)
implies one of:

1. Pres_S'(c) with witness;
2. STRICT_GAIN replacement with reconstruction witness;
3. explicitly authorized SUPERSEDED;
4. OPEN with the missing preservation coordinate exposed.

Silent disappearance is regression.

## Runtime

runtime/capability_preservation.py

Regression:

tests/test_capability_preservation.py

## Consequence

The Functionality Recovery Ledger remains the high-recall candidate universe.

This invariant supplies the missing stronger question:

not merely "did we remember the capability?"

but

"can the present system still reconstruct and operationally use it?"

## Placement

This is a kernel-level preservation constraint because every controller, tool registry,
migration, compression, and successor architecture can otherwise erase capability behavior.

It does not dictate which capability must be selected on a given job.

## Closure

Global capability completeness remains OPEN.

Finite preservation relative to a declared capability corpus is testable.
New recovered capabilities reopen the affected preservation set.
