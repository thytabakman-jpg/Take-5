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
10. loss of current source pointers after a registry/manfest/runtime change.

Primary executable guard:

runtime/tool_project_packages.py
tests/test_tool_project_packages.py
