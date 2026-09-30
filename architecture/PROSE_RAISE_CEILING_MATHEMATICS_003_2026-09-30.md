# PROSE Raise-the-Ceiling Mathematics 003

Date: 2026-09-30
Status: FROZEN BEFORE IMPLEMENTATION
Parents:
- architecture/PROSE_PROTECTED_TRANSITION_MATHEMATICS_001_2026-09-30.md
- architecture/PROSE_NUMERIC_YEAR_DATING_MATHEMATICS_002_2026-09-30.md
- architecture/PROSE_FIRST_MENTION_PERSON_DATES_MATHEMATICS_002_2026-09-30.md
Controller: Raise the Ceiling / RTC
Tool: Prose

## Preserved job

PROSE remains a protected reader-facing prose acceptance tool. It does not
decide factual truth, source validity, historical dates, or manuscript macro
architecture, and it does not silently rewrite failed prose.

## Defects localized by the ceiling run

Three owned defects are material.

1. The runtime contained two definitions of
   `audit_first_mention_person_dates`, creating a silent divergence surface.

2. The exact-name boundary regex used escaped backslashes
   (`(?<!\\w)` / `(?!\\w)`) rather than word-character boundaries
   (`(?<!\w)` / `(?!\w)`). A protected person name could therefore be
   detected inside a larger word.

3. The older first-mention mathematics gave `fl. 12th century` as an example,
   while the later numeric-year mathematics prohibits century labels. Under the
   current combined contract, the numeric-year rule controls. The contradiction
   is resolved here without rewriting historical artifacts.

## First-mention exactness

For protected display name n in prose p, let ExactMention(p,n) be an occurrence
whose immediately adjacent characters, when present, are not word characters.

```
FirstExact(p,n) = min position of ExactMention(p,n)
```

Only FirstExact is eligible for FIRST_MENTION_PERSON_DATES.

A substring embedded inside a larger token is not a mention.

## Numeric-year precedence

When NUMERIC_YEAR_DATES_ONLY and FIRST_MENTION_PERSON_DATES are both active:

```
FirstMentionDateOK(p,N)
requires
NumericYearDate(d_i)
for every mentioned (n_i,d_i) in N.
```

Therefore century-label date strings remain inadmissible even when an older
historical artifact listed one as a placement-format example.

## Ordered-anchor protection

PROSE gains one generic, explicit ordering constraint:

```
ORDERED_ANCHORS
```

A contract may supply an ordered tuple A=(a_1,...,a_n) of exact reader-facing
anchors. Let pos_p(a_i) be the selected occurrence position in p.

```
OrderedAnchors(p,A)
iff
all anchors occur
and
pos_p(a_1) < ... < pos_p(a_n).
```

Missing anchors or out-of-order anchors give REPAIR_REQUIRED.

The tool does not infer which anchors matter. The project or caller supplies
them from a frozen manuscript/paragraph/sentence-order contract. This protects
known macro or local order without giving PROSE authority to invent structure.

## New protected behavior

```
PROSE_ORDERED_ANCHOR_GATE
```

## Strict-gain test

The successor is admissible because it:
- preserves AFFIRMATIVE_FIRST;
- preserves FIRST_MENTION_PERSON_DATES;
- preserves NUMERIC_YEAR_DATES_ONLY;
- preserves semantic-strength-no-inflation receipts;
- removes duplicate runtime authority;
- fixes exact-name matching;
- resolves the date-format precedence conflict;
- adds an opt-in objective order lock without inferring new user preferences.

No existing protected constraint is weakened.
