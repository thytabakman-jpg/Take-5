# Root Cause in Observer Mode — Post-Repair 011

Date: 2026-09-25
Controller: ICC / current semantic IC-028
Entry mode: OBSERVE_DECOUPLED
Status: EXECUTED OBSERVER-FIRST DIAGNOSIS / RUNTIME ORDERING VALIDATED

## ICC rewritten prompt

Repair observer mode as an entry behavior rather than a late tool call. Freeze the original failure,
observe the current runtime without optimization pressure, reconcile the observation, close the
observer consequence boundary, then run Root Cause. Preserve the distinction between selection,
enforcement, ordering, closure, and full canonical TRC realization. Do not call the problem solved
merely because an OBSERVE label exists.

## Entry contract

Controller = IC-028
Mode0 = OBSERVE_DECOUPLED
Target = observer-mode entry and execution behavior
Boundary = Jane entry -> EntryContract -> IC028 stage plan -> observer reconciliation/closure -> Goal/Plan
Authority = successor-development
Entry receipt = required before substantive work

## Frozen observer returns

O1
runtime/entry_contract.py now binds frozen target, controller, initial mode, boundary, authority and receipt.

O2
runtime/jane.py now provides begin_turn(...), which binds the entry contract before operator work.

O3
runtime/ic028_operator.py refuses unbound entry and validates controller identity.

O4
observer-first has a distinct legal stage order:
OBSERVE
-> OBSERVE_RECONCILE
-> OBSERVE_TRC
-> RECOVER_GOAL
-> CURIOSITY_PD
-> FORMALIZE
-> PLAN_ORDER
-> ...

O5
the original failure prompt:
"Run the equation on itself, then run Goal and then run Architect"
now auto-selects OBSERVE_DECOUPLED through preflight contamination-risk classification even though
the text does not contain "observer mode".

O6
explicit observer language still selects observer-first directly.

O7
explicit GOAL_DIRECTED mode remains available and preserves the normal goal-first order.

O8
the initial implementation exposed a stale Jane import and a material-delta carry-forward defect.
Both were repaired rather than hidden by weakening tests.

O9
the full Take-5 validation workflow passes after the observer-order repair.

O10
OBSERVE_TRC is now a mandatory closure handoff point before Goal/Plan. However the repository still
does not contain a native runtime implementation proven equivalent to the full semantic Tool Run
Closure contract. The operator requires the handoff; exact full TRC realization remains OPEN.

## Reconciled observation

The original diagnosis "ENTRY-CONTRACT GAP" was directionally correct but too narrow for the whole
observer recurrence class.

There are three distinct pre-substantive control obligations:

1. BIND
   freeze target/controller/boundary/authority before work.

2. SELECT
   choose the initial mode from explicit instruction or contamination-risk preflight before
   goal-directed optimization can bias the observation.

3. ORDER/CLOSE
   when observer-first is selected, execute and reconcile independent observation, then cross
   a closure boundary before Goal/Plan.

## Root-cause diagnosis

Failure class:

F_obs =
ControllerDrift
union
ModeSelectionFailure
union
ModeOrderFailure
union
ObserverClosureBypass.

Shared root generator:

PRE_SUBSTANTIVE_CONTROL_CONTRACT_GAP.

The earlier system had no mandatory object:

PEC(u,Z)
=
<FT,Controller,Mode0,ModeBasis,Boundary,Authority,ClosureHandoff,Receipt>

bound before substantive transition.

The repaired runtime now implements:
- FT/controller/mode/boundary/authority receipt;
- explicit + preflight mode selection;
- observer-first stage ordering;
- mandatory observer closure handoff;
- regression tests.

## Causal discrimination

R1 "user did not say observer"
Rejected as root.
The original self-application prompt now selects observer-first automatically.

R2 "observer tool existed but was forgotten"
Rejected as sufficient explanation.
The prior operator structurally placed OBSERVE after goal/planning.

R3 "fixed IC028 stage order"
Confirmed proximate mechanism for ordering failure.
Repaired with mode-dependent legal stage plans.

R4 "Jane did not bind ICC entry"
Confirmed proximate mechanism for controller-entry friction.
Repaired with begin_turn -> EntryContract -> ControllerLease.

R5 "mode selector only labels a mode"
Confirmed contributor.
Entry mode now controls stage ordering.

R6 "observer result can flow into Goal before closure"
Confirmed wrapper-level risk.
Repaired structurally with mandatory OBSERVE_TRC handoff.
Full canonical TRC worker realization remains OPEN.

## Current law

Bound(PEC)
prec
SubstantiveTransition.

For observer-first:

OBSERVE
prec
OBSERVE_RECONCILE
prec
OBSERVE_TRC
prec
RECOVER_GOAL
prec
PLAN_ORDER.

## Validation

Regression coverage now includes:
- explicit ICC + observer request binds IC-028 and OBSERVE_DECOUPLED;
- the original self-application prompt auto-selects observer-first;
- OBSERVE precedes observer reconciliation;
- observer reconciliation precedes observer TRC;
- observer TRC precedes Goal and Plan;
- goal-directed mode preserves normal ordering;
- operator refuses missing entry contract;
- material delta persists across later no-delta stages.

GitHub Actions Take-5 Validation run 133:
SUCCESS.

## Disposition

OBSERVER_ENTRY_SELECTION = IMPLEMENTED + TESTED.
OBSERVER_ORDERING = IMPLEMENTED + TESTED.
ICC_ENTRY_LATCH = IMPLEMENTED + TESTED.
OBSERVER_CLOSURE_HANDOFF = IMPLEMENTED + TESTED.
FULL_CANONICAL_TRC_RUNTIME_EQUIVALENCE = OPEN.

The original observer-mode failure is repaired at the entry/order level.
Do not claim the entire semantic HF001^TRC stack is natively realized until the full TRC runtime
worker and session wrapper are independently validated.
