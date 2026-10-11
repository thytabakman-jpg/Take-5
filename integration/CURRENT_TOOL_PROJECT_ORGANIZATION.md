# Current Tool Project Organization

Date: 2026-09-27
Status: CURRENT / VALIDATED THROUGH PR #166
Authority: projects/tool-system/

**Inventory readback (2026-10-10, America/Toronto):** 95 current tool packages, 45 historical/variant packages, 140 packages total, and 5,040 coverage pages from the checked tree. The 93-tool PR #166 native sweep below remains an exact **historical** execution result; it is not evidence that its 92 native runs covered later-admitted tools. [Live index](../projects/tool-system/TOOL_INDEX.md) · [source ownership](../projects/tool-system/AUTHORITY_REGISTRY.md).

## Contents

- [Current organization](#current-organization)
- [Anti-loss invariant](#anti-loss-invariant)
- [Two 36-cell structures](#two-36-cell-structures)
- [Exhaustive current-repertoire sweep](#exhaustive-current-repertoire-sweep)
- [Regression enforcement](#regression-enforcement)
- [Currentness](#currentness)

## Current organization

The tool/ICC ecosystem uses a non-destructive project-package architecture.

Current configured tools: 95.
Recovered/historical/unresolved ICC/IC variants: 45.
Total object packages: 140.
Scope x ModeFace coverage pages: 5,040.

Every package separately owns package-local current state, authority routing,
identity routing, source map, open questions, change control, regression contract,
append-only decisions/lessons/evidence/runs/history, and one page per coverage
coordinate.

The tool-system project itself now also exposes every native ProjectManager
coordinate, including separate goal, stakeholders, schedule, resources, and
communications authorities.

## Anti-loss invariant

Existing mathematics, runtime implementations, proofs, lineage, and historical
evidence remain in their original canonical locations.

Packages point to those authorities. They do not become second editable copies.

Package generation is create-only and fails closed when an existing file differs.

## Two 36-cell structures

Per-tool project coverage:

Scope x ModeFace = 36.

Semantic directed handoff:

SourceScope x TargetScope = 36.

These remain different typed surfaces.

## Exhaustive current-repertoire sweep

PR #166 adds an executable every-tool development sweep.

For the **PR #166-era 93-tool** repertoire (historical snapshot):
- 92 registered tools executed through native/project-grounded development bindings;
- ToolConductor supplied its required self-witness;
- zero tools remained OPEN;
- ProjectManager closed with all 21 native project coordinates present;
- full configured invocation coverage closed for the complete repertoire;
- protected transition, historical replay, reachability, tool reality, package
  reality, cleanup, capability-preservation, and whole-system audits passed.

Every-tool workflow run 36348207101: SUCCESS.

The synthetic full-invocation portfolio remains a route/profile witness only.
Native development execution is recorded separately so reachability is never
misreported as semantic execution.

## Regression enforcement

- runtime/tool_project_packages.py
- tests/test_tool_project_packages.py
- runtime/tool_system_every_tool_sweep.py
- tests/test_tool_system_every_tool_sweep.py
- .github/workflows/a5-tests.yml
- .github/workflows/tool-system-every-tool-sweep.yml

Any projects/tool-system/** change triggers full Take-5 validation and the
every-tool development sweep.

## Currentness

Current live tool inventory remains owned by runtime/tool_run_registry.py.
Historical ICC/IC variant provenance is project-owned data under
projects/tool-system/ICC_VARIANT_SOURCES.json.

New current tools reopen exactly these obligations:
1. per-tool package materialization;
2. tool-index parity;
3. full configured route coverage;
4. native development binding/run;
5. regression and capability-preservation validation.

They do not justify rebuilding or rewriting unaffected packages.
