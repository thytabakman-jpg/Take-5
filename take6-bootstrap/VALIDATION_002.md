# Take-6 Bootstrap Validation 002

Date: 2026-09-27
Status: VALIDATED CANDIDATE / PRODUCTION PROMOTION OPEN
PR: #145

## Change under test

This validation adds the first executable generated-view layer for the Take-6
bootstrap.

A human/current view is now a deterministic projection of one exact compiled
semantic state. It is explicitly marked PROJECTION_ONLY and carries its source
state CID and view CID.

Authoritative formal CURRENT/CANONICAL/EXACT_CURRENT projections additionally
require:
- a compiled CURRENT root;
- exact current dependency payloads;
- explicit admission for frozen historical dependencies;
- dependency closure PASS;
- composition type-check PASS.

## New invariants

1. generated views bind exact state/compiler/authority-policy identities;
2. rebuilding the same semantic state reproduces a view that remains valid;
3. a later semantic supersession makes the old view stale;
4. hand editing a generated view breaks its receipt hash;
5. authoritative formal views cannot bypass dependency closure;
6. authoritative formal views cannot bypass composition type checking;
7. CURRENT dependencies must match the compiled current payload;
8. frozen historical dependencies require current authority-policy admission;
9. a conflicted/non-current root cannot emit an authoritative CURRENT claim;
10. human rendering identifies itself as GENERATED_PROJECTION_ONLY and exposes
    state/view receipt identities.

## Validation binding

A dedicated workflow now protects the bootstrap:

.github/workflows/take6-bootstrap-validation.yml

It triggers on Take-6 bootstrap changes and runs the isolated bootstrap suite.

This closes the earlier validation-path gap where Take-6 files were outside the
ordinary Take-5 pytest path.

## Evidence

Implementation head:
e49a8c5930aa740310168040357fd9daa7ccdff5

Take-6 Bootstrap Validation:
36293558118
SUCCESS
24 passed in 0.07s.

Capability Preservation:
36293558127
SUCCESS.

Take-5 Validation:
36293558098
SUCCESS.

## Disposition

Generated-view/runtime invariant:
CLOSED_RELATIVE.

Take-6 production promotion:
OPEN.

Take-5 remains current runtime authority.
