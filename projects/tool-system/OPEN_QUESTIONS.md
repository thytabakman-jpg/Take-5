# Tool System OPEN Questions

Status: CURRENT

- whether additional conversation-only ICC labels exist beyond the recovered variant inventory
- whether any legacy same-number ICC labels require split packages after new identity evidence appears
- whether package-local dependency graphs warrant a richer machine-readable index after the first full migration
- universal external-host routing remains outside repository ownership

OPEN items do not block the organizational package migration when their unknown
content is explicitly preserved.

## Package-layout compression review — ICC128 sample, 2026-10-13

**Scope:** exact current `current-tools/icc128/` package, **20 core pages plus 36 Scope × ModeFace coverage cells**. All 56 files were read for an initial content-placement/duplication inspection. This is a **first-pass source review, not Level 2 certification, a full package-family census, or a release change**.

**Clear facts.** All **36 cell pages** presently say `Disposition: OPEN`, `none admitted yet`, and repeat the same generic open question and non-overwrite boilerplate; only identity, numbered coordinate, scope and mode differ. Therefore these pages currently hold **no independently admitted per-cell finding**, even though their *36 separate coordinates* remain semantically distinct. The 20 core pages contain several overlapping presentations: `DEPENDENCIES.md` repeats its own pointers and re-lists edges from `SOURCE_MAP.md`/`AUTHORITY_REGISTRY.md`; `MATHEMATICS.md`, `RUNTIME.md`, and `PROTECTED_BEHAVIORS.md` primarily route to canonical sources; `HANDOFF_SURFACE.md` repeats the distinct-two-36 rule owned also in the parent `TWO_36_SURFACES.md`; `README.md` and `SOURCE_MAP.md` repeat research navigation. The evidence/runs/history channel READMEs use the same generic boilerplate **but their independently append-only evidence roles are not redundant**.

**Misplacement versus duplication.** Detailed ICC128 science/historical-source listings are arguably more naturally located in `SOURCE_MAP.md` or their existing research owners than in the human-entry `README.md`; the current copies are **navigation, not displaced canonical scientific conclusions**. No material scientific claim was found misplaced in the 36 empty cells. `AUTHORITY_REGISTRY.md` routes current configured execution via `portable_tool_conductor.py` while `runtime/icc_entry.py` declares a canonical ICC128 entry; reconcile the two different execution layers before describing either as the sole complete native route. Do not silently rewrite either runtime source.

**OPEN optimization test.** Compare (A) current 56 physical pages with (B) **one structured 36-coordinate evidence registry plus generated per-cell navigation/views**, and (C) lazy/generated placeholders only for currently empty cells. Preserve all actual evidence, coordinate identity, append-only semantics, exact finding ownership, independent retrieval, historical revisions, two non-equivalent 36 surfaces, anti-overwrite, registry/package parity and tooling cost. Compare a fully populated cell and concurrent updates, not only today's empty sample. The current [package contract](PACKAGE_CONTRACT.md), [native generator](../../runtime/tool_project_packages.py), [native package tests](../../tests/test_tool_project_packages.py) and [regression contract](REGRESSION_CONTRACT.md) **require 20+36**; no removal, merge, source-owner change, or level certification is authorized by this proposal. Real native regression and existing-tool preservation remain required before any eventual contract revision.

**Current 2026-10-14 scope correction:** [ICC129 design under ImprovementCore](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/architecture/ICC129_TOOL_DESIGN_CANDIDATE.md) now treats ICC129 as the consolidation-and-web-integrated **successor name for ICC128 Epic**, preserving its controller semantics unless independently justified refinements pass regression. ICC129 does not require a distinct new mathematical law. The 36-page Tool System package requirement remains a separately governed shared infrastructure change; it does not define ICC129's mission.

## Full 140-package empty-cell discovery — 2026-10-13

**Verified frozen Take-5 main** `1478731ab88e8edd8ae8af15ab4519126a702d99`: the complete non-truncated Git tree has **9,909 tracked paths**, including **5,040 numbered Scope x ModeFace coverage Markdown cells in 140 tool/variant packages** (95 current tools + 45 ICC/IC variants). Every one of the 5,040 Git blob SHA-1 identities matched the current generated **empty-cell template exactly** (with separately verified GOAL and MultiObject variants). None of these 5,040 files holds an admitted independent finding. This is a content-addressed, repo-wide result, much stronger than only sampling one package.

**Protected exception:** a separate generator-equivalence audit found **7 non-template core files** (2 manifests: GOAL, DelegatedExecutor; 5 regression contracts: ProjectManager, GOAL, MultiObject, DelegatedExecutor, Prose). Their independently authored additional substance is protected. All 140 logical sets of 36 coordinates must survive; the directed SourceScope × TargetScope surface is different and unaffected.

**Proposed safe decomposition, not applied:** Retire the 5,040 empty physical cell placeholders into stable **implicit/virtual 36-coordinate coverage** with a materialized evidence page **only when a finding exists**. Preserve Git lineage, manifest slots, package identity, append-only evidence and native tests; update the generator, existing core manifests/regression contracts and consumer links **atomically**. Validate behavior with fully populated and malicious/unknown-cell negative controls, source-map references, and full native testing. No mass deletion is authorized by this read-only audit.

