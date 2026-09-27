# Authority Before Formal Emission Invariant 141

Date: 2026-09-26
Status: CURRENT / IMPLEMENTED / VALIDATED / PROMOTED
Canonical repository: thytabakman-jpg/Take-5

## Problem

Two recent failures expose one deeper class.

1. A formal device can be reconstructed, architected, or improved while its exact
current identity is still unrecovered.

2. A mathematically coherent reconstruction can be emitted as the CURRENT,
CANONICAL, or EXACT_CURRENT mathematics even when its ingredients come from
different authority/currentness layers or the composition does not type-check.

The earlier Specification-Before-Transformation invariant closes the first
failure for object-changing work. It intentionally permits recovery-class work,
including RECONSTRUCT and FORMALIZE, on OPEN objects.

That is correct, but incomplete.

Recovery legality does not imply authoritative-emission legality.

The missing boundary was:

reconstruction
-> authoritative claim admission
-> green/current emission.

Without that boundary, a stale or mixed-era reconstruction can survive recovery
and coloring checks when every locally named coordinate looks recovered.

## Failure class

Name:

FORMAL_AUTHORITY_COLLAPSE.

Characteristic invalid implications:

RecoveredMath(o)
=> CurrentMath(o).

Named(o)
and LocallyTyped(o)
=> CurrentIdentity(o).

Current(root)
and Historical(dep)
=> CurrentComposition(root,dep).

Recovered(left)
and Recovered(right)
=> TypeCorrect(left op right).

None of those implications is valid without additional evidence.

## Claim object

For a formal-system claim let:

C =
<
Scope,
Bindings,
TypeCheck,
DependencyClosure,
AuthorityConsistency,
SourceConsistency
>.

Each load-bearing binding is:

b =
<
ObjectID,
VersionID,
BasisID,
AuthorityID,
Role,
IdentificationStatus,
CurrentnessStatus,
RequiredCoordinates,
RecoveredCoordinates,
InvariantCoordinates,
SourceRefs,
DependencyDisposition,
AdmittedByAuthority
>.

Supported claim scopes are:

CURRENT
CANONICAL
EXACT_CURRENT
CURRENT_FULL
HISTORICAL
CANDIDATE
RECOVERY.

## Governing relation

Let AdmitFormal(C) be the admission relation implemented by:

runtime/formal_claim_admission.py.

For a CURRENT/CANONICAL/EXACT_CURRENT/CURRENT_FULL root, admission requires:

1. exactly one load-bearing root;
2. identified root object;
3. explicit root version;
4. explicit basis;
5. explicit authority;
6. root currentness = CURRENT;
7. every load-bearing required coordinate is recovered or protected by an
   admitted invariance witness;
8. source references exist;
9. every load-bearing dependency is either CURRENT or explicitly
   ADMITTED_FROZEN by the current root authority;
10. dependency closure = PASS;
11. composition type check = PASS;
12. authority consistency = PASS;
13. source consistency = PASS.

Then:

GreenAuthoritative(C)
iff
AdmitFormal(C)=PASS.

Otherwise the claim remains OPEN/BLOCKED/CONFLICT and cannot license green
authoritative emission.

## Historical mathematics

Historical mathematics is not forced red merely because it is no longer current.

A HISTORICAL claim can be green when the exact historical object/version/basis/
authority and required mathematics are recovered.

The protected distinction is:

GREEN as historical
!=
GREEN as current.

This is necessary for frozen ICC128 Legacy mathematics and other preserved
lineage objects.

## Frozen dependencies

A current formal object may deliberately include a historical frozen dependency.

That is legal only when the current root authority explicitly admits the frozen
dependency.

Therefore:

Historical(dep)
and
AdmittedFrozen(dep,Authority(root))
and
Current(root)
and
TypeCheck=PASS

can participate in a current claim.

A merely familiar or older dependency cannot.

This prevents the repair from incorrectly rejecting current wrappers whose
identity intentionally contains a frozen historical core.

## Mathematical color consequence

