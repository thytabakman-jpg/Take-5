# Question Lineage Audit 001

Date: 2026-09-25
Status: ACTIVE / REQUIRED BEFORE QUESTION-TOOL RENAMING
Scope: Reaserch -> Take-5 epistemic/question-tool lineage

## Core correction

Historical tool identity is not the audit unit.

A named tool may contain one, two, or several distinct inquiry nuclei.
Later MT/MTA, PD, Multi-Object, RTC/Raise-the-Ceiling, 36-scope/mode work, or architecture work may:
- split one named tool into several questions;
- merge previously separate names into one question family;
- preserve the same question while changing its mathematics;
- preserve the same question while changing only wrapper/runtime/closure;
- reveal that two questions are projections of one question under different scope/mode cells;
- expand the answer domain enough to create a genuinely broader question.

Therefore rename decisions must be made on atomic question lineages, not current tool names.

## Atomic question object

Q = <Issue,Target,AnswerSpace,Presuppositions,ResolutionCondition,ProtectedResult>

Two historical tool states h_i,h_j instantiate the same atomic question relative to job J when their issue/target/resolution condition are continuation-equivalent under the protected result, even when implementation, search strategy, wrapper, representation, or scope projection differs.

Candidate relation:

SameQ_J(q1,q2)
iff
IssueEq_J(q1,q2)
and TargetEq_J(q1,q2)
and ResolutionEq_J(q1,q2)
and ContinuationEq_J(q1,q2).

## Lineage edge types

SPLIT
One historical named tool contains multiple result-sensitive atomic questions later separated.

MERGE
Previously separate names reduce to one atomic question or one question family.

SAME_QUESTION_NEW_MATH
MT/MTA/Factor/PD changes representation or mathematical solution while preserving atomic question identity.

SAME_QUESTION_STRONGER_SEARCH
RTC/Raise-the-Ceiling expands candidate/successor/search space while preserving the atomic question.

QUESTION_EXPANDED
Later work materially broadens target, answer space, or resolution condition; old question embeds as a strict special case.

QUESTION_NARROWED
Later work isolates a subquestion that was previously bundled.

36_PROJECTION
Two apparent questions are one atomic question evaluated under different Scope x ModeFace projections.

COMPOSITE_QUESTION
A named tool deliberately couples multiple atomic questions whose joint answer is not reconstructible from isolated answers.

WRAPPER_ONLY
Change concerns execution, capture, persistence, verification, reentry, authority, or configured-run semantics, not the question.

GENUINELY_NEW_QUESTION
No continuation-equivalent predecessor question recovered.

## First confirmed lineage findings

### MTA
Historical/current MTA contains at least:
1 What is the mathematical structure/model of X?
2 What structure is unnecessary/reducible?
3 Does the reconstructed model preserve the protected job?
Configured repository MTA additionally contains closure/persistence obligations.

RTC-on-MTA explicitly preserved the mathematical core while strengthening MaterialDelta return and repository closure.
Disposition so far:
- core question lineage: SAME_QUESTION_NEW_MATH / possible historical SPLIT among structure, reduction, verification;
- repository closed-loop additions: WRAPPER_ONLY relative to Basic Math question.

### Multi-Object
Historical connector bundled:
- what relations exist among objects?
- what appears only jointly?
- does order matter?
- what arity/support is irreducible?
MTA reduced the distinctive nucleus to reconstruction-resistant interaction residual.
RTC replaced arity-first search with support-lattice search while preserving arity search as a special case.
Disposition:
- historical named tool: COMPOSITE_QUESTION;
- interaction-residual nucleus: SAME_QUESTION_NEW_MATH;
- pairwise/arity/scope variants may be 36_PROJECTION or search-strategy coordinates rather than separate questions;
- exact split/merge closure remains active.

### Goal Completion
MTA separated GoalSatisfied predicate from GoalCompletion control mechanism.
Raise-the-Roof expanded boolean completion toward terminal classification, obligation discharge, contract monitoring and trace satisfaction.
Disposition:
- boolean completion question was too narrow;
- obligation/contract completion is QUESTION_EXPANDED;
- control/reentry mechanism is not itself an inquiry question.

### Authority Activation
MTA isolated a governance-selection question over licensed/current/applicable goals.
Raise-the-Roof expanded from one-goal activation to governance frontier / episode constitution and also considered eliminating standalone tool status.
Disposition:
- narrow selector question embeds in broader governance-frontier question;
- kernel/control realization is WRAPPER/PLACEMENT, not a separate question.

### OrphanScan
Repeated MTA/RTC/MTOS expanded orphanhood from missing objects to requirement-relative failures involving relations, propagation, authority/currentness and canonical reachability.
Disposition:
- likely QUESTION_EXPANDED from object-orphan query to recovery/grounding query;
- forward/reverse scans are likely projections or complementary directions, not independent atomic questions.

## Audit algorithm

For every recovered named epistemic tool and every material iteration:
1. Extract all explicit and implicit inquiry nuclei.
2. Atomize bundled questions by result-sensitive target/answer/resolution differences.
3. Compare each atom to predecessor atoms.
4. Label each transition with one or more lineage edge types.
5. Map Scope x ModeFace differences before declaring new question identity.
6. Separate semantic-question changes from mathematics/search/wrapper changes.
7. Build equivalence classes of continuation-equivalent atomic questions.
8. Rename only final atomic question classes.
9. Keep historical tool names as aliases to the relevant class or composite.
10. Do not promote a rename while any material split/merge lineage remains OPEN.

## Naming consequence

QUESTION_TOOL_RENAME_REGISTRY_001 remains provisional.
Final names will be assigned to atomic question equivalence classes, not to historical tool packages.
