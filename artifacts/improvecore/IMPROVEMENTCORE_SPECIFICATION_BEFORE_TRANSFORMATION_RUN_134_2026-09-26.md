# ImprovementCore Run 134 — Specification Before Transformation

Date: 2026-09-26
Branch: fix/specification-before-transformation-134
Base: 16631379c1373d33067b0189a7adc4bfce3cf157
Status: IMPLEMENTED / VALIDATION PENDING

## Evidence

The triggering conversation exposed a foundational contradiction:

- the system had repeatedly strengthened wrappers, architecture, persistence,
  currentness, promotion, and anti-regression machinery;
- several formal devices and ImprovementCore operators still had unrecovered or
  only partially recovered mathematics;
- architecture was therefore capable of preserving or improving a representation
  without proving that the representation fully captured the device being changed.

Existing repository evidence independently contained the pieces of the diagnosis:

- Object Hypothesis Recovery distinguished object identification from downstream
  convenience.
- Full Tool Mathematical Identity required native semantics, wrapper, geometry,
  protected behavior, lineage/currentness/runtime, and RunSpec coordinates.
- Load-Bearing Semantic Object packages explicitly allowed BLACK_BOX_OPEN.
- Emergent Object Admission prohibited new load-bearing prose from silently governing.
- Take-6 protected exact evidence and executable capsule identity.
- ImprovementCore strict-progress mathematics required preservation and causal
  effect witnesses but did not contain an explicit specification adequacy coordinate.

The missing composition was a transformation-license gate.

## Root cause

The old chain permitted:

RecoverSome(o)
-> Package(o)
-> Architect/Build/Improve(o)
-> VerifyKnownCoordinates
-> ImprovementClaim

without a mandatory witness that every coordinate on which the proposed
transformation could depend had been recovered.

Persistence solved semantic disappearance.
It did not solve semantic under-specification.

## Repair

Added the invariant:

SpecAdequate_(J,K)(o,tau)
iff
object identity is identified or tau is invariant across surviving hypotheses,
and every coordinate in Req_(J,K)(o,tau) is recovered or has an admitted
invariance witness.

TransformLicensed_(J,K)(o,tau)
iff
SpecAdequate_(J,K)(o,tau).

Recovery-class work remains legal while OPEN.

Transformation-class work fails closed.

## Enforcement points

1. runtime/specification_before_transformation.py
   - executable job-relative specification gate;
   - explicit recovery versus transformation operation classes;
   - selected-work fail-closed classification;
   - transform-sensitive strict-gain predicate.

2. runtime/ic028_operator.py
   - selected ImprovementCore work crosses SPECIFICATION_GATE after SELECT and
     before BIND/EXECUTE.

3. runtime/improvement_core_progress_relation.py
   - object-transforming strict progress at METHOD, INTERACTION, REDUCTION,
     ACTIVATION, HOST_BOUNDARY, and CONTROLLER targets requires specification
     PASS; ordinary diagnostic/controller progress remains legal.

4. runtime/emergent_admission.py
   - package reality alone cannot admit a governing transformation claim.

5. take6-bootstrap/runtime/promotion.py
   - predecessor and successor specifications must both PASS before promotion.

6. Take-6 architecture, Full Tool Mathematical Identity, Load-Bearing Semantic
   Object Package, and Object Hypothesis Recovery contracts now carry the same law.

## Consequences

The following no longer count as sufficient grounds for transformation:

- a tool name;
- a durable semantic package;
- a wrapper;
- a runtime implementation;
- exact persistence;
- a newer architecture;
- a successful test on known coordinates;
- a candidate successor;
- an ImprovementCore effect witness.

The system can continue learning while an object is OPEN, but its legal work
frontier contracts to recovery/observation/formalization/verification until the
transformation-relevant specification is adequate.

## Validation target

The branch is not current authority until CI passes and the pull request is
merged. No current pointer is changed by this artifact alone.

Remaining external boundary after repository validation:
universal enforcement in a ChatGPT host that does not execute this repository
runtime remains outside repository authority.


## Validation correction

The first Take-5 validation run exposed an over-broad first implementation:
all CONTROLLER strict-progress transitions were initially forced through the
specification gate, including ordinary recursive diagnostic progress.

That was not the governing invariant. The repaired implementation indexes the
gate by an explicit transformation claim. This preserves the distinction:

diagnose/recover unknown object = legal;

claim to architect/build/modify/improve/replace/promote unknown object = OPEN.

Current intrinsically epistemic configured tools may infer a recovery-class
operation only where that inference cannot license a mutation. Other configured
tools remain fail-closed until the selected work supplies its operation class.