The general color invariant remains claim-relative.

For an authoritative claim:

GREEN_J(x)
iff
CompleteForUse_J(x)
and
FormalClaimAdmission_J(x)=PASS.

Recovery coordinates alone are no longer sufficient for a current/canonical/
exact-current green claim.

Implementation:

runtime/mathematical_color_gate.py

New helper:

assess_authoritative_recovery(...).

A missing or non-PASS formal-claim receipt forces UNRESOLVED/red.

## ImprovementCore consequence

A formal-system math/equation job is detected by the current user-facing and
Legacy-restored ImprovementCore paths.

When such a job reaches the parent user-return boundary, COMPLETE is illegal
unless the state carries at least one formal-claim admission receipt.

A present receipt whose status is not PASS also forbids COMPLETE.

Thus:

FormalMathJob
and
NoFormalClaimReceipt
=> no COMPLETE.

FormalMathJob
and
FormalClaimReceipt != PASS
=> no COMPLETE.

This closes the bypass where reconstruction can succeed locally and then return
to the user before authority/currentness/type closure is established.

Runtime:

runtime/improvement_core_return_gate.py

Detection/admission:

runtime/formal_claim_admission.py

User-facing binding:

runtime/improvement_core_hf2_default.py

Legacy-restored binding:

runtime/improvement_core_legacy_restored.py

## Relationship to Specification Before Transformation

The two gates are complementary.

Specification-Before-Transformation asks:

Is this object recovered enough to change?

Authority-Before-Formal-Emission asks:

Is this reconstruction recovered/current/typed enough to claim as the named
authoritative mathematics?

Therefore the lawful sequence for a current formal-system reconstruction is:

Observe
-> RecoverObject
-> Reconstruct
-> Resolve exact identity/version/basis/authority
-> Currentness audit
-> Recover required coordinates
-> Close dependency admissions
-> Type-check composition
-> Admit formal claim
-> Color
-> Parent return
-> Emit.

Object-transforming work additionally crosses Specification-Before-Transformation
before the transform.

## Regression instances

The invariant directly targets the observed classes:

- a Legacy/current MT identity being treated as the same object because the
  label MT survived;
- an older ImprovementCore controller block being presented as the current
  semantic object;
- current and historical tool mathematics silently composed without an explicit
  frozen-dependency admission;
- a set union/equality expression emitted even though its operands had
  incompatible mathematical types;
- architecture/improvement proceeding from a device label whose exact protected
  identity had not yet been reconstructed.

## Nonclaims

This invariant does not establish universal host interception.

A chat host that never loads Take-5 can still bypass repository code.

The repository-owned claim is narrower:

every Take-5-governed formal-system math return that reaches the current
ImprovementCore parent-return gate is fail-closed on missing or non-PASS formal
claim admission.

## Validation surface

Runtime:
- runtime/formal_claim_admission.py
- runtime/mathematical_color_gate.py
- runtime/improvement_core_return_gate.py
- runtime/improvement_core_hf2_default.py
- runtime/improvement_core_legacy_restored.py

Regression:
- tests/test_formal_claim_admission.py
- tests/test_mathematical_color_gate.py
- tests/test_improvement_core_return_gate.py

Implementation validation on PR #143 head c45817e28ab3130402d430acfc3878e13d26d94f:

- Take-5 Validation 36292992625: SUCCESS
- Capability Preservation 36292992598: SUCCESS
- ImproveCore Legacy Restoration 130 run 36292992599: SUCCESS
- ImproveCore Legacy Semantic Holdouts 132 run 36292992595: SUCCESS

Promotion completed through PR #143.
Merge commit: d0a625e02795b0863257005de3fa958ae02533a8.

The final persisted receipt head also passed:
- Take-5 Validation 36293035440: SUCCESS
- Capability Preservation 36293035352: SUCCESS
- ImproveCore Legacy Restoration 130 run 36293035315: SUCCESS
- ImproveCore Legacy Semantic Holdouts 132 run 36293035358: SUCCESS.
