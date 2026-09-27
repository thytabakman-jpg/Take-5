# Current Tool Project Organization

Date: 2026-09-27
Status: VALIDATED CANDIDATE / PR #163
Authority: projects/tool-system/

## Current organization

The tool/ICC ecosystem now uses a non-destructive project-package architecture.

Current configured tools: 92.
Recovered/historical/unresolved ICC/IC variants: 45.
Total object packages: 137.
Scope x ModeFace coverage pages: 4,932.

Every package separately owns package-local current state, authority routing,
identity routing, source map, open questions, change control, regression contract,
append-only decisions/lessons/evidence/runs/history, and one page per coverage
coordinate.

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

## Regression enforcement

runtime/tool_project_packages.py
tests/test_tool_project_packages.py
.github/workflows/a5-tests.yml

Any projects/tool-system/** change now triggers the full Take-5 Validation workflow.

Validation run 36334999109: SUCCESS.
Capability Preservation run 36334999156: SUCCESS.

## Currentness

Current live tool inventory remains owned by runtime/tool_run_registry.py.
Historical ICC/IC variant provenance is project-owned data under
projects/tool-system/ICC_VARIANT_SOURCES.json.

New current tools or newly recovered historical variants reopen the corresponding
package/backfill obligation automatically; they do not justify rebuilding or
rewriting unaffected packages.
