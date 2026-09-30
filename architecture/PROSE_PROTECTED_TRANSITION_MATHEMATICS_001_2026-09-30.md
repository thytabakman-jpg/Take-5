# PROSE Protected Transition Mathematics 001

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Origin: RootCause HF2 on the Canonical Authority affirmative-first regression
Controller: ImprovementCore
Candidate tool: Prose

## Failure class

A protected reader-facing prose constraint can exist in project control state while a prose mutation violates it and later architecture, solution, verification, recurrence, and emission stages still accept the successor.

Observed example:

- protected rule: state the affirmative claim first;
- pre-mutation prose: "Ramban directly attacks...";
- regressed prose: "Ramban does not merely offer a different emphasis. He directly attacks...";
- the rule existed before the mutation;
- later review failed to reject the violation.

The RootCause result identifies the smallest stable generator as:

[
G_{prose}
=
	exttt{PROTECTED_BASIS_DROPPED_AT_PROSE_MUTATION_BOUNDARY}.
]

## Mathematical object

Let:

- (s) be the pre-mutation semantic/prose state;
- (p) be a candidate successor prose realization;
- (K_p) be the frozen protected prose contract;
- (O_s) be the semantic obligations that must survive;
- (E) be typed evidence/receipts;
- (V_{K_p}(p)) be the set of prose-contract violations;
- (SemPres(O_s,p,E)) mean the successor preserves the required semantic commitments with evidence;
- (StrengthPres(O_s,p,E)) mean no earned claim was silently weakened;
- (NoInflation(O_s,p,E)) mean no unsupported strengthening was introduced.

Define prose admissibility:

[
oxed{
ProseAdmissible_{K_p}(s,p,E)
iff
V_{K_p}(p)=arnothing
land
SemPres(O_s,p,E)
land
StrengthPres(O_s,p,E)
land
NoInflation(O_s,p,E)
}
]

A prose mutation is admitted only when the predicate is true.

Surface compliance alone is insufficient.
Semantic preservation alone is insufficient.

## Affirmative-first constraint

For the current regression class, define protected constraint (AF).

Let (R(p)) be the set of rhetorical negative-first contrast frames in (p), including:

- "not merely X; Y";
- "not X, but Y";
- "not X; rather Y";
- "does not X. It Y";
- equivalent forms where the reader must process a rejected frame before the affirmative claim.

Let (L(p)) be the subset whose negation is itself load-bearing logical content.

Then:

[
AF(p)
iff
R(p)setminus L(p)=arnothing.
]

Thus negation remains permitted when it is the proposition under analysis, e.g. a branch stating that a tradition does not guarantee correctness.

## Protected transition coordinates

A protected prose constraint is not preserved merely because it exists in a style file.

For each prose constraint (kin K_p), define:

[
PTP(k)
=
langle
capture,
architecture,
realization,
verification,
reentry,
emission
angle.
]

Each coordinate must be witnessed:

1. capture — constraint is present in the frozen basis;
2. architecture — successor design explicitly preserves the constraint;
3. realization — prose-mutating candidate declares and realizes preservation;
4. verification — successor is audited against the constraint;
5. reentry — a violation prevents closure and triggers re-entry;
6. emission — final reader-facing text is accepted only after the constraint passes.

Define:

[
ProtectedProseTransition(k)=VERIFIED
iff
orall cin PTP(k), Witness(c,k)
eqarnothing.
]

Missing witness gives OPEN.
Blocked witness gives BLOCKED.
A local semantic success cannot override an OPEN/BLOCKED prose transition.

## Layer responsibilities

### GOAL

GOAL owns desired substantive outcome and explicit constraints.
GOAL does not generate prose and is not the primary mutation owner.

When a protected prose constraint is in the basis, GOAL must preserve it as a constraint rather than fold it into the target claim.

### ARCHITECT

ARCHITECT owns reader/order/structural realization constraints when those constraints are marked protected.

For prose-changing work:

