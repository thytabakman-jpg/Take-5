# Root Cause + Improvement Core Architecture Repair 022

Date 2026-09-24
Scope Take-5 nonproduction
Migration authority NONE

## Root cause target

Why did the Currentness Audit and the MT/Architecture/RTC foundation sweep still miss a newer system-architecture result?

## Root cause chain

Observed failure:
component currentness checks passed or produced local patches, yet a later architectural insight changed what the system itself is.

Immediate cause:
Currentness Audit compared components against latest component-level bases.

Deeper cause:
the audit treated Architecture as one audited component instead of the basis that types all component roles.

Deeper cause:
Take-5 still encoded the system primarily as a controller/tool architecture.
The newer research identifies an endogenous work-generating research system.

Root generator:
ARCHITECTURE-BASIS EXTERNALIZATION.

The architecture basis used by Currentness was not itself a mandatory reflexive precondition of Currentness.

Therefore:
CA(x | A_old) could return CURRENT
while A_old != A_latest.

Formal failure:
forall x Current(x | A_old) does not imply Current(System | A_latest).

## Latest system identity

ConversationInterface != ResearchProcess != ResearchState.

The system lifecycle is:

Input/State
-> generate obligations/work
-> preserve plurality/incomparability
-> select reachable work
-> invoke Improvement Core policy/controller as needed
-> execute configured capabilities
-> admit/integrate verified deltas
-> persist claim/work history
-> regenerate work
-> close only when no fresh justified work remains.

Improvement Core is not the whole system.
It is the adaptive improvement/control policy inside the work lifecycle.

## Two entry modes

JOB_CONDITIONED:
a protected job exists and generates obligations relative to admitted state.

ZERO_REQUEST_DISCOVERY:
no substantive job is supplied; discovery generates candidate obligations without manufacturing authority.

## Closure correction

Bounded execution stop != closure.

CLOSED requires:
fresh generated work minus discharged work = empty
AND no blocking OPEN coordinate
AND history-based reconstruction/workflow-faithfulness certificate passes.

Otherwise:
ACTIVE
PAUSED_OPEN
or BLOCKED.

## History correction

State-only closure is insufficient.

Claims have lifecycle:
PROPOSED -> WORKING -> SUPPORTED -> ADMITTED.

Admitted claims require evidence.
Closure requires history reconstructibility and workflow faithfulness, not merely a clean current state.

## Improvement Core repair

Improvement Core now sits inside the endogenous work loop.

IC does not own existence of all work.
It owns adaptive policy over admitted obligations:
mode choice
capability/package choice
delegation
improvement
verification/reentry policy.

The Endogenous Work Generator owns:
work discovery
work regeneration after state change
discharge accounting
closure truth.

## Currentness repair

Before component audit:
1 freeze latest ArchitectureBasis;
2 compare built architecture basis to latest;
3 if material basis delta exists, component-level CURRENT claims are invalidated for affected roles;
4 propagate new role/ownership/closure/state semantics;
5 only then audit components.

Currentness is therefore reflexive and architecture-first.

## Implemented

runtime/endogenous_work.py
runtime/research_system.py
runtime/reflexive_currentness.py
tests/test_system_architecture_currentness.py

## Consequence for prior readiness

READINESS_EVIDENCE_016 and FOUNDATION_TOOL_AUDIT_021 remain historical evidence.
They are not final current-basis readiness certificates.

The system must now rerun currentness and validation under EWG-ARCH-001.

No migration is authorized.
