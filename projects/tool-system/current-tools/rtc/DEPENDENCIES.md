# Dependencies: RTC

## Canonical dependencies

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py
- integration/CURRENT_TOOL_REALITY.md

## Shared runtime/identity dependencies

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.

## RTC native functional dependency cone

- [RTC configured entrypoint](../../../../runtime/raise_the_ceiling.py)
- [Capability dispatch](../../../../runtime/capability_runtime.py)
- [C48 evaluation](../../../../runtime/a5_programs.py)
- [Native specialization regression](../../../../tests/test_recovered_native_tools_20260927.py)
- [Configured conductor regressions](../../../../tests/test_portable_tool_conductor.py)
- [Capability registry regressions](../../../../tests/test_a5_registry.py)
- [Manifest-selected native recovery specification](../../../../architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md)

A change to dispatch, C48 selection, manifest, registry or configured entrypoint reopens the affected consumers. The tests above do not alone establish complete protected-set coverage.
