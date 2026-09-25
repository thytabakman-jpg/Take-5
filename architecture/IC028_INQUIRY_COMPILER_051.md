# IC-028 Question Compiler / Inquiry Architecture 051

Date: 2026-09-24
Controller: IC-028
Status: DESIGN DECISION

## Rewritten prompt

Turn the Tool-as-Question discovery into an executable inquiry architecture. Reuse existing root-translation mathematics instead of inventing a new formalism. Determine the smallest pipeline that can select high-value research questions, translate each question to a formal object, expand it through the 36 scope/mode challenge surface, inject PD where it adds discrimination power, route the resulting probes/tools, reconcile answers, and recursively generate the next questions. Test the pipeline on the current system and on an existing mathematical research problem without derailing the active architecture program. Route project-wide question compilation as autonomous handoff work.

## Core tool

Name candidate: INQUIRY COMPILER (IQC).

IQC(J,S,k) =
SelectQuestions
-> RootTranslate
-> PDEnrich
-> Expand36
-> ArchitectInquiry
-> ExecuteProbes
-> ReconcileAnswers
-> UpdateQuestionFrontier
-> Reenter.

### Question object

Q* = <Issue,Target,Scope,AnswerSpace,Presuppositions,SuccessCondition,Dependencies,ResultSensitiveCoordinates,Authority,StateLinks>.

RootTranslate(q,S) -> Q*.

This reuses TermMTA/root-translation machinery rather than creating separate translation mathematics.

## Question selection

"Most valuable" is not a scalar unless a scalar utility is licensed.

Question frontier:
QFrontier_k(S)=ND{q in CandidateQuestions(S):
 <GoalLeverage,DependencyUnlock,DiscriminationGain,UncertaintyReduction,TransferValue,Cost,Risk> }.

Return up to k nondominated high-leverage questions, preserving incomparability.

Architect/Goal-Architect can generate candidate questions from missing roles, unresolved interfaces, goal dependencies, OPEN coordinates, conflicts and completion blockers.

## Question x 36

For formal question Q*:

Q36(Q*) = {Probe(Q*,scope=s,mode=m): s in Scope6, m in ModeFace6}.

This is a 36-cell interrogative expansion, not 36 independent meanings.

For foundational/system questions pending 35-vs-36 ablation evidence:
default full 36 terminal coverage.

For local low-impact questions:
coverage policy may be adaptive.

## PD enrichment

PD is not pasted onto every question as decorative overhead.

PD(Q*) asks:
Which distinctions, hidden selectors, boundary choices, presuppositions or answer partitions can change the answer or continuation?

Define:
PDEnrich(Q*) -> <Q*',Distinctions,Selectors,RivalPartitions,OPEN>.

Then each admitted distinction can itself generate:
- revised question;
- subquestion;
- alternate answer space;
- additional 36 probes.

This makes PD a question-refinement operator inside IQC.

PD36 already exists semantically:
PD36={Run(PD | scope=s,modeface=m)}.
It is 36 challenge cells, not 36 PD primitives.

## Architect's question role

Architect does not simply pick three questions by taste.

Goal-Architect + Workflow Architect produce the inquiry frontier.
For compact runs, k=3 is a useful configured budget:
Top3Inquiry(S)=any nondominated three-question cover maximizing distinct dependency/discrimination coverage without forced scalar ranking.

For strong research runs, preserve the wider nondominated frontier.

## Existing math-project test

Use the current native-tool-use / executable-package problem as test question:

q_math:
"When does pointwise executable admissibility of capabilities imply executable admissibility of their joint package, and what additional conditions are required when it does not?"

Root translation:

Let P={c_1,...,c_n}.
Known:
forall c in P, ExecAdm(c).

Target:
conditions C such that
[(forall c in P ExecAdm(c)) and C(P,S,A,R)] => ExecAdm(P).

Candidate obstruction coordinates:
order/noncommutation;
shared resource conflict;
authority incompatibility;
carrier/type incompatibility;
state-version assumptions;
failure/retry semantics;
return-edge compatibility;
interaction residuals.

Question form immediately clarifies the math:
find necessary/sufficient package-closure conditions, counterexamples, and minimal C.

Q36 then interrogates this at System/Subsystem/Component/Interface/Boundary/Cross-Layer x Expand/Contract/Inward/Outward/Isolate/Couple.

This does not solve the theorem by itself, but it converts the OPEN into a structured proof/research program.

## Cross-project automation

Create ProjectQuestionCompilation handoff:
for every active research project with explicit/implicit research questions:
1 inventory questions;
2 RootTranslate;
3 build dependency/inquiry graph;
4 PDEnrich material questions;
5 map probes/tools;
6 persist QuestionFrontier;
7 return only authority/value/goal ambiguity or material OPEN to user.

Jane tracks stale/uncompiled QuestionFrontiers.
IC028 schedules IQC under existing authority.
Routine compilation does not require user involvement.

## Architecture consequence

The tool map and question map become two projections of one inquiry system:

QuestionGraph --selects--> Probe/ToolGraph
Probe/Tool results --answer/update--> QuestionGraph.

Potential fixed point:
S_t -> Q_t -> T_t -> Evidence_t -> Reconcile -> S_(t+1) -> Q_(t+1).

This is a stronger candidate system loop than ToolGraph alone.

## Decision

1 Build IQC as configured composite, not new kernel primitive.
2 Reuse root-translation/TermMTA mathematics.
3 Use Goal-Architect to generate/select inquiry frontier.
4 Embed PD as question refinement.
5 Expand foundational questions to full Q36 pending empirical ablation results.
6 Use existing math OPEN as first proof fixture.
7 Route cross-project question compilation to Jane/IC028 handoff so it does not interrupt current architecture work.
