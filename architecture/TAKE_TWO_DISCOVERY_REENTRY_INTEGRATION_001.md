# Take Two Discovery Reentry Integration 001

Date: 2026-09-25
Status: IMPLEMENTED ON EXPERIMENTAL BRANCH / AWAITING VALIDATION
Decision authority: ICC synthesis using pre-upgrade ICC-128 as outer controller and ICC-123 Multi-Object residual logic as an internal challenge
Protected baseline: Take-2 remains untouched

## Executive decision

The property valued in original Take Two is not another named tool and not generic recursion.

It is representation-coupled endogenous discovery:

messy input
-> observe broadly
-> discover a new distinction/view/relation
-> change the represented problem
-> change the reachable candidate universe
-> reselect what to do
-> execute/verify
-> repeat until relative closure.

The current Take-5 system already contained the pieces separately:
- math-first wrapper;
- question-family quotient/compression;
- representation_discovery runtime;
- Multi-Object higher-order residual mathematics;
- TRC/HF1 reentry;
- canonical continuation quotient.

The missing binding was at closure.  A run could have an unchanged world/result state while a new view or candidate universe had become available, yet the default wrapper reentry rule only inspected admitted state delta.

That permits premature relative closure and loses the original Take Two affordance.

## ICC-128 outer role

Use the earlier ICC-128 shape as the outer controller:

question
-> probe
-> answer
-> admit
-> update
-> regenerate question/representation/candidate state
-> reselect.

Question families are obligations inside one reconstruction problem, not 22 mandatory serial tool calls.

For applicable material family set Q_app:

M* = min_preorder {
  M :
  Recon_J(M,X)
  and Verified_J(M)
  and forall Q_i in Q_app, Resolved_J(Q_i,M)
}.

Scope/mode lattices project obligations and search; they do not become peer questions.

## ICC-123 inner role

ICC-123 / Multi-Object is not the outer controller.

It is an internal residual test whenever multiple objects, relations, scopes, views, or candidate packages interact.

Its protected nucleus remains:

MO_core =
<Pair, Joint, Reconcile, ResidualTest>.

The residual gate prevents the outer controller from compressing away a finding that exists only jointly, under a changed representation, or under a non-reconstructible interaction.

## Discovery state

Let the controller's continuation-relevant discovery state be

D_t =
<Q*_t, V_t, Q_t, C_t, R_t, E_t>,

where:
- Q*_t is the protected continuation quotient state;
- V_t is the active view/representation state;
- Q_t is the live applicable question frontier;
- C_t is the reachable candidate universe/frontier;
- R_t is relation/higher-order residual state;
- E_t is evidence/authority/runtime-reality state.

A material discovery delta can exist even when the world state and protected result are unchanged.

Therefore:

Reenter_t
iff
Delta_world is material
or
Delta_discovery is material.

The wrapper must not interpret an unchanged world-state fingerprint as sufficient closure.

## Relative closure

Relative closure requires all of the following:

1. TRC/verification is closed relative to the declared basis.
2. Protected result is stable.
3. Applicable material question obligations are resolved or explicitly terminal OPEN/BLOCKED where licensed.
4. No new representation/view distinction changes the continuation classes.
5. No new candidate universe element changes the reachable nondominated continuation frontier.
6. ICC-123 residual testing finds no unresolved reconstruction-resistant interaction requiring another route.
7. Evidence/authority/runtime changes expose no new licensed continuation.

Compactly:

Closed_J(t)
iff
Verified_J(t)
and ResultStable_J(t)
and DiscoveryStable_J(t)
and QuestionClosed_J(t)
and ResidualClosed_J(t).

All terms are basis-relative.  Finite zero-yield is not global completeness.

## Implementation change

runtime/math_first_wrapper.py now recognizes a closure-carried discovery_delta.

A discovery delta is material when it reports any continuation-relevant change such as:
- view_changed;
- question_frontier_changed;
- candidate_universe_changed;
- relation_changed;
- authority_or_evidence_changed;
- runtime_reality_changed.

Material discovery forces reentry even when:
- admitted world state is unchanged;
- protected result is unchanged;
- a custom state-delta reentry policy would otherwise return false.

This preserves current wrapper behavior when no discovery_delta is supplied.

## Regression witness

tests/test_math_first_wrapper.py adds the protected witness:

same world state
+ same protected result
+ new view
+ new candidate universe
=> REENTER.

Only after a later round reports no discovery delta may the wrapper close relatively.

## Architectural consequence

Do not create a new peer-level Take Two tool.

Treat this as a controller invariant and feedback law shared by the math-first wrapper, question frontier, representation discovery, and Multi-Object residual testing.

Take-2 remains the historical protected behavioral baseline.
Take-5 is the experimental integration surface.
