# Source map: GOAL

## Live GOAL binding

For the **configured Take-5 GOAL tool**, resolve current authority from the
machine-owned registry and manifest rather than from file date, nearby source
names, cached text, or the historical `CURRENT` label on a predecessor.

- Current protected mathematical specification: [GOAL_FULL_TOOL_MATH_002_2026-09-30.md](../../../../architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md).
- Executable configured entrypoint: [`goal.recover_goal_configured`](../../../../runtime/goal.py), requiring the robust-MT preflight receipt.
- Current specification selector: [`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py), `manifest_for("GOAL").lineage_contract`.
- Current entrypoint selector: [`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py), `compilation_witness("GOAL").entrypoint`.

If the manifest, configured entrypoint, and this source map disagree, preserve
`OPEN` and reconcile the actual selectors before claiming current GOAL execution.
Neither an older numbered specification nor a Reaserch discovery link can silently
replace the active Take-5 configured-tool contract. Independent Reaserch canonical
goals remain governed by their own source authority and approval rules.

## Direct sources

- [`runtime/tool_run_registry.py`](../../../../runtime/tool_run_registry.py)
- [`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py)
- [`runtime/portable_tool_conductor.py`](../../../../runtime/portable_tool_conductor.py)
- [`runtime/mt_semantic_return_gate.py`](../../../../runtime/mt_semantic_return_gate.py) — required robust-MT preflight source, not an execution witness.
- [`runtime/configured_hf2_execution.py`](../../../../runtime/configured_hf2_execution.py) — downstream consumer if configured HF2 is selected.
- [`runtime/hf002_recursive_continuation.py`](../../../../runtime/hf002_recursive_continuation.py) — downstream HF2 recurrence implementation.
- [`integration/CURRENT_TOOL_REALITY.md`](../../../../integration/CURRENT_TOOL_REALITY.md)

## Shared current authorities

- [`runtime/tool_run_registry.py`](../../../../runtime/tool_run_registry.py)
- [`runtime/tool_manifest.py`](../../../../runtime/tool_manifest.py)
- [`integration/CURRENT_TOOL_REALITY.md`](../../../../integration/CURRENT_TOOL_REALITY.md)
- [`projects/tool-system/AUTHORITY_REGISTRY.md`](../../../../projects/tool-system/AUTHORITY_REGISTRY.md)

## GOAL mathematics and retained lineage

- **Active configured-tool specification:** [`architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md`](../../../../architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md), the manifest-selected successor adding the robust-MT preflight.
- **Earlier historical basis, not an alternate current selector:** [`architecture/GOAL_FULL_TOOL_MATH_001_2026-09-27.md`](../../../../architecture/GOAL_FULL_TOOL_MATH_001_2026-09-27.md). Preserve its original status and evidence as history; the selector is the manifest, not the older file's historical admission label.
- **Native implementation:** [`runtime/goal.py`](../../../../runtime/goal.py).
- **Regression witnesses:** [`tests/test_goal.py`](../../../../tests/test_goal.py) and [`tests/test_goal_fullmath_identity.py`](../../../../tests/test_goal_fullmath_identity.py).

## Cross-repository GOAL provenance (discovery only; not configured-tool authority)

- [Reaserch — typed GOAL entry and semantics](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_TYPED_CURRENT_003_2026-10-07.md)
- [Reaserch — nested-goal architecture](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_NESTED_BOX_ARCHITECTURE_001_2026-10-08.md)
- [Reaserch — intentional-object ontology](https://github.com/thytabakman-jpg/Reaserch/blob/main/INTENTIONAL_OBJECT_ONTOLOGY.md)
- [Reaserch — goal change policy](https://github.com/thytabakman-jpg/Reaserch/blob/main/GOAL_CHANGE_POLICY.md)

These links preserve discoverability, including independently governed project
goals. They are **not** alternative selectors for the configured Take-5 GOAL
runtime or mathematical identity. Cross-repository transfer of a semantic
contract requires separately admitted reconciliation; no newer filename or
external metadata automatically changes Take-5's manifest or Reaserch's
canonical goal authority.

## Rule

Pointers preserve provenance. This package does not copy legacy evidence merely
to make the folder look complete.

## Cross-repository reconciliation (derived navigation; no promotion)

- [Take-5/Reaserch crosswalk](../../SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer) — all current packages, catalogued formal objects and unresolved differences.
- [Reaserch `GOAL` (K2) catalog entry](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/FORMAL_TOOL_CATALOG_CURRENT.yaml) and [its current semantic locator](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_TYPED_CURRENT_003_2026-10-07.md). Matching names permit navigation, not automatic semantic equivalence or runnable integration.
- Take-5 configured-run authority remains [registry](../../../../runtime/tool_run_registry.py), [manifest](../../../../runtime/tool_manifest.py), [conductor](../../../../runtime/portable_tool_conductor.py). See [mathematics](MATHEMATICS.md), [runtime](RUNTIME.md), [dependencies](DEPENDENCIES.md), [regression contract](REGRESSION_CONTRACT.md).
- Native evidence surfaces are [runs](runs/README.md), [evidence](evidence/README.md), [coverage](coverage/README.md) and [history](history/README.md); a file link is not proof that configured execution or certification passed.
- [Take-5 native implementation runtime/goal.py](../../../../runtime/goal.py); native function availability alone is not configured-run proof.
- [Take-5 test tests/test_goal.py](../../../../tests/test_goal.py); assess its actual test scope before claiming coverage.
- [Take-5 test tests/test_goal_fullmath_identity.py](../../../../tests/test_goal_fullmath_identity.py); assess its actual test scope before claiming coverage.

**Owner boundary:** Do not copy mathematical truth between repositories or infer current runtime promotion from this source map. Mark unresolved mismatches OPEN and check the specialist owner.
