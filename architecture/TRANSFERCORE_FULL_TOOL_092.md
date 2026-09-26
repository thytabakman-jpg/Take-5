# TransferCore Full Tool 092

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE
Tool: TransferCore
Canonical runtime: runtime/transfer_core.py
Historical semantic sources: Reaserch TransferCore handoff contract, vNext candidate, Max(T) mathematics audit, IC-022 transfer propagation work

## Job

TransferCore determines whether a result/capability/pattern from one source licenses a material target-side consequence, and emits a typed non-authoritative handoff.

It also performs bounded target discovery when targets are not already nominated.

TransferCore does not mutate targets.

## Lifecycle

FREEZE_SOURCE
-> DISCOVER_OR_ACCEPT_BOUNDED_TARGETS
-> FREEZE_TARGET_JOB
-> TYPE_RELATION
-> TEST_APPLICABILITY
-> TEST_BRIDGE_LICENSE
-> ESTIMATE_TARGET_EFFECT
-> TEST_DUPLICATION
-> TYPE_AUTHORITY
-> DISPOSE
-> EMIT_HANDOFF
-> TARGET_REVIEW
-> TARGET_VERIFICATION
-> FEEDBACK_REENTRY.

## Core types

Source =
<source_id, source_project, source_result_ref, source_refs, object_type, payload, provenance>.

Target =
<target_id, target_project, target_job, target_type, metadata>.

Relation =
<source_id, target_id, status, statement, applicability, bridge_license,
 target_effect, material_effect, duplication_status, authority_state, evidence, OPEN>.

Relation status:
ADMITTED | REJECTED | PARKED | NO_EFFECT | OPEN | BLOCKED | CONFLICT.

Handoff =
<id, source result, source project/refs, relation status/statement,
 target, target effect, bridge license, duplication, authority state,
 review trigger, target_mutated=false>.

## Admission law

ADMITTED requires:
- applicability true;
- non-open licensed bridge;
- material target effect true;
- no full-duplicate/no-new-effect witness;
- no unresolved load-bearing coordinate.

ADMITTED does not authorize target mutation.

Unlicensed relation -> REJECTED.

No material effect or full duplicate -> NO_EFFECT.

Missing evaluator or missing load-bearing coordinate -> OPEN.

## Target discovery

Target discovery is bounded.

No default all-project cross-product is allowed.

When no explicit targets are supplied:
- a discovery adapter is required;
- target count is capped by max_targets;
- bound overflow returns OPEN;
- no target result returns NO_EFFECT.

This implements the historical TransferCore vNext rule that target search must be localized rather than combinatorial.

## Feedback

Target verification feeds back into the source-transfer relation.

Failed target verification or changed relation evidence sets relation_recompute_required and reentry_required.

Feedback never silently edits source or target state.

## FullMath

N =
<Source,Target,Relation,Handoff,Feedback> typed relation/update system.

W =
<configured wrapper -> bounded discovery -> relation evaluation -> handoff -> target authority boundary -> target verification -> feedback reentry>.

G =
source/target and higher-arity expansion remain witness-gated. Current runtime implements bounded one-source/multi-target execution and preserves higher-arity expansion as future work rather than pretending pairwise evidence proves joint transfer.

P =
<provenance preservation, bridge licensing, target-effect requirement, duplication test, no authority laundering, OPEN preservation, bounded search, target verification feedback>.

L =
<registered configured tool, canonical Take-5 runtime, historical Reaserch lineage preserved as provenance, current recovery anchor, tests>.

## Current strict gain over historical runtime

Historical Research had:
- a semantic handoff contract;
- a queue propagation utility;
- a vNext target-discovery proposal;
- a Max(T) audit showing missing state/update/reentry semantics.

Take-5 now has one callable runtime object that:
- accepts or discovers bounded targets;
- types every relation;
- derives fail-closed disposition;
- emits target-safe handoffs;
- preserves OPEN;
- supports target-verification feedback;
- is registered under the current configured-run system.

## Remaining OPEN

- multi-source irreducible joint transfer;
- representation/hierarchy challenge packages;
- persistent queue adapter in Take-5;
- automatic target-authority binding;
- matched historical replay suite;
- external-source holdout;
- target-side authorized mutation worker.
