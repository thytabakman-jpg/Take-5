# PROSE First-Mention Person Dates Mathematics 002

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Parent: architecture/PROSE_PROTECTED_TRANSITION_MATHEMATICS_001_2026-09-30.md

## Job

When a prose contract marks person dates as protected, every named person in the supplied person-date inventory must carry the supplied date string at that person's first occurrence.

Later occurrences do not require repetition.

## Object

Let (p) be prose.

Let (N={(n_i,d_i)}) be the supplied person-date inventory, where:

- (n_i) is the exact display name expected in the prose;
- (d_i) is the source-grounded date string to display.

Let (First(p,n_i)) be the first exact name occurrence.

Let (AdjacentDate(p,n_i,d_i)) mean the first occurrence is immediately followed by the parenthetical date string.

Define:

[
FirstMentionDateOK(p,N)
iff
orall (n_i,d_i)in N:
ig(
Mentioned(p,n_i)
Rightarrow
Known(d_i)land AdjacentDate(p,n_i,d_i)
ig).
]

Unknown or unresolved dates do not license guessing.

[
Mentioned(p,n_i)land 
eg Known(d_i)
Rightarrow OPEN.
]

Known date but missing first-mention parenthetical gives REPAIR_REQUIRED.

## Examples

PASS:

Rashi (1040–1105) reads the opening as a dependent construction. Rashi then supports the reading grammatically.

PASS:

Ramban (1194–1270) rejects that grammatical analysis.

OPEN:

A person is in the protected inventory and appears in the prose, but the supplied date string is empty or unresolved.

REPAIR_REQUIRED:

Rashi reads the opening as a dependent construction. Later, Rashi (1040–1105) explains...

The date belongs at the first occurrence.

## Boundary

PROSE validates placement and supplied display text.

PROSE does not independently establish historical dates. Date truth and sourcing remain external evidence obligations.

The prose contract may use approximate or floruit forms such as:

- c. 1040–1105
- fl. 12th century
- b. 1980

when those strings are supplied by the source-grounded project state.

## Protected behavior

New protected behavior:

PROSE_FIRST_MENTION_PERSON_DATES

The behavior is active only when the prose contract explicitly requests FIRST_MENTION_PERSON_DATES.
