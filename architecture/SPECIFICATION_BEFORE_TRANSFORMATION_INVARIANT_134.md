# Specification Before Transformation Invariant 134

Date: 2026-09-26
Status: CANDIDATE IMPLEMENTED ON BRANCH / VALIDATION REQUIRED

## Problem

The system can possess strong architecture, persistence, wrappers, admission,
regression tests, and currentness machinery while the object being changed is
still only partially recovered.

That permits a false sequence:

unknown object -> architecture -> implementation -> "improved"

Architecture can preserve or route known semantics.  It cannot manufacture the
missing semantics of an object whose identity or load-bearing coordinates have
not been reconstructed.

## Governing order

For an object o, job J, basis K, and proposed operation tau:

Observe
-> RecoverObject
-> SpecifyRequiredCoordinates
-> Transform
-> Verify
-> Admit.

Recovery is not required to be globally complete.  It is required to be complete
relative to the proposed transformation.

## Job-relative adequacy

Let Req_(J,K)(o,tau) be the coordinates on which the protected result of tau can
depend.

Let Res_K(o) be recovered coordinates and Inv_(J,K)(o,tau) the unresolved
coordinates accompanied by an admitted invariance witness showing that varying
the coordinate cannot alter the protected result.

Then:

SpecAdequate_(J,K)(o,tau)

iff

1. o is IDENTIFIED, or all surviving object hypotheses are transform-invariant
   for tau;
2. Req_(J,K)(o,tau) is explicit and nonempty for a material transformation;
3. Req_(J,K)(o,tau) subseteq Res_K(o) union Inv_(J,K)(o,tau);
4. no required coordinate is simultaneously asserted RESOLVED and OPEN without
   an admitted reconciliation;
5. the basis is explicit.

Therefore:

TransformLicensed_(J,K)(o,tau)
iff
SpecAdequate_(J,K)(o,tau).

An unresolved coordinate is not automatically fatal.  It is fatal exactly when
the transformation can depend on it and no invariance witness closes that
dependency.

## Legal unresolved work

OBSERVE, DISCOVER, RECOVER, OBJECTIFY, FORMALIZE, COMPARE, AUDIT, VERIFY,
DIAGNOSE, and RECONSTRUCT may operate while the object remains OPEN.

ARCHITECT, BUILD, MODIFY, TRANSFORM, IMPROVE, REPLACE, PROMOTE, SUPERSEDE,
MIGRATE, and transformative integration/execution are gated.

Thus OPEN does not halt inquiry.  It changes the legal action frontier to
recovery work.

## ImprovementCore placement

The selected-work boundary is fail closed.

A selected action/tool must either:

- declare a recovery-class operation; or
- declare a transformation-class operation and carry a passing object
  specification packet.

A selected object-transforming action with no operation class is OPEN rather
than being silently treated as safe.

Strict-gain claims about METHOD, INTERACTION, REDUCTION, ACTIVATION,
HOST_BOUNDARY, or CONTROLLER also require a PASS specification receipt.

This prevents execution or architectural churn from becoming evidence that an
unknown device was improved.

## Emergent objects

A new load-bearing object may be admitted as OPEN evidence before its full
specification is recovered.

It may not be admitted as a governing transformation, replacement, or executable
successor until the same specification gate passes.

Package existence is not specification adequacy.

## Take-6

Tool/object capsules and promotion events inherit this invariant.

Take-6 promotion requires:

SpecAdequate(predecessor)
and
SpecAdequate(successor)
and
protected-behavior preservation
and
required validation
and
consequence closure.

Immutable evidence prevents semantic disappearance.  It does not by itself prove
that the semantic object being promoted has been reconstructed.

## Regression class closed by this invariant

The following formerly separable failures are one family:

- named tool with unrecovered mathematics;
- wrapper around an unrecovered native object;
- architecture designed around a label rather than a recovered device;
- successor promotion before predecessor identity is reconstructed;
- semantic package mistaken for solved semantics;
- persistence preserving a compressed or partial object exactly;
- repeated improvement passes optimizing a representation whose protected
  behavior is not known.

The gate converts each from silent progress into explicit OPEN/RECOVERY work.
