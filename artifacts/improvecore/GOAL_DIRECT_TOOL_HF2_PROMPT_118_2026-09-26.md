# GOAL on Direct-Tool/HF2 Prompt 118

Date: 2026-09-26
Basis: MT_DIRECT_TOOL_HF2_PROMPT_118
Status: CLOSED_RELATIVE

## Governing goal

Within the Take-5-owned execution boundary, every direct command of a registered formal tool
must resolve through one canonical full-invocation contract that preserves the tool's current
configured identity and actually includes the current recurrence policy.

For every registered tool T other than the recurrence engine itself:

DirectCommand(T)
->
CanonicalIdentity(T)
->
ConfiguredRunSpec(T)
->
D36_C Plan(T)
->
NativeAdapter(T)
->
HF2[T]
->
Closure/Reentry
->
Execution/Consumption Receipt.

For HF002 itself, the recurrence coordinate is SELF rather than recursively wrapping HF2
inside another HF2.

## Required invariants

G1 CURRENT FULL PROFILE

The invocation inherits the current ConfiguredRunSpec rather than a copied hand-written
subset.

Therefore it includes:

- full wrapper;
- D36_C;
- all declared native layers;
- 792 question projections;
- 144 cognitive projections;
- OPEN preservation;
- closure;
- reentry;
- protected behaviors;
- PTI.

G2 HF2 IS AN INVOCATION COORDINATE

The configured identity must explicitly declare its recurrence engine.

For ordinary registered tools:

Recurrence(T)=HF002.

For HF002:

Recurrence(HF002)=SELF.

G3 ACTUAL RECURRENCE, NOT LABEL-ONLY

The canonical execution gateway must instantiate HF002 around the bound native adapter.

A successful invocation cannot be certified merely because the plan says "HF2".

G4 FAIL CLOSED

Missing adapter:
OPEN.

Missing/invalid recurrence evidence:
OPEN/BLOCKED.

Unregistered formal object:
BLOCKED.

No generic host reasoning may silently stand in for the selected tool.

G5 ONE REPOSITORY-OWNED DIRECT-COMMAND GATEWAY

Direct imperative commands such as "run MT" and "use GOAL" must have one canonical Take-5
routing surface.

Other repository callers may reuse its binding/execution primitives rather than implement a
weaker parallel path.

G6 PRESERVE EXISTING SYSTEMS

Do not replace:

- ConfiguredRunSpec;
- global_tool_execution;
- PTI;
- tool manifests;
- ImprovementCore bridge;
- HF002.

Compose them.

G7 EXTERNAL AUTHORITY TRUTH

Take-5 repository closure does not imply universal interception by an unrelated ChatGPT host.

HOST_INTEGRATION_BYPASS remains EXTERNAL_NOT_OWNED unless an external host binding exists.

## Success predicate

Let F(T) be the canonical full invocation of registered tool T.

RepositoryFullInvocationClosed

iff for every registered T:

IdentityClosed(T)
and
PlanComplete(T)
and
RecurrencePolicyClosed(T)
and
GatewayReachable(T)
and
MissingAdapterFailsClosed(T)
and
HF2ExecutionWitnessed(T)
and
PTIPreserved(T).

## User-level desired effect

Inside any Take-5-governed path, saying "run/use <registered tool>" can no longer degrade to a
bare/core or one-shot substitute.

The repository can then truthfully report exactly which external host integrations still sit
outside its authority.
