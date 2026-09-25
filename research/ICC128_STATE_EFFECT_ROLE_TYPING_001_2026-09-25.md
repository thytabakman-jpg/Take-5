# ICC-128 State-Effect Role Typing 001

Date: 2026-09-25
Status: RESEARCH RESULT / NO RUNTIME EFFECT
Parent: research/ICC128_COMPLETE_MEDIATION_EXPERIMENT_001_2026-09-25.md
Major-change freeze: ACTIVE

## Question

What are the load-bearing state species in current Take-5, and which of them require a protected commit/admission boundary?

The purpose is to resolve E5 far enough to distinguish legitimate multiple-state architecture from bypass defects.

## State species

Let Sigma be the set of state species.

Current evidence supports at least:

- EPISODE_WORKING
- SYSTEM_CONTROL
- RESULT
- LINEAGE
- RESEARCH_CONTROL
- SUPERVISORY
- CONFIGURATION
- VALIDATION_DERIVED

OPEN remains available when currentness evidence does not uniquely classify a path.

## Typed dispositions

### sigma_A5

Object:
runtime/a5_core.py State.

Role:
VALIDATION_DERIVED / PROTOTYPE_SEMANTIC_STATE.

Ground:
module contract says nonproduction behavioral architecture skeleton.

Legal producer:
A5.transition through AdmissionC and UpdaterU.

Authority:
effect-scoped Witness authority.

Evidence/admission:
AdmissionC ALLOW.

Provenance:
transition history.

Reentry:
not established as current production reentry state.

Shared K_exec requirement:
NO production claim. Retain as a local witness for what mediated transition can look like.

### sigma_IC

Object:
Improvement Core current/final_packet.

Role:
EPISODE_WORKING until admitted by an outer state owner.

Ground:
IC is the adaptive/policy controller, not the whole system; current foundation places it inside the work lifecycle.

Legal producers:
selected bound capability executions.

Authority:
bounded episode/delegation authority.

Evidence:
ActivationBridge execution receipt/delegation evidence.

Admission:
IC itself merges returned dictionaries into working state. This is not sufficient evidence that the result is authoritative system state.

Provenance:
partially represented through receipts and packet metadata.

Reentry:
IC delta router.

Shared K_exec requirement:
IC outputs require a later typed commit gate before becoming protected outer state.

### sigma_SYS

Object:
system_loop current, discharged set, open_coordinates, SystemResult.

Role:
SYSTEM_CONTROL.

Ground:
system_loop explicitly states that the system owns work existence/closure. reflexive_currentness states that IC is policy controller inside this work lifecycle.

Legal producer:
endogenous work lifecycle.

Current producer implementation:
ICResult.final_packet plus work-discharge bookkeeping.

Authority requirement:
not fully explicit at the system-loop update boundary.

Evidence requirement:
IC execution result plus work/closure evidence.

Admission requirement:
OPEN. Direct current.update() and discharged.add() currently serve as implementation, with no shared typed commit object.

Provenance:
insufficiently explicit at each system state delta.

Reentry:
system loop regeneration/closure.

Shared K_exec requirement:
YES, or an equivalent typed SYSTEM_CONTROL commit gate satisfying the common protected contract.

### sigma_RESULT

Object:
math-first wrapper state representing the externally relevant episode/result state.

Role:
RESULT.

Ground:
MATH_FIRST_WRAPPER_CLOSURE_039 defines admitted update U after Tool Run Closure and before Jane sync/reentry.

Legal producer:
wrapper consequence closure.

Authority:
bound EntryContract authority and protected target/job.

Evidence:
closure certificate + IC result + execution evidence as applicable.

Admission:
caller-supplied update_fn after closure.

Provenance:
delta fingerprint/receipts plus caller state.

Reentry:
wrapper material/result-sensitive reentry.

Shared K_exec requirement:
YES.

Current gap:
update_fn is a generic callback, so common-kernel enforcement depends on its implementation rather than a typed commit interface.

### sigma_REC

Object:
inquiry_session / recursive_episode state.

Role:
OPEN between EPISODE_WORKING and alternate/legacy RESULT path.

Ground:
these facades remain executable and tested; the newer math-first wrapper is also current. Exact operational authority between them is not uniquely frozen across all host paths.

Legal producer:
closure_fn followed by update_fn.

Authority/evidence:
caller-defined beyond entry binding and closure contract.

Admission:
callback-defined.

Reentry:
recursive episode / external challenge.

Shared K_exec requirement:
OPEN until lineage/currentness establishes whether this is an authoritative result path or retained alternate facade.

### sigma_LINEAGE

Object:
LineageState.

Role:
PERSISTENT_LINEAGE.

Legal producer:
admitted material state deltas only, by architecture intent.

Current producer implementation:
LineageState.apply(delta, provenance).

Authority:
not required by apply() itself.

Evidence:
provenance is required by signature, but no verification/admission receipt type is required.

Admission:
caller convention.

Reentry:
lineage changes can affect currentness and future control.

Shared K_exec requirement:
YES for material protected lineage updates, via a LINEAGE commit gate or equivalent proof that all callers are already gated.

### sigma_RESEARCH

Object:
ResearchState claims, history, discharged.

Role:
RESEARCH_CONTROL.

Ground:
ResearchState status and history participate in closure_certificate; ADMITTED claims without evidence prevent closure.

Legal producer:
research process after evidence/admission.

Current producer implementation:
record_claim() and discharge() mutate directly.

