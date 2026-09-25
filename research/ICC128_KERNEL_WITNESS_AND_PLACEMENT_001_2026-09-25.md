# ICC-128 Kernel Witness and Placement Analysis 001

Date: 2026-09-25
Status: RESEARCH RESULT / BASIS-RELATIVE PLACEMENT
Canonical repository: thytabakman-jpg/Take-5
Controller: ICC-128
Major-change freeze: ACTIVE
Runtime effect: NONE

## Question

Given current Take-5, Take Two, early MT, and representative historical Improvement Core evidence, which protected behaviors must survive any kernel refactor, and which current K laws appear externalizable from the common commit kernel without losing those behaviors?

This is not a global-minimality proof.

The full tool/ICC lineage backfill remains OPEN.

The result is relative to the recovered historical witness basis below.

## Evidence basis

Current/canonical:
- architecture/KERNEL_MATH_CONTRACT_052.yaml
- architecture/CANONICAL_FOUNDATION_034.md
- architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md
- research/ICC128_COMPLETE_MEDIATION_EXPERIMENT_001_2026-09-25.md
- research/ICC128_STATE_EFFECT_ROLE_TYPING_001_2026-09-25.md
- research/TOOL_LINEAGE_RECOVERY_CONTRACT_001_2026-09-25.md

Lineage evidence:
- thytabakman-jpg/Take-2 KERNEL.yaml
- thytabakman-jpg/Take-2 ARCHITECTURE.md
- Reaserch MT lineage experiment
- Reaserch IC-001
- Reaserch IC-015
- Reaserch IC-018
- Reaserch IC-022
- Reaserch IC-024
- Reaserch IC-028

Reaserch is provenance evidence only, not current authority.

## Conservative protected witness basis

### W_REF

Exact target, task/job, baseline, and success-condition identity remain explicit.

A plan or optimization step cannot silently change the object or goal and call it the same improvement.

Historical support:
IC-001 and descendants; Take-5 entry/identity contract.

### W_AUTH

Authority is explicit, typed, and non-expanding.

Evidence, diagnosis, priority, semantic success, selection, or local success do not create mutation/promotion authority.

Historical support:
Take Two authority law; IC-001 mutation boundary; IC-024/028 execution/promotion separation.

### W_OBSERVE

Reconnaissance/observation can occur without mutating the observed live object.

Whole-object goal-decoupled observation can expose material issues not named by a supplied local goal.

Historical support:
early MT; Take Two observations-before-causal-claims; current observer-first paths.

### W_TRANSITION

Consequential state change is represented as a typed bounded transition with baseline, target/effect, authority, expected/actual delta, verification, and result.

Historical support:
Take Two Transition primitive; IC-001 TransitionContract/checkpoint semantics.

### W_OPEN

OPEN, BLOCKED, PLURAL/INCOMPARABLE, and branch structure cannot be coerced into one success state merely to close the run.

Historical support:
Take Two; IC-001; RTC v2 in IC-018; IC-028 partial/set-valued control.

### W_EXECUTION

Specified/planned/selected/semantically applied is not implementation executed.

Execution claims require execution-state evidence.

Historical support:
IC-024 execution truth; IC-028 execution ledger; Take-5 ActivationBridge.

### W_REENTRY

Material result/search/representation/state changes can invalidate prior analysis and force reobservation, recomputation, reverification, or reselection.

Historical support:
early MT LOOK AGAIN; Take Two reentry; IC-001 recomputation; IC-018 RTC state transitions; IC-028 continuation fixed point.

### W_LINEAGE

Accepted material deltas, candidates, and successor cycles remain reconstructible by provenance/ancestry.

Later versions do not rewrite history.

Historical support:
Take Two migration-by-behavior; IC-015 cycle ancestry; IC-018 historical-version preservation; Take-5 lineage state.

### W_SURFACE

A semantic distinction does not automatically require a new registry, subsystem, or operating surface.

A new surface/primitive needs strict gain over a behaviorally sufficient view/composition.

Historical support:
Take Two.

### W_DISCOVERY

The system can generate new questions/work from observation, including zero-request/broad-corpus cases, and admitted representation changes can change the candidate universe.

Historical support:
early MT; Take Two/RCDL; IC-028 zero-request/discovery integration.

### W_PROMOTION

No local component or candidate can promote itself to stronger canonical/runtime/production authority.

Promotion is a separate governed transition.

Historical support:
Take Two; IC-001 immutable selector promotion; IC-024/028 no self-promotion; Take-5 authority gate.

### W_CLOSURE

Closure is basis-relative and must not be inferred from cycle budget, registry exhaustion, repeated no-gain, or one local fixed point.

Historical support:
IC-018 RTC closure rules; IC-028 continuation fixed point; current TRC/HF distinctions.

### W_PRESERVE

A cleaner/compressed/newer tool is not a preserving successor until the old protected witness set survives matched comparison.

