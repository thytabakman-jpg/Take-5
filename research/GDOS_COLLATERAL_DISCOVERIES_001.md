# GDOS Collateral Discoveries 001

Date: 2026-09-24
Status: CROSS-PROJECT / TOOL-ECOSYSTEM DISCOVERIES
Authority: research only

These findings arose while studying GDOS but are not merely claims about GDOS.

## 1. Tool semantics and tool orchestration are different capability classes

A system can preserve every tool's mathematical transformation and still lose the ability to use tools.

Take-5 demonstrated exactly this:
semantic capability reconstruction survived;
selection/dispatch did not.

Therefore capability preservation needs at least:
- semantic transform preservation;
- trigger preservation;
- routing preservation;
- binding preservation;
- execution preservation;
- verification/reentry preservation.

This is stronger than the current notion of behavior-preserving compression.

## 2. Negative space is first-class evidence

A tool not selected is not equivalent to a tool silently ignored.

The capability router now exposes:
SELECTED, NON_APPLICABLE, UNBOUND, BLOCKED, OPEN.

This same idea generalizes to GDOS:
an observer that generated no material observation is itself evidence about factor relevance.

Absence requires provenance.

## 3. Some "tools" are really experimental conditions

GDOS, zero-request, information-barrier replication, and frozen-target modes do not behave like ordinary transforms X->Y.

They alter the conditions under which other capabilities operate.

Candidate higher-order class:
EXECUTION REGIME / OBSERVATION REGIME.

This class is distinct from tool, behavior, boundary, and controller.

## 4. State mutation is an epistemic intervention

Updating the object between observations is not merely bookkeeping.

It changes what later observers can see.

Thus:
Update(U) belongs in experimental-design reasoning, not only state management.

This gives a new interpretation of U in T=<K,S,O,G,M,C,R,U>:
U is both a realization operator and a potential source of observational contamination.

## 5. Reconciliation may be a missing explicit capability

Current architecture has relation, reconstruction, admission, routing, update, and verification, but GDOS repeatedly relies on a distinct operation:

take independently generated observations
-> preserve conflicts and provenance
-> identify overlap, interaction, contradiction, and joint residual
-> produce a reconciled observation structure without yet optimizing it.

This is not obviously identical to RELATE or RECONSTRUCT.

Candidate status: new load-bearing object requiring MTA/admission, not silently inserted.

## 6. Observation saturation is different from closure

A GDOS sweep can reach:
no new material observations under observer basis B

without establishing:
no remaining defects,
no remaining improvements,
no remaining dependencies,
or global understanding.

Candidate typed status:
OBSERVATION_SATURATED(B)

distinct from C47 relative closure and from completion.

## 7. Capability families differ by endogenous pressure

Capabilities can be classified by how much they intrinsically impose an outcome direction.

Low endogenous pressure:
typing, identity, provenance, attribution.

Medium:
relation, diagnosis, verification, transfer.

High:
generation, strengthening, repair, routing, ceiling search, completion.

GDOS effects track this pressure more closely than they track the old named-tool families.

This may be a better predictor of when GDOS is valuable.

## 8. Goal is not binary

At least four goal layers now appear:
G0 object identity/freeze goal;
G1 observation goal;
G2 intervention/optimization goal;
G3 system-level research goal.

GDOS suppresses G2 while retaining G0, G1, and G3.

So "goal-decoupled" is a convenient name but mathematically it is selective goal-layer suppression, not absence of goals.

## 9. IC likely needs two controller modes

NORMAL:
live bottleneck -> capability selection -> intervention -> verification -> reentry.

OBSERVATION:
frozen object -> broad applicable observer set -> independent outputs -> reconciliation -> return to NORMAL.

This suggests IC is not one policy. It is a governed mode-switching controller.

## 10. Kernel may need to protect observation integrity

Not by selecting observers.

Possible global invariants:
- a declared independent observation cannot consume another independent observer's output;
- a frozen-target experiment cannot mutate the target before the observation set closes;
- execution truth must distinguish semantic observation from runtime tool invocation.

These are candidate experimental-integrity invariants, not yet admitted Kernel laws.

## 11. The repertoire quotient may be context-dependent

Two capabilities can be behaviorally equivalent under normal goal-directed continuation but non-equivalent under GDOS because their otherwise-pruned observations differ.

Therefore contextual reconstructibility must include controller regime:

h_i ~_{J,Ctx,Mode} h_j

rather than only job and composition context.

This is a major consequence for MTA quotienting.

## 12. "Every tool" is the wrong coverage primitive

The right primitive is:
every material observational function represented,
with explicit negative-space disposition.

Running every named tool can be redundant.
Running one representative per quotient class can be sufficient only after equivalence is demonstrated under the relevant controller mode.

This directly connects GDOS research to the capability-compression program.
