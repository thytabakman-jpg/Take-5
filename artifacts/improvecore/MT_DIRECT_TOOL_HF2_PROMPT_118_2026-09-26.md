# Full MT on Direct-Tool/HF2 Prompt 118

Date: 2026-09-26
Basis: Take-5 main 709ca252e258534169d3472ad52ce6411290ca91
Configured tool: MT
Mode: OBSERVER
Wrapper: canonical math-first full wrapper
Geometry: D36_C = 6 scopes x 6 mode faces = 36 cells
Question projections: 22 x 36 = 792
Cognitive projections: 4 x 36 = 144
Black-box return gate: applied
Closure/reentry: applied

## Prompt target

The user reports that direct commands such as "run MT" or "use GOAL" do not reliably
receive all of the current full-tool machinery, especially HF2, the 36-dimensional
surface, the full wrapper, and the current ideal execution profile.

Requested order:

MT -> GOAL -> IC123 rewrite -> ImprovementCore with HF2 recurrence -> final
ImprovementCore with the full result and command "Think big."

## Current evidence

### E1 — full wrapper and D36_C already exist as registered-plan invariants

runtime/configured_run.py currently requires:

- wrapper_required = true;
- default_mode = OBSERVER;
- geometry = D36_C;
- 22 question families;
- four cognitive operators;
- recursion;
- closure;
- reentry;
- OPEN preservation;
- Protected Transition Integrity reconstruction.

runtime/global_tool_execution.py builds 36 cells and rejects non-observer ordinary tool plans.

Therefore:

MISSING_D36_OR_WRAPPER_IN_CONFIGURED_PLAN

is not the current generator.

### E2 — HF2 is not part of the generic configured-run identity

ConfiguredRunSpec has no recurrence-engine coordinate.

HF002 exists as a generic recurrence substrate, but CURRENT_HF2 explicitly records:

- promoted validated built-in use: HF2[RootCause];
- validated explicit campaign composition: HF2[ImprovementCore]_campaign;
- universal wrapper promotion remains OPEN.

Therefore a normal registered tool plan does not currently imply:

HF2_ATTACHED(tool).

### E3 — the configured ImprovementCore tool bridge invokes adapters one-shot

runtime/improvement_core_tool_bridge.py:

bind_selected_tools
-> build_tool_execution_plan
-> execute_bound_tools
-> adapter(current,plan).

The bridge requires actual adapter invocation and preserves OPEN when an adapter is missing,
but the generic bridge itself does not pass every selected capability through HF002.

### E4 — direct user command routing is not one canonical Take-5 gateway

formal-object identity is recoverable through runtime/formal_object_registry.py.

However there is no current repository runtime whose contract is:

direct imperative tool command
-> canonical registered tool identity
-> full configured plan
-> actual adapter execution
-> HF2 same-capability recurrence
-> closure/reentry receipt.

Therefore repository callers can still choose narrower entry surfaces.

### E5 — external host bypass remains an authority boundary

Take-5 cannot force a ChatGPT host that never invokes Take-5 to use a repository gateway.

That is already classified:

UNIVERSAL_HOST_INTERCEPTION = EXTERNAL_NOT_OWNED.

A repository repair must not claim to solve that external authority boundary.

## 36-cell quotient

The full MT surface collapses to six material distinctions.

1. FULL_CONFIGURED_PLAN != FULL_CONFIGURED_INVOCATION

A plan can contain the 36-dimensional wrapper geometry while the actual runtime path still
fails to include HF2.

2. HF2_AVAILABLE != HF2_BOUND_TO_EVERY_TOOL

The generic engine exists; universal attachment does not.

3. TOOL_SELECTED != CANONICAL_DIRECT_COMMAND_ROUTED

A controller-selected tool can cross the ImprovementCore bridge while a free-standing user
command can still bypass that bridge.

4. ADAPTER_INVOKED_ONCE != HF2_LOCAL_RECURRENCE_GOVERNED

One implementation call does not establish same-capability reapplication after material local
change.

5. REPOSITORY_NONBYPASSABLE != HOST_UNIVERSALLY_INTERCEPTED

Take-5 can make its own canonical direct-command gateway fail closed. It cannot force an
unrelated host to enter it.

6. "IDEAL EVERYTHING" != A SECOND PARALLEL WRAPPER

The repair should reuse the current ConfiguredRunSpec, global D36 plan, PTI, tool manifests,
closure/reentry, and HF002 substrate rather than create another competing execution stack.

## MT generator diagnosis

Primary repository-owned generator:

MISSING_CANONICAL_FULL_TOOL_INVOCATION_GATE.

Subgenerator:

HF2_NOT_INTRINSIC_TO_GENERIC_CONFIGURED_INVOCATION.

External residual:

HOST_INTEGRATION_BYPASS.

## MT disposition

MATERIAL_YIELD / CLOSED_RELATIVE for prompt diagnosis.

The next required step is GOAL, using these distinctions as evidence.
