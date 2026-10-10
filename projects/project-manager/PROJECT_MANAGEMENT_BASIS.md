# Project management basis

Status: CURRENT EVIDENCE BASIS
Date checked: 2026-09-27

## Internal basis

The Sukkos question-booklet project demonstrated a working separation among charter,
goal, current state, authority registry, change control, decisions, RAID, WBS, lessons,
semantic authorities, 36-cell coverage, and tool-run receipts.

The generalization preserves those anti-loss properties while making the project-state
object domain-independent.

## External research

PMI WBS guidance
A work breakdown structure is deliverable-oriented and decomposes total project scope.
The WBS is not the schedule and moves under change control after baselining.
https://www.pmi.org/learning/library/developing-elaborating-work-breakdown-structures-7241

ISO 21502
Project-management guidance applies across organization types, project purposes,
delivery approaches, life cycles, complexity, size, cost, and duration.
https://www.iso.org/standard/74947.html

ISO project-management overview
Planning and control include risks, issues, change control, benefits and change,
and project information.
https://www.iso.org/news/ref2604.html

NASA technical management
Crosscutting control processes include planning, requirements, interfaces, risk,
configuration, data, assessment, and decision analysis.
https://www.nasa.gov/reference/6-1-technical-planning/
https://www.nasa.gov/reference/6-5-configuration-management/
https://www.nasa.gov/reference/6-6-technical-data-management/
https://www.nasa.gov/reference/6-4-technical-risk-management/
https://www.nasa.gov/reference/6-8-decision-analysis/

## Synthesis

The reusable control core needs explicit state, ownership, decomposition, dependencies,
interfaces, risk and issue state, evidence, decisions, change and baseline history,
verification, and information and handoff surfaces.

Domain-specific project content remains extensible and owned by project-specific files.


## Cross-project failure-history basis — 2026-09-30

The current raise-the-ceiling pass additionally uses the cross-project management
failure audit stored in Take-2:

audits/PROJECT_MANAGEMENT_FAILURE_HISTORY_READONLY_2026-09-30.md

The evidence spans authority/currentness, resume/handoff, scope/object typing,
adaptive planning, ownership, execution truth, change propagation, closure,
artifact production, research evidence, discoverability, recursive stopping,
cross-project transfer, concurrency/promotion, human orchestration, and lower-frequency
holdouts.

The operational generalization is encoded in FAILURE_PREVENTION_MATRIX.md rather
than treating the audit as narrative-only learning.

## Currentness and operational evidence crosswalk (2026-10-10 Level 2)

The sources above explain the design choices; they are not themselves live
executable identity or proof of full semantic regression coverage. Preserve
the original 2026-09-27 external research date and the 2026-09-30
cross-project audit attribution. The original external research links have
not been freshly reverified by this document triage.

To test a present operational claim, use the current configured owners
`runtime/tool_run_registry.py`, `runtime/tool_manifest.py`, and
`runtime/project_manager.py`, the native integrity implementation in
`runtime/project_manager_integrity.py`, the self-managed owner files and
`projects/project-manager/VERIFICATION.md`. Accepted mathematical layers
001–004 are additive provenance, not competing live identity selectors.

A passing historical regression or development-fixture sweep substantiates
its actual source head and executed tests only. Real user-authorized
commit-side admission and stale precondition checks remain separately OPEN
in `projects/project-manager/OPEN_QUESTIONS.md` Q4; exact direct
ICC128/RTC/ToolConductor coverage is OPEN as Q5 / verification V50.
These OPEN evidence boundaries do not undo already merged project controls.
