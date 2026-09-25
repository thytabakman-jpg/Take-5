# ImproveCore 36-Cell Scope × Mode Audit 001

Date: 2026-09-24
Status: EXECUTED SEMANTIC AUDIT / MATERIAL ARCHITECTURE GAIN
Target: IC-028 + IC-029 candidate + current tool-family / six-scope / mode-cube architecture
Controller authority: unchanged
Runtime authority: IC-2026-09-23-018 remains unchanged

## 0. Frozen job

Determine how the 36-cell architecture can improve ImproveCore itself and how ImproveCore can use that architecture in ordinary operation, tool selection, discovery, validation, reentry, and completion.

Protected behavior:
- broad messy-corpus intake;
- autonomous discovery;
- surprising but defensible connections;
- strong focused problem solving;
- authority and execution truth;
- evidence admission;
- persistent update;
- relative closure;
- recursive improvement without silent goal drift.

## 1. What “36” means

The current supported scope ontology is:

SCOPE =
{SYSTEM, SUBSYSTEM, COMPONENT, INTERFACE, BOUNDARY_DECOMPOSITION, CROSS_LAYER}.

The current supported mode geometry has six faces/poles:

MODE_FACE =
{EXPAND, CONTRACT, INWARD, OUTWARD, ISOLATE, COUPLE}.

Therefore the audit lattice is:

L_36 = SCOPE × MODE_FACE.

|L_36| = 6 × 6 = 36.

Important:
The 36 cells are not 36 independent tools and not 36 exclusive runtime states.

Runtime mode remains the three-axis cube:

Breadth = {EXPAND,CONTRACT}
Direction = {INWARD,OUTWARD}
Coupling = {ISOLATE,COUPLE}

with 8 complete mode corners.

The 36-cell lattice is a coverage, routing, challenge, and completion surface.

## 2. MT result on ImproveCore

Current ImproveCore can be factored as:

IC =
<Contract, State, ScopePolicy, ModePolicy, GeneratorPolicy, ToolPolicy, ExecutionPolicy,
 AdmissionPolicy, UpdatePolicy, ReentryPolicy, CompletionPolicy>.

IC-028/029 already represent most of these semantically, but ScopePolicy and ModePolicy are largely implicit.

Current dominant implementation tendency:

Tool choice
implicitly carries
scope + mode.

That is lossy.

Example:
Selecting PD does not determine whether PD is:
- SYSTEM + EXPAND + OUTWARD + ISOLATE,
or
- COMPONENT + CONTRACT + INWARD + COUPLE.

These are materially different runs.

Strong successor representation:

Run_t =
<ToolFamily_t, Scope_t, Mode_t, K_t, S_t, Evidence_t>.

The controller therefore selects not merely a tool/package, but:

NextAction_t =
<Scope, Mode, ToolPackage, Binding, Budget>.

## 3. 36-cell audit

Legend:
M = material current gap/opportunity
R = represented but under-explicit
S = strong/currently well represented

### SYSTEM

SYSTEM × EXPAND — M
Generate alternate whole-system representations, candidate work classes, hidden objectives, relation families, and architecture hypotheses.
Current weakness: expansion pressure exists through PD/G_relation/GDOS lineage but is not a first-class controller obligation.

SYSTEM × CONTRACT — S
Freeze governing target, select architecture, narrow live frontier, define completion.
ImproveCore is strong here.

SYSTEM × INWARD — S
Decompose root system into roles, modules, state, operators, generators, controller/runtime layers.
Strong through MTA, Architecture, PD, factorization.

SYSTEM × OUTWARD — M
Inspect environment, external theories, neighboring projects, comparators, tools, external mathematics, user/system boundary.
Present through Transfer/IOOC/external scans but not uniformly scheduled.

SYSTEM × ISOLATE — M
Run frozen-sibling whole-system observations, matched ablations, independent architecture challenge.
Exists experimentally, not as a standing ImproveCore policy.

SYSTEM × COUPLE — S/R
Integrate admitted discoveries across controller state, maps, tools, projects, and persistent frontier.
Strong, but overcoupling/path-dependence controls are under-explicit.

### SUBSYSTEM

SUBSYSTEM × EXPAND — M
Generate alternate subsystem decompositions, hidden dependencies, missing local capabilities, and neighboring subsystem candidates.

SUBSYSTEM × CONTRACT — S
Resolve subsystem-local obligations and certify local closure without claiming system closure.

SUBSYSTEM × INWARD — S
Descend into subsystem components, local state, operators, dependencies.

SUBSYSTEM × OUTWARD — R
Inspect enclosing-system assumptions, sibling systems, external causal inputs and inherited contracts.

