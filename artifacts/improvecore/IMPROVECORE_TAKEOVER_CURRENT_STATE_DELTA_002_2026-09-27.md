# ImproveCore Takeover Current-State Delta 002

Date: 2026-09-27
Parent: artifacts/improvecore/IMPROVECORE_TAKEOVER_CURRENT_STATE_DELTA_001_2026-09-27.md
Status: QUESTION-FAMILY SEMANTICS RECOVERED / BASIS-RELATIVE / GLOBAL MINIMALITY OPEN

## Material correction

The preceding takeover delta left the exact semantics/provenance of Q01-Q22 red.

That status is superseded on the current recovered basis.

Authoritative current-basis sources:
- research/QUESTION_SEARCH_MATH_001.md
- research/QUESTION_SEARCH_RUN_001.yaml
- architecture/QUESTION_TOOL_RENAME_REGISTRY_001.yaml
- research/ICC_ONE_EQUATION_QUESTION_COMPRESSION_003.md

The 22 families are a basis-relative fixed point over the recovered universe. They are not a theorem of globally exhaustive or globally minimal inquiry structure.

## Atomic question object

q = <Issue, Target, AnswerSpace, Presuppositions, ResolutionCondition, ProtectedResult>

Scope/mode projections are normalized before declaring distinct question identity.

L36 = Scope6 x ModeFace6

q_l = q o pi_l

Projection-only differences remain in the same family when Issue, AnswerSpace, protected continuation, and ResolutionCondition are preserved.

## Current Q01-Q22 basis

Q01 Basic Math
Question: What is the smallest adequate mathematical model or reconstruction of this object?
Math: BM(X)=Min_preorder{m in M_B(X) : Recon_J(m,X) and Preserve_J(m)}

Q02 Change Math
Question: What changes under an admissible transformation, representation, view, or mode?
Math: CM(X)={(phi,delta) : phi in Phi_B(X), delta=Delta_J(X,phi(X)), delta != 0}

Q03 Difference Math
Question: Which admissible differences actually change the protected result?
Math: DM(X)={d in D_B(X) : Out_J(X) !~_J Out_J(phi_d(X))}

Q04 Together Math
Question: What appears only when these objects are considered together?
Math: TM(S)=F_J(S) \ Cl_J,B(union_{P proper_subset S} F_J(P))

Q05 Structure Math
Question: What organization, roles, interfaces, dependencies, and obligations constitute this system?
Math: SM(X)={a in Struct_B(X) : Recon_K(a,X) and Preserve_K(a) and Obligations_K(a) are typed}

Q06 Cause Math
Question: Which live mechanism or causal/root relation explains the observed contrast?
Math: Cause(X)={h in H_B(X) : Compatible(h,E) and Causal_J(h) and RootCriterion_J(h)}

Q07 Better Math
Question: What strictly better same-job version exists while preserving protected behavior?
Math: Better(X)=ND{y : SameJob_J(y,X) and Preserve_J(y) and y >_J X}

Q08 Transfer Math
Question: What licensed consequence carries from this source to this target?
Math: Transfer(s,t)={r : Relation(s,t,r) and License(r) and MaterialEffect_t(r)}

Q09 Trace Math
Question: What dependency, contribution, provenance, or evidentiary path grounds this result?
Math: Trace(x)={p in Paths_B(x) : Licensed(p) and ProvenanceValid(p)}

Q10 Reality Check
Question: Does the claimed object, run, state, or artifact actually exist and correspond to the claim?
Math: Reality(o)=Identity(o) and Exists(o) and Connected(o) and EvidenceAdequate(o)

Q11 Grounding Check
Question: What required state is missing, and what represented state lacks valid grounding?
Math: Ground(G)=Orphan_J(G) union Ghost_J(G) union GroundingConflict_J(G)

Q12 Current Check
Question: Which representation/version/basis is current and authoritative now?
Math: Current(x) iff Delta_J(BuiltBasis(x),LatestAdmittedBasis(x))=empty and AuthorityCurrent(x)

