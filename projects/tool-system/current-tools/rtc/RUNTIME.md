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
- [C48 evaluator](../../../../runtime/a5_programs.py) filters truthy `strict_gain` and `preserves` fields; otherwise returns `NOOP` with `NO_STRICT_GAIN_FOUND`.
- [Native RTC specialization test](../../../../tests/test_recovered_native_tools_20260927.py) checks an accepted and a non-gaining candidate.

**OPEN:** This implementation does not verify coverage of every declared protected property. A source link or static package check is not an executed tool or proof of that stronger property.
