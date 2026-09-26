# MT HF-002 Reentry 088

Date: 2026-09-26
Status: EXECUTED / LOCAL RELATIVE CLOSE
Input successor: ImproveCore Run 087 audit architecture

## Reentry question

After ImproveCore changed the audit from a path-classification campaign into a typed proof-capable state machine, does the same MT job expose another material local structural delta?

## Result

The new state separates:

addressability
-> candidate extraction
-> semantic decomposition
-> load-bearingness
-> provenance/currentness reconciliation
-> disposition
-> authorized repair
-> destination verification
-> currentness rebase
-> ProofCore.

This resolves the central conflation found in MT Run 086.

## New distinction found

There remains one additional load-bearing distinction:

semantic disposition and physical relocation are not identical.

A file can be correctly dispositioned as:
KEEP_HISTORICAL
or
REFERENCE_ONLY
or
CANONICAL_POINTER_REQUIRED

without moving its bytes.

Therefore the destination stage must support both:

LogicalPlacement(x)
and
PhysicalPlacement(x).

CorrectPlacement(x)
requires logical placement to be resolved.
Physical movement is required only when the disposition licenses it.

This prevents destructive folder cleanup from becoming a false proxy for information architecture.

## Contract refinement

SemanticDispositionLedger entries require:

<Source,
 MaterialObject,
 LogicalPlacement,
 PhysicalAction,
 AuthorityEffect,
 ReferenceRepair,
 Verification,
 Open>.

PhysicalAction is one of:

KEEP
MOVE
COPY_SAFE_ABSTRACTION
ADD_POINTER
MERGE_WITH_WITNESS
DELETE_ONLY_WITH_REDUNDANCY_PROOF
OPEN.

## HF-002 local closure

No further same-job structural distinction was found after adding LogicalPlacement versus PhysicalPlacement.

HF2(MT)=RELATIVE_CLOSE under the present basis.

This does not close the corpus audit itself.
It closes the local MT reapplication frontier created by Run 086.
