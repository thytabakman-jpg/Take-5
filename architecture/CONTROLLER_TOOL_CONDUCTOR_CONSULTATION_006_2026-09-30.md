# Controller ToolConductor Consultation Contract 006

Date: 2026-09-30
Status: CURRENT CANDIDATE

## Problem

A controller must inspect the complete registered tool repertoire before work generation or selection, but inspection must not itself execute the entire repertoire. The prior branch coupled consultation to exhaustive configured execution, multiplying controller runtime by the cost of every registered tool on every controller pass.

## Formal split

Let R=(r_1,...,r_n) be the ordered MATERIAL_TOOLS registry, P the current controller packet, A the bound adapter map, C the consultation operator, S the downstream selector, and E the configured execution operator.

C(P,A)=(d_1,...,d_n)

with

pi_R(C(P,A)) = R

exactly, preserving registry order and one disposition per registered factor.

Each d_i contains tool identity, recovered entrypoint, required environment, configured-run identity, binding availability, and a typed availability disposition. C is observational:

Delta_target(C)=0

and

Calls_native(C)=0.

Execution is downstream only:

P -> C -> G_W -> S -> E

for ImprovementCore, and

G_Q -> C -> G_W -> S -> E -> A -> U -> G_Q

for ICC128.

Thus consultation completeness and execution completeness are separate coordinates. OPEN or BLOCKED factors remain evidence inside C; they do not invalidate coverage when every r_i has exactly one typed disposition. Missing, duplicated, or reordered factors fail closed.

## Anti-recursion

The active controller adapter is removed from A before C is evaluated. ToolConductor self-application is represented by its self witness rather than recursive spawn.

## Runtime invariant

The consultation path is O(|R|) in registry inspection and does not invoke configured HF2 or native tool execution. Full configured execution remains available through run_tool_conductor and through the normal post-selection configured-tool bridge.

## Verification

The repair is admitted only when:

1. exact registry coverage tests pass;
2. active-controller suppression tests pass;
3. ImprovementCore sees C before GENERATE_WORK and SELECT;
4. ICC128 sees C between G_Q and G_W;
5. consultation tests prove bound adapters are not executed;
6. full Take-5 validation, capability preservation, every-tool sweep, and ImprovementCore holdouts remain green.
