# Source map: DelegatedExecutor

## Direct sources

- [runtime/tool_run_registry.py](../../../../runtime/tool_run_registry.py)
- [runtime/tool_manifest.py](../../../../runtime/tool_manifest.py)
- [runtime/portable_tool_conductor.py](../../../../runtime/portable_tool_conductor.py)
- [runtime/delegation.py](../../../../runtime/delegation.py) — the actual bounded `delegation.delegate` implementation, selected by the conductor
- [integration/CURRENT_TOOL_REALITY.md](../../../../integration/CURRENT_TOOL_REALITY.md)

## Executable regression witnesses

- [tests/test_delegation_lineage.py](../../../../tests/test_delegation_lineage.py) — local execution, receipt hashes, bounded authority, and gated lineage updates
- [tests/test_explicit_native_manifests.py](../../../../tests/test_explicit_native_manifests.py) — explicit DelegatedExecutor manifest and tool reality on the audited registry

## Shared current authorities

- [runtime/tool_run_registry.py](../../../../runtime/tool_run_registry.py)
- [runtime/tool_manifest.py](../../../../runtime/tool_manifest.py)
- [integration/CURRENT_TOOL_REALITY.md](../../../../integration/CURRENT_TOOL_REALITY.md)
- [projects/tool-system/AUTHORITY_REGISTRY.md](../../../../projects/tool-system/AUTHORITY_REGISTRY.md)

## Rule

Pointers preserve provenance. This package does not copy legacy evidence merely
to make the folder look complete.
