# Focus and Deterministic Route Contract 054

Date: 2026-09-25

Status: CURRENT WORKING DESIGN CANDIDATE

Runtime effect: NONE until separately implemented and validated

Depends on:
- architecture/WRAPPER_CANONICAL_CONTRACT_053.md
- architecture/KERNEL_MATH_CONTRACT_052.md
- runtime/kpd_projection.py
- runtime/full_spectrum_20.py

Purpose: close the wrapper's two highest-dependency open coordinates in the correct order:
(1) exact Focus mathematics;
(2) deterministic Route input/output law.

## 1. Focus is a projection, not a chooser

Let the frozen mathematical object be mbar.

Let C(mbar) be the set of typed coordinates represented in mbar.

Let g be the frozen operational goal.

Let R(c,g,mbar) be the result-sensitivity predicate:

R(c,g,mbar)=1 iff there exist two admissible states m1,m2 differing only on coordinate c such that the goal-relevant result differs.

Formally:

R(c,g,mbar)=1
iff
exists m1,m2 in Adm(mbar):
  SameExcept(m1,m2,c)
  AND Result_g(m1) != Result_g(m2)

Define the focus set:

F(mbar,g)
=
{ c in C(mbar) | R(c,g,mbar)=1 }

This means Focus does not choose what seems interesting.
It preserves exactly the coordinates whose admissible variation can change the goal-relevant result.

If result sensitivity cannot yet be determined for c, then:

FocusDisposition(c)=OPEN

and c remains live rather than being discarded.

## 2. Focus completeness

Focus is complete relative to the current representation iff every coordinate has a disposition:

FOCUS_IN
FOCUS_OUT_CERTIFIED
OPEN
BLOCKED

FOCUS_OUT_CERTIFIED requires a witness that variation in c cannot change the goal-relevant result under the current admissible state set.

No coordinate is excluded merely because it appears low-salience.

## 3. Route input

Route receives the frozen object plus focused live obligations.

Define the routing state:

rho
=
<
  identity,
  type,
  scope,
  job,
  readings,
  result_sensitive,
  selectors,
  authority,
  provenance,
  open,
  obligations,
  relations,
  geometry,
  execution_state,
  currentness_state,
  protected_delta
>

The first ten coordinates align with K_PD projection.

Route may not use hidden conversational intuition as an input coordinate.


## 3A. Eight-role routing basis

Route does not operate directly on an unstructured bag of fields.

The recovered eight-role basis is:

T8
=
<
  K,
  S,
  O,
  G,
  M,
  C,
  R,
  U
>

with:

K = Context
S = State
O = Operator
G = Generator
M = Modifier
C = Control
R = Router
U = Update / Dynamics

The routing state rho is projected into these eight role objects before trigger evaluation.

Each role may carry multiple typed fields from rho, but the role identity is preserved.

Route therefore has the form:

rho
-> T8(rho)
-> H8(rho)
-> Trigger_i

where H8 is the typed relation structure among the eight roles.

Relevant relation classes include:
- dependency;
- order;
- authority;
- provenance;
- result sensitivity;
- transition;
- interaction;
- update consequence.

The eight-role basis constrains routing so that tool triggers are derived from structure rather than from unconstrained discretionary choice.


## 4. Tool contract

Every tool family T_i has:

T_i
=
<
  In_i,
  Out_i,
  Trigger_i,
  Covers_i,
  CostProbe_i,
  CostExec_i
>

Trigger_i(rho) has four legal outputs:

REQUIRED
NON_APPLICABLE
OPEN
BLOCKED

REQUIRED is deterministic from the typed routing state.

OPEN is mandatory when the trigger cannot be decided from available evidence.

## 5. Deterministic route

The required tool package is:

P_req(rho)
=
{ T_i | Trigger_i(rho)=REQUIRED }

The unresolved routing set is:

P_open(rho)
=
{ T_i | Trigger_i(rho)=OPEN }

The wrapper may not silently convert OPEN into NON_APPLICABLE.

Execution can proceed only when every result-sensitive obligation is covered by P_req or explicitly remains OPEN/BLOCKED.

## 6. Geometry is orthogonal to tool identity

For every required tool T_i, geometry selection is a separate function:

Gamma_i
=
Geometry(T_i,rho)

with current legal geometry types:

1
D36_C
D36_H
D216
D288

Tool identity does not determine geometry by name alone.

## 7. Initial FULL-SPECTRUM-20 trigger contract

The following trigger predicates are design contracts, not runtime claims.

### GOAL_TARGET_FREEZE

REQUIRED iff target, job, goal, or completion identity is absent, ambiguous, changed, or not frozen.

### DOS_OBSERVE

REQUIRED at episode entry and after any HF1 REENTER.

### MTA

REQUIRED iff the observed object lacks an explicit mathematical representation or contains an undefined load-bearing object.

### MT_MODE_SWEEP

REQUIRED iff a mathematical object or transform has changed and the effect of that change is result-sensitive or OPEN.

### PD

REQUIRED iff two or more live readings/objects/representations may differ in a result-sensitive way and their equivalence has not been established.

### PD_AUDIT

