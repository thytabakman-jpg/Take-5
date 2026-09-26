# Second ImprovementCore + HF2 — Bound ZIP Recovery Promotion 128

Date: 2026-09-26
Controller: ImprovementCore / IC-028
Regime: 091
Recurrence: HF002

## Successor finding

The bound-ZIP adapter is implemented and validated, but a fresh ImprovementCore recovery would not reliably discover it unless the normal recovery surfaces also name and verify it.

Selected repair:

Promote the adapter through the existing recovery manifest, current ImprovementCore anchor, and recovery validator. Do not create another registry or controller.

## Implementation

The recovery manifest now names artifact_intake, archive_artifact_intake, the Artifact-to-Work Intake Contract, and recommendation 126.

The protected behavior set now includes exact ZIP binding before intake and complete member accounting with unresolved-member preservation.

CURRENT_IMPROVEMENT_CORE now includes those behaviors and places the intake contract plus both runtime intake files in its canonical recovery load order.

runtime/improvement_core_recovery.py now requires those files and verifies the manifest and anchor pointers.

Validation after the recovery-validator change:

Take-5 Validation 36276910234: SUCCESS.
Capability Preservation 36276910242: SUCCESS.

## HF2 recurrence

Round 0:
implemented capability versus recoverable capability separated.
Material delta: recovery surfaces now carry the new capability.
HF2 -> REAPPLY_C.

Round 1:
machine recovery validator now fails when the capability disappears from the current manifest/anchor.
Material delta: omission becomes detectable regression.
HF2 -> REAPPLY_C.

Round 2:
no further repository-owned strict-gain repair is evidenced.
HF2 -> RELATIVE_CLOSE.

## Disposition

Repository-owned bound-ZIP intake:
CLOSED_RELATIVE.

Repository-owned recovery/discoverability:
CLOSED_RELATIVE.

The identity of any still-unbound substantive external archive remains OPEN_WITH_REENTRY.

No unchanged recurrence is licensed.
