# Evidence registry

Status: CURRENT

Internal authoritative and recovery evidence
architecture/FULL_TOOL_MATHEMATICAL_IDENTITY_CONTRACT_002_2026-09-26.md
architecture/SPECIFICATION_BEFORE_TRANSFORMATION_INVARIANT_134.md
architecture/FULL_CONFIGURED_TOOL_INVOCATION_121.md
architecture/ASSERT_COMPOUND_CONTRACT_055.md
architecture/GOAL_FULL_TOOL_MATH_001_2026-09-27.md
integration/CURRENT_HF2.md
integration/CURRENT_IMPROVEMENT_CORE.md
projects/sukkos-question-booklet/PROJECT_MANAGEMENT_BASIS.md
projects/sukkos-question-booklet/CONTROLLER.md
projects/sukkos-question-booklet/AUTHORITY_REGISTRY.md
projects/sukkos-question-booklet/CHANGE_CONTROL.md
projects/sukkos-question-booklet/WBS.md
projects/sukkos-question-booklet/LESSONS_LEDGER.md

External comparator and research evidence
PMI WBS guidance.
ISO 21502 project-management guidance.
NASA technical planning, configuration, data, risk, and decision-analysis guidance.

Evidence does not self-authorize admission.

## Current implementation and verification witnesses

The earlier architecture and Sukkos references above are foundational evidence,
not automatically current execution authority. For the accepted ProjectManager
capability, recover these explicitly named source/consumer surfaces:

- projects/project-manager/GOAL.md — governing goal, not a run receipt
- projects/project-manager/CONTROLLER.md — project-control semantic specification
- runtime/project_manager.py — native observer and handoff consumer
- runtime/project_manager_integrity.py — known-failure integrity consumer
- runtime/project_manager_management_spine.py — ordinary-run management spine
- runtime/tool_run_registry.py and runtime/tool_manifest.py — live configured identity
- tests/test_project_manager.py, tests/test_project_manager_failure_immunity.py,
  tests/test_project_manager_management_spine.py — dedicated regression sources
- projects/project-manager/VERIFICATION.md — checked-in evidence and open claims
- projects/project-manager/tool-runs/ALL_TOOLS_HF2_CANONICAL_001.md — historical 93-tool campaign receipt
- projects/project-manager/tool-runs/FAILURE_IMMUNITY_ICC_RTC_TOOLCONDUCTOR_001.md — original failure-immunity campaign and later merge witness
- architecture/PROJECT_MANAGER_FULL_TOOL_MATH_001_2026-09-27.md through
  architecture/PROJECT_MANAGER_FULL_TOOL_MATH_004_2026-09-30.md — distinct
  accepted mathematical-layer documents, not filename-based currentness authority

## Status and evidence admission boundary

PR 164 (core), PR 167 (historic 93-tool campaign), PR 170 (candidate admission),
PR 173 (ordinary spine) and PR 187 (failure-immunity extension) represent
different dated implementation/verification milestones. The present ProjectManager
identity is reconstructed from the *live* runtime/manifest, not these receipt
names or their numeric order. A successful CI run supports exactly its source
head and executed test coverage, not a later state or stronger semantic claim.
Actual owner-side promotion/commit evidence (Q4) and exact full semantic campaign
coverage (V50, Q5) remain OPEN unless independently demonstrated.
