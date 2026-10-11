# Dependencies: DelegatedExecutor

## Canonical dependencies

- [runtime/tool_run_registry.py](../../../../runtime/tool_run_registry.py)
- [runtime/tool_manifest.py](../../../../runtime/tool_manifest.py)
- [runtime/portable_tool_conductor.py](../../../../runtime/portable_tool_conductor.py)
- [integration/CURRENT_TOOL_REALITY.md](../../../../integration/CURRENT_TOOL_REALITY.md)

## Shared runtime/identity dependencies

These overlap with the canonical dependency set because they also serve the shared identity/runtime substrate; repeated listing does not create an independent authority or a second copy.

- [runtime/tool_run_registry.py](../../../../runtime/tool_run_registry.py)
- [runtime/tool_manifest.py](../../../../runtime/tool_manifest.py)
- [runtime/portable_tool_conductor.py](../../../../runtime/portable_tool_conductor.py)

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.
