# Goal-Decoupled Observation Sweep Cross-Sectional Study 001

Date: 2026-09-24
Status: EXPERIMENT DESIGN
Authority: research only

## Research object

Goal-Decoupled Observation Sweep (GDOS) is treated as a controller mode:

freeze target
-> suppress target-level optimization/repair/confirmation pressure
-> permit capability-relative observation
-> preserve independent outputs
-> reconcile only after observation
-> restore goal conditioning only after reconciliation.

The study tests what GDOS changes, where it helps, where it harms, and which capability interactions are responsible.

## Core hypotheses

H1 Goal conditioning before observation and goal conditioning after reconciliation do not commute.

H2 The gain attributed to GDOS contains separable contributions from:
- target freezing;
- goal decoupling;
- observer independence;
- deferred reconciliation.

H3 GDOS benefit varies by observer capability family and target capability family.

H4 Some directed pairs are asymmetric:
A observing B under GDOS != B observing A under GDOS.

H5 Some gains require pair or package interaction rather than single-capability observation.

H6 Full repertoire execution is not necessary; factor/family coverage plus targeted residual sampling can recover most material effects.

## Universe

Behavior families: B01-B58.

Behavior factor strata:
F1 DIFFERENTIATION
F2 RELATION
F3 RECONSTRUCTION
F4 STRENGTHENING
F5 GENERATION
F6 ADMISSION/GOVERNANCE
F7 ROUTING/REENTRY
F8 UPDATE/STATE TRANSITION
F9 VERIFICATION/CLOSURE
F10 REPRESENTATION/MODIFIER

Current tool families:
ORIENT C01-C06
MAP C07-C13,C49
ATTACK C14-C19
GENERATE C20-C23
IMPROVE C24-C35,C48
TRANSFER C36-C43
VALIDATE C44-C47

Special architectural targets:
Improvement Core
Kernel K
Router R
Capability Foundry
Capability Router
GDOS itself

## Stage 1: Exhaustive single-object sweep

Run GDOS once on every B01-B58 and every C01-C49 as target objects.

For each target record:
- new distinctions;
- hidden assumptions;
- dependencies;
- boundary conditions;
- failure modes;
- interactions suggested;
- whether observation duplicates known structure;
- whether a new load-bearing object is introduced;
- materiality after later reconciliation.

This is exhaustive because N is small enough and no pair explosion occurs.

Total target runs: 107 plus special architectural targets.

## Stage 2: Paired control for every factor/tool family

For sampled observer-target pairs run matched conditions:

CONTROL:
observer capability applied to target with explicit improvement/solution goal.

GDOS:
same observer, same frozen target, observation-only instruction, no object-level optimization, independent output.

Primary contrast:
Delta_GDOS = material discoveries_GDOS - material discoveries_CONTROL.

Also record:
- overlap;
- unique control findings;
- unique GDOS findings;
- false-positive/nonmaterial yield;
- contradiction rate;
- downstream usefulness only after reconciliation.

## Stage 3: Cross-family covering design

### Behavior x behavior

Use the 10 factor strata.

Require at least one directed observer-target sample for every ordered factor pair:
F_i -> F_j for all i,j.

That gives 100 factor cells rather than 58*58 raw combinations.

For diagonal cells use two distinct members of the same factor when possible.

Add a second replicate in cells showing:
- large GDOS-control difference;
- asymmetry;
- interaction residual;
- high variance;
- OPEN result.

Base behavior-pair sample: 100 directed pairs.
Adaptive expansion only where evidence warrants it.

### Tool x tool

Use seven operational tool families.

Require every ordered family pair:
7 x 7 = 49 cells.

Select one concrete directed C-tool pair per cell.
Within-family cells use distinct tools.

Add reverse-direction counterpart automatically when the first direction produces a material result.

Base tool-pair sample: 49 directed pairs.

### Behavior x tool

Cross the 10 behavior factors with seven tool families in both directions:

Behavior -> Tool: 70 cells.
Tool -> Behavior: 70 cells.

One representative pair per cell initially.

Base cross-level sample: 140 directed pairs.

## Stage 4: High-value full matrices

Do not full-matrix the whole repertoire.

Full-matrix only small anchor sets.

