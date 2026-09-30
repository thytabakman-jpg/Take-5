# PROSE Numeric-Year Dating Mathematics 002

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Controller: ImprovementCore
Tool: Prose
Parent mathematics: architecture/PROSE_PROTECTED_TRANSITION_MATHEMATICS_001_2026-09-30.md

## User rule

Historical dates in reader-facing prose use numeric year values.

Century labels are prohibited as dating substitutes.

Examples:

PASS
- 1040–1105
- c. 1075–1141
- fl. 1170–1190
- d. 1204

FAIL
- 12th century
- twelfth century
- 12th-century
- late twelfth century

## Object

Let (d) be a historical-date realization.

Let (Y(d)) be the set of explicit Arabic year-number tokens in (d).

Let (C(d)) be the set of century-label tokens in (d), including numeric-ordinal
and word-ordinal century forms.

Define:

[
NumericYearDate(d)
iff
|Y(d)|ge 1
land
C(d)=arnothing.
]

Qualifiers such as (c.), (fl.), (d.), before, after, and ranges do not
change admissibility so long as the temporal payload remains numeric years.

## Whole-prose gate

For candidate prose (p), let (D(p)) be the historical date expressions
governed by the active prose contract.

[
NumericYearDating(p)
iff
orall din D(p), NumericYearDate(d).
]

Any explicit century-label realization in reader-facing historical dating is a
protected-prose violation.

## Person-date integration

When FIRST_MENTION_PERSON_DATES is active, each configured person-date value
must satisfy NumericYearDate before it can be accepted.

Thus a contract entry such as:

[
(	ext{Person}, 	ext{"12th century"})
]

fails rather than being rendered.

An unresolved year remains OPEN. The tool must not invent a numeric year merely
to satisfy the format constraint.

## Default status

NUMERIC_YEAR_DATES_ONLY is a default protected PROSE constraint for this user's
reader-facing prose.

Its purpose is representational, not historical: it governs how an admitted date
is expressed. It does not authorize PROSE to determine a person's dates.

## Fail-closed behavior

Century label found:
REPAIR_REQUIRED.

Configured person date lacks any explicit Arabic year:
OPEN when the date is unresolved;
REPAIR_REQUIRED when a nonnumeric century substitute was supplied.

Unknown or disputed historical dates remain OPEN rather than guessed.

## Required implementation witnesses

- runtime/prose.py constant and audit;
- FIRST_MENTION_PERSON_DATES date-value validation;
- regression tests for numeric and word century labels;
- regression tests for valid numeric uncertainty formats;
- tool manifest protected behavior;
- configured-run protected behavior;
- Prose package decision/lesson record;
- whole portfolio validation remains closed.

## Anti-loss rule

Future prose tooling may add richer numeric uncertainty syntax, but no successor
may re-admit century-label dating without an explicit user-authorized contract
change and new mathematics.
