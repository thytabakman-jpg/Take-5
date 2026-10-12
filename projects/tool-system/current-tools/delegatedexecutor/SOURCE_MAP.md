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

## Cross-repository reconciliation (derived navigation; no promotion)

- [Full Take-5/Reaserch crosswalk](../../SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer).
- **UNMAPPED:** No one-to-one Reaserch formal catalog identity has been established for this separate Take-5 configured package. Do not classify it as absent or obsolete based on the other repository.
- The [Take-5 runtime registry](../../../../runtime/tool_run_registry.py), [manifest](../../../../runtime/tool_manifest.py), and [portable conductor](../../../../runtime/portable_tool_conductor.py) retain Take-5 configured-tool authority. See [mathematics pointer](MATHEMATICS.md), [runtime pointer](RUNTIME.md), [dependencies](DEPENDENCIES.md), and [regression contract](REGRESSION_CONTRACT.md).
- Inspect [runs](runs/README.md), [evidence](evidence/README.md), [coverage](coverage/README.md), and [history](history/README.md) for scoped proofs and actual execution receipts; links do not themselves certify a configured run.

No semantic owner, execution authority, tool species, or certification is transferred by this derived navigation. Unverified equivalence remains OPEN.
