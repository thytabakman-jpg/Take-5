# MTA + Raise the Ceiling — Authoritative Transition Closure 005

Date: 2026-09-24
Controller: Improvement Core
Status: EXECUTED / MATERIAL SUCCESSOR
Predecessor: MTA_LEGAL_TRANSITION_REENTRY_004
Migration authority: NONE

## Frozen job

Attack the current strongest result

Reach_auth(S0) = Cl_{U_K | C allows}(S0)

then raise its ceiling without adding architecture-specific machinery, and let Improvement Core decide what survives as the handoff to system architecture.

## Part I — MTA

### 1. Representation defect in Reach_auth

Reachability is useful but too extensional. It tells us which authoritative states can exist, but not whether an individual transition is legitimate, why it is legitimate, what evidence supported it, or whether later evidence can invalidate it.

A pure reachable-set representation can collapse:
- provenance;
- transition identity;
- rival paths;
- reversibility;
- post-verification failure;
- concurrency;
- authority consumption;
- OPEN residuals.

Therefore reachable-state closure is a consequence of the deeper object, not the deepest object.

### 2. The deeper object is a typed authoritative transition system

Candidate:

A_K = <S_A, P, W, C_K, U_K, V_K, ->_K>

where:
S_A authoritative state space;
P typed proposals/effects;
W typed witness/evidence/authority carriers;
C_K admission/evaluation relation;
U_K update relation;
V_K post-transition verification/reconciliation relation;
->_K authoritative transition relation induced by C_K and U_K.

Transition:

s --[p,w,a,e]-->_K s'

only when:
a in C_K(s,p,w);
a licenses effect e;
s' in U_K(s,p,w,a,e).

Verification may later append evidence, retract claims, compensate effects, revise state, or open repair obligations through another legal transition.

This preserves transition identity rather than only endpoint reachability.

### 3. C is not necessarily Boolean admission

C should be relational/set-valued:
C_K(s,p,w) subseteq A

because:
- multiple admissible dispositions can remain incomparable;
- authority can be effect-scoped;
- evidence can support partial effects;
- OPEN can coexist with admitted subeffects;
- rival models can license different safe continuations.

Do not force total deterministic admission.

### 4. U must be effect-scoped

A proposal can contain multiple effects.

Admitting one effect must not silently admit all proposal consequences.

Therefore:
a licenses e, not merely p.

This is a major anti-escalation invariant.

Authority and admission are both effect-scoped.

### 5. Witness is temporally indexed

Evidence can age, be superseded, or be invalidated.

Use w_t with provenance/currentness rather than timeless c.

Admission at t does not guarantee validity forever.

Current authoritative state must preserve enough derivation/provenance to determine when a later delta attacks an earlier admission basis.

This connects directly to artifact currentness and supersession.

### 6. Verification creates transitions, not exceptions

Post-transition verification failure must not mutate state outside the same law.

Rollback, compensation, retraction, invalidation and repair are themselves proposals/effects passing through C/U.

Thus there is no privileged "repair escape hatch."

### 7. Concurrency exposes order

For p1,p2:
U(U(s,p1),p2) need not equal U(U(s,p2),p1).

Therefore concurrency requires:
- commutation proof/evidence;
- serialization;
- conflict;
- merge/reconciliation;
- or OPEN/BLOCKED.

Multi-Object/order analysis becomes a conditional witness obligation.

### 8. Genesis

Genesis is not a normal transition because no prior admitted state exists.

Represent separately:
Gamma -> (K0,S0,A0,W0)

with explicit provenance and external/stipulated authority.

After genesis, all authoritative evolution is internal to ->_K unless an explicitly modeled external authority changes the governance domain.

### 9. MTA verdict

The prior closure equation is retained as a theorem-like projection:

Reach_auth(S0) = states reachable by finite legal paths in A_K.

But the transition system is more informative and has a higher ceiling.

Material delta: PASS.

## Part II — Raise the Ceiling

### Ceiling challenge 1 — Do not require centralized enforcement

The law must support:
- central reference monitor;
- distributed capability system;
- typed APIs;
- append-only event sourcing;
- transactional state machines;
- proof-carrying updates;
- replicated consensus;
- hybrid implementations.

Therefore define conformance behaviorally:

An implementation I conforms iff every externally authoritative effect it realizes corresponds to some legal transition/path in A_K with preserved witness/provenance obligations.

No single physical "heart" is required.

### Ceiling challenge 2 — Separate safety from intelligence

Safety layer:
no unauthorized/unadmitted authoritative effect.

Intelligence layer:
discover better proposals, frames, tools, explanations, models, tests and successors.

The intelligence layer can become arbitrarily capable without receiving implicit authority.

This prevents capability growth from automatically expanding governance power.

### Ceiling challenge 3 — Permit endogenous tool creation

A tool may create:
- new tools;
- new mathematical objects;
- new selectors;
- new representations;
- new candidate architecture;
- new verification methods.

These enter candidate/evidence state.

They acquire authoritative effect only through the same transition relation.

