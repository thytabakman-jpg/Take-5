# Runtime pointer: MultiObject

Current runtime realization is owned by:
- runtime/portable_tool_conductor.py
- current dedicated runtime modules referenced by runtime/tool_manifest.py

This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.

## MultiObject executable route

- [Native runtime implementation](../../../../runtime/multiobject.py) — `run_multiobject`
- [Portable invocation conductor](../../../../runtime/portable_tool_conductor.py) — `multiobject.run_multiobject`
- [Native runtime tests](../../../../tests/test_multiobject.py)

Domain relation generation requires an explicit `multiobject_provider`. Absence of the provider cannot be reported as successful domain execution. This package remains an organizational projection.