Historical support:
early MT lineage failure; Tool Lineage Recovery Contract; Take Two behavior-not-file migration.

### W_TYPED_STATE

Result, evidence, authority, persistent state, controller state, and runtime execution status remain typed rather than silently collapsed.

Historical support:
IC-028 controller state and execution ledger; Take-5 factorization and state-role experiment.

## Placement test

For current law I_i, define basis-relative externalizability:

Externalizable_B(I_i,L)
iff
there exists an assigned layer L != K_common such that:

1. every witness in B protected by I_i remains satisfiable;
2. every protected authoritative state path still crosses a typed commit gate that consumes any required proof from L;
3. removing I_i from the common gate does not allow a forbidden state transition;
4. failure/OPEN behavior remains typed;
5. the law remains non-bypassable at the layer that actually owns its job.

This tests placement, not importance.

An externalized law can remain globally mandatory.

## Current fourteen-law placement

### I_entry

Current law:
SubstantiveAction => Bound(beta).

Protected witnesses:
W_REF, W_AUTH.

Placement result:
INTERFACE/ENTRY BOUNDARY, with commit gates requiring a valid binding reference.

Reason:
entry binding happens before a state-specific commit gate. The common gate needs the bound identity/authority packet but need not own conversation-entry orchestration.

Status:
EXTERNALIZABLE_FROM_COMMON_GATE / NOT OPTIONAL.

### I_identity

Current law:
target/job remain stable during the episode.

Protected witnesses:
W_REF.

Placement result:
COMMON COMMIT CONTRACT.

Reason:
an authoritative effect on a different referent/job is a forbidden transition regardless of which controller produced it.

Status:
FOUNDATIONAL_CANDIDATE.

### I_surface

Current laws:
Distinct does not imply SeparateSurface; new surfaces require strict gain.

Protected witnesses:
W_SURFACE, W_PRESERVE.

Placement result:
ARCHITECTURE CONSTITUTION.

Reason:
this governs evolution of the architecture itself, not every ordinary state delta.

Status:
EXTERNALIZABLE_FROM_RUNTIME_COMMIT_GATE / GLOBALLY PROTECTED.

### I_transition

Current law:
consequential change requires an authorized/applied/verified typed transition.

Protected witnesses:
W_TRANSITION, W_AUTH, W_EXECUTION.

Placement result:
COMMON COMMIT CONTRACT.

Status:
FOUNDATIONAL_CANDIDATE.

### I_authority

Current law:
authority cannot expand; evidence does not self-authorize.

Protected witnesses:
W_AUTH, W_PROMOTION.

Placement result:
COMMON COMMIT CONTRACT plus separate production-promotion authority gate.

Status:
FOUNDATIONAL_CANDIDATE.

### I_observe

Current law:
observation is nonmutating.

Protected witnesses:
W_OBSERVE, W_DISCOVERY.

Placement result:
OBSERVER/INTERFACE/CONTROLLER.

A common commit gate can indirectly protect the same property by refusing effects without mutation authority during an observation-only binding.

The observer still needs its own ordering and isolation contract.

Status:
EXTERNALIZABLE_FROM_COMMON_GATE / NOT OPTIONAL.

### I_freeze

Current law:
frozen mathematical object cannot silently mutate during execution.

Protected witnesses:
W_REF, W_PRESERVE, W_TYPED_STATE.

Placement result:
WRAPPER/EPISODE CONTRACT.

A state-specific commit gate must reject effects inconsistent with the frozen/bound basis where that basis is result-sensitive, but the Freeze operation itself is orchestration.

Status:
EXTERNALIZABLE_FROM_COMMON_GATE / PROOF TOKEN CONSUMED BY GATE.

### I_execution

Current law:
complete execution requires selected, bound, dispatched, started, executed, captured, consumed.

Protected witnesses:
W_EXECUTION.

Placement result:
INTERFACE/RUNTIME EXECUTION-RECEIPT SYSTEM.

The common commit gate requires an execution receipt only for effects whose legal basis includes actual execution.

Status:
EXTERNALIZABLE_FROM COMMON GATE AS MECHANISM / EXECUTION TRUTH REMAINS A COMMIT PRECONDITION.

### I_admission

Current law:
persistent update only after admissible closure/admission.

Protected witnesses:
W_TRANSITION, W_OPEN, W_EXECUTION.

Placement result:
COMMON COMMIT CONTRACT.

The exact upstream closure machinery can vary by state species, but authoritative/persistent commit requires an admissible disposition/receipt.

Status:
FOUNDATIONAL_CANDIDATE.

### I_open

Current law:
OPEN/BLOCKED/INCOMPARABLE cannot be coerced into success.

Protected witnesses:
W_OPEN.

Placement result:
COMMON COMMIT CONTRACT and controller/status algebra.

Status:
FOUNDATIONAL_CANDIDATE.

### I_closure

Current law:
relative close requires CLOSED, result stability, and no live reentry trigger.

Protected witnesses:
W_CLOSURE, W_REENTRY.