Thus the architecture natively supports the event that triggered this investigation.

### Ceiling challenge 4 — Permit the admission machinery to improve

C_K itself may be proposed for revision.

A revision p_C is evaluated under current governance semantics.

The system can therefore improve its admission machinery without exempting that machinery from governance.

This is bounded reflexivity, not static immutability.

### Ceiling challenge 5 — Preserve plural futures

Do not require every state to have one next state.

A_K may branch.

R chooses/narrows work among legal or candidate continuations but does not erase incomparable alternatives merely to create determinism.

This preserves RIVAL/OPEN and fits nondominated-frontier routing.

### Ceiling challenge 6 — Learn from failed paths

State must preserve enough failure/search memory that reentry does not repeat equivalent failed proposals without material new evidence.

This is HF-001 anti-loop behavior.

It belongs to controller/state design, not the transition-law primitive, but high-ceiling architecture must support it.

### Ceiling challenge 7 — Recursive scale

The same law should apply at multiple scales:
- claim;
- tool;
- subsystem;
- project;
- architecture;
- governance rule.

Avoid separate governance mathematics per scale unless a counterexample requires it.

### Ceiling challenge 8 — External world

Not all effects are internal state writes.

A worker may act on an external environment E.

High-ceiling model must distinguish:
internal authoritative state transition;
external action authorization;
observation;
reconciliation between expected and observed external state.

Candidate extension:
(s,E) --[p,w,a,e]--> (s',E')
with external actions requiring effect-scoped authority and observations returning evidence rather than being silently treated as truth.

Exact external-environment algebra remains OPEN.

### Ceiling challenge 9 — Resource constraints

Legality is not feasibility.

A legal proposal may lack binding, capability, resource or evidence.

Keep:
LEGAL/ADMISSIBLE
distinct from
REALIZABLE
distinct from
EXECUTED
distinct from
VERIFIED.

This preserves the capability-boundary results.

### Ceiling challenge 10 — No universal detector assumption

Endogenous novelty detection improves recall but correctness is protected by typed authoritative-effect paths.

Periodic audits can detect implementation drift/bypass.

Thus the system can improve detectors indefinitely without redefining its basic transition law.

## Part III — Improvement Core decision

### What survives

Carry into architecture design:

1. Authoritative evolution is a typed transition system, not an unrestricted mutable store.
2. Every authoritative effect is effect-scoped and admitted under K.
3. Admission/evidence/authority/execution/verification remain distinct.
4. Candidate/evidence/OPEN state can exist without authoritative force.
5. Tools may create tools and mathematics freely in candidate space.
6. No component self-authorizes its own governing effect.
7. Repairs, rollback, retraction and self-modification use the same transition law.
8. Concurrency/order conflicts are explicit.
9. Provenance/currentness attach to transition witnesses.
10. Reachability closure is a derived projection of legal transition paths.
11. Implementations may be centralized or distributed if behaviorally conformant.
12. Genesis is explicit and separate.
13. External action needs an analogous authority/effect boundary.
14. R/HF-style reentry handles material state change and failed-path memory.
15. Existing K,C,U should be extended/refined before adding a ninth foundational role.

### What does not survive as foundation primitive

Do not freeze:
- "Semantic Governance Admission" as subsystem;
- D/T/A/G as primitive basis;
- LEGAL as ninth role;
- one centralized trusted boundary;
- perfect semantic-delta detector;
- MTA/PD/Multi-Object in kernel;
- one monolithic admission enum;
- one deterministic next state;
- certificate as formal proof;
- Reach_auth equation as the deepest object.

### Smallest current law

Let ->_K be the authoritative transition relation induced by K-constrained C and U.

Then:

AuthoritativeEvolution(S0) = Paths(->_K,S0).

And:

Every edge in ->_K is effect-scoped, authority-legal, preservation-aware, evidence/provenance-carrying, and typed with unresolved obligations rather than silently coercing them to PASS.

This is currently the smallest high-ceiling handoff.

### Architecture-design consequence

Do not begin by drawing modules.

Begin by defining:
- state authority strata;
- proposal/effect type;
- admission relation C;
- update relation U;
- witness/provenance carrier;
- authority semantics;
- verification/reconciliation;
- reentry;
- genesis;
- external-action boundary.

Then derive modules that realize those semantics.

### Remaining OPEN, now nonblocking for architecture design

- exact state-authority stratification;
- minimal witness schema;
- C/U minimality;
- concurrency algebra;
- distributed conformance proof/check;
- external environment/action model;
- genesis authority;
- exact Core/Kernel terminology and placement;
- formal global minimality.

## Final controller verdict

RETURN_TO_ARCHITECTURE_DESIGN = YES.

Reason:
The side problem has yielded an architecture-independent transition law and the remaining uncertainty is best resolved by designing and attacking concrete candidate architectures, not by further isolated repetition.

Next controller action:
resume the larger foundation architecture work using this transition law as a protected constraint, while allowing architecture design itself to generate new candidates through the same candidate/admission discipline.
