# Question Search Math 001

Date: 2026-09-25
Status: EXECUTED FIRST FULL RECOVERED-UNIVERSE PASS
Controller: Improvement Core / question-lineage audit

## Job

Recover the distinct question families actually present across the known system history without
counting names, wrappers, scope/mode projections, or later mathematical rewrites as new questions.

## Universe

Let H be the recovered tool-history universe:

H = C49 ∪ CAP33 ∪ NamedTools ∪ FullSpectrum20 ∪ NovelFrontier10 ∪ MaterialLineageArtifacts.

This is exhaustive relative to the currently recovered registries/ledgers used by Take-5.
Unknown history outside those recovered sources remains OPEN.

## Atomic question object

q = <Issue,Target,AnswerSpace,Presuppositions,ResolutionCondition,ProtectedResult>.

For historical tool state h, Atom(h) returns the smallest set of result-sensitive question
objects whose answers reconstruct h's epistemic output. Execution, persistence, authority,
binding, routing and state mutation are not question atoms.

## Projection normalization

Let L36 = Scope6 × ModeFace6.

For q asked at cell l:

q_l = q ∘ pi_l.

If changing l changes only source/target projection, search regime, coupling, or observation
direction while preserving Issue, AnswerSpace and ResolutionCondition, then q_l belongs to the
same question family.

## Same-question relation

q1 ~_J q2 iff:
1. their targets are continuation-equivalent for frozen job J;
2. each answer can be reconstructed from the other plus admitted shared basis;
3. their resolution conditions induce the same protected continuation classes;
4. differences are attributable only to representation, solver mathematics, search strategy,
   wrapper, or L36 projection.

This is stronger than name similarity and weaker than literal syntactic identity.

## Expansion relation

q1 <=_J q2 iff every licensed answer to q1 is a restriction/projection of an answer to q2 and
q2 contains at least one result-sensitive answer class not reconstructible from q1.

Use QUESTION_EXPANDED when q1 <= q2 and not q2 <= q1.

## Composite residual

For atom set S from one named tool:

HOR_J(S) = F_J(S) \ Cl_J(union_{P proper_subset S} F_J(P)).

Keep COMPOSITE_QUESTION only when HOR_J(S) is material.
Otherwise represent the historical tool as a package over its atomic question families.

## Search operator

QSearch(H_0):
  A_0 = union_{h in H_0} Atom(h)
  N_0 = Normalize36(A_0)
  Q_0 = N_0 / ~_J

  repeat:
    discover lineage artifacts touching unresolved split/merge/expansion edges
    atomize newly recovered states
    apply MT/MTA lineage comparison
    apply RTC lineage comparison
    apply Multi-Object residual test to apparent composites
    normalize 36 projections
    quotient same-question states
    preserve strict expansions and genuine composites
  until no new question class, lineage edge, or material OPEN is produced under recovered basis.

Compactly:

Q* = Fix(
       Quotient_~J(
         Normalize36(
           Atom(
             ExpandLineage(H)
           )
         )
       )
     )

subject to composite residual preservation.

## Transition labels

SPLIT
MERGE
SAME_QUESTION_NEW_MATH
SAME_QUESTION_STRONGER_SEARCH
36_PROJECTION
QUESTION_EXPANDED
QUESTION_NARROWED
COMPOSITE_QUESTION
WRAPPER_ONLY
ACTION_ONLY
GENUINELY_NEW_QUESTION

## Naming rule

Names attach only to final question-family equivalence classes.
Historical names remain aliases/provenance.
No current rename is canonical until its class survives the recovered-universe fixed-point pass.

## Current result

The first full recovered-universe pass yields 22 live question-family candidates.
This count is basis-relative, not a global theorem of completeness or minimality.
The accompanying run registry maps all C01-C49, major named tools, and N01-N10.
