# MT — Capability Mode Cube and Center Tools 003

Date: 2026-09-24
Status: MATHEMATICAL CANDIDATE
Authority: research only

## Frozen question

Can the current repertoire be organized by a small mode geometry, which regions are underrepresented, and do "center" capabilities exist for the whole geometry and for each region?

## 1. The 2x2 is insufficient

Existing axes:
B = breadth in {EXPAND, CONTRACT}
D = direction in {OBSERVE, ACT}

The GDOS experiments showed a third result-sensitive coordinate:
C = coupling in {DECOUPLED, COUPLED}

DECOUPLED:
observer/worker operates on a frozen/local packet without consuming sibling outputs during its run.

COUPLED:
observer/worker operates with shared state, feedback, or integrated outputs.

This coordinate cannot be reduced to breadth or direction:
- EXPAND+OBSERVE can be independent GDOS or collaborative synthesis.
- CONTRACT+ACT can be delegated specialist execution or tightly coupled micro-editing.
- EXPAND+ACT can be parallel candidate generation or integrated redesign.
- CONTRACT+OBSERVE can be independent discriminators or iterative narrowing with shared state.

Therefore candidate mode cube:

M = B x D x C.

Eight octants.

## 2. Octants

EO-D:
EXPAND + OBSERVE + DECOUPLED
Broad independent discovery.
Prototype: GDOS.

EO-C:
EXPAND + OBSERVE + COUPLED
Broad integrative sensemaking.
Prototype: reconciliation / multi-object synthesis / architecture scan.

CO-D:
CONTRACT + OBSERVE + DECOUPLED
Independent exact discrimination.
Prototype: focused resolution / typing / proposition freeze / holdout.

CO-C:
CONTRACT + OBSERVE + COUPLED
Iterative local resolution using accumulated state.
Prototype: recursive dependency descent / diagnosis / closure refinement.

EA-D:
EXPAND + ACT + DECOUPLED
Parallel successor/candidate generation with preserved plurality.
Prototype: rival generation / independent redesign candidates.

EA-C:
EXPAND + ACT + COUPLED
Integrated whole-system improvement.
Prototype: Improvement Core / architecture improvement / RTC-style strengthening.

CA-D:
CONTRACT + ACT + DECOUPLED
Bounded delegated specialist execution.
Prototype: real skill/tool invocation.

CA-C:
CONTRACT + ACT + COUPLED
Precise coordinated mutation inside a live integrated system.
Prototype: constrained edit / repair / transfer handoff / local state update.

## 3. Why coupling is the right third axis

Evidence:
1. GDOS benefit increased sharply when independent observations were protected.
2. Immediate reconciliation/mutation changed later observations.
3. Skill use requires temporary local transformation autonomy.
4. Reintegration is a separate step after local execution.
5. Multi-object interactions can be lost when everything is either always independent or always coupled.

Thus coupling controls information contamination and local autonomy.

## 4. "Center" is not arithmetic averaging

For a region Q with capability set H_Q, define a center capability c_Q by contextual reconstruction:

c_Q is a center when it captures the maximal common protected function shared across H_Q without importing functions that are not common to that region.

Candidate center criterion:

Core(Q) = intersection over h in H_Q of ProtectedFunction(h | Q)

subject to:
- no result-sensitive distinction in Q is erased;
- contextual composition remains legal;
- OPEN and plurality preserved.

A center is therefore a behavioral meet/core, not a popularity average.

## 5. Whole-space center

A global center cannot be one operator that "does everything."

The common function across all octants is orchestration:
- freeze target/job;
- type dominant risk;
- choose mode;
- choose capability/package;
- bind/delegate or isolate;
- preserve receipts/provenance;
- reconcile/reintegrate;
- verify;
- reenter.

Candidate whole-space center:
MODE ORCHESTRATOR.

This is a controller meta-capability, not a ninth primitive role.

## 6. Region-center candidates

EO-D center:
OBSERVATION SWEEP
Job: maximize material structural observation under frozen target while suppressing sibling contamination and premature utility filtering.

EO-C center:
RECONCILER
Job: combine plural observations into one provenance-preserving structure without yet selecting an intervention.

CO-D center:
DISCRIMINATOR
Job: freeze one question and isolate the minimal coordinate(s) that determine its typed result.

CO-C center:
RESOLVER
Job: iteratively narrow a local unresolved structure using cumulative evidence/state until unique, plural, or OPEN disposition is justified.

