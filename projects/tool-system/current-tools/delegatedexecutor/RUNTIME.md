# Runtime pointer: DelegatedExecutor

Current runtime realization is owned by:
- [runtime/portable_tool_conductor.py](../../../../runtime/portable_tool_conductor.py) — selects `delegation.delegate` with an externally supplied `worker`
- [runtime/delegation.py](../../../../runtime/delegation.py) — implements bounded in-process delegation and returns an input/output-hash receipt
- [runtime/tool_manifest.py](../../../../runtime/tool_manifest.py) — names the dedicated native identity and protected binding

The `reintegrated` field on the delegation receipt records in-call return of the worker result with its receipt; it is **not** evidence of a durable parent-state commit, external scheduling, downstream admission, or closed parent workflow. Those require separate owner/consumer evidence.

This package records organization and source routing only.

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.
