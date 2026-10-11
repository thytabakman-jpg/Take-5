# OPEN questions: GOAL

- package-specific open questions are added here only when they are not already owned by a canonical source

## Cross-repository authority boundary — OPEN

- **Resolved for configured Take-5 GOAL invocations:** the active protected specification is selected by `runtime/tool_manifest.py::manifest_for("GOAL").lineage_contract` (currently `architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md`), and its configured entrypoint by `runtime/portable_tool_conductor.py::compilation_witness("GOAL").entrypoint` (currently `goal.recover_goal_configured`). See [SOURCE_MAP.md](SOURCE_MAP.md) and [RUNTIME.md](RUNTIME.md). This binding is **not** an OPEN choice between two current Take-5 specifications.
- **Still OPEN — cross-repository handoff/equivalence:** the Take-5 configured runtime and [Reaserch typed GOAL architecture](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_TYPED_CURRENT_003_2026-10-07.md) have independently governed contracts. No admitted cross-repository equivalence, transfer, or automatic precedence rule has been established for a proposed mixed-source consumer. The relevant owner must reconcile the specific consumer, operation and authority before treating external material as an override. An invocation already governed by Take-5's configured-tool selectors is not made ambiguous by the existence of Reaserch provenance.
- **Protected boundary:** Reaserch canonical project-goal statements and approval rules retain their own authority; this package does not modify those goals or infer cross-repository admission from filename/date. If the concrete consumer's owner cannot be resolved, leave that consumer `OPEN` rather than silently choosing a source.

## Rule

OPEN is durable state. Closing an item requires evidence and a receipt; deleting
the line because a later summary is shorter is forbidden.