EA-D center:
RIVAL/SUCCESSOR FORGE
Job: generate structurally distinct action candidates independently before selection.

EA-C center:
SYSTEM IMPROVER
Job: integrate interacting deltas across the whole system while preserving protected behavior and strict gain.

CA-D center:
DELEGATED EXECUTOR
Job: hand a bounded local transformation to a specialized capability and return an unmodified execution receipt/result for reintegration.

CA-C center:
PRECISION MUTATOR
Job: perform a constrained local change inside shared state with dependency propagation, provenance, and regression verification.

## 7. Existing repertoire coverage hypothesis

The current repertoire is not balanced.

Strongly represented:
EO-D via GDOS/discovery/representation attack.
CO-C via diagnosis, recursive dependency, closure/reentry.
EA-C via IC, architecture improvement, RTC, strengthening.
CA-C via repair/update/transfer/artifact controls.

Moderately represented:
CO-D via typing, identity, proposition freeze, sensitivity, holdout.
EA-D via rival/successor generation and incomparability preservation.
EO-C via relate, multi-object, architecture synthesis, but no explicit pre-action reconciliation center.

Weakest represented:
CA-D real delegated specialist execution.

This matches the historical IC failure:
the system can reason globally and can mutate locally, but has weak machinery for handing a bounded transformation to a specialist and preserving that specialist's autonomous result through reintegration.

Second weak region:
EO-C explicit reconciliation before action.

## 8. Five-tool proposal vs cube proposal

Blindly building five tools (four quadrant centers + global center) would erase the coupling dimension.

Blindly building nine tools (eight octants + global center) would duplicate existing strong capabilities.

ImproveCore criterion:
build only centers whose protected core is not already reconstructed by the current repertoire.

Candidate build set:
1. MODE ORCHESTRATOR — missing explicit whole-space selector.
2. RECONCILER — partially missing / not explicit.
3. DISCRIMINATOR — partially reconstructed, but a coherent focused-resolution program is missing.
4. DELEGATED EXECUTOR — strongly missing.
5. PRECISION MUTATOR — mostly reconstructed; do not build unless gap test fails.
6. OBSERVATION SWEEP — GDOS already exists semantically; formalize rather than duplicate.
7. RIVAL/SUCCESSOR FORGE — existing generator family; no new center needed now.
8. SYSTEM IMPROVER — Improvement Core already occupies this region, but needs mode awareness.

Thus likely new capability count is four, not five or nine:
MODE ORCHESTRATOR
RECONCILER
DISCRIMINATOR
DELEGATED EXECUTOR

plus formalization of GDOS and upgrade of IC.

## 9. Interaction-center question

The "middle between things" PD-like tool corresponds to finding invariant/common function under controlled variation.

General center finder:

CENTER(H,J,Ctx,Mode)
= maximal common reconstructible protected function across H.

This is a distinct analysis tool:
CAPABILITY CENTER FINDER.

It can be applied to:
- all capabilities;
- each quadrant;
- each octant;
- arbitrary selected sets.

However, it should not itself become a permanent runtime mode tool unless experiments show repeated practical value.

## 10. Underrepresentation prediction

Most underrepresented octant:
CONTRACT + ACT + DECOUPLED.

Reason:
tool invocation requires local scope, delegation, execution truth, and reintegration.
Historical IC repeatedly substitutes semantic simulation for actual delegation.

Most underrepresented center function:
protected local autonomy.

The missing invariant is:
global controller may specify contract and authority envelope but must not rewrite the local transform during execution.

## 11. Tests

T1 classify B01-B58 by primary and secondary octants.
T2 classify C01-C49 by primary and secondary octants.
T3 compute coverage counts and identify empty/weak octants.
T4 run CENTER on each octant and compare candidate centers to existing capabilities.
T5 run CENTER globally.
T6 test whether Reconciler reconstructs from RELATE+RECONSTRUCT+interaction residual.
T7 test whether Discriminator reconstructs from typing+sensitivity+focused recursion.
T8 test Delegated Executor against semantic-simulation control.
T9 test Mode Orchestrator on cross-project holdouts.
T10 test whether adding coupling materially improves prediction over the 2x2 model.

## MT disposition

The evidence supports a 3D mode cube:
Breadth x Direction x Coupling.

Do not build nine tools by symmetry.
Build only functionally missing centers after repertoire classification and reconstruction tests.