Authority:
no authority token required.

Evidence:
evidence tuple stored for claims; closure checks evidence presence, not authorization.

Admission:
record_claim accepts ADMITTED status directly.

Reentry:
closure/work state depends on claims/discharge.

Shared K_exec requirement:
YES if this state participates in canonical research control, otherwise it must be explicitly demoted to derived/testing state.

### sigma_JANE

Object:
JaneSupervisoryState.

Role:
SUPERVISORY.

Legal producer:
continuity-relevant admitted deltas.

Current producer implementation:
update_after_admitted_delta / continuity_alert.

Authority:
Jane does not grant authority.

Evidence:
receipts/canonical-version relation/deltas.

Admission:
caller convention; math-first wrapper invokes sync only after admitted material relevant delta.

Reentry:
alerts/currentness/frontier can create future work.

Shared K_exec requirement:
typed supervisory gate or upstream proof. It need not share the RESULT storage mechanism, but it must not manufacture protected currentness from an unadmitted delta.

### sigma_CONFIG

Objects:
ProgramRegistry and configuration registries.

Role:
CONFIGURATION.

Legal producer:
repository/versioned configuration changes, not ordinary episode workers.

Authority:
GitHub governance/change authority.

Evidence/admission:
branch -> PR -> validation -> admission -> main.

Reentry:
configuration change can trigger currentness and test re-evaluation.

Shared K_exec requirement:
not necessarily the runtime effect gate. Repository governance is the relevant commit boundary for static configuration.

### sigma_VALIDATION

Objects:
closed_loop fixture files, zero-request dumps, validation receipts, local audit outputs.

Role:
VALIDATION_DERIVED.

Authority:
none by persistence alone.

Admission:
must be consumed by an explicit higher-level currentness/admission process before changing canonical system state.

Shared K_exec requirement:
NO direct runtime commit gate required while they remain evidence only.

## Key mathematical result

The evidence does not support forcing every state species through one physical updater object.

The stronger supported abstraction is an indexed family of commit gates.

For protected state species sigma in Sigma_P, define:

C_sigma:
<z_sigma, delta, beta, evidence>
->
<z'_sigma, receipt>
or
OPEN/BLOCKED.

Let K_common be the common protected transition contract.

Required:

for every sigma in Sigma_P,
C_sigma models K_common restricted to the laws applicable to sigma.

And complete mediation becomes:

for every protected sink Z_sigma,
for every executable path p from a legal proposal source to Z_sigma,
p intersects C_sigma.

Therefore the abstract update role is better represented as:

U = { U_sigma }_(sigma in Sigma_P)

rather than assuming one untyped universal U implementation.

This preserves one kernel contract without forcing one state store or one storage/update mechanism.

## Common contract candidate

Every protected C_sigma requires the applicable subset of:

1. stable referent/target/job identity;
2. currentness/baseline identity;
3. authority is explicit and non-expanding;
4. evidence does not self-authorize;
5. transition/effect class is typed;
6. required execution has an execution receipt;
7. required consequence closure/verification has a receipt;
8. OPEN/BLOCKED/INCOMPARABLE are preserved;
9. provenance is retained;
10. material delta triggers the required reentry/currentness effects;
11. local state cannot self-promote to a stronger authority class.

The exact minimal K_common remains OPEN pending historical witness recovery and externalizability analysis.

## Current bypass candidates after role typing

HIGH PRIORITY:
- sigma_SYS direct system_loop update/discharge;
- sigma_LINEAGE direct apply without intrinsic admission receipt;
- sigma_RESEARCH direct ADMITTED-status mutation.

CONTRACTUAL/INTERFACE GAP:
- sigma_RESULT update_fn callback lacks a common typed commit contract;
- sigma_REC update_fn callback remains currentness ambiguous.

UPSTREAM-GUARDED / LOWER PRIORITY:
- sigma_JANE, because current wrapper guards sync but direct helper invocation remains possible.

NONPRODUCTION OR DERIVED:
- sigma_A5;
- sigma_VALIDATION.

STATIC GOVERNANCE PATH:
- sigma_CONFIG.

## Architecture consequence

The next architecture experiment does not need to choose between:

one giant global updater
versus
completely independent mutation semantics.

A third candidate now dominates both as the research hypothesis:

COMMON KERNEL CONTRACT + TYPED STATE-SPECIFIC COMMIT GATES.

No production claim is made.

## Next falsifiable experiment

For sigma_SYS, sigma_RESULT, sigma_LINEAGE, sigma_RESEARCH, and sigma_JANE:

1. reconstruct every current producer/caller;
2. define required commit receipt;
3. construct a nonproduction adapter C_sigma around existing behavior;
4. matched-test existing outputs/closure;
5. inject authority/admission/OPEN failures;
6. verify that bypass attempts cannot change the protected sink through the adapter;
7. only then decide whether to migrate the real path.

Historical tool/ICC lineage remains a parallel prerequisite for shrinking K_common.

## Disposition

STATE_ROLE_TYPING:
SUFFICIENT_FOR_NEXT_EXPERIMENT.

ONE_PHYSICAL_GLOBAL_UPDATER:
NOT REQUIRED BY CURRENT EVIDENCE.

COMMON_KERNEL_CONTRACT_PLUS_TYPED_GATES:
SUPPORTED RESEARCH HYPOTHESIS.

RUNTIME MIGRATION:
NOT AUTHORIZED.

KERNEL MINIMALITY:
OPEN.
