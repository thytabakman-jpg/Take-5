# ImprovementCore + HF2 Think-Big Fix Campaign 117

Date: 2026-09-26
Command: Think big, fix this.
Controller: ImprovementCore / IC-028
HF2: explicit experimental campaign composition
Input:
- MT audit 004;
- externally verified observer campaign 115;
- selection artifact 116.

## Selected repair

EXECUTION_CLAIM_INTEGRITY_GATE.

Implementation:

runtime/execution_claim_integrity.py

Legacy integration:

runtime/icc128_legacy_reporting.py

Portable activation integration:

runtime/icc128_legacy_portable.py

Formal architecture:

architecture/EXECUTION_CLAIM_INTEGRITY_117.md

## Why this is the big repair

The configured-tool path already has validated PTI.

Therefore the action pass rejects:

DUPLICATE_CONFIGURED_PTI.

Universal host interception remains outside repository authority.

Therefore the action pass rejects:

UNIVERSAL_HOST_INTERCEPTION.

A Legacy-only patch covers one symptom.

The selected gate covers the repository-owned class:

execution claims made by artifacts outside configured-tool PTI.

## Action HF2 recurrence

### Round 0 — implementation and causal probe

ImprovementCore receives the literal command:

Think big, fix this.

Recovered generator:

UNATTESTED_EXECUTION_CLAIMS_OUTSIDE_CONFIGURED_PTI.

Admissible candidates are ranked by repository-owned coverage while preserving PTI.

Selected:

EXECUTION_CLAIM_INTEGRITY_GATE.

The implementation probe verifies:

1. an EXECUTED claim missing execution evidence remains OPEN;
2. a real ICC128 Legacy Controller.run is invoked;
3. that exact run_result is consumed by the attested reporting function;
4. a bare GitHub report receipt does not close the Legacy run;
5. persistence and report verification upgrade the same causal execution receipt to VERIFIED;
6. portable Legacy activation rejects a report receipt without a VERIFIED execution claim;
7. portable Legacy activation accepts both coordinates.

ImprovementCore admission:

IMPLEMENTED_VERIFY_REQUIRED.

HF2 disposition:

REAPPLY_C.

Reason:

execution truth strengthened and an OPEN coordinate was resolved, so the same capability must
see the changed state.

### Round 1 — same-capability verification

ImprovementCore runs again on the successor state.

It verifies:

- selected fix remains EXECUTION_CLAIM_INTEGRITY_GATE;
- incomplete claims fail closed;
- causal Legacy runtime/report chain reaches VERIFIED;
- bare report closure is rejected;
- PTI remains the configured-tool invariant;
- universal host interception remains EXTERNAL_NOT_OWNED.

Repository-owned seam:

CLOSED_RELATIVE.

HF2 disposition:

RELATIVE_CLOSE.

## New Legacy closure rule

Old:

LegacyRunClosed(r)
iff
GitHubReportCommitReceipt(r) exists.

New:

LegacyRunClosed(r)
iff
ExecutionClaim(r)=VERIFIED
and
GitHubReportCommitReceipt(r) exists.

Execution claim order:

IDENTIFIED
<
PLANNED
<
DISPATCHED
<
EXECUTED
<
CONSUMED
<
PERSISTED
<
VERIFIED.

A higher claim requires every lower causal coordinate.

## HF2 status

This campaign validates an explicit composition:

HF2[ImprovementCore]_campaign.

It does not establish universal HF2 wrapper promotion.

Universal HF2 promotion remains OPEN.

## Protected boundaries

Preserved:

- configured-tool PTI;
- fail-closed OPEN/BLOCKED semantics;
- Legacy frozen controller core;
- no cross-run Legacy controller memory inheritance;
- universal host interception classified EXTERNAL_NOT_OWNED.

## Regression

tests/test_execution_claim_integrity.py

tests/test_icc128_legacy_reporting.py

tests/test_icc128_legacy_portability.py

tests/test_improvecore_hf2_think_big_fix_20260926.py

## Pre-CI disposition

ImprovementCore action pass:
IMPLEMENTED_VERIFY_REQUIRED.

HF2:
VERIFY_REQUIRED.

Repository-owned execution-claim seam:
VERIFY_REQUIRED.

Universal host interception:
EXTERNAL_NOT_OWNED.
