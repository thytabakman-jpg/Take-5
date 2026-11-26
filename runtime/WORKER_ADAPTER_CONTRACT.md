# Semantic Worker Adapter Contract 001

**Contract revision:** 1.1. This contract governs the controller–worker boundary; it does not replace individual tool mathematics, the registered invocation profile, or the host-specific binding ABI.

## Ownership and authority

The controller selects and reselects work. The worker performs substantive capability work within the selected scope. The worker cannot expand its authority, select unrelated work, promote its own result, or treat a proposed state delta as an authorized mutation. The controller retains admission, promotion and continuation decisions. A read-only grant permits analysis and proposals, not durable writes.

## Required input

Each worker invocation must identify the following semantic fields, whether conveyed as explicit keys or by a documented equivalent typed representation:

| Field | Required content |
| --- | --- |
| Frozen target | Stable object identity, exact revision or immutable snapshot, scope and relevant content |
| Typed state | Current admitted state and its schema or representation |
| Selected capability or package | Exact registered identity, applicable tool contract, intended operation |
| Corpus references | Evidence locators, source revisions and source-access limitations; explicit absence where relevant |
| Authority grant | Permitted operations, protected constraints and excluded mutations |
| Continuation basis | Prior admitted results, affected dependencies, unresolved obligations and stop conditions |
| Provider identity | Binding identity/version, input requirements and declared semantic coverage |

Missing material input remains OPEN; invalid or contradictory input is BLOCKED or CONFLICT as appropriate. A binding is not evidence that all semantic inputs are available. Do not fill missing evidence with invented labels or infer authorization from tool selection.

## Required output

| Field | Required content |
| --- | --- |
| Result | Typed findings tied to the target and the tool's actual job |
| Evidence and provenance | Source locators, input and provider identity, method, and grounds for each material finding |
| Execution truth | What actually ran and the extent to which the selected capability was applied |
| Target effect | Material findings or changes, affected objects and dependency footprint |
| Open obligations | Missing inputs, conflicts, coverage exclusions, failed prerequisites and blockers |
| Proposed state delta | Explicit candidate change or no change; never implicit promotion |
| Verification hooks | Testable expected consequences, non-regression obligations and applicable verification method |
| Continuation signal | Material successor, local frontier, affected scope, or grounds for stopping |

Preserve the native tool's own result vocabulary and the host's documented envelope; mapping between them must preserve unresolved obligations and cannot upgrade success. Follow the [current invocation guide](../integration/CURRENT_FULL_TOOL_INVOCATION.md) for configured execution. Binding alone does not establish worker availability or semantic adequacy.

## Execution evidence and coverage

- Implementation executed: the actual native entrypoint was invoked on identified inputs. This alone does not establish semantic correctness.
- Semantically applied: evidence establishes the selected capability was substantively applied to the declared target and scope; any exclusions remain explicit.
- Full match: all applicable tool-specific requirements and configured semantic coverage have been evidenced. A complete plan or bounded result is insufficient.
- OPEN, BLOCKED and CONFLICT remain distinct dispositions. An unresolved material obligation prevents closure of its affected claim. Independent work may retain its own valid result.

Configured HF2 recurrence belongs to the shared execution boundary, not to a replacement worker loop. A worker must expose material successors and unresolved affected-scope obligations rather than claiming a fixed point prematurely.

Independent verification requires an actually independent method or evaluator with an identified basis. Repeated same-context judgment, self-reported success, synthetic interface tests and source availability alone do not establish it.

## Compatibility and admission

This semantic contract does not impose a universal Python signature, replace existing result schemas, or certify providers by declaration. Existing bindings may retain their ABI through documented mappings. New or changed providers must declare supported inputs and outputs, scope, failure behavior and evidence limits; verify the affected consumers before changing an existing interface. Explicitly distinguish missing binding, missing input, invalid input and execution failure. No generic worker is silently substituted for a tool-specific provider.

