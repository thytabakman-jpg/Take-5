# Runtime pointer: RTC

Current runtime realization is owned by:
- runtime/portable_tool_conductor.py
- current dedicated runtime modules referenced by runtime/tool_manifest.py

This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.

## RTC configured-to-native chain and verified scope

- [Portable conductor](../../../../runtime/portable_tool_conductor.py) selects `raise_the_ceiling.raise_the_ceiling` for RTC.
- [RTC entrypoint](../../../../runtime/raise_the_ceiling.py) calls `execute_capability("C48", payload)`.
- [Capability dispatcher](../../../../runtime/capability_runtime.py) sends C48 to `run_generic`.
- [C48 evaluator](../../../../runtime/a5_programs.py) accepts a candidate only when `strict_gain` and `preserves` are both explicitly `True`. An explicitly `False` field excludes a candidate; missing or non-Boolean evidence remains unresolved unless the other field excludes it. The evaluator returns `ACCEPT` with admitted candidates and any unresolved candidates, `OPEN` for an absent or invalid inventory or unresolved candidates without an admitted candidate, and `NOOP` with `NO_STRICT_GAIN_FOUND` only when no candidate is admitted or unresolved.
- [Native RTC specialization test](../../../../tests/test_recovered_native_tools_20260927.py) checks accepted and non-gaining candidates, missing inventories, non-Boolean evidence and mixed admitted/unresolved results.

**OPEN:** This implementation does not verify coverage of every declared protected property. A source link or static package check is not an executed tool or proof of that stronger property.
