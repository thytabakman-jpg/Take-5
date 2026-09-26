# Improvement Core Usage Audit 078

Date: 2026-09-26
Status: AUDIT COMPLETE / REPAIR ACTIVE
Authority: evidence report, not self-promoting architecture

## Governing question

When has Improvement Core worked in the way the user values, when has it been weak,
and what distinguishes those episodes?

The audit treats user reactions, repository behavior, runtime structure, and historical
controller records as evidence. It does not assume the current runtime or historical
labels define the desired object.

## Strong-pattern findings

The strongest Improvement Core episodes share these properties:

1. Controller ownership is explicit.
   The controller, not the surrounding host response, owns problem reconstruction,
   work generation, selection, continuation, and closure.

2. Work is regenerated after material discoveries.
   New evidence changes state, which changes the question/work frontier, which can
   change the selected capability or plan.

3. Inquiry precedes package selection.
   The system does not begin from a fixed tool list and then search for a use.

4. Execution is real and typed.
   Selected, bound, executed, returned, admitted, integrated, persisted, and consumed
   remain separate states.

5. Continuation is endogenous.
   A material result triggers reentry without requiring the user to manually ask
   for the next pass.

6. OPEN/BLOCKED remain legitimate terminal states.
   The controller does not manufacture closure to finish the conversation.

7. Observer-first behavior is available when optimization would contaminate discovery.

8. The controller can challenge its own result before promotion.

These properties are represented most richly by the IC-028 semantic controller/operator
lineage rather than by the narrower obligation/package runtime alone.

## Weak-pattern findings

Weak episodes repeatedly show one or more of these failures:

1. Host substitution.
   ChatGPT decides the plan, tool order, or stopping point before Improvement Core
   receives control.

2. Semantic-only invocation.
   A tool name is discussed or simulated without the configured controller path
   being executed.

3. Narrow-core substitution.
   runtime/improvement_core.py performs valuable obligation/package routing but does
   not itself expose the complete IC-028 lifecycle.

4. Manual continuation.
   Later user prompts supply reentry that the controller was meant to own.

5. Static problem representation.
   Material discoveries do not regenerate the work/question frontier strongly enough.

6. Activation ambiguity.
   Improvement Core exists in several historical and runtime forms, but a normal
   user invocation does not have one obvious repository entrypoint proving which
   controller actually ran.

7. Completion without rich receipts.
   A reply can sound like an Improvement Core result without demonstrating the
   IC-028 stage sequence or controller lease.

## Architectural split

Current narrow runtime:

runtime/improvement_core.py

Primary behavior:
question frontier -> package selection -> delegated execution -> delta routing.

Richer controller path:

runtime/ic028_operator.py

Protected lifecycle includes:
RECOVER_GOAL
CURIOSITY_PD
FORMALIZE
PLAN_ORDER
OBSERVE
OBJECTIFY
GENERATE_WORK
SELECT
BIND
EXECUTE
ADMIT
RECONCILE
PROPAGATE_AFFECTED_CONE
PERSIST
VERIFY
COMPLETE
REENTER

Observer-first mode additionally places frozen observation/reconciliation/TRC before
goal-directed stages.

These are not equivalent operating surfaces.

## Main diagnosis

The recurring Improvement Core problem is not simply that the controller is weak.

It is ACTIVATION IDENTITY LOSS.

The desired semantic controller exists, but ordinary use can drift among:

- ChatGPT-led reasoning;
- narrow runtime/improvement_core.py;
- historical IC labels;
- richer IC-028 operator semantics;
- ICC wrapper orchestration.

The user experiences the rich controller only when the correct path happens to be active.

## Repair target

A normal user invocation of "ImproveCore" or "Improvement Core" needs a dedicated,
testable manager entrypoint that:

1. binds the IC-028 controller lease;
2. freezes target/job/basis;
3. selects observer-first mode when contamination risk exists;
4. executes the rich IC-028 stage plan;
5. exposes receipts proving what ran;
6. preserves reentry;
7. does not silently fall back to the narrow core.

The narrow runtime may remain useful as a subordinate capability inside the manager.

## Completion test

The repair is successful only when a normal ImproveCore invocation can be mapped to
one explicit manager entry function and tests prove:

- controller == IC-028;
- entry contract is bound;
- rich stage plan executes;
- observer-first mode executes observation before goal recovery when required;
- reentry is reachable;
- missing stage bindings fail OPEN/BLOCKED rather than falling back;
- narrow improvement_core.py remains available as a child capability rather than
  being confused with the manager identity.

## Disposition

REPORT: COMPLETE_RELATIVE
ACTIVATION REPAIR: REQUIRED
GLOBAL HISTORICAL COMPLETENESS: NOT CLAIMED