Placement result:
VERIFICATION/CONTROLLER.

The commit gate may require a closure/verification receipt for particular effect classes, but it does not own search convergence or controller stopping.

Status:
EXTERNALIZABLE_FROM COMMON GATE / GLOBALLY PROTECTED.

### I_lineage

Current law:
admitted material deltas remain reconstructible.

Protected witnesses:
W_LINEAGE, W_PRESERVE.

Placement result:
STATE-SPECIFIC COMMIT CONTRACT + LINEAGE STATE.

Each protected commit must emit sufficient provenance/receipt material. Storage/reconstruction machinery remains in the state layer.

Status:
SPLIT PLACEMENT.

### I_reentry

Current law:
material/result-sensitive delta causes reentry/reverification.

Protected witnesses:
W_REENTRY, W_DISCOVERY.

Placement result:
CONTROLLER/CURRENTNESS.

A commit gate emits the typed delta/receipt; controller logic owns continuation.

Status:
EXTERNALIZABLE_FROM COMMON GATE / DELTA SIGNAL REQUIRED.

### I_promotion

Current law:
no component converts local success to production authority.

Protected witnesses:
W_PROMOTION, W_AUTH.

Placement result:
AUTHORITY/PROMOTION GATE.

The common authority law forbids authority expansion, while production/canonical promotion remains a specialized transition.

Status:
PARTLY SUBSUMED BY COMMON AUTHORITY LAW, SPECIALIZED PROMOTION GATE RETAINED.

## Basis-relative common contract candidate

The placement test supports a smaller common effect contract than the current fourteen-law list, without deleting the externalized protections.

Candidate:

K_common^B
=
K_ref
AND K_auth
AND K_trans
AND K_admit
AND K_status
AND K_prov

where:

K_ref
=
protected referent/job/currentness/state-species binding is stable for the effect.

K_auth
=
effect authority is explicit, non-expanding, and cannot be manufactured by evidence/local success.

K_trans
=
the effect is a typed transition with required baseline/effect/delta identity and applicable execution/verification proof.

K_admit
=
the state-specific disposition licenses commit; no persistent/authoritative update occurs from a merely proposed/selected/semantic result.

K_status
=
OPEN/BLOCKED/INCOMPARABLE/branch states remain non-success unless a licensed transition resolves them.

K_prov
=
the material committed delta is reconstructible enough for required lineage/currentness/reentry.

No minimality claim is made.

K_common^B is a research factorization under the recovered witness basis B.

## State-specific commit family

For each protected state species sigma:

C_sigma:
<z_sigma, delta, beta, receipts>
->
<z'_sigma, commit_receipt>
or
OPEN/BLOCKED.

Required:

C_sigma models the applicable K_common^B laws.

The remaining protected behavior lives in typed owners:

Entry:
I_entry.

Architecture constitution:
I_surface + successor/witness preservation + factor anti-loss.

Observer/controller:
I_observe.

Wrapper:
I_freeze.

Runtime/interface:
I_execution mechanics and receipts.

Verification/controller:
I_closure.

State:
lineage storage/reconstruction.

Controller/currentness:
I_reentry.

Promotion authority:
specialized I_promotion transition.

This gives:

protected_behavior
!=
all_behavior_must_live_in_the_same_kernel_function.

## Historical backfill constraint

This basis does not complete B4.

Known remaining lineage debt includes:
- full PD/PDAudit episode reconstruction;
- remaining ICC immutable versions and branch nodes;
- HF-001 lineage;
- MTA;
- RTC historical variants;
- Multi-Object;
- Architecture Analysis;
- full Take Two configuration/witness battery;
- other priority families.

Any newly recovered counterexample can split this placement.

Therefore:

GLOBAL_KERNEL_MINIMALITY = OPEN.

## Immediate implementation disposition

Do not rewrite KERNEL.yaml from this result.

Do not replace current wrapper/system loop/state modules.

Do not implement K_common^B directly yet.

Next executable design work requires:
1. nonproduction commit-gate adapters for SYSTEM_CONTROL, RESULT, LINEAGE, RESEARCH_CONTROL, and SUPERVISORY state;
2. matched preservation tests against current behavior;
3. injected authority/admission/OPEN failure tests;
4. lineage counterexample sweep against B4;
5. only then a migration proposal.

## Result

The current fourteen laws are not one natural execution-kernel block.

They factor into:
- a smaller basis-relative common effect contract;
- architecture-constitution laws;
- interface/runtime proof mechanisms;
- wrapper/controller invariants;
- state/lineage duties;
- specialized promotion authority.

The strongest current architecture hypothesis is:

COMMON PROTECTED EFFECT CONTRACT
+
TYPED STATE-SPECIFIC COMMIT GATES
+
SEPARATE ARCHITECTURE CONSTITUTION
+
REPLACEABLE CONTROLLER/WRAPPER/RUNTIME MECHANISMS.

This is a research result, not a runtime promotion.
