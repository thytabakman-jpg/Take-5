# Full Configured Tool Invocation 121

Date: 2026-09-26
Status: IMPLEMENTED CANDIDATE / THINK-BIG REPAIR
Origin:
- MT direct-tool/HF2 prompt audit 118
- GOAL direct-tool/HF2 118
- IC123 rewrite 118
- ImprovementCore + HF2 campaign 119
- ImprovementCore + HF2 Think-big pass 120

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
>.

The invocation profile is:

FULL_CONFIGURED_HF2_V1.

## Full plan

For registered T:

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

PlanComplete(T)

iff:

Wrapper(T)
and
|D36_C| = 36
and
|Questions(T)| = 22 x 36 = 792
and
|Cognitive(T)| = 4 x 36 = 144
and
RecurrenceRequired(T)
and
RecurrenceEngine(T)=Rec(T)
and
InvocationProfile(T)=FULL_CONFIGURED_HF2_V1.

## Runtime invocation

For ordinary T:

FullInvoke(T,x)
=
HF002[
    Adapter_T(
        Plan(T),
        x
    )
].

HF002 re-applies Adapter_T only while:

MaterialLocal
and
Live_T
and
UpstreamStable.

Otherwise it reaches a typed relative close, OPEN, BLOCKED, CONFLICT, RETURN_REENTER, or
resource stop according to the HF002 contract.

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

"run/use/execute/apply/call T"
-> direct_tool_command_gateway
-> bind_selected_tools
-> build_tool_execution_plan
-> execute_configured_with_hf2
-> native adapter.

These routes share the same binding and execution primitive.

## Fail-closed rules

Unregistered formal object:
BLOCKED.

Missing adapter:
OPEN.

Incomplete configured identity:
BLOCKED before plan construction.

Missing or invalid recurrence identity:
BLOCKED before successful HF2 execution.

HF2 local frontier unresolved:
OPEN or another typed HF2 disposition.

A prose analysis, a plan, a tool label, or host reasoning cannot substitute for the bound
adapter execution.

## Protected reconstruction

Every generic tool manifest now reconstructs:

CONFIGURED_HF2_RECURRENCE

and

FULL_CONFIGURED_INVOCATION_PROFILE.

ConfiguredRunSpec.complete() requires both.

Therefore recurrence is not merely an execution convention.

## Portfolio audit

runtime/full_invocation_portfolio.py

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

Inside a Take-5-governed formal-tool route, the weaker one-shot configured path is no longer
admissible.


## Post-merge Think-big reentry

A post-merge recheck found two additional repository-owned execution surfaces that could
otherwise have remained weaker parallel paths.

### Protected Transition Integrity executor

runtime/global_tool_execution.execute_protected_transition

now executes its execution edge through:

runtime/configured_hf2_execution.execute_configured_with_hf2.

Backward-compatible execute callbacks may return:

(value, evidence)

for a one-round local close, or:

(value, evidence, recurrence_hints)

when the same configured execution has a material/live local successor.

A successful PTI receipt now carries recurrence evidence such as:

configured-recurrence:HF002:RELATIVE_CLOSE:rounds=n

or, for HF002 itself:

configured-recurrence:SELF:SELF_CLOSE:rounds=1.

PTI cannot return a successful configured transition while its recurrence disposition remains
OPEN, BLOCKED, CONFLICT, RETURN_REENTER, or RESOURCE_STOP.

### Tool Conductor factors

runtime/portable_tool_conductor.py

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
