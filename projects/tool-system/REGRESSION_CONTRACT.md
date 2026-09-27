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


## Tool operational identity dimensions

Every registered current tool must pass the canonical master identity projection
defined by:

architecture/TOOL_OPERATIONAL_IDENTITY_CONTRACT_172_2026-09-27.md

and executed by:

runtime/tool_identity_dimensions.py.

The enforced union includes the operational nucleus, native/configured
mathematics, stewardship/currentness, runtime/reachability, invocation/run/host
boundaries, protected behavior, stopping/reentry, evidence/admission and
configured discovery surfaces.

Exact dimension names are owned by
runtime/tool_identity_dimensions.py::MASTER_DIMENSION_NAMES.

CI must fail on:

1. registry/projection set mismatch;
2. a missing operational nucleus;
3. an empty master coordinate;
4. a missing or incomplete configured/manifest identity;
5. a strong-reality failure for a routed runtime coordinate;
6. a tool-name-only or generic placeholder substituted for unrecovered
   result-sensitive semantics;
7. a future tool admitted without a complete master projection.

This contract deliberately points to the canonical executable dimension set
instead of copying a shorter list that can drift.
