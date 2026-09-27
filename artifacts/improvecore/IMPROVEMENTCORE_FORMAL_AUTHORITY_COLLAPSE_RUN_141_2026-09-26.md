# ImprovementCore Formal Authority Collapse Run 141

Date: 2026-09-26
Status: IMPLEMENTATION VALIDATED / PROMOTION PENDING
Controller: ImprovementCore
PR: #143

## Governing problem

Two recent conversations exposed one deeper failure family.

One conversation showed that a named device can be reconstructed or improved
before its exact current identity is recovered.

The second showed that a reconstruction can mix current and historical
mathematics, or combine locally recovered operands with an invalid composition,
and still be presented as current/green mathematics.

The root defect is not one bad equation.

It is:

FORMAL_AUTHORITY_COLLAPSE.

The invalid move is:

recovered/reconstructed
-> treated as authoritative current mathematics

without a separate proof of current identity, version, authority, dependency
admission, and type-correct composition.

## Existing protection that was insufficient

Specification-Before-Transformation correctly blocks transforming an
unrecovered object.

It intentionally permits RECOVER, RECONSTRUCT, FORMALIZE, COMPARE, AUDIT, and
VERIFY on OPEN objects.

Therefore it cannot by itself prevent a legal reconstruction from later being
mis-promoted to CURRENT/CANONICAL/EXACT_CURRENT mathematics.

The Mathematical Color Invariant also assesses coordinate recovery, but before
this repair it did not require a distinct currentness/authority/composition
receipt for authoritative claims.

## Repair

Added:

runtime/formal_claim_admission.py

The formal claim packet binds:
- exact object identity;
- exact version;
- basis;
- authority;
- claim scope;
- required/recovered coordinates;
- source references;
- dependency dispositions;
- explicit frozen-dependency admission;
- dependency closure;
- composition type check;
- authority consistency;
- source consistency.

For authoritative scopes:

CURRENT
CANONICAL
EXACT_CURRENT
CURRENT_FULL

GREEN/current emission requires:

FormalClaimAdmission = PASS.

Historical mathematics can still be green when explicitly claimed as
HISTORICAL.

A current object can use a historical frozen dependency only when the current
root authority explicitly admits it as ADMITTED_FROZEN.

## ImprovementCore closure

Formal-system math/equation output jobs now carry
formal_claim_receipt_required into the shared parent-return gate.

COMPLETE is illegal when:
- the output job requires a formal claim receipt and none exists; or
- a formal claim receipt exists but is not PASS.

A canonical producer:

admit_formal_claim_to_state(...)

normalizes the receipt into the controller state.

The rule is bound into both:
- ordinary ImprovementCore;
- Legacy-restored ImprovementCore.

## Direct emission closure

A second reentry discovered that direct formal output could bypass the
ImprovementCore parent-return path.

The shared mathematical emission API now also blocks authoritative green
mathematics without a PASS formal-claim receipt.

Thus the repair is not dependent on one controller route.

## CI-derived corrections

First CI attack exposed an import-indentation defect in the Legacy-restored path.
It was repaired.

Second CI attack exposed an over-broad request detector. A job merely referring
to a Show-Me-the-Math artifact as evidence was incorrectly treated as a request
to emit authoritative mathematics.

The detector was corrected to distinguish:

math/equation output requested by the user

from:

math/equation material merely present in target/job/evidence context.

A dedicated regression now preserves that distinction.

## Validated implementation head

c45817e28ab3130402d430acfc3878e13d26d94f

Validation:
- Take-5 Validation 36292992625: SUCCESS
- Capability Preservation 36292992598: SUCCESS
- ImproveCore Legacy Restoration 130 run 36292992599: SUCCESS
- ImproveCore Legacy Semantic Holdouts 132 run 36292992595: SUCCESS

## Take-6 consequence

The Take-6 successor architecture now carries the same invariant for generated
authoritative formal views.

A generated view is not itself authority. A CURRENT/CANONICAL/EXACT_CURRENT
formal view must be bound to the exact compiled current payload, compiler and
authority-policy identities, dependency identities, frozen-dependency
admissions, dependency closure, and a composition type-check receipt.

## Boundary

Universal host interception remains EXTERNAL_NOT_OWNED.

The repository-owned claim is:

when a formal-system mathematics job enters a Take-5-governed ImprovementCore or
shared mathematical-emission path, stale/mixed-authority reconstruction cannot
legally become authoritative green output without the formal-claim admission
receipt.

## Promotion

Implementation is validated.

Promotion waits only for the final receipt/documentation commit to pass the same
repository gates and for PR #143 to merge.
