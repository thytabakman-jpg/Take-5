# Tool Project Regression Contract

Status: CURRENT REGRESSION OBLIGATIONS; actual certification depends on current native evidence

CI must detect:

1. a registered current tool without a package;
2. a package without required core pages;
3. any package whose Scope x ModeFace coverage does not preserve exactly 36 addressable logical coordinates, or silently discards a populated, modified, unknown or provenance-bearing coordinate;
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

The approved 2026-10-14 goal permits manifest/registry representation of empty coordinates. The checks must distinguish 36 logical coordinates from an unnecessary 36-file physical requirement; retained source evidence, anti-overwrite, namespace separation and native consumer routing remain protected.

Primary executable guard:

[runtime/tool_project_packages.py](../../runtime/tool_project_packages.py)
[tests/test_tool_project_packages.py](../../tests/test_tool_project_packages.py)

## Current cross-repository organization controls (2026-10-12)

- [Source-map parity and adversarial link checks](../../tests/test_tool_project_packages.py) compare each registered Take-5 configured package with the 95-row navigation table and reject swapped, missing, misclassified or duplicated rows.
- The same tests exercise template reentry, separately authored current-tool source-map preservation, and rejection of incorrect package identity, missing runtime/manifest pointers, incorrect alias-category status, and a missing crosswalk link.
- [Conductor identity tests](../../tests/test_portable_tool_conductor.py) require one factor per configured identity; duplicates fail before native tool execution.
- [Package generator](../../runtime/tool_project_packages.py) remains create-only for generated pages. Current-tool source maps are curated navigation objects with a narrow source-map admission guard; MultiObject retains byte-for-byte generator parity.

**Limits:** These checks do not establish external Reaserch-to-Take-5 equivalence, correct every unverified external URL, prove that a configured run executed from a source-map link, or close any missing change-sensitive consumer tests. A historical successful workflow does not certify future commits; consult the latest workflow result and source commit.
