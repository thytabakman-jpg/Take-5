# Take-5

**Repository goal:** Provide the canonical working entry, authority boundaries, and navigation for the Take-5 controller stack while preserving Reaserch as rollback/provenance.

**This README's job:** Orient readers to the working repository, the authoritative migration and change-control sources, current architecture entrypoints, and validation routes. It is a navigation surface, not an independent promotion or runtime authority.

Take-5 is the canonical working successor to `thytabakman-jpg/Reaserch`.

Status: CANONICAL_WORKING
Migration stage: MIGRATED_WORKING
Production/working authority: Take-5
Rollback/provenance baseline: Reaserch, preserved intact
Promotion authorization: user authorized 2026-09-24

## Contents

- [ICC](#icc)
- [Start here](#start-here)
- [Authority rule](#authority-rule)
- [Current architecture](#current-architecture)
- [GitHub operating boundary](#github-operating-boundary)

## ICC

ICC is the user-facing name for the current integrated Take-5 stack. It does not create a second controller identity.

**Executable controller identity:** The current canonical `runtime/icc_entry.py` binds ICC128. The component names in the following description are architectural lineage and supporting roles, not a second runtime controller selector. See [current ICC128 conversation control](integration/CURRENT_ICC128_CONVERSATION_CONTROL.md).

ICC means Jane continuity/currentness supervision + the validated Kernel 053 math-first wrapper + ICC128 top-level substantive control + delegated ImprovementCore + Tool Run Closure/HF reentry + the typed configured tool system. The older IC-028 entry path remains a compatibility surface, not the active parent-controller selector.

## Start here

1. [`MIGRATION_STATE.yaml`](MIGRATION_STATE.yaml) — authoritative current repository/migration selection, rollback and post-cutover drift rules; resolve live scope before using older candidate statements.
1. [`GITHUB_GOVERNANCE.md`](GITHUB_GOVERNANCE.md) — admission, branch, validation and merge rules for consequential canonical changes.
1. [`KERNEL.yaml`](KERNEL.yaml) — current machine-readable legality contract; repository working authority is resolved against `MIGRATION_STATE.yaml`, while external-host production claims remain independently gated.
1. [`runtime/jane.py`](runtime/jane.py) + [`runtime/jane_continuity.py`](runtime/jane_continuity.py) + [`runtime/jane_icc128_bridge.py`](runtime/jane_icc128_bridge.py) — typed Jane continuity supervision, guarded ICC128 entry, and preservation of unresolved state without giving Jane controller selection authority.
1. [`architecture/PROJECT_MANAGER_FULL_TOOL_MATH_001_2026-09-27.md`](architecture/PROJECT_MANAGER_FULL_TOOL_MATH_001_2026-09-27.md) + [`runtime/project_manager.py`](runtime/project_manager.py) — reusable authority-bound ProjectManager tool; its first managed project is itself under `projects/project-manager/`.
1. [`architecture/ICC128_HOST_RELAY_001_2026-10-03.md`](architecture/ICC128_HOST_RELAY_001_2026-10-03.md) + [`runtime/icc_host_relay.py`](runtime/icc_host_relay.py) — fail-closed transport-only host relay that requires an ICC128-authored response and blocks host fallback or post-ICC mutation.
1. [`integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md`](integration/CURRENT_TOOL_PROJECT_ORGANIZATION.md) — current anti-loss organization for all live tools and recovered ICC/IC variants; per-object packages, 36-cell coverage, append-only evidence, and overwrite regression guards.
1. [`integration/CURRENT_TOOL_REALITY.md`](integration/CURRENT_TOOL_REALITY.md) — fail-closed strong whole-portfolio tool-reality gate; separates configured identity from explicit manifest identity and native realization.
1. [`integration/CURRENT_IMPROVEMENT_CORE.md`](integration/CURRENT_IMPROVEMENT_CORE.md) — current ImprovementCore recovery authority and live runtime path (resolve the current regime in that file).
1. `integration/ICC_SHUTDOWN_HANDOFF_2026-09-25.md` — historical shutdown handoff retained for provenance; it is not the current resume authority.
1. [`KERNEL_MATH_CONTRACT_053.yaml`](architecture/KERNEL_MATH_CONTRACT_053.yaml) — current validated successor contract; authoritative for runtime use only when selected by the bound runtime ICC entry, per its declared status. Do not treat a filename or this README as sufficient binding.
1. `architecture/KERNEL_MATH_CONTRACT_052.yaml` — review-only exact factorization of K, W_beta, IC, Jane, typed tools, Take Two recovered laws, and the candidate alignment operator.
1. `architecture/KERNEL_MATH_CONTRACT_052.md` — readable companion to the kernel math contract.
1. `architecture/LEARNING_TOOL_ADMISSION_DECISION_040.md` — implemented/validated typed admission of D6/D8 and learning lenses into IC only when their runtime inputs exist.
1. `runtime/learning_tool_bridge.py` — executable IC admission bridge for the learning-tool family.
1. `architecture/MATH_FIRST_WRAPPER_CLOSURE_039.md` — validated final IC/Jane/wrapper equation, implementation evidence, tool placement, and remaining nonblocking work.
1. `architecture/OBSERVER_ALL_TOOLS_SWEEP_038.md` — observer-mode C01-C49 sweep and root quotient.
1. `architecture/IC_JANE_WRAPPER_MATH_PLAN_037.md` — formal mathematics of IC, Jane, and the math-first wrapper.
1. `architecture/ARCHITECTURE_DECISION_036_MATH_FIRST_TOOL_SELECTION.md` — control choice: math first, then goal, architecture, and minimal typed tool selection.
1. `runtime/math_first_wrapper.py` — validated parallel math-first wrapper around protected Jane + IC.
1. `runtime/math_first_selector.py` — exact least-cost sufficient-cover selector, opt-in from IC.
1. `runtime/jane_relevance.py` — typed Jane supervisory-relevance predicate.
1. `architecture/CANONICAL_FOUNDATION_034.md` — current foundation and the two distinct 36-cell structures.
1. `runtime/system_loop.py` and `runtime/improvement_core.py` — lifecycle and adaptive controller.
1. `architecture/LEARNING_OPERATOR_TOOLKIT_035.md` and `runtime/learning_operator_tools.py` — typed mathematical definitions for the selectable learning/processing lenses.
1. `architecture/ASSERT_COMPOUND_CONTRACT_055.md` + `runtime/assert_compound.py` — current compound ASSERT fixed-point contract and executable orchestration shell.
1. `architecture/QUESTION_WORTH_ASKING_CONTRACT_056.md` + `runtime/question_worth_asking.py` — question-frontier valuation and selection tool.
1. `architecture/LAMBDA_MATH_QUESTION_TOOL_CONTRACT_063.md` + `runtime/lambda_math.py` — exact set-valued entry-state reconstruction question-tool.
1. `architecture/LOAD_BEARING_SEMANTIC_OBJECT_PACKAGE_CONTRACT_064.md` + `runtime/semantic_object_package.py` — mandatory durable capture for load-bearing semantic objects, with 36 directed scope-transition pages and append-only evidence.
1. `integration/SEMANTIC_PACKAGE_BACKFILL_001_2026-09-25.md` — explicit historical package backfill debt; new objects use the invariant immediately.
1. `validation/` and `tests/` — readiness, regression, holdout, and execution evidence.

## Authority rule

New work starts here.

Reaserch remains available as frozen historical evidence and rollback state. It is not deleted or overwritten by this migration. Missing historical backfill is preserved as an explicit migration obligation rather than silently treated as absent.

A later discovery can rebase this system through currentness/admission and validation. Migration is reversible and repeatable.

## Level 4 — global claim integrity and repair

[Level 4 certification and repair contract](projects/tool-system/LEVEL4_CERTIFICATION_AND_REPAIR_CONTRACT.md) governs all Level 4 reviews regardless of subject. Level 4 establishes the file's actual purpose and requirements, challenges every material assertion and dependency against its owner, repairs any discovered defects, then reverifies. A genuine OPEN research question is acceptable; an unsupported factual assertion, unsatisfied requirement, or unverified repair **blocks Level 4 certification**. A reviewer cannot obtain PASS by relabeling a previously asserted fact OPEN. A check receipt is not a substitute for specialist verification.

[Structured fail-closed receipt check](runtime/level4_certification.py) and [parent return gate](runtime/improvement_core_return_gate.py) provide conditional runtime enforcement when Level 4 is explicitly selected or the parent context includes an explicit Level 4 request; binding this flag across every entry path is a separate integration obligation, not inferred from document text.

## Current architecture

The controller uses the 36-cell Scope × ModeFace lattice for coverage and false-closure control.

A separate 36-cell SourceScope × TargetScope graph governs directed scope handoffs.

Equal cardinality does not make these the same object.

Runtime mode remains a three-axis cube with eight complete corners.

The foundation remains factored so future discoveries can add or revise coordinates without forcing a monolithic cube.

The learning-operator toolkit is factored the same way. Framework-specific mathematics remains typed and selectable rather than being flattened into one mandatory master loop.

IC and Jane remain protected role-separated suboperators. The validated math-first wrapper is implemented in parallel with the older inquiry wrapper so rollback and matched comparison remain available.

The learning lenses are now first-class IC candidates through a typed bridge. Missing runtime inputs leave the corresponding lens inapplicable and preserve OPEN; no lens is forced onto a problem merely because its mathematics exists.

Current finite registered-repertoire strong tool reality is CLOSED_RELATIVE under `integration/CURRENT_TOOL_REALITY.md`. Configured identity, explicit tool-specific manifests, and recovered native realization now agree for the current repertoire. Environment-bound execution remains explicit where a tool requires domain inputs.

Repository-owned ICC host relaying now has a fail-closed implementation surface. Universal external-host interception remains outside repository authority until the external host is connected to that relay.

## GitHub operating boundary

Repository governance is defined in `GITHUB_GOVERNANCE.md`.

Material canonical changes use branch -> pull request -> validation -> admission -> merge.
`MIGRATION_STATE.yaml` remains the authority pointer: Take-5 is canonical working state and
Reaserch is rollback/provenance evidence. Post-cutover Reaserch writes require explicit
reconciliation and do not become current by recency.