**Required approval before deployment:** the current [Tool System GOAL](GOAL.md) explicitly requires 36 physical coverage pages per package; the [package contract](PACKAGE_CONTRACT.md), generator and tests enforce them. A sparse regime changes that requirement and the canonical goal. Under the accepted [goal-change policy](https://github.com/thytabakman-jpg/Reaserch/blob/main/GOAL_CHANGE_POLICY.md), the operative GOAL change requires explicit user token `approved`. A preparatory branch exists at `candidate/tool-package-sparse-coverage-20261013`, but no deletion/contract replacement/merge was committed. This is **GOAL_CHANGE_APPROVAL_OPEN**, not a technical PASS or finished migration.

**ICC129 scope:** user expressly established a proposed **general-purpose, substantive-goal-relative controller across the available system**. Other-tool improvement is a selectable capability, not its governing job; [the original candidate design owner](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/architecture/ICC129_TOOL_DESIGN_CANDIDATE.md) records that distinction. Determine the tool's exact role against ICC128 only after the package-system cleanup.

**Completed safe content-home repair (not the 5,040-file reduction):** Take-5 commit [`3dbcfde5`](https://github.com/thytabakman-jpg/Take-5/commit/3dbcfde556dbfef3e1bc9a4141753bd8713e6aa3) relocated ICC128-specific research, bridge and historical source navigation from the `current-tools/icc128/README.md` into the existing `SOURCE_MAP.md`. The README now exactly equals the generator's minimal entry-page template (verified bytes); missing specialized links were conserved in the source map and both committed files were independently read back. **File count unchanged**, native regression execution and reader-link tests remain OPEN. The 5,040 blank-cell removal remains `GOAL_CHANGE_APPROVAL_OPEN`.

**ICC128 Epic continuation, 2026-10-14 — real preparatory code:** On the [unmerged candidate branch](https://github.com/thytabakman-jpg/Take-5/tree/candidate/tool-package-sparse-coverage-20261013), [`runtime/tool_package_sparse_migration.py`](https://github.com/thytabakman-jpg/Take-5/blob/candidate/tool-package-sparse-coverage-20261013/runtime/tool_package_sparse_migration.py) and [`tests/test_tool_package_sparse_migration.py`](https://github.com/thytabakman-jpg/Take-5/blob/candidate/tool-package-sparse-coverage-20261013/tests/test_tool_package_sparse_migration.py) are committed. The candidate scanner audits exact empty-template bytes, GOAL's link-only variant, modified/evidence-bearing cells, unknown and missing cells, and Markdown consumers pointing at candidate-retired pages. It makes **no deletions** and explicitly reports `delete_authorized=false`. The tests include positive/negative protections; **native pytest has not been run** in the unavailable checked-out runtime. This is a working-code preparatory branch, not a passing certification or an accepted Tool System goal change. Continue from its exact committed sources under ICC128 Epic's campaign, not from any outdated isolated file-count report.


## Physical 36-page requirement — exact canonical GOAL change proposal (not applied)

**Owner:** `projects/tool-system/GOAL.md`, success-condition line. **Current wording:**

`- every package has its required owned control surfaces and 36 Scope x ModeFace coverage pages;`

**Proposed replacement (single line; not a change to the distinct SourceScope x TargetScope handoff surface):**

`- every package has its required owned control surfaces and exactly 36 independently addressable Scope x ModeFace logical coverage coordinates; unpopulated coordinates may be represented in a single package manifest or evidence registry, while actual coordinate-specific findings retain independently addressable, append-only evidence with provenance;`

**Reason:** The 36 physical empty templates repeat no admitted evidence; the four-package candidate already preserves 36 separately named positions in each single `MANIFEST.md`, retaining 20 core files and zero empty numbered pages. **Do not confuse 36 logical coordinates with 36 required physical files.** Existing findings, unknown/changed cells and separate historical identities remain protected; no silent deletion is authorized.

**Affected consumers (migration conditional on approval):** `PACKAGE_CONTRACT.md`, `runtime/tool_project_packages.py`, `runtime/tool_package_sparse_migration.py`, generated package manifests and coverage indexes, `REGRESSION_CONTRACT.md` owners, `tests/test_tool_project_packages.py`, `tests/test_tool_package_sparse_migration.py`, old direct cell links and Knowledge Web source-node inventory. Preserve the existing curated exceptions and a rollback path. Require complete native test and readback evidence before any main-branch release or success claim.

**Status:** `GOAL_CHANGE_APPROVAL_OPEN`. Literal affirmative `approved` for this exact proposal is still required by `GOAL_CHANGE_POLICY.md`; `GOAL.md` has not changed. A candidate implementation exists on `candidate/tool-package-sparse-coverage-20261013` with 36 ICC128 numbered pages already absent **on that noncanonical branch only**. The main branch retains them.