Anchor set A:
- B07 Differentiate
- B08 Relate
- B09 Reconstruct
- B10 Strengthen
- B13 Interaction Residual
- B16 Route
- B20 Diagnose
- B23 Verify
- B38 Noncommutation
- B40 Completion
- Improvement Core
- Kernel

12 x 11 ordered cross-object runs = 132.

This deliberately includes the four substantive operators, control, diagnosis, verification, interaction/order, closure, IC, and Kernel.

## Stage 5: Component ablation of GDOS

On a smaller anchor sample run a 2x2x2 design over:

G: goal-directed vs goal-decoupled
I: sequential influence vs independent observers
R: immediate reconciliation/intervention vs deferred reconciliation

Freeze remains ON in the primary design.

Eight conditions per selected pair.

Use at least one pair from each of the ten behavior factors and each of the seven tool families, with overlap allowed.

Purpose:
separate the effects of decoupling, independence, and deferred reconciliation.

Then run a freeze ablation on the highest-yield subset:
frozen target vs mutating target.

## Stage 6: Order and direction tests

For every material A -> B result, test B -> A on a stratified subset.

For pairs where sequential composition is meaningful test:

A then B
B then A
independent A and B then reconcile.

Record noncommutation residual:

NCR(A,B) = R(A(B(X))) != R(B(A(X)))

and compare with independent reconciliation.

## Stage 7: IC-specific experiment

Improvement Core is both observer and target.

Run:

1. GDOS on IC using every behavior factor.
2. IC normal mode on GDOS.
3. IC under GDOS mode on GDOS.
4. Each anchor behavior observing IC under GDOS.
5. IC observing each anchor behavior under GDOS.
6. IC with capability-selection pressure enabled vs suppressed during observation.
7. Reconciliation by IC only after independent outputs are frozen.

This tests whether IC itself is the source of premature goal filtering.

## Stage 8: Kernel-specific experiment

Run the same anchor design with Kernel as target.

Questions are observational, not improvement prompts:
- what global invariants Kernel actually contains;
- which responsibilities are merely historical placement;
- which IC behaviors depend on K;
- which apparent K functions reconstruct from controller/state/interface instead;
- which GDOS findings imply a legal-transition invariant rather than controller policy.

Then compare normal architecture analysis vs GDOS architecture observation.

## Measurement

Do not score with one scalar.

For every run record a result vector:

V = <
novel_material_findings,
known_findings_recovered,
nonmaterial_findings,
contradictions,
new_dependencies,
new_interactions,
new_OPEN,
new_load_bearing_objects,
downstream_changes_after_reconciliation,
observer_target_asymmetry,
execution_cost
>.

Primary evidence is paired and structural, not a global winner score.

## Sampling totals before adaptive expansion

Single-object sweeps:
107 + special targets.

Base pair sampling:
100 behavior-factor cells
49 tool-family cells
140 cross-level cells
132 anchor full-matrix cells

Some overlap is intentional and must be deduplicated by exact observer-target-condition identity.

The study therefore samples hundreds rather than thousands of directed combinations while guaranteeing family-level coverage.

## Adaptive rule

Expand a cell only when one of these occurs:
- material GDOS-control residual;
- observer-target asymmetry;
- noncommutation;
- contradiction;
- unexplained variance;
- new load-bearing object;
- OPEN that another within-cell representative can discriminate.

Stop expanding a cell when two independent representatives produce no new material residual relative to the frozen measurement basis.

## Critical controls

- identical frozen target packet across matched conditions;
- observer identity frozen;
- no contamination from prior paired result before independent run;
- reconciliation after observation in GDOS arm;
- exact provenance for every observation;
- distinguish semantic application from runtime execution;
- preserve OPEN and incomparable results;
- randomize or counterbalance run order where prior-output contamination is possible.

## First recommended experimental tranche

Run these first because they discriminate the theory rapidly:

A. all 58 behavior self/target GDOS sweeps;
B. all 49 tool target GDOS sweeps;
C. the 12-anchor directed matrix;
D. 17 matched GDOS/control pairs, one anchored in each behavior/tool family;
E. eight-condition component ablation on four high-yield pairs;
F. IC and Kernel reciprocal observation matrix.

Only after those results decide whether the full 100+49+140 family-cell study is worth completing.
