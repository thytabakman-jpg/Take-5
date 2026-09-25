# IC-028 Role Separation Decision 045

Date: 2026-09-24
Controller: IC-028
Question: Is Jane meant to be the operator, or is Jane a lower-level kernel/guardrail/state substrate while an Improvement-Core-class controller operates?
Status: DECISION CANDIDATE FROM CODE + BEHAVIOR AUDIT

## Rewritten prompt

Determine the smallest role decomposition that preserves the useful Take-5 foundation and the strongest historical IC-028 operator behavior. Compare actual implementation, not names. Decide whether to enlarge Jane into an operator, replace Jane, or narrow Jane to a substrate role. Prefer the decomposition with lower duplication, clearer authority, shorter hot path, and stronger behavioral preservation. Do not migrate merely because a component is older.

## Actual implementation evidence

runtime/jane.py currently provides:
- JanePacket
- capability disposition wrapper
- delegation planning wrapper
- human projection

It does not implement:
- work discovery
- adaptive policy selection
- native execution loop
- return admission
- persistence/recovery
- affected-cone propagation
- recursive completion
- zero-request continuation.

runtime/improvement_core.py implements an adaptive execution loop over obligations/packages/workers with delegation, execution receipts, TRC and reentry.

runtime/system_loop.py owns endogenous work generation/selection/closure and invokes Improvement Core.

runtime/controller_episode.py implements selection->binding->execution->consumption evidence.

runtime/continuation_engine.py now exposes the missing composed continuation sequence, but handlers are not yet fully bound.

Therefore current code already falsifies the architectural story "Jane is the operator." Jane is presently an interface/control-service facade.

## Role factorization

Let:
K = legality/invariants
S = persistent typed research state/currentness/evidence
O = operator/controller
I = human interface/projection

Best current factorization:

Foundation = K + S
Operator = IC-028-class controller over current Take-5 capabilities
Interface = Jane

Jane may also expose Foundation services, but does not own research-policy intelligence merely because it is user-facing.

## Proposed responsibilities

### Foundation / Take-5 kernel
Always-on:
identity, authority, evidence, OPEN/BLOCKED/CONFLICT, execution truth, artifact reality, currentness, provenance, state transitions, controller lease, preservation.

It answers: is this transition legal, grounded, current and recoverable?

### IC-028-class operator
Episode owner:
observe, recover goal, generate work, select tools/policies, run MO-MT/MTA/PD/RTC when relevant, bind workers, execute, admit results, propagate consequences, verify, reenter, stop with CompletionCert.

It answers: what do we do next, and does the work actually reach completion?

### Jane
Human/system interface:
accept user input, construct/fetch the canonical state packet, hand an episode lease to the selected operator, present HumanView, expose receipts/open coordinates, accept explicit user authority changes.

It answers: what did the user ask, what is the system doing, and what does the user need to see/control?

## Why not make Jane equal IC-028?

Possible, but currently wasteful.
To make Jane a competent operator would require importing/reimplementing almost the entire operator loop into jane.py. That creates duplicate controller identity and repeats the migration mistake of equating a name/interface with a capability.

Jane can become "as competent" from the user's perspective by delegating to the competent operator while retaining kernel/interface responsibilities.

Competence(UserFacingJane) =
InterfaceQuality + CorrectOperatorSelection + OperatorCapability + FoundationIntegrity,
not size(jane.py).

## Kernel question

Take-5 is a better candidate foundation than historical IC-028 alone because it contains newer:
- scope/mode geometry
- currentness machinery
- RCDL
- typed Work
- activation/evidence bridge
- controller lease
- coordinate anti-conflation
- historical challenger library.

IC-028 is a better demonstrated semantic operator contract than Jane.

Therefore the evidence favors:
Take-5 foundation + IC-028-class operator + Jane interface,
not rollback to old foundation and not enlargement of Jane into a duplicate operator.

## Migration rule

Do not "migrate everything here" by copying all old files.

Migrate/reconstruct only behavior whose residual is not already implemented in Foundation or Operator.

For each historical behavior h:
Factor(h)=<foundation_part,operator_part,interface_part,residual>.
Only residual with protected result/continuation effect is imported.

## Immediate architecture repair

Rename the conceptual roles without necessarily renaming files:
Jane := interface/facade
Take5Foundation := kernel + state + evidence/currentness
Operator := configured IC-028 successor using continuation engine

Improvement Core remains the adaptive policy engine inside Operator.

## Critical remaining gap

The operator is still not persistent between chat turns. In this environment, a user message is still required to initiate another tool-execution turn. Repository code cannot itself create an always-running process. That limitation must remain explicit.

## Decision

NARROW JANE, DO NOT REBUILD JANE AS OPERATOR.

Preserve Jane because it is useful as interface/projection.
Promote role clarity, not historical runtime authority.
Build the operator from IC-028 semantics plus current Take-5 capabilities.
Use the messy-corpus fixture as the first end-to-end proof.