SUBSYSTEM × ISOLATE — M
Ablate one subsystem against frozen environment; test whether observed gain depends on sibling updates.

SUBSYSTEM × COUPLE — R/S
Synchronize admissible deltas across sibling subsystems and preserve system invariants.

### COMPONENT

COMPONENT × EXPAND — R
Generate rival implementations, representations, interpretations, local mechanisms, successor candidates.

COMPONENT × CONTRACT — S
Select/repair one component under preservation and strict-gain tests.

COMPONENT × INWARD — S
Inspect local typing, domain/codomain, failure states, internal assumptions and residual.

COMPONENT × OUTWARD — R
Inspect ports, consumers, providers, external dependencies, ownership and result effects.

COMPONENT × ISOLATE — S/R
Unit ablation, component-local holdout, local causal discrimination.
Present in validation tooling but not universally linked to mode state.

COMPONENT × COUPLE — S
Compose component result into packages/system and test interaction/noncommutation.

### INTERFACE

INTERFACE × EXPAND — M
Generate candidate handoffs, missing bridges, alternative protocols, hidden relation types.
High leverage and not yet a universal DISCOVER obligation.

INTERFACE × CONTRACT — R/S
Resolve producer/consumer contract, typing, authority, state transfer and OPEN propagation.

INTERFACE × INWARD — R
Inspect each side’s semantics and exact transformation at the edge.

INTERFACE × OUTWARD — M
Trace how one interface change propagates through wider network/consumer paths.

INTERFACE × ISOLATE — M
Hold one side fixed, perturb the other, run edge-specific counterfactual/compatibility tests.

INTERFACE × COUPLE — S
Compose handoffs, test order sensitivity, noncommutation and higher-order interaction.
Strong through Multi-Object and architecture tooling.

### BOUNDARY / DECOMPOSITION

BOUNDARY × EXPAND — M
Generate rival decompositions, ownership cuts, responsibility assignments, primitive bases and scope partitions.

BOUNDARY × CONTRACT — R/S
Select/admit a decomposition relative to protected behavior and authority.

BOUNDARY × INWARD — R
Inspect assumptions encoded by current cut and responsibility partition.

BOUNDARY × OUTWARD — M
Compare surrounding decompositions and effects on environment/project/system identity.

BOUNDARY × ISOLATE — M
Freeze job and behavior, change only boundary/decomposition, observe result delta.

BOUNDARY × COUPLE — R
Propagate approved boundary change into identities, interfaces, ownership, routing and persistence.

### CROSS-LAYER

CROSS_LAYER × EXPAND — M
Generate missing bridges among semantics, capability, package, controller, runtime, evidence, persistence and authority.

CROSS_LAYER × CONTRACT — S/R
Certify one transport path and reject semantic/runtime collapse.

CROSS_LAYER × INWARD — R
Trace each layer transition and preservation obligation.

CROSS_LAYER × OUTWARD — M
Inspect environment/runtime/provider/user effects beyond internal semantic model.

CROSS_LAYER × ISOLATE — M
Independent execution-truth, persistence, authority, and measurement verification.

CROSS_LAYER × COUPLE — S
End-to-end reality closure:
semantic intent -> runtime -> evidence -> admission -> persistence -> semantic update.

## 4. Aggregate profile

ImproveCore is currently strongest at:

1. CONTRACT
2. INWARD
3. COUPLE

ImproveCore is currently weakest/least explicit at:

1. EXPAND
2. OUTWARD
3. ISOLATE

This profile explains an observed behavioral asymmetry:

Strong CONTRACT + INWARD + COUPLE
=> excellent structured solving, repair, integration, closure.

Weak explicit EXPAND + OUTWARD + ISOLATE
=> fewer unprompted reframings, fewer external/cross-context discoveries, greater risk of path-dependent self-confirmation.

This matches the Take-2 / Take-4 / ImproveCore lineage result.

## 5. Goal Spine

G0:
Make ImproveCore mode-and-scope aware without multiplying tools or losing current execution/authority discipline.

Load-bearing subgoals:

G1. Represent current Scope and Mode explicitly.
G2. Generate candidate frontiers indexed by Scope × Mode.
G3. Select ToolPackage conditional on Scope × Mode rather than using tool identity as a proxy.
G4. Permit material discoveries to change Scope and Mode.
G5. Preserve independent/isolated validation paths.
G6. Couple admitted discoveries immediately when isolation is not required.
G7. Make completion relative to declared Scope × Mode coverage.
G8. Instrument execution so empirical selector calibration becomes possible.

