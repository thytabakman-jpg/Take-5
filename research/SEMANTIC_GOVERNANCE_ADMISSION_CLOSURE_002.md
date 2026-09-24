# Semantic Governance Admission — Closure 002

Date: 2026-09-24
Controller: Improvement Core
Status: BASIS-RELATIVE CLOSURE FOR ARCHITECTURE DESIGN
Scope: nonproduction Take-5 research
Migration authority: NONE

## 1 Frozen job

Find the smallest architecture-independent mathematics that prevents a reasoning/build system from silently changing its governing semantics, while allowing arbitrary future discovery tools and implementations.

This closes the side investigation enough to return to architecture design. It does not claim a global theorem.

## 2 Reduction

The earlier factorization SGA=<D,T,A,G> is useful operationally but is not the smallest mathematical basis.

D,T,A are ways to construct a transition certificate.
G is enforcement.

The smaller object is a certified transition relation.

Let S be admitted governing state.
Let r be a proposed result/change.
Let delta = Delta_H(S,r) be the semantic delta relative to continuation/equivalence basis H.
Let cert(delta) carry the information required to license the exact effect.

Define:

S --delta,cert--> S'

is legal iff

Effect(S,S',delta)
AND Adequate_H(cert,delta,Effect)
AND AuthorityLegal(cert,Effect)
AND Preserve_P(S,S',cert)

with unresolved material obligations represented OPEN/BLOCKED/RIVAL rather than silently erased.

The primitive protection is therefore not a named tool. It is a restriction on admissible state transitions.

## 3 Smallest formula

Candidate minimum:

LEGAL_H,P(S -> S')
iff
exists delta,c [
  Delta_H(S,S')=delta
  and Licenses_H,P(c,delta,S,S')
].

Where Licenses expands only as needed into:
- typed identity/scope of delta;
- disposition/admission for the exact governing effect;
- legal authority;
- protected-invariant obligations;
- explicit unresolved residuals.

Equivalent safety statement:

GoverningDelta_H(S,S') != empty
implies
Certificate_H,P(S,S') != absent.

No certificate means no legal governing transition.

This is the smallest current formula. D/T/A/G are an implementation/refinement of Certificate production and enforcement.

## 4 What is actually fundamental

Fundamental:
1 admitted governing state S;
2 semantic difference/delta relation Delta_H;
3 legal-transition predicate LEGAL;
4 transition certificate/grounds C;
5 protected obligations P;
6 authority relation;
7 typed unresolved carrier OPEN/BLOCKED/RIVAL/CONFLICT.

Derived/replaceable:
- MTA;
- PD/PDAudit;
- Multi-Object;
- Diagnosis;
- ARA/CAC;
- RTC/MTOS;
- scanners;
- registries;
- repository implementation;
- specific novelty detector;
- specific type system;
- specific proof language.

These tools improve certificate construction, challenge, verification and reentry. They are not the invariant itself.

## 5 Architecture placement

Do not place a whole discovery tool in the privileged heart.

Architecture-independent decomposition:

A. TRUSTED TRANSITION BOUNDARY
Owns only:
- definition/check of legal governing transition;
- authority check;
- protected invariant check;
- refusal to silently coerce OPEN into PASS.

B. EPISTEMIC CERTIFICATE FACTORY
Replaceable machinery that detects, types, analyzes and challenges semantic deltas.

C. STATE/EVIDENCE STORE
Persists admitted state, candidate deltas, certificates, OPENs, provenance and history.

D. CONTROLLER
Chooses which epistemic machinery to invoke, obtains a certificate, proposes transition, reenters after material delta.

E. RUNTIME/WORKERS
Perform substantive operations but cannot directly mutate admitted governing state.

F. VERIFICATION
Tests certificate claims, preservation, execution truth and downstream consequences.

Thus the privileged heart is a reference-monitor-like transition boundary, not the entire intelligence layer.

## 6 Bypass theorem candidate

For every component x outside the trusted transition boundary:

x may propose arbitrary r,
but x cannot directly perform a governing transition S->S' unless LEGAL(S->S') is satisfied.

This creates tool independence:
future tools can be added/replaced without weakening the invariant.

The architecture fails the design if any alternate write path can mutate governing state without the boundary.

## 7 Delta detection ceiling

Exact semantic delta detection is generally not guaranteed by syntax.

Therefore the architecture must not pretend D is perfect.

Use layered detection:
- explicit object/relation/policy/state changes;
- semantic comparison;
- dependency/consequence triggers;
- anomaly/orphan/ghost checks;
- tool-specific challenges;
- periodic whole-state audits;
- holdouts.

False negatives remain a verification/research risk.

The boundary protects against bypass after a delta is presented; the epistemic layer raises recall of presenting the right deltas.

This distinction prevents an impossible detector from contaminating the minimal invariant.

## 8 Certificate ceiling

A certificate is effect-relative, not globally true.

C must answer:
- what changed?
- what exact effect is requested?
- what grounds support the disposition?
- what protected obligations are affected?
- what authority licenses the effect?
- what remains unresolved?
- what verification is required?

A certificate can be partial/set-valued.

Admission does not imply execution.
Execution does not imply verification.
Verification does not imply promotion.
Promotion does not imply migration.

## 9 Reflexivity

Changes to the transition boundary, certificate schema, semantic-delta basis H, protected set P, or authority semantics are themselves governing deltas.

Therefore they require certificates under the currently admitted boundary.

Bootstrap exception:
an initial trusted basis B0 must be installed exogenously or by a separately authorized genesis procedure.

After bootstrap:
the mechanism governs its own modification.

This is the correct self-application point. The system does not recursively analyze itself forever; it certifies material changes to its own governing rules.

## 10 Relation to Artifact Reality

Artifact Reality is a specialization of the same transition law for persistent load-bearing representations.

When a transition changes persistent canonical state, the certificate must additionally establish:
identity/currentness/authority/reconstructibility/dependency coverage or typed residual.

Therefore CAC/ARA is not a separate privileged heart.
It is a certificate obligation activated by persistence-changing transitions.

## 11 Relation to Orphan/Ghost

Orphan/Ghost are diagnostic certificate challenges:
- Orphan: governing claim/object lacks required forward realization/support.
- Ghost: realized artifact/effect lacks admitted reverse grounding.
- Conflict: incompatible support.
- OPEN: inadequate evidence/coverage.

They feed certificate adequacy; they need not be privileged primitives.

## 12 Relation to MTA/PD/Multi-Object

MTA produces structural/factorization evidence.
PD expands/challenges the frame.
Multi-Object detects reconstruction-resistant interaction residuals.
Diagnosis discriminates causal rivals.
RTC searches same-job strict-gain successors.

All are certificate-producing/challenging services selected by the controller based on the live delta.

This gives the tools a clean common interface:

Tool(delta,S,J,H,P) -> EvidenceDelta + CandidateCertificateDelta + OPEN.

## 13 High-ceiling architecture

The ceiling is not a fixed list of tools.

The architecture admits an unbounded tool ecology provided every tool:
- has typed input/output/effect contracts;
- cannot bypass the transition boundary;
- returns evidence/provenance/OPEN;
- can be challenged/replaced;
- cannot self-authorize broader authority.

This permits future tools to improve semantic-delta detection, certificate quality, search efficiency and verification without changing the core safety law.

## 14 Failure modes and required responses

F1 missed semantic delta
Response: layered detection + periodic audits + consequence checks + holdouts.

F2 false-positive delta
Response: equivalence/reconstruction test; MERGE/NOOP.

F3 wrong typing
Response: PD/MTA/representation challenge.

F4 insufficient evidence
Response: OPEN, acquire evidence or narrow effect.

F5 authority mismatch
Response: BLOCKED for requested effect.

F6 conflicting certificates
Response: RIVAL/CONFLICT; no silent arbitrary collapse.

F7 runtime without semantic binding
Response: not executable as governing transition.

F8 persistent artifact mismatch
Response: ARA/CAC obligation.

F9 self-modification
Response: current boundary certifies proposed boundary change.

F10 boundary bypass
Response: architectural defect; repair before readiness.

## 15 Minimal implementation contract

An architecture implementing this basis needs at least:

1 one authoritative admitted-state write boundary;
2 immutable/provenanced proposal and certificate records;
3 effect-scoped authority grants;
4 typed terminal/disposition carrier;
5 protected invariant checks;
6 OPEN preservation;
7 controller path that cannot write around the boundary;
8 verification receipt;
9 reentry after admitted material change;
10 genesis/bootstrap record.

Everything else may evolve.

## 16 What not to freeze

Do not freeze:
- the name Semantic Governance Admission;
- D/T/A/G as the unique decomposition;
- a universal semantic-delta algorithm;
- a universal certificate schema;
- Kernel=transition boundary as terminology;
- exact Core/Kernel definitions;
- global completeness/minimality.

Freeze only the architectural requirement that governing transitions require effect-adequate, authority-legal, preservation-aware admission evidence and cannot bypass the trusted boundary.

## 17 Architecture-design handoff

When designing the larger architecture, treat this result as a constraint, not as the architecture itself.

Ask:
1 Where is the single admitted-state transition boundary?
2 What state counts as governing?
3 How are proposals/deltas represented?
4 How are certificate obligations compiled?
5 Which tools can discharge each obligation?
6 How is authority scoped?
7 How are OPEN/RIVAL/CONFLICT represented?
8 How are persistent-state obligations added?
9 How is bypass prevented?
10 How does reentry occur after a legal material transition?

## 18 Closure verdict

The side investigation has reached a useful basis-relative closure.

Current strongest result:

The smallest protected object is a certified legal-transition relation over admitted governing state.

The highest-ceiling implementation is a tiny non-bypassable transition boundary plus a replaceable, extensible epistemic tool ecology that constructs and challenges transition certificates.

Remaining OPENs are implementation/research coordinates, not blockers to returning to architecture design:
- exact semantic-equivalence basis;
- detector recall;
- minimal certificate schema;
- concurrency/conflict algebra;
- genesis procedure;
- formal minimality proof;
- external comparison.

Return to the larger architecture project is licensed at research scope.
