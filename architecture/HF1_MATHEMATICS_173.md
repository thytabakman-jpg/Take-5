# HF1 Mathematics 173 — Fresh Discovery Closure

Date: 2026-09-27
Status: REPAIR CANDIDATE
Supersedes for current closure semantics: architecture/HF1_MATHEMATICS_084.md

## Recovered defect

HF1 Mathematics 084 correctly typed world, discovery and result-sensitive deltas,
but delegated construction of those signatures upstream.

The corresponding runtime then accepted:

Omega(packet) = empty

as sufficient for immediate relative closure.

That is weaker than the recovered historical HF1 contract, where frontier
generation/admission and result/search delta discovery were part of the recursive
continuation behavior.

Therefore:

caller_frontier_empty
does not imply
fresh_frontier_empty.

## Current object

HF1 remains the governed episode-level continuation/reentry operator.

It is not HF2.
It is not TRC.
It is not ImprovementCore.

Let X be the typed packet space with signatures:

w(x) = world_state
d(x) = discovery_state
r(x) = result_sensitive_state.

Let Fresh_J,K(x) be the host-bound fresh whole-continuation observation operator.
Fresh must rebuild continuation-relevant obligations/questions from normalized
current state rather than inherit only the prior selected local frontier.

## Inner governed round

For live obligations:

x_t
-> K_PD(x_t)
-> O_t
-> P*_t
-> m_t
-> Exec
-> C_TR
-> x'_(t+1).

As before:

P*_t in argmin_P (sum c_i, |P|, lexical(P))

subject to package cover of every live obligation.

## Typed delta

Delta_W iff w(x) differs.
Delta_D iff d(x) differs.
Delta_R iff r(x) differs.

Unknown/missing signatures fail OPEN.

## Fresh closure challenge

Before every candidate RELATIVE_CLOSE:

f_t = Fresh_J,K(x_t).

Require f_t to be a typed packet.

Compute:

DeltaFresh
=
<Delta_W(x_t,f_t),Delta_D(x_t,f_t),Delta_R(x_t,f_t)>.

A changed full packet with no typed signature delta is:

OPEN(FRESH_REOBSERVATION_UNTYPED_DELTA).

This prevents a newly generated question/work item from appearing outside the
declared discovery/result-sensitive state.

## Reentry

rho(Delta_W,Delta_D,Delta_R) =

REENTER_OBSERVE when Delta_W or Delta_D
REVERIFY when only Delta_R
NO_REENTRY otherwise.

Fresh observation follows the same law.

Any typed fresh change reenters another HF1 round even when the refreshed packet
currently has no explicit obligation.  A second fresh pass must establish
stability on the changed basis.

## Relative closure

HF1 returns RELATIVE_CLOSE only when:

1. current TRC state is closed or no tool run was required;
2. current K_PD obligations are empty;
3. Fresh_J,K is available;
4. Fresh_J,K(x)=x on the typed W/D/R closure coordinates and exposes no new live
   obligation;
5. required reverification succeeded;
6. no result-sensitive OPEN/BLOCKED/CONFLICT coordinate is hidden by the packet.

Thus:

InheritedEmptyFrontier != Closure.

FreshStableEmptyFrontier = required closure evidence.

## Fail closed

HF1 returns OPEN for:

- FRESH_REOBSERVATION_REQUIRED;
- FRESH_REOBSERVATION_INVALID;
- FRESH_REOBSERVATION_UNTYPED_DELTA;
- missing delta signatures;
- missing/failed reverification;
- live obligation with no progress;
- resource bound.

## Relation to HF2 and parent stability

HF2 owns same-capability local recurrence.

HF1 owns episode-level fresh continuation closure and earliest upstream reentry.

ImprovementCore parent completion additionally uses
runtime/whole_job_stability.py to require repeated fresh no-delta challenge passes
before user-visible COMPLETE.

These are different scales of recurrence.

## Runtime

runtime/hf1_episode.py

Regression:

tests/test_hf1_episode.py
tests/test_whole_job_stability.py
tests/test_improvement_core_return_gate.py

## Nonclaim

Fresh_J,K is environment/semantic-provider bound.

This contract does not prove global completeness of every possible discovery
generator or unbounded termination.

It closes the concrete regression where an inherited empty frontier was accepted
without a fresh whole-state discovery pass.
