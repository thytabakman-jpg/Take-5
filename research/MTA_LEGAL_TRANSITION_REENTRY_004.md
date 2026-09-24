# MTA Reentry — LEGAL_K Transition Law 004

Date: 2026-09-24
Status: EXECUTED REENTRY / FURTHER REDUCTION
Predecessor: MTA_SEMANTIC_GOVERNANCE_EXHAUSTIVE_SWEEP_003.md

## Frozen job

Attack the reconstructed candidate LEGAL_K and determine whether it is genuinely new mathematics, a decomposition of existing C/U/K, or a representation of an already required transition condition.

## Candidate attacked

LEGAL_K(s,p,c)
=
Typed_K(p,c)
AND Adequate_K(s,p,c)
AND AuthorityLegal_K(s,p,c)
AND PreservationSatisfied_K(s,p,c).

Authoritative U_K is defined only when LEGAL_K=PASS.

## Attack 1 — Is LEGAL a new role?

Existing eight-role system:
T=<K,S,O,G,M,C,R,U>.

C already owns admission/evaluation/governance.
U already owns legal state transition under K.

Therefore a separate ninth role LEGAL is not currently justified.

Best factorization:

C_K(s,p,c) -> disposition/evaluation.
U_K(s,p,c,C_result) -> state transition.

The invariant is:

AuthoritativeEffect(U_K(...))
=> C_result licenses that exact effect under K.

Thus LEGAL_K can be a named predicate compiled from K and C and enforced as U's domain restriction.

Result:
NO ninth role admitted.

## Attack 2 — Can c be eliminated?

C may generate/evaluate from raw results and evidence. A distinct witness object c is useful for provenance, replay, audit and distributed execution, but pure extensional mathematics could fold it into C's inputs/state.

However removing c loses an explicit carrier for grounds/authority/OPEN/verification obligations across episodes.

Conclusion:
witness is not proven primitive role, but is a protected information carrier in persistent/distributed implementations.

Status:
ROLE_NOT_PRIMITIVE / CARRIER_LOAD_BEARING.

## Attack 3 — Four conjuncts

Typed, Adequate, AuthorityLegal, PreservationSatisfied are not proven independent.

Typing can be part of adequacy.
Authority can be a preservation/governance contract.
Preservation can be one family of adequacy obligations.

Smallest semantic statement is therefore:

Admissible_K(s,p,c,effect)=PASS.

But overcompression hides the exact distinctions whose collapse caused historical failures.

MTA disposition:
keep the four-family decomposition as an audit basis, not claim primitive minimality.

## Attack 4 — PASS requirement

Some systems permit speculative, reversible, sandboxed state.

Therefore the invariant must index the effect class.

An OPEN proposal may enter NONAUTHORITATIVE candidate/evidence state while remaining unable to change authoritative governing coordinates.

Define state regions/labels rather than one undifferentiated state.

Candidate:
S = <S_auth,S_candidate,S_evidence,S_open,...> modulo existing state-family model.

Then:
write to S_auth requires admissible effect;
write to candidate/evidence/open regions has weaker contracts but still provenance/type constraints.

This resolves the earlier tension where OPEN must persist without governing.

## Attack 5 — Semantic delta trigger

If every authoritative proposed effect must pass C/U legality, the kernel invariant does not need perfect prior detection of "semantic delta."

Detection is needed to route analysis and compile obligations, but the authoritative write boundary can require explicit proposal/effect typing for every authoritative update.

This is stronger architecturally:
do not depend on detecting novelty after the fact;
make authoritative change impossible except through typed proposal.

Semantic-delta detection remains epistemic defense-in-depth for hidden/bypass effects.

## Attack 6 — Highest-ceiling law

The deepest architecture-independent law is now:

No authoritative state effect occurs except through an admitted typed transition under K.

Symbolically:

Effect_auth(s,s')
=>
exists p,c,a [
  a = C_K(s,p,c)
  and Allows_K(a,p,s,s')
  and s' in U_K(s,p,c,a)
].

This uses existing C/U roles and avoids introducing a parallel governance subsystem.

## Attack 7 — Bypass

"No bypass" is not merely security language.

It is closure of authoritative transition semantics:
the set of authoritative reachable states is generated only by admitted U transitions.

Reach_auth(S0)
=
Cl_{U_K | C allows}(S0).

Any state reachable by another authoritative transition path is outside the declared model and constitutes implementation nonconformance.

This is a cleaner mathematical statement.

## Attack 8 — self-modification

Changes to K,C,U or authoritative-state partition are proposals whose effects target governance semantics.

They are admitted by the current K,C,U regime, except genesis.

This remains coherent at the semantic level.

Whether arbitrary self-modification can preserve all invariants is OPEN.

## Attack 9 — relation to "heart"

MTA result:
"heart" cannot yet be identified with a component.

The deepest discovered property is a closure/invariant over authoritative transitions.

A future Kernel PD may realize this as:
- centralized monitor;
- distributed capabilities;
- type-enforced API;
- transactional state machine;
- proof-carrying transition;
- hybrid.

Therefore the heart candidate is currently a LAW, not a MODULE.

## Fixed-point test

This reentry produced material changes:
- LEGAL not a ninth role;
- witness carrier separated from primitive role;
- authoritative vs candidate/evidence state distinction;
- novelty detection demoted from correctness dependency to defense-in-depth;
- no-bypass recast as reachable-state closure;
- heart recast from boundary component to transition law.

Therefore MTA fixed point is still not proven.

But remaining frontier is now sharply localized to:
1 exact authoritative-state/effect semantics;
2 minimal C/U contract;
3 witness carrier requirements;
4 distributed realization;
5 concurrency;
6 genesis;
7 Kernel/Core PD placement.

A further MTA pass is warranted only after one of these is formalized or new evidence is introduced; immediate blind repetition has lower expected yield.

## Verdict

MTA_REENTRY_004 = MATERIAL_YIELD / LOCAL SATURATION FOR CURRENT REPRESENTATION.

Strongest current result:

Authoritative reachable state is closed under K-constrained, C-admitted U transitions.

No separate SGA subsystem, LEGAL role, MTA primitive, novelty primitive, or centralized transition-boundary module is required by the mathematics.

Return this law to architecture design and test its realizations there.
