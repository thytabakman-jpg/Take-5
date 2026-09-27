# Current Tool Project Organization

Date: 2026-09-27
Status: CURRENT / VALIDATED THROUGH PR #166
Authority: projects/tool-system/

## Current organization

The tool/ICC ecosystem uses a non-destructive project-package architecture.

Current configured tools: 93.
Recovered/historical/unresolved ICC/IC variants: 45.
Total object packages: 138.
Scope x ModeFace coverage pages: 4,968.

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

For the current 93-tool repertoire:
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
