# RootCause Run on Current Chat 089

Date: 2026-09-26
Status: VALIDATED EXECUTABLE RUN
Tool: RootCause
Local recurrence: HF002
Parent: ImprovementCore
Validation run: 36222526907
Merge: 691462f614dc026ad199f1b343496d06bca4da1e

## Input basis

The build first used MT over:
- the phrase "Rout Cause";
- the current conversation;
- historical Root Cause artifacts;
- current HF1/HF2/ImprovementCore architecture.

MT established that spelling is nonmaterial and "root" is the result-sensitive selector.

## Frozen recurring failure class

1. COLOR_CONTRACT_CLAIMED_REPAIRED_BUT_OUTPUT_VIOLATES
2. TOOL_EXISTS_BUT_NORMAL_INVOCATION_BYPASSES_IT
3. FULL_RUN_REQUEST_DOWNGRADES_TO_BARE_OR_PARTIAL_TOOL
4. MIGRATION_PRESERVES_ARTIFACTS_BUT_LOSES_BEHAVIOR
5. RECOVERY_DOC_POINTS_TO_STALE_OR_OBSOLETE_PATH
6. HOST_REASONING_SUBSTITUTES_FOR_CONTROLLER

## Rival candidates

FINITE_ALIAS_LIST
- real local mechanism;
- explains only coloring incidents;
- not representation-stable root.

DOCUMENTATION_DRIFT
- real enabling condition;
- explains stale recovery incidents only.

ACTIVATION_IDENTITY_LOSS
- explains several invocation/migration/controller failures;
- stable and important;
- fails the removal-breaks-entire-recurrence test for the whole class.

PROTECTED_TRANSITION_INTEGRITY_FAILURE
- explains all six recurrence classes;
- survives representation changes;
- lies upstream of the narrower candidates;
- removal/enforcement would break the declared recurrence class;
- no admitted counterevidence in the frozen fixture.

## HF2 trace

Round 1
- nondominated root candidate exposed;
- smaller-generator challenge remained live;
- disposition REAPPLY_C.

Round 2
- same RootCause capability attacked the changed causal representation;
- no smaller admitted generator displaced the candidate;
- local closure passed.

Local disposition:
RELATIVE_CLOSE.

## Root result

PROTECTED_TRANSITION_INTEGRITY_FAILURE

Operational meaning:

The recurring system failure is generated when protected behavior is represented somewhere
but not enforced through one mandatory, reconstructible, verified transition chain:

canonical identity
-> configured dispatch
-> actual execution
-> result consumption
-> state update
-> reentry
-> final user-visible boundary.

Local fixes repeatedly succeed at one edge while another unprotected transition later
recreates the same failure class.

## Parent handoff

RootCause does not own global repair.

Handoff:
ImprovementCore / ADMIT_ROOT_CAUSE_AND_REPLAN.

The next global repair job is therefore to make protected-transition integrity a
first-class invariant/testable chain across the relevant configured systems, rather than
continuing to patch individual manifestations independently.

## Scope

This is a validated run over the frozen current-chat recurrence packet.

It is not proof that the same generator explains every future system failure.
New evidence can reopen the diagnosis.
