# ImprovementCore Parent Return Closure 139

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / FAIL-CLOSED
Canonical repository: thytabakman-jpg/Take-5

## Problem

Repeated ImprovementCore episodes produced a real material gain, persisted it, and then returned to the user even though the governing job still had owned work.

The existing architecture already distinguished:

Plan != Diagnosis != Artifact != PartialImplementation != ChildSuccess != ParentCompletion.

The missing enforcement point was the final user-return boundary.

HF2 correctly owned same-capability local recurrence. It did not own proof that the larger governing job was finished.

Therefore a local HF2 fixed point could be accepted after a semantic provider or stage controller marked the parent COMPLETE too early.

## Root defect

The invalid implication was:

MaterialStep
or ChildComplete
or HF2RelativeClose
=> ParentReturn.

The repaired relation is:

ParentReturn
iff
PostHF2ReturnGate
and
NoOwnedExecutableWork
and
ConsequenceClosed
and
(
  GoalClosed
  or TypedNonCompleteBoundary
).

For COMPLETE:

ReturnComplete
iff
HF2Saturated
and GoalClosed
and not OwnedWorkRemaining
and ConsequenceClosed
and EvidenceBound.

For OPEN/BLOCKED/CONFLICT:

ReturnNonComplete
iff
not OwnedWorkRemaining
and ConsequenceClosed
and TypedBlocker
and EvidenceBound.

## Recurrence law

One parent round is:

ParentRound = HF2[ImprovementCore].

After every parent round:

ParentRound
-> ReturnVerifier
-> {
     RETURN,
     CONTINUE
   }.

CONTINUE is not a user-visible answer.

CONTINUE forces:

terminal := CONTINUE
admitted_continuation := TRUE
parent_return_continuation := TRUE

and then re-enters the complete ImprovementCore path, including HF2 again.

ParentReturnContinuation and RecursiveChildContinuation are distinct coordinates.
The parent gate does not manufacture live_continuation. A verifier may set
live_continuation explicitly only when recursive child-manager work is actually live.

Therefore:

one strict gain != permission to return.

HF2 remains local recurrence.
The parent return gate owns whole-job user-return permission.
HF1 retains upstream invalidation/reentry.
TRC retains consequence closure.

## Runtime

Shared gate:

runtime/improvement_core_return_gate.py

Fixed-stage compatibility/default path:

runtime/improvement_core_hf2_default.py

Legacy-restored path:

runtime/improvement_core_legacy_restored.py

Restored semantic dispatch:

runtime/improvement_core_restored_dispatch.py

## Fail-closed behavior

Ordinary user-facing execution without a parent return verifier returns:

PARENT_RETURN_GATE_REQUIRED.

Disabling HF2 without explicit debug authority returns:

HF2_DISABLE_REQUIRES_EXPLICIT_DEBUG_AUTHORITY.

The one-pass low-level regime remains available for controlled debugging and internal tests. It is not a user-visible completion authority.

## Historical evidence

The repair is supported by repeated prior episodes in which the user had to prompt ImprovementCore again after a reported completion and a later pass found additional material work.

Relevant recurring evidence includes:

- premature stopping identified during HF1/HF2 reconstruction;
- independent ImprovementCore reruns finding strict gains after prior local closure;
- user reprompting functioning as external scheduler/reentry trigger;
- the restored Legacy benchmark's explicit NO_PREMATURE_TERMINALITY requirement;
- the current conversation's direct report that responses often return after one meaningful step rather than after the governing job is finished.

This architecture treats those as one defect class rather than separate prompting preferences.

## Regression requirements

Required tests cover:

1. a first meaningful step falsely marks COMPLETE;
2. the parent verifier identifies another owned job;
3. the first user return is forbidden;
4. the complete ImprovementCore+HF2 capability runs again;
5. a later parent closure is required before COMPLETE;
6. missing return verifier fails OPEN;
7. COMPLETE with owned work is rejected;
8. COMPLETE without goal closure is rejected;
9. return with an open consequence is rejected;
10. non-complete return without typed blocker is rejected;
11. an OPEN/BLOCKED/CONFLICT candidate cannot be upgraded to COMPLETE by the return verifier;
12. parent continuation does not silently assert recursive child-manager liveness;
13. HF2-disabled ordinary execution is rejected unless explicit debug authority is present.

## Closure boundary

This repairs repository-governed user-return logic.

It cannot force an unrelated external chat host to call the repository runtime. Universal host interception remains externally owned.

A host that does bind Take-5 ImprovementCore must supply the semantic whole-job return verifier for the restored path or receive OPEN rather than false completion.
