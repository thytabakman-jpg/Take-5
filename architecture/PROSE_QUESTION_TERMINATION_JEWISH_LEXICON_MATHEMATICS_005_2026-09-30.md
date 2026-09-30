# PROSE Question-Termination and Jewish Lexical-Form Mathematics 005

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Controller: ICC
Tool: Prose
Parent contracts:
- architecture/PROSE_PROTECTED_TRANSITION_MATHEMATICS_001_2026-09-30.md
- architecture/PROSE_FIRST_MENTION_PERSON_DATES_MATHEMATICS_002_2026-09-30.md
- architecture/PROSE_NUMERIC_YEAR_DATING_MATHEMATICS_002_2026-09-30.md
- architecture/PROSE_RAISE_CEILING_MATHEMATICS_003_2026-09-30.md
- architecture/PROSE_ARCHITECTURE_READER_LOAD_MATHEMATICS_004_2026-09-30.md

## Preserved job

PROSE remains a protected reader-facing prose acceptance tool. It evaluates concrete prose against a frozen contract. It does not decide factual truth, silently invent a transliteration standard, or rewrite failed prose.

## New defect 1: buried questions

A question may not be followed by ordinary prose in the same paragraph.

Let Paragraphs(p) be the ordered nonempty prose paragraphs obtained by blank-line separation after ordinary Markdown/HTML citation decoration is ignored for sentence termination.

For paragraph u, let SemanticText(u) remove trailing citation-only decorations such as a final `<sup>...</sup>` block while preserving ordinary lexical prose.

Define:

QuestionTerminal(u)
iff
- SemanticText(u) contains no question mark; or
- SemanticText(u) contains exactly one question mark and, after removing only terminal closing-quote / closing-delimiter / emphasis decoration, its final non-whitespace character is `?`.

The single question may constitute the whole paragraph or may be the paragraph's final sentence.

Therefore:
- "What follows?" passes.
- "\"What follows?\"" passes.
- "The paper asks one question. What follows?" passes.
- "What follows? The paper then answers it." fails.
- "What follows? Why?" fails because the first question did not terminate the paragraph.

Protected constraint:
QUESTION_TERMINATES_PARAGRAPH

Violation code:
QUESTION_BURIED_IN_PARAGRAPH

## New defect 2: Jewish lexical drift

PROSE cannot infer the correct spelling or transliteration convention for Jewish/Hebrew terms from general language-model priors.

The caller supplies a frozen Jewish lexical authority:

J = ((c_1,A_1),...,(c_n,A_n))

where:
- c_i is the canonical reader-facing form;
- A_i is a finite set of explicitly noncanonical aliases/variants that must not appear.

Define ExactTerm(p,t) as an occurrence of t whose adjacent characters, when present, are not word characters.

JewishLexicalOK(p,J)
iff
for every (c_i,A_i) in J,
no a in A_i occurs as ExactTerm(p,a).

The gate does not require a listed term to appear. It only rejects explicitly declared noncanonical forms.

If JEWISH_LEXICAL_FORMS is active and J is empty, the result is OPEN with:
JEWISH_LEXICON_REQUIRED

If the same alias is assigned to two different canonical forms, the result is OPEN with:
JEWISH_LEXICON_CONFLICT

Protected constraint:
JEWISH_LEXICAL_FORMS

Violation code:
JEWISH_TERM_NONCANONICAL

The violation carries the offending form and the required canonical form.

## Ownership boundary

QUESTION_TERMINATES_PARAGRAPH is a direct Prose surface rule because it is decidable from the concrete paragraph realization.

JEWISH_LEXICAL_FORMS is a Prose conformance gate, but lexical authority belongs to the project/caller. PROSE checks supplied authority; it does not invent it.

## Defaulting

QUESTION_TERMINATES_PARAGRAPH becomes part of the default Prose contract because the rule is global.

JEWISH_LEXICAL_FORMS remains explicit/contract-bound because non-Jewish projects have no Jewish lexical authority and because different projects may use different legitimate transliteration conventions.

## Strict-gain conditions

The successor Prose tool is admissible only when:

1. all existing protected constraints remain preserved;
2. default prose rejects a buried question;
3. a terminal question passes, including a question-only paragraph;
4. trailing citation-only markup after a terminal question does not create a false failure;
5. two questions in one paragraph fail;
6. JEWISH_LEXICAL_FORMS fails OPEN when no lexicon is supplied;
7. declared noncanonical Jewish forms fail with a repair-required violation;
8. canonical forms pass;
9. lexical alias conflicts fail OPEN;
10. no project-specific transliteration standard is hard-coded into the generic tool.

## Reentry

A REPAIR_REQUIRED result reenters after prose repair.
An OPEN lexical result reenters only after lexical authority is supplied or reconciled.
