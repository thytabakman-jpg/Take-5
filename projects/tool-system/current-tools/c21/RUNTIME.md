# Runtime pointer: C21

Current runtime realization is owned by:
- [portable tool conductor](../../../../runtime/portable_tool_conductor.py) — orchestration entrypoint
- [tool manifest](../../../../runtime/tool_manifest.py) — locate configured runtime implementation
- [tool-run registry](../../../../runtime/tool_run_registry.py) — resolve identity before dispatch
- [source map](SOURCE_MAP.md) — provenance and configuration distinctions
- [runs](runs/README.md) and [evidence](evidence/README.md) — inspect actual execution receipts

This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.
