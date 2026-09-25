# Root Cause — Observation-Mode Entry Error + ICC Conversation Friction 009

Date: 2026-09-25
Controller: current semantic IC-028 / Diagnosis protocol
Status: SUPERSEDED BY research/ROOT_CAUSE_OBSERVER_MODE_POST_REPAIR_011.md

## D0 frozen failures

F1 OBSERVER-MODE ENTRY ERROR
When the user requested:
run the equation on itself, then Goal, then Architect,
the system began goal-directed/self-application work before an independent observer/DOS pass.
The user had to ask whether observation mode had been used.

Protected behavior:
when observation-first is materially indicated, freeze target/boundary and perform goal-decoupled observation before optimization/goal/repair contaminates the evidence.

F2 ICC CONVERSATION ENTRY FRICTION
The user repeatedly had to say variants of:
Run ICC
I want to talk directly to ICC
No, with ICC
Yes, make that
I have been doing it for days

Protected behavior:
when the user invokes ICC/ImproveCore as the controller, the conversation should route the request into the current ICC controller contract without a meta-conversation about whether such a bridge exists.

Recurrence class:
new chat turns where controller identity and/or initial inquiry mode matter.

## D1 evidence

E1 DOS protocol explicitly requires:
MTA preflight -> freeze X/boundary -> suppress optimization -> independent observation -> reconcile -> restore goal.

E2 runtime/continuation_engine.py begins:
OBSERVE -> OBJECTIFY -> GENERATE_WORK -> ...

E3 runtime/ic028_operator.py hard-codes:
RECOVER_GOAL -> CURIOSITY_PD -> FORMALIZE -> PLAN_ORDER -> OBSERVE -> ...
Therefore its ordinary stage ordering cannot produce genuine observation-first behavior.

E4 runtime/mode_selector.py can label an OBSERVE mode but does not control operator stage order.
Mode selection therefore does not enforce observer-first sequencing.

E5 architecture/IC028_ROLE_SEPARATION_DECISION_045.md says Jane should:
accept user input, construct/fetch canonical state, hand an episode lease to the selected operator, and present HumanView.

E6 runtime/jane.py implements:
JanePacket, capability_disposition, delegate_work, human_view.
It does not implement raw conversation entry, controller selection/latching, controller lease handoff, or persistent conversation-mode identity.

E7 the same role-decision artifact states the operator is not persistent between turns.
That explains why a new user message is required to start a turn.
It does NOT explain why, once the message arrives, the user must repeatedly restate "ICC" or correct the initial mode.

E8 prior ICC conversation-failure diagnosis identified TARGET IDENTITY PERSISTENCE as missing.
The current incident is analogous but distinct:
CONTROLLER/MODE IDENTITY is also not bound at entry.

## D2 localization

User utterance
-> host chat interpretation
-> Jane/interface role
-> controller lease / controller selection
-> initial mode selection
-> operator stage ordering
-> substantive inquiry.

Earliest supported divergence:

There is no mandatory conversation-entry transition between raw user utterance and controller/mode execution.

Downstream manifestation A:
host begins ordinary goal-directed reasoning and only later inserts OBSERVE.

Downstream manifestation B:
host interprets "talk to ICC" as a request to discuss/build a bridge rather than as controller selection.

## D3 live rivals

R1 USER-PHRASING AMBIGUITY
Prediction:
clear explicit "Run ICC" / "observer first" should eliminate failures.
Evidence against:
the user explicitly said "Run ICC" repeatedly and still received bridge/meta explanations.
Does not explain F1 after explicit multi-stage instruction plus established observer practice.
REJECTED as root generator; can contribute locally.

R2 MODEL/CONTEXT FORGETFULNESS
Prediction:
failures arise when prior context is unavailable.
Evidence against:
the relevant DOS and ICC role artifacts were present and retrievable.
The runtime ordering itself places OBSERVE late.
PARTIAL CONTRIBUTOR, not sufficient root.

R3 IC028 FIXED STAGE ORDER
Prediction:
observer-first fails even when an OBSERVE capability exists because RECOVER_GOAL/PLAN_ORDER run first.
Confirmed by code.
Explains F1 strongly.
Does not alone explain ICC conversation-entry friction.
SURVIVES as proximate mechanism.

R4 MISSING JANE CONVERSATION-ENTRY ADAPTER
Prediction:
controller identity is not latched from raw user language and the host can remain the de facto router.
Confirmed by jane.py vs documented Jane responsibilities.
Explains F2 strongly.
Also permits wrong initial-mode selection.
SURVIVES.

R5 CHAT PLATFORM REQUIRES USER TURNS
Prediction:
system cannot continue forever without another message.
True external limitation.
But it does not predict repeated ICC-controller clarification inside an already initiated turn.
REJECTED as explanation of the reported friction; retained as external boundary.

