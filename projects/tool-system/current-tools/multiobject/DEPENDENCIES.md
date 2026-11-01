# Dependencies: MultiObject

## Canonical dependencies

- [Configured-run registry](../../../../runtime/tool_run_registry.py)
- [Protected tool manifest](../../../../runtime/tool_manifest.py)
- [Portable invocation conductor](../../../../runtime/portable_tool_conductor.py)
- [Current tool reality](../../../../integration/CURRENT_TOOL_REALITY.md)

## Shared runtime/identity dependencies

The registry, manifest, and conductor above are shared runtime/identity
authorities. The current-tool-reality source supplies the separate
currentness and execution-evidence boundary.

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.

## MultiObject native dependency edges

- [Native relation-discovery executor](../../../../runtime/multiobject.py)
- [Full-tool mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)