## 6. PD result

Hidden selectors in current ImproveCore:

H1 Tool-as-mode selector
Choosing a tool implicitly selects search regime.

H2 Current-representation selector
Candidate generation is constrained by current view unless another tool explicitly attacks it.

H3 Local-frontier selector
An empty frontier can stop work even when another scope/mode would expose material candidates.

H4 Coupling-default selector
Admitted discoveries tend to enter shared state immediately unless a special experiment requests isolation.

H5 Contract-first selector
Controller pressure naturally favors resolution/closure over fresh expansion.

Repair:
make Scope and Mode explicit inputs to generation, routing, equivalence, reentry and completion.

## 7. Architecture result

Candidate controller state:

Z_36 =
<FT,X,A,Cl,B,E,L,Q,P,Scope,Mode,V,Cov_36>.

Where:
Scope = active analysis/action scope.
Mode = <Breadth,Direction,Coupling>.
V = active view family.
Cov_36 = coverage/disposition state over relevant L_36 cells.

Controller cycle becomes:

1. RECOVER target/state.
2. COMPUTE live obligations.
3. COMPUTE relevant scope frontier.
4. COMPUTE admissible mode frontier.
5. GENERATE candidates under each selected Scope × Mode.
6. AUDIT candidate universe.
7. SELECT nondominated <Scope,Mode,ToolPackage>.
8. BIND and EXECUTE.
9. ADMIT/REJECT result.
10. UPDATE state/views.
11. RECOMPUTE affected 36-cell frontier.
12. REENTER on material result/view/scope/mode/candidate delta.
13. CERTIFY completion relative to declared coverage basis.

## 8. Root Cause

Why has ImproveCore repeatedly rediscovered useful tools/behaviors late?

Candidate root set:

R1 scope implicit in tool semantics;
R2 mode implicit in tool/routing choice;
R3 candidate universe generated only under currently active representation/regime;
R4 closure evaluated before alternative scope/mode frontiers were made explicit.

Causal chain:

implicit Scope/Mode
-> narrow generated frontier
-> router cannot select candidates never generated
-> local work appears exhausted
-> relative closure occurs on an underdeclared basis
-> later prompt/tool/experiment changes mode
-> “new” capability appears.

The 36 lattice repairs the cause by making the missing basis visible before closure.

## 9. Multi-Object / interaction result

Important irreducible combinations:

EXPAND × OUTWARD
=> cross-domain and external reframing.

EXPAND × INWARD
=> deeper hidden-structure discovery.

EXPAND × ISOLATE
=> independent fresh-observation sweep.

EXPAND × COUPLE
=> catalytic discovery chaining.

CONTRACT × ISOLATE
=> clean discrimination / holdout.

CONTRACT × COUPLE
=> integrate and operationalize.

Boundary × EXPAND
=> alternative factorization/decomposition generation.

Interface × ISOLATE
=> causal edge diagnosis.

CrossLayer × COUPLE
=> reality closure.

System × EXPAND × OUTWARD × ISOLATE
=> closest formal analogue of a fresh Take-2-style “look at the whole thing and see what appears” pass.

## 10. Factor result

Do not build 36 tools.

Factor into:

Shared Scope coordinate
+
Shared Mode coordinate
+
Tool families
+
Scope adapters
+
Mode adapters
+
Scope/Mode-aware generator/router
+
Coverage ledger.

A capability identity remains separate from its run configuration.

## 11. Strengthen / RTC

Strict successor candidate to IC-029:

IC-030 candidate =
IC-029
+ first-class Scope
+ first-class Mode
+ 36-cell coverage ledger
+ Scope/Mode-indexed candidate generation
+ Scope/Mode-aware routing
+ mode-sensitive reentry
+ 36-relative completion
+ execution instrumentation.

Strict-gain dimensions:
- broader candidate coverage;
- lower false closure;
- restored autonomous discovery;
- better isolation/control;
- improved tool selection context;
- empirical calibratability;
- clearer completion claims.

## 12. Transfer

Transfer from Take-2:
mode switching, not historical stages.

Transfer from Take-4:
rich explicit state/maps.

Transfer from six-scope family:
scope as a first-class run coordinate.

Transfer from GDOS:
EXPAND without goal loss.

Transfer from focused resolution:
CONTRACT.

Transfer from IOOC:
INWARD/OUTWARD.

Transfer from coupled-growth work:
COUPLE when independence is not informative.

Transfer from holdout/frozen-sibling work:
ISOLATE when independence is informative.

## 13. Trace

Historical pattern:
ImproveCore repeatedly acquired capabilities that correspond to previously implicit cells.

