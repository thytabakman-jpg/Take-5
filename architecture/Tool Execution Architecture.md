# Tool Execution Architecture


## Authority and reader route

This document owns the architectural invariant, formal justification and protected behaviour of full configured invocation. [Tool Execution Guide](../integration/Tool%20Execution%20Guide.md) is its operational recovery and routing summary, not an independent competing definition. The live registry, manifest and execution implementations remain the authorities for exact registered identities and executable behavior. Preserve any discrepancy as OPEN pending owner verification; do not infer semantic coverage from a routing summary.

## Problem

Plan completeness does not entail full invocation. A one-shot adapter call can use a complete plan while bypassing configured recurrence. Full invocation therefore requires both the complete registered plan and the actual configured execution path.

## Registered recurrence law

Let R be the current registered tool repertoire.

Define:

Rec(T)
=
SELF
when T = HF002,

and

Rec(T)
=
HF002
otherwise.

For every T in R, the current ConfiguredRunSpec carries:

```text
<
wrapper_required,
mode,
geometry,
native_layers,
question_families,
cognitive_operators,
closure,
reentry,
open_preservation,
PTI,
recurrence_required,
recurrence_engine,
invocation_profile
>
```

The invocation profile is:

FULL_CONFIGURED_HF2_V1.

## Full plan

For registered T:

```text
Plan(T)
=
<
T,
OBSERVER,
Wrapper,
D36_C,
Recurrence,
Native(T) x D36_C,
Q_01..Q_22 x D36_C,
{DIFFERENTIATE,RELATE,RECONSTRUCT,STRENGTHEN} x D36_C
>.

Let D = Scope x ModeFace (the canonical D36_C cells),
Q = {Q01,...,Q22},
C = {DIFFERENTIATE,RELATE,RECONSTRUCT,STRENGTHEN},
and N(T) = the nonempty registered native layer set for T.

PlanComplete(T)

iff the configured spec is complete and the plan has:

Mode(T) = OBSERVER
and Wrapper(T)
and Geometry(T) = D36_C
and Cells(T) = D, each cell exactly once
and Native(T) = N(T) x D, each projection exactly once
and Questions(T) = Q x D, each projection exactly once
and Cognitive(T) = C x D, each projection exactly once
and RecurrenceRequired(T)
and RecurrenceEngine(T) = Rec(T)
and InvocationProfile(T) = FULL_CONFIGURED_HF2_V1.

Consequently |D| = 36, |Questions(T)| = 792,
|Cognitive(T)| = 144, and |Native(T)| = 36 x |N(T)|.
```

## Runtime invocation

The configured plan is constructed from the exact registered specification by [build_tool_execution_plan](../runtime/tool_execution_plan.py); [ConfiguredRunSpec.complete](../runtime/configured_run.py) validates the governing configuration. The cardinalities alone do not establish exact coverage or semantic execution.

For ordinary T:

```text
FullInvoke(T,x)
=
HF002[
    Adapter_T(
        Plan(T),
        x
    )
]
```

When upstream control permits local continuation, HF002 re-applies Adapter_T after every material local successor, even if that successor reports its live-local frontier inactive. A material successor cannot certify its own fixed point: a subsequent non-material pass is required.

On a non-material pass, unresolved affected-scope obligations or a still-live local frontier preserve OPEN. Relative closure additionally requires the local-close condition. Upstream reentry, BLOCKED, CONFLICT and resource exhaustion retain their distinct dispositions under the HF002 contract.

For T = HF002:

FullInvoke(HF002,x)
=
HF002_SELF(x).

A second outer HF002 is not added.

## Repository routes

All repository-owned invocation routes converge on the shared configured plan and recurrence executor. The [operational guide](../integration/Tool%20Execution%20Guide.md#execution-routes) identifies the entrypoints.

- Direct commands and ImprovementCore-selected tools share `bind_selected_tools`, `build_tool_execution_plan` and `execute_configured_with_hf2`. The ordered binding must equal the authorized direct request. Inherited controller selections cannot add tools or veto a direct request merely by naming an unrelated unregistered identity.
- [Protected Transition Integrity](../runtime/global_tool_execution.py) consumes the shared [execution plan](../runtime/tool_execution_plan.py) and executes its execution edge through `execute_configured_with_hf2`. Execution callbacks may return `(value, evidence)` for a one-round local close or `(value, evidence, recurrence_hints)` for a material or live successor. Successful transitions retain configured recurrence evidence, for example `configured-recurrence:HF002:RELATIVE_CLOSE:rounds=n` or `configured-recurrence:SELF:SELF_CLOSE:rounds=1`. PTI forwards `hf2_affected_frontier` and `hf2_scope_deltas`; OPEN, BLOCKED, CONFLICT, RETURN_REENTER or RESOURCE_STOP cannot authorize successful transition.
- [ToolConductor](../runtime/portable_tool_conductor.py) emits one disposition per registered factor, not one native call. Each non-self factor that executes crosses the configured plan and recurrence executor and may take multiple HF2 rounds. The conductor self factor is a non-recursive self witness that prevents infinite conductor-on-conductor recursion. Missing environment-bound adapters remain OPEN/BLOCKED.

Inner native functions are implementations within a configured invocation, not independent evidence of full configured execution. The shared [configured HF2 executor](../runtime/configured_hf2_execution.py) owns the caller-facing recurrence disposition, admitted material-delta projection and recurrence receipt representation. Invocation routes consume these projections rather than reconstructing them independently. The protected-transition route retains its stricter transition-admission checks.

## Fail-closed rules

The direct gateway rejects recognized unregistered formal objects, including mixed requests, and identity mismatches before execution. A registered label cannot match the prefix of a longer hyphenated or word-token label. Unknown ordinary-language tokens are not assigned tool identities. Structured requests require a nonempty ordered list or tuple of unique exact registered string IDs; both structured and lexical requests converge on the same execution path.

Missing adapters preserve OPEN. Incomplete configured identities or invalid recurrence identities block execution. Unresolved local frontiers preserve typed HF2 non-closure.

Execution receipts establish only their evidenced scope. The [worker contract](Semantic%20Worker%20Contract.md#execution-evidence-and-coverage) defines execution truth and semantic evidence requirements; plan completeness, synthetic routing tests and bounded native results do not imply full semantic coverage.

## Protected reconstruction

Every generic tool manifest reconstructs:

CONFIGURED_HF2_RECURRENCE

and

FULL_CONFIGURED_INVOCATION_PROFILE.

ConfiguredRunSpec.complete() requires both.

Therefore recurrence is not merely an execution convention.

## Portfolio audit

The [portfolio audit](../runtime/full_invocation_portfolio.py) checks current registered identities, manifests, complete configured plans, direct command resolution, shared executor reachability, recurrence receipts and missing-adapter OPEN behaviour. Its synthetic adapters establish routing/profile reachability, not domain-semantic correctness.

## External host boundary

RepositoryOwnedFullInvocation
does not entail
UniversalHostInterception.

An external ChatGPT host that never invokes Take-5 can still bypass repository code.

That remains:

HOST_INTEGRATION_BYPASS = EXTERNAL_NOT_OWNED.

The direct gateway is a lexical command recognizer, not a natural-language authorization interpreter. The caller must establish that a command is genuinely requested rather than negated, quoted, hypothetical or otherwise non-operative before submitting it. This is a host responsibility, not a certified property of the regular-expression parser.

Inside a Take-5-governed formal-tool route, the weaker one-shot configured path is no longer
admissible.
