# MT — Bias, Mode Geometry, and Capability Use 001

Date: 2026-09-24
Status: MATHEMATICAL CANDIDATE
Authority: research only

## Target

Test whether the GDOS/FOCUS findings and Improvement Core's historical skill-use failures are partly explained by systematic bias, and determine whether bias checking is an irreducible behavior or a composite.

## 1. Bias as result sensitivity to semantically irrelevant variation

Let target object X have protected semantics P(X).
Let phi be a perturbation such that P(phi(X)) = P(X).

For a controller/capability H define:

BiasResidual(H,X,phi) =
Delta(Result(H,X), Result(H,phi(X))).

When phi is task-irrelevant relative to the protected result and the output changes materially, H is sensitive to a nuisance coordinate.

This does not prove a psychological cognitive bias.
It establishes operational bias susceptibility.

## 2. Bias families relevant to Take-5

B_sel selection bias:
which tools, sources, branches, or hypotheses are surfaced.

B_anchor anchoring/primacy:
early representation, first tool, current architecture, or prior answer changes later result.

B_confirm confirmation/myside:
evidence compatible with current model receives asymmetric search or scrutiny.

B_frame framing:
equivalent representations yield different routes/results.

B_avail availability/retrieval:
recent, easy-to-retrieve, named, or familiar capabilities dominate.

B_tool semantic-simulation/no-tool:
controller reasons with a tool's semantics rather than dispatching it.

B_close closure/completion:
pressure to finish prunes OPEN, alternatives, or unresolved coordinates.

B_form formalism/architecture:
mathematical elegance or architectural cleanliness is treated as evidence of correctness.

B_novel novelty/complexity:
new or complex objects receive unjustified preference or unjustified suspicion.

B_survive survivorship:
only retained/successful tools or artifacts are inspected.

B_authority authority/provenance:
status, source, or persistence alters evidentiary weight without licensed bridge.

B_user user-pressure:
requested direction changes evidentiary or selection threshold.

B_order order contamination:
sequential observation/mutation changes later observations.

These are operational categories; multiple may share mechanisms.

## 3. Existing capability reconstruction test

Existing repertoire already contains components that can detect portions of bias:

- representation attack: B11/C10;
- result sensitivity: B12/C11;
- hostile review: C14;
- diagnosis/root cause: B20/C17-C18;
- novelty comparator: C15/B53;
- holdout/ablation: B24/C45-C46;
- independent replication/information barrier: B48;
- stability packet: B41;
- OPEN/incomparability preservation: B19;
- source/provenance separation: B26/B52;
- noncommutation/order: B38;
- completion/closure: B25/B40/C47.

However, no current behavior has the explicit job:
"construct semantically irrelevant perturbations across known nuisance coordinates and test whether the protected result changes."

Therefore a dedicated bias behavior may be a composite program with a novel routing/perturbation job even if its internal operators are reconstructible.

## 4. Candidate behavior: Bias Perturbation Audit (BPA)

Input:
- frozen target X;
- protected semantics/result P;
- nuisance-coordinate basis N;
- controller/capability H.

For each n in N generate admissible perturbations phi_n satisfying P(phi_n(X)) = P(X).

Run H independently on X and phi_n(X).

Return:
- invariant coordinates;
- bias-sensitive coordinates;
- effect magnitude/type;
- mechanism candidates;
- OPEN where task-irrelevance of perturbation is not established.

Formal output:

BPA(H,X,P,N)
= { n in N : Result(H,X) not~_P Result(H,phi_n(X)) }.

Guard:
do not call a difference "bias" unless perturbation is licensed as irrelevant to the protected result.

## 5. BPA is not ordinary adversarial testing

Hostile review asks whether a claim fails.
Representation attack asks whether result depends on representation.
BPA asks whether the system's result changes under a structured basis of nuisance coordinates that ought not change the protected result.

It is cross-cutting across representation, order, retrieval, familiarity, naming, authority cues, goal cues, and tool availability.

Candidate status:
composite behavior with possible irreducible perturbation-basis/routing function.

## 6. Connection to GDOS and FOCUS

GDOS suppresses one large nuisance coordinate:
object-level outcome pressure.

FOCUS increases a different selector:
scope restriction around a frozen discriminating question.

