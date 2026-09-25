# 6 x 6 x 6 Foundation Architecture 031

Date 2026-09-24
Status candidate foundation successor
Migration remains paused pending validation

## Recovered idea

Three distinct six-structures now exist and must not be collapsed.

A. Source scope
S_src = {SYSTEM,SUBSYSTEM,COMPONENT,INTERFACE,BOUNDARY_DECOMPOSITION,CROSS_LAYER}

B. Target scope
S_dst = same six-scope set.

Together these produce the already-supported 36 directed scope-transition cells:
E_scope = S_src x S_dst.
|E_scope| = 36.

C. Mode face / control pole
F_mode = {EXPAND,CONTRACT,INWARD,OUTWARD,ISOLATE,COUPLE}.

The full new hypothesis is therefore not 36 independent dimensions.
It is a structured tensor/product:

A_666 = S_src x S_dst x F_mode

with 6 x 6 x 6 = 216 possible scope-transition/mode-face cells.

The user's reference to 36 is preserved correctly as the middle architecture:
6 x 6 = 36 directed scope transitions.
The new third six does not make arithmetic 36; it lifts each of the 36 transitions through six mode faces.

Mode itself has a deeper representation:
Mode = Breadth x Direction x Coupling
with 2 x 2 x 2 = 8 full corner configurations and six poles/faces.

Therefore 216 is a face-indexed control surface, not 216 independent primitives and not eight-mode equivalence.

## Run identity

Run =
<ToolFamily,
 SourceScope,
 TargetScope,
 TransitionKind,
 Mode,
 Contract,
 State,
 Views,
 CandidateUniverse,
 Evidence,
 Authority>.

TransitionKind in {SELF,PROJECT,LIFT,RELATE,REDECOMPOSE,TRANSPORT}.

Mode =
<Breadth,Direction,Coupling>.

The six face labels are projections/constraints on Mode, not complete Mode values.

## Foundation geometry

Tool family answers WHAT semantic job.
Source/target scope answers WHERE FROM / WHERE TO.
Mode answers HOW search/control moves.
Contract answers UNDER WHAT protected job/authority.
State/views answer FROM WHAT CURRENT WORLD.
Evidence answers WITH WHAT GROUNDS.

This prevents tool choice from accidentally encoding scope or search policy.

## Kernel candidate

Kernel is the smallest always-on legality layer. It does not do the research itself.

K666 owns:
1 exact run/tool/referent identity
2 protected behavior/currentness
3 source scope identity
4 target scope identity
5 typed transition legality
6 mode identity
7 authority/license
8 evidence/provenance
9 OPEN/BLOCKED/CONFLICT preservation
10 execution truth
11 decomposition-change admission
12 cross-layer transport evidence
13 representation/candidate-universe reentry
14 no self-promotion
15 closure relative to scope-transition x mode x generator x evidence basis

It does not own:
candidate content generation,
domain reasoning,
tool-family semantics,
successor choice beyond legality,
or substantive truth.

## Controller

ImproveCore selects a nondominated continuation over:

ToolFamily x admissible ScopeEdge x Mode x Package

rather than ToolName alone.

Cycle:
freeze K/state
-> recover residuals
-> select source scope
-> select admissible target/stay edge
-> select mode
-> generate mode/scope-indexed candidate universe
-> select semantic family/package
-> bind runtime
-> execute
-> verify/admit
-> update state/views
-> recompute candidate universe
-> compare scope/mode frontier
-> reenter or close relative to declared basis.

## RCDL integration

RCDL becomes the discovery-state feedback law inside this architecture:

admitted delta
-> state/view update
-> candidate-universe change
-> scope/mode frontier change
-> reentry.

A run can therefore reopen because:
protected result changed;
view changed;
candidate universe changed;
scope relevance changed;
mode frontier changed;
authority/evidence/runtime reality changed.

## Why this is stronger

Flat six loses direction.
6x6 directed scope graph recovers direction and handoff legality.
Adding the mode six prevents a correct scope transition from being executed under the wrong search/control regime.

Examples:
SYSTEM->COMP under EXPAND is not equivalent to SYSTEM->COMP under CONTRACT.
COMP->SYSTEM under COUPLE has different contamination/aggregation risk than under ISOLATE.
BND->SYSTEM under EXPAND can generate alternative architectures; under CONTRACT it can select among admitted decompositions.
XL->INT under ISOLATE is a challenge/holdout transport; under COUPLE it can propagate live evidence into the handoff.

## Anti-numerology guard

No claim that every cell must execute.
No claim that every tool needs all 216 cells.
No claim that six is minimal/complete universally.
No claim that the six mode faces are six independent axes.
No claim that 216 are primitive dimensions.

For each family, admissible cells form a partial typed tensor:
A_F subseteq S_src x S_dst x F_mode.

Expansion is witness-gated by result sensitivity, noncommutation, changed OPEN state, protected-result change, or reachable-continuation change.

## Validation obligations

1 six-scope ablation
2 directed-edge ablation
3 breadth ablation
4 direction ablation
5 coupling ablation
6 scope-edge x mode interaction
7 order/noncommutation
8 representation/view regeneration
9 false-positive and search-cost accounting
10 unlike-domain holdout
11 historical Take-2/Take-4 reconstruction
12 current Take-5 regression
13 cross-layer execution receipts
14 decomposition-change challenge
15 candidate-universe closure challenge

## Migration consequence

This architecture is a candidate successor to the current Take-5 foundation.
It preserves T=<K,S,O,G,M,C,R,U> as semantic algebra and adds orthogonal run geometry/control.
Migration is still intended, nondestructive, and blocked until this successor is implemented and validated.
