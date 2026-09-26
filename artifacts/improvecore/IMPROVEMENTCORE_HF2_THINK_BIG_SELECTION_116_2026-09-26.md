# ImprovementCore + HF2 Think-Big Selection 116

Date: 2026-09-26
Command: Think big, fix this.
Controller: ImprovementCore / IC-028
HF2: explicit experimental campaign composition
Input: externally verified observer campaign 115

## Observer evidence

The observer pass established:

1. configured-tool PTI is already CLOSED_RELATIVE inside Take-5;
2. the live repository-owned seam is outside that configured-tool path;
3. campaign and Legacy artifacts can make execution claims without a generic causal
   attestation object;
4. universal host interception remains EXTERNAL_NOT_OWNED;
5. HF2[ImprovementCore] is being tested as an explicit campaign binding, not assumed as
   already promoted.

## Action candidates

### A. LEGACY_ONLY_RECEIPT_PATCH

Coverage:
one current Legacy seam.

Owned:
yes.

Risk:
creates another special-case receipt path.

### B. EXECUTION_CLAIM_INTEGRITY_GATE

Coverage:
repository artifacts outside configured-tool PTI that claim execution,
including Legacy/campaign reporting.

Owned:
yes.

Architecture relation:
reuses PTI semantics and does not replace PTI.

Required property:
claims must fail closed unless the causal evidence required by the claimed execution level
is present.

### C. DUPLICATE_CONFIGURED_PTI

Coverage:
configured tools.

Owned:
yes.

Disposition:
REJECTED because the configured path already has validated PTI.

### D. UNIVERSAL_HOST_INTERCEPTION

Coverage:
external host bypass.

Owned:
no.

Disposition:
EXTERNAL_NOT_OWNED.

## ImprovementCore selection

Selected:

EXECUTION_CLAIM_INTEGRITY_GATE.

Reason:

It is the broadest repository-owned candidate that covers the recurrent evidence without
duplicating an already-validated invariant or claiming authority over the external host.

## HF2 plan for the action pass

Round 0:
select and specify the gate.

Round 1:
reapply ImprovementCore after implementation evidence exists; verify that campaign/Legacy
execution claims cannot reach VERIFIED without a causal runtime chain.

Round 2, only when required:
reapply ImprovementCore after receipt/persistence evidence changes; determine relative closure
or return/reentry.

No universal HF2 promotion is implied by this campaign.

Status:

SELECTED_FOR_IMPLEMENTATION.
