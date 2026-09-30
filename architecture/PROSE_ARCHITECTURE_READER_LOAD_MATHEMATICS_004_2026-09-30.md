# PROSE + ARCHITECTURE Reader-Load and Unit-Job Mathematics 004

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Controller: ICC
Wrapper: HF1
Targets: Prose, Architecture
Sequence: ASSERT -> PD + MT -> Architecture -> Raise the Ceiling -> HF1 reentry

## Observed regression

A Canonical Authority section contained this reader-facing unit:

> The paper therefore asks a deliberately narrow question: when canonical interpreters make incompatible truth-apt claims, what source-grounded basis, if any, can give a later evaluator warranted reason to favor one claim as true? The paper brackets four neighboring questions: which interpreter is greater, which view is legally binding, whether both views remain legitimate, and whether both belong within the tradition. Those questions can matter while leaving the truth question unresolved.

The existing PROSE tool could preserve semantics, earned strength, numeric-year rules,
affirmative-first rules, and supplied anchor order while still accepting prose whose
grammatical spine is buried under reader-processing load.

The existing Architecture tool could preserve the required result carrier and explicit
protected constraints while still accepting one paragraph that performs two different
reader-facing jobs: state the governing research question and delimit excluded questions.

## ASSERT result

The failure is real and decomposes into two non-identical ownership coordinates.

1. Prose owns realization-level reader load.
2. Architecture owns structural separation of rhetorical jobs.

Neither coordinate is equivalent to semantic correctness, claim strength, factual truth,
or anchor order.

## PD result

Let the result map be whether the reader-facing realization is admissible for publication
under a frozen contract.

Two perturbations can change that result without changing semantics:

- keep meaning and paragraph order fixed, but increase sentence processing load;
- keep every sentence fixed, but merge distinct rhetorical jobs into one paragraph.

Therefore both coordinates are result-sensitive.

They must remain distinct because a sentence can be locally clear inside a structurally
misassigned paragraph, and a paragraph can have one clean job while containing a locally
overloaded sentence.

## MT result

No reliable universal scalar can infer "clunky" prose from word count alone.

Accordingly the native tool does not pretend that length, punctuation count, or suffix
count is a sufficient semantic proxy for reader load.

Reader load is represented as an explicit evidence-bearing judgment with typed outcomes:

ReaderLoad in {PASS, REPAIR_REQUIRED, OPEN, BLOCKED}.

The evidence surface may cite concrete findings such as:

- buried grammatical spine;
- excessive simultaneous abstract referents;
- nested qualification load;
- avoidable nominalized phrasing;
- delayed arrival of the main proposition.

The Architecture environment similarly supplies explicit unit-job evidence rather than
inferring paragraph purpose from punctuation alone.

## PROSE extension

Add protected constraint:

READER_LOAD

For a prose candidate p and evidence E, define:

ReaderLoadOK(p,E)
iff
E.reader_load = PASS
and
E.reader_load_evidence is nonempty.

When READER_LOAD is active:

- PASS permits continuation;
- REPAIR_REQUIRED or FAIL yields REPAIR_REQUIRED;
- BLOCKED yields BLOCKED;
- OPEN or missing evidence yields OPEN.

This gate does not rewrite prose and does not replace semantic-preservation,
earned-strength, or no-inflation receipts.

## ARCHITECTURE extension

Add protected structural constraint:

UNIT_JOB_PURITY

Let U be the ordered set of reader-facing units under analysis.
For each u in U, the environment supplies a finite set Jobs(u) of primary rhetorical jobs.

UnitJobPure(u)
iff
|Jobs(u)| <= 1.

For an explicit exception set X supplied by the contract:

ArchitectureUnitJobOK(U,X)
iff
for every u not in X, UnitJobPure(u).

When UNIT_JOB_PURITY is protected, the Architecture result must supply
UnitJobState and explicit evidence. Missing state remains OPEN. Any unit with multiple
primary jobs is a violation and leaves the architecture OPEN until repaired.

For the observed Canonical Authority case:

- unit A job = STATE_RESEARCH_QUESTION
- unit B job = DELIMIT_SCOPE_EXCLUSIONS

Merging A and B violates unit-job purity when the project contract requires these jobs to
remain visibly distinct.

## Ownership boundary

PROSE answers:

Does this concrete sentence/paragraph realization impose avoidable reader-processing load
under the frozen prose contract?

ARCHITECTURE answers:

Are the reader-facing units divided so that each unit performs the structural job assigned
by the frozen architecture contract?

PROSE does not decide paragraph architecture.
ARCHITECTURE does not decide sentence-level smoothness.

## Raise-the-Ceiling strict-gain condition

Let B be the existing protected basis.

A successor pair (Prose', Architecture') is admissible only when:

1. every behavior in B remains preserved;
2. READER_LOAD is added without weakening semantic-strength-no-inflation controls;
3. UNIT_JOB_PURITY is added without collapsing Architecture into PROSE;
4. missing evaluator evidence fails OPEN rather than being guessed;
5. the exact observed regression is represented by tests;
6. no existing current tool identity is downgraded.

## HF1 closure

After implementation, HF1 reentry is relatively closed only when:

- the new PROSE coordinate has an execution witness;
- the new Architecture coordinate has an execution witness;
- regression tests cover PASS, REPAIR/OPEN, and missing-evidence states;
- the current tool manifest exposes both protected behaviors;
- the existing portfolio remains closed relative.

Any missing witness leaves the repair OPEN.
