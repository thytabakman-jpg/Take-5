# Architecture Analysis — Mode Cube Capability Placement 001

Date: 2026-09-24
Status: ARCHITECTURE CANDIDATE
Authority: research only
Input: research/MT_CAPABILITY_MODE_CUBE_003.md

## 1. Architectural object

Mode cube:
Breadth x Direction x Coupling

Breadth:
EXPAND / CONTRACT

Direction:
OBSERVE / ACT

Coupling:
DECOUPLED / COUPLED

These are controller/execution-regime coordinates, not new foundational system roles.

## 2. Placement rule

K:
owns legal-transition and experiment-integrity constraints only.

S:
stores mode, local/frozen packet identity, independent outputs, shared-state lineage, receipts.

O/G/M/C:
perform substantive work inside a mode.

R/controller:
chooses mode, capability/package, order, and switching.

Interface:
binds and scopes local execution; establishes delegation envelope.

Runtime:
executes selected bound capability.

Verification:
tests local contract, protected result, reintegration, and mode/perturbation claims.

Therefore Mode is best represented as an execution/configuration coordinate consumed across R/M/interface/runtime rather than a ninth role.

## 3. Octant architecture

### EO-D: Expand Observe Decoupled
Primary responsibility:
independent broad discovery.
Existing anchors:
GDOS, hidden dependency, representation attack, corpus navigation, independent discovery.
Architecture status:
strong semantic coverage; needs formal program contract, not new conceptual primitive.

### EO-C: Expand Observe Coupled
Primary responsibility:
integrative observation/sensemaking before action.
Existing anchors:
RELATE, RECONSTRUCT, Multi-Object, dependency spine, architecture scan.
Architecture status:
partial.
Missing center:
explicit provenance-preserving RECONCILER that consumes frozen independent observations without converting them into an intervention.

### CO-D: Contract Observe Decoupled
Primary responsibility:
exact discrimination on frozen local question.
Existing anchors:
typing, identity, currentness, result sensitivity, independent holdout, proposition freeze.
Architecture status:
moderate but fragmented.
Missing center:
coherent DISCRIMINATOR/Focused Resolution program.

### CO-C: Contract Observe Coupled
Primary responsibility:
iterative local diagnosis/closure using cumulative state.
Existing anchors:
root cause, recursive dependency, relative closure, failure memory, actionable continuation.
Architecture status:
strong.

### EA-D: Expand Act Decoupled
Primary responsibility:
parallel candidate/successor generation preserving plurality.
Existing anchors:
rival reconstruction, successor generation, incomparability preservation.
Architecture status:
moderate/strong semantically; runtime binding incomplete.

### EA-C: Expand Act Coupled
Primary responsibility:
whole-system integrated improvement.
Existing anchors:
Improvement Core, system architecture improvement, cross-layer improvement, RTC.
Architecture status:
strong semantically; controller/runtime gaps remain.

### CA-D: Contract Act Decoupled
Primary responsibility:
bounded specialist execution under local transformation autonomy.
Existing anchors:
binding, bounded authority, delegation concepts.
Architecture status:
weakest region.
Missing center:
DELEGATED EXECUTOR with exact execution/reintegration truth.

### CA-C: Contract Act Coupled
Primary responsibility:
precise mutation in shared state with propagation and verification.
Existing anchors:
repair, constrained edit, transfer handoff, update, artifact authority.
Architecture status:
strong/moderate.

## 4. Global center

No substantive transform is common to all octants.

The architectural center is orchestration:

TargetFreeze
-> RiskType
-> ModeSelect
-> CapabilitySelect
-> IsolationOrCouplingContract
-> Bind/Delegate
-> Execute/Observe
-> Reconcile/Reintegrate
-> Verify
-> Reenter.

Candidate capability:
MODE ORCHESTRATOR.

Placement:
controller meta-program over existing roles.

Not Kernel.

## 5. Center finder

The user's "find the middle" operation is itself valuable.

Define CAPABILITY CENTER FINDER as an epistemic analysis program:

Input:
capability set H, job J, mode region M, licensed contexts Ctx.

Output:
maximal common reconstructible protected function,
plus residual distinctions and non-equivalent members.

This is essentially a generalized PD/MTA-style meet finder.

Placement:
epistemic/controller research program.
It does not become a runtime controller by default.

## 6. Architecture risks

A. Symmetry bias:
building one tool per octant because the geometry is symmetric.

B. Center-collapse bias:
assuming every region has a nontrivial common center.

C. Tool-reification:
turning mode configurations into named tools when existing compositions already reconstruct them.

D. coupling leakage:
calling a run "decoupled" while sibling results or shared state leak in.

E. local-autonomy failure:
delegated execution remains globally rewritten.

## 7. Build decision criterion

A new center capability is justified only when:

1. the region has repeated material jobs;
2. no existing capability reconstructs the center across licensed contexts;
3. the center has an executable contract;
4. it changes protected results or execution truth;
5. it integrates without adding a new primitive role.

## 8. Current architecture conclusion

Build candidates:
- Mode Orchestrator
- Reconciler
- Discriminator
- Delegated Executor

Formalize/upgrade:
- GDOS as EO-D regime program
- Improvement Core as mode-aware EA-C/global controller
- Capability Center Finder as research/meta-analysis tool

Do not build now:
- new EA-D center, because rival/successor generation already covers it;
- new CO-C center, because diagnosis/recursive closure already cover it;
- new CA-C center, because repair/update/transfer machinery already covers it.

## 9. Expected leverage

Highest leverage:
Delegated Executor, because it repairs a known recurring execution failure.

Second:
Mode Orchestrator, because it prevents using the wrong regime.

Third:
Reconciler, because GDOS requires it and current architecture only reconstructs it implicitly.

Fourth:
Discriminator, because the low-GDOS-gain precision family is currently fragmented rather than absent.

Research leverage:
Capability Center Finder, because it can compress each region and test whether future tool creation is justified.
