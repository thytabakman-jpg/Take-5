# Tool Project Regression Contract

Status: CURRENT CANDIDATE

CI must detect:

1. a registered current tool without a package;
2. a package without required core pages;
3. any package whose Scope x ModeFace coverage is not exactly 36 cells;
4. a generator attempt to overwrite edited package content;
5. append-stream record ID reuse;
6. an ICC alias that creates a second mutable package authority;
7. accidental promotion of a historical ICC variant into current configured-tool status;
8. disappearance of explicit OPEN status from unrecovered variants;
9. conflation of Scope x ModeFace with SourceScope x TargetScope;
10. loss of current source pointers after a registry/manifest/runtime change.

## Required coverage versus observed enforcement

These ten items are **regression obligations**, not a statement that the linked test suite has already demonstrated all ten negative cases. In particular, a static source-map assertion does not by itself establish item 10: detecting pointer drift **after** a registry, manifest, or runtime change requires a change-sensitive consumer check or a negative-control mutation test.

The linked package tests exercise configured-tool/package parity, required pages and 36-cell coverage, the materializer overwrite guard, immutable append-stream identifiers, historical alias/open-state constraints, and some concrete source-map assertions. Before reporting **all ten CI obligations enforced**, map each item to an actually executed native test and check any missing change-sensitive case. Do not turn this current candidate contract into a passing CI certificate based on its wording or link existence alone. Follow the current test and workflow result; failures and untested obligations remain explicit.

Primary executable guard:

[runtime/tool_project_packages.py](../../runtime/tool_project_packages.py)
[tests/test_tool_project_packages.py](../../tests/test_tool_project_packages.py)