REQUIRED iff a PD distinction materially affects routing, architecture, execution, closure, or protected behavior and has not yet been independently verified.

### MULTI_OBJECT_MOMT

REQUIRED iff more than one live object exists and at least one inter-object relation is result-sensitive or OPEN.

### ARCHITECTURE

REQUIRED iff ownership, ordering, dependency, interface, boundary, authority placement, or control placement is result-sensitive or changed.

### ROOT_CAUSE

REQUIRED iff a recurrent or material failure is observed and the failure-generating mechanism is not already established.

### ARA_ARTIFACT_REALITY

REQUIRED iff a claim about implementation, artifact state, runtime state, or repository state is result-sensitive and not directly verified.

### ORPHAN_GHOST_CONFLICT

REQUIRED iff identity, lineage, duplication, unresolved reference, ghost object, or conflict evidence is present or OPEN.

### CURRENTNESS

REQUIRED iff the governing basis or any result-sensitive dependency may differ from the basis used to build the current component.

### ROLE_ASSIGNMENT_OWNER_CLOSURE

REQUIRED iff a live obligation lacks explicit semantic owner, authority owner, executor, verifier, or consumer.

### CONSEQUENCE_AFFECTED_CONE

REQUIRED iff a material change has downstream effects whose complete affected set is not yet certified.

### RTC_RAISE_CEILING

REQUIRED iff the current candidate/solution space is known or evidenced to be constrained by a result-sensitive ceiling and lower-cost available routes have saturated without closure.

### MTOS

REQUIRED iff the operating structure of the tool/wrapper/system itself is the result-sensitive object under analysis.

### TRANSFER_CORE

REQUIRED iff a protected behavior, mathematical object, or capability is being transferred across representation, component, repository, layer, or version boundary.

### EXECUTION_TRUTH_ACTIVATION

REQUIRED iff the result depends on whether selected work was actually bound, dispatched, started, executed, captured, and consumed.

### A16_HOLDOUT_ABLATION

REQUIRED iff a strong preservation, equivalence, completion, or improvement claim depends on behavior outside the construction cases or on the necessity of load-bearing components.

### GOAL_COMPLETION_CERT

REQUIRED iff the episode is attempting relative closure.

## 8. Probe versus execution

Every Trigger_i evaluation is the cheap probe.

The heavy tool executes only when Trigger_i=REQUIRED.

Therefore the wrapper can consult all 20 trigger contracts each routing round without executing all 20 tools.

Probe cost and heavy execution cost are distinct:

CostProbe_i << CostExec_i

is a design target, not assumed proof.


## 8A. A16 placement

A16 is not a primary selector.

Its role is adversarial verification after candidate execution and before strong preservation, equivalence, completion, or promotion claims cross closure.

Operational placement:

Execute
-> A16 when triggered
-> Evaluate
-> Tool Run Closure

A16 may use:
- holdout;
- ablation;
- hostile cases;
- alternate representations;
- edge-interaction challenges.

A16 therefore attacks the preservation or completion claim rather than choosing the initial tool package.


## 9. Interaction rule

Triggers are recomputed after every material tool result.

If tool T_j changes rho materially:

rho_n -> rho_(n+1)

then:

P_req(rho_(n+1))

is recomputed from scratch.

A previously NON_APPLICABLE tool can become REQUIRED.
A previously REQUIRED tool can become NON_APPLICABLE only with a certified basis.

## 10. Human correction

A result-sensitive human correction Delta_H is added to the routing state as evidence.

If Delta_H changes any coordinate used by Focus or Route:

Delta_H != 0
=> HF1
=> Observe
=> Phi
=> Freeze
=> Goal
=> Focus
=> Route

The previous route is not reused automatically.

## 11. Preservation delta against Wrapper Contract 053

This artifact does not reorder the wrapper.

It refines two previously OPEN stages:

O1 Focus mathematics:
OPEN -> CANDIDATE_DEFINED

O2 deterministic Route mathematics:
OPEN -> CANDIDATE_DEFINED

O3 full tool trigger equations:
OPEN -> CANDIDATE_DEFINED_FOR_FULL_SPECTRUM_20

No protected invariant from Wrapper Contract 053 is removed.

Additional preserved structure:
- the eight-role basis T8=<K,S,O,G,M,C,R,U> now constrains Route;
- A16 is placed as adversarial verification after execution, not as a free selector.

Remaining OPEN:
- exact field-to-role projection for every routing-state field;
- exact H8 relation algebra;
- proof/validation that the result-sensitivity test is computationally realizable across current object types;
- runtime implementation of Focus;
- runtime implementation of all trigger predicates;
- exact geometry-selection law;
- exact Eval mathematics;
- human-visible-math formalization;
- cost measurements;
- runtime parity.

## 12. Required validation before promotion

Promotion requires:
- PD and PD Audit over every trigger boundary;
- holdout cases where surprising tools become REQUIRED;
- ablations showing removed trigger families create detectable loss;
- execution-truth evidence that REQUIRED tools actually execute;
- regression against current wrapper invariants;
- HF1 reentry tests where routing changes after a material delta.
