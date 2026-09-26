# Mathematical Color Invariant 062

Date: 2026-09-25
Status: CURRENT CANDIDATE EMISSION CONTRACT

## Job

Control user-visible coloring of mathematical and formal-system objects relative to the current job.

Color is not a property of a name.
Color is a verdict on whether the object's mathematical role is sufficiently recovered for the current job.

## Core law

For formal object x under current job J:

GREEN_J(x)
iff
Required_J(x) is nonempty
AND
every coordinate required by J is recovered, nonconflicting, and admitted
AND
no unresolved coordinate can change the job-relevant result.

Otherwise:

RED_J(x).

Equivalently:

Color_J(x) =
GREEN when SufficientlyRecovered_J(x)
RED otherwise.

## Conservative rule

The default is RED.

A name, implementation, partial role, historical meaning, local test pass, or candidate contract does not by itself license GREEN.

## Red conditions

RED is mandatory when any job-required coordinate is:

MISSING
PARTIAL
AMBIGUOUS
CONFLICT
OPEN
BLOCKED
ONLY_NAMED
CANDIDATE_ONLY
IMPLEMENTED_BUT_NOT_SEMANTICALLY_COMPLETE
SEMANTICALLY_DEFINED_BUT_NOT_BOUND_WHEN_BINDING_IS_REQUIRED
UNVERIFIED_WHEN_VERIFICATION_IS_REQUIRED.

## Green conditions

GREEN requires evidence sufficient for the current claim.

A narrower claim can be green even when the larger object remains red.

Example:

"The runtime contains hf1_reentry_route" may be GREEN when directly verified.

"HF1 is mathematically complete" remains RED while the complete HF1 state space, transition semantics, minimality, or sufficiency remain open.

## Dependency inheritance

If a visible formal expression y depends on unresolved formal object x for its job-relevant semantics, then y is RED for that job unless y has an independently complete semantics.

Thus an unresolved HF1 can force REENTER_OBSERVE, REVERIFY, and NO_REENTRY red when their exact meanings are being asserted as parts of HF1.

## Claim-relative coloring

The same glyph can legitimately have different colors in different claims.

GREEN means sufficient for the claim currently being made, not globally complete.

## Emission gate

Before emitting a formal object:

1. identify the current job J;
2. identify the claim being made about x;
3. enumerate claim-required coordinates;
4. inspect their status;
5. emit GREEN only if all are sufficient;
6. otherwise emit RED.

No optimistic promotion from PARTIAL to GREEN.

## HF1 witness

Current job: determine the complete mathematics of HF1.

Known:
- a runtime function named hf1_reentry_route exists;
- a candidate three-input routing rule exists;
- existing CI passes for the commit containing that function.

Open:
- exact complete HF1 state vector;
- exact semantics and construction of discovery delta;
- exact result-sensitivity predicate;
- proof that the current coordinates are necessary and sufficient;
- full wrapper integration.

Therefore:
HF1 = RED for the complete-mathematics job.

Any branch labels whose exact semantics depend on the unresolved HF1 specification are also RED for that job.

## Relationship to wrapper

This contract supplies a candidate resolution for Wrapper Canonical Contract 053 open coordinate O6, human-visible-math formalization.

O6 remains not fully promoted until integration with the emission path and regression evidence are established.
