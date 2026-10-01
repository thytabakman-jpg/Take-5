# PROSE Plain-Language Raise-the-Ceiling Mathematics 005

Date: 2026-10-01
Status: GREEN / FROZEN BEFORE IMPLEMENTATION
Controller: Raise the Ceiling / RTC (C48)
Tool: Prose
Parent:
- architecture/PROSE_ARCHITECTURE_READER_LOAD_MATHEMATICS_004_2026-09-30.md

## Preserved job

PROSE remains a protected reader-facing prose acceptance tool. It preserves
semantic content, earned claim strength, and no-inflation boundaries. It does
not decide factual truth, source validity, historical dates, or manuscript
macro-architecture, and it does not silently rewrite failed prose.

## New protected property

The target rule is:

> Use the simplest words that say exactly what you mean. Use technical terms
> only when simpler words would make the meaning less accurate or precise.
> Never make the writing harder just to make it sound more academic.

Let p be a prose realization and let Alt(p) be the set of admissible
reader-facing realizations that preserve the same frozen semantic content,
claim strength, qualifications, and required technical distinctions.

Let L(q) be reader burden for q. The rule selects a realization only inside the
semantic-equivalence class:

PlainLanguage(p) iff there is no q in Alt(p) such that
L(q) < L(p) while precision(q) = precision(p).

Equivalently, prose is admissible on this coordinate when no known simpler
wording preserves every required meaning and distinction.

## Accuracy priority

The admissible set is constrained before simplicity is compared:

Alt(p) = {
  q :
  SemanticPreservation(q) = PASS
  and EarnedClaimStrength(q) = PASS
  and NoUnsupportedInflation(q) = PASS
  and RequiredDistinctions(q) = PRESERVED
}.

Therefore simplicity never licenses loss of accuracy, qualification, technical
content, or logical structure.

## Operational contract

The protected constraint is:

PLAIN_LANGUAGE

A PLAIN_LANGUAGE assessment is evidence-gated rather than vocabulary-list
gated.

PASS requires concrete evidence that the wording is already the simplest known
realization that preserves the frozen meaning and required distinctions, or
that apparently harder technical terms are necessary for precision.

REPAIR_REQUIRED means a simpler known wording preserves the same meaning and
precision.

OPEN means the comparison has not been evidenced.

BLOCKED preserves a typed blocker.

Because this is a general prose rule rather than a project-specific option, PLAIN_LANGUAGE is part of the default ProseContract. A caller can still construct a narrower explicit contract when a task intentionally audits only selected coordinates.

The runtime does not ban long words, impose a readability-score threshold, or
replace technical vocabulary automatically. Those mechanisms can reward
inaccuracy and therefore fail the preserved-job test.

## Relationship to READER_LOAD

READER_LOAD asks whether the prose is cognitively difficult to process.

PLAIN_LANGUAGE asks a narrower comparative question: when a simpler wording
preserves the same meaning and precision, was the simpler wording used?

The two constraints remain distinct because prose can have low reader load
while still using needlessly academic vocabulary, and technical prose can have
high unavoidable reader load while still satisfying PLAIN_LANGUAGE.

## Raise-the-Ceiling candidate test

Candidate A: hard-coded forbidden-academic-word list.
Rejected because lexical difficulty is context-sensitive and some technical
terms are required for precision.

Candidate B: numerical readability threshold.
Rejected because the score can be improved by deleting required distinctions
or replacing precise terminology with weaker wording.

Candidate C: evidence-gated comparative PLAIN_LANGUAGE constraint.
Accepted because it adds the requested protection while preserving semantic
accuracy, claim strength, technical distinctions, and fail-open behavior.

Candidate D: fold the rule into READER_LOAD.
Rejected because it erases a distinct failure mode and weakens diagnosis.

Under C48, Candidate C is the strict-gain successor.

## New protected behavior

PROSE_PLAIN_LANGUAGE_GATE

## Strict-gain test

The successor preserves every prior protected Prose behavior and adds one
independent protected coordinate. No existing prose rule is weakened.

Mathematical color: GREEN.
