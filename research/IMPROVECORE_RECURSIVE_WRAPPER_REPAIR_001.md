# ImproveCore Recursive Wrapper Repair 001

Date: 2026-09-24
Status: EXECUTED SEMANTIC REPAIR / NONPRODUCTION RUNTIME CANDIDATE
Authority: research only

## Rewritten governing job

Recover the strongest current recursive execution contract and make it the default wrapper for every material tool, behavior, package, and higher-order analysis episode.

Do not treat recursion as:
- optional follow-up;
- repeated identical tool invocation;
- an outer wrapper applied only after a complete run.

Use the canonical interleaved pattern:

ROUND
-> TOOL RUN CLOSURE
-> ADMITTED CONSEQUENCE UPDATE
-> HF-001 REENTRY
-> NEXT ROUND

until:
RELATIVE_CLOSE
OPEN
BLOCKED

For stronger adequacy claims, require a failure-mode-distinct external challenge after same-basis stability.

## Core correction

The prior conversation repeatedly used:
Tool A
-> read result
-> user asks for Tool B / another pass
-> discover higher-order result.

That is not the configured current system.

The configured current system requires the wrapper itself to own continuation.

## Wrapper components

1. Execution Envelope
owns target, authority, protected outputs, binding, execution truth, recovery, and episode terminal state.

2. Tool Run Closure
runs after every material/persistence-sensitive round.
It harvests and dispositions consequences before the next recursive state is trusted.

3. HF-001
re-enters on RESULT or SEARCH delta and maintains frontier, memory, OPEN/BLOCKED, and basis-relative closure.

4. External escape
after same-basis self-stability when a stronger claim requires challenge from a distinct failure mode.

## Critical GDOS rule

GDOS independence and HF-001 recursion are compatible only with two time scales.

Within a GDOS round:
- freeze X_t;
- every observer receives the same X_t;
- no observer consumes sibling output;
- no target mutation;
- reconcile only after all independent outputs are complete.

Between GDOS rounds:
- reconcile Omega_t;
- run Tool Run Closure on the reconciled material consequences;
- admit/update state;
- HF-001 decides whether material RESULT or SEARCH delta reopens the target;
- freeze X_(t+1);
- launch a new independent GDOS round.

Therefore:

GDOS_round(X_t)
= Reconcile({Observe_i(X_t)})

and recursive configured GDOS is:

X_t
-> GDOS_round
-> TRC
-> Update
-> HF001
-> X_(t+1).

This is stronger than one-pass GDOS and avoids contaminating within-round independence.

## Scope rule

Not every atomic capability must blindly repeat.

Wrapper recursion applies when:
- result delta changes protected understanding;
- search-state delta changes what may matter next;
- a material consequence changes state/currentness/evidence/ownership/authority;
- external challenge reopens the frontier.

No-delta atomic operations may terminate inside one episode when the wrapper certifies no continuation-relevant effect.

## Tool-family audit

### Canonically wrapped / strong evidence
MTA:
explicit canonical interleaving with TRC + HF-001.

Goal Spine:
nine-round wrapped self-application with TRC + HF-001 + external Architecture challenge.

Architecture Analysis:
HF-001 self-application exists and produced material recursive yield.

Diagnosis / Root Cause:
HF-001 self-application exists and produced material recursive yield.

Orphan/Ghost:
MTA + HF-001 recursive reentry exists.

### Partially wrapped / wrapper semantics present but not universalized
Multi-Object:
recursive self-application exists, but configured wrapper is not one universal entry contract for every invocation.

RTC / Raise the Ceiling:
reentry is native to ceiling search, but not every RTC invocation is explicitly enclosed by generic TRC + HF-001 episode closure.

ARA:
repeated recursive runs exist, but generic wrapper binding is not guaranteed at every invocation surface.

Goal Completion / Governance Activation:
HF-001 recursive experiments exist, but canonical unqualified invocation does not yet visibly bind the same wrapper contract as MTA.

### Wrapper-risk families
Any named tool or behavior invoked directly from conversation without resolving its canonical configured entry path.
Any atomic B/C capability run ad hoc outside an Execution Envelope.
GDOS / autonomous observation as currently represented in Take-5.
Mode experiments.
Bias perturbation experiments.
Capability-center experiments.
Newly synthesized packages.

## Take-5 implementation result

Added:
runtime/recursive_episode.py

This provides a generic nonproduction interleaved episode runner with:
- round;
- closure;
- update;
- reentry;
- typed OPEN/BLOCKED/RELATIVE_CLOSE;
- external challenge hook.

Added:
tests/test_recursive_episode.py

This proves:
- closure precedes reentry;
- material delta continues;
- external challenge can reopen apparent closure;
- OPEN closure prevents state update.

## New diagnosis

The recurring failure is not "we forgot HF1."

It is:

CONFIGURED-TOOL IDENTITY LOSS.

The semantic nucleus of a tool was preserved, but its configured execution identity:
Tool = semantic nucleus + episode wrapper + closure + reentry + external challenge obligations
was not consistently recovered at every invocation surface.

This is the same class as earlier capability migration loss:
preserving transform semantics while losing routing/binding/execution behavior.

## Higher-order propagation

Every tool specification now needs two identities:

ToolSemantics
and
ConfiguredRunSemantics.

ConfiguredRunSemantics includes:
- execution envelope;
- recursive trigger;
- closure placement;
- consequence persistence;
- reentry;
- challenger/holdout requirement;
- terminal certificate.

A tool is not fully recovered when only ToolSemantics survives.

## Improvement Core consequence

Improvement Core itself must run inside the same closure discipline.

IC round:
DISCOVER/PLAN/REALIZE/ADMIT/INTEGRATE
-> TRC
-> HF001 REENTER
-> recompute work/capability/policy frontier.

A material self-improvement delta cannot become the next IC basis merely because IC generated it.

## Immediate repair program

1. Make generic RecursiveEpisode the common nonproduction wrapper.
2. Add ConfiguredRunSpec to tool/program metadata.
3. Bind GDOS to a two-timescale recursive protocol.
4. Audit all major named tools for configured wrapper identity.
5. Rerun prior one-pass GDOS research under recursive configured GDOS.
6. Reassess conclusions that changed after later manual passes.
7. Promote no semantic conclusion solely because it survived one round.
8. Require wrapper receipt for claims that a recursive tool run was complete.

## Disposition

The user's diagnosis is CONFIRMED.

The prior GDOS and mode research remains useful as round-level evidence, but several synthesis claims require recursive rerun before being treated as stable.

The wrapper itself is not merely HF-001.
It is:

ExecutionEnvelope
+ ToolRunClosure
+ HF001
+ external escape where required.

HF-001 is the recursive reentry component inside the larger configured-run wrapper.
