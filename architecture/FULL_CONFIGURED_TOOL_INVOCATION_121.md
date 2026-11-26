# Full Configured Tool Invocation 121

Date: 2026-09-26
Status: CURRENT / MERGED; routing/profile validation is distinct from domain-semantic validation
Origin:
- MT direct-tool/HF2 prompt audit 118
- GOAL direct-tool/HF2 118
- IC123 rewrite 118
- ImprovementCore + HF2 campaign 119
- ImprovementCore + HF2 Think-big pass 120

## Contents

- [Authority and reader route](#authority-and-reader-route)
- [Problem](#problem)
- [Registered recurrence law](#registered-recurrence-law)
- [Full plan](#full-plan)
- [Runtime invocation](#runtime-invocation)
- [Repository routes](#repository-routes)
- [Fail-closed rules](#fail-closed-rules)
- [Protected reconstruction](#protected-reconstruction)
- [Portfolio audit](#portfolio-audit)
- [External host boundary](#external-host-boundary)
- [Post-merge Think-big reentry](#post-merge-think-big-reentry)
- [Strengthened route set](#strengthened-route-set)
- [Validation and merge evidence](#validation-and-merge-evidence)

## Authority and reader route

This document owns the architectural invariant, formal justification, protected behavior and validation provenance of full configured invocation. [Current Full Tool Invocation](../integration/CURRENT_FULL_TOOL_INVOCATION.md) is its operational recovery and routing summary, not an independent competing definition. The live registry, manifest and execution implementations remain the authorities for exact registered identities and executable behavior. Preserve any discrepancy as OPEN pending owner verification; do not infer semantic coverage from a routing summary.

## Problem

A registered tool could already have a complete wrapper/D36_C configured plan while a
caller still invoked its adapter through a one-shot path that did not bind HF2.

Therefore:

CompletePlan(T)

did not entail:

FullInvocation(T).

The user's recurring failure was the gap between those two objects.

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

The configured plan is constructed from the exact registered specification by [build_tool_execution_plan](../runtime/global_tool_execution.py); [ConfiguredRunSpec.complete](../runtime/configured_run.py) validates the governing configuration. The cardinalities alone do not establish exact coverage or semantic execution.

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

Controller-selected route:

ImprovementCore selection
-> bind_selected_tools
-> build_tool_execution_plan
-> execute_configured_with_hf2
-> native adapter.

Direct-command route:

"run/use/execute/apply/call T" or caller-authorized ordered exact registered IDs
-> direct_tool_command_gateway
-> bind_selected_tools
-> build_tool_execution_plan
-> execute_configured_with_hf2
-> native adapter.

These routes share the same binding and execution primitive.

The [direct command gateway](../runtime/direct_tool_command_gateway.py) binds exactly the ordered identities extracted from the authorized direct command. Inherited controller selections remain contextual state; they cannot add tools to this binding or veto it merely by naming an unrelated unregistered identity. An identity mismatch between the command and the resulting bindings is BLOCKED before adapter execution. Structured list/tuple input accepts only exact registered IDs in the supplied order; empty requests, unregistered IDs, non-string entries and duplicates are rejected before binding. The legacy lexical string interface remains available, with its original recognition semantics. Both forms enter the same binding, plan and recurrence path. Structured identity validation does not establish natural-language authorization or semantic completeness.

## Fail-closed rules

A recognized but unregistered formal object in a direct-command request:
BLOCKED, including when it is mixed with a registered tool command. A registered label cannot be matched as the prefix of a longer hyphenated or word-token label. Unknown ordinary-language tokens are not assigned a tool identity.

Missing adapter:
OPEN.

Incomplete configured identity:
BLOCKED before plan construction.

Missing or invalid recurrence identity:
BLOCKED before successful HF2 execution.

HF2 local frontier unresolved:
OPEN or another typed HF2 disposition.

A prose analysis, a plan, a tool label, or host reasoning cannot substitute for the bound
adapter execution. A successful configured route and a relative HF2 close establish only the execution and scope represented by their receipts. Distinguish IMPLEMENTATION_EXECUTED, SEMANTICALLY_APPLIED and FULL_MATCH, and do not infer full domain-semantic coverage merely from plan completeness, a synthetic routing check or a bounded native result.

## Protected reconstruction

Every generic tool manifest now reconstructs:

CONFIGURED_HF2_RECURRENCE

and

FULL_CONFIGURED_INVOCATION_PROFILE.

ConfiguredRunSpec.complete() requires both.

Therefore recurrence is not merely an execution convention.

## Portfolio audit

[runtime/full_invocation_portfolio.py](../runtime/full_invocation_portfolio.py)

For every current registered tool it verifies:

- ConfiguredRunSpec complete;
- expected recurrence engine;
- manifest reconstruction;
- direct command resolution;
- 36 cells;
- 792 question projections;
- 144 cognitive projections;
- shared execution gateway reachability;
- HF2 or SELF recurrence receipt;
- missing adapter preserves OPEN.

This audit proves routing/profile reachability with synthetic adapters. It does not claim that
every tool's domain-specific native semantics are self-contained in every environment.

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


## Post-merge Think-big reentry

A post-merge recheck found two additional repository-owned execution surfaces that could
otherwise have remained weaker parallel paths.

### Protected Transition Integrity executor

[`runtime/global_tool_execution.execute_protected_transition`](../runtime/global_tool_execution.py)

now executes its execution edge through:

[`runtime/configured_hf2_execution.execute_configured_with_hf2`](../runtime/configured_hf2_execution.py).

Backward-compatible execute callbacks may return:

(value, evidence)

for a one-round local close, or:

(value, evidence, recurrence_hints)

when the same configured execution has a material/live local successor.

A successful PTI receipt now carries recurrence evidence such as:

configured-recurrence:HF002:RELATIVE_CLOSE:rounds=n

or, for HF002 itself:

configured-recurrence:SELF:SELF_CLOSE:rounds=1.

PTI forwards `hf2_affected_frontier` and `hf2_scope_deltas` obligations to the shared recurrence executor. It cannot return a successful configured transition while its recurrence disposition remains OPEN, BLOCKED, CONFLICT, RETURN_REENTER, or RESOURCE_STOP.

### Tool Conductor factors

[runtime/portable_tool_conductor.py](../runtime/portable_tool_conductor.py)

still emits exactly one conductor-level disposition per registered factor.

However, every non-self factor that actually executes now crosses the current full configured
plan and configured recurrence executor.

Therefore:

one conductor factor disposition

does not mean:

one native adapter call.

A factor may internally take multiple HF2 rounds while remaining one factor in the exhaustive
product.

Missing environment-bound adapters remain OPEN/BLOCKED rather than being substituted.

The ToolConductor self factor remains a non-recursive self witness so the exhaustive product
does not spawn an infinite conductor-on-conductor chain.

## Strengthened route set

The current repository-owned full-invocation invariant is enforced across:

1. direct imperative formal-tool commands;
2. ImprovementCore selected-tool execution;
3. PTI end-to-end configured transitions;
4. ToolConductor factor execution.

Inner native semantic functions such as capability_runtime.execute_capability and individual
learning operators are implementations inside a configured invocation, not independent claims
of a full configured tool run.


## Validation and merge evidence

Primary full-profile repair:

PR #117

merge:
2b86fdc500f5ad1b35fa578b7c96bd92feb99f41

Regime-091 transported validation:
- Take-5 Validation 36270850293 SUCCESS
- Capability Preservation 36270850299 SUCCESS

Post-merge bypass closure:

PR #119

merge:
f35577993d076e9113db0bc6e62b91d89b062565

Post-merge validation:
- Take-5 Validation 36271301228 SUCCESS
- Capability Preservation 36271301286 SUCCESS

Final ImprovementCore + HF2 reentry:

[IMPROVEMENTCORE_HF2_THINK_BIG_REENTRY_122_2026-09-26.md](../artifacts/improvecore/IMPROVEMENTCORE_HF2_THINK_BIG_REENTRY_122_2026-09-26.md)

Current finite registered-repertoire disposition:

CLOSED_RELATIVE.

Universal external-host interception:

EXTERNAL_NOT_OWNED.
