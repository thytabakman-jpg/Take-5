# Specification Before Transformation Invariant 134

Date: 2026-09-26
Status: CURRENT VALIDATED / ENFORCED

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
HOST_BOUNDARY, or CONTROLLER require a PASS specification receipt when the
claimed gain is itself a transformation of the object. Ordinary diagnostic,
discovery, verification, or controller-state progress does not inherit a fake
object-transformation obligation.

This prevents execution or architectural churn from becoming evidence that an
unknown device was improved without blocking the work needed to recover it.

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


## Validation and promotion

Promoted through PR #140.

Validation basis on the final PR head:
- Take-5 Validation 36291341026: SUCCESS
- Capability Preservation 36291341035: SUCCESS
- ImproveCore Legacy Restoration 130 run 36291341021: SUCCESS

Merge:
14026b20c06fedee2fc9b3caa3e8826a08e93e01

The first validation pass exposed an over-broad implementation that gated every
controller progress event. The corrected implementation gates only actual
object-transforming claims and permits intrinsically epistemic/recovery work on
OPEN objects. The final validation basis includes that correction.


## Complementary authoritative-emission gate

This invariant governs whether an object may be transformed. It does not make
every legal reconstruction authoritative.

The separate invariant in:

architecture/AUTHORITY_BEFORE_FORMAL_EMISSION_141.md

governs promotion of a reconstruction to a CURRENT/CANONICAL/EXACT_CURRENT
formal claim.

Therefore:

RecoveryLicensed(o) does not imply AuthoritativeEmissionLicensed(o).

Object-transforming work crosses this specification gate before transformation.
Authoritative formal output crosses the formal-claim admission gate before green
emission and parent return.


## Pre-execution effect boundary — current validated extension

The original invariant typed the semantic operation but did not independently type
the effect authority of higher-order callbacks.

That distinction is now explicit.

For selected work w:

OpLicensed(w)
iff
Recovery(Op(w))
or
(Transform(Op(w)) and SpecAdequate(w)).

EffectLicensed(w)
iff
Effect(w)=EVIDENCE_ONLY
or
(Effect(w)=TARGET_TRANSFORM and Transform(Op(w))).

ExecLicensed(w)
iff
OpLicensed(w) and EffectLicensed(w).

Generic/higher-order callbacks with an unknown effect class fail OPEN before
invocation. Repository configured-tool execution may infer EVIDENCE_ONLY only
because its current global contract is observer-only.

This extension is implemented on current main at:
- runtime/specification_before_transformation.py
- runtime/improvement_core_recursive_manager.py
- runtime/improvement_core_legacy_candidate.py

The immutable ICC128 Legacy snapshot is not modified. Its modern wrapper constrains
the admissible executor binding before invoking the frozen E stage.

Promotion evidence:
- PR #146
- final head d3d0a19293b1f9e21aee2cb2147d9476c256587b
- merge 42d933cfbbfb9ffff942f220246df900824d3d01
- Take-5 Validation 36293609614 SUCCESS
- Capability Preservation 36293609616 SUCCESS
- ImproveCore Legacy Holdouts 131 run 36293609695 SUCCESS

The validated repository-governed disposition is CLOSED_RELATIVE. External hosts or
new executor surfaces that do not enter these governed paths remain outside this
claim and reopen the relevant boundary when they become addressable.
