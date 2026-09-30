# Controller Tool-Conductor Mandatory Consultation Mathematics 005

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Canonical repository: thytabakman-jpg/Take-5
Targets: ImprovementCore, current ICC128
Preserved object: ToolConductor
Legacy boundary: ICC128 Legacy snapshot remains immutable

## Governing defect

ToolConductor is a real configured tool with exhaustive product semantics, but the current
ImprovementCore and ICC128 controller paths do not require an actual ToolConductor traversal
before selecting work.

Therefore:

ToolConductor available

does not entail

controller consulted complete registered repertoire.

That gap permits controller episodes to skip registered tools even while the system contains
a correct exhaustive conductor.

## Preserved ToolConductor identity

Let I be the exact ordered registered repertoire MATERIAL_TOOLS.

ToolConductor remains:

TC_I(x,c) = ( T~_i(x,c) )_(i in I).

For every i in I, exactly one conductor-level disposition is emitted.

This repair does not add selection, controller recurrence, or improvement semantics to
ToolConductor.

## Consultation receipt

For controller state z and adapter environment A, define:

R_TC(z,A) = TC_I(z,A).

CoverageComplete(R_TC)
iff

1. tool_count(R_TC) = |I|;
2. the emitted tool-id sequence is exactly I;
3. every i in I occurs exactly once;
4. every factor exposes a typed disposition.

A consultation is admitted when CoverageComplete is true.

Individual factor status OPEN or BLOCKED does not invalidate the consultation.
Those statuses are part of the evidence consumed by the controller.

The controller fails OPEN only when the conductor traversal itself cannot establish complete
registered-repertoire coverage.

## Active-controller anti-recursion

When controller K in {ImprovementCore, ICC128} invokes ToolConductor, its own adapter is not
forwarded into the nested conductor environment.

A_K = A \ {K}.

The ordinary selected-tool adapter environment is not automatically reused as A. Conductor
consultation adapters must be explicitly consultation-safe. This prevents a mutating selected
tool from executing before the controller's specification/admission gates merely because the
same adapter exists for later selected execution.

Thus the active controller's ToolConductor factor may remain OPEN, but cannot recursively
spawn the same active controller through an injected adapter.

ToolConductor's own factor remains its existing SELF_WITNESS.

## ImprovementCore ordering

The rich IC-028 stage order is strengthened from:

... OBJECTIFY -> GENERATE_WORK -> SELECT ...

to:

... OBJECTIFY -> TOOL_CONDUCTOR -> GENERATE_WORK -> SELECT ...

where TOOL_CONDUCTOR is repository-owned, not a host-supplied semantic handler.

Let z* be the state after OBJECTIFY.

R = R_TC(z*, A_ImprovementCore).

Then:

z_TC = z* union {
  tool_conductor_consultation: R,
  tool_conductor_coverage: COMPLETE
}.

GENERATE_WORK and SELECT receive z_TC.

This preserves the principle that inquiry and object recovery precede tool/package selection
while guaranteeing that the full registered repertoire is visible before work selection.

## ICC128 ordering

The current controller loop is strengthened from:

G_Q -> G_W -> S -> E -> A -> U -> G_Q

to:

G_Q -> TC -> G_W -> S -> E -> A -> U -> G_Q.

After questions q_t are generated, construct a conductor packet containing the current state
and q_t. Run exhaustive consultation before work generation.

Thus G_W and S may condition on the full repertoire dispositions.

For every material reentry iteration, ToolConductor is consulted again on the new state.

## Controller-use invariant

For current ImprovementCore episode e:

Select(e) => exists R [ToolConductorConsultation(R) and CoverageComplete(R)].

For current ICC128 iteration t:

G_W(t) => exists R_t [ToolConductorConsultation(R_t) and CoverageComplete(R_t)].

A controller may choose no executable tool after consultation. It may not claim that the
registered repertoire was considered without the coverage receipt.

## OPEN preservation

Let Open(R) be the set of factors whose conductor disposition is OPEN or BLOCKED.

Open(R) is retained in controller state.

Open(R) != controller failure.

Instead Open(R) is evidence available to generation, selection, admission, and later reentry.

Only failure of CoverageComplete blocks the controller consultation stage.

## Regression requirements

Implementation is admitted only when tests prove:

1. ImprovementCore performs ToolConductor before GENERATE_WORK and SELECT.
2. ImprovementCore exposes complete repertoire coverage in state.
3. ICC128 performs ToolConductor after G_Q and before G_W/S on every iteration.
4. current active-controller adapter is suppressed to prevent recursive self-spawn.
5. factor-level OPEN/BLOCKED does not falsely terminate the controller.
6. missing or duplicate conductor factor coverage fails OPEN.
7. existing ToolConductor product semantics remain unchanged.
8. ICC128 Legacy snapshot is untouched.
9. configured full-invocation and HF2 protections remain intact.

## Scope boundary

This repair solves controller-to-ToolConductor integration.

It does not yet define the separate mandatory preflight requested elsewhere:

ASSERT -> SemanticDeterminacy -> CompressionSafety.

That preflight can precede this consultation without changing the mathematics here.