Q13 Type Check
Question: What admissible type does this task or object have?
Math: Type(x)={tau in Types_B(x) : Admissible_J(tau,x)}

Q14 Identity Check
Question: Are these references the same continuing object or different referents?
Math: Identity(x,y)=EqReferent_J(x,y) in {SAME,DISTINCT,OPEN}

Q15 Dependency Math
Question: What material dependencies or affected paths bear on this result?
Math: Dep_J(x)={(u,v) : intervention_on(u) changes protected continuation at v}

Q16 Relation Math
Question: What typed relation holds among these objects?
Math: Rel(X)={r in R_B(X) : LicensedRelation_J(r,X)}

Q17 Novelty Check
Question: What is genuinely new, uncovered, or omitted relative to the represented frontier?
Math: Novel(X)=Candidate_J(X) \ Cl_J(KnownFrontier)

Q18 Verify Math
Question: Which claims or candidates survive the required attacks and preservation tests?
Math: Verify(C)={c in C : Evidence(c) and Preserve_J(c) and RequiredTests_J(c)=PASS}

Q19 Completion Check
Question: What material unresolved coordinate remains before the declared claim is complete?
Math: Done_J iff LiveMaterial_J=empty and ConsequencesClosed and RequiredVerificationTerminal

Q20 Goal Math
Question: What governing goal is actually supported by the available control evidence?
Math: Goal(E)=ND{g : Grounded(g,E) and AuthorityTyped(g) and DeterminateEnough_J(g)}

Q21 Ownership Check
Question: What is licensed to govern, own, execute, or verify this obligation?
Math: Owner(w)={r : Capable(r,w) and Authorized(r,w) and ScopeCompatible(r,w)}

Q22 Discovery Math
Question: What material question, dependency, object, or relevant region remains undiscovered?
Math: Discover(S)=Frontier_B(S) \ Cl_J(KnownMaterial(S))

## One-equation compression

Let Q_22={Q_1,...,Q_22}.

Closed^22_{J,B}(M)
iff
for every i in {1,...,22}, Resolved_J(Q_i,M).

Then the current compression target is:

M*_{22}(X|J,B)
=
min_preorder {
  M in M_B(X)
  :
  Recon_J(M,X)
  and Verified_J(M)
  and Closed^22_{J,B}(M)
}.

The 22 are obligations inside one reconstruction problem, not 22 mandatory serial top-level tool calls.

## Relation to D36_C

For l in L36:

Resolved_J(Q_i o pi_l,M)

enters closure only when that projection is applicable/result-sensitive.

Therefore 36 changes the obligation surface. It does not multiply the outer reconstruction problem into 36 independent executions.

## Currentness result

Promote on current basis:
- Q01-Q22 family identities: RECOVERED
- family questions: RECOVERED
- family candidate math: RECOVERED
- current name/alias map: RECOVERED
- 36-projection normalization rule: RECOVERED
- basis-relative fixed point: RECOVERED

Remain OPEN:
- global completeness of all possible question families
- global minimality of the 22-family basis
- unknown history outside the recovered corpus
- unrestricted proof that no later recovered artifact splits/merges a family

## Next selected frontier

Strong tool reality remains repository-owned and OPEN.

Current native entrypoint residual:
MTA, Architecture, PD, PDAudit, GDOS, Discriminator, RTC, BiasPerturbation, MultiObject, Diagnosis, GOAL.

Current manifest identity is also generic-only for most registered tools.

ImprovementCore will not close these by assigning aliases or routing them through generic prose. Native realization and explicit protected-behavior identity must be recovered together.

## Terminal

QUESTION-FAMILY SEMANTIC RECOVERY: CLOSED_RELATIVE

STRONG WHOLE-PORTFOLIO TOOL REALITY: OPEN

UNIVERSAL EXTERNAL-HOST INTERCEPTION: EXTERNAL_NOT_OWNED
