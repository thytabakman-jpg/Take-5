# OPEN questions: RTC

- package-specific open questions are added here only when they are not already owned by a canonical source

## Rule

OPEN is durable state. Closing an item requires evidence and a receipt; deleting
the line because a later summary is shorter is forbidden.

## C48 protected-set adequacy — OPEN

The [RTC runtime chain](RUNTIME.md) currently accepts C48 candidates when `strict_gain` and `preserves` are truthy. That is not a membership/coverage check for each declared protected property. Independently reconcile the [native C48 evaluator](../../../../runtime/a5_programs.py), [manifest-bound preservation contract](../../../../runtime/tool_manifest.py), [recovery specification](../../../../architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md) and [native regressions](REGRESSION_CONTRACT.md) before asserting full protected-basis preservation. This is a **source/verification obligation**, not proof that every higher-level RTC use violates preservation; maintain separate package-current and native-run statuses.
