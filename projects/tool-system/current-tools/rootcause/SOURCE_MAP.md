# Source map: RootCause

## Direct sources

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py
- integration/CURRENT_TOOL_REALITY.md

## Shared current authorities

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- integration/CURRENT_TOOL_REALITY.md
- projects/tool-system/AUTHORITY_REGISTRY.md

## Opt-in external historical evidence (non-authoritative)

- `runtime/root_cause_managed.py` — RootCause child attachment and conditional historical consultation
- `runtime/root_cause_knowledge_lookup.py` — read-only, current-file projection over a separately bound Reaserch checkout
- `tests/test_root_cause_knowledge_lookup.py` — match, near-miss, private/no-access, no-match and non-interference tests
- [Reaserch question-first Root Cause knowledge entry](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/research/consolidations/ROOT_CAUSE_ROLLING_DISCOVERY_KNOWLEDGE.md) — discover original investigations without adopting their claims as current authority

The external research checkout is an optional historical source, not a source of canonical tool identity, executable repair permissions or causal ranking. No default payload change occurs without an explicit `research_root` binding. Approved consumers can invoke `python runtime/root_cause_knowledge_lookup.py --research-root /path/to/Reaserch "current observed failure"` and parse candidate/NO_MATCH/NO_ACCESS JSON. `record_verified_root_cause_outcome(...)` is an explicitly invoked post-repair connector to existing material or negative-learning memory, with required owner admission and verified current evidence; it is not a globally installed event hook.

## Rule

Pointers preserve provenance. This package does not copy legacy evidence merely
to make the folder look complete.

## Cross-repository reconciliation (derived navigation; no promotion)

- [Take-5/Reaserch crosswalk](../../SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer) — all current packages, catalogued formal objects and unresolved differences.
- [Reaserch `DIAGNOSIS` (K2) catalog entry](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/FORMAL_TOOL_CATALOG_CURRENT.yaml) and [its current semantic locator](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/core-system-mathematics/portable-20/ctir/root-cause_CTIR_001_2026-09-26.json). **ALIAS_COLLISION_OPEN:** Take-5 separately configures RootCause and Diagnosis, while Reaserch uses Root Cause as a DIAGNOSIS alias. No identity equivalence or merger is established.
- Take-5 configured-run authority remains [registry](../../../../runtime/tool_run_registry.py), [manifest](../../../../runtime/tool_manifest.py), [conductor](../../../../runtime/portable_tool_conductor.py). See [mathematics](MATHEMATICS.md), [runtime](RUNTIME.md), [dependencies](DEPENDENCIES.md), [regression contract](REGRESSION_CONTRACT.md).
- Native evidence surfaces are [runs](runs/README.md), [evidence](evidence/README.md), [coverage](coverage/README.md) and [history](history/README.md); a file link is not proof that configured execution or certification passed.
- [Take-5 native implementation runtime/root_cause.py](../../../../runtime/root_cause.py); native function availability alone is not configured-run proof.
- [Take-5 test tests/test_root_cause_hf2.py](../../../../tests/test_root_cause_hf2.py); assess its actual test scope before claiming coverage.

**Owner boundary:** Do not copy mathematical truth between repositories or infer current runtime promotion from this source map. Mark unresolved mismatches OPEN and check the specialist owner.
