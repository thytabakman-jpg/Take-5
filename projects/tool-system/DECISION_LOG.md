# Tool System Decision Log

Append-only.

## 2026-09-27 D001

Adopt the Sukkos-style authority registry, current-state projection, change
control, append-only lessons/decisions, and separate coverage cells for the
entire tool system.

## 2026-09-27 D002

Use a non-destructive organizational overlay. Existing semantic/runtime evidence
is referenced in place rather than moved into new package folders.

## 2026-09-27 D003

Give every current configured tool its own package and preserve historical ICC/IC
variants in a separate namespace.

## 2026-09-27 D004

Keep Scope x ModeFace coverage and SourceScope x TargetScope handoffs as separate
36-cell surfaces.

## 2026-09-27 D005

Admit the 21-coordinate ProjectManager control surface as the tool-system
project-control completeness basis. Goal, stakeholders, schedule, resources,
and communications receive separate project-level owners.

## 2026-09-27 D006

A current tool is not development-sweep complete merely because its configured
route is reachable. The every-tool campaign requires a native/project-grounded
execution disposition for every current registered tool, with ToolConductor's
self-witness as the only explicit self-reference exception.

## 2026-09-27 D007

TOOL_INDEX.md is a navigational projection and must remain in exact set/count
parity with runtime/tool_run_registry.py.

## 2026-10-14 D008 — Approved logical 36-coordinate schema

Approval source: explicit user message `Approved.` on 2026-10-14, in direct response to the exact physical-to-logical coverage GOAL replacement recorded in `projects/tool-system/OPEN_QUESTIONS.md`. This is specific authorization for that proposal, not blanket authorization to change unrelated goals.

Old success condition: `every package has its required owned control surfaces and 36 Scope x ModeFace coverage pages`.
New success condition: every package retains exactly 36 independently addressable logical Scope x ModeFace coordinates, with empty coordinates allowed in one manifest/typed registry and actual findings independently addressable and append-only with provenance. The distinct SourceScope x TargetScope handoff is unchanged.

Canonical GOAL mutation: `4daf9e9d78f233fb16efd127ff3493234f075720`, readback confirmed. Propagated package-contract change: `69e0c5e781b0c537384acbf6a29f1e61ec1c7003`; regression-contract change: `61053e17366441336747e166241bd06b83dae0c4`. All are Take-5 `main` commits. Affected: package generator, tests, 140 package consumers, source-map/navigation and Knowledge Web file-node accounting. Physical deletion is a separate implementation step, not certified merely by this decision; preserve original historical Git blobs.