Examples:
- GDOS externalized EXPAND.
- IOOC externalized direction.
- six-scope architecture externalized WHERE.
- G_relation externalized relational candidate generation.
- frozen-sibling experiments externalized ISOLATE.
- coupled-growth mode externalized COUPLE.
- new-tool frontier externalized negative-space generation.

The 36 lattice compresses these separate lessons into one controller basis.

## 14. Reconstruct

Clean-sheet controller principle:

For every live material problem, ask:

WHERE can material information reside or fail?
SYSTEM / SUBSYSTEM / COMPONENT / INTERFACE / BOUNDARY / CROSS_LAYER.

HOW can the current search regime expose or suppress it?
EXPAND / CONTRACT / INWARD / OUTWARD / ISOLATE / COUPLE.

Then select a tool/package only after those coordinates are explicit.

This reverses the old implicit order:

old:
tool -> incidental scope/mode.

new:
job -> scope/mode frontier -> tool/package.

## 15. Verify / H2

Attack:
36 cells create combinatorial explosion.

Repair:
do not exhaust all cells blindly.
Use relevance gating, singleton-first search, and expansion only on result sensitivity / interaction witnesses.

Attack:
six faces are not full mode states.

Accepted.
36 is coverage projection.
Runtime uses 8 full cube corners.

Attack:
mode labels may be redundant with existing routing.

OPEN but current counterexamples support nonredundancy because equal tool/package choices can differ materially under different mode coordinates.

Attack:
more exploration can raise false positives/cost.

Accepted.
Selector calibration and holdouts are mandatory.

## 16. New-tool suite

N01 Capability Gap Miner:
search uncovered 36 cells for missing capabilities.

N02 Tool Synthesizer:
synthesize a tool only after a live cell cannot be covered by existing capability/package composition.

N03 Candidate Universe Auditor:
verify applicable Scope × Mode candidate classes were generated.

N04 Basis Change Revalidator:
when shared basis changes, identify every affected cell/tool adapter/closure claim.

N05 Runtime Binder:
bind and record Scope + Mode with every executable tool invocation.

N06 Selector Calibrator:
learn task-conditioned policy over <Scope,Mode,ToolPackage>.

N07 Cross-Map Residual Synthesizer:
use map differences especially in EXPAND/OUTWARD and CROSS_LAYER/INTERFACE cells.

N08 Holdout Forge:
construct mode/scope-specific hidden-target and distractor fixtures.

N09 Tool Interaction Lab:
measure order/noncommutation between tools and modes.

N10 Semantic Drift Sentinel:
detect when tool semantics or runtime no longer match the declared scope/mode contract.

## 17. Completion rewrite

Current completion is basis-relative.

Add:

Cov_36(K,X)
=
disposition map over every Scope × Mode cell that is applicable to the declared claim.

A cell disposition may be:
- GENERATED_AND_DISPOSITIONED
- NOT_APPLICABLE
- BLOCKED
- OPEN
- DEFERRED_WITH_NONRESULTSENSITIVE_WITNESS.

New false-closure rule:

NoMaterialFrontier(Scope=s, Mode=m)
does not imply
NoMaterialFrontier globally.

Completion requires no undispositioned result-sensitive applicable 36-cell coordinate under the declared coverage basis.

## 18. ImproveCore controller consequence

ImproveCore does not “run all 36.”

ImproveCore uses the 36 architecture to:

1. detect where it has not looked;
2. decide how it is currently looking;
3. select tools with correct scope/mode context;
4. detect false closure;
5. decide when to switch mode;
6. decide when isolation is needed;
7. decide when discoveries can be coupled;
8. route material deltas across scopes;
9. calibrate tool effectiveness by context;
10. learn from repeated cell-level failure/success.

## 19. Strongest result

The 36 architecture gives ImproveCore a meta-control layer over its own tool use.

The controller no longer asks only:

“What tool is appropriate?”

It asks:

“What scope is live?”
“What search regime is justified?”
“What candidate classes become visible there?”
“What tool/package is best for that configured run?”
“What changed after execution?”
“What scope/mode becomes live next?”
“What cells remain capable of changing the protected result?”

This is a strict conceptual gain over IC-029.

## 20. Disposition

36-cell architecture:
ADMIT AS STRONG SEMANTIC CONTROLLER CANDIDATE.

36 independent tools:
REJECT.

36 exhaustive execution:
REJECT.

Scope/Mode-aware ImproveCore successor:
JUSTIFIED CANDIDATE.

Canonical/runtime promotion:
BLOCKED pending prospective ablation, selector calibration and runtime instrumentation.
