# ImprovementCore Mathematics 086

Date: 2026-09-26
Status: CURRENT STRICT-GAIN MATHEMATICS / VALIDATED

## Problem

The prior compact controller was:

C_(J,K) = <Z,D,A_(J,K),pi_(J,K),T_(J,K),Tau_(J,K)>.

Later runtime gains added recursive parent/child management and basis-relative learning
memory as an L3 realization layer.

That factorization was operationally useful but mathematically mixed levels:

- recursion changed the admissible action space;
- learning memory changed which actions were admissible;
- both changed the state needed to determine the next policy.

Therefore they belong inside the controller state/transition mathematics rather than
remaining external adornments.

## Augmented controller

Define memory space M as finite route-evidence histories.

A memory record is:

e = <route,basis,disposition,footprint,evidence>.

Define augmented state:

Z^+ = Z x M.

The current controller candidate becomes:

C^+_(J,K)
=
<Z^+,D,A^+_(J,K),pi^+_(J,K),T^+_(J,K),Tau^+_(J,K)>.

## Learning gate

For action a with route id r, basis b and dependency footprint F, define:

Blocked_M(a,b,Delta)
iff
the latest memory record for (r,b) has disposition in
{NO_GAIN, REJECTED, FAILED}
and
Delta intersect F = empty.

A changed coordinate reopens the route exactly when:

Delta intersect F != empty.

## Admissible action space

Let A_base(z) be ordinary admitted controller actions.

Let A_child(z,m) be admissible recursive ImprovementCore child actions.

Then:

A^+(z,m)
=
{a in A_base(z) union A_child(z,m)
 | not Blocked_M(a,b(z),Delta(z))}.

Thus recursive child work is not a new primitive controller.
It is one typed action family inside the same endogenous continuation controller.

## Policy

The previously open policy coordinate is now typed as a set-valued choice correspondence.

Let H_(J,K)(z,m) be the hard-admissible action set after authority, protected-behavior,
reachability, status, and learning-memory gates.

For each admissible action a define the current configured preference vector

v(a)
=
<goal_gain,information_gain,search_gain,-cost,-risk,reversible>.

Define strict Pareto dominance:

b >_(z,m) a

iff b is no worse than a on every configured preference coordinate and strictly
better on at least one.

Then:

pi^+_(J,K)
:
Z^+
rightrightarrows
A

with

pi^+_(J,K)(z,m)
=
ND(H_(J,K)(z,m)).

Thus pi^+ is a correspondence, not an underspecified single-action function.

Search and experimentation are not hidden inside the selector. They are typed actions
inside H_(J,K), so an information-gathering probe can appear on the same nondominated
frontier as direct work.

Execution resolution is separate:

Resolve(pi^+(z,m),c)
=
- the unique frontier action when the frontier is singleton;
- the explicitly licensed frontier action c when the frontier is plural and c belongs to it;
- OPEN_INCOMPARABLE_FRONTIER when the frontier is plural and no licensed choice exists;
- OPEN_NO_ADMISSIBLE_ACTION when continuation is live but the frontier is empty;
- TERMINAL_EMPTY only when continuation is not live.

This preserves incomparability rather than smuggling a scalar tie-breaker into pi^+.

The policy depends on both live semantic state and learned route history.
Negative evidence is therefore causally relevant to future selection rather than merely
stored provenance.

## Transition

For an ordinary action a:

a
-> Execute
-> Admit/Reconcile
-> state delta q
-> memory evidence e'
-> (z',m').

Formally:

T^+((z,m),a)
subseteq
Z^+ + D.

For a recursive child action a_c:

SelectChild(z,m)
-> ChildRun(a_c)
-> ChildReturn r
-> ParentAdmission(r,z,m)
-> ParentUpdate
-> ParentReselection.

The child return itself is not a state transition authority.

## Progress predicate

Define continuation-relevant materiality:

Mat(delta)
iff at least one of:
- material_result_delta
- material_search_delta
- open_refinement
- negative_evidence
- certified_no_gain
- changed_representation.

Then:

Tau^+(z',m') = CONTINUE
and not Mat(delta)
implies
NO_PROGRESS.

A live continuation with no selected admissible action is a typed liveness failure,
not silent completion.

## Memory update

Let L be the learning update.

m' = L(m,a,admission,delta).

Examples:

ADMIT + material delta -> GAIN
NO_GAIN -> NO_GAIN
REJECT -> REJECTED
OPEN -> OPEN.

The next policy is recomputed from (z',m').

## Unified recursion

The current deepest candidate is therefore:

(z_t,m_t)
-> A^+_(J,K)(z_t,m_t)
-> pi^+_(J,K)
-> a_t
-> T^+_(J,K)
-> (z_(t+1),m_(t+1)) or D
-> Tau^+_(J,K)
-> terminate or recompute pi^+.

This absorbs the former L3 recursion/memory layer into L0 controller mathematics.

## Realization mapping

Configured realization still has multiple operational layers:

R0
entry/self-management envelope

R1
observer/inquiry/formalization/work generation

R2
selection/binding/execution/admission/reconciliation/persistence/verification

R3
recursive child realization and learning-memory substrate.

But R3 is now a realization factor of C^+, not a separate mathematical controller layer.

## Strict gain

This change explains two runtime facts that the older C object did not encode:

1. the same semantic state z can yield a different legal next action after NO_GAIN memory;
2. a recursive child run is selected by the same parent policy and does not become
   authoritative merely by returning.

Those are result-sensitive distinctions, so the augmented state is not cosmetic.

## Remaining OPEN

- whether memory can be safely quotiented by a sufficient statistic;
- global minimality of Z^+;
- exact upstream zero-request relation generator;
- complete capability-repertoire reachability theorem;
- host-wide enforcement outside a runtime that loads Take-5.

## Current conclusion

The preferred current abstract controller is C^+, not the older C alone.

The older C remains the projection obtained by forgetting learning memory and
recursive-action distinctions.


## Validation evidence

PR #55
Merge: 39ca5616d3d8e23042f0ac887d0a447e24ec8ddf
Validation run: 36221315384
Conclusion: SUCCESS

The strict-gain witness is executable in runtime/improvement_core_math.py and
tests/test_improvement_core_math_086.py.
