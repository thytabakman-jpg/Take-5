# ICC128 (Take-5 configured) — Current Issues and Certification Frontier

**Job:** current inventory, per-file L2/L3/L4 evidence lookup and unresolved-repair frontier for the **Take-5 currently configured ICC128 package**. Identity lives at [IDENTITY.md](IDENTITY.md); the [manifest](MANIFEST.md) and [source map](SOURCE_MAP.md) own package and source definitions; [CURRENT_STATE.md](CURRENT_STATE.md) remains a distinct projection, and [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) retains its own source-specific questions.
**As observed:** 2026-10-14 Take-5 `main` tree; `20` already present package files plus this register = `21` present files. The manifest also reserves 36 *logical* coverage positions. A reserved logical position is **not** asserted to be a current physical file or an unmet certificate.
**Status:** `CENSUS_BOUNDED`, `CERTIFICATE_RECONCILIATION_OPEN`. Scope is this package's tracked files, **not** all transitively reachable tool ecosystem files.
**Critical distinction:** Reaserch [ICC128 Epic Mode](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/ICC128_EPIC_MODE_CURRENT.yaml) is a separate current semantic/runtime implementation, not automatically the Take-5 configured tool's runtime. Its dedicated [Epic live issue frontier](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/ICC128_EPIC_CURRENT_ISSUES.md) is linked, not duplicated.

## Configured ICC128 physical file census

`NV` means no **current native exact-SHA certification** has been confirmed and bound in *this* index, **not** failed/never certified.

| Source file | Independent file job | L2 | L3 | L4 |
| --- | --- | --- | --- | --- |
| [`README.md`](README.md) | Tool-package navigation | NV | NV | NV |
| [`MANIFEST.md`](MANIFEST.md) | Physical package manifest and reserved 36 coverage coordinates | NV | NV | NV |
| [`AUTHORITY_REGISTRY.md`](AUTHORITY_REGISTRY.md) | Configured authority registry | NV | NV | NV |
| [`CURRENT_STATE.md`](CURRENT_STATE.md) | Current configured state (not issue register) | NV | NV | NV |
| [`IDENTITY.md`](IDENTITY.md) | Current configured identity | NV | NV | NV |
| [`MATHEMATICS.md`](MATHEMATICS.md) | Configured mathematics | NV | NV | NV |
| [`RUNTIME.md`](RUNTIME.md) | Native runtime reference | NV | NV | NV |
| [`PROTECTED_BEHAVIORS.md`](PROTECTED_BEHAVIORS.md) | Nonregression behaviors | NV | NV | NV |
| [`DEPENDENCIES.md`](DEPENDENCIES.md) | Typed source dependencies | NV | NV | NV |
| [`SOURCE_MAP.md`](SOURCE_MAP.md) | Source and cross-repository routing | NV | NV | NV |
| [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) | Owner-specific open questions (not whole-file repair frontier) | NV | NV | NV |
| [`CHANGE_CONTROL.md`](CHANGE_CONTROL.md) | Change admission | NV | NV | NV |
| [`REGRESSION_CONTRACT.md`](REGRESSION_CONTRACT.md) | Native regression requirements | NV | NV | NV |
| [`DECISION_LOG.md`](DECISION_LOG.md) | Native decisions | NV | NV | NV |
| [`LESSONS_LEDGER.md`](LESSONS_LEDGER.md) | Native lessons | NV | NV | NV |
| [`HANDOFF_SURFACE.md`](HANDOFF_SURFACE.md) | Distinct 36-cell handoff | NV | NV | NV |
| [`evidence/README.md`](evidence/README.md) | Evidence home | NV | NV | NV |
| [`runs/README.md`](runs/README.md) | Runs home | NV | NV | NV |
| [`history/README.md`](history/README.md) | History home | NV | NV | NV |
| [`coverage/README.md`](coverage/README.md) | Coverage home | NV | NV | NV |
| [`CURRENT_ISSUES.md`](CURRENT_ISSUES.md) | This current cross-file issues/certificate lookup | NV | NV | NV |

## Live issues

- **ICC128-CI-001 — Native certificate reconciliation.** Latest Level 2/3/4 results, exact source SHAs, observed dates and receipt paths for all directly owned package files have not been independently populated. **Next:** bind exact current per-file native evidence; do not infer global PASS or FAILED from one package status. **OPEN**.
- **ICC128-CI-002 — Resolve real configured entry/host identity.** [SOURCE_MAP.md](SOURCE_MAP.md) names Take-5 `runtime/icc_entry.py` + episode adapter and a distinct Reaserch Epic controller. **Next:** verify actual entry and adapter for the intended invocation, with first-party runtime receipts; don't merge controller authorities by common name. **OPEN** for claimed cross-repo equivalence, not a blanket configured-runtime failure.
- **ICC128-CI-003 — Identify current shared repair/continuation blockers.** [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) is a specialist question home; [Reaserch Epic frontier](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/ICC128_EPIC_CURRENT_ISSUES.md) tracks the Epic run closure, host binding and certification reconciliation. **Next:** add only observed, source-bound issues genuinely affecting Take-5-owned files; never import all Epic issues as this package's obligations. **OPEN** as an unpopulated current-source projection.

- **ICC128-CI-004 — Verify configured-tool consumption of this register.** A link in README or an external Epic profile does **not** demonstrate Take-5's configured `icc_entry.py` or `ICC128EpisodeAdapter` loads current issues or writes back evidence. **Next:** add/verify an authorized native lookup and evidence-bound update hook in the configured entry only if that integration is selected; record an actual execution and source-SHA/receipt witness, preserving separate Reaserch Epic semantics. **State:** OPEN.

## Resume and closure discipline

Before each L4 attempt refresh the exact file and owner, native L2/L3/L4 receipts and **only directly justified required** dependencies. Collapse a shared defect to one live issue linked from each affected source. A report, generic folder link, ten-hop neighbor or historical audit is not a required dependency. Close a live issue after its appropriate *native* repair, test, merge/main readback and receipt, not merely on the existence of a branch or a promised later check. Preserve historic evidence where [history](history/README.md) or [runs](runs/README.md) already owns it. This register itself is not a controller, automatic monitor, historical log, or source of certification authority.
