# Dependencies: Architecture

## Current Take-5 execution dependency chain

1. [tool_run_registry.py](../../../../runtime/tool_run_registry.py) — sole registered current ID `Architecture`; do not register `Architect` as a second configured tool by string similarity.
2. [tool_manifest.py](../../../../runtime/tool_manifest.py) — protected behaviour / configured geometry / closure requirements.
3. [portable_tool_conductor.py](../../../../runtime/portable_tool_conductor.py) — configured wrapper/factor route and native-entrypoint declaration.
4. [architecture_analysis.py](../../../../runtime/architecture_analysis.py) — actual native `AA_K(A)` result carrier and protected-constraint checks.
5. Caller-supplied `analyze_architecture` — environment-specific analyzer; without a correctly typed adapter, do not infer successful native execution.
6. [CURRENT_TOOL_REALITY.md](../../../../integration/CURRENT_TOOL_REALITY.md) — strong-reality evidence gate, including its currentness limitations.

## Affected tests and conditional GOAL interface

- [Native Architecture recovery tests](../../../../tests/test_four_tool_recovery_20260927.py).
- [Protected unit-job behaviour tests](../../../../tests/test_prose_transition_layers.py).
- [Reaserch hierarchical GOAL–Architect contract](https://github.com/thytabakman-jpg/Reaserch/blob/main/projects/improvement-core/tool-ecosystem/GOAL_ARCHITECT_META_RECURSION_CONTRACT_001_2026-10-02.yaml) — separately governed **conditional integration**, not evidence that the Take-5 runtime already executes same-level pairing, parent ascent, or directed scope handoff. See [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).

A modification to a source in this chain reopens its impacted downstream
consumer or test, not every unrelated tool package. The two distinct 36-cell
surfaces remain typed separately.

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.