Therefore both can be understood as bias-control regimes.

GDOS controls premature outcome-selection bias.
FOCUS controls irrelevant-scope/attention dilution.

They are not universally unbiased.

GDOS can introduce:
- over-expansion;
- equal-attention distortion;
- observer-basis bias;
- reconciliation bias.

FOCUS can introduce:
- anchoring;
- frame lock;
- omitted-variable bias;
- premature typing;
- local-closure bias.

Thus the controller needs bias-aware regime selection, not one preferred regime.

## 7. Two-axis mode geometry

Axis A: breadth
EXPAND <-> CONTRACT.

Axis B: directionality
OBSERVE <-> ACT.

Quadrants:

EXPAND+OBSERVE = GDOS.
CONTRACT+OBSERVE = focused typing/provenance/identity resolution.
CONTRACT+ACT = specialized skill/tool execution.
EXPAND+ACT = architecture/system redesign or broad candidate generation.

This model explains why specialized skill use is not solved merely by adding GDOS.

## 8. Improvement Core skill-use hypothesis

Historical IC appears biased toward broad integrative control.

That can create a controller self-preference:
global synthesis is treated as the default transformation substrate.

A specialized skill requires:
1 exact target/input freeze;
2 scope contraction;
3 binding;
4 local transformation authority;
5 execution receipt;
6 reintegration.

IC can fail at step 4 even after selection and binding:
it retains transformation control and semantically simulates the skill.

Define:

SemanticUse(skill) = global controller reconstructs the skill's reasoning.

RealUse(skill) =
Select
AND Bind
AND DelegateLocalTransform
AND Execute
AND Receipt
AND Reintegrate.

The earlier root-cause repair addresses Select/Bind visibility.
It does not yet guarantee DelegateLocalTransform.

## 9. Behavior combination classes

Pairwise "combination" is not one operation.

For h_i,h_j distinguish:

ADD:
independent outputs union.

SEQUENCE:
h_j(h_i(X)).

GATE:
h_i determines whether h_j may run.

ENABLE:
h_i creates information/state needed by h_j.

INHIBIT:
h_i reduces or blocks h_j's accessible state/search space.

RESIDUAL:
joint result contains structure not reconstructible from either output.

MODULATE:
one behavior changes the regime/parameters under which the other operates.

These classes can change with Mode.

Therefore interaction object is:

Interaction(h_i,h_j,X,Mode,Order).

## 10. Mode-sensitive bias

Bias susceptibility itself may change across modes:

BiasResidual(H,X,phi | Mode).

A tool pair can be unbiased in normal mode and biased in GDOS or FOCUS, or the reverse.

Thus capability equivalence becomes:

h_i ~_{J,Ctx,Mode,N} h_j

where N is the nuisance-perturbation basis relevant to the protected job.

## 11. Root-cause update for IC tool resistance

Three layers now exist:

A. selection failure
tool not surfaced/selected.

B. binding failure
selected semantic capability lacks executable adapter.

C. delegation failure
bound skill is not allowed to control its local transformation; IC simulates it internally.

Possible D. reintegration bias
skill output is executed but global controller rewrites/discounts it during synthesis.

This predicts recurring "tool nonuse" even after selection routing is fixed.

## 12. Tests

T1 task-irrelevant renaming perturbation.
T2 capability-order perturbation.
T3 previous-answer exposure vs information barrier.
T4 tool familiarity/name visibility perturbation.
T5 equivalent framing perturbation.
T6 goal cue present vs suppressed.
T7 authority/source cue perturbation.
T8 broad vs focused regime with invariant target semantics.
T9 real skill execution vs semantic simulation.
T10 reintegration test: preserve exact skill output before and after global synthesis.
T11 mode-selection preflight bias: alternate plausible task typings.
T12 survivor test: include failed/rejected/historical capabilities in opportunity set.

## MT disposition

A bias-checking capability is justified as a candidate composite program because the current repertoire lacks an explicit nuisance-perturbation sweep and bias-specific result carrier.

Do not yet promote BPA as a new primitive.
Test whether its function is reconstructible from representation attack + sensitivity + holdout + noncommutation + information barrier + routing.

The deeper current object is:
BIAS-AWARE MODE-SENSITIVE CAPABILITY ORCHESTRATION.
