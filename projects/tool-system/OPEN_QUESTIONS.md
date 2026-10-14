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

**Related distinct candidate:** [ICC129 design under ImprovementCore](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/architecture/ICC129_TOOL_DESIGN_CANDIDATE.md). Its goal, primary job and responsibility **remain unagreed**; tool-improvement is at most a capability. Deciding 56-page package compression is a pre-admission shared Tool System architectural job, not an ICC129-specific research result or an argument for registering ICC129.

## Full 140-package empty-cell discovery — 2026-10-13

**Verified frozen Take-5 main** `1478731ab88e8edd8ae8af15ab4519126a702d99`: the complete non-truncated Git tree has **9,909 tracked paths**, including **5,040 numbered Scope x ModeFace coverage Markdown cells in 140 tool/variant packages** (95 current tools + 45 ICC/IC variants). Every one of the 5,040 Git blob SHA-1 identities matched the current generated **empty-cell template exactly** (with separately verified GOAL and MultiObject variants). None of these 5,040 files holds an admitted independent finding. This is a content-addressed, repo-wide result, much stronger than only sampling one package.

**Protected exception:** a separate generator-equivalence audit found **7 non-template core files** (2 manifests: GOAL, DelegatedExecutor; 5 regression contracts: ProjectManager, GOAL, MultiObject, DelegatedExecutor, Prose). Their independently authored additional substance is protected. All 140 logical sets of 36 coordinates must survive; the directed SourceScope × TargetScope surface is different and unaffected.

**Proposed safe decomposition, not applied:** Retire the 5,040 empty physical cell placeholders into stable **implicit/virtual 36-coordinate coverage** with a materialized evidence page **only when a finding exists**. Preserve Git lineage, manifest slots, package identity, append-only evidence and native tests; update the generator, existing core manifests/regression contracts and consumer links **atomically**. Validate behavior with fully populated and malicious/unknown-cell negative controls, source-map references, and full native testing. No mass deletion is authorized by this read-only audit.

**Required approval before deployment:** the current [Tool System GOAL](GOAL.md) explicitly requires 36 physical coverage pages per package; the [package contract](PACKAGE_CONTRACT.md), generator and tests enforce them. A sparse regime changes that requirement and the canonical goal. Under the accepted [goal-change policy](https://github.com/thytabakman-jpg/Reaserch/blob/main/GOAL_CHANGE_POLICY.md), the operative GOAL change requires explicit user token `approved`. A preparatory branch exists at `candidate/tool-package-sparse-coverage-20261013`, but no deletion/contract replacement/merge was committed. This is **GOAL_CHANGE_APPROVAL_OPEN**, not a technical PASS or finished migration.

**ICC129 scope:** user expressly established a proposed **general-purpose, substantive-goal-relative controller across the available system**. Other-tool improvement is a selectable capability, not its governing job; [the original candidate design owner](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/architecture/ICC129_TOOL_DESIGN_CANDIDATE.md) records that distinction. Determine the tool's exact role against ICC128 only after the package-system cleanup.
