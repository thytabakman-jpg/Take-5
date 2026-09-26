# Tool Conductor Portable Mathematics 073

Date: 2026-09-26
Status: CURRENT RECOVERED CORE / PORTABILITY CLOSURE OPEN

## Job

Apply every member of a frozen registered tool repertoire to one common target
without selecting a subset, improving the tools, or becoming the global
controller.

## Typed product semantics

Let the registered repertoire be indexed by a finite set I.

Each tool i has a typed domain D_i, codomain Y_i, and current configured
operator or relation T_i. Because the domains are heterogeneous, define an
input adapter

a_i : X x C => D_i union {OPEN_i}

and a tagged injection

j_i : Y_i -> coproduct_{k in I} ({k} x Y_k).

Define the lifted factor

T~_i(x,c) =
  BLOCKED_i                    when no effective program witness exists,
  OPEN_i                       when a_i(x,c) is unresolved,
  j_i(T_i(a_i(x,c)))           when the admitted configured execution returns.

The Tool Conductor is the exhaustive product

TC_I(x,c) = ( T~_i(x,c) )_{i in I}.

Coverage invariant:

forall i in I, exactly one conductor-level disposition is emitted.

The conductor does not infer success from repertoire traversal. OPEN and
BLOCKED remain first-class outputs.

## Effective portability coordinate

A tool is machine-portable only when there is an effective compilation witness

C_i = <e_i, enc_i, dec_i, Env_i>

for a fixed universal evaluator U such that on the admitted domain

dec_i(U(e_i, enc_i(z), Env_i)) = T_i(z).

Env_i is empty for a self-contained program. When Env_i is nonempty, the
external operations are part of the explicit input contract and cannot be
silently supplied by chat history or repository convention.

Portable(TC_I) iff for every i in I:
1. e_i exists;
2. enc_i and dec_i are effective;
3. every required Env_i operation is supplied by an effective implementation;
4. the tool's configured execution contract is preserved by compilation.

Thus semantic FullMath and effective portability are distinct coordinates.

## Self application

Tool Conductor does not recursively spawn a child Tool Conductor forever.
For its own factor, the active invocation emits a self-execution witness:

T~_TC(x,c) = SELF_WITNESS(active TC invocation).

This satisfies repertoire coverage without an infinite regress.

## Current executable realization

runtime/portable_tool_conductor.py

The runtime creates one CompilationWitness for every member of
runtime/tool_run_registry.py::MATERIAL_TOOLS and refuses to call the repertoire
portable while any factor is missing a self-contained effective realization.

Atomic C01-C49 programs bind directly to capability_runtime.execute_capability.
Learning operators bind to learning_tool_bridge and expose their caller-supplied
semantic functions as explicit environment coordinates.
Named high-level tools bind only where a native Take-5 runtime entrypoint has
been recovered without semantic substitution.

## Closure

Portable closure requires portability_open_set() = empty.

Until then, Tool Conductor itself is executable, but exhaustive cross-machine
execution of the entire repertoire remains OPEN.