R6 MISSING PRE-EXECUTION ENTRY CONTRACT
Prediction:
both controller identity and initial mode can drift before the governed operator begins.
This generates:
F1 because observer-first is not locked before goal/planning;
F2 because ICC selection is not locked before host interpretation/meta-work.
Confirmed by E3-E6.
SURVIVES and subsumes R3/R4 at the declared recurrence class.

## D4 shared root generator

ENTRY-CONTRACT GAP.

There is no mandatory first transition:

RawUserRequest
-> EntryContract
-> ControllerLease + InitialModeContract
-> GovernedOperator.

Instead the system currently permits:

RawUserRequest
-> host interpretation / goal recovery / planning
-> later controller/mode semantics.

Define:

EC(u,S)
=
<FT, Controller, Mode0, Boundary, Authority, EntryReceipt>

where:
FT = frozen target token;
Controller = selected controller identity;
Mode0 = initial inquiry mode/order;
Boundary = observation/task boundary when required;
Authority = controller/action authority;
EntryReceipt = evidence that the contract was bound before substantive work.

Required invariant:

NoSubstantiveTransition
before
Bound(EC).

For ICC-addressed turns:

Controller(EC)=IC-028/current licensed ICC successor.

For observer-first turns:

Mode0(EC)=OBSERVE_DECOUPLED
and no goal optimization/repair/successor selection may run until the frozen observation returns are reconciled.

## D5 causal roles

ROOT GENERATOR
Missing mandatory entry contract binding controller + initial mode before substantive work.

PROXIMATE MECHANISM F1
IC028 fixed stage order puts OBSERVE after goal/formalize/plan.

PROXIMATE MECHANISM F2
Jane lacks raw-message -> controller-lease handoff/latching despite architecture assigning that role.

ENABLING CONDITION
The host assistant remains the de facto conversation router.

EXTERNAL BOUNDARY
Repository code cannot initiate a new chat turn on its own.

CONTRIBUTOR
Target-identity persistence was repaired semantically, but controller/mode identity persistence was not generalized from that lesson.

## D6 counterfactual challenge

CF1
Add only observer-first stage reordering.
Expected:
F1 improves.
F2 remains.

CF2
Add only ICC conversation trigger/latch.
Expected:
F2 improves.
F1 can remain because selected ICC still starts RECOVER_GOAL before OBSERVE.

CF3
Add one mandatory EntryContract carrying both Controller and Mode0.
Expected:
both recurrence classes are blocked at the earliest divergence, provided the operator obeys the contract.

Therefore R6 is the smallest supported shared generator.

## D7 repair targets

RT1 ENTRY CONTRACT
Create a conversation-entry object and mandatory gate before operator execution.

RT2 CONTROLLER IDENTITY PERSISTENCE
"ICC", "Improvement Core", "ImproveCore", and established direct-address equivalents resolve to the current licensed ICC controller for that turn unless the user supersedes it.
Do not respond with bridge-design meta-work when the target is controller invocation.

RT3 MODE IDENTITY PERSISTENCE
Entry mode must be explicit and binding.
Observer-first must alter stage order, not merely attach an OBSERVE label.

RT4 OPERATOR ORDER
Replace one universal IC028 STAGES tuple with mode-dependent legal stage plans.
Observer-first plan must perform frozen observation before goal-directed optimization.

RT5 JANE INTERFACE COMPLETION
Implement the already-specified Jane responsibility:
raw input -> canonical state packet -> EntryContract -> ControllerLease -> operator handoff -> HumanView.

RT6 REGRESSION TESTS
A. "Run ICC" yields an IC controller lease without bridge-discussion output.
B. "run X on itself, then Goal, then Architect" under observer-first policy records OBSERVE before RECOVER_GOAL/PLAN_ORDER.
C. explicit non-observer task can still use normal goal-first ordering.
D. new user message remains required by host boundary; no false background/autonomy claim.

## D8 disposition

F1 = DIAGNOSED.
F2 = DIAGNOSED.

Shared root generator:
ENTRY-CONTRACT GAP.

Confidence basis:
direct mismatch between documented interface/controller contract and runtime implementation,
plus direct stage-order evidence reproducing the observation-mode failure class.

Runtime repair:
OPEN until EntryContract, Jane handoff, mode-dependent ordering and regression tests are implemented and pass.

## Compact root equation

Failure class:

F = ControllerDrift union ModeDrift.

Root:

Root(F)
=
not Bound(
  EC(u,S)
  =
  <FT,Controller,Mode0,Boundary,Authority,Receipt>
)
before substantive transition.

Required law:

Bound(EC)
prec
SubstantiveTransition.
