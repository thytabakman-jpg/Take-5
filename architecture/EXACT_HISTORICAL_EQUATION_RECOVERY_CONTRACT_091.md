# Exact Historical Equation Recovery Contract 091

Date: 2026-09-27
Status: IMPLEMENTED REGRESSION GUARD

## Governing distinction

[
ExactRecovery 
eq DerivedReconstruction 
eq PlausibleMatch.
]

A candidate cannot certify its own historical identity.

For candidate (c), external recovery receipt (r), and durable recovery memory (M):

[
ExactRecovered(c,r,M)
iff
ExactCopy(c)
land
SourceBacked(r)
land
ExactExpressionMatch(r,c)
land
IdentityMatch(r,c)
land
Evidence(r)
eqarnothing
land

eg Rejected_M(c).
]

Explicit rejection is durable:

[
Rejected_M(c)land
eg Reopened_M(c)
Rightarrow
Disposition(c)=REJECTED.
]

A derived or synthesized equation receives:

[
Disposition(c)=DERIVED_RECONSTRUCTION,
]

never EXACT_RECOVERY.

## HF1 consequence

When a candidate is rejected or exact source identity is unresolved, the recovery episode remains nonterminal and returns to observation/source recovery rather than emitting another exact-recovery claim.

## Implementation

- runtime/exact_equation_recovery.py
- tests/test_exact_equation_recovery.py

## Protected behavior

1. rejected candidates cannot silently reenter;
2. candidate self-certification is impossible;
3. exact recovery requires an external source receipt;
4. derived reconstruction remains explicitly typed;
5. missing provenance fails OPEN;
6. receipt identity mismatch fails CONFLICT.

## Scope boundary

This guard governs Take-5 recovery admission. An unrelated external host that bypasses Take-5 remains outside repository enforcement.