[
ArchitectureAccept(A,K_p)
iff
orall kin K_p, PreservedByDesign(A,k).
]

A successor frontier missing a protected prose constraint is OPEN, not admissible architecture.

### SOLUTION

SOLUTION owns intervention realization.

Let (P_{req}=P_{domain}cup K_p).

A candidate is relevant only when it proposes preservation of every (kin P_{req}).
A solution is SOLVED only when an external receipt verifies those preservations.

### PROSE

PROSE is a distinct tool because it owns a result-sensitive object not owned by ARCHITECT or SOLUTION:

> candidate reader-facing prose under a frozen prose contract.

Native job:

[
PROSE:(s,p,K_p,O_s,E)
	o
{PASS,REPAIR_REQUIRED,OPEN,BLOCKED}
	imes Violations
	imes Receipts.
]

PROSE does not decide factual truth, source validity, or paper architecture.
It does not silently rewrite unsupported content.
It audits protected prose realization and can emit repair obligations.

### VERIFY

Any successor-state verifier for prose-changing work must require a PASS PROSE receipt.
Semantic correctness without prose-contract compliance is insufficient for COMPLETE.

### ImprovementCore

ImprovementCore owns cross-capability admission.

For prose mutation work:

[
IC_Admit(p)
Rightarrow
ProseAdmissible_{K_p}(s,p,E).
]

A missing PROSE receipt is owned work remaining, not completion.

### HF2

HF2 re-applies the same capability after a material repair.
If PROSE returns REPAIR_REQUIRED, local closure is false.
Only a successor with no material prose violations can reach relative close.

### Emission

Final reader-visible prose inherits the same contract.
Emission is blocked when the required PROSE receipt is absent or non-PASS.

## Tool-admission test

A new tool is admitted only when it adds a result-sensitive capability not already owned at lower cost.

ARCHITECT answers:
- what structure/design satisfies the goal and protected constraints?

SOLUTION answers:
- what intervention solves the diagnosed problem and preserves required objects?

PROSE answers:
- does this concrete reader-facing realization preserve the frozen prose contract without semantic weakening or inflation?

The last question is independent and result-sensitive. The observed failure demonstrates that ARCHITECT + SOLUTION + VERIFY without a prose-specific acceptance object can admit a bad successor.

Therefore PROSE is admitted as a distinct configured tool.

## Default protected prose constraints

The tool is generic and project contracts choose which constraints are active.

Initial supported protected constraint:

- AFFIRMATIVE_FIRST

The architecture is extensible to additional explicit constraints such as:

- EARNED_CLAIM_STRENGTH;
- NO_UNSUPPORTED_INFLATION;
- TERMINOLOGY_LOCK;
- READER_ORDER_LOCK;
- FORBIDDEN_RHETORICAL_FRAME.

No new constraint is silently inferred from user preference; it must enter the frozen prose contract.

## Fail-closed rule

For prose-changing work:

[
MissingProseContractWitness
Rightarrow
OPEN.
]

[
Violation(PROSE)
Rightarrow
REPAIR_REQUIRED.
]

[
PASS(PROSE)
land
SemanticReceipt=PASS
Rightarrow
eligible for successor acceptance.
]

## Scope of enforcement

This repair governs repository-aware Take-5 execution and project workflows that bind to this contract.

Universal enforcement over an unrelated host that never loads Take-5 remains OPEN.

## Required implementation witnesses

Implementation is not complete until all exist:

- runtime/prose.py;
- tests/test_prose.py;
- Architecture protected-constraint enforcement;
- SolutionToMyProblem protected-prose preservation enforcement;
- ImprovementCore parent-return prose receipt gate;
- global emission/protected-transition integration;
- tool manifest identity for Prose;
- configured-run registration for Prose;
- current tool package with 36 Scope x ModeFace evidence pages;
- regression fixture reproducing the exact "does not merely ... directly ..." failure;
- portfolio/current-tool audits remain closed.

## Mutation rule

This document is the frozen math-first basis.

No implementation change for this repair is admitted before this mathematical object exists.
